---
layout: post
title: "DeepSeek 開源 DeepInfer：repo 開的是引擎，部署文件開的是調度，每卡每小時 38 美元的那一層只給了設計圖"
date: 2026-10-20 09:00:00 +0800
permalink: /deepseek-deepinfer-open-source-inference-design/
tags: [DeepSeek, DeepInfer, V4.1-Flash, 推理框架, inference, KV cache, 3FS, EPLB, Wide-EP, DSpark, 開源]
categories: [AI 前沿技術]
image: /assets/images/deepseek-deepinfer-design-cover.png
description: "DeepSeek 在 10 月 20 日以 Apache-2.0 開源 DeepInfer，官方說它撐著單一集群每天 155 兆 token、按離峰價每卡每小時 38 美元營收的 V4.1 Flash 服務。但 README 寫明 KV cache 系統、Prefill／Decode 分離、跨副本負載平衡三樣不在 repo 裡。這篇拆官方文件裡沒開 code、但寫到參數級的 load balancer 與 3FS KV cache 設計，特別是 prefill 完全不做 cache-aware 路由這個選擇，再算這套經濟學對 128 卡以下的部署者還剩多少。"
author: Wisely Chen
faq:
  - question: "DeepInfer 沒有開源哪些東西？"
    answer: "DeepSeek 在 2026 年 10 月 20 日以 Apache-2.0 開源的推理框架（Inference Framework）DeepInfer，README 列出三樣不在 repo 裡：KV cache 系統、Vision Encoder／Prefill／Decode 分離架構（PD Disaggregation）、跨資料平行（Data Parallel）副本的負載平衡。官方說這些跟內部基礎設施耦合太深，但設計細節寫在知乎長文《DeepSeek V4.1 Flash 大規模推理部署實踐》和 repo 內的 `doc/inference_deployment_qa.md`。這三樣正是 DeepSeek 自報 96% 輸入快取命中率背後的關鍵。"
  - question: "為什麼 DeepSeek 的 prefill 不做快取感知路由（cache-aware routing）？"
    answer: "因為 block KV cache 放在獨立的 3FS 分散式儲存集群（約 100 PiB SSD），而不是 prefill 機器本機，任何一台 prefill 機器都能命中任何前綴。這樣可以避免前綴親和路由（Prefix-Affinity Routing）和負載平衡互相衝突，路由只需要依各引擎剩餘的 compute quota 分配工作。代價是需要大型共用儲存層，官方的配置是每張 GPU 約 14.4 TB 邏輯儲存。"
  - question: "自架 DeepSeek V4.1 Flash 至少要幾張卡才能用上這套設計？"
    answer: "官方說 1 個 prefill 加 1 個 decode 實例就能跑，兩邊卡數約 1:1。但 decode 建議用 EP64 以上的寬專家平行（Wide Expert Parallelism），所以最小「高效」單元是 64 卡 prefill 加 64 卡 decode，共 128 卡；prefill 本身只用 EP2–8。另外 DSpark 投機解碼（Speculative Decoding）在每 rank 16 條序列時是 −1.5%，96 條時才有 +11.0%。一兩台 8 卡機的團隊用得到引擎優化，但用不到 Wide-EP 和高併發那一段的效益。  ---"
---

DeepSeek 今天把 DeepInfer 開源了。

官方貼文說它是「our in-house inference framework, now fully open source」。README 第三段寫的是另一件事：KV cache 系統、Vision Encoder／Prefill／Decode 分離、跨 DP 副本的負載平衡，三樣不在 repo 裡。

沒放進 repo 的那三樣，剛好是決定毛利的那三樣。

<nav class="post-toc" markdown="1">
**目錄**

* 目錄
{:toc}
</nav>

---

## 30 秒定位

| 項目 | 內容 |
|------|------|
| 發布日 | 2026 年 10 月 20 日 |
| 授權 | DeepInfer：Apache-2.0；同日開源的 deepseek-recipe：MIT |
| 範圍 | 目前只支援 V4.1 Flash，只提供離線推理；主要基於 vLLM |
| 硬體 | NVIDIA SM100 與華為昇騰 950 |
| 官方自報 | 單一集群每天 155 兆 token，按離峰價算，每張卡每小時營收 38 美元 |
| 設計文件 | 知乎長文《DeepSeek V4.1 Flash 大規模推理部署實踐》＋ repo 內 `doc/inference_deployment_qa.md` |

