---
layout: post
title: "MoE Offload 完全拆解：為什麼 671B 模型只吃 17GB VRAM 還能跑，以及 DeepSeek 從 V3 到 V4 怎麼讓它越跑越快"
date: 2026-07-23 09:00:00 +0800
permalink: /moe-offload-deepseek-v3-v4-local-inference-optimization/
description: "一個 671B 參數的模型，VRAM 只佔 17GB 就能跑推理——靠的是 MoE expert offload，把 97% 閒置的 expert 權重卸到 CPU RAM。這篇從原理拆起：MoE 為什麼天生適合 offload、offload 的機械結構（什麼放 GPU、什麼放 CPU）、PCIe 頻寬瓶頸怎麼緩解，以及 DeepSeek 從 V3 到 V4 在激活比例、KV Cache 壓縮、expert 體積三個維度上如何系統性降低 offload 的 PCIe 壓力。附 RTX Pro 6000 實測數據。"
image: /assets/images/moe-offload-cover.png
categories: [AI 前沿技術]
author: Wisely Chen
---

# MoE Offload 完全拆解：為什麼 671B 模型只吃 17GB VRAM 還能跑

先講一件聽起來不太合理的事。

上週我在一台 RTX Pro 6000（96GB VRAM）+ 512GB RAM 的機器上跑 DeepSeek V4 Flash。這個模型有 284B 參數，Q8 量化後 151GB——遠超 96GB VRAM。

但它跑起來了。而且不只是「能跑」：

| 配置 | VRAM 佔用 | Decode 速度 | CPU Expert 層數 |
|------|----------:|----------:|--------------:|
| MoE 全部放 CPU | 17.7 GB | ~7 tok/s | 43（全部） |
| 部分 MoE 留 GPU | 91.9 GB | ~25 tok/s | 20 |

一個 151GB 的模型，只用 17.7GB VRAM 就能推理。剩下的 133GB 權重去哪了？答案是 CPU RAM。

這不是什麼 hack，是 MoE 架構的核心特性——**大部分參數在每次推理時根本不會被用到，所以不需要待在 GPU 上。** 這個機制叫 MoE expert offload。

---

## 一、先搞懂 MoE 的結構：為什麼它天生適合 offload

要理解 offload，得先理解 MoE（Mixture of Experts）的內部結構。

一個標準的 Transformer 模型，每一層有兩個核心元件：**Attention**（負責「看上下文」）和 **FFN**（負責「處理資訊」）。每個 token 進來，兩個元件都要完整跑一遍——這就是 Dense 模型。

MoE 的改動只有一個：**把 FFN 拆成很多份，每份叫一個 expert，每個 token 只挑幾份來用。**

拿 DeepSeek V3 舉例。它有 61 層 Transformer，其中 60 層是 MoE 層。每個 MoE 層裡有 **256 個路由專家 + 1 個共享專家**，但每個 token 只激活其中 **8 個路由專家 + 1 個共享專家**。

算一下：256 個裡面只用 8 個，**97% 的 expert 權重在每個 token 的推理過程中是完全閒置的。**

![Dense 模型 vs MoE 模型：97% 的常態閒置](/assets/images/moe-offload-dense-vs-moe.png)

這就是 MoE 天生適合 offload 的原因——閒置的權重不需要待在 GPU 上。

### Dense 模型為什麼不行

Dense 模型（比如 Llama 405B）沒有這種「閒置」的概念。每個 token 需要模型裡的每一個參數都參與運算。你把任何一層搬到 CPU，GPU 就得等它算完才能繼續——整個 pipeline 被最慢的那一層卡死。

MoE 不一樣：那 97% 的閒置 expert 可以安靜地待在 CPU RAM 裡，只有被 router 選中的那幾個 expert 才需要臨時搬到 GPU 來算。**搬的量小（只搬被選中的 expert），而且可以預取（router 的結果可以提前知道，下一個 token 的 expert 在當前 token 計算期間就開始傳輸）。**

這就是 MoE offload 的核心邏輯。

---

## 二、MoE Offload 的機械結構：什麼放 GPU、什麼放 CPU

具體來講，MoE offload 把模型的元件分成兩類：

