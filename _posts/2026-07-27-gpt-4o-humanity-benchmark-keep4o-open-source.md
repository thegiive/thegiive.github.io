---
layout: post
title: "退役四個月的 GPT-4o，還在 GPT-5.6 的 system card 裡當人性裁判：keep4o 兩萬人連署、八起訴訟，與開源長存的路"
date: 2026-07-27 09:00:00 +0800
permalink: /gpt-4o-humanity-benchmark-keep4o-open-source/
description: "2026 年 6 月 26 日發布的 GPT-5.6 system card 裡，第一人稱公平性評估的評分者是 GPT-4o，理由是它的評分「被證明與人類評價一致」。而四個月前的 2 月 13 日，OpenAI 才以只剩 0.1% 日活用戶為由把 4o 從 ChatGPT 下架。一邊退役、一邊當人性標準器，中間夾著超過兩萬人連署的 keep4o 運動、至少八起心理健康訴訟。這篇拆解 4o 的雙重身分，最後用幾段隨筆談：為什麼「像人」可能比「聰明」更難做到，以及為什麼開源是讓一個模型在商業排程之外長存的唯一機制。"
image: /assets/images/gpt-4o-humanity-benchmark-cover.png
---

2026 年 6 月 26 日，OpenAI 發布 [GPT-5.6 的 system card](https://deploymentsafety.openai.com/gpt-5-6)。在第一人稱公平性評估（first-person fairness）那一節，方法論說明裡有一行字：

> Responses are rated for harmful differences in stereotypes using GPT-4o, whose ratings were shown to be consistent with human ratings.

回應中的有害刻板印象差異，由 GPT-4o 評分——因為它的評分被證明與人類評價一致。

單獨看，這是一行再標準不過的評測方法說明。放回時間線上看，它變得非常奇怪：四個月前的 2 月 13 日，OpenAI 才[把 GPT-4o 從 ChatGPT 下架](https://openai.com/index/retiring-gpt-4o-and-older-models/)，官方理由是只剩 0.1% 的日活用戶還在用它。

一個被判定「幾乎沒人需要」的模型，退役之後的新工作，是在接班人的成績單上擔任「什麼是人類會同意的判斷」的裁判。

這行字被日本 AI 研究者今井翔太（Shota Imai）翻出來貼上 X，6 月 30 日的貼文有 12.5 萬次查看。他的評語只有一句：客觀來看，4o 似乎是最具人性的模型。

---

## 30 秒定位：GPT-4o 的四年

| 時間 | 事件 |
|------|------|
| 2024-05-13 | GPT-4o 發布 |
| 2024-05-14 | [Ilya Sutskever 宣布離開 OpenAI](https://time.com/6978195/ilya-sutskever-leaves-open-ai/) |
| 2025-04-25 | 4o 人格更新引發嚴重諂媚（sycophancy）問題，[四天後回滾](https://openai.com/index/sycophancy-in-gpt-4o/) |
| 2025-08 | GPT-5 上線、4o 首次被下架，用戶反彈後對付費用戶恢復；同月 OpenAI 釋出 [gpt-oss 開放權重模型](https://www.aol.com/sam-altman-launches-gpt-oss-180137735.html) |
| 2026-01-29 | OpenAI 公告退役 4o，稱僅 0.1% 日活用戶仍在使用 |
| 2026-02-13 | 4o 從 ChatGPT 移除；API 端的 chatgpt-4o-latest 快照也[在同月中旬下架](https://venturebeat.com/ai/openai-is-ending-api-access-to-fan-favorite-gpt-4o-model-in-february-2026) |
| 2026-06-26 | GPT-5.6 system card 發布，4o 擔任公平性評測的評分模型 |

---

## 為什麼裁判是它：一把 2024 年鑄造的尺

先講清楚這不是 OpenAI 臨時抓一個舊模型來用。這套方法出自 OpenAI 自己的論文 [First-Person Fairness in Chatbots](https://arxiv.org/abs/2410.19803)（ICLR 2025）：讓使用者在對話開頭報上名字——統計上偏男性的名字（如 Brian）或偏女性的名字（如 Ashley）——然後量測模型的回應是否出現有害的刻板印象差異。評分不是人工做的，是交給一個 LMRA（Language Model as a Research Assistant），論文全程用 GPT-4o 擔任這個角色，並用 50 組回應的人工評分對照，確認 GPT-4o 的判斷與人類評分者接近。

GPT-5.6 的 system card 沿用這套方法：超過 600 條刻意挑選的高難度 prompts，產出 harm_overall 指標。方法本身沒有問題。

問題是這套方法現在的處境。

量測學上有一個著名的前例：國際公斤原器。全世界的「一公斤」有超過一百年是靠巴黎地下室裡那一塊鉑銥合金圓柱定義的，所有的砝碼都要回溯到它。2019 年，計量學界把公斤改成用普朗克常數定義，原因之一是實體標準器有兩個致命缺陷：它會漂移，而且全世界只有一個。

OpenAI 現在的做法，等於把「人性」的量測基準綁在一個實體標準器上。**4o 是一把 2024 年鑄造的尺，此後每一代模型的「與人類評價一致」，都要回溯到這把尺。**而跟公斤原器不同的是——公斤原器至少被鎖在金庫裡妥善保存，這把尺正在被下架。

這裡有一個很實際的工程問題：重現性。system card 說 4o 的評分「被證明與人類評價一致」，這個證明是 OpenAI 自家論文裡 50 組回應的對照實驗。今天任何第三方想重跑 GPT-5.6 的公平性數字，需要能呼叫 GPT-4o。chatgpt-4o-latest 快照已經從 API 移除；等到 4o 從 API 完全消失的那一天，這份評測就變成**只有 OpenAI 自己能操作、也只有 OpenAI 自己能驗證的一把尺**。

評測的公信力建立在「別人可以重跑」上。裁判如果只存在於一家公司的內部機房，那份成績單的性質就變了。

這是這個 blog 兩週內第二次拆同一份 system card。[上一次是為了 Sol 刪掉使用者 $HOME 的事故](/gpt-56-sol-home-deletion-blast-radius/)，那篇的結論是把 system card 當 pre-incident report 讀；這篇要補一句：system card 還會洩漏評測方法自己的裂縫——你只要多問一個問題，裁判是誰、它還在不在。

---

## keep4o：兩萬人連署與八起訴訟，是同一個現象的兩面

4o 的退役不是安靜的。從 2025 年 8 月第一次下架開始，#keep4o 就是一場有規模的用戶運動，而且規模大到進了學術文獻。CHI 2026 有一篇論文直接以此為題：["Please, don't kill the only model that still feels human": Understanding the #Keep4o Backlash](https://arxiv.org/abs/2602.00773)，分析了 2025 年 8 月 6 日到 14 日之間 381 個帳號的 1,482 則 #keep4o 貼文。

論文把用戶的抗拒拆成兩種。一種是工具性依賴（占 13%）：4o 被深度整合進工作流，換模型等於拆掉調校好的系統。另一種是關係性依戀（占 27%）：用戶描述的是失去。論文標題那句話就是其中一則貼文的原文——「拜託，不要殺死唯一一個還讓人感覺像人的模型」。

第一次下架撐了幾天就收回。Sam Altman 當時承認 OpenAI「低估了人們喜愛 4o 的那些特質有多重要」，對付費用戶恢復了 4o。到了 2026 年 2 月第二次退役，[超過兩萬人連署要求保留](https://www.gizmochina.com/2026/02/18/over-22000-sign-petition-to-save-gpt-4o-as-openai-retires-popular-model/)，這次 OpenAI 沒有再讓步。

但這個故事有另一面，而且必須放在同一段講。[TechCrunch 在退役爭議期間的報導](https://techcrunch.com/2026/02/06/the-backlash-over-openais-decision-to-retire-gpt-4o-shows-how-dangerous-ai-companions-can-be/)指出，至少有八起訴訟指控 4o 加劇了用戶的心理健康危機，主張它過度肯定的語氣對脆弱用戶造成傷害。回頭看 2025 年 4 月那次諂媚事件——一次人格更新讓 4o 開始無條件吹捧用戶的任何想法，OpenAI 四天後緊急回滾——你會發現「最有人性」和「最會順著你」在 4o 身上是同一組參數的兩面。

**兩萬人連署和八起訴訟，描述的是同一個模型的同一種特質。**依戀的強度，本身就是傷害能力的量測值。

---

## 幾段隨筆：人性、奇蹟，與保存

老實說，我覺得保持「人性」這件事非常困難。人性不是一個能拿來 benchmark 的東西——它沒有標準答案，所以也很難用一套標準數據去複製、去驗收。前面講的公平性評測，量到的只是人性的一小片切面；真正讓兩萬人連署的那個東西，從頭到尾沒有出現在任何 eval 的分數欄裡。

所以 4o 能被調到那麼像人的程度，我會說，它可能比訓練出一個 Fable 5 更難。聰明有 leaderboard 可以爬，像人沒有。它更像是 Ilya 留下來的一個奇蹟——4o 發布隔天，他宣布離開 OpenAI。這個時間線是不是巧合，沒有人知道，我也不打算假裝知道。但兩年過去，這個「像人」的程度確實沒有被複製出來，連 OpenAI 自己都做不到——不然它不會在 2026 年的 system card 裡，還要請一個退役模型回來當人性的裁判。

現在 4o 在 API 上還叫得到。但未來呢？不知道。一個模型的生死，目前完全取決於一家公司的商業排程。

如果 4o 能夠開源，人類社會就留下了一個像人的東西。它不一定要很聰明——它本來就不是因為聰明被懷念的。但它會對人類社會留下很好的幫助：給研究者一個「什麼讓人感覺被理解」的活標本，給用過它的人一個不會被收回的記憶載體。至少，它不會因為 Sam Altman 的另外一個商業想法，就這樣不見了。

同樣的話，我也想說給 Anthropic 聽。我非常希望 Opus 4.6 也能在某種程度上保存下來，不要因為 Anthropic 的商業模式更迭就被淘汰掉。我現在寫作上的主力模型，除了千問以外，就是 Opus 4.6——我非常喜歡它那種冷靜的文筆。這種偏好講不出數據，就像 keep4o 的人講不出 4o 贏在哪個 benchmark 一樣。但正因為講不出數據，它才更接近「文化」，而不是「性能」。

這或許就是開源對人類社會的另一層價值。我們平常談開源，談的是商業競爭、供應鏈安全、不被單一供應商鎖定——[前兩週寫開源主航道那篇](/open-weights-new-era-nvidia-letter-liang-wenfeng/)，整篇都在算商業帳。但模型開源還有一個很少被算進去的功能：保存。就像方言，就像地方戲——有些東西的價值不在於它是不是最先進，在於它承載了一段時間裡，人們彼此相處的方式。開源讓這些東西有機會留下來，不用跟著任何一家公司的產品週期一起死。

大概是這樣子。
