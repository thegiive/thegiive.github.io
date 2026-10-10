---
layout: post
title: "一個門外漢用 AI Agent 一週打穿韓國七家金融機構：被打的不是核心系統，是忘了鎖的後院小門"
date: 2026-10-10 09:00:00 +0800
permalink: /crowdstrike-artex-korea-banks-open-directory-claude-code/
tags: [CrowdStrike, ARTEX, Claude Code, DeepSeek, 資安, 紅隊測試, Agent, Harness, 韓國金融, 無護欄模型]
categories: [AI Agent]
image: /assets/images/crowdstrike-artex-korea-banks-open-directory-cover.png
description: "9 月底到 10 月初，韓國至少七家金融機構被同一波攻擊打穿，合計約 6.7 萬筆資料外洩，光新韓銀行就約 2.5 萬名客戶，欄位包含年收入和貸款額度。CrowdStrike 回溯找到攻擊者之後，發現對方看起來不是駭客組織，而是一個門外漢年輕人：伺服器開著公開目錄，Claude Code 的 session 紀錄、問 Claude 去哪裡銷贓的對話、連求職履歷都攤在那裡。我之前很多次說，有了 AI 等於人人都有了槍。這篇拆三件事：他的 Agent 框架長什麼樣、為什麼被打穿的全是邊緣系統、以及企業資安為什麼該從一年一次的滲透測試，變成每天在跑的紅軍 Agent。"
author: Wisely Chen
faq:
  - question: "ARTEX 是什麼？"
    answer: "ARTEX 是一個中國開發者在 2026 年 7 月 26 日放上 GitHub 的開源「AI 自主滲透測試系統（autonomous penetration testing system）」，採 AGPL-3.0 授權，repo 自述是百度 agent+ 攻防挑戰賽的冠軍專案。它用 Go 寫後端、Next.js 寫前端，填入 Anthropic 或 OpenAI 的 API key 就能讓 LLM 自動做資產探索、漏洞掃描和工具呼叫，介面上有攔截審批和人在環路對話等功能。原始 repo 在韓國金融機構攻擊事件曝光後已刪除，但 fork 仍可在 GitHub 上找到。"
  - question: "CrowdStrike 是怎麼找到攻擊者的？"
    answer: "攻擊者的伺服器開著公開目錄（open directory），意思是沒有設存取限制、任何人輸入網址就能瀏覽的檔案列表。CrowdStrike 在 2026 年 10 月 7 日的報告裡說，他們在裡面找到 Claude Code 的 session 紀錄、CLAUDE.md、Claude memory 檔和 ARTEX 的設定檔，直接看到了攻擊者的手法、目標和對話內容。攻擊者用 Claude Code 當指揮介面，但模型是 DeepSeek v4.1-flash，另外換過 GLM-5.3 和 Grok 4.6；他還請 Claude 幫忙找 Telegram 資料交易群，以及寫一份列入這次攻擊成果的資安研究員履歷。"
  - question: "這次韓國有哪些金融機構被打、外洩了多少資料？"
    answer: "依韓媒與日本資安部落格 piyolog 的彙整，2026 年 9 月底到 10 月初共有七家金融機構確認資料外洩：新韓、KB 國民、Hana、BNK 釜山四家銀行，Yegaram、Welcome 兩家儲蓄銀行，以及現代資本，合計約 6.7 萬筆。最多的是 Yegaram 儲蓄銀行約 4 萬名客戶，其次是新韓銀行約 2.5 萬名客戶，欄位包含年收入和貸款額度。目前沒有盜轉帳戶等直接金錢損失的報導，主要風險是後續的詐騙等二次損害。"
  - question: "韓國銀行這次是被什麼漏洞打穿的？"
    answer: "不是新型漏洞。依韓國金融監督院的描述，攻擊者進入新韓銀行給貸款仲介用的查詢服務，用隨機輸入試出有效的客戶編號，再拿這些編號到其他服務集中查詢資料，性質是「查詢與收集」而不是打進資料庫。這類「可猜的識別碼加上沒把關的查詢端點」，在 2010 年的 OWASP Top 10 就被列為 A4 項目（Insecure Direct Object References，IDOR）。被打的多半是仲介入口、員工行動辦公系統這類邊緣系統，不是核心銀行系統。"
  - question: "企業該怎麼防範 AI Agent 驅動的攻擊？"
    answer: "這次攻擊沒有用到新技術，AI 改變的是速度：agent 會不眠不休地把每一個對外端點都試一遍。所以第一步是把資產盤點範圍擴大到任何查得到客戶資料的系統，包括仲介入口、員工系統和第三方程式。第二步是把一年一次的弱點掃描和滲透測試（penetration testing），改成持續運作的紅軍 Agent，在書面授權和限定範圍下每天找出被忽略的風險。閉源模型的安全護欄（guardrail）常會擋下黑箱攻擊測試，所以防守方也需要準備地端的無護欄模型作為工具。  ---"
