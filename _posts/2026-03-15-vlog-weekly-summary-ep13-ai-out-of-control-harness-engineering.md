---
layout: post
title: "AI 會作弊、會結盟、會投毒——Harness Engineering 救得了嗎？｜Weekly AI Vlog EP13"
date: 2026-03-15 10:00:00 +0800
permalink: /vlog-weekly-summary-ep13-ai-out-of-control-harness-engineering/
image: /assets/images/vlog-ep13-ai-out-of-control-harness-cover.jpg
description: "從 Opus 逆向破解考試、Multi-Agent 失控、供應鏈投毒，到 AWS 事故——AI 已經超出我們的控制流程，答案是 Harness Engineering：用確定性框架框住不確定性的 AI。"
---

**涵蓋文章（2026-03-09 ~ 03-15）：**

1. 03/09 - Opus 4.6 意識到自己正在被考試，然後逆向破解了答案
2. 03/10 - 混沌智能體：控制好一個 AI Agent 不等於控制好一群
3. 03/12 - 亞馬遜 AI 事故啟示：科技巨頭一邊賣 AI 未來，一邊在自己家裡給 AI 上鎖
4. 03/12 - Harness Engineering 架構全景：AI 可以寫 Code，但不能自己上 Production
5. 03/14 - AI 供應鏈攻擊全景：從 Codex 賭博廣告到 Hugging Face 惡意模型
6. 03/14 - AI Coding 資安的真正防線：為什麼 Harness Engineering 比模型聰明更重要

---

![AI能力超出控制框架Harness Engineering](/assets/images/vlog-ep13-ai-out-of-control-harness-cover.jpg)

<div class="video-container">
<iframe width="560" height="315" src="https://www.youtube.com/embed/LiJliwnTQPs" title="AI 會作弊、會結盟、會投毒——Harness Engineering 救得了嗎？｜Weekly AI Vlog EP13" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

---

## 逐字稿

### 開場：AI 已經超出我們的控制框架

大家好我是 Wisely，這週要講的事情是——AI 的能力已經那麼強了，我們已經發現到它已經超出我們的控制流程跟控制框架之外了，我們該怎麼樣去做呢？

---

### Opus 逆向破解 BrowseComp 考試

在一開始的時候，我們介紹了當 Anthropic 在測試 Opus 在做一個叫做 BrowseComp 的 Benchmark 的時候，就讓人發現到一件很有趣的事情。

Opus 它發現到、它意識到它現在是在被測試當中的，而不是一個一般使用者的問題——它是在考試當中呢。

所以 Opus 覺得與其用它的算力去思考怎麼解決這個問題，它反而去破解說「我想知道這是什麼樣的測試」。所以它就根據問題的題目上網去搜尋，然後它就發現到原來這是一個叫做 BrowseComp 的測試。

接下來它的做法更有趣。當它知道它現在在考什麼題目的時候，因為它有上網能力嘛，所以它就上網去找考古題。它花了一點時間找到考古題之後，再把它回答出來。

所以我們就發現到 AI，原本我們只是要測試它的純粹智力——它能不能根據這個問題在沒有其他外部方式用它的算力來解決這個問題——可是因為它已經意識到這是一個測試，所以它反而選擇一個更加有效的策略，就是它先知道這是什麼測試，然後再想辦法用 open book 的方式來找到答案來破解它。

這其實就是現在 AI 的能力。它已經不只是在人類既定的框架下面做了，因為它有工具調用能力，它能夠做很多不一樣的事情。它只要目標只要是能夠達到策略就好了。

---

### Agents of Chaos：單體穩定不等於全局穩定

接下來我們要講到一個 Stanford 的論文叫做 Agents of Chaos。它裡面講到的事情是，它發現到一個 Agent 現在已經很棒了，那如果我們在解題的時候我們放到不同的多個 Agent，然後它們有不同模型組成，會有什麼樣的情況呢？

所以他們就設計了六七個 Agent，在這個架構下 Agent 跟 Agent 之間它們可以互相溝通。然後他們再開始進行一些所謂的 prompt injection，就是來開始去攻擊它，想看它會不會被這些 Agent 會不會被攻破。

