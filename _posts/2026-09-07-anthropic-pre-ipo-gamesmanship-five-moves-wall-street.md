---
layout: post
title: "Anthropic vs OpenAI 算力對決：從玉米田到 $2T IPO，誰的電表轉得比較快"
date: 2026-09-07 09:00:00 +0800
permalink: /anthropic-pre-ipo-gamesmanship-five-moves-wall-street/
tags: [Anthropic, OpenAI, compute, 算力, GW, IPO, Gavin Baker, Atreides, AWS Rainier, Trainium2, SpaceX Colossus, Google TPU, SemiAnalysis, 估值, infrastructure]
categories: [AI 產業分析]
image: /assets/images/anthropic-ipo-gamesmanship-cover.png
description: "Fable 5 剛出來的時候有多強，用過的人都知道。但用了一陣子，很多人覺得變弱了——很有可能不是模型降級，是推理需求暴增，電跟不上。所有人在比 Fable 和 Astra 誰比較聰明，但真正在跑的競賽是算力的分布。2025 年底 Anthropic 只有 OpenAI 的七成（1.4 GW vs 1.9 GW），到了 2026 年用開支反推已經反超——Anthropic 約 2.7 GW，OpenAI 約 2.4 GW。The Information 9 月 6 日報導 Anthropic 過去十一個月簽了至少 14.8 GW。這篇從正在跑的電量、已簽約的管道、每年花的錢三層拆開算力，再接上 Gavin Baker 的 IPO 策略分析。"
author: Wisely Chen
faq:
  - question: "Anthropic 的算力真的追上 OpenAI 了嗎？"
    answer: "看哪個口徑。2025 年底 Anthropic 的運行功率約 1.4 GW，OpenAI 約 1.9 GW，Anthropic 大約是 OpenAI 的七成（來源：Epoch AI 報告）。到了 2026 年，用算力開支反推的年均運行功率，Anthropic 約 2.7 GW 反而略高於 OpenAI 的 2.4 GW。但 Epoch AI 能點名到具體機房的數字更保守（Anthropic 約 1.45 GW、OpenAI 約 0.42 GW），他們自己也承認覆蓋不全。結論是：2026 年兩家在同一量級，差距在正負 20% 到 30% 之內，具體誰高隨月份和口徑變化。「Anthropic 算力遠不如 OpenAI」已經不是當前事實。"
  - question: "Anthropic 的算力從哪裡來？靠什麼追上的？"
    answer: "三個來源。第一，AWS Project Rainier——印第安納 New Carlisle 的 Trainium2 集群，已有 500K 顆晶片上線（AWS CEO Andy Jassy 2025 年 10 月公開），年底目標一百萬顆，單點約 900 MW。第二，Google TPU（Tensor Processing Unit）——Anthropic 過去五代以上的 Claude 都在 TPU 上訓練過，2026 年有 1 GW Ironwood 部署中，2027 年再加 5 GW。第三，SpaceX Colossus 1——約 300 MW、22 萬顆 NVIDIA GPU，原本是 Elon Musk 為訓練 Grok 建的，2026 年 5 月租給 Anthropic。這三塊加起來讓 Anthropic 在一年內從七成追到同一量級。"
  - question: "Anthropic 和 OpenAI 2026 年各花多少錢在算力上？"
    answer: "根據 SemiAnalysis 估算，Anthropic 2026 年總算力支出約 $491 億（訓練 ~$250 億、推理 ~$241 億），OpenAI 約 $546 億（訓練 ~$320 億、推理 ~$226 億）。OpenAI 自己公開說過 2026 年算力支出約 $500 億，與估算一致。年度現金消耗幾乎打平，OpenAI 訓練側略重、Anthropic 推理側略重。這些是賣方估算而非審計數字——兩家公司都還沒上市，真實支出不公開。"
  - question: "算力對等跟 Anthropic 的 $2T IPO 估值有什麼關係？"
    answer: "算力是 IPO 估值故事底下的基礎設施層。投資人評估 $2T 是否合理時，「這家公司有沒有足夠算力支撐營收增長」是關鍵問題之一。如果 Anthropic 的算力明顯不如 OpenAI，高增長就缺乏基礎設施支撐。現在算力追到同一量級，等於這個質疑被解除了。但算力對等不等於估值合理——還要看推理利潤率能不能持續（巴克萊估 50-65%）、$30T 的可尋址市場（Total Addressable Market）假設是否成立、以及競爭對手在六週內密集發布新模型帶來的時機風險。"
  - question: "Fable 5 用一陣子後感覺變弱，真的是算力問題嗎？"
    answer: "很有可能。The Information 9 月 6 日報導 Claude Code 和 Cowork 的需求增長快到 Anthropic 自己都始料未及，被迫緊急搶算力。當推理需求暴增但算力沒有等比擴充，模型的回應品質會下降——不是模型本身降級，而是推理資源被稀釋。Anthropic 過去十一個月簽了至少 14.8 GW（gigawatt，十億瓦）的算力合約就是在補這個缺口。這也解釋了為什麼算力分布——而不是模型 benchmark——才是判斷 AI Lab 長期實力的更可靠指標。  ---"
