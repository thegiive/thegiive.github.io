---
layout: post
title: "從 Simple RAG 到 Autonomous Agent 之間的「恐怖谷」"
date: 2025-11-23
categories: AI Agent
tags: [AIAgent, DeepResearch, LLM, ArchitecturalDesign, System2Thinking, ProductionAI]
author: Wisely Chen
excerpt: "LinkedI Post 草稿：探討 Deep Research 架構如何用 System 2 思維為 Agent 加入自我檢查能力，解決傳統架構的根本問題。"
---

![Deep Research 標題圖](/assets/images/deep-research-title-logo.png)

## 我們需要自主的 Agent

當前的 GenAI 浪潮中，我們處於一個尷尬的階段：RAG（檢索增強生成）已普及，但我們需要的是能夠在生產環境下自主活動的 Agent。

我們構建的 Agent 看似智能，但在面對複雜或模糊的現實世界問題時，其表現與期望之間存在巨大鴻溝。

這就是 **Simple RAG Agent** 和 **Truly Autonomous Agents** 之間的「巨大鴻溝」。

這不是 Prompt 可以解決的問題。這是一個架構問題。

過去一年,我們的焦點一直在「如何寫更好的 Prompt」。但真正的轉變發生在我們意識到：每一個 Agent 都無法保證 100% 正確，錯誤會級聯傳遞。如果第一次檢索的結果有誤，整個下游流程就會「一本正經地胡說八道」，而 Agent 本身對此毫無察覺。沒有回頭路。

我們開始思考：Plan-Execute 這樣的 DAG（有向無環圖）架構是否已經無法支持相關的魯棒性？

---

## 思考的快與慢

諾貝爾獎得主 Daniel Kahneman 在《快思慢想》中提出:人類有兩種思維系統。

![System 1 vs System 2 對比圖](/assets/images/system-1-vs-2-comparison.png)

**⚡ System 1(快思):** 直覺、快速、無意識的反應
- **對應 Agent:** 生成文本、進行簡單的工具調用

**🧠 System 2(慢想):** 審慎、邏輯、耗能的推理
- **對應 Agent:** 處理複雜問題、進行自我審查與批判性評估

當你面對高風險決策時(買房、簽合約、醫療選擇),你會啟動 System 2:做完決定後,再回頭檢查一遍,確認沒問題才執行。

**但現在大部分的 Agent 都只有 System 1,沒有 System 2。**

這就是為什麼它們很容易會「一本正經地胡說八道」— 因為缺乏自我檢查的能力。

---

## 架構

Deep Research 架構的核心洞察:

**不要強迫球員兼裁判，一個模型同時扮演兩個角色。**

我們的設計:

**System 1 層(快思 — 規劃與執行):**
- Planner Node: 拆解模糊請求為結構化子任務
- Executor Node: 調用工具獲取原始資訊
- 使用成本低、速度快的模型

**System 2 層(慢想 — 批判性評估):**
- Critic/Reflector Node: 一致性檢查、完整性檢查、幻覺檢測
- 使用強推理模型

這個解耦帶來兩個關鍵好處:
1. **成本效率**: 不需要用昂貴的模型做所有事情
2. **角色明確**: 規劃-執行 vs 審查-修正,各司其職

---

## 關鍵節點與控制流

![Deep Research 控制流架構](/assets/images/deep-research-control-flow.png)

傳統 Agent 是線性的 DAG（有向無環圖）：Planner 規劃任務，Executor 執行檢索，Reporter 生成報告。一路到底，沒有回頭路。

Deep Research 則是循環圖（Cyclic Graph）：在 Executor 之後，加入了 **Critic 節點**進行批判性審查。如果 Critic 發現問題（FAIL），就回到 Planner 重新規劃；只有當 Critic 確認 OK（PASS），才進入 Reporter 生成最終報告。

**Critic 節點是整個架構的靈魂。**

它不是「總結資訊」,而是扮演嚴苛的審稿人:

1. **一致性檢查**: 多個來源之間有沒有矛盾?
2. **完整性檢查**: 是否涵蓋了問題的所有面向?
3. **幻覺檢測**: 檢索結果是否真的支持我們準備生成的答案?

如果發現問題,它會給出具體的改進建議(refined queries),讓 Agent 重新規劃。

另外一個控制流設計的關鍵就是要設計斷路器: MAX_ITERATIONS = N (避免一直沒有好結果，無限循環)

---

## 為什麼強推理模型是必要條件

2023 年時，類似的循環架構嘗試大多失敗了。核心原因：**缺乏強推理模型。**

![強推理模型對比](/assets/images/strong-reasoning-models-comparison.png)

當時主流的模型（如 GPT-3.5、早期的 Gemini）在擔任 Critic 角色時，會表現出「橡皮圖章」特性——無論檢索結果多麼不相關，都傾向於「通過」，完全沒有起到審查作用。

直到 2024 年，GPT-4o、Claude 3.5 Sonnet、Gemini 2.0 Pro 等強推理模型出現，Deep Research 架構才真正變得可行。

**為什麼弱模型不行？**

因為 Critic 角色需要:
- 深層次的邏輯推理(發現矛盾)
- 批判性思考(質疑表面上合理的答案)
- 強大的 CoT(思維鏈)能力(解釋為什麼 FAIL)

只有強推理模型,才能擔任這個角色。

坦白說,這不是銀彈。用我们平常来做比喻，我们有时候在进行一些闭门的商业决策会议的时候其实是非常消耗脑力的。很多时候会放一堆糖果来让大脑补充能量，只是为了让能够让大脑能够继续大量的系统2 思考。

所以這個 Agent Model 明顯的代價：**響應時間變慢，成本顯著增加。**

每次 Critic 調用都需要使用強推理模型，而且如果平均迭代 2-3 次，整體的 token 消耗和響應時間都會是傳統單次執行的數倍。

什麼時候該用呢？人類在處理複雜事物，或是思考錯誤成本很高的時候（像是審閱文件，商業決策）， 人的大腦也是會進入系統2的慢思考。你會排除掉大量的干擾只專心在決策上，所以「複雜事物」，「錯誤代價很高」的任務就應該走這個模式。

所以決策樹很像是
- 高風險問題(法律、醫療) → Deep Research
- 一般問題 → 傳統 Plan-Execute
- 簡單問題 → 直接 RAG

用一個問題分類器在前端做判斷,只對真正需要的場景啟用 Deep Research。

---

#AIAgent #DeepResearch #LLM #ArchitecturalDesign #System2Thinking #ProductionAI
