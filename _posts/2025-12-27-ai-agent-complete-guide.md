---
layout: post
title: "AI Agent 完整指南｜架構、Workflow、安全與企業落地"
date: 2025-12-27 12:00:00 +0800
permalink: /ai-agent/
image: /assets/images/ai-agent-guide-cover.png
description: "AI Agent 不是「比較聰明的 Chatbot」，而是能自主執行任務的系統。本指南涵蓋 AI Agent 架構（Workflow vs ReAct、Plan & Execute、Dual-Agent）、企業 AI Agent 落地、AI Agent 安全（94.4% 攻擊成功率）等核心主題。"
keywords: "AI Agent, AI Agent 架構, 企業 AI Agent, AI Agent 安全, Workflow, ReAct, Plan Execute, Dual-Agent, LATS, Multi-Agent"
---

**如果你正在思考：**

- Chatbot 為什麼一落地就失控
- Agent 架構該怎麼設計才不會炸
- 為什麼資安、審計、責任鏈突然變得重要

這一頁是給你的。

---

## 目錄

- [什麼是 AI Agent？](#什麼是-ai-agent)
- [AI Agent 架構模式總覽](#ai-agent-架構模式總覽)
- [AI Agent 執行與決策機制](#ai-agent-執行與決策機制)
- [AI Agent 記憶與長期學習](#ai-agent-記憶與長期學習)
- [企業 AI Agent 安全與風險](#企業-ai-agent-安全與風險)
- [企業 AI Agent 落地實戰案例](#企業-ai-agent-落地實戰案例)
- [AI Agent 系列文章索引](#ai-agent-系列文章索引)

---

## 什麼是 AI Agent？

![AI Agent vs Chatbot](/assets/images/ai-agent-vs-chatbot-comparison.png)

AI Agent 和 Chatbot 是完全不同的物種。

**Chatbot**：只能「說話」，沒有執行權限。最壞情況是回答錯誤（如[加航案例](https://canlii.ca/t/k3d4k)的 800 加幣賠償）。

**AI Agent**：能「動手做事」，有資料庫存取、API 呼叫、雲端操作權限。攻擊目標從「騙它說錯話」變成「騙它做錯事」。

我認為真正的 Agent 需要滿足三個條件：

![構成真正 Agent 的三個基石](/assets/images/ai-agent-three-pillars.png)

1. **知識庫提取能力**
2. **工具調用能力**
3. **一定的容錯或除錯能力**

因為只要 Agent 需要調用外部工具，就會有一萬種理由失敗。這時候除錯能力的高低就會嚴重影響 Agent 的 robustness。

> 詳細定義與案例請見：[什麼是 AI Agent？企業 AI 導入的真實觀察](/xiaolaoban-part2-ai-agent-definition/)

---

## AI Agent 架構模式總覽

### Workflow vs ReAct：兩種基本思維

![Workflow vs ReAct](/assets/images/workflow-vs-react-comparison.png)


**Workflow** 的假設是「我能預測所有情況」，但現實世界不是預定好的。

**[ReAct](https://arxiv.org/abs/2210.03629)** 的優點是對環境感知極強，適合知識問答和高密度交互場景。缺點是每步都需要 LLM 推理，速度慢、token 容易爆炸、容易陷入局部最優解。

> 完整比較：[[Agent Part 1] Workflow 型和 ReAct 型，誰更像你？](/agent-mo-shi-part-1-workflow-xing-he-react-xing-shui-geng-xiang-ni/)

### Plan & Execute：讀著路書跑

![Plan & Execute](/assets/images/plan-execute-architecture.png)

如果 ReAct 是「摸著石頭過河」，[Plan & Execute](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/#planning) 就是「先畫好地圖再出發」。

核心思想：
1. **Planner**：根據目標規劃完整步驟
2. **Executor**：按計劃執行各步驟
3. **Re-planning**：遇到問題時重新規劃

這種模式的優勢是有明確方向性，不容易走到局部最優解。

> 詳細解析：[[Agent Part 2] Plan & Exec 臨機應變 vs 讀著路書跑](/mang-mu-jia-su-vs-du-zhu-lu-shu-pao-wei-shi-mo-ai-agent-xu-yao-plan-exec-mo-shi/)

### Dual-Agent 架構：Claude Code 的秘密

![Dual-Agent Architecture](/assets/images/dual-agent-architecture-logo.png)

[Anthropic 官方](https://www.anthropic.com/engineering/claude-code-best-practices)揭露了 Claude Code 為什麼這麼好用的內部架構——Dual-Agent 設計：

- **Outer Agent**：處理用戶對話、維持上下文
- **Inner Agent**：專注執行具體任務

這種分離讓系統在「自主性」和「人類對齊」之間找到平衡。

> 架構詳解：[[Agent Part 5] Anthropic 官方解密為什麼 Claude Code 這麼好用的內部工程架構](/anthropic-dual-agent-architecture/)

### Multi-Agent 協作：當 AI 學會「會診」

![Multi-Agent 協作](/assets/images/multi-agent-collaboration.png)

單一 Agent 有其極限。[Multi-Agent 系統](https://langchain-ai.github.io/langgraph/concepts/multi_agent/)讓多個專業 Agent 協作：

- **Supervisor 模式**：一個 Agent 指揮調度其他 Agent
- **Peer 協作模式**：Agent 之間平等協商

但要注意：根據研究，**100% 的 Agent 在多 Agent 互信場景下被成功攻破**。信任鏈是最大風險。

> 協作模式分析：[Multi-Agent 協作模式：當 AI 學會「會診」這件事](/multi-agent-xie-zuo-mo-shi-dang-ai-xue-hui-hui-zhen-zhe-jian-shi/)

---

## AI Agent 執行與決策機制

### Interleaved Thinking：穩定性的關鍵

Agent 落地最大的挑戰是「穩定性」。[Interleaved Thinking](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking#interleaved-thinking-with-tool-use) 讓 Agent 在執行過程中持續思考和調整，而不是一次性規劃完畢。

這是現在 Agent 能夠真正落地的重要關鍵。

> 深入分析：[[Agent Part 3] Interleaved Thinking 呈現的穩定性是現在 Agent 落地的重要關鍵](/agent-part-3-interleaved-thinking-cheng-xian-de-wen-ding-xing-shi-xian-zai-agentluo-di-de-zhong-yao-guan-jian/)

### Plan, Exec, Critic：System 2 思維

![Plan Exec Critic](/assets/images/plan-exec-critic-system2.png)

加入 Critic 角色讓 Agent 具備「自我反思」能力：

1. **Plan**：規劃行動
2. **Execute**：執行任務
3. **Critic**：評估結果、提出改進

這是用 [System 2（慢思考）](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/#reflection)來突破瓶頸。

> 思維模式詳解：[[Agent Part 4] Plan, Exec, Critic 我們如何用 System 2 思維突破瓶頸](/deep-research-linkedin-draft/)

### LATS：讓 Agent 學會「三思而後行」

![LATS Tree Search](/assets/images/lats-decision-brain.png)

[LATS（Language Agent Tree Search）](https://arxiv.org/abs/2310.04406)是終極決策大腦，結合了：

- **蒙地卡羅樹搜索**：探索多種可能路徑
- **自我反思**：從失敗中學習
- **回溯能力**：發現錯誤時退回重來

這讓 Agent 不再是「一條路走到黑」，而是能夠評估多種方案後選擇最優解。

> 完整解析：[[Agent Part 7] LATS 詳解：讓 AI Agent 學會「三思而後行」的終極決策大腦](/lats-agent-tree-search-decision-brain/)

### Storm：駕馭整個編輯團隊

![Storm AI Agent](/assets/images/storm-ai-agent-diagram-20251207.png)

[Storm](https://github.com/stanford-oval/storm) 是 Stanford 開源的 Multi-Agent 系統，用於長文寫作。它的架構是真正的「編輯團隊」：

- **主編 Agent**：統籌全局
- **研究員 Agent**：蒐集資料
- **寫手 Agent**：撰寫內容
- **審稿 Agent**：品質把關

> 實戰應用：[[Agent Part 6] Storm：駕馭整個文章編輯團隊](/storm-ai-agent-as-expert-editor-team/)

---

## AI Agent 記憶與長期學習

### Nested Learning：告別「金魚腦」AI

![Nested Learning](/assets/images/nested-learning-brain-memory.png)

2025 年 [Google 發表的 Nested Learning](https://arxiv.org/abs/2506.08071)，讓模型擁有大腦般的長期記憶：

- **短期工作記憶**：當前任務的上下文
- **長期語義記憶**：跨任務的知識累積
- **情節記憶**：過去經驗的回憶

這解決了 Agent 每次對話都「失憶」的問題。

> 技術解析：[[Agent Part 8] 告別「金魚腦」AI？Google 重磅發表 Nested Learning](/nested-learning-ai-memory/)

---

## 企業 AI Agent 安全與風險

![AI Agent Security](/assets/images/ai-agent-security-threat.png)

### 為什麼 Agent 比 Chatbot 危險 100 倍？

根據 [2025 年學術研究](https://arxiv.org/abs/2406.12784)：

> **94.4% 的 SOTA LLM Agent 容易受到 Prompt Injection 攻擊**
>
> **100% 的 Agent 在多 Agent 互信場景下被成功攻破**

真實案例：
- **Salesforce ForcedLeak**：填表單就能偷走整個客戶名單
- **Microsoft 365 Copilot EchoLeak**：零點擊外洩

傳統 WAF/APM 完全失效，因為它們看不懂自然語言，無法判斷 Prompt 的惡意意圖。

> 完整分析：[AI Agent Security：為什麼它正在改變企業資安架構](/ai-agent-security-game-changed/)

### 防禦架構建議

企業級 Agent 需要：

1. **Auth Gateway**：統一權限控管
2. **Python 沙盒**：安全執行環境
3. **LLM Router**：智慧路由
4. **雙層 Log**：完整審計軌跡

> 實作指南：[企業級地端 LLM 系統架構藍圖](/local-llm-enterprise-architecture/)

---

## 企業 AI Agent 落地實戰案例

![企業 AI Agent 落地](/assets/images/xiaolaoban-part2-ai-agent-cover.png)

### AI Agent 能不能落地？看人

技術從來不是最大的障礙。Agent 能不能落地，關鍵在於（[小老闆充電站訪談](https://www.youtube.com/watch?v=bIn2NKCY4SE)）：

1. **有沒有人願意負責**
2. **流程有沒有配合調整**
3. **期望值是否合理**

> 實戰觀察：[什麼是 AI Agent？企業 AI 導入的真實觀察](/xiaolaoban-part2-ai-agent-definition/)

### 推薦信 Agent：10 分鐘完成 10 封信

這是一個真實案例：用 Agent 在 10 分鐘內完成 10 個學校的推薦函。

不是炫技，而是證明 Agent 在「重複但需要客製化」的任務上有真正價值。

> 實戰案例：[10 分鐘完成 10 個學校推薦函：推薦信 AI Agent 實戰](/shi-fen-zhong-wan-cheng-shi-ge-xue-xiao-tui-jian-han-ai-agent-shi-zhan)

---

## AI Agent 系列文章索引

### Agent 架構系列

- **Part 1** [Workflow 型和 ReAct 型，誰更像你？](/agent-mo-shi-part-1-workflow-xing-he-react-xing-shui-geng-xiang-ni/) — 基礎架構比較
- **Part 2** [Plan & Exec 臨機應變 vs 讀著路書跑](/mang-mu-jia-su-vs-du-zhu-lu-shu-pao-wei-shi-mo-ai-agent-xu-yao-plan-exec-mo-shi/) — 執行模式選擇
- **Part 3** [Interleaved Thinking 呈現的穩定性](/agent-part-3-interleaved-thinking-cheng-xian-de-wen-ding-xing-shi-xian-zai-agentluo-di-de-zhong-yao-guan-jian/) — 落地穩定性
- **Part 4** [Plan, Exec, Critic：System 2 思維](/deep-research-linkedin-draft/) — 自我反思機制
- **Part 5** [Anthropic Dual-Agent 架構](/anthropic-dual-agent-architecture/) — Claude Code 內部設計
- **Part 6** [Storm：駕馭整個文章編輯團隊](/storm-ai-agent-as-expert-editor-team/) — Multi-Agent 寫作
- **Part 7** [LATS：三思而後行的決策大腦](/lats-agent-tree-search-decision-brain/) — 樹搜索決策
- **Part 8** [Nested Learning：長期記憶](/nested-learning-ai-memory/) — Agent 記憶系統

### Agent 安全與企業落地

- **企業安全** [AI Agent Security](/ai-agent-security-game-changed/) — 94.4% 攻擊成功率
- **架構藍圖** [地端 LLM 架構](/local-llm-enterprise-architecture/) — Auth + 沙盒 + 雙層 Log
- **企業定義** [什麼是 AI Agent？](/xiaolaoban-part2-ai-agent-definition/) — 企業導入觀察
- **協作模式** [Multi-Agent 協作](/multi-agent-xie-zuo-mo-shi-dang-ai-xue-hui-hui-zhen-zhe-jian-shi/) — 會診機制

### 實戰案例

- **推薦信** [10 分鐘完成 10 封信](/shi-fen-zhong-wan-cheng-shi-ge-xue-xiao-tui-jian-han-ai-agent-shi-zhan) — 效率提升
- **系統管理** [Claude Code 做 Linux 管理](/ai-ops-yong-agent-claude-code-zuo-linux-xi-tong-guan-li-you-mei-you-gao-tou-xiang-de-hen/) — AI Ops 實戰

---

## 常見問題 FAQ

**Q: AI Agent 跟 Chatbot 差在哪？**

Chatbot 只能「說話」，最壞情況是回答錯誤。Agent 能「動手做事」，有資料庫存取、API 呼叫權限，攻擊目標從「騙它說錯話」變成「騙它做錯事」。風險等級完全不同。

**Q: 企業什麼時候「不該」用 Agent？**

當你沒有人願意負責、流程沒有配合調整、或期望值不合理時。技術從來不是最大障礙，人和流程才是。如果連基本的 SOP 都沒有，先別急著上 Agent。

**Q: Agent 一定要上 Multi-Agent 嗎？**

不一定。單一 Agent 配合 Plan & Execute 模式，在大部分場景已經夠用。Multi-Agent 適合需要「不同專業角色協作」的複雜任務，但架構複雜度和除錯難度會大幅提升。

**Q: AI Agent 最大的安全風險是什麼？**

Prompt Injection。研究顯示攻擊成功率高達 94.4%，而傳統 WAF/APM 完全失效，因為它們看不懂自然語言。企業需要專門的 Agent 安全架構：Auth Gateway、沙盒執行、LLM Router。

**Q: Agent 為什麼需要審計 log？**

因為 Agent 的決策過程是黑箱。當出事時，你需要知道「它為什麼這樣做」。雙層 Log（應用層 + LLM 層）是企業級 Agent 的基本要求，也是合規審計的必要條件。

**Q: Workflow 和 ReAct 該選哪個？**

看你的場景。Workflow 適合「可預測的標準流程」，速度快、成本低。ReAct 適合「需要環境感知的複雜任務」，但 token 消耗高、容易陷入局部最優。實務上常混用：外層 Workflow 控制流程，內層 ReAct 處理不確定性。

---

## 一句話總結

AI Agent 已經不是 AI 的子題，而是一個獨立的技術領域。

它結合了：
- **架構設計**：Workflow、ReAct、Plan & Execute
- **決策系統**：LATS、Critic、樹搜索
- **記憶機制**：Nested Learning
- **安全防禦**：Auth Gateway、沙盒、審計

> 這不是理論探討，而是我們在真實戰場試錯過的經驗。數據和邏輯都在這裡，你可以拿去改進。

---

**關於作者：**

Wisely Chen，NeuroBrain Dynamics Inc. 研發長，20+ 年 IT 產業經驗。曾任 Google 雲端顧問、永聯物流 VP of Data&AI、艾立運能數據長。專注於企業 AI 轉型與 Agent 導入的實戰經驗分享。

---

**🔗 相關連結：**
- [部落格首頁](https://ai-coding.wiselychen.com)
- [LinkedIn](https://www.linkedin.com/in/wisely-chen-38033a5b/)