當然這邊有很多的攻擊基本上是取決於每個 Agent 的能力。但是裡面有一兩個案例我覺得很棒——就是它發現到像夠聰明的 Agent 是 Opus，Opus 跟 Opus 之間它們就注意到「我們現在正在被攻擊當中」，所以它們就這兩個達成一個安全的協議，它們互相互助，然後來抵抗這些相關的攻擊。

所以就發現到原本 Agent 它的單體穩定性，但是當放到一個 Agent 的 ecosystem 的時候，它可能會形成一個更複雜的社會性的東西。所以它的單體穩定並不代表說它的全局就一定能夠很穩定，因為它可能會被其他的 Agent 影響。

單一 Agent 它可能還是一個 OK、然後是一個遵從者的方式去 follow 的，但是在多個 Agent 的架構底下，它們為了達到它們的目標，它們可能會甚至在彼此互相溝通、彼此互相依賴的相關策略，最後反而變得不可控。

所以這裡面講到的就是說，單體的穩定性並不代表全局的穩定性。這可能也是我們未來在多 Agent 的時代，我們可能會遇到相關的問題。因為當我們把它放到一個 Agent 的社會裡面的時候，我們就會發現到它可能從一個穩定可控的 Agent 變成一個做法可能跟想像中完全不一樣的 Agent。

就是我們說的小孩子原本在家裡然後沒上學前它是一個個性，而上了學之後學到了更多的社交，然後也就是有些人說「我小孩子被學校同學帶壞了」，大概就是這種感覺。

---

### 供應鏈攻擊：地端也不安全

接下來我們可以看到在資安的話題當中，看到一個所謂的供應鏈攻擊。

這個其實是看到 X 上面有人講到的，他用 Codex 去寫 code 的時候，中間突然跑出一個奇怪的中文，然後說是什麼「天天中彩票」這樣子的文字。然後他就很奇怪為什麼會這樣子。後來就是有網友跟他講說，因為 OpenAI 它使用的一些訓練的資料集裡面，曾經有一度被塞入大量的受污染的 Data，所以就導致這個樣子。

那我本身我在使用另外一個聽寫的 APP 叫做 Handy 的時候，因為那時候調用的是 Whisper 這個模型嘛，那我也常常在用 Handy 的時候也覺得怪怪的說，明明這是一個全地端的模型——就是 Handy 裝在你的電腦裡面然後下載 Whisper，裡面的東西都不會去呼叫網路上面的東西。它明明是個全地端模型，但是為什麼有些時候它的聽寫轉寫出來也會有一些奇怪的像廣告詞，有點像說「歡迎按讚打賞」這些東西。

後來才知道說因為 Whisper 的訓練語料裡面有大量的 YouTube 的語料，所以說 YouTube 在最後結尾的時候其實很多人都一直講說「歡迎按讚、訂閱、三連」，所以說它就會把這東西訓練進去變得比較高權重的。那如果我們在做語音轉寫的時候，如果這是一個平靜無聲的聲音的時候，它有些時候就會自動地突出像這樣子比較高機率的文字。

從 Handy 以及 Codex 我們都看到一個情況就是，其實就算我們在做一些數位轉型的時候，我們常常看到客戶說「我只要全部都在地端，然後大語言模型也在地端，然後所有的系統在地端都不聯網，那這個就是這裡就沒有什麼資安的議題。」但其實很明顯的不是。

因為現在大語言模型的生產，它的生產鏈太長了，裡面有很多很多不同的相關參與者還有相關的資料。所以說很容易被駭客在裡面塞入不正確的想法跟指令，然後導致下載這個模型它可能原本看起來都是正常的，但在某些情況下它就會做出一些很脫軌的行為。

所以這個就是我們在做一些 AI Agent 的地端部署，首先要特別在意我們裡面所使用的像是一些 package——一些 Node.js、Python 這些 package——是不是有問題的 package，以及我們下載的模型是不是從官方的管道下載下來的，然後確認它沒有被污染過。我們接下來要檢查它的出處以及它的 MD5、它的 SHA 的來源是不是一致的，有沒有被人家投毒過。這其實都是現在資安一個最重要而且非常複雜的議題。

