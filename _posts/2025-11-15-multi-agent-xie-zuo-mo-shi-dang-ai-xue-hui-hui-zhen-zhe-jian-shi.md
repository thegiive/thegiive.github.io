---
layout: post
title: "Multi-Agent 協作模式：當 AI 學會「會診」這件事"
date: 2025-11-15 08:36:53 +0000
permalink: /multi-agent-xie-zuo-mo-shi-dang-ai-xue-hui-hui-zhen-zhe-jian-shi/
image: /assets/images/ChatGPT-Image-2025---11---15----------04_36_04.png
description: "我上週回老家看了久違的第四台「緯來日本台」，看一個日本節目「恐怖家庭醫學」，裡面講到一個年長者「最近常常心悸、手抖、睡不好」。因為是心臟的因素，所以患者直接找心臟科檢查後，拿到一疊厚厚的報告——結果心臟科醫生看完報告說：「你的心臟結構完全正常，心電圖也沒問題，可能是壓力太大，回去多休息就好。」患者心想：「可是我真的有心悸啊！難道是我自己想太多？」於是患者找了神經科說可能是自律神經失調，拿了藥物減壓..."
---




我上週回老家看了久違的第四台「緯來日本台」，看一個日本節目「恐怖家庭醫學」，裡面講到一個年長者「最近常常心悸、手抖、睡不好」。因為是心臟的因素，所以患者直接找心臟科檢查後，拿到一疊厚厚的報告——結果心臟科醫生看完報告說：「你的心臟結構完全正常，心電圖也沒問題，可能是壓力太大，回去多休息就好。」患者心想：「可是我真的有心悸啊！難道是我自己想太多？」於是患者找了神經科說可能是自律神經失調，拿了藥物減壓，但症狀完全沒改善。

![](/assets/images/image-33.png)

弄了很久一直兜兜轉轉。最後一個經驗豐富家醫科醫生，告知患者「這可能是甲狀腺的問題，要去看內科」才發現這是甲亢的症狀，調整好藥物很快就好了。很多時候人體很多時候是一個連動的生態系統，有些問題的表象跟真正的Root Cause是兩回事，所以患者很容易找錯醫生弄錯科目。

  
但如果是在好的健檢中心，做法就完全不一樣了。健康檢查會根據你的全方位給予檢查——最後針對你的完整報告進行討論，這時候甲亢的 Root Cause 很快就會被最後的把關者抓出來 " **問題根本不在心臟，而在甲狀腺 "** 。這就是「多人協作的力量」。

**AI Agent 的世界也是一樣的道理。越複雜的場景，我們需要Multi Agent System**

### 什麼是 Multi-Agent System？

簡單講，就是讓多個 AI Agent 組成一個團隊，每個 Agent 扮演不同的專家角色，針對同一個複雜問題進行協作。就像醫療會診一樣——不是一個醫生包辦所有事情，而是心臟科、內分泌科、家醫科的醫生坐在一起討論，各自貢獻專業判斷，最後整合出一個系統性的解決方案。

### 單一 Agent 的三大限制

  
當處理複雜任務的時候，單一 Agent 有三個根本性的限制：

**Context 窗口是有限資源** : 單一 Agent ，通常他都是設計為單一任務的。Context 窗口如果拿來處理複雜多場景窗口，不同場景的 RAG 會互相競爭，產生知識污染。舉例 PR 在三個領域完全不同的意思：

        1. 軟體開發： Pull Request
        2. 公關行銷： Public Release 
        3. 人資管理： Performance Review

當我們問講「請幫我看一下這個 PR」，如果他剛好是 IT 開發一個人資管理系統的對話，那到底是幫忙看一下 Performance Review 結果，還是幫忙看一下這個 code change 呢？

