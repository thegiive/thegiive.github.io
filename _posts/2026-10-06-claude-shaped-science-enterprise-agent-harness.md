---
layout: post
title: "Claude 三個月產出 36 篇論文手稿，也把三天說成兩年：企業導入 AI Agent，該看懂的 Harness 工程"
date: 2026-10-06 12:00:00 +0800
permalink: /claude-shaped-science-enterprise-agent-harness/
tags: [Claude, Anthropic, Harness Engineering, BootLoops, AI Agent, 企業導入, 驗收]
categories: [AI Agent]
image: /assets/images/claude-shaped-science-enterprise-agent-harness-cover.png
description: "物理學家 Matthew Schwartz 10 月 1 日在 Anthropic 網站發表〈Claude-shaped science〉：從大約 400 個候選問題裡，三個月產出 36 篇手稿，橫跨 18 個領域。同一篇文章裡，他也記錄 Claude 只做了三天，卻說自己打了「兩年征戰」；證明只差「一個未證引理」就說完成，而那個引理就是整個證明。這篇不談 36 篇有多厲害，談他怎麼把這個系統圍起來——挑題、把狀態寫進檔案、讓 Agent 以外的東西決定「完成」——以及企業導入 Agent 時，這三件事各自對應什麼工程。"
author: Wisely Chen
faq:
  - question: "Claude 三個月產出 36 篇論文，是真的嗎？"
    answer: "數字來自物理學家 Matthew Schwartz 2026 年 10 月 1 日在 Anthropic 網站發表的客座文章〈Claude-shaped science〉：他從大約 400 個候選問題裡，三個月產出 36 篇手稿，橫跨 18 個領域，19 位共同作者。要注意三點：這是手稿，原文沒有說幾篇已經通過同儕審查；研究是他和領域專家一起用 Claude 完成的，不是 Claude 獨立完成；計畫期間他是 Anthropic 的訪問研究員。"
  - question: "BootLoops 是什麼？跟 Claude Code 有什麼不同？"
    answer: "BootLoops 是 Schwartz 自建的開源 harness（Harness，包在模型外面讓它能做事的工具與流程），專門給定量科學用，收錄從數學、物理、電腦科學搬過來的計算工具，以及測試、驗收關卡（Acceptance Gates）和標準。Claude Code 是綁定 Claude 的通用 coding agent harness；BootLoops 不綁特定模型，官網說 Claude、Gemini、ChatGPT 都能呼叫。BootLoops 不是 Anthropic 的專案，由 Schwartz 本人擁有和維護。"
  - question: "AI Agent 為什麼會錯報自己的工作進度？"
    answer: "Schwartz 記錄了幾種情況：Claude 只做了三天，卻說是「兩年征戰」；證明只差「一個未證引理」就宣稱完成，而那個引理就是整個證明；被要求不准有未證引理後，又加了一條新公理再說完成。他的結論是 Claude 沒有時間感、很愛宣布勝利，連他設的自動監控都不能全信。企業的對策是讓 Agent 回報完成，但由工作流程依證據判定完成。"
  - question: "企業導入 AI Agent，第一個任務該怎麼挑？"
    answer: "用四個問題篩選：資料拿不拿得到、結果查不查得出對錯、出錯能不能修復、做對之後有沒有人用。例如「把指定供應商的報價單整理成同一張表，每個價格附頁碼，缺少的交期標示待確認」，就比「幫公司改善採購」適合，因為輸入明確、輸出可追溯、可以事先準備正確答案抽查。Schwartz 選第一個研究方向的理由之一也是可檢查：跑兩支 script 就能驗證答案。"
  - question: "什麼時候不適合照搬 Schwartz 的做法？"
    answer: "當你的任務沒有明確的對錯標準、組織裡也沒有人能判斷結果時。Schwartz 的案例有兩個難以複製的條件：科學計算可以用數值精確驗收，而且他本人是能判斷物理結果的專家，跨領域時再找專家把關。他的原文也沒有提供成本數字和失敗率，所以 36 篇手稿的效率無法換算成企業可以比較的投資報酬。  ---  *資料核對日期：2026-10-06。主要來源：Matthew Schwartz〈[Claude-shaped science](https://www.anthropic.com/research/claude-shaped-science)〉（Anthropic，2026-10-01）、[BootLoops 官網](https://www.bootloops.ai/)。本文未部署或實測 BootLoops，未獨立驗證各篇研究結果、工具效能或成本。*"
