---
layout: post
title: "「Opus 太聰明，所以它不該做 Planning」——一篇論文顛覆 Agent Ops 範式"
date: 2026-04-13 08:00:00 +0800
permalink: /agentopt-expensive-model-wrong-position-pipeline-optimization/
image: /assets/images/agentopt-paper-cover.png
description: "Columbia 大學 AgentOpt 論文用 9 個模型、81 種組合實驗證明：Ministral 8B 做 Planner + Opus 做 Solver 準確率 74.27%，完勝 Opus 做 Planner 的 31.71%。最貴的模型放在 Planner 位置反而最差——因為它太強，強到跳過工具使用直接裸答。Anthropic 自己推出的 Advisor Tool 也在修正這個方向：讓便宜模型跑主迴圈，Opus 退居顧問按需出場。Agent 管線優化的單位不是單一模型能力，而是模型組合在特定任務上的匹配度。"
---

![AgentOpt 論文：Client-Side Optimization for LLM-Based Agent](/assets/images/agentopt-paper-cover.png)

我之前一直跟大家推薦：用 Opus 當 Planner，然後讓 Sonnet 或 Haiku 當 Executor。這套邏輯聽起來很合理對吧？最強的腦袋負責規劃，便宜的手腳負責執行，分工明確、成本可控。

我自己也一直這樣用，還寫了好幾篇文章推廣這個做法。

