---
layout: post
title: "Inference Engine 選型指南 (2026)：先選硬體策略，引擎自然會浮現"
date: 2026-05-23 09:00:00 +0800
permalink: /inference-engine-selection-hardware-strategy/
image: /assets/images/inference-engine-selection-logo.png
description: "你不應該先選 inference engine，你應該先選硬體策略、workload 形狀、serving 模式。引擎只是這三個答案的函數輸出。這篇拆解 8 個主流引擎在不同硬體 / workload 下的定位，跟一份決策清單。"
---

![Inference Engine 選型地圖：硬體輸入到 8 個主流引擎](/assets/images/inference-engine-selection-logo.png)

> 你不應該先選 inference engine，你應該先選硬體策略、workload 形狀、serving 模式。引擎只是這三個答案的函數輸出。

## TL;DR

- **VRAM 決定能不能跑，bandwidth 決定跑多快。** M3 Ultra unified memory 跟 H100 HBM 都能塞 70B，但 H100 跑起來快約 4 倍。Fit ≠ Speed。
- **Inference 不是一個 phase，是兩個：** prefill 是 compute-bound，decode 是 memory-bandwidth-bound。你的 workload 形狀決定瓶頸在哪。
- **8 個主流引擎沒有「誰最好」**，只有「在什麼硬體 + 什麼 workload 下，哪個是預設答案」。
- **本地引擎 ≠ production 引擎。** llama.cpp / MLX-LM / Ollama 的 server 都不是給你扛 100 個併發用的——MLX-LM 官方文件自己就寫了 "not recommended for production"。

---

## 一個常見的錯誤問題

幾乎每個剛要碰地端 LLM 的團隊，問的第一個問題都長這樣：

> 「我應該用 vLLM 還是 TensorRT-LLM？」
> 「llama.cpp 跟 Ollama 哪個快？」
> 「ExLlamaV2 是不是現在最快的？」

這些問題本身就錯了。

它們錯在順序。引擎不是你的第一個決定——它是你前面三個決定的「函數輸出」：

1. 你的硬體長什麼樣（VRAM、bandwidth、interconnect）？
2. 你的 workload 是什麼形狀（短 prompt 長回答？長 context？高併發？）？
3. 你的 serving model 是什麼（單人 local？內部小團隊？大規模 production？）？

回答完這三題，引擎幾乎是「自動浮現」的。順序倒過來，幾乎一定踩坑。

這篇是接著 [企業級地端 LLM 系統架構藍圖](/local-llm-enterprise-architecture/) 跟 [Mac-First Enterprise Inference Stack](/mac-first-enterprise-inference-stack-mtp/) 的下一層深入——前面兩篇把引擎當黑盒子用 Ollama 或 MLX，這篇把那個黑盒子打開。

基礎概念與資料點整理自 Ahmad Osman 的 "Inference Engines for LLMs & Local AI Hardware (2026 Edition)"，再加上實際接觸客戶看到的坑跟既有框架。

---

## 看過的三種典型踩坑

坦白說，這幾種狀況我看過不只一次：

**Case 1：看 benchmark 數字選引擎**

「這個引擎 single user 跑出 180 tok/s 耶」就決定用它。到 production 才發現：
- 那是 1K input / 128 output 跑出來的數字
- 自己的 workload 是 80K context coding agent
- 50 個併發用戶上來，KV cache 直接爆掉，TTFT 變成 30 秒

Single-user tokens-per-second 是最容易誤導人的數字。它幾乎不能預測你 production 的行為。

**Case 2：以為 Tensor Parallelism 就是最快的**

「我有 4 張 GPU，當然要 TP=4 嘛」。結果板子上沒 NVLink，全靠 PCIe，TP 的 all-reduce 通訊成本爆炸，反而比 Pipeline Parallelism 慢。vLLM 官方文件就直接寫了：沒有 NVLink，PP 可能贏 TP。

但這件事不會自動跳出來提醒你。

**Case 3：用 Ollama 撐 demo，正式上線就崩**

內部 5 個人試用一切順利，正式對 50 個業務開放，第一週就卡死。Ollama / llama-server / MLX-LM 都是很棒的「個人 / demo / 內部小團隊」工具，但它們的設計目標不是 production serving。MLX-LM 官方 README 自己都寫了 "not recommended for production"——它不是在客氣。

這三個 case 的共同點：先選了引擎，才回頭發現硬體跟 workload 撐不住。

---

## 真正的轉折點：理解 inference 是兩個 phase

