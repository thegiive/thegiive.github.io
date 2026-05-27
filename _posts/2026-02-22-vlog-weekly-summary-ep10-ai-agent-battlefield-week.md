---
layout: post
title: "OpenClaw + 地端大模型是未來 AI 的勝負手｜Weekly Vlog EP10"
date: 2026-02-22 12:00:00 +0800
categories: [vlog, ai-battlefield]
tags: [weekly-vlog, openclaw, channel-war, ai-memory, local-model, stripe, moonwell, kimi, minimax, qwen, openviking]
permalink: /vlog-weekly-summary-ep10-ai-agent-battlefield-week/
image: /assets/images/vlog-ep10-ai-agent-battlefield-cover.jpg
description: "OpenClaw + 地端大模型，很可能是未來 AI 的勝負手。OpenClaw 這類第二代數位助理會是 AI Agent 的 Channel 重心，OpenAI 搶先收編作者 Peter 是這場 Channel 戰爭的關鍵手；而中國開源模型集體爆發，讓全地端部署變成現實。這個農曆新年還有 NotebookLM 終於可以輸出 PPT、Moonwell 因 AI 寫的程式碼賠了 178 萬美元。"
---

{% include youtube.html id="Vycs7uLzzjo" %}

**發佈日期：** 2026-02-22
**主題：** AI Agent 的戰場已經從「模型誰比較強」，轉移到「誰控制 Channel、誰掌握記憶、誰承擔後果」
**拍攝地點：** 台北
**涵蓋文章（2026-02-16 ~ 02-22）：**

1. 02/16 - Kimi K2.5 深度技術評估：Agent Swarm 到底厲害在哪裡？
2. 02/17 - 2026 農曆新年，中國開源大模型集體爆發 — Kimi、Qwen、GLM、MiniMax 怎麼選？
3. 02/18 - 2026 二月，不只中國在爆發 — 美國 AI 巨頭也在瘋狂輸出
4. 02/19 - 字節跳動 OpenViking 拆解：用「文件系統」重構 Agent 記憶，這可能是終局方向
5. 02/20 - AI Coding Tool 寫的程式碼讓 DeFi 賠了 178 萬美元：Moonwell 事件與 Stripe 的警訊
6. 02/20 - Channel 的戰爭：OpenClaw、Anthropic 和誰能決定 AI Agent 的未來
7. 02/20 - 別把 OpenClaw 用成 Claude Code：單 Agent 深化，才是你的護城河

---

## 逐字稿

### 開場：農曆新年又是資訊過載

大家好，祝大家新年快樂。

今年農曆新年跟去年農曆新年一樣，都是一個非常資訊過載的農曆新年。

去年農曆新年的話是 DeepSeek 剛出，展現了中國的開源模型可以那麼有效率，而且效果那麼好，接近當時 SOTA 的程度。

那在今年的農曆新年，其實呈現一個非常多方混戰的情況。DeepSeek 的 V4 沒有出，但是反而出了超級多的中國模型，然後每個都很接近現在 Opus 4.5 相關的 SOTA 的程度。

所以這整個系列，其實是非常有趣的一年。

---

### OpenClaw 作者 Peter 加入 OpenAI

然後在除夕夜的時候有個大新聞，就是 OpenClaw 的作者 Peter 宣布加入 OpenAI。這個東西其實也蠻有機可學的。

一開始的時候，Peter 非常喜歡 Claude，他一開始的名字 ClawdBot，其實也是致敬 Claude。但是因為很多原因，Anthropic 不是很喜歡他，一開始希望他改那個 CLI 的名字，還希望他改名。

後來也宣布了所有使用 Claude 訂閱制的用戶，不能使用像 OpenClaw 這樣的第三方工具。

但相反的，OpenAI 他們對 OpenClaw 其實是非常友善的。像一開始 Peter 說要改名叫 OpenClaw，上面有個「Open」，還特別在改名前去問 OpenAI 說，我能改名叫 OpenClaw 嗎？OpenAI 就說 "just do it"。

