---
layout: post
title: "Fable 5 被關門了，然後呢？——當「路徑驗證」成為 AI 產業最強的加速器"
date: 2026-06-15 08:44:57 +0800
permalink: /replication-is-easy-engineering-moat-ai-competition/
image: /assets/images/replication-engineering-moat-logo.png
description: "Anthropic 在 6 月 9 日發布了 Claude Fable 5——第一個「Mythos 級」模型，SWE-Bench Pro 自報 80.3%，比 Opus 4.8 高了 11 個百分點。"
---

![Fable 5 Path Validation](/assets/images/replication-engineering-moat-logo.png)

## 6 月 9 日，Fable 5 上線。6 月 13 日，全球下架。

Anthropic 在 6 月 9 日發布了 Claude Fable 5——第一個「Mythos 級」模型，SWE-Bench Pro 自報 80.3%，比 Opus 4.8 高了 11 個百分點。

四天後，美國政府的出口管制指令下來，Fable 5 和 Mythos 5 全球暫停存取。

看到這個消息的時候，我跟很多人一樣覺得可惜。才用了四天，手感正好，就被收回去了。

但接下來發生的事情，比 Fable 5 本身更值得寫。

---

## 關門後的 72 小時

Fable 5 下架的同一週，發生了什麼？

**6 月 12 日**：OpenRouter 正式發布 Fusion API——把多個模型的回答丟給 judge 模型做分析和合成，生成一個新的回答。三個便宜模型（Gemini 3 Flash + Kimi K2.6 + DeepSeek V4 Pro）組成的 Budget Panel，在 DRACO benchmark 上拿到 64.7%，**打贏了單獨跑的 GPT-5.5（60.0%）和 Opus 4.8（58.8%）**。

**6 月 13 日**：智譜發布 GLM-5.2——1M context window、744B MoE 參數、全華為 Ascend 晶片訓練、MIT 開源。

**6 月 14 日之後**：社群已經在用 OpenRouter Fusion 的自訂面板跑各種組合，有人把 Fable 5 發布前的存量 API call 混進 panel，跑出了 DRACO 69.0% 的成績——比 Fable 5 單獨跑的 65.3% 還高。

一扇門關了，好幾扇窗同時打開。

---

## Fable 5 最大的貢獻不是 Fable 5 本身

我現在的看法是：Anthropic 最重要的貢獻，可能不是做出了 Fable 5，而是**證明了這種級別的模型是可以被訓練出來的**，而且周期並沒有大家想像得那麼長。

一旦路徑被驗證，OpenAI 會跟，Google 會跟，國產廠商也會跟。Fable 5 關門當然能延緩擴散，但關不住方向。

在科技史上，最難的往往並非複製。就像原子彈、就像 ChatGPT——一旦行業知道了這條路能通，資金、算力和人才就會瘋狂湧入。領先者的成功消除了不確定性風險，後來者不再需要把資源浪費在試錯和懷疑上，開發周期自然會大幅縮短。

這個觀點，我以前會持保留態度。但看完 Fable 5 下架後這一週的爆發，我的想法有了變化。

---

## 數據在說話：追趕速度是指數級的

把時間線拉開來看，「路徑驗證 → 快速複製」的模式已經不是理論推演，是正在發生的事實。

**MMLU 開源 vs 閉源差距：**
- 2023 年底：17.5 個百分點
- 2026 年初：0.3 個百分點

兩年，差距從顯著到統計雜訊。

**具體追趕案例：**

| 模型 | 發布時間 | 關鍵能力 | 跟 frontier 的差距 | 價格 |
|------|---------|---------|-------------------|------|
| DeepSeek V4 | 2026/04 | SWE-bench 80.6% | 接近 Claude Opus | Opus 的 **1/29** |
| GLM-5.1 | 2026/03 | 宣稱 Opus 4.6 的 94.6% | 5.4% | 遠低於 Opus |
| GLM-5.2 | 2026/06 | 1M context，MIT 開源 | 未知（無 benchmark） | ~$0.98/M input |
| OpenRouter Fusion Budget | 2026/06 | DRACO 64.7% | 贏過單獨 Opus 4.8 | 約 Fable 5 的 **1/2** |

最後一行是最驚人的。**三個次等模型的組合體，打贏了單獨的 frontier 模型。** 不是靠更強的單一模型，而是靠架構創新——panel + judge + synthesizer 的三階段管線。

這意味著「追趕」已經不只是「造出一樣強的模型」了。追趕的方式本身也在進化。

---

