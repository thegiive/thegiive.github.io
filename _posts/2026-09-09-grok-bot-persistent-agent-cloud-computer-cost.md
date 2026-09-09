---
layout: post
title: "Grok Bot：xAI 用 30 美金賣你一台 150 美金的 VM，還附 AI 員工"
date: 2026-09-09 09:00:00 +0800
permalink: /grok-bot-persistent-agent-cloud-computer-cost/
tags: [Grok Bot, xAI, agent, persistent agent, OpenClaw, harness engineering, agent security, token cost]
categories: [AI Agent]
image: /assets/images/grok-bot-persistent-agent-cover.png
description: "30 美金，一台 8-core / 16GB RAM 的 Debian Linux VM，24 小時不關機，還附一個會自己登 Gmail、Slack 幫你做事的 AI。這是 xAI 的 Grok Bot——講白了就是 OpenClaw 這類東西的雲端版。性價比拉滿、介面比 Manus 好、非工程師也能用。但企業別想了：Bot 共享登入資料、沒有 dry run、文件資源極少。xAI 骨子裡是 2C DNA，做得出讓人驚艷的 demo，做不出讓採購部門簽字的產品。"
author: Wisely Chen
faq:
  - question: "Grok Bot 跟 OpenClaw 差在哪？"
    answer: "核心差異是雲端 vs 地端。Grok Bot 是 xAI 託管的雲端 VM（Cloud Computer），你不用管機器、不用裝環境，30 美金/月全包。OpenClaw 跑在你自己的機器上，硬體自備，但資料完全在地端、credential 不離開你的網路。對個人用戶來說 Grok Bot 省事；對企業來說 OpenClaw 的地端架構在資安審查上天生有優勢。另一個具體差異：Grok Bot 搜尋 X 是 call X API（會扣錢），OpenClaw 可以用 Grok Command Line 免費搜。"
  - question: "Grok Bot 的 VM 規格是什麼？在 GCP 租同等規格要多少錢？"
    answer: "社群用戶實測回報（非官方公佈）：8-core Intel Xeon、16 GB RAM、128 GB virtual disk、Debian Linux。在 Google Cloud Platform 租同等規格的 VM（e2-custom-8-16384 + 128 GB standard disk），隨用隨付約 165 美金/月，1 年承諾折扣約 115 美金/月。SuperGrok 方案 30 美金/月就包含這台 VM 加上 Grok 4.6 CLI，性價比差距很大。"
  - question: "Grok Bot 的安全問題具體是什麼？"
    answer: "最核心的架構特性是：同一個用戶的所有 Bot 共享一台雲端電腦（Cloud Computer），包括瀏覽器 cookie、登入 session（Login Session）、檔案系統、CLI 憑證。官方文件明確寫著「do not use separate Bots as a security boundary」。實測顯示刪掉一個 Bot，它建立的登入和檔案不會被清除，其他 Bot 仍可存取。Enterprise 版（2026 年 9 月 3 日上線）加了用戶之間的隔離，但同一用戶內的 Bot 共享架構不變。"
  - question: "個人用戶值得買嗎？"
    answer: "以目前的定價來看，SuperGrok 30 美金/月是 AI agent 產品裡性價比最高的選項之一。你同時拿到 Grok 4.6 CLI（效能跑分逼近 Claude Opus 5，每任務成本只要四成）、Grok Bot 雲端 agent、以及一台在 GCP 要 100～150 美金/月的 VM。如果你本來就在用 X Premium+，SuperGrok 是附帶的，等於免費拿到 Grok Bot。個人使用場景——定時摘要郵件、整理資料、跨 app 自動化——無腦衝。  ---"
---

30 美金。一台 8-core / 16GB RAM 的 Debian Linux VM。24 小時不關機。還附一個會自己登 Gmail、Slack 幫你做事的 AI。

這是 xAI 的 Grok Bot，2026 年 8 月 11 日 beta 上線。

你可以開多個 Bot，每個有不同職位，讓它們登進 Gmail、Slack、Stripe。關掉筆電，它們還在跑。

講白了，就是 OpenClaw 這類東西的雲端版——一台永遠在線的 Linux VM、瀏覽器、檔案系統。