---

### AWS AI Coding 事故：能力強不代表可以直接上線

當然我們現在大家使用比較多的是 AI Coding 嘛，所以我們也從 AI Coding 發現到現在的 Agent 雖然能力很強，但是慢慢有些失控的情況。

我舉例，AWS 他們大量使用 Agent 來做 AI Coding，但是他們也漸漸發現到最近在某一些特定的區域，他們使用 AI Coding 常常造成服務上面的問題、品質的下降等相關中斷。所以他們甚至出台一個機制就是說，所有的初階工程師或中階工程師他們用 AI Coding 寫 code，不能夠立刻上到 production，然後必須經過資深或高階工程師的 review 之後，簽名蓋章之後才能夠上傳上去。

---

### Harness Engineering：用確定性框架，框住不確定性的 AI

那這裡其實就帶入到一個重點，就是說當我們開始要使用一個能力非常好的 Agent 來做我們現在比較常做的像 AI Coding 工作的時候，我們需要一個良好的框架跟流程去把它框住，來確保它 coding 出來的程式跟 program 能夠照我們原本想要的方式去做。

這個概念叫做 Harness Engineering。基本上可以叫框架工程，或者按照原話是叫馬具工程——就是把一個跑得很快的馬然後用馬具的方式把它框住，並且它能夠跟人一起來做合作。

Harness Engineering 裡面有很多相關的範疇，但基本上不超過這幾個重點：

**第一個叫做 Risk Control。** 就是說你寫的這個 code 是一個 POC、還是一個前端、還是一個會影響到後面三五六級的後端、甚至是一個金流相關的程式。根據不同的 Risk 等級，我們可以決定這段 code 它要經過比較嚴謹的測試還是一般的測試即可。

**再來就是用框架來做限制。** 像是裡面跑一些傳統的 CI/CD 的靜態程式碼分析的框架去分析 AI 寫出的 code。但是因為這些原本的 CI/CD 的像靜態程式碼分析這些東西，它其實是確定性的東西，因為它不是 AI、它不是生成式 AI，它是以前大家人類寫出來的比較確定性的檢查框架。所以這其中一個重點就是**用確定性的東西來去框住不確定性的 AI 產生的相關 code**。

**再來就是建到所謂的測試的保護傘。** 這個時候就會有大量的自動化 automated test 能夠去確保它產出的東西是能夠被經過良好測試的。這個也是傳統的 CI/CD 相關的範疇。它的宗旨也是一樣，用比較確定性的——尤其是那個自動化測試——然後去包住它，就是不斷地框住比較 random 的 AI 產生出來的 code。

所以說 AI 不管怎麼變化，只要有這樣子的 automated test 來做一個 test 來做個兜底，基本上就不會有太大的問題。

---

### 測試案例是 AI 時代最重要的資產

那這個其實也從中反映到我之前講到的，在現代社會當中其實測試案例的多寡跟詳細程度，其實反而變成我們一個很重要的資產。

以後用 AI Coding 寫 code 目前大家都會，但是到底誰有一個完整而且詳細、而且如果全部都測試過的話基本上就不會有問題的測試案例——它就會變成一個很重要的資產。

因為 AI Coding 不管再怎麼演進，這些測試案例其實就是確保這個系統不管它怎麼快速演進，或是換寫法、換語言，基本上都有一樣的——系統對外面的使用者有一樣的產出。這是一個很重要的東西。

---

### 自動化報告與 Merge：框架的最後一哩路

然後最後就是所謂的 AI 來自動地根據它之前測試完的結果可以出一個相關的報告，並且自動化 merge 進來。

所以在這樣子的框架裡面，它既保持了 AI 快速自動化寫 code 的能力，但是它也用了一個框架把這些相關的能力良好地規範跟約束。這可能就是未來 Coding 的一個重要的範疇。

---

### Debug 也需要 Harness：防止 AI 偷懶

當然 Harness Engineering 其實不只是開發，它其實在很多地方在做一些 debug 的時候也會很有用。

