---
layout: post
title: "RTX 5090 + Qwen3.6-27B 七種推論引擎實測：Sonnet 4.6 等級的本地推論，NT$30 萬桌機跑得起來嗎？"
date: 2026-05-15 07:00:00 +0800
permalink: /qwen-3-6-27b-rtx-5090-inference-engine-benchmark/
image: /assets/images/qwen-3-6-27b-rtx-5090-build-cover.png
description: "Qwen 3.6-27B 接近 Sonnet 4.6，能不能塞進 NT$30 萬桌機？答案是能。但同一張 5090、同一個模型，七種推論引擎跑出 64 tok/s 到 575 tok/s 的兩種命運。這篇是 vLLM / llama.cpp / Ollama 全跑過一輪的避坑筆記。"
tags:
  - 本地 LLM
  - RTX 5090
  - Qwen3.6
  - vLLM
  - llama.cpp
  - Ollama
  - IT 架構
---

![RTX 5090 自組工作站：ROG 機殼 + 360 AIO 水冷 + TUF Gaming 主機板](/assets/images/qwen-3-6-27b-rtx-5090-build-cover.png)

## TL;DR

- **核心問題**：Qwen 3.6-27B ≈ Sonnet 4.6 等級，**這個能力能塞進 NT$30 萬以下的桌機嗎？** 答案：**能，整套 NT$30 萬剛剛好卡進企業 IT 採購的桌機/工作站預算天花板**
- **2026 是本地小模型性價比騰飛的元年** — RTX 5090（32GB VRAM）配 Qwen3.6-27B，單流 140 tok/s、並發 575 tok/s 都做得到
- **七種配置實測**：vLLM × 3、llama.cpp × 2、Ollama × 2，外加一個直接 OOM 的失敗案例
- **三個冠軍**：
  - 單流最快：**llama.cpp + MTP（Q2_K_XL）→ 140 tok/s**
  - 並發最強：**vLLM AWQ-INT4 → 575 tok/s @ 並發 8**
  - 開箱即用體驗最好但效能最差：**Ollama Q4_K_M → 64 tok/s（並發完全不擴展）**
- **最反直覺發現**：同一個 Q4_K_M GGUF，llama.cpp 比 Ollama **並發吞吐快 3.2x** — Ollama 把 batching 給關了
- **量化命名不可信**：標榜 "GPTQ-Int4" 的模型實測載入 27.5 GiB（應 ~13.5 GiB），attention/visual layer 還是 BF16

---

## 為什麼這又是一篇「無聊 IT 架構」文

又一篇 IT 架構系列文，不是炫耀 benchmark。

過去半年我一直在追這條線：**「本地 LLM 到底什麼時候 ROI 翻過來」**。前幾個月寫過 [DGX Spark 跑 Qwen3.6-27B](/qwen-3-6-27b-gb10-home-inference-sonnet-level/) 的觀察 — 那篇結論是「家用 AI 工作站時代到了」。但 DGX Spark 是 $4,699 的特規機，買的人還不多。

這次我自己組了一台桌機（消費級零組件），想回答一個非常具體的性價比問題：

> **「Qwen 3.6-27B 既然被認為接近 Sonnet 4.6 等級，那這個能力能不能塞進一台 NT$30 萬以下的桌機？選錯引擎會差多少？」**

NT$30 萬是企業 IT 採購一台「中高階桌機/工作站」的常見上限 — 過了這條線就要走資產採購、董事會審核。如果跑 Sonnet 4.6 等級的本地 AI 必須花 NT$50 萬以上，那這條路就還是只有 R&D 部門能玩，business unit 進不來。

實測答案：**整套 NT$30 萬剛好卡進企業預算天花板。** 而且這台桌機單流跑得贏多數 API 的速度（140 tok/s）、並發吞吐到 575 tok/s（GPT-4o-mini 級別）。對比之下，2025 年要跑同樣等級的模型只能買 H100，光一張卡就 NT$100 萬起跳 — **整整貴三倍以上**。

**但前提是你選對引擎、選對量化、跳過三個坑。** 選錯的話，同一張卡跑出 2x tok/s — 你會以為本地 LLM 還是不能用。

---

## 四個維度看 LLM 推論的選擇地圖

判斷一個 LLM 推論方案值不值得用，看四個維度就夠了：**模型能力、單人 tok/s、多人併發 tok/s、token/NT$**。把市面上主流方案攤開來比：

