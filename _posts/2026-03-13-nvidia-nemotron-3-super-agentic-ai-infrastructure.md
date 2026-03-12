---
layout: post
title: "NVIDIA Nemotron 3 Super：不是又一個大模型，是 Agentic AI 的水電瓦斯"
date: 2026-03-13 07:00:00 +0800
permalink: /nvidia-nemotron-3-super-agentic-ai-infrastructure/
image: /assets/images/nvidia-nemotron-3-super-cover.webp
description: "NVIDIA 發布 Nemotron 3 Super — 120B 參數、12B active、1M context window、完全開源。不是最聰明的模型，但可能是 Agentic AI 最需要的 workhorse。Benchmark 實測對比 Qwen3.5、MiniMax M2.5，加上 OpenClaw 三層路由實戰配置建議。"
---

NVIDIA 今天發布了 Nemotron 3 Super，120B 參數、12B active、1M context window、開源。

看到這些數字，你可能覺得「又一個大模型發布」。但我看完技術細節後的第一反應是：**NVIDIA 終於正式承認了 Agentic AI 的兩個致命瓶頸。**

而且不只是承認，他們給出了具體數字。

---

## Agentic AI 的兩個痛，終於有人說出口

### 痛點一：Context Explosion — 15x Token 膨脹

NVIDIA 在公告裡明確寫了一個數字：**multi-agent workflows generate up to 15x more tokens than standard chat**。

15 倍。

這不是理論推算，是他們跟企業客戶合作後觀察到的實際數據。每一次 agent 互動都要重新傳送完整的歷史記錄、工具輸出、中間推理過程。一個原本 1000 token 的對話，在 multi-agent 架構下可以膨脹到 15,000 token。

更致命的是 **Goal Drift** — 當 context 越來越長，agent 會逐漸偏離原始目標。這不是 hallucination，是結構性的失焦。你讓三個 agent 協作完成一個任務，跑了十幾輪之後，第三個 agent 可能已經忘了最初到底要做什麼。

做過 multi-agent 系統的人應該都遇過這個問題。我在之前分析 Stanford 和 Harvard 那篇「Agents of Chaos」論文時就提過，multi-agent 的結構性不穩定性是真實存在的。現在 NVIDIA 用商業化的語言重新確認了這件事。

### 痛點二：Thinking Tax — 不是每個 subtask 都需要 frontier model

第二個痛點叫 **Thinking Tax**。Complex agents 每一步都需要推理，但如果每個 subtask 都用最大的模型，整個 multi-agent 系統會變得又貴又慢。

這其實就是 **OneFlow** 那篇論文在講的事 — 單一 agent 用一個夠強的模型，可能比多個 agent 各自推理更有效率。NVIDIA 的解法不同，他們不是回到單一 agent，而是做一個「推理成本極低但準確度不差」的模型，讓你可以在 multi-agent 裡大量使用而不心痛。

---

## 五層技術堆疊：為什麼不只是「又一個 MoE」

Nemotron 3 Super 的架構有五個值得注意的設計決策：

### 1. Hybrid Architecture: Mamba + Transformer

這可能是最有趣的設計。不是純 Transformer，也不是純 Mamba，而是混合。

- **Mamba layers** — 負責高效的序列處理，4x memory and compute efficiency
- **Transformer layers** — 負責需要深度推理的部分

為什麼混合？因為 Agentic AI 的 workload 本質上就是混合的。大部分時間 agent 在處理大量的 context（適合 Mamba 的線性注意力），但關鍵決策點需要 full attention 的推理能力（適合 Transformer）。

### 2. MoE: 120B Total, 12B Active

120B 參數裡只有 12B 在推理時活躍，10:1 的比例。

對比一下：
- **GLM-5** — 744B total, 40B active（18.6:1）
- **Nemotron 3 Super** — 120B total, 12B active（10:1）
- **Qwen 3.5-9B** — 9B total, 9B active（Dense，1:1）

三條完全不同的路線。GLM-5 走超大規模 MoE，Qwen 走精煉 Dense，NVIDIA 走中間路線。