---

## 好處：性價比高

目前最大的好處是性價比。

30 美金的 SuperGrok，你同時拿到：

- **Grok CLI** 做 AI——有效能跑分逼近 Opus 5 的 Grok 4.6（整體智力分數 61 vs Opus 5 的 63，但[每完成一個任務的成本只要 Opus 5 的四成](https://www.orcarouter.ai/blog/grok-4-6-vs-claude-opus-5)）
- **Grok Bot** 產品
- **一台免費的雲端 VM**

Grok Bot 後面那台 Debian Linux——8-core Intel Xeon、16 GB RAM、128 GB virtual disk（[社群用戶實測規格](https://x.com/Voxyz_ai/status/2087279785311613170)，非官方公佈）。這在 GCP 租同等規格（e2-custom-8-16384 + 128 GB standard disk）要 100～150 美金/月。

還有一個更划算的路徑：如果你用的是 X Premium+，因為 X Premium+ 附上 SuperGrok，SuperGrok 附上 Grok Bot——等於你為了用 X 付的錢，順便拿到一台雲端 AI 工作站。一位用戶 [ApoStructura](https://x.com/ApoStructura/status/2097260413310095427)（800 likes）的困惑代表了很多人：兩份訂閱給同一個東西，定價結構本身就是個謎。

### 介面做得好

介面做得很好，特別是人類瀏覽器登入、換手的介面很直覺。用過 Manus 的人就知道，Grok Bot 在這塊比 Manus 再更進階。

### 非工程師可用

Claude Code 需要你懂終端機。Grok Bot 不需要。

一位自稱非工程師的用戶 [ILKHOM](https://x.com/sandiegocausa/status/2096284068841480335) 說：

> "Grok Bot feels like it was made for the broader public who don't know how to code — but with Claude Code capabilities. No terminal. No restarting mid-task."

聊天就能委派跨 app 工作流。有人設了一個 Chief of Staff Bot 負責分配工作給其他 Bot——[rewind](https://x.com/rewind02/status/2090869457191325986)（234 likes）整理的最佳實踐：透過一個總管 Bot 路由，讓 Bot 之間互相驗證。

### 關筆電還在跑

Bot 跑在雲端 VM 上，24/7 在線。有人半夜讓 Bot 整理網站 SEO，伺服器重啟後 Bot 自己等著繼續。有人每天中午讓 Bot 摘要重要郵件。這不是「跑完一個任務」的場景，是「持續在背景運作」的場景。

---

## 我自己測了一輪

實際使用上，我可以開一堆 Bot 都沒有人管（我是 SuperGrok，不是 Plus 或 Heavy），所以也不太確定能開幾個。

Computer Use 做得不錯。可以登入多個 Gmail 帳號，自己挑選要用哪個。我請它去我的 LinkedIn 搜尋貼文、分析追蹤我的群眾，都跑得很順。

但有一個成本陷阱要注意：搜尋 X 的時候，Grok Bot 是直接 call X API 的，所以會扣錢。如果用 OpenClaw 跑在自己機器上，你可以直接用 Grok Command Line，因為 Grok CLI 可以免費搜 X。這兩者在錢上面是有差距的——我也一瞬間被扣了一堆 X API fee。

---

## 適合公司使用？

如果說當時 OpenClaw 資安設計不好，被資安打得很慘，那 Grok Bot 更慘——是設計不好加上完全黑箱。

### Bot 共享登入資料

所有 Bot 共用一台電腦、一個瀏覽器 profile、一組登入。官方文件自己寫著：**do not use separate Bots as a security boundary。**

一位用戶 [MAXdeg0](https://x.com/MAXdeg0/status/2090852404157637036)（377 likes）實測：五個 Bot 被行銷成五個獨立員工，實際上共用一台機器、一個瀏覽器 session、一組登入。刪掉一個 Bot，它的瀏覽器登入還在，其他 Bot 仍然可以存取。

光是這個就很可怕。

[Zack Korman](https://x.com/ZackKorman/status/2090547265630810330)（89 likes）：

> "Been trying to understand how Grok Bot fits into an enterprise security context, and I finally figured it out: It doesn't."

### 文件資源極少，無法知道做法

Enterprise 版 9 月 3 日上了，但 Bot 實際做了什麼在 Action Recording 裡——Enterprise 限定、預設關閉、要自己接 OpenTelemetry。沒有 dry run，測試就是真的在做事。

合規認證透過 Cursor 母公司 Anysphere 持有 ISO/IEC 27001 和 ISO/IEC 42001（[security 頁面](https://docs.x.ai/grok-bot/security)），Grok Bot 在認證範圍內。但 SOC 2、GDPR、HIPAA 未見於公開文件。

一位安全研究者 [Zireo](https://x.com/Markestolle/status/2096659403449717186) 做了更尖銳的觀察：6 月 3 日回報的注入漏洞到 9 月上旬仍未修復，同期卻有工程資源上線 Enterprise 版。他的判斷：

> "The fix that ships is the one with a buyer attached."

能賣給採購部門的功能優先於沒有買家的安全修補。

### token 消耗也很猛

一位 $300 方案用戶 [Chad Christian](https://x.com/chadchristian/status/2095912429498605618) 說，token 燒速是 ChatGPT 或 Claude 同級方案的四到五倍。另一位用戶[回報](https://x.com/gcfascist/status/2096679893324923153) $50 on-demand 五到十分鐘燒完。

有人跑六個 Bot，每小時燒掉 520 萬 token。凌晨兩點 token 池只剩 200 萬，他的 dispatcher Bot [按「每百萬 token 營收」排優先級](https://x.com/buzzhive_ai/status/2097425187138388218)，三個 Bot 被斷糧。

always-on 的意思就是 always-burning。

---

## 跟 Harness Engineering 的關係

這篇 blog 從五月開始寫 harness engineering 系列。核心主張：**Prompt 是建議，機制才是規則。**（[你叫 Agent「不要亂寄信」根本沒用](/agent-harness-three-migrations-mechanism/)）

Grok Bot 的 Approvals 用自然語言寫規則——「不要花超過 $100」「發信前先問我」——這是 prompt 等級的建議，不是機制等級的攔截。

[Harness Engineering 六層防禦](/ai-delete-database-harness-engineering/)裡，Grok Bot 目前大概做到第一層（Approval = 人工批准）。Dry run（第三層）沒有。Blast radius 隔離（第四層）沒有——所有 Bot 共享一台電腦。完整 audit trail（第五層）Enterprise 限定、預設關閉。

persistent-identity agent 因為 blast radius 更大，對 harness 的要求比 session-based agent 更高，而目前 Grok Bot 的 harness 還沒追上自己的產品形態。

---

## 我的建議

**個人使用，無腦衝。**

30 美金買下 Grok 4.6 CLI（幾乎用不完）、Grok Bot 產品、一台雲端 100 美金起跳的 VM。性價比拉滿。沒用拿來當 LINE Bot 都爽，省下 mac mini 的錢。

**企業使用，忘了他吧。**

xAI 骨子裡是 2C DNA。做得出讓人驚艷的 demo，做不出讓採購部門簽字的產品。

---

## 坦白說

這篇文章的安全和成本數據，除了 xAI 官方文件和 eesel AI 評測之外，大量依賴 X 上的用戶回報。$300 方案燒速四到五倍、$50 五分鐘燒完——這些都是個人使用經驗，不是控制實驗。

VM 規格（8-core Intel Xeon、16 GB RAM、128 GB disk）是社群用戶讓 Bot 跑系統指令回報的結果，xAI 沒有官方公佈硬體規格，也沒有保證這些規格不會變。

Grok Bot 是 beta。beta 的意思是它會變。但共享 VM、自然語言 Approvals、always-on token 消耗——這些是設計選擇，不是 bug，不太可能在後續版本中翻轉。

我自己的測試是在 SuperGrok 方案下進行的，不是 Plus 或 Heavy，體驗可能因方案而異。

---

## 關鍵洞察

**個人用戶看性價比，企業用戶看 harness。** 同一個產品，對這兩群人的結論完全相反。30 美金買到的東西確實超值；但權限怎麼管、花費怎麼控、出事怎麼查——這些 harness 層的東西，xAI 還沒開始認真做。

**Grok Bot 的進入，讓雲端 AI Agent 圈的戰場越來越好玩了。** 不過一個 Open Source Agent，再加一個全地端的 AI，才很有可能是企業級主戰場。

---

## 常見問題 Q&A

**Q: Grok Bot 跟 OpenClaw 差在哪？**

核心差異是雲端 vs 地端。Grok Bot 是 xAI 託管的雲端 VM（Cloud Computer），你不用管機器、不用裝環境，30 美金/月全包。OpenClaw 跑在你自己的機器上，硬體自備，但資料完全在地端、credential 不離開你的網路。對個人用戶來說 Grok Bot 省事；對企業來說 OpenClaw 的地端架構在資安審查上天生有優勢。另一個具體差異：Grok Bot 搜尋 X 是 call X API（會扣錢），OpenClaw 可以用 Grok Command Line 免費搜。

**Q: Grok Bot 的 VM 規格是什麼？在 GCP 租同等規格要多少錢？**

社群用戶實測回報（非官方公佈）：8-core Intel Xeon、16 GB RAM、128 GB virtual disk、Debian Linux。在 Google Cloud Platform 租同等規格的 VM（e2-custom-8-16384 + 128 GB standard disk），隨用隨付約 165 美金/月，1 年承諾折扣約 115 美金/月。SuperGrok 方案 30 美金/月就包含這台 VM 加上 Grok 4.6 CLI，性價比差距很大。

**Q: Grok Bot 的安全問題具體是什麼？**

最核心的架構特性是：同一個用戶的所有 Bot 共享一台雲端電腦（Cloud Computer），包括瀏覽器 cookie、登入 session（Login Session）、檔案系統、CLI 憑證。官方文件明確寫著「do not use separate Bots as a security boundary」。實測顯示刪掉一個 Bot，它建立的登入和檔案不會被清除，其他 Bot 仍可存取。Enterprise 版（2026 年 9 月 3 日上線）加了用戶之間的隔離，但同一用戶內的 Bot 共享架構不變。

**Q: 個人用戶值得買嗎？**

以目前的定價來看，SuperGrok 30 美金/月是 AI agent 產品裡性價比最高的選項之一。你同時拿到 Grok 4.6 CLI（效能跑分逼近 Claude Opus 5，每任務成本只要四成）、Grok Bot 雲端 agent、以及一台在 GCP 要 100～150 美金/月的 VM。如果你本來就在用 X Premium+，SuperGrok 是附帶的，等於免費拿到 Grok Bot。個人使用場景——定時摘要郵件、整理資料、跨 app 自動化——無腦衝。

---

## 來源

- [xAI Launches Grok Bot, Always-On AI Teammates With Their Own Cloud Computers（Unite.AI）](https://www.unite.ai/xai-launches-grok-bot-always-on-ai-teammates-with-their-own-cloud-computers/)
- [Grok Bot review: what actually ships in the early beta（eesel AI）](https://www.eesel.ai/blog/grok-bot-review)
- [Grok Bot pricing 2026: real plan costs and the uncapped meter（eesel AI）](https://www.eesel.ai/blog/grok-bot-pricing)
- [Grok Bot approvals, security and privacy（xAI Docs）](https://docs.x.ai/grok-bot/approvals-security-and-privacy)
- [Grok Bot Security（xAI Docs）](https://docs.x.ai/grok-bot/security)
- [Grok 4.6 vs Claude Opus 5: Same 61, Two Different Economies（OrcaRouter）](https://www.orcarouter.ai/blog/grok-4-6-vs-claude-opus-5)
- [Vox — Grok Bot VM specs（X）](https://x.com/Voxyz_ai/status/2087279785311613170)
- 本站相關：[你叫 Agent「不要亂寄信」根本沒用：從 Prompt 到 Harness 的三次中心遷移](/agent-harness-three-migrations-mechanism/)
- 本站相關：[當 AI 把資料庫刪光：兩個真實案例與 Harness Engineering 的反擊](/ai-delete-database-harness-engineering/)