| 方案 | 模型能力 | 單人 tok/s | 多人併發 tok/s | NT$/1M tokens |
|---|---|---|---|---|
| Claude Sonnet 4.6 API | ★★★★★ 旗艦 | ~80 | 無上限 | ~270 |
| GPT-4o-mini API | ★★★ 入門 | ~120 | 無上限 | ~11 |
| **RTX 5090 + Qwen3.6-27B（最佳引擎）** | **★★★★ ≈ Sonnet 4.6** | **140** | **575** | **~10** |
| Mac Studio M3 Ultra + Qwen3.6-27B | ★★★★ | ~45 | 受限 | ~60 |
| DGX Spark + Qwen3.6-27B | ★★★★ | 136 | ~200 | ~15 |
| H100 server + Qwen3.6-27B | ★★★★ | ~150 | 1000+ | ~12（但 27B 用不滿，殺雞用牛刀）|

四個維度怎麼讀：

1. **模型能力** — 決定 workload 可不可行。Qwen3.6-27B ≈ Sonnet 4.6 是 2026 才有的事，過去本地模型都還停在 GPT-3.5 等級
2. **單人 tok/s** — 影響 IDE 補全、即時對話延遲。5090 + MTP 140 tok/s 連雲端 API 都比不上，因為 API 還要算 network RTT
3. **多人併發 tok/s** — 影響團隊共用、批次處理。5090 + vLLM 575 tok/s 已經到 GPT-4o-mini API 級別吞吐 — 一台桌機服務一個小團隊
4. **NT$/1M tokens** — 影響大規模用量的 ROI。5090 攤提下來 ~NT$10，**比 Sonnet 4.6 API 便宜 27 倍**，跟 GPT-4o-mini 同價位但能力高一級

> NT$/1M tokens 計算基準：API 用官方定價、輸入輸出 1:1 估算；本地用 NT$30 萬桌機攤提 5 年 + 電費 + 30% 利用率

**5090 + Qwen3.6-27B 是「四個維度都進前段班」的方案。** 不是極致最快、不是極致最便宜，但四個維度沒有任何一項是短板。這就是「性價比騰飛」的本質：**不是某一個維度暴衝，是全部維度同時翻過了能用的門檻**。

過去本地 LLM 在「模型能力」這個維度就被卡死了，剩下三個再好都沒意義 — 模型笨用戶不會用。現在能力到位，剩下三個維度才開始有討論價值。

---

## 第一段｜為什麼說 2026 是「小模型性價比騰飛」的元年

把過去 18 個月的關鍵節點排一下：

| 時間 | 事件 | 對「本地 LLM」的意義 |
|---|---|---|
| 2024 Q4 | 70B 模型才能 production，要 2x A100 | 一台機器破百萬，ROI 算不回來，企業不碰 |
| 2025 Q2 | Qwen 3.5-27B 出來，tool calling 可用 | 第一次 27B 達 production 門檻 |
| 2025 Q4 | 量化技術成熟：AWQ INT4、FP8 KV cache、MTP | 27B 模型壓進 16GB VRAM |
| 2026 Q1 | Blackwell（5090）零售上市 | 32GB GDDR7、SM 120，整機 NT$30 萬 |
| **2026 Q2（現在）** | **Qwen 3.6-27B + 5090 + 進化過的引擎** | **Sonnet 4.6 等級能力裝進 NT$30 萬以下桌機** |

三件事在同一個時間點交叉：

1. **模型側**：27B dense 模型品質追上 Sonnet 4.6（在 SWE-bench、Terminal-Bench 等場景）
2. **硬體側**：消費級 5090 把 32GB VRAM 帶到桌面，整機 NT$30 萬剛好卡進企業桌機預算天花板 — 過去同等級能力要 H100，光一張卡 NT$100 萬，整整貴三倍
3. **軟體側**：推論引擎這半年集體大改 — vLLM 0.20 的 cudagraph、llama.cpp 收 MTP PR、AWQ 真正純 4-bit 量化普及

**這三件事任何一件沒到位，本地 27B 都還是 demo 級。三件同時到位才算「性價比騰飛」。**

性價比的本質是「能力 ÷ 預算」。**過去能力線上不去，現在能力上來了、預算也下來了，但天花板換成了「會不會調」** — 一張同樣的卡，配對的引擎跟參數能讓 token speed 差 9 倍。所以接下來這段最想講的，不是「性價比有多好」 — 而是**選錯配置會差到讓你以為這條路走不通**。

