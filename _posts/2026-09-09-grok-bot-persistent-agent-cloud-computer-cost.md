---
layout: post
title: "Grok Bot：xAI 用 30 美金賣你一台 150 美金的 VM，還附 AI 員工"
date: 2026-09-09 09:00:00 +0800
permalink: /grok-bot-persistent-agent-cloud-computer-cost/
tags: [Grok Bot, xAI, agent, persistent agent, Claude Code, Codex, harness engineering, agent security, token cost]
categories: [AI Agent]
image: /assets/images/grok-bot-persistent-agent-cover.png
description: "xAI 的 Grok Bot 在 2026 年 8 月 11 日 beta 上線，產品定位不是聊天視窗，而是「有自己雲端電腦的 AI 隊友」——你幫它取名字、給職位、登進你的工具，關掉筆電它還在跑。社群反應兩極：有人喊 OpenClaw 時刻，有人實測後發現五個 Bot 共用一台機器、一組登入，刪掉一個 Bot 它的密碼還留著。一位 $300 方案用戶說 token 燒速是同級 Claude/ChatGPT 的四到五倍。這篇拆解 persistent-identity agent 的真正差異，以及這個設計選擇的好處和代價為什麼都比多數人以為的大。"
author: Wisely Chen
faq:
  - question: "Grok Bot 跟 Claude Code / Codex 到底差在哪？"
    answer: "核心差異不在模型能力，在 agent 的生命週期。Claude Code 和 Codex 是 session-based agent——你開一個 session 下指令，執行完就結束，下次不記得你。Grok Bot 是 persistent-identity agent——每個 Bot 有名字、有記憶、有自己的雲端 Linux VM，可以 24/7 在線、跨 session 保留狀態。實際體驗上，Claude Code 在寫碼任務上仍被多數用戶認為較強；Grok Bot 的強項是非工程師也能用、可以平行開多個 Bot 協作、關掉筆電 Bot 還在跑。一位用戶的說法是：寫 code 用 Claude Code，管桌面和系統用 Grok Bot。"
  - question: "Grok Bot 的安全問題具體是什麼？"
    answer: "最核心的架構特性是：同一個用戶的所有 Bot 共享一台雲端電腦（Cloud Computer），包括瀏覽器 cookie、登入 session、檔案系統、CLI 憑證。官方文件明確寫著「do not use separate Bots as a security boundary」。實測顯示刪掉一個 Bot，它建立的登入和檔案不會被清除，其他 Bot 仍可存取。對企業而言，這代表一個 Bot 被 prompt injection 攻擊時，blast radius 不是那一個 Bot 的任務，而是那台電腦上所有已登入系統的所有存取權限。2026 年 9 月 3 日上線的 Enterprise 版加了用戶之間的隔離，但同一用戶內的 Bot 共享架構不變。"
  - question: "Grok Bot 的 token 消耗到底有多高？"
    answer: "沒有官方公開數字，以下是用戶回報：一位 $300/月（SuperGrok Heavy）方案用戶說 token 燒速是 ChatGPT 或 Claude 同級方案的四到五倍。另一位用戶回報 $50 on-demand 額度五到十分鐘燒完。always-on agent 跟 session-based agent 的根本差異是：Bot 即使沒在執行你的指令，也在消耗 token——彼此協調、回報進度、等待回應都算。每個方案有每週 token 額度，超過照量計費，但 weekly cap 數字未公開。2026 年 9 月 5 日 xAI 全面重置 token pool，稱 routing 和 caching 優化提升效率約 10%。"
  - question: "Grok Bot 適合什麼場景？不適合什麼場景？"
    answer: "適合的場景：不需要即時人工監督的重複性工作（定時摘要郵件、整理資料、SEO 標籤管理）、非工程師需要 AI 代做跨 app 工作流、需要多個 agent 平行協作。不適合的場景：任何會對外發送的任務（寄信、發佈貼文、執行付款）——eesel AI 的評測結論是「適合先出草稿的工作，不適合任何會對外發送的任務」。也不適合需要完整合規證據鏈的企業環境——ISO/IEC 27001 認證透過 Cursor 母公司 Anysphere 持有（Grok Bot 在範圍內），但 SOC 2、GDPR、HIPAA 未見於公開文件，Action Recording 預設關閉。  ---"
---

打開 Claude Code，你看到的是一個終端機和一條等待指令的游標。

