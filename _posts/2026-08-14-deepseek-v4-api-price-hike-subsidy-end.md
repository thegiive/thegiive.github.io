---
layout: post
title: "昨天 5090 大漲價，今天 DeepSeek 大漲價——雲地混合做對沖可能是王道"
date: 2026-08-14 09:00:00 +0800
permalink: /deepseek-v4-api-price-hike-subsidy-end/
image: /assets/images/deepseek-v4-price-hike-cover.png
description: "DeepSeek 8 月 13 日公告 V4 API 新價格，8 月 16 日生效，大致三倍漲價，同時引入 peak / off-peak 分時定價。八天前我才寫過 V4 Flash 的 50 倍 cache 經濟學，現在那個 50 倍被修正成 30 倍。跟 OpenAI 重新對照，峰值時段最便宜 API 的頭銜已經易主給 GPT-5.6 Luna。昨天硬體漲、今天 API 漲，AI 時代的通膨來了——但兩邊的漲法不一樣，雲地混合做對沖可能才是最佳解。"
---

八天前我寫了一篇 [V4 Flash 的 50 倍 cache 經濟學](https://ai-coding.wiselychen.com/deepseek-v4-flash-disk-kv-cache-50x-economics/)，核心論點是「cache hit 只要 miss 的 2%，50 倍價差會變成產業基準線」。

發布當天，DeepSeek 就公告可能會大漲價。

今天 DeepSeek 如約而至，打我臉了。

8 月 13 日 DeepSeek 公告 V4 API [新價格](https://qz.com/deepseek-api-price-increase-v4-peak-off-peak-081326)，[8 月 16 日生效](https://techstartups.com/2026/08/13/deepseek-raises-v4-api-prices-by-up-to-1100-just-as-chinese-ai-startup-launches-deepseek-v4-pro/)，大致上是三倍漲價，同時引入 peak / off-peak 分時定價。這不是突襲——8 月 6 日就[在 API 文件頁預告過「significant increase」](https://dataconomy.com/2026/08/06/deepseek-significant-api-price-increase-2026/)，只是沒給數字。

---

## 漲多少

單位：美元 / 每百萬 token。

| 模型 | 項目 | 舊價 | 離峰 | 峰值 | 峰值漲幅 |
|------|------|------|------|------|----------|
| V4-Flash | Input（cache hit） | $0.0028 | $0.007 | $0.014 | 5.0x |
| V4-Flash | Input（cache miss） | $0.14 | $0.22 | $0.44 | 3.1x |
| V4-Flash | Output | $0.28 | $0.66 | $1.32 | 4.7x |
| V4-Pro (0813) | Input（cache hit） | $0.003625 | $0.022 | $0.044 | **12.1x** |
| V4-Pro (0813) | Input（cache miss） | $0.435 | $0.66 | $1.32 | 3.0x |
| V4-Pro (0813) | Output | $0.87 | $1.98 | $3.96 | 4.6x |

漲最兇的不是 output，是 cache hit——也就是我上一篇說「接近免費」的那一格。媒體標題的「[最高漲 1,100%](https://techstartups.com/2026/08/13/deepseek-raises-v4-api-prices-by-up-to-1100-just-as-chinese-ai-startup-launches-deepseek-v4-pro/)」就是 V4-Pro cache hit：$0.003625 → $0.044，12.1 倍。但多數 workload 的實際帳單漲幅落在 3 倍左右。

主要是 hit/miss 價差收斂：

| 模型 | 舊 hit/miss 價差 | 新價差 |
|------|------------------|--------|
| V4-Flash | 50x | 31.4x |
| V4-Pro | 120x | 30x |

兩個模型不約而同收斂到 30 倍。Flash 從 50 倍降、Pro 從 120 倍降，落點一樣。比較像有人重新算了一次 disk cache 的真實成本，然後統一到同一條成本曲線上。

Cache hit / miss 基準線還在，只是不是 50 倍，是 30 倍。

---

## 最便宜的 LLM 頭銜易主了

「世界最便宜 frontier API」這個頭銜過去一年沒人挑戰過。新價格生效後，跟 OpenAI 比，Luna 第一次在性價比贏了。Input 取 cache miss 價：

| 模型 | Input | Output | 備註 |
|------|-------|--------|------|
| GPT-5.6 Luna | $0.20 | $1.20 | 7/30 降價後 |
| V4-Flash（離峰） | $0.22 | $0.66 | |
| V4-Flash（峰值） | $0.44 | $1.32 | 北京/台灣上班時間 |
| V4-Pro（離峰） | $0.66 | $1.98 | |
| Claude Haiku 4.5 | $1.00 | $5.00 | |
| V4-Pro（峰值） | $1.32 | $3.96 | |
| GPT-5.6 Terra | $2.00 | $12.00 | |
| Claude Sonnet 5 | $3.00 | $15.00 | 8/31 前優惠 $2/$10 |
| Claude Opus 5 | $5.00 | $25.00 | |
| GPT-5.6 Sol | $5.00 | $30.00 | |
| Claude Fable 5 | $10.00 | $50.00 | |

（Anthropic 價格取自 [platform.claude.com](https://platform.claude.com/docs/en/pricing)；OpenAI 取自 [GPT-5.6 定價說明](https://www.layer3labs.io/guides/gpt-5-6-pricing)。）

峰值時段 Luna $0.20/$1.20 對上 Flash $0.44/$1.32，兩項都是 Luna 便宜。「最便宜 frontier API」的頭銜在每個工作日的 09:00-18:00 屬於 OpenAI。離峰 Flash output 還有優勢（$0.66 對 $1.20）。

總體來說 DeepSeek 依舊便宜，但以前那種「便宜到不用比」的斬殺線不見了。現在是美系就選 OpenAI Luna，中系就選 DeepSeek V4 Flash。

---

## 類似電力的計價結構

這次更值得注意的其實不是漲幅，是計價結構。主流 AI API 第一次出現像電力的 peak / off-peak 分時定價。

峰時 = 北京/台灣時間 09:00-12:00 和 14:00-18:00，上班時間全程在內。峰時價格是離峰的兩倍——電價就是這樣運作的，DeepSeek 把同一套邏輯搬到 LLM 上。

這是不是也暗示 DeepSeek 成本結構中，電力佔一個重要的比例呢。

OpenAI 沒有 peak / off-peak 分時定價，但有概念類似的機制：Batch API 非同步 24 小時內完成、input/output 打 5 折；Flex tier 更低價但速度慢、尖峰時段可能排不到資源。方向一樣——把不急的工作往便宜的通道擠。

---

## 雲地混合做對沖

昨天寫 [5090 三個月從 10 萬變 17 萬](https://ai-coding.wiselychen.com/memory-price-surge-local-ai-five-paths/)，今天寫 DeepSeek API 便宜到不用算的時代結束了。

硬體漲，API 也漲。我們是不是正在經歷一場 AI 時代的通貨膨脹。

但仔細想想，兩邊的漲法不一樣。

硬體漲了，但保值率跟著高。一張 5090 放三個月不但沒折舊還增值 70%。AI 算力快要變期貨了。

API 漲了，但多了分時定價。離峰砍半，batch 搬到半夜跑，帳單可以精算。另外雲端依舊死死卡著能力的天花板。

所以也許答案從頭到尾都不是二選一。雲地混合做對沖，或許是最佳方案：

1. **合理的節奏購入地端硬體**，吃穩定的推理量。購入額外硬體後將部分雲端 budget 導入地端。
2. **雲端吃彈性需求**，精算時段和 hit rate。

有點像以前 AWS 的 OnDemand + Spot Instance 配法。一開始雲 90% + 地 10%，慢慢走向雲地各半。

硬體雖然貴，但這幾年超級保值——看看一張 5090 放三個月不但沒折舊還增值 70%。

如果硬體上漲，雲端 API 會上調，這時候地端持有的硬體也跟著增值。如果硬體下跌，雲端 API 也會下調，這時候再調更多 workload 到雲即可。兩邊的成本互相 hedge 對沖。

---

## 坦白說

- 峰值 12 倍只發生在 V4-Pro cache hit 那一格。多數 Agent 工作負載的實際帳單漲幅落在 2 到 3 倍之間。
- 「30 倍 = 成本定價」是我的推論，不是 DeepSeek 的說法。也可能只是定價團隊選了個整齊的數字。
- Luna 和 V4-Flash 的價格對照不等於能力對照。DeepSeek 的 disk cache 以天計、OpenAI 的 cache 壽命 30 分鐘——跨 session 的 Agent 工作負載，DeepSeek 的實際有效單價可能還是更低。
- 開源權重不受影響。V4 Flash 仍是 MIT 授權，自架成本跟這次漲價無關。

---

## 關鍵洞察

1. **看漲價要看結構，不是看倍數。** cache hit 漲 5-12 倍、miss 只漲 3 倍、價差統一收斂到 30 倍——被修正的是補貼，不是全面提價。
2. **斬殺線消失了。** 峰值時段最便宜的 API 是 GPT-5.6 Luna，不再是 V4-Flash。「用哪個模型」之外，現在多了一題「什麼時候跑」。
3. **分時定價是容量信號。** token 正式變成 utility，跟電力一樣按時段計價。
4. **雲地混合做對沖，可能才是這波 AI 通膨的最佳解。** 地端吃穩定量、雲端吃彈性，硬體漲跌和 API 漲跌互相 hedge。

---

## 延伸閱讀

- [DeepSeek raises V4 API prices by up to 1,100%（Tech Startups）](https://techstartups.com/2026/08/13/deepseek-raises-v4-api-prices-by-up-to-1100-just-as-chinese-ai-startup-launches-deepseek-v4-pro/)
- [DeepSeek raising API prices starting Aug. 16（Quartz）](https://qz.com/deepseek-api-price-increase-v4-peak-off-peak-081326)
- [8/6 漲價預告（Dataconomy）](https://dataconomy.com/2026/08/06/deepseek-significant-api-price-increase-2026/)
- [GPT-5.6 Sol / Terra / Luna 定價（Finout）](https://www.finout.io/blog/gpt-5.6-pricing-2026-sol-terra-and-luna-tiers-explained)
- [Anthropic 官方定價](https://platform.claude.com/docs/en/pricing)
- [5090 三個月從 10 萬變 17 萬：五條技術路徑壓低地端 AI 的硬體門檻（本 blog）](https://ai-coding.wiselychen.com/memory-price-surge-local-ai-five-paths/) — 昨天的硬體漲價文
- [DeepSeek V4 Flash 的 50 倍 cache 經濟學（本 blog）](https://ai-coding.wiselychen.com/deepseek-v4-flash-disk-kv-cache-50x-economics/) — 這次被修正的那篇
