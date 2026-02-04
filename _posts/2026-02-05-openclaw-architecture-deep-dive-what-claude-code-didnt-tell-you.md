---
layout: post
title: "OpenClaw 架構全拆解：Agent 工程師必學的六層設計"
date: 2026-02-05 08:00:00 +0800
permalink: /openclaw-architecture-deep-dive-what-claude-code-didnt-tell-you/
image: /assets/images/moltbot-architecture-complete-flow.png
description: "從訊息進來到回應出去，中間經過六個關鍵元件。搞懂這條鏈路，你就知道為什麼它比 Claude Code 更像一個「員工」。"
---

## 目錄

- [為什麼要拆解 OpenClaw 的架構？](#為什麼要拆解-openclaw-的架構)
- [OpenClaw 到底是什麼？](#openclaw-到底是什麼)
- [六層架構：從訊息到回應的完整路徑](#六層架構從訊息到回應的完整路徑)
- [Channel Adapter：多通道歸一](#channel-adapter多通道歸一)
- [Gateway Server：任務協調的心臟](#gateway-server任務協調的心臟)
- [Lane Queue：為什麼序列化是對的？](#lane-queue為什麼序列化是對的)
- [Agent Runner：動態組裝系統提示詞](#agent-runner動態組裝系統提示詞)
- [Agentic Loop：工具調用的迴圈](#agentic-loop工具調用的迴圈)
- [Response Path：回到你手上](#response-path回到你手上)
- [記憶系統：簡單但有效](#記憶系統簡單但有效)
- [Computer Use：為什麼不用截圖？](#computer-use為什麼不用截圖)
- [安全設計：Allowlist 與危險指令攔截](#安全設計allowlist-與危險指令攔截)
- [坦白說](#坦白說)
- [常見問題 Q&A](#常見問題-qa)
- [延伸閱讀](#延伸閱讀)

---

## 為什麼要拆解 OpenClaw 的架構？

我最近在 Discord 看到一個問題：

> 「OpenClaw 跟 Claude Code 到底差在哪？不都是讓 LLM 執行命令嗎？」

這問題問得好。

**表面上，兩者都是「讓 AI 在你電腦上執行任務」。但底層架構完全不同。**

Claude Code 是一個 CLI 工具，你跟它互動的方式是在 Terminal 裡打字。

OpenClaw 是一個 Gateway Server，它可以同時接收來自 Telegram、Discord、Slack、WhatsApp 的訊息，然後在你的機器上執行任務。

這個差異決定了整個架構的複雜度。

今天這篇文章，我要把 OpenClaw 的架構從頭到尾拆解一遍。搞懂這條鏈路，你會更清楚它擅長什麼、不擅長什麼，以及為什麼它比 Claude Code 更像一個「員工」。

---

## OpenClaw 到底是什麼？

先說結論：

**OpenClaw（也叫 Clawdbot）是一個 TypeScript CLI 應用程式。**

不是 Python。不是 Next.js。不是 Web App。

它是一個跑在你本地機器上的 process，做三件事：

1. **暴露一個 Gateway Server**，處理來自各通道（Telegram、WhatsApp、Slack 等）的訊息
2. **呼叫 LLM API**（Anthropic、OpenAI、本地模型都可以）
3. **在你的電腦上執行工具**，包括 Shell 命令、檔案操作、Browser 控制

這跟 Claude Code 最大的差異是什麼？

**Claude Code 是單一互動介面（Terminal），OpenClaw 是多通道協調器。**

你可以同時在 Telegram 問它問題、在 Discord 叫它跑任務、用 Cron Job 讓它定期檢查信箱——這些請求都會進入同一個協調系統，排隊處理。

這就是為什麼它的架構比 Claude Code 複雜得多。

---

## 六層架構：從訊息到回應的完整路徑

當你在 Telegram 發一則訊息給 OpenClaw，中間會經過六個元件：

```
1. **You** — 從 Telegram / Discord / WhatsApp 發訊息
2. **Channel Adapter** — 正規化訊息格式、解壓附件
3. **Gateway Server** — Session Router + Lane Queue 協調任務
4. **Agent Runner** — 組裝 System Prompt、載入記憶、檢查 Context Window
5. **LLM API** — 呼叫模型（支援 streaming）
6. **Agentic Loop** — 工具呼叫迴圈，直到產出 Final Text
7. **Response Path** — 串流回應、持久化對話紀錄
8. **You** — 收到回應
```

接下來我會逐層拆解每個元件的設計邏輯。

---

## Channel Adapter：多通道歸一

第一層是 **Channel Adapter**。

每個通訊平台（Telegram、Discord、WhatsApp、Slack）都有自己的 API 格式、訊息結構、附件處理方式。

Channel Adapter 的工作是：

1. **接收原始訊息**
2. **正規化格式**（統一成內部資料結構）
3. **解壓附件**（圖片、檔案、語音）

這樣後面的元件就不用管訊息是從哪個平台來的。

**設計原則：Separation of Concerns。**

每個通道有自己的 Adapter，互不干擾。如果 Telegram 改了 API，只需要改 Telegram Adapter，其他不受影響。

---

## Gateway Server：任務協調的心臟

第二層是 **Gateway Server**，這是 OpenClaw 的心臟。

它做兩件事：

### 1. Session Router

把訊息路由到正確的 Session。

什麼是 Session？每一個「對話情境」就是一個 Session。

- 你跟 OpenClaw 的私聊是一個 Session
- 某個 Discord 頻道是另一個 Session
- 某個 WhatsApp 群組是又一個 Session

Session Router 根據訊息來源，決定要分配到哪個 Session。

### 2. Lane Queue

這是最關鍵的設計。

OpenClaw 用 **Lane-based Command Queue** 來序列化操作。

每個 Session 有自己專屬的 Lane（通道），同一 Lane 內的任務必須**嚴格序列執行**。

但是，低風險、可並行的任務（例如 Cron Job）可以跑在獨立的 parallel Lane。

**為什麼要這樣設計？**

因為 async/await 的並行執行會帶來 Race Condition。

---

## Lane Queue：為什麼序列化是對的？

這裡值得深入講一下。

如果你寫過 Agent，你一定遇過這種問題：

- Agent 同時嘗試讀取和寫入同一個檔案
- Log 交錯在一起，完全無法 debug
- 共享狀態在並行執行下出現不可預測的行為

傳統做法是加鎖（Lock）。但加鎖容易漏，而且心智負擔很重——你要一直想「這裡要不要鎖？」

**OpenClaw 的做法是反過來：預設序列化，只有明確安全的才並行。**

這跟 Cognition（Devin 的公司）在「Don't Build Multi-Agents」那篇文章的觀點一致：

> A simple async setup per agent will leave you with a dump of interleaved garbage.

Lane Queue 把序列化變成預設架構，而不是事後補救。

**心智模型從「我要鎖什麼？」變成「什麼可以並行？」**

大多數情況下，答案是「都不要並行」。只有真正獨立、不共享狀態的任務才放到 parallel lane。

---

## Agent Runner：動態組裝系統提示詞

第三層是 **Agent Runner**，這是 AI 真正介入的地方。

它做四件事：

### 1. Model Resolver

決定要用哪個模型（Claude、GPT、本地模型）。

如果主要模型失敗（API key 超限、服務異常），會自動 fallback 到備用模型。

### 2. System Prompt Builder

**動態組裝系統提示詞。**

這是 OpenClaw 跟 Claude Code 的關鍵差異。

Claude Code 的 CLAUDE.md 是靜態注入的——你寫好什麼，它就讀什麼。

OpenClaw 的 System Prompt 是動態組裝的：

- 當前可用的 Tools
- 已安裝的 Skills
- 從 memory/ 讀取的記憶
- Session 的上下文

這讓 Agent 可以「知道」自己現在能做什麼、記得什麼。

### 3. Session History Loader

從 `.jsonl` 檔案載入對話歷史。

每一行是一個 JSON 物件，記錄了使用者訊息、工具呼叫、執行結果、Agent 回應。

### 4. Context Window Guard

監控 Token 使用量。

如果快要超過 Context Window 上限，會觸發壓縮機制——把早期對話摘要化，騰出空間。

這就是為什麼 OpenClaw 可以跑很長的對話而不會爆掉。

---

## Agentic Loop：工具調用的迴圈

第四層是 **LLM API 呼叫** + 第五層 **Agentic Loop**。

這是標準的 **ReAct（Reasoning + Acting）** 架構：

1. 呼叫 LLM API（支援 streaming）
2. 如果 LLM 回傳 tool call → 執行工具 → 把結果加入對話 → 回到步驟 1
3. 如果 LLM 回傳 final text → 結束迴圈

**預設最大迴圈次數約 20 次**，避免無限 loop。

### 為什麼是 ReAct 而不是 Plan & Execute？

| 項目 | ReAct（OpenClaw 用的） | Plan & Execute |
|------|---------------------|----------------|
| 執行流程 | 一步一步走，邊做邊決定下一步 | 先產出完整計畫，再逐步執行 |
| 彈性 | 高（可根據工具輸出即時調整） | 低（計畫定了就照做） |
| Token 消耗 | 較高（每步都要完整 context） | 較低（計畫階段只思考一次） |
| 適合場景 | 探索性任務、不確定步驟數 | 明確流程、可預測步驟 |

OpenClaw 選擇 ReAct 是合理的——它要處理的任務類型太廣（從發會議邀請到剪片），無法預先規劃完整步驟。

**ReAct 的核心循環：思考 → 行動 → 觀察 → 再思考。**

這裡發生的事情包括：

- Computer Use（執行 Shell 命令）
- 檔案讀寫
- Browser 操作
- 外部 API 呼叫

---

## Response Path：回到你手上

第六層是 **Response Path**。

回應經過 Stream Chunks 處理（讓你可以即時看到 Agent 正在打字），然後透過 Channel Adapter 傳回你使用的平台。

同時，整個對話會被持久化到 `.jsonl` 檔案。

這就是 OpenClaw 的「記憶」——下次對話時，Session History Loader 會讀取這個檔案，讓 Agent 記得之前發生過什麼。

---

## 記憶系統：簡單但有效

OpenClaw 的記憶系統出乎意料地簡單：

### 1. Session Transcripts（.jsonl）

每個 Session 的完整對話紀錄。每一行是一個 JSON 物件。

### 2. Memory Files（Markdown）

長期記憶存在 `MEMORY.md` 或 `memory/` 資料夾。

Agent 自己寫入這些檔案——沒有特殊的 Memory API，就是用標準的 file write 工具。

### 3. Hybrid Search

搜尋時用 **Vector Search + Keyword Match** 混合策略：

- Vector Search（語意搜尋）：搜「authentication bug」會找到「auth issues」
- Keyword Search（關鍵字搜尋）：精確匹配「authentication bug」

底層用 SQLite + FTS5（SQLite 的全文搜尋擴充）。

### 4. Smart Syncing

檔案監聽器（File Watcher）偵測到記憶檔案變更時，自動觸發同步。

**這套設計的特點是：沒有花俏的記憶壓縮、沒有遺忘曲線。**

舊記憶跟新記憶權重相同。簡單、可解釋、但也意味著記憶檔案會無限膨脹。

---

## Computer Use：為什麼不用截圖？

OpenClaw 給 Agent 完整的電腦控制權限。這包括：

### 1. Exec Tool（Shell 命令）

可以在三種環境執行：

- **Sandbox**（預設）：Docker 容器內執行
- **Host**：直接在你的機器上執行
- **Remote**：在遠端設備執行

### 2. Filesystem Tools

標準的 read、write、edit 工具。

### 3. Process Management

啟動背景程序、終止程序、監控程序狀態。

### 4. Browser Tool

這個最有趣。

**OpenClaw 的 Browser 不是用截圖，而是用 Semantic Snapshots。**

什麼是 Semantic Snapshot？就是把網頁的 Accessibility Tree（ARIA）轉成文字：

```
- button "Sign In" [ref=1]
- textbox "Email" [ref=2]
- textbox "Password" [ref=3]
- link "Forgot password?" [ref=4]
- heading "Welcome back"
- list
  - listitem "Dashboard"
  - listitem "Settings"
```

這樣做的好處：

| 項目 | 截圖 | Semantic Snapshot |
|------|------|-------------------|
| 大小 | ~5 MB | ~50 KB |
| Token 成本 | 很高（圖像 Token） | 很低（純文字） |
| 操作精確度 | 模糊（要猜座標） | 精確（直接用 ref） |
| 速度 | 慢 | 快 |

**瀏覽網頁本質上不是視覺任務，而是語意任務。**

Agent 不需要「看」到登入按鈕長什麼樣，它只需要知道「有一個叫 Sign In 的 button，ref=1」。

---

## 安全設計：Allowlist 與危險指令攔截

OpenClaw 的安全設計跟 Claude Code 類似：

### 1. Command Allowlist

```json
// ~/.clawdbot/exec-approvals.json
{
  "agents": {
    "main": {
      "allowlist": [
        { "pattern": "/usr/bin/npm", "lastUsedAt": 1706644800 },
        { "pattern": "/opt/homebrew/bin/git", "lastUsedAt": 1706644900 }
      ]
    }
  }
}
```

使用者可以 allow once、always、deny。

### 2. Safe Commands Pre-approved

安全指令已預先核准：`jq`、`grep`、`cut`、`sort`、`uniq`、`head`、`tail`、`tr`、`wc`。

### 3. Dangerous Constructs Blocked

危險的 Shell 構造會被攔截：

```bash
# 這些會被拒絕執行：
npm install $(cat /etc/passwd)     # command substitution
cat file > /etc/hosts              # redirection
rm -rf / || echo "failed"          # chained with ||
(sudo rm -rf /)                    # subshell
```

**核心原則：給使用者最大自主權，同時阻擋明顯的惡意操作。**

---

## 坦白說

### 這套架構的優點

1. **多通道支援**：Telegram、Discord、WhatsApp、Slack 一個 Agent 搞定
2. **序列化設計**：Lane Queue 避免了大多數 Race Condition
3. **動態 Context**：System Prompt 根據當前狀態組裝
4. **記憶持久化**：簡單但有效的 Markdown + JSONL 設計
5. **Browser Semantic Snapshot**：比截圖便宜 100 倍

### 這套架構的缺點

1. **TypeScript 限制**：比 Python 生態系統小，ML 相關工具整合困難
2. **序列化瓶頸**：同一 Session 的任務無法並行，長任務會阻塞
3. **記憶膨脹**：沒有遺忘機制，memory/ 會越來越大
4. **安全風險**：給 Agent 電腦控制權本身就是高風險操作

### 跟 Claude Code 的本質差異

| 項目 | Claude Code | OpenClaw |
|------|-------------|---------|
| 互動介面 | Terminal 單一入口 | 多通道（Telegram、Discord 等） |
| 執行模式 | 使用者觸發 | 使用者觸發 + Cron Job |
| System Prompt | 靜態（CLAUDE.md） | 動態組裝 |
| 記憶 | 單次對話 | 跨對話持久化 |
| Browser | 無 | Semantic Snapshot |

**Claude Code 是工具，OpenClaw 是員工。**

工具等你叫它才動。員工會自己檢查信箱、記得昨天交代的事、主動回報進度。

這就是為什麼 OpenClaw 的架構複雜那麼多——因為它要支撐的使用情境複雜那麼多。

---

## 常見問題 Q&A

**Q: OpenClaw 用什麼語言寫的？**

TypeScript。不是 Python、不是 Next.js、不是 Web App。是一個跑在本地的 CLI 應用程式，暴露 Gateway Server 處理多通道訊息。

**Q: Lane Queue 跟一般的 async/await 有什麼差別？**

傳統 async/await 預設並行，你要主動加鎖避免 Race Condition。Lane Queue 預設序列化，你要主動指定哪些可以並行。心智負擔從「我要鎖什麼」變成「什麼可以並行」，大多數情況下答案是「都不要並行」。

**Q: 為什麼 Browser 用 Semantic Snapshot 而不是截圖？**

因為截圖 5MB、Semantic Snapshot 50KB。Token 成本差 100 倍。而且瀏覽網頁本質上是語意任務——Agent 不需要看到按鈕長什麼樣，只需要知道「有一個叫 Sign In 的 button」。

**Q: OpenClaw 的記憶會不會越來越慢？**

會。因為沒有遺忘機制，memory/ 檔案會持續膨脹。建議每週整理，只保留最近 7 天的 daily notes，重要資訊轉移到 MEMORY.md。

**Q: 安全風險怎麼處理？**

OpenClaw 有 Allowlist、Safe Commands Pre-approved、Dangerous Constructs Blocking 三層防護。但核心問題是：你給 Agent 電腦控制權本身就是高風險操作。建議用獨立虛擬機跑，不要在主力機上執行。

---

## 延伸閱讀

- [OpenClaw 記憶系統全解析：SOUL.md、AGENTS.md 與高昂的 Token 成本](/openclaw-architecture-deep-dive-context-memory-token-crusher/) — 記憶架構的深度剖析
- [OpenClaw 四層縱深防禦加固指南](/moltbot-security-hardening-guide/) — 安全設定必讀
- [從「套殼 1.0」到「套殼 2.0」：為什麼真正該緊張的是 Anthropic](/shell-wrapper-2-anthropic-real-threat/) — 生態系統觀點
- [個人 AI 助手決戰週：Claude Code vs OpenClaw 殊途同歸](/personal-ai-agent-future-claude-code-vs-openclaw/) — 兩條路線的比較
- [這幾天我密集使用小龍蝦 OpenClaw：為什麼我決定把它納入工作流](/openclaw-real-world-usage-workflow-not-chatbox/) — 實際使用體驗

---

**關於作者：**

Wisely Chen，NeuroBrain Dynamics Inc. 研發長，20+ 年 IT 產業經驗。曾任 Google 雲端顧問、永聯物流 VP of Data & AI、艾立運能數據長。專注於傳統產業 AI 轉型與 Agent 導入的實戰經驗分享。

---

**相關連結：**
- 部落格首頁：https://ai-coding.wiselychen.com
- LinkedIn：https://www.linkedin.com/in/wisely-chen-38033a5b/
