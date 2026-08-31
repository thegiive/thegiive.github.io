---
layout: post
title: "\"巴克萊拆帳：AI 每收 $100 的三層利潤鏈，推理毛利一年跳到 65%\""
date: 2026-08-31 09:00:00 +0800
permalink: /barclays-ai-profit-chain-cloud-tax-inference-margin/
tags: [Barclays, 巴克萊, AI profit, 利潤鏈, cloud providers, 雲端, inference margin, 推理利潤, AWS, Azure, Google Cloud, Goldman Sachs, 高盛, token economics]
categories: [AI 產業分析]
image: /assets/images/barclays-ai-profit-chain-cover.png
description: "\"巴克萊 8 月 28 日研報拆了一條 AI 利潤鏈：模型公司每賺 100 美元，35 到 40 美元流向三大雲，雲端從中拿走 10 到 20 美元營業利潤，利潤率最高 47%。反轉在模型這頭——付費推理利潤率從 2025 年的低雙位數跳到 2026 年的 50% 到 65%，API 推理超過 80%。全球 AI 實驗室營收兩年內從 70 億膨脹到 1,370 億美元。但高盛上個月的報告畫出完全不同的圖景：中國頭部模型 EBIT -30% 到 -39%。這篇把兩份研報的帳攤在一起，看利潤到底集中在誰手上。\""
author: Wisely Chen
faq:
  - question: "巴克萊這份研報的核心結論是什麼？"
    answer: "巴克萊 2026 年 8 月 28 日的研報拆了一條 AI 利潤鏈（AI Profit Chain）：AI 模型公司每賺 100 美元，35 到 40 美元流向三大雲端供應商（AWS、Azure、Google Cloud），雲端從中賺取 10 到 20 美元營業利潤，利潤率 35% 到 47%。模型公司本身的付費推理利潤率（Paid Inference Margin）從 2025 年的低雙位數，一年內跳到 50% 到 65%，其中 API 推理超過 80%。全球 AI 實驗室營收從 2024 年的 70 億美元膨脹到 2026 年的 1,370 億美元。"
  - question: "為什麼 AI 推理利潤率能在一年內跳這麼多？"
    answer: "巴克萊歸納了五個同時發生的力量。收入端：企業客戶和 agentic 工作流變成「必買品」，推理用量暴增；同時 frontier labs 的 API 名義定價在上調，不是下降。成本端：模型的 token 效率提升，完成同一個任務需要的 token 變少；推理基礎設施持續優化——量化（Quantization）、投機解碼（Speculative Decoding）、新一代算力壓低單次推理成本；加上規模效應，全球 AI 實驗室營收兩年內從 70 億膨脹到 1,370 億美元，固定成本被更大的營收基數攤薄。收入漲、成本降，五個力量同時推，利潤率就從十幾跳到六十幾。"
  - question: "巴克萊說利潤率 65%，但高盛說中國模型虧 30%，這兩個數字怎麼同時成立？"
    answer: "因為它們量的不是同一群公司。巴克萊量的是 frontier labs（Anthropic、OpenAI、Google DeepMind），這些公司用三大雲跑推理、以有利潤空間的價格賣 API 和訂閱。高盛量的是中國模型公司（DeepSeek、智譜、通義），它們的策略是虧損定價換市占——DeepSeek V4 Flash API 輸出價 $0.28/百萬 token，約為 Anthropic 最便宜模型的十分之一以下。兩本帳攤開來看，利潤不是從 AI 產業消失了，而是集中在有定價權（Pricing Power）的 frontier labs 手上。"
  - question: "這份研報對企業選擇 API vs 自建推理的決策有什麼影響？"
    answer: "巴克萊的分帳模型顯示，企業透過 API 用 AI，每 100 美元帳單裡有 35 到 41 美元是付給雲端供應商的，其中近一半是雲端利潤。訂閱制（Subscription）比 API 直售讓雲端賺更多（47% vs 34% 利潤率）。這意味著如果一家企業的 AI 用量夠大，自建推理（On-premise Inference）能省下的不只是模型公司的利潤，還包括雲端那一層的近五成利潤。不過自建需要 GPU、運維團隊和持續更新模型的 capex，適不適合取決於用量規模和技術能力。  ---"
