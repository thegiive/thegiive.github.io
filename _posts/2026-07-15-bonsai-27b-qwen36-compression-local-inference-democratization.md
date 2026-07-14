---
layout: post
title: "55.6GB → 3.9GB，保留 90% 智力：Bonsai 27B 把 Qwen 3.6 壓到手機上跑，但本地 Agent 的瓶頸不在模型大小"
date: 2026-07-15 09:00:00 +0800
permalink: /bonsai-27b-qwen36-compression-local-inference/
image: /assets/images/bonsai-27b-prismml-announcement-cover.png
description: "PrismML 7/14 發布 Bonsai 27B，把 Qwen 3.6 27B 從 55.6GB 壓到 5.9GB（ternary）和 3.9GB（1-bit），在 iPhone 17 Pro 上跑。Apple 正在跟 PrismML 洽談，Vinod Khosla 稱之為 mathematical breakthrough。AnythingLLM 創辦人說「比 Fable + Mythos + GPT 5.6 加起來都重要」。但 benchmark 拆開看：MATH 500 從 99.4 只掉到 98，TauBench（tool calling）卻從 82.9 掉到 61.3——壓縮後的智力損失不均勻。這篇拆解為什麼「本地能跑 27B」和「本地 Agent 可用」之間還有一道鴻溝。"
---

