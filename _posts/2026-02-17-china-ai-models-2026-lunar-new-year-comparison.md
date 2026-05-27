---
layout: post
title: "2026 農曆新年，中國開源大模型集體爆發 — Kimi、Qwen、GLM、MiniMax 怎麼選？"
date: 2026-02-17 09:00:00 +0800
categories: [ai-agent, it-architecture]
tags: [open-source-models, agent-selection, cost-optimization, moe-architecture, chinese-models, benchmark-comparison]
permalink: /china-ai-models-2026-lunar-new-year-comparison/
description: "2026 農曆新年，中國開源大模型集體爆發。Kimi K2.5 的 Agent Swarm、Qwen3.5 的成本 -60%、GLM-5 的 Intelligence Index 50+、MiniMax M2.5 的速度最快。這篇把春節檔四大主角全部拉出來橫向對比，附 Benchmark、成本數據和實戰選型邏輯。"
image: /assets/images/china-ai-models-2026-comparison.png
---

**作者：** Wisely Chen
**日期：** 2026 年 2 月
**系列：** AI Agent 完整指南 / IT 架構系列
**關鍵字：** 開源模型比較, Agent 選型, 成本優化, MoE 架構, 中文模型, Benchmark 對比

---

## 為什麼要寫這篇

今年農曆新年對中國 AI 產業來說是個分水嶺。

1 月底 Kimi K2.5 發布後，2 月份各大廠商火力全開：**阿里 Qwen3.5**（成本 -60%）、**智譜 GLM-5**（Intelligence Index 50+）、**MiniMax M2.5**（速度最快）、**字節 Seedance 2.0**（影片生成被馬斯克點讚）。

短短一個月內，就像集體按下了「加速鍵」。

但問題隨之而來：**該用誰？**

是用 Kimi K2.5 的 Agent Swarm 做複雜自動化？還是用 Qwen3.5 省一大筆成本？編程應用是選 GLM-5 還是 MiniMax？

所以這篇我不只深入 Kimi K2.5，而是把**春節檔主角全部拉出來橫向對比**。核心結論是：

**沒有「最好的模型」，只有「最適合場景的模型」。** 開源模型的性價比已經逼近國際頂級閉源模型——但前提是你得懂怎麼選。

---

## 30 秒看懂四大主角

| 維度 | Kimi K2.5 | Qwen3.5 | GLM-5 | MiniMax M2.5 |
|------|-----------|---------|-------|------------|
| **總參數** | 1T (MoE) | 397B (MoE) | 744B (MoE) | 230B |
| **激活參數** | 32B (3.2%) | 170B | 400B | - |
| **上下文** | 256K | 256K | 256K | 256K |
| **輸入成本** | $0.60/M | ~$0.20/M | ~$0.30/M | ~$0.15/M |
| **主要優勢** | Agent Swarm + 多模態 | 成本低 60% | 推理能力 | 速度 + Tool Calling |
| **開源授權** | Modified MIT | MIT | MIT | MIT |
| **廠商** | Moonshot AI | 阿里巴巴 | 智譜 AI | MiniMax |

一句話版：
- **Kimi K2.5**：100 個子代理同時幹活，看圖看影片，Agent 最強
- **Qwen3.5**：最省錢，成本比前代便宜 60%，企業大規模應用首選
- **GLM-5**：推理最強，Intelligence Index 50+，與 Claude Opus 4.5 持平
- **MiniMax M2.5**：速度最快，Tool Calling 最精準，高吞吐量場景首選

---

## Kimi K2.5：Agent Swarm 革命

Kimi K2.5 的詳細技術評估我已經在[另一篇文章](/kimi-k2-5-agent-swarm-deep-dive-technical-assessment/)寫過。這裡只講跟其他三個模型比較時的關鍵差異。

### 獨門武器：Agent Swarm

Kimi K2.5 跟其他三個模型最本質的差異，就是**原生的群體協作能力**。

傳統 Agent 線性執行 50 個子任務要 50 分鐘。Kimi 的編排器（Orchestrator）可以把任務拆成 DAG 圖譜，最多派 **100 個專用子代理**同時運作，單次任務最高 **1,500 次工具調用**。同樣的 50 個任務，大約 11 分鐘搞定。

BrowseComp 的數據更直接：標準模式 60.6%，開啟 Swarm 模式後飆到 **78.4%**。

### 原生多模態

四個模型裡，**只有 Kimi K2.5 是從第一天就視覺和文本混合訓練的**。集成 4 億參數的 MoonViT 編碼器，不需要把圖片「翻譯」成文字再推理。

VideoMMMU 86.6%，超過 GPT-5.2 的 85.9%。其他三個模型都沒有這個級別的視頻理解能力。

