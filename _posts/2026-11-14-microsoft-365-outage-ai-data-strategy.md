---
layout: post
title: "微軟當機 26 小時：不是雲端不可信，而是雲地混合更有韌性"
date: 2026-11-14 15:30:00 +0800
permalink: /microsoft-365-outage-ai-data-strategy/
description: "Microsoft 365 全球大當機超過 26 小時，不只 Teams 建私密群與 Power BI 匯出報錯，英國醫院退回紙本、金融機構改用電話報數，連帶讓 Copilot、Claude 與 ChatGPT 集體失明。買三家 AI 不等於分散風險——這場重連風暴揭露企業真正該補的是四層 DR 災難復原與雲地混合韌性。"
categories: [AI 觀點, AI 產業分析, AI 地端部署]
tags: [Microsoft 365, Exchange Online, Copilot, Claude, ChatGPT, 單點故障, 重連風暴, 災難復原, 雲地混合, 企業 AI 架構]
image: /assets/images/microsoft-365-outage-ai-data-strategy-cover.png
image_alt: "微軟當機 26 小時：不是雲端不可信，而是雲地混合更有韌性"
author: Wisely Chen
---

## 一次設定改動，全球折騰超過 26 小時

11 月 12 日（台灣時間 11 月 13 日凌晨）開始的這場微軟全球大當機，前前後後折騰了超過 26 小時，很多朋友上班時遇到的怪象特別邪門。打開 Teams，和同事們語音開會、在老群裡發訊息都沒問題，但一旦想新建私密群，介面立刻報錯；打開 Power BI 線上看數據報表也沒問題，只要一點匯出 PDF 就卡死，微軟官方給的臨時辦法居然是讓大家手動把檔案上面的保密標籤（sensitivity label）刪掉再匯出。

軟體的別扭迅速演變成現實世界裡的手忙腳亂。英國醫療協作網斷聯後，倫敦和曼徹斯特的多家公立醫院直接拿出紙筆，回歸手寫病歷和處方；專注心理健康服務的 Lincolnshire Partnership NHS Foundation Trust 甚至發公告呼籲：需要轉診或正經歷危機的患者請直接打電話，不要寄電郵。金融城與企業界也陷入混亂，英格蘭銀行（Bank of England）、英國金融監管局（FCA）和泛歐交易所（Euronext）緊急暫停線上申報系統，要求各大機構改為電話口頭報數；美國眾議院、坦帕與路易斯維爾等多個市政府、洛杉磯縣法醫辦公室、航運巨頭馬士基（Maersk）也相繼受波及，底特律工業公司 Workhorse Group 甚至被迫延後第三季財報電話會議。

IT 技術服務公司 Envision Technology Advisors 首席技術官 Stephen Rose 向《華爾街日報》形容，客戶因為無法發信全改打電話，「我們的服務台完全癱瘓」，最後只能希望消息靠電話口耳相傳。難怪佛州政治策略師 Steve Schale 會在 X 上調侃：「親愛的微軟——你關錯了。請把我們的電郵開回來，把 Teams 關掉。」

沒有駭客攻擊，沒有海底電纜斷裂。全世界的混亂，純粹是因為微軟的雲端信箱掛了。網路公司 Infoblox 分析主管 Doug Madory 估算核心中斷約 19 小時，而從週四開始到全球各地與連接器陸續恢復，前前後後折騰了超過 26 小時。

---

## 一個老信箱，為什麼能鎖死整棟辦公大樓

為什麼平時不用郵件的人也遭殃？因為很多人以為信箱只是公司前台的收發室，但在微軟二十多年的技術累積裡，Exchange Online 其實是整棟辦公大樓的總登記處。你的行事曆、聯絡人、手機上的個人待辦清單，都藏在個人信箱的某個隱藏資料夾裡。

Teams 平時單聊和語音走另一條獨立通道，但新建私密群需要在信箱總登記處辦戶口；Power BI 匯出機密 PDF 或帶企業加密鎖的雲端電腦開機，也要透過同一條底層通道核驗權限、蓋保密公章。老信箱大門一鎖，樓上所有看似獨立的軟體全都辦不了正事。

這不是硬體老舊。Exchange Online 跑在微軟最新的機房裡。老的是架構：一個二十多年前誕生的郵件系統，一層層被疊上新服務，變成一棟不斷加蓋、地基卻沒換過的老房子。