---

## 第二段｜七種配置實測，包含一個直接失敗的

機器規格先放著：

- GPU: NVIDIA RTX 5090（Blackwell, SM 120, 32GB GDDR7）
- Driver: 595.58.03（最高支援 CUDA 13.2，但編譯**必須用 12.9** — Unsloth 警告 13.2 會輸出亂碼）
- Host: Ubuntu 24.04 原生（不是 WSL）
- RAM: 64GB

測試 prompt 用同一段 63 token 的提示寫關於計算機歷史的 essay，`temperature=0` 跑單流，`temperature=0.7` 跑並發。

### Config 1：vLLM + GPTQ-Int4（直接 OOM 失敗）

我一開始抓的是 `raydelossantos/Qwen3.6-27B-GPTQ-Int4`，名字寫 "Int4"，磁碟大小 29 GB。

啟動就死：
```
ValueError: No available memory for the cache blocks
```

模型載入吃了 **27.51 GiB**（純 Int4 27B 應該只要 ~13.5 GiB），KV cache 只剩 0.18 GiB 直接掛掉。

去翻 `config.json` 才發現名實不符：

```json
"quantization_config": {
  "bits": 4,
  "dynamic": {
    "-:.*attn.*": {},          // attention 不量化
    "-:.*mtp.*": {},           // MTP 層不量化
    "-:.*shared_expert.*": {}, // shared expert 不量化
    "-:.*visual.*": {},        // visual encoder 不量化
    "lm_head": {}
  }
}
```

**只有 MoE expert 部分是 Int4，attention、visual、MTP head 全部是 BF16。** 名字叫 "Int4" 但本質是「部分量化」。32GB VRAM 在 5090 上根本不夠塞。

**Reality check：模型卡上寫「Int4」「INT4」「W4A16」千萬不要照單全收。** 看 `config.json` 裡的 `dynamic` 例外清單，或對比磁碟容量 — 純 4-bit 27B 模型應該 ~14 GB，不該 29 GB。

### Config 2：vLLM + NVFP4-BF16 + enforce-eager（救命但慢）

換 `rdtand/...NVFP4-BF16-vllm`（19 GB），這次能跑了，但要加 `--enforce-eager` 才能塞進 32GB：

```bash
~/vllm-qwen-env/bin/vllm serve rdtand/Qwen3.6-27B-PrismaSCOUT-Blackwell-NVFP4-BF16-vllm \
  --gpu-memory-utilization 0.92 \
  --max-model-len 8192 \
  --enforce-eager \
  --served-model-name qwen-nvfp4
```

`--enforce-eager` 是救命 flag — 它跳過 cudagraph capture 階段（會吃 12GB+ VRAM）。**但代價是砍掉 30-50% decode 速度。**

實測：
- 單流：**20.5 tok/s**（比 Ollama 還慢！）
- 並發 16：304 tok/s

學到的事：**32GB VRAM 跑 27B 模型，模型本體必須壓到 ~16 GiB 以下**，才有空間給 cudagraph 跑全速。19 GB 已經太大。

### Config 3：vLLM + AWQ-INT4 + cudagraph（並發冠軍）⭐

換 `cyankiwi/Qwen3.6-27B-AWQ-INT4`（20 GB on disk，**真正的純 4-bit AWQ**）。然後做兩件事讓 cudagraph 跑起來：

```bash
~/vllm-qwen-env/bin/vllm serve cyankiwi/Qwen3.6-27B-AWQ-INT4 \
  --gpu-memory-utilization 0.92 \
  --max-model-len 4096 \
  --max-num-seqs 8 \          # ← 關鍵
  --kv-cache-dtype fp8 \      # ← 關鍵
  --served-model-name qwen-awq
```

- `--max-num-seqs 8`：vLLM 預設要 capture 51 個 cudagraph size，會 OOM。砍到 8 之後只 capture `[1,2,4,8,16]` 五個
- `--kv-cache-dtype fp8`：KV cache 從 fp16 壓成 fp8，省一半記憶體

實測：
- 單流：**80.5 tok/s**（比 enforce-eager 快 4x）
- 並發 4：263 tok/s
- 並發 8：**575 tok/s** 🏆
- 並發 16：574（被 max-num-seqs 上限卡住）

**575 tok/s 是什麼概念？** 比 Ollama 同條件快 9x，比 GPT-4o-mini 的 API 吞吐還高（用同一張卡服務 8 個並發用戶）。

