---
title: "CAISI 說 DeepSeek V4 落後 8 個月——但你看錯重點了：跑分輸掉、方向贏了"
date: 2026-05-04 14:00:00 +0800
permalink: /caisi-deepseek-v4-eight-month-gap-debate/
description: "美國 NIST 旗下的 CAISI 在 2026/5 發布報告：DeepSeek V4 Pro 落後美國 frontier 約 8 個月，DeepSeek 自己 paper 講的是 3 個月。兩邊都對，但都看錯重點——DeepSeek V4 真正贏的不是跑分，是 Vendor Agnostic（NVIDIA / 華為隨時抽換）+ KV Cache 降 7-10%，直接突破老黄的 HBM 供應鏈鎖喉。完整論述在 YouTube 影片，這篇文章只放關鍵論點跟 source。"
---

# CAISI 說 DeepSeek V4 落後 8 個月——但你看錯重點了：跑分輸掉、方向贏了

[![YouTube Preview](https://img.youtube.com/vi/JViBJYx3WKw/maxresdefault.jpg)](https://youtu.be/JViBJYx3WKw)

> 完整 15 分鐘論述在上面影片，這篇文章只放關鍵論點。

## 兩個數字、一個誤會

2026/5/3，美國 NIST 旗下的 [CAISI（Center for AI Standards and Innovation）](https://www.nist.gov/news-events/news/2026/05/caisi-evaluation-deepseek-v4-pro) 發布對 DeepSeek V4 Pro 的官方評估，結論一句話：

> **「DeepSeek V4 Pro 是目前最強的中國模型，但能力落後美國 frontier 約 8 個月。」**

[DeepSeek 自己的 V4 paper](https://techcrunch.com/2026/04/24/deepseek-previews-new-ai-model-that-closes-the-gap-with-frontier-models/) 講的是另一個故事：**「我們落後 frontier 大約 3 個月。」**

兩邊差了一倍多。網路上會吵半年「誰對」。

但其實**兩邊都對，也都看錯了重點**。

差距怎麼算的差別在於：CAISI 用 holdout benchmark（DeepSeek 沒看過的題目），DeepSeek 用公開 benchmark 自評（公開題目可能在訓練時被 fine-tune）。**這就是為什麼自評 90% 在 CAISI holdout 變成 44%。**

## 但「跑分差幾個月」根本不是 DeepSeek V4 的重點

DeepSeek V4 跑分確實不 SOTA。在某些 benchmark 上甚至輸給 GLM 5.1。

如果你只看 leaderboard，DeepSeek 這次發表是個 disappointment——尤其在他們今年內部還流失了像羅福莉這種核心人才、需要對外募資的背景下。

但你打開 [DeepSeek V4 的 technical paper](https://simonwillison.net/2026/apr/24/deepseek-v4/) 看實際的工程貢獻，會發現他們真正在解決的是另一個層級的問題：**怎麼在老黄的 HBM 供應鏈封鎖下，繼續做出可規模化部署的模型。**

兩個關鍵突破：

**1. Vendor Agnostic — 訓練 / 推理可隨時抽換 NVIDIA / 華為**

這件事在 IT 界做過 infra 的人都知道有多難。同一個模型在不同硬體 vendor 之間切換，從 kernel 到 framework 到 numerical precision 全部要重新調，效能掉個 30% 是常態。

DeepSeek V4 做到「這次跑 NVIDIA、下次跑華為，自由切換」——他們為了這件事在 V3 跟 V3.2 之間吃了非常多虧、training 拉得很長、效果也沒到很好。但 V4 真的做出來了。**這是這次發表最重要的工程成就，比跑分重要 10 倍。**

**2. KV Cache 降 7-10%（CSA + HCA 注意力機制）**

百萬 context 的故事大家去年聽過了，但學術上一直被詬病「不是真的百萬 context」——training 主體是 200K，最後幾步硬撐到 1M，加上 [Lost in the Middle](https://arxiv.org/abs/2307.03172) 問題沒解。

DeepSeek V4 用 [CSA + HCA](/deepseek-v4-million-token-csa-hca-attention/)（我之前寫過深度解析）這套機制，在做 long context 推理時 KV Cache 比 V3.2 降 7-10%。

聽起來不多？算下來在 production 場景就是**HBM 需求直接打 9 折**。

## 為什麼這兩件事比跑分重要 10 倍

回到 [我之前那篇 DDR/HBM Token 經濟學的文章](/ddr-hbm-token-economics-nvidia-lock-supply-chain/)。當時的核心結論：

- **128GB DDR5 一年漲 3 倍，HBM 把記憶體廠產能整個吃掉**
- **老黄鎖住 2026/27/28 大量 HBM 產能**——其他人連排隊都很難
- **突破這個封鎖只有兩條路：硬體多 vendor、軟體算法壓縮**

DeepSeek V4 同時走了這兩條路。

**反觀 Anthropic：** 同樣的時間點 [Opus 4.6 / 4.7 的「降智」抱怨](https://www.mindstudio.ai/blog/claude-opus-4-7-review)，業界普遍解讀就是缺算力——理論上有最強的模型，但 serving capacity 跟不上需求。如果老黄的 HBM 封鎖再持續兩三年，這件事會越來越嚴重。

**目前真正走通供應鏈突破路徑的，全世界只有兩家：DeepSeek 跟 Google（TPU 自研 + [TurboQuant 軟體優化](https://arxiv.org/abs/2510.16064)）。** GLM 算第二梯隊（適配華為，但還沒到 vendor agnostic）。

OpenAI 的策略是「圈錢圈算力」，這條路在資本市場仍能走，但成本越走越高。

## 對你的實際意義

CAISI 報告會被媒體大肆引用「中國落後 8 個月」，這個 framing 服務 chip export control 的政策論述。但對企業選型，這個敘事是 mislead 的。

實際上你該問的問題是：

- **「我能不能取得算力？」**比「誰跑分高 3 分」重要
- **「Token 單價未來會漲還是跌？」**比「現在最強是誰」重要
- **「open weight 能不能 self-host 在我可控的硬體上？」**比「閉源 vs 開源」重要

完整論述跟我對梁文鋒的觀察、Anthropic 缺算力的細節、Token 漲價趨勢——**都在 YouTube 影片裡**：

👉 **[YouTube 完整影片](https://youtu.be/JViBJYx3WKw)**

---

## Source

- [NIST CAISI 官方報告（2026/5）](https://www.nist.gov/news-events/news/2026/05/caisi-evaluation-deepseek-v4-pro)
- [DeepSeek V4 paper / TechCrunch 報導](https://techcrunch.com/2026/04/24/deepseek-previews-new-ai-model-that-closes-the-gap-with-frontier-models/)
- [Simon Willison — DeepSeek V4 評測](https://simonwillison.net/2026/apr/24/deepseek-v4/)
- [The Decoder — 對 CAISI framing 的批判視角](https://the-decoder.com/china-is-falling-behind-in-the-ai-race-according-to-a-us-government-benchmark/)
- [Council on Foreign Relations — 地緣政治分析](https://www.cfr.org/articles/deepseek-v4-signals-a-new-phase-in-the-u-s-china-ai-rivalry)

## 站內相關（這篇文章接續的論述脈絡）

- [一張原價屋估價單看懂 Token 經濟學跟老黄供應鏈鎖喉](/ddr-hbm-token-economics-nvidia-lock-supply-chain/)
- [DeepSeek V4 Million Token CSA / HCA Attention 技術解析](/deepseek-v4-million-token-csa-hca-attention/)
- [非英語稅：你用 Claude 寫中文比美國人貴 71%](/non-english-tax-tokenizer-cost-claude-openai/)
- [中國 Token 出口：賣 intelligence 的新貿易模式](/china-token-export-new-trade-model-selling-intelligence/)
