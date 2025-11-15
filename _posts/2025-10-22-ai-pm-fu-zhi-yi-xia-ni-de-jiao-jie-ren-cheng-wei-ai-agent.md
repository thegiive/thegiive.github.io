---
layout: post
title: "[AI PM]  複製一下你的交接人成為AI Agent"
date: 2025-10-22 01:13:09 +0000
permalink: /ai-pm-fu-zhi-yi-xia-ni-de-jiao-jie-ren-cheng-wei-ai-agent/
image: /assets/images/Generated-Image-October-22--2025---5_52AM-1.png
description: "既然跟同事交接很困難，那就直接複製一下你的交接同事成為 Agent 吧.... XD..."
---

[pm](https://ai-coding.wiselychen.com/tag/pm/)

# [AI PM] 複製一下你的交接人成為AI Agent

[ ![Wisely Chen](/content/images/size/w160/2025/09/6672228-F20250919----02-----------SN------10945w-1.jpg) ](/author/wisely/)

#### [Wisely Chen](/author/wisely/)

22 Oct 2025 — 5 min read

![\[AI PM\]  複製一下你的交接人成為AI Agent](/content/images/size/w1200/2025/10/Generated-Image-October-22--2025---5_52AM-1.png)

既然跟同事交接很困難，那就直接複製一下你的交接同事成為 Agent 吧.... XD

這幾天一直在接那位資深同事的專案交接。對接到一半，我坐在電腦前突然愣住：等等，我之前不是已經叫 Claude Code 把這 50+ 個專案的文件都讀過一遍了嗎？那些 insights 都躺在我硬碟裡，距離做成 RAG 知識庫根本就差「最後一哩路」而已。

那還廢話什麼，直接做成 Agent 不就好了？我們公司就是做 AI Agent 的欸，自己不用自家產品實在太不專業了吧 😂

### RAG 建立

我們公司的 Agent ，或是市面上的 Chatbot Agent 大多根據 QA / 向量做 RAG ，但是 Claude Code 用的是 文件系統，所以我在此沒時間微調彼此做法差距，我直接請萬能 Claude Code 來

  1. 分析之前抽取過的 50幾個專案文件的 insight markdown (這個[上一期](https://ai-coding.wiselychen.com/ai-pm-shi-zhan-gao-bie-zhuan-an-wen-jian-mi-gong-yong-claude-code-agent-kuai-su-xiao-hua-qian-ren-liu-xia-de-hai-liang-zi-liao/)做完了）
  2. 請他根據 RAG 的基本形式來做 Excel 等級的表格呈現
  3. 拿我們公司的 QA Excel 模板來 mapping 上面的基本 rag 

![](/assets/images/image-33-1.png)Step 2 

### Step 1

有趣的是，[上一篇](https://ai-coding.wiselychen.com/ai-pm-shi-zhan-gao-bie-zhuan-an-wen-jian-mi-gong-yong-claude-code-agent-kuai-su-xiao-hua-qian-ren-liu-xia-de-hai-liang-zi-liao/)的 Claude Code 去爬專案文件，最後結果不是 RAG ，他是產出一堆文件當作 inisght ，之後我要問 Claude Code問題 ，他會自己自動的基於那些 inisight grep 的關鍵字搜尋（他們稱之為「agentic search」）。

![](/assets/images/image-34-1-1.png)上一步的最終產出結果，有了這些 file 就可以快速回答問題

Claude Code 的設計很有趣，一位 Claude 工程師在 Hacker News 上承認 Claude Code 完全不使用 RAG，而是高/中/低三種層次逐行 grep 你的代碼庫。

  * 靈活的低層： 使用不同 Bash Command 做根據場景做不同指令，一言不合的話就會寫 Python 來搞定複雜邏輯
  * 搜索中層：模型用 Grep/Read/Glob，而不是直接 cat /grep ，減少失败率。
  * 抽象高層 : 用一個用一個 Task / Todo 來包裝中層低層指令，定期進度落地到 local disk 方邊追蹤，這層負責「不讓事情失控」

### Step 2 : Doc 到 RAG 微調

Step 2 提示詞很簡單，但是其實是很難的工程， 因為我們[上一期](https://ai-coding.wiselychen.com/ai-pm-shi-zhan-gao-bie-zhuan-an-wen-jian-mi-gong-yong-claude-code-agent-kuai-su-xiao-hua-qian-ren-liu-xia-de-hai-liang-zi-liao/)的輸出一堆 project insight markdown ，要轉成類似問答的 Question List。這個我沒把握 Claude Code 完全轉換其中含義，所以我就花了一堆時間 back and forward 反覆驗證微調輸出結果。所以我才將 Step 2 跟 Step3 分開。

因為 Step 3 基本很簡單，的就是丟模板給 Claude Code , 進行再一次數據轉換。最終產生一個 RAG Excel File as 專案知識庫! 最後匯入我們公司 Agent 知識庫，這裡已經可以搞定查找文件這些問題了。

裡面牽涉到 RAG 調整的知識，老實說還挺難的，而且跟 Agent 系統設計有關係，調得不好 Agent 很容易失控，​

舉例假設原始技術文件片段

![](/assets/images/image-38.png)

以下為錯誤的 QA 拆分方式

![](/assets/images/image-39.png)

正確的拆分方式為

![](/assets/images/image-40.png)

**關鍵差異：**

  * **語義密度** ：一個 QA 涵蓋完整邏輯鏈，而非碎片化資訊
  * **上下文保留** ：答案包含「為什麼」而非只有「是什麼」
  * **可推理性** ：Agent 可以基於這些 QA 回答衍生問題

這就是為什麼我在 Step 2 反覆調整——每一組 QA 都要確保「拆得夠細但不失完整性」。當然就不展開啦，如果你有調整 RAG 需求歡迎聯繫我 or 我們公司。

Step 3，就不提了，單純的資料轉換而已

### 語意人設建立

當然，只做上面的話超無聊的，Agent 最重要是有人性!!!!!，因為這幾天開了幾場交接會議，就將會議記錄的逐字稿拉出來，然後請 Claude Code 來分析他的用詞方式，最後產生人設。因為牽涉到對方的語氣，這裡就不太適合演示。我請 Claude Code 來分析我的 Blog吧 

![](/assets/images/image-37.png)

嘖嘖，也太中肯了吧 , 看來 Claude Code 情緒價值給滿 😄

### 結果

最後就建了一個同事 A agent ，跟我們團隊一起繼續努力！

![](/assets/images/image-35-1-1.png)

[ ![Multi-Agent 協作模式：當 AI 學會「會診」這件事](/content/images/size/w600/2025/11/ChatGPT-Image-2025---11---15----------04_36_04.png) Multi-Agent 協作模式：當 AI 學會「會診」這件事 我上週回老家看了久違的第四台「緯來日本台」，看一個日本節目「恐怖家庭醫學」，裡面講到一個年長者「最近常常心悸、手抖、睡不好」。因為是心臟的因素，所以患者直接找心臟科檢查後，拿到一疊厚厚的報告——結果心臟科醫生看完報告說：「你的心臟結構完全正常，心電圖也沒問題，可能是壓力太大，回去多休息就好。」患者心想：「可是我真的有心悸啊！難道是我自己想太多？」於是患者找了神經科說可能是自律神經失調，拿了藥物減壓，但症狀完全沒改善。 弄了很久一直兜兜轉轉。最後一個經驗豐富家醫科醫生，告知患者「這可能是甲狀腺的問題，要去看內科」才發現這是甲亢的症狀，調整好藥物很快就好了。很多時候人體很多時候是一個連動的生態系統，有些問題的表象跟真正的Root Cause是兩回事，所以患者很容易找錯醫生弄錯科目。 但如果是在好的健檢中心，做法就完全不一樣了。健康檢查會根據你的全方位給予檢查——最後針對你的完整報告進行討論，這時候甲亢的 Root Cause 很快就會被最後的把關者抓出來 " 問題根本不在心臟，而在甲狀腺 " 。這就是「多人協作的力量」。 AI Agent 的世界也是一樣的道理。 By Wisely Chen 15 Nov 2025 ](/multi-agent-xie-zuo-mo-shi-dang-ai-xue-hui-hui-zhen-zhe-jian-shi/) [ ![那天我在產業園區分享：AI 能不能做起來，其實看人](/content/images/size/w600/2025/11/S__88875042.jpg) 那天我在產業園區分享：AI 能不能做起來，其實看人 今天我在新北產業園區，在我們公司的 AI 轉型的活動 在各位傳統產業的前輩講述我之前在傳統產業做 AI 轉型的經驗 我認為「 AI 要在傳產落地，先解決的永遠不是模型，而是人、流程與文化。」 我把這幾年的實戰經驗濃縮成一套能在傳統產業中真正起作用的框架： 現況分析：先理解現場，再談技術 我們創建了一個以 公司各部門的老前輩 + Intern 為主的種子團隊，深入一線流程、取得高層支持，建立真正的共識。 AI 不是空降，而是跟現場一起改。 快速勝利：小範圍試點，讓大家看到成效 選一個可控的場域，把 AI +種子團隊拉進真實流程。 像我用 AI + RPA + OCR + 快速掃描器 = 一個可持續可落地，並且有效益成果 這樣的「小勝利」，是推動組織願意往下走的關鍵。 全面升級：從工具導入到組織轉型 把建置的種子團隊散步到全公司各個部門 可以用很快的速度去 scale 全面開花 By Wisely Chen 13 Nov 2025 ](/na-tian-wo-zai-chan-ye-yuan-qu-fen-xiang-ai-neng-bu-neng-zuo-qi-lai-qi-shi-kan-ren/) [ ![AI 信任崩塌的真正原因：勞資零和賽局的再現](/content/images/size/w600/2025/11/ChatGPT-Image-2025---11---10----------09_24_03.png) AI 信任崩塌的真正原因：勞資零和賽局的再現 根據《Harvard Business Review》近期發表的〈Workers Don’t Trust AI. Here’s How Companies Can Change That〉，美國基層員工對公司提供的 AI 工具信任度在短短數月內暴跌：對生成式 AI 的信任下降 31%，對自主決策型 AI 更下滑 89%。近半數員工反而更信任非官方AI 工具。另外無獨有偶MIT 的研究《The GenAI Divide: State of AI in Business 2025》更進一步揭示了這種現象，並命名為 Shadow AI：員工在公司外私下使用未授權的 AI 來完成工作。研究指出，約有 By Wisely Chen 10 Nov 2025 ](/ai-xin-ren-beng-ta-de-zhen-zheng-yuan-yin-lao-zi-ling-he-sai-ju-de-zai-xian/) [ ![\[Agent part 3\] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵](/content/images/size/w600/2025/11/ChatGPT-Image-2025---11---8----------08_01_49.png) [Agent part 3] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵 大家都知道我用 AI 來 enable 很多intern 來當作很多正職的事情，當然他們雖然都很年輕跟熱情，但是我管理團隊時發現一個規律： 當我派給幾個 Senior 的同事 ，我通常只需要 weekly 跟他開會，給他幾個任務，一週後檢查一次就好。他可以獨立工作，中間遇到問題會自己判斷、調整，如果有大問題他們會舉手跟我講，不容易走偏。 當我要安排工作給我的 intern ，跟 Senior 最大的不同就是， Junior 我通常會每半天或是每過一天就會跟他聊一下提醒一下可能要注意什么事情。因為他很容易遇到了某些複雜任務時，他就可能在某一步卡住，又沒有舉手，基於錯誤理解繼續做下去，最後整個方向偏了，也浪費了他整天的時間。 這是Sr 跟 Jr 經驗的差別，獨立作戰的能力 AI Agent 也是如此 現在考驗 AI Agent 最大的地方，不是他的智商，主要著重點是它的連續工作穩定性。如果人類需要介入的越少，就代表它可以自主完成工作， By Wisely Chen 08 Nov 2025 ](/agent-part-3-interleaved-thinking-cheng-xian-de-wen-ding-xing-shi-xian-zai-agentluo-di-de-zhong-yao-guan-jian/)