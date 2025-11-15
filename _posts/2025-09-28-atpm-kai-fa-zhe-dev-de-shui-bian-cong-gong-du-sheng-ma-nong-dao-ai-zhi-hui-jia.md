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

[ ![Wisely Chen](/content/images/size/w160/2025/09/6672228-F20250919----02-----------SN------10945w-1.jpg) ](/author/wisely/)

#### [Wisely Chen](/author/wisely/)

28 Sep 2025 — 11 min read

![\[ATPM\] 開發者 \(Dev\) 的蛻變—從embed , copilot 到 agent](/content/images/size/w1200/2025/09/Generated-Image-September-28--2025---10_17PM-1-1.png)

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

[ ![\[Agent模式 Part 2 \] 臨機應變 vs 讀著路書跑 — 為什麼 AI Agent 需要 Plan & Exec 模式](/content/images/size/w600/2025/11/ChatGPT-Image-2025---11---1----------11_27_12.png) [Agent模式 Part 2 ] 臨機應變 vs 讀著路書跑 — 為什麼 AI Agent 需要 Plan & Exec 模式 WRC 賽車最經典的場面就是除了賽車手開著市售車款飛天遁地以外，最有趣的就是旁邊坐著一個副駕，讀著一本稱為「路書」的路線圖，用一些簡略的話去指引賽車手前進。 這個設計在追求速度的賽車界很有趣，因為坐一個副駕更重呀，為何需要把複雜的任務分成兩個角色——規劃者和執行者? 原因很簡單，WRC的賽道都是非常複雜，路況多變的越野賽到，他們經驗發現「規劃者搞清楚計劃，執行者全力執行然後隨機應變最有效率」 回到 AI Agenrt ，你有沒有想過當一個 AI 被指派一個複雜任務，它的腦子裡是怎麼想的？ 上一篇我們比較 AI Workflow 跟經典的 ReAct Agent， 我們看到 ReAct Agent 最後解決了客戶問題。但你有沒有想過，在 ReAct Agent 的彈性的優點下有沒有哪個致命的問題。今天來介紹一下一個新的 Agent 模型，或許是現在大家最常看的 Plan & Exec 模型。 Plan-and-Execute Plan-and-Execute（計畫與執行） By Wisely Chen 01 Nov 2025 ](/mang-mu-jia-su-vs-du-zhu-lu-shu-pao-wei-shi-mo-ai-agent-xu-yao-plan-exec-mo-shi/) [ ![\[Agent 模式 part 1\]  - Workflow 型和 ReAct 型，誰更像你？](/content/images/size/w600/2025/10/ChatGPT-Image-2025---10---30----------10_36_55.png) [Agent 模式 part 1] - Workflow 型和 ReAct 型，誰更像你？ 你有沒有發現，自己工作中也分裂成兩個人，有時按規則做事，有時根據現實應變。其實AI Agent 也一樣。想像一下下面的場景 客戶問：「我想查詢上個月的訂單」。 Agent A Agent : 連接「訂單歷史資料庫」 ❌ 連線失敗（資料庫正在維護） Agent : 系統回答客戶：「抱歉，我們的系統現在無法查詢。請稍後再試。」 結果：客戶必須稍後重試，專業一點的 Agent 就是會請人介入談話 Agent B Agent : 連接「訂單歷史資料庫」 ❌ 連線失敗（資料庫正在維護） Agent 觀察：思考：「主資料庫不通。但我的目標是『找到訂單』，不是『從主資料庫查訂單』。 有其他方式嗎？我們有備份系統嗎？」 Agent 行動：查詢「訂單備份硬碟」觀察：✓ 找到訂單 By Wisely Chen 30 Oct 2025 ](/agent-mo-shi-part-1-workflow-xing-he-react-xing-shui-geng-xiang-ni/) [ ![为什麼 AI Agent 无法企業落地？看泰山的挑水工就懂了](/content/images/size/w600/2025/10/-------2025-10-28-------10.13.48.png) 为什麼 AI Agent 无法企業落地？看泰山的挑水工就懂了 今天刷到一張照片，泰山樓梯上，一個白髮蒼蒼的挑水工用扁擔挑著水，一步步往上爬。除了心疼他的辛苦，還看到評論區飄出一條大橫幅 人口紅利正在減弱，以後替代的就是無人機紅利 這簡直一句話點燃了整個思維導火索。是呀、對呀、完全講得通啊 泰山挑水 = 無人機的完美技術應用場景 老齡化 + 無人接班 = 業務痛點 對的技術選型，有痛點，啟動專案的先決條件全部吻合。所以呢，立刻啟動項目、尋找無人機規格、選廠商、進行試點……邏輯完全沒毛病。 真的是這樣嗎？ 回覆區有人發了一句話，說得讓數位轉型顧問們恨不得摀臉——根本用不著什麼無人機黑科技，早就有個老東西完美解決這個場景：纜車。便宜、穩定、用了一百年了。 這就像我們在轉型會議室天天上演的劇碼：某個 AI 顧問拎著最新的 AI 大殺器進場，PPT 講得飛起，結論是「降本增效不能再好」。最後甲方的老 IT歪著頭問了一句——「等等，這事兒用批次自動化不就完了？」一句話， By Wisely Chen 29 Oct 2025 ](/shu-wei-zhuan/) [ ![超慢跑也能 Coding：Claude Code 帶來的真正生產力](/content/images/size/w600/2025/10/-------2025-10-26-------6.58.28-1-1.png) 超慢跑也能 Coding：Claude Code 帶來的真正生產力 大家都說 AI可以增加生產力，那到底啥是真正的生產力？ 今早台北下大雨，我在家陽台跑了一小時的超慢跑，上面的圖是我的環境。這一小時裡，我同時做了四件事： 1\. 運動 : 超慢跑 2\. 知識擷取: 聽Youtube Video (AI Topic) 3\. Vibe Coding / 數據分析 : Claude Code 4\. 網頁搜尋資訊: ChatGPT Altas 這個工作流之所以可行 ，因為「超慢跑 」+ 「Claude Code」 這個組合根本就是天作之合，超慢跑並非慢跑很安全，不需要太多注意力。 Claude Code 老實說真的在做事的時候，95% 的時間不需要去顧，但是總是有 5% 的需要出來 debug 一下，這時候超慢跑停下來一兩分鐘也沒差。 我這樣的 routine 已經持續了3個月之久了，如果是出太陽的時候， By Wisely Chen 28 Oct 2025 ](/vibe-duo-ai-ru-he-zeng-jia-wo-de-sheng-chan-li/)