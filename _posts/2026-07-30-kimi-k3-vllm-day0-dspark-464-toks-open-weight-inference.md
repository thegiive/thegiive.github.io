---
layout: post
title: "Kimi K3 + vLLM Day-0：2.8T 開源模型跑出 464 tok/s，自部署 Frontier AI 的遊戲規則變了"
date: 2026-07-30 10:00:00 +0800
permalink: /kimi-k3-vllm-day0-dspark-464-toks-open-weight-inference/
image: /assets/images/kimi-k3-vllm-464-toks-cover.png
description: "vLLM 官方宣布 Kimi K3 Day-0 支援，搭配 Inferact 的 DSpark 投機解碼，在 4×GB300 上跑出 464 tok/s 的 bs=1 peak decode 速度。2.8 兆參數的開源模型，推理速度追上甚至超越閉源 API——自部署 frontier AI 的經濟學正在被改寫。"
---

![vLLM Kimi K3 464 tok/s](/assets/images/kimi-k3-vllm-464-toks-cover.png)

## 五個月前我寫了 K2.5，結論是「大多數 Agent 應用，Kimi K2.5 都夠用」

今年二月我做了 [Kimi K2.5 的深度技術評估](https://ai-coding.wiselychen.com/kimi-k2.5-agent-swarm-deep-dive-technical-assessment/)，當時的結論很明確：1 兆參數但推理只用 32B，API 輸入只要 $0.60/M tokens，OpenClaw 社群用得最多的模型就是 K2.5。

五個月後，Moonshot AI 直接把參數量從 1T 拉到 2.8T，active 參數從 32B 跳到 104B，context window 從 256K 拉到 1M tokens。

但真正讓我決定寫這篇的不是 K3 本身——是 vLLM 官方在 7/27 宣布的那條推文：

**「vLLM hit new peak bs=1 decode on Kimi-K3: 464 tok/s」**

464 tokens per second，batch size 1，在 4×GB300（16 張 GPU，TP16）上用 DSpark 投機解碼跑出來的。這個數字的意義是：一個完全開源、可以下載權重自己跑的 frontier 模型，單用戶推理速度已經快到讓人重新思考「我還需要付 API 費用嗎」這個問題。

---

## Kimi K3 架構：從 K2.5 到 K3 變了什麼

先用一張表快速對比：

| 項目 | Kimi K2.5 | Kimi K3 |
|------|-----------|---------|
| 總參數 | 1T | **2.8T** |
| MoE 專家數 | - | **896** |
| 每 token 啟用專家 | - | **16** |
| 推理激活參數 | 32B | **104B** |
| Context Window | 256K | **1M** |
| 原生多模態 | 文本 + 圖像 + 視頻 | 文本 + 視覺 |
| 注意力機制 | 標準 | **Kimi Delta Attention (KDA)** |
| 權重格式 | FP16 | **原生 MXFP4** |
| API 輸入價格 | $0.60/M | $3.00/M（cache hit $0.30/M）|
| 授權 | Modified MIT | 開源 |

幾個值得注意的架構變化：

### Kimi Delta Attention (KDA)

K3 最核心的創新。KDA 是一種混合注意力機制——結合了線性注意力的固定大小 recurrent state 和完整注意力的精確度。在 1M context 的長序列場景下，KDA 比傳統全注意力快 **6.3 倍**。

這不是理論數字。當你在跑長文檔 RAG 或大型 codebase 分析時，KDA 讓 K3 不需要為了 context window 大小付出等比例的推理成本。

### Attention Residuals (AttnRes)

跨層的深度方向學習混合。傳統 Transformer 每一層的表示是累加的，AttnRes 讓模型可以選擇性地從不同深度的層去檢索表示。簡單講就是：模型不只是「逐層加工」，而是可以「跨層回頭看」。

### Stable LatentMoE + Quantile Balancing

896 個專家裡只用 16 個，這種極高稀疏度的 MoE 很容易出問題——某些專家被過度使用、某些完全閒置。K3 用 Quantile Balancing 直接從 router score 的分位數來分配專家，不需要啟發式更新，scaling 效率比 K2 提升約 2.5 倍。

### 原生 MXFP4

K3 從 SFT 階段就開始做 quantization-aware training，原生支援 4-bit 權重（MXFP4）配 8-bit 激活（MXFP8）。這不是事後量化，是訓練時就考慮進去的——量化損失更小，而且大幅降低了部署的 GPU 記憶體需求。

---

## vLLM Day-0 支援：464 tok/s 怎麼來的

vLLM 在 Kimi K3 權重公開的同一天（7/27）就推出完整支援。這裡面有兩個關鍵數字要拆開看：

### 基礎推理速度（無投機解碼）

| 配置 | Batch Size 1 吞吐量 |
|------|---------------------|
| TP8（8 張 GB300） | 111 tok/s |
| TP16（16 張 GB300） | 118 tok/s |

111-118 tok/s 已經是一個可用的速度了。作為對比，Kimi K3 官方 API 的 output speed 大約是 62 tok/s。自部署跑得比官方 API 還快。

### 加上 DSpark 投機解碼

| 配置 | 無 DSpark | 有 DSpark | 加速倍率 |
|------|-----------|-----------|---------|
| TP8 | 111 tok/s | 331 tok/s | 2.98× |
| TP16 | 118 tok/s | 370 tok/s | 3.14× |
| TP16（低熵推理） | 118 tok/s | **464 tok/s** | **3.93×** |

464 tok/s 這個 peak 數字是在低熵推理任務（low-entropy reasoning workload，例如代碼生成）上跑出來的。因為代碼生成的 token 預測確定性比較高，投機解碼的「猜測命中率」更高，所以加速效果更明顯。

---

## DSpark 到底是什麼：4B 的小模型讓 2.8T 的大模型快 4 倍

DSpark 是 Inferact 團隊針對 Kimi K3 訓練的投機解碼（Speculative Decoding）draft 模型，已經開源在 HuggingFace（Inferact/Kimi-K3-DSpark）。

### 投機解碼的基本概念

傳統自回歸生成是一次預測一個 token。投機解碼的想法是：用一個小而快的 draft 模型先「猜」出好幾個 token，然後讓大模型一次性驗證這批猜測。猜對的直接用，猜錯的從錯誤點重新生成。

如果 draft 模型的猜測命中率夠高，等於是用小模型的速度做大模型的推理。

### DSpark 的技術細節

DSpark 不是一般的投機解碼。它用了一種叫 **block-diffusion** 的架構：

- **4B 參數的 draft 模型**，包含 5 層 dense layer，使用 non-causal attention
- **一次性並行生成 7 個 token**（不是逐個生成）
- **Low-rank Markov head**（rank=256）提供 block 內的 token 間依賴關係
- **Confidence head** 預測每個 draft token 的可信度，用於資源感知排程
- 與目標模型共用 576 維的 latent KV cache，不需要額外的 cache 記憶體

### 實測命中率

DSpark 在 14 個 benchmark 上的平均接受長度：

| 條件 | 每步平均接受 token 數 |
|------|---------------------|
| Temperature = 0（確定性生成） | 3.85 / 7 |
| Temperature = 1.0（隨機生成） | 3.73 / 7 |
| 低熵任務（coding） | ~4.73 / 7 |
| 高熵任務（創意寫作） | ~2.61 / 7 |

低熵任務上每步接受 4.73 個 token，這就是為什麼 coding 場景可以跑到 464 tok/s——猜測命中率高，驗證通過率高，實際生成速度就飆上去了。

### 訓練方式

最有趣的是訓練方法：DSpark 是**在 vLLM 推理過程中直接抽取目標模型的 hidden states** 來訓練的。用 TorchSpec 將 vLLM 的即時 hidden states 串流到並行的 FSDP draft 訓練中。

這意味著 draft 模型不是在離線數據上訓練的，而是直接學習目標模型的「思維方式」。大約兩個 epoch，跨多個 GB300 node，用 cross-entropy + L1 distribution-distillation 雙損失函數。

---

## Benchmark 定位：Kimi K3 在 frontier 模型裡排第幾

根據 Artificial Analysis Intelligence Index v4.1，Kimi K3 排名第 4，僅次於 Claude Fable 5 和 GPT-5.6 Sol：

| 排名 | 模型 | Intelligence Index | 開源 |
|------|------|-------------------|------|
| 1 | Claude Fable 5 | — | 否 |
| 2 | GPT-5.6 Sol | — | 否 |
| 3 | Claude Opus 4.8 | — | 否 |
| 4 | **Kimi K3** | **57** | **是** |

幾個關鍵 benchmark：

| 測試 | Kimi K3 | 備註 |
|------|---------|------|
| Terminal-Bench 2.1 | 80.90% | 第 2 名 |
| Arena WebDev | 1,679 | 第 1 名（初步） |
| DeepSWE | 67.3 | 用 Kimi Code harness |
| Vals Index | 74.70% | 第 2 / 38 |

Moonshot AI 自己也很誠實地說：「K3 的用戶體驗與 Claude Fable 5 和 GPT-5.6 Sol 仍有差距」，而且在決策上可能「過度主動」（excessively proactive）。

這種坦誠很像我在 K2.5 文章裡說的——K2.5 贏在 Agent 和視覺，輸在純數學和大型代碼庫修復。K3 往上走了一大步，但頂端仍然是閉源模型的天下。

差別在於：K3 是**可以自己部署的 frontier 模型**。

---

## 自部署經濟學：什麼時候自己跑比付 API 划算

這是最實際的問題。K3 API 定價 $3.00/M input tokens、$15.00/M output tokens（cache hit 只要 $0.30/M）。跟 K2.5 的 $0.60/M 相比貴了 5 倍，但跟 Claude Opus 的 $5.00/$25.00 相比仍然便宜 40-67%。

自部署的硬體需求：

| 項目 | 數字 |
|------|------|
| 原始權重大小 | ~1.4 TB（MXFP4） |
| 最低 GPU 配置 | 8× GB300 / B300 |
| 推薦配置 | 16× GB300（TP16） |
| 超級節點配置 | 64+ 加速器 |

以 16 張 GB300 的雲端租用成本來估算，大約 $15,000-20,000/月。如果你的 API 用量超過每月 1M output tokens（$15,000/月），自部署就開始划算了。

而且自部署的隱形優勢：
1. **數據不出海** — 金融、醫療、政府場景的硬需求
2. **無限 context cache** — 官方 API 的 cache hit rate 約 90%+，但自己跑可以做到 100% 可控
3. **客製化推理配置** — prefix caching 策略、投機解碼參數、batch size 都可以針對場景調整
4. **沒有 rate limit** — Agent Swarm 場景下不受 API 限流影響

---

## 從 K2.5 到 K3：Moonshot AI 的開源飛輪

回頭看這五個月的演進，Moonshot AI 的策略越來越清晰：

**K2.5（2026/02）：** 用極致性價比打開市場。$0.60/M tokens + Agent Swarm，讓開發者願意試用。OpenClaw 社群的大量採用驗證了這個策略。

**K3（2026/07）：** 用 frontier 級能力建立技術壁壘。2.8T 參數、KDA、原生 MXFP4——這些不是簡單地把模型變大，是在架構層面做了根本性的創新。

而 vLLM 的 Day-0 支援 + Inferact 的 DSpark 投機解碼，則代表了開源生態系統的另一個重要訊號：**最重要的 frontier 模型不只是要開源權重，還需要整個推理基礎設施一起到位。**

vLLM 的 blog 標題叫 "Efficient Day-0 Support"——不是 Day-1、不是 "coming soon"、是模型權重公開的同一天就能跑。這種配合速度本身就是生態系統成熟度的指標。

---

## 給 IT 團隊的 Takeaway

如果你在評估自部署 frontier 模型：

1. **464 tok/s 是真的** — 但前提是 16 張 GB300 + DSpark + 低熵任務。日常混合任務更實際的期望值是 330-370 tok/s，這仍然非常快。

2. **DSpark 投機解碼是必開的** — 3-4 倍的加速，幾乎沒有品質損失。4B 的 draft 模型相對於 2.8T 的目標模型幾乎不佔額外資源。

3. **MXFP4 原生量化是關鍵** — K3 不是「事後壓縮」，而是訓練時就在 4-bit 精度下優化過的。這讓 2.8T 模型的記憶體需求降到 1.4 TB，用 16 張高端 GPU 就能跑。

4. **K3 vs K2.5 不是替代關係** — K2.5 的 32B active 參數 + $0.60/M pricing 在成本敏感場景仍有巨大價值。K3 是給「需要 frontier 能力但不想依賴閉源 API」的場景。

5. **注意 KDA 對長 context 的影響** — 如果你的應用大量使用長文檔（RAG、代碼庫分析），KDA 的 6.3 倍加速在 1M context 下是實際可感知的效能差異。

---

## 我接下來會做什麼

之前 K2.5 文章結尾我說要做多模態壓力測試和 OpenCode 實戰。K2.5 在日常場景確實很穩，已經成為龍蝦的主力模型之一。

K3 的測試計畫不太一樣——我更關心的是 **inference infrastructure** 的故事：

1. **vLLM + DSpark 實際部署體驗** — 用 Docker image 在 RTX Pro 6000 上試跑（雖然 GPU 數不夠跑完整模型，但可以測 pipeline）
2. **KDA 在長 context 場景的真實加速** — 拿實際的 RAG 場景測 1M context 下的 latency 差異
3. **K3 vs K2.5 的 Agent 任務品質對比** — 同一組 Agent Swarm 任務，看 104B active 相對於 32B active 的品質提升值不值得 5 倍的成本

如果測試結果好，K3 有可能成為「需要高品質但不想被閉源 API 綁住」的最佳選擇。

---

## 參考資料

1. [vLLM 官方推文 — Kimi K3 464 tok/s peak benchmark](https://x.com/vllm_project/status/2081767404598919213)
2. [Kimi K3 Is Here: Efficient Day-0 Support on vLLM — vLLM Blog](https://vllm.ai/blog/2026-07-27-k3)
3. [Inferact/Kimi-K3-DSpark — HuggingFace](https://huggingface.co/Inferact/Kimi-K3-DSpark)
4. [Kimi K3 Tech Blog: Open Frontier Intelligence — Moonshot AI](https://www.kimi.com/blog/kimi-k3)
5. [moonshotai/Kimi-K3 — HuggingFace](https://huggingface.co/moonshotai/Kimi-K3)
6. [Kimi K3 Technical Report — arXiv](https://arxiv.org/pdf/2607.24653)
7. [Kimi K3 benchmarks, pricing, and self-hosting — Northflank](https://northflank.com/blog/what-is-kimi-k3-self-hosting)
8. [Kimi K2.5 深度技術評估 — AI Coding Blog](https://ai-coding.wiselychen.com/kimi-k2.5-agent-swarm-deep-dive-technical-assessment/)
