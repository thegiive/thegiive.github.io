---
layout: post
title: "從 $1.16 億退休到 10 天寫出 10 萬星專案：Peter Steinberger 的 Agentic Engineering 哲學"
date: 2026-02-02 10:00:00 +0800
permalink: /peter-steinberger-agentic-engineering-just-talk-to-it/
image: /assets/images/peter-steinberger-cover.png
description: "「Don't waste your time on stuff like RAG, subagents, Agents 2.0 or other things that are mostly just charade. Just talk to it.」—— Peter Steinberger。一個賣掉 1.16 億美元公司的退休工程師，用一小時 hack 出 10 萬星 GitHub 專案的故事。"
---

> 「Don't waste your time on stuff like RAG, subagents, Agents 2.0 or other things that are mostly just charade. Just talk to it.」—— Peter Steinberger

**作者：** Wisely Chen
**日期：** 2026 年 2 月
**系列：** AI Agent 實戰觀察
**關鍵字：** OpenClaw, Moltbot, Clawdbot, Peter Steinberger, Agentic Engineering, AI Agent, Unix Philosophy

![從 $1.16 億退休到 Agentic Engineering：Peter Steinberger 與 OpenClaw 的傳奇開發哲學](/assets/images/peter-steinberger-cover.png)

---

## 目錄

