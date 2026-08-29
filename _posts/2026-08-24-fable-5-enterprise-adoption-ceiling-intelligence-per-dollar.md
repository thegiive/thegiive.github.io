---
layout: post
title: "\"Fable 5 只佔 Anthropic 銷售的 11%：當最強模型不是賣最好的模型，你需要開始計算單位美元可以買到的智能 %\""
date: 2026-08-24 12:00:00 +0800
permalink: /fable-5-enterprise-adoption-ceiling-intelligence-per-dollar/
tags: [Fable 5, Anthropic, enterprise adoption, intelligence per dollar, Ramp, token usage, model pricing, 模型定價, Artificial Analysis, 智能密度, Claude, 企業採用, cost analysis]
categories: [AI 產業分析]
image: /assets/images/fable-5-adoption-ceiling-cover.png
description: "\"Ramp 追蹤七萬家企業的支付數據顯示，Fable 5 發布超過兩個月，只佔 Anthropic 模型支出的 11.4%、token 使用量的 6%。這篇從數據出發，拆解三個推開 Fable 5 的力量，提出「每美元多少智能」和「每 B 多少智能」兩個新指標，用 Artificial Analysis Intelligence Index 比較雲端 API 和開源模型的智能密度。\""
author: Wisely Chen
---

Anthropic 的 Fable 5 是目前市面上最強的模型。這一點沒有爭議。

