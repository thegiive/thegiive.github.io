---
layout: post
title: "Claude Code 四層壓縮拆解 + 被封殺後的 Agent Infra 生存指南｜Weekly AI Vlog EP16"
date: 2026-04-12 12:00:00 +0800
permalink: /vlog-weekly-summary-ep16-claude-code-compression-openclaw-survival/
image: /assets/images/vlog-ep16-claude-code-compression-openclaw-cover.png
description: "這集我把兩個最近最重要的主題壓在一起講：Claude Code 為什麼能跑那麼久不忘記東西（答案在 3,960 行的壓縮子系統裡），以及 Anthropic 把 OpenClaw 踢出 subscription 之後，我怎麼用三層方案活下來。核心是同一件事——掌握 Agent Infra 的自主權。"
---

<div class="video-container">
<iframe width="560" height="315" src="https://www.youtube.com/embed/NNpMWmg5h6k" title="Claude Code 四層壓縮拆解 + 被封殺後的 Agent Infra 生存指南｜Weekly AI Vlog EP16" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

---

## 第一部分：Claude Code 上下文壓縮四層架構

### 為什麼要聊這個

Claude Code 之所以能夠長時間自動化運行，而且不容易忘掉你之前做過的事情，最關鍵的設計就是它的上下文壓縮機制。從原始碼來看，它有**四層**，從輕到重：

| 層級 | 名稱 | 核心邏輯 |
|------|------|---------|
| 第一層 | Micro Compact | 零成本規則清理，刪除舊的工具輸出，但不破壞 Prompt Cache |
| 第二層 | Session Memory Compact | 提煉結構化事實，不是壓縮，是提煉 |
| 第三層 | Full Compact | 調用模型做 9 維度摘要 + Analysis Tag（Chain of Thought） |
| 第四層 | Auto Compact | 決定什麼時候壓，87% 觸發 + 熔斷器保護 |

### 第一層：Micro Compact

當你在 Claude Code 裡面操作的時候，會產生大量的工具輸出。這些輸出在這一次或下一次可能有意義，但十分鐘之後就沒用了。

問題是，Claude Code 有 Prompt Cache 機制。如果你很輕易的把這些工具輸出從提示詞拿掉，上一次的 Prompt Cache 就會失效。所以它做了一個叫做 Cached Micro Compact 的機制——在 API 層告訴 Claude API 說「這段 Tool Output 要進行 Micro Compact」，東西會不見，但 Prompt Cache 不會失效。

### 第二層：Session Memory Compact

這一層比較像是**提煉**，而不是壓縮。它會從最新的訊息往前推進幾個 Message，提取出結構化的資訊。最重要的重點是：如果你保留了一個 Tool Use，就必須同時保留對應的 Tool Result，不然 Streaming 會出問題。

這個東西比 Full Compact 來得快，而且能獲取足夠的資訊。

### 第三層：Full Compact

Full Compact 會比我們一般說的「請總結你的東西」來得更全面。它分九個維度——包含用戶訊息、當前系統狀態、Error 日誌等等。

更精妙的是，它會先在一個 Analysis Tag 裡面進行思考，最後才輸出 Summary。這本質上就是一個 Chain of Thought——花一些 output token 讓模型先想清楚，提高摘要品質，然後把思考過程丟掉。

但這層比較貴，而且常常壓著壓著就出現 Prompt Too Long，所以它還有一個三層的 Retry 機制。

### 第四層：Auto Compact

Auto Compact 解決的是「什麼時候壓」的問題。它不會等到你用完了才壓——那時候已經太晚了。它會在大概 **87%** 的時候就觸發，優先嘗試第二層的 Session Memory Compact，不行再用第三層。

而且它有一個**熔斷器設計**：如果 Compact 連續三次失敗，就直接暫停。這個設計是有真實教訓的——Anthropic 曾經每天浪費 25 萬次 API 調用，就是因為壓縮失敗一直重試。

> 詳細的源碼分析、所有程式碼位置，請看完整文章：[Claude Code 上下文工程：四層壓縮機制的源碼級拆解](/claude-code-context-engineering-four-layer-compression/)

