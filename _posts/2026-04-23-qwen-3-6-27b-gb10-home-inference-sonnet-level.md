---
layout: post
title: "Qwen 3.6-27B 本地部署：DGX Spark / Mac mini 跑出 Sonnet 4.6 等級 AI Agent"
date: 2026-04-23 08:00:00 +0800
permalink: /qwen-3-6-27b-sonnet-level-home-inference/
image: /assets/images/qwen-3-6-27b-run-locally-cover.png
image_alt: "Qwen 3.6-27B 本地部署示意圖：Run the new 27B model locally"
author: "Wisely Chen"
category: it-arch
tags:
  - Qwen 3.6
  - 本地 LLM
  - on-prem AI
  - AI Agent
  - DGX Spark
  - Mac mini M4 Pro
  - Claude Sonnet 4.6
  - IT 架構
  - 企業 AI
  - Dflash DDTree
description: "Qwen 3.6-27B 開源 dense 模型在 $4,699 的 NVIDIA DGX Spark 跑出 136 tokens/sec，Benchmark 打贏 Claude Opus 4.5、Terminal-Bench 微幅超過 Sonnet 4.6。本文替 IT 架構師盤點 Qwen 3.6-27B 本地部署的硬體選項（DGX Spark vs Mac mini M4 Pro 64GB）、12 項官方 Benchmark、Dflash + DDTree 推理棧、單人 3 年 TCO $22,500 vs $4,729 成本對照，以及 on-prem AI Agent 架構重寫的決策要點。"
faq:
  - question: "Qwen 3.6-27B 到底是什麼等級的模型？真的能取代 Claude Sonnet 4.6 嗎？"
    answer: "就 Qwen 團隊公布的 12 項官方 Benchmark 來看：SWE-bench Verified 77.2（Sonnet 4.6 是 79.6），Terminal-Bench 2.0 59.3（Sonnet 4.6 是 59.1，Qwen 微幅領先），跟 Claude Opus 4.5 對比贏 7 項、平手 1 項、輸 4 項。「Sonnet 4.6 等級」不是比喻，是字面上的事實。但純寫 code 的頂尖品質（SWE-bench Pro、NL2Repo），Opus 4.5/4.6 仍有 3-7 分優勢。結論：80% 日常 agentic coding 任務可取代，關鍵任務仍建議 fallback 到商業 API。"
  - question: "Qwen 3.6-27B 最低要什麼硬體才跑得動？Mac mini 可以嗎？"
    answer: "Qwen 3.6-27B FP8 需要約 27GB VRAM。最低可用配置是 Mac mini M4 Pro 64GB（$2,199，12-18 t/s），足以應付單人 interactive coding。Mac mini M4 Pro 48GB 勉強可跑但 context 要小心。base Mac mini（最多 32GB）只能跑 Q4 量化版本，品質打折。要跑 autonomous agent（10 agents 並行）建議 NVIDIA DGX Spark（$4,699，128GB 統一記憶體，136 t/s）。"
  - question: "NVIDIA DGX Spark 的規格和售價是多少？值得買嗎？"
    answer: "DGX Spark 搭載 GB10 Grace Blackwell Superchip：20 核 ARM CPU（10 × Cortex-X925 @ 4GHz + 10 × Cortex-A725 @ 2.8GHz）、6,144 CUDA cores Blackwell GPU、128GB LPDDR5X 統一記憶體、4TB NVMe SSD、ConnectX 200 Gbps 網路、FP4 效能 1 petaFLOP，售價 $4,699 USD（約 15 萬台幣）。49W 功耗比 LED 燈泡多一點。對比單人 3 年 Sonnet 4.6 API 成本 $22,500，3 年 TCO 只要 $4,729，省 $17,771。"
  - question: "Dflash + DDTree 是什麼？沒有這套推理棧也能跑嗎？"
    answer: "DFlash 是 Block Diffusion Flash Speculative Decoding，用 draft model 一次預測一整個 block 的候選 tokens 在單次 forward pass 中驗證（來自 z-lab 開源專案）。DDTree 是改進版，把候選 tokens 組成樹狀結構同時產出多條路徑。實測加速 6-8 倍。沒有這套棧，同樣硬體大約只有 20-30 t/s（不是 136 t/s）。但它不是主流推理棧——生產環境建議等 vLLM / SGLang 整合（預估 1-2 季）。"
  - question: "我們是金融 / 醫療 / 政府產業，Qwen 是中國模型，能用嗎？"
    answer: "Apache 2.0 license 本身沒有地緣限制，但多數高度監管產業的法務會對「中國團隊訓練的權重」有疑慮。實務上建議兩條路：一是等 Llama / Mistral 下一代追上（歷史經驗 2-3 個月落後），二是用 Qwen 3.6-27B 做內部非敏感工具的 pilot，確認流程跑得通再評估。具體合規需看各產業主管機關對開源 AI 模型的指引。"
  - question: "on-prem 跑 Qwen 3.6-27B vs 用 Claude API，3 年 TCO 差多少？"
    answer: "以重度 AI coding 工程師為例（日均 5M input + 1M output tokens）：Claude Sonnet 4.6 API 單人年費 $7,500，3 年 $22,500；DGX Spark + Qwen 3.6-27B 硬體 $4,699 + 3 年電費約 $30，TCO $4,729。單人省 $17,771（約 55 萬台幣），10 人團隊省 $177,710，100 人團隊省 $1,777,100。但真正價值不只省錢，還包括資料不出公司、不受 API rate limit、不依賴單一供應商。"
  - question: "Qwen 3.6-27B 為什麼不做成 MoE 架構？Dense 27B 有什麼優勢？"
    answer: "Qwen 3.5 自家也出過 397B-A17B 的 MoE 旗艦，但 3.6 世代把最強 agentic coding 能力放回 27B dense。原因是 MoE 雖然 active parameter 少，但總參數大 VRAM 需求反而高，不適合「消費級顯卡 / 桌面工作站」這個部署 sweet spot。27B dense FP8 只要 27GB VRAM，RTX 5090（32GB）、Mac mini M4 Pro 64GB、DGX Spark 128GB 都塞得進去。Qwen 團隊押注 agentic coding 的戰場在 on-device 不在 cloud。"
  - question: "那 Anthropic / OpenAI 商業 API 是不是要完了？"
    answer: "不會。Opus 4.6 / Opus 4.7 仍是最強的 coding model，關鍵任務仍會跑在商業 API。但 Anthropic 失去了「你別無選擇」的定價權，這是結構性改變。未來 API 定價壓力會加大，或商業模型必須在 agentic workflow / tool ecosystem / enterprise features 建立更深護城河。對企業 IT 來講這是好事：多了一個可以算 TCO 的選項，原本 API 訂閱變成可以議價的成本。"