打開 Grok Bot，它先問你：這個 Bot 叫什麼名字？它的職位是什麼？

這不是 UI 差異。這是兩種完全不同的 agent 架構在爭奪未來的工作形態。

---

## 兩種 agent，兩種世界觀

Claude Code、Codex 這類工具是 session-based agent：你開一個 session，下指令，它執行完回報，session 結束。下次再開，它不記得你是誰。它是一把工具——用完放回去。

Grok Bot 走的路不一樣。2026 年 8 月 11 日 beta 上線，xAI 的行銷語是「always-on AI teammates with their own cloud computer」。每個 Bot 有名字、有職位、有自己的雲端電腦（一台 Linux VM）、有瀏覽器、有檔案系統、有記憶。你可以讓它登進你的 Gmail、你的 Slack、你的 Stripe，然後關掉筆電。它還在跑。

一位用過兩邊的開發者 [Vox](https://x.com/Voxyz_ai/status/2087646987071938618)（360 likes, 146K views）把差異講得最清楚：

> "When I open Codex or Claude Code, I mostly see a task or session. Grok Bot starts by asking me to name the Bot and give it a job. Its computer, files, browser sessions, memory, and routines all sit under that name."

開 Codex 看到的是任務。開 Grok Bot 看到的是一個有身分的員工。

這不是文案的差別。它底下對應的是不同的產品決策：session-based agent 的 blast radius 是一個 session 的生命週期；persistent-identity agent 的 blast radius 是那台電腦上所有 credential 的生命週期。

---

## 好處：被低估的三件事

### 一、非工程師可用

Claude Code 需要你懂終端機。Grok Bot 不需要。

一位自稱非工程師的用戶 [ILKHOM](https://x.com/sandiegocausa/status/2096284068841480335) 說：

> "Grok Bot feels like it was made for the broader public who don't know how to code — but with Claude Code capabilities. No terminal. No restarting mid-task. You just chat and it gets the work done."

沒有 terminal、不用重來、聊天就行。這聽起來像降級，但對非工程師來說是准入門檻的根本改變。

### 二、平行委派

Claude Code 一次跑一個 session。你可以開多個，但每個是獨立的、互不知道。

Grok Bot 可以同時開多個有名字的 Bot，它們共享同一台電腦，可以互相發訊息、在 group chat 裡協調。有人設了一個 Chief of Staff Bot 負責分配任務給其他 Bot——[rewind](https://x.com/rewind02/status/2090869457191325986)（234 likes, 29K views）整理了一份最佳實踐：

> "route through one chief-of-staff agent, not fifteen separate chats"
> "make agents verify each other — invoice flagged → finance agent checks the bank statement before anything moves"

透過一個總管 Bot 路由，讓 Bot 之間互相驗證。這跟 Claude Code 的單 session 模式是不同量級的工作流。

### 三、關筆電還在跑

session-based agent 的生命週期綁在你的 session 上。你關掉 tab，它就停了。

Grok Bot 的 Bot 跑在雲端 VM 上，24/7 在線。有人[半夜讓 Bot 整理網站 SEO](https://x.com/tspy/status/2093481517171564589)，伺服器重啟後 Bot 自己等著繼續。有人[每天中午讓 Bot 摘要重要郵件](https://x.com/starzq/status/2096168440717615605)。這些不是「跑完一個任務」的場景，是「持續在背景運作」的場景。

一位從 Lenny's Podcast 訪談整理的中文用戶 [evans](https://x.com/EStar28518/status/2097360049651990735) 的觀察：

> 「Codex、Claude Code 這類 Agent 已經能完成很複雜的工作，但產品仍更多圍繞『任務』組織…… Grok Bot 往前走了一步：先有一個持續存在的主體，再把任務不斷交給它。」

---

## 代價：被低估的三件事

### 一、五個員工共用一組密碼

所有 Bot 共用一台雲端電腦——瀏覽器 cookie、登入 session、檔案系統、CLI 憑證全部共享。官方文件自己寫著：**do not use separate Bots as a security boundary。**

一位用戶 [MAXdeg0](https://x.com/MAXdeg0/status/2090852404157637036)（377 likes, 62K views）實測後的結論：

> "Five bots, sold as five separate hires… All five live on one machine → one browser session → one login shared across every single one. He tested it himself: one account, eleven apps signed in, one shared profile. Deleted a bot. Its access stayed alive anyway."

五個 Bot 被行銷成五個獨立員工。實際上是一台電腦、一個瀏覽器 profile、一組登入。刪掉一個 Bot，它留下的瀏覽器登入和檔案還在那台電腦上，其他 Bot 仍然可以存取。

[Zack Korman](https://x.com/ZackKorman/status/2090547265630810330)（89 likes）：

> "Been trying to understand how Grok Bot fits into an enterprise security context, and I finally figured it out: It doesn't."

這不是 beta 毛邊。這是設計選擇。Persistent identity 需要 persistent state，persistent state 需要一台一直在線的電腦，一台電腦上的所有東西天然共享。好處（Bot 之間可以協作、共享上下文）和代價（一個 Bot 被注入，所有 credential 都在 blast radius 裡）來自同一個根。

### 二、token 五分鐘燒完

Grok Bot 的 Bot 是 always-on 的，意思是它們隨時在消耗 token——不只是你下指令的時候，還包括它們彼此協調、回報進度、等待你回應的時候。

一位 $300 方案用戶 [Chad Christian](https://x.com/chadchristian/status/2095912429498605618) 說，token 燒速是 ChatGPT 或 Claude 同級方案的四到五倍。

另一位用戶[回報](https://x.com/gcfascist/status/2096679893324923153) $50 的 on-demand 額度在五到十分鐘內燒完，然後說：

> "I can hire a human intern for $50/hr and it would be 6x more cost efficient."

有人跑六個 Bot，每小時燒掉 520 萬 token。凌晨兩點 token 池只剩 200 萬，他的 dispatcher Bot [按「每百萬 token 營收」排優先級](https://x.com/buzzhive_ai/status/2097425187138388218)，三個 Bot 被斷糧。

[Elite Automation](https://x.com/MalachiGreb/status/2097409244785995967) 的觀察更具體：

> "I can't tell if tokens are just being eaten up to ask me to login 100 times in 5min or actual work is being paid for. It feels like there is a lot of inefficiency in all the bots saying 'on it' and explaining what they are doing vs getting tangible stuff done."

分不清 token 是花在工作上還是花在 Bot 跟你報告「收到」上。always-on 的代價是 always-burning。

也有反面聲音。一位用戶[說](https://x.com/denverbitcoin/status/2095707689515188695)「Elon keeps resetting usage every 4 days」，覺得目前等於免費運算。9 月 5 日官方確實全面重置 token pool，稱 routing 和 caching 優化讓 token 效率提升約 10%。但 weekly cap 沒有公開數字，定價的穩定性是個問號。

### 三、Enterprise 版補了牆，但留了門

9 月 3 日開放 Enterprise 版，加了存取控制、網路控制、稽核控制，附兩週免費試用。

但幾個細節值得看：

**Audit Log 記的不是你以為的東西。** Audit Log 記的是管理和認證事件（誰登入、誰改了設定）。Bot 實際做了什麼——打開了哪個網頁、寄了哪封信、改了哪個檔案——在另一個叫 Action Recording 的功能裡，Enterprise 限定、預設關閉，要自己接 OpenTelemetry 才看得到。

**沒有 dry run。** 你的「測試」就是真的在做事。沒有沙盒、沒有模擬模式。

**合規認證透過 Cursor 母公司。** Grok Bot 的 [security 頁面](https://docs.x.ai/grok-bot/security)寫著：Anysphere（Cursor 母公司）持有 ISO/IEC 27001 和 ISO/IEC 42001 認證，稽核機構是 Schellman，Grok Bot 在認證範圍內。但認證持有者是 Anysphere 不是 xAI，而且 SOC 2、GDPR、HIPAA 沒有出現在公開文件裡。對需要完整合規證據鏈的企業來說，「透過被收購公司繼承認證」和「自己通過稽核」是不同的東西。

eesel AI 的結論是：**適合先出草稿的工作，不適合任何會對外發送的任務。**

一位安全研究者 [Zireo](https://x.com/Markestolle/status/2096659403449717186) 做了更尖銳的觀察：6 月 3 日回報的注入漏洞到 9 月上旬仍未修復，同期卻有工程資源上線 Enterprise 版。他的判斷：

> "The fix that ships is the one with a buyer attached."

能賣給採購部門的功能優先於沒有買家的安全修補。

---

## 訂閱方案本身就是一個產品問題

入門 $20/月（Cursor Pro），最高 $300/月（SuperGrok Heavy）。個人門檻兩週內從 $200 降到 $20——降價速度本身就說明初始定價不是市場均衡。

但真正的問題不是價格，是方案之間的關係。一位用戶 [ApoStructura](https://x.com/ApoStructura/status/2097260413310095427)（800 likes, 41K views）的困惑代表了很多人：

> "I pay for X premium+ which also gives me SuperGrok which gives me grok bot, and I also have a cursor account linked to my grok account with a pro+ subscription which also gives me grok bot…"

兩份訂閱給同一個東西。plugins 清單已含 Outlook、Calendar、OneDrive、Stripe Link——Stripe Link 意思是 agent 可以線上付款。一個定價混亂的產品加上一個能花錢的 agent，這個組合值得想一下。

---

## 跟本 blog 既有觀點的碰撞

這篇 blog 從五月開始寫了一系列 harness engineering 的文章。核心主張是：**Prompt 是建議，機制才是規則。** 你叫 agent「不要亂寄信」沒用，因為那是一段它可以選擇不照做的建議。能用 hook、權限、型別擋的事，就不要寫在文件裡求它自願遵守（[你叫 Agent「不要亂寄信」根本沒用](/agent-harness-three-migrations-mechanism/)）。

Grok Bot 的 Approvals 系統——用自然語言寫規則（「不要花超過 $100」「發信前先問我」）——正好落在這條線上。它是 prompt 等級的規則，不是機制等級的。eesel AI 的評語準確：Approvals 是「散文規則，不是硬政策」。

[Harness Engineering 六層防禦](/ai-delete-database-harness-engineering/)裡，Grok Bot 目前大概做到第一層（Approval = 人工批准）。Dry run（第三層）沒有。Blast radius 隔離（第四層）沒有——所有 Bot 共享一台電腦。完整 audit trail（第五層）Enterprise 限定、預設關閉。

這不是在說 Grok Bot 不好。這是在說：**persistent-identity agent 因為 blast radius 更大，對 harness 的要求比 session-based agent 更高，而目前 Grok Bot 的 harness 還沒有追上它自己的產品形態。**

---

## 坦白說

這篇文章的安全和成本數據，除了 xAI 官方文件和 eesel AI 評測之外，大量依賴 X 上的用戶回報。$300 方案燒速四到五倍、$50 五分鐘燒完、六個 Bot 每小時 520 萬 token——這些都是個人使用經驗，不是控制實驗。不同工作流、不同 Bot 數量、不同時段的 token 消耗差異可能很大。

Enterprise 版才上線一週（9 月 3 日開放），Action Recording、OpenTelemetry 整合這些功能的實際體驗還沒有足夠的獨立評測。

注入漏洞的說法來自一位安全研究者在 X 上的公開貼文，沒有看到 xAI 的官方回應或第三方復現。

Grok Bot 是 beta。beta 的意思是它會變。今天的缺口不代表明天的缺口。但反過來說，beta 階段暴露出來的架構選擇——共享 VM、自然語言 Approvals、always-on token 消耗——這些是設計選擇，不是 bug，不太可能在後續版本中翻轉。

---

## 關鍵洞察

**session-based 和 persistent-identity 是兩種不同的產品賭注，不是同一條路上的先後。** Claude Code/Codex 賭的是「把一次性任務做到極致」；Grok Bot 賭的是「讓 AI 變成常駐員工」。你選哪一邊，取決於你要委派的是任務還是角色。

**如果你在評估 Grok Bot 做 pilot，先問三件事。** (a) 你的 Bot 會登入哪些系統？它們共享 credential 你能接受嗎？(b) Bot 做了什麼事你怎麼看到？Action Recording 預設關閉、要自己接 OpenTelemetry。(c) 如果一個 Bot 被注入，blast radius 是什麼？答案是那台共享電腦上所有登入的所有系統。

**agent 產品的勝負不在模型，在 harness。** Grok Bot 和 Claude Code 底下的模型會持續升級、持續追趕。但權限怎麼管、花費怎麼控、出事怎麼查——這些 harness 層的設計選擇才是決定一個 agent 產品能不能從 demo 走到 production 的分界線。

---

## 常見問題 Q&A

**Q: Grok Bot 跟 Claude Code / Codex 到底差在哪？**

核心差異不在模型能力，在 agent 的生命週期。Claude Code 和 Codex 是 session-based agent——你開一個 session 下指令，執行完就結束，下次不記得你。Grok Bot 是 persistent-identity agent——每個 Bot 有名字、有記憶、有自己的雲端 Linux VM，可以 24/7 在線、跨 session 保留狀態。實際體驗上，Claude Code 在寫碼任務上仍被多數用戶認為較強；Grok Bot 的強項是非工程師也能用、可以平行開多個 Bot 協作、關掉筆電 Bot 還在跑。一位用戶的說法是：寫 code 用 Claude Code，管桌面和系統用 Grok Bot。

**Q: Grok Bot 的安全問題具體是什麼？**

最核心的架構特性是：同一個用戶的所有 Bot 共享一台雲端電腦（Cloud Computer），包括瀏覽器 cookie、登入 session、檔案系統、CLI 憑證。官方文件明確寫著「do not use separate Bots as a security boundary」。實測顯示刪掉一個 Bot，它建立的登入和檔案不會被清除，其他 Bot 仍可存取。對企業而言，這代表一個 Bot 被 prompt injection 攻擊時，blast radius 不是那一個 Bot 的任務，而是那台電腦上所有已登入系統的所有存取權限。2026 年 9 月 3 日上線的 Enterprise 版加了用戶之間的隔離，但同一用戶內的 Bot 共享架構不變。

**Q: Grok Bot 的 token 消耗到底有多高？**

沒有官方公開數字，以下是用戶回報：一位 $300/月（SuperGrok Heavy）方案用戶說 token 燒速是 ChatGPT 或 Claude 同級方案的四到五倍。另一位用戶回報 $50 on-demand 額度五到十分鐘燒完。always-on agent 跟 session-based agent 的根本差異是：Bot 即使沒在執行你的指令，也在消耗 token——彼此協調、回報進度、等待回應都算。每個方案有每週 token 額度，超過照量計費，但 weekly cap 數字未公開。2026 年 9 月 5 日 xAI 全面重置 token pool，稱 routing 和 caching 優化提升效率約 10%。

**Q: Grok Bot 適合什麼場景？不適合什麼場景？**

適合的場景：不需要即時人工監督的重複性工作（定時摘要郵件、整理資料、SEO 標籤管理）、非工程師需要 AI 代做跨 app 工作流、需要多個 agent 平行協作。不適合的場景：任何會對外發送的任務（寄信、發佈貼文、執行付款）——eesel AI 的評測結論是「適合先出草稿的工作，不適合任何會對外發送的任務」。也不適合需要完整合規證據鏈的企業環境——ISO/IEC 27001 認證透過 Cursor 母公司 Anysphere 持有（Grok Bot 在範圍內），但 SOC 2、GDPR、HIPAA 未見於公開文件，Action Recording 預設關閉。

---

## 來源

- [xAI Launches Grok Bot, Always-On AI Teammates With Their Own Cloud Computers（Unite.AI）](https://www.unite.ai/xai-launches-grok-bot-always-on-ai-teammates-with-their-own-cloud-computers/)
- [Grok Bot review: what actually ships in the early beta（eesel AI）](https://www.eesel.ai/blog/grok-bot-review)
- [Grok Bot pricing 2026: real plan costs and the uncapped meter（eesel AI）](https://www.eesel.ai/blog/grok-bot-pricing)
- [Grok Bot for teams and enterprises（xAI Docs）](https://docs.x.ai/grok-bot/teams-and-enterprises)
- [Grok Bot approvals, security and privacy（xAI Docs）](https://docs.x.ai/grok-bot/approvals-security-and-privacy)
- [Grok Bot FAQ（xAI Docs）](https://docs.x.ai/grok-bot/faq)
- [Grok Bot Pricing Explained（CellCog）](https://cellcog.ai/blog/grok-bot-pricing/)
- [Grok Bot Security, Explained: What the Shared-Computer Model Means（CellCog）](https://cellcog.ai/blog/grok-bot-security/)
- 本站相關：[你叫 Agent「不要亂寄信」根本沒用：從 Prompt 到 Harness 的三次中心遷移](/agent-harness-three-migrations-mechanism/)
- 本站相關：[當 AI 把資料庫刪光：兩個真實案例與 Harness Engineering 的反擊](/ai-delete-database-harness-engineering/)
