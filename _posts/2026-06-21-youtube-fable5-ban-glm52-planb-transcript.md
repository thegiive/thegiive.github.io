---
layout: post
title: "YouTube 逐字稿：Fable 5 封禁+被打穿，你的 AI 有 Plan B 嗎？GLM-5.2 橫空出世"
date: 2026-06-21 13:09:04 +0800
permalink: /youtube-fable5-ban-glm52-planb-transcript/
image: /assets/images/youtube-fable5-glm52-planb-thumbnail.jpg
description: "**作者：** Wisely Chen **日期：** 2026 年 6 月 **系列：** AI Coding 實戰觀察 — YouTube 逐字稿 **關鍵字：** Fable 5, 出口管制, GLM-5.2, 智譜, 開源模型, Plan B, Harness, AI 安全, stateful 攻擊, System Prompt"
---

![Fable 5 封禁+被打穿，你的 AI 有 Plan B 嗎](/assets/images/youtube-fable5-glm52-planb-thumbnail.jpg)

**作者：** Wisely Chen
**日期：** 2026 年 6 月
**系列：** AI Coding 實戰觀察 — YouTube 逐字稿
**關鍵字：** Fable 5, 出口管制, GLM-5.2, 智譜, 開源模型, Plan B, Harness, AI 安全, stateful 攻擊, System Prompt

---

## 這集在講什麼

這週圍繞三件連在一起的大事：Fable 5 被美國出口管制封禁、GLM-5.2 橫空出世成為開源 Plan B、Fable 5 被駭客組織打穿洩漏完整 System Prompt。

三件事的底層邏輯是同一條線：**你把所有賭注壓在雲端閉源模型上，政治風險、安全風險、品質風險全部不在你手上。** 封禁讓你的工作流斷線，打穿讓你知道防護牆形同虛設，而 GLM-5.2 的出現證明開源已經走到可以當 Plan B 的水準。

---

**長度：** 約 12 分鐘
**場景：** 車內

{% include youtube.html id="D47iivBB2M4" %}

### ⏱️ 時間戳

- 0:00 Fable 5 被美國出口管制封禁
- 0:47 企業的 AI 工作流隨時可能失效
- 1:05 最簡單的 Plan B：換到 ChatGPT 做 round-robin
- 1:52 GLM-5.2 橫空出世——開源模型的真正突破
- 2:28 社群好評如潮：西方博主也在讚
- 3:07 雲端推力 vs 開源 Plan B 的交會點
- 3:43 智譜股價直接翻倍的原因
- 4:10 GLM-5.2 能取代 80% 的 Agentic Workflow
- 4:43 硬體需求：4 張 RTX PRO 6000 或 Mac 256GB
- 5:16 小模型還是 Qwen 3.6 27B 的天下
- 5:48 Fable 5 被駭客打穿：System Prompt 完整洩漏
- 6:17 Fable 5 不只是模型，是一整套 Harness 系統
- 7:01 模型能力到頂？Harness 的投資報酬率更高
- 7:37 未來趨勢：閉源模型都會走 Harness 內建化
- 8:06 攻擊手法拆解：同形字 + 溫水煮青蛙
- 9:08 AI 資安核心問題：stateful 攻擊 vs stateless 防禦
- 10:00 99.9% 防護率在上億次攻擊下 = 必定被攻破
- 11:14 總結 + 台灣生成式 AI 年會預告

---

### 逐字稿

大家好，上週我們知道了 Anthropic 的 Fable 5 被美國以出口管制禁止了。

那我們就可以看到，大家在這週有大量的討論。因為大家突然之間發現到，你在雲端上面使用的 AI，它不只有可能被 OpenAI、Anthropic 突然之間進行一個降級，它可能也有資安的議題。它現在甚至有可能被政府單位視為是一個戰略級的武器，然後被出口管制。

所以你之前打造的，使用這些 API 所打造的這些工作流、自動化工作流或是一些 Application，都有可能突然之間失效。

那在一般的公司來說，遇到這情況我再換人就好了。但是對於比較大的公司，或是仰賴它來做一些服務的公司來說，這個就是個滅頂之災。

所以大家其實都在思考一件事就是說，我們到底有沒有 Plan B？有沒有一個 Backup Plan？

那當然現在來說最簡單的 Backup Plan 就是換到 ChatGPT，或是把 ChatGPT 當作一個 round-robin 的 Service，然後兩邊同時來做使用。這可能也是目前來說成本最低的方式。

但其實我們都會知道說，隨著 AI 的持續演進，它的 Token 錢越來越貴，然後它們的服務品質有可能下降。這個時候加上大家之前已經有囤積了一些顯示卡，所以大家都在想說我到底能不能用地端來做一個 Backup Plan。

