---
layout: post
title: "2026 年大廠怎麼面試：三種考法、五類要準備的問題，和那題「為什麼要請你，不是請 AI」"
date: 2026-10-02 09:00:00 +0800
permalink: /ai-era-interview-2026-three-camps/
tags: [技術面試, AI面試, Meta, Google, Amazon, Anthropic, Canva, take-home, LeetCode, AI-enabled interview, 招募, 人機分工]
categories: [AI 產業分析]
image: /assets/images/ai-era-interview-2026-three-camps-cover.png
description: "Anthropic 有一份 take-home 從 2024 年初用到現在，同樣時限下 Claude Opus 4 贏過多數應徵者，Opus 4.5 連最強的那批都追平。大廠的回應分成三派：Meta、Canva 讓你帶 AI 進場；Google、Amazon 把人叫回現場、禁止 AI；Anthropic 把題目改成 AI 沒看過的解謎。這篇用三段講完：現在怎麼面試、要準備哪些問題，以及到最後每個人都得回應的那一題：「為什麼要請你，不是請 AI」。"
author: Wisely Chen
faq:
  - question: "2026 年大廠的技術面試還考 LeetCode 嗎？"
    answer: "還考，但不再是唯一的考法。Google 至少保留一輪面對面面試，Pichai 說是為了確認基本功；Amazon 的內部指引規定，未經允許在面試中使用生成式 AI 可能被取消資格。另一邊，Meta 和 Canva 已經有讓候選人使用 AI 助手的面試輪次，題目改成在陌生程式碼庫（codebase）裡做真實開發。準備時演算法不能放掉，但要先問 recruiter 你遇到的是哪一種。"
  - question: "AI 輔助面試（AI-enabled coding interview）到底在打什麼分？"
    answer: "既然 AI 能寫出正確答案，打分重點就從「答案對不對」移到「你怎麼跟 AI 協作」。根據 Canva 官方部落格和 X 上的候選人面經，常見評分項目包括：能不能拆解模糊需求、能不能找出 AI 產生程式碼的錯誤或次佳寫法、是否讀過並能解釋 AI 改的程式碼差異（diff）、以及能不能主導和面試官的溝通。Canva 觀察到，不常用 AI 的候選人卡住，往往不是因為不會寫程式，而是不知道怎麼引導 AI。"
  - question: "大廠面試真的會問「為什麼要請你，不是請 AI」嗎？"
    answer: "目前查不到任何一家公司把這題列入正式面試流程。說 FAANG 會新增「為什麼不用 AI 取代你」一輪的貼文發在 2026 年 4 月 1 日，被許多人認為是愚人節玩笑，文末還在推銷課程。不過這題在 X 上以假設題形式廣泛討論，它值得準備，因為它逼你說清楚自己在人機分工（human-AI division of labor）裡的位置。好的回答是一個具體時刻：你推翻 AI 建議、抓到它的錯、或為一個取捨負責的經驗。"
  - question: "AI 時代，工程師贏過 AI 的地方在哪？"
    answer: "寫得快、寫得對、記得多，這幾項人已經贏不了：Anthropic 的 take-home 在 2 小時時限下，Claude 追平了人類最佳成績。人還有優勢的地方包括：沒人做過的新問題（Anthropic 把考題改成模擬新工作後才重新拉開差距）、問對問題和引導 AI 的判斷力、為上線結果負責，以及從失敗中學到的經驗。這份清單會隨模型進步而縮小，需要持續更新。"
  - question: "Anthropic 面試能不能用 AI？"
    answer: "要分開看。Anthropic 的申請表要求申請過程不要使用 AI 助手，理由是想評估沒有經過 AI 修飾的表達能力，發言人也表示政策可能隨工具進步而更新。但它效能工程團隊的 take-home 作業明確允許使用 AI。這份 take-home 從 2024 年初開始使用、超過 1,000 位候選人做過；同樣時限下 Claude Opus 4 贏過多數應徵者，Opus 4.5 追平最強的候選人，因此 Anthropic 在 2026 年 1 月公開說明改成 AI 沒看過的解謎題型。  ---"
---

Anthropic 有一份 take-home，2024 年初開始用，超過 1,000 位候選人做過。

同樣時限下，Claude Opus 4 贏過多數人類應徵者。Opus 4.5 連最強的那批都追平了。出題的 Tristan Hume 只好把題目重寫，今年一月他寫：

> "I'm still sad to have given up the realism and varied depth of the original. But realism may be a luxury we no longer have. The original worked because it resembled real work. The replacement works because it simulates novel work."
>
> 舊題目有效，是因為它像真實工作。新題目有效，是因為它是沒人做過的工作。