要避開上面的坑，你必須先理解一件事——「LLM 推論」根本不是一個 phase，是兩個截然不同的階段：

### Prefill（讀 prompt）
- **動作：** 把整個 input prompt 跑完一遍 forward pass，建立初始 KV cache
- **特性：** Compute-intensive，吃 FLOPS
- **誰快？** 看你的 attention kernel、chunked prefill 做得好不好

### Decode（一個一個吐 token）
- **動作：** 每吐一個 token，要重新讀一次權重 + KV cache
- **特性：** Memory-bandwidth-bound，吃 GB/s
- **誰快？** 看你的記憶體頻寬

這個區分解釋了 90% 的事情：

| Workload 形狀 | 瓶頸在哪 |
|--------------|---------|
| 短 prompt、長回答（一般 chat） | Decode，看 memory bandwidth |
| 長 prompt、短回答（RAG / 文件摘要） | Prefill，看 attention kernel + chunked prefill |
| 多人併發 | Scheduler 品質（continuous batching、cache paging） |
| 長 context | KV cache 管理（PagedAttention、KV quant） |
| MoE 模型 | Expert routing + interconnect（all-to-all） |
| 多機 multi-node | Interconnect（NVLink、RDMA、disaggregation） |

這也是為什麼「VRAM 大就贏」是個迷思。

舉個具體的數字——Apple M3 Ultra unified memory bandwidth 是 819 GB/s。NVIDIA H100 SXM HBM bandwidth 是 3.35 TB/s。一台 M3 Ultra Mac Studio 可以塞下 H100 塞不下的大模型（unified memory 容量大），但同樣模型 H100 跑起來大約快 4 倍。

**Fit 是 capacity 的問題。Speed 是 bandwidth 的問題。這兩件事不一樣。**

---

## 真正的 5 個瓶頸（不是只有 VRAM）

在你選引擎之前，要看的不是 VRAM，是這 5 件事：

### 1. Memory bandwidth（不是只看 VRAM 大小）
VRAM 決定能不能跑，bandwidth 決定 decode 多快。consumer GPU 跟 datacenter GPU 之間的差距，bandwidth 比 VRAM 大。

### 2. KV cache 成長
KV cache 跟 batch size、context length 成正比。長 context 場景，常常「權重塞得下，KV cache 塞不下」。PagedAttention 解的就是這件事。

### 3. Interconnect（一旦跨卡就要付通訊成本）
- Tensor parallelism：頻繁 all-reduce，吃 NVLink
- Pipeline parallelism：只在 stage 邊界通訊，PCIe 也撐得住
- Expert parallelism（MoE）：all-to-all，吃 interconnect 吃得最兇

### 4. Scheduler 品質
誰決定哪個 request 進 batch？長 prompt 會不會卡住短 decode？怎麼避免某個用戶餓死？「支援 batching」跟「scheduler 像 production 系統」是兩回事。

### 5. Runtime overhead
CUDA graphs、kernel fusion、sampling、tokenizer、HTTP layer、LoRA 切換、structured decoding——單獨看每個都只是 1-2% overhead，加起來就是雙位數差距。

---

## 8 個主流引擎的定位地圖

OK，講完瓶頸，現在來看引擎本身。我把它們分成四個家族：

### 家族一：可攜性 (Portability)

**llama.cpp**
- 角色：硬體 weird、constrained、edge、offline 的時候，幾乎沒對手
- 支援：Apple Silicon (Metal)、x86 (AVX/AMX)、CUDA、AMD HIP、Vulkan、SYCL、CPU+GPU hybrid offload
- llama-server 不是「玩具」——它有 OpenAI-compatible API、continuous batching、JSON schema、function calling、speculative decoding
- **限制：** 多機 production serving 不要用，官方文件自己說 RPC backend 是 "proof-of-concept, fragile, insecure"
- **不要拿來：** Multi-GPU production serving

### 家族二：Apple Unified Memory

**MLX / MLX-LM**
- 角色：Mac-first，吃 unified memory 紅利
- 為什麼特別：unified memory 不用在 CPU / GPU 之間搬陣列，可以塞 24 GB consumer GPU 塞不下的模型
- **限制：** 比 H100 慢，而且 MLX-LM 官方 README 自己寫 server 不建議 production

### 家族三：Consumer CUDA 量化引擎

**ExLlamaV2**
- 角色：單張 RTX 3090 / 4090 / 5090 的本機愛好者引擎
- 支援：paged attention、dynamic batching、prompt caching、KV cache dedup、speculative decoding
- 適合：本地 coding assistant、EXL2 量化模型、prosumer workstation