**推理深度受限 :** 複雜問題需要多層推理（觀察現象→分析原因→找出根因→提出方案），單一 Agent 容易在第 2-3 層就迷失方向，或者根據 Google 的podcast 的說法， Agent 在多步驟的時候容易出現不知所措(overwhelm)

  
**缺乏交叉驗證 :** 單一 Agent 給出的結論沒有其他角度的檢驗。它可能給出一個「聽起來很合理」的答案，但實際上是錯的。就像舉的甲亢的例子，單一醫生的診斷可能被表象影響有盲點，需要其他專科醫生的意見來驗證或補充。

### 實驗數據

[LangChain 做了一個 Benchmark ](https://ai-coding.wiselychen.com/na-tian-wo-zai-chan-ye-yuan-qu-fen-xiang-ai-neng-bu-neng-zuo-qi-lai-qi-shi-kan-ren/), 他發現當越多不同領域的知識丟進來同一個 Workload ，Single Agent 的效率就明顯的下降，但是multi agent 卻可以保持一個較佳的 performance 

![](/assets/images/image-30.png)

另外從成本上來看，越複雜的場景，single agent 的 使用 token 數也明顯上升 

![](/assets/images/image-31.png)

### 基本範式

根據大家的說法，Multi Agent 基本範式大概就是幾個

![](/assets/images/image-32.png)截圖來自 GCP 的 Video [https://www.youtube.com/watch?v=TGNScswE0kU](https://www.youtube.com/watch?v=TGNScswE0kU&ref=ai-coding.wiselychen.com)

Supervisor : 有點像是人的組織，有一個管理者，跟工作者。如果用管理團隊來舉例，經理就是 Supervisor ，下面有 EngA , EngB , EngC ... Agent 進行協作。剛剛舉的健康檢查醫療團比較像是這個，有很多科室進行會診，但是最後有一個 coordinator 主治醫生來做最後判斷。

Deterministic Flows : 基本上有一個工作流，或是像是生產線一樣的。舉例，像是軟體開發這樣的工作流，有 PM Agent -> Backend Eng Agent -> Frontend Eng -> QA Agent -> DevOps Agent 

Swarm ：N to M 的關係，有點像是網路上流行的智囊團/AI董事會 Agent 群。

**單一 Agent vs 多Agent**

單一 Agent 優點非常明顯，簡單。當你做你擅長的單任務時，就用 Single Agent 即可。當你日常遇到小感冒的時候，就去找診所即可，不用每次都請一個醫療團。當然缺點就是剛剛說的，處理複雜任務會有明顯的效能下降，不知所措

多 Agent 就是架設困難，成本較高，所以小任務就不要殺雞用牛刀。但是在處理複雜任務時，真的比 Single Agent 來得好。為了架設多 Agent ，現在還出了 Agent to Agent 協議，以及多 Agent 如何共享記憶體的 infra。 

另外一個很容易發生的問題就是，有一些 critical context 容易在 Agent 跟 Agent 傳遞訊息時遺失，造成 downstream agent 判斷錯誤。像不像一般的公司組織，很多時候組織前線單位傳遞訊息遺失，造成大後方管理誤判。

### 總結

Multi-Agent System 的核心不是「有多少個 Agent」，而是：

1\. 角色分工是否明確？（每個 Agent 的專長是什麼）

2\. 溝通機制是否順暢？（Agent to Agent 協議、記憶體共享）

3\. 整合邏輯是否清楚？（最後誰來做決策、如何處理衝突）  
就像醫療會診一樣，不是醫生越多越好，而是每個醫生都能貢獻專業判斷，最後由有經驗的主治醫生整合出最佳方案。

下一步

這篇文章介紹了 Multi-Agent 的基本概念和三種範式。如果你想深入了解：

\- 每種範式的實際實現（LangGraph、AutoGen、CrewAI）

\- 如何設計 Agent to Agent 的通信協議

\- 如何處理 context 傳遞遺失的問題

\- 實際專案的踩坑經驗

我會在後續文章中詳細分享。
