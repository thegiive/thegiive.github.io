---
layout: post
title: "AI Coding On-Prem 的三條路：雲端內網化、真地端、還是灰色折衷？"
date: 2026-01-22 08:00:00 +0800
categories: [IT架構, AI Coding]
tags: [On-Prem, Claude Code, Bedrock, Vertex AI, OpenCode, Ollama, 企業治理]
description: "On-Prem LLM 很火，但 AI Coding On-Prem 幾乎沒人講。關鍵差異在工具支持度——Tool Calling 精準度、多步驟推理、錯誤恢復能力，地端模型和雲端模型有巨大落差。模型可能有替代品，但 Claude Code 幾乎無可取代。本文分析三條路徑：雲端內網化（法務最好交代）、真 On-Prem（主權優先）、灰色折衷（技術可行但治理惡夢）。"
image: /assets/images/ai-coding-onprem-decision-framework.png
---

> 問題不是「能不能做」，而是「出事誰負責」

![AI Coding On-Prem 決策框架](/assets/images/ai-coding-onprem-decision-framework.png)

---

## 為什麼這篇文章很重要

**On-Prem LLM 很火，但 AI Coding On-Prem 幾乎沒人講。**

過去一年，Ollama、vLLM、llama.cpp 讓「地端跑 LLM」變得超簡單。隨便 Google 一下「Local LLM deployment」，教學文滿天飛。

但當你把場景從「聊天機器人」切換到「AI Coding Agent」，情況完全不同。

### 最關鍵的差異：工具支持度

AI Coding 不只是「呼叫 API 拿回文字」。它是 Agentic Workflow —— Agent 要讀檔案、寫程式碼、執行 bash 指令、自動修 bug。

這裡的核心不是「模型多聰明」，而是「工具鏈多穩定」。

- **Tool Calling 的精準度** — Agent 能不能正確解析 function schema、傳對參數？
- **多步驟推理的連貫性** — Agent 能不能在 10 個工具呼叫後還記得原始目標？
- **錯誤恢復能力** — bash 指令失敗了，Agent 會不會卡死？

這些能力，目前地端模型和雲端模型有**巨大落差**。

### 一個不爭的事實

**模型可能有替代品，Claude Code 幾乎無可取代。**

Opus 4.5 很強，但 Llama 3、Qwen、DeepSeek 也在快速追趕。模型層面，差距會逐漸縮小。

但 Claude Code 這個「Agentic 工具」不一樣。它不只是 API wrapper，而是一整套為 coding workflow 優化的：

- **上下文管理** — 自動決定哪些檔案要讀、哪些要忽略
- **工具定義** — 針對 coding 場景設計的 20+ 個原生工具
- **錯誤處理** — bash 失敗後的自動重試與 fallback 邏輯
- **Permission 系統** — 危險操作的確認機制

這些是 Anthropic 幾千個小時的工程累積。開源替代品（OpenCode、Aider）功能上可用，但成熟度差了一大截。

當然，看到 OpenCode 這樣的開源專案急起直追，我是很開心的。競爭會讓整個生態變好。但現階段如果要上生產環境，差距還是明顯存在。

**所以問題變成：「我想要 On-Prem，但又捨不得 Claude Code 的體驗」。**

這篇文章就是在回答這個問題。

---

**這裡有個市場空白：**

- 講 On-Prem LLM 的文章：**成千上萬**
- 講 AI Coding On-Prem 怎麼做的文章：**幾乎沒有**

為什麼？因為踩過坑的人發現：**技術上可行，治理上是惡夢。**

這篇文章是我和多家企業客戶討論後的總結。不是理論推演，是真實的企業需求和我們給的建議。

---

## TL;DR

- **路徑 1：雲端內網化（Claude Code + Bedrock/Vertex）** — 模型在雲端，控制面在公司，法務最好交代
- **路徑 2：真 On-Prem（OpenCode + Ollama）** — 資料零外流，但放棄 Claude Code，責任全在自己
- **路徑 3：灰色折衷（Claude Code + Proxy + Ollama）** — 技術可行，但官方不支援，出事沒人負責

