---
layout: post
title: "[Agent 模式 part 1]  - Workflow 型和 ReAct 型，誰更像你？"
date: 2025-10-30 14:41:57 +0000
permalink: /agent-mo-shi-part-1-workflow-xing-he-react-xing-shui-geng-xiang-ni/
image: /assets/images/ChatGPT-Image-2025---10---30----------10_36_55.png
description: "你有沒有發現，自己工作中也分裂成兩個人，有時按規則做事，有時根據現實應變。其實AI Agent 也一樣。想像一下下面的場景..."
---

[agent](https://ai-coding.wiselychen.com/tag/agent/)

# [Agent 模式 part 1] - Workflow 型和 ReAct 型，誰更像你？

[ ![Wisely Chen](/content/images/size/w160/2025/09/6672228-F20250919----02-----------SN------10945w-1.jpg) ](/author/wisely/)

#### [Wisely Chen](/author/wisely/)

30 Oct 2025 — 8 min read

![\[Agent 模式 part 1\]  - Workflow 型和 ReAct 型，誰更像你？](/content/images/size/w1200/2025/10/ChatGPT-Image-2025---10---30----------10_36_55.png)

你有沒有發現，自己工作中也分裂成兩個人，有時按規則做事，有時根據現實應變。其實AI Agent 也一樣。想像一下下面的場景

客戶問：「我想查詢上個月的訂單」。

**Agent A**

Agent : 連接「訂單歷史資料庫」 ❌ 連線失敗（資料庫正在維護）

Agent : 系統回答客戶：「抱歉，我們的系統現在無法查詢。請稍後再試。」

結果：客戶必須稍後重試，專業一點的 Agent 就是會請人介入談話

**Agent B**

Agent : 連接「訂單歷史資料庫」 ❌ 連線失敗（資料庫正在維護）

Agent 觀察：思考：「主資料庫不通。但我的目標是『找到訂單』，不是『從主資料庫查訂單』。 有其他方式嗎？我們有備份系統嗎？」

Agent 行動：查詢「訂單備份硬碟」觀察：✓ 找到訂單

Agent : 系統回答客戶：「由於我們的主資料庫正在維護，我從備份系統為您找到了上個月的訂單： - 9 月 15 日：$299 。如果您需要信息，建議在 2 小時後重新查詢，屆時主系統將恢復。」  
  
結果：解決客戶問題

###  AI Workflow vs AI Agent 

今年大家都在討論 Agent Agent Agent ，但是其實我發現到很多公司說的 Agent 更像是 AI Workflow ，在一個穩定的框架下，有固定流程跟規則

但是我所認知的 Agent ，是能夠滿足三個條件

  1. 知識庫提取能力
  2. 工具調用能力
  3. 一定的容錯或是除錯能力的

因為只要Agent 需要調用外部工具，就會有一萬種理由失敗，這時候除錯能力的高低就會嚴重影響 Agent 的robonest (或是你可以說魯棒性)，像剛剛 Agent B這種根據現實狀況動態調整的，會比較偏向真正的 AI Agent 

Workflow 通常都是會在 make.com or N8N 畫出一個 DAG 流程圖，來做特定的事情。為了解決一些外部系統不可空的意外，這裡 N8N or Make.com 通常會用很多可以做很多 Error Handling 的處理，

![](/assets/images/image-56-1.png)

但是有運營過的都知道，Workflow 就算竭盡所能地窮舉，也會出現很可怕無法維運的 DAG 圖，像是上面那張。我之前在做數位回單，的確用 make.com 為了 Error handling ，也畫出類似密度的 DAG 圖，那時候的經驗是除非作者，其他人根本就無法維運，最後出問題還是得打電話給作者。

另外一個問題，是 Workflow 的假設：「我能預測所有情況，所以我預先規劃好了所有步驟」

> 但是現實世界不是預定好的

我們就算怎麼窮舉，也會遇到完全無法預料的狀況，像是誰會知道前幾天 AWS/Azure 也會大當機.... 邊界情況層出不窮，Workflow 面對每一個新情況都說：「對不起，我沒有預案」

### 可以針對現實狀況除錯的 AI Agent : ReAct 模式

既然我們看到 Agent A : AI Workflow 的問題，那我們怎麼做出 Agent B 可以根據現場狀況除錯的 Agent 呢？這時候就要先來看經典的 ReAct 模式了

ReAct （Reason + Act）讓語言模型在單一循環中交替產生**推理（Thought）** 與**行動（Action）** 。具體而言，代理首先觀察到用戶問題，接著產生一段內部推理內容（如思考下一步該搜尋什麼），然後發出一個行動指令（如執行 Tool 或查詢資料庫）。環境執行該行動並返回**觀察結果（Observation）** 給代理。隨後模型根據新的資訊再進行推理、決定下個行動，以此迭代，直到產生最後答案。

![](/assets/images/image-57-1.png)

ReAct 的設計想法並不難,它就源自於你我日常解決問題的方法。舉個例子:

  * 你寫了一段程式(類似思考了一番)
  * 然後放到編譯器裡執行一下(類似 Action,執行某種動作),
  * 然後得到執行結果(來自現實環境的反饋),
  * 再然後透過觀察(看看執行結果),來決定下一步動作,
  * 是修復細節問題呢?
  * 提交程式碼。

其實就是現實狀況中人處理問題的方式，傳說中的摸著石頭過河，找方向(Reason)->實踐(Action)->收集回饋->實踐(Action)->收集回饋->....->到達目的地。

**優點：** 就是對環境感知極強，魯棒性相比起 workflow 好非常多，很適合知識問答/研究型的 Agent (需要查網路），或是像網路遊戲這種高密度交互IO的 Agent 。

**缺點：** 幾乎每一步思考都需要一個 LLM ，速度慢。基本上每次推理要把之前推理的 context 都放進去，token 容易爆炸。因為出問題後，解決問題的思路會比較無法控制，容易產生幻覺，debug 困難。最大的問題就是摸著石頭過河是沒有明確方向性的，很容易走到局部最優解，而非全局最優解的行動路徑。

相比起來，workflow 的優點也不少，速度快，人易於理解跟掌握，遇到問題好除錯。

> 不管ReAct 問題再多，我認為 ReAct 是 AI Agent 的基本入門

因為「人」最強的其中一個部分就是「不論環境如何變化，人都可以非常彈性的改變方式解決問題」，而無法跟外界環境交互跟除錯的 Agent ，真的只是 workflow 不是 類人的 Agent 。

### 要怎麼解決 ReAct 的問題？有更好的模式嗎？

當然很多人都試著提出很多模式來優化 ReAct 的問題。這個文章系列，接下來會講其他 Agent 模型的優缺點，像是 Plan & Exec ，REWООO，LLM Compiler ，Basic Reflection，LATS (Language Agent Tree Search)。

![](/assets/images/image-58.png)我比較喜歡的 Plan & Exec 

當然太學術的我會略過。不過這些東西基本上大部分就是 ReAct 跟 Workflow concept 的優化跟組合。

### 有更簡單的方式嗎？看看工具怎麼做

另外一個簡單的方式，就是 Claude Code 一樣，Claude Code 加入「人」(兼顧效率跟魯棒性) 在他的模式裡面。 Claude Code 的交互介面一開始就設計成跟人交互，而非完全自主完成。

Claude Code 在小任務上通常可以自我除錯，不需要人來介入。但是在關鍵節點，或是邊際狀況上，他會主動的提示人這裡有問題，要跟人對齊。

![](/assets/images/image-59-1.png)

這裡 Claude Code 就一直在「自主性」和「人類對齊」之間找平衡

### 再回到剛剛的場景

客戶打電話問：「我想查詢上個月的訂單」。

**真人客服 A**

真人客服 A : 連接「訂單歷史資料庫」 ❌ 連線失敗（資料庫正在維護）

真人客服 A: 回答客戶：「抱歉，我們的系統現在無法查詢。請稍後再試。」

**真人客服 B**

真人客服 B: 連接「訂單歷史資料庫」 ❌ 連線失敗（資料庫正在維護）

真人客服 B：思考：「主資料庫不通。但我的目標是『找到訂單』，不是『從主資料庫查訂單』。 有其他方式嗎？我們有備份系統嗎？」

真人客服 B 行動：查詢「訂單備份硬碟」觀察：✓ 找到訂單

真人客服 B 回答客戶：「由於我們的主資料庫正在維護，我從備份系統為您找到了上個月的訂單： - 9 月 15 日：$299 。如果您需要信息，建議在 2 小時後重新查詢，屆時主系統將恢復。」

有沒有感覺也很像日常生活會遇到的場景  

###  Agent 思考模型跟人一樣

  
在我們的日常生活，也很常遇到不同類型的人，有些人是 ReAct ，有些人是 Workflow 類型。ReAct 的人腦袋靈活，但是很多時候不好控制，野路子很多也容易失控。Workflow 類型的人雖然呆板，但是往好的方面想也是「一絲不苟」。

想想 Claude Code 要在「自主性」和「人類對齊」上找平衡

> 我們人也不就是一直在 ReAct 跟 Workflow 上追求一個 tradeoff ？

[ ![\[Agent模式 Part 2 \] 臨機應變 vs 讀著路書跑 — 為什麼 AI Agent 需要 Plan & Exec 模式](/content/images/size/w600/2025/11/ChatGPT-Image-2025---11---1----------11_27_12.png) [Agent模式 Part 2 ] 臨機應變 vs 讀著路書跑 — 為什麼 AI Agent 需要 Plan & Exec 模式 WRC 賽車最經典的場面就是除了賽車手開著市售車款飛天遁地以外，最有趣的就是旁邊坐著一個副駕，讀著一本稱為「路書」的路線圖，用一些簡略的話去指引賽車手前進。 這個設計在追求速度的賽車界很有趣，因為坐一個副駕更重呀，為何需要把複雜的任務分成兩個角色——規劃者和執行者? 原因很簡單，WRC的賽道都是非常複雜，路況多變的越野賽到，他們經驗發現「規劃者搞清楚計劃，執行者全力執行然後隨機應變最有效率」 回到 AI Agenrt ，你有沒有想過當一個 AI 被指派一個複雜任務，它的腦子裡是怎麼想的？ 上一篇我們比較 AI Workflow 跟經典的 ReAct Agent， 我們看到 ReAct Agent 最後解決了客戶問題。但你有沒有想過，在 ReAct Agent 的彈性的優點下有沒有哪個致命的問題。今天來介紹一下一個新的 Agent 模型，或許是現在大家最常看的 Plan & Exec 模型。 Plan-and-Execute Plan-and-Execute（計畫與執行） By Wisely Chen 01 Nov 2025 ](/mang-mu-jia-su-vs-du-zhu-lu-shu-pao-wei-shi-mo-ai-agent-xu-yao-plan-exec-mo-shi/) [ ![为什麼 AI Agent 无法企業落地？看泰山的挑水工就懂了](/content/images/size/w600/2025/10/-------2025-10-28-------10.13.48.png) 为什麼 AI Agent 无法企業落地？看泰山的挑水工就懂了 今天刷到一張照片，泰山樓梯上，一個白髮蒼蒼的挑水工用扁擔挑著水，一步步往上爬。除了心疼他的辛苦，還看到評論區飄出一條大橫幅 人口紅利正在減弱，以後替代的就是無人機紅利 這簡直一句話點燃了整個思維導火索。是呀、對呀、完全講得通啊 泰山挑水 = 無人機的完美技術應用場景 老齡化 + 無人接班 = 業務痛點 對的技術選型，有痛點，啟動專案的先決條件全部吻合。所以呢，立刻啟動項目、尋找無人機規格、選廠商、進行試點……邏輯完全沒毛病。 真的是這樣嗎？ 回覆區有人發了一句話，說得讓數位轉型顧問們恨不得摀臉——根本用不著什麼無人機黑科技，早就有個老東西完美解決這個場景：纜車。便宜、穩定、用了一百年了。 這就像我們在轉型會議室天天上演的劇碼：某個 AI 顧問拎著最新的 AI 大殺器進場，PPT 講得飛起，結論是「降本增效不能再好」。最後甲方的老 IT歪著頭問了一句——「等等，這事兒用批次自動化不就完了？」一句話， By Wisely Chen 29 Oct 2025 ](/shu-wei-zhuan/) [ ![超慢跑也能 Coding：Claude Code 帶來的真正生產力](/content/images/size/w600/2025/10/-------2025-10-26-------6.58.28-1-1.png) 超慢跑也能 Coding：Claude Code 帶來的真正生產力 大家都說 AI可以增加生產力，那到底啥是真正的生產力？ 今早台北下大雨，我在家陽台跑了一小時的超慢跑，上面的圖是我的環境。這一小時裡，我同時做了四件事： 1\. 運動 : 超慢跑 2\. 知識擷取: 聽Youtube Video (AI Topic) 3\. Vibe Coding / 數據分析 : Claude Code 4\. 網頁搜尋資訊: ChatGPT Altas 這個工作流之所以可行 ，因為「超慢跑 」+ 「Claude Code」 這個組合根本就是天作之合，超慢跑並非慢跑很安全，不需要太多注意力。 Claude Code 老實說真的在做事的時候，95% 的時間不需要去顧，但是總是有 5% 的需要出來 debug 一下，這時候超慢跑停下來一兩分鐘也沒差。 我這樣的 routine 已經持續了3個月之久了，如果是出太陽的時候， By Wisely Chen 28 Oct 2025 ](/vibe-duo-ai-ru-he-zeng-jia-wo-de-sheng-chan-li/) [ ![\[AI Ops\] 用 Agent\(Claude Code\) 做 Linux 系統管理有沒有搞頭？香得很！](/content/images/size/w600/2025/10/ChatGPT-Image-2025---10---24----------08_31_52.png) [AI Ops] 用 Agent(Claude Code) 做 Linux 系統管理有沒有搞頭？香得很！ 今天突然發現用 Claude Code 做 Linux 系統管理超香的。不只可以幫你寫 code，還順便幫你考古系統程式，挖出系統裡不為人知的秘密，最棒的是能讓你找到之前同事寫好的 code 提早下班，享受當老闆的樂趣。 話說今天某個客戶系統出問題了，大家忙到炸掉。為了安撫客戶，我就跟客戶說 「我來寫 monitor script 吧」 既然牛都吹了，來都來了，就來寫吧，反正也不是我寫 XD。我對 Claude Code 很有信心，因為 Linux 系統管理本質就是 command line，而 Claude Code 生來就是為 command line 而生，而且很專精！ 目標 我的目標就是在一台 Linux machine 寫 monitor By Wisely Chen 24 Oct 2025 ](/ai-ops-yong-agent-claude-code-zuo-linux-xi-tong-guan-li-you-mei-you-gao-tou-xiang-de-hen/)