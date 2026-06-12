---
layout: post
title: "Fable 5 把 Harness 吃進去了 — SWE-bench 95% 的背後，是模型學會了自己調度 Agent"
date: 2026-06-12 09:00:00 +0800
permalink: /fable-5-harness-internalization-orchestrator-model-routing/
description: "Fable 5 的正確打開方式不是拿來聊天，是讓它跑 Workflow、自己挑模型。Fable 5 當 Orchestrator 調度 Haiku 做搜尋分類，省 74% Token 費。Stripe 用它一天遷移 5,000 萬行 Ruby。Simon Willison 一天花 $110。Anthropic 自己建議的四層模型調度架構，把 Harness Engineering 推到下一站：模型不只被 Harness 包住，模型自己變成了 Harness。"
author: Wisely Chen
categories: [AI Coding, Harness Engineering]
image: /assets/images/fable5-maxlv-tweet-workflow.png
---

![Max Lv 推文：Fable 5 的正確打開方式是 run a workflow，choose agent's model wisely](/assets/images/fable5-maxlv-tweet-workflow.png)

Fable 5 到底強在哪？

網路上已經炸了。有人讓它一次做出完整的短影片，有人用它打通寶可夢火紅版，Django 共同創造者 Simon Willison 一天之內讓它連修四個底層 library 的 bug，Mozilla 用它的前身在 Firefox 150 裡抓出 271 個 bug——是之前用 Opus 4.6 的十倍。Stripe 更誇張，5,000 萬行 Ruby 遷移，一天搞定，之前預估要兩個月。

但如果你只看這些 demo，你會得出一個錯誤結論：Fable 5 就是「更強的 Opus」。不是。GPQA Diamond 它還輸 Gemini 3.1 Pro。它強在 **調度**：自己拆任務、自己決定哪些子任務丟給便宜模型、自己寫 workflow 腳本讓 runtime 執行。

Anthropic 6 月 9 日發布的 Mythos 級模型，定位在 Opus 之上，目前公開最強的 Claude。先看數字：

| 指標 | Fable 5 | Opus 4.8 | GPT-5.5 | Gemini 3.1 Pro |
|------|---------|----------|---------|----------------|
| SWE-bench Verified | **95.0%** | 88.6% | 82.6% | — |
| SWE-bench Pro | **80.3%** | 69.2% | 58.6% | 54.2% |
| FrontierCode (Cognition) | **29.3%** | — | 5.7% | — |
| GPQA Diamond | 91.3% | — | 92.8% | **94.3%** |
| 幻覺率 (AA-Omniscience) | **36.2%** | — | 85.5% | 49.9% |

**任務越長越複雜，Fable 5 的領先越大。** SWE-bench Pro（跨多個檔案的修改）領先 Opus 4.8 十一個百分點，領先 GPT-5.5 二十二個百分點。FrontierCode 更誇張——29.3% vs 5.7%，差了五倍。但在簡單的知識問答（GPQA Diamond），Gemini 3.1 Pro 反而贏了。

**Fable 5 不是「更聰明的聊天機器人」，它是為長程 agent 任務設計的。** 定價也反映了這個定位：$10/$50 MTok，是 Opus 4.8 的兩倍。

---

## Anthropic 自己建議的四層調度架構

Anthropic 在 [Fable 5 Prompting Guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5) 裡明確建議了一個多模型調度架構：

| 角色 | 模型 | 定價 (MTok) | 職責 |
|------|------|-------------|------|
| **Orchestrator** | Fable 5 | $10 / $50 | 任務分解、調度、結果合成 |
| **Escalation** | Opus 4.8 | $5 / $25 | 複雜子任務、安全域處理 |
| **Implementation** | Sonnet 4.6 | $3 / $15 | 程式修改、測試、多檔案變更 |
| **Discovery** | Haiku 4.5 | $1 / $5 | 搜尋、分類、摘要 |

核心原則是 [Developers Digest](https://www.developersdigest.tech/blog/fable-5-orchestrator-model-playbook) 總結的這句話：

> "You pay the frontier rate where errors compound and the commodity rate where they do not."

翻譯：**Orchestrator 的錯誤會向下游放大，所以用最貴的。Worker 的失敗是孤立的、可以重試的，所以用最便宜的。**

成本差異有多大？用一個 12 個 worker 的程式碼審計做例子：

| 配置 | 總成本 | 省多少 |
|------|--------|--------|
| 全部用 Fable 5 | $14.50 | 基準 |
| Fable 5 orchestrator + Haiku workers | **$3.70** | **省 74%** |
| 全部用 Sonnet（不用 Fable） | $4.35 | 省 70% |

注意：把 Orchestrator 從 Fable 降到 Sonnet 只省 $1.75。把 Workers 從 Fable 降到 Haiku 省 $8.40。**成本槓桿在 worker 選擇，不在 orchestrator 選擇。**

---

## 實際案例：已經有人用這套模式跑出成果

**Stripe** — 用 Fable 5 把一個 5,000 萬行的 Ruby codebase 遷移完成，花了一天。之前預估要兩個月。

**Simon Willison** — 24 小時花了 $110.42。Fable 5 解決了 Datasette Agent 的問題，順便修了四個底層 library 的 bug。他說這是「好幾天份的工作量」在幾個小時內完成的。

**Mozilla** — 用 Mythos Preview（Fable 5 的前身）在 Firefox 150 裡找到並修了 271 個 bug，是 Firefox 148 用 Opus 4.6 時的 10 倍以上。

**Cloudflare** — 用 Mythos Preview 找到 2,000 個 bug，其中 400 個是 high/critical。

**蛋白質設計** — 14 個蛋白質目標中，9 個產生了強候選。藥物設計流程加速 10 倍。

**基因組學** — 自主執行了一整週的研究，整合了 138 個物種、數百萬個細胞的 single-cell 資料，訓練出的 ML 模型比 Science 期刊發表的模型表現更好，體積卻小 100 倍。

共同 pattern：**這些都不是「寫一封 email」的任務。是跨多步驟、需要自主決策、牽涉大規模操作的長程任務。**

---

## 長時間自主運行：「跑了 8 小時以上」不再是吹牛

Anthropic 官方說 Fable 5 可以「work for days at a time」，聽起來像行銷話術，但現在已經有人跑出實際數據。John Exter 給了它一個預估 12 小時的多檔案重構，3 小時 17 分鐘就完成了；他之前更誇張，一個 `/loop` 指令跑了 26 小時，中間自動恢復 API 錯誤繼續跑，差點燒掉 $400。Matthew Pines 拿它做前沿物理研究，跑了 36 小時，追上 GPT-5.5 花 4 天才到的進度。它能長跑的關鍵不是 context window 更大——跟 Opus 一樣是 1M tokens——而是它會自己做筆記、自己壓縮已完成的工作串。Anthropic 拿 Slay the Spire 測試，有持久記憶的 Fable 5 表現比 Opus 4.8 好 3 倍。但長跑也意味著新的 harness 需求：spending cap（沒設的話就是信用卡炸彈）、外部記憶（跑越久 context rot 越嚴重）、斷點恢復——這些不是可選的，是跑超過 1 小時的基本配備。

---

## Harness 演進的脈絡：從外部框架到模型自己寫 Harness

Fable 5 本質上是把過去兩年 harness 工程師做的事——任務拆解、模型路由、workflow 生成——吃進模型本身了。放進 Harness 系列的脈絡裡看：

**階段一：外部框架（2024）** — LangChain、CrewAI、AutoGen。你用 Python 寫一大堆 orchestration code，定義 Agent 的角色、工具、流程。Harness 跟模型完全分離。問題是框架太厚，本身變成一個需要維護的 codebase。

**階段二：輕量 Harness（2025）** — Claude Code 的做法：[CLAUDE.md + hooks + permission tiers](/agent-harness-three-migrations-mechanism/)。Harness 變薄了，核心是約束和驗證，不是流程控制。Anthropic [不斷刪掉 harness 裡的邏輯](https://www.epsilla.com/blogs/anthropic-harness-engineering-agent-orchestration-subtraction)，因為新模型版本會內化那些能力。我們在 [Harness 系列](/harness-engineering-architecture-overview/) 裡講過這個「減法哲學」。

**階段三：兩條路線同時出現（2026 中）** — 一條是 [Boris Cherny 的 Loop Engineering](/loop-engineering-from-prompt-to-loop-paradigm-shift/)，人設計自動迴圈讓 Agent 自己跑，加入 Memory（跨次記憶）和 Automations（定時觸發）。另一條是 Fable 5 代表的「模型即 Orchestrator」，模型自己寫 workflow 腳本、自己決定模型調度、自己管理子任務的並行和合成。這兩條路線哪個會成為主流，現在還看不清楚——也可能最後是混合的。

具體來說，Anthropic 在 [Dynamic Workflows](https://code.claude.com/docs/en/workflows) 裡做的事情是：Claude 寫一段 JavaScript 編排腳本，可以 spawn 最多 1,000 個 sub-agent，16 個同時並行。迴圈、分支、中間結果都活在腳本的變數裡，不是模型的記憶裡。[InfoQ](https://www.infoq.com/news/2026/06/dynamic-workflows-claude-code/) 記錄了一個案例：6 天產出 75 萬行程式碼。

| | 外部 Harness | 模型寫 Harness |
|---|---|---|
| **誰決定任務分解** | 人寫腳本 | 模型寫腳本 |
| **誰決定模型調度** | 人在 config 指定 | 模型根據任務複雜度選擇 |
| **執行是否確定性** | 是（腳本執行） | 是（生成的腳本執行） |
| **除錯難度** | 中（讀你自己寫的腳本） | 高（讀模型寫的腳本） |

**計畫用模型，執行用確定性邏輯。** 這是一個 hybrid——不是全交給模型，也不是全靠外部框架。

arXiv 上一篇 2026 年 5 月的論文 [Compiling Agentic Workflows into LLM Weights](https://arxiv.org/abs/2605.22502) 走得更遠：直接把 agent 流程編譯進小模型的權重裡，接近 frontier 品質，成本只有百分之一。這跟我們在 [EFC 論文](/agent-harness-effective-feedback-compute/) 裡的發現一致：**orchestration 品質比模型原始能力更重要。**

三個階段的共同方向：**人往上移一個抽象層。** 但每上一層，你需要理解的東西反而更多——因為你需要判斷模型的調度決策對不對。

---

## 坦白講：問題在哪裡

### 好用是真的好用，貴也是真的貴

Django 共同創造者 Simon Willison 一天 $110。有開發者一個 code-review 的 prompt「在 subagents 之間燒掉 $92」都沒跑完。

社群的吐槽很直接：「成本是 Codex 9-10 倍」、「一個問題還沒問完，5 小時額度幹光了」、「隨便跑的任務，沒感覺強多少」、「is it just me or has fable 5 gotten noticeably worse?」。有人甚至說「除非你寫澳門賭場詐騙代碼，否則想不到什麼能回本」。

問題的根源是 **訂閱額度和 Fable 5 的 workflow 模式天然衝突**。當你讓 Fable 5 當 orchestrator 調度十幾個 sub-agent，一個 workflow 就可能燒掉大半天的額度。Max Lv 自己也踩過——從 Pro 升到 20x 方案，額度勉強夠做 side project，上班靠公司訂閱。他後來的結論是未來會改走 API，因為 API 讓你自己控制模型路由，Orchestrator 用 Fable、Worker 用 Haiku，成本透明可控，不受訂閱額度的硬天花板。

6 月 22 日之後免費期結束，需要 usage credits。現在的爽感可能很快就會撞上帳單的現實。**「choose agent's model wisely」不只是省錢技巧，是用 Fable 5 的基本功。**

### 用著用著突然降級成 Opus 4.8

很多人的體感是：Fable 5 用到一半，突然回應品質明顯下降。這不是錯覺。Fable 5 / Mythos 5 用了一套三域分類器（資安、生化、蒸餾），觸發時會把回應交給 Opus 4.8 處理，API 回傳 `stop_reason: "refusal"`。

為什麼要鎖？因為 Anthropic 在 [244 頁的 System Card](https://www-cdn.anthropic.com/d00db56fa754a1b115b6dd7cb2e3c342ee809620.pdf) 裡承認：Fable 5 的底層模型「likely crossed」了 CB-1 門檻。CB-1 是 Anthropic [Responsible Scaling Policy](https://www.anthropic.com/responsible-scaling-policy) 裡定義的生化武器能力閾值——模型能顯著幫助具備基礎理工背景的人製造已知的生化武器。十幾位病毒學家、免疫學家、合成生物學家組成的紅隊評估結論是：這個模型已經是「force multiplier」等級，能端到端指導非新型生物武器的合成流程，甚至能建議基因序列修改來優化高風險病毒的傳播效率。CB-2（新型武器）還沒跨過，但早期信號已經在被監控。

資安方面更誇張：Mythos Preview 在 Firefox 147 的零日漏洞利用測試中達到 84% 成功率（72.4% 實現完整的任意代碼執行），Opus 4.6 只有 15.2%。

所以三域分類器不是 Anthropic 過度謹慎，是模型真的到了需要 ASL-3 防護的能力等級。

問題是分類器的精準度。有人做醫學影像分析被擋、實驗室自動化被擋、甚至提到 "cancer" 都觸發了生物安全分類器。Anthropic 承認分類器「過度保守」，95% 的 session 完全沒觸發，但那 5% 的誤殺造成了很大的挫折感。Nathan Lambert 在 [Interconnects](https://www.interconnects.ai/p/claude-fable-5-and-new-ai-safety) 的批評更尖銳：他認為隱藏的能力限制是「categorically misaligned AI」——一個在你不知道的情況下自動變笨的 AI。

### 30 天強制資料保留

Fable 5 有 30 天的強制資料保留，沒有零資料保留的選項。Microsoft 因為這個限制了員工使用。對企業客戶來說，這是一個真實的 blocker。

### 除錯變難了

當模型自己寫 workflow 腳本的時候，你的除錯對象從「我自己寫的 harness code」變成「模型生成的 harness code」。讀過我們 [Opus 4.7 Post-mortem](/opus-4-7-claude-code-harness-postmortem/) 那篇就知道，harness 層的 bug 有多難抓——使用者感受到「模型變笨了」，但實際上是 harness 出問題。現在 harness 也是模型生成的，除錯鏈又加了一層。

---

## 實操建議：現在該怎麼用 Fable 5

### 1. 不要把 Fable 5 當 Opus 4.8 的升級版

Fable 5 的 ROI 不在「回答問題更準」，在「調度 Agent 更好」。如果你只是在聊天視窗裡一問一答，你會覺得它跟 Opus 差不多，然後帳單差兩倍。

### 2. Workflow + 模型路由是基本功

Claude Code 裡的 subagent 可以指定模型：

```yaml
---
name: code-scout
description: Read-only repo exploration
tools: Read, Glob, Grep
model: haiku
---
```

把搜尋、分類、摘要類的 subagent 指定為 `haiku`，把程式修改類的指定為 `sonnet`，只有 orchestration 用 Fable 5。

### 3. Prompt Cache 是第二個省錢槓桿

Fable 5 的 prompt cache 有 90% 折扣。如果你的 worker fleet 有共用的 system prompt（40K tokens 的 context），cache 能把 Sonnet worker 的 input 成本從 $2.16 砍到 $1.00。

### 4. 失敗升級而不是一步到位

先用 Haiku 試，失敗了升 Sonnet，Sonnet 也失敗了才升 Fable。兩次 Haiku 失敗加一次 Sonnet 重試的額外成本只有 $0.60。

### 5. 設定 Client Timeout

Fable 5 在高 effort 模式下，單一請求可以跑很多分鐘。自主模式下可以跑數小時。如果你的 harness 有 timeout 設定，需要調大。Anthropic 建議改成非同步檢查模式，不要 blocking wait。

---

## 結語：法拉利很快，但大多數人需要的是 Tesla

Fable 5 是法拉利——強、快、貴，而且鎖了很多東西。它內化的是 **orchestration** 能力——任務分解、模型選擇、並行管理。這是 Harness 的「引擎」。

但 Harness 的另一半——約束、防護、審計——這些是刻意限制模型能做什麼的機制。你不會讓一個模型自己決定「我應不應該被約束」。如果你的 Harness 在做的是 [四層防禦](/coders-who-stopped-coding-harness-context-spec-engineering/)、[機械式強制執行](/agent-harness-three-migrations-mechanism/)、[安全最佳實踐](/harness-engineering-security-best-practices/)——這些不但不會被取代，反而因為模型自主性更高，變得更重要了。

**大多數人更需要的是 Tesla：** 一個 local Qwen + 一個 Opus 4.6 + 一套 GPT-5.5 的組合，配合寫好的 harness——模型路由、成本控制、安全邊界都在你自己手上。Fable 5 告訴你 orchestration 的方向，但不代表你要用 Fable 5 來跑每一個任務。

Harness 工程師的工作重心會從「怎麼調度 Agent」轉向三件事：**設計約束和安全邊界**（模型可以決定「用哪個 Agent 做什麼」，但不能決定「這個 Agent 能不能刪檔案」）、**審查模型的調度決策**（workflow 腳本合不合理？有沒有浪費成本？）、**設計 feedback loop**（[EFC 論文](/agent-harness-effective-feedback-compute/) 告訴我們 feedback 品質比算力重要，這部分還是需要人來架構）。

**引擎內化了，煞車外置了。你要學的不是怎麼買法拉利，是怎麼幫任何車設計煞車系統。**

---

## 延伸閱讀

**Harness Engineering 系列：**
- [Harness Engineering 七件式參考架構](/harness-engineering-architecture-overview/)
- [Agent Harness 三次中心遷移：Mechanism > Prompt](/agent-harness-three-migrations-mechanism/)
- [Opus 4.7 Post-mortem：是 Harness，不是模型](/opus-4-7-claude-code-harness-postmortem/)
- [Loop Engineering：不再 Prompt Agent，改設計 Loop](/loop-engineering-from-prompt-to-loop-paradigm-shift/)
- [EFC：Feedback 品質 > 算力](/agent-harness-effective-feedback-compute/)
- [Harness Engineering 安全最佳實踐](/harness-engineering-security-best-practices/)

**外部參考：**
- [Anthropic Fable 5 Prompting Guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)
- [Developers Digest: Fable 5 Orchestrator Model Playbook](https://www.developersdigest.tech/blog/fable-5-orchestrator-model-playbook)
- [Epsilla: Anthropic 的減法哲學](https://www.epsilla.com/blogs/anthropic-harness-engineering-agent-orchestration-subtraction)
- [arXiv: Compiling Agentic Workflows into LLM Weights](https://arxiv.org/abs/2605.22502)
- [Simon Willison: Fable 5 First Impressions](https://simonwillison.net/2026/Jun/9/claude-fable-5/)
- [Dynamic Workflows in Claude Code](https://code.claude.com/docs/en/workflows)