---

## 為什麼按了撤回鍵，還卡了 26 小時

更讓人納悶的是，既然知道是週四下午一次常規網路設定改動觸發了潛伏缺陷，為什麼工程師按了撤回鍵還卡了 26 個小時？

**第一，排查繞了六個鐘頭彎路。**起初工程師以為是外部流量洪峰，後來看到自動健康檢查（health check）成批踢掉無回應的郵件伺服器，又以為是巡檢誤報，直到深夜才查出是負責安全入場核驗的程序算力過載，把伺服器直接凍死了。

**第二，週五零點重啟上線，真正的噩夢才剛開始。**平時全球幾億用戶的手機和電腦已經連在線上，就像員工已經在樓內就座，保安只需輕鬆維持秩序。這次大規模斷網把幾億台手機、電腦和背景腳本同時趕到大街上，每秒自動發起重連請求，要求在大門口重新驗證身分和辦理出入證，計算量遠超平時數百甚至數千倍。剛重啟好的伺服器大門才開一條縫，瞬間又被這股「自動重連風暴」擠癱。

**第三，房門從裡面反鎖了。**到了週五凌晨 3 點半，工程師想要撤銷前一天改錯的設定，卻發現後端伺服器已經卡死，連接收撤回指令的餘力都沒有——這就像房門從裡面反鎖，外面的人遞再多新鑰匙也塞不進去，上游路由還在瘋狂問路加劇擁堵。

最後微軟只能用笨辦法：一邊緊急加機器、關小大門流量閥，一邊把伺服器一台台斷網重啟，像擰水龍頭一樣一滴一滴放人進來。微軟發言人對《華爾街日報》的說法也很直接：「鑑於需求規模，我們逐步恢復服務，並在每個階段驗證穩定性。雖然耗時更長，但有助於確保穩定恢復。」這套慢工細活跑通的時候，剛好趕上亞洲時間週五傍晚，日本和亞太的上班族紛紛關電腦下班過週末，門口排隊的設備少了一大半，亞太區才最先喘過氣來；而正值週五上班高峰的歐美用戶，只能眼睜睜多熬了半天。

---

## 買三家 AI，卻共用同一個老閥門

這場事故還意外暴露了另一個真相。許多公司為了避免被單一供應商綁死，同時採購了微軟的 Copilot、Anthropic 的 Claude 和 OpenAI 的 ChatGPT，以為把雞蛋放在三個籃子裡。結果週四下午到週五，三大辦公助手在同一時刻集體失明，無法幫你總結郵件或查詢行程。

要講清楚：**大模型自己的算力晶片一顆都沒壞。**Claude 和 ChatGPT 照樣能聊天、寫程式。但企業資料安全規矩不允許任何大模型私自囤積公司的郵件和行事曆，每次你在對話框裡提問，大模型都需要當場派個信使去拿臨時通行證敲微軟信箱的門。老收發室從裡面焊死，外面的大腦再聰明也拿不到半頁紙資料。

籃子是三個，底下的桌子只有一張。

以前信箱壞了，大家手動重新整理兩次沒反應就去茶水間喝咖啡聊天，伺服器自然有喘息的時間。現在幾億台設備、背景腳本和不知疲倦的辦公連接器全都寫死了斷線自動重試，三個最聰明的助手共用同一個二十多年前的老信箱閥門，一次設定閃斷就能演變成 26 小時的全球拉鋸戰。

所以多買幾家 AI 不是答案。這次暴露的不是 AI 策略的問題，而是更根本的問題：你的 DR（災難復原）到底有沒有做好。

---

## 真正的安全：DR 要做到四層

很多人聽到這裡會說：那就搬回地端。我不同意。大多數企業自己維運的可靠度，根本比不上微軟。而且雲端出事可以怪微軟，地端出事只能罵自己，這是真實的組織心理。

但怪罪微軟救不了你的損失，醫院照樣得退回紙本，金融機構照樣得用電話報數。重點不是雲端還是地端，而是不要只有一個故障域（failure domain）。主力留在雲端負責效率，地端放最關鍵的一小塊負責韌性。

所以該問的不是「要不要搬回地端」，而是「每一層的 DR 有沒有做好」。我把它拆成四層：

