---
layout: post
title: "北京一家酒吧免費請你用 DeepSeek V4 Flash：兩台地端 DGX Spark，token 無限量"
date: 2026-08-03 09:00:00 +0800
permalink: /agi-bar-free-token-dgx-spark-inference-infrastructure/
description: "北京中關村創業大街的 AGI Bar（知識蒸餾），從 8 月起對店內消費的客人提供免費無限量 DeepSeek V4 Flash API token。不用註冊、不用訂閱，連上店內 WiFi，填 Base URL 和 API Key 到 Claude Code、Cursor 或任何 OpenAI API 相容客戶端，就能直接用。所有推理都在店內的 NVIDIA DGX Spark 上跑，不走雲端。一台 DGX Spark 售價 $4,699、重 1.2 公斤，跑 284B 參數的 V4 Flash 能達到 15-20 t/s。這篇拆解一件事：當硬體成本一次性、邊際 token 成本趨近於零，AI 推理的分發邏輯會怎麼變。"
image: /assets/images/agi-bar-dgx-spark-free-token-cover.png
categories: [AI 產業分析]
author: Wisely Chen
---

北京中關村創業大街上有一家叫「知識蒸餾」的酒吧，英文名 AGI Bar，2025 年 6 月開業。白天是 AI 產品展示空間，晚上是酒吧。Midjourney 創辦人 David Holz 來中國時在 X 上貼過這裡的照片，配文 ["Meanwhile in China"](https://m.huxiu.com/article/4819513.html)。

8 月 3 日，[X 帳號 @MaxForAI（赛博禅心）發了一則貼文](https://x.com/MaxForAI/status/2083907939811922105)：AGI Bar 從今天起，對店內消費的客人提供免費、無限量的 DeepSeek V4 Flash API token。

使用方法：進店，連上 WiFi，拿到 Base URL 和 API Key，填到 Claude Code、Cursor、Cherry Studio 或任何 OpenAI API 相容客戶端。不用註冊，不用訂閱，不用付 token 費用。

所有推理都在店內的 NVIDIA DGX Spark 上跑。

---

## 先看硬體：一台 $4,699 的盒子能做什麼

[DGX Spark](https://intuitionlabs.ai/articles/nvidia-dgx-spark-review) 是 NVIDIA 2025 年推出的桌面 AI 電腦。GB10 Grace Blackwell Superchip，128GB LPDDR5x 統一記憶體，稀疏 FP4 算力約 1 PFLOP。整台機器約 15 × 15 × 5 公分，重 1.2 公斤。

[售價最初公布 $2,999，上市定價 $3,999，2026 年 2 月漲到 $4,699](https://forums.developer.nvidia.com/t/2-23-2026-price-change-announcement/361713)（NVIDIA 公告原因是全球記憶體供應吃緊）。

跑在上面的模型是 [DeepSeek V4 Flash](https://www.morphllm.com/deepseek-v4-flash)：284B 參數的 MoE 架構，每個 token 只激活 13B，2026 年 4 月發布，MIT 開源。官方 API 定價 $0.14 / $0.28 per M tokens（輸入/輸出）。

為什麼是這個模型？看一眼 [Artificial Analysis Intelligence Index v4.1](https://artificialanalysis.ai/)（2026-07-31 數據）就知道了。V4 Flash 0731 在智力指標上拿到約 50 分，每 task 成本約 $0.02。這兩個數字畫出一條斬殺線：**比它強的模型沒幾個，沒有一個比它便宜；比它便宜的，能力是斷崖式下降——同價位最接近它的，是幾個月前的 DeepSeek V4 Flash 舊版。** Claude Opus 5、GPT-5.6 Sol 這些更強的模型，每 task 成本在 $0.50-$3，貴了 25-150 倍。

換句話說，V4 Flash 是目前性價比的 Pareto 最優解。而 AGI Bar 做的事情是：把這條斬殺線上的最優模型搬到店裡，連那 $0.02 都省掉。

從推文的截圖看，店裡至少有兩台 DGX Spark。這個數字有意義：[單台 128GB 跑 V4 Flash 需要 Q2 量化（壓到 ~80GB），生成速度約 15-20 t/s](https://ai-muninn.com/en/blog/dgx-spark-deepseek-v4-flash-284b-ds4-engine)；[雙台 256GB 可以用 FP8 精度跑，41 t/s，品質損失小很多](https://flowtivity.ai/blog/deepseek-v4-flash-1m-context-dual-dgx-spark/)。

---

## 成本結構：為什麼「免費 token」不是慈善

做一個粗略的成本概算。這不是 AGI Bar 公布的數字，是根據公開硬體規格推算的：

| 項目 | 估算 |
|------|------|
| 硬體 | 2 × DGX Spark ≈ $9,400 |
| 功耗 | 每台約 300W × 2 = 600W |
| 日均電費 | 營業 12 小時 → 7.2 kWh → 約 7 元人民幣（商業電價） |
| 年電費 | 約 $360 |
| 硬體年攤（3 年） | 約 $3,130 |
| **年化總成本** | **約 $3,500** |

對比：如果同樣的推理量走 V4 Flash API，一天消耗 50M tokens（混合輸入輸出均價 $0.21/M），一天約 $10.5，一年約 $3,800。

**硬體路線大約一年回本，之後每年只花 $360 電費。**

這就是「免費 token」的經濟學：跟免費 WiFi 一樣，不是因為東西不值錢，是因為邊際成本低到可以被場域的其他收入吸收。酒吧賣一杯酒的利潤就足以覆蓋好幾個小時的推理電費。

---

## 這件事在本 blog 地端推理系列裡的位置

我兩週前寫過[借到 RTX Pro 6000 跑 GLM 5.2 和 V4 Flash 的經歷](/glm-52-single-machine-rtx-pro-6000-tier1-local/)，當時的結論是：V4 Flash 的 13B 激活參數是目前「單機 Tier 1」的性價比甜蜜點。跑得起來，速度也可用。

AGI Bar 做的事情，等於把「個人開發者在家跑地端模型」這件事，往前推了一步：**不是你自己買硬體、自己跑，而是場域替你跑好了，你帶著筆電來就行。**

這跟十年前咖啡廳提供免費 WiFi 的邏輯完全一樣。2010 年代初，能提供穩定免費 WiFi 的咖啡廳是差異化賣點；到 2020 年代，WiFi 已經是預設配備，沒有才奇怪。AGI Bar 在賭：AI 推理能力會走同一條路。

再拉遠一步。[高盛 7 月的報告](/goldman-sachs-china-ai-moe-token-price-war-agent-coding/)拆過一條邏輯鏈：低激活比例 + 低利潤率定價 → 拿下 token 密集型場景。V4 Flash 正是那條邏輯鏈的產物——284B 參數只激活 13B，API 定價 $0.14/M。AGI Bar 再往下推一層：**如果硬體成本一次性攤完，你連 $0.14/M 都不用付。**

高盛報告描述的是 API 層的價格戰。AGI Bar 做的事情是把戰場搬到邊際成本的邏輯終點：零。

---

## 反方：這個類比有一個致命漏洞

「免費 WiFi」的類比聽起來漂亮，但有一個結構性差異必須正面處理。

WiFi 頻寬可以切分給所有人——50 個人同時連 WiFi，每個人慢一點，但都能用。GPU 推理不是這樣。它是序列化的。

根據 [Flowtivity 的雙 Spark 實測](https://flowtivity.ai/blog/deepseek-v4-flash-1m-context-dual-dgx-spark/)，兩台 DGX Spark 在 1M context 下最多支撐 6 個並行序列。就算把 context 壓短到一般對話長度（幾千 token），並行數也不會超過幾十個。

這意味著：如果酒吧同時有 20 個開發者坐下來，把 API Key 填進 Cursor 開始跑 agent，後面的人就要排隊等。這不是「每個人慢一點」，是「前面的人跑完你才能開始」。

更實際的問題：

**品質。** 如果 AGI Bar 用的是單台 Spark（Q2 量化），模型從 284B 壓到 80GB，智力折損不小。我[之前測 GLM 5.2 的 2-bit 量化](/glm-52-single-machine-rtx-pro-6000-tier1-local/)，結論是「跑得起來」但離「可用」有距離。V4 Flash 的 13B 激活量比 GLM 5.2 的 40B 小很多，量化折損可能沒那麼嚴重，但沒看到 AGI Bar 的實測數據，不好下定論。

**安全。** 你連上一個不認識的 WiFi，然後把 API endpoint 填進你的開發工具。你的 prompt、你的程式碼、你的對話內容，都經過這個 endpoint。對於只是隨意試玩的人，這無所謂；對於正在寫正式專案的開發者，這是需要考慮的風險。

這些限制不會殺死這個模式，但它們決定了這個模式的適用範圍：**低強度、探索性使用——不是生產環境的替代品。**

---

## 坦白說

推文是單一來源。@MaxForAI 發的貼文和截圖是目前唯一的公開資訊。AGI Bar 沒有官方公告，沒有技術規格說明，沒有講到底用了幾台 Spark、什麼量化精度、有沒有速率限制。本文所有技術推算都是根據公開的 DGX Spark 規格和第三方實測數據反推的，不是 AGI Bar 確認的。

成本概算很粗糙。我假設了 3 年攤提、商業電價、12 小時營業，任何一個假設變了，數字就不同。這個計算的意義不在精確數字，在於量級——硬體路線的年化成本和 API 路線在同一個數量級，甚至更低。

「免費無限量」這個宣稱本身也需要打折看。物理上，兩台 DGX Spark 的推理吞吐量有硬上限。如果同時使用的人多，要麼排隊、要麼限速、要麼降低 context 長度。「無限量」更可能是「在正常使用情境下不設人為上限」，不是「物理上無限」。

另一個資訊落差：虎嗅 2025 年底的[報導](https://m.huxiu.com/article/4819513.html)寫到 AGI Bar 老闆「大聰明」經營「赛博禅心」帳號，但推文裡 @MaxForAI（赛博禅心）說「這家酒吧是我朋友開的」。這個出入可能是多人共同經營、帳號轉手、或報導有誤，本文不做判定，只記錄有這個差異存在。

---

## 關鍵洞察

**Token 的分發邏輯正在分裂成兩條路線。** 一條是雲端 API，按量計費，適合彈性需求和生產環境。另一條是場域基礎設施，硬體一次性投入，邊際成本趨零，適合引流和社群經營。AGI Bar 是第二條路線的第一個公開案例。這兩條路線不互斥——你可能在 AGI Bar 用免費 token 做原型，回家用付費 API 跑生產。

**判斷一個「免費 AI」服務是不是可持續，看硬體成本佔營收的比例。** 兩台 DGX Spark 不到一萬美元，酒吧的客單價和翻桌率可以輕鬆覆蓋。如果有人拿這個模式去套「免費 AI 寫作助手」或「免費 AI 客服」，先算一下：你的業務有沒有足夠的非 AI 營收來吸收硬體攤提？WiFi 之所以能免費，是因為咖啡的毛利扛得住路由器的錢。

**對台灣的共創空間和咖啡廳經營者：一台 DGX Spark 約 15 萬台幣，能不能成為差異化賣點？** 但模型選擇比硬體更關鍵——V4 Flash 是 MIT 開源、跑在 128GB 記憶體上剛好夠用、13B 激活量速度可用。如果換一個需要更多記憶體或激活量更大的模型，同樣的硬體就撐不住。在考慮「要不要買一台 Spark 放在店裡」之前，先問自己的客群需要什麼模型、能接受什麼品質。
