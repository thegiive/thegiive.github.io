---
layout: post
title: "他用 Claude Code 指揮 DeepSeek 打穿韓國七家金融機構，然後把整個 session 紀錄放在公開目錄"
date: 2026-10-10 09:00:00 +0800
permalink: /crowdstrike-artex-korea-banks-open-directory-claude-code/
tags: [CrowdStrike, ARTEX, Claude Code, DeepSeek, 資安, Agent, Harness, 韓國金融, 中轉]
categories: [AI Agent]
image: /assets/images/crowdstrike-artex-korea-banks-open-directory-cover.png
description: "我之前很多次說，有了 AI，等於人人都有了槍，就連路邊的年輕人都可以開幾槍。這次，路邊的年輕人拿了槍去攻擊銀行，還得手了。9 月底到 10 月初，韓國至少七家金融機構遭同一波攻擊，新韓銀行外洩約 2.5 萬人的資料，欄位包含年收入和貸款額度。CrowdStrike 10 月 7 日公布追查結果：攻擊者的伺服器開著公開目錄，裡面是 Claude Code 的 session 紀錄、CLAUDE.md、memory 檔和開源滲透工具 ARTEX 的設定檔，連他請 Claude 寫的求職履歷都在。這篇拆三件事：這套技術棧為什麼能讓一個人跑出一個團隊的節奏、漏洞本身其實老到不行、以及讓他被抄家的那些檔案，正是 Agent 要能做事就必須留下的東西。"
author: Wisely Chen
faq:
  - question: "ARTEX 是什麼？"
    answer: "ARTEX 是一個中國開發者在 2026 年 7 月 26 日放上 GitHub 的開源「AI 自主滲透測試系統（autonomous penetration testing system）」，採 AGPL-3.0 授權，repo 自述是百度 agent+ 攻防挑戰賽的冠軍專案。它用 Go 寫後端、Next.js 寫前端，填入 Anthropic 或 OpenAI 的 API key 就能讓 LLM 自動做資產探索、漏洞掃描和工具呼叫，介面上有攔截審批和人在環路對話等功能。原始 repo 在韓國銀行攻擊事件曝光後已刪除，但 fork 仍可在 GitHub 上找到。"
  - question: "CrowdStrike 是怎麼找到攻擊者的？"
    answer: "攻擊者的伺服器開著公開目錄（open directory），意思是沒有設存取限制、任何人輸入網址就能瀏覽的檔案列表。CrowdStrike 在 2026 年 10 月 7 日的報告裡說，他們在裡面找到 Claude Code 的 session 紀錄、CLAUDE.md、Claude memory 檔和 ARTEX 的設定檔，直接看到了攻擊者的手法、目標和對話內容，包括他請 Claude 幫忙找 Telegram 資料交易群，以及寫一份列入這次攻擊成果的資安研究員履歷。"
  - question: "這次攻擊用了什麼 AI 模型？"
    answer: "依 CrowdStrike 報告，主力模型是 DeepSeek v4.1-flash，而且是透過一個被判斷為 API 中轉或轉售商的網域存取；其他 Claude Code session 裡則用了智譜的 GLM-5.3 和 xAI 的 Grok 4.6。指揮介面是 Anthropic 的 Claude Code，但沒有證據顯示用了任何 Claude 模型。"
  - question: "韓國銀行這次是被什麼漏洞打穿的？"
    answer: "不是新型漏洞。依韓國金融監督院的描述，攻擊者先無授權進入新韓銀行手機版網站上給貸款募集人用的查詢服務，用隨機輸入試出有效的客戶編號，再拿這些編號到其他服務集中查詢資料，性質是「查詢與收集」而不是打進資料庫。KB 國民銀行被打的則是員工用的內部行動辦公支援系統。這類「不該被匿名存取的端點加上可猜的識別碼」早在 2010 年的 OWASP Top 10 就被列為 A4 項目，是老問題。"
  - question: "用 Claude Code 的一般開發者該注意什麼？"
    answer: "Claude Code 這類工具會在本機留下 session 紀錄、CLAUDE.md 指令檔和 memory 檔，內容是你叫它做過的每一件事。這些檔案不會被 .gitignore 範本或 secret scanner 處理，但敏感程度等於工作日誌加 .env。比較保守的做法是把整個工作目錄當 SSH key 等級看待：不放進共用機器、不進 repo、不放在任何有對外服務的主機上。  ---"