### Config 5：llama.cpp + MTP（單流冠軍）⭐

切換引擎到 llama.cpp，跑 `unsloth/Qwen3.6-27B-MTP-GGUF` 的 Q2_K_XL（**只有 12 GB**）。

MTP 是 Multi-Token Prediction — 模型內建一個 draft head 預測接下來 2 個 token，target model 驗證。接受率 70%+ 等於免費加速。

Build 過程要小心 CUDA 雷區：

```bash
# 必須用 CUDA 12.9 toolkit，不是 13.2（會輸出亂碼）
export PATH=/usr/local/cuda-12.9/bin:$PATH
export CUDACXX=/usr/local/cuda-12.9/bin/nvcc

# Blackwell SM 120 要明確指定
cmake -B build -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=120 \
  -DCMAKE_BUILD_TYPE=Release -G Ninja

# 需要 PR 22673（MTP 支援還沒進 main）
git fetch origin pull/22673/head:mtp && git checkout mtp
```

啟動：
```bash
llama-server -m Qwen3.6-27B-UD-Q2_K_XL.gguf \
  -ngl 99 --ctx-size 4096 \
  --spec-type draft-mtp \
  --spec-draft-n-max 2          # MTP draft 2 個 token
```

實測：
- 單流：**140 tok/s** 🏆（全場最快）
- 並發 8：**118 tok/s**（反而退化！）

**MTP 跟 batching 互斥** — draft model 和 target model 共享 KV cache，並發時雙方都要搶記憶體 → batching 失效。

所以 MTP 是「**單人神器、多人毒藥**」。自己用爽歪歪、開 API 給隊友就完蛋。

### Config 6 + 7：Ollama vs llama.cpp（同一個 GGUF，效能差 3.2x）

這是最反直覺的一段。

**Ollama**（開箱即用，`ollama pull qwen3.6:27b`，內部就是 Q4_K_M GGUF）：
- 單流：67 tok/s
- 並發 4：64 tok/s
- 並發 8：64 tok/s
- **並發完全不擴展**，等於序列化

我懷疑是 Ollama wrapper 的問題，所以拿同樣的 Q4_K_M GGUF 用 llama.cpp 直接跑（Config 7）：
- 單流：75 tok/s（+12%）
- 並發 4：**204 tok/s**（+219%）
- 並發 8：189 tok/s

**同一個 GGUF、同一張卡，llama.cpp 比 Ollama 並發吞吐快 3.2x。**

我不知道 Ollama 內部做了什麼把 batching 給關了 — 它預設有 `OLLAMA_NUM_PARALLEL=4`，但實測表現完全不像有 batching。如果你現在用 Ollama 做生產 API，這 3.2x 的效能就是你白白送掉的。

> 小插曲：想用 Ollama 已經下載好的 GGUF 餵給 llama.cpp 不行，會報 `qwen35.rope.dimension_sections has wrong array length`。Ollama 的 GGUF metadata 跟 llama.cpp PR 22673 不相容，要從 unsloth HF 重下載一份。

---

## 第三段｜總成績單

| Config | 引擎 | 量化 | 模型大小 | GPU 用量 | 單流 | 並發 4 | 並發 8 |
|---|---|---|---|---|---|---|---|
| 1 | vLLM | "GPTQ-Int4"（假）| 29 GB | ❌ OOM | - | - | - |
| 2 | vLLM | NVFP4 + eager | 19 GB | 30.2 GB | 20.5 | 74 | 127 |
| **3** | **vLLM** | **AWQ-INT4 + cudagraph** | 20 GB | 28.3 GB | 80.5 | 263 | **575** 🏆 |
| 4 | vLLM | AWQ-INT4 單人版 | 20 GB | 28.9 GB | 80.7 | - | - |
| **5** | **llama.cpp** | **Q2_K_XL + MTP** | 12 GB | 14.5 GB | **140** 🏆 | 118 | 118 |
| 6 | Ollama | Q4_K_M | 17 GB | 24.6 GB | 67 | 64 | 64 |
| **7** | **llama.cpp** | **Q4_K_M（無 MTP）** | 16 GB | 17.6 GB | 75 | 204 | 189 |

三個冠軍的用途分流：

