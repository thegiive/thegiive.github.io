---
layout: post
title: "[Agent part 3] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵"
date: 2025-11-08 12:18:37 +0000
permalink: /agent-part-3-interleaved-thinking-cheng-xian-de-wen-ding-xing-shi-xian-zai-agentluo-di-de-zhong-yao-guan-jian/
image: /assets/images/ChatGPT-Image-2025---11---8----------08_01_49.png
description: "大家都知道我用 AI 來 enable 很多intern 來當作很多正職的事情，當然他們雖然都很年輕跟熱情，但是我管理團隊時發現一個規律：..."
---

[agent](https://ai-coding.wiselychen.com/tag/agent/)

# [Agent part 3] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵

[ ![Wisely Chen](/assets/images/6672228-F20250919----02-----------SN------10945w-1.jpg) ](/author/wisely/)

#### [Wisely Chen](/author/wisely/)

08 Nov 2025 — 7 min read

![\[Agent part 3\] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵](/assets/images/ChatGPT-Image-2025---11---8----------08_01_49.png)

大家都知道我用 AI 來 enable 很多intern 來當作很多正職的事情，當然他們雖然都很年輕跟熱情，但是我管理團隊時發現一個規律：

![](/assets/images/image-26.png)有 Sr 的經驗，跟有 Jr 熱情的 Data&AI; Team 

當我派給幾個 Senior 的同事 ，我通常只需要 weekly 跟他開會，給他幾個任務，一週後檢查一次就好。他可以獨立工作，中間遇到問題會自己判斷、調整，如果有大問題他們會舉手跟我講，不容易走偏。

當我要安排工作給我的 intern ，跟 Senior 最大的不同就是， Junior 我通常會每半天或是每過一天就會跟他聊一下提醒一下可能要注意什么事情。因為他很容易遇到了某些複雜任務時，他就可能在某一步卡住，又沒有舉手，基於錯誤理解繼續做下去，最後整個方向偏了，也浪費了他整天的時間。

這是Sr 跟 Jr 經驗的差別，獨立作戰的能力

###  AI Agent 也是如此 

  
現在考驗 AI Agent 最大的地方，不是他的智商，主要著重點是它的連續工作穩定性。如果人類需要介入的越少，就代表它可以自主完成工作，不需要人打擾，生產力就會釋放出來。

在 Agent 界有一個很重要的考核指標叫做 METR。Claude 3.7 Sonnet 2025 初METR 可以獨立工作約 1小時，之後就需要人類確認方向。2025 年五月 Opus 已經可以到 7小時，到了 2025 年 9 月，Claude Sonnet 4.5 已經可以持續專注工作超過 30 小時，無需人工干預自主構建完整的聊天應用，生成 11,000 行代碼。

![](/assets/images/image-25.png)

為什麼進步這麼快？關鍵就是 Claude 4.5 加入了 interleaved thinking（交錯思考）這樣的機制——讓 Agent 像 Senior PM一樣，每一步都自我驗證、發現問題立即調整、遇到大問題主動舉手。當這種 Agent 獨立作業的能力到臨界值，Agent 就可以像 Sr PM 一樣，在半夜或是不需要介入的情況下，直接做事，等早上人類起床驗收。

### Interleaved Thinking 

傳統的 Agent 架構（如 ReAct 和 Plan & Execute）有個共同做法：思考和執行是分離的，Interleaved Thinking 不一樣， 它讓「思考」貫穿整個執行過程——不只是在工具調用之間思考，而是在每個行動的前、中、後都持續思考。規劃與行動交錯進行

具體來說： 思考 → 行動 → 驗證 → 調整 → 保存檢查點 → 重複

![](/assets/images/image-23.png)

這就像不是「做完再想」，而是「邊做邊想邊驗證」。實作來說

> Plan & Exec 只要支援一次呼叫（像 `run_agent()`），  
> Interleaved Thinking 需要支援「連續多次 API 呼叫 + 狀態回饋」

從實作上，Interleaved Thinking 通常需要一個 **中控 loop** 來管理「思考 ↔ 行動 ↔ 反思」的循環：

![](/assets/images/image-24.png)

所以系統要能：

  1. 暫存中間狀態（memory / context buffer）
  2. 動態更新 prompt（inject observation）
  3. 控制 reasoning token 數量（防止爆 token）

從實作來說，API 也需要實作以下的相關功能

類別| 說明| 範例  
---|---|---  
**Streaming 回饋**|  模型思考時能即時輸出 reasoning 片段| `response_format: reasoning` 或 `logprobs`  
**函式調用回饋 (function / tool calls)**|  每步能呼叫外部工具並根據回傳再思考下一步| `tool_calls` in OpenAI API, `functions` in Anthropic  
**狀態持續化 (state persistence)**|  每輪能記住目前任務進度| e.g. Session-based API (`session_id`)  
**思考可見化 (visible reasoning)**|  可開啟「思考區塊」，幫助debug| e.g. `o1-preview` 模式輸出有 “reasoning trace”  
  
有支援的 Model

  * Claude 4 系列開始支援「interleaved thinking」
  * OpenAI Responses API : GPT-4.1 , o3, o4 , O1, 若系統希望達成真正「邊思邊做」（即 interleaved thinking：思考 → 工具／行動 → 再思考 → 下一步）流程，除了模型／API 支援之外，還需要在系統端設計一個 **迴圈 (loop)** ：監控工具調用結果、更新上下文、觸發下一輪思考。
  * Gemini : 2.5 支援「thinking 模式」，但 **是否真正支援完整的「interleaved thinking」（邊做邊思考／思考 ↔ 行動 交錯）** 尚未完全被官方標示。

## Interleaved thinking 好處

  * **穩定度提升** ：由於在每個步驟之間都有反饋與再思考機制，模型能即時修正推理軌跡，顯著降低多步錯誤累積。
  * **推理深度增加** ：模型學會「先驗假設—驗證—修正」循環，而非線性生成；使在數學、邏輯、編程等任務中更接近人類思考。
  * **速度與效率並進** ：Interleaved Thinking 透過部分並行思考與中途決策更新，使平均回覆時間更短、token 消耗更少。

基本上讓模型在多步推理任務中更穩、更快、更準，提升幅度平均約 20–30 %，錯誤率下降 35 %以上，已成為下一代 Reasoning Model 的核心趨勢

### Interleaved Thinking 缺點

  1. 成本與效率 : Token 消耗增加 15-30%： 每一步都要思考、验证、调整, 執行時間變長： 需要 5-10 次 API 調用，而非一次性完成
  2. 技術實作複雜度高： 需要設計中控 loop 管理狀態, 需要暫存中間狀態： memory / context buffer 管理困難, 錯誤處理複雜： 需要處理迴圈中每一步的失敗情況
  3. 無法控制行為問題：容易陷入過度思考迴圈： 反覆驗證同一結果，無限循環, 另外需要設定終止條件： 最大迭代次數、收斂條件等
  4. 模型要求要求高： 需要準確判斷、找備選方案、知道何時求助。如果硬要用舊模型表現差，反而降低成功率
  5. 適用性限制: 簡單任務不划算, 不適合即時應用： 聊天機器人、客服系統等需要快速回應的場景，也不適合高度可控場景： 金融交易、醫療決策等需要明確可預測的流程

### 總結

  
Interleaved Thinking 讓 AI Agent 的連續穩定工作時間大增，這是 AI Agent 整合進去企業端的關鍵指標。但代價是 token 消耗增加 15-30%、執行時間變長、對模型要求複雜度高，適合複雜多步驟任務，但對簡單任務或即時應用來說不划算。

一句話：選對場景，才能發揮最大價值。

[ ![Multi-Agent 協作模式：當 AI 學會「會診」這件事](/assets/images/ChatGPT-Image-2025---11---15----------04_36_04.png) Multi-Agent 協作模式：當 AI 學會「會診」這件事 我上週回老家看了久違的第四台「緯來日本台」，看一個日本節目「恐怖家庭醫學」，裡面講到一個年長者「最近常常心悸、手抖、睡不好」。因為是心臟的因素，所以患者直接找心臟科檢查後，拿到一疊厚厚的報告——結果心臟科醫生看完報告說：「你的心臟結構完全正常，心電圖也沒問題，可能是壓力太大，回去多休息就好。」患者心想：「可是我真的有心悸啊！難道是我自己想太多？」於是患者找了神經科說可能是自律神經失調，拿了藥物減壓，但症狀完全沒改善。 弄了很久一直兜兜轉轉。最後一個經驗豐富家醫科醫生，告知患者「這可能是甲狀腺的問題，要去看內科」才發現這是甲亢的症狀，調整好藥物很快就好了。很多時候人體很多時候是一個連動的生態系統，有些問題的表象跟真正的Root Cause是兩回事，所以患者很容易找錯醫生弄錯科目。 但如果是在好的健檢中心，做法就完全不一樣了。健康檢查會根據你的全方位給予檢查——最後針對你的完整報告進行討論，這時候甲亢的 Root Cause 很快就會被最後的把關者抓出來 " 問題根本不在心臟，而在甲狀腺 " 。這就是「多人協作的力量」。 AI Agent 的世界也是一樣的道理。 By Wisely Chen 15 Nov 2025 ](/multi-agent-xie-zuo-mo-shi-dang-ai-xue-hui-hui-zhen-zhe-jian-shi/) [ ![那天我在產業園區分享：AI 能不能做起來，其實看人](/assets/images/S__88875042.jpg) 那天我在產業園區分享：AI 能不能做起來，其實看人 今天我在新北產業園區，在我們公司的 AI 轉型的活動 在各位傳統產業的前輩講述我之前在傳統產業做 AI 轉型的經驗 我認為「 AI 要在傳產落地，先解決的永遠不是模型，而是人、流程與文化。」 我把這幾年的實戰經驗濃縮成一套能在傳統產業中真正起作用的框架： 現況分析：先理解現場，再談技術 我們創建了一個以 公司各部門的老前輩 + Intern 為主的種子團隊，深入一線流程、取得高層支持，建立真正的共識。 AI 不是空降，而是跟現場一起改。 快速勝利：小範圍試點，讓大家看到成效 選一個可控的場域，把 AI +種子團隊拉進真實流程。 像我用 AI + RPA + OCR + 快速掃描器 = 一個可持續可落地，並且有效益成果 這樣的「小勝利」，是推動組織願意往下走的關鍵。 全面升級：從工具導入到組織轉型 把建置的種子團隊散步到全公司各個部門 可以用很快的速度去 scale 全面開花 By Wisely Chen 13 Nov 2025 ](/na-tian-wo-zai-chan-ye-yuan-qu-fen-xiang-ai-neng-bu-neng-zuo-qi-lai-qi-shi-kan-ren/) [ ![AI 信任崩塌的真正原因：勞資零和賽局的再現](/assets/images/ChatGPT-Image-2025---11---10----------09_24_03.png) AI 信任崩塌的真正原因：勞資零和賽局的再現 根據《Harvard Business Review》近期發表的〈Workers Don’t Trust AI. Here’s How Companies Can Change That〉，美國基層員工對公司提供的 AI 工具信任度在短短數月內暴跌：對生成式 AI 的信任下降 31%，對自主決策型 AI 更下滑 89%。近半數員工反而更信任非官方AI 工具。另外無獨有偶MIT 的研究《The GenAI Divide: State of AI in Business 2025》更進一步揭示了這種現象，並命名為 Shadow AI：員工在公司外私下使用未授權的 AI 來完成工作。研究指出，約有 By Wisely Chen 10 Nov 2025 ](/ai-xin-ren-beng-ta-de-zhen-zheng-yuan-yin-lao-zi-ling-he-sai-ju-de-zai-xian/) [ ![為什麼 AI 會議記錄工具 99% 都需要人工修正——用企業知識庫來救](/assets/images/ChatGPT-Image-2025---11---7----------06_28_19.png) 為什麼 AI 會議記錄工具 99% 都需要人工修正——用企業知識庫來救 當我還在物流業的時候，某個週一下午，PM 在 email 上丟出上周五會議的AI自動紀要。 我看了兩眼就懵了：「我們物流業什麼時候決定投資英鎊了？」後來看一下會議轉寫稿。我看到這個才恍然大悟，原來 AI 把 物流的 InBound(入庫) 聽成英鎊了。 AI 轉寫工具的極限 2024 年末，AI 會議記錄工具滿天飛。Ottr、Plaud、各種標榜「自動轉寫、秒出紀要」的應用，都在宣傳自己的驚人準確度。 只是現實很殘酷，實際到了可以寄給客戶的會議紀要階段，90% 都需要人工修正 不是技術問題。是語境問題。一個通用的 ASR（自動語音辨識）無法理解你公司內部的黑話。它聽不懂你的同音混淆、分不清人名、搞不懂企業專有名詞。而這些東西，決定了會議記錄到底能不能用。 我在工作中觀察了足夠多的會議記錄失敗案例，歸納出 4 個層級的問題。越往下， By Wisely Chen 07 Nov 2025 ](/wei-shi-mo-ai-hui-yi-ji-lu-gong-ju-99-du-xu-yao-ren-gong-xiu-zheng-yong-qi-ye-zhi-shi-ku-lai-jiu/)