---
layout: post
title: "一篇 PACT 2025 論文，把 Loop Engineering 的每個論點都做了 Ablation Study"
date: 2026-06-30 09:00:00 +0800
permalink: /compilot-loop-engineering-academic-proof/
description: "Loop Engineering 有沒有科學化的方式證明有用？NYU Abu Dhabi 在 PACT 2025 發表的 ComPilot 論文，讓 LLM 當 agent 去優化 compiler loop nest——在人類當中算是超難的任務——然後做了 6 組 ablation study。移除 feedback loop 效能掉 23-40%。64% 的提案是錯的但系統照樣快了 2.66 倍。通用模型打敗專用 coding 模型。最後一個發現讓我想到王陽明：你不需要一開始就有精細的 system prompt，loop 本身收集的 data 就是最佳的 context。執行本身就是一種最好的學習。"
image: /assets/images/compilot-loop-engineering-proof.png
categories: [AI Coding, Agent Engineering]
author: Wisely Chen
---

## Loop Engineering 有沒有科學化的方式證明有用？

又到了週二看論文的時間。

Loop Engineering 系列我寫了三篇。[第一篇](/loop-engineering-from-prompt-to-loop-paradigm-shift/)拆概念和邊界、[第二篇](/loop-engineering-five-plus-one-implementation-guide/)講五個組件的實作、[第三篇](/loop-engineering-buzzword-video-transcript/)在高鐵上錄了一段影片講判斷標準。全是實務經驗。

好用，但沒有任何理論知識支撐。也沒有 ablation study。沒有人用科學的方式告訴你 loop 為何要這樣設計，或是「把 feedback loop 拿掉會怎樣」「多跑幾輪的邊際收益到底是多少」。

