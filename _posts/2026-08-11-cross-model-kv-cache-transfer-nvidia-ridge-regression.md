---
layout: post
title: "切模型就要重算 KV cache？NVIDIA 用一條線性映射省掉 re-prefill"
date: 2026-08-11 09:00:00 +0800
permalink: /cross-model-kv-cache-transfer-nvidia-ridge-regression/
image: /assets/images/cross-model-kv-cache-transfer-cover.png
description: "LLM 推理中，KV cache 是最大的成本槓桿之一——Anthropic 的 prompt caching 讓 cache hit 只收原價 10%，DeepSeek V4 Flash 把價差拉到 50 倍。但這些省下來的錢有一個隱藏前提：你不能換模型。一旦從 14B 切到 32B，整份 KV cache 作廢，全部重算。NVIDIA 九人團隊發現同家族模型的 KV 表徵之間存在強線性結構，用 closed-form ridge regression 就能把一個模型的 cache 映射到另一個，速度比重算快 2.7-25 倍，四組模型對保留 73-98% 的原始準確度。"
---

LLM API 是無狀態的。每一輪對話，你的 harness 把整段歷史重新送進模型，模型從頭讀完才開始生成下一個 token，讀的部分全部計費為 input。

Prompt caching 的發明就是為了解這個問題：provider 把穩定 prefix 的 KV cache 留著，下次命中就不用重算，只收原價的一成。Anthropic 收 10%，DeepSeek V4 Flash 更狠，[cache hit 只收 miss 的 2%，價差 50 倍](https://ai-coding.wiselychen.com/deepseek-v4-flash-disk-kv-cache-50x-economics/)。

但所有的 prompt caching 都有一個隱含前提：**cache 只對產生它的那個模型有效。**

Key 和 Value 是從那個模型的權重算出來的，換一個模型就讀不懂。切模型的那一刻，整份 KV cache 作廢，context 從頭重算，帳單重新歸零。

在 model routing 場景——簡單請求走小模型省錢、難的升級大模型保品質——這意味著每次 upgrade 都要付一次 re-prefill 的全額帳單。如果 context 有 32K tokens，大模型的 prefill 要好幾秒。latency spike 加上成本歸零，讓很多團隊在實務上放棄 routing，乾脆只用一個模型。

NVIDIA 九人團隊（Heo et al., 2026-08-04, [arXiv 2608.03893](https://arxiv.org/abs/2608.03893)）問了一個直接的問題：**KV cache 能不能從一個模型「翻譯」給同家族的另一個模型？**

---

## 30 秒定位

| 項目 | 數字 |
|------|------|
| 論文 | Cross-Model KV Cache Transfer in LLM Families |
| 團隊 | NVIDIA（9 位作者，第一作者 Taekyung Heo） |
| 方法 | Closed-form ridge regression，per-head 獨立映射 |
| 校準資料 | 500 條 FineWeb-Edu 序列，每條 1,024 tokens |
| 測試範圍 | 6 組模型對，橫跨 Qwen3 / Llama 3.1 / Ministral 3 三個家族 |
| Accuracy 保留 | 4 組保留 73-98%，2 組退化嚴重（~42%） |
| 速度 | 比 re-prefill 快 2.7-25 倍 |
| Mapper 大小 | 1.01-3.36B 參數（4-12 GB） |

---

## 為什麼 KV 能被「翻譯」——線性結構的發現

Prefill 的唯一產出就是 KV cache。所以要把 cache 從一個模型搬到另一個，本質上是個表徵轉換問題：把 source 模型的 KV 空間映射到 target 模型的 KV 空間。

研究者先檢查這個映射有沒有可利用的結構。

他們對 Qwen3 14B → 32B 做了最基本的測試：拿 source 的單一層做 target 單一層的線性迴歸。結果：**keys 的方差解釋量 56%，values 32%。** 對一個只有一層對一層的線性擬合來說，這個數字出乎意料地高——代表兩個不同大小的模型，雖然層數不同、權重不同，但 KV 的表徵空間有相當程度的共享結構。

但 56% 不夠用。14B 有 40 層，32B 有 64 層，沒有天然的一對一配對。研究者的做法是：對每一個 target 層，把所有 source 層按 R^2 排名，選前 k 個拼接起來一起做迴歸。

用 8 層 source 拼接之後：**keys 的方差解釋量從 56% 升到 79%，values 從 32% 升到 65%。**

這個跳升說明：target 的每一層不只是從 source 的「對應位置」抽資訊，而是從多個不同深度的 source 層組合出自己需要的表徵。消融實驗也證實了這一點——cross-layer selection 是三個設計中貢獻最大的，拿掉它（k 從 8 降到 1），HellaSwag 從 80.70 掉到 44.81。

---

## Mapper 的三個零件

整個映射器由三個零件組成，每一個都可以獨立理解：

**零件一：Cross-layer source selection。** 每個 target 層獨立選擇自己的 top-k source 層，依據是 head-averaged R^2。Qwen3 14B → 32B 用 k=8，Llama 3.1 8B → 70B 用 k=20（層數差距大，需要更多 source 層）。選完之後把這些 source 層的 KV 拼接成一個大矩陣，當作迴歸的輸入。

**零件二：RoPE 剝離。** Keys 裡帶了 RoPE（Rotary Position Embedding）的位置旋轉。如果不處理，mapper 學到的就是「在位置 t 的映射」，換個位置或換個 context 長度就不準。做法：先把 source keys 的 RoPE 反旋轉掉，在無位置的空間裡做迴歸，推理時再套上 target 模型的 RoPE。這讓 mapper 對 context 長度不敏感——校準用 1,024 tokens，推理時可以跑更長。

**零件三：Per-head ridge regression。** 每個 attention head 獨立解一個 closed-form 的 ridge regression：

W* = (X^T X + lambda I)^{-1} X^T Y

沒有梯度下降，沒有迭代，一步解出。lambda = 0.01。校準只需要 500 條 FineWeb-Edu 序列（stride-4 subsampled），在一台 8xH100 上跑 47-87 分鐘就能 fit 完一組模型對。

用搬家打個比方：你從小公寓（14B）搬到大房子（32B），家具的風格其實一致（同家族），但房間數不同、格局不同。cross-layer selection 是「把舊公寓三個房間的東西拼到新房子的客廳裡」；RoPE 剝離是「先把家具上的地址標籤撕掉，搬到新地址再貼新標籤」；ridge regression 是「量好尺寸，算出每件家具要縮放多少才放得進新空間」。

---

## 六組模型對：四組成功，兩組翻車

| 家族 | 模型對 | k | Avg Retention | HellaSwag | 等級 |
|------|--------|---|---------------|-----------|------|
| Qwen3 | 14B → 32B | 8 | 97.6% | 97.6% | Tier 1 |
| Qwen3 | 8B → 32B | 12 | 87.5% | 95.2% | Tier 1 |
| Llama 3.1 | 8B → 70B | 20 | 72.8% | 90.9% | Tier 1 |
| Ministral 3 | 3B → 8B | all | 76.2% | 93.3% | Tier 1 |
| Ministral 3 | 3B → 14B | 20 | 44.2% | 68.0% | Tier 2 |
| Ministral 3 | 8B → 14B | 12 | 41.6% | 58.7% | Tier 2 |

Tier 1 的四組，accuracy retention 在 73-98%。Qwen3 14B → 32B 最好：97.6% retention，幾乎跟大模型自己 prefill 一樣。Llama 3.1 8B → 70B 稍差（72.8%），但 HellaSwag 仍有 90.9%。

Tier 2 的兩組是 Ministral 家族的跨尺寸轉移，retention 掉到 42-44%，線性映射明顯不夠用。論文用 nonlinear MLP 當 fallback，在最差的那組回收了 +37 pp HellaSwag retention——但代價是 mapper 變大、不再 closed-form。

速度方面，以 Qwen3 14B ↔ 32B 為例：

| Context 長度 | 小→大 加速倍數 | 大→小 加速倍數 |
|-------------|---------------|---------------|
| 64 tokens | 4x | 3x |
| 8,192 tokens | 17x | 5x |
| 32,768 tokens | 25x | 7x |

Context 越長，省得越多——因為 mapper 的計算量是固定的，而 re-prefill 跟 context 長度線性成長。

---

## Multi-turn 會不會越飄越遠？

真實對話不是單次 prefill。如果每一輪都累積 mapper 的誤差，十輪之後會不會完全走樣？

論文在 CoQA（100 段對話，每段約 15 輪，橫跨五個領域）上測了 Qwen3 14B ↔ 32B：

- 小→大方向，10 輪之後 gap 只擴大 1.7 pp，基本穩定
- 大→小方向，drift 以每輪 0.33 pp 線性成長

大→小的累積確實是個問題——如果跑 30 輪，drift 就接近 10 pp。但實務上大→小的場景（從大模型降級回小模型）通常發生在確認任務簡單之後，不太會跑很多輪。

---

## 跟既有研究的位置關係

Cross-model KV reuse 不是全新的概念。之前的做法要嘛訓練一個 neural adapter（per pair，等於多訓練一次），要嘛要求兩個模型架構完全一致。

這篇的特殊之處在於：**closed-form + training-free。** 一個矩陣運算解出 mapper，不需要梯度下降，不需要 GPU 做 training iteration。47-87 分鐘的校準時間本質上是在做資料收集和矩陣分解，不是在訓練模型。

但 closed-form 的代價也清楚：它只能抓線性關係。模型對之間如果有非線性的表徵差異（Ministral 3B → 14B），線性 mapper 就會翻車，必須 fallback 到 MLP。

---

## 跟 DeepSeek V4 Flash 的 KV cache 經濟學合在一起看

我在兩週前寫的 [DeepSeek V4 Flash 那篇](https://ai-coding.wiselychen.com/deepseek-v4-flash-disk-kv-cache-50x-economics/)，核心論點是：**當 cache hit 價差拉到 50 倍，帳單跟 miss rate 走，不跟 token 數走。** 所以 prefix stability 是成本工程的核心。

那篇有一個沒講的隱含假設：你只用一個模型。

這篇論文揭示了第二層問題。即使你的 prefix 設計完美、hit rate 拉到 99%，**只要 routing 決定切模型，cache 整個作廢，miss rate 瞬間跳回 100%。** 前面累積的所有 cache 投資，一筆歸零。

兩個問題合在一起才是完整的 KV cache 成本工程圖像：

1. **同模型內的 cache 效率** → prefix stability，DeepSeek 那篇的主題
2. **跨模型的 cache 存續** → KV transfer，這篇論文的主題

如果 NVIDIA 這套方法成熟到可以上線，model routing 的成本模型會根本性改變：切模型不再是「重來」，而是「翻譯」。routing 的成本從 O(context_length) 的 re-prefill 降到 O(mapper) 的矩陣乘法。

---

## 坦白說

這篇論文是早期研究，離上線還有很多限制要正視。

**只在同家族內測過。** 六組模型對全部是 Qwen → Qwen、Llama → Llama、Ministral → Ministral。跨家族轉移（例如 Qwen → Llama）論文明確列為 future work。這不奇怪——不同家族的預訓練資料、tokenizer、架構設計差異大，線性結構可能根本不存在。

**六組裡有兩組翻車。** Ministral 3B → 14B 和 8B → 14B 的 retention 只有 42-44%，ridge regression 的 R^2 在某些 token 上是負數（-7.81 和 -3.22，比隨機猜還差）。雖然 MLP 可以回收一部分，但這代表 closed-form 的優雅不是普遍適用的——你必須先驗證你的模型對是 Tier 1 還是 Tier 2。

**所有模型對碰巧 KV head count 和 per-head dimension 都一樣。** 也就是說，source 和 target 的 KV 形狀完全相同，mapper 只做空間內的旋轉和縮放，不需要處理維度不匹配。如果 head count 不同（例如跨代模型改了 GQA 的 group 數），mapper 的設計會變得更複雜，目前未測。

**校準只用了單一領域。** 500 條 FineWeb-Edu（教育類文本），換成 code 或其他領域時，CodeAlpaca 上 HellaSwag 掉了 5.24 pp。

**Mapper 本身不小。** 1.01-3.36B 參數、4-12 GB 儲存。在 GPU-rich 的雲端環境這不是問題，但如果你在考慮端側或小叢集部署，這筆額外開銷要算進去。

但這篇做對了一件事：**它證明了 KV 表徵在同家族模型之間的線性結構確實存在，而且強到足以用 closed-form 解法做有意義的轉移。** 這個發現本身——不管最終上線的方案是 ridge、MLP、還是別的什麼——打開了 KV cache 跨模型複用這整條路。

---

## 關鍵洞察

1. **KV cache 的成本工程有兩層。** 第一層是同模型的 cache hit rate（prefix stability），第二層是跨模型的 cache 存續（KV transfer）。只解第一層，model routing 一啟動就全部歸零。

2. **Cross-layer selection 是最大的槓桿。** 消融實驗很清楚：不是「14B 第 10 層對應 32B 第 16 層」這種直覺映射，而是每個 target 層從多個 source 層組合資訊。理解這個結構，才能理解為什麼簡單的層對層 copy 不 work。

3. **線性映射 work 的邊界要先測。** 六組裡兩組翻車（Tier 2），而且翻車的規律不是「尺寸差太多」——Llama 8B → 70B（8.75 倍）反而是 Tier 1，Ministral 8B → 14B（1.75 倍）卻是 Tier 2。模型對能不能用，必須實測 R^2，不能靠直覺推斷。

4. **如果你在做 model routing，現在就值得關注這個方向。** 不一定要等這篇的方法上線。核心的 insight 是：routing 的成本不只是兩個模型的單價差，還有切換時 KV cache 報廢的隱藏稅。現在設計 routing 策略時，把 cache invalidation cost 算進去，比等一個銀子彈更實際。