**ExLlamaV3**
- 角色：V2 的延伸版，往 multi-GPU 跟本地 MoE 走
- 加入：EXL3 量化（基於 QTIP）、TP / EP 給 consumer 硬體、TabbyAPI（OpenAI-compatible）
- 適合：2-4 張 consumer NVIDIA GPU、想在本地跑 MoE
- **警告：** 還是有些模型不支援 TP / EP，邊緣比較粗糙

### 家族四：Production Serving

**vLLM**——這是大部分團隊上 production 的「預設答案」
- PagedAttention KV 管理、continuous batching、chunked prefill、prefix caching
- 量化支援廣：FP8 / MXFP8 / MXFP4 / NVFP4 / INT8 / INT4 / GPTQ / AWQ / GGUF
- 平行支援：TP / PP / DP / EP / CP（context parallel）
- OpenAI 跟 Anthropic Messages API 相容、gRPC、multi-LoRA
- 硬體支援廣：NVIDIA、AMD、x86/ARM/PowerPC CPU，TPU/Gaudi/Ascend/Apple Silicon 透過 plugin

**SGLang**——當你的 production 變醜的時候
- RadixAttention prefix cache、prefill-decode disaggregation、speculative decoding
- 差異化：把 prefill（compute-heavy）跟 decode（memory-heavy）拆成不同 instance，KV cache 在它們之間搬
- 適合：結構化輸出、長 context、MoE、routing、disaggregation 場景
- 一句話描述：你的問題不是「能不能跑」而是「在敵意流量下 latency / cost 會不會崩」的時候用它

**TensorRT-LLM**——NVIDIA-only 的極致性能
- 角色：你已經 lock 在 NVIDIA datacenter，要把硬體榨乾
- 強項：FP8（H100 上 double 性能、halve 記憶體，accuracy loss minimal）、FP4（B200）
- 包含：custom kernels、prefill-decode disaggregation、Wide Expert Parallelism、speculative decoding
- **限制：** 不要拿來做可攜性、不適合快速變動的實驗性模型、不適合小型本機

**NVIDIA Dynamo**（不是引擎，是引擎之上的 orchestration）
- 角色：當單一引擎已經不夠用，要管整個 fleet
- 功能：disaggregation、intelligent routing、multi-tier KV caching
- 通常坐在 vLLM / SGLang / TensorRT-LLM 之上

---

## 一頁式決策清單

照這個順序問自己（這就是 Ahmad 的選型框架，我把它寫成決策樹）：

```
1. 我的硬體？
   ├─ Laptop / edge / 奇怪硬體 → llama.cpp
   ├─ Mac → MLX / MLX-LM
   ├─ 單張 RTX → ExLlamaV2 或 vLLM
   ├─ 2-4 張 consumer GPU → ExLlamaV3 或 vLLM
   ├─ 8×H100 node → vLLM / SGLang / TensorRT-LLM benchmark 三個
   ├─ B200 / GB200 fleet → TensorRT-LLM + Dynamo
   ├─ AMD MI300+ → vLLM / SGLang on ROCm
   └─ Intel Xeon / Arc → OpenVINO GenAI

2. 我的 workload？
   ├─ 短 prompt 長回答 → decode 為主，看 memory bandwidth
   ├─ 長 prompt 短回答 → prefill 為主，要 chunked prefill
   ├─ 多人併發 → scheduler 品質決定一切
   ├─ 長 context → KV cache 管理是核心
   ├─ MoE → expert parallelism + interconnect
   └─ Multi-node → disaggregation + KV routing

3. 我的 serving model？
   ├─ 一個人本地用 → llama.cpp / MLX / ExLlamaV2 都行
   ├─ Demo / 內部 5-10 人 → llama-server / MLX-LM / Ollama 撐得住
   ├─ 內部團隊 50-500 人 → vLLM 起跳，看狀況加 SGLang
   ├─ 對外大規模 production → vLLM / SGLang / TensorRT-LLM 三選一 + Dynamo
   └─ 跨機房 fleet → Dynamo orchestration
```

---

## Benchmark 的時候，不要只看 tok/s

最後一個建議：benchmark 引擎的時候，「我跑出 180 tok/s」這個數字幾乎沒有意義。

一個有意義的 benchmark 要包含：

**情境定義**
- 模型：精確型號、架構、參數量、MoE active params
- 權重：dtype、量化格式、group size、calibration
- 引擎：版本、commit、backend、flags
- 硬體：GPU SKU、記憶體容量、bandwidth、interconnect

