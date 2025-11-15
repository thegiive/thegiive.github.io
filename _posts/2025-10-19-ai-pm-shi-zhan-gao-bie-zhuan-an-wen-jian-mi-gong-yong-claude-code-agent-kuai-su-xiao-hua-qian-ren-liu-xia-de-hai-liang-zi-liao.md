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

[ ![Wisely Chen](/assets/images/6672228-F20250919----02-----------SN------10945w-1.jpg) ](/author/wisely/)

#### [Wisely Chen](/author/wisely/)

19 Oct 2025 — 7 min read

![【AI PM 實戰】告別專案文件迷宮！用 Claude Code Agent 快速消化前任留下的海量資料](/assets/images/Generated-Image-October-19--2025---5_19PM.png)

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

[ ![Multi-Agent 協作模式：當 AI 學會「會診」這件事](/assets/images/ChatGPT-Image-2025---11---15----------04_36_04.png) Multi-Agent 協作模式：當 AI 學會「會診」這件事 我上週回老家看了久違的第四台「緯來日本台」，看一個日本節目「恐怖家庭醫學」，裡面講到一個年長者「最近常常心悸、手抖、睡不好」。因為是心臟的因素，所以患者直接找心臟科檢查後，拿到一疊厚厚的報告——結果心臟科醫生看完報告說：「你的心臟結構完全正常，心電圖也沒問題，可能是壓力太大，回去多休息就好。」患者心想：「可是我真的有心悸啊！難道是我自己想太多？」於是患者找了神經科說可能是自律神經失調，拿了藥物減壓，但症狀完全沒改善。 弄了很久一直兜兜轉轉。最後一個經驗豐富家醫科醫生，告知患者「這可能是甲狀腺的問題，要去看內科」才發現這是甲亢的症狀，調整好藥物很快就好了。很多時候人體很多時候是一個連動的生態系統，有些問題的表象跟真正的Root Cause是兩回事，所以患者很容易找錯醫生弄錯科目。 但如果是在好的健檢中心，做法就完全不一樣了。健康檢查會根據你的全方位給予檢查——最後針對你的完整報告進行討論，這時候甲亢的 Root Cause 很快就會被最後的把關者抓出來 " 問題根本不在心臟，而在甲狀腺 " 。這就是「多人協作的力量」。 AI Agent 的世界也是一樣的道理。 By Wisely Chen 15 Nov 2025 ](/multi-agent-xie-zuo-mo-shi-dang-ai-xue-hui-hui-zhen-zhe-jian-shi/) [ ![那天我在產業園區分享：AI 能不能做起來，其實看人](/assets/images/S__88875042.jpg) 那天我在產業園區分享：AI 能不能做起來，其實看人 今天我在新北產業園區，在我們公司的 AI 轉型的活動 在各位傳統產業的前輩講述我之前在傳統產業做 AI 轉型的經驗 我認為「 AI 要在傳產落地，先解決的永遠不是模型，而是人、流程與文化。」 我把這幾年的實戰經驗濃縮成一套能在傳統產業中真正起作用的框架： 現況分析：先理解現場，再談技術 我們創建了一個以 公司各部門的老前輩 + Intern 為主的種子團隊，深入一線流程、取得高層支持，建立真正的共識。 AI 不是空降，而是跟現場一起改。 快速勝利：小範圍試點，讓大家看到成效 選一個可控的場域，把 AI +種子團隊拉進真實流程。 像我用 AI + RPA + OCR + 快速掃描器 = 一個可持續可落地，並且有效益成果 這樣的「小勝利」，是推動組織願意往下走的關鍵。 全面升級：從工具導入到組織轉型 把建置的種子團隊散步到全公司各個部門 可以用很快的速度去 scale 全面開花 By Wisely Chen 13 Nov 2025 ](/na-tian-wo-zai-chan-ye-yuan-qu-fen-xiang-ai-neng-bu-neng-zuo-qi-lai-qi-shi-kan-ren/) [ ![AI 信任崩塌的真正原因：勞資零和賽局的再現](/assets/images/ChatGPT-Image-2025---11---10----------09_24_03.png) AI 信任崩塌的真正原因：勞資零和賽局的再現 根據《Harvard Business Review》近期發表的〈Workers Don’t Trust AI. Here’s How Companies Can Change That〉，美國基層員工對公司提供的 AI 工具信任度在短短數月內暴跌：對生成式 AI 的信任下降 31%，對自主決策型 AI 更下滑 89%。近半數員工反而更信任非官方AI 工具。另外無獨有偶MIT 的研究《The GenAI Divide: State of AI in Business 2025》更進一步揭示了這種現象，並命名為 Shadow AI：員工在公司外私下使用未授權的 AI 來完成工作。研究指出，約有 By Wisely Chen 10 Nov 2025 ](/ai-xin-ren-beng-ta-de-zhen-zheng-yuan-yin-lao-zi-ling-he-sai-ju-de-zai-xian/) [ ![\[Agent part 3\] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵](/assets/images/ChatGPT-Image-2025---11---8----------08_01_49.png) [Agent part 3] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵 大家都知道我用 AI 來 enable 很多intern 來當作很多正職的事情，當然他們雖然都很年輕跟熱情，但是我管理團隊時發現一個規律： 當我派給幾個 Senior 的同事 ，我通常只需要 weekly 跟他開會，給他幾個任務，一週後檢查一次就好。他可以獨立工作，中間遇到問題會自己判斷、調整，如果有大問題他們會舉手跟我講，不容易走偏。 當我要安排工作給我的 intern ，跟 Senior 最大的不同就是， Junior 我通常會每半天或是每過一天就會跟他聊一下提醒一下可能要注意什么事情。因為他很容易遇到了某些複雜任務時，他就可能在某一步卡住，又沒有舉手，基於錯誤理解繼續做下去，最後整個方向偏了，也浪費了他整天的時間。 這是Sr 跟 Jr 經驗的差別，獨立作戰的能力 AI Agent 也是如此 現在考驗 AI Agent 最大的地方，不是他的智商，主要著重點是它的連續工作穩定性。如果人類需要介入的越少，就代表它可以自主完成工作， By Wisely Chen 08 Nov 2025 ](/agent-part-3-interleaved-thinking-cheng-xian-de-wen-ding-xing-shi-xian-zai-agentluo-di-de-zhong-yao-guan-jian/)