---
layout: post
title: "[AI Ops] 用 Agent(Claude Code) 做 Linux 系統管理有沒有搞頭？香得很！"
date: 2025-10-24 00:34:56 +0000
permalink: /ai-ops-yong-agent-claude-code-zuo-linux-xi-tong-guan-li-you-mei-you-gao-tou-xiang-de-hen/
image: /assets/images/ChatGPT-Image-2025---10---24----------08_31_52.png
description: "今天突然發現用 Claude Code 做 Linux 系統管理超香的。不只可以幫你寫 code，還順便幫你考古系統程式，挖出系統裡不為人知的秘密，最棒的是能讓你找到之前同事寫好的 code 提早下班，享受當老闆的樂趣。..."
---

[agent](https://ai-coding.wiselychen.com/tag/agent/)

# [AI Ops] 用 Agent(Claude Code) 做 Linux 系統管理有沒有搞頭？香得很！

[ ![Wisely Chen](/content/images/size/w160/2025/09/6672228-F20250919----02-----------SN------10945w-1.jpg) ](/author/wisely/)

#### [Wisely Chen](/author/wisely/)

24 Oct 2025 — 5 min read

![\[AI Ops\] 用 Agent\(Claude Code\) 做 Linux 系統管理有沒有搞頭？香得很！](/content/images/size/w1200/2025/10/ChatGPT-Image-2025---10---24----------08_31_52.png)

今天突然發現用 Claude Code 做 Linux 系統管理超香的。不只可以幫你寫 code，還順便幫你考古系統程式，挖出系統裡不為人知的秘密，最棒的是能讓你找到之前同事寫好的 code 提早下班，享受當老闆的樂趣。  
  
話說今天某個客戶系統出問題了，大家忙到炸掉。為了安撫客戶，我就跟客戶說

> 「我來寫 monitor script 吧」

既然牛都吹了，來都來了，就來寫吧，反正也不是我寫 XD。我對 Claude Code 很有信心，因為 Linux 系統管理本質就是 command line，而 Claude Code 生來就是為 command line 而生，而且很專精！

### 目標

我的目標就是在一台 Linux machine 寫 monitor script，確認某些檔案在特定的時間必須要產出，並且產出檔名要合乎規格。不過就要報 alert 。說實在話，我沒有任何這台系統資訊，我只是先溝通了 IT 拿到 ssh 就衝了。

關於我自己在 linux 上，其實不算白板，我有一點點 linux admin 經驗但是不多。我一直會寫 bash/perl script ，而且我很自豪我可以用 vim 寫一個 project 面不改色。總之，我算熟悉，不算精通 IT Admin。

### 讓 Claude Code 幫你解決問題

但是我很清楚 Agent (尤其是 Claude Code ）在這個場景，應該是他的絕對舒適區。所以我的步驟是不給資訊，讓 Claude Code 盲猜以下的 Case 

  1. 請 Claude Code ssh vm 
  2. 請他先看一下系統的summary 
  3. 找出非系統的 deamon 
  4. 解釋一下 deamon 的意義

結果真的還蠻驚喜的。

FYI : 當然有下提示詞, 禁止做任何修改性的動作

### Case : 看一下系統 Summary 

這根本就是一堆基本操作，對每個 IT OPS 都會的 step , 相信 Claude Code 沒問題吧 

> Prompt : 幫我看一下系統跑哪些 application 

雖然有心理準備，還是我驚嘆 CC的精細度，連crontab jon 說明都有 ，代表他有進去看 code 

![](/assets/images/image-41-1.png)

### Case : 找出非系統的 daemon

因為擔心裡面有太多 system daemon ，混淆視聽，我請他直接 filter 掉，只看業務

> Prompt : 幫我過濾到常見的 app 跟 GCP 預設的管理 app 

裡面最神的就是 Claude Code 怎麼知道這台伺服器就是轉運站的? Claude Code 去看裡面每個 code ? 

![](/assets/images/image-42-1.png)

### Case : 解釋一下 daemon 的意義

通常我們在系統上，遇到老機器，如果老 IT 不在的話，常會遇到一些daemon 很難理解沒有人記得的 application 。這時候常常很難解釋。

但是今天我們發現到

> AI 會去翻程式，告訴你古老程式的細節, 簡直是天選考古人。

當然我在猜要看得懂應該是要明文的 code 像是 bash or python 這種啦

![](/assets/images/image-43-1-1.png)

### 彩蛋 Case : 幫我翻到老程式，Claude Code 幫我提早下班

我本來上這台VM是要寫 monitor script ，沒想到 Claude Code 看著看著，居然發現上面有一個兩年前的老 script ，裡面邏輯就是 exactly 我要做的事情

![](/assets/images/image-45-1-1.png)

只可惜之前的 IT 不知道誰忘了他，也已經沒有跑了。不過沒關係， Claude Code 從泥土中找到這個程式，重新擦亮他。我可以提早下班了。

![](/assets/images/ChatGPT-Image-2025---10---24----------09_40_08-1.png)喜歡這張圖

### Final Case : 享受當老闆的樂趣

最後 , Claude Code給我最好的情緒價值就是，我可以從牛馬轉成老闆，問出一句經典名言

> Prompt : 今天機器一切順利嗎? 

![](/assets/images/image-44-1.png)

### 從牛馬變老闆的快樂

這次用 Claude Code 做 Linux 系統管理，最大的感受就是**角色轉換** 。以前遇到老舊系統，要嘛找老員工問（如果還在的話），要嘛自己土法煉鋼一個指令一個指令試，通常要花一段時間才能搞清楚狀況，更別說寫出能用的 monitor script。

但這次不一樣。我只是給了 SSH 帳號，剩下的 Claude Code 全包了：自動探索系統、分析 daemon、解釋古老 script、甚至找出兩年前被遺忘的程式。30 分鐘的活 3 分鐘搞定，我從「又要加班的牛馬」變成可以悠哉問出「今天機器一切順利嗎？」的老闆。

最後一句話： 下次遇到老舊 Linux 系統，除了翻文檔找人問，直接問 Claude Code。它會帶你考古、幫你寫 script，還順便讓你早點下班！

[ ![\[Agent模式 Part 2 \] 臨機應變 vs 讀著路書跑 — 為什麼 AI Agent 需要 Plan & Exec 模式](/content/images/size/w600/2025/11/ChatGPT-Image-2025---11---1----------11_27_12.png) [Agent模式 Part 2 ] 臨機應變 vs 讀著路書跑 — 為什麼 AI Agent 需要 Plan & Exec 模式 WRC 賽車最經典的場面就是除了賽車手開著市售車款飛天遁地以外，最有趣的就是旁邊坐著一個副駕，讀著一本稱為「路書」的路線圖，用一些簡略的話去指引賽車手前進。 這個設計在追求速度的賽車界很有趣，因為坐一個副駕更重呀，為何需要把複雜的任務分成兩個角色——規劃者和執行者? 原因很簡單，WRC的賽道都是非常複雜，路況多變的越野賽到，他們經驗發現「規劃者搞清楚計劃，執行者全力執行然後隨機應變最有效率」 回到 AI Agenrt ，你有沒有想過當一個 AI 被指派一個複雜任務，它的腦子裡是怎麼想的？ 上一篇我們比較 AI Workflow 跟經典的 ReAct Agent， 我們看到 ReAct Agent 最後解決了客戶問題。但你有沒有想過，在 ReAct Agent 的彈性的優點下有沒有哪個致命的問題。今天來介紹一下一個新的 Agent 模型，或許是現在大家最常看的 Plan & Exec 模型。 Plan-and-Execute Plan-and-Execute（計畫與執行） By Wisely Chen 01 Nov 2025 ](/mang-mu-jia-su-vs-du-zhu-lu-shu-pao-wei-shi-mo-ai-agent-xu-yao-plan-exec-mo-shi/) [ ![\[Agent 模式 part 1\]  - Workflow 型和 ReAct 型，誰更像你？](/content/images/size/w600/2025/10/ChatGPT-Image-2025---10---30----------10_36_55.png) [Agent 模式 part 1] - Workflow 型和 ReAct 型，誰更像你？ 你有沒有發現，自己工作中也分裂成兩個人，有時按規則做事，有時根據現實應變。其實AI Agent 也一樣。想像一下下面的場景 客戶問：「我想查詢上個月的訂單」。 Agent A Agent : 連接「訂單歷史資料庫」 ❌ 連線失敗（資料庫正在維護） Agent : 系統回答客戶：「抱歉，我們的系統現在無法查詢。請稍後再試。」 結果：客戶必須稍後重試，專業一點的 Agent 就是會請人介入談話 Agent B Agent : 連接「訂單歷史資料庫」 ❌ 連線失敗（資料庫正在維護） Agent 觀察：思考：「主資料庫不通。但我的目標是『找到訂單』，不是『從主資料庫查訂單』。 有其他方式嗎？我們有備份系統嗎？」 Agent 行動：查詢「訂單備份硬碟」觀察：✓ 找到訂單 By Wisely Chen 30 Oct 2025 ](/agent-mo-shi-part-1-workflow-xing-he-react-xing-shui-geng-xiang-ni/) [ ![为什麼 AI Agent 无法企業落地？看泰山的挑水工就懂了](/content/images/size/w600/2025/10/-------2025-10-28-------10.13.48.png) 为什麼 AI Agent 无法企業落地？看泰山的挑水工就懂了 今天刷到一張照片，泰山樓梯上，一個白髮蒼蒼的挑水工用扁擔挑著水，一步步往上爬。除了心疼他的辛苦，還看到評論區飄出一條大橫幅 人口紅利正在減弱，以後替代的就是無人機紅利 這簡直一句話點燃了整個思維導火索。是呀、對呀、完全講得通啊 泰山挑水 = 無人機的完美技術應用場景 老齡化 + 無人接班 = 業務痛點 對的技術選型，有痛點，啟動專案的先決條件全部吻合。所以呢，立刻啟動項目、尋找無人機規格、選廠商、進行試點……邏輯完全沒毛病。 真的是這樣嗎？ 回覆區有人發了一句話，說得讓數位轉型顧問們恨不得摀臉——根本用不著什麼無人機黑科技，早就有個老東西完美解決這個場景：纜車。便宜、穩定、用了一百年了。 這就像我們在轉型會議室天天上演的劇碼：某個 AI 顧問拎著最新的 AI 大殺器進場，PPT 講得飛起，結論是「降本增效不能再好」。最後甲方的老 IT歪著頭問了一句——「等等，這事兒用批次自動化不就完了？」一句話， By Wisely Chen 29 Oct 2025 ](/shu-wei-zhuan/) [ ![超慢跑也能 Coding：Claude Code 帶來的真正生產力](/content/images/size/w600/2025/10/-------2025-10-26-------6.58.28-1-1.png) 超慢跑也能 Coding：Claude Code 帶來的真正生產力 大家都說 AI可以增加生產力，那到底啥是真正的生產力？ 今早台北下大雨，我在家陽台跑了一小時的超慢跑，上面的圖是我的環境。這一小時裡，我同時做了四件事： 1\. 運動 : 超慢跑 2\. 知識擷取: 聽Youtube Video (AI Topic) 3\. Vibe Coding / 數據分析 : Claude Code 4\. 網頁搜尋資訊: ChatGPT Altas 這個工作流之所以可行 ，因為「超慢跑 」+ 「Claude Code」 這個組合根本就是天作之合，超慢跑並非慢跑很安全，不需要太多注意力。 Claude Code 老實說真的在做事的時候，95% 的時間不需要去顧，但是總是有 5% 的需要出來 debug 一下，這時候超慢跑停下來一兩分鐘也沒差。 我這樣的 routine 已經持續了3個月之久了，如果是出太陽的時候， By Wisely Chen 28 Oct 2025 ](/vibe-duo-ai-ru-he-zeng-jia-wo-de-sheng-chan-li/)