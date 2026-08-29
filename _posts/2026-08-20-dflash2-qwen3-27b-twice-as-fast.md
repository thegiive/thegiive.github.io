---
layout: post
title: "DFlash 2 讓 Qwen3.8-27B 快了兩倍：同模型、同輸出、同一張卡，純粹靠更聰明的推理"
date: 2026-08-20 12:00:00 +0800
permalink: /dflash2-qwen3-27b-twice-as-fast/
tags: [DFlash 2, Qwen3.8-27B, block diffusion, speculative decoding, inference optimization, 推論加速, SGLang, vLLM, llama.cpp, tok/s, 地端推論, on-premise, GPU inference]
image: /assets/images/dflash2-benchmark-cover.png
description: "DFlash 2 用 block diffusion 平行草稿 + 路徑選擇器 + 動態卷積，把 Qwen3.8-27B 的推理速度從 28.9 tok/s 推到 59.1 tok/s。已經進 SGLang、vLLM、llama.cpp，drop-in 升級，輸出完全一致。這不是品質換速度的取捨，是推理層的免費加速。"
---

同一個模型、同一張卡、同樣的輸出——速度翻倍。

DFlash 2 剛釋出，Inco AI 和 Z Lab 聯手把 speculative decoding 推到新的水準。拿 Qwen3.8-27B 實測，baseline autoregressive 跑出 28.9 tok/s，換上 DFlash 2 直接到 59.1 tok/s。不是換模型、不是降精度、不是犧牲品質，純粹是推理引擎層的升級。

這篇拆解 DFlash 2 到底做了什麼、為什麼能快這麼多、怎麼用。

## 先講結論：數字說話

Qwen3.8-27B 在 H200 上的 throughput 數據（SGLang，greedy decoding）：

| 任務 | Autoregressive | DFlash 2 | 加速倍率 |
|------|---------------:|---------:|---------:|
| GSM8K | 68.8 tok/s | 236.1 tok/s | 3.43× |
| MATH-500 | 69.1 tok/s | 230.7 tok/s | 3.34× |
| MT-Bench | 68.9 tok/s | 184.0 tok/s | 2.67× |

單一請求最高 3.43 倍，8 個並行請求還能維持 2.84 倍。這不是實驗室數字，是 SGLang 生產級 serving 框架跑出來的。

DFlash 2 釋出不到 48 小時，X 上已經一堆人拿自己的硬體跑出數字：