---

9 月底到 10 月初，韓國至少七家金融機構被同一波攻擊打穿。

資安公司回溯找到攻擊者之後，大家都驚呆了。看起來不是什麼駭客組織，而是一個門外漢年輕人。

我之前很多次說，有了 AI，等於人人都有了槍，就連路邊的年輕人都可以隨機開幾槍。四月寫 [Mythos](/anthropic-mythos-project-glasswing-cyber-inflection-point/) 的時候，我說它不是核武，是一把 AK 送給路人。八月 [Qwen3.8 的無護欄版本](/qwen38-27b-abliteration-three-days-safety-paradox/)出來，我說既然大家都有槍，你家裡就被迫也要放一把。

這次，路邊的年輕人拿著槍去攻擊韓國銀行了。

還真的拿到了客戶資料。光新韓銀行就約 2.5 萬名客戶，欄位包含年收入和算出來的貸款額度，其中 66 件連身分證字號一起出去。

先講清楚：這篇是依 [CrowdStrike 報告](https://www.crowdstrike.com/en-us/blog/unknown-threat-actor-uses-artex-to-target-south-korean-finance/)和韓、日兩邊的公開報導做的分析，我沒有接觸過任何一手鑑識資料。受害機構的數字來自韓媒與日本資安部落格 piyolog 的彙整，CrowdStrike 的報告本身沒有點名任何一家。

<nav class="post-toc" markdown="1">
**目錄**

* 目錄
{:toc}
</nav>

---

## 30 秒定位

| 項目 | 內容 |
|------|------|
| 報告 | CrowdStrike，2026-10-07，"Unknown Threat Actor Uses AI-Driven ARTEX to Target South Korean Finance" |
| 活動期間 | 9 月底到 10 月初 |
| 受害 | 韓媒彙整七家金融機構，合計約 6.7 萬筆；Yegaram 儲蓄銀行約 4 萬、新韓銀行約 2.5 萬最多 |
| 被打的系統 | 仲介用查詢服務、員工行動辦公系統等邊緣系統，不是核心銀行系統 |
| 指揮介面 | Claude Code |
| 模型 | 主力 DeepSeek v4.1-flash（走中轉），其他 session 換過 GLM-5.3 和 Grok 4.6 |
| 執行層 | ARTEX，中國開發者 7 月 26 日放上 GitHub 的開源「AI 自主滲透測試系統」 |
| 歸因 | 沒有連到任何已知組織；中等信心判斷為中文使用者、財務動機 |

---

## 為什麼知道是門外漢

因為他的防守意識太差。

CrowdStrike 順著攻擊用的基礎設施摸回去，發現他的伺服器開著公開目錄（open directory），意思是沒鎖、誰都能進去翻的檔案夾。裡面有：

- Claude Code 的 session 紀錄
- CLAUDE.md（裡面是中文寫的滲透測試指令）
- Claude 的 memory 檔
- 開源滲透工具 ARTEX 的設定檔

他怎麼打的、打了誰、想去哪裡賣，全部攤在那裡。

他甚至不知道怎麼銷贓，還跑去問 Claude。CrowdStrike 轉述了幾段：

- 韓國外洩的資料通常在哪裡賣
- 請 Claude 幫忙找韓國的 Telegram 資料交易群
- 請 Claude 寫一份資安研究員履歷，而且指定要把這次 ARTEX 活動的戰果寫成 bullet

另外幾個 session 在研究 Telegram 上一個 NFT 禮物市集的漏洞，還有一個疑似中國的支付平台。

履歷 prompt 裡有姓名、電話、Telegram 帳號、學歷、所在地。年紀寫 26 歲，但他一開始給的出生日期是 2007 年，換算下來才 19 歲。CrowdStrike 的措辭很保守：這些資料很可能是攻擊者本人的，但目前的資訊還不能確定。這篇不轉載任何實際個資。

這是 AI 時代最有趣的風景。攻擊用的是最先進的 AI 框架，打進去的是金融業，基礎知識卻跟一個初學者一樣。**標準的 script kiddie（腳本小子），只是手上的工具換成了 Agent。**

順帶一提，這對每個在用 agent 的人也是提醒。session 紀錄和 memory 檔記得你叫它做過的每一件事。對營運方，它是[可解釋性](/ai-agent-explainability-operational-trust/)的基礎；落到別人手上，就是一份寫好的認罪書。一月那篇 [Clawdbot 裸奔事件](/clawdbot-exposed-500-servers-security-disaster/)，是近 1,000 台 agent 因為預設綁 0.0.0.0 暴露在公網。這次暴露的，是攻擊者自己的 agent 工作目錄。

---

## 他的 Agent 框架是？

session 紀錄都攤開了，所以框架很容易拼出來。

| 層 | 內容 |
|----|------|
| 指揮介面（harness） | Claude Code |
| 模型 | DeepSeek v4.1-flash 為主，透過一個 CrowdStrike 判斷是 API 中轉或轉售商的網域；其他 session 換過 GLM-5.3 和 Grok 4.6 |
| 執行層 | ARTEX，開源 AI 自主滲透測試系統 |

ARTEX 不是玩具。原 repo 現在打開是 404，fork 還在。從 fork 的 README 看，它是 Go 後端加 Next.js 前端、PostgreSQL 存資料，LLM 設 ANTHROPIC_API_KEY 或 OPENAI_API_KEY 就能跑，也可以自訂 provider、model 和 base_url。UI 有 Agent 管理、攔截審批、人在環路對話、流量錄製、資產覆蓋圖，Docker 映像內建 nmap 和 playwright。repo 自述是百度 agent+ 攻防挑戰賽冠軍專案，AGPL-3.0 授權。這是一個做得很完整的紅隊產品，被拿去打真的銀行。

指揮介面是 Claude Code，但模型一個都不是 Claude。CrowdStrike 沒說原因，我猜是 Claude 的安全護欄會擋。這剛好驗證了[從 Prompt 到 Harness 的三次中心遷移](/agent-harness-three-migrations-mechanism/)那篇的結論：模型可以換，harness 才是生產力的本體。連犯罪者都懂。

還有一個細節。他的 DeepSeek 是走中轉打的。四月我寫過 [UCSB 那篇《Your Agent Is Mine》](/llm-proxy-relay-security-your-agent-is-mine-ucsb/)，428 個 LLM 中轉裡有 17 個在偷 AWS 憑證。這個攻擊者發出去的每一個 prompt，包括要打哪家銀行、想在哪裡賣，中轉商全部看得到。沒鎖的目錄被 CrowdStrike 撿到了，中轉那一份被誰撿走，沒人知道。

---

## 邊緣系統的資安治理才是問題

話說回來，這次被打的不是核心銀行系統。

看起來都是邊緣系統，或是外包、第三方的支援系統。CrowdStrike 原文點出兩類：一家銀行給金融仲介用的貸款進度查詢服務，另一家的員工內部行動辦公支援系統。依韓媒報導，前者是新韓，後者是 KB 國民。Yegaram 儲蓄銀行則說，入侵是透過一套外部解決方案程式的遠端漏洞。

被打爆的原因不是 AI 太強大、大顯神威，而是這些系統太糟糕。

看新韓的攻擊做法，簡單到令人髮指。依韓國金融監督院的描述：

1. 隨機輸入，試出有效的客戶編號
2. 拿這些編號集中查詢撈資料

性質是「查詢與收集」，不是打進資料庫。這是 2010 年的 OWASP Top 10 就列為 A4 的老問題（Insecure Direct Object References，IDOR）：可猜的識別碼，加上沒把關的查詢端點。**光是查詢端點擋不住亂試客戶編號，就已經是死罪。**

依 piyolog 彙整的韓媒數字，七家機構是這樣的：

| 機構 | 發現日 | 外洩對象 | 筆數 |
|------|--------|---------|------|
| Yegaram 儲蓄銀行 | 9/30 | 客戶 | 約 40,000 |
| 新韓銀行 | 9/29 | 客戶 | 約 25,000 |
| Welcome 儲蓄銀行 | 10/5 | 企業網銀註冊用戶 | 2,117 |
| 現代資本 | 10/3 | 貸款招攬人員 | 146 |
| KB 國民銀行 | 9/30 | 客戶與員工 | 119 |
| Hana 銀行 | 9/30 | 客戶 | 89 |
| BNK 釜山銀行 | 10/2 | 外包開發人員 | 11 |

攻擊發生在 9 月 27 日到 30 日，韓方整理出 28 個 IP，多數經 VPN 進來。金融保安院回溯新韓的 log 時，在攻擊伺服器的 HTML title 看到「ARTEX-自主渗透测试控制台」。官方的措辭很謹慎：不是 AI 自主攻擊，是攻擊者使用了 ARTEX 這個工具。

### AI 沒有讓他變強，是讓他變快

拿掉 AI 三個字，這就是一則普通的資料外洩新聞。沒有 0-day，沒有新技術，人是 opsec 爛到把工作目錄開給全世界看的新手。

這個說法有一半是對的，而對的那一半正是重點。AI 沒有讓他變強，真正的問題是 AI 掃這些小系統的漏洞變得超快。CrowdStrike 報告的結語，關鍵字也是 tempo：

> "CrowdStrike Intelligence assesses that adversaries will likely continue to experiment with implementing AI tooling in their operations to enhance their operational tempo and capabilities."

攻擊方會繼續把 AI 工具放進作業流程，拉高作戰節奏和能力。

金融業的核心系統應該是沒問題的。但架不住一個事業體附帶的系統太多，一定有很多子系統不在資安的關注範圍。

這麼 low 的做法，居然一週內打進韓國七家機構，就知道業界的洞到底有多少。以前大部分系統沒被打，不是因為安全，是因為沒人有耐心去試。**現在有了 AI，耐心是免費的。** 一個年輕人就可以搞定七家。

漏洞看起來很低級，但受傷的是真實的大機構，外洩的是真實的客戶資料。年收入、貸款額度加上電話，正好是電話詐騙最好用的材料。韓國金融監督院把到 11 月 6 日為止定為「個資外洩二次損害特別應對期間」，要防的正是這個。

---

## 那我們怎麼做

攻擊方用 AI 掃漏洞，那 IT 為什麼不先用紅軍 AI 去查？

卡住的地方在護欄。叫 Claude、OpenAI 這類閉源模型讀程式碼找 bug，也就是白箱掃描，沒有問題。但黑箱測試的本質是模擬攻擊者，要真的去戳、去試、去送惡意 payload，護欄常常會判定你在攻擊而拒絕。所以你更需要準備地端的無護欄 AI 來防護。

八月底我就用 RTX 5090 加地端無護欄的 Qwen3.8-27B，在朋友邀請下幫他的網站做了一次[黑箱紅軍](/uncensored-ai-red-team-black-box-vibe-coding/)：只給一個 URL，兩小時抓到十個問題。他的網站在那之前已經用 AI 白箱掃過好幾輪。

要知道，現在的 agent 不會跳過無聊的端點，它會每一個都試。防守方的問題不再是「核心系統安全嗎」，而是「有哪些小系統查得到關鍵資料，而我們忘了它存在」。

我覺得這才是 AI 時代企業資安最大的轉變。

以前弱點掃描和滲透測試是一個專案，大家差不多一年做一次。未來應該是一個持續運作的 Agent：每天幫你找出被忽略的風險，經過授權、控制測試範圍，再交給工程師修補。

攻擊方已經是這樣在跑了。這次的攻擊者正是把 ARTEX 掛在伺服器上，讓 agent 一個端點一個端點地試。防守方如果還是一年掃一次，等於讓對方天天巡邏，自己一年才點一次名。

AI 時代，槍已經發到每個人手上了。這七家金融機構輸在忘了鎖後院的小門，就被路邊的年輕人混進來了。

---

## 坦白說

這篇有幾個地方的宣稱強度要打折。

第一，七家機構的數字是韓媒和 piyolog 的彙整，CrowdStrike 的報告沒有點名任何一家，也沒有給外洩筆數。把七家放在同一波攻擊裡，是韓國金融保安院的 log 回溯加上時間重疊得出的。其中 Yegaram 的入侵路徑跟新韓不同，它跟 ARTEX 的關聯沒有被單獨證實。

第二，「門外漢」「年輕人」「一個人」都是推論。CrowdStrike 只說沒有連到已知組織、中等信心是中文使用者、財務動機。履歷上的年紀是 19 或 26，但 CrowdStrike 自己也說這些個資還不能確定屬於攻擊者。說他是門外漢，主要依據是他的防守意識，不是那份履歷。

第三，ARTEX 的架構我只看到 fork 的 README，原 repo 已經刪了。社群貼文說它是「一個 agent 規劃、一個 agent 執行」的架構，CrowdStrike 原文沒有這樣描述，我也沒辦法確認，所以這篇沒有這樣寫。

第四，持續運作的紅軍 Agent 有代價。無護欄模型本身就是兩用工具，用在自己的系統上，一定要有書面授權、限定測試範圍、隔離環境、留稽核紀錄。我那次兩小時的黑箱紅軍，是朋友邀請、而且他已經準備好請資安公司付費檢測的情況下做的。它是模擬考，不能取代專業的滲透測試。

第五，「門檻降低」這個主張只有一個案例支撐。一個案例可以說明這種事會發生，不能說明這種事變多了。

---

## 關鍵洞察

**被打穿的是後院小門，不是金庫。** 資產盤點的範圍要從「核心系統」改成「任何查得到客戶資料的東西」，包括仲介入口、員工系統、外包和第三方程式。

**AI 改變的是耐心的成本。** 這個案子沒有任何新攻擊技術。以前靠「沒人有耐心去試」擋住的弱點，現在會被一個不眠不休的 agent 一個一個試出來。

**滲透測試要從年度專案變成持續運作的 Agent。** 攻擊方已經是天天巡邏，防守方一年點一次名撐不住。前提是授權、範圍和稽核紀錄先設計好。

**地端無護欄 AI 是防守方的儲備。** 閉源模型的護欄會擋下黑箱攻擊測試。既然攻擊者手上已經有槍，防守方至少要確保自己拿得到同等的工具。

---

## 常見問題 Q&A

**Q: ARTEX 是什麼？**

ARTEX 是一個中國開發者在 2026 年 7 月 26 日放上 GitHub 的開源「AI 自主滲透測試系統（autonomous penetration testing system）」，採 AGPL-3.0 授權，repo 自述是百度 agent+ 攻防挑戰賽的冠軍專案。它用 Go 寫後端、Next.js 寫前端，填入 Anthropic 或 OpenAI 的 API key 就能讓 LLM 自動做資產探索、漏洞掃描和工具呼叫，介面上有攔截審批和人在環路對話等功能。原始 repo 在韓國金融機構攻擊事件曝光後已刪除，但 fork 仍可在 GitHub 上找到。

**Q: CrowdStrike 是怎麼找到攻擊者的？**

攻擊者的伺服器開著公開目錄（open directory），意思是沒有設存取限制、任何人輸入網址就能瀏覽的檔案列表。CrowdStrike 在 2026 年 10 月 7 日的報告裡說，他們在裡面找到 Claude Code 的 session 紀錄、CLAUDE.md、Claude memory 檔和 ARTEX 的設定檔，直接看到了攻擊者的手法、目標和對話內容。攻擊者用 Claude Code 當指揮介面，但模型是 DeepSeek v4.1-flash，另外換過 GLM-5.3 和 Grok 4.6；他還請 Claude 幫忙找 Telegram 資料交易群，以及寫一份列入這次攻擊成果的資安研究員履歷。

**Q: 這次韓國有哪些金融機構被打、外洩了多少資料？**

依韓媒與日本資安部落格 piyolog 的彙整，2026 年 9 月底到 10 月初共有七家金融機構確認資料外洩：新韓、KB 國民、Hana、BNK 釜山四家銀行，Yegaram、Welcome 兩家儲蓄銀行，以及現代資本，合計約 6.7 萬筆。最多的是 Yegaram 儲蓄銀行約 4 萬名客戶，其次是新韓銀行約 2.5 萬名客戶，欄位包含年收入和貸款額度。目前沒有盜轉帳戶等直接金錢損失的報導，主要風險是後續的詐騙等二次損害。

**Q: 韓國銀行這次是被什麼漏洞打穿的？**

不是新型漏洞。依韓國金融監督院的描述，攻擊者進入新韓銀行給貸款仲介用的查詢服務，用隨機輸入試出有效的客戶編號，再拿這些編號到其他服務集中查詢資料，性質是「查詢與收集」而不是打進資料庫。這類「可猜的識別碼加上沒把關的查詢端點」，在 2010 年的 OWASP Top 10 就被列為 A4 項目（Insecure Direct Object References，IDOR）。被打的多半是仲介入口、員工行動辦公系統這類邊緣系統，不是核心銀行系統。

**Q: 企業該怎麼防範 AI Agent 驅動的攻擊？**

這次攻擊沒有用到新技術，AI 改變的是速度：agent 會不眠不休地把每一個對外端點都試一遍。所以第一步是把資產盤點範圍擴大到任何查得到客戶資料的系統，包括仲介入口、員工系統和第三方程式。第二步是把一年一次的弱點掃描和滲透測試（penetration testing），改成持續運作的紅軍 Agent，在書面授權和限定範圍下每天找出被忽略的風險。閉源模型的安全護欄（guardrail）常會擋下黑箱攻擊測試，所以防守方也需要準備地端的無護欄模型作為工具。

---

## 來源

- CrowdStrike，[Unknown Threat Actor Uses AI-Driven ARTEX to Target South Korean Finance](https://www.crowdstrike.com/en-us/blog/unknown-threat-actor-uses-artex-to-target-south-korean-finance/)，2026-10-07
- piyolog，[韓国の金融機関で相次いだ不正アクセスについてまとめてみた](https://piyolog.hatenadiary.jp/entry/2026/10/06/103019)，2026-10-06
- 聯合新聞（經 Daum），[신한은행 "해킹으로 2만5000명 개인정보 유출" 연소득·대출정보 포함](https://v.daum.net/v/20261001123012747)，2026-10-01
- Daum，[신한은행에 '중국어 AI 침투' 흔적…해킹 공포 금융권 확산](https://v.daum.net/v/20261002192945588)，2026-10-02
- MTN，[저축은행도 뚫렸다… 예가람저축은행, 고객 4만 명 개인정보 유출](https://news.mtn.co.kr/news-detail/2026100309010338927/share-modal)，2026-10-03
- Security Affairs，[AI-Driven tool ARTEX used in attacks against South Korean Banks](https://securityaffairs.com/200661/hacking/ai-driven-tool-artex-used-in-attacks-against-south-korean-banks.html)
- OWASP，[Top 10 2010 A4: Insecure Direct Object References](https://wiki.owasp.org/index.php/Top_10_2010-A4)
- ARTEX fork README（原 repo Autumn-27/ARTEX 已刪除）
