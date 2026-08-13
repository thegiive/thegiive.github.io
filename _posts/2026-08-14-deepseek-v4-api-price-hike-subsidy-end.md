---
layout: post
title: "DeepSeek V4 漲價最高 12 倍——八天前我才寫過 50 倍經濟學，被打臉了"
date: 2026-08-14 09:00:00 +0800
permalink: /deepseek-v4-api-price-hike-subsidy-end/
image: /assets/images/deepseek-v4-price-hike-cover.png
description: "DeepSeek 8 月 13 日公告 V4 API 新價格，8 月 16 日生效。V4-Flash output 從 $0.28 漲到峰值 $1.32，V4-Pro cache hit 漲 12 倍。八天前我才寫過 V4 Flash 的 50 倍 cache 經濟學，現在那個 50 倍被修正成 30 倍——我被打臉了。跟 OpenAI、Anthropic 重新對照，峰值時段最便宜 API 的頭銜已經易主給 GPT-5.6 Luna。"
---

## 漲價不是突襲

8 月 13 日，DeepSeek 公告 V4 API 新價格表，[8 月 16 日 16:00 UTC 生效](https://qz.com/deepseek-api-price-increase-v4-peak-off-peak-081326)。

這不是突襲。8 月 6 日 DeepSeek 就[在 API 文件頁預告過「significant increase」](https://dataconomy.com/2026/08/06/deepseek-significant-api-price-increase-2026/)，只是沒給數字；創辦人 Jun Song 後來在 X 上補了一句：[就算漲 2 到 10 倍，還是比多數西方對手便宜](https://www.explainx.ai/blog/deepseek-api-price-increase-jun-song-august-2026)。

數字出來了，落在預告區間的上緣。單位：美元 / 每百萬 token。

| 模型 | 項目 | 舊價 | 離峰 | 峰值 | 峰值漲幅 |
|------|------|------|------|------|----------|
| V4-Flash | Input（cache hit） | $0.0028 | $0.007 | $0.014 | 5.0x |
| V4-Flash | Input（cache miss） | $0.14 | $0.22 | $0.44 | 3.1x |
| V4-Flash | Output | $0.28 | $0.66 | $1.32 | 4.7x |
| V4-Pro (0813) | Input（cache hit） | $0.003625 | $0.022 | $0.044 | **12.1x** |
| V4-Pro (0813) | Input（cache miss） | $0.435 | $0.66 | $1.32 | 3.0x |
| V4-Pro (0813) | Output | $0.87 | $1.98 | $3.96 | 4.6x |

媒體標題的「[最高漲 1,100%](https://techstartups.com/2026/08/13/deepseek-raises-v4-api-prices-by-up-to-1100-just-as-chinese-ai-startup-launches-deepseek-v4-pro/)」就是 V4-Pro cache hit 那一格：$0.003625 → $0.044，12.1 倍。

---

## 我被打臉了

八天前我才寫了 [V4 Flash 的 50 倍 cache 經濟學](https://ai-coding.wiselychen.com/deepseek-v4-flash-disk-kv-cache-50x-economics/)，核心論點是「cache hit 只要 miss 的 2%，50 倍價差，這會變成產業基準線」。

那篇的坦白說裡有一條：「$0.0028 是策略定價還是成本定價，外界無從驗證。如果是補貼換市佔，這個數字未必撐得過價格戰下一輪。」

答案來得比我預期快。

| 模型 | 舊 hit/miss 價差 | 新價差 |
|------|------------------|--------|
| V4-Flash | 50x | 31.4x |
| V4-Pro | 120x | 30x |

兩個模型不約而同收斂到 30 倍。Flash 從 50 倍降、Pro 從 120 倍降，落點一樣。這不太像行銷定價，比較像有人重新算了一次 disk cache 的真實成本結構，然後統一到同一條成本曲線。

如果這個解讀成立，那上一篇的判斷就明確了：**$0.0028 是補貼價，30 倍價差才是接近成本的數字。** 50 倍和 120 倍之間多出來的部分，是 DeepSeek 掏錢請全世界的開發者養成 prefix stability 的習慣。

我的「產業基準線」判斷還在，只是基準線不是 50 倍，是 30 倍。

---

## 跟 OpenAI、Anthropic 重新對照：最便宜的頭銜易主了

「世界最便宜 frontier API」這個頭銜過去一年沒人挑戰過。新價格生效後，這張表要重新看。Input 取 cache miss 價：

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

**峰值時段，V4-Flash 已經不是最便宜的。** Luna $0.20/$1.20 對上 Flash 峰值 $0.44/$1.32，兩項都是 Luna 便宜。「最便宜 API」的頭銜在每個工作日的 09:00-18:00 屬於 OpenAI。

離峰 Flash 仍有 output 優勢（$0.66 對 $1.20），但 input 端 $0.22 對 $0.20 已經打平。

V4-Pro 對 Terra / Sonnet 的性價比還在——峰值 $1.32/$3.96 對 Terra $2/$12，output 仍只有三分之一。Jun Song 說的「漲完還是便宜」在 Pro 這一級成立，在 Flash 這一級已經不成立。

依舊便宜，但以前那種「便宜到不用比」的斬殺線不見了。現在需要拿計算機出來算了，這就是變化本身。

---

## 分時定價：token 正式變成電力

這次更值得注意的其實不是漲幅，是計價結構：AI API 第一次出現主流廠商的 peak / off-peak 分時定價。

峰時 = 週一到週五 01:00-04:00 與 06:00-10:00 UTC，換算就是北京/台灣時間 **09:00-12:00 和 14:00-18:00**——上班時間全程在內，峰時價格是離峰的兩倍。

台電的時間電價就是這樣運作的：尖峰時段電網容量吃緊，用價格把負載趕去離峰。DeepSeek 把同一套邏輯搬到 GPU 上。這個信號比漲價本身重要，因為它說明漲價的原因不是「想多賺」，而是容量不夠。想多賺的廠商直接調單價；容量不夠的廠商才需要分時配給。

token 正式變成 utility。跟水電一樣，用多少、什麼時候用，都會影響帳單。

---

## 坦白說

- 峰值 12 倍只發生在 V4-Pro cache hit 那一格。多數 Agent 工作負載的實際帳單漲幅落在 2 到 3 倍之間。
- 「30 倍 = 成本定價」是我的推論，不是 DeepSeek 的說法。也可能只是定價團隊選了個整齊的數字。
- Luna 和 V4-Flash 的價格對照不等於能力對照。DeepSeek 的 disk cache 以天計、OpenAI 的 cache 壽命 30 分鐘——跨 session 的 Agent 工作負載，DeepSeek 的實際有效單價可能還是更低。
- 開源權重不受影響。V4 Flash 仍是 MIT 授權，自架成本跟這次漲價無關。

---

## 關鍵洞察

1. **看漲價要看結構，不是看倍數。** cache hit 漲 5-12 倍、miss 只漲 3 倍、價差統一收斂到 30 倍——被修正的是補貼，不是全面提價。
2. **峰值時段最便宜的 API 是 GPT-5.6 Luna，不再是 V4-Flash。** 但離峰 Flash 的 output 仍有一半價差優勢。「用哪個模型」之外，現在多了一題「什麼時候跑」。
3. **分時定價是容量信號，不是貪婪信號。** batch 工作搬到離峰（台灣時間 18:00 後），帳單直接砍半。

---

## 延伸閱讀

- [DeepSeek raises V4 API prices by up to 1,100%（Tech Startups）](https://techstartups.com/2026/08/13/deepseek-raises-v4-api-prices-by-up-to-1100-just-as-chinese-ai-startup-launches-deepseek-v4-pro/)
- [DeepSeek raising API prices starting Aug. 16（Quartz）](https://qz.com/deepseek-api-price-increase-v4-peak-off-peak-081326)
- [8/6 漲價預告（Dataconomy）](https://dataconomy.com/2026/08/06/deepseek-significant-api-price-increase-2026/)
- [GPT-5.6 Sol / Terra / Luna 定價（Finout）](https://www.finout.io/blog/gpt-5.6-pricing-2026-sol-terra-and-luna-tiers-explained)
- [Anthropic 官方定價](https://platform.claude.com/docs/en/pricing)
- [DeepSeek V4 Flash 的 50 倍 cache 經濟學（本 blog）](https://ai-coding.wiselychen.com/deepseek-v4-flash-disk-kv-cache-50x-economics/) — 這次被修正的那篇
