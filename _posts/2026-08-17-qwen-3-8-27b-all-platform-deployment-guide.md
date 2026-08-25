---
layout: post
title: "Qwen3.8-27B 實測：RTX 3090／4090／5090／PRO 6000／DGX Spark／Mac tok/s 整理"
date: 2026-08-17 09:00:00 +0800
permalink: /qwen-3-8-27b-all-platform-deployment-guide/
description: "Qwen3.8-27B 社群實測 tok/s 整理：RTX 3090 25–57、RTX 4090 45–97、RTX 5090 74–153、PRO 6000 高併發 1,171、DGX Spark 調校後 75、Mac MTP 解鎖後 56。六種硬體、300+ 條 X 貼文，附啟動參數與來源連結。"
image: /assets/images/qwen-3-8-27b-deployment-guide-cover.png
categories: [AI 技術實作]
tags: [Qwen3.8-27B, RTX 3090, RTX 4090, RTX 5090, RTX PRO 6000, DGX Spark, Apple Silicon, llama.cpp, SGLang, vLLM, MTP, NVFP4, 本地部署, benchmark, tok/s]
author: Wisely Chen
---

# Qwen3.8-27B 實測：RTX 3090／4090／5090／PRO 6000／DGX Spark／Mac tok/s 整理

這兩天我的 X timeline 被 Qwen3.8-27B 洗版。每個人都在曬自己的 tok/s，問題是——同一個模型，數字從 6 到 400 都有人喊。

我決定做一個想想就很吃力不討好的事情：用我跟 AI 一起把 300+ 條 X 貼文一條一條拆開，對照硬體、量化、context、引擎版本、MTP 設定，整理成六條部署路線。再加上本站 RTX 5090 用 SGLang、vLLM、llama.cpp 三套引擎跑的實測數字。

只有一句話，太可怕的社群力量了。

先看總表，再往下挑你的硬體。

---

## Qwen3.8-27B 總表：六種硬體 tok/s 對比

| 硬體 | VRAM／RAM | 建議量化 | Context 起點 | 建議 Runtime | 單人 Decode（tok/s） |
|---|---:|---|---:|---|---|
| RTX 3090 24GB | 24GB | Q4 | 32K | llama.cpp + MTP | 25–57；最佳化 stack 宣稱 82 |
| RTX 4090 24GB | 24GB | Q4 | 32K | llama.cpp + MTP | 45–97 |
| RTX 5090 32GB | 32GB | Q4／NVFP4 | 32K–128K | llama.cpp 單人；SGLang／vLLM 多人 | 單人 74–153；本站四人每人 106 |
| RTX PRO 6000 | 96GB | BF16／NVFP4／FP8 | 64K–256K | vLLM／SGLang | BF16 約 23；NVFP4 45–223，條件差異大 |
| DGX Spark | 128GB 統一 | NVFP4／Q4 | 32K | SGLang | baseline 8–13；調校 22–75；DSpark coding 51.5 |
| Mac 24–36GB | 24–36GB | Q4 | 8K–16K | MLX／llama.cpp | 6–18 |
| Mac 64–128GB | 64–128GB | Q6／8-bit | 32K | MLX／llama.cpp | 10–27；MTP 解鎖後 47–56；MTPLX V2.9 最高 175 |

**看數字之前，先讀這三點：**

1. 除了 RTX 5090 以外，我沒有其他硬體。其餘五條路線的數字全部來自 X 社群網友自行回報，我整理並附上原始貼文連結。
2. 即使是我自己實測的 5090 數字（附有完整啟動參數），我也不認為可以 100% 重現。Linux 版本、GPU driver 版本、C library 版本、SGLang／vLLM 版本不同，結果都可能不同。
3. 所有數字都是參考區間，不是保證值。

一句購買建議：

1. 預算敏感，找二手 RTX 3090 24GB。
2. 想要最成熟的單卡體驗，RTX 4090 24GB。
3. 要 100 tok/s 級互動與長 context 餘裕，RTX 5090 32GB。
4. 要長 context、多人 serving 與 96GB VRAM，才看 RTX PRO 6000。
5. 已經有 Mac 或 DGX Spark，就用現有機器。不要只因統一記憶體很大就購買。

---

## Qwen3.8-27B 部署前必知：模型權重、KV cache、記憶體頻寬

最常見的錯誤是只看模型檔案大小。

Q4 GGUF 約 17–18GB，很多人看到 24GB 顯卡就推論「還剩 6GB，262K 沒問題」。但執行時還要放 KV cache、運算 buffer、MTP draft state，若啟用多模態還有 projector，作業系統和桌面也吃 VRAM。

| 精度 | 約略大小 | 適合硬體 |
|---|---:|---|
| BF16 | 51.76 GiB | 64GB 級以上 |
| FP8 | 28.76 GiB | 48GB 較舒服；32GB 很緊 |
| Q6 | 約 23GB | 32GB GPU 或大統一記憶體 |
| Q4 | 約 17–18GB | 24GB GPU 的主力 |
| IQ3／低位元 MLX | 約 11–15GB | 16–24GB Mac 實驗用 |

### GGUF 量化品質不只看位元數——AtomicChat AD layout

