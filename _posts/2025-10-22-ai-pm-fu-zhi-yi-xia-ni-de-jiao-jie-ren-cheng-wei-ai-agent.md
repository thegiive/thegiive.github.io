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

[ ![\[Agent模式 Part 2 \] 臨機應變 vs 讀著路書跑 — 為什麼 AI Agent 需要 Plan & Exec 模式](/content/images/size/w600/2025/11/ChatGPT-Image-2025---11---1----------11_27_12.png) [Agent模式 Part 2 ] 臨機應變 vs 讀著路書跑 — 為什麼 AI Agent 需要 Plan & Exec 模式 WRC 賽車最經典的場面就是除了賽車手開著市售車款飛天遁地以外，最有趣的就是旁邊坐著一個副駕，讀著一本稱為「路書」的路線圖，用一些簡略的話去指引賽車手前進。 這個設計在追求速度的賽車界很有趣，因為坐一個副駕更重呀，為何需要把複雜的任務分成兩個角色——規劃者和執行者? 原因很簡單，WRC的賽道都是非常複雜，路況多變的越野賽到，他們經驗發現「規劃者搞清楚計劃，執行者全力執行然後隨機應變最有效率」 回到 AI Agenrt ，你有沒有想過當一個 AI 被指派一個複雜任務，它的腦子裡是怎麼想的？ 上一篇我們比較 AI Workflow 跟經典的 ReAct Agent， 我們看到 ReAct Agent 最後解決了客戶問題。但你有沒有想過，在 ReAct Agent 的彈性的優點下有沒有哪個致命的問題。今天來介紹一下一個新的 Agent 模型，或許是現在大家最常看的 Plan & Exec 模型。 Plan-and-Execute Plan-and-Execute（計畫與執行） By Wisely Chen 01 Nov 2025 ](/mang-mu-jia-su-vs-du-zhu-lu-shu-pao-wei-shi-mo-ai-agent-xu-yao-plan-exec-mo-shi/) [ ![\[Agent 模式 part 1\]  - Workflow 型和 ReAct 型，誰更像你？](/content/images/size/w600/2025/10/ChatGPT-Image-2025---10---30----------10_36_55.png) [Agent 模式 part 1] - Workflow 型和 ReAct 型，誰更像你？ 你有沒有發現，自己工作中也分裂成兩個人，有時按規則做事，有時根據現實應變。其實AI Agent 也一樣。想像一下下面的場景 客戶問：「我想查詢上個月的訂單」。 Agent A Agent : 連接「訂單歷史資料庫」 ❌ 連線失敗（資料庫正在維護） Agent : 系統回答客戶：「抱歉，我們的系統現在無法查詢。請稍後再試。」 結果：客戶必須稍後重試，專業一點的 Agent 就是會請人介入談話 Agent B Agent : 連接「訂單歷史資料庫」 ❌ 連線失敗（資料庫正在維護） Agent 觀察：思考：「主資料庫不通。但我的目標是『找到訂單』，不是『從主資料庫查訂單』。 有其他方式嗎？我們有備份系統嗎？」 Agent 行動：查詢「訂單備份硬碟」觀察：✓ 找到訂單 By Wisely Chen 30 Oct 2025 ](/agent-mo-shi-part-1-workflow-xing-he-react-xing-shui-geng-xiang-ni/) [ ![为什麼 AI Agent 无法企業落地？看泰山的挑水工就懂了](/content/images/size/w600/2025/10/-------2025-10-28-------10.13.48.png) 为什麼 AI Agent 无法企業落地？看泰山的挑水工就懂了 今天刷到一張照片，泰山樓梯上，一個白髮蒼蒼的挑水工用扁擔挑著水，一步步往上爬。除了心疼他的辛苦，還看到評論區飄出一條大橫幅 人口紅利正在減弱，以後替代的就是無人機紅利 這簡直一句話點燃了整個思維導火索。是呀、對呀、完全講得通啊 泰山挑水 = 無人機的完美技術應用場景 老齡化 + 無人接班 = 業務痛點 對的技術選型，有痛點，啟動專案的先決條件全部吻合。所以呢，立刻啟動項目、尋找無人機規格、選廠商、進行試點……邏輯完全沒毛病。 真的是這樣嗎？ 回覆區有人發了一句話，說得讓數位轉型顧問們恨不得摀臉——根本用不著什麼無人機黑科技，早就有個老東西完美解決這個場景：纜車。便宜、穩定、用了一百年了。 這就像我們在轉型會議室天天上演的劇碼：某個 AI 顧問拎著最新的 AI 大殺器進場，PPT 講得飛起，結論是「降本增效不能再好」。最後甲方的老 IT歪著頭問了一句——「等等，這事兒用批次自動化不就完了？」一句話， By Wisely Chen 29 Oct 2025 ](/shu-wei-zhuan/) [ ![超慢跑也能 Coding：Claude Code 帶來的真正生產力](/content/images/size/w600/2025/10/-------2025-10-26-------6.58.28-1-1.png) 超慢跑也能 Coding：Claude Code 帶來的真正生產力 大家都說 AI可以增加生產力，那到底啥是真正的生產力？ 今早台北下大雨，我在家陽台跑了一小時的超慢跑，上面的圖是我的環境。這一小時裡，我同時做了四件事： 1\. 運動 : 超慢跑 2\. 知識擷取: 聽Youtube Video (AI Topic) 3\. Vibe Coding / 數據分析 : Claude Code 4\. 網頁搜尋資訊: ChatGPT Altas 這個工作流之所以可行 ，因為「超慢跑 」+ 「Claude Code」 這個組合根本就是天作之合，超慢跑並非慢跑很安全，不需要太多注意力。 Claude Code 老實說真的在做事的時候，95% 的時間不需要去顧，但是總是有 5% 的需要出來 debug 一下，這時候超慢跑停下來一兩分鐘也沒差。 我這樣的 routine 已經持續了3個月之久了，如果是出太陽的時候， By Wisely Chen 28 Oct 2025 ](/vibe-duo-ai-ru-he-zeng-jia-wo-de-sheng-chan-li/)