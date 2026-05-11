---
layout: post
title: "KV Cache 量化選擇地圖：vLLM 實測後，TurboQuant 該用在哪？"
date: 2026-05-12 08:00:00 +0800
permalink: /turboquant-kvquant-vllm-benchmark/
image: /assets/images/turboquant-qwen3-longcontext-benchmark.png
description: "FP8 還是 TurboQuant？2x 容量夠不夠？4bit-nc 值不值得？vLLM 工程師橫跨 4 個模型、5 個 benchmark 的誠實評測，終於把 KV Cache 量化的選擇邏輯說清楚了。不同情境有不同答案，但每個答案都有具體數字。"
---

KV Cache 量化一直是個「看起來美，用起來踩坑」的領域。

論文說壓縮到 2.5-bit 只有邊際損失，工程師實測說 reasoning 任務掉了 20 分；社區說 3-bit 在 MacBook 上跑 OpenAI 開源模型絲滑流暢，部署團隊說吞吐量剩 66%。

同一個技術，沒有人說謊，只是每個人站在不同的地方看。

這週 vLLM 工程師 Eldar Kurtić（Red Hat AI）發了一篇罕見的誠實報告，橫跨 4 個模型、5 個 benchmark，把 TurboQuant 各個變體在精確度、延遲、吞吐量上都測了一遍，並且直接給出了實用建議——不是「視情況而定」，是非常具體的「什麼情境用什麼」。

這種清晰度，在 AI 工具評測裡不常見。值得認真看一下。

---

## TurboQuant 是什麼

先說清楚技術背景。

TurboQuant 是 Google 在 2025 年 4 月發表的論文（arXiv 2504.19874），已被 ICLR 2026 接受。核心解決的問題是 **KV Cache 的記憶體開銷**。

現代 LLM 在推理時會把每個 token 的 Key/Value 向量暫存起來（KV Cache），讓後續 token 不用重算。問題是，長上下文下這個 Cache 會吃掉大量 GPU/RAM：一個 70B 模型處理 128K token 時，KV Cache 可以輕鬆超過 10GB。

傳統量化方式（如 FP8）已經把這個問題改善了一半，TurboQuant 想更進一步，用 2.5-3.5 bit 把 KV Cache 壓縮到極致。

**論文的核心技術：**
1. 把向量隨機旋轉（Random Rotation），讓座標分布集中（Beta 分布）
2. 利用高維空間中不同座標的近似獨立性，對每個座標分別做最優純量量化
3. 加入 1-bit QJL（Quantized Johnson-Lindenstrauss）殘差校正，修正 inner product 偏差

論文聲稱的成果：
- **3.5 bit per channel = 質量中性（absolute quality neutrality）**
- **2.5 bit per channel = 邊際質量下降（marginal quality degradation）**
- **最高 6x KV 記憶體壓縮，最高 8x attention 加速（H100）**

聽起來很美。

---

## vLLM 工程師的實測

vLLM 團隊（Eldar Kurtić + Miguel Goin, Red Hat AI）沒有跟著一起說「很美」。他們拿了真實模型跑了 5 個 benchmark。

**測試模型：**
- Llama-3.3-70B-Instruct
- Qwen3-30B-A3B-Instruct
- Qwen3-30B-A3B-Thinking（thinking 版本）
- MiniMax-M2.7（200B+ 旗艦）

**測試方法對比：**

| 量化方式 | KV 記憶體容量 | 精確度 | 吞吐量 |
|---|---|---|---|
| BF16（基準） | 1x | 100% | 100% |
| FP8 | **2x** | ≈100%（幾乎無損） | **≈100%** |
| TQ k8v4 | 2.4x | 輕微下降 | 66-75% |
| TQ 4bit-nc | 3.4x | 1-4 分下降 | 73-80% |
| TQ k3v4-nc | ≈4x | 嚴重下降 | 66-75% |
| TQ 3bit-nc | ≈4x | **嚴重下降** | **最差** |

### 精確度：3-bit 真的掉很多

最能說明問題的是 reasoning 任務：

**Qwen3-30B-Thinking 在 AIME25：**
- BF16：正常表現
- TQ 3bit-nc：**掉了約 20 分**

這不是邊際損失，這是實質退化。AIME 這種數學競賽題，20 分的差距代表模型在困難推理鏈上開始出錯。