然後我看到了 Columbia 大學 DAPLab 的 [AgentOpt 論文](https://arxiv.org/abs/2604.06296)。

**我被打臉了。徹徹底底地被打臉了。**

論文裡有一組數字：同一個任務、同一個 Agent 管線架構，只是「誰做 Planner、誰做 Solver」調換了一下——

- **Ministral 8B（Planner）+ Opus（Solver）：74.27%**
- **Opus（Planner）+ 任何模型（Solver）：31.71%**

準確率差了 42 個百分點。而且贏的那組，Planner 用的是市面上最便宜的模型之一——Opus 價格的三十三分之一。

9 個模型、81 種組合的大規模實驗，結果顛覆了一個我一直深信不疑的假設：

> **「最強的模型放在最重要的位置，就會得到最好的結果。」**

不一定。有時候恰好相反。而且不是小幅度的差異，是翻倍的差距。

---

## 先看最反直覺的結果

AgentOpt 團隊在 HotpotQA（多跳問答）基準上，測試了 9 個模型的所有兩兩組合——一個當 Planner（負責分解問題），一個當 Solver（負責用搜尋工具找答案）。

結果排名最前和最後的：

| 組合 | 準確率 |
|------|--------|
| **Ministral 8B（Planner）+ Claude Opus 4.6（Solver）** | **74.27%** |
| Claude Opus 4.6（Planner）+ 任何 Solver | **31-32%**（倒數 11 名全是 Opus 當 Planner） |

Ministral 8B 是什麼？是 Mistral AI 的 8B 參數端側小模型，定價 $0.15/百萬 token——差不多是 Opus 的 **三十三分之一**。

但它當 Planner 的效果，比 Opus 當 Planner 好了一倍以上。

---

## 為什麼最強模型反而最差？

論文團隊分析了執行日誌，發現了原因——

**Opus 太強了，強到不願意委派任務。**

在 9 種 Opus 當 Planner 的組合中，有 7 種出現了 `role2_never_called`——Solver 從頭到尾沒有被呼叫過。Opus 看到多跳問題後，直接自己回答了，完全跳過了搜尋工具。

問題是，這個任務的設計就是需要搜尋外部資料才能準確回答的。Opus 自信地「裸答」，結果自然慘烈。

反觀 Ministral 8B：它知道自己回答不了這種複雜問題，所以老老實實地把問題分解、交給 Solver 去用搜尋工具查。這恰好是 Planner 該做的事。

**弱模型的「無能」，反而成了架構上的優勢。**

這讓我想到一個在企業裡常見的管理悖論：最有能力的人被放到管理位置後，反而因為「什麼都自己來」而讓團隊失效。好的管理者不是最強的執行者，而是最懂得委派的人。

---

## 這不是個案：跨基準的系統性發現

AgentOpt 不只測了 HotpotQA。他們在四個基準上跑了完整實驗：

### 1. HotpotQA（多跳問答）——Planner + Solver 架構

最佳組合：Ministral 8B + Opus = **74.27%**
最差集群：Opus + 任何 = **~31%**

**結論：** Planner 的角色需要的不是「聰明」，而是「守規矩」。

### 2. MathQA（數學推理）——Answerer + Critic 架構

最佳組合：Opus（Answerer）+ Haiku 4.5（Critic）= **98.84%**

有意思的發現：一旦 Answerer 夠強（用 Opus），**Critic 用什麼模型幾乎沒差**——9 個 Critic 的準確率差距只有 2.9 個百分點。

**結論：** 不是每個角色都值得花大錢。有些角色的影響力天生就低。

### 3. GPQA Diamond（研究生等級科學問答）——單模型

唯一一個「用最強模型就對了」的基準。Opus 單獨跑拿到 74.75%。

**結論：** 如果任務不涉及工具使用和角色分工，模型能力排名確實能預測表現。

### 4. BFCL v3（多輪函數呼叫）——單模型

三個模型並列 70%（Opus、Qwen3 Next、另一個），但成本差 **32 倍**。

**結論：** 同分時，選便宜的就對了。

---

## 「直接用最好的模型」到底多浪費？

論文給了一組成本對比數據：

| 基準 | 高成本組合 | 平價組合（準確率相近） | 成本差距 |
|------|-----------|---------------------|---------|
| HotpotQA | Opus + Opus (~73%) | Qwen3 Next + gpt-oss-120b (71.3%) | **21 倍** |
| MathQA | Opus + Opus (~98.5%) | Ministral + Claude 3 Haiku (94.0%) | **118 倍** |
| BFCL | Opus (72%) | Qwen3 Next (71%) | **32 倍** |

**在準確率相近的情況下，最佳和最差的模型組合，成本差距可以到 13-32 倍。**

這對任何跑 Agent 管線的團隊來說都是真金白銀。如果你每天跑幾千次 Agent pipeline，選錯組合一個月就是幾萬美金的浪費。

---

## 為什麼你不能靠直覺選模型組合？

論文測試了 8 種搜索演算法來找最佳組合，其中一個叫 **LM Proposal**——讓 GPT-4.1 這種強模型來「推薦」最佳組合。

結果呢？

- GPQA（直覺有效）：表現不錯
- **HotpotQA（直覺失效）：只有 34%**
- **BFCL：只有 45%**

連最強的語言模型都無法預測哪個組合最好。因為 pipeline 中的角色交互是非線性的——你不能從「A 模型在 benchmark X 上表現好」推導出「A 模型在 pipeline 角色 Y 上表現好」。

另一個有趣的失敗是 **Hill Climbing**（爬山法）：在 HotpotQA 上只有 **52% 的機率找到最佳組合**。為什麼？因為最佳組合（Ministral 8B + Opus）跟它的「鄰居」組合表現完全不同——從任何相鄰的組合出發，局部搜索都走不到全局最優。

**贏家是 Arm Elimination（臂消除法）**，一種基於信賴區間的逐輪淘汰策略，能在保持接近暴力搜索準確率的同時，節省 40-60% 的搜索預算。

---

## Anthropic 自己也在修正這個思路

讀到這裡，你可能跟我一樣想到了 Anthropic 自己的 Claude Code 架構。

我在之前寫的 [Anthropic 官方解密：為什麼 Claude Code 這麼好用？](https://ai-coding.wiselychen.com/anthropic-dual-agent-architecture-claude-code/) 那篇分析過，Claude Code 用的就是雙 Agent 架構——Initializer Agent 負責規劃任務清單，Coding Agent 負責逐步實作。在 `opusplan` 模式下，更是明確地用 Opus 做規劃、Sonnet 做執行。

**但就在 AgentOpt 論文發表前後，Anthropic 自己推出了一個新東西：[Advisor Tool](https://www.inside.com.tw/article/41043-anthropic-claude-advisor-tool-opus-executor-agent-cost)。**

這個設計完全翻轉了 Opus 的角色定位——

過去的做法：**Opus 當主腦（Planner），便宜模型當手腳（Executor）**
Advisor Tool 的做法：**便宜模型（Haiku / Sonnet）跑主迴圈當執行者，Opus 退居幕後當「顧問」，只在關鍵時刻被呼叫出場**

具體來說：
- 執行者模型（Haiku 4.5 或 Sonnet 4.6）負責整個任務的主迴圈，逐步推進
- 當執行者判斷「這一步我搞不定」時，透過 API 呼叫 Opus 4.6 作為 Advisor
- Opus 讀取完整對話紀錄，回傳策略建議（通常 400-700 個 token）
- 執行者拿到建議後繼續跑，Opus 不接管控制權

根據外媒 TestingCatalog 的測試，**Haiku 搭配 Opus 顧問的表現，大幅超過 Haiku 單獨運行，而總成本仍低於直接用 Sonnet。**

這代表什麼？Anthropic 自己也意識到了 AgentOpt 論文指出的問題：

1. **Opus 不應該永遠坐在 Planner 的位置上。** 讓它一直掌控全局，反而可能像 HotpotQA 實驗一樣「搶活幹」
2. **按需呼叫比全程使用更有效。** Advisor Tool 的 `max_uses` 參數可以限制 Opus 被呼叫的次數——你可以設定「整個任務最多問顧問 3 次」
3. **執行者判斷「何時需要顧問」才是關鍵。** 這跟 AgentOpt 的發現完全吻合：pipeline 的效能不取決於單一角色的模型強度，而是角色之間的互動方式

有趣的是，Advisor Tool 還有一個容錯設計：如果顧問呼叫失敗，執行者不會中止，而是繼續完成任務。這等於承認了一件事——**很多時候，執行者其實不需要顧問也能搞定。**

---

AgentOpt 的研究加上 Anthropic 自己的 Advisor Tool，指向同一個結論：**最佳的模型分工取決於具體任務類型，而不是「最強的放最前面」。**

- **需要工具使用的任務**（像 HotpotQA）：弱模型當 Planner 可能更好，因為它不會「搶活幹」
- **純推理任務**（像 GPQA）：強模型獨挑就行
- **需要批判審查的任務**（像 MathQA）：Critic 角色的模型選擇影響不大
- **多步驟長程任務**（像 SWE-bench）：便宜模型跑主迴圈 + 強模型按需諮詢，可能是最佳平衡

未來的 Agent 框架，不應該硬編碼「某個角色永遠用某個模型」，而是應該根據任務動態分配——甚至讓模型自己決定「什麼時候該叫顧問」。

---

## 實戰啟示：你現在可以做什麼？

### 1. 審計你的 Agent 管線成本

如果你正在跑 multi-agent pipeline，花 30 分鐘列一下：

- 每個角色用的是什麼模型？
- 每個角色每月消耗多少 token？
- 有沒有角色其實換成便宜模型也不影響結果？

MathQA 的案例告訴我們：Critic 角色的模型選擇幾乎不影響最終準確率。你的 pipeline 裡可能也有這種「假高價值」角色。

### 2. 警惕「能力過剩」的陷阱

Opus 在 HotpotQA 的失敗不是因為它不夠好，而是因為它太好——好到跳過了架構設計的關鍵步驟。

在你的 pipeline 裡，檢查一下：**有沒有哪個角色的模型「太聰明」，聰明到繞過了它該遵守的流程？**

這在 AI Agent 和人類組織裡都是同樣的問題。

### 3. 用系統化方法找最佳組合

AgentOpt 是[開源的](https://agentoptimizer.github.io/agentopt/)，支援 LangGraph、AutoGen、CrewAI 等主流框架。核心 API 很簡單：

```python
selector = ArmEliminationModelSelector(
    agent=MyAgent,
    models={"planner": [...], "solver": [...]},
    eval_fn=eval_fn,
    dataset=dataset,
    model_prices=model_prices,
)
results = selector.select_best(parallel=True)
```

它的原理是在 HTTP 層攔截 LLM API 呼叫，用快取避免重複計算，然後用 Arm Elimination 演算法逐步淘汰差的組合。如果你的 pipeline 有 3 個以上角色，暴力搜索的成本會指數增長——這時候這類工具就很有價值。

### 4. 別相信直覺，包括 AI 的直覺

論文最殘酷的結論之一：**讓 LLM 自己推薦模型組合，效果跟隨機差不多。** GPT-4.1 在 HotpotQA 上推薦的組合只有 34% 準確率——比 Ministral 8B + Opus 的 74.27% 差了一倍。

如果連 frontier model 都猜不準，你和我靠直覺選就更不靠譜了。

---

## 一句話總結

> **Agent 管線優化的單位不是「單一模型的能力」，而是「模型組合在特定任務上的匹配度」。** 用錯組合，你可能花 32 倍的錢，拿到一半的效果。

這篇論文讓我重新思考了一件事：我們在建 Agent 系統時，花了大量時間在 prompt engineering、工具設計、記憶管理上——但可能從來沒認真想過「這個角色真的需要用這個模型嗎？」

也許，這才是最容易被忽略、但投資報酬率最高的優化槓桿。

---

## 參考資料

- **AgentOpt 論文：** [AgentOpt v0.1 Technical Report: Client-Side Optimization for LLM-Based Agent](https://arxiv.org/abs/2604.06296)
- **專案主頁：** [AgentOpt GitHub](https://agentoptimizer.github.io/agentopt/)
- **DAPLab Blog：** [Why Your Agent Needs a Model Combo Optimizer, Not Just a Model](https://daplab.cs.columbia.edu/general/2026/03/22/why-your-agent-needs-a-model-combo-optimizer.html)
- **Anthropic Advisor Tool：** [Anthropic 讓 Opus 變「顧問」：AI 代理人新架構](https://www.inside.com.tw/article/41043-anthropic-claude-advisor-tool-opus-executor-agent-cost)
- **延伸閱讀：** [Anthropic 官方解密：為什麼 Claude Code 這麼好用？](https://ai-coding.wiselychen.com/anthropic-dual-agent-architecture-claude-code/)

---

## 常見問題 Q&A

**Q: 這個研究是不是說小模型永遠比大模型適合當 Planner？**

不是。在 GPQA（純科學問答）上，Opus 獨挑就是最佳選擇。AgentOpt 的結論是「沒有普適的最佳組合」——你必須針對你的具體任務去測。Ministral 8B 當 Planner 之所以在 HotpotQA 上贏，是因為那個任務需要 Planner 乖乖分解問題而不是搶答。換一個任務，結果可能完全不同。

**Q: 我只有 2 個角色的 pipeline，值得用 AgentOpt 嗎？**

如果你有 9 個候選模型 × 2 個角色 = 81 種組合，暴力搜索的成本在 $50-120 之間（取決於任務複雜度）。Arm Elimination 可以把這個降到 $30-70。如果你的 pipeline 每月 API 成本超過 $500，花一次搜索費用找到最佳組合是值得的。

**Q: 這跟 LLM Router（如 RouteLLM）有什麼不同？**

LLM Router 是針對單個查詢做路由——「這個問題該給 Opus 還是 Haiku？」AgentOpt 是針對整個 pipeline 做組合優化——「Planner 用什麼、Solver 用什麼、Critic 用什麼的組合最好？」這是不同層次的問題。Router 可以幫你省單次呼叫的錢，AgentOpt 幫你省整條管線的錢。