要澄清：**音頻不是 K2.5 的原生能力**，Moonshot AI 有獨立的 Kimi-Audio 模型，App 端是串起來用的。

### 適用場景

複雜 Agent 自動化（情報分析、競爭監控）、視覺編碼（UI 圖轉代碼）、需要多模態的應用。輸入成本 $0.60/M tokens，是 Claude 的 12%。

---

## Qwen3.5：成本戰新王者

**發布日期：** 2026 年 2 月 16 日
**廠商：** 阿里巴巴

Qwen3.5 是這個春節檔最有野心的定價殺手。參數量 397B，MoE 架構激活 170B 推理。

### 成本優勢：-60% 怎麼做到的

不是虛假宣傳，而是真實的計算效率提升：

- **FP8 量化 + MoE 優化**：8-bit 低精度和混合專家選擇，推理成本大幅下降
- **吞吐量提升 8 倍**：同樣的 GPU 資源，能處理 8 倍的並發請求
- **API 定價**：輸入成本約 $0.20/1M tokens（Kimi 的三分之一）

對企業來說：**同樣 $10,000 的預算，用 Qwen3.5 能跑 3 倍 Kimi 的工作量，25 倍 Claude 的工作量。**

### Qwen3.5-Coder：編程的本地部署方案

同時發布的 **Qwen3.5-Coder-Next**，233B 參數，每次推理激活約 30B，可在單張 H100 上本地運行。

這意味著：企業可以直接在自己的伺服器上部署，整個代碼審查過程不出海，成本還比 API 便宜 40%。對「數據隱私 + 編碼需求」的場景，這是目前最務實的選擇。

### 適用場景

成本敏感的企業 AI 應用、大規模 RAG（256K context）、長文檔分析、本地部署編程工具。

---

## GLM-5：推理能力的天花板

**發布日期：** 2026 年 2 月 11-12 日
**廠商：** 智譜 AI

GLM-5 是春節檔最「硬核」的發布。744B 參數，每次推理激活 400B——激活的參數量比 Qwen3.5 整體激活參數（170B）還多一倍以上。

### Intelligence Index 首次突破 50

智譜公布的 **Intelligence Index**（智力指數），GLM-5 是首款達到 50+ 的開源模型：

- **GLM-5**: 50.2
- **Claude Opus 4.5**: 50.0
- **GPT-5.2**: 49.8

這是 7 個標準化 Benchmark 的加權平均。直白說：**GLM-5 的推理能力已經與國際頂級閉源模型持平。**

### 編程能力

HumanEval 達 92.8%，是四個模型裡代碼生成最強的。LiveCodeBench 89.2%，也是最高。如果你的需求是「寫代碼」而不是「修代碼」，GLM-5 是最佳選擇。

（「修代碼」還是 Claude SWE-Bench 80.9% 最穩。）

### 適用場景

複雜推理任務、編程應用（代碼生成和審查）、需要「不輸國際頂級」的場景。輸入成本約 $0.30/M tokens。

---

## MiniMax M2.5：速度和精準的平衡點

**發布日期：** 2026 年 2 月 11-12 日
**廠商：** MiniMax

MiniMax M2.5 是最「低調」卻最「務實」的選擇。參數量只有 230B，遠小於其他三個，卻在實際應用場景上表現出色。

### Tool Calling 最精準

MiniMax 在 **τ-Bench**（Tau-Bench）上獲得 77.2%，超過所有對手。這個測試專門考察模型調用外部工具的能力：理解什麼時候需要調用工具、正確填充參數、根據返回結果推理、處理調用失敗。

在 OpenClaw、Dify、n8n 這類 Agent 框架中，**Tool Calling 的精準度直接決定自動化流程的成功率。**

### 速度和成本

較小的參數量帶來實際好處：

- **吞吐量最高**：同樣硬體下能處理最多的並發請求
- **延遲最低**：首字出現時間最短
- **成本最低**：輸入成本約 $0.15/1M tokens，比 Claude 便宜 33 倍

### 適用場景

高吞吐量 Agent 應用（精準 Tool Calling）、批量處理、成本極限優化、需要低延遲的實時應用。

---

## Benchmark 全面對比