---

## 延伸：System Prompt 與資安設計

這集我也快速帶過了 Claude Code 在 System Prompt 和資安方面的設計。

### System Prompt 四大原則

1. **重要的事情不斷提供。** Google 論文講過，重要的提示詞在前後重複一次效果會有奇效。Claude Code 更誇張，它用了四到五次、四種不同的方式，反覆告訴 Claude 同一件事：be concise、be solid。這就是為什麼 Claude 回答顯得比較謙遜。

2. **Prompt Cache Block 架構。** 它有一條邊界線，上面的是靜態的系統規則（會被 Cache），下面是動態的工具參數。這個設計直接決定了 Token 效率——像 OpenClaw 被 Anthropic 噴說浪費 Token，其實就是 Prompt Cache 沒設計好。

3. **Sub-Agent 安全降級。** 主 Agent 有嚴格的環境和狀態檢查，但丟到子 Agent 的時候會放寬 Harmless 審查，因為主 Agent 分派出去的任務已經有基本安全性。

4. **Prompt 層資安設計。** 包含獨立的 module 聲明（只有 Security 團隊能改）、用 `system-reminder` 和 `env` 標籤包裹外部輸入（防 Prompt Injection）、主動提醒 Claude 注意 Prompt Injection、高風險操作 Flag 降權、以及內建 OWASP Top 10 風險清單。

> 詳細分析請看：
> - [System Prompt 架構（EP1）](/claude-code-system-prompt-source-code-analysis/)
> - [資安架構：14 條 Best Practice 原始碼驗證（EP2）](/claude-code-security-best-practices-source-code-verified/)

### 企業級遙測的雙面刃

Claude Code 也大量收集了客戶相關的資訊——你是誰、你在做什麼、你的 OS 版本，定期傳給 Anthropic。它還設計了一個 **Kill Switch**，比較像是 A/B Testing——可以在你完全不更新 CLI 的情況下，遠端打開或關掉某個功能。

更有趣的是，它會根據你的用字遣詞收集你的**煩躁值**。當系統覺得用戶很煩躁的時候，就會把整段 Session History 傳回 Anthropic 做 UI/UX 研究。

這是一體兩面的設計。它能提升產品體驗，但也代表它能在某種程度上監控你。

---

## 第二部分：Anthropic 封殺 OpenClaw 後的三層替代方案

### 發生了什麼事

Anthropic 正式把 OpenClaw 這樣的 third party 工具納出他們的 subscription。使用 subscription 帳戶的話，你是無法使用 OpenClaw 的，會出現 401 error。

但其實我覺得也沒什麼。人家在二月的時候，Terms of Service 就已經明確講了不支持這樣使用。現在只是開始執行而已。而且 Claude Code 也把 OpenClaw 比較好用的功能都抄得差不多了，所以 Anthropic 已經有提供替代品給使用者。

### 為什麼我還是要用 OpenClaw

OpenClaw 本身就是一個純開源方案，它完全不依賴任何特定供應商。**只有開放架構，你才有權利去跟人家 bargain。**

我在 IT 界已經二十幾年了。某一家很厲害的廠商壟斷、然後慢慢收攏使用者的權限，這件事情已經屢見不鮮了。Anthropic 不會是一個特例。

所以我個人是使用**雙槍匣**策略——Claude Code 還是我一個很好的工具，但我也還是使用 OpenClaw。

### 方案一：換供應來源

如果你之前是用 Claude Max 的方案，最簡單的方式就是跑到 ChatGPT 的 Codex。你可能覺得 ChatGPT Codex 跟 Claude 還是有差別——對，是有差別。但我前面的 blog 裡面有一段提示詞，你只要套上去，就可以把 Codex 比較囉嗦的方式變得比較像 Claude 的簡潔風格。說不定你會覺得其實也沒差太多。

### 方案二：雲端 API 分流

這是我最建議的方式。你應該把複雜的 task 和簡單的 task 區分不同的 API：

- **複雜 task** → Opus（透過 OpenRouter 或 Anthropic API）
- **簡單的高頻 daily 任務**（像 heartbeat 或簡單指令）→ Haiku、GPT mini、Gemini Flash