同樣叫 Q4，不同來源的 GGUF 品質差異很大。[AtomicChat 用 KL divergence vs BF16 做了一張完整比較圖](https://x.com/atomic_chat_hq)，把自家 AD（Atomic Dynamic）layout 跟 unsloth、lmstudio-community、ggml-org 的 GGUF 逐一對比（reference = BF16、4x RTX 5090、4096 context）。結論：**同樣檔案大小，AD layout 的 KL divergence 一致低於其他社群 GGUF。**

按記憶體級距的建議量化：

| 可用記憶體 | 建議量化 | 檔案大小 | Top-1 準確率 | Mean KL Divergence |
|---:|---|---:|---:|---:|
| 12GB | AD-IQ2_XS | 9.9GB | 83.5% | 0.1617 |
| 16GB | AD-IQ3_S | 13.8GB | 92.4% | 0.0325 |
| 24GB | AD-Q5_K | 20.2GB | 97.3% | 0.0042 |
| 32GB | AD-Q6_K | 25.0GB | 98.7% | 0.0011 |
| 48GB | Q8_0 | 28.9GB | 98.9% | 0.0006 |

幾個值得注意的點：

- **24GB 級距（RTX 3090／4090）不一定要卡在 Q4。** AD-Q5_K 只有 20.2GB，塞得進 24GB VRAM，KL divergence 從 Q4 級的 ~0.01 降到 0.0042，Top-1 從 ~95% 升到 97.3%。代價是 KV cache 空間更少、context 天花板更低。
- **16GB → 24GB 是品質斷崖。** KL divergence 從 0.0325 降到 0.0042，差 8 倍。12GB 的 0.1617 已經是另一個世界。
- **32GB 的 AD-Q6_K（98.7%）和 48GB 的 Q8_0（98.9%）差距只有 0.2%。** 32GB 卡不需要追到 Q8。

這張圖不能直接等於 agent task 品質——KL divergence 是 token distribution 層級的度量，不是 tool calling 成功率。但它是目前最系統性的 GGUF 量化品質比較。選 GGUF 來源時，不要只看位元數，要看誰做的。

KV cache 決定 context 能開多長。Qwen3.8-27B 的 hybrid architecture（64 層裡只有 16 層 full attention，其餘 48 層 Gated DeltaNet）比純 Transformer 省，但 262K 仍然不是免費的。本站 RTX 5090 32GB 實測：Q4 權重 + Q8 KV，約 67K token 就 OOM；改成 Q4 KV，才完成約 237K token 輸入。

記憶體頻寬決定吐字速度。Dense 27B 每生成一個 token 要把大部分權重讀一遍——未調校的 DGX Spark baseline 約 8–13 tok/s，而 RTX 4090 Q4 + MTP 可以到 86.5。容量解決 fit，頻寬才決定 decode。

**Fit ≠ Speed。這是整篇最重要的一行。**

---

## RTX 3090 24GB：可用

Q4 + llama.cpp + MTP，25–57 tok/s，最佳化 stack 宣稱 82。二手市場最便宜的實用起點。

社群實測：

- [未接 MTP 約 25 tok/s，90K context 深度仍約 26 tok/s](https://x.com/sudoingX/status/2088327367500714279)——但原 po 自己發現 llama.cpp 忽略了 MTP tensors
- [vLLM W4A16 + MTP 最佳化 stack 宣稱單請求約 82 tok/s，64 concurrent 峰值 672 TPS](https://x.com/MGHenrichsen/status/2088924568450662429)（repo README 目前數字較保守，約 40 tps 單流、416 tps 64 併發）
- [198K context、處理約 141,236 tokens、39 分鐘完成](https://x.com/elketepe/status/2088925907356439024)
- [全 GPU 執行約 57 tok/s，經 Hermes Agent 跑 coding 任務後端到端 31–52 tok/s](https://x.com/IbrahimSait_/status/2089015226809094476)

有趣的一條：一位使用者的 3090 eGPU（OCuLink 外接）被靜默限制在 210W，[解除到 300W 後無 MTP 從 19.7 升到 36.1 tok/s、MTP n=2 約 48.9–49.8 tok/s](https://x.com/Samsara4567B4/status/2088980390325187055)。llama-bench 進入 131K 深度後 decode 約減半。

8/18 更新：[sudoingX 的 MTP A/B benchmark repo](https://github.com/sudoingX/qwen38-mtp) 收集了 20+ 張卡的標準化對照數字。3090 baseline 31.0 → MTP 41.3 tok/s（n-max 2）；3090 Ti 在 128K context 下[拿到 70 tok/s](https://x.com/0xArchitect)；turboquant n-max 6 配置在 3090 上推到 61.5 tok/s。

**llama.cpp commit、MTP、功耗限制和 agent harness 已經跟硬體型號同樣重要。**

---

## RTX 4090 24GB：單人順暢

Q4 + llama.cpp + MTP，45–97 tok/s。單人 coding agent、tool calling、RAG 或低併發 API，4090 是速度與軟體成熟度最平衡的配置。[24GB VRAM + 4-bit 是比較實際的單卡條件](https://x.com/ram4_dev/status/2088380537693941817)。

一組[完整參數實測](https://x.com/outsource_/status/2088743407543812436)用 `UD-Q4_K_XL`、全層 GPU offload、Flash Attention、MTP：[未開 speculative decoding 約 44.9 tok/s；開 MTP 後 32K context 一般工作負載約 86.5 tok/s，coding 峰值約 97.3 tok/s（8K context、draft KV 改 q8_0）](https://x.com/outsource_/status/2088743329760469374)。

4090 起手式：

```bash
llama-server \
  -m Qwen3.8-27B-UD-Q4_K_XL.gguf \
  -ngl 999 \
  -c 32768 \
  -fa on \
  -np 1 \
  --cache-type-k f16 \
  --cache-type-v f16 \
  --spec-type draft-mtp \
  --spec-draft-n-max 4 \
  --host 127.0.0.1 \
  --port 8000
```

這不是最佳參數，是容易驗證的 baseline。先關 MTP 記錄 decode、TTFT 與 VRAM，再用 draft 2、4 跑同一組 prompt；32K 穩定後才升 64K，VRAM 不足時先量化 KV cache。

8/18 更新：[@ryan4yin 分享了一組 130K context 的完整配置](https://gist.github.com/ryan4yin/19db9fa44972c5735c1d181e8888d4fe)——同樣 `UD-Q4_K_XL`，KV cache 改用 `kvarn6`（品質優於標準量化）、最後 2,048 tokens 保留 F16 防止 attention drift、MTP n-max 3、Flash Attention on。日常 decode 約 60–70 tok/s，126.6K input context 仍有 50–62 tok/s。關鍵陷阱：主線 llama.cpp 對非 Q4 KV cache 會靜默 fallback 到 CPU，他用的是 BeeLlama fork；150K 在多輪對話會 OOM，實際天花板約 130K。

---

## RTX 5090 32GB：可以四人

Q4 或 NVFP4，單人 74–153 tok/s，本站四人每人 106 tok/s。多出的 8GB 最實用的價值不是更高精度，是 context headroom。

### 社群數字

| Stack | Context／條件 | Decode |
|---|---|---:|
| [llama.cpp Q4 baseline](https://x.com/TechPractice1/status/2088398765480620520) | context 未揭露 | 約 74 tok/s |
| [llama.cpp Q4 + MTP](https://x.com/TechPractice1/status/2088398765480620520) | context 未揭露 | 約 113 tok/s |
| [Docker llama.cpp + Q4 KV + MTP](https://x.com/johnny_ver_2/status/2088836684771180904) | 131K | 約 102 tok/s |
| [vLLM + NVFP4 + MTP](https://x.com/MiaAI_lab/status/2088919884730106138) | 256K、單 session（structural 數字，非實跑） | 約 147 tok/s |
| [SGLang + NVFP4 + MTP](https://x.com/calneymgp/status/2088822975550071292) | Triton attention、lm_head NVFP4 | 約 153 tok/s |
| [llama.cpp Q4 baseline → MTP n-max 4](https://github.com/sudoingX/qwen38-mtp) | desktop，sudoingX A/B repo | 61.4 → 135 |
| [llama.cpp UD-Q5_K_XL + MTP n-max 4](https://github.com/sudoingX/qwen38-mtp) | desktop | 66.3 → 144.2 |
| [llama.cpp Q6_K + MTP](https://github.com/sudoingX/qwen38-mtp) | 128K context | 61.9 → 130 |
| [llama.cpp Q6_K + MTP](https://github.com/sudoingX/qwen38-mtp) | 256K context | 62.0 → 121.7 |
| [SGLang NVFP4 + DSpark](https://x.com/smugseahorse) | runpod 5090、single slot | 約 140 tok/s |

[同一則貼文下的回覆也提醒，147 tok/s 會隨 workload 與設定變動，應在自己的硬體上重測](https://x.com/KostyaOnchain/status/2088929890678575368)。

### 本站實測

我在同一張 32GB 5090 上跑了三套引擎。llama.cpp 偏單人長 context、SGLang 和 vLLM 偏多人 serving。完整過程在[這集 YouTube 逐字稿](https://ai-coding.wiselychen.com/youtube-qwen38-27b-rtx5090-sglang-vllm-mtp-transcript/)。

**llama.cpp Q4 + MTP（單人互動）：**

| Context | Decode |
|---|---:|
| 7K–28K 日常 | 100–126 tok/s |
| 約 237K 長文 | 49–55 tok/s |

context 從日常區間進到 200K 後速度直接掉一半。**長 context 是一種 workload，不是一個 checkbox。**

128K 以上啟動參數：

```bash
llama-server \
  -m Qwen3.8-27B-UD-Q4_K_XL.gguf \
  -ngl 999 \
  --ctx-size 131072 \
  --flash-attn on \
  --cache-type-k q4_0 \
  --cache-type-v q4_0 \
  --spec-type draft-mtp \
  --spec-draft-p-min 0.75 \
  --spec-draft-n-max 2 \
  --parallel 1 \
  --host 127.0.0.1 \
  --port 8000
```

**SGLang／vLLM + NVFP4（多人 serving）：**

同一張 5090 換成 `RadixArk/Qwen3.8-27B-NVFP4`，用 SGLang（FlashInfer、NEXTN／MTP 2 draft tokens、`--disable-radix-cache`）和 vLLM 0.27.1（FlashInfer、FP8 KV、32K context、`num_speculative_tokens: 2`）各跑一輪。

| 配置 | 單人 tok/s | 四人總吞吐 tok/s | 每人 tok/s | MTP 接受率 |
|---|---:|---:|---:|---:|
| SGLang MTP-2 | 113.75 | 425.44（19.3 秒） | 106–108 | 78–91% |
| SGLang MTP-2、八人 | — | 303.4（約 54 秒） | 實際 3–4 人在跑，其餘排隊 | 74–94% |
| vLLM 無 MTP | 57.83 | 210.37 | 52–53 | — |
| vLLM MTP-1 | 85.63 | 305.09 | 76–80 | — |
| vLLM MTP-2 | 100.33 | 351.71 | 88–94 | 平均約 69% |

三個結論：

1. **四人是這張卡的甜蜜點。** 四人並行每人仍有 106–108 tok/s，跟單人差不到 7%；八人時 KV pool 只剩約 7,703 tokens（四人約 64,079），長輸出時實際只有 3–4 個請求在生成，其餘排隊。**32GB 的天花板不是權重，是 KV pool。**
2. **MTP 在 serving engine 上一樣是免費午餐。** vLLM 無 MTP 到 MTP-2，單人快 73.5%、四人快 67.2%。
3. **SGLang 目前比 vLLM 快 12–17%。** 差距來自 Verified 配置、CUDA Graph 與排程較成熟。vLLM 0.20.2 會撞到 `lm_head.input_scale` 錯誤，要升到 0.27.1。

兩個誠實的註腳：SGLang 四人測試每人輸出 2,048 tokens，vLLM A/B/C 是 512 tokens，tok/s 只能看趨勢；SGLang 為了把 Mamba state 塞進 32GB 用了 `--disable-radix-cache`，代價是沒有共享前綴快取。

SGLang 四人啟動參數：

```bash
sglang serve \
  --trust-remote-code \
  --model-path RadixArk/Qwen3.8-27B-NVFP4 \
  --mem-fraction-static 0.98 \
  --attention-backend flashinfer \
  --chunked-prefill-size 2048 \
  --reasoning-parser qwen3 \
  --tool-call-parser qwen3_coder \
  --mamba-full-memory-ratio 4.59 \
  --max-running-requests 4 \
  --speculative-algorithm NEXTN \
  --speculative-num-steps 1 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 2 \
  --cuda-graph-max-bs-decode 4 \
  --disable-radix-cache \
  --host 0.0.0.0 \
  --port 30000
```

vLLM MTP-2：

```bash
vllm serve RadixArk/Qwen3.8-27B-NVFP4 \
  --trust-remote-code \
  --served-model-name Qwen3.8-27B \
  --gpu-memory-utilization 0.95 \
  --max-model-len 32768 \
  --max-num-seqs 4 \
  --max-num-batched-tokens 8192 \
  --attention-backend FLASHINFER \
  --reasoning-parser qwen3 \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_coder \
  --speculative-config '{"method":"mtp","num_speculative_tokens":2}' \
  --host 0.0.0.0 \
  --port 30000
```

同一張 5090 其實是兩種產品：`llama.cpp + GGUF Q4 + MTP` 是單人長 context 互動機（237K 塞得進去，49–55 tok/s）；`SGLang／vLLM + NVFP4 + MTP-2` 是四人小團隊 model server（每人 106 tok/s，但 context 被 KV pool 綁在幾萬 tokens）。選哪種，取決於這台機器服務一個人還是四個人。

### 2x RTX 5090 TP=2：8 路每路仍有 141 tok/s

8/24 更新：[yage.ai 發布了一組 2x RTX 5090 + SGLang TP=2 + NVFP4 的完整測試](https://yage.ai/share/2x5090-27b-sweet-spot-20260824.html)，包含真實 24 小時 workload 分析。

| 併發數 | 總吞吐 tok/s | 每路 decode tok/s | 加速倍數 |
|---:|---:|---:|---:|
| 1 | 268 | 286 | 1.00x |
| 2 | 461 | 253 | 1.72x |
| 4 | 692 | 196 | 2.58x |
| 8 | 962 | 141 | 3.59x |

單流 268 tok/s 接近單卡的 2.4 倍；8 路併發總吞吐 962 tok/s，每路仍有 141 tok/s——單卡四人每人 106，雙卡八人每人 141，scaling 效率不錯。

更有意思的是真實 workload 分析（8/23 一整天）：224M prefill tokens 裡 182M 命中 prefix cache（幾乎不耗算力）；實際新生成 decode tokens 只有 2.25M；active generation 時間約 3.8 小時/天。硬體投資 US$6,000–8,000，持續 500W 功耗每月電費約 US$11。跟商業 API 比，自架每月省約 US$20 營運費，但硬體要 25–33 年回本。

結論：**雙卡 5090 是消費級 inference 的甜蜜點，但回本計算要看真實使用量而不是峰值 tok/s。**

---

## RTX PRO 6000 96GB：16 人以上，可以當公司 AI Coding Server

BF16／NVFP4／FP8，BF16 約 23 tok/s，NVFP4 45–223 tok/s，條件差異大。96GB VRAM 最獨特的能力：BF16 權重約 51.76 GiB，單張 PRO 6000 放得下，不需要量化。[FP8 實測單人約 23 tok/s（262K context、vLLM 0.27.1）](https://huggingface.co/Qwen/Qwen3.8-27B-FP8/discussions/9)，MTP-2 可推至約 62 tok/s。[SGLang 跑 FP16 decode 甚至比 vLLM FP8 + MTP 還快](https://x.com/OrganicGPT/status/2088704873973879065)，但原帖沒有給確切數字。

8/18 更新：[llama.cpp MTP A/B 測試 baseline 63.8 → MTP 91.5 tok/s](https://github.com/sudoingX/qwen38-mtp)（@commdata2338）；[3 slot concurrency 配置下 peaks 達 500 tg/s](https://x.com/smugseahorse)（@smugseahorse）。

高併發才是 PRO 6000 真正拉開差距的地方。[LLM 高併發測試：16 路每路約 30 tok/s、總計約 480；32 路總計約 720；64 路總計約 1,171 tok/s](https://x.com/Wbackdown/status/2089129248737124590)。這是消費卡做不到的——RTX 5090 四人已經是極限，PRO 6000 可以推到 64 路。

空間充裕，[NVFP4 + SGLang + DSpark、256K context、concurrency 8，單 stream 約 200–223 tok/s](https://x.com/MiaAI_lab/status/2088917237230932186)。但[full precision 實測裡 context 從 10K 增至 60K，速度約下降一半，TTFT 明顯升高](https://x.com/OrganicGPT/status/2088340860110811322)。容量、單流速度和長 context latency 仍然要分開驗收。

更重要的是 fast path 還在快速變動。一組 500 題 coding suite 測試中，[Inferact NVFP4 + vLLM nightly + MTP 得到 478/500、約 45 tok/s decode、5,200 tok/s prefill；同時測到 llama.cpp CUDA GGUF、vLLM FP8 + MTP 和部分 abliterated 權重有嚴重品質問題](https://x.com/sethprattsf/status/2089078472341852608)。單一使用者的早期結果不能直接當引擎定論，但足以提醒：**最快的路徑如果沒有跑品質 regression suite，就還不算可用。**

---

## DGX Spark：絕對可用，只是沒有用到統一記憶體全部優勢

NVFP4／Q4，baseline 8–13 tok/s，調校後 22–75 tok/s。DGX Spark 跑 Qwen3.8-27B 的早期 baseline：[llama.cpp + unsloth GGUF，prompt processing 約 837 tok/s、generation 約 11.6 tok/s](https://x.com/SaiyamPathak/status/2088305881159184552)；[跨硬體比較約 12.6 tok/s](https://x.com/mertcobanov/status/2088915144646545545)。

但 8/17 的新結果證明這不是固定上限。[七配置比較從 vLLM + NVFP4 的 11.2 tok/s，調到 SGLang cookbook 單流 21.6、10 streams aggregate 158 tok/s](https://x.com/Luc_Gibson/status/2089091152255373648)；[0xBakeer 花了一個週末從 stock FP8 的 7.88 一路調到單流 75、16 streams aggregate 256 tok/s](https://x.com/0xBakeer/status/2089092964404601310)，過程拆得很細：

- **Speculative decoding 是最大單一變數。** 同一組 FP8 權重，開 speculative decoding 從 7.88 直接跳到 58.5 tok/s（7.4x），模型輸出完全不變——因為主模型驗證每個 draft token，猜錯的丟掉。
- **DSpark drafter 比 MTP 便宜。** MTP 是模型內建的多缸引擎，每跑一次要過完整 vocab projection；DSpark 是外掛的 1B drafter，一次出 7 個 token。DSpark 接受率更低，但每個 draft token 成本 0.046 vs 0.153，整體快 46%。
- **Acceptance rate 是陷阱。** k=7 到 k=14，接受率從 98.7% 掉到 68.7%，但 generation 反而快 27%。決定吞吐量的不是接受率，是 mean tokens per forward pass。
- **Prefix caching 預設是關的。** vLLM 對 hybrid attention 模型（Qwen3.8-27B 回報 `is_hybrid=True`）自動停用 prefix caching，啟動日誌不會提示。手動打開後：19K shared prefix 的 prefill 快 14 倍，53K 的快 22 倍。
- **4-bit vs FP8 在高併發時收斂。** 單人 4-bit 比 FP8 快 27%；4 人快 20%；8 人快 10%；16 人時兩者差距收到 0.2% 以內，基本一樣。原因是單流是 memory-bandwidth bound（位元數越少越快），多流變成 compute bound（FP8 的額外精度不再是瓶頸）。

較保守的 matched-prompt bake-off 測到 [SGLang + EAGLE 單流約 31–32 tok/s，並明確表示沒有復現 161 tok/s 的單流說法](https://x.com/wikiwayne/status/2089084344015200280)。

這個 baseline 值得停下來看一眼：一台定位為 AI 工作站、128GB unified memory 的機器，未調校時跑 27B dense 竟然慢於多年前的 RTX 3090。

原因不是 Spark 差，是 workload 不對。Spark 的大記憶體適合放消費卡塞不下的大 MoE 或高精度模型；Qwen3.8-27B Q4 已經住進 24GB VRAM，這時 NVIDIA 獨顯的高記憶體頻寬才是決定性優勢。

**Spark 的 baseline 慢，但 serving stack 調整空間非常大——0xBakeer 從 7.88 到 75 全靠 stack 調校，沒有換模型也沒有換硬體。已經有 Spark 可以部署；要為 Qwen3.8-27B 買硬體，拿真實單流 latency 與多流 aggregate 分開比較，不能只看 128GB，也不能只看調校後的 256 tok/s。**

8/19 更新：[@MiaAI_lab 釋出 Spark 專用的最佳化 DSpark path](https://x.com/MiaAI_lab/status/2089806765290565991)，coding 場景（LRUCache）DSpark 51.5 tok/s 大幅領先 MTP 的 34.5；但長文寫作 MTP 反過來贏（24.1 vs 18.3）。一般聊天兩者差不多，約 21–24 tok/s。

| 場景 | DSpark tok/s | MTP tok/s | 勝出 |
|---|---:|---:|---|
| Coding（LRUCache） | 51.5 | 34.5 | DSpark +49% |
| Long essay | 18.3 | 24.1 | MTP +32% |
| Chat T=0 thinking off | 22.0 | 24.6 | MTP |
| Chat T=1 thinking on（預設） | 23.2 | 21.0 | DSpark |
| LRUCache 400 tok | 47.1 | 33.6 | DSpark +40% |

結論很清楚：**Spark 上 coding 用 DSpark、寫作用 MTP。** 不是選一個就好，是看 workload 切換。

---

## Mac：48GB 以上絕對可用

24–36GB Q4 約 6–18 tok/s；64–128GB Q6／8-bit 約 10–27 tok/s，MTP 解鎖後 47–56 tok/s。Apple Silicon 的優點很明確：安靜、省電、統一記憶體大、部署方便。缺點也很明確：Qwen3.8-27B 是 dense model，每個 token 都要讀取大部分權重，decode 吃記憶體頻寬。[社群早在發布當天就提醒：unified memory 機器要的是 MoE，dense 模型塞得下但會很慢](https://x.com/TheAhmadOsman/status/2088348410193600527)；[也有 Mac 使用者回報 dense 跑不好、MoE 表現好得多，連 MTP 都沒幫上忙](https://x.com/goinggodotnet/status/2088661342903251141)。

社群實測：

| 機器 | 量化／Runtime | Decode |
|---|---|---:|
| [M5 Max 128GB](https://x.com/kystudio_jp/status/2088924387391283639) | Q6 | 約 26.6 tok/s |
| [M4 Max 128GB](https://x.com/vigg_1991/status/2088932231029072198) | 8-bit MLX／LM Studio | 約 14.3 tok/s |
| [M4 Max 36GB](https://x.com/enesapp/status/2088923823676535096) | Q4、8K | 約 17.53 tok/s |
| [M4 Max、mlx-community MTP head](https://x.com/WescheNex1q) | MTP unlocked（239MB drafter） | 46.8 prose / 56.1 code |
| [M4 Max、MTPLX 最佳化](https://x.com/TypeNuevo/status/2089100306441269427) | MTPLX、coding agent | 約 52 tok/s |
| [M4 Pro 24GB Mac mini](https://x.com/mertcobanov/status/2088915144646545545) | 條件未完整揭露 | 約 15.1 tok/s |
| [M3 Max 36GB](https://x.com/rdvnrslnd/status/2088910439576928551) | Q6_K | 約 9.3 tok/s |
| [M3 Ultra 256GB](https://x.com/rophilogene/status/2088975801358143909) | 條件未完整揭露 | 約 21 tok/s |
| [M2 Max 96GB](https://x.com/outsource_/status/2088743329760469374) | BF16 | 約 13–20 tok/s |
| [M2 Max 96GB](https://x.com/outsource_/status/2088743407543812436) | Ollama MLX NVFP4 + adaptive MTP、thinking off | 約 31.5 tok/s |
| [M1 Max 64GB](https://x.com/shotalab_com/status/2088914258373542213) | Q4、128K、llama.cpp | 約 10.2 tok/s |

值得注意的是 @WescheNex1q 的 M4 Max「take 2」：前一天只有 29.5 tok/s，mlx-community 把 MTP head 拆成 239MB 獨立權重後，decode 跳到 46.8（prose）和 56.1（code）。但 prefill 仍然是 Mac 的瓶頸——同一個 8.6K token paste，Spark 4 秒吃完，Mac 要 35 秒。**Decode 已經不是 Mac 的問題了，prefill 才是。**

8/18 更新：[oMLX 0.6.1 發布](https://x.com/jundotkim)，這版直接針對 Qwen3.8 做了兩項最佳化。一是 Dual-ANE/GPU prefill（實驗性），有人去挖 private Apple runtime interface、用近似 INT8 weight，硬把 ANE 跟 GPU 塞在同一個 prefill path——[M3 Ultra 上 32K context prompt 處理 +18.9%](https://x.com/Leoskie_L)。二是 Lightning MTP kernel 再調一輪，[16K context decode 最高 +34%](https://x.com/Leoskie_L)。Dual-ANE/GPU prefill 預設關閉，因為峰值記憶體更高、載入時間更長。[omlx.ai 社群已經累積快 40 萬筆 Apple Silicon 速度結果](https://x.com/jundotkim)，從 0.6 開始連 intelligence benchmark 也收進去了。

8/19 更新：[MTPLX V2.9 發布](https://x.com/Youssofal_/status/2090384590913556598)——CLI 速度 +30%、app 速度 +60%、CPU 使用率降 80%、streaming 卡頓減少 95%。所有 MTPLX 模型重新調校為更小且更快（同品質，需重新下載）。bare speed model 搭配 session bank 達到 **175 tok/s**——這是目前 Mac 上 Qwen3.8-27B 回報的最高數字。

按記憶體級距處理：

- **16GB：** 極低位元量化，只做試跑。[16GB MacBook Air 用 Atomic Dynamic AD-IQ3_S 能載入](https://x.com/atomic_chat_hq/status/2088380082780074236)，但原貼沒有提供速度，不能把「能載入」外推成「工作流暢」。
- **24–36GB：** Q4，從 8K／16K context 起步。[約 13GB 的 MLX build 在 M2 Pro 回報峰值記憶體約 14.6GB、約 11 tok/s](https://x.com/Chirag693/status/2088966506675581233)，代價是 vision quality 低於標準 4-bit。
- **64GB：** Q4／Q6，32K context，保留系統記憶體。
- **96–128GB：** 可測 Q6、8-bit 甚至 BF16，但先問高精度是否真的比速度重要。

一組[橫跨三台 Mac 與 RTX 3090 的比較](https://x.com/JoshuaSWarren/status/2089093647484518511)：MLX 約比 Ollama 快 1.5 倍，Q3 反而比 Q4 慢 2.7 倍，MTP 增益隨硬體大幅變動。「量化越小一定越快」與「MTP 一定加速」都不能當預設假設。

一個容易誤讀的 outlier：[M5 Max Abliterated + MTPLX 特製混合精度版本跑到約 58 tok/s](https://x.com/trevorwood222/status/2088881640001138752)，但只有 4K context，模型與推理配置不是標準 Q6。不能直接代表一般 M5 Max 部署。

Mac 是你每天工作的主機的話，不要把記憶體全部給模型。36GB 機器載入 23GB 的 Q6，理論上放得下，實務上 OS、IDE、瀏覽器和 agent tools 都搶同一池記憶體。**本地 AI 的機器不是只有模型在用。**

---

## AMD／Intel 社群數字：RX 7900 XTX、Arc Pro B70、Radeon AI PRO R9700

8/18 更新：[sudoingX 的 MTP A/B benchmark repo](https://github.com/sudoingX/qwen38-mtp) 也收集了非 NVIDIA 硬體的標準化數字。

| 硬體 | Baseline tok/s | MTP tok/s | 增幅 | 備註 |
|---|---:|---:|---|---|
| [RX 7900 XTX](https://github.com/sudoingX/qwen38-mtp) | 30.7 | 43.9 | +43% | llama.cpp |
| [2x RX 9070](https://github.com/sudoingX/qwen38-mtp) | 22.1 | 41.6 | +88% | 雙卡 |
| [AMD Radeon AI PRO R9700](https://github.com/sudoingX/qwen38-mtp) | — | 43.3 | — | 單筆數據 |
| [Intel Arc Pro B70](https://github.com/sudoingX/qwen38-mtp) | 33.7 | 86.5 | **+157%** | vLLM，MTP 增幅最大的一張 |

Intel Arc Pro B70 的 +157% MTP 增幅是整張表裡最高的，而且跑的是 vLLM 不是 llama.cpp。AMD 這邊 RX 7900 XTX 的 43.9 tok/s 和 Radeon AI PRO R9700 的 43.3 tok/s 大約在 RTX 3090 MTP 範圍內。雙 RX 9070 的 41.6 有趣但不高——兩張卡不一定比一張快，跨卡通訊有成本。

這些數字樣本量都只有個位數，只能當定位參考，不能當採購依據。

---

## Qwen3.8-27B MTP Speculative Decoding：最值得開，也最容易被誤讀

MTP 讓模型用自己的 prediction head 先草擬多個 token，再由主模型驗證。RTX 4090 社群數字從約 44.9 拉到 86.5 tok/s；RTX 5090 也有約 74 到 113 的回報。本站 vLLM 測試從 57.83 到 100.33，單人快 73.5%。[sudoingX 的 MTP A/B benchmark repo](https://github.com/sudoingX/qwen38-mtp) 收集了 20+ 張卡的標準化 baseline vs MTP 對照，是目前最完整的社群資源。

但 MTP 不是固定 2 倍。最明確的反例來自 M4 Mac mini：Q4_K_M、llama.cpp v10360 的 sweep 中，[baseline 5.91 tok/s，最佳 n-max 2／p-min 0.8 只有 6.34；n-max 4／p-min 0.0 反而掉到 3.05](https://x.com/GreenDragonDM/status/2089086455125770437)。

幾個實際觀察：

- Coding、boilerplate 等可預測輸出，acceptance 通常較高。
- 複雜 reasoning、創意文字，接受率可能下降。
- draft 數越高不一定越快，驗證也有成本。
- 不同 llama.cpp commit 可能出現效能變化。

部署程序：MTP 關閉跑 20 組真實 prompt → draft 2 同一組 → draft 4 同一組。比較的不是瞬間 tok/s，是整個任務 wall time、acceptance rate、TTFT 與失敗率。

---

## Qwen3.8-27B 量化品質驗收：Q4 vs FP8 agent 實測

Qwen3.8-27B 的賣點是 agentic workflow。部署驗收要測 agent，不是問「台北有什麼景點」。

保留一套 20–50 題的 golden set，至少包含：正確選擇 5–10 種 tools、必填與選填參數不混淆、嚴格輸出 JSON schema、tool error 後能修正不陷入 loop、20K 以上 context 仍能引用前文、修改程式後會跑測試、thinking on／off 各跑一次、Q4 與更低位元量化做對照。

低位元量化的損失不是平均分配。前代 Qwen3.6-27B 的壓縮測試就出現數學 benchmark 幾乎沒掉、[TauBench tool calling 卻從 82.9 掉到 61.3、降幅 26%](https://ai-coding.wiselychen.com/bonsai-27b-qwen36-compression-local-inference-democratization/) 的情況。Qwen3.8-27B 的早期 Q4 回報也呈現類似警訊：[長程 Agent 與 tool calling 可以很穩，但細節能力仍落後 frontier 模型](https://x.com/ryan4yin/status/2088927226482032826)；[跟 GPT-5.6 Luna Max 做相同實作，雖能完成，產出品質仍有明顯差距](https://x.com/_nodelay/status/2088921417102573893)。

而且部署驗收不能只沿用官方表格。[社群指出 Qwen3.8-27B 與 Qwen3.6-27B 的 HF config 完全相同、零變更，卻宣稱 DeepSWE 提升 217%、19 項 benchmark 贏 Opus 4.6 15 項，質疑這是純訓練帶來的真實進步，還是 benchmark 文化出了問題](https://x.com/DefaultUser1777/status/2088932630033231885)。這不等於模型沒有進步，是提醒：最後採用哪個量化、runtime 和 prompt template，必須用自己的任務復現。

---

## 坦白說

這篇的數據全部來自 X 社群自行回報和本站實測，不是同條件 benchmark。每個人的 llama.cpp commit 不同、量化版本不同、context 設定不同、MTP 開關不同、甚至有人功耗限制都沒察覺。sethprattsf 在 RTX PRO 6000 上測到 llama.cpp CUDA GGUF 品質直接崩掉，本站自己的 agent 品質系統性評測也還沒做——[前一篇](https://ai-coding.wiselychen.com/qwen-3-8-27b-open-weights-local-security/)就承認了這一點。

把這些數字當成「部署區間」而不是排行榜。你真正需要的 benchmark 只有一個：**你自己的 workload、你自己的 prompt、你自己的品質 golden set。**

---

## Qwen3.8-27B Runtime 選擇：llama.cpp vs vLLM vs SGLang vs MLX

| 情境 | 預設選擇 | 原因 |
|---|---|---|
| 想最快開始聊天 | LM Studio／Ollama | 安裝方便 |
| 單人 coding agent | llama.cpp + MTP | 單流快、跨平台、參數可控 |
| NVIDIA 多使用者 API | vLLM | continuous batching、生態成熟 |
| 長 context／進階 serving | SGLang | scheduler、cache 與 serving 最佳化 |
| DGX Spark | SGLang | 調校空間最大 |
| Apple Silicon | MLX 或 llama.cpp | 原生 Metal 路線 |

不要把 GUI、模型格式和 inference engine 混成同一件事。Ollama 是很好的入口，但 production 需要併發排程、p95 latency、metrics 和故障隔離。

選引擎之前先回答：**這台機器服務一個人，還是五十個人？**

---

## Qwen3.8-27B Production 部署 Checklist

### 模型與品質

- [ ] 固定模型 repo、檔名、hash 與 license
- [ ] 保存 Q4／IQ3 的 agent golden set 結果
- [ ] 測 thinking on／off 的品質與 token 成本
- [ ] 多模態若要用，確認 projector 與 API path 已實測

### 效能

- [ ] 分開記錄 prefill 與 decode
- [ ] 記錄 TTFT、TPOT、p50、p95，不只平均 tok/s
- [ ] 用真實 input／output 長度測試
- [ ] 用真實併發數測試，不拿 single-stream 代替 production

### 容量與穩定性

- [ ] 8K、32K、64K 分段量 VRAM／RAM
- [ ] 保留 10–15% 記憶體 headroom
- [ ] Runtime、driver、CUDA／Metal 更新後自動重跑 benchmark
- [ ] Server 前面放 auth、rate limit、timeout 與 sandbox；地端不等於安全完成

---

## Qwen3.8-27B 硬體選購與部署決策樹

**你已經有硬體嗎？**

- 有 RTX 3090：Q4 + llama.cpp + MTP + 32K，先檢查 power limit。
- 有 RTX 4090：同一套起步，單人 coding agent 最均衡。
- 有 RTX 5090：單人用 llama.cpp Q4 + MTP，32K 日常、128K 改量化 KV 並單獨壓測；給小團隊用就換 SGLang NVFP4 + MTP-2，四人上限，不要貪到八人。
- 有 RTX PRO 6000：優先測 NVFP4／vLLM／SGLang，品質 regression suite 不能省。
- 有 Mac：按統一記憶體容量選 Q4／Q6，MLX 與 llama.cpp 都要實測。
- 有 DGX Spark：從 SGLang cookbook 起步，分開量 single-stream 與 aggregate throughput。

**你準備買硬體嗎？**

- 最低成本實用：[二手 RTX 3090 24GB；社群也有約 US$2,000 等級整機的入門建議](https://x.com/jun_song/status/2088297115227468168)。
- 低風險高成熟度：RTX 4090 24GB。
- 高速、長 context、NVFP4：RTX 5090 32GB。
- 多使用者服務、96GB VRAM：RTX PRO 6000。
- 已經在 Apple 生態且重視安靜、省電：Mac；不要只看統一記憶體容量。
- 想跑多種大模型與多流 serving：DGX Spark；不要用 aggregate TPS 代替單人互動速度。

**你的需求真的需要 262K 嗎？**

- 不確定：就不需要。從 32K 開始。
- 只有少數長文件：把長文任務排到獨立 endpoint。
- 每個 session 都超過 100K：這是 serving architecture 問題，不只是把 `--ctx-size` 數字改大。

---

## 結語

我跟 AI 將看到的 X 貼文整理成這張表。我加 AI 也不可能看過所有網友實測，我將看到的放在這裡，應該會逐步更新（不保證時效）。

48 小時內，快要 300+ 篇關於自己的實測報告。開源社群把一個開源模型，在六種硬體加上一堆冷門硬體的 serving stack 參數，全部摸過一遍。有人從 7.88 調到 75，有人把 Mac MTP 從不能用調到 56 tok/s。沒有一人是原廠工程師。

開源模型真正的護城河不是權重，是這群人。

---

## 參考資料

### 官方文件與本站文章

- [Qwen3.8-27B 官方模型頁](https://huggingface.co/Qwen/Qwen3.8-27B)
- [llama.cpp multimodal 文件](https://github.com/ggml-org/llama.cpp/blob/master/docs/multimodal.md)
- [llama.cpp speculative decoding 文件](https://github.com/ggml-org/llama.cpp/blob/master/docs/speculative.md)
- [vLLM MTP 文件](https://docs.vllm.ai/projects/speculators/en/latest/user_guide/algorithms/mtp/)
- [本站：Qwen3.8-27B 開源與 RTX 5090 長 context 實測](https://ai-coding.wiselychen.com/qwen-3-8-27b-open-weights-local-security/)
- [本站：Qwen3.8-27B RTX 5090 SGLang／vLLM／llama.cpp 實測（YouTube 逐字稿）](https://ai-coding.wiselychen.com/youtube-qwen38-27b-rtx5090-sglang-vllm-mtp-transcript/)
- [本站：Inference Engine 選型不是技術問題，是硬體策略問題](https://ai-coding.wiselychen.com/inference-engine-selection-hardware-strategy/)
- [本站：Bonsai 27B 壓縮測試——TauBench tool calling 掉 26%](https://ai-coding.wiselychen.com/bonsai-27b-qwen36-compression-local-inference-democratization/)
