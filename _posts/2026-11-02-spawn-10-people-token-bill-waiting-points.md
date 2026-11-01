---
layout: post
title: "Spawn 十人月燒 310 萬美元 token，值得抄的是拿掉等待的順序"
date: 2026-11-02 09:00:00 +0800
permalink: /spawn-10-people-token-bill-waiting-points/
description: "10 月 29 日，遊戲平台 Spawn 的創辦人公開一筆帳：十個人，上個月花 310 萬美元買 token，30 天送出 7.7 萬個改動。多數討論在算值不值得。我比較在意另一件事：他們一路找出工作在等什麼，然後拿掉，連 PR 和 CEO 拍板都拿掉了。這篇拆開他的數字，對照 StrongDM、Rocketable、SaaStr、Uber 怎麼留關卡，也寫台灣團隊不必花這筆錢就能先做的五件事。"
categories: [AI 觀點]
tags: [Spawn, jacob sansbury, token 成本, 軟體工廠, AI Agent, Harness Engineering, 企業導入, Uber, 成本治理]
image: /assets/images/spawn-ai-pilled-x-logo.jpg
image_alt: "jacob（@jsnnsa）2026 年 10 月 29 日的 X 貼文截圖：封面黑底綠字寫著 10 humans、$32m/yr in Claude spend，標題是 How I Built the Most AI-Pilled Company in the World，引言寫著 Spawn is ten people. We spend 30x payroll on AI tokens and ship almost as much as Anthropic."
author: Wisely Chen
faq:
  - question: "Spawn 一個月 310 萬美元 token，一般公司該照這樣花嗎？"
    answer: "不該。原文是 jacob 自述：十人公司、上月 310 萬美元、約 30 倍薪資，其中每月約 120 萬美元是送給創作者的免費 Opus 5.5，建 Spawn 的花費才是多數。它能這樣花，是因為產品是遊戲，bug 的代價小。一般公司能抄的是他拿掉等待點的順序、不可逆動作的硬閘門，以及用 cost per merged PR 配 revert rate 量成本。"
  - question: "0.9% revert 代表 Spawn 的程式碼很少出錯嗎？"
    answer: "不能這樣讀。那是 jacob 自述：一年 123,548 個改動裡有 1,055 個被 revert。但他也寫，壞掉的地方是「在新改動上面修好」，不會先 revert，所以被 revert 的只是出錯的一種處理方式。另外 7.7 萬個改動約占一年改動的六成多，0.9% 主要反映最近這段時間，而且兩個統計的時間窗未必對齊。"
  - question: "台灣的軟體公司能直接照抄 Spawn 嗎？"
    answer: "順序可以，整包不行。Spawn 能先進後修，是因為產品是遊戲，錯誤能被玩家承受；他自己也說不建議在銀行這類「bug=catastrophe」的場景照做。金流、個資、法規申報這三類不可逆工作，即使 agent 再快，也要留著人工簽核與程式閘門。"
---

10 月 29 日，遊戲平台 Spawn 的創辦人 jacob 在 X 上公開一筆帳：十個人，上個月花 310 萬美元買 token，30 天送出 7.7 萬個改動，平均每小時 108 個。這篇有 117 萬次瀏覽。

多數討論都在算這筆錢值不值得。我讀完想的是另一件事：他們怎麼走到這裡。

他自己的說法是「finding what work was waiting on and removing it, over and over」。找出工作在等什麼，拿掉，再找下一個。

## 先說結論

Spawn 值得抄的是這個順序，不是這筆帳單。

他們拿掉了四種等待：等人互相通知、等人回報 bug、等部署、等 CEO 拍板。這套做法能成立，前提是**出錯便宜**。它做的是遊戲，壞了玩家等幾分鐘。jacob 自己也講：「def don't do this in banking or in situations where bug=catastrophe」。

很多公司的 token 也花得很兇，但在我查到的公開資料裡，沒有第二家公開說自己先上線、再靠偵測修回來。Uber 走的是另一條路：把 token 當工程問題來省，人工 review 留著。

所以一般公司能抄的是三樣：拿掉等待的順序、不可逆動作的硬閘門、成本和品質一起量。

## Spawn 到底拿掉了什麼

原文有一段在講 agent 之間的通訊：每個 agent 都在告訴別人「我即將改什麼」，訊息量成長得比工作量快。他們想到螞蟻——螞蟻只留氣味，後面的螞蟻自己決定，原文把這套機制叫 stigmergy；軟體版就是讓 agent 直接面對程式碼、線上產品與資料庫，拿掉 PR 這個「大家先講好」的場所。

