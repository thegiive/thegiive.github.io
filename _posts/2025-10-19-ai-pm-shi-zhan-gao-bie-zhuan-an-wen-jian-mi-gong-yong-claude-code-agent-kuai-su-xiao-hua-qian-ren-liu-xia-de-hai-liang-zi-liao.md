---
layout: post
title: "【AI PM 實戰】告別專案文件迷宮！用 Claude Code Agent 快速消化前任留下的海量資料"
date: 2025-10-19 10:01:44 +0000
permalink: /ai-pm-shi-zhan-gao-bie-zhuan-an-wen-jian-mi-gong-yong-claude-code-agent-kuai-su-xiao-hua-qian-ren-liu-xia-de-hai-liang-zi-liao/
image: /assets/images/Generated-Image-October-19--2025---5_19PM.png
description: "身為 PM，你是不是也遇過這種狀況：你得在極短時間內看完前任PM所有東西？ 這時候除了認命加班看文章，有沒有更好的方式？試試看 AI Agent 吧..."
---




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
