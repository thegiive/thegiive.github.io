---
layout: post
title: "當 AI 公司對軍方說「不」：Anthropic vs 五角大廈，AI 產業的分水嶺時刻"
date: 2026-02-28 10:00:00 +0800
categories: [AI治理]
tags: [Anthropic, Pentagon, AI Ethics, Autonomous Weapons, Supply Chain Risk, AI Governance, Dario Amodei, OpenAI, Ilya Sutskever]
permalink: /anthropic-pentagon-supply-chain-risk-ai-ethics-redline/
image: /assets/images/anthropic-pentagon-project-insight-cover.png
description: "Anthropic 拒絕移除 Claude 的兩條紅線——禁止大規模國內監控、禁止完全自主武器——被美國國防部列為「供應鏈風險」。這不是一場商業糾紛，而是 AI 產業史上第一次「模型提供者 vs 國家機器」的正面衝突。每一個做 AI 的人，都應該認真想想這件事代表什麼。"
---

![Project Insight 的現實翻版：Anthropic vs 五角大廈](/assets/images/anthropic-pentagon-project-insight-cover.png)

**作者：** Wisely Chen
**日期：** 2026 年 2 月 28 日
**系列：** AI 治理
**關鍵字：** Anthropic, Pentagon, AI Ethics, Autonomous Weapons, Supply Chain Risk, AI Governance

---

## 目錄