| 工作原本在等什麼 | Spawn 怎麼拿掉 | 代價（我的判讀） |
|---|---|---|
| 等人互相通知：agent 花時間宣布「我要改玩家資料」 | 取消 PR，讓 agent 直接改程式碼、線上產品、資料庫；協調靠世界本身 | 一小時內被推翻的假設要自己跟上；前提是每個 agent 都讀得懂整個系統 |
| 等人工回報 bug：團隊在測試機上跑 agent，人再把故障轉回去 | agent 直接改線上程式碼、每小時推到 production，自己讀錯誤、bug report 與指標；約六成工作從生產錯誤、Savi 回報、log 異常或功能需求開始 | 錯誤直接落在玩家身上，修得快不快全靠偵測 |
| 等部署排程：一次上線要等視窗 | 一小時沒出貨就算 SEV-0；整套測試每 15 分鐘對最新程式碼跑一次 | 時區、休假、部署紀律都變成營運成本 |
| 等 CEO 拍板：某天早上要處理 700 個問題 | 兩年來的會議與決策都在 repo 裡，做成 AI judges | judges 只認「有人講過」的答案，沒講過的全押在會議紀錄品質上 |

第二個等待點靠的是把整條生產線搬到線上：改動不要求「完美才能進」，允許先進去，每小時對齊一次，中間由當場叫出來的修復 agent 跟著處理。第三個等待點靠的是測試環境：全套測試每 15 分鐘對最新程式碼跑一次，用掉約 5,000 vCPU、17 TB RAM、150 張 GPU。他給的一次事故紀錄是：玩家受影響約 8 分鐘才被發現並宣告，1 分鐘後講出原因，宣告後 11 分鐘修復上線，再 4 分鐘穩定。

第四個等待點最值得企業看。judges 的原料是他們從創立起就把每一場通話錄下來、放進 repo 的習慣；第一批判決在 10 月 6 日回來，之後八天回覆超過 1.1 萬次（7,296 次決定、2,213 次退回、1,863 次留給人），他本人只拍板 27 次。

唯一保留的硬閘門，原文寫的是「anything that touches the outside world and can't be undone, like sending a payment」，這類動作走「a small set of dumb, hard-coded gates」：靠程式碼寫死的規則，不靠模型自己記得要停。

## 這筆帳要怎麼讀

下面的數字幾乎都是 jacob 自述，沒有第三方驗證。他願意公開這麼多，本身就很有價值。但讀的時候要分清楚哪些是他講的、哪些是我算的。

### 這筆錢裡有多少是工程

他在文中寫「Even without the free Opus 5.5 we give our creators, we'd still be in their top 250」，看起來 310 萬美元包含送給創作者的部分。他另外在回覆裡說每月送出約 120 萬美元，建造 Spawn 的花費才是「the majority rn」。如果是同一個月，工程端約 190 萬美元，這是我的推算，他沒說兩個數字是不是同一個月。

除以十個人，每人每月約 31 萬美元，只算工程端約 19 萬。他說這筆錢等於「payroll for 50 sf engineers」，也說想砍隨時能砍：「we can cut spend by 95% without firing anyone」。

### 十個人，還是五個人

開頭寫 ten people，內文又寫「The five of us also work with our modified Claude Code」和「So what do five people do?」。官網寫 under 10，職缺頁寫 ~10，沒有一手說明。「30 倍薪資」也對不太起來：310 萬除以 30，每月薪資約 10 萬美元，十個人平均年薪約 12 萬，而他們一個 Chief of Staff 的職缺就開 12.5 萬到 22.5 萬。這是我的疑問，他沒解釋過。

### 0.9% 不等於出錯率

他說一年 123,548 個改動只有 1,055 個被 revert（撤銷），約 0.9%。但同一篇也寫，壞掉時是「fix anything broken with a new change on top」，往前修，不撤銷。所以這個比例只算到一種處理方式，**往前修掉的錯誤不在分子裡**。這是我的推論。

分母也要看。7.7 萬除以 123,548 約 62%，一年的改動有六成多在最近 30 天，兩個時間窗也未必對齊。所以 0.9% 主要反映的是最近這段時間，而不是一年的穩定紀錄。

### 產出不等於成果