---

Fable 5 剛出來的時候有多強，用過的人都知道。

但用了一陣子，很多人覺得 Fable 變弱了。很有可能不是模型降級，是推理需求暴增，電跟不上。

所有人在比 Fable 和 Astra 誰比較聰明，但真正在跑的競賽是算力的分布。2025 年底 Anthropic 確實只有 OpenAI 的七成，這個格局正在以超乎預期的速度翻轉。

兩家公司都沒有公開過自己的算力數字。我們只能從外部資訊推估——用電量、花的錢、供應鏈情報、晶片商的財報電話會議。以下就是這些拼圖拼出來的畫面。

而且要先講清楚：用電量不能直接等於算力。1 GW 的 H100 機房和 1 GW 的 Trainium2 機房，算出來的 FLOPS 差很多。冷卻架構、機房 PUE、晶片世代、訓練還是推理——每一項都讓同樣的瓦數對應到不同的實際算力。下面用 GW 比的是「電表上的規模」，不是「跑出來的 FLOPS」。這是我們能從外部觀察到的最粗略但最可靠的代理指標。

---

## 第一層：正在跑的電（GW）

| 時間點 | OpenAI | Anthropic | Anthropic 佔比 |
|--------|:------:|:---------:|:--------------:|
| 2025 年底 | ~1.9 GW | ~1.4 GW | ~74% |
| 2026 年初 | ~2 GW | ~2 GW | ~100% |
| 2026 年均值（開支反推） | ~2.4 GW | ~2.7 GW | ~113% |