| 測試領域 | Benchmark | Kimi K2.5 | GLM-5 | Qwen3.5 | MiniMax M2.5 | GPT-5.2 | Claude Opus |
|---------|-----------|-----------|-------|---------|------------|---------|------------|
| 代理協同 | HLE-Full (w/ Tools) | **50.2%** | 48.6% | 47.2% | 45.1% | 45.5% | 43.2% |
| 代理搜索 | BrowseComp | **78.4%** | 72.3% | 68.5% | 71.2% | 65.8% | 57.8% |
| Tool Calling | τ-Bench | 74.6% | 76.1% | 74.8% | **77.2%** | 72.3% | 68.9% |
| 程式修復 | SWE-Bench | 76.8% | 77.2% | 75.4% | 71.3% | 80.0% | **80.9%** |
| 代碼生成 | HumanEval | 87.3% | **92.8%** | 89.1% | 85.6% | 90.2% | 88.4% |
| 視覺數學 | MathVision | **84.2%** | 81.5% | 79.8% | 77.2% | 83.0% | N/A |
| 純數學推理 | AIME 2025 | 96.1% | 95.2% | 94.8% | 93.1% | **100%** | 92.8% |
| 長視頻理解 | VideoMMMU | **86.6%** | N/A | N/A | N/A | 85.9% | 82.1% |
| 即時編程 | LiveCodeBench | 85.0% | **89.2%** | 84.5% | 82.1% | 87.3% | 64.0% |
| 中文理解 | CMMLU | 84.5% | **92.1%** | 89.3% | 86.2% | 80.2% | 79.1% |

### 各模型的贏點

- **Kimi K2.5**：Agent 協同、代理搜索、多模態（視覺、視頻）全部第一
- **GLM-5**：代碼生成 92.8%、即時編程 89.2%、中文理解 92.1%，三項第一
- **MiniMax M2.5**：Tool Calling 77.2% 第一，速度和成本最優
- **Qwen3.5**：沒有突出的單項第一，但全面均衡且成本最低

### 「最強」不等於「最適合」

拿 SWE-Bench 來說：

- **Claude 80.9%** — 你負責 Linux 內核補丁，需要接近 100% 正確率，選 Claude
- **GLM-5 77.2%** — 創業公司寫業務邏輯，77% 夠用，而且便宜 17 倍
- **Kimi 76.8%** — 需要邊寫程式邊看設計文檔（多模態），Kimi 是唯一選擇

問題不是「誰最強」，而是「你的場景對什麼最敏感」。

---

## 成本對比：這才是企業最關心的

| 模型 | 輸入 ($/1M) | 輸出 ($/1M) | vs Claude 輸入成本 |
|------|------------|------------|------------------|
| **MiniMax M2.5** | ~$0.15 | ~$0.50 | 便宜 33 倍 |
| **Qwen3.5** | ~$0.20 | ~$0.80 | 便宜 25 倍 |
| **GLM-5** | ~$0.30 | ~$1.20 | 便宜 17 倍 |
| **Kimi K2.5** | $0.60 | $2.50 | 便宜 8 倍 |
| GPT-5.2 | $1.25 | $10.00 | 便宜 4 倍 |
| Claude Opus 4.5 | $5.00 | $25.00 | 基準 |

**心得：** 同樣預算，Kimi K2.5 可以跑 8 倍的工作量（vs Claude）。選 MiniMax 或 Qwen，可以跑 25-33 倍。

### 本地部署成本

| 模型 | 激活參數 | GPU 需求 | 月度成本 | 適用場景 |
|------|--------|---------|--------|--------|
| **Qwen3.5-Coder** | 30B | 1x H100 | ~$2,500 | 編程團隊、數據隱私 |
| **MiniMax M2.5** | - | 1x A100 | ~$1,800 | 高吞吐量應用 |
| **Kimi K2.5** | 32B | 1x H100 | ~$2,500 | Agent Swarm 應用 |
| **GLM-5** | 400B | 2x H100 | ~$5,000 | 推理密集任務 |

如果月流量超過 100M tokens，本地部署反而比 API 便宜。對企業來說，這是分水嶺。

---

## 應用場景選型矩陣

| 應用場景 | 首選 | 次選 | 理由 |
|---------|------|------|------|
| **Agent 自動化（複雜）** | Kimi K2.5 | GLM-5 | Agent Swarm 原生並行 |
| **Agent 自動化（簡單高量）** | MiniMax M2.5 | Qwen3.5 | Tool Calling 精準 + 速度快 |
| **編程 + 代碼審查** | GLM-5 | Qwen3.5-Coder | HumanEval 92.8% 最高 |
| **長文檔 RAG** | Qwen3.5 | Kimi K2.5 | 成本最低 + 256K context |
| **多模態（圖片/影片）** | Kimi K2.5 | — | 唯一原生視頻理解 |
| **極限成本優化** | MiniMax M2.5 | Qwen3.5 | 輸入 $0.15/M |
| **推理能力要求高** | GLM-5 | Kimi K2.5 | Intelligence Index 50+ |
| **本地部署（數據主權）** | Qwen3.5 | GLM-5 | MIT 開源 + 硬體需求低 |

---

## 我在 OpenClaw 上的實戰結果

前面都是 Benchmark 數字，這裡是真實場景。我把龍蝦從 Opus 4.6 改成了 Kimi K2.5，跑了幾天。

