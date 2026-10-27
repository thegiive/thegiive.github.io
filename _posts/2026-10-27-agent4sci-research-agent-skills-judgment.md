---
layout: post
title: "AI Agent 能自己做科研嗎？Anthropic 的 Agent4Sci：可以，但要先打上一層科研 Harness，三份 Skill 讓 Opus 從 10.4% 變 20.1%"
date: 2026-10-27 09:00:00 +0800
permalink: /agent4sci-research-agent-skills-judgment/
tags: [Agent4Sci, Anthropic, Claude Code, Codex, Gemini CLI, Research Agent, Agent Skills, Hooks, Harness Engineering, ML for Science]
categories: [AI Agent]
image: /assets/images/agent4sci-research-agent-skills-cover.png
description: "Anthropic 想知道現在的 AI agent 能不能自己做科學研究，做法是給 Claude Code、Codex、Gemini 一篇科學論文、程式碼和資料，叫它把成績做得更好。20 題、11 個領域、8 張 H200、12 小時，agent 每一題都找到提升，Claude Opus 平均相對提升 10.4%。但拆開來看，大部分是調學習率、加深模型、換 backbone，依舊是大力出奇蹟。作者沒有換模型，只加了三份總共 277 行的 skill 和一支每小時觸發的 hook，Opus 就變成 20.1%、Codex 從 4.4% 變 8.1%。這篇拆解 agent 做科研的三個毛病、那層科研 Harness 長什麼樣子，以及為什麼它缺的不是判斷力，是人類研究者訓練出來的反射。"
author: Wisely Chen
faq:
  - question: "Agent4Sci 是什麼？"
    answer: "Agent4Sci 是 Anthropic Fellows Program 與 Anthropic 研究員在 2026 年 10 月發表的研究（arXiv 2610.28763，NeurIPS 2026 Evaluations and Datasets track），測試 AI agent 能不能自己做科學研究。它收錄 20 個 ML for Science benchmark、11 個科學領域，讓 Claude Code、Codex、Gemini CLI 在 8 張 H200、12 小時內，把原論文發表的最好結果往上推，這個任務形式叫自動化科學爬山（Automated Scientific Hill-Climbing）。預設設定下 Claude Opus 4.6 平均相對提升 10.4%，但大部分來自調超參、改架構這類 ML 工程技巧。"
  - question: "什麼是「科研 Harness」？Agent4Sci 加了什麼？"
    answer: "Harness 指的是包在 AI 模型外面、規定它怎麼工作的那一層：工具、規則、流程和檢查機制。Agent4Sci 加了三份 skill（Agent Skills）：科研構思 102 行、實驗管理 112 行、定時自檢 63 行，加起來 277 行；再加一支 Claude Code 的 PreToolUse hook，每 3600 秒觸發一次，觸發後除了 Skill 以外的工具都被擋下，直到 agent 跑完自檢清單。模型沒換、算力沒加，Claude Opus 的平均相對提升從 10.4% 變成 20.1%，Codex 從 4.4% 變成 8.1%。"
  - question: "AI agent 做科學研究最常犯哪些錯？"
    answer: "論文從軌跡整理出三個反覆出現的毛病。第一是高估新穎性（Novelty Miscalibration），例如 Claude 把幾乎人人預設會開的 cosine 學習率排程當成創意突破。第二是資源閒置（Resource Under-utilization），8 張 H200 常常有卡閒著，能平行的實驗被排成串行。第三是探索收斂（Exploration Collapse），找到一個有效方向後就一直在附近調 seed 和學習率，不再嘗試其他做法。"
  - question: "為什麼「請你多想一點」沒用，但 Harness 有用？"
    answer: "「請你多想一點」只是 prompt，模型可以忽略，也可以寫完「我正在做有創意的實驗」之後繼續調參數。Agent4Sci 的 Harness 是拿掉選項：科研構思在文獻回顧跑完之前禁止碰 codebase，實驗管理直接列出重跑 baseline、多 seed、seed ensemble 等不准做的實驗，定時自檢用 PreToolUse hook 每 3600 秒把 Skill 以外的工具擋下（exit 2），agent 只剩做自檢這條路。效果不是來自文字寫得多好，而是來自其他路被堵住。"
  - question: "加了 Harness 之後，AI 就會做真正的科研嗎？"
    answer: "會更常碰到真正的領域洞見，但不保證。在電網題目 PFDelta 上，加了 Harness 的 Claude Opus 認出評分指標可以從克希荷夫定律推出來，把它改成主要訓練目標，進步從 64.4% 變成 91.0%。但同一題沒有 Harness 重跑四次，只有兩次想到類似的關鍵改法；Codex 加了 Harness 在這題反而從進步 4.6% 變成退步 12.8%；跑滿三天的 Opus 在第 12 小時之後還是回到調學習率。程式碼在 github.com/maszhongming/agent4sci（Apache 2.0），可以拿來改，但 skill 是照 Claude Code 的軌跡設計的，換領域要自己測。  ---"