### 常駐 GPU 的元件
- **Attention 層**（Q/K/V 投影、KV Cache）——每個 token 都要用，而且對延遲最敏感
- **共享專家（Shared Expert）**——每個 token 都會經過，不能省
- **路由閘門（Router/Gate）**——決定每個 token 走哪些 expert，計算量極小但必須即時

### 放 CPU RAM 的元件
- **路由專家（Routed Experts）的 FFN 權重**——每個 token 只用其中 3-8%，其餘閒置

在 llama.cpp 裡，這對應兩個關鍵參數：

```
-ngl 999        # 把所有非 MoE 層（attention 等）推到 GPU
--n-cpu-moe 999 # 把所有 MoE expert 放 CPU
```

第一個參數確保 attention 在 GPU 上跑得快，第二個參數把大量閒置的 expert 權重卸到 CPU RAM。兩個配合，就是最基本的 MoE offload 配置——**模型的「大腦」（attention + shared expert）在 GPU 上快速運算，模型的「知識庫」（routed experts）在 CPU RAM 裡待命。**

這也解釋了為什麼上面那張表裡 MoE 全放 CPU 只佔 17.7GB VRAM——那 17.7GB 就是 attention 層 + shared expert + router 的大小，整個 MoE expert 倉庫都在 CPU 的 512GB RAM 裡。

---

## 三、瓶頸：PCIe 頻寬決定一切

但 offload 不是免費的午餐。

Expert 權重從 CPU RAM 傳到 GPU，走的是 PCIe 匯流排。PCIe 4.0 x16 的理論頻寬是 ~32 GB/s，PCIe 5.0 是 ~64 GB/s。GPU 本身的計算其實很快——在 MoE offload 的配置下，GPU 計算只佔總時間的 15% 左右，**剩下 85% 的時間都在等 PCIe 傳輸。**

這就是為什麼 MoE 全放 CPU 只有 7 tok/s——不是 GPU 算不動，是等資料等到天荒地老。

![核心瓶頸：GPU 85% 時間在等 PCIe 傳輸](/assets/images/moe-offload-pcie-bottleneck.png)

問題的本質是：每生成一個 token，router 選中 8 個 expert（V3 的情況），這 8 個 expert 的權重要從 CPU RAM 搬到 GPU，GPU 算完再搬下一批。搬的次數 x 每次搬的量 / PCIe 頻寬 = 你的等待時間。

### 三種緩解策略

**一、Expert 預取（Prefetching）。** 在當前 token 計算的同時，提前把下一個 token 可能需要的 expert 權重從 CPU 搬到 GPU。原理是 router 可以提前算出「下一個 token 大概需要哪些 expert」，利用計算和傳輸的 overlap 來隱藏延遲。問題是 router 的選擇跟輸入有關，預測不可能百分之百準確——預取錯了就白搬。

**二、部分 MoE 層留 GPU。** 不是全放 CPU，而是把一部分高頻使用的 MoE 層留在 GPU VRAM 裡。上面表格裡的第二行就是這個策略——43 層 MoE 裡留 23 層在 GPU，速度從 7 跳到 25 tok/s，代價是 VRAM 從 17.7GB 漲到 91.9GB。

這是最直覺的 trade-off：**VRAM 越多，能留在 GPU 的 expert 越多，需要走 PCIe 的就越少，速度就越快。** 所以 MoE offload 場景下，512GB RAM 這種大 DRAM 配置才有意義——不是為了記憶體本身，是為了讓更多 expert 有地方待。

**三、減小每次搬運的量。** 這是架構層面的優化——如果每個 token 激活的 expert 數量更少、每個 expert 更小，PCIe 搬運量就下降。這正是 DeepSeek V4 相對於 V3 的核心改進方向。

### 容易忽略的坑：NUMA 記憶體擺放

PCIe 頻寬是最明顯的瓶頸，但還有一個容易忽略的問題：**expert 權重放在哪顆 CPU 的記憶體上。**

我的測試機是雙 CPU（2× Xeon Gold 6548Y+），512GB RAM 分散在兩個 NUMA node 上，每顆 CPU 各管 256GB。GPU 物理上只接在其中一顆 CPU（NUMA node 0）上。

這意味著：放在 node 0 記憶體上的 expert 走的路徑是 DRAM → PCIe → GPU，直達。但放在 node 1 上的 expert 要多走一段：DRAM → UPI（CPU 間互連）→ CPU 0 → PCIe → GPU。