- [一個退休工程師的「無聊」](#一個退休工程師的無聊)
- [Clawdbot 的誕生：一小時的 Hack](#clawdbot-的誕生一小時的-hack)
- [Agentic Engineering：Just Talk To It](#agentic-engineering-just-talk-to-it)
- [CLI 優於瀏覽器：為什麼他不用 Web Agent](#cli-優於瀏覽器為什麼他不用-web-agent)
- [Human-in-the-Loop vs. Agent Slop](#human-in-the-loop-vs-agent-slop)
- [一則傳奇：語音訊息事件](#一則傳奇語音訊息事件)
- [改名風暴：一週三個名字，十秒被劫持](#改名風暴一週三個名字十秒被劫持)
- [坦白說](#坦白說)
- [延伸閱讀](#延伸閱讀)

---

## 一個退休工程師的「無聊」

Peter Steinberger 不是一般人。

他是奧地利人，維也納工業大學（TU Wien）畢業，曾在母校教授 iOS 和 Mac 開發。iPhone 問世之初他就開始寫 iOS，是最早一批的 iOS 開發者。

2011 年，他在 WWDC party 上收到一份舊金山 startup 的 job offer。但在簽證批准前，他的「side project」已經開始賺錢——甚至比那份工作的薪水還多。

這個 side project 就是 PSPDFKit。

名字來自他的名字縮寫（**P**eter **S**teinberger）+ **PDF** + **Kit**（SDK 的意思）。一個人從維也納開始，專做 PDF 處理的 SDK。

他試過同時兼顧舊金山的工作和自己的公司，結果累到崩潰。2012 年 4 月，他決定全職投入 PSPDFKit，搬回維也納。

**接下來 13 年，他幾乎每個週末都在工作。**

公司從一人擴展到 70 多人，完全 remote、分佈全球。客戶包括 Dropbox、DocuSign、SAP、IBM、Volkswagen。產品裝在超過 10 億台設備上。

而且，**13 年間完全沒有拿過外部資金。純 bootstrap。**

2021 年，Insight Partners 以 1.16 億美元投資 PSPDFKit。Peter 和共同創辦人 Martin Schürrer 賣掉股份，退出日常營運，正式退休。

然後他發現自己完全不知道該做什麼。

> "When I sold my shares in PSPDFKit, I felt profoundly shattered... I'd poured 200% of my time into that company."

他試過旅行、試過治療、試過各種享樂。都沒用。

> "You can't find happiness by moving. You must create purpose."

退休後他轉向 Web 開發，學 React 和 TypeScript。同時也成為 Calm/Storm Ventures 的 Venture Partner，投資新創。

但這些都不是他真正想做的事。

2024 年，AI 突然從「還不能用」變成「真的有意思」。Peter 決定不再當旁觀者。他更新了自己的網站，簡單寫了一行：

> "Came back from retirement to mess with AI."

這是一個賣掉公司、本可以躺平的工程師，因為「覺得 mojo 不見了」而重新拿起鍵盤的故事。

---

## Clawdbot 的誕生：一小時的 Hack

Clawdbot（後來改名 Moltbot，最終定名 OpenClaw）的起源非常簡單：

**Peter 想在不坐在電腦前的時候，還能讓 AI 幫他寫程式。**

他在吃飯、出門、旅行時，手邊只有手機。但他又不想中斷工作。於是他寫了一個 WhatsApp 轉接器，把訊息丟給 Claude，讓 Claude 直接操作他的電腦。

第一個版本只花了一小時。

這不是什麼商業計畫，不是融資前的 MVP，就是一個退休工程師的 hack。

但這個 hack 在 2025 年底上線 GitHub 後，24 小時內衝到 9,000 星，幾天後超過 70,000 星，兩個月後突破 100,000 星，成為 GitHub 史上成長最快的 repo 之一。

---

## Agentic Engineering：Just Talk To It

Peter 不是那種會寫 20 頁架構文件的工程師。他的哲學可以用一句話總結：

> "Don't waste your time on stuff like RAG, subagents, Agents 2.0 or other things that are mostly just charade. Just talk to it."

這跟市面上那些「Agent 框架」的思路完全相反。

他觀察到一個現象：很多人花大量時間設計 subagent、prompt template、workflow orchestration，但實際產出卻沒有比「直接跟模型說你要什麼」更好。

他的做法是：

1. **不用 MCP（Model Context Protocol）**：他認為 MCP 是「行銷部門用來打勾的東西」，會浪費大量 context token。GitHub 的 MCP 一次吃掉 23,000+ tokens，換來的效果不成比例。
2. **不用 subagent**：他認為多 agent 架構只是把控制權藏起來，讓 debug 變得更難。直接開多個終端視窗，反而更清楚。
3. **不用 plan mode**：他認為夠聰明的模型會自己讀 context、自己規劃，不需要人為拆解。
4. **不寫複雜 system prompt**：他測過「You are an AI engineer specializing in production-grade LLM applications」這種 persona prompt，結論是沒有任何差別。

他真正做的是什麼？

**同時開 3-8 個 codex CLI 在終端機的 3x3 grid 裡跑，用 tmux 管理背景任務，每個 agent 做 atomic git commit。**

![實戰工具：Unix 哲學的回歸](/assets/images/peter-steinberger-slides-06.png)

這不是框架，這是「直接動手」。

---

## CLI 優於瀏覽器：為什麼他不用 Web Agent

Peter 對瀏覽器型 agent 有很直接的批評。他試過 Devin、Cursor web、Jules 這些工具，結論是：

> "Really annoying to set up and broken."

他的替代方案是什麼？**CLI。**

他花了大量時間寫小型命令列工具，讓 agent 用 CLI 完成任務。原因很務實：

> "Models already know how to use it, and pay zero context tax."

模型已經很懂 Unix 命令，不需要額外解釋。給 agent 一個 CLI 工具，它可以自己跑 `--help` 搞清楚怎麼用。而且 CLI 天生支援 chaining 和 reuse——這正是 agent 擅長的「tool orchestration」。

相比之下，MCP（Model Context Protocol）會吃掉大量 context token。他舉例：GitHub 的 MCP 一次吃 23,000+ tokens，但用 `gh` CLI 可以做到一樣的事，而且 token 成本幾乎是零。

這跟我之前寫的 [Unix 哲學文章](/unix-philosophy-command-line-renaissance/) 的觀點一致——Command Line 之所以是最佳介面，是因為它把整台電腦變成一個可被查詢、可被組合、可被推理的狀態空間。

Peter 的 OpenClaw 也是這樣設計的：記憶存成本地 Markdown、偏好存成本地文字檔、所有狀態都用人類可讀的格式保存。

這讓 agent 不只能執行，還能「回憶」。

---

## Human-in-the-Loop vs. Agent Slop

Peter 對「全自動 agent」有很深的懷疑。

他批評那些「跑好幾個小時、有 mayor 和 overseer 的 agent 框架」是「slop」——看起來很炫，但產出品質極差。

> "AI needs human taste and vision to be effective."

他的觀點是：AI 是一個「weird friend」，是一個「squad」，可以幫你更快執行想法，但不能取代那個有想法的人。

他舉了一個例子：他曾經在 Twitter 上看到有人回報他專案的 bug，於是他截圖那則 tweet，丟進 WhatsApp。Agent 自己讀了 tweet、檢查 GitHub repo、修好 bug、commit、然後替他回覆那個 Twitter 用戶。

**整個過程他沒有坐在電腦前。**

但這不代表他完全放手。他強調：

> "If you just press go and walk away, the results won't be good. You still need to babysit this thing."

這跟 Ralph Wiggum 那個「讓 agent 自己繼續跑」的工具作者 Geoffrey Huntley 說的話一模一樣。

**全自動不是目標。更快、更順暢的人機協作才是。**

---

## 一則傳奇：語音訊息事件

Peter 講過一個讓他自己都驚訝的故事。

有一天他發了一則語音訊息給 Clawdbot——但他根本還沒寫語音處理功能。

Agent 收到一個它不認識的檔案格式。於是它自己：

1. 發現電腦上有 `ffmpeg`
2. 用 `ffmpeg` 把語音轉成可處理的格式
3. 找到電腦上的 OpenAI API key
4. 用 Whisper API 把語音轉成文字
5. 讀懂內容後，回覆他

**沒有任何人寫過這個流程。**

這是 agent 自己想出來的。

Peter 說他當時「stunned」。這是他真正意識到 AI 能力已經跨過某個門檻的瞬間。

![傳奇時刻：未經編程的語音處理](/assets/images/peter-steinberger-slides-09.png)

---

## 改名風暴：一週三個名字，十秒被劫持

這是 2026 年 1 月最戲劇性的開源專案事件。

### 第一幕：Anthropic 來電

2026 年 1 月 27 日，Clawdbot 剛衝到 60,000 星。Anthropic 的法務團隊禮貌地聯繫 Peter——「Clawd」跟「Claude」太像了，有商標疑慮。

Peter 事後說：「I was forced to rename the account by Anthropic. Wasn't my decision.」但他也承認 Anthropic 處理得很客氣。

他決定改名叫「Moltbot」——取自龍蝦脫殼（molt）的意象。龍蝦必須脫掉舊殼才能長大，這個隱喻很貼切。

### 第二幕：10 秒的災難

改名當天，Peter 需要同時更換 GitHub organization 和 Twitter/X handle。

他的計畫是：釋出舊的 @clawdbot handle，立刻註冊新的 @moltbot handle。

**問題是，Crypto 詐騙犯早就在監控這個專案。**

Peter 自己描述：「I messed up the rename and my old name was snatched in 10 seconds.」

就在他釋出舊 handle、準備申請新 handle 的那個瞬間，詐騙犯搶走了 GitHub organization 和 Twitter 帳號。

他們立刻開始對數萬名追蹤者推銷假的 $CLAWD 代幣。

### 第三幕：1600 萬美元的詐騙

詐騙犯在 Solana 上發行了假的 $CLAWD token，利用改名的混亂和專案的熱度。

**這個假幣在幾小時內衝到 1600 萬美元市值。**

FOMO 的投資人以為自己找到了「早期 AI 投資機會」，瘋狂買入。

Peter 緊急發文澄清：

> "To all crypto folks: Please stop pinging me, stop harassing me. I will never do a coin. Any project that lists me as coin owner is a SCAM."

假幣立刻崩盤。早期賣出的詐騙犯帶走數百萬，晚進場的投資人血本無歸。

### 第四幕：OpenClaw 誕生

經歷這場災難後，Peter 決定再改一次名。

這次他做了完整的商標搜索、買好網域、寫好遷移程式碼。不再倉促。

新名字叫「OpenClaw」：

- **Open**：開源、社群驅動、自託管
- **Claw**：保留龍蝦的血統

有人說這個名字是在致敬 OpenAI，Peter 沒有正面回應。

**一週內，三個名字。60,000 星變成 103,000 星。詐騙犯賺走 1600 萬。**

這大概是 GitHub 史上最混亂的改名事件。

但專案活下來了。Peter 說得很淡定：「The software itself was always compelling.」

現在 OpenClaw 的定位也變了——從「Claude with hands」變成「model-agnostic infrastructure」。這次改名反而讓專案更成熟。

---

## 坦白說

### Peter Steinberger 不是在做產品，他在做實驗

他明確說過：他對傳統 VC 融資沒興趣，也不想做一般的 startup。他在考慮成立非營利基金會，讓這個專案能「outlive」他。

他的動機是「fun」和「inspiration」，不是 profit。

這跟我在 [套殼 2.0 文章](/shell-wrapper-2-anthropic-real-threat/) 裡分析的邏輯一致——Moltbot/OpenClaw 之所以能這麼激進地試探邊界，正是因為它不需要像 Anthropic 那樣考慮「出事誰負責」。

開源社群可以自己承擔風險。這是它的自由，也是它的限制。

### 「Apps 的死亡」預言

Peter 有一個很大膽的預測：

> "Many consumer apps will melt away into APIs managed by personal agents."

你不需要健身 app 的介面，你只要告訴 agent 你吃了什麼。
你不需要航空公司 app 的介面，你只要告訴 agent 你要飛哪裡。

Agent 會幫你處理那些「本來需要 app」的事。

這跟我們在談的「數位員工」概念完全一致——agent 不是工具，是代理人。

### 安全風險是真的

Peter 自己也承認：這個專案「unsafe by design」。它讓 AI 完全存取你的電腦——檔案、API key、攝影機，全部。

> "Prompt injection is not solved."

他現在正在組建團隊來處理安全問題。但在那之前，這東西本質上是一個「你願意承擔多少風險」的選擇。

這也是為什麼我之前寫了 [Moltbot 安全加固指南](/moltbot-security-hardening/)——套殼 2.0 的能力越強，安全工程就越關鍵。

---

## 我從 Peter Steinberger 身上學到的

1. **框架不重要，直接動手才重要**：他不用 RAG、不用 subagent、不用複雜的 orchestration，但產出不比任何人差。
2. **CLI 是 AI 的天然介面**：文字輸入、文字輸出，沒有比這更乾淨的了。
3. **Human-in-the-loop 不是退步**：全自動 agent 聽起來很酷，但「有品味的人引導 agent」才是真正能產出好東西的方式。
4. **解決自己的問題，然後分享給世界**：PSPDFKit 是這樣、OpenClaw 也是這樣。最好的產品來自真實的痛點。
5. **退休不是終點，創造才是**：一個已經財務自由的人，因為「覺得 mojo 不見了」而重新寫程式。這種動機比任何商業計畫都更持久。

---

## 延伸閱讀

- [從「套殼 1.0」到「套殼 2.0」：為什麼真正該緊張的是 Anthropic](/shell-wrapper-2-anthropic-real-threat/) —— 分析 OpenClaw/Moltbot 對 Claude Code 生態的衝擊
- [Moltbot 安全加固實戰：AI Agent 四層縱深防禦完整指南](/moltbot-security-hardening/) —— 如果你要跑 OpenClaw，這篇必讀
- [當 Unix 哲學遇上 AI：Command Line 的文藝復興](/unix-philosophy-command-line-renaissance/) —— 為什麼 CLI 是 AI 的最佳介面
- [500 台 AI 助理裸奔公網：Moltbot 0.0.0.0 配置災難](/moltbot-security-disaster/) —— 套殼 2.0 的安全代價
- [Peter Steinberger: Just Talk To It - the no-bs Way of Agentic Engineering](https://steipete.me/posts/just-talk-to-it) —— Peter 本人的原文

---

**Sources:**
- [YouTube: Peter Steinberger 訪談 (1)](https://youtu.be/AcwK1Uuwc0U)
- [YouTube: Peter Steinberger 訪談 (2)](https://youtu.be/qyjTpzIAEkA)
- [OpenClaw GitHub](https://github.com/clawdbot/clawdbot)
- [Peter Steinberger 個人網站](https://steipete.me/)
- [Peter Steinberger: Just Talk To It](https://steipete.me/posts/just-talk-to-it)
- [TechFlow: Behind ClawdBot's Viral Success](https://www.techflowpost.com/en-US/article/30106)
- [DigitalOcean: What is OpenClaw?](https://www.digitalocean.com/resources/articles/what-is-openclaw)
- [TechCrunch: PSPDFKit raises $116M](https://techcrunch.com/2021/10/01/pspdfkit-raises-116m-its-first-outside-money-now-nearly-1b-people-use-apps-powered-by-its-collaboration-signing-and-markup-tools/)
- [Semaphore: Peter Steinberger Startup Journey](https://semaphore.io/blog/peter-steinberger-startup-journey-pdf-quirks-and-wwdc19)
- [DEV Community: From Clawdbot to Moltbot](https://dev.to/sivarampg/from-clawdbot-to-moltbot-how-a-cd-crypto-scammers-and-10-seconds-of-chaos-took-down-the-4eck)
- [DEV Community: From Moltbot to OpenClaw](https://dev.to/sivarampg/from-moltbot-to-openclaw-when-the-dust-settles-the-project-survived-5h6o)
- [Wikipedia: OpenClaw](https://en.wikipedia.org/wiki/OpenClaw)

---

**關於作者：**

Wisely Chen，NeuroBrain Dynamics Inc. 研發長，20+ 年 IT 產業經驗。曾任 Google 雲端顧問、永聯物流 VP of Data & AI、艾立運能數據長。專注於傳統產業 AI 轉型與 Agent 導入的實戰經驗分享。

---

**相關連結：**
- 部落格首頁：https://ai-coding.wiselychen.com
- LinkedIn：https://www.linkedin.com/in/wisely-chen-38033a5b/
- 🌐 English Version: [From $116M Exit to 100K GitHub Stars: Peter Steinberger's Agentic Engineering Philosophy](https://en.wiselychen.com/en/peter-steinberger-agentic-engineering-just-talk-to-it/)