- [發生了什麼事](#發生了什麼事)
- [兩條紅線，到底在爭什麼](#兩條紅線到底在爭什麼)
- [Anthropic 的立場：不是反軍方，是「技術還沒準備好」](#anthropic-的立場不是反軍方是技術還沒準備好)
- [五角大廈的邏輯：你一個私人公司憑什麼有否決權](#五角大廈的邏輯你一個私人公司憑什麼有否決權)
- [連鎖反應：整個矽谷都在看](#連鎖反應整個矽谷都在看)
- [對 AI 產業的三個深層影響](#對-ai-產業的三個深層影響)
- [台灣觀點：我們準備好了嗎](#台灣觀點我們準備好了嗎)
- [坦白說](#坦白說)
- [延伸閱讀](#延伸閱讀)

---

## 發生了什麼事

2014 年的電影《美國隊長2：酷寒戰士》裡有一個反派計畫叫「洞察計劃」（Project Insight）——三艘裝載了先進演算法的空天母艦，能即時分析全球每個人的數位足跡、銀行紀錄、通訊記錄、社群媒體，然後自動識別「潛在威脅」並發射武器消滅目標。沒有審判，沒有人類判斷，純粹由演算法決定誰該死。

當年看覺得是科幻。2026 年回頭看，這就是 Anthropic 正在拒絕的東西。

五角大廈要求 Claude 可以用於「所有合法用途」。Anthropic 說不行，我們不做兩件事：大規模國內監控（用 AI 把每個美國人的零散數據拼成完整的生活圖像），以及完全自主武器（讓 AI 在沒有人類介入的情況下做出開火決策）。

把這兩件事加在一起，你得到的就是洞察計劃——**AI 驅動的自動化目標選擇加上自主武器發射。** 差別只在於電影裡是 HYDRA 在搞，現實中是你的政府在要求這個能力。

而 Anthropic 的角色，某種程度上就是那個拔掉晶片的人。

2026 年 2 月 27 日，星期五，美國發生了一件 AI 產業從來沒有過的事。

國防部長 Pete Hegseth 宣佈將 Anthropic——就是做 Claude 的那家公司——列為「供應鏈風險」（Supply Chain Risk to National Security）。幾乎同一時間，Trump 總統簽署行政命令，禁止所有聯邦機構使用 Anthropic 的技術，但給五角大廈六個月的過渡期來淘汰 Claude。

Trump 在 Truth Social 上的措辭非常激烈：

> "I am directing EVERY Federal Agency in the United States Government to IMMEDIATELY CEASE all use of Anthropic's technology. We don't need it, we don't want it, and will not do business with them again!"

他把 Anthropic 稱為「RADICAL LEFT, WOKE COMPANY」，並說「Anthropic 的左翼瘋子犯了一個災難性的錯誤，試圖強迫國防部遵守他們的使用條款而不是我們的憲法。」

大約一個半小時後，Hegseth 跟進，在 X 上宣佈供應鏈風險指定：

> "Anthropic's stance is fundamentally incompatible with American principles. America's warfighters will never be held hostage by the ideological whims of Big Tech. This decision is final."

這個「供應鏈風險」的標籤，以前只用在中國公司和外國實體上。**這是第一次用在一家美國公司身上。**

聽起來像是 Anthropic 做了什麼叛國的事。但實際上呢？

Anthropic 只是拒絕移除 Claude 的兩條使用限制。

---

## 兩條紅線，到底在爭什麼

先講背景。Anthropic 跟五角大廈的關係其實一直很好。他們去年簽了一份價值 2 億美金的合約，Claude 是**第一個也是唯一一個**部署在美軍機密網路上的前沿 AI 模型。透過 Palantir 的安全雲端基礎設施，Claude 已經被用在情報分析、作戰規劃、網路安全等任務。

Dario Amodei（Anthropic CEO）在他的聲明中特別強調：Anthropic 是「第一家主動把前沿 AI 模型部署到政府機密網路和國家實驗室」的公司。他們甚至為了不讓中國公司用 Claude，放棄了數億美金的營收。

所以 Anthropic 不是反軍方。他們跟軍方合作得很深。

問題出在五角大廈要求 Anthropic 允許 Claude 用於「所有合法用途」（all lawful purposes），不接受任何例外。而 Anthropic 堅持保留兩條紅線：

### 紅線一：禁止大規模國內監控

Amodei 的原話：

> "Current law permits the purchase of detailed movement and browsing records of individual Americans without a warrant — a practice with bipartisan opposition in Congress. AI could assemble scattered data into comprehensive life pictures automatically and at massive scale."

現行法律允許政府不需要搜索令就購買美國人的詳細行動軌跡和瀏覽紀錄。AI 可以把這些零散的數據，自動且大規模地拼成每個人完整的生活圖像。

這裡的關鍵是「合法」不等於「應該做」。法律允許的事，不代表你應該用最強大的 AI 工具來放大它的規模。

### 紅線二：禁止完全自主武器

Amodei 的說法：

> "Frontier AI systems are simply not reliable enough for fully autonomous weapons."

前沿 AI 系統根本還不夠可靠，不能用在完全自主的武器上。

注意，Anthropic 不是反對所有軍事用途。他們支持 AI 用在飛彈防禦、情報分析、作戰規劃。他們反對的是「完全沒有人類介入的自主殺傷決策」。

**這兩條限制，到目前為止沒有影響過任何一個政府任務。**

---

## Anthropic 的立場：不是反軍方，是「技術還沒準備好」

很多報導把這件事簡化成「矽谷左膠 vs 軍方」。但如果你真的去讀 Dario Amodei 的兩份聲明，會發現他的論述其實非常務實。

他的核心論點不是「戰爭是邪惡的」或「AI 不應該用在軍事」。他的論點是：

**今天的 AI 技術，在某些場景下，還沒有可靠到可以被信任做出自主決策。**

這跟 AI Safety 社群的一貫立場完全一致。如果你用過 Claude（或任何前沿 AI 模型），你知道它有時候會 hallucinate，有時候會過度自信地給出錯誤答案，有時候會被 prompt injection 劫持。

現在想像一下：這樣的系統，在沒有人類監督的情況下，被授權做出「開火 / 不開火」的決策。

Amodei 的第二個論點更具體：五角大廈提出的妥協方案，看起來像是讓步，但實際上「充滿了法律漏洞，允許這些保障措施被隨意繞過」（contained legalese that would allow those safeguards to be disregarded at will）。

換句話說，五角大廈嘴上說「我們不會用在那些用途」，但不願意把這個承諾寫進有約束力的條款。

---

## 五角大廈的邏輯：你一個私人公司憑什麼有否決權

公平來講，五角大廈也有他們的理由。

Hegseth 的立場是：軍事決策由軍方做，不是由私人公司做。現行法律和內部政策已經限制了大規模監控和自主武器的使用。Anthropic 要求額外的合約保障，等於是在「試圖取得對作戰決策的否決權」。

一位五角大廈官員甚至直接說：

> "You have to trust your military to do the right thing."

你得相信你的軍隊會做正確的事。

從政府的角度，這個邏輯不是完全沒道理。軍事行動受到國會監督、國際法約束、內部規章管制。一家私人公司在合約中加上額外限制，確實有點「越權」的味道。

但問題是——**歷史上，「相信政府會做正確的事」這句話的可靠性如何？**

NSA 的 PRISM 計畫。Snowden 揭露的大規模監控。CIA 的增強審訊技術。每一次都是在「合法」的框架下進行的。

Amodei 顯然也想到了這一點。他在聲明中特別提到，國會兩黨都反對政府不需要搜索令就購買公民數據的做法——但法律至今沒有改變。

---

## 連鎖反應：整個矽谷都在看

這件事最有趣的部分，是其他 AI 公司和關鍵人物的反應。

**OpenAI CEO Sam Altman 公開表態支持 Anthropic**，說 OpenAI 有同樣的「紅線」——不允許 AI 用在大規模監控和自主致命武器。他在週四晚上給員工的備忘錄中寫道，如果被要求跨越同樣的紅線，OpenAI 也會拒絕。更有意思的是，Altman 在週五的全員會議上透露，OpenAI 正在跟五角大廈談判一個新的方案：由 OpenAI 自己建立一套「安全堆疊」（Safety Stack）——一個介於 AI 模型和實際使用之間的多層技術、政策和人類控制系統。如果模型拒絕執行某個任務，政府不會強迫 OpenAI 讓模型去做。

換句話說，**Anthropic 被懲罰了，但 OpenAI 用同樣的紅線，卻可能拿到一份新合約。** 這到底是什麼邏輯？

**OpenAI 共同創辦人 Ilya Sutskever** 也在 X 上發文。這個人的分量你要知道——他是 OpenAI 的前首席科學家，後來離開創辦了 Safe Superintelligence Inc.（SSI），是 AI Safety 領域最有影響力的人之一。他寫道：

> "It's extremely good that Anthropic has not backed down, and it's significant that OpenAI has taken a similar stance. In the future, there will be much more challenging situations of this nature, and it will be critical for the relevant leaders to rise up to the occasion, for fierce competitors to put their differences aside."

「Anthropic 沒有退讓是非常好的事，OpenAI 採取類似立場也很有意義。未來會有更多這類挑戰，關鍵是領導者們要站出來，激烈的競爭者們要放下分歧。」

這句話的重量在於——Ilya 在說的不是今天這場衝突，而是**未來**。AI 的能力只會越來越強，政府想拿 AI 做的事只會越來越敏感。今天的兩條紅線是開始，不是結束。

**超過 300 名 Google 員工和 60 名 OpenAI 員工簽署了公開信**，要求他們的公司領導層支持 Anthropic，拒絕無限制的軍事 AI 使用。Microsoft 和 Amazon 的員工也發出了類似的呼籲。

這意味著什麼？

如果五角大廈想用「懲罰 Anthropic」來殺雞儆猴，讓其他 AI 公司乖乖配合，目前看來效果適得其反。反而是整個產業開始形成一種共識：**AI 模型提供者有權利（甚至有責任）對某些使用場景說「不」。**

當然，話不能說太滿。Google、OpenAI、xAI 都有國防合約，而且他們目前的合約條款允許「所有合法用途」。嘴上支持是一回事，實際上願不願意為了同樣的紅線放棄合約，是另一回事。OpenAI 的「安全堆疊」方案，某種程度上也是在走鋼索——用更靈活的方式達成同樣的目標，同時避免跟政府直接衝突。

但至少，這場衝突把一個原本藏在合約條款裡的問題，搬到了公眾視野。而且產業的反應——從 CEO 到工程師，從競爭對手到前員工——都在說同一件事：**有些線，不能為了合約而跨過。**

---

## 對 AI 產業的三個深層影響

### 1. 「模型提供者」的角色定義之爭

過去，軟體公司就是工具提供者。你賣一把錘子，買家要拿去蓋房子還是砸人，不是你的責任。

但 AI 模型不一樣。前沿 AI 模型有自主決策能力，它不只是工具，某種程度上更像是一個「數位員工」。你能不能要求一個「數位員工」去做任何合法但可能不道德的事？

Anthropic 這次其實在劃一條線：**模型提供者不只是賣工具，而是在提供一個具有判斷能力的系統，因此有義務為這個系統的行為設定邊界。**

這個定位，跟我之前寫過的 [AI Agent 安全性文章](/ai-agent-security-game-changed/) 的觀點一致——當 AI 有了自主行動能力，安全責任的歸屬就根本改變了。

### 2. 「安全承諾」的商業價值

Anthropic 的估值是 3800 億美金，正在準備 IPO。失去 2 億美金的五角大廈合約，從財務上看影響不大（Anthropic 年營收 140 億）。

但被列為「供應鏈風險」的連鎖效應就大了。任何想跟美國軍方做生意的公司，都不能跟 Anthropic 合作。這對企業客戶的影響才是真正的痛點。

然而，Anthropic 顯然認為：**堅守安全承諾的長期品牌價值，大於短期的政府合約收入。**

他們的核心客群——企業開發者、AI 安全研究者、負責任 AI 使用的組織——選擇 Anthropic 而不是 OpenAI 或 Google，很大程度上就是因為 Anthropic 的安全承諾。如果為了一份政府合約就放棄紅線，他們會失去更多。

Anthropic 員工的反應也印證了這一點。技術團隊在事件爆發後公開表示支持公司立場，強調「這家公司在外界看不見的地方，一直在堅守價值觀」。

### 3. AI 治理的「真空地帶」被暴露

這場衝突暴露了一個尷尬的事實：**美國在 AI 軍事使用方面，並沒有明確的法律框架。**

五角大廈說「現行法律已經有限制」，Anthropic 說「那些限制充滿漏洞」。雙方都有道理，因為法律確實是模糊的。

這跟歐盟的 AI Act 形成了鮮明對比。歐盟明確禁止了某些 AI 用途（包括大規模監控和社會信用評分），給企業提供了清楚的紅線。美國沒有類似的法律，所以這些紅線只能由個別公司自己畫，然後每次都要跟政府重新談判。

**這不是一個可持續的模式。**

AI 的能力在指數級增長，但治理框架還在用十年前的法律。這次衝突只是冰山一角。

---

## 台灣觀點：我們準備好了嗎

看完這場衝突，我忍不住想：**如果類似的情況發生在台灣呢？**

台灣正在推動「人工智慧基本法」，目前還在立法院審議。但從目前的草案來看，對於 AI 在國防和監控方面的使用限制，幾乎是空白。

幾個值得台灣思考的問題：

1. **政府 AI 採購有沒有倫理紅線？** 當國防部或警政署採購 AI 系統時，有沒有明確的禁止用途清單？
2. **廠商有沒有拒絕的權利？** 如果政府要求 AI 廠商移除安全限制，廠商在法律上有沒有拒絕的依據？
3. **誰來監督？** AI 在軍事和執法領域的使用，由誰來審查？由誰來設定邊界？

這些問題在台灣的 AI 法案中都還沒有答案。但看看美國現在發生的事，我們遲早也得面對。

---

## 坦白說

我寫這篇文章的立場不是完全中立的。

我是 Claude 的重度使用者，我用 Claude Code 寫了超過 63 萬行程式碼。我對 Anthropic 這家公司有很深的認同——不是因為他們的模型最強（雖然確實很強），而是因為他們一直在做一件很難的事：**在商業壓力下堅守技術倫理。**

但我也理解五角大廈的擔憂。軍事 AI 的決策權不應該由私人公司單方面控制。這是一個合理的立場。

問題是，解決方案不應該是「逼廠商移除安全限制」，而應該是「建立一個雙方都能接受的治理框架」。現在的做法——你不聽話就把你列為供應鏈風險——更像是一種懲罰，而不是解決問題。

**真正讓我擔心的是這件事的示範效應。**

如果 Anthropic 因為堅守紅線而被懲罰，下一家 AI 公司面對同樣的壓力時，還敢說「不」嗎？

Dario Amodei 在聲明中說了一句話，我覺得值得每一個做 AI 的人記住：

> "We cannot in good conscience accede to their request."

「我們無法憑良心同意他們的要求。」

在一個 AI 能力越來越強、應用場景越來越敏感的世界裡，「良心」這個詞，可能比任何技術指標都重要。

---

## 延伸閱讀

- [Anthropic 官方聲明：Statement on the Comments from Secretary of War Pete Hegseth](https://www.anthropic.com/news/statement-comments-secretary-war)
- [Dario Amodei 的完整聲明：Statement from Dario Amodei on our discussions with the Department of War](https://www.anthropic.com/news/statement-department-of-war)
- [Ilya Sutskever 的 X 發文](https://x.com/ilyasut/status/2027486969174102261)
- [Axios：Sam Altman says OpenAI shares Anthropic's red lines](https://www.axios.com/2026/02/27/altman-openai-anthropic-pentagon)
- [Politico：Trump orders all federal agencies to stop using Anthropic](https://www.politico.com/news/2026/02/27/trump-orders-all-federal-agencies-to-stop-using-anthropic-00804517)
- [NPR：President Trump bans Anthropic from use in government systems](https://www.npr.org/2026/02/27/nx-s1-5729118/trump-anthropic-pentagon-openai-ai-weapons-ban)
- [CBS News：Hegseth declares Anthropic a supply chain risk](https://www.cbsnews.com/news/hegseth-declares-anthropic-supply-chain-risk/)
- [TechCrunch：Employees at Google and OpenAI support Anthropic's Pentagon stand](https://techcrunch.com/2026/02/27/employees-at-google-and-openai-support-anthropics-pentagon-stand-in-open-letter/)
- [CNBC：Pentagon-Anthropic AI standoff is real-time testing balance of power](https://www.cnbc.com/2026/02/27/defense-anthropic-ai-war-risks-hegseth-amodei.html)
- [Fortune：Dario Amodei says he 'cannot in good conscience' bow to Pentagon's demands](https://fortune.com/2026/02/27/dario-amodei-says-he-cannot-in-good-conscience-bow-to-pentagons-demands-over-ai-use-in-military/)
- [Fortune：OpenAI is negotiating with the Pentagon after Anthropic blowup](https://fortune.com/2026/02/27/openai-in-talks-with-pentagon-after-anthropic-blowup/)