然後後來，OpenAI 也把他整合到生態系裡面去。最後就是在 Peter 加入 OpenAI 之後，確實 Anthropic 全面宣布在 Claude Pro 裡面，使用訂閱制的話，基本上都不能使用 OpenClaw。

---

### Channel 的戰爭：模型不是最重要的

那其實 OpenClaw 相關的一些用戶，原本是使用 Opus 的。然後他們使用 API，花的錢是很貴的。後來如果有了像 ChatGPT 這樣的訂閱制，有一個蠻接近 Opus 相關智能的模型，但是比較便宜，只需要 20 美金的訂閱費就能使用的話，那對他們來說，相關的 Opus 用戶會不會有大規模轉向使用 OpenAI 服務的可能性？

我覺得這個可能性是有的。

原因是因為在現在的 AI 時代裡面，模型其實是最底層的，它被使用的時候，必須要經過相關的 Channel。像之前的話，Cursor 是第一個 Channel，它把 Claude 的 Sonnet 包起來。後來新的 Channel 就是 Claude Code，他們自己的 CLI 自己下來做。

所以 Claude 最近會那麼流行的原因，不是因為 Claude 不夠強，而是因為他掌握了一個絕佳的 Channel 叫 Claude Code。

但現在今年年初又出了 OpenClaw，它又是 Channel 的下一代，是 AI Agent 的下一代。那在這個時代裡面，模型的能力已經不是最重要的考核點，反而是第一強化性價比，第二是能夠被某一個 Channel 所掌握，或是被哪個 Channel 所綁定，這會是比較大的重點。

所以我個人認為 OpenClaw 在這一次崛起中間遇到的一些困難，還有到最後被 Sam Altman 的 OpenAI 所收購，它可能是另外一個轉折點，對於 Anthropic 跟 OpenAI 之間的戰爭當中，是一個蠻重要的轉折點。所以我們就拭目以待吧。

---

### 中國開源模型的大爆發

然後在初一的時候，我們並沒有等到萬眾矚目的 DeepSeek V4，但是從一月底一直到整個二月，其實我們迎來了大量中國開源模型的大爆發。

像一開始的 Kimi K2.5，它有一個很好的 MoE 架構，一個 Agent Swarm 的蜂群模式，還有多模態架構，以及相當不錯的模型能力，也受到 Peter 非常大的推薦。所以到目前為止，使用 OpenClaw 當中，使用 Kimi 的還佔很大的流量。

然後後來在這週，出現了 MiniMax 的 M2.5，也有相當類似 Kimi 的能力，並且在效能這邊表現也很好。有一些網友測試，不用到非常高的顯卡就能跑 MiniMax M2.5，推論速度也相對很快。所以這也是蠻適合地端部署的一個模型。

再來到了初一，阿里巴巴出了千問最新的 3.5 版本。同樣的，它一樣標榜有相對接近 Opus 4.5 的能力，然後也有很快的推論速度跟多模態。基本上這些中國模型都非常類似，有接近 SOTA 的能力，可以說是九成或八成的水準。

同樣的，它們主要在拼所謂的性價比。而且到現在為止，MoE 的架構以及多模態架構，都已經是目前的標配。

所以再搭上像 OpenClaw 這樣的純開源、可以做純地端的系統，可以看到另外一個趨勢慢慢崛起——就是純地端的多功能 AI Agent，像 OpenClaw 這樣的架構，加上大量便宜、能力好、性能好的中國模型，能夠做很好的地端部署。這個可能會是今年一個很重要的旋律。

---

### 美國這邊也很卷

然後在初二的時候，其實不只是中國模型，美國這邊其實也蠻卷的。

首先是萬眾矚目的 NotebookLM 終於可以輸出了，除了 PDF 輸出以外，也加入了 PPT 輸出。這真的是對大家來說，比起那麼多中國模型的進展，最有感的。因為大家都大量使用 NotebookLM 來做簡報，但修改一直是個很大的問題，所以有這樣的輸出，是一個很好的更新。根據 X 上面的說法，他們會慢慢 roll out 到所有付費用戶。