UPI 本身的頻寬不低（~96 GB/s），比 PCIe 5.0 的 ~64 GB/s 還寬，所以 throughput 不是問題。但每次跨 NUMA 存取會多 100-200ns 的延遲。MoE offload 的特性是每個 token 都要搬 expert，搬的次數非常頻繁——延遲的累積效果比頻寬損失更明顯。

實測發現：**讓系統把 expert 權重平均分散在兩顆 CPU 的記憶體上，效果不如集中放在 GPU 直連的那顆 CPU。** Windows 預設的記憶體分配策略是跨 NUMA node 平均分配，這在一般應用場景沒問題，但在 MoE offload 這種高頻搬運場景，平均分配反而讓一半的 expert 搬運都多走一段 UPI。

Linux 上可以用 `numactl --membind=0` 強制分配到指定 NUMA node。Windows 上控制手段有限，這也是為什麼同樣的硬體配置，Linux 跑 MoE offload 通常比 Windows 快——不只是驅動效率，還有 NUMA 記憶體策略的可控程度。

這個發現的實際意義是：**如果你的機器是雙 CPU，跑 MoE offload 之前先確認 GPU 接在哪顆 CPU 上，然後盡量把 expert 權重綁定在那顆 CPU 的記憶體上。** 這比調 llama.cpp 參數容易忽略，但對速度的影響可能比你想的大。

---

## 四、DeepSeek V3 到 V4：針對 offload 的三個架構優化

DeepSeek 的 MoE 架構從 V2 開始迭代了三代。從 offload 效率的角度看，V3 到 V4 的核心改進可以歸結為三件事，**每一件都在降低 PCIe 搬運壓力。**

![DeepSeek V4：三個維度同時降低 PCIe 搬運壓力](/assets/images/moe-offload-deepseek-v4-optimization.png)

### 4.1 激活比例持續壓低——每次搬更少

| 模型 | 總參數 | 激活參數 | 層數 | 路由專家數 | 每 token 激活 | 激活比例 |
|------|------:|--------:|----:|---------:|------------:|--------:|
| DeepSeek V3 | 671B | 37B | 61 | 256 | 8 | 5.5% |
| DeepSeek V4 Pro | 1.6T | 49B | 61 | 384 | 6 | 3.1% |
| DeepSeek V4 Flash | 284B | 13B | 43 | 256 | 6 | ~4.6% |

V4 Pro 的做法是**專家更多、每次激活更少**——從 V3 的 top-8/256 變成 top-6/384，每個 expert 的 FFN 中間層從 2,048 拉到 3,072（單個更大但激活更少）。激活比例從 5.5% 壓到 3.1%。

V4 Flash 保持 256 個路由專家但把激活數從 8 降到 6，再把整體層數從 61 砍到 43。

**對 offload 的直接影響：** 每個 token 需要從 CPU 搬到 GPU 的 expert 數量，V3 是 8 個，V4 是 6 個——少搬兩個 expert，PCIe 傳輸量直接降 25%。

### 4.2 KV Cache 壓縮——騰出 VRAM 給 expert

MoE offload 的速度取決於「多少 expert 能留在 GPU」。但 GPU VRAM 不是只放 expert——Attention 的 KV Cache 也在搶 VRAM 空間，而且隨著 context 變長，KV Cache 會越吃越大。

V3 用 MLA（Multi-head Latent Attention）把 KV Cache 壓到同級模型的 1/3 到 1/5。V4 更激進，用 CSA + HCA 雙 Attention 把 KV Cache 壓到 V3.2 的 7%（V4 Flash）。

詳細機制[這篇已經拆過](/deepseek-v4-million-token-csa-hca-attention/)，這裡只講跟 offload 相關的那一句話：

**KV Cache 省得越多，同樣大小的 VRAM 就能多留幾層 MoE expert 在 GPU，需要走 PCIe 的 expert 就越少，速度就越快。** V4 的 Attention 壓縮不只是為了支援百萬 token context——它同時在為 offload 場景騰 VRAM。

### 4.3 V4 Flash 的體積設計——整體更小，offload 壓力更低

V4 Flash 不只是 V4 Pro 的閹割版，它的體積設計本身就是為 offload 場景優化的。

