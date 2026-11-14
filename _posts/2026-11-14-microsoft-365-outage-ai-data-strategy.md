---
layout: post
title: "微軟當機 26 小時：Exchange 原來是業務層 AuthZ 總管，連三家 AI 都被重連風暴拖下水"
date: 2026-11-14 16:10:00 +0800
permalink: /microsoft-365-outage-ai-data-strategy/
description: "Microsoft 365 全球大當機超過 26 小時（核心中斷約 19 小時），不只是收不到信，而是整棟辦公大樓的業務層 AuthZ 行政處鎖死。從 GCP 4 小時就是年度盛事的維運視角，拆解 6 小時排查、重連風暴、三家 AI Agent 連帶失效，以及剛發生的美國 FAA 全國停飛 4 小時。"
categories: [AI 觀點, AI 產業分析, AI 資安]
tags: [Microsoft 365, Exchange Online, AuthZ, Copilot, Claude, ChatGPT, 重連風暴, FAA, Infra Outage, 企業 AI 架構]
image: /assets/images/microsoft-365-outage-ai-data-strategy-cover.png
image_alt: "微軟當機 26 小時：Exchange 原來是業務層 AuthZ 總管，連三家 AI 都被重連風暴拖下水"
author: Wisely Chen
---

## 一次設定改動，把全世界逼回上個世紀

微軟這次全球大當機前前後後折騰了超過 26 小時（核心中斷約 19 小時），從 11 月 12 日一路拖到週五，把全世界的辦公室逼回上個世紀。（我以外，我們公司是 GWS XD）

很多朋友早上一進公司遇到的怪象特別邪門。打開 Teams，語音開會、在老群裡發訊息都沒問題，但一旦想新建私密群，介面立刻報錯；打開 Power BI 線上看數據報表也沒問題，只要一點匯出 PDF 就卡死，微軟官方給的臨時辦法居然是讓大家手動把檔案上面的保密標籤（sensitivity label）刪掉再匯出。佛州政治策略師 Steve Schale 甚至在 X 上無奈調侃：「親愛的微軟——你關錯了。請把我們的電郵開回來，把 Teams 關掉。」

軟體的別扭迅速演變成現實世界裡的大混亂：

- **英國醫療系統**：醫療協作網斷聯後，倫敦和曼徹斯特的多家公立醫院直接拿出紙筆，回歸手寫病歷和處方；專注心理健康服務的 Lincolnshire Partnership NHS Foundation Trust 甚至發公告呼籲：需要轉診或正經歷危機的患者請直接打電話，不要寄電郵。
- **金融圈與公共部門**：英格蘭銀行（Bank of England）、英國金融監管局（FCA）和泛歐交易所（Euronext）緊急暫停線上申報系統，要求各大機構改為電話口頭報數；美國眾議院、坦帕與路易斯維爾等多個市政府、洛杉磯縣法醫辦公室、航運巨頭馬士基（Maersk）也相繼受波及，底特律工業公司 Workhorse Group 甚至被迫延後第三季財報電話會議。
- **第一線 IT 服務台**：技術服務公司 Envision Technology Advisors 首席技術官 Stephen Rose 向《華爾街日報》坦言，客戶因為無法發信全改打電話，「我們的服務台完全癱瘓」，只能希望消息靠電話口耳相傳。

---

## Exchange 不是收發室，而是業務層 AuthZ 的「行政處」

昨天事件最後復盤：沒有 AI 駭客，沒有海底電纜斷裂，純粹是 Exchange Online 掛了。

為什麼平時不用郵件的人也遭殃？因為在微軟二十多年的架構累積裡，Exchange 不只是 Email 收發室，它還扛了大量**業務層的 AuthZ（權限核驗／合規檢查）與資源登記**，等於整棟辦公大樓的「行政處」。

很多人會困惑：AuthN（身分驗證）不是在 Entra ID（原 Azure AD）嗎？沒錯，Entra ID 沒掛，所以你依然能登入、Teams 單聊與語音會議走獨立通道也正常、Power BI 也能線上開報表。但只要涉及跨服務的資源建立與合規授權，就得過 Exchange 這關：

- **群組與資源登記**：Teams 新建私密群或 M365 Group，必須到 Exchange 行政處登記戶口與信箱路由。
- **保密標籤與權限核驗**：Power BI 匯出機密 PDF，或帶企業加密鎖的雲端電腦開機，都要透過同一條底層通道核驗敏感度標籤與解密權限（AuthZ）、蓋保密公章——這也是為什麼刪掉標籤就能匯出，因為繞過了那層 AuthZ 檢查。

老信箱大門一鎖，樓上所有看似獨立的軟體全都辦不了正事。這不是硬體老舊，老的是架構：一個二十多年前誕生的郵件系統，一層層被疊上新服務，變成一棟不斷加蓋、地基卻沒換過的老房子。

---

## 為什麼卡了 26 小時？從 GCP 維運視角看這場「重連風暴」

更反常的是恢復時間。我之前在 GCP 做事的時候，其實全球的 Infra 要一次垮 4 個小時就是年度盛事了；這次微軟拖了超過 26 小時，非常詭異。

根據多方技術復盤，工程師早已定位是週四下午一次常規網路設定改動惹 Exchange 的禍，卻還是卡了這麼久，關鍵在五個連鎖反應：

