---
layout: post
title: "用手錶跟龍蝦對話：OpenClaw、Anthropic 和一場 Channel 戰爭的啟示"
date: 2026-02-20 10:00:00 +0800
permalink: /openclaw-anthropic-channel-war/
description: "OpenClaw v2.19 出了 Apple Watch MVP，Anthropic 封鎖 OAuth 禁止第三方使用訂閱制，Sam Altman 收編 Peter Steinberger 擁抱開源。三件事串在一起，看到的不是技術競爭，而是 AI 產業最殘酷的現實：掌握 Channel 的人，才能決定模型的命運。"
image: /assets/images/anthropic-oauth-ban-official-docs.png
---

## 開場：用手錶跟龍蝦對話

OpenClaw v2.19 剛出了 Apple Watch MVP。

沒錯，你現在可以用手錶跟你的 AI Agent 對話了。Watch Inbox UI、通知推播、手錶端直接下指令——聽起來像科幻片，但它就是這週的 release notes。

我第一反應是：這個團隊的想像力也太大了吧。

但仔細想想，這其實不是想像力的問題。這是一個產品思維極度清晰的團隊，在回答一個非常具體的問題：

**「AI Agent 的介面應該在哪裡？」**

答案不是 IDE，不是 terminal，不是瀏覽器——是「你人在哪裡，它就在哪裡」。

Apple Watch、Telegram Streaming（逐字推播、inline button、用戶 reaction 觸發 agent event）、40+ 項安全加固、OTEL v2 遷移——這些不是花哨的功能堆疊，這是一個正在認真建設基礎設施的專案。

而同一個禮拜，Anthropic 在幹嘛？

封 OAuth。

---

## Channel 才是 AI 產業的王道

我想講一個很多人不願意面對的現實：**在 AI 產業，模型再強，沒有 Channel 就是零。**

讓我回顧一下歷史。

### 2024：Cursor 帶起 Anthropic

2024 年，AI Coding 真正變成可行的事情，靠的是什麼？

Cursor + Sonnet 3.5。

那時候 Cursor 的崛起帶動了整個 AI Coding 的生態，而 Sonnet 3.5 恰好是最適合 coding 的模型。但你仔細想——Anthropic 在這裡扮演的角色是什麼？

**是被選中的供應商。**

Channel 在 Cursor 手上。用戶黏性在 Cursor 手上。定價權、使用場景、用戶體驗——全部在 Cursor 手上。Anthropic 只是提供了後面的引擎。

而且你去看那時候的統計數據，2025 年初 ChatGPT 再怎麼不重視 coding，光是 GitHub Copilot 這個 Channel 依然是最大的 AI Coding 用戶群。不是因為 Copilot 的模型最強，而是因為它嵌在 VS Code 裡面——**Channel 決定了一切。**

### 2025：Claude Code 的誕生

然後 Claude Code 出現了。

這是 Anthropic 第一次除了 toB API 業務以外，真正掌握了 Channel。

Claude Code 讓 Anthropic 直接面對開發者。不用透過 Cursor，不用透過 Copilot，不用透過任何第三方。開發者打開 terminal，就是 Claude 的世界。

我在之前的文章寫過，[Claude Code 是用正確的介面連接真實世界](/shell-wrapper-2-anthropic-real-threat/)——Command Line 把整台電腦變成可被查詢、可被推理的狀態空間，而大語言模型恰好是用文字在思考的。這不是巧合，這是結構上最合理的選擇。

Claude Code 的成功，讓 Anthropic 終於不再只是「被別人選中的模型供應商」。

**但這個優勢，撐了不到一年。**

---

## OpenClaw 帶來的真正衝擊

老實說，從今年一月 OpenClaw 出現開始，我的 Claude Code 使用量就在慢慢下降。

不是因為 Claude Code 不好用。它依然是我見過最精準的 coding agent。但 OpenClaw demo 了一個全新的 use case，一個 Claude Code 刻意不做的事情：

**真正的 AI Agent。**

不是「幫你寫 code」的 agent，是「幫你過日子」的 agent。

Telegram 上收到訊息可以即時串流回覆。Google Calendar 自動排程。YouTube 影片自動處理。現在連 Apple Watch 都可以下指令了。

Claude Code 是一個極度克制的產品——它只做 coding，而且只在 terminal 裡面做。這個克制在技術上是對的，但在產品上，它留下了一個巨大的空白。

OpenClaw 就是衝著這個空白來的。

而且不只是功能上的空白。OpenClaw 帶來的是一種完全不同的產品哲學：

- **Claude Code 說：** 我是最聰明的 coding agent，你來 terminal 找我
- **OpenClaw 說：** 我在你的手機、手錶、Telegram、瀏覽器裡，你在哪我就在哪

這兩種哲學，面對的是完全不同規模的市場。