| 硬體 | 測試者 | Baseline | DFlash 2 | 加速 |
|------|--------|----------:|---------:|-----:|
| A100 | [Fahd Mirza](https://x.com/fahdmirza/status/2089944918584381541) | 28.9 tok/s | 59.1 tok/s | 2.04× |
| RTX 4090 | [Alok](https://x.com/analogalok/status/2089979723166200196) | 60 tok/s (MTP) | 90 tok/s | 1.50× |
| RTX 4090 | [Eric](https://x.com/outsource_/status/2089872776752468129) | — | 109 tok/s | — |
| RTX 5090 | [Austin](https://x.com/TrickRiggin/status/2090202987813916903) | 56.8 tok/s | 123.1 tok/s | 2.17× |
| M5 Max MacBook | [Zhijian Liu（作者）](https://x.com/zhijianliu_/status/2089836737132650504) | — | 70 tok/s | 4.6× vs AR |
| oMLX (Mac) | [Ivan Fioravanti](https://x.com/ivanfioravanti/status/2090006978772804021) | 34 tok/s (AR) / 79 (MTP) | 88 tok/s | 2.59× vs AR |

消費級硬體也吃得到，而且數字很扎實——這些是各自獨立跑出來的。

## DFlash 2 到底做了什麼？

要理解 DFlash 2，先回頭看 speculative decoding 的基本邏輯。

### Speculative decoding 101

傳統 autoregressive 推理：生一個 token、跑一次 forward pass、再生一個。GPU 大部分時間在等記憶體搬資料，compute 利用率低得可憐。

Speculative decoding 的想法很簡單：用一個小的 draft model 快速猜多個 token，再讓大模型一次性驗證。猜對的直接用，猜錯的從那裡重來。驗證多個 token 的成本跟驗證一個差不多（都是一次 forward pass），所以猜對率愈高、省的時間愈多。

### DFlash 1 的突破：Block Diffusion

DFlash 1（2026 年 1 月，ICML 2026）的核心觀察：傳統 draft model 還是一個一個 token 生，為什麼不一次生一整塊？

它用 block diffusion model 取代 autoregressive drafter——一次 forward pass 就預測整個 block 的 K 個 token。生 K 個 token 的成本約等於生 1 個，因為是平行推理。EAGLE-3 要 K 步才能產出 K 個候選，DFlash 一步搞定。

DFlash 1 在 Qwen3-8B 上拿到 6 倍加速，比 EAGLE-3 快 2.5 倍，下載量突破 350 萬。

### DFlash 2 的三個改進

DFlash 2 在 DFlash 1 的基礎上加了三件事，每一件都不大，合起來多擠出「每次驗證多一整個 token」的效果。

**1. 保留多候選（Keep Top-16）**

DFlash 1 每個位置只留最高機率的一個 token。DFlash 2 改成保留 top 16 個候選。這不是新想法，但 DFlash 2 做到不增加計算量的前提下利用這些候選。

**2. 輕量路徑選擇器（Path Selector）**

16 個位置 × 16 個候選 = 理論上有 16⁸ 條路徑。暴力搜尋不可能。

DFlash 2 的路徑選擇器用 bilinear attention 對相鄰位置的候選配對打分：

```
S_t(a, b) = U_t(b) + ⟨A(a) ⊙ H(h_t), B(b)⟩
```

U 是 unigram 分數（這個 token 本身多好），後面那項是 bigram 分數（前一個 token 是 a 的情況下，b 有多合理）。用 Viterbi 動態規劃一掃就能找出最佳路徑。

代價？只加了 200 萬參數（+0.6% 延遲）。效果？greedy decoding 下 acceptance length 多 0.34 token。

**3. 雙抽動態卷積（Two-Tap Dynamic Convolution）**

Block diffusion 有個固有問題：block 尾端的預測品質會衰減（suffix decay），因為每個位置的預測是獨立的，缺乏局部依賴。

DFlash 2 在 attention 和 feed-forward 層前後插入動態卷積：每個位置的表示會混入前一個位置的資訊。16 個 channel 共享一個修正。

代價？1,650 萬參數（佔整體 3%），0.7% 延遲。效果？5 層 backbone 逼近 15 層的預測品質。

### 三件事加起來

DFlash 2 vs DFlash 1，per-request mean acceptance length：

| 模型 | DFlash 1 | DFlash 2 | 提升 |
|------|----------:|----------:|-----:|
| Qwen3.5-4B | 4.92 | 5.97 | +1.05 |
| Qwen3.8-27B | 4.28 (MTP) | 4.80 | +0.52 |
| Muse Glimmer | 4.44 | 5.70 | +1.26 |

每次驗證多接受約一個 token，聽起來不多？但 speculative decoding 每秒跑幾十次驗證，每次多一個 token 就是直接翻倍。

## 輸出完全一致——這很重要

這不是「快但有點不一樣」的那種加速。

DFlash 2 是 lossless speculative decoding：greedy decoding 下，輸出跟原本的 autoregressive 逐 token 推理完全相同；sampling 模式下，保持目標模型的機率分佈不變。

驗證步驟就是讓目標模型自己跑一次 forward pass 確認，任何跟目標模型不一致的 token 都會被拒絕。數學上可證明輸出分佈不變。

## 怎麼用？

DFlash 2 已經進了主流推理框架，都是 drop-in 升級。

### SGLang

```bash
pip install "sglang[all] @ git+https://github.com/sgl-project/sglang.git#subdirectory=python"

python -m sglang.launch_server \
  --model-path Qwen/Qwen3.8-27B \
  --speculative-algorithm DFLASH \
  --speculative-draft-model-path incoai/Qwen3.8-27B-DFlash2 \
  --speculative-num-draft-tokens 8
```

### vLLM

```bash
vllm serve Qwen/Qwen3.8-27B \
  --speculative-config '{
    "method": "dflash",
    "model": "incoai/Qwen3.8-27B-DFlash2",
    "num_speculative_tokens": 7
  }'
```

目前需要 vLLM nightly。

### llama.cpp

llama.cpp 支援已經在 PR 中，GGUF 量化版也有了（`incoai/Qwen3.8-27B-DFlash2-GGUF` 和 `z-lab/Qwen3.8-27B-DFlash2-GGUF`），可以在 Ollama、LM Studio 裡跑。

### macOS

oMLX 有預建的 macOS 應用，M 系列晶片直接用。

## 社群的保留意見——不是銀彈

數字很漂亮，但 X 上也有踩坑回報，值得記下來：

**1. Mac 上 Lightning MTP 可能更快**

[CylentSec 在 M5 Max 上實測](https://x.com/cylentsec/status/2090172518627672120)：DFlash 2 只跑到 31 tok/s，Lightning MTP 反而有 48 tok/s。不是所有平台、所有量化組合都穩贏。如果你在 Mac 上已經用 MTP 跑得很順，先 benchmark 再決定要不要換。

**2. 結構化輸出加速最明顯，free prose 收益較小**

[Yume_X 提醒](https://x.com/yume_arasaki/status/2090189859302625487)：DFlash 2 在 math 和 code 這類結構化輸出上加速最猛，free prose 不一定贏原生 MTP。這合理——結構化文本的 token 可預測性高，draft model 猜對率自然也高。

**3. llama.cpp 還沒正式 merge**

目前要用 llama.cpp 跑 DFlash 2，得自己 pull PR #27342 然後 build。不是下載就能用的穩定版。SGLang 和 vLLM 的支援比較成熟，但 vLLM 也還在 nightly。

## 什麼時候該用、什麼時候不該

**適合用的場景：**
- batch size 低（1~8），GPU 有閒置 compute
- 輸出較長（reasoning、code generation、長文生成）
- 需要加速但不能降品質
- NVIDIA GPU（目前實測數據最豐富、加速最穩定）

**不適合的場景：**
- batch size > 32（並行請求太多，GPU compute 已經吃滿）
- 輸出很短（< 50 tokens，speculative decoding 的 overhead 抵消收益）
- 沒有對應的 draft checkpoint
- Mac 上已經用 Lightning MTP 跑得很好（先 benchmark 再決定）
- 主要跑 creative writing / free prose（收益可能不如 structured 任務）

推薦的 draft token 數量：instruction 任務用 8，混合任務用 6，creative 任務用 4。

## 實戰踩坑：RTX 5090 + NVFP4 量化的完整記錄

理論歸理論，我在自己的 RTX 5090（32GB VRAM）上實際跑了一輪。結論先講：**207 tok/s，3.34 倍加速，確實猛**——但中間踩了七個坑，每一個都會讓你卡住。

### 坑 1：SGLang 正式版還沒有完整 DFlash 2 支援

必須使用包含 DFlash 2 merge 的特定 commit：

```
SGLang commit: c14312a66420b75ca9a11bf1817c4db1fa26b097
版本: 0.5.6.post3.dev9094+gc14312a66
```

建議升級前先備份整個虛擬環境，我的備份在 `sglang-env-pre-dflash2-20260820`。

### 坑 2：官方範例用 dense BF16，但 5090 塞不下

官方範例直接用 `Qwen/Qwen3.8-27B`（BF16），完整 27B 要 54GB，5090 只有 32GB。所以實際使用 `RadixArk/Qwen3.8-27B-NVFP4`。

然後 DFlash 2 直接報錯：

```
RuntimeError:
DFlash2 selector requires a dense FP16/BF16/FP32 target lm_head.
```

原因：這個 NVFP4 checkpoint 把 `lm_head` 也量化了，DFlash 2 的 selector 預設只接受 dense weight。

### 坑 3：`--enable-fp32-lm-head` 不能解決問題

這個參數只是讓 logits 輸出轉成 FP32，並不會把量化後的 `lm_head` 還原成 dense weight。加了仍然過不了 DFlash 2 的 selector 檢查。

### 坑 4：必須手動補 NVFP4 lm-head 相容路徑

最後修改了 SGLang 的 `dflash.py`：

```
路徑: sglang/srt/models/dflash.py
```

核心邏輯：如果 `lm_head.weight` 不是 FP16/BF16/FP32，就改用 SGLang 已有的 `lm_head.quant_method.apply()` 做 top-k candidate selection。

限制：目前這個相容補丁只支援 TP=1，剛好符合單張 5090。

### 坑 5：FlashInfer FP8 BMM 的 CUBLAS 初始化失敗

遇到 `CUBLAS initialization failed`，修改 `fp8_utils.py` 把 BMM backend 從 `cublas` 改成 `cudnn` 解決。

### 坑 6：關掉 Decode CUDA Graph 速度會崩

除錯期間用了 `--cuda-graph-backend-decode disabled`，結果 DFlash 2 只跑出 63.85 tok/s。恢復 Decode CUDA Graph 後直接跳到 207.52 tok/s——**差距超過三倍**。

Prefill CUDA Graph 則可以安全關閉（`--disable-prefill-cuda-graph`），不影響 decode 加速。

### 坑 7：記憶體非常接近上限

執行中 VRAM 使用 29,076 / 32,607 MiB，大致分佈：

| 項目 | 估計用量 |
|------|--------:|
| Target NVFP4 weights | 20.14 GB |
| DFlash 2 draft model | 3.72 GB |
| Mamba/intermediate | ~1.5 GB |
| 其餘（KV cache、CUDA Graph、workspace） | ~3.7 GB |

最終啟動參數：

```bash
--mem-fraction-static 0.85 \
--max-running-requests 1 \
--max-mamba-cache-size 4 \
--kv-cache-dtype fp8_e4m3
```

不建議把 `mem-fraction-static` 改回 0.95，長 context 或 CUDA Graph capture 時可能 OOM。

### 最終 benchmark 數字

測試條件：RTX 5090、Qwen3.8-27B-NVFP4、單一 request、temperature=0、thinking off、固定 prompt、每次輸出 1024 tokens。

| 方法 | Decode 速度 | Wall Time | 備註 |
|------|------------:|----------:|------|
| 純 Autoregressive | 62.14 tok/s | 16.58 sec | baseline |
| DSpark | 152.14 tok/s | — | speculative decoding 替代方案 |
| DFlash 2（無 CUDA Graph） | 63.85 tok/s | — | 沒有使用價值 |
| **DFlash 2（有 CUDA Graph）** | **207.52 tok/s** | **5.03 sec** | 三次結果穩定：205.0 / 207.6 / 207.5 |

換算加速：

| 比較 | 倍率 | 提升幅度 |
|------|-----:|--------:|
| DFlash 2 vs 純 AR | 3.34× | +233.9% |
| DFlash 2 vs DSpark | 1.36× | +36.4% |

Speculative decoding 統計：平均接受長度約 4–5 tokens，接受率約 50–60%，最高區段速度約 247 tok/s。

### 品質註記

DFlash 2 三次輸出彼此完全一致（hash 相同），但**沒有和純 autoregressive 得到相同的 byte-level hash**。

```
純 AR hash:     81ea7773c4c275f128eaac6cffe9e3d431d5f375...
DFlash 2 hash:  6f3a75025b5ef5885c3ef54874bd0a3ad53d8895...
DSpark hash:    3172b2b91e6dfc035b557a62b7f432b43d388567...
```

三者各不相同。原因可能是 NVFP4 量化 lm-head 的相容路徑引入了微小的數值差異。在 dense BF16 target 上，DFlash 2 的 lossless 保證是數學可證的；但在量化 target + 自訂相容補丁的情況下，目前不能宣稱與純 AR「逐 token 完全相同」。

速度大幅提升、輸出穩定可復現——對實際應用來說，這已經夠用了。

## 四人同時用：720 tok/s 總吞吐

單人跑得快是一回事，能不能同時服務多人才是地端部署的真問題。我們拿同一張 RTX 5090 測了四人同時送 request 的場景。

### 測試條件

4 個請求同時送出，每人生成 1024 tokens，temperature=0，thinking off。

### 暖機後結果（第二輪）

| 使用者 | Decode 速度 | 完成時間 |
|--------|------------:|----------:|
| User 1 | 187.19 tok/s | 5.69 sec |
| User 2 | 214.87 tok/s | 4.98 sec |
| User 3 | 192.19 tok/s | 5.54 sec |
| User 4 | 192.42 tok/s | 5.54 sec |

彙總：

| 指標 | 數值 |
|------|-----:|
| 每人 decode 中位數 | 192.30 tok/s |
| 四人總吞吐 | 719.84 tok/s |
| TTFT 中位數 | 222 ms |
| 完成時間中位數 | 5.54 sec |
| 總輸出 | 4,096 tokens |

冷啟動（第一輪）數字則是：四人總吞吐 575.48 tok/s、每人中位數 178.48 tok/s、TTFT 中位數 1.16 秒。暖機後提升明顯。

### 四人並行的專用設定

要讓四人真正同時跑起來，不能直接套用單人設定。以下是調整過的參數和原因：

```bash
--mem-fraction-static 0.95 \
--max-total-tokens 8192 \
--max-running-requests 4 \
--max-mamba-cache-size 4 \
--disable-radix-cache \
--cuda-graph-max-bs-decode 4
```

每個參數都有理由：

- **`--disable-radix-cache`**：關鍵。Radix cache 開啟時，每個請求需要 4 個 Mamba state slots；關閉後降到 1，才能真正同時跑四人。
- **`--cuda-graph-max-bs-decode 4`**：避免預設捕捉到 batch 24 而 OOM。
- **`--max-total-tokens 8192`**：避免 SGLang 把剩餘 VRAM 全拿去建立 40K 的 KV cache，保留 CUDA Graph workspace。
- **`--mem-fraction-static 0.95`**：四人模式下可以比單人（0.85）更積極，因為 KV cache 總量已經被 `max-total-tokens` 限住。

### 目前服務狀態

```
服務：       active
Health：     HTTP 200
並行上限：   4
KV token 池：8192
VRAM：       31,211 / 32,607 MiB
```

### 適用與限制

這個設定是**四人吞吐優先**。Radix prefix cache 已關閉，8192 是所有執行中請求共用的 token pool。適合四人一般對話或每人約 1–2K context，**不適合四個人同時跑超長 context**。如果需要更長的 context window，要降低並行數或增加 `max-total-tokens`（但可能 OOM）。

換個角度看：一張 32GB 的消費級顯卡，跑 27B 量化模型 + DFlash 2，同時服務四個人，每人還有接近 200 tok/s。這在半年前是不可能的數字。

## 更大的圖景

DFlash 2 代表的趨勢很清楚：**推理加速的下一波紅利來自推理層，不是模型層。**

同一個模型、同一張卡，光靠更聰明的 speculative decoding 就能翻倍。這意味著：

1. **硬體升級不是唯一出路。** 你的 4090 或 A100 還沒被榨乾，推理框架的進步可以讓現有硬體再撐一輪。
2. **地端部署的 cost/performance 重新計算。** 原本覺得 27B 太慢不堪用的場景，現在可能可以了。
3. **框架選擇比以前更重要。** SGLang、vLLM、llama.cpp 誰先整合新的推理技術，誰的用戶就先吃到紅利。

DFlash 1 從今年一月到現在半年多，下載量 350 萬。DFlash 2 帶著更好的數字來了，應該會更快。

值得花十分鐘把你的推理 pipeline 升級一下。

---

**參考資料：**

- [DFlash 2: Keep Drafting Parallel — Inco AI](https://inco.ai/blog/dflash2/)
- [DFlash: Block Diffusion for Flash Speculative Decoding (ICML 2026)](https://arxiv.org/abs/2602.06036)
- [z-lab/Qwen3.8-27B-DFlash2 — Hugging Face](https://huggingface.co/z-lab/Qwen3.8-27B-DFlash2)
- [incoai/Qwen3.8-27B-DFlash2 — Hugging Face](https://huggingface.co/incoai/Qwen3.8-27B-DFlash2)
- [GitHub: z-lab/dflash](https://github.com/z-lab/dflash)
- [DFlash on GPU Cloud — Spheron](https://www.spheron.network/blog/dflash-block-diffusion-speculative-decoding-gpu-cloud/)
- [Z Lab DFlash Project Page](https://z-lab.ai/projects/dflash/)
