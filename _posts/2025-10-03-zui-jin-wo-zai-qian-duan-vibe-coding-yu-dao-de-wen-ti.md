---
layout: post
title: "最近我在前端 Vibe Coding 遇到的問題"
date: 2025-10-03 15:13:06 +0000
permalink: /zui-jin-wo-zai-qian-duan-vibe-coding-yu-dao-de-wen-ti/
image: /assets/images/Generated-Image-October-03--2025---10_51PM.png
description: "我這幾天因為一個重要的案子，決定也來 VIBE Coding 一下，寫寫frontend feature（我從來沒寫過 frontend Vue 的程式）..."
---

[ai-coding](https://ai-coding.wiselychen.com/tag/ai-coding/)

# 最近我在前端 Vibe Coding 遇到的問題

[ ![Wisely Chen](/content/images/size/w160/2025/09/6672228-F20250919----02-----------SN------10945w-1.jpg) ](/author/wisely/)

#### [Wisely Chen](/author/wisely/)

03 Oct 2025 — 3 min read

![最近我在前端 Vibe Coding 遇到的問題](/content/images/size/w1200/2025/10/Generated-Image-October-03--2025---10_51PM.png)

我這幾天因為一個重要的案子，決定也來 VIBE Coding 一下，寫寫frontend feature（我從來沒寫過 frontend Vue 的程式）

我發現到 vibe coding 在「現有網站加ui 功能」似乎遇到巨大的問題。我的場景是有

> 「現有的上線網站，為了加入幾個功能頁，設計師弄了幾頁設計圖，要改上去」

修改規模大概就是100個頁面加入10頁，這種 10% 規模。不是改bug , 但也不是重寫

當我將 Claude code 去讀 Figma設計圖，然後加feature 。居然連 Claude 4.5 Sonnet 都顯得左支右著 , 非常狼狽。

![](/assets/images/Generated-Image-October-03--2025---10_57PM-1.png)

要嘛就是

  1. 頁面改太少，不能根據設計圖復刻
  2. 或是加入UI feature 成功,但是大規模波及到現有ui 
  3. 也可能是 Ui 成功創立，但是api 改壞

這個經驗大家熟知的vibe coding 可以快速兜出一個美觀的 ui，可能有巨大的認知差距

我估計vibe coding 適合

  1. 0-> 100 : 沒有草稿，直接從idea 讓AI 自由發揮的 POC 網站，或是 startup 第一版，沒有前人的包袱
  2. 99% -> 100% : 現有網站，直接改bug 這種 1%的工作

但是今天這種大概 10%修改，好像要了AI 的命。要嘛改不動，要嘛改太多，變成refactor 。這種情況，我當然碰過。我在做[ATPM](https://ai-coding.wiselychen.com/atpm-a-real-production-vibe-coding-process/) 時，在這種情景，撰寫明確的PRD 細節，規格。通常可以解決這個問題。但是一個 已經運行線上的現有網站，哪有可能寫舊有「完整」的 PRD 規格書 , 別騙人了 XD 

![](/assets/images/image.png)

在我今天的情況，我有的就是「新增規格書」，而且還是接近FIGMA 的圖形規格書。我有試過 Claude Code ，請 AI 根據現有網站弄出 PRD , 但是現行 UI 幾乎都是 VUE or React 框架元件，加一堆商用UI lib render 出來的頁面。AI Coding 都是看 Code ，也很難AI 自己腦中render 出來原本長哪樣。然後新規格書又是圖片 ，如果我們要比差距，似乎一定要就有UI render 出來才能比對。

我在猜如果Claude code 操作browser mcp ，去截圖舊網站，然後再請 AI Vision 比較新規格書的圖片，應該比現在ai 看code更有奇效。這個場景 , 就好像很難發揮ai coding 。仔細想想，這種場景跟改bug一樣才是真高頻場景 , 誰會每天寫 POC 呀XD

當然這一切都是我自己前端經驗不夠，別忘了我本週二才開始人生中第一次碰 frontend coding。也算是另外一種 Vibe Coder。

不過今天下午試出一些作法，終於比較好改動了，連假晚點分享

[ ![\[Agent模式 Part 2 \] 臨機應變 vs 讀著路書跑 — 為什麼 AI Agent 需要 Plan & Exec 模式](/content/images/size/w600/2025/11/ChatGPT-Image-2025---11---1----------11_27_12.png) [Agent模式 Part 2 ] 臨機應變 vs 讀著路書跑 — 為什麼 AI Agent 需要 Plan & Exec 模式 WRC 賽車最經典的場面就是除了賽車手開著市售車款飛天遁地以外，最有趣的就是旁邊坐著一個副駕，讀著一本稱為「路書」的路線圖，用一些簡略的話去指引賽車手前進。 這個設計在追求速度的賽車界很有趣，因為坐一個副駕更重呀，為何需要把複雜的任務分成兩個角色——規劃者和執行者? 原因很簡單，WRC的賽道都是非常複雜，路況多變的越野賽到，他們經驗發現「規劃者搞清楚計劃，執行者全力執行然後隨機應變最有效率」 回到 AI Agenrt ，你有沒有想過當一個 AI 被指派一個複雜任務，它的腦子裡是怎麼想的？ 上一篇我們比較 AI Workflow 跟經典的 ReAct Agent， 我們看到 ReAct Agent 最後解決了客戶問題。但你有沒有想過，在 ReAct Agent 的彈性的優點下有沒有哪個致命的問題。今天來介紹一下一個新的 Agent 模型，或許是現在大家最常看的 Plan & Exec 模型。 Plan-and-Execute Plan-and-Execute（計畫與執行） By Wisely Chen 01 Nov 2025 ](/mang-mu-jia-su-vs-du-zhu-lu-shu-pao-wei-shi-mo-ai-agent-xu-yao-plan-exec-mo-shi/) [ ![\[Agent 模式 part 1\]  - Workflow 型和 ReAct 型，誰更像你？](/content/images/size/w600/2025/10/ChatGPT-Image-2025---10---30----------10_36_55.png) [Agent 模式 part 1] - Workflow 型和 ReAct 型，誰更像你？ 你有沒有發現，自己工作中也分裂成兩個人，有時按規則做事，有時根據現實應變。其實AI Agent 也一樣。想像一下下面的場景 客戶問：「我想查詢上個月的訂單」。 Agent A Agent : 連接「訂單歷史資料庫」 ❌ 連線失敗（資料庫正在維護） Agent : 系統回答客戶：「抱歉，我們的系統現在無法查詢。請稍後再試。」 結果：客戶必須稍後重試，專業一點的 Agent 就是會請人介入談話 Agent B Agent : 連接「訂單歷史資料庫」 ❌ 連線失敗（資料庫正在維護） Agent 觀察：思考：「主資料庫不通。但我的目標是『找到訂單』，不是『從主資料庫查訂單』。 有其他方式嗎？我們有備份系統嗎？」 Agent 行動：查詢「訂單備份硬碟」觀察：✓ 找到訂單 By Wisely Chen 30 Oct 2025 ](/agent-mo-shi-part-1-workflow-xing-he-react-xing-shui-geng-xiang-ni/) [ ![为什麼 AI Agent 无法企業落地？看泰山的挑水工就懂了](/content/images/size/w600/2025/10/-------2025-10-28-------10.13.48.png) 为什麼 AI Agent 无法企業落地？看泰山的挑水工就懂了 今天刷到一張照片，泰山樓梯上，一個白髮蒼蒼的挑水工用扁擔挑著水，一步步往上爬。除了心疼他的辛苦，還看到評論區飄出一條大橫幅 人口紅利正在減弱，以後替代的就是無人機紅利 這簡直一句話點燃了整個思維導火索。是呀、對呀、完全講得通啊 泰山挑水 = 無人機的完美技術應用場景 老齡化 + 無人接班 = 業務痛點 對的技術選型，有痛點，啟動專案的先決條件全部吻合。所以呢，立刻啟動項目、尋找無人機規格、選廠商、進行試點……邏輯完全沒毛病。 真的是這樣嗎？ 回覆區有人發了一句話，說得讓數位轉型顧問們恨不得摀臉——根本用不著什麼無人機黑科技，早就有個老東西完美解決這個場景：纜車。便宜、穩定、用了一百年了。 這就像我們在轉型會議室天天上演的劇碼：某個 AI 顧問拎著最新的 AI 大殺器進場，PPT 講得飛起，結論是「降本增效不能再好」。最後甲方的老 IT歪著頭問了一句——「等等，這事兒用批次自動化不就完了？」一句話， By Wisely Chen 29 Oct 2025 ](/shu-wei-zhuan/) [ ![超慢跑也能 Coding：Claude Code 帶來的真正生產力](/content/images/size/w600/2025/10/-------2025-10-26-------6.58.28-1-1.png) 超慢跑也能 Coding：Claude Code 帶來的真正生產力 大家都說 AI可以增加生產力，那到底啥是真正的生產力？ 今早台北下大雨，我在家陽台跑了一小時的超慢跑，上面的圖是我的環境。這一小時裡，我同時做了四件事： 1\. 運動 : 超慢跑 2\. 知識擷取: 聽Youtube Video (AI Topic) 3\. Vibe Coding / 數據分析 : Claude Code 4\. 網頁搜尋資訊: ChatGPT Altas 這個工作流之所以可行 ，因為「超慢跑 」+ 「Claude Code」 這個組合根本就是天作之合，超慢跑並非慢跑很安全，不需要太多注意力。 Claude Code 老實說真的在做事的時候，95% 的時間不需要去顧，但是總是有 5% 的需要出來 debug 一下，這時候超慢跑停下來一兩分鐘也沒差。 我這樣的 routine 已經持續了3個月之久了，如果是出太陽的時候， By Wisely Chen 28 Oct 2025 ](/vibe-duo-ai-ru-he-zeng-jia-wo-de-sheng-chan-li/)