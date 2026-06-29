---
layout: post
title: "一篇 PACT 2025 論文，把 Loop Engineering 的每個論點都做了 Ablation Study"
date: 2026-06-30 09:00:00 +0800
permalink: /compilot-loop-engineering-academic-proof/
image: /assets/images/compilot-loop-engineering-proof.png
description: "我在 Loop Engineering 系列講了三篇：feedback loop 是核心、stop condition 要設好、可量化 metric 是前提、模型不是重點架構才是。這些全是實務經驗。然後我讀到 NYU Abu Dhabi 這篇 ComPilot 論文——他們讓 LLM 當 agent 去優化 compiler loop nest，用 Tiramisu compiler 當護欄做驗證，跑了完整的 ablation study。結果？移除 feedback loop 效能掉 23-40%。通用模型打敗專用 coding 模型。LLM 64% 的提案都是錯的，但系統照樣快了 2.66 倍。每一個數據點都在講同一件事：Loop 的工程設計比裡面跑的模型重要。"
---

Loop Engineering 系列寫到第三篇的時候，我一直有個心結：我講的東西全是實務經驗和社群觀察。Peter Steinberger 開 50 個 Codex 並行、Karpathy 用 630 行 Python 跑 700 次實驗——這些都是「某個很厲害的人做了某件事，效果不錯」。

好用嗎？好用。但你要我拿出 ablation study 證明「移除 feedback loop 會怎樣」、「多跑幾輪的邊際收益是多少」——我拿不出來。

然後我讀到這篇論文。

---

## ComPilot：用 LLM 當 Agent 優化 Compiler Loop

