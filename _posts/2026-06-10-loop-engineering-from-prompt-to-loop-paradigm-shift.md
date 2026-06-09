---
layout: post
title: "Loop Engineering：不再 Prompt Agent，改設計 Loop 讓 Agent Prompt Agent"
date: 2026-06-10 09:00:00 +0800
permalink: /loop-engineering-from-prompt-to-loop-paradigm-shift/
image: /assets/images/loop-engineering-steinberger-tweet.png
description: "Peter Steinberger 一條推文 3 百萬觀看：「你不該再 Prompt Agent 了，你該設計 Loop。」Boris Cherny（Anthropic Claude Code 負責人）說他現在的工作是寫 Loop，不是寫 Prompt。Karpathy 用 630 行 Python 跑了 700 次實驗、發現 20 個優化、提速 11%。Loop Engineering 是下一個 buzzword，還是從 Harness 自然長出來的範式轉移？這篇拆解三個來源的定義差異，對照 Harness 系列已經講過的概念，然後劃一條線：哪些工作該 Loop 化，哪些不該。"
---

> "You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents."
> —— Peter Steinberger，2026 年 6 月 8 日，3 百萬觀看

![Peter Steinberger 推文：You should be designing loops that prompt your agents（3M Views）](/assets/images/loop-engineering-steinberger-tweet.png)

如果你不認識 Peter Steinberger，他是 OpenClaw 的作者，之前我們在 [Harness Engineering 系列](/harness-engineering-control-plane-pattern-agent-review-loop/) 裡提過他：開 50 個 Codex 並行審 3,000 個 PR，單日 627 次提交。他不是在講理論，他是在講他每天在做的事。

