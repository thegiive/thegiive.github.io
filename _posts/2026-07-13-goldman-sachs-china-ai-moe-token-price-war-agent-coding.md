---
layout: post
title: "高盛 50 頁報告的題眼：中國模型每個 Token 只點亮 3-5% 的參數，所以 Agent 和 Coding 的市占已經拿下了"
date: 2026-07-13 09:00:00 +0800
permalink: /goldman-sachs-china-ai-moe-token-price-war-agent-coding/
description: "高盛 Ronald Keung 團隊 7 月初發布約 50 頁中國 AI 模型深度報告。核心數字：中國頭部編程模型混合 token 價格約 $1/百萬 token，美國 SOTA 是 $4-8；DeepSeek V4 Pro 在 1.6T 總參數中只激活 49B，GLM 5.2 在 744B 中只激活 40B——每個 token 激活不到總參數的 8%。結果已經在 OpenRouter 上體現：中國模型占 agent token 的 85%、代碼 token 的 89%。GS 測算這些模型目前 EBIT 利潤率是 -30% 到 -39%，靠現金硬扛，預計 2030 年轉正。這篇拆解架構如何決定定價下限、定價下限如何決定場景歸屬，以及這對你選模型的實際影響。"
image: /assets/images/goldman-sachs-china-ai-token-cover.png
categories: [AI 產業分析]
author: Wisely Chen
---

高盛亞洲互聯網研究主管 Ronald Keung 團隊 7 月初發了一份約 50 頁的報告，標題問的是「誰會是中國 AI 大模型產業的長期贏家」。

報告裡的數字很多，但真正的題眼只有一條邏輯鏈：

**低激活比例 + 低利潤率定價 → 拿下 token 密集型場景 → 拉低全行業混合 token 均價。**

不是品質、不是品牌、不是生態——是更激進的稀疏架構加上虧損定價策略，決定了誰拿走哪塊市場。

---

## 30 秒定位：關鍵數字總覽

| 項目 | 中國頭部模型 | 美國 SOTA |
|------|-------------|-----------|
| 混合 token 價格 | ~$1/百萬 token（GLM 5.2、Qwen 3.7 Max） | $4-8/百萬 token |
| 每 token 激活參數占比 | 3-5%（DeepSeek V4 Pro: 49B/1.6T；GLM 5.2: 40B/744B） | 未公開（同為 MoE，但激活比例普遍較高） |
| Agent token 市占（OpenRouter） | 85% | — |
| 代碼 token 市占（OpenRouter） | 89% | — |
| EBIT 利潤率（GS 測算，當前） | Agentic: -30%；Coding: -39% | — |
| EBIT 利潤率（GS 預測，2030） | Agentic: +14%；Coding: +22% | — |

---

![架構決定成本：知識的儲存與調用分離](/assets/images/goldman-sachs-china-ai-moe-architecture.png)

## 架構決定成本：不是 MoE vs Dense，是激活比例的差距

先釐清一個常見誤解：MoE 不是中國模型的專利。GPT-4 開始 OpenAI 就被廣泛認為使用 MoE，GPT-5 系列幾乎確定是 MoE，Google 的 Gemini 同樣是。**現在 Dense 才是少數派。**

所以問題不是「中國用 MoE、美國用 Dense」——大家都在用 MoE。真正的差異在於：**中國頭部模型把激活比例壓得更低。**

拿 DeepSeek V4 Pro 舉例。它有 1.6T 個參數，384 個路由專家加 1 個共享專家，每個 token 只激活其中 6 個路由專家。結果：每個 token 實際計算量只有 49B 參數的規模——**總參數的 3.06%**。

GLM 5.2 同樣是 744B 總參數，256 個專家中激活 8+1 個，每 token 激活 40B——**總參數的 5.4%**。

GS 報告的數字是：中國頭部模型全線激活比例不到 8%。這意味著什麼？FLOPs 跟激活參數成正比。你用一個 1.6T 的模型，但每個 token 的推理成本只相當於一個 49B 模型。模型的「知識」來自 1.6T，模型的「帳單」按 49B 算。

但激活比例低只是成本方程式的一層。4-8 倍的價差背後其實是三層結構疊在一起：

