---
layout: post
title: "微軟 Terminus-4B：用 4B 小模型當 Coding Agent 的「終端機跑腿」，砍掉 30% 算力消耗"
date: 2026-06-09 06:10:49 +0800
permalink: /microsoft-terminus-4b-small-model-subagent-routing/
description: "**作者：** Wisely Chen **日期：** 2026年6月 **系列：** AI Agent 實戰觀察 **關鍵字：** Terminus-4B, Small Language Model, Subagent Architecture, SWE-Bench, Agent Cost Optimization, Microsoft Research,"
---

**作者：** Wisely Chen
**日期：** 2026年6月
**系列：** AI Agent 實戰觀察
**關鍵字：** Terminus-4B, Small Language Model, Subagent Architecture, SWE-Bench, Agent Cost Optimization, Microsoft Research, Qwen3-4B

---

我之前寫過一篇 [AgentOpt](agentopt-expensive-model-wrong-position-pipeline-optimization.md) 的文章，核心結論是：**最貴的模型不一定要放在最重要的位置**。Columbia 大學的數據顯示，8B 小模型當 Planner、Opus 當 Executor，準確率比反過來高了一倍。

那篇是講「誰該規劃、誰該執行」的位置問題。

今天這篇微軟的 [Terminus-4B 論文](https://arxiv.org/abs/2605.03195)，則是在講另一個問題——**很多 Agent 任務裡，有大量的「髒活」根本不需要 Opus 這種等級的模型去碰**。

什麼是「髒活」？就是那些 Agent coding 過程中不斷出現的終端機操作：跑測試、看 build log、讀報錯訊息、裝套件。這些操作產生大量的 verbose 輸出（一次 build log 可能就 60KB），全部塞進主 Agent 的 context window，不只浪費 token，還會污染上下文。

微軟的方案很直覺：**用一個 4B 的小模型專門處理這些終端機任務**，主 Agent 只需要看小模型回傳的摘要。

結果呢？Frontier LLM 的 token 消耗降了 13-32%，任務成功率幾乎不變。

---

## 先看數字

### SWE-Bench Pro（主 Agent 用 Claude Opus 4.6）

| Subagent 配置 | 解題率 | 主 Agent Token | Frontier Token 變化 | 主 Agent 直接呼叫終端次數 |
|---|---|---|---|---|
| 無 Subagent（基線）| 30.0% | 836k | — | 3.8 次 |
| 用 Opus 當 Subagent | 32.0% | 729k | -10.5% | 0.5 次（-86.8%）|
| 用 Sonnet 當 Subagent | 32.6% | 756k | -7.4% | 0.6 次（-84.2%）|
| **Terminus-4B** | **31.5%** | **730k** | **-12.7%** | **1.0 次（-73.7%）** |
| Vanilla Qwen3-4B | 30.4% | 840k | +0.5% | 1.9 次（-50.0%）|

這裡面最值得注意的數字：

1. **Terminus-4B 的 token 節省（-12.7%）幾乎等於用 Opus 當 Subagent（-10.5%）**。一個 4B 模型在 token 效率上追平了自己的「老闆」。
2. **未經訓練的 Vanilla Qwen3-4B 完全沒用**——token 消耗反而微增 0.5%，因為主 Agent 不信任它，事後自己又跑了一遍。
3. 解題率幾乎不動。30.0% → 31.5%，沒有顯著退步。

### SWE-Bench C#（跨三個主 Agent）

這張表更猛，因為 Terminus-4B 訓練資料裡有大量 C# 和 TypeScript：

| Subagent | Opus 4.6 Token 變化 | Sonnet 4.5 Token 變化 | GPT-5.3-Codex Token 變化 |
|---|---|---|---|
| 無 Subagent（基線）| 1,010k | 1,496k | 1,036k |
| Opus Subagent | -29.7% | -24.8% | -26.3% |
| **Terminus-4B** | **-31.4%** | **-21.3%** | **-32.0%** |

**在 C# benchmark 上，Terminus-4B 比用 Opus 當 Subagent 還省**。GPT-5.3-Codex 那組省了 32%。

而且解題率呢？

| Subagent | Opus 4.6 解題率 | Sonnet 4.5 解題率 | GPT-5.3-Codex 解題率 |
|---|---|---|---|
| 無 Subagent | 46.7% | 47.3% | 38.0% |
| Terminus-4B | 46.7% | 46.7% | 38.0% |

**完全持平。**一個 4B 模型替你省了三成 token，解題率一點都沒掉。

---

## 為什麼能省這麼多？關鍵是 Context Window 保護

先講清楚這個 Subagent 在做什麼。

傳統的 Coding Agent 工作流程是這樣的：

```
主 Agent（Opus）
  ├── ReadFile("src/auth.ts")        → 讀進 context
  ├── Terminal("npm test")           → 跑測試，輸出 60KB build log
  │                                     全部塞進 context window
  ├── Terminal("grep -r 'error'")    → 又一堆輸出塞進來
  ├── Edit("src/auth.ts")            → 改檔案
  └── Terminal("npm test")           → 再跑一次，又 60KB
```

每一次 Terminal 操作的輸出都會進入主 Agent 的 context。一個中等複雜的 bug fix，Terminal 可能跑 3-6 次，每次輸出 20-60KB。這些 verbose 的 build log、test output 佔用了大量 token，但主 Agent 真正需要的資訊可能只有「3 個 test 失敗了，錯誤是 TypeError: Cannot read property 'id' of undefined」這一行。

加了 Subagent 之後：

```
主 Agent（Opus）
  ├── ReadFile("src/auth.ts")
  ├── Subagent("run the test suite and tell me what failed")
  │     └── Terminus-4B
  │           ├── Terminal("npm test")  → 60KB 輸出留在 Subagent context
  │           ├── Terminal("cat ...")    → 進一步查看失敗細節
  │           └── <final_answer>
  │                 "3 tests failed in auth.test.ts:
  │                  - line 42: TypeError ..."
  │                 </final_answer>     → 只有摘要回傳主 Agent
  ├── Edit("src/auth.ts")
  └── Subagent("run tests again")
        └── Terminus-4B → "All 47 tests passed."
```

**主 Agent 從來不看 build log 原文。** 它只看 Terminus-4B 消化過的摘要。

這就是為什麼 token 能省那麼多：不是任務變少了，是那些 verbose 輸出被隔離在一個 4B 模型的 context 裡，而 4B 模型的推論成本大約是 frontier 模型的三十分之一。

數據也證實了：加了 Terminus-4B 之後，主 Agent 自己直接呼叫 Terminal 的次數從 3.8 次降到 1.0 次（-73.7%）。大部分終端操作都委派出去了。

---

## Terminus-4B 怎麼訓練的？

這是這篇論文我覺得最實用的部分。因為如果你想在自己的 Agent 系統裡複製這個做法，訓練方法比架構更重要。

### 底座：Qwen3-4B-Instruct

微軟沒有從頭訓練，用的是阿里 Qwen3 系列的 4B 指令微調版。

### Phase 1：SFT（監督微調）

從 frontier 模型（Opus、Sonnet）的真實 Agent 執行記錄裡，擷取了約 3,009 條「Subagent 被呼叫 → 執行終端指令 → 回傳結果」的完整軌跡。

訓練資料的語言分佈：

| 語言 | 佔比 |
|---|---|
| TypeScript | 36.5% |
| C# | 27.8% |
| Java | 26.2% |
| JavaScript | 7.1% |
| Python | 2.3% |

有個有趣的觀察：Python 只佔 2.3%，但 Terminus-4B 在 SWE-Bench Pro（以 Python 為主）上的表現並沒有明顯退步。這說明終端機操作的核心能力——跑指令、讀 log、抓錯誤——是跨語言的。

### Phase 2：RL（強化學習）

這是 Terminus-4B 從「堪用」到「好用」的關鍵一步。用的是 GRPO（Group Relative Policy Optimization），每個 prompt 產生 8 個 rollout，然後用 LLM-as-judge 打分。

**獎勵函數設計得蠻有巧思的**，用了三個維度的分數：

**正面品質（7 項）：** 指令正確性、錯誤處理、結果準確度、關鍵資訊擷取、完整性、效率、可操作性

**失敗模式（4 項，扣分）：** 幻覺結果、遺漏錯誤、錯誤診斷、不必要的指令

**最終回答品質（3 項）：** 細節程度、事實正確、資訊量

公式：**r = (1−α)(正面分 − 失敗分) + α × 回答品質分**，α = 0.5。

另外設了硬性懲罰：
- 輸出超過 30K token → r = -100
- 沒有 `<final_answer>` tag → r = -100
- 一條指令都沒跑 → r = -50

這些硬性懲罰很重要。沒有它們，模型會學到一個捷徑：直接回答「我覺得可能是 X 的問題」而不去跑任何指令。加了 -50 的懲罰之後，模型被迫要真的動手執行。

### 訓練結果對比

SFT 之後的模型（SFT-4B）其實已經蠻能用了：

| 模型 | SWE-Bench Pro 解題率 | Token 節省 |
|---|---|---|
| Vanilla Qwen3-4B | 30.4% | +0.5%（沒用）|
| SFT-4B | 32.4% | -13.0% |
| Terminus-4B（SFT+RL）| 31.5% | -12.7% |

在 SWE-Bench Pro 上，SFT 和 RL 的差距不大。但在 C# benchmark 上就拉開了——Terminus-4B 省了 31.4% token，SFT-4B 只省了 17.5%。**RL 主要提升的是泛化能力和跨語言表現**。

---

## 「信任度」是整個系統的核心變數

論文裡有一個指標我覺得非常精彩：**Subagent→Terminal（信任度代理指標）**。

這個數字衡量的是：Subagent 完成任務後，主 Agent 有沒有「不放心」，自己又跑了一次一模一樣的終端操作來驗證。

| Subagent | 主 Agent 事後自己跑 Terminal 的次數 |
|---|---|
| Opus（最高信任）| 0.04 次 |
| Sonnet | 0.06 次 |
| Terminus-4B | 0.14 次 |
| Vanilla Qwen3-4B | 0.27 次 |

Opus 當 Subagent 時，主 Agent 幾乎從不覆核。Vanilla Qwen3-4B 時，主 Agent 經常「不放心」去驗證一次——這就抵消了 Subagent 省下的 token。

Terminus-4B 的 0.14 次已經接近 frontier 模型的水準。這是 RL 訓練的功勞——RL 教會了模型產出「讓主 Agent 信任」的回答格式和細節程度。

**這裡有一個對 Agent 系統設計很重要的洞察：省 token 不只是省在「用便宜模型」，更是省在「讓便宜模型的輸出品質好到不需要二次驗證」。** 如果你的小模型不夠可靠，主 Agent 會自己做一遍，那 Subagent 就白跑了，token 反而更多。

---

## 跟 AgentOpt 放在一起看：小模型的兩個戰場

把這篇跟 [AgentOpt 那篇](agentopt-expensive-model-wrong-position-pipeline-optimization.md) 放在一起看，一個更完整的圖景就出來了：

### AgentOpt 的發現：小模型更適合當 Planner

- 8B Ministral 當 Planner + Opus 當 Solver → 74.27%
- Opus 當 Planner + 任何 Solver → 31%
- 原因：小模型產出簡潔的 plan，不會過度展開細節

### Terminus-4B 的發現：小模型更適合當 Terminal Executor

- 4B 模型處理終端操作，省 13-32% token
- 原因：terminal 任務結構化程度高，不需要深度推理

兩個發現指向同一個結論：

> **Frontier 模型最有價值的地方，是「理解程式碼意圖」和「決定改哪裡」這種需要深度推理的環節。在那之外的所有事——規劃分解、終端操作、log 閱讀——小模型都能做得一樣好甚至更好。**

這不是說 Opus 或 GPT-5 沒用，而是說我們目前的用法太浪費。就像你請一個年薪千萬的架構師去跑 `npm test` 然後幫你讀 build log——他當然能做，但這不是他應該做的事。

---

## 實作上的啟示

### 1. 你現在就可以自己做的事

如果你在用 Claude Code 或類似的 Agent coding 工具，你可以把 Terminus-4B 的概念簡化應用：

- **在需要大量終端操作的 task 前，先把指令列好**，讓 Agent 一次跑完而不是互動式地一條一條來
- **清理 context window**：如果你知道前面的 build log 不再需要，用 `/compact` 或 summary 機制把它壓縮掉
- **分段委派**：把「跑測試然後告訴我結果」和「根據結果修改程式碼」拆成兩個步驟

### 2. Agent 框架開發者該做的事

如果你在建 Agent 系統：

- **Terminal 工具的輸出應該有摘要機制**，而不是把 raw output 全部灌進 context
- **考慮用小模型當 Terminal Executor**，現在 Qwen3-4B 的 SFT 資料微軟雖然沒開源模型權重，但論文把訓練方法寫得很清楚——3,009 條軌跡、GRPO、三維度 LLM-as-judge reward
- **加入「信任度」監控**：追蹤主 Agent 有多常在 Subagent 回答後自己又做一遍同樣的事。這個指標直接反映你的 Subagent 是否真的在省錢

### 3. 企業成本優化

對企業來說，這篇論文最大的啟示是：

**你不需要等模型降價。你需要的是把正確的模型放在正確的位置。**

一個典型的 Agent coding session 裡，真正需要 frontier 模型深度推理的可能只有 30-40% 的操作。剩下 60-70% 是讀檔案、跑測試、看 log 這些「認知簡單但 token 密集」的任務。把這些任務路由到小模型，就是純粹的成本節省。

---

## 論文的局限

誠實講幾個這篇論文的限制：

1. **只測了 Bash/Unix 環境**。沒有 PowerShell、沒有 Windows。很多企業場景跑的是 Windows 環境。
2. **SWE-Bench 都是開源 GitHub issue**，是 Docker container 裡的乾淨環境。真實世界的 production debugging 比這亂得多——你得連 VPN、讀不完整的 log、處理各種奇怪的環境差異。
3. **只測了 4B 這一個尺寸**。8B、14B、30B 的表現如何？有沒有甜蜜點？論文沒有涉及。
4. **訓練資料偏向 TypeScript/C#**，Python 只佔 2.3%。雖然在 Python benchmark 上表現還行，但這可能是因為 Qwen3-4B 底座本身 Python 能力就不差，不一定是 SFT/RL 的功勞。

---

## 我的看法

這篇論文跟 AgentOpt 一起，正在改變我對 Agent 系統架構的理解。

以前我們想的是一個「金字塔」：頂上放最強的模型，下面堆便宜的模型。

現在的圖景更像一個「工作站」：

- **Planner 位置**：反而適合小模型（AgentOpt 的發現）
- **Code Reasoning 位置**：需要 frontier 模型（深度理解 codebase、設計修改方案）
- **Execution 位置**：小模型就夠了（Terminus-4B 的發現）
- **Verification 位置**：可能也適合小模型或 rule-based 工具

Frontier 模型的最佳戰場，可能只是整個 pipeline 裡的一小段。這不是在唱衰 Opus 或 GPT-5——這些模型在那個最關鍵的推理環節是不可替代的。但是讓它們去做所有事情，就像讓外科醫師自己去搬病床、洗器械、填病歷表一樣。

微軟用一個 4B 模型證明了：**專業化分工在 AI Agent 系統裡一樣成立**。你不需要一個全能的超級模型，你需要的是把每個環節匹配到性價比最高的模型。

30% 的成本節省，不是靠等模型降價、不是靠壓縮 prompt、不是靠砍功能。是靠在正確的地方，用正確的工具。

---

## 參考資料

- Garg, S., Nitin, V., & Huang, Y. (2026). [Terminus-4B: Can a Smaller Model Replace Frontier LLMs at Agentic Execution Tasks?](https://arxiv.org/abs/2605.03195) Microsoft Research.
- 相關閱讀：[AgentOpt 論文：Opus 太聰明，所以它不該做 Planning](agentopt-expensive-model-wrong-position-pipeline-optimization.md)
- 相關閱讀：[On-Prem 小模型爆發時代來了](on-prem-small-model-explosion-2026-shift.md)

---

## 常見問題 Q&A

**Q: Terminus-4B 有開源嗎？**

截至論文發表時，微軟沒有開源模型權重。但論文把訓練方法（SFT 資料來源、RL 獎勵函數、超參數）寫得非常詳細，用 Qwen3-4B 底座自己復現是可行的。

**Q: 我用 Claude Code，能直接用這個方法嗎？**

Claude Code 目前的 Subagent 機制是用 Sonnet 或 Haiku，不支援自訂小模型。但概念上你可以透過減少不必要的 Terminal 互動、善用 compact 機制來達到類似效果。如果你自建 Agent 系統，這篇論文的架構可以直接參考。

**Q: 為什麼不用更大的小模型，比如 8B 或 14B？**

論文沒測其他尺寸。但從成本角度看，4B 的推論成本大約是 frontier 的三十分之一，而且能跑在消費級 GPU 上。8B 或 14B 可能表現更好，但邊際成本也更高。4B 似乎是「效能夠用、成本最低」的甜蜜點。

**Q: 這跟 MoE（Mixture of Experts）有什麼不同？**

MoE 是模型內部的路由機制——一個模型裡面有多個專家，每次只啟動一部分。Terminus-4B 是系統層級的路由——多個獨立模型之間分工。兩者可以疊加使用，不衝突。