同樣在這段時間，Gemini 除了 3.1 Pro，又重新刷榜。然後 Anthropic 這邊除了 Sonnet 4.6，也有很好的相關結果。也可以看到美國雖然都是走閉源模型，但也是非常努力地在讓能力往前面的邊界推進。所以美國這邊的動態，雖然不像中國那樣瘋狂，但其實也是非常卷的。

---

### OpenViking：記憶系統的重要性

到了週四，我們講到了字節出的 OpenViking，它是一個記憶相關的架構。

那我個人覺得在這時候，記憶系統蠻重要的。原因是在去年的時候，雖然我們看到模型不斷在演進，但這些閉源模型有一個很大的護城河，就是你在上面所做的任何操作，它都能夠記憶起來，變成一個獨家記憶。

像我在 ChatGPT 上面的記憶是個人記憶比較多，在 Claude 上面的記憶就會是比較工作上面的。然後 Cursor 上面有另外一組相關的記憶。那其實在這些不同的服務之間，記憶無法互相遷移，是一個很大的問題。

所以到最後我會選擇不只看模型的能力，還會看它對我的記憶、理解是不是比較深，來選擇我是不是要使用它。那這個其實是一個蠻重要的護城河。

但是今年有了 OpenClaw 這樣的開源工具出來之後，第一個好處就是我們在上面的操作、所有的記憶，都能落地成 Markdown 檔案，並且按照適當的方式來擺放。所以之後就算我們不用 OpenClaw，用其他新的數位助理架構，我們的記憶都能做相關的遷移，這是蠻重要的一點。

但是 OpenClaw 上面的記憶擺放方式，並不是最佳優化的。所以有像 OpenViking 這樣的架構其實很重要。

OpenViking 做的事情，其實是把相關的檔案像一個檔案系統一樣來擺放，根據專案或者針對主題，把它進行相關的分類擺放。當你真的要去搜尋的時候，就可以做所謂的索引搜尋。

有這樣的方式之後，你每次存取的時候就不用全部載入上下文，而是只需要透過索引搜尋。同時你也可以加入記憶的生存週期——有些比較重要的記憶它的存在是永遠的，有些比較不重要的記憶存在 30 天或 60 天。

用時間以及重要性的方式來擺放的話，那其實就已經很像我們人腦的記憶系統了。

所以我個人認為像這樣的架構，到最後可能會是新時代 AI Agent 服務的重要護城河。

---

### Moonwell 事件、Stripe 警訊、權責分離問題

最後，在這週其實也發生一個重要事情，就是有一個加密貨幣的廠商叫做 Moonwell，因為程式碼寫錯，出了一些問題，損失了 100 多萬美金。但是相關的程式碼，上面表述是由 Claude Code 這邊 AI Coding 所做出來的。

雖然到最後大家復盤的時候，一些資深的人也說，這個問題就算是人來寫，也很難發現。這其實是一個比較難的 bug。

但是這又回到說，我們現在對 AI Coding 的掌握還沒到很好的程度。AI Coding 發展還太新了，我們都知道怎麼加速 10 倍、100 倍，但是相關的配套，像是 Methodology 的選擇、Code Review Process，完全無法 cover AI Coding 相關的極致產出量。

所以現在如果是一些比較一般的 MVP 或小專案的部分，相對來說比較簡單，就 just do it。但如果是離錢比較近的，像金融、保險、醫療方面的部分，我們是不是真的能夠完全信賴 AI Coding 做的東西，而不做 Code Review？這是比較難的。

同樣在同一時間看到 Stripe，他在 X 上面宣布他們有一個新的 AI 系統叫做 Minions。最新這週，他已經用 AI 自動寫了 1,000 個 PR。1,000 個 PR 很多，但下面就有人問說，1,000 個 PR，那你要怎麼做 Code Review？你是 human review 嗎？

你該怎麼做這件事情？這其實問到一個很大的問題。如果當你一週有 1,000 個 PR，這樣的產出量，像 Stripe 絕對不會有這樣的人力去做 human review，這是不可能的。

那在這情況下，Stripe 對大家來說算是一個 Tier 0 的重要場景，因為他是金融場景。你隨便一個 bug，都可能造成幾百萬、幾千萬的相關損失。在這情況下，我們是不是真的能夠用 human review 來做 AI code 的東西？裡面存在很多問題。這是現在看到最大的問題。