**一句話結論：** 路徑 3 看起來兩全其美，但在稽核時無法 defend。

---

## 「On-Prem」不是單一技術需求

當企業說「我們要 On-Prem」，追問下去會發現其實是三件不同的事：

**治理需求（The Governance Need）**
> 我們可以上雲，但必須在我們的 VPC 裡跑，資料不能離開治理邊界。

**資安需求（The Security Need）**
> 我們的環境是 air-gapped，需要完全與網際網路物理隔離。

**UX/成本需求（The UX/Cost Need）**
> 我想用 Claude Code 的介面，但模型要跑在自己的 GPU 上省錢。

這三個需求，技術上都可以做到。但**治理層面的風險完全不同**。

---

## 核心問題：不是「能不能建」，而是「壞掉誰負責」

**技術現實（The Technical Reality）**

實作地端 LLM 現在技術上很簡單。Ollama 和本地量化讓部署變得即時。

**治理現實（The Governance Reality）**

挑戰在於「可防禦性」（Defensibility）。當 Agent 產生幻覺或失敗時，你能向董事會、法務、或稽核單位交代這個架構嗎？

本文從「責任歸屬」、「穩定性」、「治理」三個面向評估三種架構。

---

## 三條路線比較（快速版）

| 面向 | 路徑 1 雲端內網化 | 路徑 2 真 On-Prem | 路徑 3 灰色折衷 |
|------|-----------------|-----------------|------------|
| **Claude Code** | 官方支援 | 不可用 | 非官方 Hack |
| **模型品質** | 優 | 中 | 中下 |
| **Tool Calling 穩定度** | 優 | 中 | 低 |
| **法務風險** | 低 | 中 | **高** |

---

## 路徑 1：雲端內網化（企業標準）

### 一句話定義

> 模型在雲端，控制面在公司。

### 技術組合

- **Claude Code CLI** — Anthropic 官方工具
- **Amazon Bedrock / Google Vertex AI / Azure AI Foundry** — 模型託管
- **Enterprise LLM Gateway** — IAM / Audit / Proxy

### 架構

![Path 1: Cloud-Internalized Architecture](/assets/images/ai-coding-onprem-path1-cloud-internalized.png)

### 為什麼這是「可防禦」的選擇

對大多數企業來說，能產出審計軌跡的能力，遠比 token 成本重要。

**1. 官方支援**

使用原生參數如 `bedrock:anthropic...`。這不是 hack，是廠商設計好的企業用法。

```bash
# Amazon Bedrock
claude --model bedrock:anthropic.claude-3-5-sonnet-20241022-v2:0

# Google Vertex AI
claude --model vertex:claude-3-5-sonnet-v2@20241022
```

**2. Tool Calling 穩定度最高**

Agent 讀取檔案、執行 bash 指令、編輯程式碼的能力，是針對 Claude 模型特別優化的。穩定度在這裡最高。

**3. 審計軌跡完整**

依賴成熟的雲端基礎設施（AWS CloudTrail、Google Cloud Logging）來追蹤「誰在什麼時候呼叫了哪個模型」。

### 代價

- 依賴雲端廠商的 SLA
- 成本是 OpEx（按 token 計費），不是 CapEx

---

## 路徑 2：真 On-Prem（堡壘模式）

### 一句話定義

> 資料零外流，完全主權。

### 技術組合

- **OpenCode** — 社群開發的 Claude Code 替代品
- **Ollama** — 地端模型推理引擎
- **地端模型** — Llama 3、GLM-4、Qwen 等

### 架構

![Path 2: True On-Prem Architecture](/assets/images/ai-coding-onprem-path2-true-onprem.png)

### 主權的代價：你失去什麼

**1. 失去 Claude Code 軟體**

必須使用 OpenCode 等開源替代品。功能上可用，但缺乏官方 CLI 的精緻度、穩定度、和快速功能更新。

**2. Tool Calling 不穩定**

