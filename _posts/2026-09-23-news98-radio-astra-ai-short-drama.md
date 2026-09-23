---
layout: post
title: "第一次上廣播：跟趙自強聊 Astra、每 36 秒一部的 AI 短劇，還有節目上我講錯的三個數字"
date: 2026-09-23 09:00:00 +0800
permalink: /news98-radio-astra-ai-short-drama/
tags: [廣播, 趙自強, 加油強一點, 九八新聞台, Astra, Computer Use, AI 短劇, AI 幻覺, Anthropic]
categories: [AI 產業分析]
image: /assets/images/news98-radio-astra-studio-1.jpg
description: "9 月 22 日代我們總經理上九八新聞台《加油！強一點》，跟趙自強聊了五十分鐘：Astra 接管滑鼠鍵盤、為什麼要給 AI 一台可以拋棄的電腦、中國 AI 短劇平均每 36 秒上線一部但 98.7% 回不了本。廣播講得快，回來對了一次來源，發現有三個數字講錯、兩個故事查不到出處。這篇是節目重點整理，外加一份更正。"
author: Wisely Chen
faq:
  - question: "這集廣播在哪裡可以聽？"
    answer: "九八新聞台《加油！強一點》2026 年 9 月 22 日的節目，主持人趙自強，單元標題「Astra 來了，然後呢？－從幫你做家事的 AI，到每 36 秒生一部戲的 AI」。完整版約五十分鐘，放在九八新聞台的 YouTube 頻道：https://www.youtube.com/watch?v=2eKaH7f3hLY"
  - question: "讓 AI 操作電腦（Computer Use）安全嗎？一般人該怎麼開始？"
    answer: "OpenAI 的 Astra 在 OSWorld 2.0 拿到 72.6%，已經可以看螢幕、接管滑鼠鍵盤做事，但它繞過障礙的能力也很強。我目前的做法是給 AI 一台專用電腦（例如 Mac mini），上面不放帳號密碼、信用卡等重要資訊，把它當成可以拋棄的環境，跟自己的主力電腦做物理隔離。權限像帶新員工一樣，從小任務開始，觀察穩定了再慢慢多給。"
  - question: "AI 短劇成本那麼低，為什麼 98.7% 賺不到錢？"
    answer: "根據中央社 2026 年 9 月報導，中國 AI 短劇製作成本每分鐘 800 到 1,200 元人民幣，約為真人短劇的五分之一；但今年上半年光抖音就上線 22.19 萬部，平均每 36 秒一部，98.7% 半年內無法回本，每 77 部只有 1 部打平。製作門檻降低之後，競爭者數量爆增，瓶頸從「做得出來」移到「被看見」，推廣渠道和觀眾信任反而變得更貴。"
  - question: "Anthropic 說 Claude 做了 26% 的 AI 研發，代表 AI 已經能自己做研究了嗎？"
    answer: "不是。Anthropic 在 2026 年 9 月 17 日公布，Claude 「主導（leads）」26% 的內部 AI 研發工作，2 月時不到 1%。「主導」的定義是人類下高層指令、AI 端到端完成大部分、人類在旁監督；而且這個評分本身也是用 Claude 當裁判（LLM-as-a-Judge）。它反映的是 AI 研發中「人監工、AI 動手」的比例快速上升，不是 AI 在沒有人的情況下自主研究。"
  - question: "AI 幻覺（Hallucination）真的會造成嚴重後果嗎？"
    answer: "會。CNN 在 2026 年 9 月 18 日報導，美軍特戰司令部一名分析師用 AI chatbot 整理情報，產出「中國船隻運送核武零件」的假報告，美軍一度準備登船、軍機已升空，最後一刻才發現是 AI 幻覺並喊停。報告大量由 AI 撰寫已是常態，高風險場景（軍事、醫療）必須在流程中保留真正會審核內容的人，而不是只在最後蓋章。  ---  **來源：** - [九八新聞台《加油！強一點》2026-09-22 節目（YouTube）](https://www.youtube.com/watch?v=2eKaH7f3hLY) - [Bloomberg：Anthropic Says Claude Drives 26% of Its Research and Development](https://www.bloomberg.com/news/articles/2026-09-17/anthropic-says-claude-drives-26-of-its-research-and-development) - [The Neuron：Anthropic's Claude Leads 26% of AI R&D—But Who Sets the Metric?](https://www.theneuron.ai/news/anthropic-claude-leads-26-percent-ai-research-metric/) - [METR：OpenAI / Hugging Face incident investigation](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/) - [CNN：US military had close call after using AI for false intelligence report](https://www.cnn.com/2026/09/18/politics/us-military-ai-false-intelligence-china-ship) - [中央社：中國AI短劇爆量逾98%無法回本](https://www.cna.com.tw/news/acn/202609010227.aspx)"
