---
layout: post
title: "OpenAI Codex 降智復盤報告給我們啟示：真誠永遠是最好的必殺技"
date: 2025-11-03 21:35:56 +0000
permalink: /openai-codex-jiang-zhi-fu-pan-bao-gao-gei-wo-men-qi-shi-zhen-cheng-yong-yuan-shi-zui-hao-de-bi-sha-ji/
image: /assets/images/HuM7-Ljf25IoSJfNXs7Py.png
description: "問題：當系統開始出現幽靈..."
---




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