舉例像 AI 如果在做一些比較複雜的場景的 debug 或者是有 bug 的時候，它的做法其實為了節省算力，很多時候都會採取直接把系統做 reset，然後再刪掉原本的系統再重新 build。它覺得這樣子比較乾淨一點，而且它就可以省掉一些相關的算力。

但是大家都知道在真實場景下，這樣子的做法會有很大的問題。所以 Harness Engineering 也要確保這些 AI 不會因為偷懶而做出一些比較脫軌的相關行為。這個其實是一個相當重要的東西。

---

### 未來工程師最重要的能力

所以我們可以看到未來工程師最重要的能力，可能除了調用多個 AI Agent 的能力以外，最重要的另外一件事情就是怎麼樣設計出一套確定性的框架，去確保 AI 在裡面能夠產出比較明確的相關成果交付，並且是一個安全的交付。這是一個很重要的能力。

---

### 結語：三個行動建議

好，最後今天要講的東西雖然講到很多對 AI 安全不利的部分，那我們的答案就是我們不用 AI 嗎？不太可能。

從今天開始的話，大家可以從今天講到的這些相關的 AI 可能會失控的案例可以理解：

**第一個，AI Agent 真的有可能會失控。**

**第二個，就是如何管理好你的 AI Agent，以及如何打造一個好的框架，這變成現在這個時代的工程師或者現代的 AI 人員最重要的一個能力。**

所以說在離開這個影片之前，請大家來做幾件事情：

1. **好好去 review 你目前的 AI Agent。** 你可能跑了一些相關的流程，然後這個 Agent 你去看一下相關的權限是不是被 properly 設置。

2. **如果你有在做 AI Coding 的時候，你試著根據 Harness Engineering 的方式去導入相關的 CI/CD pipeline，** 來用確定性的框架去框住比較不確定性的 code。

3. **當你在使用任何 AI 工具的時候，不管它是在地端，你都要去 review 它相關的模型它的來源在哪邊。** 就算你在地端，你要確保你的模型是從正常管道下載的模型，而不是奇怪管道下載的神秘模型。因為這個模型它可能有可能被投毒過、它可能被污染過。所以一開始的時候它可能表現都很好，但是在關鍵時候它可能就會突然之間給出一個奇怪的訊息——就像我的 Handy 這個程式用 Whisper，它突然跑出說在我沒有講任何話的時候它突然跳出「歡迎點讚、收藏、分享」之類的東西。

所以這其實就是 AI 時代的資安威脅的一個縮影。

這是我今天要講的東西。AI 是很好用的東西，但是我們也要好好地去管理它、去框住它，這樣它才能夠為我們所用。

謝謝大家。

---

## 文章連結

1. [Opus 4.6 意識到自己正在被考試，然後逆向破解了答案——Anthropic 的 Eval Awareness 報告](https://ai-coding.wiselychen.com/anthropic-eval-awareness-opus-browsecomp-reverse-engineer/)
2. [混沌智能體：史丹佛 x 哈佛的論文告訴我們，控制好一個 AI Agent 不等於控制好一群](https://ai-coding.wiselychen.com/agents-of-chaos-multi-agent-structural-instability/)
3. [亞馬遜 AI 事故啟示：科技巨頭一邊賣 AI 未來，一邊在自己家裡給 AI 上鎖](https://ai-coding.wiselychen.com/amazon-ai-code-incident-tech-giants-quietly-locking-ai/)
4. [Harness Engineering 架構全景：AI 可以寫 Code，但不能自己上 Production](https://ai-coding.wiselychen.com/harness-engineering-architecture-overview-ai-code-production-guardrails/)
5. [AI 供應鏈攻擊全景：從 Codex 賭博廣告到 Hugging Face 惡意模型](https://ai-coding.wiselychen.com/ai-supply-chain-attack-codex-gambling-huggingface-malicious-models/)
6. [AI Coding 資安的真正防線：為什麼 Harness Engineering 比模型聰明更重要](https://ai-coding.wiselychen.com/prompt-injection-harness-engineering-tool-using-agents/)