會用 terminal 的人全世界可能幾千萬。但會用手錶、會用 Telegram 的人，是幾十億。

---

## Anthropic 的連環失策

如果只是市場定位不同，那還好。真正讓我覺得「要洗牌了」的，是 Anthropic 這段時間的一連串操作。

### 第一刀：法務信（2026-01-27）

Anthropic 的法務團隊對 Peter Steinberger 發了 cease-and-desist，理由是「Clawd」跟「Claude」太像。

結果呢？

Peter 改名成 Moltbot（龍蝦脫殼的意思，蠻幽默的）。但改名過程中的 10 秒空窗期，被 crypto scammer 搶走了原本的 namespace，搞出一個 $CLAWD 代幣漲到 1600 萬美金市值。

然後再改名成 OpenClaw。

然後 Sam Altman 就出手了。

多家媒體的標題是：「$30B Fumble: Anthropic Kills 1.5M-Agent Beast - OpenAI Poaches Creator in Seconds!」

用法務信把最火的 agent 專案逼到競爭對手懷裡——這個操作，怎麼看都像是策略性失誤。

### 第二刀：OAuth 封鎖（2026-01-09 執行）

![Anthropic 官方文件明確禁止 OAuth 用於第三方產品](/assets/images/anthropic-oauth-ban-official-docs.png)

Anthropic 在服務器端部署了防護措施，封鎖了訂閱制 OAuth token 在第三方產品的使用。

錯誤訊息很直白：

> "This credential is only authorized for use with Claude Code and cannot be used for other API requests."

官方條款更明確：

> "Using OAuth tokens obtained through Claude Free, Pro, or Max accounts in any other product, tool, or service — including the Agent SDK — is not permitted and constitutes a violation of the Consumer Terms of Service."

Rails 之父 DHH 直接評論：「very customer hostile」。

之前很多團隊用 Claude Max 訂閱（$100-$200/月）搭配 OpenClaw、OpenCode、Roo Code 這些第三方工具，避開按用量計費的 API 成本。Anthropic 一刀切斷了這條路。

而且被發現 OpenCode（GitHub 上 107K+ stars）甚至在 spoof Claude Code 的 HTTP headers 來繞過限制。

### 對比：Sam Altman 的擁抱策略

2026 年 2 月 15 日，Sam Altman 在 X 上宣布：

> "Peter Steinberger is joining OpenAI to drive the next generation of personal agents. He is a genius with a lot of amazing ideas about the future of very smart agents interacting with each other to do very useful things for people."

同時承諾 OpenClaw 將以 foundation 形式維持開源，暗示可能會有 OpenAI 版本作為 ChatGPT 訂閱的一部分。

一邊在發法務信趕人，一邊在發 offer 搶人。

**這個對比太殘忍了。**

---

## 模型大洗牌：每個人都在被迫選邊站

OpenClaw 生態的爆發，連帶引發了另一個現象：模型選擇的大洗牌。

### Opus 4.6：最聰明，但太貴了

Opus 4.6 依然是這幾天網友們公認跑 OpenClaw 的智能首選。在複雜推理、長上下文理解、coding 品質上，它確實是目前最強的。

但問題很現實：**$25/1M output tokens。**

一個重度使用者一天燒掉 $50-100 是正常的。這不是一般人或小團隊能負擔的。

所以每個人都在被迫尋找替代方案。

### Kimi K2.5：免費 + 性能好

Moonshot AI 的 Kimi K2.5 在 agentic benchmarks 上表現超越 Opus 4.5，SWE-bench 成績亮眼。API 價格只要 $3/1M output tokens——是 Opus 的 **八分之一**。

Peter 之前就推過 Kimi K2 和 K2.1 Turbo，加上 Moonshot 直接推出了 Kimi Claw（基於 OpenClaw 框架的瀏覽器原生版本），Kimi K2.5 在 OpenClaw 生態裡的存在感越來越強。

而且它目前有免費額度，對個人用戶來說門檻極低。

### Gemini 3 Flash Preview：反應速度碾壓

Google 的 Gemini 3 Flash Preview 剛上線，跑出了 218 tokens/second 的速度，SWE-bench 78%。

最關鍵的是成本不到 Gemini 3 Pro 的四分之一，而且 Google 自己說「Outperforms 2.5 Pro while being 3x faster」。

對於需要快速回應的 agent 場景（比如 Telegram streaming、Apple Watch 互動），速度就是體驗。Gemini 3 Flash 在這個維度上是碾壓級的。

### MiniMax M2.5：地端性價比之王

MiniMax M2.5 是開源的 230B MoE 模型（10B active parameters），SWE-bench 80.2%——距離 Opus 4.6 的 80.8% 只差 0.6 個百分點。

關鍵數字：3-bit 量化後 101GB，可以跑在 128GB 統一記憶體的 Mac 上。