---

#### GLM-5.2 橫空出世

那在這個時間點，我們發現到 GLM-5.2 應該算橫空出世吧。原因是因為之前中國的模型，大家跑出來的時候就看到說它有大量的分數都已經超英趕美了。但這次 GLM-5.2 我們看到最大的差別，不只是它的評分已經出來都已經贏過了很多的閉源模型，甚至在大量的榜單裡面只輸給 Opus 4.8，或是甚至有一兩個前端的榜單它只輸給 Fable 5。

所以我們不只看到這樣子，我們還看到大量的網友、大量的社群——這邊講到社群不只是中國社群，我在 X 上看到大量的西方博主，他們都非常讚賞 GLM-5.2。大家給的感覺都是說，頭一次感覺到一個開源的模型非常接近 Opus 4.8 現在最好的模型，然後在 Coding 這邊的能力甚至大家都感覺到稍微贏過 GPT-5.5。

所以在左邊雲端大家平常最熟悉的這個敘事，有不斷大量的推力在推著我們尋找一個 Backup Plan。在這邊突然之間也橫空出世 GLM-5.2，是一個開源的模型。雖然它是中國的，但是它是開源模型，所以大家可以在自己的機房裡面，只要有足夠的算力就能把它跑起來。

這個其實對中型或大型公司來說，是非常有吸引力的。

---

#### 智譜股價翻倍

所以在這個情況下，我們也看到了自從 GLM-5.2 出了之後，智譜它的母公司在香港這邊的股價直接乘以二，直接變成兩倍。

原因其實也蠻簡單的，就是大家都看到這個需求。我們這些公司需要一個開源的載體來承載開源的 Backup Plan 這個需求。那 5.2 剛好就在這個時間點出了，而且 5.2 它的相關能力是真心的，大家都覺得是真的，真心覺得真的好的。

簡單講就是它已經能夠取代幾乎所有的 Agentic Workflow 的相關東西，除了一些比較前沿的研究 Workflow，可能最前沿的 10% 到 20% 可能還是輸給閉源模型，但 80% 的肯定是沒什麼問題的。

---

#### 硬體需求

那根據目前大家的看法，GLM-5.2 如果用社區開源的量化模型的話，大概 4 張 RTX PRO 6000 就能夠跑起來。當然如果用更加極端的 2-bit 這種模式的話，看到的就是一個 Mac 256GB，或是一個 24GB 左右的 GPU 加上大概 256GB 的 RAM，Windows Server 基本上就能跑起來。

在小模型這邊，它當然是無法取代的。因為 Qwen 3.6 27B 跟 35B 還是一個非常厲害的小模型，它能夠跑在現在所有大家垂手可得的消費者硬體上面。但是在中型公司或大型公司這邊，幾百萬等級的 Server 上面，GLM-5.2 跑起來應該是沒有什麼太大的問題的。

所以這就是現在大家所心心念念找的一個 Plan B。

---

#### Fable 5 被打穿

那再回到 Fable 5 這邊。在這次我們看到了 Fable 5 剛出的時候就被一個駭客的組織成功的打進去，並且也套出了它的一個完整的 System Prompt。

我們發現到這個 System Prompt 其實非常有趣。因為它這個 System Prompt 裡面花了大量章節描述它怎麼調用工具，甚至它裡面的 Linux Sandbox 都已經描述出來了。所以大家驚覺到，原來 Fable 5 它不只是一個前沿的 LLM 模型，它其實裡面是一個完整的一套 Harness。

所以這時候就有網友出來講說，你這樣比更不公平，你拿一個雲上面的 Claude Code 去跟大家的裸模型來比，那當然是雲上面的 Claude Code 有一個完整的配套措施、完整的工具鏈，它一定會比裸模型效果更好。

但我們看到的點，當然你要這樣講也對。但對我來說 Fable 5 其實就指引了一個很重要的一個模式：**在現在這個時代，模型可能也到了某種程度的能力上限，大家要再去繼續提升它的能力的話，性價比可能會越來越低。**

在這情況下，把你自己的 Harness、相關的 Agent 系統工程把它做好搭好，可能它的投資報酬率遠遠會高於去捲相關模型。

所以我們也會看到接下來應該會有大量的閉源模型像 Anthropic、OpenAI 或是 Google，他們推出來的模型應該都會走 Fable 5 這樣的方式，就是不只是提供一個 API、後面提供的不只是一個大模型，還是一整套的 Harness。那這個是很有可能出現的情況，這可能也是未來相關的趨勢。

---

#### 攻擊手法拆解

