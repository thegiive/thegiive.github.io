---
layout: post
title: "[ATPM] 來看看矽谷公司怎麼用 AI 來把關 Vibe Coding 的成果"
date: 2025-10-12 22:15:32 +0000
permalink: /atpm-lai-kan-kan-xi-gu-gong-si-zen-mo-yong-ai-lai-ba-guan-vibe-coding-de-cheng-guo/
image: /assets/images/Generated-Image-October-13--2025---5_33AM.png
description: "現在有了 AI ，Coding 的東西可以又快又完整，但是我們怎麼知道 AI 做的Code 裡面會不會有更多的地雷(多收費，寫出有資安議題, 實現很糟糕) 呢？..."
---

# [ATPM] 來看看矽谷公司怎麼用 AI 來把關 Vibe Coding 的成果

[ ![Wisely Chen](/content/images/size/w160/2025/09/6672228-F20250919----02-----------SN------10945w-1.jpg) ](/author/wisely/)

#### [Wisely Chen](/author/wisely/)

13 Oct 2025 — 6 min read

![\[ATPM\] 來看看矽谷公司怎麼用 AI 來把關 Vibe Coding 的成果](/content/images/size/w1200/2025/10/Generated-Image-October-13--2025---5_33AM.png)

現在有了 AI ，Coding 的東西可以又快又完整，但是我們怎麼知道 AI 做的Code 裡面會不會有更多的地雷(多收費，寫出有資安議題, 實現很糟糕) 呢？

### 矽谷怎麼搞