同一時間看到 Anthropic，宣布可以用 Opus 來做相關的 Security Check。這當然是目前大家都在做的事情，但其實也聽起來蠻好笑的，因為我們用 Opus 來寫程式，又用 Opus 來做 Code Review 或 Security Review。

在資訊金融行業裡面，就完全無法做到所謂的權責分離。撰寫的人用這個模型來做，但 review 的人也用同一個模型來做 review。那假設如果這個模型有些系統性的問題，這個問題是不是就會直接繞過這樣的 review 模式，直接出去呢？

所以這個問題，可能在未來會越來越嚴重。不管是像 Stripe 或者是像 Anthropic 這樣的機制，隨著 AI Coding 越來越強、效率越來越明顯，這個問題一定會越來越被大家發現。我們該怎麼樣做出一個治理的架構，這會是未來最重要的機制。

---

### 本週總結：2026 年的主旋律

最後，在這個農曆新年期間看到一個蠻重要的重點。

我覺得 2026 年的主旋律，就是像 OpenClaw 這樣的第二代數位助理會慢慢崛起。而且比較好的事情是，它不會再被某一個模型廠商或某一家廠商所控制。它能夠做到全開源、全部可以自行部署，甚至能夠做到全地端的相關機制。

並且相關的護城河——Memory 系統，也可以完全被開源的架構用檔案或使用比較好的索引儲存、向量搜尋，以及加上比較好的 TTL 機制，都能夠控制。

所以這樣搭配下去的話，每個人人手一個 AI 助理，這件事也不再是個夢。

同樣的，最重要的大腦這邊，也看到了大量中國開源模型的輸出。有 Kimi K2.5、MiniMax M2.5，還有千問 3.5，以及未來可能會出的 DeepSeek V4。這些模型每一個都有接近 SOTA 70%、80% 到 90% 的能力，加上很好的性價比。

然後搭配 OpenClaw 這樣的工具，都可以做到全地端。可以發現到，現在美國追求的閉源模型加上相關工具鏈的模式，會慢慢失效。

未來只會有兩條線：一條是比較貴、但效果好一點點的工具鏈跟模型。以及大量的私人助理，能夠部署到全地端，並且用開源模型做到完全的數據自主權。

那我個人認為今年的話，可能是後者這件事情會越來越大、越滾越大。這可能是大家可以參考的方向。

這就是我在這個農曆過年跟大家分享的東西。謝謝大家，也再次祝大家新年快樂。

---

## 文章連結

1. [Kimi K2.5 深度技術評估：Agent Swarm 到底厲害在哪裡？](https://ai-coding.wiselychen.com/kimi-k2-5-agent-swarm-deep-dive-technical-assessment/)
2. [2026 農曆新年，中國開源大模型集體爆發 — Kimi、Qwen、GLM、MiniMax 怎麼選？](https://ai-coding.wiselychen.com/china-ai-models-2026-lunar-new-year-comparison/)
3. [2026 二月，不只中國在爆發 — 美國 AI 巨頭也在瘋狂輸出](https://ai-coding.wiselychen.com/ai-weekly-notebooklm-pptx-claude-sonnet-4-6/)
4. [字節跳動 OpenViking 拆解：用「文件系統」重構 Agent 記憶，這可能是終局方向](https://ai-coding.wiselychen.com/openviking-agent-memory-filesystem-paradigm/)
5. [AI Coding Tool 寫的程式碼讓 DeFi 賠了 178 萬美元：Moonwell 事件與 Stripe 的警訊](https://ai-coding.wiselychen.com/moonwell-oracle-mispricing-ai-coding-178m/)
6. [Channel 的戰爭：OpenClaw、Anthropic 和誰能決定 AI Agent 的未來](https://ai-coding.wiselychen.com/openclaw-anthropic-channel-war/)
7. [別把 OpenClaw 用成 Claude Code：單 Agent 深化，才是你的護城河](https://ai-coding.wiselychen.com/single-agent-vs-multi-agent-openclaw/)