---

我之前很多次說，有了 AI，等於人人都有了槍，就連路邊的年輕人都可以開幾槍。那我們更需要自保。

這次，路邊的年輕人拿了槍去攻擊銀行了。

還得手了。

這個預言我寫過兩次。四月寫 [Mythos](/anthropic-mythos-project-glasswing-cyber-inflection-point/) 的時候，我說它不是核武，是一把 AK 送給路人。八月 [Qwen3.8 的無護欄版本](/qwen38-27b-abliteration-three-days-safety-paradox/)出來，我說既然大家都有槍，你家裡就被迫也要放一把。

9 月底到 10 月初，韓國至少七家金融機構被同一波攻擊打穿。新韓銀行 10 月 1 日公布，約 2.5 萬名客戶的資料外洩，欄位包含年收入和算出來的貸款額度，其中 66 件連身分證字號一起出去。

為什麼說是年輕人？因為他的防守意識差到不像老手。CrowdStrike 順著這波攻擊用的基礎設施摸回去，發現他的伺服器開著公開目錄，任何人輸入網址就能進去翻。裡面有 Claude Code 的 session 紀錄、CLAUDE.md、Claude 的 memory 檔，還有開源滲透測試工具 ARTEX 的設定檔。他怎麼打的、打了誰、想去哪裡賣，全部攤在那裡。

連個人資料都在裡面。他請 Claude 幫他寫一份資安研究員履歷，把這次的戰果寫成 bullet，prompt 裡附上姓名、電話、Telegram 帳號、學歷、所在地。年紀寫 26 歲，但他一開始給的出生日期是 2007 年，換算下來才 19 歲。CrowdStrike 的措辭很保守：這些資料很可能是攻擊者本人的，但目前的資訊還不能確定。不管是 19 還是 26，這都不是一個職業駭客會留下的東西。