地端模型（GLM-4、Qwen）的 Function Calling 品質參差不齊。Agent 可能無法解析參數，或無法執行 Claude 原生處理的複雜多步驟任務。

**3. 自保風險**

沒有廠商 SLA。如果模型產生幻覺或基礎設施故障，你的內部團隊是唯一的支援線。你要自己扛 uptime。

### 目標使用情境

軍事、政府、高安全性研究環境的強制選項。

---

## 路徑 3：灰色折衷（陷阱）

### 一句話定義

> 官方介面，非官方模型，零保固。

### 技術組合

- **Claude Code** — Anthropic 官方 CLI
- **LiteLLM / Claude Code Proxy** — API 轉換層
- **Ollama** — 地端模型推理引擎
- **開源模型** — Llama 3、Qwen、DeepSeek 等

### 架構

![Path 3: The Grey Compromise Architecture](/assets/images/ai-coding-onprem-path3-grey-compromise.png)

### 「兩全其美」的假象

**吸引力（The Appeal）**

熟悉的 Claude UI + 低 Token 成本 + 資料隱私

**現實（The Reality）**

Demo 可以用，但對生產環境是治理惡夢。

**1. 脆弱性（Fragility）**

Anthropic 不支援這種用法。Claude Code 的一次更新就可能瞬間破壞 Proxy 相容性。

**2. Agent 失敗**

Claude Code 的 agentic 邏輯（規劃、編輯）是為 Claude 調校的。強迫它驅動 Llama 模型會導致迴圈中斷。

**3. 責任推諉（The Blame Game）**

- Anthropic 說：「這不是我們的配置」
- Proxy 開發者說：「Use at own risk」
- 模型供應商說：「這不是我們的整合」

**誰來負責？只有你自己。**

### 判決

可接受用於實驗；**對生產環境危險**。

---

## Tool Calling 風險：技術深潛

AI Coding 不只是聊天，而是 Agentic Workflow。

![Tool Calling Risk Comparison](/assets/images/ai-coding-onprem-tool-calling-risk.png)

**Claude + Claude（原生優化）：** 原生優化，高成功率。

**Claude 邏輯 + 地端模型（參數不匹配）：** 地端模型常常難以解析複雜的工具定義，導致 Agent「卡住」。

---

## 決策框架

![Strategic Decision Framework](/assets/images/ai-coding-onprem-decision-framework.png)

---

## 怎麼跟法務與資安說

**為路徑 1 辯護**

> 「我們使用官方 AWS/Google IAM 日誌進行審計。資料不離開 VPC 治理邊界。我們有廠商合約可以指向。」

**為路徑 2 辯護**

> 「我們保證資料零外流。即使網路線被切斷，系統仍能運作。我們接受內部維護的成本。」

**為什麼我們拒絕路徑 3**

> 「在稽核時無法防禦。我們無法回答『誰負責穩定性？』因為整合依賴不受支援的社群 Proxy。」

---

## 使用情境建議

**生產環境 → 路徑 1**

重點：安全性、穩定性、廠商問責

**高安全性 / 政府 / 軍事 → 路徑 2**

重點：主權 > UX。必須編列內部工程支援預算。

**實驗室 / PoC / 個人 → 路徑 3**

條件：必須有嚴格邊界。不整合進生產工作流程。預期會壞掉。

---

## 最終判決：治理 > 技術

如果你選擇路徑 3，問題不是「今天能不能用」，而是「明天能不能 defend」。

真正的企業架構需要清楚的責任邊界。

---

## 延伸閱讀

- [企業級地端 LLM 系統架構藍圖](/local-llm-enterprise-architecture/) — 如果選擇路徑 2，這篇講 Auth Gateway、LLM Router、Python 沙盒的設計
- [LiteLLM 官方文檔](https://docs.litellm.ai/) — 如果你還是想用路徑 3 做實驗
- [OpenCode GitHub](https://github.com/opencode-ai/opencode) — 路徑 2 的開源 Claude Code 替代品
