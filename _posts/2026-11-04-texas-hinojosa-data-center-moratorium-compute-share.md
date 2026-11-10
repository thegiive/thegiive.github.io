---
layout: post
title: "Gina Hinojosa 贏下德州：約 13 GW 資料中心有風險，規模相當於全球 AI 電力的三成"
date: 2026-11-04 09:00:00 +0800
permalink: /texas-hinojosa-data-center-moratorium-compute-share/
tags: [Gina Hinojosa, 德州, ERCOT, 資料中心, moratorium, 算力, CoreWeave, Neo-cloud, Epoch AI, 地端模型, 故障域]
categories: [AI 產業分析]
image: /assets/images/texas-governor-hinojosa-nbc-results-1.png
description: "Gina Hinojosa 以 52.9% 對 45.6% 贏下德州州長，Nasdaq 100 期貨最深跌 2.2%，CoreWeave 跌 7%。但德州的暫停令是敗選的 Abbott 在 8 月就下了。這次真正改變的是結束條件：從審計做完，變成立法通過。這篇把 ERCOT 的 474 GW 一層層扣到 6.6 GW 和約 13 GW，算出它們相當於全球 AI 資料中心電力的 15% 到 38%，再拆 CoreWeave 從 5.9% 到近 15% 的資金成本，以及這對用推論的人代表什麼。"
author: Wisely Chen
faq:
  - question: "德州的資料中心暫停令是 Gina Hinojosa 下的嗎？"
    answer: "不是。現行的暫停是現任共和黨州長 Greg Abbott 下的：2026 年 8 月 3 日要求暫停新資料中心併網，9 月 21 日要求德州環境品質委員會（TCEQ）暫停相關許可，直到德州電網營運商 ERCOT 完成審計，審計目標日是 2026 年 12 月 10 日。Hinojosa 的競選承諾是暫停到議會立法，差別在結束條件，而不是有沒有暫停。"
  - question: "德州卡住的資料中心容量相當於全球 AI 算力多少？"
    answer: "作者依 Epoch AI 資料估算，2026 年 6 月全球 AI 資料中心總電力（Total Facility Power）約 35–44 GW。只差送電核准的 6.6 GW 規模相當於其中 15–19%，分析師估的 13.3 GW 風險容量相當於 30–38%。這些都是未來幾年的新增容量，不是現役算力被關掉，所以應讀成「規模相當於」，不是「佔了」。"
  - question: "ERCOT 的 474 GW 排隊量是真實需求嗎？"
    answer: "不完全是。474 GW 是德州電網營運商 ERCOT 的大型用電併網申請（Large Load Interconnection）總量，約 90% 是資料中心，是德州 91.1 GW 歷史尖峰的 5.2 倍。Utility Dive 引述專家說，其中相當部分可能是投機或重複申請。比較接近落地的數字是 17 個大型用電戶、約 6.6 GW，它們截至 2026 年 8 月 20 日只差送電核准，且要分約五年拉滿。"
  - question: "CoreWeave 真的是用 15% 的利率借錢嗎？"
    answer: "不是。近 15% 是 CoreWeave 2032 年到期票據在次級市場的殖利率（Yield），2026 年 10 月中一度衝到這個水準，該票據的票面利率是 9.625%。CoreWeave 2026 年新融資的成本約在 5.9%（3 月投資級 GPU 貸款）到 10.44%（7 月貸款的到期殖利率）之間。殖利率衝高代表債市要求更高的風險補償，但不等於公司實際付出的利息。"
  - question: "這件事對企業使用 AI 推論有什麼實際影響？"
    answer: "短期不會讓現有服務停擺，德州現役機房仍在運轉。比較實際的影響是新增容量的不確定性變高，尤其是新增容量集中在德州、又依賴高息債的算力雲（Neo-cloud）。可以做的事有兩件：向供應商確認新增容量的州別與許可狀態，以及把便宜模型能處理的工作移過去，並測過一次切回大廠或地端的回退路徑。  ---"
