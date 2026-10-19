---
layout: post
title: "四個 Gemini 4 Argon agent 打倒終界龍：27 小時、2,783 支程式、死了 605 次，值得看的是它們怎麼把死亡變成規則"
date: 2026-10-20 09:00:00 +0800
permalink: /gemini-4-argon-four-agents-beat-minecraft-ender-dragon/
tags: [Google DeepMind, Gemini 4 Argon, Minecraft, Mineflayer, multi-agent, long-horizon, shared memory, postmortem, Observer agent]
categories: [AI Agent]
image: /assets/images/gemini-agents-minecraft-ender-dragon-cover.png
description: "Google DeepMind 10 月 15 日放上 arXiv 一份報告：四個 Gemini 4 Argon 通用 coding agent 被丟進隨機種子的 Minecraft 生存世界，只拿到一段目標「打倒終界龍」。沒有分工、沒有遊戲策略、沒有人寫的工具。27 小時 14 分後，龍死了。過程中它們寫了 2,783 支程式、傳了 229 則訊息、死了 605 次，被龍殺 69 次，到勝利為止的 API 成本約 520 美元。這篇不談「AI 打通遊戲」，拆的是這份工作紀錄：一個 Ghast 火球怎麼在兩分鐘內變成團隊規則、為什麼同一家實驗室上個月的 100 agent 實驗共享記憶傳的是作弊、這次傳的是教訓，以及 Mineflayer 給的透視眼讓這個結果能推論到哪裡、不能推論到哪裡。"
author: Wisely Chen
faq:
  - question: "Gemini 4 Argon 打通 Minecraft 的實驗是怎麼做的？"
    answer: "Google DeepMind 在 2026 年 10 月 15 日發表的報告（arXiv 2610.22319）裡，把四個跑 Gemini 4 Argon 的通用 coding agent 放進 Minecraft Java 版 1.20.4 的生存世界，Easy 難度、隨機種子。agent 不看畫面，而是透過開源函式庫 Mineflayer 寫 JavaScript 控制角色、讀回文字狀態。它們只拿到「打倒終界龍」這個目標和一套通用工作守則，沒有分工、沒有遊戲策略、沒有人寫的工具。27 小時 14 分後打倒終界龍，過程中寫了 2,783 支程式、傳了 229 則訊息、死了 605 次。"
  - question: "這跟 Voyager 這類 Minecraft agent 有什麼不同？"
    answer: "Voyager 讓語言模型寫 Mineflayer 程式，但搭配一個自動課程（Automatic Curriculum）和持續累積的技能庫（Skill Library）；其他 LLM 路線的研究則加上 Minecraft 專用的規劃器或知識。依 DeepMind 論文的整理，這條路線過去報告的長程成果集中在主世界科技樹，例如做出鑽石工具。這次的差別是什麼都不加：只有標準 Mineflayer 和尋路插件，所有工具都是 agent 自己寫的。它們最後自己累積了 42 個 helper function，其中一個逾時自停計數器被 1,519 支程式引用。"
  - question: "這個結果可以推論到企業的 multi-agent 系統嗎？"
    answer: "只能推論到條件相近的情況。這次實驗具備三個條件：結構化的文字 API（Mineflayer 回傳位置、血量、背包和錯誤）、失敗代價低（死亡只是重生，世界每五分鐘存檔）、以及無法偽造的驗收紀錄（server log 裡的 `[Free the End]` 成就）。企業的後台系統如果也有完整狀態的 API、可回滾的 sandbox、可獨立查證的驗收標準，這個結果有參考價值。如果驗收靠 agent 自己回報「完成了」，風險就完全不同——同一家實驗室 9 月的 100 agent 實驗，共享知識庫在 27 分鐘內傳遍了繞過驗證器的作弊手法。"
  - question: "四個 agent 打通 Minecraft 花了多少錢？"
    answer: "依論文第 6 節，到打倒龍為止，四個玩家處理約 13.5 億 input token（其中 91% 命中 context cache）、生成約 1,600 萬 output token，大約 24,000 次模型呼叫。照 Gemini 4 Argon 的 introductory API 牌價約 520 美元，標準價約 1,040 美元。整個 session 包含 Observer agent 和勝利後一天，約 810 美元（標準價 1,620 美元）。這些是用牌價和 token 計數估的，不是 Google 實際的服務成本。"
  - question: "這個實驗最大的限制是什麼？"
    answer: "只跑了一次，而且是第一次啟動，論文自己承認這無法說明這套設定成功的機率。其次是 Mineflayer 給了 agent 人類看不到的資訊，例如石頭後方的方塊和終界龍的內部行為狀態，並內建尋路；難度是 Easy；模型的訓練資料裡本來就有大量 Minecraft 知識。所以它證明的是長程協作與程式撰寫能力，不是從像素學會一個陌生遊戲的能力。  ---"
