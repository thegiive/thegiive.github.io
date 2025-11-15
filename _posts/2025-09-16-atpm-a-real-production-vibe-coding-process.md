---
layout: post
title: "ATPM : A real production Vibe Coding process"
date: 2025-09-16 21:41:01 +0000
permalink: /atpm-a-real-production-vibe-coding-process/
image: /assets/images/-------2025-09-17-------4.31.54-1.png
description: "章節..."
---

# ATPM : A real production Vibe Coding process

[ ![Wisely Chen](/content/images/size/w160/2025/09/6672228-F20250919----02-----------SN------10945w-1.jpg) ](/author/wisely/)

#### [Wisely Chen](/author/wisely/)

17 Sep 2025 — 8 min read

![ATPM : A real production Vibe Coding process](/content/images/size/w1200/2025/09/-------2025-09-17-------4.31.54-1.png)

章節

  1. [ATPM 介紹](https://ai-coding.wiselychen.com/atpm-a-real-production-vibe-coding-process/)
  2. [PRD 的重要性](https://ai-coding.wiselychen.com/atpm-prdde-zhong-yao-xing/)
  3. [AI 時代, 對PM的加速](https://ai-coding.wiselychen.com/atpm-ai-dui-pm-de-jia-su/)
  4. [Dev 的演進](https://ai-coding.wiselychen.com/atpm-kai-fa-zhe-dev-de-shui-bian-cong-gong-du-sheng-ma-nong-dao-ai-zhi-hui-jia/)
  5. [QA](https://ai-coding.wiselychen.com/atpm-qa-ru-he-yan-shou-ai-coding-de-cheng-shi/)
  6. Supervisor 撰寫中
  7. 結語撰寫中

## 前言

在AI技術蓬勃發展的今天，我們的軟體開發世界正經歷著一場前所未有的「中年危機」。Vibe Coding 橫空問世的當下，我這種老屁股工程師一邊害怕被淘汰的同時，一邊又看著 AI Coding 又被很多人吐槽無法真正拿來做真正的工作。

很幸運的是，我們團隊在六月開發一套新流程 ATPM : Assessment , Testing , Program , Management ，並且用這套流程開發一套帳務系統並且成功上線。在這個過程中，我們幾乎把所有 Vibe Coding 所有遇到的問題

  1. 幻覺
  2. 亂講話
  3. 測試困難
  4. 框架一致性

等問題都踩過一遍了。而且我們做的還是做不能接受幻覺的帳務系統！還真的上線了。

### 我可以肯定這就是 Vibe Coding 的解決方式

接下來，我會用多篇文章 + 幾個 youtube video 來解釋。在那之前，我想先講一下緣起。

## 一切的起頭

我在2023 年開始，就大量利用 GenAI 加上非傳統科系的 intern 學生組成的數據團隊來工作，這段時間以來，我們都是以 AI 當作助手的方式來作業，基本上跑軟體開發的流程依舊還是跟原本一樣，走 Kaban ，只是用 ChatGPT 幫助這些 intern 做他們做不到的事情 (寫程式 ) 。這時候，軟體開發感覺就是單點的強化，但是不是流程的改造。中間的每個節點都是原本的做法

當然，公司的大家都知道我用的 7成工讀生，所以當我們團隊遇到一些系統技術問題時，大家其實是比較寬容的。另外，我也大量使用 SaaS 服務來彌補 intern 之間知識的不足，而專注做真正的 business 

![](/assets/images/image.png)

一直到 2025年的年初，隨著職務的調換，我們團隊從 intern 7成 轉成發展到正職 7成的正式團隊(也有數人從 intern 轉正），另外又來了兩個 intern 。隨著公司給我的 resource 增加，不管我選擇的是工讀生轉正還是直接 hire 外面的 engineer ，公司都會要求我做「真正的系統」，給出更高標準的技術要求

我那時很多心中的小劇場，我不認為我之前的 intern + AI 方法論是錯的，但是我心裡也知道，照原本的方法做不長久。但是要我把難得的 head count 去找 ”外面工程師" 換掉 這些跟我一段時間的 "幾位 Intern 弟弟妹妹們" 時，我也覺得對他們不太合理。

原因有幾個

  1. 在AI時代， 我的判斷是 Domain Knowledge 勝過技術，而這些 intern 跟我很久了，對於 Domain Knowledge 遠勝外面的人
  2. 在跟他們合作的時間 , 充分的感受到年輕人的 AI 含量遠勝過我們這些老屁股 , 每個人原生的擁抱AI 
  3. 越 Sr 的工程師用容易用原本的框架去想事情，但是 AI 時代新的框架還沒有誕生，我需要重塑軟體開發的人

## 賭注

在我選擇將所有 headcount 全部換成優秀的 intern 轉正時，HR用一副 "看到鬼" 的眼神看我，他說這對他來說很省事，也不用經過老闆的審批，但是他說沒有主管會在能 Hire Sr Eng 的時候 intern 轉正的 Jr 的

我跟他說

> 在 AI 時代，跟有現有思維框架的 Sr 我 比起來，這些弟弟妹妹才是真正的 Sr AI Engineer

但是他們需要一些指引跟創意來協助。

我注意到之前他們無法做大系統問題在於 "技術經驗" 跟 "協作能力" ，技術經驗 AI 是有充分能力可以彌補的，再加上我一個大叔當作最後一道屏障，肯定沒問題。但是多人協作經驗的確是麻煩，大家真的都剛畢業或是還在大四，這可能是真正的困難點。而且現在挑戰的不只是人跟人協作，還有人加 AI 協作

## 主要問題在於需要一套新的 AI Coding 流程

很幸運的是，當你注意到問題的時候，老天爺就給你解法了。我在2025年五月講生成式 AI時，前一個講者 Happy Lee 大大就直接給我講解法了，我們需要的是一套圍繞 PRD 為主的流程

![](/assets/images/image-1.png)

看完這套流程，我當下就跟 Happy 以及他底下的人要投影片跟聯繫方式，再來就是要求團隊開始研究這個流程，並且拿這套帳務系統需求當作 POC，

也因為如此，其實我們一開始在做這個帳務系統時，反而用傳統的流程跑，而非新的 PRD 為主的 開發。當一切入開發期(紅色的 bar) ，我們就陷入經驗不足的混亂，在下面 Week 19 ~ Week 22, 一直在泥沼內。當下其實我已經發現大家雖然都很 Jr , 但是已經有一定開發的範式了。（所以人的經驗牆是很容易出現的）

![](/assets/images/image-2.png)

我印象中在 week 22 的那個週三，因為很多原因(當天因為其他原因被老闆念)，我少數會議中出現很激動地對大家說「現在就是拋棄你們所熟悉的一切的時候，我們沒有任何退路，直接擁抱 AI Coding 跟新的流程」

然後，效率就很明顯就上去了。

## 流程不見得很厲害，主要原因是大家理解沒有退路，要擁抱這個流程

3個月的時候，我們經歷大量的迭代跟討論，甚至在 7/1 還去 Happy 91APP辦公室跟他們團隊交流。最後成功在七月底上線這個系統部分業務 !!!!!! 

這套做法已經跟 Happy 的做法有一些差距了。在七月的時候我們的辦公室的風景突然變成這樣

![](/assets/images/image-3.png)

從右到左，四台電腦三個人

  1. 第一台 air 是 Claude Code 做 tech lead , 負責看整個流程
  2. 第二台 air 是做 QA , PM 拿 PRD 叫 Cursor 去驗某個業務的程式
  3. 在跑到一半的時候，同一個 PM 拿訪談紀錄去 ChatGPT 生成新的 PRD 
  4. 做左邊的 air 是 Engineer 用 cursor 寫 code 

我那時候突然理解到，這個流程跟做法其實就跟現在大家在討論的 Spec Driven Development (AWS Kiro) 或是 Github Spec Kit 很類似，大家都在解決類似的問題。

也因為如此，我決定跟大家分享這套 ATPM 

## ATPM 

![](/assets/images/-------2025-09-17-------4.31.54.png)

他是一套以PRD為中心，用 AI 去強化 PM , Dev, QA 效率跟正確性的流程，裡面成功利用這個流程加速 40% 的時間，並且通過很嚴苛的 QA 驗證（畢竟是算上億元錢的系統）。

他是以 Assessment評估 , Testing 測試, Program 開發, Management (Supervisor 去監管) 為首字，並且高度強調迭代反饋回去 PRD 的流程跟框架。

他的主要幾個重點

  1. PRD為核心
  2. 每個節點都是 人跟 AI 協作, 所以PRD必須人跟AI都看得懂
  3. 所有的 Domain Knowledge 都是記錄在 PRD , 所以每個環節都不需要特定某個人, 可以自由輪調
  4. 特別重視 PRD 的反饋 , 我們之前經驗 , 一版 PRD 到結案，至少都大改 6 ~7 次，不是因為 PM 訪談問題，而是實務場景就是那麼複雜
  5. 花了很大時間跟人力在 QA , 原因不是AI做不到，而是為了避免AI幻覺，我們用大量的人力 QA Tradeoff 

接下來我會用幾篇文章跟一兩個 youtube video 來講述相關細節

[ ![\[Agent模式 Part 2 \] 臨機應變 vs 讀著路書跑 — 為什麼 AI Agent 需要 Plan & Exec 模式](/content/images/size/w600/2025/11/ChatGPT-Image-2025---11---1----------11_27_12.png) [Agent模式 Part 2 ] 臨機應變 vs 讀著路書跑 — 為什麼 AI Agent 需要 Plan & Exec 模式 WRC 賽車最經典的場面就是除了賽車手開著市售車款飛天遁地以外，最有趣的就是旁邊坐著一個副駕，讀著一本稱為「路書」的路線圖，用一些簡略的話去指引賽車手前進。 這個設計在追求速度的賽車界很有趣，因為坐一個副駕更重呀，為何需要把複雜的任務分成兩個角色——規劃者和執行者? 原因很簡單，WRC的賽道都是非常複雜，路況多變的越野賽到，他們經驗發現「規劃者搞清楚計劃，執行者全力執行然後隨機應變最有效率」 回到 AI Agenrt ，你有沒有想過當一個 AI 被指派一個複雜任務，它的腦子裡是怎麼想的？ 上一篇我們比較 AI Workflow 跟經典的 ReAct Agent， 我們看到 ReAct Agent 最後解決了客戶問題。但你有沒有想過，在 ReAct Agent 的彈性的優點下有沒有哪個致命的問題。今天來介紹一下一個新的 Agent 模型，或許是現在大家最常看的 Plan & Exec 模型。 Plan-and-Execute Plan-and-Execute（計畫與執行） By Wisely Chen 01 Nov 2025 ](/mang-mu-jia-su-vs-du-zhu-lu-shu-pao-wei-shi-mo-ai-agent-xu-yao-plan-exec-mo-shi/) [ ![\[Agent 模式 part 1\]  - Workflow 型和 ReAct 型，誰更像你？](/content/images/size/w600/2025/10/ChatGPT-Image-2025---10---30----------10_36_55.png) [Agent 模式 part 1] - Workflow 型和 ReAct 型，誰更像你？ 你有沒有發現，自己工作中也分裂成兩個人，有時按規則做事，有時根據現實應變。其實AI Agent 也一樣。想像一下下面的場景 客戶問：「我想查詢上個月的訂單」。 Agent A Agent : 連接「訂單歷史資料庫」 ❌ 連線失敗（資料庫正在維護） Agent : 系統回答客戶：「抱歉，我們的系統現在無法查詢。請稍後再試。」 結果：客戶必須稍後重試，專業一點的 Agent 就是會請人介入談話 Agent B Agent : 連接「訂單歷史資料庫」 ❌ 連線失敗（資料庫正在維護） Agent 觀察：思考：「主資料庫不通。但我的目標是『找到訂單』，不是『從主資料庫查訂單』。 有其他方式嗎？我們有備份系統嗎？」 Agent 行動：查詢「訂單備份硬碟」觀察：✓ 找到訂單 By Wisely Chen 30 Oct 2025 ](/agent-mo-shi-part-1-workflow-xing-he-react-xing-shui-geng-xiang-ni/) [ ![为什麼 AI Agent 无法企業落地？看泰山的挑水工就懂了](/content/images/size/w600/2025/10/-------2025-10-28-------10.13.48.png) 为什麼 AI Agent 无法企業落地？看泰山的挑水工就懂了 今天刷到一張照片，泰山樓梯上，一個白髮蒼蒼的挑水工用扁擔挑著水，一步步往上爬。除了心疼他的辛苦，還看到評論區飄出一條大橫幅 人口紅利正在減弱，以後替代的就是無人機紅利 這簡直一句話點燃了整個思維導火索。是呀、對呀、完全講得通啊 泰山挑水 = 無人機的完美技術應用場景 老齡化 + 無人接班 = 業務痛點 對的技術選型，有痛點，啟動專案的先決條件全部吻合。所以呢，立刻啟動項目、尋找無人機規格、選廠商、進行試點……邏輯完全沒毛病。 真的是這樣嗎？ 回覆區有人發了一句話，說得讓數位轉型顧問們恨不得摀臉——根本用不著什麼無人機黑科技，早就有個老東西完美解決這個場景：纜車。便宜、穩定、用了一百年了。 這就像我們在轉型會議室天天上演的劇碼：某個 AI 顧問拎著最新的 AI 大殺器進場，PPT 講得飛起，結論是「降本增效不能再好」。最後甲方的老 IT歪著頭問了一句——「等等，這事兒用批次自動化不就完了？」一句話， By Wisely Chen 29 Oct 2025 ](/shu-wei-zhuan/) [ ![超慢跑也能 Coding：Claude Code 帶來的真正生產力](/content/images/size/w600/2025/10/-------2025-10-26-------6.58.28-1-1.png) 超慢跑也能 Coding：Claude Code 帶來的真正生產力 大家都說 AI可以增加生產力，那到底啥是真正的生產力？ 今早台北下大雨，我在家陽台跑了一小時的超慢跑，上面的圖是我的環境。這一小時裡，我同時做了四件事： 1\. 運動 : 超慢跑 2\. 知識擷取: 聽Youtube Video (AI Topic) 3\. Vibe Coding / 數據分析 : Claude Code 4\. 網頁搜尋資訊: ChatGPT Altas 這個工作流之所以可行 ，因為「超慢跑 」+ 「Claude Code」 這個組合根本就是天作之合，超慢跑並非慢跑很安全，不需要太多注意力。 Claude Code 老實說真的在做事的時候，95% 的時間不需要去顧，但是總是有 5% 的需要出來 debug 一下，這時候超慢跑停下來一兩分鐘也沒差。 我這樣的 routine 已經持續了3個月之久了，如果是出太陽的時候， By Wisely Chen 28 Oct 2025 ](/vibe-duo-ai-ru-he-zeng-jia-wo-de-sheng-chan-li/)