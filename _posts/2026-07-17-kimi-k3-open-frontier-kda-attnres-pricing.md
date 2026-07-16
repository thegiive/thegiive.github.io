---
layout: post
title: "Kimi K3 登場：2.8T 參數、十天後開源，但真正的訊號是它悄悄退出了中國價格戰"
date: 2026-07-17 09:00:00 +0800
permalink: /kimi-k3-open-frontier-kda-attnres-pricing/
image: /assets/images/kimi-k3-aa-intelligence-index-cover.png
description: "Moonshot 7/16 發布 Kimi K3：2.8T 參數、1M context，7/27 前開源權重。24 小時內定位立起三根柱子：Frontend Code Arena 以 1,679 分登頂、把 Claude Fable 5 壓到第二；Artificial Analysis 獨立測得 57 分，coding/agent 進第一梯隊、只落後 Fable 5 和 GPT-5.6 Sol；加上原生 vision，權重釋出後它會是開源陣營最強的多模態模型。這篇拆 KDA 如何走出百萬上下文的第二條路線、cost per task $0.94 如何宣告退出中國價格戰，以及 2.8T 的『開源』對你的實際意義。"
---

Kimi K3 發布後幾個小時，[Arena.ai 的 Frontend Code Arena](https://x.com/arena/status/2077824029126504525) 榜首換人了：K3 以 1,679 分登頂，Claude Fable 5（1,631）退到第二，七個 domain 裡拿下六個第一。上一代 K2.6 在同一個榜上排第 18——一個版本跳了 17 名。

這是 [Moonshot 7 月 16 日發布的 Kimi K3](https://www.kimi.com/blog/kimi-k3)：2.8T 參數、1M token context、原生多模態，承諾 7 月 27 日前釋出完整權重，屆時它會是史上最大的開放權重模型。官方對整體能力的自我評價很誠實：

> "While its overall performance still trails the most powerful proprietary models, Claude Fable 5 and GPT 5.6 Sol, Kimi K3 demonstrated frontier-level performance across our evaluation suite, consistently outperforming other tested models."

發布 24 小時內，K3 的定位立起了三根柱子。**第一，coding 和 agent 進了第一梯隊**：整體只落後 Fable 5 和 GPT-5.6 Sol，穩定贏過包括 Opus 4.8 在內的其他所有受測模型——這不只是官方說法，第三方隔天就驗證了（見下）。**第二，前端直接登頂**，連 Fable 5 都被壓過。**第三，它會是開源陣營裡最強的多模態模型**：GLM-5.2 是純文字，DeepSeek V4 Pro 有 vision 但智力差一個級距。三根柱子疊起來，就是這篇要拆的東西：架構怎麼做到的、定價在說什麼、2.8T 的開源對你的實際意義是什麼。

---

## 30 秒定位

| 項目 | 內容 |
|------|------|
| 規模 | 2.8T 總參數，MoE：896 個 experts、每 token 激活 16 個（激活量未公布） |
| Context | 1M tokens，原生多模態輸入（影像＋文字進、純文字出） |
| 核心架構 | Kimi Delta Attention（KDA）+ Attention Residuals（AttnRes） |
| 效率宣稱 | 1M context decoding 最高快 6.3 倍；對 K2 scaling efficiency 約 2.5 倍 |
| 定價 | $0.30/M（cache hit）、$3.00/M（cache miss）、$15.00/M（output） |
| 開源 | 完整權重 2026-07-27 前釋出 |
| 第三方 | AA Intelligence Index 57（僅次 Fable 5、GPT-5.6 Sol）；Frontend Code Arena 第 1 |

---

## Benchmark：長程任務是主場，第三方隔天就驗證了

官方表格三十幾格，有資訊量的是模式：**贏的格子集中在長程、多步、真實工作流；輸的格子集中在單點智力上限。** 長程軟體工程的 SWE Marathon，K3 拿 42.0 全場第一（Fable 5 是 35.0、Opus 4.8 是 40.0，GPT-5.5 只有 14.0）；BrowseComp 91.2、OmniDocBench 91.1 也都是第一。反過來，HLE-Full 43.5 對 Fable 5 的 53.3 差了近 10 分，FrontierSWE 81.2 對 86.6——純智力上限的差距，短期堆不出來。

發布隔天，[Artificial Analysis](https://artificialanalysis.ai/models/kimi-k3) 放出獨立評測（Intelligence Index v4.1，綜合九項評測）：

| 模型 | AA Intelligence Index |
|------|----------------------|
| Claude Fable 5 | 60 |
| GPT-5.6 Sol | 59 |
| **Kimi K3** | **57** |
| Claude Opus 4.8 | 56 |
| GLM-5.2 | 51 |
| DeepSeek V4 Pro | 44 |
| Kimi K2.6 | 44 |

兩件事值得注意。第一，排序跟官方自我評價完全一致——廠商說自己第三，獨立評測方測出來也是第三。**這種對齊比高分本身更少見。** 第二，世代跳幅：K2.6 到 K3 一代跳了 13 分；AA 的長時程知識工作評測 AA-Briefcase，K3 比 K2.6 高 732 Elo、僅次於 Fable 5；AutomationBench-AA 直接拿第一。「長程 agentic 是主場」，官方和第三方數據給了同一個答案。

不過 AA 也量到一個張力：K3 的輸出速度只有 62 tokens/s，189 個模型裡排第 90。KDA 的 6.3 倍加速是 1M context 下的相對值，讓超長上下文「變得可行」，不代表日常用起來快。

一句話總結：**K3 不是要當最聰明的模型，是要當跑得最久的模型。**

---

## KDA：打百萬上下文的第二條路線

三個月前我拆過 [DeepSeek V4 的 CSA + HCA](/deepseek-v4-million-token-csa-hca-attention/)：百萬上下文的兩個天花板是訓練端 O(n²) 和推理端 KV Cache 爆炸，DeepSeek 的解法是**稀疏化**——讓模型只對挑出來的重點 token 算 full attention。

Kimi 走另一條路：**線性化**。KDA 出自 2025 年 10 月的 [Kimi Linear 論文](https://arxiv.org/abs/2510.26692)，本質是把「每個 token 回頭看所有歷史」改成「把歷史壓縮進固定大小的狀態，邊讀邊更新」——計算量變 O(n)，KV Cache 不再隨長度膨脹。代價是固定大小的記憶會忘東西，所以採 hybrid 設計：每三層 KDA 配一層 full attention。論文在 48B 規模驗證：KV Cache 減 75%、decoding 最高快 6 倍、品質不輸 full attention。K3 做的事就是把它放大到 2.8T。

類比：full attention 像 `git log -p`，每次攤開完整歷史，精確但越來越慢；KDA 像只保留固定大小 summary 的 changelog，永遠一樣快但細節會被壓縮。Hybrid 等於平常看 changelog，每隔幾步准你跑一次 `git log -p` 對答案。

同樣面對 1M context，DeepSeek 賭「重點只有一小部分」，Kimi 賭「歷史可以壓縮」。**O(n²) 這面牆現在至少有兩個方向的裂縫。** 至於另一個新元件 AttnRes（讓深層選擇性取回淺層表示，宣稱訓練效率 +25%、額外成本 <2%），目前只有官方單一來源，細節要等技術報告。

---

## 定價的弦外之音：Kimi 退出了價格戰

這是整場發布最被低估的訊號。

上週[高盛那份中國 AI 報告](/goldman-sachs-china-ai-moe-token-price-war-agent-coding/)的敘事是：中國頭部模型把混合 token 價格壓到約 $1/M（美國 SOTA 是 $4-8），虧損定價換到 OpenRouter 上 85% 的 agent token。Kimi 自己的 K2.5 就是樣板——我[二月測它](/kimi-k2-5-agent-swarm-deep-dive-technical-assessment/)的結論是「沒有明顯降級感，價格便宜 3-5 倍」。

K3 的 output 定價 $15/M，是那個 $1 世界的十五倍。

而且往上走的路 GLM 已經先走了一段：[GLM-5.2 官方 API 是 $1.40/$4.40](https://felloai.com/glm-pricing/)，output 單價約為 DeepSeek 的五倍。AA 的 cost per task 把階梯排得很清楚：**DeepSeek $0.04 → GLM-5.2 $0.32 → K3 $0.94 → GPT-5.6 Sol $1.04 → Opus 4.8 $1.80。** K3 的定價鄰居不是中國同行，是美國一線閉源模型，而且是 Opus 4.8 的一半。單 token 貴了（K2.6 的 output 是 $4）、單任務卻有競爭力，中間差的是 token 效率：AA 測到 K3 比 K2.6 少用 21% 的 output tokens，分數還更高。

所以高盛報告需要加註腳：「中國模型＝低價搶量」只描述得了階梯的下半段。**當追趕者覺得自己追上了，第一件事就是把價格調到跟自信相符的位置。**

這個定價選擇有明確的資本時間表。[SCMP](https://www.scmp.com/tech/big-tech/article/3354078/chinas-moonshot-ai-moves-unwind-offshore-structure-ipo-pursuit-sources) 和 [The Next Web](https://thenextweb.com/news/moonshot-ai-vie-unwind-hong-kong-ipo-kimi) 報導，Moonshot 正在拆離岸 VIE 結構、為赴港上市鋪路，窗口估計 2026 底到 2027 初；Zhipu 和 MiniMax [已在年初先後掛牌](https://blog.redhub.ai/hong-kong-ai-ipo-market/)。Moonshot 年化營收約 $2 億，對 $20B 估值是 100 倍 revenue multiple。**要撐這種倍數上市，需要的不是市占故事，是「每個 token 都收得到錢」的營收品質故事——$15/M 就是這個故事的第一頁。** 「Kimi 走 GLM 的路」在兩個層面同時成立：定價先往上走，再帶著能力敘事去香港掛牌。

---

## 2.8T 的「開源」，對你的意義跟你想的不一樣

先做算術：2.8T 參數用 FP8 存也要 2.8TB 上下。這週我才[寫過 Bonsai 27B](/bonsai-27b-qwen36-compression-local-inference/) 壓到 3.9GB 塞進 iPhone——K3 的權重是它的七百倍以上。所以受益者要分開看：

**個人開發者：** 你不會自己架 K3，決策點只剩 API。長程 agentic coding（一個任務跑幾小時）已有官方 SWE Marathon 第一加 AA 兩項獨立佐證，值得花一個下午用自己的 harness 實測；短互動、高頻呼叫，K2.5 和 DeepSeek 那個低幾階的價格帶仍是對的選擇。

**企業 CTO：** 2.8T 開放權重的實際意義是「可審計、可私有化——如果你有 GPU 叢集」。數據不出境的場景多了一個接近一線的選項，但基礎設施門檻高一個數量級。

**推理供應商與主權雲：** 開源真正的受眾。史上最大開放權重模型會變成 inference optimization 的公開靶場，KDA kernel、MoE routing 全部攤開。

還有一個容易被 2.8T 淹沒的差異：**vision**。開源旗艦這層，[GLM-5.2 是純文字](https://codingfleet.com/blog/glm-5-2-vs-deepseek-v4-pro/)；DeepSeek V4 Pro 有影像輸入但 AA index 只有 44，跟 K3 的 57 差一整個級距。權重釋出後，「一線智力＋原生 vision」的開源組合只有 K3 一個。官方 demo 主打的 vision in the loop——模型看著 live screenshot 迭代程式碼——正是 frontend 和 E2E 測試每天在做的事。開頭那個 Frontend Arena 登頂，跟這個能力不是巧合的關係：前端是「看得見畫面」回報率最高的場景。只要 coding 和 agent 守得住前段班，這個位置本身就是市場。

---

## 坦白說

官方那三十幾格分數是廠商自報，自家 harness 普遍偏樂觀，K3 不會是例外。AA 補上了整體定位的交叉驗證，但它是單一評測方，coding 主場的具體格子（SWE Marathon、FrontierSWE）還沒有第三方復現。K3 上線預設 max thinking effort，分數是「火力全開」的成績，實際成本和延遲會反映這一點。官方另外宣稱的 self-evolving 案例（K3 花 15 小時優化自己的訓練 kernel、模擬中設計晶片）敘事很強，但全是單方陳述、無可復現細節，當定位宣言讀就好。最後，開源承諾還沒兌現——7 月 27 日目前是一個日期，不是一個 Hugging Face 連結。

即便打完折扣，有一件事表格內外一致：一家中國 lab 承認輸給兩個美國閉源模型、同時把定價拉離中國同行一個數量級。這種「不靠便宜、直接對線」的姿態，比任何單一分數都更能說明頭部中國模型現在的位置。

---

## 關鍵洞察

**1M context 的技術路線正式分岔了。** DeepSeek 走稀疏化、Kimi 走線性化，成本曲線不同：稀疏化保留精確回看、線性化把 decoding 壓得更低。誰勝出未知，但 O(n²) full attention 在 1M 尺度確定是輸家。

**選模型的問題從「哪個便宜」變成「你的任務跑多長」。** 任務跑數小時的 agent 值得實測 K3；要單次推理上限，Fable 5 和 GPT-5.6 的領先還在。需要看畫面的 agent（frontend、E2E），「一線智力＋原生 vision」的開源選項只有它一個。

**看中國模型要用階梯框架，不是價格戰框架。** cost per task：DeepSeek $0.04、GLM $0.32、K3 $0.94——低價搶量只描述得了下半段。配合拆 VIE 赴港上市的節奏，K3 定價是上市前的營收品質故事。值得盯：有沒有人用真實工作負載為 $15/M 買單。

**7 月 27 日是下一個檢查點。** coding 格子的獨立復現、62 tokens/s 是 serving 問題還是 2.8T 的架構代價，都要等權重釋出、更多第三方跑過才有答案。