**Workload 定義**
- input / output length 分布
- 併發數
- 是否 streaming
- 有沒有 shared prefix（影響 prefix cache）
- 有沒有 structured output

**指標**
- TTFT（time to first token）
- TPOT（time per output token）
- p50 / p95 / p99 latency
- Tokens/s、Requests/s
- GPU memory headroom
- KV cache hit rate
- Cost per 1M tokens

**鐵則**
- 不要只用 single-user tok/s 比引擎
- 要用你「真實的 prompt 跟 output 分布」測
- 要用「真實的併發數」測
- prefill 跟 decode 分開測
- 看 p95 / p99 不是只看平均
- 看 KV cache reuse（如果你的 app 有重複 prefix）
- structured output / multi-LoRA 要分開 benchmark
- 每次升級 driver / CUDA / model / engine 都要重測

---

## 一句話總結

引擎不是入口，是出口。

先回答這 10 個問題，你的引擎自然會浮現：

1. 我的硬體是什麼？
2. 模型塞得進 fast memory 嗎，還是只能塞 unified / system memory？
3. 我的瓶頸是 prefill 還是 decode？
4. 我的 context length 跟併發數要多大？
5. 我的 prompt 有沒有 shared prefix？
6. 我的模型是 dense / MoE / multimodal / hybrid？
7. 我要 local convenience，還是 production serving，還是 fleet orchestration？
8. 我要的量化格式，在目標引擎上有 optimized kernel 嗎？
9. 我的 interconnect 是什麼（PCIe / NVLink / NVSwitch / RDMA）？
10. 我在優化哪一個：latency / throughput / cost / privacy / portability / dev speed？

回答完，剩下的就只是把答案對照上面那張地圖。

---

## 常見問題 Q&A

**Q: Ollama 到底能不能用？**

個人本機、demo、5-10 人內部試用都沒問題，方便又輕。但你要對外開放 50+ 用戶、或要進 production，就應該換 vLLM 或 SGLang。這不是 Ollama 不好，是它的設計目標不一樣。

**Q: 為什麼我看到的 benchmark 跟我自己跑出來的差很多？**

幾乎一定是 workload 形狀不一樣。對方的 benchmark 可能是 1K input / 128 output / 1 user，你的 production 是 80K context / 500 output / 50 concurrent users。這完全不是同一回事。

**Q: 我已經買了 8 張 RTX 4090，可以用 TensorRT-LLM 嗎？**

可以，但你的瓶頸大概不是引擎效能，是 interconnect。沒有 NVLink 的話，先試 PP（pipeline parallel），不要預設 TP。vLLM / ExLlamaV3 在這個配置上可能更合適。

**Q: 我要做地端 RAG，引擎怎麼選？**

RAG 是「長 prompt 短回答」的形狀——prefill 為主。重點看：(1) 引擎有沒有 chunked prefill (2) 有沒有 prefix caching（你的 retrieved chunks 會重複）。vLLM 跟 SGLang 都行，SGLang 的 RadixAttention 在重複 prefix 上更猛。

**Q: 我的工作流是 long-context coding agent（80K+），怎麼選？**

KV cache 會變成主要瓶頸。一定要 PagedAttention 等級的管理。在 production：vLLM / SGLang 起跳。在 local：llama.cpp 跟 ExLlamaV2 都有 paged attention，但要小心 context length 上限跟 KV quantization 的選項。

---

## 相關資源

- Ahmad Osman, [Inference Engines for LLMs & Local AI Hardware (2026 Edition)](https://x.com/TheAhmadOsman) — 本篇基礎概念來源
- [企業級地端 LLM 系統架構藍圖](/local-llm-enterprise-architecture/) — 引擎外圍的 Auth / Log / Sandbox 設計
- [Mac-First Enterprise Inference Stack](/mac-first-enterprise-inference-stack-mtp/) — Apple Silicon 推論細節
- [llama.cpp MTP merged](/llama-cpp-mtp-merged-local-llm-2x-speedup/) — llama.cpp 最新效能進展
- [Qwen 3.6 27B on GB10](/qwen-3-6-27b-gb10-home-inference-sonnet-level/) — 家用推論硬體實測

---

挑引擎這件事很容易變成「跟著最潮的工具走」。但 inference engine 的選型，本質是硬體 × workload × serving model 的函數。先把這三個輸入想清楚，輸出（引擎）幾乎是自動的。

順序倒過來，你會在 production 上線那天才發現踩坑——而那時候要換引擎，成本就高了。