但據 FT 最新報導，引用支付數據公司 [Ramp](https://ramp.com/data/ai-index-august-2026) 追蹤約七萬家企業的數據，Fable 5 上線超過兩個月，只佔 Anthropic 模型支出的 11.4%，token 使用量更只有 6%。

更讓人意外的是：7 月底才發布、價格正好便宜一半的 Opus 5，企業支出已經超過 Fable 5。

一家公司史上最強的旗艦模型，在商業上被自家上線不到一個月的次旗艦打敗。這在 AI 產業是頭一次。

---

## 數字先攤開來

| 模型 | 輸入 / 百萬 token | 輸出 / 百萬 token | Anthropic 支出佔比 | Token 佔比 |
|------|:--:|:--:|:--:|:--:|
| Fable 5 | $10 | $50 | 11.4% | 6% |
| Opus 5 | $5 | $25 | >11.4%（已超越） | — |
| Sonnet 5 | $2 | $10 | — | — |
| Haiku 4.5 | $1 | $5 | — | — |

Fable 5 的定價是 Opus 5 的整整兩倍。token 佔比只有 6% 但支出佔了 11.4%，代表它的每個 token 確實貴，但企業連這個貴的量都不願意多買。

對比 OpenAI，GPT-5.6 Sol 在 OpenAI 模型中拿到了 25% 的 token 使用量和 23% 的支出佔比。同為旗艦，Sol 的企業採用率是 Fable 5 的四倍以上。

---

## 三個力量同時把 Fable 5 推開

**價格。** Fable 5 每百萬 token $10/$50，Opus 5 是 $5/$25。在 agent 場景下一個任務動輒幾萬 token output，每月帳單差兩倍不是技術決策，是 CFO 一看就懂的數字。

**資料留存。** Fable 5 要求所有流量強制留存 30 天，覆蓋掉企業既有的零留存（ZDR）協議。Opus 5 支援零留存。對受 GDPR、HIPAA 約束的企業來說，這不是性能取捨，是「合規團隊還沒審完，這個模型根本不能用」。[Forrester](https://www.forrester.com/blogs/how-fable-5-and-mythos-5-change-ai-security-data-retention-and-vendor-risk/) 把這叫做 vendor risk 等級升高。

**性能沒有體感差。** Opus 5 在 CursorBench 3.2 上只差 Fable 5 半個百分點，在 OSWorld 2.0 甚至贏了 Fable 5 而且只用三分之一預算。多付 100% 的錢，能力只多了 0.5%——每多花一塊錢，買到的邊際智能幾乎為零。

---

## 飛輪第一次轉不動

過去兩年模型公司的增長邏輯很清楚：**更強的模型 → 企業升級 → 收入增加 → 訓練下一代**。從 GPT-3.5 到 GPT-4、從 Claude 2 到 Claude 3.5 Sonnet，每次都轉得很順，因為能力差距肉眼可見。

但 Fable 5 的能力提升進入了「邊際收益遞減」區間——不是不強，是強的那部分大量真實工作感受不到。Accel 合夥人 Miles Clements 在 FT 報導裡說：「Most people don't need to operate at the frontier.」他接著說，企業偏好旗艦模型的那個時代「was not a sustainable era」。

---

## 這不是 Anthropic 獨有的問題

Anthropic 整體表現不差——七月 ARR 達 $65B，企業採用率 43.5% 超過 OpenAI 的 39.7%。但這件事揭示的是結構性轉變：**模型能力到了某個水平，繼續提升的邊際價值在企業端迅速遞減。**

未來主要收入可能不是來自最強的模型，而是「夠強、夠便宜」的模型。旗艦模型從收入引擎變成技術展示窗口——證明你有前沿能力，但真正產生現金流的是 Sonnet 和 Opus 級別。Ramp 首席經濟學家 Ara Kharazian 的評論：Fable 5「disappointed both in adoption and real-world application given price + data retention requirements」。

---

## 新指標：每美元多少智能、每 B 多少智能

如果企業買的不是「最強」而是「每塊錢最划算」，競爭軸就從 benchmark 分數轉向智能密度。

[Artificial Analysis](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index) 的 Intelligence Index（II）是目前業界最常被引用的綜合評測之一，涵蓋多個 benchmark 的加權分數。把 Anthropic 和 OpenAI 的雲端 API 按 II 排在一起：

### 雲端 API：每美元多少智能

| 模型 | Intelligence Index | 輸入 $/MTok | 輸出 $/MTok | II / 輸出$ |
|------|:--:|--:|--:|:--:|
| Opus 5 | 63 | $5 | $25 | 2.52 |
| Fable 5 | 62 | $10 | $50 | 1.24 |
| GPT-5.6 Sol | 61 | $5 | $30 | 2.03 |
| Sonnet 5 | 55 | $2 | $10 | 5.50 |
| GPT-5.6 Terra | 55 | $2 | $12 | 4.58 |
| GPT-5.6 Luna | 52 | $0.20 | $1.20 | 43.33 |
| Haiku 4.5 | 30 | $1 | $5 | 6.00 |

Opus 5 分數比 Fable 5 還高一分（63 vs 62），價格卻便宜一半——Fable 5 是整張表裡最貴的，而且不是最聰明的。GPT-5.6 Luna 用 $0.20/$1.20 拿到 52 分，而 Haiku 4.5 花 $1/$5 只拿到 30 分——Luna 便宜五倍，分數高了 73%。

![雲端 API 輸出定價比較](/assets/images/fable-5-cloud-api-output-price.png)

### 開源模型：每 B 多少智能

雲端 API 看的是每美元多少智能，但開源模型跑在自己的 GPU 上，沒有按 token 計價的帳單。對它們來說，成本取決於模型大小——佔多少顯存（Total B）、每個 token 花多少算力（Active B）。所以換一個指標：II / Total B 和 II / Active B。

| 模型 | II | Total | Active | II / Total B | II / Active B |
|------|:--:|------:|------:|:--:|:--:|
| Kimi K3 | 60 | 2,800B | 104B | 0.021 | 0.58 |
| GLM-5.3 | 60 | 753B | 40B | 0.080 | 1.50 |
| Qwen3.8 2.4T | 58 | 2,400B | 95B | 0.024 | 0.61 |
| Qwen3.8 27B | 52 | 27B | 27B | 1.926 | 1.93 |
| Qwen3.6 27B | 46 | 27B | 27B | 1.704 | 1.70 |
| Qwen3.6 35B A3B | 43 | 36B | 3B | 1.194 | 14.33 |
| DeepSeek V4 Flash | 52 | 284B | 13B | 0.183 | 4.00 |
| Gemma 4 31B | 39 | 31B | 31B | 1.258 | 1.26 |
| Gemma 4 26B A4B | 31 | 26B | 4B | 1.192 | 7.75 |

### API vs 開源 = Opex vs Capex

這兩張表不是要你二選一。它們是兩種不同的成本結構：

雲端 API 是 **Opex**——按用量付費，零前期投入，適合需求波動大或剛起步的場景。開源模型是 **Capex**——買 GPU、部署推理服務，前期投入高但邊際成本趨近零，適合量大且穩定的場景。

務實的做法是兩者並行：用雲端 API 做原型和低量任務，等用量穩定後把高頻任務遷移到自建的開源模型。不是選邊站，是看你在哪個階段。

---

## 兩張圖怎麼讀

下面兩張散點圖把上面開源模型的表格視覺化。X 軸都是 Intelligence Index，虛線分割線在 II = 40——右邊是多數場景可用的「通用級」，左邊是特定技能才夠用的「利基級」。

**第一張：II vs II / Total B（記憶體效率）。** Y 軸是每十億總參數擠出多少智能分數。越高代表用越少顯存就能拿到同樣的分數。右上角是最理想的位置——聰明而且記憶體效率高。Qwen3.8 27B（Q38_27）和 Qwen3.6 27B（Q36_27）兩個 dense 小模型在這個指標上遙遙領先，因為它們整顆模型就是 27B，單卡就能跑。大模型（K3 的 2,800B、Q38_2.4T 的 2,400B）分數高但記憶體效率低，擠在圖的底部。

![開源模型 II vs 記憶體效率](/assets/images/fable-5-open-weight-memory-efficiency.png)

**第二張：II vs II / Active B（算力效率）。** Y 軸是每十億活躍參數擠出多少智能分數。MoE 模型在這裡有結構性優勢——Qwen3.6 35B A3B 只用 3B active 就拿到 43 分，II / Active B 高達 14.33，遠離其他所有點。Gemma 4 26B A4B 也因為 4B active 衝到 7.75。但要注意，這個指標對 dense 模型（active = total）天然不利，所以兩張圖要一起看才完整。

![開源模型 II vs 算力效率](/assets/images/fable-5-open-weight-compute-efficiency.png)

這些數字指向同一個結論：智能正在被壓進越來越小的空間。Kimi K3 和 GLM-5.3 都拿到 60 分，只差 Fable 5 兩分。DeepSeek V4 Flash 和 Qwen3.8 27B 拿到 52 分，跟 Sonnet 5 的 55 分差距不大，但一個只用 13B active，一個單卡就能跑。Fable 5 不只被自家的 Opus 5 和 Sonnet 5 從上面和中間夾擊，還被開源模型從下面逼近。Frontier 的護城河，在 Intelligence Index 上只剩兩三分。

---

## 對務實者的建議

**一、預設選 Opus 5 或 Sonnet 5，只在必要時升級。** 這已經是 Ramp 數據反映出來的多數企業行為。大部分 coding agent、文件處理、客服場景，Opus 5 能處理。

**二、注意 Fable 5 的 30 天資料留存。** 有零留存需求的組織，在合規團隊完成審查前不要碰 Fable 5 API。

**三、高頻場景考慮自建開源模型。** 如果你的 API 帳單已經穩定在每月五位數以上，把高頻任務遷移到 DeepSeek V4 Flash 或 Qwen3.8 27B 這類模型可能更划算。雲端 API 和自建推理不是二選一，是 Opex 和 Capex 的配比問題。

**四、重新定義「好」。** 不是 benchmark 最高分就是最好的選擇。在你的真實任務上，每塊錢能買到最多正確輸出的模型才是。

---

## 最後的觀察

人類在 AI 這邊折騰了這幾年，最後還是重新發現了一個很古老的商業規律：

**最好的產品，不一定是賣得最好的產品。**

Toyota Camry 不是最好的車。UNIQLO 不是最好的衣服。但它們賣得最好，因為它們在「夠好」和「夠便宜」之間找到了最甜蜜的平衡點。

Fable 5 今天面對的，是同樣的故事。Frontier Intelligence 依然重要，它定義了整個產業的技術天花板。但真正承擔絕大多數商業收入的，會是那些站在天花板下面兩層、但價格只要十分之一的模型。

對模型公司來說，下一個階段的競爭可能不再是「誰的模型最強」，而是「誰能在最低的成本下交付足夠的智能」。

這個轉變已經開始了。Fable 5 的 11.4% 就是證據。
