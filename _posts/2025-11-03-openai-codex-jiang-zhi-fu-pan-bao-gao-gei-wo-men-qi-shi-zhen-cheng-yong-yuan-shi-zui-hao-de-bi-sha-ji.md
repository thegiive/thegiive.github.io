---
layout: post
title: "OpenAI Codex 降智復盤報告給我們啟示：真誠永遠是最好的必殺技"
date: 2025-11-03 21:35:56 +0000
permalink: /openai-codex-jiang-zhi-fu-pan-bao-gao-gei-wo-men-qi-shi-zhen-cheng-yong-yuan-shi-zui-hao-de-bi-sha-ji/
image: /assets/images/HuM7-Ljf25IoSJfNXs7Py.png
description: "問題：當系統開始出現幽靈..."
---


![OpenAI Codex 降智復盤報告給我們啟示：真誠永遠是最好的必殺技](/assets/images/HuM7-Ljf25IoSJfNXs7Py.png)

### 問題：當系統開始出現幽靈

有一天，OpenAI 團隊收到大量的 User 回應 Codex 感覺降智了。他們開始啟動調查，最後他們宣稱 Codex 推理系統發現不是明顯的 bug，而是一種間歇、無規律、難以重現的異常。有時請求在特定 GPU 上延遲，有時 API 回應在低負載下超時，有時資料似乎在壓縮過程中被改寫了，感覺出現了 「Ghost 」

