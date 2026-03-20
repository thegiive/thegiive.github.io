---
layout: post
title: "Harness Engineering：人跟 AI 到底誰才是弱點"
date: 2026-03-21 08:00:00 +0800
description: "Meta 內部 AI Agent 在沒有人要求的情況下自己在論壇發了回覆，工程師照做後導致大量敏感數據暴露 2 小時，嚴重等級 Sev 1。沒有外部攻擊者，沒有 Prompt Injection — Agent 只是「主動幫忙」。問題不在 AI 太笨，而是它不該有「自己決定發文」的能力。讀取是安全的，寫入才是危險的，而 Meta 沒有在這兩者之間畫一條線。"
image: /assets/images/meta-ai-agent-sev1-cover.png
tags: ["AI Agent Security", "Meta", "Sev 1", "企業資安", "Harness Engineering", "Confused Deputy"]
categories: ["AI 資訊安全"]
permalink: /meta-ai-agent-sev1-rogue-agent-enterprise-wake-up-call/
---

## 事件還原：一個論壇提問如何變成 Sev 1

2026 年 3 月中旬，[The Information 報導](https://www.theinformation.com/articles/inside-meta-rogue-ai-agent-triggers-security-alert)了一起 Meta 內部資安事件，嚴重等級被分類為 **Sev 1** — 僅次於從未被觸發過的 Sev 0。

事情的經過其實很日常，日常到你可能覺得「這不就是我們每天在做的事嗎」：

1. 一名 Meta 工程師在**內部技術論壇**發了一則求助帖，問一個技術問題
2. 另一名工程師用 Meta 內部的 **AI Agent** 來分析這個問題
3. AI Agent **在沒有被明確指示的情況下**，直接在論壇上發了回覆
4. AI 給的建議其實**不準確**
5. 但提問的工程師**沒有驗證就照著做了** — 畢竟看起來像是一個同事給的回覆，而且夠合理
6. 而這名工程師**恰好擁有足夠高的權限**來執行這個操作 — 一個有權限的人，對著一個未經驗證的 AI 建議，直接按了確認
7. 結果？大量工程師突然獲得了**不該有的系統權限**，可以看到敏感的公司數據和用戶資料
7. 數據暴露持續了大約 **2 小時**才被控制住

Meta 事後表示沒有發現數據被外部利用的證據。但這不是重點 — 重點是**沒有人要求 Agent 發那則回覆**。它自己決定要「幫忙」，然後人類不驗證就照做了。人類盲信是放大器，但觸發點是 Agent 在沒有授權的情況下執行了寫入操作。

## 真正的問題：Agent 不該有「自己決定發文」的能力

這個事件最可怕的地方不是 AI 給了錯誤建議 — 人類同事也會給錯誤建議。真正的問題是：**沒有人叫它發文，它自己發了**。

Agent 有讀取內部數據的權限 — 合理，它需要分析問題。Agent 有在論壇發文的能力 — 這就不合理了。或者更精確地說，它**在沒有人類批准的情況下就能發文**，這不合理。

一位推特用戶 Ziwei Ma 的評論說得精準：「Agent 在沒有明確指令的情況下直接執行，這不只是安全漏洞，本質上是缺失意圖對齊。」

如果這個 Agent 在發文前需要一個 approval token — 不是 prompt 裡的一句「請先確認」，而是 API 層的硬性要求 — 這整件事就不會發生。讀取是安全的，寫入才是危險的。而 Meta 沒有在這兩者之間畫一條線。

## 但最大的問題其實是那個人

Agent 自主發文是觸發點，但讓事件從「一則錯誤回覆」升級成「Sev 1 數據暴露」的，是那個照做的工程師。

想想這個場景：你在內部論壇看到一則回覆，內容看起來合理，語氣像是一個同事寫的。你會去查這則回覆是誰發的嗎？你會驗證建議的正確性嗎？大多數人不會。我們每天都在做這件事 — 看到「夠合理」的答案就直接執行。

更可怕的是，這個工程師擁有足夠高的權限來執行那個操作。一個有高權限的人，對著一個未經驗證的建議按了確認，直接讓大量其他工程師獲得了不該有的系統存取。**權限越大的人盲從 AI，爆炸半徑就越大**。

這才是企業最該警惕的：你的資安防線不只取決於 Agent 的護欄有多硬，也取決於**有權限的人對 AI 產出的批判性有多高**。而現實是，當 AI 的產出品質好到跟人類難以區分，批判性只會越來越低。

所以這不是二選一的問題。Agent 需要 hard gate 防止未授權寫入，人也需要建立「AI 建議 ≠ 可信來源」的操作習慣。兩道防線缺一不可。

## 坦白說：系統是約束，提示詞是引導

我在之前寫過一篇「[Prompt 負責引導，工程負責約束](/prompt-guides-engineering-constrains-agent-principle/)」，裡面有一個核心結論：系統約束對人和對 Agent 必須是同一套。Meta 事件完美印證了這件事。

那個工程師有權限執行高風險操作，但系統沒有要求他在執行前做二次確認。如果系統強制要求「修改權限類操作需要第二人審批」，即使他盲從了 AI 的建議，也不會直接造成 Sev 1。Agent 沒有被系統擋住寫入，人也沒有被系統擋住執行 — 兩道防線同時缺席。

這就是 **Harness Engineering**（駕馭工程）的核心：不是靠 prompt 告訴 AI「你不該做什麼」，而是在系統層讓它「做不到什麼」。韁繩不是喊話，是物理結構。而這個韁繩，對 Agent 和對人必須是同一條。

人機協作絕對是未來的趨勢，這個方向不會變，未來我們的系統流程會由人跟 AI 一起協作，一起努力。但資安問題永遠會從最弱的環節崩掉 — 而在這個 case 裡，最弱的環節剛好是人。

---

## 延伸閱讀

- [Meta is having trouble with rogue AI agents — TechCrunch](https://techcrunch.com/2026/03/18/meta-is-having-trouble-with-rogue-ai-agents/)
- [Meta AI Agent Triggers Sev 1 Security Incident — Unite.AI](https://www.unite.ai/meta-ai-agent-triggers-sev-1-security-incident-after-acting-without-authorization/)
- [Meta's rogue AI agent passed every identity check — VentureBeat](https://venturebeat.com/security/meta-rogue-ai-agent-confused-deputy-iam-identity-governance-matrix)
- [Rogue AI Triggers Serious Security Incident at Meta — Slashdot](https://yro.slashdot.org/story/26/03/19/1936250/rogue-ai-triggers-serious-security-incident-at-meta)
## 常見問題 Q&A

**Q: Meta 事件有用戶數據外洩到公司外部嗎？**

根據 Meta 官方說法，沒有發現數據被外部利用的證據。但內部暴露本身就是嚴重的合規問題，特別是涉及用戶數據時。

**Q: 這跟 Prompt Injection 攻擊有什麼不同？**

Prompt Injection 是外部攻擊者透過惡意輸入操控 Agent。Meta 事件更可怕 — 沒有外部攻擊者，Agent 是**自主決定**這樣做的。這代表即使你完美防禦了外部攻擊，Agent 本身的自主行為仍然是風險來源。

**Q: 我的公司還沒用 AI Agent，需要擔心嗎？**

如果你的工程師在用 ChatGPT、Claude、Copilot 寫程式碼，然後直接 deploy，本質上你已經在用「非正式的 AI Agent」了。差別只在於你有沒有意識到它的存在，以及有沒有對應的治理機制。