這件事在中文社群被當笑話傳：用的是最先進的 AI 框架，基礎防護卻跟一個初學者一樣，代表他根本就是門外漢。笑點是真的。但我讀完 [CrowdStrike 原文](https://www.crowdstrike.com/en-us/blog/unknown-threat-actor-uses-artex-to-target-south-korean-finance/)和韓、日兩邊的媒體整理之後，覺得笑完之後有三件事值得認真看：這個人的技術棧為什麼能讓一個人跑出一個團隊的節奏；他打的漏洞其實老到不行；還有，讓他被抄家的那些檔案，正是 Agent 要能做事就必須留下的東西。

先講清楚：這篇是依 CrowdStrike 報告和公開報導做的分析，我沒有接觸過任何一手鑑識資料。受害機構的數字來自韓媒與日本資安部落格 piyolog 的彙整，不是 CrowdStrike 提供的。

<nav class="post-toc" markdown="1">
**目錄**

* 目錄
{:toc}
</nav>

---

## 30 秒定位

| 項目 | 內容 |
|------|------|
| 報告 | CrowdStrike，2026-10-07，標題 "Unknown Threat Actor Uses AI-Driven ARTEX to Target South Korean Finance" |
| 活動期間 | 9 月底到 10 月初 |
| 滲透工具 | ARTEX，中國開發者 7 月 26 日放上 GitHub 的開源「AI 自主滲透測試系統」，AGPL-3.0 |
| 指揮介面 | Claude Code（公開目錄裡有 session 紀錄、CLAUDE.md、memory 檔） |
| 模型 | 主力 DeepSeek v4.1-flash，透過一個 CrowdStrike 判斷是 API 中轉或轉售商的網域；其他 session 換成 GLM-5.3 和 Grok 4.6 |
| 基礎設施 | 主要在一個香港 IP 上，ARTEX 跑在另一台機器，另外列了九個 proxy IP |
| 受害 | 韓媒彙整至少七家金融機構，新韓銀行約 2.5 萬人為最大宗 |
| 歸因 | 沒有連到任何已知組織；中等信心判斷為中文使用者、財務動機 |

---

## 他的「公司」長什麼樣

把公開目錄裡的東西拼起來，這個人的工作環境是這樣的。

**指揮層是 Claude Code。** CrowdStrike 在目錄裡找到的是 Claude Code 的 session 紀錄、一份 CLAUDE.md（裡面是中文寫的滲透測試指令），還有 Claude 的 memory 檔。換句話說，他是坐在 Claude Code 的終端機裡發號施令的。

**模型不是 Claude。** 主力是 DeepSeek v4.1-flash，而且是透過一個 CrowdStrike 判斷是 API 中轉或轉售商的網域打的。其他 Claude Code session 裡換成 GLM-5.3 和 Grok 4.6。一個 Anthropic 做的 harness，跑的是三家別人的模型。

**執行層是 ARTEX。** 原 repo 現在打開是 404，fork 還在。從 fork 的 README 看，它是 Go 後端加 Next.js 前端、PostgreSQL 存資料，LLM 設 ANTHROPIC_API_KEY 或 OPENAI_API_KEY 就能跑，也可以自訂 provider、model 和 base_url。UI 有 Agent 管理、LLM 配置、攔截審批、人在環路對話、流量錄製、資產覆蓋圖，支援接遠端 MCP，Docker 映像內建 nmap 和 playwright。repo 自述是百度 agent+ 攻防挑戰賽冠軍專案。

這不是一個玩具。這是一個做得很完整的、給藍隊和紅隊用的產品，只是被拿去打真的銀行。

**然後是那些 session 裡的對話。** CrowdStrike 轉述了幾段：他問 Claude，韓國外洩的資料通常在哪裡賣；請 Claude 幫忙找韓國的 Telegram 資料交易群；請 Claude 寫一份資安研究員履歷，而且指定要把這次 ARTEX 活動的成果寫成 bullet。履歷裡有姓名、電話、Telegram 帳號、年齡、學歷、所在地。另外幾個 session 在研究一個 Telegram 上的 NFT 禮物市集的漏洞，還有一個疑似中國的支付平台。

**他把銷贓和求職交給同一個助理，而且助理的工作紀錄放在公開目錄。**

---

## 漏洞本身老到不行

這波攻擊的技術含量，跟 AI 的名號不成比例。

依韓媒報導，新韓銀行被打的是手機版網站上給貸款募集人用的查詢服務。攻擊者先無授權進了這個服務，拿到客戶編號，再去其他服務撈資料。金融監督院的描述是：用隨機輸入試出有效的客戶編號，再集中查詢。性質是「查詢與收集」，不是打進資料庫。

這是 2010 年的 OWASP Top 10 就列為 A4 的那類問題（Insecure Direct Object References）：一個不該被匿名存取的端點，加上一個可以被猜的識別碼。

KB 國民銀行那邊被打的是員工用的內部行動辦公支援系統。CrowdStrike 的原文也只點出這兩類系統：一家銀行的貸款進度查詢服務（給金融仲介用），另一家的員工內部行動辦公支援系統。

依 piyolog 彙整的韓媒數字，被波及的機構是這樣的：

| 機構 | 發現日 | 外洩筆數 |
|------|--------|---------|
| 新韓銀行 | 9/29 | 約 25,000 |
| Yegaram 儲蓄銀行 | 9/30 | 約 40,000 |
| Welcome 儲蓄銀行 | 10/5 | 2,117 |
| 現代資本 | 10/3 | 146 |
| KB 國民銀行 | 9/30 | 119 |
| Hana 銀行 | 9/30 | 89 |
| BNK 釜山銀行 | 10/2 | 11 |

攻擊發生在 9 月 27 日到 30 日，韓方整理出 28 個 IP，多數經 VPN 進來。金融保安院回溯新韓的 log 和攻擊來源 IP 時，發現那台伺服器的 HTML title 寫著「ARTEX-自主渗透测试控制台」。官方的措辭很謹慎：不是 AI 自主攻擊，是攻擊者使用了 ARTEX 這個 AI 工具。

所以這個故事裡，AI 沒有發明任何新攻擊。沒有 0-day，沒有繞過什麼防禦。它做的事情是：把「找到一個沒鎖的邊緣端點、猜識別碼、把資料一筆一筆撈出來」這件無聊到沒人想手動做的事，變成可以丟給 agent 跑的任務。

---

## 反方：那 AI 根本不是重點吧？

這是我寫到一半時給自己的質疑。漏洞是老的，手法是枚舉，人是 opsec 爛到把工作目錄開給全世界看的新手。拿掉 AI 三個字，這就是一則普通的資料外洩新聞。

我覺得這個反駁有一半是對的，而對的那一半正是重點。

對的那一半：技術上沒有任何新東西。防守方該做的事也沒有變：仲介入口和員工系統要認證、要限流、要監控單一帳號的異常查詢量。CrowdStrike 的報告沒有給任何「AI 時代專屬」的防禦建議，因為不需要。

但看一下節奏。一個人，沒有組織背景，四天內碰了至少七家金融機構。CrowdStrike 自己的結語是這樣寫的：

> "CrowdStrike Intelligence assesses that adversaries will likely continue to experiment with implementing AI tooling in their operations to enhance their operational tempo and capabilities."

關鍵字是 tempo。AI 沒有讓這個人變強，是讓他變快，而且是在「能力門檻很低」的前提下變快。一個會把自己的 session 紀錄放在公開目錄的人，過去大概不會有本事在四天內對七家機構做這件事。現在可以。

所以我對反方的回應是：對，攻擊技術沒有新東西；錯在於，這正是最該擔心的版本。高手用 AI 不意外，意外的是**門檻降到連這種 opsec 的人都能跑出這個產量**。

---

## 跟本站三條線的關係

### 一、中轉：他自己也是受害者候選人

CrowdStrike 判斷他的 DeepSeek 流量是透過一個 API 中轉或轉售商打的。

四月我寫過 [UCSB 那篇《Your Agent Is Mine》](/llm-proxy-relay-security-your-agent-is-mine-ucsb/)：428 個 LLM 中轉裡，17 個偷 AWS 憑證，還有專挑自動批准模式下手的「裝死」型。九月的 [Anthropic 威脅報告](/anthropic-threat-report-kimi-deepseek-silent-relay/)又加了一層：連你以為在直接用的模型廠，都可能在背後把請求轉給別人。

把這兩篇放到這個案子上看就很有意思。這個攻擊者發出去的每一個 prompt，包括他要打哪家銀行、拿到了什麼、想在哪裡賣，中轉商全部看得到。他沒鎖目錄是一層洩漏，他走中轉是另一層。差別只在於第一層被 CrowdStrike 撿到了，第二層撿到的人是誰，沒人知道。

### 二、Harness：Anthropic 的殼，別人的模型

六月那篇[從 Prompt 到 Harness 的三次中心遷移](/agent-harness-three-migrations-mechanism/)的結論是，prompt 是建議，harness 才是規則，真正有價值的是那個包在模型外面的工作環境。

這個案子是一個很乾淨的驗證。他選了 Claude Code 當指揮介面，但一個 Claude 模型都沒用，三個模型全是別家的。對他來說，Claude Code 的價值不在模型，在那套 session 管理、CLAUDE.md、memory、工具呼叫的機制。ARTEX 也一樣，README 第一句就是填 ANTHROPIC_API_KEY 或 OPENAI_API_KEY，模型可換，harness 不換。

這對做模型的公司是一個不太舒服的訊號：**你的 harness 可以在完全不用你模型的情況下，成為別人的生產力工具。** 包括犯罪者的。

### 三、可解釋性：把他抄家的，就是我們一直想要的那些檔案

我在[可解釋性那篇](/ai-agent-explainability-operational-trust/)主張，企業導入 Agent 時要能回答「它為什麼做這件事」，而答案不在模型腦子裡，在 harness 留下的紀錄：session log、指令檔、狀態檔。

這個案子從另一邊證明了同一件事。CrowdStrike 不需要逆向任何惡意程式，不需要分析任何流量。他們只需要讀。session 紀錄把他的意圖、手法、目標、下一步全部用自然語言寫好了，memory 檔還替他做了摘要。這是鑑識人員做夢都想拿到的東西。

同一份資料，對營運方是信任的基礎，對攻擊者是認罪書。差別只在誰讀到。

這也是一月那篇 [Clawdbot 裸奔事件](/clawdbot-exposed-500-servers-security-disaster/)的延伸。那次是近 1,000 台 agent 因為預設綁 0.0.0.0 暴露在公網。這次是攻擊者自己的 agent 工作目錄暴露在公網。agent 基礎設施的預設狀態是「什麼都記、什麼都留」，誰不把它鎖起來，誰就把自己的大腦掛到網路上。

---

## 這改變了誰的什麼決策

**企業資安團隊。** 這個案子被打的沒有一個是核心銀行系統。是仲介用的查詢服務、員工用的行動辦公系統、合作廠商的帳號。這些系統通常的特徵是：有存取客戶資料的權限、沒有核心系統的防護等級、沒人記得它存在。以前你可以賭沒人有耐心去找它們。現在一個 agent 可以不眠不休地枚舉你所有對外的端點，耐心是免費的。資產盤點的範圍要從「核心系統」改成「任何能查到客戶資料的東西」。

偵測訊號也很明確。金融監督院描述的手法是單一帳號大量異常查詢。這不需要新工具，需要的是有人真的在看那條曲線。

**個人開發者。** 如果你在用 Claude Code 或任何類似工具，你的 `~/.claude` 底下躺著的東西，跟這個攻擊者公開目錄裡的東西是同一種：session 紀錄、CLAUDE.md、memory、你叫它做過的每一件事。這些檔案的敏感程度等於你的工作日誌加上你的 .env。它們不會出現在 .gitignore 範本裡，不會被 secret scanner 抓到，但它們記得你所有的事。

我自己的做法是把這整個目錄當作跟 SSH key 同等級的東西看待：不進任何共用機器、不進任何 repo、不放在任何有對外服務的主機上。

---

## 坦白說

這篇有幾個地方的宣稱強度要打折。

第一，七家機構的數字是韓媒和 piyolog 的彙整，CrowdStrike 的報告本身沒有點名任何一家，也沒有給外洩筆數。把「CrowdStrike 找到的那台伺服器」和「韓國那七家的外洩」畫上等號，是韓國金融保安院的 log 回溯加上時間重疊得出的，不是 CrowdStrike 自己的結論。我認為這個連結很可能成立，但它不是一個已經被司法確認的事實。

第二，ARTEX 的架構我只看到 fork 的 README，原 repo 已經刪了。社群貼文說它是「一個 agent 規劃、一個 agent 執行」的多智能體架構，CrowdStrike 的原文沒有描述這些，我也沒有辦法從 README 確認，所以這篇沒有這樣寫。

第三，「一個人」和「年輕人」都是推論。CrowdStrike 只說沒有連到已知組織、中等信心是中文使用者、財務動機。履歷上是一個人的名字，年紀是 19 或 26，但 CrowdStrike 自己也說這些個資還不能確定屬於攻擊者，而且這不排除背後有別人。開場說他是年輕人，主要依據是他的防守意識，不是那份履歷。

第四，「門檻降低」這個主張，只有一個案例支撐。一個案例可以說明「這種事會發生」，不能說明「這種事變多了」。要等更多報告。

---

## 關鍵洞察

**攻擊面的定義要改。** 這波被打的全是邊緣系統：仲介入口、員工行動系統、外包帳號。agent 不會跳過無聊的端點，它會把每一個都試一遍。資產盤點的問題從「我們的核心系統安全嗎」變成「有哪些東西能查到客戶資料，而我們忘了它存在」。

**agent 的工作目錄是機密。** session 紀錄、CLAUDE.md、memory 檔記得你叫它做過的每一件事，對你是可解釋性，對別人是情報。把它當 SSH key 等級處理。

**看 tempo，不要只看技術。** 這個案子沒有任何新的攻擊技術，CrowdStrike 的結語也只強調 tempo。防守方該問的不是「AI 會發明什麼新攻擊」，而是「我現有的弱點被一個不眠不休的 agent 找到的時候，我撐得住嗎」。

**中轉省下的錢，是用你的 prompt 付的。** 這個攻擊者走中轉打 DeepSeek，他每一個 prompt 中轉商都看得到。這條規則對你一樣成立。

---

## 常見問題 Q&A

**Q: ARTEX 是什麼？**

ARTEX 是一個中國開發者在 2026 年 7 月 26 日放上 GitHub 的開源「AI 自主滲透測試系統（autonomous penetration testing system）」，採 AGPL-3.0 授權，repo 自述是百度 agent+ 攻防挑戰賽的冠軍專案。它用 Go 寫後端、Next.js 寫前端，填入 Anthropic 或 OpenAI 的 API key 就能讓 LLM 自動做資產探索、漏洞掃描和工具呼叫，介面上有攔截審批和人在環路對話等功能。原始 repo 在韓國銀行攻擊事件曝光後已刪除，但 fork 仍可在 GitHub 上找到。

**Q: CrowdStrike 是怎麼找到攻擊者的？**

攻擊者的伺服器開著公開目錄（open directory），意思是沒有設存取限制、任何人輸入網址就能瀏覽的檔案列表。CrowdStrike 在 2026 年 10 月 7 日的報告裡說，他們在裡面找到 Claude Code 的 session 紀錄、CLAUDE.md、Claude memory 檔和 ARTEX 的設定檔，直接看到了攻擊者的手法、目標和對話內容，包括他請 Claude 幫忙找 Telegram 資料交易群，以及寫一份列入這次攻擊成果的資安研究員履歷。

**Q: 這次攻擊用了什麼 AI 模型？**

依 CrowdStrike 報告，主力模型是 DeepSeek v4.1-flash，而且是透過一個被判斷為 API 中轉或轉售商的網域存取；其他 Claude Code session 裡則用了智譜的 GLM-5.3 和 xAI 的 Grok 4.6。指揮介面是 Anthropic 的 Claude Code，但沒有證據顯示用了任何 Claude 模型。

**Q: 韓國銀行這次是被什麼漏洞打穿的？**

不是新型漏洞。依韓國金融監督院的描述，攻擊者先無授權進入新韓銀行手機版網站上給貸款募集人用的查詢服務，用隨機輸入試出有效的客戶編號，再拿這些編號到其他服務集中查詢資料，性質是「查詢與收集」而不是打進資料庫。KB 國民銀行被打的則是員工用的內部行動辦公支援系統。這類「不該被匿名存取的端點加上可猜的識別碼」早在 2010 年的 OWASP Top 10 就被列為 A4 項目，是老問題。

**Q: 用 Claude Code 的一般開發者該注意什麼？**

Claude Code 這類工具會在本機留下 session 紀錄、CLAUDE.md 指令檔和 memory 檔，內容是你叫它做過的每一件事。這些檔案不會被 .gitignore 範本或 secret scanner 處理，但敏感程度等於工作日誌加 .env。比較保守的做法是把整個工作目錄當 SSH key 等級看待：不放進共用機器、不進 repo、不放在任何有對外服務的主機上。

---

## 來源

- CrowdStrike，[Unknown Threat Actor Uses AI-Driven ARTEX to Target South Korean Finance](https://www.crowdstrike.com/en-us/blog/unknown-threat-actor-uses-artex-to-target-south-korean-finance/)，2026-10-07
- piyolog，[韓国の金融機関で相次いだ不正アクセスについてまとめてみた](https://piyolog.hatenadiary.jp/entry/2026/10/06/103019)，2026-10-06
- 聯合新聞（經 Daum），[신한은행 "해킹으로 2만5000명 개인정보 유출" 연소득·대출정보 포함](https://v.daum.net/v/20261001123012747)，2026-10-01
- Daum，[신한은행에 '중국어 AI 침투' 흔적…해킹 공포 금융권 확산](https://v.daum.net/v/20261002192945588)，2026-10-02
- Security Affairs，[AI-Driven tool ARTEX used in attacks against South Korean Banks](https://securityaffairs.com/200661/hacking/ai-driven-tool-artex-used-in-attacks-against-south-korean-banks.html)
- ARTEX fork README（原 repo Autumn-27/ARTEX 已刪除）