MiniMax 自己說：「$1 可以持續運行模型一小時，速度 100 tokens/second。」這是第一個讓人不用擔心成本的 frontier 模型。

對於在意數據隱私、想在地端跑的用戶，MiniMax M2.5 可能是目前最務實的選擇。

### 訂閱制的可能轉變

如果 Sam Altman 真的把 OpenClaw 整合進 ChatGPT 訂閱——哪怕只是部分功能——那訂閱制的用戶會瞬間暴增。

想想看：你已經在付 ChatGPT Plus 的錢了，現在告訴你可以直接跑 AI Agent，不用額外付 API 費用。這個 channel 效應會非常巨大。

---

## 坦白說

我的判斷可能有偏差。

我用 OpenClaw 的時間不算長，對它的很多功能還在摸索階段。我對 Anthropic 內部的決策邏輯也不清楚——也許 OAuth 封鎖有我不知道的財務壓力或合規考量。

但有幾件事我比較確定：

**確定的部分：**

1. **Channel 的重要性被反覆驗證。** Cursor 帶起 Anthropic，Claude Code 讓 Anthropic 拿回 Channel，現在 OpenClaw 又在重新分配 Channel。歷史在重演。

2. **Anthropic 的防守策略代價很高。** 法務信 + OAuth 封鎖，短期保護了自己的訂閱收入，但長期把最活躍的社群推向了競爭對手。這跟當年 Oracle 控告 Google 用 Java API 的邏輯有點像——贏了官司，輸了生態。

3. **模型的護城河正在消失。** 當 MiniMax M2.5 開源模型在 SWE-bench 上追到 Opus 4.6 只差 0.6%，當 Kimi K2.5 只要八分之一的價格就能跑出接近的品質——模型本身已經越來越難成為差異化的武器。

4. **OpenClaw 代表的不只是一個產品。** 它背後是先進的產品思維、巨量的社群流量、現在又有 OpenAI 加持。它有機會成為 AI Agent 時代的「Chrome」——不是最聰明的，但是覆蓋面最廣的。

**不確定的部分：**

1. **OpenAI 會怎麼整合 OpenClaw？** 是維持開源的獨立性，還是逐漸變成 ChatGPT 的附屬功能？Peter 加入 OpenAI 後的角色定位還不清楚。

2. **Anthropic 會不會調整策略？** 也許他們會推出更開放的第三方整合方案，或者用 Claude Code 的新功能來回應。目前看起來還沒有，但不代表不會。

3. **免費模型的品質天花板在哪？** Kimi K2.5 免費、MiniMax M2.5 幾乎免費，但「幾乎一樣好」和「真的一樣好」在生產環境是兩回事。對於要求極高可靠性的場景，Opus 4.6 的溢價可能還是值得的。

---

## 關鍵洞察

1. **AI 產業的競爭本質是 Channel 戰爭，不是模型戰爭。** 誰控制用戶的入口，誰就控制模型的命運。Cursor、Copilot、Claude Code、OpenClaw——每一次 Channel 的轉移，都帶來一次生態的洗牌。

2. **防守策略在開源生態裡是毒藥。** 法務信和 OAuth 封鎖可以保護短期利益，但在一個社群驅動的生態裡，這些動作只會加速用戶流失。Google 的 Android 策略（擁抱開源、用服務變現）遠比 Oracle 的 Java 策略有效。

3. **模型正在商品化，Agent 基礎設施才是新的差異化。** 當多個模型都能在 SWE-bench 跑到 78-80%，決定用戶選擇的就不再是模型本身，而是圍繞模型的使用體驗——持續性、跨設備、安全性、成本控制。這些都是 OpenClaw 在做的事。

4. **最大的 insight：Anthropic 當初靠 Cursor 被帶起來，用 Claude Code 脫離了 Channel 依賴。但 OpenClaw 證明了 coding 只是 agent 的一個子集——真正的 agent 市場比 coding 大十倍。** 如果 Anthropic 不能在更廣的 agent 場景裡建立自己的 Channel，那 Claude Code 的成功可能只是一個美麗的插曲。

---

## 延伸閱讀

- [從「套殼 1.0」到「套殼 2.0」：為什麼真正該緊張的是 Anthropic](/shell-wrapper-2-anthropic-real-threat/)
- [OpenClaw 架構深度拆解：Context、Memory 和 Token Crusher 的設計哲學](/openclaw-architecture-deep-dive/)
- [OpenClaw 成本優化實戰：從 $200/天到 $6/天的 97% 降幅](/openclaw-cost-optimization-guide/)
- [OpenClaw 安全隔離：Gmail Sandbox 與最小權限原則](/openclaw-security-isolation-gmail-sandbox/)
- [Peter Steinberger 的 Agentic Engineering 哲學：Just Talk to It](/peter-steinberger-agentic-engineering-philosophy/)