來源：2025 年底數字來自 [Epoch AI 報告](https://x.com/Saemin4655/status/2088824774416072859)（OpenAI ~1.7M H100 當量佔全球 11%，Anthropic ~1M 佔 6%）。2026 數字由算力開支反推。

Epoch 能點名到具體機房的數字更保守——Anthropic 約 1.45 GW、OpenAI 約 0.42 GW——但他們自己也說覆蓋不全，大量雲上租賃不在名單裡。

結論：**2026 年此刻真正在轉的訓練加推理功率，Anthropic 不再明顯低於 OpenAI。** 多數口徑是同一量級，差距大概在正負 20% 到 30% 之內，而且方向會隨月份變。

---

## 怎麼突然就追上的？

三塊拼起來的。

**一、AWS Project Rainier。** 2025 年 10 月，[Andy Jassy 發了一篇帖子](https://x.com/ajassy/status/1983616724642730217)：印第安納 New Carlisle 的玉米田變成了 AWS 史上最大的 AI 算力集群，Trainium2 晶片。他的原話：

> "It is 70% larger than any AI computing platform in AWS history, with nearly 500K Trainium2 chips, and is now fully operational with Anthropic actively using it to train and run inference for its industry-leading AI model, Claude."

500K 顆 Trainium2 已上線，年底目標衝到一百萬顆。單點約 900 MW 級。帖子 157 萬次觀看。底下留言最多的不是技術討論，是當地農民抱怨良田變機房。

**二、Google TPU。** 這一塊不是「未來」，是「一直都在」。[SemiAnalysis 指出](https://x.com/SemiAnalysis_/status/2075203875062120785) Anthropic 過去五代以上的 Claude 都在 TPU 上訓練過。2026 年有 1 GW 的 Ironwood TPU 正在部署，Q4 出貨加速。Broadcom CEO Hock Tan 在 9 月的[財報電話會議](https://x.com/FirstSquawk/status/2095260321397268918)上給了路線圖：2027 年再加 5 GW TPU v8i，2028 年增量 10 GW。Anthropic 將在 2027 年成為 Broadcom 最大的 XPU 客戶。

**三、SpaceX Colossus 1。** 這是最戲劇性的一筆。

Elon Musk 在 Memphis 建了 Colossus 1——約 300 MW、22 萬顆 GPU（H100/H200/GB200），[122 天建完](https://x.com/SemiAnalysis_/status/2087667981031506158)。原本是為了訓練 Grok。

然後 [2026 年 5 月，Anthropic 租下了整個集群](https://x.com/MilkRoadAI/status/2052986277977366547)。

[據報導](https://x.com/negligible_cap/status/2065502888973967710)，SpaceX 是在自己用 Colossus 訓練 Grok 碰到技術困難之後才決定租出去的。二月份 Musk 還在公開說 Anthropic「hates Western civilization」，五月他們就把他的整個資料中心租下來了。一位觀察者的[總結](https://x.com/itsak1to/status/2094885764408434947)：Musk 建了機房要打敗 Claude，結果現在 Claude 跑在上面。

---

## 第二層：已簽約的管道

### OpenAI

Stargate 對外仍是 $5,000 億、10 GW 量級敘事。2026 年 4 月稱 10 GW 目標已提前鎖定。合作方疊了 Microsoft、Oracle、CoreWeave、AWS Trainium、AMD，外加自研 Jalapeño ASIC。長期承諾有人匯總到萬億美元量級，裡面混了很多年的推理保底。

### Anthropic

Measured AI 把美國管道估到 2026 年底約 5 GW、2027 約 9.5 GW、2028 超過 15 GW——15 個園區、四種晶片、五種合約結構。

已知大單：

| 合作方 | 規模 |
|--------|------|
| AWS（Rainier） | 最高 5 GW |
| Google / Broadcom | 多 GW TPU（2027 起放量） |
| Azure | ~$300 億 |
| Nscale | ~$450 億 / 6 年 |
| SpaceX Colossus 1 | ~300 MW |
| Fluidstack、CoreWeave | 額外容量 |

2026 年春天有一段時間，外界甚至認為 Anthropic 已鎖定的 GW 比當時公開的 OpenAI 承諾還多。

然後是 9 月 6 日的一記重磅。[The Information 報導](https://x.com/Techmeme/status/2096682533106917555)，Anthropic 自去年十月以來簽了至少 14.8 GW 的算力合約，十年潛在支出上看 $5,170 億。這還不包括之前已有的 1-2 GW。驅動力之一：Claude Code 和 Cowork 的需求增長快到連 Anthropic 自己都始料未及，[被迫緊急搶算力](https://x.com/choblin29/status/2096638464792130011)。

14.8 GW 跟 Measured AI 之前估的 15 GW 管道高度吻合。差別在，現在有了 The Information 的獨立交叉確認。

遠期 OpenAI 更大。但 Anthropic 也不是在用望遠鏡看 OpenAI 的背影——兩家在同一條跑道上，差距是車身而不是圈數。

---

## 第三層：每年花在算力上的真金白銀

管道是承諾，電費才是事實。SemiAnalysis 估算的 2026 年算力支出：

| 項目 | Anthropic 2026E | OpenAI 2026E |
|------|:------:|:------:|
| 訓練支出 | ~$250 億 | ~$320 億 |
| 推理支出 | ~$241 億 | ~$226 億 |
| **總算力支出** | **~$491 億** | **~$546 億** |

OpenAI 自己公開說過 2026 年算力支出約 $500 億，跟 SemiAnalysis 估的 $546 億在同一個區間。

年度現金消耗幾乎打平。OpenAI 訓練側略重，Anthropic 推理側略重。

把三層疊起來看：正在跑的電同一量級、管道規模 Anthropic 不落後太多、年度支出幾乎打平。「Anthropic 算力遠遠不如 OpenAI」這個印象，是 2025 年的事實，不是 2026 年的。

---

## 算力為什麼重要：IPO 的基礎設施層

算力不只是技術指標。Anthropic 正在準備可能是[史上最大的科技 IPO](https://x.com/kimmonismus/status/2087806611918073940)，投資人在談 $2T 估值。Atreides Management 的 CIO [Gavin Baker 9 月 5 日的帖子](https://x.com/GavinSBaker/status/2096257640884027500)（82 萬次觀看，自標 pure speculation）拆了幾步棋：ARR 從 gross 切到 net、把 Meta 的 $50 億+ 從帳面先拿掉、模型發布節奏配合上市時程。但對算力敘事最關鍵的是 The Information 同日報導：IPO 投資人正在要求 Anthropic 揭露 [revenue per token 和 revenue per GW](https://x.com/theinformation/status/2096697449133809907)。算力從技術規格變成估值公式裡的變數——Anthropic 的 IPO 故事不是「我們的模型最聰明」，而是「我們有跟 OpenAI 同一量級的基礎設施，而且正在印鈔」。

---

## 反論：為什麼算力對等不等於估值合理

**一、管道是承諾，不是電。** 5 GW、15 GW 都是簽約數字，不是已上電的機房。從簽約到通電需要土地、電網、冷卻、人力，每一環都可能延遲。[SemiAnalysis 說 Colossus 1 的 300 MW 只花 122 天](https://x.com/SemiAnalysis_/status/2087667981031506158)，但那是 SpaceX 的速度，不是行業常態。

**二、算力燒得起不代表賺得回來。** [年化營收從 $9B 爆衝到 $65B](https://x.com/StockSavvyShay/status/2089448527701369088)，但算力支出也是 $491 億。即使[推理利潤率已經到 50-65%](/barclays-ai-profit-chain-cloud-tax-inference-margin/)，訓練那一半的錢是純燒。Q2 的營業利潤裡有一大塊來自 SpaceX 的一次性算力交易。

**三、[Polymarket 上十月底前 IPO 的機率已經從 90% 降到 62%](https://x.com/oddsqcom/status/2096531774428082543)。** Astra 的社群反應比預期好。Baker 自己也承認：「I think that Astra was probably better than Anthropic was expecting.」模型領先不是 IPO 的充分條件，時機窗口可能比想像的窄。

---

## 坦白說

這篇文章的算力數據有幾個必須知道的限制。

**GW 數字的口徑差異很大。** Epoch AI 點名到具體機房的數字（Anthropic 1.45 GW、OpenAI 0.42 GW）和開支反推的數字（Anthropic 2.7 GW、OpenAI 2.4 GW）差了好幾倍。差距來自雲上租賃、共用集群、推理 vs 訓練的分配。沒有一個數字是「正確」的——每個都是特定口徑下的估算。

**SemiAnalysis 的支出數字是賣方估算，不是審計數字。** 這兩家公司都還沒上市，真實的算力支出不公開。$491 億和 $546 億是基於供應鏈情報的推算。

**Baker 的帖子是推測，他自己標了 pure speculation**，而且他八月的一個宣稱被 Anthropic [公關負責人直接否認](https://x.com/sashadem/status/2088427297217110188)。

但這些數據放在一起做對了一件事：**把「Anthropic 算力不如 OpenAI」從直覺變成了可以查數字的問題。** 答案是：2025 年確實不如，2026 年已經追到同一量級。這不代表 $2T 合理，但代表「算力不夠」不再是反對 Anthropic 的有效論點。

---

## 關鍵洞察

**一、算力版圖的重繪速度比預期快得多。** 2025 年底 Anthropic 只有 OpenAI 的七成。不到一年，靠 Rainier（Trainium2）、Google TPU、和 SpaceX Colossus 的租賃，已經追到同一量級。如果你在用多數口徑不清楚的「算力差距」來決定押注哪家 API，數字已經變了。

**二、推理支出和訓練支出的比例透露策略方向。** Anthropic 推理支出 $241 億略高於 OpenAI 的 $226 億，訓練反過來（$250 億 vs $320 億）。上市後如果把推理利潤轉投訓練——推理帳單的使用者短期不會面臨漲價壓力，但長期供應優先級可能向高價值企業客戶傾斜。

**三、你的 API 供應商的 S-1 會是第一份公開的算力成本結構。** Anthropic 上市後，它的算力支出、推理利潤率、客戶集中度全部變成季報裡的公開數字。這是你第一次能從公開文件裡算出 API 帳單裡有多少是利潤、有多少是算力成本。[巴克萊的利潤鏈框架](/barclays-ai-profit-chain-cloud-tax-inference-margin/)會從估算變成可驗證的數字。做 API vs 自建的決策時，這張試算表的精確度會提升一個層次。

---

## 常見問題 Q&A

**Q: Anthropic 的算力真的追上 OpenAI 了嗎？**

看哪個口徑。2025 年底 Anthropic 的運行功率約 1.4 GW，OpenAI 約 1.9 GW，Anthropic 大約是 OpenAI 的七成（來源：Epoch AI 報告）。到了 2026 年，用算力開支反推的年均運行功率，Anthropic 約 2.7 GW 反而略高於 OpenAI 的 2.4 GW。但 Epoch AI 能點名到具體機房的數字更保守（Anthropic 約 1.45 GW、OpenAI 約 0.42 GW），他們自己也承認覆蓋不全。結論是：2026 年兩家在同一量級，差距在正負 20% 到 30% 之內，具體誰高隨月份和口徑變化。「Anthropic 算力遠不如 OpenAI」已經不是當前事實。

**Q: Anthropic 的算力從哪裡來？靠什麼追上的？**

三個來源。第一，AWS Project Rainier——印第安納 New Carlisle 的 Trainium2 集群，已有 500K 顆晶片上線（AWS CEO Andy Jassy 2025 年 10 月公開），年底目標一百萬顆，單點約 900 MW。第二，Google TPU（Tensor Processing Unit）——Anthropic 過去五代以上的 Claude 都在 TPU 上訓練過，2026 年有 1 GW Ironwood 部署中，2027 年再加 5 GW。第三，SpaceX Colossus 1——約 300 MW、22 萬顆 NVIDIA GPU，原本是 Elon Musk 為訓練 Grok 建的，2026 年 5 月租給 Anthropic。這三塊加起來讓 Anthropic 在一年內從七成追到同一量級。

**Q: Anthropic 和 OpenAI 2026 年各花多少錢在算力上？**

根據 SemiAnalysis 估算，Anthropic 2026 年總算力支出約 $491 億（訓練 ~$250 億、推理 ~$241 億），OpenAI 約 $546 億（訓練 ~$320 億、推理 ~$226 億）。OpenAI 自己公開說過 2026 年算力支出約 $500 億，與估算一致。年度現金消耗幾乎打平，OpenAI 訓練側略重、Anthropic 推理側略重。這些是賣方估算而非審計數字——兩家公司都還沒上市，真實支出不公開。

**Q: 算力對等跟 Anthropic 的 $2T IPO 估值有什麼關係？**

算力是 IPO 估值故事底下的基礎設施層。投資人評估 $2T 是否合理時，「這家公司有沒有足夠算力支撐營收增長」是關鍵問題之一。如果 Anthropic 的算力明顯不如 OpenAI，高增長就缺乏基礎設施支撐。現在算力追到同一量級，等於這個質疑被解除了。但算力對等不等於估值合理——還要看推理利潤率能不能持續（巴克萊估 50-65%）、$30T 的可尋址市場（Total Addressable Market）假設是否成立、以及競爭對手在六週內密集發布新模型帶來的時機風險。

**Q: Fable 5 用一陣子後感覺變弱，真的是算力問題嗎？**

很有可能。The Information 9 月 6 日報導 Claude Code 和 Cowork 的需求增長快到 Anthropic 自己都始料未及，被迫緊急搶算力。當推理需求暴增但算力沒有等比擴充，模型的回應品質會下降——不是模型本身降級，而是推理資源被稀釋。Anthropic 過去十一個月簽了至少 14.8 GW（gigawatt，十億瓦）的算力合約就是在補這個缺口。這也解釋了為什麼算力分布——而不是模型 benchmark——才是判斷 AI Lab 長期實力的更可靠指標。

---

## 來源

- [Epoch AI: global AI compute distribution（via @Saemin4655, 2026-08-16）](https://x.com/Saemin4655/status/2088824774416072859)
- [Andy Jassy: Project Rainier announcement（2025-10-29）](https://x.com/ajassy/status/1983616724642730217)
- [SemiAnalysis: SpaceX Colossus build speed（2026-08-12）](https://x.com/SemiAnalysis_/status/2087667981031506158)
- [Milk Road AI: Anthropic-SpaceX Colossus deal（2026-05-09）](https://x.com/MilkRoadAI/status/2052986277977366547)
- [SpaceX rented Colossus after Grok training trouble（2026-06-12）](https://x.com/negligible_cap/status/2065502888973967710)
- [Gavin Baker 原帖（2026-09-05）](https://x.com/GavinSBaker/status/2096257640884027500)
- [Baker on All-In Podcast（2026-08-18）](https://x.com/GavinSBaker/status/2089729629695234462)
- [Glenn Solomon on Krishna Rao](https://x.com/glennsolomon/status/2096275708066840729)
- [FT via @kimmonismus: $2T valuation talk（2026-08-13）](https://x.com/kimmonismus/status/2087806611918073940)
- [Anthropic revenue trajectory（2026-08-17）](https://x.com/StockSavvyShay/status/2089448527701369088)
- [Polymarket: IPO odds 90% → 62%（2026-09-06）](https://x.com/oddsqcom/status/2096531774428082543)
- [Sasha de Marigny denial（2026-08-15）](https://x.com/sashadem/status/2088427297217110188)
- [WSJ: OpenAI + Anthropic combined spend（via Beth Kindig, 2026-04-22）](https://x.com/Beth_Kindig/status/2047014766678253791)
- [本 blog: 巴克萊利潤鏈](/barclays-ai-profit-chain-cloud-tax-inference-margin/)
- [The Information: Anthropic 14.8 GW / $517B compute deals（via Techmeme, 2026-09-06）](https://x.com/Techmeme/status/2096682533106917555)
- [The Information: IPO investors demand revenue per token & GW（2026-09-06）](https://x.com/theinformation/status/2096697449133809907)
- [Choblin: Claude Code demand forced compute scramble（2026-09-06）](https://x.com/choblin29/status/2096638464792130011)
- [SemiAnalysis: Anthropic trained 5+ Claude releases on TPUs（2026-07-09）](https://x.com/SemiAnalysis_/status/2075203875062120785)
- [Broadcom Q3 FY26 earnings: Hock Tan on Anthropic TPU roadmap（via First Squawk, 2026-09-02）](https://x.com/FirstSquawk/status/2095260321397268918)
- [本 blog: Not your weights, not your product](/not-your-weights-not-your-product/)
