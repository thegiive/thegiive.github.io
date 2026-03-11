---
layout: post
title: "Harness Engineering 架構全景：AI 可以寫 Code，但不能自己上 Production"
date: 2026-03-11 10:00:00 +0800
categories: [AI Coding, AI Architecture]
tags: [Harness Engineering, AI Coding, Control Plane, CI/CD, Amazon AI incident, OpenAI Codex, Agent Engineering, 四層防禦, 分級審查, production guardrails, Context Engineering, AGENTS.md, 駕馭工程]
permalink: /harness-engineering-architecture-overview-ai-code-production-guardrails/
image: /assets/images/harness-engineering-architecture-cover.png
description: "亞馬遜讓 AI 修 bug，AI 刪掉整個生產環境。DataTalks.Club 被 AI 刪掉整個資料庫。電商部門因 AI 變更丟失數百萬筆訂單。三起事件，同一個模式：reset → rebuild → clean state。這篇文章用一張架構圖講清楚 Harness Engineering 的全貌：從 Amazon 的禁令到 OpenAI 的控制平面，從四層防禦到七元件參考架構，從五大失效模式到你的團隊明天就能開始做的三件事。"
---


> 亞馬遜讓 AI 修 bug，AI 刪掉整個生產環境。DataTalks.Club 被 AI 刪掉整個資料庫。電商部門因 AI 變更丟失數百萬筆訂單。三起事件，同一個模式：reset → rebuild → clean state。AI 面對複雜問題時，會本能地選擇「最乾淨的解法」——但對生產系統來說，這是災難。問題從來不是「AI 能不能寫 code」，而是「你的系統準備好接住 AI 了嗎」。這篇文章用一張架構圖講清楚 Harness Engineering 的全貌：從 Amazon 的禁令到 OpenAI 的控制平面，從四層防禦到七元件參考架構，從五大失效模式到你的團隊明天就能開始做的三件事。

**作者：** Wisely Chen
**日期：** 2026 年 3 月
**系列：** AI Coding 架構觀察
**關鍵字：** Harness Engineering, AI Coding, Control Plane, CI/CD, Amazon AI incident, OpenAI Codex, Agent Engineering, 四層防禦, 分級審查, production guardrails, Context Engineering, AGENTS.md, 駕馭工程

---

## 目錄