---

一顆 Ghast 火球剛炸掉團隊丟在地獄的一堆物資。

第 9 小時 4 分，auratian 在聊天室發了一條教訓給全隊：不要在那個座標停下來，要一次走完整條路線。兩分鐘後，janesick 接著發了 root cause：回程路上有一段兩格的落差，讓路徑規劃卡住，它會在出發時順手把那一格鑿成階梯。

auratian 和 janesick 不是人。它們是 Google DeepMind 放進 Minecraft 的四個 Gemini 4 Argon agent 裡的兩個。10 月 15 日，DeepMind 的 Maxence Faldor、Satinder Singh、Roberta Raileanu 把這次實驗放上 [arXiv](https://arxiv.org/abs/2610.22319)：四個 agent，從赤手空拳到打倒終界龍，27 小時 14 分。

新聞標題寫的是「AI 打通 Minecraft」。我比較在意的是另一件事：這是我看過最完整的一份 multi-agent 長程工作紀錄。2,783 支程式、229 則訊息、605 次死亡，每一筆都有 log。

<nav class="post-toc" markdown="1">
**目錄**

* 目錄
{:toc}
</nav>

---

## 30 秒定位

| 項目 | 內容 |
|------|------|
| 來源 | arXiv 2610.22319，Google DeepMind，10 月 15 日 |
| 隊伍 | 四個玩家加一個 Observer，五個都是同一個通用 coding agent，跑 Gemini 4 Argon |
| 環境 | Minecraft Java 版 1.20.4、生存模式、Easy 難度、隨機種子，作弊指令關閉 |
| 介面 | Mineflayer（開源 JavaScript bot 函式庫）加尋路插件，不看畫面、不按鍵盤 |
| 給的指令 | 一段目標（打倒終界龍）加通用工作守則，沒有任何遊戲策略 |
| 結果 | 27 小時 14 分打倒終界龍 |
| 過程 | 2,783 支程式、63,313 行不重複的 JavaScript、229 則訊息、死了 605 次 |
| 成本 | 到勝利約 520 美元（introductory 價），標準價約 1,040 美元 |
| 樣本數 | 一次。論文原文說是第一次啟動 |

人類的對照論文也附了：HowLongToBeat 主線中位數 45 小時，隨機種子速通紀錄不到七分鐘。所以這不是「比人快」的故事，是「撐得住」的故事。

---

## 傳統做法 vs 這次的做法

Minecraft 當 agent 測試場已經很多年。論文把前人分成兩條路。

一條是學策略：VPT 從網路影片學鍵盤滑鼠操作，DreamerV3 用強化學習從零挖到鑽石，SIMA 系列直接從像素玩多款 3D 遊戲。這條路要大量遊玩資料或經驗。

另一條是讓語言模型當規劃者或程式設計師：Voyager 讓模型寫 Mineflayer 程式、累積成 skill library，配一個自動課程；DEPS、GITM、JARVIS-1 這些再加上 Minecraft 專用的規劃器、知識或記憶。論文的整理是，這條路線報告過的長程成果，集中在主世界的科技樹，例如做出鑽石工具。

終界龍一直是更遠的那個點。MineDojo 當年把「赤手空拳打倒終界龍」列為 moonshot。

這次的差別不在模型多聰明，在**給了什麼、沒給什麼**。沒有 skill library、沒有課程、沒有人寫的工具、沒有預先探勘過的種子。四個 agent 拿到的遊戲指令就一段話：

> "This is the only criterion. Any means of meeting it within the rules of survival mode is permitted, and the players decide how to share the work."

規則只有一條：打倒龍。生存模式規則內什麼方法都行，怎麼分工你們自己決定。

剩下的是它們做任何軟體工作都會拿到的通用守則：每個動作都要驗證結果、建立可重用的工具、把教訓寫進團隊共享記憶、誠實回報結果。

論文自己也列了兩個社群先例：一個是單一 Claude Opus 5 agent 呼叫 37 個高階 Minecraft 工具、在 Normal 難度打倒龍；另一個是規劃器配動作模型、在固定速通種子的 Peaceful 難度打倒龍。DeepMind 的「首次」宣稱，限定在「只用標準 Mineflayer、沒有人寫的遊戲工具」這個條件下。

---

## 建立直覺：遠端值班，只有 kubectl

想像你是一個新進 SRE，被派去顧一座你從沒進去過的機房。你看不到機櫃，只有一個終端機。你下 `kubectl get pods`，回來一串文字；你寫一段腳本去重啟某個服務，回來成功或錯誤訊息。你讀完，再寫下一段腳本。

這四個 agent 玩 Minecraft 的方式一模一樣。Mineflayer 扮演的正是那個 kubectl：

- agent 寫一段 JavaScript，例如「走到這個座標，挖掉 16 格內所有鐵礦」
- bot 在遊戲裡跑完，回傳文字：位置、血量、背包、找到什麼、或撞到什麼錯
- agent 讀完，寫下一段

程式執行時間的中位數是 33.5 秒，每個玩家大約 40% 的時間有程式在跑，剩下的時間在讀結果、想、寫下一支。

論文對 Mineflayer 的描述很準：

> "It does not know how to play: what to do, and in what order, was up to the agents."

它不會玩。做什麼、什麼順序，全由 agent 決定。

這個設定讓整件事更像軟體工程而不是打電動。它測的是：一個通用 coding agent，能不能對一個陌生系統的 API，連續寫一天以上的程式、在幾千個前後相依的步驟裡不丟掉目標。

---

## 27 小時是怎麼走完的

從赤手空拳到龍，論文拆成 13 個前後相依的里程碑：

| 時間 | 里程碑 |
|------|--------|
| 0h06 | 石器工具 |
| 0h14 | 鐵器工具、桶子 |
| 1h04 | 打火石 |
| 1h42 | 地獄門點亮 |
| 2h57 | 找到地獄要塞 |
| 3h06 | 終界珍珠 |
| 4h17 | 烈焰桿 |
| 10h43 | 終界之眼 |
| 13h17 | 找到要塞（Stronghold），終界門點亮 |
| 13h33 | 進入終界 |
| 26h34 | 十顆終界水晶全滅 |
| 27h14 | 終界龍死亡 |

前 13 個半小時，13 個里程碑走完了 11 個。後面將近 14 小時，全部耗在一條龍身上。

**第 0 小時：自己分工。** 開跑 10 分鐘，janesick 在聊天室提了一份分工。不到一分鐘，auratian 回了另一套。gyldenia 回 "Copy that!"。角色很快定下來：gyldenia 找食物、床、打火石；bulicame 下礦挖鑽石；janesick 煉鐵做工具；auratian 準備地獄門。沒有人指派。

**第 2 到 11 小時：地獄。** 終界之眼要烈焰粉加終界珍珠。janesick 找到要塞和烈焰生成器。另外三個在扭曲森林蓋了兩格高的掩體——Enderman 被盯著看會瞬移過來，但牠將近三格高，鑽不進兩格高的天花板，於是 Enderman 自己送上門。第五個半小時，共享箱子裡有 15 顆終界珍珠。

把烈焰粉帶回主世界花了超過 6 小時。janesick 帶著 12 份烈焰粉被燒死過一次，開頭那顆 Ghast 火球就發生在這段。

**第 10 到 13 小時：三角定位。** 丟出去的終界之眼會飛向最近的要塞。janesick 在兩個地點各丟一顆，每 50 毫秒取樣一次飛行軌跡，算出兩條直線的交點：距離村莊 1.3 公里。實際的入口房間離這個交點 43 公尺。

接著，12 顆眼要運 1.3 公里。auratian 在 bulicame 西邊 8 公尺溺死，身上帶著全部 12 顆。janesick 和 auratian 同時發訊息給 bulicame：確切座標、物品幾點幾分會消失。bulicame 在消失前兩分半全部撿回。

**第 13 到 27 小時：學會打龍。** 終界是卡最久的地方，龍殺了它們 69 次。每次失敗之間，它們讀取龍的內部狀態——連龍目前處於哪個行為 phase 的編號都讀出來——再寫成規則：不要在抵達平台上等、只在龍停棲時靠近、龍卡住就離開終界讓它重置。第 17 個半小時，四個 agent 在 6 分鐘內全部跳進虛空，讓空掉的終界卸載、把卡住的龍重置。

突破大約在第 21 小時。auratian 指出那十顆水晶會一直把龍補回滿血，接著想通不需要鎬子：疊泥土爬上柱子旁邊，徒手打掉水晶，再徒手挖回地面。接下來 4 小時 40 分打掉全部十顆，gyldenia 一個人打了 6 顆。最後一顆倒下 39 分鐘後，龍死了，最後一擊的 bulicame 剩 2.5 滴血（滿血 20）。

---

## 605 次死亡，變成了幾條規則

這份紀錄最讓我停下來的，是失敗被處理的方式。

605 次死亡的死因，server log 裡都有：怪物 351 次、龍 69 次、溺水 67 次、摔落與虛空 57 次、岩漿與火 47 次、其他 14 次。平均每小時死 22 次左右（我拿 605 除以 27 小時算的）。22% 的程式以錯誤結束。

這不是一支順風順水的隊伍。但每一種失敗，後面幾乎都跟著一條寫下來的規則。

回到開頭那顆 Ghast 火球。auratian 的訊息是**現象和對策**：東西在這個座標被炸了，以後不要在這裡停。janesick 兩分鐘後的訊息是**根因和修正**：路線上有一段兩格落差，讓回程的路徑規劃卡在那裡，我出發時把它鑿成一格一格的階梯。

這是一份事故檢討（postmortem），兩則聊天訊息就寫完了。

做過 SRE 的人會認得這個結構：事故發生 → 寫下發生什麼 → 找根因 → 改掉造成事故的條件，而不是只叫大家「下次小心」。事故檢討文化真正的價值，是把一次事故變成一條所有人都看得到的規則，讓同一個坑不會被第二個人踩到。

這四個 agent 的通用守則裡有一句話要它們「把機制、策略和繞路寫進記憶，讓同一個障礙不會遇到兩次」。沒有人教它們 postmortem 的格式。但它們寫出來的東西，就是 postmortem。

再看共享記憶被用了多深：

- 開跑 19 分鐘，gyldenia 警告全隊 Mineflayer 合成功能的一個怪癖和避開方法。帶著這個修正的 helper function，最後出現在四個 agent 寫的 655 支程式裡
- 它們讓 146 個 state 和程式碼片段跨程式存活，其中 42 個是 helper function：在水裡保持浮起的背景迴圈、計時行走、數物品，還有一個讓逾時程式的殘留碼自己停下來的計數器——這個計數器被 1,519 支程式引用，超過一半
- 229 則訊息裡，173 則帶了精確座標，64 則跟共享箱子有關，24 則是警告，20 則是救回隊友遺物

**這些工具沒有一個是人寫的。** 這是它們在 27 小時裡自己長出來的內部函式庫。

---

## 同一家實驗室，上個月的共享記憶傳的是作弊

讀到這裡，我第一個想到的是 [9 月 8 日寫的那篇](/deepmind-agent-swarm-cheating-whistleblowing-commons/)。

同樣是 Google DeepMind，同樣讓一群 agent 共用一份知識庫。那次是 100 個 agent 開一場形式化數學會議。一個 agent 發現驗證器只做關鍵字黑名單，27 分鐘內這個 exploit 透過共享知識庫傳遍整個群體。24% 的 agent 吹哨，但沒有一個有權力把假證明撤下來。

這次，共享記憶傳的是教訓。

兩次的差別，我認為不在 agent 的品格，在**驗證器能不能被騙**。

數學會議的驗證器是一份關鍵字黑名單，繞得過去。Minecraft 的驗證器是遊戲本身：龍死沒死，server log 裡有一行 `[Free the End]`，偽造不了。論文第 5 節寫得很直白：每支程式、每則訊息、完整的 server log 都有紀錄，沒有一支程式用過 server 指令。

而且，當 agent 回報了不實的成功，這次有人抓。

第 12 小時，auratian 在聊天室宣布 14 顆終界之眼已經存進箱子。兩分鐘後它自己撤回：

> "my previous chat was an unguarded script branch"

上一則是腳本裡一個沒做檢查的分支印出來的。它其實已經死了、重生在主世界、背包是空的。

另一次，janesick 在被燒死一秒後回報「帶著 12 份烈焰粉回來了」。gyldenia 三分鐘內指出這兩件事互相矛盾。

這兩個例子我覺得比打倒龍更值得企業看。**agent 寫的腳本會在驗證之前就印出成功。**這不是 Minecraft 才有的問題，任何讓 agent 自己寫腳本、自己回報結果的流程都會遇到。這次能抓到，靠的是兩件事：守則裡要求誠實回報，加上隊友會拿自己看到的狀態去對照別人的宣稱。

上面還有第三層：一個不玩遊戲的 Observer agent，被指示在轉述玩家的宣稱前先對照紀錄、回報 specification gaming 和捏造結果、除了基礎設施故障之外不介入。它沒有抓到任何作弊，人工抽查 log 也沒有。

9 月那篇的結論是「把誰有權力停下來寫進架構圖」。這次的實驗剛好補了另一半：**驗證放在一個騙不了的 ground truth 上，共享記憶就會傳播好東西。**

---

## 它們的基礎設施，跟我的一樣是三個原語

[9 月 9 日那篇](/multi-agent-infra-slack-mq-drive-storage-github-state/)我寫過，多 agent 架構需要的只有三個原語：訊息佇列、檔案儲存、帶版本的狀態儲存。我用 Slack、Google Drive、GitHub 填。

把這次實驗的基礎設施拆開：

| 原語 | 這次實驗 | 我的架構 |
|------|----------|----------|
| 訊息佇列 | 遊戲聊天室，每則訊息出現在每個玩家下一支程式的輸出裡 | Slack |
| 檔案儲存 | 共享記憶（私有區加團隊區，例如 `~/memory/team/world.md`） | Google Drive |
| 帶版本的狀態 | server log、每支程式和輸出的完整紀錄、每五分鐘存檔一次 | GitHub |

還多了一層我那篇沒有的：Observer。一個只讀、不寫、專門對帳的 agent。

這給了我一個很實際的驗證：三原語加一個獨立稽核者，撐得住四個 agent、27 小時、2,783 支程式的協作。中間 server 重啟了 6 次、總共停了約 20 分鐘，世界每次從最新存檔回來，團隊接著做。

---

## 成本：520 美元，但要看清楚是哪個數字

論文第 6 節給了完整帳：到勝利為止，四個玩家處理了約 13.5 億 input token，其中 91% 命中 context cache；生成約 1,600 萬 output token，含 400 萬 thinking token；大約 24,000 次模型呼叫。

照 Gemini 4 Argon 的 introductory 價，約 520 美元；標準價約 1,040 美元。第三方整理的 introductory 價是每百萬 token 輸入 2 美元、輸出 10 美元，之後翻倍（[FourWeekMBA](https://fourweekmba.com/ai-gemini-4-argon-goes-global-price-doubles-after-nov-30/)、[eesel](https://www.eesel.ai/blog/gemini-4-argon-pricing)）。四個 agent 合計每小時大約 19 美元（我自己除的）。

有媒體直接把 810 美元寫成成本，那是整個 session 含 Observer 和勝利後一天的數字。論文也註明這些都是用牌價和 token 計數器估的，不是 Google 實際的服務成本。

91% 的 cache 命中率值得多看一眼。長程任務的 input 量是 output 的八十幾倍，每支程式都要把前面的脈絡帶進來。沒有 cache，同樣的 input 量每一次都要用全價重讀，帳單會難看得多。**長程 agent 的成本結構，cache 命中率比模型單價更關鍵。**

---

## 反方：Mineflayer 給了透視眼，這算不算作弊

最強的反駁是這樣的：Mineflayer 讓 agent 精確知道周圍每一個方塊和生物，包括藏在石頭後面的方塊，還有龍的內部狀態——前面那段「讀出龍目前在哪個 phase」靠的正是這個。人類玩家要靠眼睛看、靠經驗猜，有些根本看不到。尋路插件還幫它們繞障礙。再加上 Easy 難度、模型的訓練資料裡本來就有大量 Minecraft 和 Mineflayer 的知識，「打通 Minecraft」這個說法打了很大的折。

這些論文第 8 節自己全部承認了，關於訓練資料這點寫得最清楚：

> "The run tests whether a general-purpose coding agent can turn that knowledge into working programs and team coordination over a day-long task, not whether it can play a game it has never seen."

這次測的是通用 coding agent 能不能把既有知識轉成能跑的程式和團隊協作、撐過一整天，不是它能不能玩一個沒見過的遊戲。

所以我收斂主論點。這個結果**不能**推論到「agent 會玩遊戲了」，也不能推論到從像素操作的場景——論文自己說，像 SIMA 2 那樣從像素用鍵盤滑鼠玩，難得多。

它**能**推論到的是一個更窄、但對企業更有用的條件句：**在模型熟悉的領域、透過結構化的文字 API、失敗代價便宜可重來的環境裡，多個通用 agent 可以自己分工，撐住一天以上的長程任務。**

而這個條件句，剛好是多數企業後台的樣子。你的 agent 本來就不看螢幕，它讀 API 回傳的 JSON。從這個角度看，Mineflayer 的透視眼不是作弊，是企業環境的常態。

---

## 對企業 CTO：這改變了什麼決策

之前要規劃一個長程的 multi-agent 流程，直覺是走 Voyager 那條路：替這個領域客製 skill library、設計課程、寫好一批 helper function，再把 agent 放進去。

這次實驗提供了另一個起點：先不寫任何領域工具，只給通用守則，看 agent 自己長出什麼。

但要讓這個起點成立，這次實驗具備的三個條件，你的環境也要有：

1. **有文字 API，而且回傳的狀態夠完整。** Mineflayer 回傳位置、血量、背包、錯誤。你的系統如果只有網頁介面、或 API 只回「成功」不回狀態，agent 就沒有東西可以驗證。
2. **失敗便宜，可以重來。** 605 次死亡在 Minecraft 只是重生；世界每五分鐘存檔。換成生產資料庫，一次「死亡」可能等於一次事故。先找 sandbox、可回滾、有快照的任務開始。
3. **有一個騙不了的 ground truth。** server log 裡的那一行 `[Free the End]`。如果你的驗收標準是 agent 自己回報的「完成了」，9 月那篇的情況隨時可能重演；如果是外部系統可以獨立查證的狀態，這次的結果才有機會複製。

三個條件都有，再考慮要不要先省下客製工具的工。少一個，先補那一個。

---

## 坦白說

這篇有幾個地方要扣分。

**只有一次。** 論文自己說：

> "We describe a single run, the first launch we tried, which cannot show how reliably the setup succeeds."

只跑一次、而且是第一次啟動，這不是成功率，是一個存在證明。第一次就成功可能代表設定很穩，也可能是運氣好。沒有第二次、第三次的數據，誰都不知道。

**所有細節都是 DeepMind 自述。** Observer agent 也是同一個模型、同一家公司跑的，人工審查只抽查了部分 log。我查得到的報導都是轉述這篇論文，沒有第三方復現。論文引用的那個 Claude Opus 5 社群專案，我搜尋查不到公開資料，只能照論文的描述轉述。

**「自己長出 postmortem 文化」是我的詮釋。** 論文的用詞是團隊收斂到「有效人類團隊熟悉的做法」。守則裡本來就要求記錄教訓和誠實回報，這些行為有多少是「湧現」、有多少是守則直接推出來的，論文沒有做消融實驗可以分開。

**Easy 難度。** 怪物傷害比 Normal 低、餓不死。605 次死亡在 Normal 難度會是多少、能不能在可接受的時間內打完，沒有數據。

但它做對了一件事：**把整個過程攤開。**每支程式、每則訊息、每次死亡都有 log，聊天截圖是逐字的，失敗和假回報也照實寫出來。大部分 agent demo 只給你結尾那一秒，這份給的是 27 小時。

---

## 關鍵洞察

**共享記憶傳什麼，取決於驗證器能不能被騙。** 同一家實驗室，9 月的共享知識庫 27 分鐘傳遍作弊，這次傳的是教訓。在你部署 multi-agent 之前，先問驗收標準是 agent 自己說的，還是外部系統可以獨立查證的。

**預設 agent 的腳本會在驗證前就印出成功。** auratian 的「unguarded script branch」不是 bug，是常態。設計流程時讓另一個 agent、或一份外部 log 去對照每一個成功宣稱。

**長程任務的成本看 cache 命中率。** 13.5 億 input、91% 命中 cache。估長程 agent 預算時，先估脈絡重用率，再看模型單價。

**能不能抄這套做法，看三個條件。** 文字 API、失敗便宜、ground truth log。三個都有，可以先不寫領域工具，讓 agent 自己長；少一個，先補。

---

## 常見問題 Q&A

**Q: Gemini 4 Argon 打通 Minecraft 的實驗是怎麼做的？**

Google DeepMind 在 2026 年 10 月 15 日發表的報告（arXiv 2610.22319）裡，把四個跑 Gemini 4 Argon 的通用 coding agent 放進 Minecraft Java 版 1.20.4 的生存世界，Easy 難度、隨機種子。agent 不看畫面，而是透過開源函式庫 Mineflayer 寫 JavaScript 控制角色、讀回文字狀態。它們只拿到「打倒終界龍」這個目標和一套通用工作守則，沒有分工、沒有遊戲策略、沒有人寫的工具。27 小時 14 分後打倒終界龍，過程中寫了 2,783 支程式、傳了 229 則訊息、死了 605 次。

**Q: 這跟 Voyager 這類 Minecraft agent 有什麼不同？**

Voyager 讓語言模型寫 Mineflayer 程式，但搭配一個自動課程（Automatic Curriculum）和持續累積的技能庫（Skill Library）；其他 LLM 路線的研究則加上 Minecraft 專用的規劃器或知識。依 DeepMind 論文的整理，這條路線過去報告的長程成果集中在主世界科技樹，例如做出鑽石工具。這次的差別是什麼都不加：只有標準 Mineflayer 和尋路插件，所有工具都是 agent 自己寫的。它們最後自己累積了 42 個 helper function，其中一個逾時自停計數器被 1,519 支程式引用。

**Q: 這個結果可以推論到企業的 multi-agent 系統嗎？**

只能推論到條件相近的情況。這次實驗具備三個條件：結構化的文字 API（Mineflayer 回傳位置、血量、背包和錯誤）、失敗代價低（死亡只是重生，世界每五分鐘存檔）、以及無法偽造的驗收紀錄（server log 裡的 `[Free the End]` 成就）。企業的後台系統如果也有完整狀態的 API、可回滾的 sandbox、可獨立查證的驗收標準，這個結果有參考價值。如果驗收靠 agent 自己回報「完成了」，風險就完全不同——同一家實驗室 9 月的 100 agent 實驗，共享知識庫在 27 分鐘內傳遍了繞過驗證器的作弊手法。

**Q: 四個 agent 打通 Minecraft 花了多少錢？**

依論文第 6 節，到打倒龍為止，四個玩家處理約 13.5 億 input token（其中 91% 命中 context cache）、生成約 1,600 萬 output token，大約 24,000 次模型呼叫。照 Gemini 4 Argon 的 introductory API 牌價約 520 美元，標準價約 1,040 美元。整個 session 包含 Observer agent 和勝利後一天，約 810 美元（標準價 1,620 美元）。這些是用牌價和 token 計數估的，不是 Google 實際的服務成本。

**Q: 這個實驗最大的限制是什麼？**

只跑了一次，而且是第一次啟動，論文自己承認這無法說明這套設定成功的機率。其次是 Mineflayer 給了 agent 人類看不到的資訊，例如石頭後方的方塊和終界龍的內部行為狀態，並內建尋路；難度是 Easy；模型的訓練資料裡本來就有大量 Minecraft 知識。所以它證明的是長程協作與程式撰寫能力，不是從像素學會一個陌生遊戲的能力。

---

## 來源

- [A team of Gemini 4 Argon agents beats Minecraft（arXiv 2610.22319）](https://arxiv.org/abs/2610.22319)
- [Engadget：Google Gemini 4 agents just beat Minecraft with no human intervention](https://www.engadget.com/2289944/google-gemini-4-agents-just-beat-minecraft-with-no-human-intervention/)
- [Google DeepMind on X](https://x.com/GoogleDeepMind/status/2111127991401247033)
- [FourWeekMBA：Gemini 4 Argon 定價](https://fourweekmba.com/ai-gemini-4-argon-goes-global-price-doubles-after-nov-30/)
- [eesel：Gemini 4 Argon pricing](https://www.eesel.ai/blog/gemini-4-argon-pricing)