### 3. Latent MoE — 四個 Expert 的能力，一個的成本

這是 Nemotron 3 Super 的獨特創新。在生成下一個 token 時，啟動 4 個 expert specialists，但只付 1 個的計算成本。

具體怎麼做到的 NVIDIA 還沒公開完整論文，但這個方向很有意思 — 不是減少 expert 數量，而是讓多個 expert 的啟動成本趨近於一個。

### 4. Multi-Token Prediction — 3x 推理加速

同時預測多個未來的 token，而不是一次只預測一個。這帶來 3x 的推理速度提升。

結合 Blackwell 平台的 NVFP4 精度，整體推理速度比 Hopper 上的 FP8 快 4 倍，而且不損失準確度。

### 5. 1M Token Context Window

一百萬 token 的 context window。一個完整的 codebase 可以直接塞進去，不需要切割。

NVIDIA 的用詞是 "preventing goal drift" — 因為所有的 workflow state 都在記憶體裡，agent 不會忘記自己在做什麼。

---

## Benchmark 實測：到底在哪裡贏、在哪裡輸？

光看 NVIDIA 自己的公告會以為這個模型什麼都好。但把第三方 benchmark 攤開看，真相更有趣。

### 跟同級開源模型的硬碰硬

| Benchmark | Nemotron 3 Super | Qwen3.5-122B | GPT-OSS-120B | MiniMax M2.5 |
|-----------|-----------------|--------------|--------------|--------------|
| **SWE-Bench Verified** | 60.47% | 66.40% | — | **80.2%** |
| **MMLU-Pro** | 83.73 | **86.70** | — | — |
| **GPQA** | 79.23 | **86.60** | — | — |
| **HMMT (數學推理)** | **93.67** | 91.40 | — | — |
| **LiveCodeBench** | **81.19** | 78.93 | — | — |
| **RULER @1M tokens** | **91.75%** | 91.75% | 22.30% | — |
| **Function Calling (BFCL)** | — | — | — | **76.8** |
| **PinchBench (Agent)** | **85.6%** | — | — | — |
| **Artificial Analysis Intelligence** | 36 | — | 33 | **42** |

幾個值得注意的模式：

**Nemotron 3 Super 贏在哪？**
- **吞吐量碾壓** — 451.7 tokens/sec，同級開源模型中位數只有 76.5 t/s（快 6 倍）
- vs GPT-OSS-120B 快 **2.2x**，vs Qwen3.5-122B 快 **7.5x**
- TTFT 只要 **0.56 秒**（同級中位數 1.46 秒）
- 長 context recall（RULER @1M）**91.75%**，GPT-OSS-120B 只有 22.30% — 直接碾壓
- 數學推理（HMMT）和 LiveCodeBench 微幅領先 Qwen3.5

**Nemotron 3 Super 輸在哪？**
- SWE-Bench 只有 60.47% — **MiniMax M2.5 的 80.2% 高出 20 個百分點**，Qwen3.5 的 66.40% 也明顯領先
- MMLU-Pro 和 GPQA 都輸給 Qwen3.5，差距不小（3-7 分）
- Artificial Analysis Intelligence Index 36 分 — MiniMax M2.5 拿 42 分，Gemini 3.1 Pro 和 GPT-5.4 更是 57 分

### MiniMax M2.5：真正的對比對象

MiniMax M2.5 值得單獨拿出來比，因為它跟 Nemotron 3 Super 都是 MoE 架構、都瞄準 Agentic AI：

| 維度 | Nemotron 3 Super | MiniMax M2.5 |
|------|-----------------|--------------|
| **總參數** | 120B | 230B |
| **Active 參數** | 12B (10%) | 10B (4.3%) |
| **架構** | Mamba + Transformer + MoE | MoE |
| **SWE-Bench** | 60.47% | **80.2%** |
| **Function Calling** | — | **76.8** (勝 Claude 4.6) |
| **Context Window** | 1M | 1M |
| **Output Speed** | **451.7 t/s** | — |
| **Training Data 公開** | **Yes (10T+)** | No |
| **OpenHands Index** | — | **第 4 名**（僅次 Opus 4.6、GPT-5.2 Codex） |

