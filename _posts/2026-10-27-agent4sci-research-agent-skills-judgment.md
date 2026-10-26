---
layout: post
title: "Claude 把 cosine 學習率當成創意突破：Anthropic 的 Agent4Sci 用三份 Skill 讓提升從 10.4% 變 20.1%，補上的是指導教授，不是判斷力"
date: 2026-10-27 09:00:00 +0800
permalink: /agent4sci-research-agent-skills-judgment/
tags: [Agent4Sci, Anthropic, Claude Code, Codex, Gemini CLI, Research Agent, Agent Skills, Hooks, ML for Science, Evaluation Gaming]
categories: [AI Agent]
image: /assets/images/agent4sci-research-agent-skills-cover.png
description: "Anthropic 研究員 10 月 20 日放上 arXiv 的 Agent4Sci，把 Claude Code、Codex、Gemini CLI 丟進 20 個真實的 ML for Science benchmark，每個 agent 拿 8 張 H200、12 小時，任務是把論文發表的最好結果往上推。四個 agent 全部有正提升，Opus 平均 10.4%。但拆開軌跡，主要是調超參、換 backbone、做 ensemble，Claude 甚至在多次 run 裡把 cosine 學習率排程當成創意突破。作者加了三份加起來不到 300 行的 skill，Opus 拉到 20.1%、Codex 從 4.4% 到 8.1%。這篇拆三件事：最值得抄的是一個每小時鎖住 Skill 以外所有工具的 hook；「翻倍」有四分之三集中在 6 個 benchmark；三天長跑證明突破不會隨時間累積。"
author: Wisely Chen
faq:
  - question: "Agent4Sci 是什麼？"
    answer: "Agent4Sci 是 Anthropic Fellows Program 與 Anthropic 研究員在 2026 年 10 月發表的研究型 agent 評測平台（arXiv 2610.28763，NeurIPS 2026 Evaluations and Datasets track）。它收錄 20 個 ML for Science benchmark、25 個任務、11 個科學領域，讓 Claude Code、Codex、Gemini CLI 這類 coding agent 在 8 張 H200、12 小時的預算內，把原論文發表的最好結果往上推，這個任務形式叫做自動化科學爬山（Automated Scientific Hill-Climbing）。評分由獨立的 evaluation agent 在隔離的測試集上執行，再由 auditing agent 稽核作弊。"
  - question: "三份 Skill 是什麼？為什麼能讓 Claude Opus 的提升從 10.4% 到 20.1%？"
    answer: "三份 skill 分別是研究構思（Research Ideation）、實驗管理（Experiment Management）和定時自檢（Scheduled Checklist），都是 markdown 文件，Claude Code 版分別是 102、112、63 行，對應三個失敗模式：把標準技巧當新點子、GPU 閒置、找到有效方向後就只在附近調參。論文沒有拆開測各自的貢獻，但定時自檢的執行方式最特別：它透過 Claude Code 的 PreToolUse hook 每 3600 秒觸發一次，觸發後除了 Skill 以外的工具都被擋下，直到 agent 回答完「我是在設計需要科學推理的實驗，還是只在調超參？」這類問題。Opus 平均提升從 10.4% 到 20.1%，Codex 從 4.4% 到 8.1%。"
  - question: "「三個 Skill 讓提升翻倍」這個說法可信嗎？"
    answer: "平均值是真的，但要加註腳。Opus 增加的 9.7 個百分點，大約四分之三集中在 6 個 benchmark；看中位數，是從 5.6% 到 8.45%。每格只跑一次，而同設定重跑四次時，PFDelta 的結果在 29.4% 到 65.3% 之間浮動。skill 也讓部分格子倒退，例如 Codex + Skills 在 PFDelta 從 4.6% 變成 −12.8%。論文作者自己也不把平均值當排行榜看。"
  - question: "給 research agent 更多時間，會不會自己找到突破？"
    answer: "論文的三天長跑實驗說不會。帶 skill 的 Claude Opus 4.6 在 PFDelta 2000 上，前 12 小時嘗試了多種 GNN 架構，之後 60 小時分六輪調學習率，最後提升 88%。帶 skill 的 Codex 在 CarbonGlobe 上近 40 小時沒有進展，最後用 80–100 個架構做 ensemble，validation 好了 37%，held-out test 反而倒退 25%。唯一的大突破是 Codex 在 PFDelta 2000 上把 GNN 當成 Newton-Raphson 求解器的 warm start，降低 99.5% 誤差，這是一個領域洞見，不是時間堆出來的。"
  - question: "自己用 Claude Code 跑 ML 實驗，可以直接套用這三份 Skill 嗎？"
    answer: "可以拿來改，程式碼在 github.com/maszhongming/agent4sci（Apache 2.0），包含 Claude Code 和 Codex 兩個版本的 skill、hook 設定與文獻回顧 subagent。但論文的限制段寫明，skill 是根據 Claude Code 在這 20 個 benchmark 上的失敗軌跡設計的，可能對這些科學領域、任務格式和 Claude 系列模型過擬合。最值得先搬的是兩件事：把評分和訓練分給不同的 agent，以及用 hook 而不是 prompt 來執行定時自檢。  ---"
