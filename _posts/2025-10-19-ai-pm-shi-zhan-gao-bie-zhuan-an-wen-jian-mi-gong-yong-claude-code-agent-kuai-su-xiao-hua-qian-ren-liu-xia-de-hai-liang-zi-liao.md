---
layout: post
title: "【AI PM 實戰】告別專案文件迷宮！用 Claude Code Agent 快速消化前任留下的海量資料"
date: 2025-10-19 10:01:44 +0000
permalink: /ai-pm-shi-zhan-gao-bie-zhuan-an-wen-jian-mi-gong-yong-claude-code-agent-kuai-su-xiao-hua-qian-ren-liu-xia-de-hai-liang-zi-liao/
image: /assets/images/Generated-Image-October-19--2025---5_19PM.png
description: "身為 PM，你是不是也遇過這種狀況：你得在極短時間內看完前任PM所有東西？ 這時候除了認命加班看文章，有沒有更好的方式？試試看 AI Agent 吧..."
---

[pm](https://ai-coding.wiselychen.com/tag/pm/)

# 【AI PM 實戰】告別專案文件迷宮！用 Claude Code Agent 快速消化前任留下的海量資料

[ ![Wisely Chen](/content/images/size/w160/2025/09/6672228-F20250919----02-----------SN------10945w-1.jpg) ](/author/wisely/)

#### [Wisely Chen](/author/wisely/)

19 Oct 2025 — 7 min read

![【AI PM 實戰】告別專案文件迷宮！用 Claude Code Agent 快速消化前任留下的海量資料](/content/images/size/w1200/2025/10/Generated-Image-October-19--2025---5_19PM.png)

身為 PM，你是不是也遇過這種狀況：你得在極短時間內看完前任PM所有東西？ 這時候除了認命加班看文章，有沒有更好的方式？試試看 AI Agent 吧

身為 Claude Code的愛好者，我發現 Claude Code Agent 不只是 Vibe Coding ，他是可以在方方面面能真正幫 PM 和技術人員省下大量閱讀時間的好幫手。

## 我遇到的真實案例

這兩週公司剛好有個資深 PM 要調整職務。偏偏他負責的是我們最大的海外客戶，而且這位老兄還是個「文件紀錄狂」——光是 Google Drive 裡就有 **50+ 個專案** 的完整文檔 , **數百個檔案** ，橫跨三四年。從提案、合約、執行細節、會議記錄、Change Request 到客戶 Q&A;，應有盡有

以前沒有 AI 的時候，因為我不是主要交接人（但我帶 PM 團隊），通常抓個大概就過了。但現在有 AI 了，你想想，Claude Code 連大量歷史程式碼都能看懂並抓出重點，那這些專案文件應該更是小菜一碟吧？

### 專案文件的環境

  * 儲存: 專案文件都在 Google Drive 上
  * 檔案格式: 格式很不穩定(Docx , google doc , PPTX , Excel , Google Sheet, PDF...etc) 
  * 專案類型: 有維運，有開發，有CR , 有雲的 infra , 也有 Machine Learning 

我這次 Agent 選擇的是 Claude Code ，一開始使用 Sonnet 4.5 ，後來因為 Claude Haiku 4.5剛出，我也將幾個任務用 Haiku 來做，處理這種任務，速度很快體感不錯。

### 本次目標

  1. 快速知道這個大客戶之前的來龍去脈，有個具體的 folder summary 最重要, 並且針對幾個正在進行中的專案有更詳細的認知
  2. 拉出一個客戶的專案演進時間線
  3. 拉出所有專案的技術線
  4. 分析專案 folder / file naming rule 擺放, 提供相關建議

![](/assets/images/Generated-Image-October-19--2025---5_41PM--1--1.png)

根據之前的經驗， 這種等級的交接，接手人來做用幾週內能做到 #1 就萬幸了，但是有了 AI ，我們 #2 ~ #4應該都有機會。

最後結果是 #1 ~ #4 都做大概 1天搞完，但是 Claude Code 好處是放給他跑，我來開會，不太浪費時間。最後換成 Haiku 速度更快。另外值得一提的彩蛋是，在接手的那幾天，剛好被客戶問到 (Aka : 凹）加入一個新的 data field ，我立馬請 Claude Code 去爬整個一年多的專案 meeting note PDF/PPT ，後來發現裡面會議記錄沒有 commit 這個 data field ，就成功打回去...XD

### 場景 1 : 全專案 Summary 

這個應該是最容易的 , 我的做法是先用 [GDrive MCP](https://github.com/isaacphi/mcp-gdrive?ref=ai-coding.wiselychen.com) 直接請 Claude Code 

  * Step 1 : MCP 去爬裡面的檔案列表
  * Step 2 : 然後根據列表去讀裡面每一個檔案，取出大概在幹嘛
  * Step 3 : 最後產生出 Summary

原本使用 Google Drive MCP ，是可以用，但是在 Step 2 下速度就慢非常多，後來改採用 Google Drive 原生 APP 去下載到 local disk 之後，再寫 python 分析檔案，會快非常多。會選擇下載下來的另外一個原因是，Claude Code 其實很多時候工具鏈原生使用 Unix 指令庫 find / head / tail / wc / grep 來做很多基本操作，而且效果很好，用 API 當 backend 的 MCP 速度會比較慢，也不少問題。後來決定還是全抓下來再做，整體分析速度快 100倍​。

![](/assets/images/image-27-1.png)Claude Code 用很多 Unix Command 

最後出來的 Summary 很不錯，每個檔案都有 AI看過（這個人就很難做到），然後給出 Summary 

![](/assets/images/image-29-1.png)

同場加映 : Gemini , 因為是 Google Drive ，我在這也試過 Google Drive 旁邊 UI 的 Gemini 來做，很可惜 Gemini原生效果很差，連 Summary 出來的 folder 數量都錯很多，更別說 Summary 的內容了。

### 場景 2 : 本客戶的所有專案的總時間線

如同我說的，這是一個大客戶, 50幾個專案的總文檔，我請 Claude Code 根據裡面所有有專案時間的檔案，匯總出一個超大的歷史時間線。這個當然人做得到，但是是要對專案很理解的人才能做，如果像我們這種剛接手的人來說，有時間線真的很幫助理解。

![](/assets/images/image-30-1-1.png)

### 場景 3 : 本客戶的所有專案的總技術線

這個用 Claude Code 來做也不難，提示詞"將裡面專案所使用的技術棧都列出來 , by project ，最後就這個客戶做匯總即可" ，這可以幫助我們快速知道如果有問題，大概技術棧使用哪些技術

![](/assets/images/image-32-1.png)

### 場景 4 : 本客戶的所有專案的folder 命名規則匯總

最後身為PM，想也知道裡面專案，每個 PM 都不同，命名規則一定有很多不同。借這個機會進行問題統整分析一下，等到明確專案接起來之後，再請 Claude Code 根據 Google Drive MCP 來進行 folder / naming 調整。

![](/assets/images/image-31-1.png)

### 寫在最後：AI 不是來搶你飯碗，真的是來幫你升級的

這次實測下來，我最大的感想是：AI Agent 真的把 PM 的工作效率提升到另一個層次。

AI真正用法應該是人做不好的事情以外的補充，舉例以前面對這種交接案，光是看文件就要花好幾週，更別說整理出時間線、技術線這種「想做但沒時間做」的事。現在有了 Claude Code，不只基本任務做得更快更準，連以前「想做但做不到」的深度分析都能實現。

但這不代表 PM 可以完全依賴 AI。AI 幫你省下的時間，應該用來做更有價值的事：「把人搞好」，因為 PM 最重要的任務是把團隊當中的人（客戶，team , partner )理順，詳實記錄只是一個基本工作。

**另外一個結論 , Claude Code 這樣的 Agent 真的可以做很多 VIBE Coding 不同的工作。** 如果你也是 PM 或技術人員，面臨類似的文件地獄，真心建議試試看 Claude Code。它不只是個工具，更是能讓你從「埋頭苦幹」升級到「高效決策」的好夥伴。

[ ![\[Agent模式 Part 2 \] 臨機應變 vs 讀著路書跑 — 為什麼 AI Agent 需要 Plan & Exec 模式](/content/images/size/w600/2025/11/ChatGPT-Image-2025---11---1----------11_27_12.png) [Agent模式 Part 2 ] 臨機應變 vs 讀著路書跑 — 為什麼 AI Agent 需要 Plan & Exec 模式 WRC 賽車最經典的場面就是除了賽車手開著市售車款飛天遁地以外，最有趣的就是旁邊坐著一個副駕，讀著一本稱為「路書」的路線圖，用一些簡略的話去指引賽車手前進。 這個設計在追求速度的賽車界很有趣，因為坐一個副駕更重呀，為何需要把複雜的任務分成兩個角色——規劃者和執行者? 原因很簡單，WRC的賽道都是非常複雜，路況多變的越野賽到，他們經驗發現「規劃者搞清楚計劃，執行者全力執行然後隨機應變最有效率」 回到 AI Agenrt ，你有沒有想過當一個 AI 被指派一個複雜任務，它的腦子裡是怎麼想的？ 上一篇我們比較 AI Workflow 跟經典的 ReAct Agent， 我們看到 ReAct Agent 最後解決了客戶問題。但你有沒有想過，在 ReAct Agent 的彈性的優點下有沒有哪個致命的問題。今天來介紹一下一個新的 Agent 模型，或許是現在大家最常看的 Plan & Exec 模型。 Plan-and-Execute Plan-and-Execute（計畫與執行） By Wisely Chen 01 Nov 2025 ](/mang-mu-jia-su-vs-du-zhu-lu-shu-pao-wei-shi-mo-ai-agent-xu-yao-plan-exec-mo-shi/) [ ![\[Agent 模式 part 1\]  - Workflow 型和 ReAct 型，誰更像你？](/content/images/size/w600/2025/10/ChatGPT-Image-2025---10---30----------10_36_55.png) [Agent 模式 part 1] - Workflow 型和 ReAct 型，誰更像你？ 你有沒有發現，自己工作中也分裂成兩個人，有時按規則做事，有時根據現實應變。其實AI Agent 也一樣。想像一下下面的場景 客戶問：「我想查詢上個月的訂單」。 Agent A Agent : 連接「訂單歷史資料庫」 ❌ 連線失敗（資料庫正在維護） Agent : 系統回答客戶：「抱歉，我們的系統現在無法查詢。請稍後再試。」 結果：客戶必須稍後重試，專業一點的 Agent 就是會請人介入談話 Agent B Agent : 連接「訂單歷史資料庫」 ❌ 連線失敗（資料庫正在維護） Agent 觀察：思考：「主資料庫不通。但我的目標是『找到訂單』，不是『從主資料庫查訂單』。 有其他方式嗎？我們有備份系統嗎？」 Agent 行動：查詢「訂單備份硬碟」觀察：✓ 找到訂單 By Wisely Chen 30 Oct 2025 ](/agent-mo-shi-part-1-workflow-xing-he-react-xing-shui-geng-xiang-ni/) [ ![为什麼 AI Agent 无法企業落地？看泰山的挑水工就懂了](/content/images/size/w600/2025/10/-------2025-10-28-------10.13.48.png) 为什麼 AI Agent 无法企業落地？看泰山的挑水工就懂了 今天刷到一張照片，泰山樓梯上，一個白髮蒼蒼的挑水工用扁擔挑著水，一步步往上爬。除了心疼他的辛苦，還看到評論區飄出一條大橫幅 人口紅利正在減弱，以後替代的就是無人機紅利 這簡直一句話點燃了整個思維導火索。是呀、對呀、完全講得通啊 泰山挑水 = 無人機的完美技術應用場景 老齡化 + 無人接班 = 業務痛點 對的技術選型，有痛點，啟動專案的先決條件全部吻合。所以呢，立刻啟動項目、尋找無人機規格、選廠商、進行試點……邏輯完全沒毛病。 真的是這樣嗎？ 回覆區有人發了一句話，說得讓數位轉型顧問們恨不得摀臉——根本用不著什麼無人機黑科技，早就有個老東西完美解決這個場景：纜車。便宜、穩定、用了一百年了。 這就像我們在轉型會議室天天上演的劇碼：某個 AI 顧問拎著最新的 AI 大殺器進場，PPT 講得飛起，結論是「降本增效不能再好」。最後甲方的老 IT歪著頭問了一句——「等等，這事兒用批次自動化不就完了？」一句話， By Wisely Chen 29 Oct 2025 ](/shu-wei-zhuan/) [ ![超慢跑也能 Coding：Claude Code 帶來的真正生產力](/content/images/size/w600/2025/10/-------2025-10-26-------6.58.28-1-1.png) 超慢跑也能 Coding：Claude Code 帶來的真正生產力 大家都說 AI可以增加生產力，那到底啥是真正的生產力？ 今早台北下大雨，我在家陽台跑了一小時的超慢跑，上面的圖是我的環境。這一小時裡，我同時做了四件事： 1\. 運動 : 超慢跑 2\. 知識擷取: 聽Youtube Video (AI Topic) 3\. Vibe Coding / 數據分析 : Claude Code 4\. 網頁搜尋資訊: ChatGPT Altas 這個工作流之所以可行 ，因為「超慢跑 」+ 「Claude Code」 這個組合根本就是天作之合，超慢跑並非慢跑很安全，不需要太多注意力。 Claude Code 老實說真的在做事的時候，95% 的時間不需要去顧，但是總是有 5% 的需要出來 debug 一下，這時候超慢跑停下來一兩分鐘也沒差。 我這樣的 routine 已經持續了3個月之久了，如果是出太陽的時候， By Wisely Chen 28 Oct 2025 ](/vibe-duo-ai-ru-he-zeng-jia-wo-de-sheng-chan-li/)