X 上做推理的 susun（[@SuJinYan123](https://x.com/SuJinYan123/status/2112485918527590435)）一句話定調：

> 「感觉 git repo 本身，对我们这样研发来说意义不太大，有一点点吧，但是好些东西没开。」
>
> 「精华本身在 zhihu 那篇文章，这篇文章很有价值」

這篇照這個判斷走：repo 簡單帶過，重點拆那兩份文件。

---

## repo 裡有的：一個單模型引擎

功能列包含最佳化 kernel、Attention DP、MoE EP + EPLB、DSpark 投機解碼、SWA bounded replay、非同步排程、結構化輸出。官方說之後新模型的推理碼也會放進同一個 repo。

有一個差距官方自己寫了：開源版 FlashMLA 少一個手調的 SASS 優化，decoding kernel 慢 5% 到 10%，端到端最多差 5%。

---

## 沒開 code 的：load balancer

attention 用 data parallelism，MoE 用 expert parallelism，任何一個副本負載不均，最慢的那張卡就決定整組速度。所以 DeepSeek 做了四個 load balancer，最值得看的是 prefill 這個。

### Prefill：分桶，然後不看快取

請求先依總 context 長度分成 4 檔：<16K、16K–64K、64K–256K、≥256K，每檔分到幾台引擎依上一輪需求動態重分。DP 組之間，引擎依剩餘 compute quota 主動拉工作。然後是整份文件最關鍵的一句：

> "Since any engine can hit any prefix, there is no prefix-affinity routing."

任何引擎都能命中任何前綴，所以不做前綴親和路由。

susun 的讀法是「不做任何的 cache aware，靠池化兜底」。KV cache 不放在 prefill 機器本機，而是放在所有機器共用的 3FS 儲存池。如果快取放本機，路由就得把同一段前綴送回同一台機器，負載平衡和快取命中會互相拉扯。**把快取抽成共用池，路由就只需要管負載。** 這是拿儲存換掉路由複雜度。

到單張卡，chunk size 不固定，而是給每一步一個時間預算，用擬合的二次成本模型 `cost(q, c)` 反推這一步能塞多少 token，上限 32,768。susun 說他自己也做過同樣的東西：先離線量成本曲線，線上反推。

### 其他三個 balancer

- **Decode**：同時平衡請求數和 KV cache 總長。短請求給併發低但 KV 長的卡，長請求給 KV 短的卡。
- **EPLB**：每卡多放冗餘位置裝熱門專家副本，prefill 每卡 4 個、decode 每卡 1 個，定期依統計重新分配。decode 實測 moe_lb 1.090，最慢的卡比平均慢 9%。prefill 的 moe_lb 知乎寫 1.0618／1.0320，repo Q&A 寫 1.074／1.045，兩份官方文件對不上，差約 1 個百分點。
- **擴縮容**：prefill 依非快取 token 數、decode 依 running requests 調整；quota 使用率高於 0.8 禁止縮容。

四個加起來，官方說大約達到完美均衡離線 benchmark 的 80%。

---

## KV cache：3FS 和兩種壽命的快取

依知乎長文的線上統計（轉載數字），平均輸入命中率 96%，同一張卡 prefill 不命中每秒約 6 萬 token，命中約 150 萬，差 25 倍。96% 是整套經濟學的地基，地基是這樣蓋的：

block KV cache 放在獨立的 3FS 集群，約 100 PiB 的 SSD，每張 GPU 配約 14.4 TB（邏輯大小），10+2 erasure coding。TTL 是 agent 流量 3 天、chatbot 流量 7 天。計算節點的故障率比儲存節點高一個數量級以上，快取跟計算脫鉤，機器掛了快取還在。

TTL 這段要讀仔細。susun 寫的是：

> 「kv cache 呢就是 3fs，然后 3天的 ttl，能换到 0.5 - 1% 的命中率。」

原文的意思更具體：chatbot 的命中長尾很重，如果也只留 3 天，命中率會掉 0.5% 到 1%。這是從 3 天延長到 7 天多換到的命中率，不是 3 天 TTL 本身換到的。

他另一個猜測「kv cache 管理由 decode 主导？这样输出也能被 hit」是對的。原文寫「Block KVCache 由 decode 实例落盘存储，使得 prefill 和 decode 输出均被复用」。

換入 HBM 的那一段，原文的關鍵句是：

> "Because the CUDA copy engine performs poorly on the fine-grained copies of KV cache blocks, swap-in is implemented with GDR: an RDMA NIC saturates PCIe bandwidth without consuming SMs."

搬細碎的 KV block 不佔 GPU 運算單元，只有在大量換入的規模才需要這種設計。

另一層 SWA KVCache 剛好相反：完全不落盤，留在產生它的機器記憶體裡，線上 TTL 約 180 秒，命中率 98% 以上。V4 曾經把它也落盤，結果佔去持久快取近一半容量；V4.1 改成沒命中就只重算最近 128 個 token。**能活幾天的資料放 SSD，只活幾分鐘的資料寧可重算。**

---

## DSpark：真的上線了，但看併發

draft model 一次猜 5 個 token，DSpark 用 Confidence Head 預測接受率，只驗證邊際收益最高的那一段。每步驗證 token 從 5.00 降到 3.2–4.4，接受長度幾乎不變，知乎給的線上吞吐提升是 +6%。

但官方表格的另一半同樣重要：

| 每 rank 併發序列數 | 吞吐變化（vs 固定驗證 5 個） |
|------|------|
| 16 | **−1.5%** |
| 32 | +1.6% |
| 60 | +5.4% |
| 96 | +11.0% |

併發低的時候，DSpark 是負收益。

---

## 修正八月那篇

我 8 月寫 [DeepSeek V4 Flash 的 disk KV cache](/deepseek-v4-flash-disk-kv-cache-50x-economics/) 時下了兩個結論：「功能能抄，經濟學抄不動」，以及「這不是護城河，是產業的新地板」。

第一句被強化了。3FS、每卡 14.4 TB、7 天 TTL 是一整套儲存基礎設施，不是 feature flag。8 月時官方只說快取保留「幾小時到幾天」，今天變成具體的 3 天和 7 天。

第二句要修正。地板的設計開了，程式碼沒開，而且沒開的剛好是最難重做的那一層。khazzz1c（[@Chonghan_Liu](https://x.com/Chonghan_Liu/status/2112521832696041720)）的判斷一樣：最貴也最重要的是 KV cache 和命中快取，這兩塊沒開，雲廠商搬不走 DeepSeek 的大部分優勢。**DeepSeek 開源了怎麼做，保留了做好的那一份。**

---

## 反方：中小部署該不該學 EP

susun 的架構質疑：

> 「总的来说在中小部署我看好 pp（几个 prefill worker 这种），大部署我才看好 ep。」

文件有個細節讓這題變窄：DeepSeek 自己的 prefill 只用 EP2–8，是「HBM 允許的最小值」；大 EP 在 decode 側，EP64–128。所以官方說 P 和 D 卡數約 1:1，最小「高效」單元是 64 卡 prefill 加 64 卡 decode。

我的回應：EP 的規模門檻在 decode，不在 prefill。susun 的結論在 decode 側成立；prefill 該用 PP 還是小 EP，文件沒討論 PP，回答不了。

---

## 手上只有 16 張卡的團隊

台灣企業自架 V4.1 Flash 的典型情境是一兩台 8 卡機。

| | 看到新聞時 | 讀完文件後 |
|---|---|---|
| 成本 | 自架也能接近官方 API | 最小高效單元 128 卡，16 卡是它的八分之一 |
| DSpark | 直接開 | 每 rank 16 條序列時是 −1.5%，先量併發 |
| KV cache | 照抄 96% | 背後是獨立 3FS 和 3 到 7 天 TTL，repo 裡沒有 |
| 硬體 | 現有 GPU 能跑 | 只支援 SM100 和昇騰 950 |

---

## 坦白說

- **線上統計是二手數字。** 96%、6 萬對 150 萬在知乎原文是一張圖表，我取自新智元轉載與 Zhihu Frontier 摘要，兩方一致，但沒直接核對那張圖。設計細節來自知乎原文與 repo Q&A，是一手。
- **效能都是 DeepSeek 自報。** 目前沒有第三方 benchmark。38 美元是營收不是利潤，按離峰價算，不含折舊。X 上有人自測說比 SGLang、vLLM 快三到五倍，但那是個人測試，比的又是單模型引擎對通用框架。
- **我沒逐行讀 code。** 文件說的設計有多少已在開源程式碼裡，本文沒驗證。

但它做對了一件事：沒開 code 的部分，用文件把參數寫出來，連 DSpark 的負收益、開源版 kernel 比內部版慢多少都附上。這比一句「fully open source」有資訊量。

---

## 關鍵洞察

1. **讀 DeepInfer 先讀部署文件，再讀 code。** 決定毛利的兩層不在 repo 裡，但設計和參數在文件裡。
2. **「不做 cache-aware 路由」可以借，前提是你有共用儲存層。** 沒有的話，cache-aware 路由仍然比較實際。
3. **先量併發，再決定要不要開變長驗證。** 16 條序列 −1.5%，96 條 +11.0%，同一個功能正負號會變。

---

## 常見問題 Q&A

**Q: DeepInfer 沒有開源哪些東西？**

DeepSeek 在 2026 年 10 月 20 日以 Apache-2.0 開源的推理框架（Inference Framework）DeepInfer，README 列出三樣不在 repo 裡：KV cache 系統、Vision Encoder／Prefill／Decode 分離架構（PD Disaggregation）、跨資料平行（Data Parallel）副本的負載平衡。官方說這些跟內部基礎設施耦合太深，但設計細節寫在知乎長文《DeepSeek V4.1 Flash 大規模推理部署實踐》和 repo 內的 `doc/inference_deployment_qa.md`。這三樣正是 DeepSeek 自報 96% 輸入快取命中率背後的關鍵。

**Q: 為什麼 DeepSeek 的 prefill 不做快取感知路由（cache-aware routing）？**

因為 block KV cache 放在獨立的 3FS 分散式儲存集群（約 100 PiB SSD），而不是 prefill 機器本機，任何一台 prefill 機器都能命中任何前綴。這樣可以避免前綴親和路由（Prefix-Affinity Routing）和負載平衡互相衝突，路由只需要依各引擎剩餘的 compute quota 分配工作。代價是需要大型共用儲存層，官方的配置是每張 GPU 約 14.4 TB 邏輯儲存。

**Q: 自架 DeepSeek V4.1 Flash 至少要幾張卡才能用上這套設計？**

官方說 1 個 prefill 加 1 個 decode 實例就能跑，兩邊卡數約 1:1。但 decode 建議用 EP64 以上的寬專家平行（Wide Expert Parallelism），所以最小「高效」單元是 64 卡 prefill 加 64 卡 decode，共 128 卡；prefill 本身只用 EP2–8。另外 DSpark 投機解碼（Speculative Decoding）在每 rank 16 條序列時是 −1.5%，96 條時才有 +11.0%。一兩台 8 卡機的團隊用得到引擎優化，但用不到 Wide-EP 和高併發那一段的效益。

---

## 延伸閱讀

- [DeepInfer GitHub repo](https://github.com/deepseek-ai/DeepInfer)
- [DeepSeek V4.1 Flash Inference Deployment Q&A（repo 內文件）](https://github.com/deepseek-ai/DeepInfer/blob/main/doc/inference_deployment_qa.md)
- [DeepSeek V4.1 Flash 大規模推理部署實踐（知乎，需登入）](https://zhuanlan.zhihu.com/p/2095560295930508953)
- [susun 的 DeepInfer 推理側銳評（X）](https://x.com/SuJinYan123/status/2112485918527590435)
- [DeepSeek V4 Flash 0731 為何那麼強：disk KV cache 與 50 倍價差（本 blog）](/deepseek-v4-flash-disk-kv-cache-50x-economics/) — 本文修正的那篇
- [DeepSeek V4.1-Flash-1017：官方說是小更新（本 blog）](/deepseek-v41-flash-1017-open-source/)