[The Information](https://www.theinformation.com/articles/khosla-backed-startup-claims-breakthrough-largest-ever-ai-model-iphone) 和 [CNBC](https://www.cnbc.com/2026/07/14/apple-prismml-ai-compression-iphone.html) 在 7 月 9-10 日報導，**Apple 正在跟 PrismML 進行早期洽談**，探索用後者的壓縮技術在 iPhone 上跑更大的 AI 模型。幾天後的 7/14，PrismML 把底牌攤出來了：[Bonsai 27B](https://prismml.com/news/bonsai-27b)。

Qwen 3.6 27B 要 55.6GB 記憶體才能跑。PrismML 把它壓到 5.9GB（ternary，1.58-bit）和 3.9GB（1-bit），在 iPhone 17 Pro 上全參數推理，保留 90-95% 的 benchmark 表現。Apache 2.0 開源。

Apple 目前自己的 AFM 3 Core Advanced 有 20B 參數，但一次只激活 1-4B。如果外部的 27B 全參數模型能在 iPhone 上跑，Apple 在 on-device AI 的選項會多很多。Khosla Ventures 的 Vinod Khosla 稱 PrismML 的做法是 ["mathematical breakthrough"](https://cryptobriefing.com/apple-prismml-on-device-ai-iphone/)。

[AnythingLLM](https://anythingllm.com/) 創辦人 Tim Carambat 的評價更直接：

> "The impact of this is far more important than Fable, Mythos, or GPT 5.6. Probably combined too."

> "This is the real DeepSeek moment for AI. What is the value of billions of dollars of GPUs when we can do more with much, much less."

推理側的 DeepSeek 時刻。這個判斷值得認真拆解——不是因為它錯，而是因為 benchmark 拆開看，壓縮後的智力損失不是均勻的。有些能力幾乎無損，有些掉得足以影響實用性。

---

## 30 秒定位：四個模型的壓縮比較

| 模型 | 大小 | 壓縮倍數 | 平均分數 | 保留率 |
|------|------|----------|----------|--------|
| Qwen 3.6 27B（FP16 基準） | 55.6GB | 1.0x | 85.0 | 100% |
| **Ternary Bonsai 27B** | **5.9GB** | **9.4x** | **80.5** | **95%** |
| **1-Bit Bonsai 27B** | **3.9GB** | **14.3x** | **76.1** | **90%** |
| Unsloth-IQ2 2.8bit | 9.4GB | 5.9x | 72.7 | 85% |

最值得注意的一行：**Ternary Bonsai 用 5.9GB 拿到 80.5 的平均分，Unsloth IQ2 用 9.4GB 只拿到 72.7。** 體積小 37%，分數高 10.7%。

這不是微調出來的——壓縮方法本身的差異造成了截然不同的智力保留曲線。

---

## PrismML 是誰

PrismML 2026 年 3 月 31 日從 stealth 出來，拿了 [$16.25M 種子輪](https://finance.yahoo.com/sectors/technology/articles/prismml-introduces-ternary-bonsai-model-180000385.html)，投資方包括 Khosla Ventures、Cerberus、Google、Samsung。CEO Babak Hassibi 是 Caltech 電機教授。

他們 4 月先發了 [Ternary Bonsai 系列](https://prismml.com/news/ternary-bonsai)（8B、4B、1.7B），7/14 把同樣的壓縮技術推到 Qwen 3.6 27B——這是第一次有人把 27B 級模型壓到手機可執行的大小，且保留了多模態能力（vision、tool calling、262K context）。之前也成功壓過 Flux2-Klein（圖片生成模型），說明這不是只針對 text LLM 的技巧。長期目標是壓縮 trillion-parameter 級的模型。

---

## Ternary 壓縮跟一般量化有什麼不同

先講結論：Bonsai 不是 GGUF 量化。它更激進，但效果反而更好。

標準量化（如 Unsloth 的 IQ2）是把 FP16 權重映射到更少的 bit 數——本質是「用更粗的尺去量同樣的東西」。資訊損失來自精度下降，且損失分布取決於量化演算法對不同 layer 的處理策略。

PrismML 的做法不同。Ternary Bonsai 把每個語言網路的權重限制為三個值：{-1, 0, +1}，搭配每個 group 一個 FP16 的 scale factor。**1.71 effective bits per weight。** 1-Bit 更極端：只有 {-1, +1}，1.125 bits per weight。

關鍵差異在於，PrismML 宣稱這個壓縮是「end to end across the language network, embeddings, attention, MLPs, and the LM head, with no higher-precision escape hatches」——整個語言網路一致壓縮，沒有「某些 layer 偷偷保留高精度」的後門。

聽起來更極端，結果卻更好。為什麼？

一個可能的解釋是：ternary 的搜索空間更結構化。{-1, 0, +1} 的組合比任意低 bit 值更容易優化，因為你只需要決定每個權重的「方向」和「是否激活」，而不是在連續空間裡找一個最佳的離散近似。

這不是我的猜測——[BitNet 系列論文](https://arxiv.org/abs/2310.11453)早在 2023 年就展示過 1-bit transformer 在特定條件下可以逼近 full precision 的表現。PrismML 的貢獻是把它工程化到一個已經訓練好的 27B 模型上，而不是從頭訓練一個 1-bit 模型。

---

## Benchmark 拆解：數學幾乎無損，Tool Calling 是軟肋

15 個 benchmark 攤開來看，壓縮後的智力損失有非常明顯的分類模式。

### 數學推理：保留得最好

| Benchmark | FP16 | Ternary | 1-Bit | 1-Bit 降幅 |
|-----------|-------|---------|-------|-----------|
| MATH 500 | 99.40 | 99.2 | 98.0 | -1.4% |
| GSM8K | 95.30 | **96.06** | 92.8 | -2.6% |
| AIME25 | 93.29 | 90.84 | 88.75 | -4.9% |
| AIME26 | 93.33 | 87.5 | 87.08 | -6.7% |

MATH 500 從 99.4 掉到 98，幾乎可以當作測量誤差。GSM8K 的 Ternary 版甚至比原版還高（96.06 vs 95.30）。

**數學推理的核心是邏輯鏈的正確展開，不依賴權重的精度細節。** 1+1 在 FP16 裡等於 2，在 1-bit 裡也等於 2。這解釋了為什麼數學是壓縮最友好的能力類別。

### 編程能力：中等損失

| Benchmark | FP16 | Ternary | 1-Bit | 1-Bit 降幅 |
|-----------|-------|---------|-------|-----------|
| HumanEval+ | 95.12 | 93.9 | 89.63 | -5.8% |
| MBPP+ | 83.33 | 81.22 | 79.6 | -4.5% |
| LiveCodeBench | 87.77 | 82.75 | 76.4 | -13.0% |

LiveCodeBench 的 -13% 值得關注——它測的是真實世界的程式碼生成，比 HumanEval 這種標準題更接近實際使用場景。

### Tool Calling 與 Instruction Following：掉最多

| Benchmark | FP16 | Ternary | 1-Bit | 1-Bit 降幅 |
|-----------|-------|---------|-------|-----------|
| TauBench | 82.90 | 73.61 | 61.34 | **-26.0%** |
| IFBench | 68.03 | 58.5 | 52.36 | **-23.0%** |
| BFCL v3 | 77.10 | 74.41 | 70.72 | -8.3% |
| IFEval | 88.91 | 85.03 | 79.11 | -11.0% |

**TauBench（Agent 級 tool calling）從 82.9 掉到 61.3，降幅 26%。IFBench 掉 23%。**

這兩個數字是整張 benchmark 表裡最刺眼的。而且恰好是 Agent 使用場景最在意的能力。

為什麼 tool calling 比數學脆弱得多？一個合理的推測：tool calling 需要模型精確地產出結構化輸出（JSON schema、function signature、正確的參數類型），這比「推出正確的數學步驟」對權重的精度更敏感。**數學是 pattern matching + logical chaining，tool calling 是 syntactic precision。** 後者更容易被壓縮破壞。

### 視覺能力：顯著下降

| Benchmark | FP16 | Ternary | 1-Bit | 1-Bit 降幅 |
|-----------|-------|---------|-------|-----------|
| MMMU Pro | 79.94 | 68.96 | 60.48 | -24.3% |
| OCR Bench | 65.28 | 61.42 | 58.65 | -10.2% |

Vision tower 用的是 4-bit 獨立壓縮，損失比語言側大。如果你的使用場景重度依賴圖片理解，Ternary 版比 1-Bit 版安全很多（MMMU Pro 69 vs 60）。

---

## 跟 Unsloth 的對比揭示了一件重要的事

回頭看 benchmark 總表裡的 Unsloth-IQ2 2.8bit。它用 9.4GB 只拿到 72.7 平均分、85% 保留率。Ternary Bonsai 用 5.9GB 拿到 80.5、95% 保留率。

但更有趣的是逐項比較：

| Benchmark | Ternary Bonsai (5.9GB) | Unsloth IQ2 (9.4GB) | 差距 |
|-----------|----------------------|---------------------|------|
| MATH 500 | 99.2 | 84.6 | +14.6 |
| AIME25 | 90.84 | 66.67 | +24.2 |
| LiveCodeBench | 82.75 | 56.4 | +26.4 |
| TauBench | 73.61 | 74.58 | -1.0 |

**Ternary Bonsai 在數學和程式碼上把 Unsloth 打得很慘（AIME25 差 24 分），但在 TauBench 上 Unsloth 反而微幅領先。**

這驗證了前面的觀察：不同壓縮方法毀掉的能力類別不一樣。Bonsai 的 ternary 方法對數學和推理特別友好，對 tool calling 不那麼友好。傳統量化剛好反過來——數學掉得多，tool calling 相對保留。

**這意味著「哪個壓縮比較好」沒有通用答案。取決於你要拿它做什麼。**

---

## 呼應：「核心不是模型多聰明，而是工具鏈多穩定」

[另一篇關於 AI Coding On-Prem 的文章](/ai-coding-on-prem-three-paths/)裡，我們的結論是：

> 「AI Coding 不只是呼叫 API 拿回文字。它是 Agentic Workflow——Agent 要讀檔案、寫程式碼、執行 bash 指令。核心不是模型多聰明，而是工具鏈多穩定。」

Bonsai 27B 的 benchmark 數據精準地驗證了這個判斷。數學推理掉 2-5%，無關緊要。**但 TauBench（多步 tool calling）掉 26%，IFBench（指令遵循）掉 23%——這兩項恰好是 Agentic Workflow 的核心能力。**

換句話說：你現在可以在手機上跑一個很會算數學的 27B 模型。但如果你想讓它當 Agent——自動讀檔、呼叫 API、按步驟執行任務——壓縮帶來的精度損失剛好命中要害。

---

## Jevons Paradox：Tim 說對了方向，但機制跟他想的不一樣

Tim Carambat 把 Bonsai 稱為「the real DeepSeek moment」，意思是：當推理成本趨近零、模型能跑在每個人的硬體上，那數十億美元的 GPU 投資還有什麼意義？

這個直覺指向 Jevons Paradox——19 世紀經濟學家 Jevons 發現蒸汽機效率提高後，煤炭消耗量不減反增。因為效率提升→成本下降→使用場景增加→總消耗更高。

AI 領域的數據支持這個模式：過去兩年，企業 GenAI 支出[成長 22 倍](https://elitecurrensea.com/stocks/the-better-ai-gets-the-smaller-its-share-jevons-paradox-meets-ai-when-12vds/)，同期 per-token 價格下跌超過 90%。Deloitte 2026 TMT 報告預測，推理已佔所有 AI 運算量的約三分之二。

所以 Tim 的方向是對的：Bonsai 這類技術會讓更多人在更多場景使用 AI。但這不會取代雲端 GPU——**它會創造一個之前不存在的本地推理市場，同時雲端推理的需求也繼續成長。** 蛋糕變大了，不是切法變了。

DeepSeek 的真正衝擊是用更少的訓練資源達到 frontier 能力。Bonsai 做的事不一樣——它不降低 frontier，它降低 deployment 門檻。**前者挑戰的是「誰能訓練最強模型」，後者挑戰的是「誰能用最強模型」。兩個都重要，但不是同一種重要。**

---

## 坦白說

Bonsai 27B 的 benchmark 數字來自 PrismML 自己的測試。目前沒有大規模的第三方獨立驗證。Tim Carambat 的測試是目前最知名的外部評估，但他跟 PrismML 有合作關係（Bonsai 模型整合進 AnythingLLM），這不是完全獨立的第三方。

Hacker News 上的[討論](https://news.ycombinator.com/item?id=48910545)有幾個值得記錄的聲音：

- 有人測試 Android demo 產出亂碼（「!!!!!!!!!!!!」）
- 有人質疑 benchmark 是否反映真實使用——「can't imagine the ternary being any good based on this」
- 有人指出 Gemma 4 12B 量化後也只要不到 7GB，且 tool-use 表現更穩定
- Tool calling 的 5-8% 降幅被評為「significant in real-life use cases」

這些不是 FUD。benchmark 上 TauBench 73.61 看起來還可以，但在真實的多步 Agent 工作流裡，每一步 5% 的錯誤率會指數放大。跑 10 步的 Agent pipeline，0.95^10 = 60% 的成功率；0.92^10 = 43%。**幾個百分點的 tool calling 精度差異，在多步場景裡是致命的。**

但它做對了一件很重要的事：**把 27B 級的數學和推理能力帶到消費硬體上。** 在 RTX 5090 上 163 tok/s、M5 Max 上 87 tok/s、iPhone 17 Pro 上能跑——這是之前做不到的。如果你的場景是本地推理、知識問答、數學輔助、程式碼生成（非 Agent），Ternary Bonsai 是目前最佳的選項之一。

---

## 關鍵洞察

1. **壓縮後的智力損失不是均勻的。** 數學推理保留 95%+，tool calling 掉 26%。選壓縮模型之前，先確認你的使用場景落在哪個類別。需要 Agent 能力的，Ternary（5.9GB）是下限，1-Bit 不建議。

2. **Ternary Bonsai 5.9GB 全面碾壓 Unsloth IQ2 9.4GB——但不是每個維度都碾壓。** 在 TauBench 上兩者幾乎平手。不同壓縮方法毀掉的能力類別不同。如果你要做 tool calling 密集的工作，用你自己的工作流跑一次比看 leaderboard 有用。

3. **「本地能跑 27B」和「本地 Agent 可用」是兩個不同的里程碑。** Bonsai 達成了前者。後者需要 tool calling 和 instruction following 的保留率再往上拉——或者 harness 工具鏈端做更多補償。模型壓縮只解了硬體門檻，沒解能力門檻。

4. **這不是 DeepSeek 時刻，這是 deployment democratization。** DeepSeek 改變了「誰能訓練 frontier 模型」的答案。Bonsai 改變的是「誰能跑 27B 級推理」的答案。對個人開發者來說，後者可能更直接有用——你不需要訓練模型，你需要用模型。