## OpenRouter Fusion：一個更有趣的訊號

如果只是「別的公司也造出強模型」，那只是老故事的重演。但 OpenRouter Fusion 代表的是一個不同層次的突破。

先看架構：

**第一步（Panel）：** 同一個 prompt 平行送給 1-8 個模型，每個模型都可以做 web search。

**第二步（Judge）：** 一個 judge 模型讀取所有回答，產出結構化分析——哪些是共識點（高信心）、哪些是矛盾、哪些是某個模型獨有的洞見、哪些是所有模型都沒注意到的盲區。

**第三步（Synthesizer）：** 最終模型根據 judge 的分析寫出一個新的回答——**不是投票，不是選最好的一個，而是綜合所有模型的推理去合成一個新答案**。

DRACO 的結果很有意思：

- Opus 4.8 單獨跑：**58.8%**
- Opus 4.8 跟自己 Fusion（同一個模型跑兩次）：**65.5%**
- 三個便宜模型 Budget Panel：**64.7%**

**同一個模型跟自己 Fusion，都能提升 6.7 個百分點。** 這說明 Fusion 的價值不只是「模型多樣性」，合成過程本身就在創造新的品質。

對從業者來說，這個數據的意義是：**你不需要等下一個 Fable 5 才能獲得 Fable 5 級別的能力。用現有模型的聰明組合，就能逼近甚至超越。**

---

## 這代表什麼？情況會越來越好

把這些事件串在一起看，有一個清晰的趨勢：

**2023 年：** 你需要 OpenAI 級別的資源才能做 frontier model。ChatGPT 獨佔市場，沒有替代品。

**2024 年：** 開源追趕開始（Llama、Mistral），但差距仍然明顯。

**2025 年：** DeepSeek 證明小團隊也能做 frontier-class 模型。開源差距快速縮小。

**2026 年上半年：** GLM-5 證明不用 NVIDIA 也能做。OpenRouter Fusion 證明不需要 frontier model 也能得到 frontier 級結果。Fable 5 關門後一週內，替代方案從四面八方湧出。

**趨勢方向是確定的：AI 能力的取得門檻正在指數級下降。**

這裡面有幾個具體的驅動力：

1. **算力基礎設施的多元化**：華為 Ascend 已經能跑 frontier 訓練，不再是 NVIDIA 獨佔。15% 的效能差距在持續縮小。

2. **蒸餾和微調技術的成熟**：小模型能從大模型學到越來越多東西。DeepSeek V4 的 49B active parameters 做到了接近 Opus 水準。

3. **架構創新的民主化**：OpenRouter Fusion 的三階段管線不是什麼黑科技，任何開發者都能用現有的 API 組裝。

4. **開源生態的正反饋循環**：MIT 授權的模型越多，基於這些模型的工具和優化就越多，又吸引更多人開源。

---

## 我的判斷

管四的核心觀點我現在完全同意：**Fable 5 最大的貢獻是證明了方向可行，而不是 Fable 5 本身。**

Phoenix Yin 的延伸也是對的：**路徑驗證消除不確定性，加速所有後來者。**

Fable 5 關門了四天，但方向已經被驗證了。GLM-5.2 用華為晶片跑出 frontier-class 的開源模型，OpenRouter Fusion 用三個便宜模型打贏了單獨的 Opus 4.8。

**一扇門關了，好幾扇窗已經打開。而且這些窗戶只會越開越多。**

---

## 關鍵數據速查

| 事件 | 數據 | 意義 |
|------|------|------|
| Fable 5 SWE-Bench Pro | 80.3%（自報） | 設定了 Mythos 級別的性能標竿 |
| Fable 5 在線天數 | 4 天（6/9-6/13） | 路徑已驗證，即使產品被關 |
| OpenRouter Fusion Budget Panel | DRACO 64.7% | 三個便宜模型打贏單獨 Opus 4.8（58.8%） |
| Fusion 最佳組合 | DRACO 69.0% | 比 Fable 5 單獨（65.3%）還高 |
| GLM-5.2 | 1M context，MIT 開源 | 100% 華為晶片訓練的 frontier-class 模型 |
| DeepSeek V4 vs Claude 價差 | 1/29 價格 | benchmark 接近，成本差一個數量級 |
| MMLU 開源 vs 閉源 | 17.5 → 0.3 百分點 | 2 年追平 |
| OpenRouter 估值 | $13 億（B 輪） | 模型路由/融合本身是大生意 |
| OpenRouter 週處理量 | 25 兆 tokens | 多模型生態已成規模 |