**Qwen3-30B 在 256K 超長上下文（MRCR benchmark）：**
- BF16：45.8% AUC
- TQ 3bit-nc：31.2% AUC
- 相對下降：**30%**

長上下文的損失更嚴重，因為 KV Cache 越大，壓縮造成的資訊損失就越累積。

### 延遲：dequantization 是隱藏成本

Eldar 解釋了原因：

**FP8 為什麼幾乎零開銷？**  
FP8 把量化操作融入 attention 計算本身（quantized attention），不需要額外的 dequantize 步驟。

**TurboQuant 為什麼有開銷？**  
TurboQuant 在計算 attention 前，必須把 KV Cache 從低 bit 儲存格式 dequantize 回 BF16，這個步驟的代價隨著 KV Cache 大小線性增長。

結果：
- TurboQuant 所有變體：**10-68% 延遲增加**
- 吞吐量只剩 BF16 的 **66-80%**
- 在高並發（burst）下，Llama-70B 的 TPOT（每 token 延遲），FP8 比 BF16 快 2x，TQ 變體反而比 BF16 慢 1.5-2.5x

### 唯一勝出的場景：TTFT 在記憶體瓶頸下

TurboQuant 有一個真實的優勢。

在 Llama-70B 的高並發測試中，當 GPU 記憶體被 KV Cache 吃滿後：
- **BF16 的 TTFT（首個 token 延遲）爆炸到 ~17 秒**（系統開始排隊）
- **TurboQuant 所有變體維持在 3.5 秒以內**（5x 改善）

這才是 TurboQuant 真正的使用場景：**記憶體嚴重不足，且寧願犧牲精確度和吞吐量，換取「能跑」**。

---

## 論文 vs. 工程：為什麼結論不一樣

這不是誰在說謊，是測試環境不同。

**論文測試的是什麼？**  
論文主要評估的是 **perplexity（困惑度）和學術 benchmark**，在受控的記憶體和計算假設下。論文聲稱 3.5-bit 達到「質量中性」，是在特定測試集和模型下的結果。

**工程師測試的是什麼？**  
vLLM 測試的是 **生產環境的真實指標**：reasoning 任務精確度、長上下文能力、系統吞吐量、端到端延遲。而且測試的是最先進的模型（70B, MoE, Thinking 模型）。

Eldar 在 X 上說得很直接：

> 「我們刻意避開了關於 TurboQuant 學術新穎性、與先前工作的關係、以及 QJL 效果的討論。我們的主要目標是為 vLLM 使用者提供可以幫助他們做決策的數據。」

這是工程師的誠實。他沒有說論文是錯的，他說的是「論文的結論不直接適用於你的生產環境」。

---

## 但是：本地推理的世界完全不同

同一週，gpt-oss-20b 在 MacBook 上跑起來了。

OpenAI 在 2025 年 8 月開源了 gpt-oss 系列：
- **gpt-oss-20b**：20B+ 參數 MoE，Apache 2.0 授權，原生 MXFP4 量化
- **支援平台**：PyTorch + Apple Metal（MLX）
- **最低硬體要求：16GB 記憶體**

社區進一步用 TurboQuant 3-bit 量化後（GGUF tq3 格式），效果是：
- 解碼速度：**60-80 tok/s**（M 系列 Mac）
- 上下文長度：**131K**
- 完全離線，無 API 費用

這個場景的決策邏輯完全不同：

**伺服器場景的問題**：「我有 8x H100，要最大化吞吐量，KV Cache 是瓶頸嗎？」  
→ 用 FP8，不用 TurboQuant。

**本地推理的問題**：「我的 Mac 只有 16GB，20B 模型 BF16 需要 40GB+，根本跑不起來，怎麼辦？」  
→ 3-bit 是唯一選項，accuracy 損失是可接受的 trade-off。

在本地推理的世界，**「能跑」本身就是贏**。

---

## 五個 Takeaway（Eldar 的版本，加上我的補充）

**Takeaway 1（Eldar）：FP8 是 KV Cache 量化的最佳預設**  
2x 容量，零吞吐量代價，幾乎無精確度損失。如果你在跑 vLLM，先開 `--kv-cache-dtype fp8`，再考慮其他選項。

