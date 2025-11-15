---
layout: post
title: "[VIBE Coding] 我在前端新增需求的 PRD 跟 Prompt 解法"
date: 2025-10-08 00:43:22 +0000
permalink: /vibe-coding-wo-zai-qian-duan-xin-zeng-xu-qiu-de-prd-gen-prompt-jie-fa/
image: /assets/images/Gemini_Generated_Image_6zdw0k6zdw0k6zdw-1.png
description: "上次提到我在前端這邊做AI Coding 很適合 0% -> 70% , 或是 99 -> 100%的做法，但是在 90% -> 100% 遇到了蠻多的小問題，經過幾天的討論修正之後，我已經大概列出了比較適合的方式。根據這一週來改了十幾個 Feature的經驗，這個流程對我這樣非前端的人來說，感覺 90% -> 100% 除了後續檢核需要前端幫忙以外，幾乎都是我可以自己處理。..."
---

[ai-coding](https://ai-coding.wiselychen.com/tag/ai-coding/)

# [VIBE Coding] 我在前端新增需求的 PRD 跟 Prompt 解法

[ ![Wisely Chen](/content/images/size/w160/2025/09/6672228-F20250919----02-----------SN------10945w-1.jpg) ](/author/wisely/)

#### [Wisely Chen](/author/wisely/)

08 Oct 2025 — 4 min read

![\[VIBE Coding\] 我在前端新增需求的 PRD 跟 Prompt 解法](/content/images/size/w1200/2025/10/Gemini_Generated_Image_6zdw0k6zdw0k6zdw-1.png)

上次提到[我在前端這邊做AI Coding](https://ai-coding.wiselychen.com/zui-jin-wo-zai-qian-duan-vibe-coding-yu-dao-de-wen-ti/) 很適合 0% -> 70% , 或是 99 -> 100%的做法，但是在 90% -> 100% 遇到了蠻多的小問題，經過幾天的討論修正之後，我已經大概列出了比較適合的方式。根據這一週來改了十幾個 Feature的經驗，這個流程對我這樣非前端的人來說，感覺 90% -> 100% 除了後續檢核需要前端幫忙以外，幾乎都是我可以自己處理。

這個場景其實還蠻常見的，現在 VIBE Coding 大家都在講從頭新建一個網站，這個東西對工程師來說太低頻了，其實程式設計師大部分的時候都是在新增修改功能某個到在現有的 App 上，所以這個技巧我實際跟前端一起弄四五天後，我個人覺得還蠻好用的。

### 流程圖

![](/assets/images/image-10-1.png)

首先第一個就是把舊設計稿跟U I的截圖請A I幫我做比較，這個部分主要是列出新增或修改的UI介面在哪邊，這個時候出來的東西可能是一個free format，但不要緊。舉例，我截圖一個 Google Doc 畫面，我故意把中間的 提示 icon 修掉 , 當作做 feature 之前的 V1.0 ，然後再把原始圖變成 V1.1 

![](/assets/images/-------2025-10-08-------7.57.40-------1.png)範例：我故意把中間的 提示 icon 修掉 , 當作做 feature 之前的 V1.0 ![](/assets/images/-------2025-10-08-------7.57.40-1.png)範例：原始畫面當作做做完 feature 之前的 V1.1 

接下來下一步，我們請A I幫我產生有剛剛的修改的或是新增的需求列表表，這個時候就是一個比較粗的P R D。這裡我其實都會預設使用 Gemini ，因為我體感 Gemini OCR 蠻強的，UI 抓中文字比較簡單

![](/assets/images/image-11.png)Gemini OCR 

然後我們請他變成一些 feature list ，一個一個 功能變化都寫成簡易的 feature list ，此處我還是不規範 PRD ，隨意產生即可。下面的範例是我這幾天 onProd 某個功能 masking 過的寫法，保證真實，不像外面開課程都是一堆 demo code XD

![](/assets/images/data-src-image-6d5fe5e6-67de-46b4-bd1f-2fa4ee08e5b5.png)相關功能文件 - 簡略的 feature list 

下一步我們準備好的P R D 的Temple，以及相關的 supporting Tech PRD 資料(API文件 或是相關的程式碼的規範文件) ，就會產生一個完整的P R D。以下也是那功能最後產生的 詳細 PRD 

![](/assets/images/data-src-image-a3b4ee0e-4b31-405a-868e-d57931f5710f-1.png) 有 需求列表 , tech requirement , 還有 supporting data 的

有這個完整的P R D之後，我們就可以請AI幫我們做Coding，我之前經驗幾乎一次過。產生 code 的 Prompt 超級簡單的，因為 PRD 都已經寫好了。

![](/assets/images/data-src-image-fa64d1f5-e960-433b-b391-b34c23398453-1.png)![](/assets/images/data-src-image-473c3d0b-dafc-4184-bea1-7d11d78f9530-1.png)

最後給 RD 檢核， 送交 QA 。

### 結果

根據這一週來改了十幾個 Feature的經驗，這個流程對我這樣非前端的人來說，感覺 90% -> 100% 除了後續檢核需要前端幫忙以外，幾乎都是我可以自己處理。

### 附件A: PRD Template 

## This post is for subscribers only

Subscribe now

Already have an account? Sign in

[ ![\[Agent模式 Part 2 \] 臨機應變 vs 讀著路書跑 — 為什麼 AI Agent 需要 Plan & Exec 模式](/content/images/size/w600/2025/11/ChatGPT-Image-2025---11---1----------11_27_12.png) [Agent模式 Part 2 ] 臨機應變 vs 讀著路書跑 — 為什麼 AI Agent 需要 Plan & Exec 模式 WRC 賽車最經典的場面就是除了賽車手開著市售車款飛天遁地以外，最有趣的就是旁邊坐著一個副駕，讀著一本稱為「路書」的路線圖，用一些簡略的話去指引賽車手前進。 這個設計在追求速度的賽車界很有趣，因為坐一個副駕更重呀，為何需要把複雜的任務分成兩個角色——規劃者和執行者? 原因很簡單，WRC的賽道都是非常複雜，路況多變的越野賽到，他們經驗發現「規劃者搞清楚計劃，執行者全力執行然後隨機應變最有效率」 回到 AI Agenrt ，你有沒有想過當一個 AI 被指派一個複雜任務，它的腦子裡是怎麼想的？ 上一篇我們比較 AI Workflow 跟經典的 ReAct Agent， 我們看到 ReAct Agent 最後解決了客戶問題。但你有沒有想過，在 ReAct Agent 的彈性的優點下有沒有哪個致命的問題。今天來介紹一下一個新的 Agent 模型，或許是現在大家最常看的 Plan & Exec 模型。 Plan-and-Execute Plan-and-Execute（計畫與執行） By Wisely Chen 01 Nov 2025 ](/mang-mu-jia-su-vs-du-zhu-lu-shu-pao-wei-shi-mo-ai-agent-xu-yao-plan-exec-mo-shi/) [ ![\[Agent 模式 part 1\]  - Workflow 型和 ReAct 型，誰更像你？](/content/images/size/w600/2025/10/ChatGPT-Image-2025---10---30----------10_36_55.png) [Agent 模式 part 1] - Workflow 型和 ReAct 型，誰更像你？ 你有沒有發現，自己工作中也分裂成兩個人，有時按規則做事，有時根據現實應變。其實AI Agent 也一樣。想像一下下面的場景 客戶問：「我想查詢上個月的訂單」。 Agent A Agent : 連接「訂單歷史資料庫」 ❌ 連線失敗（資料庫正在維護） Agent : 系統回答客戶：「抱歉，我們的系統現在無法查詢。請稍後再試。」 結果：客戶必須稍後重試，專業一點的 Agent 就是會請人介入談話 Agent B Agent : 連接「訂單歷史資料庫」 ❌ 連線失敗（資料庫正在維護） Agent 觀察：思考：「主資料庫不通。但我的目標是『找到訂單』，不是『從主資料庫查訂單』。 有其他方式嗎？我們有備份系統嗎？」 Agent 行動：查詢「訂單備份硬碟」觀察：✓ 找到訂單 By Wisely Chen 30 Oct 2025 ](/agent-mo-shi-part-1-workflow-xing-he-react-xing-shui-geng-xiang-ni/) [ ![为什麼 AI Agent 无法企業落地？看泰山的挑水工就懂了](/content/images/size/w600/2025/10/-------2025-10-28-------10.13.48.png) 为什麼 AI Agent 无法企業落地？看泰山的挑水工就懂了 今天刷到一張照片，泰山樓梯上，一個白髮蒼蒼的挑水工用扁擔挑著水，一步步往上爬。除了心疼他的辛苦，還看到評論區飄出一條大橫幅 人口紅利正在減弱，以後替代的就是無人機紅利 這簡直一句話點燃了整個思維導火索。是呀、對呀、完全講得通啊 泰山挑水 = 無人機的完美技術應用場景 老齡化 + 無人接班 = 業務痛點 對的技術選型，有痛點，啟動專案的先決條件全部吻合。所以呢，立刻啟動項目、尋找無人機規格、選廠商、進行試點……邏輯完全沒毛病。 真的是這樣嗎？ 回覆區有人發了一句話，說得讓數位轉型顧問們恨不得摀臉——根本用不著什麼無人機黑科技，早就有個老東西完美解決這個場景：纜車。便宜、穩定、用了一百年了。 這就像我們在轉型會議室天天上演的劇碼：某個 AI 顧問拎著最新的 AI 大殺器進場，PPT 講得飛起，結論是「降本增效不能再好」。最後甲方的老 IT歪著頭問了一句——「等等，這事兒用批次自動化不就完了？」一句話， By Wisely Chen 29 Oct 2025 ](/shu-wei-zhuan/) [ ![超慢跑也能 Coding：Claude Code 帶來的真正生產力](/content/images/size/w600/2025/10/-------2025-10-26-------6.58.28-1-1.png) 超慢跑也能 Coding：Claude Code 帶來的真正生產力 大家都說 AI可以增加生產力，那到底啥是真正的生產力？ 今早台北下大雨，我在家陽台跑了一小時的超慢跑，上面的圖是我的環境。這一小時裡，我同時做了四件事： 1\. 運動 : 超慢跑 2\. 知識擷取: 聽Youtube Video (AI Topic) 3\. Vibe Coding / 數據分析 : Claude Code 4\. 網頁搜尋資訊: ChatGPT Altas 這個工作流之所以可行 ，因為「超慢跑 」+ 「Claude Code」 這個組合根本就是天作之合，超慢跑並非慢跑很安全，不需要太多注意力。 Claude Code 老實說真的在做事的時候，95% 的時間不需要去顧，但是總是有 5% 的需要出來 debug 一下，這時候超慢跑停下來一兩分鐘也沒差。 我這樣的 routine 已經持續了3個月之久了，如果是出太陽的時候， By Wisely Chen 28 Oct 2025 ](/vibe-duo-ai-ru-he-zeng-jia-wo-de-sheng-chan-li/)