V3 的 671B 總參數，Q8 量化後約 335GB。即使做 offload，每個 MoE 層的 expert 倉庫也很大，每次搬運的單位更重。

V4 Flash 砍到 284B，Q8 量化後約 151GB——不到 V3 的一半。同樣的 offload 策略，每層 expert 更小，PCIe 搬的量更少。而且 43 層比 V3 的 61 層少了 18 層，需要做 offload 的 MoE 層本身就更少。

**三件事疊起來看：** 激活數從 8 降到 6（少搬 25%）、KV Cache 壓到 7%（騰出 VRAM 多放 expert）、整體從 671B 砍到 284B（每層 expert 更小）。三個維度同時降低 PCIe 壓力，才有了 V4 Flash 在 offload 場景下顯著優於 V3 的速度表現。

---

## 五、實測數據：三個模型的 offload 表現

回到[那台 RTX Pro 6000 測試機](/rtx-pro-6000-tier1-local-day1-2-glm52-deepseek-v4-flash/)。三個 MoE 模型、不同的 offload 策略：

| 模型 | 總參數/激活 | 量化(大小) | Offload 策略 | 速度 | VRAM |
|------|:-:|:-:|:-:|--:|--:|
| GLM 5.2 | 753B / 40B | IQ2_M (222GB) | MoE 全放 CPU | ~9 tok/s | 23.5 GB |
| DSV4 Flash | 284B / 13B | Q8 (151GB) | MoE 全放 CPU | ~7 tok/s | 17.7 GB |
| DSV4 Flash | 284B / 13B | Q8 (151GB) | 20 層留 CPU | ~25 tok/s | 91.9 GB |

幾個觀察：

**GLM 5.2 和 DeepSeek V4 Flash 全放 CPU 的速度差不多（9 vs 7）。** 看起來矛盾——GLM 是 753B，DeepSeek 才 284B，為什麼更小的反而更慢？因為 GLM 用的是 IQ2_M（2-bit），DeepSeek 用的是 Q8（8-bit）。**在全 offload 場景下，決定速度的不是模型大小，是 PCIe 每次搬多少 byte。** Q8 的每個 expert 比 IQ2_M 大 4 倍，搬運量更多，所以反而更慢。

**留部分 MoE 在 GPU，速度直接 3.5 倍。** 從 7 到 25 tok/s，就是把 23 層 MoE 從 CPU 搬回 GPU。但代價是 VRAM 從 17.7GB 漲到 91.9GB——幾乎吃滿 96GB。

**PCIe 頻寬就是天花板。** 三個測試結果都指向同一件事：offload 場景下，模型大小和品質幾乎不影響速度，**唯一影響速度的是有多少 expert 需要走 PCIe**。這就是為什麼大 RAM 在 MoE offload 場景下不是奢侈品——512GB RAM 讓所有 expert 有地方放，然後你用 VRAM 的大小來控制「多少 expert 不用走 PCIe」。

---

## 六、n-gram 推測解碼的踩坑

測試過程中我還試了 llama.cpp 的 n-gram 推測解碼（speculative decoding），想看能不能在 offload 配置下再加速。結果是**負優化**：

| 配置 | Decode 速度 |
|------|----------:|
| Q8 部分 offload（無推測） | ~25 tok/s |
| Q8 部分 offload + n-gram | ~15 tok/s |

草稿接受率只有 37%。問題出在：推測解碼會先用小模型生成幾個候選 token，再用大模型驗證。在全 GPU 場景下這能省時間，因為驗證的計算量可以 batch。但在 offload 場景下，**每個候選 token 都要觸發一次 expert 搬運**——被拒絕的草稿 token 等於白搬了一堆 expert，CPU 上的 MoE 層多算好幾倍，速度反而掉。

教訓是：**推測解碼和 MoE offload 互相衝突。** 推測解碼假設「多算幾個 token 很便宜」，但 offload 場景下每個 token 的成本主要在 PCIe 傳輸，不是計算。多算 = 多搬 = 更慢。

---

## 七、MoE Offload 的元件分布總結

簡單講，MoE offload 就是把模型拆成「每個 token 都要用」和「大部分時候閒置」兩類，前者常駐 GPU，後者放 CPU RAM 待命：