| 場景 | 推薦 Config | 為什麼 |
|---|---|---|
| 自己一個人本地對話、寫 code 副駕 | **Config 5（llama.cpp + MTP）** | 140 tok/s、省顯存 14.5 GB，VRAM 剩一半可以同時開 IDE |
| 開 API 給團隊/客戶用 | **Config 3（vLLM AWQ）** | 575 tok/s 是其他配置的 5-9x，並發是 production 的本質 |
| 自用 + 偶爾 2-3 人連 | **Config 7（llama.cpp Q4 無 MTP）** | 單流 75 + 並發 204 平衡，build 也不需要 PR 22673 |
| 不想 build、開箱即用 | Config 6（Ollama）| 一行 `ollama pull` 就好，但接受效能只剩 1/3-1/9 |

---

## 第四段｜五個不會寫在 README 的觀察

### 1. 量化命名不可信，看 config 跟磁碟大小

純 4-bit 量化的 27B 模型應該 ~14 GB。看到 29 GB 還叫 "Int4" 的，多半是 attention/visual 沒量化。檢驗方法：

```bash
# 純 4-bit GGUF 大小參考
ls -lh *.gguf
# Q2_K_XL: ~12 GB（極致壓縮）
# Q4_K_M:  ~16 GB（生產標配）
# Q6_K:    ~22 GB（高品質）
```

看到 GPTQ/AWQ 模型也是一樣 — 直接看 `config.json` 的 `quantization_config.dynamic` 例外清單，或 `du -sh` 整個目錄。

### 2. vLLM 的 cudagraph 是核心優化，不是 nice-to-have

`--enforce-eager` 砍掉 cudagraph + torch.compile 之後，速度從 80 跌到 20.5（**-75%**）。但在 32GB VRAM 跑 27B 模型，**模型本體必須 < 16 GiB** 才有空間給 cudagraph capture。

換言之：選量化版本不要看「能不能載入」，要看「載入後還剩多少給 cudagraph」。

### 3. cudagraph capture 預設 51 個 size 會 OOM

vLLM 預設 `cudagraph_capture_sizes = [1, 2, 4, 8, 16, 24, 32, ..., 512]`，51 個 capture 每個吃幾百 MB，在 32GB 卡上必爆。

解法是 `--max-num-seqs 8`，把 capture 砍到 `[1, 2, 4, 8, 16]` 五個。如果你只有單流需求，可以更激進 `--max-num-seqs 1`，只 capture `[1, 2]`。

### 4. MTP 跟 batching 互斥 — 是「個人神器」不是「服務利器」

Q2 + MTP 單流 140，並發 8 退化到 118。Q4 無 MTP 單流 75，並發 8 衝到 189。

原因：draft model + target model 共享 KV cache，並發時雙方都要記憶體 → 互相搶 → batching 退化。

**做個人助理用 MTP，開 API 給人用就不要碰 MTP。**

### 5. CUDA 13.2 + Blackwell 是雷區

Driver 寫支援 CUDA 13.2，但實測會輸出亂碼（Unsloth 官方有警告）。解法：driver 留著、編譯 toolkit 用 12.9。`nvidia-smi` 顯示的 CUDA 版本只是 driver 最高支援，不代表你必須用那個 toolkit。

---

## 第五段｜這對 IT 架構意味著什麼

我不是說「全部 workload 都該轉本地」。Claude/GPT 的 API 該用就用，特別是 Opus 級別的長思考任務、複雜 agentic 工作流，雲端旗艦模型還是大幅領先。

但有幾類 workload 現在 ROI 真的翻過來了：

| Workload | 雲端 API | 本地 5090 + Qwen3.6-27B |
|---|---|---|
| 員工問答 / 內部知識庫 RAG | 隱私風險 + 重複 token 燒錢 | 全在內網，固定成本 |
| 程式碼補全（IDE inline）| 等待 200-400ms 才開始吐字 | 本機 TTFB < 50ms |
| 大量批次處理（log 分析、文件摘要）| 跑 1 萬筆要等好幾天排隊 | 並發 8 跑 575 tok/s，一個下午跑完 |
| Tool calling 為主的 agent | 每個 tool round 都付 token | 一張卡多人共用 |

**這幾類 workload 的共通點：**
- 任務不需要旗艦模型（27B 夠用）
- 量大、重複、token 燒得快
- 對隱私敏感，或對延遲敏感

**過去半年我給客戶的建議是「先用雲端 API 把流程跑出來，等開源追上再考慮本地」。從這次實測之後，我會改說：**

> 「先用雲端 API 證明流程有 ROI，然後抓你最燒錢、最不能漏的那 20% workload，現在就可以開始評估本地化。**一台 NT$30 萬的 5090 桌機，就是這 20% workload 的最佳 ROI 起點。**」