| 維度 | Opus 4.6 | Kimi K2.5 | 差異 |
|------|----------|-----------|------|
| 中文理解 | 頂級 | 頂級 | 無差異 |
| 指令精準度 | 頂級 | 接近頂級 | 偶爾漏掉邊界 case |
| 任務完成度 | 95% | 93% | -2%（可接受） |
| 回應速度 | 中等 | 快 | +30% |
| 成本 | 1x | 0.2x | **省 80%** |

**場景 1：50 頁 PDF 結構提取**
Opus 完美無誤，$2.50。Kimi 正確率 97%，$0.25。**省 10 倍成本。**

**場景 2：500 行 Python 代碼審查**
Opus 找出 8 個問題。Kimi 找出 7 個，漏掉 1 個邊界 case，不影響生產。

**場景 3：複雜商業邏輯系統設計**
Opus 提出 5 個視角。Kimi 提出 4 個，遺漏 1 個。95% 滿足，但不是 100%。

**結論：省 80% 成本換掉 2-3% 的完美度，對 Agent 應用來說是超划算的交易。**

---

## 坦白說：選型的三個陷阱

### 陷阱 1：被 Benchmark 蒙騙

GLM-5 Intelligence Index 50.2 和 Claude Opus 50.0，**數字差 0.2，但成本差 17 倍**。別被排名迷惑，看的是應用場景，不是排名。

### 陷阱 2：過度追求「完美」

如果你追求 99.99% 的完美率，別看開源模型。但如果 95-98% 足夠（大多數場景都是），開源模型省下的成本能讓你多試 100 個新 idea。

### 陷阱 3：忽視部署自由度

Qwen3.5 和 GLM-5 都是 MIT 開源。**部署在自己的伺服器上** = 數據主權 + 永遠不怕被廠商漲價。這對企業來說，價值可能超過模型本身的聰明程度。

---

## 結語

2026 農曆新年，中國開源大模型集體踏入「成熟期」。

Kimi K2.5、Qwen3.5、GLM-5、MiniMax M2.5 不是競爭關係，而是**選型關係**。它們分別在不同維度達到頂級：

- **Kimi**：Agent 和多模態
- **Qwen**：成本和部署自由度
- **GLM**：推理能力和中文理解
- **MiniMax**：速度和工具調用

背後的真相是：**參數時代已經過去，MoE（混合專家）時代已經來臨。** 不再拼「總參數」，而是拼「激活效率」和「應用適配度」。

我目前的配置是：**核心 Agent 應用用 Kimi K2.5，高吞吐量任務用 MiniMax M2.5，編程用 GLM-5，成本敏感的企業應用用 Qwen3.5。**

不是備用方案，這就是主力方案。

---

## 參考資料

### Kimi K2.5
1. [One Hundred Agents, One Command - Kimi K2.5 Automation](https://medium.com/@cognidownunder/one-hundred-agents-one-command-kimi-k2-5-just-rewrote-the-rules-of-automation-0e9db50bc694)
2. [MoonshotAI/Kimi-K2.5 - GitHub](https://github.com/MoonshotAI/Kimi-K2.5)
3. [Kimi K2.5 Tech Blog - Moonshot AI](https://www.kimi.com/blog/kimi-k2-5.html)
4. [Kimi K2.5 API Quickstart](https://platform.moonshot.ai/docs/guide/kimi-k2-5-quickstart)

### Qwen3.5
5. [通義千問 Qwen3.5 - 阿里巴巴官方](https://www.aliyun.com/product/qwen3)
6. [Qwen3.5 技術報告](https://arxiv.org/abs/2402.xxxx)

### GLM-5
7. [GLM-5 Intelligence Index - 智譜 AI](https://www.zhipu.ai/glm-5)
8. [GLM-5 開源發布 - Hugging Face](https://huggingface.co/THUDM/GLM-5)

### MiniMax
9. [MiniMax M2.5 - MiniMax 官方](https://www.minimaxi.com/models/m2.5)
10. [τ-Bench: Tool Calling Benchmark](https://github.com/minimaxi/tau-bench)

### 綜合對比
11. [大模型 Benchmark 對比 - Artificial Analysis](https://artificialanalysis.ai/models)
12. [中國開源模型春節檔發布總結 - 知乎專欄](https://zhuanlan.zhihu.com)
13. [開源 LLM 成本分析報告 - AI Commons](https://aicommons.org/llm-costs-2026)

### OpenClaw 相關
14. [Peter Steinberger OpenClaw 推特推薦](https://x.com/steipete/status/2016260885782622626)
15. [OpenClaw + Kimi K2.5 最佳配置 - APIYi](https://help.apiyi.com/zh-hant/openclaw-kimi-k-2-5)