NYU Abu Dhabi 的團隊在 PACT 2025（平行架構與編譯技術頂會）發表了一篇叫 [ComPilot](https://arxiv.org/abs/2511.00592) 的論文。他們做的事情用一句話講完：

**讓 LLM 當 agent，反覆提案怎麼優化一段程式的 loop nest，compiler 驗證提案是否合法、量測加速比，然後把結果回饋給 LLM 讓它修正策略。**

這裡的「loop」有雙重含義。字面上，他們在優化 compiler 裡的迴圈結構——tiling、parallelization、fusion 這些。但更重要的是，整個系統本身就是一個 feedback loop：LLM 提案 → compiler 驗證 → 回饋成敗 → LLM 修正 → 再來一輪。

他們用 Tiramisu compiler 當護欄，跑 PolyBench 的 30 個 kernel、5 種 input size，總共 150 個測試實例。測了 8 個不同的 LLM。然後——這是我最在意的部分——他們做了完整的 ablation study，逐一拆解系統裡每個設計決策的貢獻。

---

## 數據一：移除 Feedback Loop，效能掉 23-40%

我在[第一篇](/loop-engineering-from-prompt-to-loop-paradigm-shift/)就講過：Loop Engineering 的核心不是讓 agent「跑很多次」，是讓每一次的結果回饋到下一次的決策裡。沒有 feedback 的重複執行只是 brute-force search。

ComPilot 的 ablation 直接驗證了這件事。

他們把同一個系統分成兩種模式：

- **With Feedback：** LLM 收到 compiler 的驗證結果（成功/失敗/加速比），用完整對話歷史做 in-context learning
- **Without Feedback：** LLM 每次獨立提案，不知道之前的結果

| 模式 | Gemini 2.0 Flash | GPT-4o |
|------|-------------------|--------|
| With Feedback | 2.66x | 2.63x |
| Without Feedback | 2.01x | ~1.6x |
| **差距** | **23%** | **~40%** |

論文原文的結論是：「Lack of feedback prevents LLM from using ICL capabilities to learn from mistakes or successes... essentially performs blind, open-loop search.」

開放迴路的搜索。盲猜。

這不是說 feedback 讓模型「變聰明」了。是 feedback 讓模型能把整個搜索空間的資訊累積起來，避免重複犯錯。你想像一個人在黑暗中找出口——一個記得每次撞牆的位置，一個不記得。走的步數可能一樣多，但結果完全不同。

---

## 數據二：LLM 64% 的提案是錯的，但系統照樣快了 2.66 倍

這個數據是我覺得整篇論文最重要的一個。

在 30 輪迭代中，LLM 提案的平均結果分布：

| 類別 | 比例 |
|------|------|
| 合法且可執行 | 36.1% |
| 語法/語義錯誤（Invalid） | 31.4% |
| 違反依賴關係（Illegal） | 32.5% |

**將近三分之二的提案是錯的。**

但系統的最終結果是 2.66 倍加速（single run），best-of-5 達到 3.54 倍，在多數案例中打敗了傳統的 Pluto 多面體優化器。

這告訴我們什麼？

**Loop 的價值不在於每一輪都做對，而在於系統能容忍錯誤、從錯誤中學習、逐步收斂到好的解。** Compiler 當護欄攔住了所有違法的提案（不會真的生成錯誤的程式碼），LLM 從失敗回饋中學到哪些轉換會違反依賴關係，下一輪就換方向。

第一輪的非法提案率是 60%。到第三十輪降到 30-40%。LLM 在迴圈裡學會了 compiler 的約束條件，不是透過 fine-tuning，而是透過 in-context learning。

我在 [Harness Engineering 系列](/harness-engineering-architecture-overview-ai-code-production-guardrails/) 裡一直在講的「護欄」概念——讓 AI 大膽嘗試，但用系統攔住危險操作——在這裡被量化了。沒有 compiler 當護欄，36% 的成功率根本不夠用。有了護欄，36% 就夠了。

---

## 數據三：通用模型打敗專用 Coding 模型

這個結果可能會讓很多人意外。

| 模型 | 類型 | Single Run | Best-of-5 |
|------|------|------------|-----------|
| Gemini 2.0 Flash | 通用 | 2.66x | 3.54x |
| GPT-4o | 通用 | 2.63x | 3.26x |
| LLaMA 3.3 70B | 通用 | 2.47x | 3.08x |
| QwQ 32B | 推理 | 2.36x | 2.94x |
| Qwen2.5-Coder 32B | Coding 專用 | 2.14x | 3.00x |
| Gemma3 27B | 通用 | 2.03x | 2.58x |
| Codestral 22B | Coding 專用 | 1.75x | 2.30x |

**Gemini 2.0 Flash 和 GPT-4o 這兩個通用模型，在 single run 上明顯打敗了 Qwen2.5-Coder 和 Codestral 這些專門為寫程式訓練的模型。**

Codestral 的可執行提案率只有 15%，Gemini 和 GPT-4o 在 36-38% 左右。

這跟我們在 AI Coding 實務中觀察到的現象一致：在 agentic 的場景下，「理解任務、分析回饋、調整策略」的能力比「寫出語法正確的程式碼」更重要。ComPilot 的 LLM 根本不寫程式碼——它只提出轉換指令（「把 L0 並行化，L1 和 L2 做 32x32 tiling」），程式碼由 compiler 生成。

模型需要的是推理能力和遵循指令的能力，不是背誦程式碼 pattern 的能力。

---

## 數據四：Stop Condition 與收益遞減

我在[影片裡](/loop-engineering-buzzword-video-transcript/)講過：做 Loop Engineering 之前要先過三關，其中一關是「Stop Condition 設好了沒」。ComPilot 的數據把收益遞減的曲線畫得很清楚：

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

從 T=1 到 T=10，每一輪都有顯著進步。T=10 到 T=30，邊際收益快速遞減。T=30 之後，多跑 45 輪只多拿 0.40x。

Multi-run 的收益遞減更明顯：

| 執行次數 | 加速比 | 邊際增益 |
|----------|--------|----------|
| K=1 | 2.66x | — |
| K=5 | 3.54x | +0.88x |
| K=10 | 3.75x | +0.21x |
| K=13 | 3.82x | +0.07x |

K=5 到 K=13 之間，多跑了 8 次只多拿 0.28x。

論文選了 T=30、K=5 作為他們的標準配置，理由是「reasonable balance between optimization time and achieved speedup」。每個 benchmark 平均跑 8.9 分鐘，其中 78.5% 的時間花在 compiler 端（驗證、編譯、執行），LLM 通訊只佔 1-3 分鐘。

這給了我們一個設計 loop 的實用原則：**不是迭代越多越好，而是要找到收益曲線的拐點。** 在 ComPilot 的案例裡，10-30 輪是甜蜜區。超過這個範圍，你花的算力和時間換不到等比的改善。

---

## 數據五：讓 LLM 直接寫程式碼，比「提案+驗證」更差

ComPilot 的設計有一個關鍵選擇：LLM 不直接生成優化過的程式碼，它只提出轉換指令（schedule），由 compiler 負責生成程式碼和驗證正確性。

論文測試了反過來的做法——讓 LLM 直接生成轉換後的 C 語言程式碼：

| 指標 | 提案+驗證 | 直接生成程式碼 |
|------|-----------|----------------|
| 加速比 | 2.66x | 低 14-16% |
| 正確性 | Compiler 保證 | 17.6% false positive |
| Token 消耗 | 基準 | 5.3 倍 |

17.6% 的 false positive 是什麼意思？就是 LLM 生成的程式碼「看起來」輸出一樣（用 output comparison 驗證），但其實語義不等價。在 compiler 優化的場景下，這代表上線之後可能出現 silent bug。

而且 token 消耗多了 5.3 倍——因為生成完整的程式碼比生成一行轉換指令需要多得多的 token。

這個結果直接映射到 AI Coding 的架構選擇：**把 LLM 的角色限縮在「決策」，把「執行」和「驗證」交給確定性的工具。** 不是因為 LLM 寫不了程式碼，是因為在 loop 的場景下，每一輪的正確性驗證成本會被放大 30 倍。用 compiler 驗證一次就知道對不對。用 output comparison 驗證，17.6% 的機率你以為對了但其實不對。

---

## 數據六：硬體資訊對 LLM 決策的影響趨近於零

這個發現我覺得很有意思。

ComPilot 的 system prompt 裡包含了完整的硬體規格（Intel Xeon E5-2695 v2、48 thread、128GB RAM、L1/L2/L3 cache 大小）。論文做了一個 ablation：把硬體資訊從 prompt 裡拿掉，看效能會不會掉。

結果：**沒有統計顯著的差異。**

論文的解釋是兩個可能：一、LLM 依賴的是從訓練資料學到的通用優化原則，不是根據具體硬體規格做計算。二、feedback loop 的迭代回饋覆蓋了 prompt 裡硬體資訊的效果——就算不知道硬體規格，跑幾輪之後從 speedup 數字就能推斷出什麼有效什麼沒效。

這給了我們另一個設計啟示：**在有 feedback 的 loop 裡，過度精細的 context 可能沒你想的那麼重要。** Loop 本身就是一種資訊獲取機制——每一輪的執行結果本身就在告訴 agent 環境的特性。

---

## 一個 LLM 會放棄的問題

論文記錄了一個我沒預料到的現象：LLM 會過早放棄。

在找到一個顯著加速之後，或者連續幾輪失敗之後，LLM 會主動說「我覺得已經找到最好的了」然後停止提案。論文的做法是強制要求它繼續探索——結果發現要推到第 5 次「放棄」之後，效能才會接近 T=30 的水準。大約 2% 的情況下，LLM 完全拒絕繼續。

這在 Loop Engineering 的設計裡是一個真實的問題。Agent 有自己的「停止傾向」，不完全受你的 stop condition 控制。你設定了 T=30，但 agent 可能在 T=12 就覺得夠了。

系統設計要考慮到這一點：不只是設定外部的 stop condition，還要處理 agent 的內部停止傾向。ComPilot 的做法是用 explicit prompting 把它推回去。

---

## 回到 Loop Engineering 系列：論文驗證了什麼

把 ComPilot 的 ablation 數據對齊我在前三篇講過的論點：

| 系列論點 | ComPilot 的數據 |
|----------|-----------------|
| Feedback loop 是核心，不是跑很多次 | 移除 feedback → 效能掉 23-40% |
| 做之前先確認有可量化 metric | speedup ratio 是唯一 metric，無模糊判斷 |
| Stop condition 要設好 | T=30 後收益遞減 87%（+0.08x vs +0.42x） |
| 護欄比模型重要 | 64% 提案失敗但系統仍達 2.66x |
| 模型選擇不是最關鍵的 | 通用模型 > coding 專用模型 |
| 把 AI 限縮在決策，執行交給工具 | 直接生成程式碼慢 14-16%，17.6% false positive |

每一條都有數據支撐。不是某個人的經驗談，是跑了 150 個 benchmark、8 個模型、做了 6 組 ablation 的結果。

---

## 為什麼是 Compiler？因為學術論文需要「可驗證的場景」

讀到這裡你可能會問：為什麼這個團隊選 compiler loop optimization 來做研究？

因為發論文需要可重現、可量化、可比較的實驗。Compiler 的場景剛好全部符合：

- **驗證是確定性的。** 多面體依賴分析給出的是 binary judgment——合法就是合法，不合法就是不合法。不存在「大概合法」或「看情況」。
- **效能是可量測的。** Execution time 跑出來就是一個數字，2.66x 就是 2.66x。不需要人去判斷「這個優化好不好」。
- **搜索空間是有限的。** 9 種 transformation primitive，組合雖然多，但邊界清楚。
- **有成熟的 baseline。** Pluto 多面體優化器跑了幾十年，數據公開可比較。

這些特性讓 ablation study 的結論非常硬——當你移除 feedback loop 後效能掉 23-40%，這個「23-40%」是精確量測出來的，不是問卷或人工評分。

**但也正因為如此，你不能直接把這些數字搬到你的 AI Coding 場景裡。** 你的 code review loop 沒有辦法像 compiler 一樣給出「合法/不合法」的 binary judgment。你的 refactor loop 的「對不對」要靠 test suite 間接推斷，test suite 本身可能不完整。你的 agent 做完一輪之後「好了多少」，很多時候是人的主觀判斷。

那這篇論文還有參考價值嗎？有。

它的價值不在於告訴你「你的場景也會掉 23%」，而在於**用嚴格的實驗設計證明了方向性的結論**：feedback loop 比 open-loop 好、護欄比換模型重要、迭代有收益遞減。這些結論的「方向」在你的場景裡大概率成立，只是「幅度」會因為驗證參數的模糊程度而不同。

學術論文選乾淨的場景是為了發 paper。我們讀它是為了拿走那些跨場景依然成立的結構性洞見。

---

## 坦白說

幾個其他限制，誠實講：

**效能數據有 variance。** 同一個模型跑同一個 benchmark，K=5 比 K=1 好 33%，說明結果有顯著的隨機性。Best-of-5 的數據比 single run 漂亮很多，實務上你不一定能負擔五次完整執行的成本。

**大型輸入上 Pluto 贏了。** ComPilot 在 MINI 到 MEDIUM 的 input size 上大幅領先 Pluto（16.35x 到 1.87x），但在 XLARGE 上反過來輸了（0.82x）。傳統 compiler 的 size-tuned heuristics 在大型資料上仍然有優勢。

**Token 成本是指數增長的。** 因為每一輪都把完整對話歷史送進去，context 越來越長，token 消耗是非線性增長的。論文沒有明確量化總 token 成本，但在商業模型上這是一個實際問題。

這些限制不影響核心結論——feedback loop 的價值、護欄的必要性、stop condition 的重要性——但它們提醒我們：從一個高度結構化的場景泛化到一般 AI Coding，中間有距離。

---

## 一句話收尾

Loop Engineering 不是讓 AI 跑很多次。是工程化那個讓 AI 能在 64% 失敗率下依然收斂到好結果的回饋迴路。ComPilot 用 ablation study 證明了這一點。

---

**延伸閱讀：**
- [Loop Engineering：不再 Prompt Agent，改設計 Loop 讓 Agent Prompt Agent](/loop-engineering-from-prompt-to-loop-paradigm-shift/)
- [Loop Engineering 實作指南：五個組件 + 一個記憶體，讓 Agent 自己跑起來](/loop-engineering-five-plus-one-implementation-guide/)
- [影片逐字稿｜Loop Engineering 是真趨勢還是 Buzzword？](/loop-engineering-buzzword-video-transcript/)
- [Harness Engineering 架構全景](/harness-engineering-architecture-overview-ai-code-production-guardrails/)

**論文原文：** Merouani, M., Kara Bernou, I., & Baghdadi, R. (2025). Agentic Auto-Scheduling: An Experimental Study of LLM-Guided Loop Optimization. PACT 2025. arXiv:2511.00592v2.