**第一層：架構激進度。** 中國模型激活 3-5%，大家都用 MoE 但中國壓得更低，這帶來的成本優勢大概是 2-3 倍。

**第二層：要素成本與財政補貼。** 這是 GS 報告沒有深入展開、但可能是最被低估的一層。逐項拆開看，每一項的真實貢獻其實不一樣：

- **人才**：中國 AI 工程師平均年薪約 45.5 萬人民幣（約 [$63k](https://www.glassdoor.com/Salaries/china-ai-engineer-salary-SRCH_IL.0,5_IN48_KO6,17.htm)），矽谷 AI/ML 工程師是 $170-245k——中位對中位大約 1/3 到 1/5。這對訓練和研發成本的攤銷影響很大。
- **電力**：基準工業電價中美其實差距不大（中國 0.62-0.81 元/kWh，約 $0.086-0.113，跟美國工業平均價在同一個量級）。真正的優勢在定向補貼：[甘肅、貴州、內蒙把 AI 資料中心電價砍半到 0.4 元/kWh](https://triviumchina.com/2025/11/06/china-subsidizes-power-for-ai-data-centers/)（約 $0.056），而且**用 NVIDIA/AMD 晶片的設施不能享受**——電價補貼是綁定國產晶片的政策工具。但要誠實講：電力只佔推理成本的 10-20% 左右，GPU 折舊才是大頭，所以電力優勢是真的，對 token 價差的直接貢獻卻沒有直覺想的大。
- **財政補貼**：這才是最大的真金白銀。[算力券已經鋪開到北京、上海、深圳、成都等城市](https://www.tomshardware.com/tech-industry/artificial-intelligence/china-subsidizes-ai-computing-for-small-domestic-companies-computing-power-vouchers-spread-across-multiple-chinese-cities)，上海一地發了 6 億人民幣、覆蓋最高 80% 的算力租用費。GS 測算的 -30%/-39% 虧損為什麼撐得住？有一部分實際上是地方財政在吸收。

一個常見的誤解要在這裡拆掉：**「華為昇騰比 H100 便宜」是錯的。** [910C 單價約 18-20 萬人民幣（$25-28k）](https://www.trendforce.com/news/2025/03/13/news-huaweis-ascend-910c-takes-on-nvidia-as-chinas-ai-race-heats-up-more-alleged-details/)，跟 H100 的 $25-30k 幾乎一樣；但性能只有 H100 的約 80%，die 面積反而大 60%，[SMIC 7nm 良率約 40%](https://www.digitimes.com/news/a20250225PD224/huawei-ascend-ai-chip-yield-rate.html)（行業標準是 60%）。換算 per-FLOP 成本，昇騰可能比 H100 更貴。GLM 5.2 用 10 萬張昇騰、零 NVIDIA 訓練出來，這件事的價值不是省錢——**是不會被斷供。全產業鏈自主買的是安全，不是成本。**

**第三層：定價策略。** 美國 SOTA 模型定價 $4-8/百萬 token，裡面包含了高毛利（OpenAI 的 API 毛利率被估計在 50% 以上）；中國模型定價 $1 甚至更低，GS 測算是虧損狀態。一邊在賺錢，一邊在貼錢搶市場。

**三層疊起來才有 4-8 倍的價差。** 架構是一層（真實、可持續），人才和補貼是一層（人才真實、補貼看財政意願），定價意願是一層（隨時可以收）。即使補貼結束、定價回歸理性，架構和人才的優勢不會消失——但硬體那一項，在昇騰追平 NVIDIA 的能效之前，其實是中國廠商在成本上的逆風，不是順風。

---

## 成本決定定價：先虧錢，後收割

GS 報告把中國模型市場分成兩層：

- **高端層**：GLM 5.2、Qwen 3.7 Max，混合 token 價格約 $1/百萬 token
- **低端層**：DeepSeek V4 Flash 等，價格壓到 $0.06-0.2/百萬 token

對比美國 SOTA 模型的 $4-8，價差是 4 到 8 倍。低端層的價差甚至到 40 倍以上。

但報告同時指出，這個定價是虧的。GS 測算，主打性價比的 agentic 模型目前 EBIT 利潤率為 -30%，編程模型為 -39%。靠的是現金充裕的資產負債表——背後是阿里巴巴、字節跳動、騰訊這些「母體」的彈藥。

這裡用 EBIT（Earnings Before Interest and Taxes，稅息前利潤）而不是 EBITA 或 EBITDA，是一個值得注意的選擇。三者的差別在於「幫你加回多少成本」：

- **EBIT** = 營收 - 營運成本 - 訓練攤銷（最嚴格，虧就是虧）
- **EBITA** = 把訓練攤銷加回來，當作沒這筆帳（數字好看一些）
- **EBITDA** = 再把硬體折舊也加回來（數字最好看）

如果 GS 用 EBITA 算，-30% 可能變成 -15%；用 EBITDA 可能更接近打平。但 GS 選了最嚴格的 EBIT——訓練一個 1.6T 參數模型花的錢，每年攤到帳上，虧就是虧，不幫你美化。**投行報告用 EBIT 而不是 EBITDA，等於沒有幫中國模型廠商遮醜，這些虧損數字是真的。**

GS 的模型預測，這些虧損到 2030 年分別轉正至 +14% 和 +22%。邏輯是：token 消耗量會以 25 倍的速度成長（從 2026 年日均 350 兆 token 到 2030 年 4600 兆），但單位成本會持續下降，量起來之後毛利翻正。

中國互聯網公司做這種「先虧損搶市占，後靠規模效應翻正」的生意，不是第一次。滴滴、美團、拼多多都走過這條路。差別在於，**這次的價格下限不只是燒錢意願，而是有 MoE 架構做結構性支撐。**即使停止補貼，成本結構本身就比 Dense 低。

---

![定價決定歸屬：單任務成本觸發的市場翻轉](/assets/images/goldman-sachs-china-ai-market-share.png)

## 定價決定場景歸屬：Agent 和 Coding 已經被拿下

GS 報告引用 OpenRouter 的數據畫出一張很清晰的圖：

按支出算，中國模型只占 5-16%——因為單價低，花一樣的錢買到更多 token。但按 token 消耗量算，中國模型占 agent token 的 85%、代碼 token 的 89%。

這個差距本身就說明了一切：**凡是 token 消耗量大到讓「單任務成本」變成關鍵指標的場景，中國模型都在贏。**

Agent 和 coding 恰好是這種場景。一個 coding agent 跑一個任務動輒幾百萬 token，一個 agentic 工作流一天的 token 消耗是普通對話的上百倍。GS 報告引用的數據是：一個軟體開發 agent 每天消耗約 709 萬 token，成本 $13；一個客服語音 agent 每天 $92。

當任務成本從「可忽略」變成「需要算帳」，4 倍到 8 倍的價差就不是「省一點錢」的問題，而是「能不能規模化部署」的問題。$13 一天你可以跑 100 個 agent，$52-104 一天你只能跑 25 個。

結果已經體現在混合 token 價格指數上。Silicon Data 的 LLM Token Expenditure Index（SDLLMTK），這是一個追蹤全行業混合 token 均價的指數，6 月初見頂於約 2.07 美元/百萬 token，到 7 月上旬已經回落到約 1.67。中國模型的大量 token 消耗把整個行業的加權均價往下拉了。

---

![實務決策：能力不等於最佳位置](/assets/images/goldman-sachs-china-ai-pipeline.png)

## 這跟 AgentOpt 論文的交叉驗證

這個 blog [四月寫過 AgentOpt 論文](/agentopt-expensive-model-wrong-position-pipeline-optimization/)的一個關鍵發現：在 agent pipeline 裡，把最貴的模型放在 Planner 位置，效果反而最差。Ministral 8B（Opus 價格的三十三分之一）當 Planner + Opus 當 Solver，準確率比 Opus 全包高了 42 個百分點。

那篇講的是「能力不等於最佳位置」。GS 報告從產業面補上了另一半論證：**價格結構正在決定哪些模型能佔據哪些位置。**

Agent pipeline 通常有多個環節：planning、tool calling、code generation、verification。不是每個環節都需要 frontier 能力，但每個環節都會消耗 token。當中國 MoE 模型在 coding 和 agentic 場景拿下 85-89% 的 token 消耗，意味著實際部署中，pipeline 裡的多數環節已經被換成了低成本模型。

這不是理論推演，是 OpenRouter 上已經發生的事。

---

## 對出口管制敘事的修正

這個 blog [上週寫過](/ai-lockdown-era-china-us-dual-export-control/)中美 AI 出口管制的雙向夾擊——美國管中國的晶片，中國可能管自己的模型出口。那篇的結論是「越動態的環境，越需要確定性的東西——地端知識庫加地端 AI」。

GS 報告給這個敘事加了一個之前沒充分考慮的維度：**即使管制限制了模型的跨境流動，成本結構的優勢已經透過 API 定價滲透進全球開發者的工作流了。**

OpenRouter 上 89% 的代碼 token 來自中國模型，這些 token 不需要模型權重跨境——API 調用就夠了。出口管制可以鎖住權重下載，但鎖不住 API 調用（除非你願意封 IP，那是另一個等級的事情）。價格優勢的傳導機制，比權重開源更難管制。

---

## 對不同角色的決策影響

**企業 CTO / 架構師：**

Before：「我們用 Opus/GPT 做所有 agentic 任務，因為它最強。」
After：「我需要把 pipeline 拆開，每個環節獨立評估。高思考密度的環節用 frontier，高 token 消耗的環節用 MoE 模型。」GS 的數據顯示，走混合路線的企業在 agent 場景的成本可以降到純 frontier 方案的 1/4。

**個人開發者：**

Before：「中國模型便宜但能力差，正式專案不敢用。」
After：GLM 5.2 在 FrontierSWE 只差 Opus 一個百分點（[之前的文章](/glm5-it-architecture-huawei-ascend-moe-infrastructure/)有拆過這個數字），而 token 價格是 Opus 的 1/5 到 1/8。如果你在跑 agent 任務，光是 token 帳單的差異就可能決定你能不能把一個 side project 撐過原型階段。

---

## 坦白說

GS 報告裡的 EBIT 利潤率（-30%、-39%）和 2030 年轉正預測（+14%、+22%），是高盛自己的模型測算，不是實際財報數字。這些模型依賴的假設——token 消耗量 25 倍成長、單位成本持續下降、競爭格局不發生劇變——每一個都有可能不成立。

OpenRouter 的數據有代表性問題。OpenRouter 是一個 API 路由平台，用戶以開發者和小型團隊為主，大企業通常直接走模型廠商的 API。85% 和 89% 這兩個數字反映的是「對價格敏感、有能力自己切換模型的開發者群體」的選擇，不是全行業的市占率。

另一個這篇沒展開的變數是品質。中國模型在 benchmark 上追上美國 frontier 模型，但在長鏈推理、複雜 debugging、跨文件重構這些「真正燒 frontier 能力」的任務上，差距是否真的只剩一個百分點，沒有大規模獨立評測能確認。GS 報告也沒有做這個層級的品質分析——它是一份投行報告，關注的是市場結構和盈利模型，不是工程評測。

---

## 關鍵洞察

1. **4-8 倍的價差是三層結構疊出來的，但每層的持續性不同。** 架構（激活 3-5%）和人才（薪資 1/3-1/5）是可持續的真實優勢；財政補貼（算力券覆蓋 80% 租用費、定向電價減半）是真金白銀但看財政意願；虧損定價隨時可以收。至於硬體——昇騰 per-FLOP 成本可能比 H100 更貴，它買的是供應鏈安全不是成本優勢。做成本規劃時，不要假設價差會收斂到 1-2 倍，但也不要把 4-8 倍全當成永久結構——比較穩的估計是架構加人才撐起的 2-3 倍長期存在。

2. **「佔支出的 5-16%，佔 token 的 85-89%」這組數字本身就是判斷工具。** 它告訴你：在 token 密集型場景，市場已經用腳投票了。如果你的 pipeline 裡有任何環節的 token 消耗量大到讓成本成為瓶頸，現在就該測試中國模型，而不是等「品質追上」——GS 的數據顯示，很多場景它們已經追上了。

3. **投行開始把「token 價格」當成一個有自己指數的資產類別來追蹤了。** SDLLMTK 從 2.07 跌到 1.67，背後是整個行業的定價權正在從 frontier 模型廠商手裡轉移出去。這對 API 定價策略、agent 部署的 ROI 計算、甚至模型選型的決策框架，都有直接影響。