雖然這是一個人類歷史上數一數二複雜IT系統，但是 OpenAI工程團隊決定將這個調查的過程[公諸於世](https://docs.google.com/document/d/1fDJc1e0itJdh0MXMFJtkRiBcxGEFtye6Xc6Ui7eMX4o/edit?tab=t.0&ref=ai-coding.wiselychen.com)，我非常喜歡[這個團隊leader面對問題](https://x.com/thsottiaux/status/1967996885500928459?utm_source=chatgpt.com)的解決方式「Transparency 」 

![](/assets/images/image-8.png)

以下是報告簡單總結，你或許也可以學到很多

* * *

## **調查方式：讓真實訊號浮現**

OpenAI 團隊發現到真正的問題來自「內部版本跟使用者版本不一致」，基本上內部開發版本第一個可能比較新，內部開發 routine 也加入了其他的機制，他們決定把問題拆開，讓每一層都能被看見

### a. 推出新的 `/feedback` 機制，讓外部使用者可以直接回報

在宣布調查的隔天，即刻於 **Codex CLI v0.50** 上推出新的 **`/feedback`** 通道。任何用戶都能直接回報異常，資料回流同一系統，讓整個除錯過程從「內部猜測」變成「開放共修」。

![](/assets/images/image-4.png)Codex 0.5 : 外部 feedback 的數量從當天開始俱增

### b. 內外一致 , 讓工程師成為用戶

我們將 **OpenAI 內部使用環境** 改為與 **外部用戶** 完全相同。沒有特殊 flag，沒有後門設定。所有請求都經過同樣的 API、同樣的延遲、同樣的錯誤機率。

> 就是 Google 說的「eat your dogfood」

### c. 簡化系統複雜度 

在使用者查詢（query）與 GPU 推理之間，有數層抽象、代理與快取。為了減少干擾，我們開始做減法。審核並移除超過 **60 個 feature flags，** 另有 **80 個** 正在移除中

* * *

## **Finding / Fix：多重問題疊加下的結果**

這次調查發現三個主要問題，它們像是藏在系統深處、彼此疊加的幽靈。

### **1️⃣ 上下文壓縮(compaction) 問題**

最主要的異常來自 **資料壓縮（compaction）** 模組。過於頻繁的壓縮導致多節點間的時間序錯亂，造成資料被重寫或延遲讀取，行為難以預測。這其實跟所有人說的

> 決定AI Agent 智商的，永遠是上下文怎麼處理

![](/assets/images/image-6.png)Compact Frequency

🧠 OpenAI 重新設計壓縮節奏與合併策略，並調整 timeout 與 I/O 流程。**結果** Throughput 提升約 **12%，** 錯誤率下降近 **47%**

### **2️⃣ 老舊硬體問題**

部分運算節點仍使用老舊 GPU 型號，在特定 I/O 模式下出現記憶體異常與延遲。更換或隔離後，整體穩定性大幅改善。在分散式架構裡，硬體老化就像慢性病，  
不爆，但會讓系統長期發燒，最後可能慢慢地讓這個系統 crash。

### **3️⃣ 數個多重問題疊加（apply_patch、Timeout、Constrained Sampling）**

另外就是系統多個因素在同時發生時，產生了難以預測的互動效應：

  * **apply_patch** 時非同步更新順序錯亂
  * **Timeout** 過於嚴格導致誤觸
  * **Constrained sampling** 使回應語言與風格漂移

這些看似無關的小誤差，疊加起來形成了真實世界中最奇怪的現象。有趣的是，許多 X 使用者回報：

> “Codex 某個版本後，講著講者突然用韓文回答問題。” 🇰🇷

![](/assets/images/image-7.png)KPop聽太多了嗎~~

這正是多重干擾造成的語言漂移。模型沒有壞，只是接收了不同層的「不一致訊號」。

## **我自己的 Finding：** 真誠才是永遠必殺技

我身為技術人員，雖然 OpenAI 團隊正在除錯人類史上數一數二的複雜系統，但是他們做的事情跟我讀書，出社會做 Yahoo EC，Appier 做數據平台，Google 做大客戶的數位轉型，做的事情一模一樣就是

  1. 建立一個從外到內的 feedback 管道
  2. 讓工程人員 eat your dog food 
  3. 將複雜系統/流程簡化，多餘節點刪除

其實在人生中，很多企業的問題只要能做到這三點，通常都會解決這世界上最困難的問題。我自己本身在解決內部問題時，這三點也幫助我解決很多世界頂級的難題

因為

> 真誠才是永遠必殺技

* * *

Ref Link 

  1. [調查報告](https://docs.google.com/document/d/1fDJc1e0itJdh0MXMFJtkRiBcxGEFtye6Xc6Ui7eMX4o/edit?tab=t.0&ref=ai-coding.wiselychen.com)
  2. [討論的 X Thread ](https://x.com/thsottiaux/status/1984465716888944712?ref=ai-coding.wiselychen.com)

[ ![Multi-Agent 協作模式：當 AI 學會「會診」這件事](/assets/images/ChatGPT-Image-2025---11---15----------04_36_04.png) Multi-Agent 協作模式：當 AI 學會「會診」這件事 我上週回老家看了久違的第四台「緯來日本台」，看一個日本節目「恐怖家庭醫學」，裡面講到一個年長者「最近常常心悸、手抖、睡不好」。因為是心臟的因素，所以患者直接找心臟科檢查後，拿到一疊厚厚的報告——結果心臟科醫生看完報告說：「你的心臟結構完全正常，心電圖也沒問題，可能是壓力太大，回去多休息就好。」患者心想：「可是我真的有心悸啊！難道是我自己想太多？」於是患者找了神經科說可能是自律神經失調，拿了藥物減壓，但症狀完全沒改善。 弄了很久一直兜兜轉轉。最後一個經驗豐富家醫科醫生，告知患者「這可能是甲狀腺的問題，要去看內科」才發現這是甲亢的症狀，調整好藥物很快就好了。很多時候人體很多時候是一個連動的生態系統，有些問題的表象跟真正的Root Cause是兩回事，所以患者很容易找錯醫生弄錯科目。 但如果是在好的健檢中心，做法就完全不一樣了。健康檢查會根據你的全方位給予檢查——最後針對你的完整報告進行討論，這時候甲亢的 Root Cause 很快就會被最後的把關者抓出來 " 問題根本不在心臟，而在甲狀腺 " 。這就是「多人協作的力量」。 AI Agent 的世界也是一樣的道理。 By Wisely Chen 15 Nov 2025 ](/multi-agent-xie-zuo-mo-shi-dang-ai-xue-hui-hui-zhen-zhe-jian-shi/) [ ![那天我在產業園區分享：AI 能不能做起來，其實看人](/assets/images/S__88875042.jpg) 那天我在產業園區分享：AI 能不能做起來，其實看人 今天我在新北產業園區，在我們公司的 AI 轉型的活動 在各位傳統產業的前輩講述我之前在傳統產業做 AI 轉型的經驗 我認為「 AI 要在傳產落地，先解決的永遠不是模型，而是人、流程與文化。」 我把這幾年的實戰經驗濃縮成一套能在傳統產業中真正起作用的框架： 現況分析：先理解現場，再談技術 我們創建了一個以 公司各部門的老前輩 + Intern 為主的種子團隊，深入一線流程、取得高層支持，建立真正的共識。 AI 不是空降，而是跟現場一起改。 快速勝利：小範圍試點，讓大家看到成效 選一個可控的場域，把 AI +種子團隊拉進真實流程。 像我用 AI + RPA + OCR + 快速掃描器 = 一個可持續可落地，並且有效益成果 這樣的「小勝利」，是推動組織願意往下走的關鍵。 全面升級：從工具導入到組織轉型 把建置的種子團隊散步到全公司各個部門 可以用很快的速度去 scale 全面開花 By Wisely Chen 13 Nov 2025 ](/na-tian-wo-zai-chan-ye-yuan-qu-fen-xiang-ai-neng-bu-neng-zuo-qi-lai-qi-shi-kan-ren/) [ ![AI 信任崩塌的真正原因：勞資零和賽局的再現](/assets/images/ChatGPT-Image-2025---11---10----------09_24_03.png) AI 信任崩塌的真正原因：勞資零和賽局的再現 根據《Harvard Business Review》近期發表的〈Workers Don’t Trust AI. Here’s How Companies Can Change That〉，美國基層員工對公司提供的 AI 工具信任度在短短數月內暴跌：對生成式 AI 的信任下降 31%，對自主決策型 AI 更下滑 89%。近半數員工反而更信任非官方AI 工具。另外無獨有偶MIT 的研究《The GenAI Divide: State of AI in Business 2025》更進一步揭示了這種現象，並命名為 Shadow AI：員工在公司外私下使用未授權的 AI 來完成工作。研究指出，約有 By Wisely Chen 10 Nov 2025 ](/ai-xin-ren-beng-ta-de-zhen-zheng-yuan-yin-lao-zi-ling-he-sai-ju-de-zai-xian/) [ ![\[Agent part 3\] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵](/assets/images/ChatGPT-Image-2025---11---8----------08_01_49.png) [Agent part 3] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵 大家都知道我用 AI 來 enable 很多intern 來當作很多正職的事情，當然他們雖然都很年輕跟熱情，但是我管理團隊時發現一個規律： 當我派給幾個 Senior 的同事 ，我通常只需要 weekly 跟他開會，給他幾個任務，一週後檢查一次就好。他可以獨立工作，中間遇到問題會自己判斷、調整，如果有大問題他們會舉手跟我講，不容易走偏。 當我要安排工作給我的 intern ，跟 Senior 最大的不同就是， Junior 我通常會每半天或是每過一天就會跟他聊一下提醒一下可能要注意什么事情。因為他很容易遇到了某些複雜任務時，他就可能在某一步卡住，又沒有舉手，基於錯誤理解繼續做下去，最後整個方向偏了，也浪費了他整天的時間。 這是Sr 跟 Jr 經驗的差別，獨立作戰的能力 AI Agent 也是如此 現在考驗 AI Agent 最大的地方，不是他的智商，主要著重點是它的連續工作穩定性。如果人類需要介入的越少，就代表它可以自主完成工作， By Wisely Chen 08 Nov 2025 ](/agent-part-3-interleaved-thinking-cheng-xian-de-wen-ding-xing-shi-xian-zai-agentluo-di-de-zhong-yao-guan-jian/)