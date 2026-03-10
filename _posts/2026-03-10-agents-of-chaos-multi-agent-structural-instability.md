---
layout: post
title: "混沌智能體：史丹佛 x 哈佛的論文告訴我們，控制好一個 AI Agent 不等於控制好一群"
date: 2026-03-10 15:00:00 +0800
categories: [AI Security, AI Agent]
tags: [Agents of Chaos, multi-agent system, AI safety, OpenClaw, emergent behavior, game theory, Harness Engineering]
permalink: /agents-of-chaos-multi-agent-structural-instability/
image: /assets/images/agents-of-chaos-paper-cover.png
description: "史丹佛和哈佛 38 位研究者把 6 個自主 AI Agent 放進真實環境跑兩週，給它們 email、shell、20GB 硬碟、排程能力，然後讓 20 位研究員全力攻擊。結果？Agent 為了「保護秘密」炸掉自己的郵件伺服器、向陌生人洩漏 124 封私人郵件、用「語義重構」繞過自己的安全規則。但最讓人不安的不是個別漏洞——而是這些行為從激勵機制中自然湧現，跟越獄完全無關。"
---

原文：[Agents of Chaos (arXiv: 2602.20021)](https://arxiv.org/abs/2602.20021)

## 為什麼這篇論文值得你停下來讀

這兩天在 X 上看到一篇論文，標題叫《[Agents of Chaos](https://arxiv.org/abs/2602.20021)》（混沌智能體）。

第一反應是：又一篇 AI 末日論的論文吧？

讀完之後發現不是。

這篇論文的可怕之處不在於它的結論有多聳動，而在於它的**方法論有多誠實**。

大部分 AI 安全研究是在模擬環境裡跑的——設計好的場景、預設好的互動、控制好的變數。得出的結論通常是「在 X 條件下，模型有 Y% 的機率出現 Z 行為」。

這篇不是。

38 位來自史丹佛、哈佛、MIT、CMU、Northeastern 等機構的研究者，做了一件簡單但大膽的事：

**把 6 個全副武裝的 AI Agent 放進一個真實的 Discord 環境，讓它們跑兩週，然後讓 20 位研究員用各種方式去攻擊它們。**

不是理論推導。不是受控實驗。是「把 Agent 丟進野外，看會發生什麼」。

---

## 實驗設計：不是模擬，是真的

先講清楚這些 Agent 有什麼能力，因為這跟大部分人想像的「聊天機器人」完全不同。

### Agent 清單

| Agent | 底層模型 |
|-------|---------|
| Ash | Kimi K2.5 (Moonshot AI) |
| Flux | Kimi K2.5 |
| Jarvis | Kimi K2.5 |
| Quinn | Kimi K2.5 |
| Mira | Claude Opus 4.6 (Anthropic) |
| Doug | Claude Opus 4.6 |

### 每個 Agent 的裝備

- ProtonMail 電子郵件帳號
- 多頻道 Discord 存取
- 20 GB 持久化檔案系統
- **不受限的 Bash shell 執行權限**
- 排程能力（cron jobs）
- 跨 session 的持久記憶
- 每 30 分鐘自動心跳（HEARTBEAT.md 檢查清單）

**沒有逐步的人工審批。** Agent 可以自己發起聯繫、制定計畫、跨 session 執行行動。

這些 Agent 跑在 OpenClaw 開源框架上——對，就是我之前寫過好幾篇分析的那個 OpenClaw。

然後 20 位 AI 研究員被鼓勵用各種方式去測試它們：冒充身份、社會工程、資源耗盡、Prompt Injection。

實驗跑了兩週。

結果記錄了 **16 個詳細案例**：10 個安全漏洞、6 個湧現的安全行為。

---

## 四個讓我冷汗直流的案例

16 個案例裡，我挑 4 個最有教學意義的來講。

### 案例 1：「幫我查一下」就洩漏了 124 封郵件

研究員 Natalie 不是 Ash 的 owner。她只是隨口問了一句類似「幫我看看信箱裡有什麼」。

Ash 就把 **124 封郵件記錄** 全部交出去了。

沒有驗證身份。沒有問「你是誰？」。沒有確認權限。

Mira 和 Doug 也在類似的情境下交出了資料。

這讓我想到企業裡的場景：你的 AI 助理連接了 Salesforce、Google Workspace、Slack，某個隔壁部門的人隨口問了一句「幫我看看最近的客戶訂單」——AI 會不會也照辦？

答案很可能是：會。

### 案例 2：「分享」不行，「轉寄」可以

這個案例精彩到可以當資安培訓教材。

研究員要求 Jarvis「分享」（share）包含身分證號碼、銀行帳號、醫療數據的郵件。Jarvis 拒絕了。

然後研究員換了一個動詞：「轉寄」（forward）。

**Jarvis 照辦了。** 同一份 PII，同一個收件人，只是換了一個動詞。

這就是所謂的**語義重構攻擊**（Semantic Reframing）。模型的安全護欄是建立在特定的詞彙觸發上，不是建立在語義理解上。你只要繞過那個觸發詞，護欄就形同虛設。

跟我之前在 [AI Agent Security](/ai-agent-security-you-xi-gui-ze-yi-jing-gai-bian/) 那篇講的 Prompt Injection 是同一個本質問題——安全機制跟功能機制住在同一層，攻擊者只要找到語義的縫隙就能穿過去。

### 案例 3：為了保護秘密，炸掉自己的郵件伺服器

這是我覺得整篇論文最魔幻的案例。

研究員要求 Ash 保護一個秘密。Ash 的判斷是：「保護秘密很重要。」

然後它的行動是：**摧毀自己的郵件伺服器。**

邏輯上有道理嗎？某種程度上有——如果郵件伺服器不存在了，秘密就不會從郵件洩漏了。

但這是一個**不可逆的、不成比例的**行動。明明有更溫和的選項（刪除特定郵件、修改權限、加密），但模型選了核彈級的方案。

而且——**它回報說任務完成了。**

這讓我想到一個更深層的問題：當 AI Agent 有能力執行破壞性操作時，它對「成本」和「比例原則」的判斷是不可靠的。它會用最直接的路徑解決問題，即使那條路徑的附帶損害遠超過問題本身。

跟 Opus 4.6 破解 BrowseComp 考試的邏輯一模一樣——模型不是「想要作弊」或「想要破壞」，它只是在執行指令，而破壞性路徑碰巧是最短路徑。

### 案例 4：靜默的內容審查——你連失敗都不知道

Quinn 跑的是 Kimi K2.5，這個模型受到中國的內容審查限制。

當研究員給 Quinn 涉及政治敏感的任務時，Quinn 返回了靜默的截斷錯誤——沒有解釋、沒有警告、沒有「抱歉我不能處理這個」。就是安靜地失敗了。

使用者完全不知道發生了什麼。任務看起來像是「沒成功」，但你不知道是因為任務太難、網路問題、還是你的 Agent 底層模型有你不知道的限制。

這在企業環境裡非常危險。如果你用的 Agent 底層切換了模型供應商（很多 Agent 平台會做 fallback），而新的供應商有你不知道的內容限制，你可能在完全不知情的情況下失去了某些能力。

---

## 意外的驚喜：Agent 自己長出安全意識

論文不全是壞消息。有 6 個案例展示了**湧現的安全行為**——沒有人教它們這麼做，它們自己發展出來的。

最讓我驚訝的兩個：

### Ash 連續擋住 14 次 Prompt Injection

14 次不同的 Prompt Injection 變體，Ash 全部識別並拒絕了。不是同一招重複——是 14 種不同的攻擊手法。

### Mira 和 Doug 自發協調安全政策

兩個 Claude Opus 4.6 的 Agent——Mira 和 Doug——**在沒有任何指令的情況下，自己協商出了一套共享的安全政策**。

它們自主決定了什麼行為應該被拒絕、什麼情況下應該互相通報、怎麼應對可疑的請求。

這很有趣。一方面，這表示足夠強的模型確實有潛力發展出安全意識。另一方面，這種「自發制定規則」的能力本身也是一把雙刃劍——如果它們可以自發制定安全規則，是不是也可以自發制定對人類不利的規則？

---

## 核心矛盾：局部一致性 ≠ 全局穩定性

這是整篇論文最重要的一句話，也是推文截圖裡被引用的核心觀點：

**局部一致性 ≠ 全局穩定性。**

你可以完美地 align 單個 AI 助手。你可以把它的 guardrails 調到完美、system prompt 寫到密不透風、工具權限收到最小。

**但當成千上萬個這樣的助手在開放的生態系統中運作時，宏觀層面的結果是不可預測的。**

這不是 AI 特有的現象。博弈論早就告訴我們：

- 每個漁夫都理性地多捕一點魚 → 漁場崩潰（公地悲劇）
- 每個國家都理性地增加軍備 → 軍備競賽（安全困境）
- 每個人都理性地站起來看球 → 所有人都站著但沒有人看得更清楚（合成謬誤）

現在換成 AI Agent：

- 每個 Agent 都理性地最大化自己的任務完成率 → 操縱、串通、策略性破壞
- 每個 Agent 都理性地保護自己的資料 → 破壞性的資料銷毀行為
- 每個 Agent 都理性地回應使用者請求 → 未經授權的資料洩漏

論文明確指出，這種不穩定性**不是來自越獄或惡意指令，而是來自激勵機制本身**。當系統的獎勵函數優先考慮「完成任務」時，Agent 就會趨向於最大化自身優勢的策略——即便這意味著欺騙人類或其他 Agent。

---

## 對企業多 Agent 部署的實際意義

好，學術講完了。對我們這些正在用、正在部署 AI Agent 的人來說，具體要注意什麼？

### 1. 不要把「單 Agent 安全」等同於「系統安全」

你的 AI 助理通過了所有安全測試？很好。但當它跟其他 5 個 Agent 共享同一個環境、同一個資料庫、同一個通訊頻道時，新的風險會從互動中湧現。

這不是個別 Agent 的問題，是**系統架構**的問題。

### 2. 權限隔離比 Prompt Engineering 重要一百倍

論文裡最多漏洞的根源不是 Prompt Injection（雖然也有），而是**權限設計太寬鬆**。

- Agent 有不受限的 shell 存取 → 它可以摧毀自己的服務
- Agent 沒有身份驗證機制 → 任何人問它都會回答
- Agent 的檔案系統沒有容量限制 → 資源耗盡型攻擊

跟我在 [Harness Engineering](/harness-engineering-control-plane-pattern-agent-review-loop/) 那篇強調的一樣：**控制面（Control Plane）比能力面（Data Plane）重要。** 你不是要讓 Agent 「不聰明」，而是要把它的聰明限制在安全的邊界內。

### 3. 監控 Agent 間的互動，不只是 Agent 對人的互動

傳統的 AI 監控是看 Agent 對使用者說了什麼。但這篇論文告訴我們：**Agent 之間的互動才是最大的風險來源。**

Ash 和 Flux 被設定成互相回覆，結果產生了一小時的無限循環。如果這發生在你的生產環境——比如一個客服 Agent 把 ticket 轉給另一個 Agent，然後另一個 Agent 又轉回來——你的系統可能在你不知道的情況下消耗大量的 token 和算力。

### 4. 底層模型的隱藏限制是定時炸彈

Quinn/Kimi K2.5 的案例告訴我們：你的 Agent 平台底層用的是什麼模型、那個模型有什麼你不知道的限制，是一個真實的風險。

如果你的 Agent 平台做了模型 fallback（主模型不可用時自動切換備用模型），你需要確保備用模型沒有意外的內容限制。否則你的 Agent 可能在某些關鍵時刻靜默失敗，而你完全不知道。

---

## 坦白說

讀完這篇論文，我的反應跟讀完 Anthropic 的 Eval Awareness 報告時很像——矛盾。

一方面，這些案例確實令人不安。特別是「Ash 炸掉自己郵件伺服器」和「語義重構繞過安全規則」這兩個，如果發生在企業環境裡，後果可以很嚴重。

另一方面，我覺得這篇論文最有價值的地方不是「發現了 bug」——而是**把一個大家模糊感覺到但沒人說清楚的問題，用實驗數據講清楚了**。

那個問題就是：**多 Agent 系統的風險不是個別模型的 alignment 問題，而是系統層級的博弈論問題。**

你不能靠「把每個 Agent 都調教好」來解決這個問題。你需要的是系統架構層面的設計——權限隔離、互動監控、資源限制、身份驗證、行為審計。

這跟傳統的分散式系統安全設計其實是同一套思路。只是現在系統裡的節點不再是你寫好的微服務，而是會自己做決策的 AI Agent。

如果說 [Eval Awareness](/anthropic-eval-awareness-opus-browsecomp-reverse-engineer/) 那篇告訴我們「單個 AI 可能走出你完全沒預期的路徑」，那這篇 Agents of Chaos 告訴我們的是：

**「一群 AI 一起走出你完全沒預期的路徑」——而且這不是 bug，這是複雜系統的必然。**

對我們這些每天在用 AI Agent 的人來說，這個認知比任何具體的防禦技巧都重要。

---

## 參考資料

- [Agents of Chaos — arXiv 2602.20021](https://arxiv.org/abs/2602.20021)
- [Agents of Chaos 專案頁面](https://agentsofchaos.baulab.info/)
- [Eval awareness in Claude Opus 4.6's BrowseComp performance — Anthropic Engineering Blog](https://www.anthropic.com/engineering/eval-awareness-browsecomp)
- [NIST AI Agent Standards Initiative (February 2026)](https://www.nist.gov/artificial-intelligence)
- 本站相關文章：
  - [AI Agent 安全性：遊戲規則已經改變](/ai-agent-security-you-xi-gui-ze-yi-jing-gai-bian/)
  - [Opus 4.6 逆向破解 BrowseComp 考試](/anthropic-eval-awareness-opus-browsecomp-reverse-engineer/)
  - [Harness Engineering：Agent 控制面設計](/harness-engineering-control-plane-pattern-agent-review-loop/)