1. **排查先繞了 6 小時彎路。**起初工程師以為是外部流量洪峰，看到自動健康檢查（health check）成批踢掉無回應的郵件伺服器又以為是巡檢誤報，直到深夜才查出是負責安全入場核驗的程序算力過載，把伺服器直接凍死了。
2. **週五零點重啟後，真正的噩夢「重連風暴」才開始。**平時幾億用戶的手機和電腦已經在線上，像員工已在樓內就座，保安只需維持秩序。斷網把幾億台設備和背景腳本同時趕到大街上，每秒自動發起重連請求要求重新驗身分，計算量暴增數百上千倍，剛開一條縫的大門瞬間又被擠癱。
3. **凌晨 3 點半想撤回設定時，後端已經卡死到收不到工程師指令。**這就像房門從裡面反鎖，外面遞再多新鑰匙也塞不進去，上游路由還在瘋狂問路加劇擁堵。
4. **最後微軟只好用笨辦法，一邊緊急加機器、關小大門流量閥。**
5. **工程師一邊把伺服器一台台斷網重啟。**

微軟發言人對《華爾街日報》的說法很直接：「鑑於需求規模，我們逐步恢復服務，並在每個階段驗證穩定性。」說白了，就是只能像擰水龍頭一樣一滴一滴放行。這套慢工細活跑通時，剛好趕上亞洲時間週五傍晚，日本與亞太上班族紛紛關電腦下班過週末，門口排隊的設備少了一大半，亞太區才最先喘過氣；而正值週五上班高峰的歐美用戶，只能眼睜睜多熬了半天。

---

## 三家 AI 模型沒壞，但 Agent 一起廢了一半

這一次還有一件很有趣的事：許多企業同時採購了微軟 Copilot、Anthropic Claude 與 OpenAI ChatGPT，結果在微軟這波事件裡，三家的模型大腦本身都沒壞，卻在同一時間無法使用 Exchange Connector。

企業資安規矩不允許任何大模型私自囤積公司的郵件與行事曆，每次在對話框裡提問，Agent 都得當場派信使拿臨時通行證去敲 Exchange 的門。老行政處從裡面反鎖，外面的大模型算力再強，也拿不到半頁紙資料，等於直接廢了一半。

更微妙的是：**以前信箱壞了，大家手動重新整理兩次沒反應就去茶水間喝咖啡聊天，伺服器自然有喘息空間；現在幾億台設備、背景腳本加上各家 AI 連接器，全都寫死了斷線自動重試。**

這 26 小時的超長恢復時間，AI Agent 造成的 retry 風暴可能也貢獻了不少力氣 XD。

---

## AI 該留住老經驗，而不是取代它

事件一出，網路上馬上有人把矛頭指向裁員（微軟 2025 年裁了約 15,000 人、今年 7 月又裁了約 4,800 個職位）。

但有一個風險比謠言更值得我們警惕：組織知識流失。這次的缺陷在系統裡潛伏了很久，排障團隊一開始繞了 6 個小時才找到安全核驗與連線程序。那種「我看過這個症狀」的直覺，不在任何文件裡，只在資深工程師的腦子裡。

很多 AI 轉型專案的敘事是「AI 可以取代老經驗」。我的看法剛好相反：**AI 只能承接被寫下來的經驗，取代不了沒寫下來的那些。**人先走了，AI 也學不到。

所以順序不能反：

1. 先用 AI 把資深人員的排障過程、判斷邏輯萃取出來，變成組織的知識庫。
2. 用真實事件驗證這個知識庫站不站得住。
3. 最後才談精簡人力。

---

## 從十月資安潮，到十一月 Infra Outage 潮？

微軟這邊才剛喘口氣，結果今天（美東時間 11/13 下午、台灣時間清晨）美國聯邦航空總署（FAA）的航管通訊與雷達控制系統又出問題了，發布了 9/11 以來第三次全國性停飛令，整個美國不能起降超過 4 小時（官方紀錄 4 小時 21 分鐘），問題同樣指向老舊航管通訊網路與路由器的資料過載。

一開始是十月的資安潮，現在要迎來 Infra outage 潮了嗎⋯⋯

---

## Disclaimer：有多少資料講多少話

我們是有多少資料講多少話的人，照例補上目前的事實邊界：

1. **沒有任何證據**顯示 MS 365 當機，與微軟這幾年因為 AI 裁員有關。
2. **沒有任何證據**顯示 MS 365 當機是網傳的 AI 攻擊導致的（微軟與多方技術復盤均指向網路設定變更）。
3. **沒有任何證據**顯示 MS 365 當機，跟 Claude 昨天（11/13）自己發生的兩波登入與 API 大當機有關。
4. **沒有任何證據**顯示 MS 365 當機，跟今天美國 FAA 機場航管系統出問題有關。

呼⋯⋯多事之秋。寫到這裡頭都暈了，但至少把事實與架構邊界先畫清楚，剩下的就是看各家企業怎麼把自己的單點故障與退避（backoff）機制補起來。

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
- [CBS News：FAA lifts nationwide ground stop after air traffic control system outage](https://www.cbsnews.com/news/faa-ground-stop-air-traffic-control-outage/)
- [Fast Company：Microsoft cuts 4,800 jobs](https://www.fastcompany.com/section/microsoft)