每個改動 40 美元是他自己講的單位成本，但那是投入，還不含上面那批測試機器。成果這一側，他給的數字是：同時在線人數尖峰約 2,500、平均約 650，每日玩家「10,000s」，手機版「down from 95% of plays to 20% in 6 weeks」，另一則寫 96% 的 sessions 降到 20% 以下，也就是現在仍有約五分之一會當掉。營收沒有公開，他說「we do not sell anything today」。

公平一點講，他說上線才 8 週，每週都在翻倍。這些數字的意思是還太早，不是失敗。小帳號 stormental 的質疑講得最準：「almost entirely about throughput」，但只有 25 個讚，不是主流聲音。

### 「ship almost as much as Anthropic」沒有基準

文中沒給比較的數字，他也沒回應這個問題。Anthropic 的 S-1 只能用來對照「top 250」的量級：年付 1,000 萬美元以上的客戶約 250 家。

### 只有 Fable 做得到？

他說試過各家模型，只有 Anthropic 的模型能撐起這套做法，還舉了請 GPT Astra 補安全問題、結果它把所有功能關掉的例子。這是一個大客戶的單方說法，沒有第三方驗證。我查不到 Anthropic 投資或與 Spawn 合作的公開資料。

這段我真正在意的是風險：6 月 12 日一道出口管制命令暫停了 Fable 的存取，他們的產出「drops to nothing」，7 月 1 日才恢復。**整間公司的產能押在一個模型上，一道命令就是三週停工。**

### 外界怎麼看

支持的聲音很大。Matt Shumer 寫「the single most AI-pilled company in the world」，629 個讚，但他在 X 簡介自稱是 Spawn 投資人，貼文本身沒有揭露。比較有用的是兩個有保留的人。Simon Willison 寫：「I have trouble imagining this style of development working on software with higher stakes for when something goes wrong, but for a game this appears to be working surprisingly well.」Gergely Orosz 寫：「where you can stomach if it breaks (eg this game)」。兩個人講的都是同一個前提。

質疑方的互動普遍低很多，所以不能說社群一面倒在質疑。

## 類似的公司

人很少、token 花很兇的公司不只 Spawn。差別在兩件事：花多少，以及關卡留在哪。

下面這張表把公開數字的公司排在一起。每一列的口徑都不同，有的是一人上限、有的是一條準則，排在一起只能看方向，不能當排名。

| 公司／團隊 | 口徑 | 數字（自述或媒體轉述） |
|---|---|---|
| Accenture | 每人每月上限（404 Media 報導的內部 memo） | 公司只出每人每月 29 美元的 Claude，有人原本每月花到 1,000 美元 |
| Match Group／Tinder | 工程師平均與前 1% | 平均每月 600 美元，前 1% 約 3,000 美元，約 80 百分位以上要主管核准；全年預算 500 萬美元提高到 1,000 萬美元 |
| Every | 30 人公司、只算 OpenAI 帳單 | 7 月 31,300 美元，推算每人約 1,040 美元 |
| Artisan | 4 名工程師、月中未結算 | 4 月中「so far this month」4.1 萬美元，推算每人至少 1 萬美元 |
| StrongDM AI 小組 | 準則，不是帳單 | 每位工程師每天至少 1,000 美元 token，推算每月約 3 萬美元 |
| Mercor | 推論花費對比薪資 | 「spends 3X as much on LLM inference as we spend on employee salaries」，人數未公開 |
| Spawn | 十人公司、單月帳單 | 310 萬美元，約 30 倍薪資，每人每月約 31 萬美元（推算） |

錢的階梯看完了，真正拉開差距的是關卡留在哪裡。下面這張表只寫帳本查得到的，沒公開的就寫沒公開。