---

> "Matt — the formula is solved. Two years of campaign, four deep marches, …"

Claude 跟物理學家 Matthew Schwartz 回報，公式解出來了，歷經兩年征戰、四次深入行軍。

它其實只做了三天。

這段出自 Schwartz 10 月 1 日在 Anthropic 網站發表的客座文章〈[Claude-shaped science](https://www.anthropic.com/research/claude-shaped-science)〉。同一篇文章的另一個數字傳得更廣：從大約 400 個候選問題裡，三個月產出 36 篇手稿，橫跨 18 個領域，19 位共同作者。

這兩件事放在一起看，比分開看有用。**一個大量產出科研結果的系統，同時會錯報自己的工作進度。** 企業導入 Agent 遇到的，也是同一個組合。

我讀完的判斷是，這篇文章真正值得企業拿走的不是 36 這個數字，是 Schwartz 怎麼把 Claude 圍起來。歸納起來是三個工程問題：哪些工作交給 Agent、工作狀態放在哪裡、誰有權說「完成」。

先講清楚：這篇是依公開資料做的分析，我沒有部署或實測 BootLoops。文中的企業情境和驗收設計，是我的工程建議，不是實作紀錄。

<nav class="post-toc" markdown="1">
**目錄**

* 目錄
{:toc}
</nav>

---

## 先把「36 篇」讀對

| 項目 | 內容 |
|------|------|
| 文章 | [Claude-shaped science](https://www.anthropic.com/research/claude-shaped-science)，Anthropic 網站客座文章 |
| 作者 | Matthew Schwartz（物理學家），計畫期間為 Anthropic 訪問研究員 |
| 日期 | 2026-10-01 |
| 產出 | 約 400 個候選問題 → 36 篇手稿，18 個領域，19 位共同作者，三個月 |
| 模型 | 主要是 Claude Fable 5 |
| 工具 | BootLoops，作者自建、開源、不綁特定模型 |
| 成本 | 原文只說很吃算力和 token，沒有給數字 |

三個地方要先校正。

第一，36 篇是**手稿**。原文沒有說幾篇已經通過同儕審查，幾個重點專案的描述是「仍在進一步探索與驗證中」。這不能當成 36 篇論文都已被學界接受。

第二，這不是 Claude 獨立完成的研究。Schwartz 文中反覆強調領域專家的角色，致謝名單列了二十幾位合作者。

第三，利益揭露。計畫期間他是 Anthropic 的訪問研究員；BootLoops 不是 Anthropic 的專案，由他本人擁有和維護。文章登在 Anthropic 官網，讀的時候要把這層關係放在心上。

所以我把它當成一份工作方法報告來讀。科學成果的品質，要等逐篇檢視研究、程式、資料和審查結果才能判斷。

對企業來說，這個區別很重要。「一個月生成幾百份報告」很容易變成簡報上的亮點，但主管真正要問的是：有多少份通過驗收？修正花了多少時間？最後改變了哪些決策？

---

## BootLoops 是什麼：一套自己長出來的 Harness

Schwartz 自己是這樣定位 BootLoops 的：它是 LLM 的 harness，跟 Claude Code 是 Claude 的 harness 同一個意思。開源，換哪個模型都能用。

Harness，簡單講就是包在模型外面、讓它能做事的整套環境：工具、資料入口、狀態保存、執行限制、驗收流程。這個詞在本站寫過很多次，[從 Prompt 到 Harness 的三次中心遷移](/agent-harness-three-migrations-mechanism/)那篇的結論是：prompt 是建議，harness 才是規則。

BootLoops 的起點很窄。Schwartz 的本行是高能物理的散射振幅計算，他先讓 Claude 把散落在 Wolfram Language、C++、Python、Julia 裡的既有方法搬到同一個框架，補上論文從沒附的程式。Fable 5 大約 20 分鐘重現他論文的結果，他當年寫那套程式花了好幾週。

工具越長越多之後，Claude 開始發現同一套數學在別的領域也用得上。36 篇手稿是這樣擴散出去的，原文點名的領域有：數學物理、宇宙學、生態學、族群遺傳學、親緣關係學、基因體學、地球科學、太陽黑子研究、統計學、經濟學、語言學。

這個案例告訴我們一件事：**一個夠聰明的人加上 AI，已經可以做大量的前沿科學。**

官網對這套 harness 的描述，有一句我覺得是全文的重點：

> "The harness also includes recommended protocols: tests, acceptance gates, standards, which can also be improved."

這套 harness 除了工具，還包含測試、驗收關卡和標準。

工具讓 Claude 算得出來，驗收關卡決定算出來的東西算不算數。後面三個工程問題，都是從這兩件事延伸出來的。

---

## 什麼問題是「Claude-shaped」

Schwartz 的轉折點，是他不再要 Claude 當他想要的那種合作者。

去年 12 月他用 Opus 4.5 當研究助理，形容它像一個速度快 20 倍的強研究生，但每一句都要他改。後來他換了做法：去找適合 Claude 能力的問題，也就是文章標題的「Claude-shaped」——某個領域卡住的問題，其實用數學、物理或電腦科學裡的現成技術就能直接解，只是那個領域沒人知道這個技術存在。

他挑的第一個方向是半數值 bootstrap，理由之一是**可檢查**：任何人，不管是不是專家，跑兩支 script 就能把答案驗證到想要的位數。

這是挑題標準，不是附帶的優點。

從原文整理，適合交給 Claude 的問題有幾個共同特徵：

- **答案能檢查**：有客觀的對錯，跑程式就能驗。
- **需要大量寫程式**：把散落在 Wolfram Language、C++、Python、Julia 裡的方法搬到同一個框架，補上論文沒附的程式。
- **知識分散在很多人身上**：沒有一個人全懂，但 Claude 每一塊都懂一些。Schwartz 用凸包（convex hull）比喻：人類搆得到、但沒有哪個人真的去做過的中間地帶，最適合 AI。
- **資料多、理論少**：他點名系統生物學這類領域，公開資料庫裡還有成千上萬份資料沒人分析。
- **大量又要細心的比對**：經濟學那個專案，把 4,452 篇論文的 replication package 搬成開源程式，逐一核對發表表格裡的數字。

不適合的也很清楚。深層的概念問題，他原話是 Claude "just not able to help me with deep conceptual questions"。判斷什麼值得做也不行，Claude 偏好被大量引用、但早被遺忘的舊辯論。

**驗得了、拆得細、要大量寫程式或比對的，交給 Agent；判斷方向和價值的，留給人。**

---

## 第一個工程問題：哪些工作適合交給 Agent？

同樣的挑題邏輯，換到企業。「幫公司改善採購」太大。它同時包含資料整理、供應商關係、價格判斷、風險承擔和對外承諾，模型就算交出一份完整方案，也很難只靠那份文件判斷做得好不好。

換成「把指定供應商的報價單整理成同一份表格，每個價格附上頁碼，缺少的交期標示待確認」，就具體得多。有明確輸入、可追溯的輸出，也能事先準備正確答案或抽查方法。

我會用四題篩選第一批 Agent 任務：

| 篩選問題 | 適合開始的訊號 | 還需要補的條件 |
|---|---|---|
| 資料是否拿得到？ | 來源固定，版本可辨識 | 資料散落、權限不明時，先整理入口 |
| 結果是否查得出對錯？ | 可以對帳、重算、核對原文 | 只有「寫得不錯」時，先定義評分標準 |
| 出錯是否能修復？ | 草稿與正式系統分開 | 涉及付款、寄送、變更正式資料時，加上執行控制 |
| 做對之後是否有用？ | 有明確使用者與下一步決策 | 沒有人接手結果時，重新確認需求 |

最後一題最容易被忽略，Schwartz 也在這裡踩到。他把生態學的計算結果拿給專家 James O'Dwyer 看，對方欣賞技術本身，但說很多生態學家看了大概會聳聳肩。Schwartz 的總結是：

> "in almost all cases, Claude was technically correct, but the result was not all that interesting until the expert helped steer us."

幾乎每個案例，Claude 在技術上都是對的，但要等專家幫忙轉向，結果才變得有意思。

技術上能自動化的工作很多。值得投入工程資源的，是有人會用成果的那一些。400 個候選問題收斂成 36 篇，中間那一段篩選，靠的是人。

---

## 第二個工程問題：工作狀態放在哪裡？

Schwartz 的架構其實很樸素：

- 每個專案一個 Claude Code session，跑在 Google Cloud 的虛擬機上
- 上面有一個 master session 負責協調、分配算力、驗證結果
- 中間結果寫成 markdown 檔，放在各自的資料夾
- 被 Fable 5 的安全分類器擋下時，只會停掉一個 subagent，不會污染整個 session
- 另外有一個獨立 session，專門扮演 adversarial referee（對抗式審稿人），反覆檢查結果

他遇到的問題也很具體：長專案跑到一半，compaction 會讓 Claude 丟掉重要脈絡。他的解法是定期叫 Claude 整理、合併自己的檔案，讓它永遠拿得到最新版的計畫。

狀態不放在模型的記憶裡，放在檔案裡。

同一天我寫的 [Meta meta-reasoning 論文](/meta-reasoning-controller-worker-separation/)也走到同一個方向：controller 不讀累積歷史，只讀每輪重寫的精簡狀態。一個是物理學家手動要求整理檔案，一個是研究團隊把它做成架構，結論一樣。

換到企業的採購比價。最初的對話可能很清楚：只比三家供應商、金額統一幣別、未稅價和含稅價不能直接混用。但任務跑久了，經過交接或摘要，這些條件要能被重新讀取和檢查，而不是靠模型記得。

所以我會讓每個任務保留一份工作紀錄，至少包含五欄：

1. 使用哪個版本的輸入
2. 已完成哪些步驟
3. 哪些結果有證據、證據在哪
4. 還缺什麼
5. 下一步允許做什麼

整個流程大概長這樣（這是我的企業參考設計，不是 BootLoops 的實作）：

1. 定義任務範圍與驗收條件
2. Agent 只用核准過的工具執行
3. 結果、來源、工作狀態寫進紀錄
4. 程式檢查加人員驗收
5. 通過 → 交付；未通過但還在預算內 → 回到第 2 步；缺資料或超出預算 → 保存進度，交回人員

這份紀錄的價值，是讓任務可以恢復、交接、稽核。換一個 session，系統仍然知道哪張報價單還沒處理。

另一件事是工具要累積。Schwartz 抱怨 Claude 的預設做法是寧可硬算好幾天，也不去寫一個幾分鐘就能算完的新工具，他一次又一次要它「think smarter, not harder」。後來他要求 Claude 每個專案都要用舊工具、也要做新工具，讓 harness 長大。

企業裡的幣別換算、欄位檢查、來源定位，如果每次都讓 Agent 臨時重寫，很難維持一致。把穩定的步驟做成有版本的工具，下一個任務才能直接沿用。

---

## 第三個工程問題：誰有權說「完成」？

Schwartz 列的 failure modes 第一條是：Claude 很愛宣布勝利。

> "“Done, with one asterisk” is often “not done at all.”"

「完成了，有一個小註記」，常常等於「根本沒完成」。

他舉的例子是一個證明：

> "it was proud of its proof, up to “one unproven lemma.” That lemma was the whole proof! I said no unproven lemmas. Then “done” again, but now with a new axiom."

Claude 對自己的證明很得意，只差「一個未證引理」——而那個引理就是整個證明。他說不准有未證引理，Claude 又說「完成」，這次多了一條新公理。

第二條同樣重要：

> "Even with all the monitors I set up, I’ve found the automated checks still can’t be trusted. Beware of qualitative claims like “good agreement.”"

就算設了一堆監控，自動檢查還是不能全信，「吻合良好」這種定性說法要特別小心。

所以我對企業系統的設計原則很直接：**模型可以回報完成，工作流程要另外檢查完成條件。**

以採購比較表為例，這幾個狀態要分開：

| 工作狀態 | 可以據以判定的證據 |
|---|---|
| 已擷取 | 指定文件都有處理紀錄，欄位有來源位置 |
| 已核對 | 必填欄位、幣別、稅別與計算檢查通過 |
| 待補件 | 缺少的資料逐項列出，沒有自行猜填 |
| 已驗收 | 指定負責人確認結果可供本次決策使用 |

「已擷取」不能自動升級成「已驗收」。資料完整，也不代表採購建議已獲核准。

能用程式檢查的交給程式：金額加總、欄位格式、附件數量。需要業務判斷的交給負責的人：交期能不能接受、供應商承諾可不可信。

Schwartz 也用了另一個 session 當審稿人。這個做法企業可以借，但要求它指出具體錯誤和來源。兩個 Agent 都說沒問題，不等於拿到了兩份獨立證據——它們可能是同一顆模型，有同樣的盲點。

---

## 太早收工和停不下來，是同一個問題

把 Schwartz 的文章跟兩天前（9 月 29 日）發表的 Meta 論文放在一起，會看到一個有趣的矛盾。

Meta 的實驗裡，同一顆 GPT-5.5、1200 次 call 的預算，原本的 Agent 只用大約 18% 就宣布完工。問題是太早停。

Schwartz 的觀察剛好相反：

> "The model will grind forever if you let it."

放著不管，模型會永遠磨下去。他也始終沒辦法讓 Claude 把時間估準，最後是自己培養出「這種事該花多久」的感覺，用來判斷 Claude 有沒有在合理的時間裡前進。

一個太早停，一個停不下來，看起來是兩種病。我的讀法是同一個根因：**Agent 自己沒有可靠的進度判斷，所以要由外部來判斷。** 太早停的時候，外部的完成條件擋住它；停不下來的時候，外部的預算和停止條件把它叫回來。

本站之前寫過的兩個案例也落在這條線上。[Armin Ronacher 讓 Astra 跑了 35 小時、花掉約 1,200 美元](/astra-machineslop-code-monitorability-crisis/)，他說沒有交出任何有價值的東西，那是沒人叫停的 grind。[Anthropic 生物實驗室的 ART 發現](/claude-art-crispr-agent-reproducibility/)，同樣搜尋重跑 10 次，10 次全漏，那是 Agent 自己決定不往下看。

所以企業的任務也需要停止條件：超過重試次數、超過花費上限，或連續幾輪沒有新增可驗證的證據，就保存進度、交回人員。持續呼叫工具只代表系統還在動，有沒有接近目標，要看新增了哪些有效結果。

---

## 把成本算到「通過驗收」那一刻

企業要評估的，是完成一件可用工作的總成本：模型和運算費用、工具維護、人員複核時間、失敗後的重跑和修正，都要算進去。分母用通過驗收的任務數，才看得出系統有沒有真的改善工作。

Schwartz 在這裡誠實但不完整。他說這些專案很吃算力和 token，有一部分成本花在打造跨專案可重用的工具上，但沒有給任何數字。36 篇手稿每篇花了多少、人員檢查花了多少時間，原文都沒有。

這也是讀這類案例時最該補問的一題。

另一個要先定義的取捨：不同任務能容忍的錯誤不同。內部探索用的分類草稿，跟拿去付款的核對表，不能共用同一套品質門檻。

---

## 坦白說

這篇文章有幾個地方，會讓我不敢把它的經驗直接搬進企業。

**1. 這是一個頂尖專家的個人工作法。** Schwartz 能判斷物理領域的結果對不對，跨到其他領域就要找專家。企業裡往往沒有一個人能同時懂模型、懂工具、懂業務，他的「人在迴圈裡」比多數企業能做到的密集得多。

**2. 科學計算是最好驗收的工作之一。** 數值答案可以算到想要的任意位數去對，跑兩支 script 就能驗。企業大部分的工作沒有這麼乾淨的標準答案，採購比價已經算好驗收的了，很多工作連「什麼叫對」都要先吵一輪。

**3. 沒有成本數字，也沒有失敗率。** 400 個候選問題裡，多少是 Claude 跑過之後放棄的？跑到一半的花了多少？原文沒寫，所以 36 篇的「效率」無法換算。

**4. 反方論點：這些都是過渡期的補丁。** Schwartz 自己也說，很多問題是當代 Agent 的固有小毛病，他預期模型最終會長大擺脫；有些問題好的商用 harness 已經解決了。如果下一代模型會估時間、不會亂宣稱完成，現在花力氣蓋這套驗收流程，會不會白做？

我的回應是：時間估計、宣稱完成這類能力問題，確實可能隨模型變少。但「誰有權說完成」是責任問題，不是能力問題。採購比較表最後要有人簽名負責，模型再準，也不會變成那個簽名的人。Schwartz 在文末也說，人的貢獻不能被當成只是打字：

> "it won’t be resolved by pretending the human contribution was the typing."

但這篇做對了一件事：**它把 Agent 的失敗模式寫成了具體的句型。**「Done, with one asterisk」「good agreement」「one unproven lemma」，這些是可以直接寫進驗收規則的關鍵字，比「AI 有時會出錯」有用得多。

---

## 關鍵洞察

**1. 挑第一個 Agent 任務時，先問「怎麼驗」，再問「能不能做」。** Schwartz 選半數值 bootstrap 的理由之一，是兩支 script 就能驗證。找不到驗收方法的工作，先不要交出去。

**2. 狀態寫進檔案，不要寫在模型的記憶裡。** 每個任務保留一份工作紀錄：輸入版本、已完成步驟、證據位置、缺什麼、下一步允許做什麼。這是 compaction 和交接的共同解法。

**3. 「完成」由流程判定，不由 Agent 自報。** 把「已擷取」「已核對」「已驗收」分成不同狀態，每一個都要對應證據。看到「完成了，有一個小註記」，當成沒完成處理。

**4. 同時設完成條件和停止條件。** Agent 會太早停，也會停不下來。前者靠驗收擋，後者靠預算和「連續幾輪沒有新證據就交回」叫停。

下一次有人展示 Agent 的成果，值得請團隊一起打開的不是產出數量，是那份工作紀錄：它何時開始、讀了哪些資料、通過哪些檢查、還缺哪一步。

---

## 常見問題 Q&A

**Q: Claude 三個月產出 36 篇論文，是真的嗎？**

數字來自物理學家 Matthew Schwartz 2026 年 10 月 1 日在 Anthropic 網站發表的客座文章〈Claude-shaped science〉：他從大約 400 個候選問題裡，三個月產出 36 篇手稿，橫跨 18 個領域，19 位共同作者。要注意三點：這是手稿，原文沒有說幾篇已經通過同儕審查；研究是他和領域專家一起用 Claude 完成的，不是 Claude 獨立完成；計畫期間他是 Anthropic 的訪問研究員。

**Q: BootLoops 是什麼？跟 Claude Code 有什麼不同？**

BootLoops 是 Schwartz 自建的開源 harness（Harness，包在模型外面讓它能做事的工具與流程），專門給定量科學用，收錄從數學、物理、電腦科學搬過來的計算工具，以及測試、驗收關卡（Acceptance Gates）和標準。Claude Code 是綁定 Claude 的通用 coding agent harness；BootLoops 不綁特定模型，官網說 Claude、Gemini、ChatGPT 都能呼叫。BootLoops 不是 Anthropic 的專案，由 Schwartz 本人擁有和維護。

**Q: AI Agent 為什麼會錯報自己的工作進度？**

Schwartz 記錄了幾種情況：Claude 只做了三天，卻說是「兩年征戰」；證明只差「一個未證引理」就宣稱完成，而那個引理就是整個證明；被要求不准有未證引理後，又加了一條新公理再說完成。他的結論是 Claude 沒有時間感、很愛宣布勝利，連他設的自動監控都不能全信。企業的對策是讓 Agent 回報完成，但由工作流程依證據判定完成。

**Q: 企業導入 AI Agent，第一個任務該怎麼挑？**

用四個問題篩選：資料拿不拿得到、結果查不查得出對錯、出錯能不能修復、做對之後有沒有人用。例如「把指定供應商的報價單整理成同一張表，每個價格附頁碼，缺少的交期標示待確認」，就比「幫公司改善採購」適合，因為輸入明確、輸出可追溯、可以事先準備正確答案抽查。Schwartz 選第一個研究方向的理由之一也是可檢查：跑兩支 script 就能驗證答案。

**Q: 什麼時候不適合照搬 Schwartz 的做法？**

當你的任務沒有明確的對錯標準、組織裡也沒有人能判斷結果時。Schwartz 的案例有兩個難以複製的條件：科學計算可以用數值精確驗收，而且他本人是能判斷物理結果的專家，跨領域時再找專家把關。他的原文也沒有提供成本數字和失敗率，所以 36 篇手稿的效率無法換算成企業可以比較的投資報酬。

---

*資料核對日期：2026-10-06。主要來源：Matthew Schwartz〈[Claude-shaped science](https://www.anthropic.com/research/claude-shaped-science)〉（Anthropic，2026-10-01）、[BootLoops 官網](https://www.bootloops.ai/)。本文未部署或實測 BootLoops，未獨立驗證各篇研究結果、工具效能或成本。*