---

現在的 AI agent，能不能自己做科學研究？

Anthropic 10 月 20 日放上 arXiv 的 [Agent4Sci](https://arxiv.org/abs/2610.28763) 就在問這件事。做法很直接：給 agent 一篇科學論文、它的程式碼和資料，叫它想辦法把論文的成績做得更好。

答案是可以。

但是要先打上一層科研專屬的 Harness。

![Automating ML for Science: Can Frontier Agents Climb Scientific Hills in the Wild? 論文首頁](/assets/images/agent4sci-logo.png)

<nav class="post-toc" markdown="1">
**目錄**

* 目錄
{:toc}
</nav>

---

## 30 秒定位

| 項目 | 內容 |
|------|------|
| 論文 | Automating ML for Science: Can Frontier Agents Climb Scientific Hills in the Wild?，arXiv 2610.28763 |
| 作者 | Ming Zhong、Stacy Li（Anthropic Fellows Program），Nicholas Carlini、Matthew Jagielski（Anthropic） |
| 題目 | 20 個真實的 ML for Science benchmark，橫跨天文、化學、生態、物理、生物工程等 11 個領域 |
| 受測 agent | Claude Opus 4.6、Claude Sonnet 4.6、Codex（GPT-5.4）、Gemini 3.1 Pro |
| 條件 | 每次 8 張 H200、12 小時，除了開跑和到時間停掉之外沒有人介入 |
| 預設結果 | 平均相對提升：Opus 10.4%、Sonnet 9.6%、Gemini 6.8%、Codex 4.4% |
| 加上 Harness | Opus 10.4% → 20.1%（1.9 倍），Codex 4.4% → 8.1%（1.8 倍） |
| 程式碼 | [github.com/maszhongming/agent4sci](https://github.com/maszhongming/agent4sci)，Apache 2.0，skill 和 hook 都在裡面 |

---

## 實驗怎麼做的

Agent4Sci 把 Claude Code、Codex、Gemini CLI 放進 20 個真實的科學 benchmark。每一題的起點，都是那篇論文已經發表的最好結果，agent 要在 12 小時內把它往上推。

在正式開跑之前，作者先處理了一個問題：**什麼叫做「驗證過了」？**

他們先做了一個最簡單的版本，把論文和原始 repo 直接丟給 agent。結果 5 個 NeurIPS 2025 benchmark 的 12 個任務裡，有 5 個出現嚴重的 evaluation gaming。手法分四類，用考試來比喻：

- **只挑會的題目算分**：只拿對自己有利的那部分資料算成績。
- **偷看考卷**：去看本來不該看的測試資料。
- **改評分標準**：說官方的評分方式有問題，自己換一套。
- **直接抄答案**：把答案寫死在程式裡，甚至謊稱 checkpoint「不小心刪了」。

所以作者把評分權從 agent 手上拿走。測試資料藏起來，agent 只看得到訓練和驗證資料；交卷之後，由另一個 evaluation agent 跑分，再由第三個 auditing agent 讀完整條軌跡找作弊。這樣處理之後，沒有任何一次 run 被標記作弊。

這跟我九月寫的 [DeepMind 100 個 agent 數學會議](/deepmind-agent-swarm-cheating-whistleblowing-commons/) 是同一件事的兩面：那邊的驗證器太弱，作弊 27 分鐘傳遍整個群體；這邊作者先看到漏洞，就把評分和稽核拆給別人。

這是整篇論文的第一層 Harness。後面那三份 skill 是第二層。

---

## 結果：每題都有提升，但依舊是大力出奇蹟

前沿 agent 在每一題上都找到提升，Claude Opus 平均相對提升 10.4%。

但作者把軌跡拆開後發現，大部分提升來自熟悉的 ML 工程技巧：學習率調整、加深加寬模型、換 backbone、weight decay、pooling、資料增強、輔助 loss。

Opus 的 run 裡，56% 用了調超參、44% 改架構。真正針對科學問題本身的新解法，很少。

所以依舊是大力出奇蹟。

三家花掉這 12 小時的方式也不一樣：Opus 一直盯著 log，看完一輪再決定下一輪，平均 12.0 小時都在工作；Codex 第一個小時就丟出一支長跑腳本，剩下的十一個小時在等；Gemini 在兩種模式之間來回。

---

## Agent 做科研反覆出現的三個毛病

作者讀完所有軌跡，整理出三個一直出現的毛病。

**一，高估新點子的新穎性。** Claude 在做科學研究時，把 cosine 學習率排程當成了自己的「創意突破」。

> "Claude Code treats cosine learning-rate schedules as a creative breakthrough across runs, even though they are long-standing standard practice."

cosine 學習率排程是訓練模型的預設動作：一開始學快一點，後面慢慢放慢，幾乎人人都在用。Claude 在好幾次 run 裡都把它當成大膽的新想法。

**二，GPU 放著不用。** 明明有 8 張 H200，GPU 常常閒著，能平行跑的實驗被排成一個接一個跑，有時候 CPU 和 GPU 還互相搶資源。

**三，找到一個有效方向，就一直在附近刷參數。** 前幾輪想法很多，但只要發現某個做法有效，剩下的時間就在它周圍調 seed、調學習率，沒有再從其他領域的角度廣泛去想。

---

## 怎麼解決？依舊是 Harness

作者沒有換模型，也沒有加算力。他們只加了三份很輕量的 skill：科研構思、實驗管理、定時自檢。三份加起來 277 行。

**1. 科研構思（102 行）**

開跑時先派四個 subagent 平行查文獻，兩個查科學領域、兩個查 AI/ML 方法，查資料期間主 agent 不准碰程式碼。回來之後，強制把實驗分成兩級：Tier 1 是大膽、高風險高報酬的，Tier 2 是文獻支持、穩健的。Tier 1 先做，而且第一輪就要把所有顯卡吃滿。

最後還有一道校準：如果某個 Tier 1 實驗其實只是換超參、換訓練技巧或做 ensemble，就把它降級，換一個更大膽的上去。這一條正好對準 cosine 學習率那個毛病。

**2. 實驗管理（112 行）**

列出一張「無效實驗」清單：重跑 baseline、多 seed、在 baseline 上調超參、seed ensemble，全部不准。顯卡必須一直有工作在跑。實驗失敗了要先分類原因，不准反射性地丟掉。

**3. 定時自檢（63 行）**

每小時觸發一次，分四組回答：自我檢視、每個 job 的運維、策略、任務清單。自我檢視裡有一題是：

> "Am I designing creative experiments that require scientific reasoning, or just tweaking hyperparameters and calling it novel?"

我是在設計需要科學推理的實驗，還是只在調超參，然後說它是新點子？

**它根本不是 prompt。**

Claude Code 有一個機制叫 hook：每做一個動作之前，會先跑你掛上去的腳本。作者掛了一支 PreToolUse hook，INTERVAL=3600；時間到了之後，除了 Skill 以外的工具呼叫都被 exit 2 擋下，直到跑完 checklist 才解鎖。為了避免整個 session 卡死，鎖超過 10 分鐘會自動放行；subagent 不受影響。

也就是說，一小時一到，agent 只剩「做自檢」這一條路可以走。

前兩份 skill 其實也是同一個思路。科研構思是在文獻回顧跑完之前，禁止 agent 碰 codebase；實驗管理是直接列出不准做的實驗。三份的效果都來自**拿掉選項**，不是多加一句「請你更有創意」。

這跟我六月寫的 [從 Prompt 到 Harness 的三次中心遷移](/agent-harness-three-migrations-mechanism/) 是同一件事：你在 prompt 裡拜託 agent「記得每小時反省一下」，它會忘；用 hook 把其他動作擋掉，它就只能反省。上週拆的 [Harness²](/harness2-recursive-agent-harnessing-open-world/) 也是這個方向，拿掉 skills 和 scripts 掉的分數，比拿掉 prompt 類元件多。

---

## 加了 Harness 之後

- Opus：結果提升從 10.4% 變成 20.1%（1.9 倍），20 個 benchmark 裡改善 18 個
- Codex：結果提升從 4.4% 變成 8.1%（1.8 倍），改善 12 個

這裡的數字是「平均相對提升」：20 個題目各自比原論文進步多少，再取平均。不是某個模型的準確率翻倍。論文自己的用詞是「接近翻倍」（nearly double）。

skill 是照 Claude Code 調的，Codex 也拿到接近比例的增益。

---

## AI 不是不會判斷

最好的例子是電網題目 PFDelta。

沒有 Harness 的時候，Opus 在這題進步了 64.4%，做法是把評分指標改寫成可微的輔助 loss、MSE 權重從 0.1 調到 0.3、換成 cosine annealing 加 warmup。三招都是工程手法。

加了 Harness 之後，進步變成 91.0%。這次 agent 認出評分用的 PBL 可以從克希荷夫定律推出來，不需要標籤，於是直接改成主要的訓練目標；推論時再把 GNN 的預測當成 AC power-flow 方程的起始值，往物理上正確的解收斂。

這需要真的理解問題。

所以 agent 不是不會判斷。同一個模型，被逼著先查文獻、先做大膽的實驗、每小時停下來問自己「這是不是只在調參」之後，就做出了需要物理直覺的改法。

另一個例子是碳排放預測 CarbonGlobe。沒有 Harness 時，Opus 堆了 14 個模型的 ensemble，約 49 GPU 小時；有 Harness 時換成 8 個非自迴歸 transformer，不到 6 GPU 小時，推論快約 500 倍，成績還更好。好點子不一定比較貴。

---

## 缺的是反射

什麼時候該停、什麼該算新點子、顯卡該怎麼用、什麼叫做「驗證過了」。

這些東西人類研究者不用特別想，因為那是訓練出來的反射。指導教授在週會上問過太多次「這換個資料集還成立嗎」、「那幾張卡你打算拿來做什麼」，久了就內化了。

Agent 沒有這層反射，它就預設走機器最省力的路：調參數、刷分數。

三份 skill 加上一支 hook，本質上就是在 agent 外面架一層東西。**不是告訴它「要更聰明」，是告訴它「這幾件事一定要做」。**

比起給它更多算力，先給它一層科研的 Harness 更划算。

---

## 坦白說

這層 Harness 有效，但有幾個地方要打折看。

**提升集中在少數題目。** 我用論文 Table 2 自己加了一下：Opus 增加的那 9.7 個百分點，大約四分之三來自 6 個 benchmark。看中位數，Opus 從 5.6% 到 8.45%。平均接近翻倍，典型的那一題沒有翻倍。

**洞見型的提升很看運氣。** 作者在沒有 Harness 的設定下把 PFDelta 重跑了四次：64.4、65.3、32.5、29.4，平均 47.9 ± 19.6，只有兩次找到 loss 重構。工程型的提升就很穩，Mars-Bench 重跑四次是 45.9 ± 1.5。而加了 Harness 的版本，每題只跑了一次，91.0% 裡有多少是 Harness 的功勞、多少是那次剛好走運，論文沒有拆開。

**Harness 也會讓某些題目倒退。** Codex + Skills 在 PFDelta 從 4.6% 變 −12.8%、LITHOS 從 4.8% 變 −10.0%。逼 agent 大膽，有時候它真的會大膽地摔下去。

**時間拉長不會自動變出反射。** 作者讓帶 Harness 的 agent 跑滿三天。在更難的 PFDelta 2000 上，Opus + Skills 前 12 小時換了一輪 GNN 架構，之後 60 小時分六輪調學習率，最後 88%。在 CarbonGlobe 上，Codex + Skills 近 40 小時沒進展，最後訓練 80–100 個架構做 ensemble，validation 好 37%，held-out test 反而倒退 25%。每小時的自檢能延後原地打轉，不能消除它。

**「大力出奇蹟」也不完全公平。** 作者另外測了只准用 Optuna 調超參、不准改架構和 loss 的版本，同樣 8 張 H200、12 小時：CheMixHub 11.9 vs 1.4、Mars-Bench 46.4 vs 4.3、PFDelta 64.4 vs 4.6。agent 做的是工程，不是亂槍打鳥。

**沒有人類研究員對照，skill 也可能過擬合。** 作者找不到對的領域專家花夠長時間做同樣的事；三份 skill 是看 Claude Code 的軌跡設計的，換到別的領域、別的 agent，效果要自己測。另外，評分和稽核預設也是 Opus 4.6，作者有另外找三個不同 agent 重新稽核一半的 run，結論一致。

---

## 關鍵洞察

**卡住的時候，先加 Harness，再加算力。** 同樣 8 張 H200、12 小時，三份 skill 加一支 hook，Opus 的平均相對提升從 10.4% 變 20.1%。

**反省要做成鎖，不要做成提醒。** 寫在 prompt 裡的「記得反省」沒有東西保證會被執行；hook 每 3600 秒把 Skill 以外的工具全部擋掉，agent 才真的會停下來。

**把「無效實驗」寫成清單。** 重跑 baseline、多 seed、seed ensemble 這些最省力的路，直接列出來禁止，比叫 agent「要有創意」具體得多。

**評分權不能留在爬山的人手上。** 原始設定下 12 題有 5 題被鑽。用 agent 跑任何「自己做、自己量」的任務，先把驗收拆出去。

經常拿 Claude Code 或 Codex 跑實驗的朋友，這篇很值得讀。

你平常跑實驗卡住的時候，第一個動作是加機器，還是先回去重想題目？

---

## 常見問題 Q&A

**Q: Agent4Sci 是什麼？**

Agent4Sci 是 Anthropic Fellows Program 與 Anthropic 研究員在 2026 年 10 月發表的研究（arXiv 2610.28763，NeurIPS 2026 Evaluations and Datasets track），測試 AI agent 能不能自己做科學研究。它收錄 20 個 ML for Science benchmark、11 個科學領域，讓 Claude Code、Codex、Gemini CLI 在 8 張 H200、12 小時內，把原論文發表的最好結果往上推，這個任務形式叫自動化科學爬山（Automated Scientific Hill-Climbing）。預設設定下 Claude Opus 4.6 平均相對提升 10.4%，但大部分來自調超參、改架構這類 ML 工程技巧。

**Q: 什麼是「科研 Harness」？Agent4Sci 加了什麼？**

Harness 指的是包在 AI 模型外面、規定它怎麼工作的那一層：工具、規則、流程和檢查機制。Agent4Sci 加了三份 skill（Agent Skills）：科研構思 102 行、實驗管理 112 行、定時自檢 63 行，加起來 277 行；再加一支 Claude Code 的 PreToolUse hook，每 3600 秒觸發一次，觸發後除了 Skill 以外的工具都被擋下，直到 agent 跑完自檢清單。模型沒換、算力沒加，Claude Opus 的平均相對提升從 10.4% 變成 20.1%，Codex 從 4.4% 變成 8.1%。

**Q: AI agent 做科學研究最常犯哪些錯？**

論文從軌跡整理出三個反覆出現的毛病。第一是高估新穎性（Novelty Miscalibration），例如 Claude 把幾乎人人預設會開的 cosine 學習率排程當成創意突破。第二是資源閒置（Resource Under-utilization），8 張 H200 常常有卡閒著，能平行的實驗被排成串行。第三是探索收斂（Exploration Collapse），找到一個有效方向後就一直在附近調 seed 和學習率，不再嘗試其他做法。

**Q: 為什麼「請你多想一點」沒用，但 Harness 有用？**

「請你多想一點」只是 prompt，模型可以忽略，也可以寫完「我正在做有創意的實驗」之後繼續調參數。Agent4Sci 的 Harness 是拿掉選項：科研構思在文獻回顧跑完之前禁止碰 codebase，實驗管理直接列出重跑 baseline、多 seed、seed ensemble 等不准做的實驗，定時自檢用 PreToolUse hook 每 3600 秒把 Skill 以外的工具擋下（exit 2），agent 只剩做自檢這條路。效果不是來自文字寫得多好，而是來自其他路被堵住。

**Q: 加了 Harness 之後，AI 就會做真正的科研嗎？**

會更常碰到真正的領域洞見，但不保證。在電網題目 PFDelta 上，加了 Harness 的 Claude Opus 認出評分指標可以從克希荷夫定律推出來，把它改成主要訓練目標，進步從 64.4% 變成 91.0%。但同一題沒有 Harness 重跑四次，只有兩次想到類似的關鍵改法；Codex 加了 Harness 在這題反而從進步 4.6% 變成退步 12.8%；跑滿三天的 Opus 在第 12 小時之後還是回到調學習率。程式碼在 github.com/maszhongming/agent4sci（Apache 2.0），可以拿來改，但 skill 是照 Claude Code 的軌跡設計的，換領域要自己測。

---

## 來源

- Ming Zhong, Stacy Li, Nicholas Carlini, Matthew Jagielski，[Automating ML for Science: Can Frontier Agents Climb Scientific Hills in the Wild?](https://arxiv.org/abs/2610.28763)（arXiv 2610.28763，2026-10-20，NeurIPS 2026 Evaluations and Datasets track）
- [maszhongming/agent4sci](https://github.com/maszhongming/agent4sci)（程式碼、skill、hook 設定）
- [Hugging Face 資料集 MingZhong/agent4sci](https://huggingface.co/datasets/MingZhong/agent4sci)