| 層級 | 涵蓋什麼 | DR 要做到 | 這次的教訓 |
| :--- | :--- | :--- | :--- |
| **應用（App）** | Outlook、Teams、Power BI、Copilot、自家系統與 AI agent | 盤點每個 App 依賴哪些底層服務；斷線時要有降級模式與退避（backoff）機制 | 看似獨立的 App，建私密群、匯出 PDF 全插在同一個 Exchange 上；無腦重試更把伺服器擠死 |
| **關鍵基礎設施** | Exchange、AD／身分認證、MQ、網路 | 找出單點故障，關鍵服務要有第二條路 | 一次網路設定改動，安全核驗與 Exchange 倒下，上面全部跟著倒 |
| **Infra** | 雲端、地端、AI 推論環境 | 不只一個故障域；備援環境要能獨立登入、獨立運作 | 雲端不是不會壞，只是壞的時候大家一起壞 |
| **資料** | 雲地兩邊的關鍵資料 | 關鍵資料雲地雙份、權限同步、標示新鮮度 | 模型沒壞，拿不到資料一樣失效 |

認證這層特別要注意。這次微軟是對上游認證與路由元件進行處理並分段放行才穩下來，代表認證本身就是單點故障。

最後一條沒有捷徑：定期做切換演練。沒演練過的備援，等於沒有備援。

---

## AI 該留住老經驗，而不是取代它

事件一出，網路上馬上有人把矛頭指向裁員。微軟 2025 年裁了約 15,000 人，今年 7 月又裁了約 4,800 個職位。

先講清楚：**目前沒有任何證據顯示這次當機是裁員造成的。**微軟否認的「跟 AI 無關」，指的是 AI agent 流量擠爆伺服器的傳言，不是人力問題。把裁員寫成原因，就是在編故事。

但有一個風險是真實存在的：組織知識流失。這次的缺陷在系統裡潛伏了很久，平常沒人知道。排障團隊一開始以為是流量問題，繞了六個小時才找到安全核驗與連線程序。這種「我看過這個症狀」的直覺，不在任何文件裡，只在資深工程師的腦子裡。

這對我們自己的論述也是一劑預防針。很多 AI 轉型專案的敘事是「AI 可以取代老經驗」。我的看法是：**AI 只能承接被寫下來的經驗，取代不了沒寫下來的那些。**人先走了，AI 也學不到。

所以順序不能反：

1. 先用 AI 把資深人員的排障過程、判斷邏輯萃取出來，變成組織的知識庫。
2. 用真實事件驗證這個知識庫站不站得住。
3. 最後才談精簡人力。

順序反過來，就是今天大家在質疑微軟的那個風險。

---

## Sources

- [The Wall Street Journal：The Chaos and Unexpected Joys of a 19-Hour Global Email Outage](https://www.wsj.com/business/telecom/the-chaos-and-unexpected-joys-of-a-19-hour-global-email-outage-37b7170c)
- [MacRumors：Microsoft 365 Outage Resolving After Nearly 24 Hours](https://www.macrumors.com/2026/11/13/microsoft-365-outage-resolving/)
- [Control Plane：What Caused the Microsoft 365 Outage of November 12, 2026](https://controlplane.com/blog/post/microsoft-365-outage-november-2026-cause)
- [DEV Community：Microsoft 365 Outage (Nov 2026) timeline](https://dev.to/epifive/microsoft-365-outage-nov-2026-what-we-know-about-the-root-cause-and-what-it-admins-should-learn-4hld)
- [SecurityWeek：Microsoft 365 Outage Disrupts Outlook, Exchange Online and Teams](https://www.securityweek.com/microsoft-365-outage-disrupts-outlook-exchange-online-and-teams/)
- [Arab News：NHS triggers contingency after Microsoft outage](https://www.arabnews.pk/world/englands-health-service-triggers-contingency-after-microsoft-outage-3006927)
- [The Next Web：Claude and ChatGPT integrations affected](https://thenextweb.com/news/microsoft-outage-outlook-teams-12-hours-global)
- [Claude Status](https://status.claude.com/)
- [TechRepublic：Uptime — outages less frequent but more expensive](https://techrepublic.com/article/news-data-center-outages-decline-costs-rise/)
- [中央社：Uptime 2026 年度停機分析報告](https://n.yam.com/Article/20260514877394)
- [Fast Company：Microsoft cuts 4,800 jobs](https://www.fastcompany.com/section/microsoft)
