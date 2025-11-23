---
layout: post
title: "[AI PM]  複製一下你的交接人成為AI Agent"
date: 2025-10-22 01:13:09 +0000
permalink: /ai-pm-fu-zhi-yi-xia-ni-de-jiao-jie-ren-cheng-wei-ai-agent/
image: /assets/images/Generated-Image-October-22--2025---5_52AM-1.png
description: "既然跟同事交接很困難，那就直接複製一下你的交接同事成為 Agent 吧.... XD..."
---



# [AI PM] 複製一下你的交接人成為AI Agent





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
