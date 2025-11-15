---
layout: post
title: "[ATPM] 開發者 (Dev) 的蛻變—從embed , copilot 到 agent"
date: 2025-09-28 14:19:39 +0000
permalink: /atpm-kai-fa-zhe-dev-de-shui-bian-cong-gong-du-sheng-ma-nong-dao-ai-zhi-hui-jia/
image: /assets/images/Generated-Image-September-28--2025---10_17PM-1-1.png
description: "三種層次的人跟AI協作模式..."
---

[ATPM](https://ai-coding.wiselychen.com/tag/atpm/)

# [ATPM] 開發者 (Dev) 的蛻變—從embed , copilot 到 agent

[ ![Wisely Chen](/assets/images/6672228-F20250919----02-----------SN------10945w-1.jpg) ](/author/wisely/)

#### [Wisely Chen](/author/wisely/)

28 Sep 2025 — 11 min read

![\[ATPM\] 開發者 \(Dev\) 的蛻變—從embed , copilot 到 agent](/assets/images/Generated-Image-September-28--2025---10_17PM-1-1.png)

#### 三種層次的人跟AI協作模式

還記得大約兩年前 ChatGPT 剛出的時候，我在中國網路上就看到一張關於「人與AI協同的三種模式」的圖，時至今日，我一直拿他出來講的原因是，不管這個世界工具怎麼演進，我們的模式都一直在這張圖的三個層次當中打轉

![](/assets/images/image-38.png)這張圖我在 2023 年3月我就看過了，不確定出處，但是我真的很喜歡這張圖，而且這個比較像是一個預言，到現在還是無法脫離

我認為它清晰地描繪了我們與 AI 協作的美好藍圖，如果從 Coding 這個場景來說，將協作模式分為三個層次，

  1. **Embedding 模式** ：這是最基礎的應用。我們把 AI 當作像 Google 一樣的對話助手，需要的時候問一下、找點資料或建議，但絕大部分的工作還是由人類手刻完成。AI在這邊是一個知識庫或是助手，不佔據任何主動的性質。AI Coding 的場景下，embedding 就是 ChatGPT 這個介面。
  2. **Copilot 模式** ：這是更進階的協作，這裡通常要搭配特定的工具配合 。我們預先設定好目標與規格，將其中一部分任務交由 AI 完成初稿，但人類必須介入進行修改、調整與最終確認。AI 的工作成果需要被嚴格檢核。所以在這個情況下，人依舊是需要大量的專業知識去輔助的，但是已經有很快的加速。AI Coding 下，Cursor 初期是一個代表性的產品
  3. **Agent 模式** ：這是終極的理想型態。我們把 AI 當作一個真正的員工或代理人，只需指派任務，它便能自主進行規劃、取用工具、推理，並最終交付成果。人依舊要驗證產出的結果，但是在這個情況下，其實人通常不需要知道細節，或是改不太動細節了，因為他只要看 output 即可。AI Coding 下，Claude Code , Cursor Agent 模式，Replit 都是很經典的產品

在 AI Coding 這個場景下，我的團隊從 2023 開始，就一直處於 Embed (把 ChatGPT 當 Google 來用) 這種模式，在一開始很成功的原因是「沒有 Embed 模式的 AI , 這個團隊建不起來」，這是 0 -> 1 的 binary 問題  
  
隨著團隊越來越大，cursor , Sonnet 3.5 , BigQuery MCP 三本柱出現，我們進入了 Copilot 模式。這個時候 AI Coding 的速度飛躍，我們也開始重視 context engineering 的部分概念，並且落地在 .cursorrules , 那時候 cursor 還沒改方案，美好的那幾個月.  
  
Copilot mode 很多很好，就是沒有標準化，後來我們要做帳務系統，隨著場景越來越大，我們設計了 ATPM 讓 Context 都統一落地到 PRD ，讓整個協作體系越來越標準，並且也慢慢進入了 Agent 模式...我們試著切到 Agent 模式，但是很快因為 Claude Code降智很快切回來，也意識到 QA 體系沒建立前不能直接那麼大辣辣進去 agent

以下為細節

### **我們團隊的經驗 : 一開始 Embed**

就我們團隊建隊來說，我們幾乎2023/09 ~2025/01 都處於 embed 模式，基本上大量使用 ChatGPT , Google Sheet , Make.com , BigQuery , Google Chat Tasks來做事情，基本上傳遞訊息還是靠一般的軟體開發流程(Kaban,Scurm)，AI在這邊是一個助手，但是從來就不是一個獨立的單點。

![](/assets/images/image-39.png)

### 0 -> 1 的關鍵因素

Embed 這個模式那時候在我們團隊非常的成功，因為我那時候要解決的問題是「找不到軟體工程師」的 0->1的問題，用 非資訊系+ ChatGPT做 embed 模式非常合適。我們大量使用 BigQuery 跟 Google Sheet 當作 PaaS 載體，我們每天都是問 Code Snippet 

  1. BigQuery SQL Code Snippet 
  2. Google Sheet 公式 Code Snippet 
  3. Google Sheet App Script Code Snippet 

基本上 embed 可以 work ，就是因為每次問答就是一堆 code snippet 來調整或是撰寫，需要提供上下文不多。需要的工作都在一個 Prompt 左右就可以，舉例

> 我想要寫一個Google Sheet 公式，將 A:B 之間的數字取 XXX ...

### Embed 的好處

最重要的就是流程整合簡單，基本上不需要改流程，只需要某一個節點 AI特別方便的，改成用 AI 去做，人機整合的方式就是 Copy&Paste; Prompt 過去就好，在這邊通常都會整理出很多可以重複使用的提示詞，我們通常會寫成 SOP +Promot文件大全 當作經驗傳承，也就這樣簡單的管理模式就弄了一年多，基本上很好實施。

### Embed 的問題

只是當我們越來越成功，要解決問題越來越複雜，到ChatGPT 的 Context 就越來越多，甚至為了寫 BigQeury SQL ，還要先打一堆 BigQuery Schema 在前面，越來越煩，效率也低下

![](/assets/images/image-41-1.png)每次都要截圖 BigQuery 有點煩

我曾經買了 1年的 Monica ，主要就是每次寫 BigQuery SQL 的時候，直接用側邊欄的 Monica 來截圖 BigQuery Schema 系統截圖，這樣方便 SQL 撰寫。不過基本上沒解決上下文的問題，很快的隨著工具快速演進，我們切到了 CoPilot 。

## **ATPM : Copilot 模式**

後來隨著 Cursor 的進步，我們很快就在嘗試 cursor 對寫程式的近一步加速。主要的 trigger point 是 Cursor + Claude Sonnet 3.5 + BigQuery MCP 可以用，我們幾乎是立馬就奔向 Copilot 模式。

![](/assets/images/image-42-1.png)

沒辦法，有了 BigQuery MCP ，寫 SQL 有 BigQuery MCP，不用提供 Schema 了。另外 Claude Sonnet 3.5 有時候還會去查一下 BigQuery 的 table 前 100筆，看看長啥樣子，才會去寫相關的程式碼。對我們寫程式碼的提效大概 2~5倍左右吧。

有一次在於我們某一次針對一個 excel 公式轉 SQL 場景，我們覺得 excel 裡面公式太多了，上百個，一個一個叫 Cursor 去轉加速能力不高，還不如人來手刻，因為我們知道邏輯。這時候我跟他們說，我們試試看叫 Claude 去直接看含幾百個公式的 excel 檔案，然後直接將裡面幾百個公式轉成 SQL 。

![](/assets/images/image-43.png)

結果真的一次過，Claude 3.5 那時很強悍的，直接很勤勞的寫一堆 python ，把 fomula 印出來，然後把整個上百個公式一次搞定。看到這段，我們超 high 的，這簡直是把 3~5天的工作變成 5分鐘完成。

這時候 ATPM 的 Dev 原型基本出來了，我們在開發階段根據 excel 裡面公式內容，轉成放到 .cursorrule ，然後根據 .cursorrule 紀錄資料表來源、計算規則、計算方式分類（箱數、材積等）​。當然隨著之後我們進入到 Copilot/Agent 模式，.cursorrule 改成 PRD 的形式。

### Copilot 好處跟壞處

通常 Copilot 只要跑得起來，效率跟人工比起來一定是碾壓。因為 Embed 進入 Copilot 模式最難的還是人要撰寫一個明確目標，跟相關的細節邏輯，讓 AI 可以自動執行，只要有這個前提，基本上都是效率碾壓，像是剛剛說的 excel 轉 SQL 。

另外 Copilot 模式跟 Agent 模式比最大的好處是，人在每個時間點都可以停下來，人可以隨意暫停，進去驗證，或是 rollback 。所以人其實一直都保持著切成人工的按鍵按下。這個對於驗證 AI 的幻覺非常的重要。

壞處其實就是要有人去寫相關的目標，跟拆解成 AI可執行的文字。這個前提其實不一定每次都可以滿足。對於大任務當然會有 PM 做，但是對於很多 random 任務，其實有點太 heavy 。

另外一個壞處就是 Copilot 其實不夠標準化，每個人拆解任務寫下來的方式都不同，讓 AI 進去做某個業務的範圍也見仁見智，所以有些人進去 Copilot 模式，某些人就自己用自己的 embed 模式，對管理者來說，每個人+AI都是獨立作業某個獨立的區塊，不容易跟其他人合作。

## 標準化 Copilot + 部分 Agent 模式

其實到 Copilot 模式我們 team 已經很滿意了，但是我那時候遇到更大的挑戰，我們要用 AI Coding 做出一個全業務的帳務系統。我們需要一個能夠

  1. 現在 10倍大系統的體系，所以 Copilot 模式要標準化，並且讓當時的工讀生都可以參與
  2. 因為要算錢，我們需要一個完整避免幻覺的 QA 機制。並且這個 QA 體制，可以直接驗證 Agent 的成果

基於這個要求，我們根據那時候 91APP在年會分享的流程，做出了現在的 ATPM 

![](/assets/images/image-44.png)

ATPM Dev是可以接 Agent mode 的，只是我們當下 Dev 主體是 Copilot Mode，( .cursorrule +Excel 改成 PRD) 。當時我們的工具以及團隊的積累，不是不能做 Agent Mode ，只是帳務系統需要大量驗證，如果 Agent mode 很難說服 BU 。另外當下 QA方式也在設計中，怕一次步子邁太大。

另外為了這個帳務系統，我們除了 QA以外，還在 Dev 過程加入類似 Unit Test 機制，餵入相關部分驗證數據來請 AI 自動驗證部分 SQL 模組成果是否正確

![](/assets/images/image-45-1-1.png)Cursor 的輸出

就如同我說的，只要寫好 PRD 當作 South of Truth ，其實先期用 Copilot Mode ，後面再用 Agent Mode 也沒關係。我那時候也試著把一兩個小業務試著用 Agent Mode 加上 PRD 來撰寫，只是那時候 Claude Code 突然之間降了智，穩定性難以預測。我就先暫停 Agent Mode 的嘗試，避免造成專案 delay 。

## QA的保證是 Agent Mode的核心要素  

在商業世界裡，**最終必須有人為產出的品質負起全責** 。這意味著無論 AI 多麼強大，我們都無法完全放手。畢竟 AI 最不能做的就是 「背鍋」

在這個情況下，我們要選擇做好幕約在2025年會說的「人的價值在於開案跟驗收」，簡單講就是 PRD撰寫，跟QA驗收。所以 ATPM 極度強調

  1. PRD 撰寫跟反饋
  2. QA驗證的重要性

至於 Dev , 要走 Copilot mode 還是 Agent Mode ，其實都是很容易的切換的。

這篇文章差不多把 Dev 的起源跟轉變講的差不多，最後的下一篇要來講 QA 

[ ![Multi-Agent 協作模式：當 AI 學會「會診」這件事](/assets/images/ChatGPT-Image-2025---11---15----------04_36_04.png) Multi-Agent 協作模式：當 AI 學會「會診」這件事 我上週回老家看了久違的第四台「緯來日本台」，看一個日本節目「恐怖家庭醫學」，裡面講到一個年長者「最近常常心悸、手抖、睡不好」。因為是心臟的因素，所以患者直接找心臟科檢查後，拿到一疊厚厚的報告——結果心臟科醫生看完報告說：「你的心臟結構完全正常，心電圖也沒問題，可能是壓力太大，回去多休息就好。」患者心想：「可是我真的有心悸啊！難道是我自己想太多？」於是患者找了神經科說可能是自律神經失調，拿了藥物減壓，但症狀完全沒改善。 弄了很久一直兜兜轉轉。最後一個經驗豐富家醫科醫生，告知患者「這可能是甲狀腺的問題，要去看內科」才發現這是甲亢的症狀，調整好藥物很快就好了。很多時候人體很多時候是一個連動的生態系統，有些問題的表象跟真正的Root Cause是兩回事，所以患者很容易找錯醫生弄錯科目。 但如果是在好的健檢中心，做法就完全不一樣了。健康檢查會根據你的全方位給予檢查——最後針對你的完整報告進行討論，這時候甲亢的 Root Cause 很快就會被最後的把關者抓出來 " 問題根本不在心臟，而在甲狀腺 " 。這就是「多人協作的力量」。 AI Agent 的世界也是一樣的道理。 By Wisely Chen 15 Nov 2025 ](/multi-agent-xie-zuo-mo-shi-dang-ai-xue-hui-hui-zhen-zhe-jian-shi/) [ ![那天我在產業園區分享：AI 能不能做起來，其實看人](/assets/images/S__88875042.jpg) 那天我在產業園區分享：AI 能不能做起來，其實看人 今天我在新北產業園區，在我們公司的 AI 轉型的活動 在各位傳統產業的前輩講述我之前在傳統產業做 AI 轉型的經驗 我認為「 AI 要在傳產落地，先解決的永遠不是模型，而是人、流程與文化。」 我把這幾年的實戰經驗濃縮成一套能在傳統產業中真正起作用的框架： 現況分析：先理解現場，再談技術 我們創建了一個以 公司各部門的老前輩 + Intern 為主的種子團隊，深入一線流程、取得高層支持，建立真正的共識。 AI 不是空降，而是跟現場一起改。 快速勝利：小範圍試點，讓大家看到成效 選一個可控的場域，把 AI +種子團隊拉進真實流程。 像我用 AI + RPA + OCR + 快速掃描器 = 一個可持續可落地，並且有效益成果 這樣的「小勝利」，是推動組織願意往下走的關鍵。 全面升級：從工具導入到組織轉型 把建置的種子團隊散步到全公司各個部門 可以用很快的速度去 scale 全面開花 By Wisely Chen 13 Nov 2025 ](/na-tian-wo-zai-chan-ye-yuan-qu-fen-xiang-ai-neng-bu-neng-zuo-qi-lai-qi-shi-kan-ren/) [ ![AI 信任崩塌的真正原因：勞資零和賽局的再現](/assets/images/ChatGPT-Image-2025---11---10----------09_24_03.png) AI 信任崩塌的真正原因：勞資零和賽局的再現 根據《Harvard Business Review》近期發表的〈Workers Don’t Trust AI. Here’s How Companies Can Change That〉，美國基層員工對公司提供的 AI 工具信任度在短短數月內暴跌：對生成式 AI 的信任下降 31%，對自主決策型 AI 更下滑 89%。近半數員工反而更信任非官方AI 工具。另外無獨有偶MIT 的研究《The GenAI Divide: State of AI in Business 2025》更進一步揭示了這種現象，並命名為 Shadow AI：員工在公司外私下使用未授權的 AI 來完成工作。研究指出，約有 By Wisely Chen 10 Nov 2025 ](/ai-xin-ren-beng-ta-de-zhen-zheng-yuan-yin-lao-zi-ling-he-sai-ju-de-zai-xian/) [ ![\[Agent part 3\] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵](/assets/images/ChatGPT-Image-2025---11---8----------08_01_49.png) [Agent part 3] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵 大家都知道我用 AI 來 enable 很多intern 來當作很多正職的事情，當然他們雖然都很年輕跟熱情，但是我管理團隊時發現一個規律： 當我派給幾個 Senior 的同事 ，我通常只需要 weekly 跟他開會，給他幾個任務，一週後檢查一次就好。他可以獨立工作，中間遇到問題會自己判斷、調整，如果有大問題他們會舉手跟我講，不容易走偏。 當我要安排工作給我的 intern ，跟 Senior 最大的不同就是， Junior 我通常會每半天或是每過一天就會跟他聊一下提醒一下可能要注意什么事情。因為他很容易遇到了某些複雜任務時，他就可能在某一步卡住，又沒有舉手，基於錯誤理解繼續做下去，最後整個方向偏了，也浪費了他整天的時間。 這是Sr 跟 Jr 經驗的差別，獨立作戰的能力 AI Agent 也是如此 現在考驗 AI Agent 最大的地方，不是他的智商，主要著重點是它的連續工作穩定性。如果人類需要介入的越少，就代表它可以自主完成工作， By Wisely Chen 08 Nov 2025 ](/agent-part-3-interleaved-thinking-cheng-xian-de-wen-ding-xing-shi-xian-zai-agentluo-di-de-zhong-yao-guan-jian/)