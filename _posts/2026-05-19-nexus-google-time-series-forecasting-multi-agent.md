---
layout: post
title: "預測未來，不只需要歷史 — Google Nexus 論文把 Agent 塞進時間序列"
date: 2026-05-19 07:30:00 +0800
permalink: /nexus-google-time-series-forecasting-multi-agent/
image: /assets/images/nexus-google-time-series-forecasting.png
description: "Google 跟 Penn State 的 Nexus 論文用四個專職 Agent — Event Extractor、Macro Regime Reader、Local Shock Tracker、Synthesizer — 把時間序列預測拆成可解釋的多 Agent 流程，在 Zillow 房地產資料集把 MAPE 比直接 CoT prompting 砍掉 86.6%。但測試樣本窄、單次評估、沒有成本分析，這是值得偷學架構但不是可以直接搬去生產的配方。"
---

![Nexus: An Agentic Framework for Time Series Forecasting](/assets/images/nexus-google-time-series-forecasting.png)

我一直覺得，時間序列預測是一個被低估的「AI Agent 戰場」。

不是因為它技術上有多複雜——ARIMA 用了幾十年，Prophet 也很成熟——而是因為它有一個根本上的思維盲點：

**它只問「過去發生了什麼」，從不問「為什麼發生」。**

Google 跟賓州州立大學最近發表的 Nexus 論文（[arxiv 2605.14389](https://arxiv.org/abs/2605.14389)），正面挑戰了這個假設。

結果很有趣。數字很驚人。但我的疑慮也不少。讓我老實跟你說。

---

## 問題的本質：曲線背後有故事，但模型看不懂故事

傳統時間序列模型——不管是 ARIMA、Prophet，還是這幾年很熱的 Time Series Foundation Models（TSFM，比如 TimesFM、Moirai）——它們的共同特徵是：

**它們讀數字，不讀故事。**

拿房地產來說。2020 年疫情初期，美國某些城市的房屋庫存曲線突然暴跌。從數字上看，這是一個異常點。但 TSFM 不知道背後發生了什麼：封城、供應鏈斷裂、房東觀望心態。

然後 2021 年，曲線反彈。TSFM 可能把這解讀成「季節性回升」，但實際上是利率超低、遠端工作浪潮、移民潮同時出現。

**有些模式是事件造成的，不是時間造成的。**

這是 Nexus 論文開宗明義的第一句話，也是我覺得最精準的一句話。

那 LLM 呢？LLM 知道這些事件。它看過新聞、看過 Fed 會議記錄、看過分析師報告。它可以告訴你「2021 年 Q2 房地產反彈的三大驅動因素」。

但 LLM 不會跑時間序列。它沒有數值計算的訓練，也沒有序列建模的架構。

**這就是問題的核心：** 懂故事的不懂數字，懂數字的不懂故事。

---

## Nexus 怎麼處理這個問題？

Nexus 的答案不是「讓 LLM 直接預測」，也不是「讓 TSFM 讀新聞」。

它的做法是：**把預測這件事，拆成四個專職 Agent，讓它們各司其職，最後合成。**

這個思路我之前在 AgentOpt 論文裡看過類似的影子——最強的模型放在最重要的位置，不一定得到最好的結果。分工的設計，比選哪個模型更重要。

Nexus 的四個 Agent：

**1. 事件整理員（Event Extractor）**

把混亂的歷史文本——新聞、公告、研究報告——整理成乾淨的事件時間軸。它的工作只有一件：把「文字時間」轉換成「事件時間線」。不預測，不解讀，只整理。

**2. 宏觀觀察員（Macro Regime Reader）**

讀的是大格局：這個市場現在處於什麼「體制」（regime）？擴張期？衰退期？政策轉向期？它不管細節，只判斷「現在是哪種時代」。

**3. 微觀追蹤員（Local Shock Tracker）**

追蹤局部衝擊：某個城市的特殊事件、某支股票的 earnings 驚喜、某個地區的供應鏈斷裂。它關注的是「這件事，為什麼跟大趨勢不一樣」。

**4. 合成員（Synthesizer）**

把前三個 Agent 的輸出，加上過去預測的誤差記錄，合成最終預測。它不只整合資訊，還會根據「過去我在哪些情況下預測錯了」來校正自己的信心。

---

## 數字：86.6% 是什麼等級的改善？

論文在 Zillow 房地產數據集上，比較了 Nexus 跟幾種基準做法的誤差（MAPE）：

- **vs direct chain-of-thought prompting（Claude）：降低 86.6%**
- vs state-of-the-art TSFM：持平或更好

86.6% 的 MAPE 降低，換個方式理解：如果原本預測誤差是 10%，Nexus 把它壓到大概 1.4%。這是一個很誇張的改善幅度。

不過這裡有個關鍵：比較基準是「direct CoT prompting」。

也就是說，他們比的是「用一個 Prompt 叫 Claude 直接預測」vs「用四個 Agent 分工再合成」。

這個比較本身是公平的——它在回答「結構化多 Agent 比單一 CoT 好多少」這個問題。但它沒有告訴你「跟最好的傳統 TSFM 相比，到底贏在哪」。

那個數字，論文說是「持平或更好」，但沒有給出一個漂亮的單一數字。

---

## 坦白說：我有哪些疑慮

我覺得 Nexus 的架構思路是對的，但論文本身承認了幾個限制，我覺得值得放在這裡說清楚：

**限制一：測試集很窄。**

Zillow 房地產指標 + 7 支股票。這是 2 個領域、大概幾十個時間序列。對於一篇想要「顛覆預測範式」的論文，這個樣本量算小。

**限制二：單次評估（single-run evaluations）。**

沒有跑多次取平均。LLM 的輸出本來就有隨機性，單次評估的方差會很大。

**限制三：Post-cutoff 數據。**

數據是在 LLM 的訓練截止點之後產生的——這是為了避免模型「記住答案」。這個設計很誠實，但也代表測試條件是特意選的最嚴格場景，不一定代表真實部署的平均表現。

**限制四：沒有成本分析。**

四個 Agent 跑完，token 消耗是多少？延遲是多少？這些數字都沒有。如果比直接 CoT 貴 10 倍，那 86.6% 的改善還合算嗎？視應用場景而定。

這些不是要否定論文，而是在說：**這是一個很有潛力的方向，但還不是一個你可以直接拿去生產的配方。**

---

## 對 AI 工程師最有用的啟示

把 Nexus 的論文結果放在一邊，它在架構設計上的思路，其實很值得偷學：

**1. 把「做什麼」和「怎麼解讀」拆開。**

Nexus 的 Event Extractor 只整理事實，不解讀。Macro Reader 只判斷體制，不預測。分工越清晰，每個 Agent 的 Prompt 越精準，失焦的可能性越低。

這跟我之前說的 AgentOpt 結論是一致的：角色定義比模型選擇更重要。

**2. 校正是一種 memory。**

Synthesizer 會讀「過去我在哪裡預測錯了」然後調整信心。這不是什麼特別新的概念，但在時間序列這個場景裡，它讓 Agent 有了一種「從失敗中學習」的機制——不需要 fine-tuning，只需要把誤差記錄餵進 context。

**3. 一個 Prompt 做完所有事，通常不是最好的設計。**

這是 Nexus 最核心的主張，也是整個論文能做到 86.6% 改善的原因。

一個 Prompt 要同時：整理歷史文本 + 判斷宏觀體制 + 追蹤局部衝擊 + 合成預測 + 根據過去誤差校正——這對 LLM 來說太多了。每增加一個任務，其他任務的注意力就被稀釋。

**結構幫助 LLM 使用 context，而不是讓它在 context 裡迷失。**

這句話，是論文裡我覺得最有份量的一句。

---

## 更大的方向：未來的預測師，不只外推曲線，還要辯論「是什麼讓曲線移動」

論文最後的結論，我覺得說得很好：

> 未來的預測，不只是外推曲線，而是討論「是什麼讓曲線移動」。

這個方向，我相信是對的。

不管是房地產、股票、還是電商銷量——純粹的數值模型，在事件驅動的波動面前，永遠有它的天花板。把「事件理解」接進來，是必然的趨勢。

Nexus 提供了一個值得參考的架構藍圖。不是最終答案，但可能是一個好的起點。

---

## 結語

我沒有在生產環境跑過 Nexus。這篇文章是基於論文分析，不是實戰數據。

但我認為它的架構思路是對的，值得在你的下一個預測專案裡借鑒「分工 + 角色專職化 + 誤差校正記憶」這三個設計原則。

至於 86.6% 這個數字——記得加上一句「在特定測試條件下」。

---

**論文資訊：**
- **標題：** Nexus: An Agentic Framework for Time Series Forecasting
- **作者：** Sarkar Snigdha Sarathi Das, Palash Goyal, Mihir Parmar 等（Google + Penn State）
- **arXiv：** [2605.14389](https://arxiv.org/abs/2605.14389)
- **發表：** 2026年5月14日

**延伸閱讀：**
- [AgentOpt：貴模型放錯位置，反而比便宜模型差](/agentopt-expensive-model-wrong-position-pipeline-optimization/)
- [Agent 模式 Part 3：Deep Research 架構探討](/agent-mo-shi-part-3-deep-research-architecture/)
- [多 Agent 的結構性不穩定性](/agents-of-chaos-multi-agent-structural-instability/)
