---
layout: post
title: "Mac 用戶等了 16 個月：第一次能用「企業級」LLM 推理加速"
date: 2026-05-21 07:00:00 +0800
permalink: /mac-first-enterprise-inference-stack-mtp/
image: /assets/images/mac-enterprise-inference-mtp-cover.png
description: "硬體上最適合跑大模型的家用機器是 Mac Studio M3 Ultra（256GB 統一記憶體連 RTX 5090 都比不上），但軟體棧上 Mac 用戶過去 16 個月一直被 lock out 於所有現代 LLM 推理加速技術——MTP、EAGLE、Medusa，通通跑不了。直到 2026 年 5 月 16 日，llama.cpp 合併了 PR #22673。這是 Mac 第一次能用上「企業級」的推理加速。"
---

![Mac Studio M3 Ultra MTP unlocked: first time Apple Silicon gets enterprise-tier inference acceleration](/assets/images/mac-enterprise-inference-mtp-cover.png)

## 目錄

- [TL;DR](#tldr)
- [Mac 在 LLM 推理上的奇怪處境：硬體頂、軟體底](#mac-在-llm-推理上的奇怪處境硬體頂軟體底)
- [為什麼 vLLM / SGLang / TensorRT-LLM 永遠不會支援 Apple Silicon](#為什麼-vllm--sglang--tensorrt-llm-永遠不會支援-apple-silicon)
- [過去 16 個月 Mac 用戶的「次優」清單](#過去-16-個月-mac-用戶的次優清單)
- [PR #22673 對 Mac 用戶的意義：從鎖死到打開](#pr-22673-對-mac-用戶的意義從鎖死到打開)
- [為什麼 Mac 應該拿到比 NVIDIA 卡更大的 MTP 紅利](#為什麼-mac-應該拿到比-nvidia-卡更大的-mtp-紅利)
- [誠實揭露：Mac 還沒追上的部分](#誠實揭露mac-還沒追上的部分)
- [對企業 IT 架構師意味著什麼](#對企業-it-架構師意味著什麼)
- [常見問題 Q&A](#常見問題-qa)

## TL;DR

- **Mac 不能跑 vLLM、SGLang、TensorRT-LLM**——沒 CUDA、沒 ROCm，根本起不來
- 過去 16 個月 Mac 跑 LLM 的所有路徑（llama.cpp / MLX / Ollama / LM Studio）**全部沒有 MTP 支援**——意思是 Mac 用戶完全用不到 DeepSeek V3、Qwen3.6 這些模型的內建加速能力
- 2026-05-16 llama.cpp PR #22673 merge 之後，**Mac 第一次有「enterprise tier」的推理加速技術可以用**
- 預期 Mac Studio / Mac mini 拿到的 MTP 加速會**接近 PR 描述的 2.5x（接近頻寬瓶頸機型的紅利上限）**，而不是 RTX 3090 的 1.71x——因為 Apple Silicon 統一記憶體本來就是頻寬 bound 的架構
- 對企業 IT 架構：**公司原本就配發 Mac 給工程師的，現在不用再買 NVIDIA on-prem 機器，也能用生產級推理**

---

## Mac 在 LLM 推理上的奇怪處境：硬體頂、軟體底

從硬體規格表來看，Mac Studio M3 Ultra 是一台很奇怪的機器。

| 機器 | 統一記憶體 / VRAM | 記憶體頻寬 | 價格 |
|------|----------------|----------|------|
| **Mac Studio M3 Ultra（頂規）** | **512GB** 統一記憶體 | ~819 GB/s | ~$14,000 |
| **Mac Studio M3 Ultra（中階）** | **256GB** 統一記憶體 | ~819 GB/s | ~$7,400 |
| RTX 5090 | 32GB GDDR7 | 1,792 GB/s | $2,000（卡）+ 整機 |
| RTX 4090 | 24GB GDDR6X | 1,008 GB/s | $1,600（卡）+ 整機 |
| DGX Spark | 128GB LPDDR5X | ~273 GB/s | $4,699 |

Mac Studio 的優勢非常具體：**整顆 Qwen3.6-27B FP16（54GB）能直接塞進 256GB 統一記憶體，連量化都不用**。RTX 5090 必須先量化到 Q4 / FP8 才塞得進 32GB VRAM——這是檔位的差距。

換句話說：

**如果只看「能不能跑」，Mac Studio M3 Ultra 是家用機器的天花板。**

那為什麼過去一年講本地 LLM 的場合，大家總是先講 NVIDIA 卡？因為**軟體棧上 Mac 被 lock out 於所有現代推理加速技術**。硬體能扛模型權重，但跑得很「素」——只有最基本的 autoregressive decoding，沒有 speculative decoding、沒有 multi-token prediction、沒有 EAGLE / Medusa 這類 draft model 加速。

這是一個典型的「硬體頂、軟體底」處境。

## 為什麼 vLLM / SGLang / TensorRT-LLM 永遠不會支援 Apple Silicon

要理解為什麼 Mac 用戶被 lock out 這麼久，得先理解這些 enterprise 推理框架的技術棧。

| 框架 | 底層依賴 | 在 Mac 上能跑嗎 |
|------|---------|--------------|
| **vLLM** | CUDA / ROCm / TPU | ❌ 完全跑不起來 |
| **SGLang** | CUDA / ROCm | ❌ 完全跑不起來 |
| **TensorRT-LLM** | CUDA + TensorRT | ❌ NVIDIA 獨家 |
| **DeepSpeed-Inference** | CUDA | ❌ 跑不起來 |

這些框架的核心優化（FlashAttention、PagedAttention、continuous batching、speculative decoding kernel）**全部是用 CUDA kernel 寫的**。要在 Apple Silicon 上跑，等於整個 kernel 層要重寫成 Metal——這不是 porting 工作，是重做一份。

**這件事永遠不會發生**，因為：

1. **市場規模不對**：vLLM / SGLang 的主要市場是雲端 GPU 推理服務商，Mac 在這個市場根本不是 target
2. **資源優先級不對**：DeepSeek、Anthropic、OpenAI 內部用 NVIDIA H100 / H200 推理，PR 都優先給 NVIDIA 平台
3. **Apple 自己有 MLX**：Apple 不會去推動別人優化 Apple Silicon，他們押在自己的 MLX 框架

所以結論很清楚：**Mac 想用 enterprise tier 的推理加速，唯一的路是 llama.cpp 把這些 feature 一個一個 backport 進來**。

而 llama.cpp 是一個志願者社群 + 部分商業贊助的開源專案，feature 速度當然比不上有完整工程團隊的 vLLM。所以 Mac 用戶享受 enterprise tier feature 的時間差，就是「論文發表 → vLLM 實作 → llama.cpp backport」這個 pipeline 的延遲。

過去這個延遲是**16 個月**（MTP 從 DeepSeek V3 release 到 llama.cpp merge）。

## 過去 16 個月 Mac 用戶的「次優」清單

期間 Mac 用戶不是完全沒得跑——只是每個選擇都有明顯的「不夠專業」之處。

**1. llama.cpp + Metal backend**
- ✅ 跨平台、跨 Apple 全產品線
- ✅ 量化支援完整（GGUF）
- ❌ 沒 MTP、沒 EAGLE、沒 Medusa
- ❌ Metal kernel 通常比 CUDA kernel 慢 30-50%

**2. MLX（Apple 自家框架）**
- ✅ 對 Apple Silicon 架構優化最好
- ✅ 跟 PyTorch API 接近，研究友善
- ❌ **沒有原生 MTP 支援**（即使 Apple 自己也沒做）
- ❌ 量化支援比 GGUF 弱
- ❌ 模型生態小（很多模型沒人轉成 MLX 格式）

**3. Ollama / LM Studio**
- ✅ 一鍵安裝、UI 友善
- ❌ 底層是 llama.cpp，繼承所有 llama.cpp 的限制
- ❌ Release cadence 比 llama.cpp 還慢（要等 upstream 更新後再 bump）

**4. Rapid-MLX（社群專案，相容 OpenAI API）**
- ✅ 在 [Qwen3.6-27B 跑出 36.5 t/s @ M3 Ultra](https://ai-coding.wiselychen.com/qwen-3-6-27b-gb10-home-inference-sonnet-level/)（4-bit）
- ❌ 還是沒 MTP

把這四條路擺在一起，會發現一個尷尬的事實：**Mac 用戶過去一年想用 MTP，沒有任何一條路走得通**。不是「麻煩但能用」，是「根本沒這條路」。

## PR #22673 對 Mac 用戶的意義：從鎖死到打開

這是這篇文章的核心：**llama.cpp PR #22673（2026-05-16 merge）是 Mac 用戶能用 MTP 的第一條路**。

不是「現在多了一個選項」，是「**從零到一**」。

具體解鎖了什麼？

**1. MTP 在 Metal backend 上可運作**
PR 描述明寫了支援 CUDA、Metal、Vulkan 三個 backend。意思是 M1 / M2 / M3 / M4 系列、Mac Studio / Mac mini / MacBook Pro / iMac，**全產品線都能用**。

**2. 不需要重新下載模型**
GGUF 檔案裡如果原本就有 MTP heads 的 tensor（DeepSeek V3 / R1、Qwen3.6 系列），llama.cpp 升版後直接讀。已經下載的權重不浪費。

**3. 跟現有工具鏈相容**
LM Studio、Ollama、KoboldCpp 全部底層是 llama.cpp。預計 1-2 個月內這些工具會 bump 版本，使用者完全不用懂 `--spec-type mtp` 這種 flag，背後就自動開啟。

換句話說：**正在用 Mac Studio 跑 LM Studio 的工程師，再過幾週升級到下一個版本，speed 就會自動變 1.7x-2.5x**。沒有人需要做任何事。

## 為什麼 Mac 應該拿到比 NVIDIA 卡更大的 MTP 紅利

這是技術上最有意思的一段，也是這個 PR 對 Mac 用戶**特別**重要的原因。

MTP 的核心紅利是「**同一次 memory access 算出多個 token**」。直白講：

```
傳統 autoregressive：
  讀一次權重 → 算 1 個 token → 讀一次權重 → 算 1 個 token ...

MTP：
  讀一次權重 → 同時算出 N 個 token 草稿 → 驗證 → 接受 K 個
```

那什麼樣的硬體會從 MTP 拿到最大紅利？答案是**記憶體頻寬 bound 的硬體**。

對照 PR 描述跟社群實測的加速倍率：

| 硬體 | 加速倍率 | 為什麼 |
|------|--------|-------|
| **DGX Spark**（273 GB/s 頻寬）| **2.57x** | 頻寬最差 → 紅利最大 |
| **RTX 3090**（1008 GB/s 頻寬）| **1.71x** | 頻寬充足 → 紅利縮水 |
| **RTX 5090**（1792 GB/s 頻寬）| **~1.87x**（我自己實測）| 頻寬最好 → 紅利再縮 |

**規律很清楚：頻寬越緊張的硬體，MTP 加速越大。**

那 Mac Studio M3 Ultra 落在哪？**819 GB/s**。比 DGX Spark 寬，但比 RTX 3090 緊。

更關鍵的是：**Apple Silicon 統一記憶體架構本來就是「記憶體頻寬 bound」設計**。CPU、GPU、Neural Engine 共享同一條記憶體匯流排，這條匯流排是整個系統的天花板。

所以我的預期是：**Mac Studio M3 Ultra 跑 Qwen3.6-27B 開 MTP，加速倍率會落在 2.0x ~ 2.4x 區間**，比 RTX 5090 上的 1.87x 更好。

如果這個預期成立，意思是：

- M3 Ultra 跑 Qwen3.6-27B 在沒 MTP 時大概 20-25 t/s（社群實測）
- 開 MTP 之後預期會到 **45-55 t/s 單流**
- 這個速度對「一個工程師、一個 chat 框」的 interactive coding 場景**完全夠用**

對比 Sonnet 4.6 API 的 60-80 t/s streaming，Mac Studio 跟商業 API 的差距會縮到 1.5x 以內——而且沒有網路延遲、沒有 rate limit。

## 誠實揭露：Mac 還沒追上的部分

寫到這裡得潑點冷水。Mac 用上 MTP 不代表追平 NVIDIA。

**1. Metal kernel 效率還是輸 CUDA kernel**
即使有 MTP，底層的 attention / matmul kernel 在 Apple Silicon 上的實作通常比 CUDA 慢 20-40%。MTP 給的是「整體吞吐」的加速，不會修補 kernel 層的差距。

**2. MLX 還沒有 MTP**
Apple 自家的 MLX 框架到 2026 年 5 月為止還沒實作 MTP。如果你的 workflow 是 MLX-based（例如用 mlx-lm 寫研究 code），這個 PR 對你沒用，要等 MLX 團隊跟進。

**3. 並發場景 Mac 還是輸**
跟 NVIDIA 卡一樣，llama.cpp + MTP 目前強制 `n_parallel=1`。如果你想用 Mac Studio 服務團隊（5-10 人同時用），這個 setup 不適合，要切回沒 MTP 的設定。但因為 vLLM 不支援 Mac，所以 Mac 在「並發 serving」這個場景**沒有好答案**。

**4. 實測數字還沒大量出現**
PR 才 merge 一週多，Mac 用戶的實測 benchmark 還沒充分湧現。我前面講的「2.0x-2.4x 預期」是基於頻寬論證，不是實測。實際數字要再等幾週社群 benchmark 累積。

**5. M1 / M2 機器加速可能比 M3 / M4 小**
PR 用了一些新的 ggml 操作，這些操作在 M3 / M4 上有專門優化，M1 / M2 可能落到 fallback 路徑，加速幅度會縮水。

## 對企業 IT 架構師意味著什麼

這次解鎖最關鍵的影響是**改寫了 Mac 在企業 AI 架構裡的角色**。

過去六個月，企業評估 on-prem AI Coding 的標準答案是：
- 買 DGX Spark / RTX 5090 工作站
- 跑 Qwen3.6-27B / DeepSeek V3
- 跑 vLLM 服務多個工程師

這個方案的問題是「**多了一份硬體 + 多了一份運維**」。很多矽谷公司本來就配發 Mac Studio 或 MacBook Pro 給工程師——這些機器原本只是「終端」，不是「推理 server」。

PR #22673 改變了這個假設：

**配發給工程師的 Mac Studio M3 Ultra 256GB**，本身就是一台**單人推理 server**。
- 硬體扛得動 Qwen3.6-27B 不量化版本
- 軟體（llama.cpp + MTP）給出 enterprise tier 加速
- 速度預期 45-55 t/s，interactive coding 完全夠用
- 不用任何額外採購、不用 IT 部署 K8s

這對 IT 架構的意義：

**1. on-prem AI Coding 的 TCO 重算**
原本要算「採購 NVIDIA 工作站 + 運維」，現在可以走「公司本來就配的 Mac，多開一個推理 process」。TCO 直接砍掉硬體採購線。

**2. 資安合規場景多一個答案**
金融 / 法律 / 醫療這些不能 call cloud API 的場景，過去的答案是「on-prem NVIDIA」，現在多了「員工自帶 Mac Studio 跑本地推理」這個選項。資料完全不離開員工那台機器。

**3. 不同團隊的工具策略可以分流**
- **研發團隊（個人工作流）**：MacBook Pro / Mac Studio + LM Studio + MTP → 個人單流
- **平台團隊（共用服務）**：NVIDIA 工作站 + vLLM + AWQ + 並發 batching → 多用戶
- **這兩條路不衝突，可以同時走**

換個方式講：**Mac 在 LLM 推理上從「次優選擇」升級成「特定場景的最佳選擇」**——特別是「一人一台、不需要共享、不能上雲」這類場景。

## 常見問題 Q&A

**Q: 我用 Mac mini M4 / MacBook Pro M3，這個更新有用嗎？**

有用，但效果取決於記憶體大小。M4 Mac mini（24GB / 32GB）能跑 Qwen3.6-27B Q4 量化版本（約 16GB），開 MTP 預期加速 1.8x-2.2x。MacBook Pro M3 Max（36GB / 64GB / 128GB）可以跑更大模型，加速幅度類似。

**Q: 我已經在用 LM Studio，需要做什麼？**

短期內不用做什麼。等 LM Studio 下一版升上 llama.cpp 的新 master（樂觀估計 1-2 個月內），更新後 MTP 會自動啟用。如果你想立刻試，可以直接編譯 llama.cpp master + 手動下 CLI。

**Q: MLX 跟 llama.cpp，Mac 用戶該選哪個？**

短期內如果重視速度，選 llama.cpp（有 MTP）。如果你的工作流是研究 / fine-tuning / 需要 PyTorch-like API，繼續用 MLX。中期看 MLX 會不會跟進 MTP——如果跟進了，MLX 在 Apple Silicon 上的 kernel 效率本來就比 llama.cpp 好，到時會反超。

**Q: Mac Studio M3 Ultra 跟 RTX 5090 該怎麼選？**

不是同個量級的決策。RTX 5090 適合「跑量化模型 + 並發 serving + 想用 vLLM 整套」；Mac Studio M3 Ultra 適合「跑大模型不量化 + 單人 interactive + 安靜省電」。如果你已經有 Mac，加 MTP 是免費升級；如果還沒買，看你的 workload 偏哪邊。

**Q: 為什麼說 MTP 是「enterprise tier」？**

因為過去這項技術只在 vLLM / SGLang / TensorRT-LLM 這些企業推理棧裡可用——換句話說，要享受 MTP 的人要有 CUDA 卡、要會起 Python server、要懂 deployment。家用 GGUF 路線（llama.cpp / Ollama / LM Studio）的使用者完全用不到。PR #22673 把這個技術從 enterprise tier 下放到家用 tier，而 Mac 是這次下放的最大受益者——因為 Mac 連 enterprise tier 都進不去。

---

## 結語

PR #22673 對大多數人來說是「llama.cpp 又更新一個 feature」，但對 Mac 用戶來說是**整整 16 個月的等待結束**——第一次能用上跟 H100 推理伺服器同等級的加速技術。

更有意思的是，從頻寬論證來看，Mac 拿到的紅利可能比 NVIDIA 消費卡還大。

我接下來會在我朋友的 Mac Studio M3 Ultra 256GB 上實測 Qwen3.6-27B 開 MTP 前後的數字，搭配前面 [RTX 5090 跑出 140 tok/s 的 benchmark](https://ai-coding.wiselychen.com/qwen-3-6-27b-rtx-5090-inference-engine-benchmark/) 做完整對照。預期會看到 Mac 的相對加速幅度大過 RTX 5090——但具體數字要實測才算。

數據出來再分享。

---

**相關文章：**
- [llama.cpp 終於合併 MTP：你的 DeepSeek / Qwen3.6 一直少跑了 30-60% 的速度](https://ai-coding.wiselychen.com/llama-cpp-mtp-merged-local-llm-2x-speedup/)
- [Qwen 3.6-27B 在 RTX 5090 上的 inference engine benchmark](https://ai-coding.wiselychen.com/qwen-3-6-27b-rtx-5090-inference-engine-benchmark/)
- [Qwen 3.6-27B 在 DGX Spark 跑出 Sonnet 4.6 等級](https://ai-coding.wiselychen.com/qwen-3-6-27b-gb10-home-inference-sonnet-level/)

**參考資料：**
- [llama.cpp PR #22673: llama + spec: MTP Support](https://github.com/ggml-org/llama.cpp/pull/22673)
- [vLLM Speculative Decoding docs (MTP)](https://docs.vllm.ai/en/latest/features/speculative_decoding/mtp/)
- [Reddit: r/LocalLLaMA "That's a good news..."](https://www.reddit.com/r/LocalLLaMA/comments/1teqnf2/thats_a_good_news/)