**常駐 GPU（VRAM）：** Attention 層（Q/K/V 投影 + KV Cache）、共享專家、路由閘門。這些每個 token 都要跑，對延遲最敏感，不能離開 GPU。如果 VRAM 還有空間，盡量多留幾層 MoE expert 在 GPU——留越多，需要走 PCIe 的就越少，速度就越快。

**放 CPU（DRAM）：** 其餘的路由專家 FFN 權重。每個 token 只有 3-8% 會被 router 選中，選中時才透過 PCIe 搬到 GPU 計算。92-97% 的 expert 在任何一次推理中都是閒置的。

**速度公式：** 大致上就是 VRAM 越大 → 能留在 GPU 的 expert 層數越多 → 需要走 PCIe 搬的越少 → 越快。

---

## 八、工具鏈現況

### llama.cpp

目前最成熟的 MoE offload 方案。關鍵參數：

```bash
-ngl 999          # 所有非 MoE 層推 GPU
--n-cpu-moe N     # 前 N 個 MoE 層放 CPU（999 = 全部）
-fa on            # Flash Attention
-t 64             # CPU 線程數（配合 CPU expert 計算）
--cache-type-k q8_0  # KV Cache 量化（省 VRAM 給 expert）
--cache-type-v q8_0
```

量化格式以 Unsloth 的 UD 系列最完整——Q8_K_XL、Q4_K_XL、IQ2_M 等。要注意：Unsloth 轉檔時會把 MTP（Multi-Token Prediction）層丟掉，想用原生 MTP 必須走 KTransformers。

### KTransformers

專為 MoE offload 設計。用 Marlin 量化 GPU kernel 跑 attention，用 CPU（配合 AVX-512 / AMX 指令集）跑 expert FFN。官方數字：DeepSeek R1（671B）在單張 24GB GPU + 382GB DRAM 上跑到 generation 13.6 tok/s。比 llama.cpp 全 CPU-MoE 的 7 tok/s 快將近一倍——主要贏在 CPU 端 expert 計算的指令集優化和更好的 prefetch 策略。

代價是工程門檻高：需要 WSL2 或原生 Linux、要編譯、要下載完整原始權重。

### vLLM / SGLang

目前都不支援 expert 粒度的 CPU offload。vLLM 有 RFC 在推進（GPU expert cache + LFRU eviction + CPU pinned memory），但還不是 production-ready。兩個框架的重點在多卡分散推理，不在單機 offload。

---

## 結語

MoE offload 的原理很簡單：MoE 模型 97% 的 expert 在每次推理時是閒置的，閒置的權重不需要待在貴的 GPU VRAM 上。放 CPU RAM，用到時再搬過來。

但「簡單」不代表「沒有代價」。代價就是 PCIe 頻寬——每個 token 都要透過 PCIe 搬 expert，搬多少、搬多快，直接決定了你的推理速度。

DeepSeek 從 V3 到 V4 的架構演化，看起來在做很多事（CSA、HCA、Hash Routing、MTP），但從 offload 的角度抽出來看，核心邏輯只有一條：**降低每個 token 需要走 PCIe 的資料量。** 激活更少 expert、壓更小 KV Cache 騰 VRAM、整體體積更小——三個維度都指向同一個目標。

對地端部署的實際意義是：

> **MoE offload 場景下，速度 = f(VRAM 能留多少 expert)。大 VRAM 不是為了塞下模型，是為了少搬 PCIe。**

---

## 延伸閱讀

- [單機跑得動 Tier 1 地端 Model 嗎？RTX Pro 6000 一週實驗 Day 1-2](/rtx-pro-6000-tier1-local-day1-2-glm52-deepseek-v4-flash/)
- [DeepSeek V4 把百萬 Token 上下文打到傳統 2% 成本——拆解 CSA + HCA 雙 Attention 設計](/deepseek-v4-million-token-csa-hca-attention/)
- [高盛 50 頁報告的題眼：中國模型每個 Token 只點亮 3-5% 的參數](/goldman-sachs-china-ai-moe-token-price-war-agent-coding/)
- [DeepSeek V4 3.1 那 200 字才是真正的地震——訓練棧硬體無關](/deepseek-v4-section-3-1-hardware-agnostic-earthquake/)