結論很清楚：**MiniMax M2.5 是更強的 agent brain，Nemotron 3 Super 是更快的 agent workhorse。**

如果你的 multi-agent 系統需要一個「主腦」做複雜推理和 coding — M2.5 更適合。如果你需要大量 subtask 並行、每分鐘處理上千次推理呼叫 — Nemotron 3 Super 的吞吐量優勢更明顯。

實務上最佳策略可能是混搭：**M2.5 當 orchestrator，Nemotron 3 Super 當 worker。** 這恰好呼應了 NVIDIA 自己說的 Thinking Tax 問題 — 不是每個 subtask 都需要最聰明的模型。

---

## 真正值得關注的：Open Weights + Open Data + Open Recipes

NVIDIA 這次不只是開源模型權重。他們公開了：

- **Open weights** — permissive license
- **10T+ tokens** 的 pre-training 和 post-training datasets
- **15 個 RL training environments**
- **完整的 evaluation recipes**

這跟 Meta 的 Llama 開源策略不同。Meta 開源模型權重但不開源訓練數據。NVIDIA 這次是把「怎麼訓練的」也全部攤開。

從企業角度看，這意味著你可以拿 NeMo 平台去 fine-tune，甚至用他們的 methodology 訓練自己的版本。

---

## 企業生態系：已經不是「即將推出」，是「今天就能用」

這篇公告最讓我注意的不是技術，是企業採用的深度。

**AI-Native 公司：**
- Perplexity AI — 搜尋引擎底層
- CodeRabbit, Factory AI, Greptile — AI coding agents（CodeRabbit 我們在 ATPM 框架裡用過）
- Edison Sciences, Lila Sciences — 生命科學

**傳統企業：**
- Amdocs（電信）、Palantir（網安）、Cadence（半導體設計）、Dassault 3DS 和 Siemens（製造）

**雲端與推理服務：**
- Google Cloud Vertex AI、Oracle Cloud — 已上線
- AWS Bedrock、Azure — 即將上線
- CoreWeave、Crusoe、Nebius、Together — 已上線
- 加上 Baseten、Cloudflare、DeepInfra、Fireworks 等十多家 inference provider

**硬體合作：**
- Dell — Enterprise Hub，on-premise 部署
- HPE — agents hub

這個生態系的廣度說明一件事：**Agentic AI 的基礎設施層正在快速標準化。**

---

## 坦白說

### 讓我興奮的

1. **15x token 膨脹** 這個數字被 NVIDIA 官方確認，以後跟企業客戶解釋 multi-agent 成本時有了權威出處
2. **Mamba + Transformer hybrid** 是正確的方向，Agentic workload 本質上就是混合型的
3. **完全開源（含訓練數據和 recipes）** 比 Meta Llama 更徹底

### 讓我存疑的

1. **DeepResearch Bench 第一名** — 是搭配 NVIDIA AI-Q agent 系統的成績，不是 Nemotron 3 Super 單模型的能力。這個描述容易誤導
2. **Latent MoE 的具體實現** 還沒有完整論文，「4 個 expert 的能力，1 個的成本」聽起來太好，需要看細節
3. **1M context window 的實際品質** — 有 window 不代表 1M token 範圍內的 recall 都是可靠的。Needle-in-a-haystack 測試結果呢？
4. **SWE-Bench 60.47% 是個問題** — MiniMax M2.5 拿 80.2%，差距 20 個百分點。如果你的 agent 主要任務是寫 code，Nemotron 3 Super 可能不是正確的選擇

### 我的判斷

Nemotron 3 Super 不是要跟 GPT-5 或 Claude Opus 搶「最聰明」的位置。它的定位是 **Agentic AI 系統裡的 workhorse** — 不是最強，但夠強、夠快、夠便宜、context window 夠大。