來看看矽谷公司現在怎麼搞的？看看 [Reddit 這一篇](https://www.reddit.com/r/vibecoding/comments/1nnl19h/how_a_senior_engineer_at_a_140m_startup_actually/?ref=ai-coding.wiselychen.com)

![](/assets/images/image-18.png)

這是一個 最近剛 raise 140M 的 startup 裡面 Sr 工程師在reddit 上發表他的做法

  1. 一開始他跟 Claude Code 去討論規格，確定沒有太多問題就叫 AI 寫 Code 了，重點是一開始不要糾結規格完美程度，70% 差不多就做了。
  2. Coding 中間一個重點， cleanup Code ，他會realtime 切到 Cursor 去看 AI 怎麼 Coding ，因為 UI 介面他比較好清晰知道那裡新增了啥 ，而且他不喜歡全部產生 code difference 再看，他喜歡一開始就去 catch AI 的幻覺，避免問題
  3. 再來就是請 AI Code Review ，他說用 AI 做 Code Review 跟人一起 Code Review 雖然看起來重複，其實**「AI 可以幫忙 catch 不同的的 issue」** ，他們最後用的是 coderabbit ，一開始 commit 前先 local 快速 check ，等到 PR 時候，再用一個 github app 來做 detail analysis 
  4. Testing pipeline 完全是由人來控制的，所有的東西都會在 staging 環境做詳細的自動化/人工測試， AI 在裡面會幫忙寫 automation test script ，但是 deploy 與否的決策主導權完全在人

![](/assets/images/image-20.png)

###   
人跟機器做 Code Review 的差別

裡面提到人跟機器 「Code Review 看的東西不太一樣」，我非常的有同感。

一般來說，AI做 Code Review ，在檢查 Code Syntax check , 快速發現常見問題(SQL Injection, XSS, Memory Leak ...etc），以及Best Practice / Anti pattern 。非常的有效率。

另外就是 AI 在知識的廣度遠超人類，就算是工程師，也很難全知全能，就算都是你這個領域，很多 code 的 lib 你也不一定 update-to-date 。這時候 AI 是一個很好的補齊。

人類看的東西，第一個是判斷「過度工程」vs「適度抽象」的平衡，第二個是理解技術債的緣由，知道能判斷「為什麼要這樣寫」，而不只是「寫了什麼」。很多時候，這些 code 看起來很爛，是因為你不理解團隊的在當時的業務限制，技術架構決策的前因後果。

舉一個技術債例子，我在艾立做數位回單時。ETL 一開始用很多 App Script ，中間慢慢改成 make.com + Cloud Run ，後來漸漸變成 GCP Cloud Scheduler + Cloud Run 。  
\- 為何一開始 App Script 打到底，因為我工讀生們那時候剛是剛來工讀生，啥都不懂，一開始導入太多東西會搞死人  
\- make.com : 後來工讀生有些人已經穩定下來幾個月，已經有基本知識了，可以導入第二個 SaaS 套件，才慢慢走向 make.com   
\- 最後怎麼又把 make.com 拋棄掉，因為跟 make.com 談便宜年約談不太下來，加上集團要整合資源砍掉一些 SaaS ，所以就整合進去 GCP   
。  
看看每個技術選型都有很多 context 需要 align , AI 很難完全 align tech lead 的決策

![](/assets/images/Generated-Image-October-13--2025---6_31AM-1.png)

再來就是對業務的理解通常比 AI 好，但是很多時候其實不一定為真 XD ，還是要寫好 PRD Spec ，讓 AI 跟 人都 on the same page 才比較好。

最後一個是 AI 通常對雨後春筍般的 雲服務/SaaS 不是完全理解，所以很多時候在最重要雲服務/SaaS 的 Cost 成本優化上很難做到人的程度，不過這個議題本來人來做也很難的。

### 我的 Comment 

整體來說，雖然這篇不是在講方法論的，但是卻講的很清楚。該有的卡點都有 ，而且是人類跟 AI 穿插做審核。整個觀念很棒 , 而且很 practical 

Code Review 前期，強調產生 Code 的過程當下就用UI做「人力的即時檢核」，不能夠一次做一大包 code review 。這裡感覺跟工程師屆的 Ship Small , Ship fast 很像。

AI Code Review 的部分很有趣，用 [CodeRabbit ](https://www.coderabbit.ai/?ref=ai-coding.wiselychen.com)來做，我用的大多數是之前時代的 code review 工具，主要針對一些 security，還有 syntax check，我還真的沒用過新時代的 AI Code Review SaaS Service 。看來要看看一下了，但是我的問題是我感覺 Claude Code / Codex 應該很容易做到類似的功能，這個 SaaS 網站的差異化在哪呢？

![](/assets/images/image-21.png)

最後 QA 的決策環節，還是人力為主，你要對自己的 Code 負責而不是丟給 AI 。

整個觀念很棒 , 而且很 practical 。應該是真的實戰派出來寫的。而且不像 SDD 學院派一樣強調太多冗長的環節。

最後，他說這套流程大概加速的 40% 的時間，怎麼跟我的 [ATPM 最後測出來的感覺一模一樣](https://ai-coding.wiselychen.com/atpm-a-real-production-vibe-coding-process/)....XD

![](/assets/images/image-19-1.png)

明天跟團隊討論這個流程一下看了那麼多 SDD , ATPM 終於可以升級了趕快來線上實測新流程

[ ![\[Agent模式 Part 2 \] 臨機應變 vs 讀著路書跑 — 為什麼 AI Agent 需要 Plan & Exec 模式](/content/images/size/w600/2025/11/ChatGPT-Image-2025---11---1----------11_27_12.png) [Agent模式 Part 2 ] 臨機應變 vs 讀著路書跑 — 為什麼 AI Agent 需要 Plan & Exec 模式 WRC 賽車最經典的場面就是除了賽車手開著市售車款飛天遁地以外，最有趣的就是旁邊坐著一個副駕，讀著一本稱為「路書」的路線圖，用一些簡略的話去指引賽車手前進。 這個設計在追求速度的賽車界很有趣，因為坐一個副駕更重呀，為何需要把複雜的任務分成兩個角色——規劃者和執行者? 原因很簡單，WRC的賽道都是非常複雜，路況多變的越野賽到，他們經驗發現「規劃者搞清楚計劃，執行者全力執行然後隨機應變最有效率」 回到 AI Agenrt ，你有沒有想過當一個 AI 被指派一個複雜任務，它的腦子裡是怎麼想的？ 上一篇我們比較 AI Workflow 跟經典的 ReAct Agent， 我們看到 ReAct Agent 最後解決了客戶問題。但你有沒有想過，在 ReAct Agent 的彈性的優點下有沒有哪個致命的問題。今天來介紹一下一個新的 Agent 模型，或許是現在大家最常看的 Plan & Exec 模型。 Plan-and-Execute Plan-and-Execute（計畫與執行） By Wisely Chen 01 Nov 2025 ](/mang-mu-jia-su-vs-du-zhu-lu-shu-pao-wei-shi-mo-ai-agent-xu-yao-plan-exec-mo-shi/) [ ![\[Agent 模式 part 1\]  - Workflow 型和 ReAct 型，誰更像你？](/content/images/size/w600/2025/10/ChatGPT-Image-2025---10---30----------10_36_55.png) [Agent 模式 part 1] - Workflow 型和 ReAct 型，誰更像你？ 你有沒有發現，自己工作中也分裂成兩個人，有時按規則做事，有時根據現實應變。其實AI Agent 也一樣。想像一下下面的場景 客戶問：「我想查詢上個月的訂單」。 Agent A Agent : 連接「訂單歷史資料庫」 ❌ 連線失敗（資料庫正在維護） Agent : 系統回答客戶：「抱歉，我們的系統現在無法查詢。請稍後再試。」 結果：客戶必須稍後重試，專業一點的 Agent 就是會請人介入談話 Agent B Agent : 連接「訂單歷史資料庫」 ❌ 連線失敗（資料庫正在維護） Agent 觀察：思考：「主資料庫不通。但我的目標是『找到訂單』，不是『從主資料庫查訂單』。 有其他方式嗎？我們有備份系統嗎？」 Agent 行動：查詢「訂單備份硬碟」觀察：✓ 找到訂單 By Wisely Chen 30 Oct 2025 ](/agent-mo-shi-part-1-workflow-xing-he-react-xing-shui-geng-xiang-ni/) [ ![为什麼 AI Agent 无法企業落地？看泰山的挑水工就懂了](/content/images/size/w600/2025/10/-------2025-10-28-------10.13.48.png) 为什麼 AI Agent 无法企業落地？看泰山的挑水工就懂了 今天刷到一張照片，泰山樓梯上，一個白髮蒼蒼的挑水工用扁擔挑著水，一步步往上爬。除了心疼他的辛苦，還看到評論區飄出一條大橫幅 人口紅利正在減弱，以後替代的就是無人機紅利 這簡直一句話點燃了整個思維導火索。是呀、對呀、完全講得通啊 泰山挑水 = 無人機的完美技術應用場景 老齡化 + 無人接班 = 業務痛點 對的技術選型，有痛點，啟動專案的先決條件全部吻合。所以呢，立刻啟動項目、尋找無人機規格、選廠商、進行試點……邏輯完全沒毛病。 真的是這樣嗎？ 回覆區有人發了一句話，說得讓數位轉型顧問們恨不得摀臉——根本用不著什麼無人機黑科技，早就有個老東西完美解決這個場景：纜車。便宜、穩定、用了一百年了。 這就像我們在轉型會議室天天上演的劇碼：某個 AI 顧問拎著最新的 AI 大殺器進場，PPT 講得飛起，結論是「降本增效不能再好」。最後甲方的老 IT歪著頭問了一句——「等等，這事兒用批次自動化不就完了？」一句話， By Wisely Chen 29 Oct 2025 ](/shu-wei-zhuan/) [ ![超慢跑也能 Coding：Claude Code 帶來的真正生產力](/content/images/size/w600/2025/10/-------2025-10-26-------6.58.28-1-1.png) 超慢跑也能 Coding：Claude Code 帶來的真正生產力 大家都說 AI可以增加生產力，那到底啥是真正的生產力？ 今早台北下大雨，我在家陽台跑了一小時的超慢跑，上面的圖是我的環境。這一小時裡，我同時做了四件事： 1\. 運動 : 超慢跑 2\. 知識擷取: 聽Youtube Video (AI Topic) 3\. Vibe Coding / 數據分析 : Claude Code 4\. 網頁搜尋資訊: ChatGPT Altas 這個工作流之所以可行 ，因為「超慢跑 」+ 「Claude Code」 這個組合根本就是天作之合，超慢跑並非慢跑很安全，不需要太多注意力。 Claude Code 老實說真的在做事的時候，95% 的時間不需要去顧，但是總是有 5% 的需要出來 debug 一下，這時候超慢跑停下來一兩分鐘也沒差。 我這樣的 routine 已經持續了3個月之久了，如果是出太陽的時候， By Wisely Chen 28 Oct 2025 ](/vibe-duo-ai-ru-he-zeng-jia-wo-de-sheng-chan-li/)