---

Gina Hinojosa 贏了。NBC 的開票頁面在美東時間上午 8:33 顯示 52.9% 對 45.6%，開票 96.3%（本文封面即該頁截圖）。報導說 Hinojosa 是 [1990 年以來德州第一位民主黨州長](https://www.unite.ai/data-center-policy-fears-hit-ai-stocks-after-hinojosas-texas-win/)，競選承諾之一是暫停新資料中心建設。

市場當晚就反應了。[Nasdaq 100 期貨最深跌 2.2%](https://businessmirror.com.ph/2026/11/04/ai-data-center-boom-seen-set-for-upheaval-after-us-elections/)，[之後收復大半](https://huggingnews.com/us-politics/us-stock-futures-erase-drop-over-texas-governor-flip-and-data-center-fre-6bc2bd1d)。個股的差別比指數有意思：[CoreWeave、SpaceX 跌 7%，Iren 跌 6%，Oracle 跌 4.3%，Nebius 跌 3%；Alphabet、Meta、Microsoft 多數上漲](https://www.cnbc.com/2026/11/04/ai-stocks-texas-governor-data-centers.html)。

很多人把這件事當政治或財經八卦看。我想做的事很單純：把數字攤開，算出被卡住的容量到底有多大。

<nav class="post-toc" markdown="1">
**目錄**

* 目錄
{:toc}
</nav>

## 30 秒定位

| 項目 | 內容 |
|------|------|
| 事件 | Hinojosa 擊敗現任州長 Abbott，52.9% 對 45.6%（開票 96.3%） |
| 排隊總量 | ERCOT 大型用電申請 474 GW，約 90% 是資料中心 |
| 只差送電核准 | 17 個大型用電戶、約 6.6 GW，分約五年拉滿 |
| 分析師估的風險容量 | GLJ 約 13 GW、Jefferies 13.3 GW |
| 相當於全球 AI 電力 | 15–19%（6.6 GW）、30–38%（13.3 GW），我的估算 |
| 德州佔全美規劃容量 | 27%（Wells Fargo） |

## 暫停令不是她下的

先釐清一件很容易寫錯的事：德州現在的暫停令，是敗選的 Abbott 下的。

Abbott 在 [8 月 3 日要求暫停新資料中心併網](https://utilitydive.com/news/ercot-texas-puc-data-center-audit/828472)，[9 月 21 日再要求 TCEQ 暫停資料中心相關許可](https://www.cnbc.com/2026/09/21/texas-governor-abbott-ai-data-center-permits.html)，直到 ERCOT 完成審計。ERCOT 的審計目標日是 12 月 10 日。

所以這次選舉改變的不是「有沒有暫停」，**是暫停的結束條件。**

Hinojosa 競選網站的原話是：

> We need an immediate moratorium on data centers to last until the legislature can meet to put in place real protections

暫停要持續到議會開會、訂出真正的保護措施。SemiAnalysis 的讀法更嚴格（[Bloomberg 引述](https://businessmirror.com.ph/2026/11/04/ai-data-center-boom-seen-set-for-upheaval-after-us-elections/)）：

> she would impose a moratorium until legislation is passed that gives communities a voice

要等法案通過，而且法案要讓社區有發言權。

把兩邊放在一起：

| | Abbott 版 | Hinojosa 版 |
|---|---|---|
| 結束條件 | ERCOT 審計完成 | 議會立法 |
| 條件性質 | 技術 | 政治 |
| 最近的時間點 | 審計目標 12 月 10 日 | 會期 2027 年 1 月 12 日開議，5 月 31 日結束 |

審計有目標日，立法沒有。這才是投資人在定價的東西。GLJ 估計有電力但還沒拿到州環保許可的專案，[可能延宕 12 到 18 個月](https://businessmirror.com.ph/2026/11/04/ai-data-center-boom-seen-set-for-upheaval-after-us-elections/)。

## 把 474 GW 一層層扣掉

**第一層：排隊總量。** [ERCOT 的併網申請約 474 GW，約 90% 是資料中心](https://utilitydive.com/news/ercot-texas-puc-data-center-audit/828472)，也就是約 427 GW。德州[歷史最高尖峰是 91.1 GW（2026 年 7 月 22 日）](https://www.eia.gov/TODAYinENERGY/detail.php?id=67906)，排隊量是它的 5.2 倍。

這個數字看看就好。Utility Dive 引述專家的說法，其中相當部分可能是投機或重複申請。

**第二層：風險容量。** Bloomberg 引述 GLJ，[約 13 GW 直接暴露在風險中](https://businessmirror.com.ph/2026/11/04/ai-data-center-boom-seen-set-for-upheaval-after-us-elections/)。[Jefferies 估已宣布專案有 13.3 GW](https://huggingnews.com/us-politics/hinojosas-texas-governor-win-puts-133-gw-of-data-centers-at-risk-as-nasd-2974e9d0)，這個數字我只查到聚合站轉述，沒看到原報告。兩家的量級接近，所以下面用 13.3 GW 計算。

**第三層：最接近落地的。** 截至 8 月 20 日，[17 個大型用電戶、約 6.6 GW 只差最後的送電核准](https://utilitydive.com/news/ercot-texas-puc-data-center-audit/828472)，分約五年拉滿。這批是 Abbott 的審計卡住的，跟這次選舉無關。

## 算力比例怎麼算

市面上有一種說法：德州卡住的容量等於「全球現役算力 25–50%」。我查不到來源，所以自己算一次。

**Step 1：找全球分母。** 我找不到官方的 2026 年全球 AI 電力數字。[Epoch AI 估 2025 年底約 30 GW](https://epoch.ai/data-insights/ai-datacenter-power)，已經舊了快一年。比較新的線索是 [Epoch 追蹤的 86 座設施、約 13.3 GW IT 電力，約佔 2026 年 6 月全球已部署 AI 算力的 46%](https://cryptobriefing.com/epoch-ai-data-center-research-global-compute/)。

反推全球 IT 電力：

```
13.3 GW ÷ 46% ≈ 29 GW（IT 電力）
```

**Step 2：把 IT 電力換成總電力。** 分析師講的 GW 通常是總電力，要算上冷卻和其他設施損耗。我用兩個係數：

```
下緣：29 GW × 1.2（PUE 1.2）   ≈ 35 GW
上緣：29 GW × 1.52（Helios）   ≈ 44 GW
```

1.52 來自 [Helios 第一到第三期：800 MW 總電力對 526 MW IT 負載](https://blockspace.media/insight/galaxy-delivers-helios-to-coreweave/)。所以全球分母抓 **35–44 GW**。這跟 Epoch 2025 年底的約 30 GW 接得上。

**Step 3：算比例。**

| 分子 | 定義 | 佔 35–44 GW |
|------|------|:--:|
| 6.6 GW | 只差送電核准，分約五年拉滿 | 15–19% |
| 13.3 GW | 已宣布、可能受影響的專案（Jefferies） | 30–38% |
| [16.7 GW](https://huggingnews.com/us-politics/hinojosas-potential-texas-win-jeopardizes-133-gw-of-data-center-capacity-c4b72ac7) | 2028 年規劃容量（SemiAnalysis，二手來源） | 38–48% |

**Step 4：換算成 GPU。** [GB200 NVL72 一櫃 132 kW、72 張](https://supermicro.com/en/products/system/gpu/48u/srs-gb200-nvl72)，每張約 1.83 kW。同樣用 1.2 到 1.52 倍換算：

| 容量 | 粗估 GPU 張數 |
|------|:--:|
| 6.6 GW | 240–300 萬張 |
| 13.3 GW | 480–600 萬張 |

如果只除機櫃功耗、不算設施損耗，張數會高估 1.2 到 1.52 倍。

**這個比例的正確讀法是「規模相當於」，不是「佔了」。** 分子是未來幾年的新增，分母是今天的存量，把它說成「掐住了全球三成現役算力」是錯的。德州現役的機房還在正常運轉。

想看定義一致的比較，這兩個比較乾淨：[德州佔全美規劃資料中心容量 27%（Wells Fargo）](https://www.cnbc.com/2026/11/04/ai-stocks-texas-governor-data-centers.html)，以及[德州佔 2028 年全美容量接近 30%（SemiAnalysis）](https://businessmirror.com.ph/2026/11/04/ai-data-center-boom-seen-set-for-upheaval-after-us-elections/)。

## 延宕為什麼打到 Neo-cloud

Neo-cloud 的商業模式是借錢買卡、蓋機房，前提是晶片一落地就通電賺租金。

CoreWeave 今年的資金成本是最好的觀察點：

| 時間 | 融資 | 成本 |
|------|------|:--:|
| 3 月 | [85 億美元投資級 GPU 貸款](https://www.barchart.com/story/news/1061388/coreweave-closes-landmark-8-5-billion-financing-facility-achieving-first-investment-grade-rated-gpu-backed-financing) | 固定利率約 5.9% |
| 4 月 | [2031 年到期票據](https://www.pulse.bot/ai/deals/coreweave-issues-1b-of-975-senior-notes-e1ff4902-197e-45a1-8e60-d735fd4bf7ea/) | 票面 9.75% |
| 7 月 | [26 億美元貸款](https://ai2.work/blog/coreweave-s-10-4-loan-signals-lenders-are-repricing-ai-debt-risk) | 到期殖利率 10.44% |
| 10 月中 | [2032 年到期票據，票面 9.625%](https://www.metirai.com/blog/coreweave-bond-yields-15-percent-backlog-debt-oct-2026) | 次級市場殖利率一度衝到近 15%，價格跌破 80 美分 |

這四筆的擔保條件和信用等級都不同，不能直接當成同一條利率曲線。而且 15% 不是 CoreWeave 借錢的利率，是舊債跌價後市場要求的報酬。但它是在選前兩到三週就出現的訊號：**債市已經開始懷疑了。**

如果機房遲遲接不上電，利息還是每天照扣。一旦資金鏈斷裂，質押的晶片可能被迫拋售。這段是推演，不是現況，目前我沒查到有 Neo-cloud 因為德州暫停令違約。

已經發生的影響比較小，也比較具體。Galaxy 的 Helios 園區在西德州，[800 MW 全部由 CoreWeave 承租](https://datacenterdynamics.com/en/news/galaxy-secures-approval-for-more-than-800mw-at-helios-campus-in-texas)，第一期已經交付，[Rosenblatt 認為已核准的容量大致不受影響](https://blockspace.media/insight/galaxy-stock-buy-rating-helios-data-centers/)。但[已核准的 830 MW 二期還沒租出去](https://blockspace.media/insight/galaxy-drops-helios-ii-deal/)，部分潛在租戶想等德州的審查有結果再簽。

GLJ 有一句話講得最精準：

> Projects with power, permits and steel keep going

電力、許可、鋼材都到位的繼續蓋。Alphabet、Meta、Microsoft 當天多數上漲，大概也是這個邏輯：手上有現貨的人，稀缺反而是利多。

## 這修正了我之前寫過的一篇

9 月三家大當機時，我在[《Claude 先掛、Grok 跟著、ChatGPT 晚一小時》](/ai-triple-outage-shared-failure-domain/)寫過：故障域要看實體位置，不是看 vendor logo。

那篇只講了電力和機房，這次要補一層：**州政府也是故障域。**

機房壞了可以修。一個州的許可凍結，影響的是該州未來所有的新增容量，修理時間由議會會期決定，不是由工程師決定。

## 這具體改變了誰的什麼決策

**企業 CTO。** 之前選算力雲看的是單價和交期。現在合約談判要多問三題：新增容量在哪一州、併網和環保許可拿到了沒、對方的債務何時到期。一個單價最低但新增容量都押在德州、又靠高息債撐著的供應商，風險已經不是規格表看得到的。

如果你的推論全押在單一 Neo-cloud，先把回退路徑準備好，能切回大廠或地端。如果你本來就用三大雲的預留容量，這次的直接影響相對小。

**個人開發者。** 之前的選型邏輯是等 API 繼續降價。現在這個假設要打折。比較穩的做法是讓便宜模型先扛掉能扛的工作，例如 Flash 系列或開源小模型，把旗艦模型留給真正複雜的推理。這本來就該做，算力吃緊只是讓偷懶的代價變高。

**雲端模型不穩定這件事。** 我的體感是模型時不時變笨。如果算力更吃緊，固定跑一組小測試（像是畫鵜鶘這種），隨時準備換供應商，可能會變成常態。但「服務商為了省算力偷偷降規格」外面很難證明，[Anthropic 在 2025 年 9 月的事後檢討就否認因需求、時段或伺服器負載而降低模型品質](https://www.infoq.com/news/2025/10/anthropic-infrastructure-bugs)。所以我只把它當成要監控的風險，不當成已知事實。

至於地端，我在 [RTX Pro 6000 一週實驗](/rtx-pro-6000-tier1-week-final-offload-qwen-vl-vllm/)裡的動機原本是隱私和成本。9 月的大當機多了故障域這個理由，這次又多一個：在不確定的時候，手上掌握一點確定性。

## 反方：這篇可能高估了

最強的反駁有三個。

**第一，需求會搬家。** GLJ 自己就說，沒拿到條件的專案「probably go to Louisiana, Oklahoma or nowhere」。德州少蓋不等於全球少蓋。BloombergNEF 選前估德州暫停影響[將近 50 GW，佔全美 253 GW 管線將近兩成](https://www.cnbc.com/2026/09/21/texas-governor-abbott-ai-data-center-permits.html)，換句話說，還有八成在別的地方。我的回應：搬家要時間，而且 [Bloomberg 估民主黨這波勝選可能影響約一半的美國 AI 資料中心新增提案](https://businessmirror.com.ph/2026/11/04/ai-data-center-boom-seen-set-for-upheaval-after-us-elections/)，能搬的地方也在變少。但「nowhere」和「晚一年」的差別很大，我沒有數字能分辨。

**第二，爆雷可能讓算力變便宜。** 如果 Neo-cloud 真的斷鏈、晶片被拋售，短期市場上的 GPU 反而變多。這跟「算力一定漲價」是矛盾的。我的回應：短期可能便宜，但蓋好的機房和接好的電不會跟著變多，能不能通電才是瓶頸。這點我沒有資料證明，所以「算力漲價」我只敢說可能性變高。

**第三，廠商有空間吸收成本。** 我在[巴克萊利潤鏈那篇](/barclays-ai-profit-chain-cloud-tax-inference-margin/)寫過，付費推理利潤率已經到 50% 到 65%。成本上升不一定會轉嫁給客戶。所以真正會漲價的機制，可能要看供給是否緊到讓廠商不必降價，而不是成本本身。

## 坦白說

這篇的核心比例是我算的，不是任何機構公布的。

分母有三個洞：46% 指的是算力佔比，我直接當成電力佔比，新機房效率較高，這會有偏差；46% 是 6 月的數字，Epoch 設施清單的時點卻標到 9 月，兩者可能對不齊，也可能混到部分興建中的容量；而且算力成長很快，到今天分母更大，比例會更低。

分子也不乾淨。13.3 GW 我查不到原始報告，也不確定它是總電力還是 IT 電力。

政治這邊更不確定。我查不到州長能不能單獨下全州暫停令的法律分析，也查不到選後州議會的席次。Hinojosa 當初是要求 Abbott 用行政命令暫停，但她上任後實際會怎麼做，目前只有競選承諾。**如果議會很快立法，暫停可能比市場擔心的短。**

市場本身也沒有恐慌到底：期貨當天就收復大半，Nasdaq 100 在選前的 10 月底就已經進入修正，這次下跌不能全算在德州頭上。

但有一件事我比較有把握：474 GW 的新聞標題幾乎沒有決策價值，真正要追的是那 6.6 GW 什麼時候拿到送電核准。

## 關鍵洞察

**看條件，不要看標題。** 下兩個觀察點是 12 月 10 日的 ERCOT 審計，以及 2027 年 1 月 12 日開議的立法會期。前者決定 Abbott 版的暫停能不能結束，後者決定 Hinojosa 版的暫停何時結束。

**算力風險要問到州。** 問供應商的新增容量在哪裡、許可拿到了沒。問不到答案，就當作你的供應鏈裡有一個自己看不到的故障域。

**便宜的工作流先做。** 不管德州最後怎麼走，把便宜模型扛得住的工作移過去、把回退路徑測過一次，這兩件事都不會白做。

AI 這波狂潮不會輸給模型不夠聰明，但可能先被變壓器、議會會期和衝到 15% 的債券殖利率上一課。

---

## 常見問題 Q&A

**Q: 德州的資料中心暫停令是 Gina Hinojosa 下的嗎？**

不是。現行的暫停是現任共和黨州長 Greg Abbott 下的：2026 年 8 月 3 日要求暫停新資料中心併網，9 月 21 日要求德州環境品質委員會（TCEQ）暫停相關許可，直到德州電網營運商 ERCOT 完成審計，審計目標日是 2026 年 12 月 10 日。Hinojosa 的競選承諾是暫停到議會立法，差別在結束條件，而不是有沒有暫停。

**Q: 德州卡住的資料中心容量相當於全球 AI 算力多少？**

作者依 Epoch AI 資料估算，2026 年 6 月全球 AI 資料中心總電力（Total Facility Power）約 35–44 GW。只差送電核准的 6.6 GW 規模相當於其中 15–19%，分析師估的 13.3 GW 風險容量相當於 30–38%。這些都是未來幾年的新增容量，不是現役算力被關掉，所以應讀成「規模相當於」，不是「佔了」。

**Q: ERCOT 的 474 GW 排隊量是真實需求嗎？**

不完全是。474 GW 是德州電網營運商 ERCOT 的大型用電併網申請（Large Load Interconnection）總量，約 90% 是資料中心，是德州 91.1 GW 歷史尖峰的 5.2 倍。Utility Dive 引述專家說，其中相當部分可能是投機或重複申請。比較接近落地的數字是 17 個大型用電戶、約 6.6 GW，它們截至 2026 年 8 月 20 日只差送電核准，且要分約五年拉滿。

**Q: CoreWeave 真的是用 15% 的利率借錢嗎？**

不是。近 15% 是 CoreWeave 2032 年到期票據在次級市場的殖利率（Yield），2026 年 10 月中一度衝到這個水準，該票據的票面利率是 9.625%。CoreWeave 2026 年新融資的成本約在 5.9%（3 月投資級 GPU 貸款）到 10.44%（7 月貸款的到期殖利率）之間。殖利率衝高代表債市要求更高的風險補償，但不等於公司實際付出的利息。

**Q: 這件事對企業使用 AI 推論有什麼實際影響？**

短期不會讓現有服務停擺，德州現役機房仍在運轉。比較實際的影響是新增容量的不確定性變高，尤其是新增容量集中在德州、又依賴高息債的算力雲（Neo-cloud）。可以做的事有兩件：向供應商確認新增容量的州別與許可狀態，以及把便宜模型能處理的工作移過去，並測過一次切回大廠或地端的回退路徑。

---

## 資料來源

- [Bloomberg（BusinessMirror 轉載）：AI data center boom seen set for upheaval after US elections](https://businessmirror.com.ph/2026/11/04/ai-data-center-boom-seen-set-for-upheaval-after-us-elections/)
- [CNBC：AI data center stocks decline as Texas governor result raises risks](https://www.cnbc.com/2026/11/04/ai-stocks-texas-governor-data-centers.html)
- [CNBC：Abbott orders data center permit halt](https://www.cnbc.com/2026/09/21/texas-governor-abbott-ai-data-center-permits.html)
- [Utility Dive：ERCOT data center audit](https://utilitydive.com/news/ercot-texas-puc-data-center-audit/828472)
- [Gina Hinojosa 競選網站：Data Centers](https://ginafortexas.com/priority/data-centers/)
- [Yahoo Finance：Democrat won the Texas governor's race](https://finance.yahoo.com/economy/article/a-democrat-won-the-texas-governors-race-after-promising-to-halt-new-data-center-construction-044536389.html)
- [Unite.AI：Data center policy fears hit AI stocks](https://www.unite.ai/data-center-policy-fears-hit-ai-stocks-after-hinojosas-texas-win/)
- [EIA：ERCOT 尖峰負載紀錄](https://www.eia.gov/TODAYinENERGY/detail.php?id=67906)
- [Epoch AI：AI data center power](https://epoch.ai/data-insights/ai-datacenter-power)
- [Crypto Briefing：Epoch AI 資料中心研究](https://cryptobriefing.com/epoch-ai-data-center-research-global-compute/)
- [Supermicro：GB200 NVL72 規格](https://supermicro.com/en/products/system/gpu/48u/srs-gb200-nvl72)
- [DCD：Galaxy Helios 核准](https://datacenterdynamics.com/en/news/galaxy-secures-approval-for-more-than-800mw-at-helios-campus-in-texas)
- [Blockspace：Helios 交付 CoreWeave](https://blockspace.media/insight/galaxy-delivers-helios-to-coreweave/)
- [Blockspace：Rosenblatt 評 Helios](https://blockspace.media/insight/galaxy-stock-buy-rating-helios-data-centers/)
- [Blockspace：Helios II 租約](https://blockspace.media/insight/galaxy-drops-helios-ii-deal/)
- [Barchart：CoreWeave 85 億美元投資級融資](https://www.barchart.com/story/news/1061388/coreweave-closes-landmark-8-5-billion-financing-facility-achieving-first-investment-grade-rated-gpu-backed-financing)
- [Pulse：CoreWeave 9.75% 票據](https://www.pulse.bot/ai/deals/coreweave-issues-1b-of-975-senior-notes-e1ff4902-197e-45a1-8e60-d735fd4bf7ea/)
- [AI2.work：CoreWeave 10.44% 貸款](https://ai2.work/blog/coreweave-s-10-4-loan-signals-lenders-are-repricing-ai-debt-risk)
- [Metir AI：CoreWeave 債券殖利率](https://www.metirai.com/blog/coreweave-bond-yields-15-percent-backlog-debt-oct-2026)
- [InfoQ：Anthropic 基礎設施 bug 事後檢討](https://www.infoq.com/news/2025/10/anthropic-infrastructure-bugs)
- [HuggingNews：期貨收復跌幅](https://huggingnews.com/us-politics/us-stock-futures-erase-drop-over-texas-governor-flip-and-data-center-fre-6bc2bd1d)
- [HuggingNews：Jefferies 13.3 GW](https://huggingnews.com/us-politics/hinojosas-texas-governor-win-puts-133-gw-of-data-centers-at-risk-as-nasd-2974e9d0)
- [HuggingNews：SemiAnalysis 16.7 GW](https://huggingnews.com/us-politics/hinojosas-potential-texas-win-jeopardizes-133-gw-of-data-center-capacity-c4b72ac7)
