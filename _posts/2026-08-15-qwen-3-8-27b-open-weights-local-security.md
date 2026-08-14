---
layout: post
title: "Qwen3.8-27B 開源：SWE-bench Pro 61.7 贏過 Opus 4.6 Max，「那就用地端」第一次不是妥協"
date: 2026-08-15 09:00:00 +0800
permalink: /qwen-3-8-27b-open-weights-local-security/
description: "8/14 Qwen3.8-27B 開源，Apache 2.0，27B dense、原生多模態、262K context。官方 benchmark：SWE-bench Pro 61.7 贏過 Claude Opus 4.6 Max 的 53.4，OSWorld 84.3 對 72.7，AndroidWorld 81.9 對 62.0——贏的全是 agentic workflow 類項目，輸的全是知識天花板類。這篇拆解這個贏輸分布對企業地端部署的意義：跟資安部門開會時，「能力差太多」這個反對地端的理由，第一次接不下去了。"
image: /assets/images/qwen-3-8-27b-local-security-cover.png
categories: [AI 產業分析]
author: Wisely Chen
---

# Qwen3.8-27B 開源：SWE-bench Pro 61.7 贏過 Opus 4.6 Max，「那就用地端」第一次不是妥協

這是我看過大家敲碗最久的小模型。

三月林俊楊離職的時候，社群都在擔心千問即將閉源。[Qwen 3.7 只出了 API-only 的 Max，沒有開源 27B](https://insiderllm.com/guides/qwen-3-7-preview-scored-57-aai-27b-35b-open-weights-watch/)，擔心變成了恐慌。結果這幾個月 Kimi、DeepSeek、GLM 齊力發力，千問在開源圈的領先被碾了一輪。被打到危機之後，Qwen 重新記起它最強的優勢在哪裡了。

[8/14，Qwen3.8-27B 權重放出來](https://huggingface.co/Qwen/Qwen3.8-27B)。Apache 2.0，27B dense，原生多模態，262K context。

官方 benchmark 表裡最顯眼的一行：SWE-bench Pro 61.7。Claude Opus 4.6 Max 是 53.4。

![SWE-bench Pro：Qwen3.8-27B 61.7 vs Claude Opus 4.6 Max 53.4](/assets/images/qwen-3-8-27b-briefing-2.png)

一個跑在自己腳下的 local AI，能力直逼我最喜歡的 Opus 4.6。天上掉餡餅。

今天是資安日。這個發布值得放在資安日講，因為過去企業想用地端模型，永遠繞不開同一個尷尬：地端是安全的，但也是降級的。Qwen3.8-27B 是第一次在官方數字上，27B 級距的開源模型在 agentic 任務贏過 frontier 閉源模型——「那就用地端」第一次不是妥協。

---

## 30 秒定位

| 項目 | Qwen3.8-27B |
|------|-------------|
| 架構 | 27B dense，64 層混合（48 Gated DeltaNet + 16 full attention） |
| 模態 | 原生多模態：文字、圖片、影片輸入 |
| Context | 262K 原生，YaRN 可擴到 1M |
| License | Apache 2.0 |
| 權重大小 | BF16 51.76 GiB / FP8 28.76 GiB / 第三方 Q4 約 17 GiB |
| 同場發布 | Qwen3.8-2.4T-A95B（Max 級）權重也已開源 |

## 贏輸分布比單一分數重要

把官方 benchmark 表攤開，跟 Opus 4.6 Max 的對戰結果有一個很清楚的結構。

**27B 贏的項目：**

| Benchmark | Qwen3.8-27B | Opus 4.6 Max |
|-----------|-------------|--------------|
| SWE-bench Pro（agentic coding） | 61.7 | 53.4 |
| LiveCodeBench v6（競程） | 90.3 | 88.8 |
| CoWorkBench（長程辦公任務） | 70.7 | 68.2 |
| IFBench（指令遵循） | 79.5 | 62.5 |
| [OSWorld-Verified（電腦操作）](https://kingy.ai/blog/qwen3-8-27b-specs-benchmarks-local-hardware/) | 84.3 | 72.7 |
| AndroidWorld（手機操作） | 81.9 | 62.0 |

**27B 輸的項目：**

| Benchmark | Qwen3.8-27B | Opus 4.6 Max |
|-----------|-------------|--------------|
| Terminal Bench 2.1 | 73.0 | 78.2 |
| GPQA Diamond（科學推理） | 89.2 | 91.3 |
| HLE（跨領域推理） | 30.8 | 40.0 |
| NL2Repo-Bench（整 repo 生成） | 42.3 | 47.6 |

分布不是隨機的。**贏的全是 agentic workflow 類：改 code、跑流程、操作電腦和手機、聽懂指令。輸的全是知識和推理天花板類：科學推理、跨領域難題、從零生成整個 repo。**

![贏輸分布：Agentic 任務全贏，知識天花板任務全輸](/assets/images/qwen-3-8-27b-briefing-4.png)

這個分布恰好對到企業內部部署的需求清單。企業 agent 的日常是「讀 ticket、改三個檔案、跑測試、填表單、操作內部系統」，不是解 GPQA 等級的科學題。天花板類能力輸 Opus 幾分，對這類 workload 的影響有限；agentic 類能力贏，才是每天都用得到的差異。

對比前代也能看出這次的重心：同一張表裡，SWE-bench Pro 從 Qwen3.6-27B 的 53.5 拉到 61.7，DeepSWE 從 13.3 拉到 42.2，OSWorld 從 63.9 拉到 84.3。這不是全面均勻進步，是對著 agent 場景集中火力。

---

## 架構沒變，變的是 agent 訓練

這個贏輸分布為什麼長這樣？把 Qwen3.8-27B 的 config.json、權重索引和 Transformers 實作翻一遍，答案很明確：**底層架構跟 Qwen3.6-27B 幾乎沒有變化。**

model_type 仍然是 `qwen3_5`。64 層 decoder、5120 hidden size、17408 FFN、48 層 Gated DeltaNet + 16 層 full attention、24 個 query heads、4 個 KV heads、262K context、同一套視覺塔、同一套 MTP 配置、同一個詞表——逐項對比，關鍵參數完全一樣。

這意味著 agentic benchmark 的跳升不是來自架構創新。更合理的判斷是：阿里已經把 Qwen3.5 這套 hybrid 架構穩定下來，集中火力優化權重、agent 軌跡訓練、coding 環境交互數據、強化學習和 tool calling 行為。

**Qwen3.8 不是「架構上的 3.8」，是「agent 行為上的 3.8」。**

![底層架構 0 變化，飛躍的進步來自後訓練](/assets/images/qwen-3-8-27b-briefing-5.png)

這也解釋了為什麼 GPQA Diamond 只進步 1.4 分、HLE 幾乎沒動，而 OSWorld 跳了 20.4 分、DeepSWE 跳了 28.9 分——前者靠的是模型容量和預訓練知識，後者靠的是後訓練和環境交互數據。架構不變、後訓練集中火力，跳的自然是後者。

對生產系統來說，這反而是好消息。架構穩定意味著 vLLM、SGLang 等推理引擎不用重新適配算子，量化方案可以繼承，已有的 kernel 優化可以複用，企業遷移成本更低。

---

## 部署現實：Hybrid 架構天生省 KV cache

前面講了架構沒變，但這套 hybrid 架構本身對地端部署有一個很實際的好處：**64 層裡只有 16 層需要存隨 context 線性增長的 KV cache。**

![混合架構記憶體優勢：48 Gated DeltaNet + 16 Full Attention](/assets/images/qwen-3-8-27b-briefing-6.png)

48 層 Gated DeltaNet 維護的是固定大小的遞迴狀態矩陣，不管 context 多長，記憶體佔用不變。傳統純 Transformer 的 64 層每層都要存 KV cache，Qwen3.8 只有 16 層要。這讓它比同規模的純 Transformer 天生更適合長會話、coding agent、多輪 tool calling 這類 context 越跑越長的場景。

但不能神化——那 16 層 full attention 的 KV cache 還是在的。BF16 下每個 token 約 64 KiB，[262K 全開約 16 GiB，1M context 約 61 GiB](https://kingy.ai/blog/qwen3-8-27b-specs-benchmarks-local-hardware/)。二次複雜度從 64 層降到 16 層，不是消除了二次複雜度。

資安日系列的老讀者知道，我七月[借 RTX Pro 6000 跑過一週 Tier 1 地端實驗](https://ai-coding.wiselychen.com/rtx-pro-6000-tier1-week-final-offload-qwen-vl-vllm/)：GLM 5.2 那種 744B 級的模型，96GB VRAM 塞不下，得靠 MoE offload 到系統 RAM，天花板釘死在每秒十個 token 上下，互動式 agent 用起來是煎熬。

27B dense + hybrid cache 完全是另一個世界：

- **FP8 官方版 28.76 GiB**：一張 48GB 級的卡，權重加上工作 context 的 KV cache 可以住得舒服
- **第三方 Q4 量化約 17 GiB**：一張 24GB 消費卡就能跑中等 context
- 唯一要注意的是長 context 的帳：262K 全開時光 full-attention 那 16 層的 KV cache 就要約 16 GiB，24GB 卡跑的是「Q4 + 節制的 context」，不是規格表上的滿血狀態

我自己在 RTX 5090 32GB 上跑了一輪：UD-Q4_K_XL 量化、Q8 KV Cache、Flash Attention 與 MTP 全開，平均生成速度約 125 tok/s，一般回應大概 3 秒。關掉 MTP 大約 72 tok/s，MTP 帶來約 55%～66% 加速，draft 接受率約 64%～69%。上個月同一台機器跑 GLM 5.2 offload 是十幾 tok/s 的煎熬，27B dense 跑 125 tok/s——即時對話、長文摘要、高頻推論都沒問題，互動式 agent 完全可以用。

兩天前我才在[記憶體漲價那篇](https://ai-coding.wiselychen.com/memory-price-surge-local-ai-five-paths/)寫「先選模型，才決定買什麼硬體；27B 級距讓你避開整個為大模型而生的硬體採購」，當時 Qwen3.8-27B 權重還沒放出來，只能當期貨寫。現在權重在手，這條路線補上了最關鍵的一塊：**27B 級距第一次有了官方數字上打贏 frontier 模型的選項。**

但量化有一個舊帳要記得。[Bonsai 27B 那篇的教訓](https://ai-coding.wiselychen.com/bonsai-27b-qwen36-compression-local-inference/)：壓縮損失不均勻，前代 Qwen3.6-27B 壓到 1-bit 時 MATH 500 從 99.4 只掉到 98，TauBench（tool calling）卻從 82.9 掉到 61.3。官方 benchmark 是 BF16/FP8 測的，你在 24GB 卡上跑的 Q4 版折損多少、有沒有剛好折在 agentic 能力上——目前沒有人量過。**拿到量化版之後，先測 tool calling，再決定信多少。**

---

## 「地端模型比較安全」的誠實版本

「地端模型比較安全」——這句話現在工程師可以理直氣壯地講了，而且不用心虛能力差太多。

但今天是資安日，這句話本身也要過一次資安檢驗。

地端部署真正解掉的是**資料出境風險**：prompt、程式碼、客戶資料不離開機房，沒有供應商的資料保留條款要審，沒有跨境傳輸的合規問題要處理。對台灣的金融、醫療、政府標案場景，這一類風險經常是「一票否決」級的，地端把它整個拿掉，這是真的。

但地端**沒有**解掉 agent 行為風險。一個能改 code、跑指令、操作內部系統的 agent，跑在你自己的機器上，prompt injection 一樣打得進來，權限給太大一樣刪得掉資料庫。這一類風險跟模型放在哪裡無關，跟 harness 怎麼設計有關。

![資安邊界：地端解決資料出境，但 agent 行為風險仍在](/assets/images/qwen-3-8-27b-briefing-8.png)

所以誠實版本是：**地端解掉的是「資料流向誰」的問題，不是「agent 會做什麼」的問題。** 前者是採購和合規層級，後者是工程層級。「地端比較安全」這句話成立，但只成立一半——權限收斂和工具鏈隔離的工還是一樣多。

---

## 反方：這些是 Qwen 自己測的

先把最強的反駁擺出來：整張 benchmark 表是 Qwen 發的。

而且測法不對等。官方註明，SWE-bench Pro 上除了 Opus 4.6 Max 用官方報告分數，其他模型都是 Qwen 用 Claude Code harness、temp=1.0、256K context 自己測的——這不是同一套條件下的對照實驗。分差最大的兩項（QwenSWEBench 79.0 對 63.8、CoWorkBench 70.7 對 68.2）恰好都是 Qwen 自家出的 benchmark。發布隔天，[還沒有任何第三方獨立復現](https://kingy.ai/blog/qwen3-8-27b-specs-benchmarks-local-hardware/)。輸掉的四項倒是不用懷疑，那是官方表自己承認的。

這些折扣都打完之後，剩下什麼？

剩下的其實還夠。這個論點不需要「27B 全面超越 Opus 4.6 Max」才成立——那個宣稱本來就不成立，天花板類的四項輸得清清楚楚。它只需要「27B 在企業 agent workload 上夠接近 frontier，讓能力差距不再是否決地端的理由」。SWE-bench Pro 是公開 benchmark，53.5 到 61.7 的世代進步是同 harness 同條件測出來的；OSWorld 從 63.9 到 84.3 的跳幅，就算打七折也還是換了一個級距。方向的可信度，比單點數字的精確度高。

---

## 坦白說

- 全部數字來自官方發布，發布隔天沒有第三方復現。這篇是「官方宣稱的拆解」，不是實測報告。
- 速度我自己跑出來了（RTX 5090 + Q4_K_XL + MTP 約 125 tok/s），但 agent 品質的系統性評測還沒做——尤其是 Q4 量化後的 tool calling 折損。benchmark 判斷仍掛著「如果官方數字可信」的前提。
- 「贏的都是 agentic 類」這個分布，也可以反過來解讀成「Qwen 挑了對自己有利的項目放進表格」。OSWorld 和 AndroidWorld 的對比數字來自官方公布，Opus 那一側的測試條件我查不到公開細節。
- **社群第一批實測反饋最一致的抱怨是「想太多」。** 官方預設 reasoning_effort=xhigh，有人拿同一個 Tetris 任務測，3.6 想了約 3,000 字就動手，3.8 想到 15,000 字還在想。成品確實更精緻（自己加了暫停、高分榜、復古音效），但牆鐘時間差了好幾倍。從開源 chat template 來看，reasoning_effort 本質上是 prompt steering（system prompt 裡加不同強度的「仔細想」指示），不是動態網路深度。調成 medium 或關掉 thinking 之後問題會小很多，但這表示**官方 benchmark 大概率是 xhigh 跑出來的分數，日常使用如果調低 effort 來換速度，能力是否打折還不知道。**
- 27B 打的是 Opus 4.6 Max 這一代。frontier 模型也在動，這個「夠接近」的窗口能開多久，沒人知道。

---

## 關鍵洞察

1. **「那就用地端」第一次不是妥協。** 過去選地端等於接受降級。現在 27B 在 agentic 任務的官方數字贏過 Opus 4.6 Max，能力差距這個反對理由接不下去了。

2. **看 benchmark 先看贏輸分布，再看單一分數。** 27B 贏在 agentic workflow，輸在知識天花板。你的 workload 落在哪一類，決定這張表對你是利多還是雜訊。企業內部 agent 多數落在前者。

3. **量化之後先測 tool calling。** 官方數字是 BF16/FP8 的，24GB 卡上跑的 Q4 是另一顆沒人測過的模型。Bonsai 的教訓還熱著：壓縮最先傷的就是 agent 能力。

4. **「地端比較安全」只解一半。** 資料出境風險歸零，agent 行為風險原封不動。會議打贏之後，harness 的權限設計才是資安工作的開始。

---

## 延伸閱讀

### 一手來源

- [Qwen3.8-27B 權重（Hugging Face）](https://huggingface.co/Qwen/Qwen3.8-27B)
- [Qwen3.8-27B 規格與硬體需求拆解（kingy.ai）](https://kingy.ai/blog/qwen3-8-27b-specs-benchmarks-local-hardware/)
- [Qwen3.8-2.4T-A95B GGUF（Unsloth）](https://huggingface.co/unsloth/Qwen3.8-2.4T-A95B-GGUF)

### 我之前寫過的相關文章

- [5090 三個月從 10 萬變 17 萬：五條技術路徑壓低地端 AI 的硬體門檻](https://ai-coding.wiselychen.com/memory-price-surge-local-ai-five-paths/) — 兩天前的「先選模型再買硬體」，本篇補上關鍵一塊
- [Bonsai 27B：55.6GB → 3.9GB 保留 90% 智力](https://ai-coding.wiselychen.com/bonsai-27b-qwen36-compression-local-inference/) — 量化損失不均勻、tool calling 最先受傷的證據
- [單機跑 Tier 1 地端 Model 一週實驗完賽](https://ai-coding.wiselychen.com/rtx-pro-6000-tier1-week-final-offload-qwen-vl-vllm/) — 大模型 offload 的速度天花板，對照 27B dense 的部署差異
- [AI Coding On-Prem 的三條路](https://ai-coding.wiselychen.com/ai-coding-on-prem-three-paths/) — 核心不是模型多聰明，而是工具鏈多穩定