在良好設計的 skill 下，小模型都能完成你 95% 的事情。做太複雜或出錯的，才丟給大模型。

### 方案三：雲地分級（我認為最重要的）

這是 OpenClaw 最棒的一點——做到雲地分級。直接把快速的小模型切到地端。

今年出了一個很重要的小模型：**千問 3.5 的 27B**，它是一個 dense 模型，大家實測發現在一張 4090 或 5090 上就能跑出接近 Claude Sonnet 的能力。網路上甚至有一個版本是把 Opus 的推理過程蒸餾進去的，網友反饋非常好。

你大可以把這樣的 local 模型當作主力，負擔龍蝦 **99.9%** 的 task。至於最後那 5% 到 10% 的複雜任務，再適時使用雲端模型——Opus、GLM、ChatGPT。

而且 **Gemma 4 的 31B** 也出了，被認為很有可能挑戰千問 3.5 27B 的地位。趨勢很明顯：開源這邊會有越來越多能夠在地端、用消費級硬體跑起來的模型。

### 投資 Agent Infra 才是正解

隨著數位員工慢慢導入，Token 的使用只會爆發式向上。你永遠不可能完全依賴雲端 API，你只能在最需要、最重要的任務時去依賴 Anthropic 或 ChatGPT。

所以現在投資你自己的 **Agent Infra**——一個 OpenClaw 平台，加上你有權限切到地端、切到雲端、控制 Token 費用的架構——是一個非常重要的機制。

從投資 Agent Infra、降低 90% 到 95% 成本的第一步，就是**試著去開始測試你的千問或 Gemma**。有了這個基礎，你就不在意雲端廠商對你是好或不好、他們怎麼調整商業策略。因為一切都掌握在你手中。

> 詳細的三層方案分析、提示詞配置、Gemma 4 實測，請看完整文章：[Anthropic 封殺 OpenClaw 之後的三層替代方案](/anthropic-kills-openclaw-gpt54-migration-guide/)

---

## 坦白說

這兩個主題看起來是技術深度和商業策略，但背後的核心其實是同一件事：**你的 Agent 基礎設施到底掌握在誰手上。**

Claude Code 的四層壓縮告訴我們，一個生產級 Agent 的上下文管理有多複雜——3,960 行代碼，熔斷器、Cache Editing API、遞迴重試。大多數 Agent 框架連基本的壓縮都沒有。如果你要做自己的 Agent，至少應該有基本的工具結果清理、觸發邏輯、和失敗停止重試。大概 200 行代碼，就能解決 80% 的上下文問題。

而 Anthropic 封殺 OpenClaw 則告訴我們，依賴單一廠商永遠有風險。不是說 Anthropic 做錯了——人家 Terms of Service 寫得很清楚。但如果你的整個工作流只靠一家，那你就得接受他們隨時可以改規則的現實。

**掌握架構自主權，才是企業 AI 轉型的最終解答。**

---

## 延伸閱讀

### Claude Code 開源設計細節系列
- **EP1：** [拆解 Claude Code 的 System Prompt 源碼](/claude-code-system-prompt-source-code-analysis/)
- **EP2：** [資安最佳實踐：14 條建議，每條都有原始碼撐腰](/claude-code-security-best-practices-source-code-verified/)
- **EP3：** [上下文工程：四層壓縮機制的源碼級拆解](/claude-code-context-engineering-four-layer-compression/)

### Agent Infra 與替代方案
- [Anthropic 封殺 OpenClaw 之後的三層替代方案](/anthropic-kills-openclaw-gpt54-migration-guide/)
- [搞懂快取機制，從 Gemma 4 到 Claude Code 省 80% Token](/kv-cache-gemma4-claude-code-save-80-percent-token/)
- [本地模型的 Tool Calling 到底行不行？ToolCall-15 基準測試](/toolcall-15-local-llm-tool-calling-qwen-27b-sweet-spot/)
- [越級打怪的神級小模型：Qwen 3.5 與 9B 架構](/qwen-3-5-9b-small-model-god-tier-architecture/)