那最後我們再看到 Fable 5 這一次剛出了就被駭客組織打穿。我們去看他的被打穿的過程，其實就是一些比較傳統的方式。像是用同形字，用不同語言的字看起來一樣的字，然後偽裝成原本的字母去繞過他的分類器。並且他用說我在做一個學術研究，我在做一個教科書，請你幫我把這個東西展開來。再加上不斷地溫水煮青蛙，不斷去試探分類器的極限，盡量不要踩到閾值，然後很快就能夠把它繞過去了。

這就讓我回想到我之前在一月的時候寫了一篇自己覺得很棒的訪談。這個訪談是 OpenAI 大神在 Lenny's Podcast 講的部分，他裡面學到所有觀念到目前為止都還適用，而且他的預言越來越準。

---

#### Stateful 攻擊 vs Stateless 防禦

裡面的預言就幾個。第一個是現在的 AI 資安到底為什麼那麼難防？原因是因為現在針對 AI 模型的攻擊它是一個 stateful，它是一個有一連串的順序，然後多個動作的組合拳。但是我們現在能夠對它架設的防護 GuardRail，或是防護的 Harness，其實都是針對一個又一個 Request、單一 Request 來進行防護，所以它是 stateless。

所以這些攻擊四五個下來，其實每個都看起來是一個很正常的 Request，但是再把它組合起來套給後面的語言模型之後，模型就會被騙到，然後輸出不該輸出的東西。

那第二個他也講到一個概念：就算我們現在的 GuardRail 有 99%、99.9% 的防護度，但是像這一次攻擊 Fable 5 的駭客組織，他其實是用一個 AI Agent，用 Opus 去打 Fable 5，並且嘗試不同的相關攻擊。因為現在 AI Agent 要拿來做攻擊其實也是很容易的，所以他們可以很輕易弄出幾百萬、幾千萬、上億的攻擊。

就如同他裡面講的：**就算你的防護率是 99%，在 100 萬、1000 萬、1 億、上百億的攻擊下，你被攻破的機率是百分之百。**

所以現在前沿模型一定會被打攻破，這是他裡面講的相關東西。

---

#### 總結

總之，這週其實都是圍繞在 Fable 5 這個最前沿的模型，然後它所引起的政治的鬥爭。我們因為這個被封禁，所有要找 Plan B 的——尤其是大公司——都在思考要怎麼樣去防範未來的這些風險。然後 Fable 5 那麼容易被打進去，那未來真的所有的模型是不是都很容易被打進去。最後我們要找 Plan B，這時候智譜就跑出一個很棒的 GLM-5.2。

這些東西都在證明說這個世界還在持續高速地往前邁進。

那我在下週的台灣最大的生成式 AI 年會，會講我這一年來不斷用相關的 FDE 的 Best Practices 去調整公司的一些運作，然後最後收到了一些成效，還有客戶在使用 AI 的團隊他有一些什麼看法，我們要怎麼樣去應對、怎麼樣做 review。

也歡迎下個週末能夠遇見到大家。那個雖然端午節過了，也祝大家端午安康。謝謝大家。

---

## 📖 延伸閱讀

- [上線三天就被「政府下架」：Fable 5 事件的真正重點不是 Fable 5](https://ai-coding.wiselychen.com/fable-5-takedown-ai-export-control-precedent/)
- [Fable 5 發布 24 小時就被扒穿：當對齊技術撞上結構化攻擊](https://ai-coding.wiselychen.com/fable-5-jailbreak-24hr-alignment-geopolitics/)
- [Fable 5 後面不是模型，是一個 Harness 系統](https://ai-coding.wiselychen.com/claude-fable-5-system-prompt-leak-harness-architecture-exposed/)
- [Fable 5 把 Harness 吃進去了——SWE-bench 95% 的背後](https://ai-coding.wiselychen.com/fable-5-harness-internalization-orchestrator-model-routing/)
- [GLM-5.2：華為晶片訓練的 744B 開源模型，1M Context 直接挑戰 Claude Code](https://ai-coding.wiselychen.com/glm-5-2-zhipu-1m-context-agentic-coding-huawei-ascend/)
- [智譜 GLM-5.2：1M Context、全華為晶片訓練、MIT 開源](https://ai-coding.wiselychen.com/glm-5-2-zhipu-1m-context-no-benchmark-open-source/)
- [AI Agent 安全性：遊戲規則已經改變](https://ai-coding.wiselychen.com/ai-agent-security-you-xi-gui-ze-yi-jing-gai-bian/)
- [AI Coding On-Prem 的三條路](https://ai-coding.wiselychen.com/ai-coding-on-prem-three-paths/)