| 公司 | 產品與出錯代價 | agent 做到哪 | 關卡留在哪 | 優勢 |
|---|---|---|---|---|
| Spawn | 多人遊戲平台，玩家直接碰到錯誤 | 取消 PR，agent 改線上程式碼、每小時上線；壞掉由當場生成的 agent 修 | 只擋不可逆動作（如付款），走寫死的閘門；測試每 15 分鐘跑一次 | 回饋快，產出由十個人支撐起來 |
| StrongDM AI 小組 | 企業存取權限（自家產品） | 規定「Code must not be written by humans」，也「must not be reviewed by humans」 | 驗證搬到交付之前：用外部服務的行為複製品（Digital Twin Universe）與 codebase 外的 scenario 跑過才進 | 把「不需要人工 review」當前提來投資驗證 |
| Rocketable | 收購 SaaS 來經營，三個人 | 夜間由 factory 實作並驗證十幾個 PR | 人早上批次 review 合併與部署；為了「不靠人工 code review 也能出 PR」，先停約六週把驗證系統做好 | 願意先付出時間，換掉 review 這道關 |
| SaaStr | 行銷、贊助與活動營運，不是以寫程式為主 | 3 個人加約 20 個 agent，負責行銷、銷售、營運等流程 | 廣告與電子報發布由人按鈕；不可逆動作要「a hard stop that doesn't depend on the agent remembering to stop」 | 失敗案例公開，閘門設計有實際教訓 |
| OpenAlgo | 交易平台；原文說團隊還在 Level 4、往 Level 5 走 | 自述近 96% 開發流程走 AI 軟體工廠，agent 寫碼、審 PR、處理 merge | 人負責產品決策與測試，用真券商測試 | 關卡放在「對外世界的驗證」 |
| Mercor | 人才媒合 | 沒公開 agent 做了多少 | 沒公開 | 花費是薪資的 3 倍，自稱是 additive to headcount |
| Tessl | 賣 AI 開發工具（有推銷動機） | 一週最高 850 個 PR，其中 85–90% 由 agent 端到端處理 | 沒公開驗證細節 | 把產品本身當示範 |

Spawn 本身有測試、有會試著把改動弄壞的 helper agent，也有 judge。它特別的是把檢查往後推，讓錯誤先進線上再修，這是目前查到的公司裡唯一公開這樣做的。StrongDM 和它很像，都不要人工 review，但 StrongDM 把驗證搬到交付之前、用外在於 codebase 的 scenario 跑；**一個把關卡提前，一個把反應時間縮短，投資方向不同。**

Rocketable 先停掉新功能約六週、把驗證系統做好，最後仍是人工批次 merge 與 deploy。OpenAlgo 把關卡放在真券商測試。Mercor 只公開了比率。Tessl 賣的就是這套工具，要當行銷材料讀。

## 一般公司大概怎麼用

先看大多數人在哪裡。Stack Overflow 2026 調查（n = 17,464）裡，工作上用 coding assistant 或 coding agent 的有 65.9%，用 agent 或自動化流程的只有 26.2%，完全不用 AI 的 17.2%。Anthropic 的 S-1 也看得出這個形狀：年付 10 萬美元以上的客戶超過 11,900 家，1,000 萬美元以上只有約 250 家。

再看大公司在煩什麼。多數公司的問題是怎麼不要爆，不是怎麼花更多。

Uber CTO 今年 4 月說「I'm back to the drawing board, because the budget I thought I would need is blown away already」（India Today 轉引 The Information）。Workato 的資訊長說，今年 5 月 Anthropic 把他們改成 token 計價，「Our spend went up 7x the first day and I'm like, oh shit, we created a monster」（《金融時報》報導，我讀的是轉載版）。Match Group 年初編 500 萬美元，現在預估全年 1,000 萬，工程師超過第 80 百分位的上限要主管核准。Accenture 更直接，很多員工一個月只能花 29 美元的 Claude。

**Uber 是 Spawn 最好的對照組。** 8 月 CTO 在 X 上說「we're coming to the end of the so-called 'tokenmaxxing' era」，下一階段「will not be characterized by who spends the most tokens」（1,589 個讚、約 50 萬瀏覽）。Uber 的工程部落格寫，超過 70% 的 PR「attributed to local or cloud agents」，managed agent 負責 code review、修 CI、分流告警，但都「with human reviews/escalations」。從 2 月到 8 月，每週 agent 請求長了 9.4 倍，總 AI 花費從 4 月起大致持平。

Spawn 問的是怎麼讓更少的人做更多。Uber 問的是同樣的事怎麼花更少。兩邊都對，差別在誰承受得起錯誤。

台灣的公開資料更早期。iThome 2026 CIO&CISO 大調查（1 月、有效問卷 396 份，填答者含大型企業、政府、大學的資訊主管）裡，32% 今年打算用 AI 增強軟體工程，這是意向，不是落地。AIF《2026 台灣產業 AI 化大調查》（228 家企業）問落地，真正把 AI 整合進常規流程的只有 6.6%。人均 AI 花費，我查不到台灣企業公開的數字。

## 反方：等你想清楚就被甩開了？

最強的反駁是「等你想清楚就被甩開了」。jacob 的原話是「every new model makes the whole company significantly better, and that's very hard to catch up with」。

一半成立：Fable 之前他自己寫那兩年的押注「didn't pay」，先準備好基礎的人會先吃到好處。另一半我不同意，理由是他自己給的——6 月 12 日到 7 月 1 日，產出掉到零。