**Takeaway 2（Eldar）：TurboQuant k8v4 沒有實質優勢**  
只比 FP8 多 0.4x 容量（2.4x vs 2x），代價是 20-34% 吞吐量損失。數學不成立。

**Takeaway 3（Eldar）：TurboQuant 4bit-nc 是最實際的 TQ 變體**  
記憶體嚴重不足時，3.4x 容量 + 1-4 分精確度損失，可接受。但要先測你的 use case。

**Takeaway 4（Eldar）：3-bit 變體不適合生產**  
reasoning 任務 -20 分、長上下文 -30%，吞吐量最差。除非你完全不做推理任務。

**Takeaway 5（我的補充）：本地推理的判斷標準不同**  
對本地推理用戶而言，TurboQuant 3-bit 讓 20B+ 模型從「不可能」變成「可能」。這個技術是有意義的，只是不要拿伺服器的標準去評估它。

---

## 最後說一件事

TurboQuant 論文本身是否有學術創新，這個問題工程師們也在討論。

Tim Dettmers（量化領域知名研究者）和 Dan Alistarh 都提供了一些歷史背景，vLLM 的 PR 討論串也有相關討論（github.com/vllm-project/vllm/pull/40194）。

但這篇文章不是要評判論文的新穎性。

我想說的是：**量化技術現在分裂成兩個世界，有兩套評估標準。** 一套是伺服器吞吐量和生產精確度，另一套是「我的 MacBook 能不能跑這個模型」。

這兩套標準都是真實需求，只是服務不同的人。

如果你在企業部署 LLM，先用 FP8，不要被論文的 3-bit 數字吸引。  
如果你想在自己電腦上跑 20B 模型，TurboQuant 3-bit 可能正好是你需要的東西。

認清自己在哪個世界，才能做對的決定。

---

## 附錄：一張 Consumer GPU 能跑什麼？

既然談到本地推理，順便補一個實際問題：這次 benchmark 測的 4 個模型，在 RTX 4090 / 5090 + 64GB RAM 上能跑哪些？

**先看模型 VRAM 需求：**

| 模型 | BF16 需求 | 4090（24GB） | 5090（32GB） |
|---|---|---|---|
| Qwen3-30B-A3B（MoE） | ~60GB | ✅ INT4 ~15GB | ✅ FP8 剛好 / INT4 舒適 |
| Llama-3.3-70B | ~140GB | ❌ | ❌（需雙卡） |
| MiniMax-M2.7（200B+） | ~400GB+ | ❌ | ❌ |

4 個 benchmark 模型裡，consumer GPU 只能跑 **Qwen3-30B-A3B**。

### 一張 5090（32GB）怎麼配最甜

| 目標 | 配法 | VRAM 分配 | 速度 | 上下文 |
|---|---|---|---|---|
| 日常使用 | INT4 + FP8 KV | 15GB 權重 ＋ 14GB KV | ~50 tok/s | 64K |
| 長文件分析 | INT4 + TQ 4bit-nc | 15GB 權重 ＋ 14GB KV | ~40 tok/s | 100K+ |
| 最高精確度 | FP8 權重 + BF16 KV | 30GB ＋ 2GB | ~60 tok/s | ~2K |

**推薦：INT4 + FP8 KV Cache**。15GB 放模型，14GB 放 KV Cache，64K 上下文 + 50 tok/s，對個人或小團隊夠用。64GB RAM 在這個配置下幾乎是備用——除非要跑 CPU offload（會掉到 5-12 tok/s，不推薦）。

```bash
# vLLM（生產級，支援 FP8 KV + TurboQuant）
vllm serve Qwen/Qwen3-30B-A3B-Instruct \
  --quantization awq \
  --kv-cache-dtype fp8

# 或 Ollama（最省事）
ollama run qwen3:30b-a3b
```

---

**數據來源：**  
- [vllm.ai TurboQuant Benchmark](https://vllm.ai/blog/turboquant)（Eldar Kurtić, Miguel Goin, Alexandre Marques）  
- [TurboQuant 論文 arXiv 2504.19874](https://arxiv.org/abs/2504.19874)（Google Research，ICLR 2026）  
- [Eldar Kurtić @_EldarKurtic X Thread](https://x.com/_EldarKurtic/status/2053809608976666758)  
- [OpenAI gpt-oss 模型發布](https://openai.com/index/introducing-gpt-oss/)