---

2024 年，AI 實驗室的營收是 70 億美元，整個產業還在討論「AI 到底能不能賺錢」。

2026 年，巴克萊估算這個數字是 1,370 億。[研報在 8 月 28 日發布](https://cryptobriefing.com/barclays-ai-revenue-cloud-providers/)，拆的不是哪家公司的財報，而是一條完整的利潤鏈：模型公司每賺 100 美元，錢怎麼在各層之間流動，每一層的利潤率多高。

結論很直白：每一層都在賺錢。而且賺的比 2024 年任何人預期的都多。

---

## 利潤地圖：每 $100 的分帳

巴克萊建了兩個假想的 frontier lab 模型：Lab A 以 API 營收為主（占七成），Lab B 以訂閱營收為主（占八成）。分帳結構如下：

| 項目 | Lab A（API 為主） | Lab B（訂閱為主） |
|------|:--:|:--:|
| 模型公司營收 | $100 | $100 |
| 流向雲端（AWS/Azure/GCP） | $35 | $41 |
| 雲端營業利潤 | $11.80 | $19.10 |
| 雲端利潤率 | 34% | 47% |

模型公司每賺 100 美元，35 到 40 美元流向三大雲——AWS、Azure、Google Cloud。

雲端從中賺到 10 到 20 美元營業利潤，利潤率 35% 到 45%。電力成本、GPU 折舊全部扣完之後的數字。訂閱制模型（Lab B）讓雲端賺更多，因為訂閱帶來穩定的推理負載，基礎設施利用率更高。

用一個比喻：三大雲是 AI 產業後面的水表。模型公司跑多少推理，水表就轉多快。而水表的毛利率接近五成。

---

## 反轉在模型這頭

雲端賺錢不意外——賣鏟子的在淘金熱裡向來不虧。真正讓這條利潤鏈超出預期的，是模型層自己。

巴克萊的數字：付費推理利潤率從 2025 年的低雙位數，一年內跳到 50% 到 65%。

拆開看更驚人：

| 產品類型 | 2025 推理利潤率 | 2026 推理利潤率 |
|---------|:--:|:--:|
| 訂閱制 | 低雙位數 | ~70% |
| API 直售 | 低雙位數 | >80% |

API 推理的利潤率超過 80%。

這意味著 Anthropic 的 Claude、OpenAI 的 GPT 每處理一次 API 呼叫，扣掉雲端費用和運算成本之後，留下的利潤超過八成。一年前這個數字還是十幾個百分點。

巴克萊把利潤率跳升歸因於五個同時發生的力量：

1. **需求端拉動**：企業客戶和 agentic 工作流變成「必買品」，推理用量暴增
2. **API 名義定價上調**：frontier labs 在漲價，不是降價
3. **模型 token 效率提升**：完成同一個任務需要的 token 變少了
4. **推理基礎設施優化**：量化、speculative decoding、新一代算力持續壓低單次推理成本
5. **規模效應**：營收從 70 億漲到 1,370 億，固定成本被攤薄

前兩個是收入端的故事（賣得更多、賣得更貴），後三個是成本端的故事（花得更少）。五個同時推，利潤率就從十幾跳到六十幾。

---

## 飛輪的規模

利潤率高只是故事的一半。另一半是規模。

| 年份 | 全球 AI 實驗室營收 | 訓練支出占營收比 |
|------|:--:|:--:|
| 2024 | $70 億 | 96% |
| 2026 | $1,370 億（估） | 48% |
| 2028 | $6,900 億（預估） | 30% |

2024 年，訓練支出占營收的 96%——幾乎每一塊錢收入都拿去訓練下一代模型。到 2026 年這個比例降到 48%。不是訓練花的錢變少了，是推理帶進來的收入漲太快。

巴克萊估算 2026 年底的年化經常性收入約 2,000 億美元。調整後毛利率同比增加 30 到 50 個百分點。

一句話概括：訓練是 capex，推理是印鈔機。印鈔機已經啟動了。

---

## 高盛的另一本帳：同一個產業，完全相反的數字

如果只看巴克萊，故事是「AI 全面印鈔」。但高盛上個月的報告畫了一張完全不同的圖。

[高盛 Ronald Keung 團隊 7 月的 50 頁中國 AI 模型深度報告](/goldman-sachs-china-ai-moe-token-price-war-agent-coding/)測算：中國頭部模型 Agentic 場景 EBIT -30%，Coding 場景 -39%。高盛預測要到 2030 年才轉正。

巴克萊說利潤率 65%。高盛說利潤率 -30%。

兩個數字同時為真，因為它們量的不是同一群人。

巴克萊量的是 frontier labs——Anthropic、OpenAI、Google DeepMind 這些用三大雲跑推理、賣 API 和訂閱的公司。它們的定價有利潤空間：Claude API 每百萬 token 輸出 $10-50（依模型等級），定價本身就包含了利潤。

高盛量的是中國模型公司——DeepSeek、智譜、通義。它們的策略完全相反：用虧損定價換市占。DeepSeek V4 Flash API 每百萬 token 輸出 $0.28，是 Anthropic 最便宜模型的十分之一以下。中國模型在 [OpenRouter 上拿下 agent token 的 85%、代碼 token 的 89%](/goldman-sachs-china-ai-moe-token-price-war-agent-coding/)，代價是每賣一塊錢虧三毛到四毛。

**利潤不是從 AI 產業消失了——是集中在有定價權的那群人手上。** 有定價權的是 frontier labs，沒有定價權的在用虧損換市占。兩本帳攤開來看，全球 AI 的利潤分配比任何一份單獨報告顯示的都更極端。

---

## 但 frontier labs 整體賺錢嗎？把訓練加回去

推理利潤率 50-65% 聽起來是印鈔機。但巴克萊的推理利潤率是扣掉雲端成本和運算費用之後的數字——**沒有扣訓練**。

訓練支出占營收比 2026 年是 48%。把它加回來，帳就不一樣了：

| | 調整後毛利率 | 減：訓練占營收比 | 每 $100 剩多少 |
|---|:--:|:--:|:--:|
| Lab A（API 為主） | ~55% | 48% | ~$7 |
| Lab B（訂閱為主） | ~38% | 48% | ~-$10 |
| 三大雲 | 34-47% | 0% | $10-20 |

Lab A 每賺 100 美元，扣完雲端、推理成本、訓練支出，剩大約 7 塊。Lab B 還是負的——訓練成本吃掉了全部毛利再多吃 10 塊。

三大雲不訓練模型，不承擔研發風險。它們抽的是水費，不管模型公司是盈是虧，水表都在轉。

**誰在賺錢，誰在賠錢：**

- **三大雲：穩賺。** 每 $100 拿走 $10-20 利潤，利潤率 34-47%，而且這個利潤跟模型換代無關——下一代模型還是要跑在它們的基礎設施上。
- **Frontier labs（API 為主）：勉強打平。** 推理印鈔，但訓練燒掉了大部分。Lab A 的 $7 利潤薄得像紙——下一次訓練預算膨脹就可能吃掉。
- **Frontier labs（訂閱為主）：還在虧。** 訂閱制讓雲端抽更多（47% vs 34%），留給模型公司的毛利更少，扣完訓練就是負數。
- **中國模型公司：大幅虧損。** 高盛測算 EBIT -30% 到 -39%，預計 2030 年才轉正。它們連推理都在虧，訓練更不用說。

Frontier labs 的策略是用推理利潤補貼訓練——2024 年訓練占 96%，2026 年降到 48%，不是訓練便宜了，是推理收入漲太快。但「推理補貼訓練」跟「整體賺錢」是兩回事。推理那頭確實在印鈔，訓練那頭也確實在燒。淨下來，Lab A 剛好打平，Lab B 還是虧。

**整條利潤鏈裡真正的贏家是雲端。** 它們不需要下注哪個模型會贏，不需要承擔訓練失敗的風險，只要 AI 推理持續跑在它們的基礎設施上，水表就持續轉。這就是為什麼 AWS、Azure、GCP 的股價跟 AI 故事正相關——它們賣的不是模型，是模型必須跑在上面的東西。

---

## 行為證據：全產業定價遷移，殺訂閱、推 token 計費

如果巴克萊的利潤模型是對的——API 計費（Lab A）毛利 55%，訂閱制（Lab B）只有 38%——那模型公司的理性行為就是竭盡所能把客戶從訂閱趕到 API 計費。

過去一年，它們確實在這麼做。

| 公司 | 產品 | 時間 | 變化 |
|------|------|------|------|
| Anthropic | Enterprise Claude | 2025/11 起 → 2026/04 完成 | 固定座位費含 token → [座位費 + per-token 另計](https://www.theregister.com/2026/04/16/anthropic_ejects_bundled_tokens_enterprise/)，150 人以上無 flat-fee 選項 |
| OpenAI | ChatGPT / Codex | 2026/04/02 | per-message → [token credit 計費](https://lilting.ch/en/articles/openai-codex-token-based-pricing-rate-card)，Business 座位費從 $25 降到 $20 |
| GitHub | Copilot | 2026/04 → 06 | 固定配額 → [AI Credits（token 計費）](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/) |
| Anthropic | Pro / Max（消費者） | 2026/05/13 宣布（[6/15 暫緩](https://www.techtimes.com/articles/317625/20260602/anthropic-ends-subscription-subsidy-agents-june-15-credit-pool-replaces-flat-rate-access.htm)） | flat-rate → credit pool + per-token |
| Google | Gemini Notebook（原 NotebookLM） | [2026/08/28 宣布](https://9to5google.com/2026/08/28/gemini-notebook-usage-limits/)，9/2 生效 | 每日固定次數 → compute-based，5 小時滾動窗口 + 週限額 |

Anthropic 的路徑最完整：2025 年 11 月開始把企業客戶續約改成 usage-based，2026 年 2 月推出新制（$20/人月只買平台入場券，token 全部照 API 費率另計），3 月 8 日是 legacy plan 硬截止。到了 4 月，bundled token 從企業方案裡徹底移除。甚至 5 月嘗試把消費者方案的 agent 用量也拆出來改 credit 計費——雖然在 6/15 暫緩了，方向沒變。

OpenAI 的動作更乾脆：4 月 2 日一刀切，Plus、Pro、Business 全部從 per-message 改 token credit。座位費反而降了 $5——降座位費是為了讓客戶覺得「便宜了」，真正的收入來源搬到了 token 消耗。

Google 的 Gemini Notebook 是最新一個。巴克萊報告 8/28 發布，同一天 Google 宣布把 NotebookLM 從「每天 N 次」固定配額改成 compute-based 計費——每個請求按運算量算，短對話便宜、複雜 prompt 貴。

**五家公司在同一季做了同一件事。** 方向完全一致：座位費／月費變成入場券，真正的收入來源搬到 per-token 或 per-compute。這不是巧合，是利潤結構決定的必然——巴克萊的數字解釋了為什麼。API 計費比訂閱制每 $100 多留 $17 的毛利。在營收 1,370 億的規模上，17 個百分點是超過 200 億美元的差距。

---

## 反方：這個利潤率能撐多久

巴克萊的數字是 2026 年的快照。它能不能代表新常態，至少有三個理由質疑：

**一、開源逼近 frontier。** [Kimi K3 和 GLM-5.3 在 Artificial Analysis Intelligence Index 上拿到 60，Fable 5 是 62](/not-your-weights-not-your-product/)。差距只剩 2 分。當開源模型的能力接近封閉模型，企業 CTO 有了替代選項。替代選項出現的那一天，定價權就開始鬆動。

**二、中國模型的虧損定價不會永遠持續，但它會在結束之前壓低全行業價格預期。** DeepSeek V4 Flash 的 $0.28/M token 已經在 agent 和 coding 場景建立了價格錨。即使中國模型未來漲價，市場對「合理 token 價格」的預期已經被拉低了。Frontier labs 要維持 80% API 利潤率，必須持續證明它們的品質差距值那個溢價。

**三、地端推理正在把邊際成本推向零。** 這個 blog [寫過北京 AGI Bar 的案例](/agi-bar-free-token-dgx-spark-inference-infrastructure/)：兩台 DGX Spark（共 $9,400）跑 V4 Flash，年化成本約 $3,500，之後只剩電費。當硬體一次性攤完、token 邊際成本趨零，雲端 API 的利潤就面臨結構性壓力。

**四、Frontier labs 自己在脫離雲端。** 巴克萊假設 $35-40 流向三大雲，但 frontier labs 看得懂這筆帳——被抽走 $35-40、雲端還賺 34-47% 利潤，自己扣完訓練只剩 $7 或虧 $10。理性反應就是自建機房，把雲端利潤吃回來。OpenAI 啟動了 [Project Camellia（喬治亞州自建機房，3.2GW）](https://builtin.com/articles/openai-cloud-deals)加上 Stargate（7GW，$4,000 億以上），infra 預算拉到 2030 年 $7,500 億。Anthropic 簽了 [$500 億 Fluidstack 機房合約](https://www.techcrunch.com/2025/11/12/anthropic-announces-50-billion-data-center-plan/)，2026 年 8 月跟 Macquarie 和 GIC 成立 [Theseus Infrastructure JV](https://enterprisedna.co/resources/news/anthropic-theseus-infrastructure-macquarie-gic-data-centers-2026/) 自建專用機房。xAI 從頭就自建——Memphis Colossus 已到 1GW、55 萬顆 GPU。Google DeepMind 跑在 Google 自有 TPU 上，Meta 的 Llama 全在自有機房訓練。雲端的水表生意短期很好，但最大客戶正在自己裝水管。

**但雲端大廠不是坐等被脫離——它們有三層防線。**

第一層是**股權綁定**。Amazon 累計投入 Anthropic [$330 億](https://www.forbes.com/sites/jonmarkman/2026/04/22/amazon-33-billion-anthropic-deal-and-the-limits-of-ai-infrastructure/)，Microsoft 投 OpenAI $130 億以上並鎖定 [$2,500 億 Azure 承諾](https://techcrunch.com/2026/07/29/microsoft-is-openly-competing-with-openai-anthropic-more-than-ever/)到 2032 年。即使 frontier labs 自建機房，雲端作為股東照樣分利潤。投資不只是雲生意，是對沖。

第二層是**自研晶片的遷移成本**。AWS Trainium [年化營收 $200 億](https://cryptobriefing.com/amazon-trainium-chip-20b-revenue/)，鎖定超過 $2,250 億承諾營收，Anthropic 和 OpenAI 都簽了多年合約。Google TPU 賣到 100 萬顆給 Anthropic，Gemini 完全在 TPU 上訓練。在 Trainium / TPU 上訓練的模型，搬家成本極高——不只搬資料，是重新適配整套訓練棧。

第三層是**自建模型**。Microsoft 2025 年 9 月[拿到自建模型的自由](https://www.cnbc.com/2026/06/02/microsoft-unveils-new-ai-models-lessen-reliance-on-openai-lower-costs.html)後，2026 年推出 MAI-Code-1-Flash、MAI-Thinking-1 等一系列自有模型。Amazon AGI 團隊被要求做出超越 Claude 的模型。Google 的 Gemini 本來就是自己的。三大雲的訊息很明確：你不跑我的雲？那我自己也有模型。

再加上 Bedrock、Vertex AI、Azure Foundry 這種多模型平台——上面同時放了 Claude、Llama、Gemini、Mistral——企業客戶換模型不用換雲，這本身就是留客機制。

這五個力量沒有一個已經擊穿 frontier labs 的利潤。但它們同時在推，方向一致。巴克萊的 65% 是此刻的利潤率，不是鐵板。而雲端的 34-47% 利潤率也不是穩態——它既被客戶自建威脅，又被自己的三層防線保護著。攻防還在進行中。

---

## 坦白說

這份報告有幾個必須知道的限制。

**巴克萊的分帳模型是假想的，不是任何一家公司的真實財報。** Lab A 和 Lab B 是模型公司的典型化描繪，不是 Anthropic 或 OpenAI 的真實成本結構。真實數字不公開——這些公司都還沒上市。所以 34% 和 47% 的雲端利潤率是估算，不是審計後的數字。

**「全球 AI 實驗室營收 1,370 億」的口徑不清楚。** 這個數字包含哪些公司、怎麼定義「AI 實驗室」（Google Cloud 的 AI 營收算嗎？Microsoft Copilot 算嗎？）、如何處理企業內部使用的 AI 推理（不走外部 API），報告的二手報導裡沒有說明。70 億到 1,370 億，數字本身可能沒問題，但定義邊界會大幅影響規模感。

**推理利潤率 50-65% 是行業中位估計，不是每家都到。** Frontier labs 賣 API 超過 80%，但規模較小的模型公司、或者定價策略比較激進的，利潤率可能低得多。中位數掩蓋了分佈。

但它做對了一件事：**第一次把 AI 的利潤從「模型公司賺不賺錢」拆到「每一層賺多少」。** 訓練的帳大家盯了三年，推理的帳現在才被攤開。知道雲端在每 100 美元裡抽走 35-40、再賺近五成，這對選擇自建 vs API 的決策是有用的算術。

---

## 關鍵洞察

**一、AI 產業的利潤結構已經可計算了。** 2024 年只有訓練成本可算，收入是猜的。2026 年，推理收入、雲端抽成、各層利潤率都有了估算框架。不同意巴克萊的數字沒關係，重要的是你可以拿這個框架去填你自己的數字——算你的 API 帳單裡有多少是雲端利潤、多少是模型利潤、有多少空間可以透過自建省下來。

**二、雲端稅是真的，而且訂閱制比 API 付的更多。** Lab B（訂閱為主）的雲端利潤率 47%，Lab A（API 為主）是 34%。如果你是企業 CTO、用訂閱制的 AI 產品（Copilot、Claude Pro），你付的價格裡有接近一半是雲端利潤。做自建 vs 買服務的決策時，這個數字值得放進試算表。

**三、利潤集中在有定價權的那群人手上。** 巴克萊的 65% 和高盛的 -30% 同時存在。差別不是技術，是定價權。有定價權的 frontier labs 在印鈔，沒有定價權的中國模型在用虧損換市占。你的決策取決於你賭哪一邊先到拐點——中國模型 2030 年轉正的速度，還是開源模型填掉那 2 分差距的速度。

---

## 三方大逃殺，一個軍火商

把上面所有動作攤開來看，這不是單一條利潤鏈——是一場三方大逃殺，每一方都在同時逃離和鎖定其他兩方：

**Users** 被趕向 API 計費（帳單變貴）→ 反應是往地端跑、擁抱開源和 sovereign AI → labs 失去定價權。**Labs** 被雲端抽走 $35-40 → 趕 users 去 API 提高毛利、同時自建機房脫離雲端 → 但 capex 暴增，而且被 users 不滿。**Cloud** 背一身 capex 建機房 → 用自研晶片（Trainium、TPU）鎖 labs、用股權對沖出走風險、自己訓模型當 plan B → 直接變成 labs 的競爭對手。

每一方的防禦動作，都是另一方的新威脅。循環不斷。

但不管這場大逃殺誰贏誰輸，有一方穩坐釣魚台。

| 角色 | 處境 | 利潤率 |
|------|------|--------|
| NVIDIA | 賣 GPU 給所有人 | [~60%+ 毛利，AI 晶片市佔 80-85%](https://presenc.ai/research/ai-chip-market-share-2026) |
| Cloud | 賣水表，三層防線鎖客 | 34-47% |
| Frontier labs（API） | 推理印鈔但訓練燒掉 | ~7% net |
| Frontier labs（訂閱） | 被兩頭夾 | -10% net |
| 中國模型 | 虧損換市占 | -30% to -39% |

Users 逃去地端——買 NVIDIA GPU。Labs 自建機房——買 NVIDIA GPU。Cloud 擴建——買 NVIDIA GPU。NVIDIA FY2026 資料中心營收 [$1,937 億](https://www.datacenterdynamics.com/en/news/nvidia-reports-record-data-center-revenues-of-623bn-up-75-yoy/)，2026 Q2 單季 $890 億，YoY +117%。

**越上游越賺。** NVIDIA 賣鏟子，雲端賣水，labs 淘金，中國模型在虧錢拉人頭。唯一的威脅是自研晶片——Trainium、TPU 合計已吃到 15-20% 市佔，TCO 優勢 40-65%——但這些晶片只有做它的那家雲端自己能用，不是公開市場。對所有非超大規模客戶來說，能買的還是 NVIDIA。

老黃是這場大逃殺裡唯一不用逃的人。

---

## 常見問題 Q&A

**Q: 巴克萊這份研報的核心結論是什麼？**

巴克萊 2026 年 8 月 28 日的研報拆了一條 AI 利潤鏈（AI Profit Chain）：AI 模型公司每賺 100 美元，35 到 40 美元流向三大雲端供應商（AWS、Azure、Google Cloud），雲端從中賺取 10 到 20 美元營業利潤，利潤率 35% 到 47%。模型公司本身的付費推理利潤率（Paid Inference Margin）從 2025 年的低雙位數，一年內跳到 50% 到 65%，其中 API 推理超過 80%。全球 AI 實驗室營收從 2024 年的 70 億美元膨脹到 2026 年的 1,370 億美元。

**Q: 為什麼 AI 推理利潤率能在一年內跳這麼多？**

巴克萊歸納了五個同時發生的力量。收入端：企業客戶和 agentic 工作流變成「必買品」，推理用量暴增；同時 frontier labs 的 API 名義定價在上調，不是下降。成本端：模型的 token 效率提升，完成同一個任務需要的 token 變少；推理基礎設施持續優化——量化（Quantization）、投機解碼（Speculative Decoding）、新一代算力壓低單次推理成本；加上規模效應，全球 AI 實驗室營收兩年內從 70 億膨脹到 1,370 億美元，固定成本被更大的營收基數攤薄。收入漲、成本降，五個力量同時推，利潤率就從十幾跳到六十幾。

**Q: 巴克萊說利潤率 65%，但高盛說中國模型虧 30%，這兩個數字怎麼同時成立？**

因為它們量的不是同一群公司。巴克萊量的是 frontier labs（Anthropic、OpenAI、Google DeepMind），這些公司用三大雲跑推理、以有利潤空間的價格賣 API 和訂閱。高盛量的是中國模型公司（DeepSeek、智譜、通義），它們的策略是虧損定價換市占——DeepSeek V4 Flash API 輸出價 $0.28/百萬 token，約為 Anthropic 最便宜模型的十分之一以下。兩本帳攤開來看，利潤不是從 AI 產業消失了，而是集中在有定價權（Pricing Power）的 frontier labs 手上。

**Q: 這份研報對企業選擇 API vs 自建推理的決策有什麼影響？**

巴克萊的分帳模型顯示，企業透過 API 用 AI，每 100 美元帳單裡有 35 到 41 美元是付給雲端供應商的，其中近一半是雲端利潤。訂閱制（Subscription）比 API 直售讓雲端賺更多（47% vs 34% 利潤率）。這意味著如果一家企業的 AI 用量夠大，自建推理（On-premise Inference）能省下的不只是模型公司的利潤，還包括雲端那一層的近五成利潤。不過自建需要 GPU、運維團隊和持續更新模型的 capex，適不適合取決於用量規模和技術能力。

---

## 來源

- [CryptoBriefing: Barclays report on cloud providers' AI revenue](https://cryptobriefing.com/barclays-ai-revenue-cloud-providers/)
- [AllWeatherFinance: AI profit structure analysis](https://allweatherfinance.com/ai-profit-structure-for-every-100-in-revenue-generated-by-model-companies-35-40-flows-to-cloud-providers-bringing-them-10-20-in-operating-profit/)