直到我讀到 NYU Abu Dhabi 在 PACT 2025 發表的 [ComPilot](https://arxiv.org/abs/2511.00592) 論文。

---

## ComPilot：用 LLM 當 Agent 優化 Compiler Loop

他們讓 LLM 當 agent 優化 compiler 的 loop nest。

這在人類當中算是超難的任務。你要同時搞懂演算法的依賴結構、目標硬體的 cache hierarchy 和指令管線特性，然後從 9 種轉換（tiling、parallelization、fusion、interchange、unrolling、skewing、shifting、reversal、3D tiling）裡選出正確的組合——每種都有參數要調，而且順序會影響結果，先 fusion 再 tiling 跟先 tiling 再 fusion 完全不同。組合爆炸到 senior compiler engineer 手動調一個 kernel 可能花好幾天。自動化工具 Pluto 用多面體分析做了幾十年，也沒能通吃所有場景。

他們用另一個 compiler（Tiramisu）當護欄做驗證，跑了 PolyBench 的 30 個 kernel、5 種 input size，總共 150 個測試實例，測了 8 個不同的 LLM。

然後做 ablation study——把系統裡的某一塊移除掉，看看會怎樣。

---

## Ablation Study 的結果

以下是讓我印象最深的五組數據。

### 數據一：移除 Feedback Loop，效能掉 23-40%

同一個系統，有 feedback 的版本讓 LLM 收到每一輪的成敗和加速比，沒 feedback 的版本讓 LLM 每次獨立提案。

| 模式 | Gemini 2.0 Flash | GPT-4o |
|------|-------------------|--------|
| With Feedback | 2.66x | 2.63x |
| Without Feedback | 2.01x | ~1.6x |
| **差距** | **23%** | **~40%** |

結果效能狂掉。

論文原文說得直接：「essentially performs blind, open-loop search.」

Feedback 不是讓模型變聰明，是讓它能累積搜索空間的資訊，避免重複犯錯。沒有 feedback 的 loop 就是盲猜。

### 數據二：64% 的提案是錯的，但系統照樣快了 2.66 倍

30 輪迭代中，合法可執行的提案只有 36.1%。語法/語義錯誤佔 31.4%，違反依賴關係佔 32.5%。

將近三分之二是錯的。

但 compiler 當護欄攔住了所有違法提案，LLM 從失敗回饋中逐步學會約束條件——第一輪非法率 60%，到第三十輪降到 30-40%。不靠 fine-tuning，靠 in-context learning。護欄的存在讓 36% 的成功率就夠用了。

這代表設計良好的 Harness 護欄可以讓整個系統變 robust。不是因為 AI 不會犯錯，是因為系統能容忍錯誤、從錯誤中學習、逐步收斂到好的解。沒有 compiler 當護欄，36% 的成功率根本不夠用。有了護欄，36% 就夠了。

### 數據三：通用模型打敗專用 Coding 模型

| 模型 | 類型 | Single Run | Best-of-5 |
|------|------|------------|-----------|
| Gemini 2.0 Flash | 通用 | 2.66x | 3.54x |
| GPT-4o | 通用 | 2.63x | 3.26x |
| LLaMA 3.3 70B | 通用 | 2.47x | 3.08x |
| QwQ 32B | 推理 | 2.36x | 2.94x |
| Qwen2.5-Coder 32B | Coding 專用 | 2.14x | 3.00x |
| Gemma3 27B | 通用 | 2.03x | 2.58x |
| Codestral 22B | Coding 專用 | 1.75x | 2.30x |

Gemini 2.0 Flash（2.66x）和 GPT-4o（2.63x）明顯贏過 Qwen2.5-Coder（2.14x）和 Codestral（1.75x）。

在 Loop Engineering 的場景下，「理解任務、分析回饋、調整策略」的能力比「寫出語法正確的程式碼」更重要。模型需要的是推理能力，不是背誦 pattern 的能力。

### 數據四：收益遞減的曲線

| 迭代次數 | 加速比 | 邊際增益 |
|----------|--------|----------|
| T=1 | 1.41x | — |
| T=5 | 1.83x | +0.42x |
| T=10 | 2.06x | +0.23x |
| T=15 | 2.32x | +0.26x |
| T=20 | 2.49x | +0.17x |
| T=25 | 2.58x | +0.09x |
| T=30 | 2.66x | +0.08x |
| T=75 | 3.06x | +0.40x（但多花了 45 輪） |

前 10 輪每輪都有顯著進步。T=30 之後多跑 45 輪只多拿 0.40x。Multi-run 也一樣——K=5 是 3.54x，K=13 是 3.82x，多跑 8 次只多拿 0.28x。

不是迭代越多越好，是要找到收益曲線的甜蜜點。不能太少（達不到效果），不能太多（效益太低，token 經濟賬算不過來）。

所以你在設計 stop condition 的時候，這件事非常重要。

### 數據五：一開始的 Context 對決策的影響趨近於零

ComPilot 的 prompt 包含完整硬體規格——CPU 型號、48 thread、128GB RAM、cache 大小。但是經過 loop 之後，把這些資訊拿掉呢？

沒有統計顯著的差異。

在有 feedback 的 loop 裡，過度精細的 context 可能沒你想的那麼重要。每一輪的執行結果本身就在告訴 agent 環境的特性。Loop 本身收集的 data，就是一種最佳的 context。

---

## 為什麼選 Compiler 場景？

首先，這只是其中一個場景。

論文為什麼選 compiler loop optimization？因為學術論文需要可重現、可量化的實驗。Compiler 的驗證參數極度乾淨——合法性是 binary judgment，效能是精確數字。這讓結論非常數據導向。

但你不能直接把這些數字搬到你的場景裡。你的 loop 沒有 binary judgment，你的 refactor loop 靠 test suite 間接推斷。

不過方向性的結論依然成立。

---

## Loop Engineering 不是讓 AI 跑很多次

從這篇論文的 ablation study，我看到三個跨場景依然成立的結論：

1. **設計良好的 feedback loop 比 open-loop 好。** 移除 feedback 效能掉 23-40%，這不是邊際差異。
2. **護欄比換模型重要。** 64% 的提案失敗但系統仍達 2.66x。設計良好的 Harness 讓低成功率也能收斂。
3. **迭代有收益遞減，stop condition 要好好設計。** 不能太少，不能太多，要找到甜蜜點。

最後一點。

你不需要一開始就有精細的 system prompt。Loop 本身收集的 data，就是一種最佳的 context。

放在人身上，執行本身就是一種最好的學習。

這不就是王陽明說的知行合一？

每次讀 LLM 論文，都可以讀到人生的道理。

---

**延伸閱讀：**
- [Loop Engineering：不再 Prompt Agent，改設計 Loop 讓 Agent Prompt Agent](/loop-engineering-from-prompt-to-loop-paradigm-shift/)
- [Loop Engineering 實作指南：五個組件 + 一個記憶體，讓 Agent 自己跑起來](/loop-engineering-five-plus-one-implementation-guide/)
- [影片逐字稿｜Loop Engineering 是真趨勢還是 Buzzword？](/loop-engineering-buzzword-video-transcript/)
- [Harness Engineering 架構全景](/harness-engineering-architecture-overview-ai-code-production-guardrails/)

**論文原文：** Merouani, M., Kara Bernou, I., & Baghdadi, R. (2025). Agentic Auto-Scheduling: An Experimental Study of LLM-Guided Loop Optimization. PACT 2025. arXiv:2511.00592v2.