不是要全面取代雲端，是 **workload 分流的時機到了**。

### 回到開頭那個問題

> **「Qwen 3.6-27B 接近 Sonnet 4.6，那能不能在 NT$30 萬以下桌機跑起來？」**

答案是：**能，整套 NT$30 萬剛好卡進企業桌機/工作站採購天花板，不用走資產採購、不用董事會審核。**

但前提是你要：
- 選對引擎（vLLM 並發、llama.cpp 單人，不要 Ollama 進 production）
- 選對量化（AWQ-INT4 或 Q4_K_M，不要被「Int4」字面騙）
- 跳過三個坑（cudagraph capture、MTP vs batching、CUDA 12.9 而非 13.2）

把這幾件事做對，你的 NT$30 萬桌機就是一台「Sonnet 4.6 等級、575 tok/s 並發、零雲端依賴」的 AI 服務器。這不是 demo、不是玩具，是 production-ready 的本地推論。

---

## 常見問題 Q&A

**Q: 為什麼不直接買 H100 / B200？**

5090 整機 NT$30 萬，H100 一張卡 NT$100 萬起跳，B200 更貴。如果你的 workload 是「能在 32GB 內塞下的模型，並發 8 以下」，5090 的 NT$/token 比 H100 划算 10 倍以上。H100 適合 70B+ 模型或要做 KV cache 共享的大規模服務，27B 用 H100 是殺雞用牛刀。

**Q: 為什麼不等 Qwen 3.7、5090 改款？**

可以等，但機會成本是「現在用不到本地推論的 6 個月」。我這次實測的目的就是回答「現在這個時間點，到底夠不夠用」 — 答案是夠了。等下一代是無止盡的循環，每代都會有人說「再等等」。

**Q: Mac Studio M3 Ultra 不是也能跑 27B？**

可以，但 token speed 大概是 5090 的 1/3 左右（M3 Ultra 約 40-50 tok/s，5090 cudagraph 配置 80+ tok/s）。Mac 的優勢是統一記憶體可以塞 70B+ 模型，5090 的優勢是純算力快、價格低。**選 Mac 還是 5090，看你要跑多大的模型**。

**Q: 為什麼 Ollama 並發那麼差，社群還這麼推？**

Ollama 的優勢是「開箱即用」 — 不會 build、不熟 CUDA、不知道 `--max-num-seqs` 怎麼調的人，五分鐘就有一個能用的 LLM API。對「我只是想試試看本地 LLM」的人來說，這個體驗值很多。但要進 production，請直接用 llama.cpp 或 vLLM。

**Q: Qwen3.6-27B 比 Sonnet 4.6 還強？**

不是，是「某些 benchmark 上接近 Sonnet 4.6 等級」。實際使用品質 Sonnet 4.6 還是更穩、更會處理長 context、更會 reasoning。但對於「員工問 HR 政策、log 分類、code lint、簡單摘要」這類任務，27B 已經足夠 — 而且不會把客戶資料送出公司。

**Q: 要不要等 vLLM 出 FP4 kernel？**

值得期待，但不用為這個延遲決策。AWQ-INT4 + FP8 KV cache 在 5090 上已經跑得很好。FP4 出來估計再快 30-50%，但不會改變「現在能不能做」的答案。

---

## 完整 reproducibility

所有實測命令、啟動參數、踩坑紀錄都在我的內部報告：模型版本、cudagraph capture sizes、KV cache dtype、CUDA toolkit 版本，全部列清楚了。如果你也在規劃 5090 / 4090 / RTX PRO 系列跑本地 LLM，這份報告省你的時間絕對超過你的時薪。

**最後總結一句**：

> 「2026 是本地小模型性價比騰飛的元年。但同一張卡能跑出 64 tok/s 也能跑出 575 tok/s — 差別不是硬體，是你選不選得對。」

---

**延伸閱讀：**
- [Qwen 3.6-27B 本地部署：DGX Spark / Mac mini 跑出 Sonnet 4.6 等級 AI Agent](/qwen-3-6-27b-gb10-home-inference-sonnet-level/)
- [企業級地端 LLM 系統架構藍圖](/local-llm-enterprise-architecture/)
- [Tool Calling 1.5 - 本地 LLM Tool Calling 與 27B Sweet Spot](/toolcall-15-local-llm-tool-calling-qwen-27b-sweet-spot/)