同一週，Boris Cherny——Anthropic Claude Code 的負責人——在 [Addy Osmani 的訪談](https://addyosmani.com/blog/loop-engineering/)裡說了幾乎一模一樣的話：

> "I don't prompt Claude anymore. I have loops running that prompt Claude. My job is to write loops."

然後三月份，Karpathy 用 630 行 Python 讓一群 Agent 自己跑了 700 次實驗，發現 20 個優化，在更大模型上實現了 11% 的訓練加速。他說：「All LLM frontier labs will do this. It's the final boss battle.」

三個獨立的信號指向同一個方向：**工程師的工作正在從「Prompt Agent」變成「設計 Loop 讓 Agent Prompt Agent」。**

社群開始把這套做法叫 Loop Engineering。

問題是：這是真的範式轉移，還是繼 Vibe Coding、Harness Engineering 之後又一個 buzzword？

---

## 先釐清：三個人講的「Loop」不是同一件事

我看了三個主要來源之後發現，大家嘴裡的 Loop Engineering 其實指涉三個不同的層次。

### Karpathy 的 Loop：單一 metric 的自主研究迴圈

Karpathy 的做法很純粹。[Fortune 的報導](https://fortune.com/2026/03/17/andrej-karpathy-loop-autonomous-ai-agents-future/)描述了整個流程：

一群 LLM Agent 被放進一個迴圈裡，每一輪做三件事：讀研究論文和過去的實驗紀錄、產生假設和代碼修改、跑實驗測量一個明確的 metric。跑完一輪，結果回到紀錄裡，下一輪再用。

630 行 Python。2 天。700 次實驗。20 個有效發現。

Shopify CEO Tobias Lutke 複製了這個做法：一個晚上跑了 37 次實驗，內部 AI 模型性能提升 19%。

Karpathy 區分了這跟 AutoML 的差別：「This is an actual LLM writing arbitrary code... It's not even close.」AutoML 是隨機搜索超參數，Karpathy Loop 是 Agent 讀論文、形成假設、寫代碼、從失敗中學習。

關鍵限制：**你需要一個可以自動衡量的 metric。** 有 metric 就能 loop，沒有 metric 就只能靠人判斷。

### Boris Cherny 的 Loop：多 Agent 開發工作流的編排

Boris 講的是另一個維度。他在 Addy Osmani 的訪談裡定義了 Loop 的五個組件：

1. **Automations**——定時觸發的發現和分類流程，不需要人啟動
2. **Worktrees**——隔離的平行執行環境，防止多個 Agent 的檔案衝突
3. **Skills**——把專案知識編碼成 `SKILL.md`，不用每次重新解釋 context
4. **Connectors**——透過 MCP 連接外部工具和服務
5. **Sub-agents**——用獨立的 Agent 做驗證，防止一個 Agent 自己改自己審

加上 **Memory**——跨次執行的狀態追蹤，用 markdown 檔案或 Linear board 維護持久記憶。

他做了一個清楚的分層：

> Prompt Engineering → Harness Engineering → Loop Engineering

Prompt 是手動對話。Harness 是替單一 Agent 建約束環境。Loop 是在 Harness 之上，管理多個 Agent 的時序、決策、和自主迴圈。

### Reddit 用戶的 Loop：最務實的定義

一個 Reddit 用戶把 Loop 拆成了六個元素：

```
loop = trigger + context + action + verification + state + retry/stop rules
```

然後說了一句我覺得是全場最清醒的話：

> "I don't want to loop-engineer the creative/editorial part, because that works better when I'm actively steering it."

他的實際做法是只在「邊緣」加 Loop：

- **Before I show up**: gather candidates, de-dupe, check sources
- **After I write/select**: verify links, check facts, validate images, leave draft only

中間的創意決策？留給人。

---

## 從 Prompt 到 Loop：三次遷移的脈絡

如果你一直在跟我們的 Harness Engineering 系列，這個演進其實很自然。

**第一次遷移：Prompt Engineering（2023-2024）**

工程師手動跟 AI 對話。寫好 prompt、貼上 context、讀回覆、判斷、再寫 prompt。瓶頸是人的打字速度和注意力。

**第二次遷移：Harness Engineering（2025-2026 初）**

我們在 [Harness Engineering 系列](/harness-engineering-control-plane-pattern-agent-review-loop/) 裡講過：OpenAI 3 個工程師用 Codex 在 5 個月產出 100 萬行代碼、0 行人寫。核心是建約束——[preflight gate、SHA discipline、remediation loop](/harness-engineering-control-plane-pattern-agent-review-loop/)、[hooks 機制](/agent-harness-three-migrations-mechanism/)。人不再寫代碼，但仍然在每一步觸發和審查 Agent。

**第三次遷移：Loop Engineering（2026 中）**

人不再手動觸發 Agent。人設計自動觸發的迴圈，Agent 在迴圈裡自己跑、自己驗證、甚至自己觸發其他 Agent。人的角色從「操作員」變成「系統設計師」。

三次遷移的共同方向是一樣的：**人往上移一個抽象層。**

從寫代碼 → 寫 Prompt → 建 Harness → 設計 Loop。每上一層，你需要理解的東西反而更多，不是更少。

---

## Boris 的五個組件 vs. 我們已經講過的概念

Boris Cherny 的五個組件聽起來很新，但如果你讀過 Harness 系列，會發現大部分概念已經存在——只是被重新組合和升級了。

| Boris 的組件 | Harness 系列的對應概念 | 新在哪裡 |
|---|---|---|
| Automations | 沒有直接對應 | **全新**：定時自動觸發，不需要人啟動 |
| Worktrees | [Control Plane Pattern](/harness-engineering-control-plane-pattern-agent-review-loop/) 裡的 git worktree | 從單一 Agent 擴展到多 Agent 平行 |
| Skills | AGENTS.md / CLAUDE.md 知識庫 | 更結構化，變成可複用的 SKILL.md |
| Connectors | MCP 工具整合 | 基本相同 |
| Sub-agents | [EFC 論文](/agent-harness-effective-feedback-compute/) 的 verifier agent | 從概念落地到具體架構角色 |
| Memory | 沒有直接對應 | **全新**：跨次執行的持久狀態 |

真正新的東西是兩個：**Automations（自動觸發）** 和 **Memory（跨次記憶）**。

這兩個加在一起，讓系統從「人按一下跑一次」變成「自己決定什麼時候跑、記得上次跑到哪裡」。

這就是 Harness 和 Loop 的本質差異。Harness 是「接住 Agent 的產出」，Loop 是「讓 Agent 自己決定什麼時候產出、產出什麼」。

---

## Karpathy Loop 的數據：Loop 為什麼有效

Karpathy 的實驗提供了目前最硬的數據來說明 Loop 的威力。

關鍵數字：

- **630 行 Python** 寫的 Loop 系統
- **700 次實驗**，2 天跑完
- **20 個有效優化**被發現
- **11% 訓練加速**（在更大模型上）
- Shopify 複製：**37 次實驗一個晚上**，**19% 性能提升**

Karpathy 定義了他的 Loop 的三個要素（後來被分析師 Janakiram MSV 命名為「The Karpathy Loop」）：

1. 一個有檔案修改權限的 Agent
2. 一個可以客觀測量的 metric
3. 每次實驗有固定的時間限制

然後他講了一句很重要的話：

> "The goal is not to emulate a single PhD student, it's to emulate a research community of them."

不是一個 Agent 跑一個很長的 loop。是一群 Agent 同時跑很多個 loop，彼此的結果互相啟發。他用的詞是「agent swarm」——Agent 群。

**但這有一個前提條件大家容易忽略：你需要一個可以自動衡量的 metric。**

Karpathy 的 metric 是訓練速度。Shopify 的 metric 是模型性能。這些都可以跑完一次實驗就自動得出數字。

如果你的工作是「寫一篇好的技術文章」或「設計一個易用的 UI」，什麼是你的自動 metric？沒有明確的自動 metric，Loop 就退化成一個自動跑但不知道自己跑得好不好的系統。

---

## Loop 的成本：你的帳單也在 Loop

這是大部分 Loop Engineering 討論裡被跳過的部分。

手動 Prompt Agent，你的成本是線性的——打一次 prompt、花一次 token、看一次結果。Loop 的成本結構完全不同，因為三個乘數同時作用：

**成本 = 迭代次數 × 每次 Agent 呼叫的 token × 平行實例數**

Karpathy 跑了 700 次實驗。每次實驗 Agent 要讀之前的實驗紀錄、讀研究論文、產生假設、寫代碼、跑驗證。假設每次迭代消耗 10K input tokens + 2K output tokens，光是 Agent 呼叫的 API 成本就不低。再加上他說的「agent swarm」——不是一個 Agent 跑 700 次，是多個 Agent 平行跑。

如果你用 sub-agent 做驗證（Boris 的五個組件裡明確要求這個），成本直接翻倍——因為每一個 Agent 的產出都要另一個 Agent 審一遍。

更危險的是：**Loop 在你睡覺的時候也在跑。** Shopify 的 37 次實驗是「一個晚上」跑完的。Peter Steinberger 單日 627 次提交也不是他坐在電腦前盯出來的。這代表如果你的 Loop 沒有設好停止條件，你醒來的時候帳單可能已經失控了。

幾個實際的成本控制機制：

1. **固定時間限制**——Karpathy Loop 的第三個要素就是「每次實驗有固定的時間限制」，這同時也是成本上限
2. **Budget cap**——設定每個 Loop 的 token 預算，超過就停
3. **收斂檢測**——如果連續 N 次迭代都沒有改善 metric，自動停止，不要空轉燒錢
4. **分層用模型**——Loop 裡的初篩用便宜模型（Haiku），只在關鍵判斷點用貴的模型（Opus）

ROI 的算法也不一樣了。以前是「AI 幫我省了多少小時的人力成本」，現在是「Loop 的 API 成本 + 設計成本，有沒有低於它發現的價值」。Karpathy 的 11% 訓練加速，對一個前沿 AI 實驗室來說，省下的 GPU 時間遠超 API 成本。但如果你的 Loop 只是自動跑 lint 然後開 PR，算一下 token 帳單再決定值不值得。

**Loop Engineering 不只是工程問題，也是經濟問題。** 設計 Loop 的時候，停止條件和成本上限跟迴圈邏輯一樣重要。

---

## 邊界在哪裡？不是所有工作都該 Loop 化

這是我覺得整場討論裡最重要的問題，也是那個 Reddit 用戶講得最清楚的地方。

他把自己的研究寫作工作流分成兩段：

**適合 Loop 的部分（重複、可驗證、風險可控）：**
- 收集候選素材、去重、檢查來源
- 驗證連結有效性、事實查核、圖片校驗
- 輸出草稿但不發布

**不適合 Loop 的部分（需要判斷、創意、掌舵）：**
- 選題決策
- 觀點建構
- 敘事結構
- 最終定稿

他的結論是：Loop Engineering 的正確用法是「在重複或高風險的環節加上 memory、verification 和 guardrails」，而不是「把整個工作流變成剛性腳本」。

Boris Cherny 自己也發出了類似的警告：

> "Build the loop. But build it like someone who intends to stay the engineer, not just the person who presses go."

他特別提到了兩個風險：

1. **Comprehension debt**——代碼出貨速度越快，工程師對自己系統的理解可能跟不上
2. **Cognitive surrender**——為了省腦力而建 Loop，結果是放大問題而不是解決問題

---

## 跟 Harness 系列的關係：Loop 是 Harness 的自然延伸

如果你是第一次看到 Loop Engineering 這個詞，可能會覺得這是一個全新的概念。但如果你跟著我們的 Harness 系列走過來，你會發現 Loop 是 Harness 往上長了一層。

我們之前講過的每一個概念，都是 Loop 的基礎：

- [四層防禦架構](/harness-engineering-architecture-overview-ai-code-production-guardrails/)——Loop 裡面的每個 Agent 仍然需要這些約束
- [Control Plane Pattern](/harness-engineering-control-plane-pattern-agent-review-loop/)——Loop 的「verification」環節就是 control plane 的自動化版本
- [Prompt 是建議，機制才是規則](/agent-harness-three-migrations-mechanism/)——Loop 裡的約束更需要是機制而不是 prompt，因為人不在旁邊盯
- [Effective Feedback Compute](/agent-harness-effective-feedback-compute/)——Loop 的效率取決於反饋信號的品質，不是跑的次數

**沒有 Harness 的 Loop，就是一個自動跑、自動出錯、自動製造垃圾的系統。**

Peter Steinberger 在 Reddit 上被問到具體怎麼做 Loop 時，回答是：「I have my Claw supervising my Codexes.」然後開玩笑說，幾個月後我們會在談「fleets that design your loops」——設計你的 Loop 的 Fleet。

這不是玩笑。這是抽象層不斷往上疊的現實。但每往上一層，下面的基礎就更重要——你的 CI/CD 夠不夠穩、你的測試覆蓋率夠不夠高、你的 Agent 約束機制夠不夠硬。

---

## 坦白說

我自己的使用狀態大概在 Harness 和 Loop 的交界。

日常的 Claude Code 使用裡，我已經在做一些 Loop 的雛形：hooks 自動攔截高風險操作、`/loop` 指令跑定期檢查、sub-agent 做獨立驗證。但離 Boris Cherny 說的「我不再 Prompt Claude，我寫 Loop 讓 Claude 自己跑」還有一段距離。

真正的瓶頸不是技術，而是我前面說的那個問題：**很多工作沒有可以自動衡量的 metric。**

寫 blog、做技術決策、設計系統架構——這些工作的「好壞」需要人來判斷。你可以 Loop 化收集素材和校驗事實，但你不能 Loop 化「這個觀點有沒有洞見」。

Karpathy 的成功恰恰是因為他的場景完美符合 Loop 的前提：一個明確的 metric（訓練速度）、一個可以自動跑的驗證流程（跑模型測 benchmark）、一個封閉的修改空間（訓練代碼）。

大多數軟體工程的日常不長這樣。

---

## 所以 Loop Engineering 是 buzzword 嗎？

是，也不是。

**是 buzzword 的部分：** 把一件本來就存在的事（自動化工作流 + CI/CD + cron job）換了一個新名字，然後宣稱這是「範式轉移」。如果你之前就有好的 CI/CD、好的測試、好的 Agent 約束，你已經在做 Loop Engineering 的一部分了。

**不是 buzzword 的部分：** LLM Agent 帶來的真正新能力是「讀 context、產生假設、從失敗中學習」。這不是傳統的 cron job + script 能做到的。Karpathy 的 700 次實驗不是隨機搜索，是 Agent 在讀之前的實驗結果、形成新的假設、寫新的代碼。這是質的差異。

我的判斷是：**Loop Engineering 的核心概念是真的，但適用範圍比推文讓你以為的窄很多。**

三個條件決定你能不能有效 Loop 化一個工作環節：

1. **有可自動衡量的 metric 嗎？** 沒有 → 不能 Loop，或者只能 Loop 到「輸出草稿等人審」
2. **失敗的代價可控嗎？** 不可控 → 需要人在 Loop 裡，不是 Loop 外
3. **你的 Harness 夠硬嗎？** 不夠 → 先補 Harness，不要急著建 Loop

Reddit 用戶的那句話是最好的總結：

> "Maybe loop engineering is more 'add memory, verification, and guardrails around repetitive or risky parts.'"

不是把整個工作流 Loop 化。是在重複和高風險的環節，加上記憶、驗證、和護欄。

其餘的部分——需要判斷、需要創意、需要掌舵的部分——那還是你的工作。

人設計 Loop。但設計 Loop 的那個人，不能停止當工程師。