這跟 Jensen Huang 在 Cisco AI Summit 講的「domain expertise becomes the new IP」是一脈相承的。NVIDIA 不只賣 GPU，他們在定義 Agentic AI 的基礎設施標準 — 從硬體（Blackwell）到軟體（NIM microservice）到模型（Nemotron）。

---

## 實戰場景：OpenClaw 的三層路由怎麼用？

講完理論，來看一個具體的應用場景。OpenClaw 已經有成熟的 **三層模型路由（Three-Tier Routing）** 架構，Nemotron 3 Super 剛好可以塞進去。

### OpenClaw 目前的三層路由

| Tier | 用途 | 目前常用模型 | 成本比 |
|------|------|------------|--------|
| **Tier 1** | 架構決策、複雜重構、安全分析 | Claude Opus 4.6 / GPT-5.2 | 100% |
| **Tier 2** | Code generation、research、drafting | Claude Haiku / DeepSeek / Kimi K2.5 | 2-10% |
| **Tier 3** | 分類、heartbeat、簡單查詢 | Gemini Flash / Ollama local | 0-1% |

這個路由策略已經被驗證過：從 Opus-only 切換到三層路由，成本從 **$1,500 降到 $50/月**，省了 97%。

### Nemotron 3 Super 該放在哪一層？

**答案是 Tier 2 — 日常工作層。**

為什麼不是 Tier 1？
- SWE-Bench 60.47% — 跟 Opus 4.6 的 80.8% 差距太大，複雜 coding 任務不夠可靠
- MMLU-Pro、GPQA 都不是頂尖，深度推理還是交給 frontier model

為什麼不是 Tier 3？
- 451.7 t/s 的吞吐量放在 heartbeat 層是殺雞用牛刀
- 12B active 參數的能力遠超 Gemini Flash-Lite 或 llama3.2:3b

為什麼 Tier 2 最適合？
1. **吞吐量 451.7 t/s** — Tier 2 的任務量大但不需要最深度推理，速度比準確度重要
2. **1M context window** — OpenClaw 有 pre-emptive memory flush 機制，是為了應對 context 不夠用的問題。1M window 可以大幅減少 flush 頻率，agent 的「記憶」更完整
3. **12B active 參數** — 成本極低，符合 OpenClaw「When in doubt, use Haiku first」的預設便宜原則
4. **開源可自建** — OpenClaw 已經支援 Ollama local 部署，Nemotron 開源意味著可以完全 on-premise，不走 API

### 建議配置

```
Tier 1: Claude Opus 4.6 / MiniMax M2.5
        → 架構決策、複雜重構、安全分析

Tier 2: Nemotron 3 Super（取代 Haiku/DeepSeek）
        → code generation、data research、drafting
        → 吞吐量優勢讓批量任務快 6 倍

Tier 3: Gemini Flash-Lite / Ollama llama3.2:3b
        → heartbeat、分類、簡單查詢
```

### 被忽略的戰略價值：純美制開源的唯一地端選項

OpenClaw 的 `openclaw.json` 透過 API endpoint 配置模型路由。Nemotron 3 Super 已經有十多家 inference provider（Baseten、Cloudflare、DeepInfra、Fireworks 等），所以 **API 接入不是問題**。

但更值得注意的是一個容易被忽略的事實：**如果你需要「純美制」的開源地端模型，Nemotron 3 Super 可能是 OpenClaw 目前唯一的選擇。**

把目前 OpenClaw 生態裡的開源模型攤開看：

| 模型 | 來源 | 開源 | 地端可行 | 能力等級 |
|------|------|------|---------|---------|
| **Nemotron 3 Super** | NVIDIA（美國） | ✅ | ✅ | Tier 2 |
| GPT-OSS-120B | OpenAI（美國） | ✅ | ✅ | ⚠️ 已過時（RULER @1M 只有 22%） |
| MiniMax M2.5 | MiniMax（中國） | ✅ | ✅ | Tier 1-2 |
| Qwen 3.5 | 阿里巴巴（中國） | ✅ | ✅ | Tier 1-2 |
| DeepSeek V3 | DeepSeek（中國） | ✅ | ✅ | Tier 2 |
| Kimi K2.5 | Moonshot AI（中國） | ✅ | ✅ | Tier 2 |
| Claude Opus 4.6 | Anthropic（美國） | ❌ | ❌ | Tier 1 |
| GPT-5.2 | OpenAI（美國） | ❌ | ❌ | Tier 1 |
| Gemini 3 Flash | Google（美國） | ❌ | ❌ | Tier 2-3 |