一家做 AI 的公司，承認「像真實工作」在面試裡已經是奢侈品。

這篇分三段：現在大廠怎麼面試、要準備哪些問題，最後是那一題「為什麼要請你，不是請 AI」。

<nav class="post-toc" markdown="1">
**目錄**

* 目錄
{:toc}
</nav>

---

## 一、現在怎麼面試：三派

AI 讓兩種老考法失效：take-home 可以整份交給 agent 做；遠端 coding 面試很難確認是誰在作答。大廠的回應分成三派：

| | 做法 | 代表 | 放棄了什麼 |
|---|---|---|---|
| 第一派 | 讓 AI 進場，改打過程分 | Meta、Canva、Stripe | 只看產出打分 |
| 第二派 | 叫回現場，禁 AI | Google、Amazon | 不必防 AI |
| 第三派 | 出 AI 沒看過的題 | Anthropic take-home | 像真實工作 |

**第一派。** 2025 年 7 月底，404 Media 看到 Meta 的內部訊息：部分 coding 職缺的候選人，面試時可以用 AI 助手。Canva 更早，2025 年 6 月直接在工程部落格宣布技術面試「不只准用 AI，而且要求你用」。題目改成在陌生 codebase 裡加功能、修 bug，打分看你怎麼拆需求、有沒有讀 AI 改的 diff、能不能抓出 AI 的錯。

**第二派。** Pichai 在 2025 年 6 月上 Lex Fridman 的 podcast 說：

> "Look, we are making sure we'll introduce at least one round of in-person interviews for people just to make sure the fundamentals are there."
>
> 我們會確保至少有一輪面對面，確認基本功在。

Amazon 的內部指引則寫明，除非明確允許，面試時用生成式 AI 可能被取消資格。

**第三派。** 就是開頭的 Anthropic。有個細節常被講錯：Anthropic 的申請表確實禁 AI，但那份 take-home 明確准用 AI。到 2 小時那一刻，Claude 的分數追平了人類最佳成績——而那位人類本身就大量用 Claude 4 在輔助。新版題目改成 Zachtronics 風格的解謎：極小的指令集，不給任何除錯工具。

三派排在一起看，是一道三選二：**像真實工作、不必防 AI、只看產出就能打分，最多拿兩個。** 越像真實工作、越多人做過的題目，AI 越容易解；想讓題目像工作又只看產出，就得把 AI 擋在門外。

這也是為什麼同一個動作在不同公司會得到相反結果。九月有位面試官在 X 上說，他告訴候選人什麼工具都可以用，結果對方一分享螢幕就打開 Claude，他直接掛斷，這則有超過 120 萬次瀏覽。另一位在 2025 年說，候選人 90% 的時間都在問 Claude，他們錄取了他，理由是 "He asked Claude the best questions."

**面試前先問 recruiter 三件事：准不准用 AI、現場還是遠端、什麼環境。** 這三個答案決定你屬於哪一派。

---

## 二、要準備哪些問題

這份清單是我從前面提到的面經和 X 貼文整理的。X 上沒有人直接給一份題目清單。

**1. 你怎麼跟 AI 協作**

- 最近一個用 agent 做完的功能，你怎麼拆需求、怎麼下 prompt、在哪裡推翻了 AI 的建議？
- AI 寫的這一行為什麼要存在？換一種寫法，代價是什麼？
- 你怎麼抓出 AI 產生的幻覺或錯誤？

先準備好一份真實的 agent 對話紀錄，面試時拿得出來。

**2. 現場分享螢幕**

Aakash Gupta 轉述一位產品長，面試任何職位都會問一句「可以分享螢幕嗎」。平常開著哪些工具、跑著哪些自動化、做過哪些實際成品，這個沒辦法前一晚臨時準備，要靠平時累積。

**3. 在陌生程式碼庫裡除錯**

- 練習在 30 分鐘內看懂一個沒碰過的 repo，找出 bug 並修好。
- 併發、容錯這類上班真的會碰到的題目。一位候選人在 X 上寫的 CoderPad 面經，最後一段就是把功能往併發、延遲、儲存去優化。

**4. 做完之後被逐行追問**

