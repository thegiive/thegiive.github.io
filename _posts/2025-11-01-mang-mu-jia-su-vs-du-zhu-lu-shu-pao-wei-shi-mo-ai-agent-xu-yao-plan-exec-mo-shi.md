---
layout: post
title: "[Agent模式 Part 2 ] 臨機應變 vs 讀著路書跑 — 為什麼 AI Agent 需要 Plan & Exec 模式"
date: 2025-11-01 03:59:36 +0000
permalink: /mang-mu-jia-su-vs-du-zhu-lu-shu-pao-wei-shi-mo-ai-agent-xu-yao-plan-exec-mo-shi/
image: /assets/images/ChatGPT-Image-2025---11---1----------11_27_12.png
description: "WRC 賽車最經典的場面就是除了賽車手開著市售車款飛天遁地以外，最有趣的就是旁邊坐著一個副駕，讀著一本稱為「路書」的路線圖，用一些簡略的話去指引賽車手前進。 這個設計在追求速度的賽車界很有趣，因為坐一個副駕更重呀，為何需要把複雜的任務分成兩個角色——規劃者和執行者?..."
---

[agent](https://ai-coding.wiselychen.com/tag/agent/)

# [Agent模式 Part 2 ] 臨機應變 vs 讀著路書跑 — 為什麼 AI Agent 需要 Plan & Exec 模式

[ ![Wisely Chen](/assets/images/6672228-F20250919----02-----------SN------10945w-1.jpg) ](/author/wisely/)

#### [Wisely Chen](/author/wisely/)

01 Nov 2025 — 7 min read

![\[Agent模式 Part 2 \] 臨機應變 vs 讀著路書跑 — 為什麼 AI Agent 需要 Plan & Exec 模式](/assets/images/ChatGPT-Image-2025---11---1----------11_27_12.png)

WRC 賽車最經典的場面就是除了賽車手開著市售車款飛天遁地以外，最有趣的就是旁邊坐著一個副駕，讀著一本稱為「路書」的路線圖，用一些簡略的話去指引賽車手前進。 這個設計在追求速度的賽車界很有趣，因為坐一個副駕更重呀，為何需要把複雜的任務分成兩個角色——規劃者和執行者? 

原因很簡單，WRC的賽道都是非常複雜，路況多變的越野賽到，他們經驗發現「規劃者搞清楚計劃，執行者全力執行然後隨機應變最有效率」

![](/assets/images/image-3.png)

回到 AI Agenrt ，你有沒有想過當一個 AI 被指派一個複雜任務，它的腦子裡是怎麼想的？ [上一篇](https://ai-coding.wiselychen.com/agent-mo-shi-part-1-workflow-xing-he-react-xing-shui-geng-xiang-ni/)我們比較 AI Workflow 跟經典的 ReAct Agent， 我們看到 ReAct Agent 最後解決了客戶問題。但你有沒有想過，在 ReAct Agent 的彈性的優點下有沒有哪個致命的問題。今天來介紹一下一個新的 Agent 模型，或許是現在大家最常看的 Plan & Exec 模型。

## Plan-and-Execute

Plan-and-Execute（計畫與執行）架構的出現，其實是對 ReAct 高成本和低效率問題的直接回應。 它的核心思想很簡單：把 Agent 的工作流明確地分成兩個獨立的階段。

  * 第一階段是「規劃」。這裡交給最強大的 LLM 做一件事：一次性思考清楚，生成一個詳細的、多步驟的完整計畫。不著急執行，就是想清楚。
  * 第二階段是「執行」。計畫已經定好了，執行器就按照計畫逐一完成每個步驟。這裡不需要每次都調用大型 LLM來做決策。可以用更輕量級的模型，甚至簡單的規則來執行。

![](/assets/images/image-60.png)

為什麼這樣更好？ ReAct 的問題是每一步都要 LLM 思考，所以成本高、速度慢。Plan-and-Execute 的優勢是思考集中在規劃階段，執行階段使用輕鬆便宜的 LLM。 WRC的車手也說，因為 WRC 路線實在太過複雜，一個人真的記不住路書又要靈機應變，所以真的需要副駕駛，基本上車手就是遇到 token 爆炸的問題。

### 跟 ReAct 比優點：

  * 大幅降低成本 — 不需要每一步都調用昂貴的大型 LLM。只在初始規劃和計畫失敗需要重新規劃時才用它。執行階段可以用更小、更快的模型，大大節省成本和時間。
  * 避免局部最優 — ReAct 邊走邊想，容易走進死胡同。Plan-and-Execute 強制 LLM 在出門前就做全局思考，一次性想清楚所有邊界情況，避免了局部最優的陷阱。

### 跟 ReAct 比缺點：

  * 應變能力弱，魯棒性差 — 計畫是寫死的，執行過程中可以應對狀況，但是沒有 ReAct 做得那麼好 。一旦某個步驟失敗，只能靈活性。
  * 執行效率有限 — 很多 Plan-and-Execute 的實現還是一步一步來，無法並行。所以效率提升空間還很大(比起其他可以平行 run 的 模式) 。

### 場景差距

跟聊天機器人來比的話，ReAct 更適合是一個陪伴型的 ChatBot , 或是知識問答 ChatBot ，他靈活簡單，問到特定問題模型邊想邊查，但是較難處理複雜問題（超過5步），容易出現局部最優但是不是全局最佳。

Plan & Exec 更適合是「旅遊規劃」聊天機器人，或是 Coding Agent，用戶說需求到模型規劃整個對話路線（確認問題到查詢方案到提供建議到執行決策）到逐步引導用戶走完流程。缺點就是首個回應慢（需要較長規劃時間）。

## Plan & Exec 跟 ReAct 的經典使用

老實說，並沒有看到哪個工具都用 ReAct ，也沒有看到哪個工具一定用的是 Plan & Exec。首先，商務場景下根本就不可能看到純 ReAct ，現實上一定採取限制步數的 ReAct ，因為純 ReAct 遇到無法解決的問題一定是 token 爆炸

### ReAct 舉例

一般現在有水準，可以搜尋的 Chatbot ，幾乎都是 受限制ReAct 的教科書案例

像是我故意問ChatGPT 5 Thinking：「對比 Claude 5、GPT-6、Gemini 最新版本在推理、代碼生成、多語言方面的表現，給出具體測試數據」。有沒有注意到，我故意問錯的問題( 2025/11/1 時間，Claude公開只出到 4.5 ，GPT只出到 6），要考驗他們除錯都能力。

![](/assets/images/image-1.png)

ChatGpt：思考 → 搜尋多個來源（新聞、技術論壇、官方公告）→ 觀察結果 → 再思考「我找到的夠完整嗎」→ 可能再搜尋補充 → 最後綜合回答。你能看到它的思考過程，它在即時調整搜尋策略。

### Plan & Exec 舉例

同比 Plan & Exec 最直觀的例子就是 Deep Research 了，尤其是 Gemini 的 Deep Research 在 UI 設計上根本就是教科書級別 Plan & Research 介紹

![](/assets/images/image-2-1.png)

當我問到 Gemini 「幫我解釋 react 跟plan and exec 在ai agent 模式的不同 」，他會先給你一個研究大綱，等你確認後，再去每一步搜尋，調整，每一步都有可能找錯資料，但是會在每一步的範疇內微調。

當然，Claude Code 的 Plan Mode 也是很好很直觀的 Plan&Exec; 的案例。當我們下達修改某個 feature，通常都只要稍微複雜，就會需要先 Plan 列出來後才進行修改

## 你的 Agent 是盲目加速還是讀著路書跑？

  
之前說到如果環境多變化，你需要 ReAct 來保證魯棒性，但是如果環境多變化，任務又很複雜——你需要 Plan-and-Execute。 整體用 Plan 保證不亂走，局部用 ReAct 靈活應對。就像真實的 WRC：副駕手寫好路書，永遠看著整個賽道全局最優，但主駕手在每個彎道仍然要靠直覺微調。這才是 WRC 的勝利方程式，兼顧全局跟細節的微調。

[ ![Multi-Agent 協作模式：當 AI 學會「會診」這件事](/assets/images/ChatGPT-Image-2025---11---15----------04_36_04.png) Multi-Agent 協作模式：當 AI 學會「會診」這件事 我上週回老家看了久違的第四台「緯來日本台」，看一個日本節目「恐怖家庭醫學」，裡面講到一個年長者「最近常常心悸、手抖、睡不好」。因為是心臟的因素，所以患者直接找心臟科檢查後，拿到一疊厚厚的報告——結果心臟科醫生看完報告說：「你的心臟結構完全正常，心電圖也沒問題，可能是壓力太大，回去多休息就好。」患者心想：「可是我真的有心悸啊！難道是我自己想太多？」於是患者找了神經科說可能是自律神經失調，拿了藥物減壓，但症狀完全沒改善。 弄了很久一直兜兜轉轉。最後一個經驗豐富家醫科醫生，告知患者「這可能是甲狀腺的問題，要去看內科」才發現這是甲亢的症狀，調整好藥物很快就好了。很多時候人體很多時候是一個連動的生態系統，有些問題的表象跟真正的Root Cause是兩回事，所以患者很容易找錯醫生弄錯科目。 但如果是在好的健檢中心，做法就完全不一樣了。健康檢查會根據你的全方位給予檢查——最後針對你的完整報告進行討論，這時候甲亢的 Root Cause 很快就會被最後的把關者抓出來 " 問題根本不在心臟，而在甲狀腺 " 。這就是「多人協作的力量」。 AI Agent 的世界也是一樣的道理。 By Wisely Chen 15 Nov 2025 ](/multi-agent-xie-zuo-mo-shi-dang-ai-xue-hui-hui-zhen-zhe-jian-shi/) [ ![那天我在產業園區分享：AI 能不能做起來，其實看人](/assets/images/S__88875042.jpg) 那天我在產業園區分享：AI 能不能做起來，其實看人 今天我在新北產業園區，在我們公司的 AI 轉型的活動 在各位傳統產業的前輩講述我之前在傳統產業做 AI 轉型的經驗 我認為「 AI 要在傳產落地，先解決的永遠不是模型，而是人、流程與文化。」 我把這幾年的實戰經驗濃縮成一套能在傳統產業中真正起作用的框架： 現況分析：先理解現場，再談技術 我們創建了一個以 公司各部門的老前輩 + Intern 為主的種子團隊，深入一線流程、取得高層支持，建立真正的共識。 AI 不是空降，而是跟現場一起改。 快速勝利：小範圍試點，讓大家看到成效 選一個可控的場域，把 AI +種子團隊拉進真實流程。 像我用 AI + RPA + OCR + 快速掃描器 = 一個可持續可落地，並且有效益成果 這樣的「小勝利」，是推動組織願意往下走的關鍵。 全面升級：從工具導入到組織轉型 把建置的種子團隊散步到全公司各個部門 可以用很快的速度去 scale 全面開花 By Wisely Chen 13 Nov 2025 ](/na-tian-wo-zai-chan-ye-yuan-qu-fen-xiang-ai-neng-bu-neng-zuo-qi-lai-qi-shi-kan-ren/) [ ![AI 信任崩塌的真正原因：勞資零和賽局的再現](/assets/images/ChatGPT-Image-2025---11---10----------09_24_03.png) AI 信任崩塌的真正原因：勞資零和賽局的再現 根據《Harvard Business Review》近期發表的〈Workers Don’t Trust AI. Here’s How Companies Can Change That〉，美國基層員工對公司提供的 AI 工具信任度在短短數月內暴跌：對生成式 AI 的信任下降 31%，對自主決策型 AI 更下滑 89%。近半數員工反而更信任非官方AI 工具。另外無獨有偶MIT 的研究《The GenAI Divide: State of AI in Business 2025》更進一步揭示了這種現象，並命名為 Shadow AI：員工在公司外私下使用未授權的 AI 來完成工作。研究指出，約有 By Wisely Chen 10 Nov 2025 ](/ai-xin-ren-beng-ta-de-zhen-zheng-yuan-yin-lao-zi-ling-he-sai-ju-de-zai-xian/) [ ![\[Agent part 3\] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵](/assets/images/ChatGPT-Image-2025---11---8----------08_01_49.png) [Agent part 3] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵 大家都知道我用 AI 來 enable 很多intern 來當作很多正職的事情，當然他們雖然都很年輕跟熱情，但是我管理團隊時發現一個規律： 當我派給幾個 Senior 的同事 ，我通常只需要 weekly 跟他開會，給他幾個任務，一週後檢查一次就好。他可以獨立工作，中間遇到問題會自己判斷、調整，如果有大問題他們會舉手跟我講，不容易走偏。 當我要安排工作給我的 intern ，跟 Senior 最大的不同就是， Junior 我通常會每半天或是每過一天就會跟他聊一下提醒一下可能要注意什么事情。因為他很容易遇到了某些複雜任務時，他就可能在某一步卡住，又沒有舉手，基於錯誤理解繼續做下去，最後整個方向偏了，也浪費了他整天的時間。 這是Sr 跟 Jr 經驗的差別，獨立作戰的能力 AI Agent 也是如此 現在考驗 AI Agent 最大的地方，不是他的智商，主要著重點是它的連續工作穩定性。如果人類需要介入的越少，就代表它可以自主完成工作， By Wisely Chen 08 Nov 2025 ](/agent-part-3-interleaved-thinking-cheng-xian-de-wen-ding-xing-shi-xian-zai-agentluo-di-de-zhong-yao-guan-jian/)