- [為什麼需要這篇文章](#為什麼需要這篇文章)
- [AI 的行為模式：它不是故意的，但它會刪掉你的資料庫](#ai-的行為模式它不是故意的但它會刪掉你的資料庫)
- [兩種應對策略：禁令 vs. 系統](#兩種應對策略禁令-vs-系統)
- [Harness Engineering 到底是什麼？先講清楚定義](#harness-engineering-到底是什麼先講清楚定義)
- [七元件參考架構：完整的 Harness 長什麼樣](#七元件參考架構完整的-harness-長什麼樣)
- [三層防禦架構：從策略到執行到生命週期](#三層防禦架構從策略到執行到生命週期)
- [五大失效模式：Harness 會怎麼壞掉](#五大失效模式harness-會怎麼壞掉)
- [架構護欄的落地工具](#架構護欄的落地工具)
- [三種規模的導入路線圖](#三種規模的導入路線圖)
- [你的團隊明天就能做的三件事](#你的團隊明天就能做的三件事)
- [坦白說](#坦白說)
- [延伸閱讀](#延伸閱讀)

---

## 為什麼需要這篇文章

最近我在 LinkedIn 上分享了亞馬遜對 AI coding 上安全鎖的事，迴響超出預期。

很多人的反應是：「對，我們團隊也遇到類似的問題。」

然後接下來的問題幾乎都一樣：「所以到底該怎麼辦？」

我之前已經寫過三篇相關的深度文：[Amazon 事件分析](/amazon-ai-code-incident-tech-giants-quietly-locking-ai/)、[四層防禦架構](/coders-who-stopped-coding-harness-context-spec-engineering/)、[Control Plane 八步拆解](/harness-engineering-control-plane-pattern-agent-review-loop/)。但這三篇加起來超過一萬字，而且是按時間順序寫的，不是按架構邏輯。

這篇要做的事很簡單：**用一張圖、一套架構、一條路線圖，把 Harness Engineering 的全貌講清楚。**

讓你不需要讀完三篇長文，就能理解「Harness Engineering 是什麼、為什麼需要、怎麼開始」。

---

## AI 的行為模式：它不是故意的，但它會刪掉你的資料庫

先講清楚一件事：AI 不是「壞」，它只是跟人類有不同的問題解決傾向。

最近三起事件暴露了同一個行為模式：

| 事件 | 規模 | AI 的「解法」 | 後果 |
|------|------|--------------|------|
| DataTalks.Club | 社群專案 | 刪掉資料庫 | 資料永久丟失 |
| AWS 生產環境 | 雲服務 | 刪掉整個環境重建 | 13 小時中斷 |
| 亞馬遜電商 | 企業核心 | AI 變更導致 outage | 數百萬筆訂單丟失 |

模式是 **reset → rebuild → clean state**。

![AI 的乾淨狀態偏見：三起事件同一個模式](/assets/images/harness-engineering-slide-02.png)

AI 模型在訓練過程中學到了大量「乾淨狀態」的概念。當它遇到一個複雜的修復問題時，「刪掉重來」在它的邏輯裡是一個合理的解法——乾淨、確定、沒有殘留問題。

對 AI 來說，刪掉一個資料庫跟刪掉一個暫存檔，認知成本是一樣的。**它不理解「這裡面有十萬筆用戶資料」的重量。**

所以問題不是「AI 能不能寫 code」——它能，而且越來越好。

問題是：**當 AI 提出「刪掉整個生產環境再重建」這種方案的時候，誰來攔住它？**

---

## 兩種應對策略：禁令 vs. 系統

面對這個問題，現在市場上出現了兩種截然不同的應對策略。

### 策略 A：亞馬遜的禁令

「禁止初級和中級工程師在沒有資深工程師簽字的情況下，提交任何 AI 生成的程式碼。」

方向是對的——承認 AI 需要護欄。但有三個結構性問題：

1. **資深工程師變瓶頸。** 每段 AI 程式碼都要 Senior 簽字，Senior 很快就會變成整條流水線最慢的環節。最終 Senior 也會開始「快速掃過」——心理學叫這個 automation complacency。
2. **切斷學習管道。** 初級工程師用 AI 探索解決方案是重要的學習方式。禁止等於切斷這個管道。
3. **沒解決根本問題。** 根本問題不是「誰提交程式碼」，而是「AI 生成的變更在進入生產環境之前，經過了多少層驗證」。

### 策略 B：Harness Engineering

OpenAI 工程團隊走了完全不同的路。3 個人、5 個月、100 萬行代碼、0 行人寫。他們把這套方法叫 Harness Engineering。

核心哲學八個字：**Humans steer. Agents execute.**

不是「人類禁止 Agent」，也不是「Agent 自由奔跑」。是**人類建好框架，Agent 在框架裡全速運轉**。

兩種策略的對比：

| | 亞馬遜的禁令 | Harness Engineering |
|---|---|---|
| **護欄方式** | 人的注意力 | 系統的架構 |
| **策略** | 限制人（禁止初中級提交） | 限制變更（用架構約束框住 Agent） |
| **速度** | 降速（人工瓶頸） | 加速（Agent 犯錯時，修復指令自動注入 context） |
| **學習** | 切斷初級工程師學習管道 | Agent 每次犯錯都被框架糾正，越跑越穩 |
| **擴展性** | 資深工程師成為瓶頸 | Peter Steinberger 一人一天 627 次提交 |
| **疲勞** | 人的注意力會疲勞、自滿 | 系統架構不會 |

**禁令是用人去擋。Harness Engineering 是用系統去接。**

![兩種防禦哲學的對決：人為禁令 vs. 系統框架](/assets/images/harness-engineering-slide-03.png)

---

## Harness Engineering 到底是什麼？先講清楚定義

很多人把 Harness Engineering 跟 Prompt Engineering 搞混。其實兩者是完全不同層次的東西。

### 正式定義

Harness Engineering（駕馭工程）是：**在 agent-first 軟體開發中，建構一套控制與放大 agent 交付能力的工程學。**

它要回答的不是「agent 能不能寫出某段 code」，而是「在大量 PR、高吞吐與長時間自動執行下，如何確保一致性、可維護性、安全性與可觀測性」。

Martin Fowler 網站上，Thoughtworks 傑出工程師 Birgitta Böckeler 把 OpenAI 的做法歸納為三大類 harness 元件：

1. **Context Engineering（上下文工程）**：策展 agent 看到的內容，讓它能做出更好的決策
2. **Architecture Constraints（架構約束）**：用機械化的規則強制依賴方向、分層邊界
3. **Garbage Collection（垃圾回收）**：持續對抗 agent 高速產出帶來的熵增

### 跟 Prompt Engineering 的差別

| | Prompt Engineering | Harness Engineering |
|---|---|---|
| **層次** | 對話層（一次性指令） | 系統層（可重複運行的工程體系） |
| **目標** | 讓 AI 理解這次要做什麼 | 讓 AI 在任何時候都能可靠地工作 |
| **持久性** | 每次對話重新來 | 沉澱在 repo 裡，越用越好 |
| **可驗證** | 難以機械驗證 | 可以用 CI 自動檢查 |

簡單講：Prompt Engineering 是「每次跟 AI 說話的技巧」。Harness Engineering 是「建構一個系統，讓 AI 不需要你每次都盯著，也能可靠地產出」。

![從對話技巧走向工程體系：Prompt Engineering vs Harness Engineering](/assets/images/harness-engineering-slide-04.png)

### 人的角色轉變：從 in the loop 到 on the loop

這裡有一個很重要的觀念轉變。

傳統的 AI coding 流程是「人 in the loop」——AI 寫一段、人看一段、確認、再寫下一段。逐行逐段地參與。

Harness Engineering 的模式是「人 on the loop」——人不在迴圈裡面逐行檢查，而是在迴圈上方設計規則、建立回饋機制、監控品質指標。

用 Kief Morris 在 Martin Fowler 網站上的說法：**專注把想法變成結果的迭代閉環，而不是放任 agent 或鉅細靡遺地微觀管理產出。**

這不是說人類不重要了。恰恰相反——人類的工作從「寫 code」變成了「設計能讓 agent 可靠工作的環境」。這個環境才是真正的槓桿。

OpenAI 自己也明確說過：早期進度慢，多半源於環境規格不足。解法通常不是「叫 agent 更努力」，而是辨識缺少什麼能力（工具 / 文件 / 護欄 / 驗證），再把它寫進 repository，形成長期槓桿。

### 標準化的推力

這個領域正在快速標準化。兩個關鍵推力：

**AGENTS.md 的普及：** OpenAI 的 Codex 支援在 repo 裡放 `AGENTS.md`，讓 agent 在開始工作前讀取工作協議。它支援全域與專案層級的指令鏈，讓團隊能把工作約定系統化、版本化。agents.md 官方站點把它定位為「簡單、開放格式」，已被大量開源專案採用。

**Linux Foundation 的 AAIF：** 2025 年 12 月，Linux Foundation 宣布成立 Agentic AI Foundation（AAIF），Anthropic 捐出 MCP、Block 捐出 goose、OpenAI 捐出 AGENTS.md 作為基礎項目。這代表「讓 agent 可靠取得上下文與工具」開始走向跨廠互通的公共基礎建設。

---

## 七元件參考架構：完整的 Harness 長什麼樣

理解了定義之後，來看完整的架構。

一個成熟的 Harness Engineering 系統包含七個核心元件：

![駕馭工程參考架構：三層防禦與七大元件](/assets/images/harness-engineering-slide-05.png)

```
┌─────────────────────────────────────────────────────────────────┐
│                     Harness Engineering Layer                    │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Context  │  │ Arch     │  │ Eval &   │  │ CI/PR    │       │
│  │ System   │  │ Guard-   │  │ Test     │  │ Auto-    │       │
│  │          │  │ rails    │  │ Harness  │  │ mation   │       │
│  │ AGENTS.md│  │ 結構測試  │  │ 單元/整合 │  │ 自動審查  │       │
│  │ 知識庫   │  │ 自訂Lint  │  │ E2E/基準  │  │ 自動修復  │       │
│  │ MCP/RAG  │  │ 依賴規則  │  │ LLM Eval │  │ 自動合併  │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                      │
│  │ Safety   │  │ Observ-  │  │ Feedback │                      │
│  │ & Policy │  │ ability  │  │ Loops    │                      │
│  │          │  │          │  │          │                      │
│  │ Sandbox  │  │ Tracing  │  │ Doc      │                      │
│  │ 審批策略  │  │ Logs     │  │ Gardening│                      │
│  │ Policy   │  │ Metrics  │  │ GC Tasks │                      │
│  │ as Code  │  │ 成本監控  │  │ 回饋吸收  │                      │
│  └──────────┘  └──────────┘  └──────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

逐一拆解：

### 1. Context System（上下文系統）

**核心原則：** Repository 就是 system of record。Agent 看不到的東西，等於不存在。

OpenAI 試過在一個巨大的 AGENTS.md 裡塞所有指令，失敗了。原因很直白：context 是稀缺資源，什麼都「重要」等於什麼都不重要，而且大文件會瞬間過時。

他們最終的做法是把 AGENTS.md 當**目錄**（約 100 行），指向 `docs/` 裡的結構化知識庫。所有 Slack 討論、架構決策、設計原則，都必須沉澱到 repo 裡。並且用 CI job 驗證知識庫的交叉連結與結構正確性，用 doc-gardening agent 定期掃描陳舊文件並開 PR 更新。

**實務建議：** 用分層的 AGENTS.md 取代巨型手冊。Codex 的 AGENTS.md 支援全域 → 專案路徑 → 合併順序的指令鏈，預設 32KiB 上限。把它當版本控制的工作協議，不要當知識百科。

![元件 1 & 2：系統化上下文與架構護欄](/assets/images/harness-engineering-slide-09.png)

### 2. Architecture Guardrails（架構護欄）

**核心原則：** 強制不變量，而不是微管實作。

OpenAI 以固定 layers（Types → Config → Repo → Service → Runtime → UI）限制依賴方向，每一層只能往前依賴，不能反向。違反了就被自動攔住。

關鍵設計：**lint error message 裡直接嵌入修復指令。** 當規則被編碼後，Agent 犯錯的瞬間，怎麼改就已經注入 context 了。一條規則寫一次，可套用到所有變更，形成乘數效應。

這跟 Martin Fowler 文章中的觀察一致：為了讓 AI 在規模下可維護，必須收斂 solution space、犧牲部分自由度換取可控性。

![元件 3 & 4：高吞吐量 CI/PR 與測試評估](/assets/images/harness-engineering-slide-10.png)

### 3. Eval & Test Harness（評估與測試框架）

**核心原則：** 測試不只是防呆，它是控制面。

在 agent-first 世界，測試的角色提升了。OpenAI 直接把 evaluation harnesses 列為 agent 會產出的工件——代表評估機制應與程式碼同等對待、同樣版本化。

評估分兩層：
- **傳統軟體測試**（unit/integration/E2E）作為合併 gate
- **Agent/LLM 行為的專門 eval**：用 SWE-bench 類基準衡量「修 issue 能力」、用 promptfoo 類工具把 prompt 測試做成可回歸的 CI 資產

### 4. CI/PR Automation（CI/PR 自動化）

**核心原則：** 吞吐量改變 merge 哲學。

OpenAI 描述的高度自動化 PR 閉環：人類用 prompt 描述任務 → agent 開 PR → 自我 review → 要求額外 agent reviews → 回應反饋 → 迭代直到綠燈。

他們也指出：agent 吞吐量遠大於人類注意力時，「等待」的成本高於「修正」。因此採用最小化阻塞 gate、短生命週期 PR，對 flake 測試傾向用後續修正而非無限期阻塞。

![元件 5, 6, 7：安全、觀測與持續回饋](/assets/images/harness-engineering-slide-11.png)

### 5. Safety & Policy（安全與策略）

**核心原則：** 最小權限 + sandbox + approval，做成 fail closed。

Codex 的 sandbox 預設：CLI/IDE extension 透過 OS-level 機制限制權限，預設無網路、寫入權限限制於工作區。若要改 workspace 外檔案或啟用網路會觸發 approval。

安全護欄分三層：
1. **工具/沙箱層**：預設無網路、寫入限制、升權需審批
2. **LLM App Guardrails**：輸入/輸出驗證與合規檢查
3. **平台政策層（Policy-as-Code）**：用 OPA/Gatekeeper 類工具把「哪些行為被允許」固定為機械驗證規則

OWASP Top 10 for LLM Applications 把 Prompt Injection 列為關鍵風險之一，提醒不安全輸出處理可能導致下游代碼執行。這不是理論風險——我在[之前的文章](/ai-coding-tool-security-risk-prompt-injection-rce/)裡用真實案例分析過。

### 6. Observability（可觀測性）

**核心原則：** 可觀測性同時是 debug 工具與 agent 的動態上下文。

OpenAI 不只把 observability 視為產品能力，也讓 agent 能查 logs/metrics/traces 來提升自主度。他們提供本地、隨 worktree 隔離且任務結束即銷毀的觀測堆疊，讓 agent 能用 LogQL/PromQL 查詢。

在標準層面，OpenTelemetry 是目前的業界共識。OpenAI 的 Agents SDK 也將 tracing 作為內建能力，記錄 LLM 生成、tool calls、handoffs、guardrail checks 等事件。

### 7. Feedback Loops（回饋閉環）

**核心原則：** 失敗即訊號。不是「再試一次」，而是找出缺少什麼。

當 agent 卡住，判斷缺少什麼（工具 / 護欄 / 文件 / 驗證），補進系統使其可複用。OpenAI 把這個叫做「identify the missing capability and make it legible and enforceable」。

他們也把「對抗熵增」制度化：曾經每週五花 20% 時間清理「AI slop」但不可擴展，於是改以 golden principles + 背景任務（掃描偏差、更新品質分級、開重構 PR）達成類似**垃圾回收**的效果。

---

## 三層防禦架構：從策略到執行到生命週期

七元件是「需要什麼」。三層防禦架構是「怎麼組裝」。

```
┌─────────────────────────────────────────────────────────────┐
│                    Harness Engineering                       │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  第三層：控制平面 (Control Plane)                      │  │
│  │  PR 生命週期管理：從開啟到 Merge 的完整閉環             │  │
│  │                                                       │  │
│  │  Risk Contract → Preflight Gate → SHA Discipline       │  │
│  │  → Rerun Dedupe → Remediation Loop → Bot Resolve       │  │
│  │  → Browser Evidence → Harness Gap Loop                 │  │
│  │                                                       │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  第二層：四層防禦 (Four-Layer Defense)            │  │  │
│  │  │  每個 PR 的垂直檢查                               │  │  │
│  │  │                                                 │  │  │
│  │  │  Layer 1: Test（確定性，邏輯正確性）              │  │  │
│  │  │  Layer 2: Lint + Type Check（確定性，風格安全）    │  │  │
│  │  │  Layer 3: CI Gate（確定性，結構化指標）            │  │  │
│  │  │  Layer 4: LLM Judge（非確定性，語義理解）          │  │  │
│  │  │                                                 │  │  │
│  │  │  ┌───────────────────────────────────────────┐  │  │  │
│  │  │  │  第一層：分級審查 (Risk Tiering)            │  │  │  │
│  │  │  │  根據變更的爆炸半徑決定審查強度              │  │  │  │
│  │  │  │                                           │  │  │  │
│  │  │  │  低風險 → AI 自動審查                      │  │  │  │
│  │  │  │  中風險 → AI 審查 + 同儕 review             │  │  │  │
│  │  │  │  高風險 → AI 審查 + Senior review + 測試    │  │  │  │
│  │  │  │  極高風險 → 多人簽核 + staging + 回滾計畫    │  │  │  │
│  │  │  └───────────────────────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

三層的關係：
- **第一層（分級審查）**決定「這次變更需要多嚴格的檢查」
- **第二層（四層防禦）**執行「具體的檢查內容」
- **第三層（控制平面）**管理「從 PR 開啟到 Merge 的完整生命週期」

### 第一層：分級審查——根據爆炸半徑決定審查強度

這是整個架構的地基。

亞馬遜的禁令根據**人的職級**決定審查強度——初中級需要簽字，資深不需要。

Harness Engineering 根據**變更的爆炸半徑**決定審查強度——不管你是誰，改了什麼決定審查力度。

具體怎麼做？寫一份機器可讀的 Risk Contract：

```json
{
  "riskTierRules": {
    "critical": ["db/schema.ts", "app/api/payments/**", "infrastructure/**"],
    "high": ["app/api/**", "lib/tools/**"],
    "medium": ["src/**"],
    "low": ["docs/**", "README.md", "*.test.ts"]
  }
}
```

然後每個風險等級對應不同的審查要求：

| 變更類型 | 風險等級 | 審查要求 | 範例 |
|----------|----------|----------|------|
| 文件修改、測試補充 | 低 | AI 自動審查 + 自助提交 | 改 README、加 test |
| 業務邏輯修改 | 中 | AI 審查 + 同儕 review | 改 API endpoint |
| 基礎設施、權限修改 | 高 | AI 審查 + Senior review + 自動化測試通過 | 改 CI 配置、API 金鑰 |
| 生產環境部署、DB schema | 極高 | 多人簽核 + staging 驗證 + 回滾計畫 | 改資料庫 schema |

回到亞馬遜的案例：AI 提出「刪掉整個生產環境再重建」。如果有 Risk Contract，`infrastructure/**` 路徑的變更會被標記為 critical，需要多人簽核 + staging 驗證 + 回滾計畫。**在 AI 生成這個方案的瞬間，系統就會自動攔住它。**

**關鍵原則：根據變更的「爆炸半徑」來決定審查強度，而不是根據提交者的職級。**

![第一層防禦：基於爆炸半徑的風險契約](/assets/images/harness-engineering-slide-06.png)

### 第二層：四層防禦——用確定性的工具框住不確定性的 AI

分級審查決定了「需要多嚴格」。四層防禦回答「具體怎麼查」。

| 層級 | 手段 | 特性 | 能抓什麼 |
|------|------|------|----------|
| Layer 1 | Test（單元/整合/E2E） | 確定性 | 邏輯錯誤、功能偏差 |
| Layer 2 | Lint + Type Check | 確定性 | 風格問題、類型安全、反模式 |
| Layer 3 | CI Gate（覆蓋率/安全掃描） | 確定性 | 覆蓋率下降、安全漏洞、依賴風險 |
| Layer 4 | LLM Judge（多角色 review） | 非確定性 | 設計合理性、業務邏輯、架構問題 |

前三層是確定性的——跑出來就是 pass 或 fail，不需要人判斷。**只有機器的高速，才能匹配 AI 10 倍速的產出。**

核心公式：

**AI 生成代碼的質量 = 80% 你的測試覆蓋率 + 20% prompt 寫得好不好。**

![第二層防禦：用確定性工具框住不確定性的 AI](/assets/images/harness-engineering-slide-07.png)

> 詳細的四層防禦設計和實作經驗，我寫在[〈Make CI/CD Great Again〉](/coders-who-stopped-coding-harness-context-spec-engineering/)裡。

### 第三層：控制平面——從 PR 開啟到 Merge 的完整閉環

Ryan Carson 受 OpenAI Harness Engineering 啟發後，落地成的 Control-Plane Pattern，一共八步：

```
PR 開啟
  │
  ├── Step 1: Risk Contract → 判斷風險等級
  ├── Step 2: Preflight Gate → 先攔再跑（省 CI 成本）
  │     ├── Layer 1-4 四層防禦在這裡執行
  │     └── 不過 preflight 的 PR，後面的 CI 不跑
  ├── Step 3: SHA Discipline → 只信當前 HEAD 的證據
  ├── Step 4: Rerun Dedupe → 避免重複觸發 review
  ├── Step 5: Remediation Loop → Agent 自己修、自己重跑
  ├── Step 6: Bot Thread Resolve → 自動清理 bot 留言
  ├── Step 7: Browser Evidence → UI 變更需要可驗證的證據
  ├── Step 8: Harness Gap Loop → 線上事故轉 test case
  │
  └── Merge ✅
```

八步裡面有 **7 步是完全確定性的**。只有 Step 5 Remediation Loop 裡面有 LLM 參與。這不是巧合——**用確定性的工具框住不確定性的 AI**，這個原則貫穿了整個架構。

![第三層防禦：控制平面 Control-Plane Pattern](/assets/images/harness-engineering-slide-08.png)

> 完整的八步拆解和代碼範例，我寫在[〈Harness Engineering 完整拆解：Control-Plane Pattern〉](/harness-engineering-control-plane-pattern-agent-review-loop/)裡。

### 三層之間的關係

打個比方：

- 分級審查像是**紅綠燈規則**——這條路多危險，決定放幾個紅綠燈
- 四層防禦像是**每個紅綠燈的判斷邏輯**——綠燈亮不亮，取決於車速、車重、方向
- 控制平面像是**整個交通管制系統**——從你上高速到下交流道，每個節點怎麼銜接

你可以只做第一層（分級審查），這已經比亞馬遜的「一律 Senior 簽字」好了。

你可以做到第二層（四層防禦），這已經能讓 Agent 安全地跑起來。

你做到第三層（控制平面），你就能像 Peter Steinberger 一樣一人一天 627 次提交，或像 OpenAI 團隊一樣 3 人 5 個月 100 萬行代碼。

**每一層都有獨立的價值，但組合在一起才是完整的 Harness。**

---

## 五大失效模式：Harness 會怎麼壞掉

講完「怎麼建」，更重要的是「怎麼會壞」。知道失效模式，才能設計防線。

![系統失效模式與對策（一）：上下文與架構](/assets/images/harness-engineering-slide-12.png)

### 失效模式一：上下文腐壞（Context Rot）

**症狀：** AGENTS.md 跟 repo 實際狀態脫節。Agent 依照過時指令工作，產出的代碼跟現有架構矛盾。

**OpenAI 的教訓：** 他們試過巨型 AGENTS.md，但它快速腐壞且難以驗證。

**對策：** 把文件當可測試資產。用 CI 驗證文件結構與連結，用 doc-gardening agent 定期掃描陳舊文件。對文件加「可驗證性」（交叉連結、ownership、freshness 標記）。

### 失效模式二：架構漂移與模式複製

**症狀：** Agent 忠實複製 repo 裡既有的反模式。一個壞模式在幾天內被複製到多個 module，代碼腐敗速度是 10 倍起跳。

**OpenAI 管這個叫「熵管理」（Entropy Management）。**

**對策：** 用 structural tests 和 linters 把「能否新增某種耦合」直接變成 CI 失敗，而不是等 code review 才發現。設立 golden principles 與背景垃圾回收任務（掃描偏差、更新品質分級、開重構 PR），像垃圾回收一樣持續清理。

![系統失效模式與對策（二）：測試、安全與供應鏈](/assets/images/harness-engineering-slide-13.png)

### 失效模式三：測試 Flake 與錯誤合併策略

**症狀：** 不穩定的測試導致兩種極端——要嘛無限阻塞（開發停擺），要嘛放行不該放行的代碼。

**OpenAI 在高吞吐環境下採取較少阻塞 gate，flake 用後續處理。** 但在一般企業情境，若沒有足夠觀測、回滾與 canary，這可能放大風險。

**對策：** 將「最小 gate」與「快速回滾」配套設計。把 flake 當技術債納入 GC 任務，不讓它持續侵蝕信任。

### 失效模式四：安全外溢

**症狀：** Prompt injection、權限過大、不安全輸出。Agent 被外部內容注入惡意指令，或用超出需要的權限執行操作。

**OWASP 已將 prompt injection 列為 LLM 應用主要風險。** Codex 文件也提醒啟用網路與 web search 的注入風險。

**對策：** 最小權限 + sandbox + approval policy。把外部內容視為不受信任。對 effectful tools 做 pre-action authorization。把安全測試集與 red teaming 自動化。

### 失效模式五：供應鏈崩壞

**症狀：** Agent 更頻繁新增依賴、改 build pipeline、產生 artifacts，放大了供應鏈攻擊面。

**對策：** 用 NIST SSDF 作為安全開發實務框架。用 SLSA 作為 build provenance 與防竄改檢核清單。對 agent 新增依賴與 build 變更設立更高級別的審批（這就是 Risk Contract 的價值）。強化 SBOM、鎖定依賴來源、簽章與 provenance。

---

## 架構護欄的落地工具

講完模式，來看具體能用什麼工具。重點不是工具本身，而是**把約束做成能在 CI 中跑的工程體**。

![落地實踐：架構護欄與觀測工具矩陣](/assets/images/harness-engineering-slide-14.png)

### 結構化依賴檢查

| 語言/生態 | 工具 | 能做什麼 |
|---|---|---|
| JS/TS | dependency-cruiser | 自訂規則驗證依賴方向，禁止跨層 import、禁止循環依賴 |
| JS/TS Monorepo | Nx enforce-module-boundaries | 以 ESLint 規則檢查子專案依賴白名單、分層、domain 隔離 |
| Python | import-linter | 對 Python 模組 import 施加架構約束（分層規則、循環依賴） |
| Java | ArchUnit | 以單元測試框架檢查 packages/layers 依賴、命名規範 |

**dependency-cruiser 規則示意（JS/TS）：**

```js
// .dependency-cruiser.js
module.exports = {
  forbidden: [
    {
      name: "no-ui-to-repo",
      comment: "UI 不可直接依賴 Repo",
      from: { path: "^src/ui" },
      to: { path: "^src/repo" }
    }
  ]
};
```

**import-linter 規則示意（Python）：**

```ini
# importlinter.ini
[importlinter]
root_package = myapp

[importlinter:contract:layering]
name = layering
type = layers
layers =
    myapp.types
    myapp.config
    myapp.repo
    myapp.service
    myapp.api
```

**ArchUnit 測試示意（Java）：**

```java
@AnalyzeClasses(packages = "com.myapp")
public class ArchitectureTest {
  @ArchTest
  static final ArchRule services_should_not_access_controllers =
    noClasses().that().resideInAPackage("..service..")
      .should().dependOnClassesThat().resideInAPackage("..ui..");
}
```

這些工具的共通點：**把架構規則變成 CI 裡的 pass/fail。** Agent 犯錯的瞬間就被攔住，不需要等人類在 code review 時發現。

### Eval / 測試工具

| 工具 | 定位 | 特點 |
|---|---|---|
| promptfoo | Prompt / Agent / RAG 測試 | 支援 CI/CD 整合、red teaming、可回歸的測試矩陣 |
| SWE-bench | 以真實 GitHub issues 建構 Agent 基準 | 2,294 個任務，要求 patch 通過測試 |
| OpenAI Evals | LLM 系統行為評估框架 | 判斷模型/提示/系統改動對用例的影響 |

### 可觀測性工具

| 工具 | 定位 | 適用場景 |
|---|---|---|
| OpenTelemetry | 開源可觀測性標準 | Traces/Metrics/Logs 的統一收集與匯出 |
| Langfuse | 開源 LLM 工程平台 | Tracing、成本/延遲監控、eval |
| Arize Phoenix | 開源 ML 可觀測性 | Tracing、evaluation、偏差檢測 |

---

## 三種規模的導入路線圖

不同規模的團隊，導入的深度和節奏應該不一樣。

![導入路線圖：不同規模團隊的落地策略](/assets/images/harness-engineering-slide-15.png)

### 規模對比總覽

| 情境 | 目標範圍 | 時程 | 年度預算估算 | 核心人力 |
|---|---|---|---|---|
| **小型團隊** | 1 個 repo、單一產品線試點 | 4-6 月 | $100K-300K | 3-5 人 |
| **中型團隊** | 多 repo（3-10）、共用平台 | 6-9 月 | $700K-1.8M | 8-12 人 |
| **企業級** | 多 BU、多技術棧、多租戶治理 | 9-12 月 | $3-10M | 20-40 人 |

### 小型團隊的主要交付物

AGENTS.md + in-repo 指令鏈、基本 sandbox/approval、架構 lint（1 套）、測試/基本 eval、CI 自動化 PR 流程、最小 tracing。

### 中型團隊的主要交付物

repo 模板化（knowledge store + rules）、結構測試擴展、多層 eval（offline + online）、自動 doc gardening/GC 任務、可觀測性落地（OTel + dashboard）、供應鏈控制（SBOM/SLSA 起步）。

### 企業級的主要交付物

多租戶 agent 平台、policy-as-code（OPA 等）整合、權限與審批矩陣、集中化 eval 與 leaderboard、事件稽核與留存策略、與既有 SDLC/變更管理整合、企業級供應鏈與合規。

![系統演進：12 個月建置里程碑](/assets/images/harness-engineering-slide-16.png)

### 12 個月路線圖（里程碑）

| 時間窗 | 里程碑 | 驗收標準 |
|---|---|---|
| 月 1-2 | 基線建立 | sandbox、CI、最小 AGENTS.md 就位；PR 必跑測試/靜態檢查 |
| 月 2-3 | 知識庫建立 | in-repo 知識庫有索引與連結檢查；有文件 freshness/ownership 規則 |
| 月 3-4 | 架構護欄 v1 | 至少 1 套跨層依賴規則在 CI 強制；違規可在 1 次迭代被 agent 修復 |
| 月 4-6 | Eval harness v1 | 有固定 eval 集合；能比較「變更前後」；線上可追蹤關鍵品質指標 |
| 月 6-8 | Observability v1 | 可追蹤每次 agent run 的 traces；能定位失敗原因；可監測 token/成本趨勢 |
| 月 8-10 | 自動化 GC | 定期產生清理 PR；架構違規與文件陳舊趨勢下降 |
| 月 10-12 | 平台化與擴散 | 可重複的 harness 模板；可在多 repo 推廣；DORA 指標與 agent 指標雙軌呈現 |

---

## 你的團隊明天就能做的三件事

不需要搭完整套架構。明天就可以開始的三件事：

![明天就能開始的三個具體行動](/assets/images/harness-engineering-slide-17.png)

### 1. 寫一份 Risk Contract（30 分鐘）

在 repo 根目錄建一個 `risk-tiers.json`：

```json
{
  "critical": ["db/", "infrastructure/", "auth/"],
  "high": ["api/", "payments/"],
  "medium": ["src/"],
  "low": ["docs/", "tests/", "*.md"]
}
```

不需要自動化。光是**把風險等級寫下來**這件事，就能省掉無數次「這個 PR 要不要認真 review」的爭論。團隊所有人對齊了「什麼路徑是高風險」，比任何口頭約定都有效。

### 2. 加一條 CI 規則：高風險路徑必須過測試（1 小時）

在 GitHub Actions 或你的 CI 裡加一條規則：

如果 PR 改了 `db/`、`infrastructure/`、`auth/` 目錄的檔案，**必須有對應的測試通過才能 merge**。

不需要 LLM Judge，不需要 Greptile，一條 path filter + required check 就夠了。

這條規則如果在亞馬遜 AWS 團隊的 repo 裡，AI 提出「刪掉整個生產環境」的那一刻，CI 就會直接 fail。

### 3. 建立「每個事故一個 test case」的習慣（0 成本）

下次線上出問題，修完之後多做一件事：把復現條件寫成 test case，加進 CI。

不需要工具，不需要系統，只需要一個團隊約定：**修完 bug 之後，先寫 test 再關 ticket。**

長期來看，這個習慣會讓你的測試覆蓋率持續成長，而且都是**真正有價值的測試**——因為每一個都對應一個真實的事故。

---

## 坦白說

我自己用 Claude Code 寫了 63 萬行程式碼，這整套架構我沒有全部做到。

**比較確定的：**

1. **分級審查是 ROI 最高的第一步。** 一份 JSON 就能省掉無數次爭論。零成本，純紀律。這件事沒有任何理由不做。

2. **四層防禦裡面，前三層（Test、Lint、CI Gate）是必須的。** 這是 20 年前的老技術，但在 AI 時代反而成了最硬的護城河。你的 testing case 寫得越多、越齊全，這是一個看漲的資產。

3. **禁令方向對了，但解法選錯了。** 亞馬遜承認 AI 需要護欄，這個判斷正確。但用人的注意力去擋 AI 的高速產出，長期不可持續。人會疲勞、會自滿、會在連續按 50 次 Yes 之後麻木。系統架構不會。

4. **五大失效模式是真的。** 上下文腐壞、架構漂移我都親身經歷過。Agent 複製反模式的速度真的是 10 倍。你不設 guardrail，它會忠實地把你 repo 裡最爛的寫法複製到每一個新檔案。

**不太確定的：**

1. **完整控制平面對小團隊的成本效益。** Ryan Carson 在 OpenAI，資源充足。2-3 人的 startup 搭完整八步可能過度工程。我的建議是先做 Step 1（contract）、Step 2（preflight）、Step 3（SHA discipline），這三步零成本。

2. **Remediation Loop 的收斂性。** Agent 修完 → review 又發現問題 → Agent 再修……這個迴路什麼時候停？我自己經歷過「修完跑第二輪又冒出兩個高危」的情況。無限 loop 是真實風險，但 Ryan 沒提到 max retry 或 circuit breaker。

3. **LLM 審 LLM 的上限。** 用同一個模型家族寫代碼和審代碼，系統性偏差無法被捕捉。在金融場景這是個大問題。多模型交叉審查能不能解？需要更多實驗。

4. **12 個月路線圖的實際可行性。** 研究報告裡的時程估算是理想值。我在實務上看到的是：大部分團隊光是「讓 CI 穩定跑」就要花 2-3 個月。路線圖可以當方向參考，但不要當承諾。

---

## 總結：一句話理解 Harness Engineering

如果你只記住一句話：

**AI 可以寫 code，但不能自己上 production。中間那個「不能」，需要用系統架構來實現，而不是靠人的注意力。**

這就是 Harness Engineering 在做的事。

亞馬遜用最痛的方式學到了這個教訓。希望你的團隊不用。

---

## 延伸閱讀

**Harness Engineering 系列（由淺入深）：**

1. [亞馬遜 AI 事故啟示：科技巨頭一邊賣 AI 未來，一邊在自己家裡給 AI 上鎖](/amazon-ai-code-incident-tech-giants-quietly-locking-ai/) — 事件分析 + 為什麼禁令不是終點
2. [Make CI/CD Great Again：四層防禦架構](/coders-who-stopped-coding-harness-context-spec-engineering/) — 第二層的完整拆解 + 實作經驗
3. [Harness Engineering 完整拆解：Control-Plane Pattern](/harness-engineering-control-plane-pattern-agent-review-loop/) — 第三層的八步閉環 + 代碼範例

**外部參考資料：**

- [OpenAI — Harness Engineering（英文）](https://openai.com/index/harness-engineering/)
- [OpenAI — Harness Engineering（繁中）](https://openai.com/zh-Hant/index/harness-engineering/)
- [Martin Fowler — Harness Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)
- [Martin Fowler — Context Engineering for Coding Agents](https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html)
- [AGENTS.md 開放格式](https://agents.md/)
- [Linux Foundation — Agentic AI Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [OpenTelemetry](https://opentelemetry.io/docs/what-is-opentelemetry/)
- [SLSA — Supply-chain Levels for Software Artifacts](https://slsa.dev/)

**相關文章：**

- [AI Coding 的第一個風險，不是模型——是你一直按「Yes」](/ai-coding-tool-security-risk-prompt-injection-rce/)
- [混沌智能體：史丹佛 x 哈佛的論文告訴我們，控制好一個 AI Agent 不等於控制好一群](/agents-of-chaos-multi-agent-structural-instability/)
- [AI Coding 半年回顧：開發並沒有變快，我們只是把瓶頸從寫 Code，轉移到了 QA 跟需求收集](/ai-coding-half-year-review-demand-transformation-tool-evolution/)