看到了嗎？在「美國來源 + 開源 + 能力還行」這個交集裡，扣掉已經過時的 GPT-OSS-120B（長 context 幾乎不能用），**只剩 Nemotron 3 Super**。

這對某些企業場景是關鍵的：
- **政府標案或國防相關** — 不能用中國來源的模型，也不能走 API（資料不能離境）
- **金融機構合規** — 監管要求模型來源可追溯，且資料不能上雲
- **台灣的資安法規趨勢** — 關鍵基礎設施越來越要求「可控來源」的 AI 供應鏈

NVIDIA 開源了完整的 training data（10T+ tokens）和 training recipes，這在合規審查時是加分項 — 你可以說清楚這個模型是怎麼訓練的、用了什麼資料。MiniMax M2.5 雖然也開源權重，但訓練數據不公開，在嚴格的合規環境下會被打問號。

### 地端部署的現實

說回部署門檻：120B MoE 模型即使只有 12B active，完整模型檔案還是很大。不像 MiniMax M2.5 可以 3-bit 量化到 101GB 跑在 128GB Mac 上。Nemotron 3 Super 的 local 部署需要更高的硬體規格，可能需要多張 GPU。

但換個角度想 — 如果你的場景就是「純美制 + 地端 + 開源」，**你沒有其他選擇**。這不是「要不要用」的問題，是「只能用它」的問題。

對大多數 OpenClaw 用戶來說，**透過 API 使用 Nemotron 3 Super 作為 Tier 2 workhorse** 是最務實的選擇。但對有合規需求的企業來說，它可能是 **唯一的選擇**。

---

## 對我們的意義

如果你在做 multi-agent 系統：

1. **Token 膨脹問題** — 15x 這個數字要記住，做成本估算時用得到
2. **模型選型策略** — 不是所有 subtask 都需要 frontier model。Nemotron 3 Super 這類「高效率 workhorse」才是 multi-agent 架構真正需要的
3. **Context window 的用法** — 1M token 不是用來塞更多 prompt，是用來維持 agent 的 workflow state，防止 goal drift
4. **開源生態** — 完全開源意味著你可以 fine-tune、自建。對有隱私需求的企業來說，這比用 API 重要
5. **三層路由是標配** — OpenClaw 已經驗證了這個模式。Nemotron 3 Super 的定位就是 Tier 2 workhorse，不要拿它當 Tier 1 用

---

## 關鍵數字速查

| 指標 | 數值 |
|------|------|
| 總參數量 | 120B |
| 活躍參數量 | 12B (10%) |
| Context Window | 1M tokens |
| Output Speed | 451.7 t/s（同級中位數 76.5 t/s） |
| Throughput vs GPT-OSS-120B | 2.2x |
| Throughput vs Qwen3.5-122B | 7.5x |
| RULER @1M tokens | 91.75% |
| SWE-Bench Verified | 60.47%（MiniMax M2.5: 80.2%） |
| HMMT 數學推理 | 93.67（Qwen3.5: 91.40） |
| Multi-Token Prediction 加速 | 3x |
| Blackwell NVFP4 vs Hopper FP8 | 4x faster |
| Multi-agent token 膨脹 | 15x vs standard chat |
| Training data | 10T+ tokens |
| RL environments | 15 |
| License | Permissive (open weights) |

---

*Nemotron 3 Super 的發布，標誌著 Agentic AI 從「概念驗證」進入「基礎設施標準化」的階段。不是模型越大越好，而是模型要為系統架構服務。這可能是 2026 年最重要的一次模型發布 — 不是因為它最強，而是因為它最務實。*