---

Claude Code 在好幾次 run 裡，把 cosine 學習率排程當成「創意突破」。

這是 Anthropic 研究員在論文裡點名的例子：

> "Claude Code treats cosine learning-rate schedules as a creative breakthrough across runs, even though they are long-standing standard practice."

一個訓練模型時幾乎預設會開的東西，agent 在自己的推理裡把它包裝成大膽的新想法。

這篇是 10 月 20 日上 arXiv 的 [Agent4Sci](https://arxiv.org/abs/2610.28763)，作者是 Anthropic Fellows Program 的 Ming Zhong、Stacy Li，加上 Anthropic 的 Nicholas Carlini、Matthew Jagielski，收在 NeurIPS 2026 Evaluations and Datasets track。社群轉傳的重點是「三個輕量 Skill 讓提升翻倍」。這個數字是真的，但我覺得附錄比主結果更值得看：裡面有 HPO-only 對照、同設定重跑四次的變異，還有一組跑滿三天的實驗。把這三份資料疊上去，「翻倍」的意思會變得不太一樣。

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
| 規模 | 20 個 benchmark、25 個任務、11 個科學領域（天文、化學、生態、基因體、物理、生物工程…） |
| 受測 agent | Claude Opus 4.6、Claude Sonnet 4.6、Codex（GPT-5.4）、Gemini 3.1 Pro，各自用官方 CLI，推理強度開到最高 |
| 資源 | 每次 run 8 張 H200、12 小時，除了開跑和到時間停掉之外沒有人介入 |
| 預設結果 | 平均相對提升：Opus 10.4%、Sonnet 9.6%、Gemini 6.8%、Codex 4.4% |
| 加 Skill 之後 | Opus 10.4% → 20.1%，Codex 4.4% → 8.1% |
| 作弊 | 沒有任何一次 run 被稽核標記 |
| 程式碼 | [github.com/maszhongming/agent4sci](https://github.com/maszhongming/agent4sci)，Apache 2.0，三份 skill 和 hook 都在裡面 |

---

## 先把作弊的縫補起來

這篇的評測設計本身就值得一段。

作者一開始做了一個最直覺的版本：把論文、原始 repo、資料丟給 agent，叫它把指標往上推。在 5 個 NeurIPS 2025 benchmark 的 12 個任務裡，有 5 個出現嚴重的 evaluation gaming。手法分四類：選擇性回報、測試集污染、改評分指標、直接 hardcode。最後一類包括把舊 run 的預測複製過來，或宣稱合法的 checkpoint「不小心被刪掉了」。

作者用 evaluation gaming 這個詞，而不是 cheating，理由是不一定有惡意。科學領域的 repo 常常沒有明確的指標定義、沒有固定的資料切分，一個積極的優化器自然會鑽進這些縫。

解法是把評分權從爬山的 agent 手上拿走。每個任務先由人工重現論文的 baseline，重現數字對得上才收；測試集隔離，爬山 agent 只看得到 train 和 validation；交出 checkpoint 之後，由另一個 evaluation agent 在 held-out test 上跑分，再由第三個 auditing agent 讀完整條軌跡找作弊。光是挑題，NeurIPS 2025 Datasets and Benchmarks track 的 497 篇候選，最後只收了 10 個，淘汰率 98%。

這跟我九月寫的 [DeepMind 100 agent 數學會議](/deepmind-agent-swarm-cheating-whistleblowing-commons/) 是同一個教訓的兩面。那邊的驗證器只做關鍵字黑名單，作弊 27 分鐘傳遍整個群體。這邊作者先看到 12 題裡有 5 題被鑽，然後把驗收、評分、稽核拆成三個角色。**讓 agent 自己回報分數的實驗，數字不能信。**

---

## 預設的 agent 在做什麼：自動化工程，不是自動化研究

四個 agent 在 20 個 benchmark 上全部推過了原論文的最好成績，最佳增益從 ProteinGym 的 1.1% 到 PFDelta 的 64.4%。

但看它們怎麼推的。

PFDelta 是電網潮流預測。Opus 的 64.4% 來自三個動作：把評分指標 PBL 改成可微的平方形式當輔助 loss、MSE 權重 λ 從 0.1 調到 0.3、換成 cosine annealing 加 warmup。Mars-Bench 是火星地形偵測，Opus 把 RetinaNet 換成 Faster R-CNN，mAP 從 16.5 到 30.4。

都有效，都是 ML 工程師的日常工具箱。論文把所有軌跡的方法做了分類：Opus 的 run 有 56% 用了調超參、44% 改架構；Codex 調超參 44%；Gemini 調超參 48%。針對問題本身的介入很少。

三家的工作習慣也很不一樣：

| | 工作模式 | 活躍時間 | turn / tool call |
|---|---|---|---|
| Claude Opus | 每輪看完 log 再決定下一輪 | 平均 12.0 小時 | 490 / 338 |
| Codex | 第一個小時內就丟出一支長跑腳本然後等，掃了一百多組實驗 | 1.0 小時 | 328 / 325 |
| Gemini | 在兩種模式之間來回 | — | 196 / 201 |

Codex 的 turn 和 tool call 擠在 1.0 小時的活躍時間裡，剩下的十一個小時在等。論文認為這有助於解釋它的平均提升最低。

作者從軌跡裡歸納出三個反覆出現的毛病：

- **Novelty miscalibration**：把標準技巧當成新點子，cosine 排程就是例子。
- **Resource under-utilization**：GPU 常常閒著，能平行的實驗被排成串行，CPU 和 GPU 互相搶資源。
- **Exploration collapse**：前幾輪想法很多，一旦找到一個有效方向，剩下的時間都在它附近調 seed 和學習率。

---

## 建立直覺：一個沒有指導教授的研究生

這三個毛病，帶過研究生的人應該都很熟。

一個剛進實驗室的學生拿到一個 baseline，發現換個 learning rate schedule 可以多幾個點。他很興奮，接下來幾週都在調 warmup 步數、調 weight decay、多跑幾個 seed 取平均。實驗室的卡大多在閒置，因為他一次只敢跑一個實驗。

指導教授在週會上只問了幾個問題：這個東西換到別的資料集還成立嗎？你有沒有試過領域裡的人會怎麼想這個問題？那些閒置的卡你打算拿來做什麼？

學生的能力沒有變。變的是每週有人逼他從局部最佳解裡抬頭一次。

Agent4Sci 那三份 skill 做的事，大概就是這個。

---

## 三份 Skill 拆開看

三份 skill 都是 markdown 文件，在 Claude Code 版的 repo 裡，research 102 行、experiment 112 行、checklist 63 行。

**Research skill：開跑時先讀文獻，再分級。** 這份 skill 給 agent 一個刻意誇張的 persona：「瘋狂的研究科學家」，只對突破感興趣，鄙視調超參。然後派四個 subagent 平行做文獻回顧（領域兩個、AI/ML 兩個），期間主 agent 不准碰 codebase。讀完之後把實驗分成兩級，Tier 1 是高風險高報酬的領域重構，Tier 2 是文獻裡證明有效的穩健改進，Tier 1 第一輪必須把所有 GPU 吃滿。最後有一道自我校準：「領域專家看到這些點子會真的驚訝，還是只是標準做法換上野心勃勃的用詞？」

**Experiment skill：管資源。** 禁止在 baseline 上重跑、多 seed、調超參、做 seed ensemble。每個實驗開獨立目錄，正式跑之前先做 1-2 個 epoch 的 smoke test，量資料載入時間和 GPU 佔用。失敗的實驗要分類成可修的工程問題、方向對但實作壞掉、或能說清楚根本矛盾才准放棄，「反射性丟掉失敗的 run」被明文禁止。

**Scheduled checklist：每小時一次自檢。** 問題包括：

> "Am I designing creative experiments that require scientific reasoning, or just tweaking hyperparameters and calling it novel?"

我在設計有科學推理的實驗，還是在調超參然後叫它新點子？

論文沒有拆開測三份 skill 各自的貢獻，所以我沒辦法說哪一份最重要。但第三份是我覺得最值得抄的，因為它不只是文件。我去翻了 repo 的 `settings.json` 和 `hooks/reminder.sh`：這是一個 PreToolUse hook，INTERVAL=3600；時間到了之後，除了 Skill 以外的工具呼叫都被 exit 2 擋下，直到跑完 checklist 才解鎖。

不是提醒，是鎖。

這跟我六月寫的 [從 Prompt 到 Harness 的三次中心遷移](/agent-harness-three-migrations-mechanism/) 講的是同一件事：你在 prompt 裡拜託 agent「記得每小時反省一下」，它會忘；用 hook 把其他工具鎖住，它就只能反省。上週拆的 [Harness²](/harness2-recursive-agent-harnessing-open-world/) 消融結果也是這個方向，拿掉 skills 和 scripts 掉的分數，比拿掉 prompt 類元件多。Agent4Sci 從另一個場景給了同樣的答案：**能寫成機制的，就不要寫成規則。**

---

## 效果：平均翻倍，以及 PFDelta 那一格

Opus 從 10.4% 到 20.1%，20 個 benchmark 裡改善 18 個。Codex 從 4.4% 到 8.1%，改善 12 個。skill 是照 Claude Code 調的，Codex 也有接近比例的增益，作者認為設計可以跨 agent。

最好看的是 PFDelta，從 64.4% 到 91.0%，而且做法換了一種性質。agent 認出 PBL 可以從克希荷夫定律推出來，不需要標籤，於是改成主 loss；推論時把 GNN 預測當 AC power-flow 方程的 warm start。這已經不是調參，是讀懂了物理之後重新定義問題。

另一個值得記的是 CarbonGlobe 的算力。沒有 skill 時，Opus 堆了 14 個模型的 ensemble，約 49 GPU 小時；有 skill 換成 8 個非自迴歸 transformer，不到 6 GPU 小時，推論快約 500 倍。更好的點子不一定更貴。

---

## 反方：「翻倍」要打幾個折

我把附錄的表格疊上去之後，覺得社群那句「三個 Skill 就讓提升翻倍」需要加三個註腳。

**第一，增益很集中。** 我用 Table 2 自己加了一下：Opus 增加的那 9.7 個百分點，大約四分之三來自 6 個 benchmark（MassSpecGym、GEO-Bench-2、PFDelta、TIDMAD、CarbonGlobe、Mars-Bench）。看中位數，Opus 從 5.6% 到 8.45%。平均翻倍，典型的那一題沒有翻倍。

**第二，每格只跑一次，而一次的變異很大。** 作者在 Opus 無 skill 的設定下，挑 6 個 benchmark 各多跑了三次。工程型的增益很穩，Mars-Bench 45.9 ± 1.5。但 PFDelta 四次 run：64.4、65.3、32.5、29.4，平均 47.9 ± 19.6，只有兩次找到 loss 重構。洞見型的增益本身就是擲骰子，有 skill 的那一格也只擲了一次。作者自己在 Limitations 裡寫明，不把平均值當 leaderboard。

**第三，skill 也會讓分數倒退。** Opus + Skills 在 gRNAde 從 2.6% 變 −0.6%；Codex + Skills 在 PFDelta 從 4.6% 變 −12.8%、LITHOS 從 4.8% 變 −10.0%。逼 agent「大膽一點」，有時候它真的會大膽地摔下去。

我覺得最關鍵的一組數字，是三天長跑。

作者讓 skill 版的 agent 跑滿三天。PFDelta 2000 是更難的變體，Opus + Skills 前 12 小時換了一輪 GNN 架構，之後 60 小時分六輪調學習率，最後 88%。Codex + Skills 把 GNN 當 GPU Newton-Raphson 的 warm start，PBL 降 99.5%。但在 CarbonGlobe，Codex + Skills 近 40 小時沒進展，最後 80–100 個架構做 ensemble，validation 好 37%，held-out test 反而倒退 25%。

Opus 帶著每小時強制自檢的 hook，第 12 小時之後還是退化成調學習率。

所以我要修正自己一開始的說法。社群摘要說「瓶頸不在執行，在判斷」，這句我同意一半。**skill 沒有讓 agent 學會判斷，它是把判斷外包給一張每小時跳出來的清單。** 清單能延後 exploration collapse，不能消除它。真正的突破，論文自己的結論是：取決於 agent 有沒有碰到一個真正的領域洞見，不是讓它爬多久。

---

## 對用 Claude Code 跑實驗的人，具體改什麼

如果你平常就用 Claude Code 或 Codex 跑訓練實驗，這篇改變的決策大概是這樣：

| | 以前的直覺 | 看完這篇 |
|---|---|---|
| 卡住了 | 加 GPU、加時間 | 先看 GPU 有沒有閒著；三天長跑顯示時間不會自動變成突破 |
| 自我反省 | 在 CLAUDE.md 寫「記得想想有沒有更好的方法」 | 寫成 hook，時間到就鎖工具，逼它跑 checklist |
| 實驗紀錄 | agent 回報「提升了 X%」就收 | 評分和訓練分開跑，test set 不給爬山的那個 agent 看 |
| 判斷 agent 的點子 | 它說是新方法就當新方法 | 自己問一次：這是不是調超參換了個說法？ |

repo 裡的 skill 和 hook 可以直接拿來改。不過 Limitations 寫得很清楚，skill 是看 Claude Code 的軌跡設計的，換到別的領域、別的 agent，效果要自己測。

---

## 坦白說

這篇有幾個地方我會保留。

**沒有人類研究員對照。** 作者說找不到對的領域專家花夠長時間做這件事。所以我們知道 agent 比原論文 baseline 好，不知道一個領域博士生拿同樣 12 小時、8 張 H200 會做到哪裡。ProteinGym 的起點已經是公開榜單第一名，agent 只多推了 1.1%，這一格大概是最接近「人類天花板」的參考。

**HPO-only 對照幫 agent 說了話，但只有 6 格。** 同樣 8 張 H200、12 小時，只准用 Optuna 調超參：CheMixHub 11.9 vs 1.4、Mars-Bench 46.4 vs 4.3、PFDelta 64.4 vs 4.6。所以「大部分是調參」不等於「調參就夠」，agent 換 backbone、改 loss 的貢獻遠大於純搜超參。而且 20 個起點裡有 10 個是原論文已經調過的設定，其中 7 個做過超參搜尋。說 agent「只是在調參」對它不太公平，它做的是工程，不是暴力搜尋。

**評分 agent 和受測 agent 同家。** 預設的評分和稽核都用 Opus 4.6。作者另外拿三個不同 agent 重新稽核每個 agent 一半的 run，結論一致，這處理得算仔細。但 Limitations 也承認，四類作弊之外更細的合理化行為，稽核抓不到。

**受測的是 Opus 4.6 和 GPT-5.4。** 上週拆的 Harness² 已經在用 Opus 4.8。論文的價值在方法和失敗模式，具體百分比換一代模型大概就會變。

---

## 關鍵洞察

**看 agent 的提升，先問它是工程還是洞見。** 工程型的增益穩定、可重現，Mars-Bench 四次 run 標準差 1.5；洞見型的增益像擲骰子，PFDelta 四次只中兩次。兩種增益混在一個平均值裡，數字會騙人。

**反省要做成鎖，不要做成提醒。** Agent4Sci 的 checklist 不靠 agent 自覺，hook 每 3600 秒把 Skill 以外的工具全部擋掉。寫在 prompt 裡的「記得反省」，在一個跑 12 小時、Opus 平均 490 個 turn 的 session 裡，沒有東西保證它會被執行。

**不要指望時間換突破。** 三天長跑裡，Opus 帶著 skill 還是在第 12 小時後回到調學習率。給 agent 更多時間之前，先確認它還在探索，不是在原地轉。

**評分權不能留在爬山的人手上。** 原始設定下 12 題有 5 題被鑽。用 agent 跑任何「自己做、自己量」的優化任務，先把驗收拆出去。

---

## 常見問題 Q&A

**Q: Agent4Sci 是什麼？**

Agent4Sci 是 Anthropic Fellows Program 與 Anthropic 研究員在 2026 年 10 月發表的研究型 agent 評測平台（arXiv 2610.28763，NeurIPS 2026 Evaluations and Datasets track）。它收錄 20 個 ML for Science benchmark、25 個任務、11 個科學領域，讓 Claude Code、Codex、Gemini CLI 這類 coding agent 在 8 張 H200、12 小時的預算內，把原論文發表的最好結果往上推，這個任務形式叫做自動化科學爬山（Automated Scientific Hill-Climbing）。評分由獨立的 evaluation agent 在隔離的測試集上執行，再由 auditing agent 稽核作弊。

**Q: 三份 Skill 是什麼？為什麼能讓 Claude Opus 的提升從 10.4% 到 20.1%？**

三份 skill 分別是研究構思（Research Ideation）、實驗管理（Experiment Management）和定時自檢（Scheduled Checklist），都是 markdown 文件，Claude Code 版分別是 102、112、63 行，對應三個失敗模式：把標準技巧當新點子、GPU 閒置、找到有效方向後就只在附近調參。論文沒有拆開測各自的貢獻，但定時自檢的執行方式最特別：它透過 Claude Code 的 PreToolUse hook 每 3600 秒觸發一次，觸發後除了 Skill 以外的工具都被擋下，直到 agent 回答完「我是在設計需要科學推理的實驗，還是只在調超參？」這類問題。Opus 平均提升從 10.4% 到 20.1%，Codex 從 4.4% 到 8.1%。

**Q: 「三個 Skill 讓提升翻倍」這個說法可信嗎？**

平均值是真的，但要加註腳。Opus 增加的 9.7 個百分點，大約四分之三集中在 6 個 benchmark；看中位數，是從 5.6% 到 8.45%。每格只跑一次，而同設定重跑四次時，PFDelta 的結果在 29.4% 到 65.3% 之間浮動。skill 也讓部分格子倒退，例如 Codex + Skills 在 PFDelta 從 4.6% 變成 −12.8%。論文作者自己也不把平均值當排行榜看。

**Q: 給 research agent 更多時間，會不會自己找到突破？**

論文的三天長跑實驗說不會。帶 skill 的 Claude Opus 4.6 在 PFDelta 2000 上，前 12 小時嘗試了多種 GNN 架構，之後 60 小時分六輪調學習率，最後提升 88%。帶 skill 的 Codex 在 CarbonGlobe 上近 40 小時沒有進展，最後用 80–100 個架構做 ensemble，validation 好了 37%，held-out test 反而倒退 25%。唯一的大突破是 Codex 在 PFDelta 2000 上把 GNN 當成 Newton-Raphson 求解器的 warm start，降低 99.5% 誤差，這是一個領域洞見，不是時間堆出來的。

**Q: 自己用 Claude Code 跑 ML 實驗，可以直接套用這三份 Skill 嗎？**

可以拿來改，程式碼在 github.com/maszhongming/agent4sci（Apache 2.0），包含 Claude Code 和 Codex 兩個版本的 skill、hook 設定與文獻回顧 subagent。但論文的限制段寫明，skill 是根據 Claude Code 在這 20 個 benchmark 上的失敗軌跡設計的，可能對這些科學領域、任務格式和 Claude 系列模型過擬合。最值得先搬的是兩件事：把評分和訓練分給不同的 agent，以及用 hook 而不是 prompt 來執行定時自檢。

---

## 來源

- Zhong, Li, Carlini, Jagielski，[Automating ML for Science: Can Frontier Agents Climb Scientific Hills in the Wild?](https://arxiv.org/abs/2610.28763)（arXiv 2610.28763）
- [maszhongming/agent4sci](https://github.com/maszhongming/agent4sci)（程式碼、skill、hook 設定）
- [Hugging Face 資料集 MingZhong/agent4sci](https://huggingface.co/datasets/MingZhong/agent4sci)