交出去的每一段程式都要講得出設計上的取捨。X 上有位自稱 60 歲的面試官分享，他讓候選人當場用 AI 寫完再講解給他聽，覺得水準不夠，就當場告知不會有二面。（[連結](https://x.com/shdfn219284/status/2105620902557974993)）

**5. 老派的題目還沒消失**

有些公司仍然考不准用 AI 的 LeetCode，2026 年九月還有人在線上測驗寫 Maximal Rectangle（[連結](https://x.com/r4zeigen/status/2103928661925925126)）。基本的演算法能力不能完全放掉。

---

## 三、「為什麼要請你，不是請 AI？」

其實，到最後我們都得回應一個問題：**人到底贏 AI 在哪裡。**

先承認輸的地方。同樣 2 小時，Claude 追平了人類最佳成績。寫得快、寫得對、記得多，這幾項人已經贏不了。用這幾項回答這題，等於自己認輸。

從這篇整理的證據看，人還贏的地方有四個。

**1. 沒人做過的問題。** Tristan Hume 試過一版資料轉置的題目，又被 Claude 解掉，他的檢討是很多工程師卡過這類問題，Claude 手上有大量訓練資料可以參考。最後能分出人跟 AI 的，是他說的 "simulates novel work"。他也寫到，時間不限的話，人類還是能贏過模型。AI 強在很多人做過的事，人的機會在沒人做過的事。

**2. 問對問題。** 前面那位錄取候選人的理由不是他寫得多好，是 "He asked Claude the best questions." Canva 也觀察到，不常用 AI 的候選人卡住，不是因為不會寫程式：

> "Interestingly, candidates with minimal AI experience often struggled, not because they couldn't code, but because they lacked the judgment to guide AI effectively or identify when its suggestions were suboptimal."
>
> 卡住的原因是不知道怎麼引導 AI，也看不出它的建議哪裡不夠好。

**3. 為結果負責。** 九月那則假設題底下，有一則回覆把這件事講得很具體：

> "The reason this seat exists is that you still need a person who can give Claude the right technical context, write sharper prompts, own the architecture, catch what the model misses, and take responsibility for what actually ships."
>
> 這個位子存在，是因為還需要一個人給 Claude 正確的脈絡、擁有架構、抓出模型漏掉的東西，並為上線的結果負責。

這跟我去年十一月寫的[〈AI 時代的面試：我不考 coding，只問為什麼〉](https://ai-coding.wiselychen.com/ai-era-interview-why-not-coding/)是同一件事。那時我面試 Jr FDE，只追問「為什麼用這個」，因為你要知道為什麼這樣選，才能對方案負責。當時那比較像個人偏好，現在大廠准用 AI 的那一派，評分項目本質上也是「為什麼」換了包裝。

**4. 失敗過。** 那篇我也寫過：AI 不會失敗，永遠有答案，所以遇到無解的問題會亂回答。我想找的是有失敗經驗、能從中吸取教訓的人。你講得出一次自己卡住、走錯、最後怎麼收拾的經驗，這是 AI 給不出來的答案。

所以這題的好答案不是口號，是證據。準備一個具體時刻：你推翻了 AI 的建議、你抓到它的錯、你為一個它沒想到的取捨負了責。講出這個時刻，比講「我有判斷力」有用得多。

最強的反方是：對某些職位，這題的誠實答案可能是「你不該請我」。如果一個職位的工作內容就是把清楚的需求翻成程式碼，那 AI 確實做得更快。我的回應是，這正好是這題的價值——它不只在考候選人，也在逼公司想清楚這個職位到底要人做什麼。答不出來的如果是公司，那問題不在候選人。

---

## 坦白說

這篇的證據等級落差很大。Anthropic、Canva 的內容來自官方工程部落格，Pichai 那段是 podcast 逐字稿，這三個可以信。Meta 和 Amazon 是媒體取得的內部文件，可信但看不到全文。CoderPad 面經、掛斷電話和錄取的兩則故事，都是 X 上的個人分享，可能只代表一個人的經驗。

三派的分類是我做的，不是哪家公司自己這樣說。同一家公司會同時走兩條路，Anthropic 申請表禁 AI、take-home 卻准用就是例子。

第三段「人贏 AI 的四個地方」是我從這些證據歸納的，不是任何研究的結論。而且這份清單會縮水：Anthropic 的題目每出一代新模型就要重新設計一次，今天人還贏的地方，下一代模型可能就追上了。

---

## 關鍵洞察

1. **面試前先問三件事：准不准用 AI、現場還是遠端、什麼環境。** 同樣是打開 Claude，有人因此被錄取，有人因此被掛電話。
2. **准用 AI 的面試，分數在過程不在答案。** 讀 diff、寫測試抓 AI 的錯、講得出為什麼，這三個動作要練到變成習慣。
3. **「為什麼要請你，不是請 AI」要用一個具體時刻回答。** 你推翻 AI、抓到它的錯、為取捨負責的那一次，比任何形容詞都有說服力。

---

## 常見問題 Q&A

**Q: 2026 年大廠的技術面試還考 LeetCode 嗎？**

還考，但不再是唯一的考法。Google 至少保留一輪面對面面試，Pichai 說是為了確認基本功；Amazon 的內部指引規定，未經允許在面試中使用生成式 AI 可能被取消資格。另一邊，Meta 和 Canva 已經有讓候選人使用 AI 助手的面試輪次，題目改成在陌生程式碼庫（codebase）裡做真實開發。準備時演算法不能放掉，但要先問 recruiter 你遇到的是哪一種。

**Q: AI 輔助面試（AI-enabled coding interview）到底在打什麼分？**

既然 AI 能寫出正確答案，打分重點就從「答案對不對」移到「你怎麼跟 AI 協作」。根據 Canva 官方部落格和 X 上的候選人面經，常見評分項目包括：能不能拆解模糊需求、能不能找出 AI 產生程式碼的錯誤或次佳寫法、是否讀過並能解釋 AI 改的程式碼差異（diff）、以及能不能主導和面試官的溝通。Canva 觀察到，不常用 AI 的候選人卡住，往往不是因為不會寫程式，而是不知道怎麼引導 AI。

**Q: 大廠面試真的會問「為什麼要請你，不是請 AI」嗎？**

目前查不到任何一家公司把這題列入正式面試流程。說 FAANG 會新增「為什麼不用 AI 取代你」一輪的貼文發在 2026 年 4 月 1 日，被許多人認為是愚人節玩笑，文末還在推銷課程。不過這題在 X 上以假設題形式廣泛討論，它值得準備，因為它逼你說清楚自己在人機分工（human-AI division of labor）裡的位置。好的回答是一個具體時刻：你推翻 AI 建議、抓到它的錯、或為一個取捨負責的經驗。

**Q: AI 時代，工程師贏過 AI 的地方在哪？**

寫得快、寫得對、記得多，這幾項人已經贏不了：Anthropic 的 take-home 在 2 小時時限下，Claude 追平了人類最佳成績。人還有優勢的地方包括：沒人做過的新問題（Anthropic 把考題改成模擬新工作後才重新拉開差距）、問對問題和引導 AI 的判斷力、為上線結果負責，以及從失敗中學到的經驗。這份清單會隨模型進步而縮小，需要持續更新。

**Q: Anthropic 面試能不能用 AI？**

要分開看。Anthropic 的申請表要求申請過程不要使用 AI 助手，理由是想評估沒有經過 AI 修飾的表達能力，發言人也表示政策可能隨工具進步而更新。但它效能工程團隊的 take-home 作業明確允許使用 AI。這份 take-home 從 2024 年初開始使用、超過 1,000 位候選人做過；同樣時限下 Claude Opus 4 贏過多數應徵者，Opus 4.5 追平最強的候選人，因此 Anthropic 在 2026 年 1 月公開說明改成 AI 沒看過的解謎題型。

---

## 參考來源

- Anthropic Engineering, Tristan Hume, "Designing AI-resistant technical evaluations"（2026-01-21）：https://www.anthropic.com/engineering/AI-resistant-technical-evaluations
- Canva Engineering Blog, "Yes, You Can Use AI in Our Interviews. In fact, we insist"（2025-06-11）：https://www.canva.dev/blog/engineering/yes-you-can-use-ai-in-our-interviews/
- 404 Media, "Meta Is Going to Let Job Candidates Use AI During Coding Tests"（2025-07-29）：https://www.404media.co/meta-is-going-to-let-job-candidates-use-ai-during-coding-tests/
- Lex Fridman Podcast #471, Sundar Pichai 逐字稿：https://lexfridman.com/sundar-pichai-transcript/
- ITPro 轉述 Business Insider 取得的 Amazon 面試指引：https://www.itpro.com/business/careers-and-training/amazon-bans-ai-tools-during-job-interviews
- ITPro, Anthropic 申請表禁用 AI：https://www.itpro.com/technology/artificial-intelligence/anthropic-job-applications-ai
- X 貼文：[WarrenInTheBuff（打開 Claude 被掛電話）](https://x.com/WarrenInTheBuff/status/2100389588560728387)、[Patrick Collins（問 Claude 最好的問題而被錄取）](https://x.com/PatrickAlphaC/status/1984271373242655002)、[themishra4402（「為什麼要請你」假設題）](https://x.com/themishra4402/status/2104550509478809826)、[Wijdan（回覆）](https://x.com/wijdanri/status/2104624722520703372)、[Akshay Saini（四月一日貼文）](https://x.com/akshaymarch7/status/2039281011608146132)、[Aakash Gupta](https://x.com/aakashgupta/status/2072410669790773324)、[MillsNotMiles（CoderPad 面經）](https://x.com/MillsNotMiles/status/2103879587323134238)