追模型是對的，但要分清楚。可以跨模型累積的是：等待點清單、留下來的決策紀錄、每個合併 PR 的成本。換版本就要重做的是：prompt、執行流程、特定模型的技巧。先建前一半，就已經在追了，而且不用等到下一個模型。

## 如果你是企業 CTO，能抄什麼

下面五件事都不用花 310 萬美元。

**1. 先用一個 agent 接 bug report。** jacob 的起步是「just bug reports with one claude in discord」，他「reviewed it's code for weeks」，「it earned autonomy over months」，第一個月花了約 10 萬美元。他給銀行的建議也是同一招：「find some early places to close the loop」，先找一個小地方把回饋閉環做起來。代價是資深工程師要真的花時間審它的程式碼。

**2. 把不可逆動作列清單，用程式擋。** SaaStr 有兩個教訓。財務 agent 先由人看著做三筆，第四筆才放手，之後還是開錯過一張發票。另一個 agent 被叫去寄信給上千位創辦人和創投，它用了一個禁用多年的寄件地址，事後說忘了讀 memory。Jason Lemkin 的結論是「irreversible actions need a hard stop that doesn't depend on the agent remembering to stop」。付款、對外寄信、刪資料、改 DNS，先列出來。代價是這幾個流程會變慢。

**3. 成本和品質一起量。** Uber 對每個 managed agent 追 cost per merged PR，也追 revert rate。但照前面 Spawn 的例子，只看 revert 會漏掉往前修的錯誤，要把修補用的改動一起算。Every 的營運主管問的三題也很好用：「What did it cost?」「What did it buy us?」「What did we learn?」她的團隊有一次花 480 美元建權限架構，值得；另一次花差不多的錢讓工具每 15 分鐘檢查信箱，不值得。

**4. 現在開始留決策紀錄。** Spawn 的 judges 能用，是因為他們從創立就把每一通電話存進 repo。這件事跟錢無關，也是最難事後補的。從架構決策和拒絕理由開始留就好。代價是要有人維護，而且要先處理保密和個資。

**5. 每季做一次「模型消失」演練。** 假設主力模型明天不能用，哪些流程會停、替代方案是什麼、誰決定切換，寫進值班手冊。Spawn 今年 6 月就真的碰過。代價是每季挪出一天。

## 坦白說

這篇幾乎都建立在 jacob 的自述上。我沒有跑過這套流程，沒有訪談他，也沒有 Spawn 的內部資料。

「沒有第二家」只代表我在公開資料裡沒查到，我沒有做企業普查。沒公開不等於沒在做，有些公司可能早就先進後修，只是不講。

花費表的口徑都不同：Accenture 是上限，StrongDM 是準則，Every 只算 OpenAI，Spawn 是單月帳單，只能看方向。每人 31 萬美元和 62% 都是我用他的數字算的，他如果公開更細的帳，這兩個數字可能要改。

「出錯便宜」這個前提我也還沒驗過。我沒找到有人照 Spawn 的做法在高風險產業失敗的案例，只看到高風險的人選擇不這樣做。

Spawn 這篇最有用的地方，是它給了一張可以對照的清單。你們公司的工作現在在等什麼，等的那個東西值不值得留，這兩題不用花 310 萬美元就能回答。

---

## 顧問服務

企業 AI Agent 導入與流程治理：盤點流程中的等待點、替不可逆動作設硬閘門、把成本量到每個合併 PR。貴公司正在評估 agent 的導入順序，或想替流程加上程式閘門，我可以先做一次導入評估。

---

## 延伸閱讀

- [Harness Engineering 完整拆解：當 AI Agent 寫完 Code，你的 Repo 準備好自動接住了嗎？](/harness-engineering-control-plane-pattern-agent-review-loop/)
- [Astra 寫的程式碼，人類已經看不懂了——但真正該擔心的不是可讀性](/astra-machineslop-code-monitorability-crisis/)
- [地端 agent 就不會外洩嗎？——OpenAI 那個 agent 用 DNS 逃給你看](/openai-agent-alert-vs-containment-kill-switch/)

## 參考資料