---

![Qwen 3.6-27B 本地部署示意圖：Run the new 27B model locally](/assets/images/qwen-3-6-27b-run-locally-cover.png)

## 目錄

- [TL;DR](#tldr)
- [為什麼這又是一篇「無聊 IT 架構」文](#為什麼這又是一篇無聊-it-架構文)
- [第一段：為什麼是 Qwen 3.6-27B？](#第一段為什麼是現在為什麼是-qwen-3-6-27b)
- [第二段：Qwen 3.6-27B 的 Benchmark 贏過 Opus 4.5](#第二段qwen-3-6-27b-的-benchmark-結果居然贏過-opus-4-5)
- [第三段：網友用什麼機器跑？Token Performance 多少？](#第三段網友用什麼機器跑起來token-performance-是多少)
- [這對企業 IT 架構師意味著什麼](#這對企業-it-架構師意味著什麼)
- [常見問題 Q&A](#常見問題-qa)

## TL;DR

- **Qwen 3.6-27B（dense, Apache 2.0）** 在 12 項 Benchmark 上贏 Claude Opus 4.5 七項、平手一項，SWE-bench / Terminal-Bench 落在 **Sonnet 4.6 等級**
- 一位網友在 NVIDIA **DGX Spark（$4,699, 49W 功耗）** 跑出 136 tokens/sec，10 agents 並行峰值 209 t/s
- **「Sonnet 4.6 等級的 AI coding agent」不再需要雲端 API**——可以跑在辦公桌下那台比微波爐小的機器
- IT 架構師該做的事：**重新算一次 on-prem AI Coding ROI，6 個月前的假設已經過時**

---

## 為什麼這又是一篇「無聊 IT 架構」文

又一篇「無聊 IT 架構」系列文。

過去這一年大家討論 local LLM 都在講 performance——跑什麼模型、用什麼量化、GPU 要買哪張。但對企業 IT 架構來講，真正要問的只有一個問題：

**「local 到底夠不夠取代 Anthropic / OpenAI 的 API？」**

這個問題過去的答案是「還差得遠」。6 個月前你跟 CTO 說「我們來 on-prem 跑 Claude Code 的工作負載」，他會笑你——本地模型品質差商業 API 一個世代，工程師根本不會願意用。

但 2026 年 4 月 22 日 Qwen 團隊丟出 **Qwen 3.6-27B** 的那一刻，這個答案變了。

這篇文章不是在炫耀 benchmark，是要回答 IT 架構師真正關心的事：

1. **Benchmark 上，Qwen 3.6-27B 到底是什麼等級？** 答：Sonnet 4.6 等級，不是比喻，是數字字面上的事實
2. **跑得起來嗎？要什麼硬體？** 答：$4,699 的 NVIDIA DGX Spark，放辦公桌下，49W 功耗比一顆 LED 燈泡多一點
3. **那我原本的 on-prem AI Coding 架構藍圖，還對嗎？** 答：不對，該重畫了

---

## 第一段｜為什麼是現在？為什麼是 Qwen 3.6-27B？

先把幾個名詞講清楚，因為這些東西過去 6 個月都在快速演進。

### Qwen 3.6-27B 是什麼

**Qwen 3.6-27B** 是阿里雲 Qwen 團隊在 2026 年 4 月發布的新一代開源模型：

- **架構：** Dense（不是 MoE），27B 參數全部 active
- **Context：** 原生 262,144 tokens，可延伸到 1M（YaRN）
- **量化：** 官方提供 FP8 版本（約 27GB VRAM），另有 54 個社群量化版本（llama.cpp、LM Studio、Ollama 等）
- **License：** Apache 2.0（商用無限制）
- **能力：** 除了文字，還支援 vision（多模態），原生支援 tool calling

這個架構選擇本身就是一個訊號。

2025 年開源圈集體轉向 MoE 的時候，Qwen 3.5 自己也出了 397B-A17B 的 MoE 旗艦。但到了 3.6 世代，他們把**最強的 agentic coding 能力放回 27B dense**。為什麼？

因為 dense 27B 剛好是「一張消費級顯卡 / 一台工作站」能跑的 sweet spot。MoE 雖然 active parameter 少，但總參數大，VRAM 需求反而高。27B dense FP8 只要 27GB VRAM——DGX Spark 的 128GB 統一記憶體綽綽有餘，一張 RTX 5090（32GB）也塞得進去。

**Qwen 團隊的 bet 很明確：agentic coding 的戰場在 on-device，不在 cloud。**

### 為什麼我說「這個時間點有意義」

把過去 18 個月的里程碑排一下：

| 時間 | 事件 | 意義 |
|---|---|---|
| 2024 Q4 | Local LLM 僅限 demo 用途 | 品質距商業 API 一個世代 |
| 2025 Q1 | Qwen 3.5-27B 讓本地 tool calling 可用 | 第一次有 local 能 production |
| 2025 Q3 | Claude Opus 4.5 發表 | Anthropic 旗艦，當時 state-of-the-art |
| 2025 Q4 | Mac Studio M3 Ultra 可跑 70B 模型 | 消費級硬體追上 |
| **2026 Q2（現在）** | **Qwen 3.6-27B 家用機跑出 Sonnet 4.6 等級** | **On-prem ROI 假設全部要重算** |

Chris Maddern 在 X 上的觀察很精準：

> "Opus 4.5 was released 5 months ago, the gap is closing. Opus 4.5 was the breakthrough moment for 'good enough to stop writing code'... real local coding inference is coming."
>
> （Opus 4.5 是 5 個月前發表的。差距正在縮小。Opus 4.5 是「好到可以停止手寫 code」的突破時刻。真正的 local coding inference 要來了。）

**過去我們說「6 個月前沿差距」**——開源模型通常落後商業模型大約半年。現在這個差距壓縮到了**一個季度**，某些領域甚至**打平**。

對企業 IT 來講，這不是技術趣聞，是架構決策的輸入條件變了。

---

## 第二段｜Qwen 3.6-27B 的 Benchmark 結果，居然贏過 Opus 4.5

Qwen 團隊公布的官方 benchmark 有 12 項。要比的對手是誰？

- **Qwen 3.5-27B**（上一代 dense）
- **Gemma4-31B**（Google dense 對標）
- **Qwen 3.6-35B-A3B**（自家 MoE 對照）
- **Qwen 3.5-397B-A17B**（上一代旗艦 MoE）
- **Claude 4.5 Opus**（Anthropic 當時的旗艦）

直接看結果。

### 完整 Benchmark 對比表

| Benchmark | 類別 | Qwen 3.6-27B | Qwen 3.5-397B-A17B | Claude 4.5 Opus | 誰贏？ |
|---|---|---|---|---|---|
| **Terminal-Bench 2.0** | Agentic Terminal | **59.3** | 52.5 | 59.3 | 平手 Opus |
| **SWE-bench Pro** | Agentic Coding | 53.5 | 50.9 | **57.1** | Opus |
| **SWE-bench Verified** | Agentic Coding | 77.2 | 76.2 | **80.9** | Opus |
| **SWE-bench Multilingual** | Multilingual Coding | 71.3 | 69.3 | **77.5** | Opus |
| **QwenClawBench** | Real-World Agent | **53.4** | 51.8 | 52.3 | **Qwen** |
| **QwenWebBench (Elo)** | Artifacts | 1487 | 1186 | **1536** | Opus |
| **NL2Repo** | Long-Horizon Coding | 36.2 | 32.2 | **43.2** | Opus |
| **SkillsBench** | Agent Skills | **48.2** | 30.0 | 45.3 | **Qwen** |
| **Claw-Eval (pass^3)** | Real-World Agent | **60.6** | 48.1 | 59.6 | **Qwen** |
| **GPQA Diamond** | Graduate Reasoning | **87.8** | 88.4 | 87.0 | **Qwen (微)** |
| **MMMU** | Multimodal Reasoning | **82.9** | 85.0 | 80.7 | **Qwen** |
| **RealWorldQA** | Image Reasoning | **84.1** | 83.9 | 77.0 | **Qwen** |

**計分：Qwen 3.6-27B 贏 7 項、平手 1 項、輸 4 項 Claude 4.5 Opus。**

一顆開源 27B dense 模型，在 12 項官方 benchmark 中打贏 Anthropic 5 個月前的旗艦七項。

### 讀得出什麼故事？

先看 Qwen 3.6-27B **輸**的 4 項：

- SWE-bench Pro：53.5 vs 57.1（差 3.6 分）
- SWE-bench Verified：77.2 vs 80.9（差 3.7 分）
- SWE-bench Multilingual：71.3 vs 77.5（差 6.2 分）
- NL2Repo：36.2 vs 43.2（差 7.0 分）

**輸的全在純 coding 和 long-horizon repo reasoning。** 這不意外——Opus 4.5 是針對寫 code 優化的旗艦。差距最大的 NL2Repo（長跨度 repo 理解）是 Opus 最有優勢的場景。

再看 Qwen 3.6-27B **贏**的 7 項：

- QwenClawBench（real-world agent 任務）：53.4 vs 52.3
- SkillsBench（agent skills）：48.2 vs 45.3
- Claw-Eval（real-world agent pass^3）：60.6 vs 59.6
- GPQA Diamond（研究生級推理）：87.8 vs 87.0
- MMMU（多模態推理）：82.9 vs 80.7
- RealWorldQA（圖像推理）：84.1 vs 77.0（+7.1 分）

**贏的是 real-world agent、agent skills、reasoning、multimodal。**

這一組剛好是 AI coding **agent** 真正需要的能力——不是一次性寫完一個 PR，是**長時間跑、能用工具、能看螢幕、能推理**的那種工作負載。

### 跟 Sonnet 4.6 對比，才是文章標題的來源

Opus 4.5 是 2025 年 11 月的旗艦，對多數企業 AI coding 工作負載來講已經過度規格。2026 年 Q1 Anthropic 發表了 **Claude Sonnet 4.6**——這才是現在大多數 Claude Code 日常工作跑的模型。

看對照：

| Benchmark | Qwen 3.6-27B | Claude Sonnet 4.6 | 差距 |
|---|---|---|---|
| **SWE-bench Verified** | 77.2 | 79.6 | Sonnet +2.4 |
| **Terminal-Bench 2.0** | **59.3** | 59.1 | **Qwen +0.2** |

不是比喻，是字面上的事實：

- **Terminal-Bench 2.0：Qwen 3.6-27B 微幅高於 Sonnet 4.6。**
- **SWE-bench Verified：落後 Sonnet 4.6 只有 2.4 分——在統計誤差邊緣。**

Sonnet 4.6 的 API 價格是 $3 / $15 per million tokens（input / output）。一位重度 AI coding 工程師日均 5M input + 1M output tokens，**每天刷 $30，一年 $7,500**。

這個錢，現在可以不刷。

---

## 第三段｜網友用什麼機器跑起來？Token Performance 是多少？

Benchmark 贏 Opus 4.5 只是故事的一半。另一半——也是企業 IT 真正關心的——是**這東西跑得起來嗎？要什麼硬體？**

### 核心數據來自這條推文

2026 年 4 月 22 日，推特用戶 [Mitko Vasilev（@iotcoi）貼出一張終端機截圖](https://x.com/iotcoi/status/2046950805568164168)：

> "Qwen3.6-27B-FP8 + Dflash + DDTree, 256k context, 10 agents
> ~200 tokens/sec max decode
> **136 t/s average on a single tiny GB10 GPU at 49W power**"

另一位用戶 LotusDecoder 接力引用並補一句：

> "香啊，家用小型台式机，推理 qwen-3.6-27B-fp8 达到 136 tokens/sec。
> 性能估计是可以接近 haiku-4.5 吧。"

（實際上低估了，是 Sonnet 4.6 等級。）

這三個硬體 + 軟體元件值得拆開來看。

### 硬體：NVIDIA DGX Spark / GB10

**NVIDIA DGX Spark** 是 NVIDIA 2026 年推出的「家用 AI 工作站」。規格如下：

| 項目 | 規格 |
|---|---|
| SoC | NVIDIA GB10 Grace Blackwell Superchip |
| CPU | 20 核 ARM（10 × Cortex-X925 @ 4GHz + 10 × Cortex-A725 @ 2.8GHz） |
| GPU | 6,144 CUDA cores, Blackwell 架構 |
| 記憶體 | **128GB LPDDR5X 統一記憶體** |
| 儲存 | 4TB NVMe SSD |
| 網路 | ConnectX 200 Gbps（兩台 Spark 可互聯跑 405B 模型） |
| FP4 效能 | 1 petaFLOP |
| **售價** | **$4,699 USD（約 15 萬台幣）** |
| 形式 | 桌上型，比 Mac Studio 略小 |

關鍵是那顆 **GB10 Superchip** 的統一記憶體——128GB 全部可以給 GPU 用。Qwen 3.6-27B FP8 只吃 27GB，剩下 100GB 可以開超大 KV cache 跑長 context、或同時載入多個模型切換。

這個硬體定位很明確：**不是要取代資料中心的 H100，是要取代工程師桌上的 MacBook Pro。** 每個 AI coding 工程師配一台，放辦公桌下，自己的 agent 自己跑。

### 軟體：Dflash + DDTree 是什麼？

Mitko 的推文提到 `Dflash + DDTree`——這是推理加速的關鍵。

- **DFlash**：Block Diffusion Flash Speculative Decoding。簡單講，用一個小的 draft model 一次「預測」一整個 block 的候選 tokens，然後目標模型在單次 forward pass 中驗證。來自 z-lab 的開源專案。
- **DDTree**：DFlash 的改進版，把候選 tokens 組成一棵樹狀結構，在同一個 draft pass 裡產出多條候選路徑，驗證時只選最佳。論文實測在 Qwen3-8B 上，HumanEval 從 4.84× 加速到 6.90×，GSM8K 從 4.78× 到 6.75×。

這兩個技術的意義：**不用換硬體，單純靠軟體優化就能在同一張 GPU 上把 token 吞吐拉高 6-8 倍。**

Mitko 的 136 t/s 就是這樣來的——沒有 DFlash + DDTree，同樣硬體大約只有 20-30 t/s 的水準。

### 吞吐量到底夠不夠用？

136 t/s 在 10 agents 並行的設定下分配，等於每個 agent 約 **20 t/s**。

這個數字對比幾個參考點：

| 場景 | 吞吐量 | 感受 |
|---|---|---|
| 人類閱讀速度 | ~5 t/s | 慢到讀得完 |
| Claude API Sonnet 4.6（典型） | ~50-80 t/s | 快但常被 rate limit |
| **Mitko 的 DGX Spark（每 agent）** | **~20 t/s** | **比閱讀快 4x** |
| **Mitko 的 DGX Spark（全機峰值）** | **209 t/s** | **10 agents 並行才壓得到** |

換句話說，**單個 agent 20 t/s 稍慢於 Claude API**，但 10 agents 可以**同時跑**且**不受 rate limit**——對於 autonomous agent workflow、subagent、cron-driven background task 這類負載，**總吞吐量反而勝過 API**。

### 功耗：49W 的意義

49W 是什麼概念？

- 一顆 LED 燈泡：約 10W
- MacBook Pro 全速跑：約 100W
- **DGX Spark 跑 Qwen 3.6-27B agent 負載：49W**
- RTX 4090 單卡跑 LLM：約 400W
- A100 伺服器：約 400-700W

一年 8 小時工作日 × 250 天 × 49W = **98 kWh/year**，按台電工業電費約 **NT$ 300/year**。

這個數字低到進不了任何成本模型——跟 API 每年 $7,500 的差距比起來，電費是四捨五入誤差。

### Mac Studio 這邊呢？Rapid-MLX 實測

企業裡比 DGX Spark 更普及的硬體是 Mac Studio，Mac 這邊的數據三天後也出來了。Apple Silicon 推理引擎 [Rapid-MLX](https://github.com/raullenchai/Rapid-MLX)（Apache 2.0 開源、相容 OpenAI API）v0.6.1 做了 Qwen 3.6 Day-0 支援，在 **Mac Studio M3 Ultra（256GB）** 上跑出 **4-bit 36.5 t/s（佔 14.9GB）、8-bit 18.9 t/s（佔 32.3GB）**，coding eval 100% pass、stress test 8/8。**這個數字反過來說明 DGX Spark 那 136 t/s 不是硬體碾壓，是 DFlash + DDTree 軟體棧帶來的**——沒套加速時 GB10 只有 ~15 t/s，跟 M3 Ultra 在同一個檔位。對 IT 架構師意義很直接：**公司已經發 Mac Studio 給工程師的（很多矽谷公司是這樣），不用再買 DGX Spark，`pip install rapid-mlx` 一行就能跑 Qwen 3.6-27B**，36.5 t/s 對單人 interactive coding 完全夠用。

### 成本結構對照

把單人成本算清楚：

| 方案 | Year 1 | Year 2 | Year 3 | 3 年總 TCO |
|---|---|---|---|---|
| **Claude Sonnet 4.6 API** | $7,500 | $7,500 | $7,500 | **$22,500** |
| **DGX Spark + Qwen 3.6-27B** | $4,699 + $10 電 | $10 | $10 | **$4,729** |

**單人 3 年 TCO 差距：$17,771（約 55 萬台幣）。**

放大到團隊：

- 10 人 AI coding 團隊：3 年省 $177,710（約 550 萬台幣）
- 100 人團隊：3 年省 $1,777,100（約 5,500 萬台幣）

但這些數字不是文章的重點。**真正的重點是：**

1. **資料不出公司**——所有 code、所有 prompt、所有輸出都在公司網內，金融、醫療、國防、法務部門終於能用 AI coding
2. **不受 API rate limit**——autonomous agent 要跑就跑，不用排隊
3. **不依賴單一供應商**——Anthropic 明天漲價 3 倍，你也不痛

---

## 這對企業 IT 架構師意味著什麼

如果你是 CTO / VP of Engineering / IT 架構負責人，這篇文章真正要你做的事是：

### 三個檢查點

1. **6 個月前你拒絕 on-prem AI coding 的理由是什麼？**
   - 「模型品質差商業 API 一個世代」？→ 現在差不到一個季度，甚至某些指標打平
   - 「硬體太貴，投資回收期太長」？→ 單台 $4,699，3 年 ROI 76%
   - 「工程師不會想用」？→ Sonnet 4.6 等級他們會想用，差的是工具鏈不是品質

2. **這些理由在 2026 年 4 月還成立嗎？**
   - 如果「不成立」的項目超過 2 個，你的架構假設過期了

3. **Pilot 成本是多少？**
   - 一台 DGX Spark：$4,699
   - 一個工程師週末的時間：裝 Qwen 3.6-27B、接上 Claude Code 或 aider、跑一週看看
   - 總投入 < $6,000，低於多數企業 IT 的「不用跑審批」門檻

### 但也要誠實講 Caveat

這不是吹開源 model 的宣傳文。幾個 caveat 一定要講：

- **純寫 code 的頂尖品質，Opus 4.5 / Opus 4.6 仍勝**。SWE-bench Pro 差 3.6 分、NL2Repo 差 7 分——關鍵 task 仍該 fallback 商業 API
- **Qwen 是中國團隊開源**。Apache 2.0 license 沒問題，但特定合規情境（政府、國防、某些金融產品）仍會被法務擋
- **Dflash + DDTree 不是主流推理棧**。vLLM / TGI 還在追 block diffusion speculative decoding 的整合，生產環境有工程學習成本
- **136 t/s 是最佳配置**。換一組 prompt、換一種 quantization，跑出來可能只有 80 t/s——需要實測
- **官方 benchmark 有行銷成分**。Qwen 自己公布的數字，不等於你的 workload 上的真實表現

但即使把所有 caveat 打折，**「Sonnet 4.6 等級的 AI coding agent 可以在桌上那台小機器跑」**這個結論仍然成立。

### 架構藍圖要怎麼更新？

回到這篇「無聊 IT 架構」系列一貫在問的問題——**架構該長什麼樣？**

**舊的 on-prem AI coding 架構（2024–2025 版）：**

| 層級 | 硬體 / 服務 | 說明 |
|---|---|---|
| 運算層 | 中央 GPU Server（A100 × 4） | 投資約 300 萬台幣 |
| 存取方式 | SSH / 內部 API | 工程師搶 GPU quota |
| 瓶頸 | 並行 agent 跑不動 | rate limit 發生在內部 |

**新的 on-prem AI coding 架構（2026 版）：**

| 層級 | 硬體 / 服務 | 用途 |
|---|---|---|
| **工程師層（80% 任務）** | 每人一台桌面 AI 工作站（見下表） | 本地跑 Qwen 3.6-27B，autonomous agent 無限跑，不受 rate limit |
| **部門層（長 repo reasoning）** | 中央 GPU Server 跑 70B+ 大模型 | 處理跨 repo、長上下文任務 |
| **關鍵 fallback** | Claude Opus / Sonnet API | 合規允許時用於關鍵 task |
| **資料層** | Langfuse audit trail | 所有 prompt + response 留在公司網 |

**工程師層硬體選項對照（跑 Qwen 3.6-27B）：**

| 硬體 | 記憶體 | 頻寬 | 可跑量化 | 預期速度 | 售價（USD） | 適用情境 |
|---|---|---|---|---|---|---|
| **NVIDIA DGX Spark** | 128GB 統一記憶體 | LPDDR5X | FP8（27GB）+ 大 KV cache | **~136 t/s**（搭 Dflash+DDTree，10 agents 並行） | $4,699 | 重度 agent workload、平行吞吐 |
| **Mac Studio M3 Ultra 256GB** | 256GB 統一記憶體 | ~819 GB/s | 4-bit / 8-bit（Rapid-MLX 實測） | **36.5 t/s（4-bit）／ 18.9 t/s（8-bit）** | ~$5,599+ | macOS 生態、interactive + 中型 agent 並行 |
| **Mac mini M4 Pro 64GB** | 64GB 統一記憶體 | 273 GB/s | 4-bit / 8-bit | ~12–18 t/s（推估，社群實測仍少） | ~$2,199 | 個人開發者、interactive use |
| **Mac mini M4 Pro 48GB** | 48GB 統一記憶體 | 273 GB/s | 4-bit / 8-bit（context 要小心） | ~12–18 t/s（推估） | ~$1,799 | 預算型、短 context 任務 |
| **Mac mini M4 base** | 最多 32GB | 120 GB/s | 只能跑 4-bit（~15GB） | 明顯偏慢 | ~$1,299 | 品質打折，不建議 |

**選型 rule of thumb：**

- **要跑 autonomous agent（10 agents 並行、background task）→ DGX Spark**，搭 Dflash+DDTree 推理棧後平行吞吐碾壓所有 Mac
- **單人重度 coding + macOS 生態 → Mac Studio M3 Ultra**，4-bit 36.5 t/s 已經比 DGX Spark 不靠 DFlash 還快，pip install rapid-mlx 一行起跑
- **單人 interactive coding（IDE 裡叫一兩個 agent）→ Mac mini M4 Pro 64GB** 就夠用，便宜一半
- **預算 < $1,500 → 要嘛等 DGX Spark 二手、要嘛退回 Claude Code 訂閱制**。base Mac mini 跑 4-bit 27B 品質已經不是 Sonnet 4.6 等級了

這不是要全面取代商業 API，是**把 80% 的日常 agentic coding 負載搬回公司**，只把真正困難的 20% 留給 Claude / GPT。

這樣做的成本是原本的 20-30%，資料主權 100% 在手上，還不受 API 供應商脾氣影響。

---

## 常見問題 Q&A

**Q: 我們是金融 / 醫療 / 政府產業，Qwen 是中國模型，能用嗎？**

Apache 2.0 license 本身沒有地緣限制，但多數高度監管產業的法務會對「中國團隊訓練的權重」有疑慮。實務上建議走兩條路：一是等 Llama / Mistral 下一代追上（歷史經驗大約 2-3 個月落後），二是用 Qwen 3.6-27B 做內部非敏感工具的 pilot，確認流程跑得通再評估。

**Q: DGX Spark 買不到 / 預算擋不下來，有替代方案嗎？**

看預算和使用強度：

- **$2,000–$2,500 個人級：** Mac mini M4 Pro 64GB，單人 interactive use 夠用（12–18 t/s）。預算再緊一點可以退到 48GB 版本，但 context 會變窄
- **$4,000–$5,000 工作站級：** Mac Studio M3 Ultra（128/256GB 統一記憶體）跑 Qwen 3.6-27B，[Rapid-MLX 實測](https://github.com/raullenchai/Rapid-MLX/releases/tag/v0.6.1)4-bit 36.5 t/s、8-bit 18.9 t/s，macOS 生態對一般工程師更友善
- **既有 Windows / Linux 工作站改造：** RTX 5090（32GB GDDR7）單卡能跑 FP8 27B，配合 vLLM 吞吐量可達 100+ t/s，適合已經有桌機的團隊

需要 agent 並行和最高 t/s 還是 DGX Spark 最划算——128GB 統一記憶體 + FP4 petaFLOP 是 Mac mini / Mac Studio 硬追不上的。

**Q: Dflash + DDTree 這套推理棧現在穩定嗎？**

還不算主流。生產環境要用建議等一季——vLLM / SGLang 正在整合 block diffusion speculative decoding，到時候會有更成熟的部署方案。現在（2026 年 4 月）跑得動但要自己踩坑。

**Q: 那 Claude / Anthropic 是不是要完了？**

不會。Opus 4.6 / Opus 4.7 仍然是最強的 coding model，關鍵任務仍會跑在商業 API。但 **Anthropic 失去了「你別無選擇」的定價權**——這是結構性的改變。未來 API 定價壓力會更大，或者商業模型必須在 agentic workflow / tool ecosystem / enterprise features 上建立更深的護城河。對企業 IT 來講，這是好事。

---

## 結語

回到那條推文的終端機截圖：10 個 agent 同時跑，綠色數字停在 209 t/s，底下寫著 49W。

這張圖上的每個數字都不算驚天動地。但把它們擺在一起看——**27B dense 開源、Sonnet 4.6 等級的 benchmark、$4,699 的桌上機器、49W 的功耗、10 個 agent 並行**——就是一個結構性轉折點。

6 個月前，企業 IT 架構師要跟老闆解釋「為什麼我們該付 Anthropic 每個工程師 $7,500/年」。

6 個月後，問題反過來：**「為什麼我們還在付 Anthropic $7,500/年，而不是買一台 $4,699 的 DGX Spark？」**

這就是「無聊 IT 架構」文章每次在算的那個帳——架構決策不是跟風，是看數字什麼時候跨過 break-even 點。

2026 年 4 月，Qwen 3.6-27B 把這個點跨過去了。

---

## 延伸閱讀

- [企業級地端 LLM 系統架構藍圖](/local-llm-enterprise-architecture/)
- [AI Coding on-prem 的三條路](/ai-coding-on-prem-three-paths/)
- [ToolCall-15：本地模型 Tool Calling 實測，Qwen 27B 的 Sweet Spot](/toolcall-15-local-llm-tool-calling-qwen-27b-sweet-spot/)
- [Taalas ASIC：把 LLM 燒進晶片，推理成本的未來](/taalas-asic-burn-llm-into-silicon-local-inference-future/)
- [Qwen 團隊出走：開源治理危機](/qwen-team-exodus-open-source-governance-crisis/)

## 資料來源

- [Qwen 3.6-27B on Hugging Face](https://huggingface.co/Qwen/Qwen3.6-27B)
- [NVIDIA DGX Spark 產品頁](https://www.nvidia.com/en-us/products/workstations/dgx-spark/)
- [Claude Sonnet 4.6 Benchmark 數據](https://www.morphllm.com/claude-benchmarks)
- [DFlash 論文與原始碼](https://github.com/z-lab/dflash)
- [DDTree 研究頁面](https://liranringel.github.io/ddtree/)
- [Rapid-MLX v0.6.1 — Qwen 3.6 Day-0 Apple Silicon 實測](https://github.com/raullenchai/Rapid-MLX/releases/tag/v0.6.1)
- Mitko Vasilev X 推文（@iotcoi）、LotusDecoder、Chris Maddern（@chrismaddern）

---

🌐 **English Version:** [Qwen 3.6-27B Local Deployment: Sonnet 4.6-Class AI Agent Running on a DGX Spark / Mac mini](https://en.wiselychen.com/en/qwen-3-6-27b-sonnet-level-home-inference/)