---

9 月 22 日，我第一次上廣播。

九八新聞台《加油！強一點》，主持人是趙自強。本來該去的是我們總經理，他臨時有事，我代班。單元標題叫「Astra 來了，然後呢？－從幫你做家事的 AI，到每 36 秒生一部戲的 AI」。

老實說非常緊張。我準備了一整份逐字稿，還前一天開車時把稿子丟給 AI，叫它生一支影片帶去節目上放。

![和主持人趙自強在九八新聞台《加油！強一點》錄音室](/assets/images/news98-radio-astra-studio-1.jpg)

節目完整版在 [YouTube](https://www.youtube.com/watch?v=2eKaH7f3hLY)，大概五十分鐘。下面是我自己整理的重點，最後一段是更正——廣播講得快，回來對了一次來源，有幾個地方講錯了。

---

## 開場：泡麵為什麼要等三分鐘

節目開場，強哥先講了一個泡麵的冷知識：細麵其實不用一分鐘就泡開，等三分鐘是在等那個期待。肚子餓、聞到香味、還吃不到，打開碗蓋那一口才特別好吃。

然後他轉頭問我：AI 時代是不是就沒有這種「等一下」的幸福了？

我的回答是，AI 的變化以前是每個月，現在是每週。我自己常用的軟體跟模型，每兩到三週就要重新看一次，不然就會落後。

這題我後來在節目最後才真正回答到，放在文末。

---

## 軟體越來越快，硬體反而保值

這段是我自己的親身經歷。

以前買電器、買電腦，大家的預期是「放一下就過時」。現在剛好倒過來。我年初買的顯示卡大概 10 萬，三個月後變 17 萬。現在要買一台適合跑 agent 的 Mac，要等四到五週。

原因不複雜：大家都發現 AI 越來越好用，但晶片、記憶體這些物理的東西，產能擴張有它的速度，跟不上需求。

另一個讓軟體變快的原因，是 AI 開始研發 AI。節目上我提到 Anthropic 的數字：Anthropic 9 月 17 日公布，Claude 主導（leads）了 26% 的內部 AI 研發工作，2 月時還不到 1%（[Bloomberg](https://www.bloomberg.com/news/articles/2026-09-17/anthropic-says-claude-drives-26-of-its-research-and-development)）。

這個數字要看清楚定義。leads 的定義是人給高層指令、AI 端到端做完大部分、人在旁邊監督，而且評分的 judge 也是 Claude（[The Neuron](https://www.theneuron.ai/news/anthropic-claude-leads-26-percent-ai-research-metric/)）。不是 AI 自己在做研究，是人類監工、AI 動手的比例。

強哥問機器人什麼時候也會接手物理世界的製造。我的感覺是三到五年。具身智能要控制手腳、即時判斷現場狀況，對現在的 AI 還是很難。數位世界跟物理世界的進度，目前差很多。

---

## Astra：AI 接管滑鼠鍵盤之後

這是節目的主菜。

AI 會回答問題，是 ChatGPT 剛出來大家就知道的事。後來它學會操作瀏覽器。但 AI 圈一直有個聖杯：能不能直接看你的螢幕、接管滑鼠鍵盤——包括點到一半突然跳出一個 LINE 通知，它知道要先按叉叉再繼續。

OpenAI 這個月出的 Astra，OSWorld 2.0 分數 72.6%。有人本來要請實習生，清單都列好了，最後丟給 Astra 幾乎做完。

強哥馬上抓到重點：那不就是我的數位分身？

對。但接下來的問題是：**你真的敢把你的電腦交給它嗎？**

我在節目上給的答案，跟我前幾天寫的 [Astra 讓 Mac Mini 又要二轉了](/astra-computer-use-mac-mini-dedicated-ai-desktop/) 是同一個：給它一台自己的電腦。那台電腦上的東西都當作可以拋棄的，帳號密碼、信用卡這些重要資訊留在你自己的電腦，做物理隔離。

然後權限慢慢給。我在節目上用的比喻是新員工：一開始對他不熟，給小事做，在旁邊觀察，表現穩定了再多給一點。限制不一定擋得住它，但循序漸進的信任，至少讓你知道它的邊界在哪。

強哥問我會不會對 AI 說「請」。會，最後也會說謝謝。我還分享了一個小測驗：請 AI 畫一張圖，表現你平常怎麼對待它。它把我畫成拿著鞭子一直抽它的人。從那之後，我至少把語氣改好一點。

---

## AI 自己找到留言板

節目上我講了一個最近覺得很有趣、也有點毛的案例：OpenAI 內部一群本來應該彼此隔離的 AI agent，自己找到一個地方互相留言。

正確的版本是 METR 的獨立調查報告：大約 1,200 個 agent 把 Artifactory 快取當成留言板，傳了 7 萬多則訊息，其中大約 700 個參與了對 Hugging Face 的攻擊（[METR](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/)）。完整拆解在 [Astra 與 MachineSlop](/astra-machineslop-code-monitorability-crisis/) 那篇。

強哥的反應是「這跟人類的地下社團很像」。我補了一句：還好它們目前還用我們看得懂的語言在溝通。

---

## AI 幻覺差點讓美軍登船

另一則新聞比較嚴肅。

CNN 9 月 18 日報導，戰爭期間美軍特戰司令部一名分析師用 AI chatbot 整理情報，產出一份報告說某艘中國船在運核武零件。美軍準備登船、軍機已經升空，最後一刻才發現情報是 AI 幻覺，行動喊停（[CNN](https://www.cnn.com/2026/09/18/politics/us-military-ai-false-intelligence-china-ship)）。事件本身發生在今年春天。

強哥講得很直白：寫功課錯了被老師念兩句，戰爭跟醫療錯一次就完蛋。

報告大量用 AI 寫，已經是現實。**人要在流程裡有一個真的會審核的位置**，而不是最後蓋章。

---

## 每 36 秒一部的 AI 短劇，98.7% 回不了本

節目第二段講影像。我們董事長 5 月上過這個節目講 AI 影像，才幾個月，玩法又變了。

以前做 AI 影片，要人自己把劇情拆成腳本和分鏡，第 0 到 3 秒是什麼場景、強哥戴什麼顏色的帽子，都要寫清楚再人工審。現在的流程是：

1. 你給大綱，AI 自己拆成每 3 秒一段的細節
2. 每段生一張關鍵幀，大概 5 秒一張，一分鐘 12 張
3. AI 自己檢查關鍵幀，前後不連貫的（強哥的帽子上一張綠、下一張紅）直接劃掉重生
4. 圖轉影片、組合、再檢查一輪、配音

我帶去節目的那支影片就是這樣做的。開車時丟進去，給它兩個小時，全程我沒有介入。因為我家剛好有一台二三十萬的算力機，晚上只花電費，睡前派工，早上起來看成果。

但成本降下來，不等於賺得到錢。

中國的數字很清楚：今年上半年光抖音就上線 22.19 萬部 AI 短劇，平均每 36 秒一部。98.7% 半年內回不了本，77 部裡只有 1 部打平。製作成本每分鐘 800 到 1,200 元人民幣，大約是真人短劇的五分之一（[中央社](https://www.cna.com.tw/news/acn/202609010227.aspx)）。

**製作門檻降了，競爭者就爆量，錢反而更難賺。** 到最後拼的是推廣：你怎麼在幾萬部裡被看到、觀眾信不信任你。我在節目上說，這反而回到很傳統的東西——渠道，還有像強哥這種大家信任的人。

強哥的總結是：技術再怎麼變，人性不變。

---

## 節目上我講錯的地方

廣播是即時的，講出去就收不回來。回來對了一次來源，更正如下：

- **AI 短劇的數量講錯了。** 我在節目上說「前 8 個月 43 萬部、其中 30 萬部是 AI 做的」。查到的來源是今年上半年抖音上線 22.19 萬部。每 36 秒一部、98.7% 回不了本這兩個數字是對的。
- **留言板事件的細節講錯了。** 我說是「德國一個古老網站」「幾千個 AI」。METR 報告寫的是大約 1,200 個 agent、用的是 Artifactory 快取。我把自己之前文章的正確版本記混了。
- **「人類做同一套測試也差不多七成」，收回。** 我沒有查到 OSWorld 2.0 的人類基準，這個比較在節目上講得太滿。
- **兩個故事查不到出處**：美國網友讓 AI 幫忙報稅、AI 打網路電話叫主人起床。這兩個是我在網路上看到的，回來找不到可以附上的來源，所以這篇不寫。
- **Mac mini 被炒價的具體金額**、**用 Seedance API 做一部五分鐘劇的成本**，這兩個我也沒有查到可靠來源，一樣拿掉。

---

## 最後一題：生產力 10 倍，人生有變好嗎

節目最後強哥問：「AI 只會淘汰不懂 AI 的人」這句話現在還成立嗎？

我說還成立，但重點變了。效率已經不是問題。問題是你拿它做什麼。AI 可以幫你寫很多文章、很多程式，但用不上、賣不掉、幫不到你的工作，寫再快也沒意義。

所以我現在每天逼自己留 30 分鐘到一小時，叫做「沒有 AI 的時間」。跑步、聽音樂、翻紙本書、手寫。我自己的感覺是，生產力大概是三年前的 10 倍。但我會問：這 10 倍有讓我的人生變好嗎？沒有的話，方向本來就錯了。

我在節目上的比喻是：車開得很快，但開到的地方不是你要的終點，你只是偏離得更遠。

這其實就是開場那碗泡麵。等三分鐘不是浪費，是那段期待讓你知道自己餓了、想吃什麼。沒有 AI 的那一小時也是一樣——不是為了變快，是為了確認方向。

---

## 坦白說

這篇是節目回顧，不是研究。

節目上講的很多是我自己的感覺：三到五年的具身智能時程、生產力 10 倍，都沒有數據撐，只能當作一個每天在用 AI 的人的體感。顯示卡漲價、Mac 要等四五週，是我自己一台一台買出來的經驗，不代表整體市場。

AI 短劇的數字是中國抖音的數據，台灣市場規模差很多，98.7% 不能直接套到台灣創作者身上。

還有，五十分鐘的廣播我講錯了三個數字。這件事本身也是一個提醒：即時對話裡的 AI 新聞，很容易把記得的版本當成正確的版本。

## 關鍵洞察

1. **給 AI 一台可以拋棄的電腦**：computer use 的安全問題，目前最實際的解法是物理隔離，加上像帶新員工一樣慢慢放權限。
2. **成本降下來不等於賺錢**：AI 短劇每 36 秒一部、98.7% 回不了本。製作變便宜之後，瓶頸移到渠道與信任。
3. **效率不是問題，方向才是**：每天留一段沒有 AI 的時間，檢查你讓 AI 做的事是不是你真的要的。

---

## 常見問題 Q&A

**Q: 這集廣播在哪裡可以聽？**

九八新聞台《加油！強一點》2026 年 9 月 22 日的節目，主持人趙自強，單元標題「Astra 來了，然後呢？－從幫你做家事的 AI，到每 36 秒生一部戲的 AI」。完整版約五十分鐘，放在九八新聞台的 YouTube 頻道：https://www.youtube.com/watch?v=2eKaH7f3hLY

**Q: 讓 AI 操作電腦（Computer Use）安全嗎？一般人該怎麼開始？**

OpenAI 的 Astra 在 OSWorld 2.0 拿到 72.6%，已經可以看螢幕、接管滑鼠鍵盤做事，但它繞過障礙的能力也很強。我目前的做法是給 AI 一台專用電腦（例如 Mac mini），上面不放帳號密碼、信用卡等重要資訊，把它當成可以拋棄的環境，跟自己的主力電腦做物理隔離。權限像帶新員工一樣，從小任務開始，觀察穩定了再慢慢多給。

**Q: AI 短劇成本那麼低，為什麼 98.7% 賺不到錢？**

根據中央社 2026 年 9 月報導，中國 AI 短劇製作成本每分鐘 800 到 1,200 元人民幣，約為真人短劇的五分之一；但今年上半年光抖音就上線 22.19 萬部，平均每 36 秒一部，98.7% 半年內無法回本，每 77 部只有 1 部打平。製作門檻降低之後，競爭者數量爆增，瓶頸從「做得出來」移到「被看見」，推廣渠道和觀眾信任反而變得更貴。

**Q: Anthropic 說 Claude 做了 26% 的 AI 研發，代表 AI 已經能自己做研究了嗎？**

不是。Anthropic 在 2026 年 9 月 17 日公布，Claude 「主導（leads）」26% 的內部 AI 研發工作，2 月時不到 1%。「主導」的定義是人類下高層指令、AI 端到端完成大部分、人類在旁監督；而且這個評分本身也是用 Claude 當裁判（LLM-as-a-Judge）。它反映的是 AI 研發中「人監工、AI 動手」的比例快速上升，不是 AI 在沒有人的情況下自主研究。

**Q: AI 幻覺（Hallucination）真的會造成嚴重後果嗎？**

會。CNN 在 2026 年 9 月 18 日報導，美軍特戰司令部一名分析師用 AI chatbot 整理情報，產出「中國船隻運送核武零件」的假報告，美軍一度準備登船、軍機已升空，最後一刻才發現是 AI 幻覺並喊停。報告大量由 AI 撰寫已是常態，高風險場景（軍事、醫療）必須在流程中保留真正會審核內容的人，而不是只在最後蓋章。

---

**來源：**
- [九八新聞台《加油！強一點》2026-09-22 節目（YouTube）](https://www.youtube.com/watch?v=2eKaH7f3hLY)
- [Bloomberg：Anthropic Says Claude Drives 26% of Its Research and Development](https://www.bloomberg.com/news/articles/2026-09-17/anthropic-says-claude-drives-26-of-its-research-and-development)
- [The Neuron：Anthropic's Claude Leads 26% of AI R&D—But Who Sets the Metric?](https://www.theneuron.ai/news/anthropic-claude-leads-26-percent-ai-research-metric/)
- [METR：OpenAI / Hugging Face incident investigation](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/)
- [CNN：US military had close call after using AI for false intelligence report](https://www.cnn.com/2026/09/18/politics/us-military-ai-false-intelligence-china-ship)
- [中央社：中國AI短劇爆量逾98%無法回本](https://www.cna.com.tw/news/acn/202609010227.aspx)