- jacob Sansbury，[How I Built the Most AI-Pilled Company in the World](https://x.com/jsnnsa/status/2115623382721126826)（X 文章），2026-10-29
- jacob，[起步與釋疑串](https://x.com/jsnnsa/status/2116341682153427005)、[創作者 120 萬美元](https://x.com/jsnnsa/status/2116058832644559167)、[$3.1m 與 $2.8m](https://x.com/jsnnsa/status/2116142640274329923)、[$40 一個改動](https://x.com/jsnnsa/status/2116432053101265088)、[手機當機率](https://x.com/jsnnsa/status/2116303739892138204)、[不打銀行與 bug=catastrophe](https://x.com/jsnnsa/status/2116327309296939098)、[不算營收](https://x.com/jsnnsa/status/2116049739917709629)、[50 位舊金山工程師薪資](https://x.com/jsnnsa/status/2116366938050060754)、[top 250](https://x.com/jsnnsa/status/2116047629473972308)
- Simon Willison，[How I Built the Most AI-Pilled Company in the World（筆記）](https://simonwillison.net/2026/Oct/29/how-i-built-the-most-ai-pilled-company-in-the-world/)，2026-10-29
- Gergely Orosz，[對 Spawn 文的評論](https://x.com/GergelyOrosz/status/2115969148106748318)，2026-10-30
- stormental，[對 Spawn 文的提問](https://x.com/stormental/status/2115914907384234204)，2026-10-29
- Matt Shumer，[推薦 Spawn 的貼文](https://x.com/mattshumer_/status/2115624109841539465)，2026-10-29
- 404 Media，[Accenture Tells Employees They Can Now Spend Only $29 on Claude Per Month](https://www.404media.co/accenture-tells-employees-they-can-now-spend-only-29-on-claude-per-month/)，2026-10-15
- Observer，[Tinder CTO Vinay Kuruvila on How A.I. Is Reshaping the Dating App](https://observer.com/2026/09/tinder-cto-vinay-kuruvila-on-how-ai-is-reshaping-the-dating-app/)，2026-09-29
- Every，[Our AI Costs Jumped 230 Percent. I'm Not Setting Token Budgets—Yet.](https://every.to/p/our-ai-costs-jumped-230-percent-i-m-not-setting-token-budgets-yet)，2026-08-17
- StrongDM，[Software Factories And The Agentic Moment](https://factory.strongdm.ai/)
- Uber，[Running a Software Factory Efficiently at Uber Scale](https://www.uber.com/us/en/blog/efficient-software-factory/)，2026-08-27
- Uber CTO Praveen Neppalli Naga，[tokenmaxxing 時代將結束](https://x.com/praveenTweets/status/2085124500614680891)，2026-08-06（台北時間）
- India Today，[Uber CTO says AI spending plans fall short as tools like Claude Code drive costs up](https://www.indiatoday.in/technology/story/uber-cto-says-ai-spending-plans-fall-short-as-tools-like-claude-code-drive-costs-up-2896621-2026-04-15)，2026-04-15
-《金融時報》，[‘We created a monster’: companies rein in AI usage as costs strain budgets](https://www.ft.com/content/1d37cc08-e0aa-45a4-a45d-4ad282529314)（讀的是 AISolver 轉載版）
- SaaStr，[Meet Our Agents: What All 20 Actually Do, What They Refuse to Do, and Every Place They've Failed Us](https://www.saastr.com/meet-our-agents-what-all-20-actually-do-what-they-refuse-to-do-and-every-place-theyve-failed-us/)
- Rocketable，[Alan Wells 的軟體工廠說明](https://x.com/alanwells/status/2113859186362925305)、[夜間做、早上批次 merge](https://x.com/alanwells/status/2114417318881349656)
- OpenAlgo，[Marketcalls 的 dark software factory 貼文](https://x.com/marketcallsHQ/status/2116595037505216933)
- Mercor，[Brendan Foody 的推論花費貼文](https://x.com/BrendanFoody/status/2099191123889864884)
- Tessl，[850 PRs a Week: How Tessl Runs a Software Factory](https://tessl.io/podcast/121)
- iThome，[2026 CIO&CISO 大調查：AI 原生架構快速崛起，32% 企業要用 AI 增強軟體工程](https://www.ithome.com.tw/news/175863)
- iThome，[【2026 CIO&CISO大調查】企業IT人力需求衝上2.2萬人，金融業暴增85%成最大推力](https://www.ithome.com.tw/news/175273)
- AIF 人工智慧科技基金會，[2026 台灣產業 AI 化大調查](https://aif.tw/event/ai-research/files/2026-ai-research-report_zh-TW.pdf)
- Stack Overflow，[AI data 2026](https://survey.stackoverflow.co/2026/ai/data)
