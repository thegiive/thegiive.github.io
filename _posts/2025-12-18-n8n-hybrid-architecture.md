---
layout: post
title: "[保證無聊的技術架構篇] n8n 雲地混合架構：為什麼它不只是一個 Low-Code 工具"
date: 2025-12-18 10:00:00 +0800
permalink: /n8n-hybrid-architecture/
image: /assets/images/n8n-hybrid-architecture.png
description: "n8n 的底層是 DAG + 狀態機，Core/Worker 分離架構讓它天生適合雲地混合部署。企業可以把彈性放雲端、敏感資料留地端，Workflow 成為兩者的協調層。"
---

上次寫了「[非AI，保證內容很無聊的技術架構系列](https://ai-coding.wiselychen.com/on-premise-ocr-api/)」還寫得蠻開心，觸及率也還好，這次再來寫 n8n 的雲地混合架構。

很多人看 n8n，第一眼看到的是那個 UI 介面。然後就覺得：這是一個 low-code 自動化工具。

但是我覺得這個認知有點淺。n8n 目前確實都是小廠商在落地，但當你要在企業環境部署 n8n，特別是有「雲地整合」需求的時候，你需要理解它真正的架構。

---

## n8n 的底層：DAG + 狀態機

n8n 的底層，其實是 **DAG + 狀態機**。

當你畫完一個 workflow 按下執行，它會先「編譯」成 DAG（有向無環圖），標記每個節點的依賴關係。然後由 **Execution Orchestrator**（狀態機）負責調度，決定誰可以跑、誰要等。

真正執行的是 **Worker**，從 Redis queue 拿任務，跑完寫回 DB（這裡建議是 PostgreSQL）。

這個架構設計，讓 n8n 原生支援：
- **Retry 機制**：任務失敗可以自動重試
- **Error handling**：細粒度的錯誤處理
- **分支流程**：根據條件走不同路徑
- **長時間非同步任務**：不會 timeout，可以跑幾小時的任務

---

## Scale n8n 的正確姿勢

Scale n8n 的正確姿勢，跟很多人想的不一樣。

❌ 不是多開 workflow
❌ 不是把 Core 開很大
✅ 而是**只需要 scale Worker**

為什麼？因為 n8n 把「調度」和「執行」分開了。

- **Core 的工作量很小**，就是決定誰可以跑、維護 DAG 狀態
- **Worker 才是真正的瓶頸**，跑 API、跑 LLM、跑資料處理

所以在 production 環境，真正會 auto-scaling 的只有 Worker。Core 通常一台就夠，但 Worker 可能需要 10 台、20 台，根據負載動態調整。

這個設計很聰明：
- 調度邏輯集中，不會有分散式一致性問題
- 執行可以無限水平擴展
- 成本效益高，只 scale 真正需要的部分

---

## 企業導入最常被問的問題

企業導入時，被問最多的問題不是「能不能接某某 API」。

而是：
- **Key 放哪？** Credential 怎麼管理？
- **Workflow 會不會看到敏感資料？** 資料流經哪些節點？
- **能不能做環境隔離？** Dev / Staging / Prod 怎麼分？
- **能不能接地端大模型？** 讓 Worker 都在地端串地端系統

資安的議題我下次再討論，這次先講為什麼 n8n 很適合做雲地整合。

---

## 大部分企業的現實：雲地衝突

大部分企業的現實是這樣：

**地端需求：**
- 核心資料在地端（ERP、財務系統不能上雲）
- 法規合規要求（金融、醫療、政府）
- 既有投資的 legacy 系統

**雲端需求：**
- 流程與 AI 需要 scale（LLM、SaaS、突發流量）
- 彈性高，成本更可控
- 新服務快速上線

這兩個需求是衝突的。傳統解法是：要嘛全上雲（資安風險），要嘛全地端（失去彈性）。

---

## n8n 的 Hybrid 架構解法

n8n 因為 Core / Worker 分離，很自然成為 Hybrid 架構的中樞。

### 各層職責

**雲端負責：**
- n8n Core（彈性擴充、高可用）
- PostgreSQL（Workflow 定義、執行歷史）
- Redis（任務 Queue）
- OpenAI / SaaS 整合

**地端負責：**
- n8n Worker（執行敏感任務）
- ERP / 內部資料庫 / 敏感資料
- Local LLM（Ollama、vLLM 等）

**中間層：**
- VPN / Private Link / Webhook
- 地端的 Worker 需要能連回雲端的 Redis 拿任務

### 結果

這個架構的結果是：

1. **雲端負責彈性與擴充** — 流量大的時候可以快速 scale
2. **地端保留資料主權** — 敏感資料永遠不離開地端
3. **Workflow 成為兩者的協調層** — 一個 workflow 可以同時調度雲端和地端任務
4. **成本最佳化** — 只有需要彈性的部分放雲端

---

## n8n 的真正價值

n8n 的價值不在節點多不多。

在於它的**架構自由度**：
- **Self-host**：完全掌控部署環境
- **分離 Core/Worker**：靈活的混合部署
- **控制 credential**：敏感金鑰不離開特定環境
- **做雲地整合**：原生支援 Hybrid 架構

當你把它當成 **workflow execution platform**，而不是單純的自動化工具，很多企業級的解法自然就出現了。

---

## 結語

如果你正在評估有雲地整合需求的自動化工具，n8n 的架構值得認真看一下。

它不是最好用的 low-code 工具（Zapier、Make 的 UI 更友善），但它是目前少數能做到：

- ✅ 完全 self-host
- ✅ Core/Worker 分離部署
- ✅ 原生支援 Hybrid 架構
- ✅ 開源、可審計

對於有資安、合規、雲地整合需求的企業，這些特性比「節點數量」重要得多。

---

## 常見問題 Q&A

**Q: n8n 不就是 low-code 自動化工具嗎？**

表面上看是，但底層是 DAG + 狀態機架構。這讓它原生支援 Retry、Error handling、長時間非同步任務。當你要做企業級部署時，這些特性比 UI 更重要。

**Q: 為什麼 scale n8n 只需要 scale Worker？**

因為 Core 只負責調度（決定誰可以跑、維護 DAG 狀態），工作量很小。真正吃資源的是 Worker（跑 API、LLM、資料處理）。Core 一台就夠，Worker 可以根據負載動態擴展。

**Q: 什麼是雲地混合架構？為什麼 n8n 適合？**

雲地混合是讓彈性服務放雲端、敏感資料留地端。n8n 因為 Core/Worker 分離，天生適合：Core 放雲端負責彈性擴充，Worker 放地端處理敏感任務，Workflow 成為兩者的協調層。

**Q: n8n 跟 Zapier、Make 比，優勢在哪？**

Zapier、Make 的 UI 更友善，但 n8n 可以完全 self-host、Core/Worker 分離部署、原生支援 Hybrid 架構、開源可審計。對有資安合規需求的企業，這些比節點數量重要。
