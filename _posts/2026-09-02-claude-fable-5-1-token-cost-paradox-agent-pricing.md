---
layout: post
title: "Intelligence Index 66 分登頂：Fable 5.1 是目前最強的模型，成本帳怎麼算"
date: 2026-09-02 09:00:00 +0800
permalink: /claude-fable-5-1-token-cost-paradox-agent-pricing/
tags: [Anthropic, Claude, Fable 5.1, Mythos 5.1, Intelligence Index, cache read, token cost, per-task cost, Artificial Analysis, agent pricing, thinking block, anti-distillation]
categories: [AI 產業分析]
image: /assets/images/fable-5-1-cost-paradox-cover.png
description: "Anthropic 9 月 1 日發布 Fable 5.1，Artificial Analysis Intelligence Index 66 分登頂，Terminal-Bench Science 從 24.7% 翻倍到 52.6%，把 Opus 5、GPT-5.6 Sol、Grok 4.6 全部壓在後面。同時 cache read 降價 75%（$1 → $0.25/M token），對 agent 工作流省 25-45%。但 Artificial Analysis 測出 per-task cost 反而貴了 20%——因為模型更話多，output token 量漲 1.7 倍。這篇攤開能力帳和成本帳，看目前最強模型的真實代價。"
author: Wisely Chen
faq:
  - question: "Fable 5.1 到底是不是目前最強的 AI 模型？"
    answer: "截至 2026 年 9 月 1 日，在 Artificial Analysis Intelligence Index（綜合排行，涵蓋 agent、coding、通用能力、科學推理四個維度）上，Fable 5.1 以 66 分排名第一，領先 Claude Opus 5 的 63 分、GPT-5.6 Sol 的 61 分、Grok 4.6 的 61 分。在 Terminal-Bench Science 0.1（科學研究自主操作）上拿到 52.6%，是第二名 Opus 5 的 29.0% 的近兩倍。需要注意這是公開 benchmark 的結果，不等於在所有特定領域都最強——但從綜合排行來看，它是目前測得到的天花板。"
  - question: "Fable 5.1 的 cache read 降價 75% 對實際帳單影響多大？"
    answer: "取決於你的工作流。在 agentic coding loop（Agent 編程迴圈）裡，同一段對話歷史每次 API 呼叫都重送，cache read 佔整體 token 量的絕大多數（實測約 95.6%），也佔帳單的 53-56%。Cache read 從 $1 降到 $0.25 per million token，帳單的最大一塊被砍了 75%。Anthropic 估計典型工作流省約 25%，重度 agent 工作流（Agent Workflow）省到 45%。但如果你的工作流是短問答、獨立任務，cache 佔比低，降價的效果也小。"
  - question: "為什麼 Artificial Analysis 說 Fable 5.1 per-task cost 貴了 20%？"
    answer: "因為 Fable 5.1 平均輸出 1.7 倍的 token——模型更聰明但也更話多。Output 單價 $50/M 是 cache read 新價 $0.25/M 的 200 倍，所以 output 多吃的錢把 cache 省下的吃回去了。Artificial Analysis 的 per-task cost（每任務成本）$3.69 是跑 Intelligence Index benchmark 的結果，這類 benchmark 是一組獨立問題，cache 佔比遠低於真實 agent 長對話。在 cache 佔比高的真實 agent 工作流裡，整體成本方向是省的。"
  - question: "訂閱用戶（Claude Pro / Max）用 Fable 5.1 有什麼要注意的？"
    answer: "1.7 倍的 output token 在訂閱制下不會多收錢，但會更快消耗你的配額上限——5 小時窗口限額和週限額都會更快用完。有用戶反映一次小調查就燒掉 5 小時限額的 13%。建議把 Fable 5.1 留給高價值的長時間 coding / agent 任務，日常工作用 Opus 5（Intelligence Index 63 分，per-task cost $2.34），在能力和配額之間找平衡。  ---"
---

Artificial Analysis Intelligence Index 66 分。Opus 5 是 63，GPT-5.6 Sol 是 61，Grok 4.6 是 61。

截至 2026 年 9 月 1 日，Fable 5.1 是這個排行榜上的第一名，而且領先第二名 3 分。

---

## Intelligence Index 排行：四個維度都在前面

Artificial Analysis Intelligence Index 是目前追蹤範圍最廣的 AI 模型綜合排行，由四個維度各佔 25% 加權組成：agent、coding、通用能力、科學推理。底層包含 9 個 benchmark（GDPval-AA v2、τ³-Banking、Terminal-Bench v2.1、SciCode、Humanity's Last Exam、GPQA Diamond、CritPt、AA-Omniscience、AA-LCR），所有評測由 Artificial Analysis 獨立執行。

[9 月 1 日的排行](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index)：

| 排名 | 模型 | 分數 |
|:--:|------|:--:|
| 1 | Claude Fable 5.1 (max) | 66 |
| 2 | Claude Fable 5.1 (xhigh) | 65 |
| 3 | Claude Opus 5 (max) | 63 |
| 4 | Claude Fable 5 (max) | 62 |
| 5 | GPT-5.6 Sol | 61 |
| 5 | Grok 4.6 (high) | 61 |
| 7 | Kimi K3 (max) | 60 |
| 7 | GLM-5.1 (max) | 60 |
| 9 | MiniMax Spark 1.2 (high) | 57 |

前四名都是 Anthropic 的模型。AA-Omniscience 準確率 67.2%，Fable 5 是 65.4%。

---

## Benchmark 拆開看：哪裡強、強多少

| Benchmark | Fable 5 | Fable 5.1 | 變化 |
|-----------|:--:|:--:|:--:|
| Terminal-Bench Science 0.1 | 24.7% | 52.6% | +113% |
| Terminal-Bench 4.0 | 42.0% | 55.8% | +33% |
| AutomationBench | 17.1% | 31.4% | +84% |
| OSWorld 2.0 | 36.1% | 41.7% | +16% |
| CursorBench 3.2.0 | 70.5% | 73.4% | +4% |
| Humanity's Last Exam | 63.8% | 65.0% | +2% |

Terminal-Bench Science 0.1 上，Fable 5.1 拿到 52.6%，Fable 5 是 24.7%——翻了一倍多。這個 benchmark 涵蓋 70 個科學工作流（生命、物理、地球、數學、工程科學），agent 在封閉終端環境裡自主操作，產出物由隱藏測試評分。Opus 5 在同一個 benchmark 上是 29.0%，GPT-5.6 Sol 是 22.4%。

Terminal-Bench 4.0（agentic coding）從 42.0% 到 55.8%。AutomationBench（商業自動化流程）從 17.1% 到 31.4%——接近翻倍。

Anthropic 自己的說法：Fable 5.1 特別針對「長時間複雜任務」強化。Threads 上的 [aiposthub 串文](https://www.threads.com/@aiposthub)講得更白：

> 以後叫 Claude 跑那種幾十分鐘、甚至更久的 coding / Agent 任務，穩定度跟能力可能又往前跳了一大截。

這和 benchmark 數字的方向一致——漲幅最大的都在需要自主操作、多步驟、長時間的任務上（Terminal-Bench Science +113%、AutomationBench +84%），而偏短任務的 benchmark（CursorBench +4%、Humanity's Last Exam +2%）提升有限。

---

## 成本帳：cache 降 75%，對 agent 是真的便宜

| 項目 | Fable 5 | Fable 5.1 |
|------|:--:|:--:|
| Input | $10/M token | $10/M token |
| Output | $50/M token | $50/M token |
| Cache read | $1/M token | $0.25/M token |

input 和 output 單價沒動。cache read 從 $1 降到 $0.25 per million token，降了 75%。

為什麼這很重要？因為 Agent 真正燒錢的地方，就是不停讀 context、跑工具、回頭確認、繼續執行——每一個 loop 都在做 cache read。[aiposthub 的觀察](https://www.threads.com/@aiposthub)：「現在連讓 Agent 長時間工作的成本也開始被壓下來了。」

數字對得上。[我 8 月拆自己帳單的時候](/ai-coding-token-cost-calculation-cache-read/)，17.2 億 token 裡 95.6% 是 cache read，cache read 佔帳單的 53-56%。帳單裡最大的一塊，被砍了 75%。

Anthropic 自己的估算：典型工作流省約 25%，重度 agent 工作流省到 45%。

有用戶用同一組遊戲 prompt 測：Fable 5.1 是 $7.08，Fable 5 是 $7.65，[便宜了 7%](https://x.com/noclipepe/status/2094926898232996291)，同時品質更好。他的結論：Fable 5 很快沒有理由再用了。

---

## 但 per-task cost 貴了 20%——這筆帳怎麼看

[Artificial Analysis 的測試結果](https://x.com/ArtificialAnlys/status/2094881171066978525)：

> "Claude Fable 5.1 tops the Artificial Analysis Intelligence Index but costs 20% more per task than Fable 5 despite a 75% cache read price cut"

per-task cost $3.69，比 Fable 5 貴約 20%。原因：Fable 5.1 平均輸出 1.7 倍的 token。

Anthropic 說省 25%，Artificial Analysis 說貴 20%。兩個都對，因為量的東西不同。

Anthropic 量的是 per-token cost——同一個 cache read token 便宜了 75%。Artificial Analysis 量的是 per-task cost——完成同一個 benchmark 任務的總 API 花費。Fable 5.1 更聰明但更話多，它用 1.7 倍的 output token 完成任務，output 單價 $50/M 是 cache read 新價 $0.25/M 的 200 倍——cache 省下來的錢被 output 多吐的 token 吃回去了。

差別在 cache 佔比。Artificial Analysis 的 Intelligence Index benchmark 不是長對話的 agentic loop——它是一組獨立問題，每個問題的 context 不大，cache 佔比遠低於真實 coding agent 的 95.6%。cache 佔比低，降幅省不了多少；output 暴增的代價就蓋過去了。

用我的帳單結構粗算：cache read 佔 55% 降 75%（省 41.25%）、output 佔 20% 漲 1.7 倍（多 14%）、淨效果省約 27%——和 Anthropic 的「省 25%」方向一致。

**結論：如果你跑 agent 長對話（cache 佔比高），Fable 5.1 又強又便宜。如果你跑短任務多輪獨立呼叫（cache 佔比低），可能反而貴。** 但即使貴了 20%，你買到的是 Intelligence Index 第一名的能力。

---

## 訂閱用戶：配額會更快用完

API 用戶看帳單，訂閱用戶看配額。1.7 倍的 output token 在訂閱制下不是多付錢——是更快撞牆。

有用戶一次小調查就燒掉 5 小時限額的 13%、週限額的 3%，這是在 [$100/月的 Max 訂閱上](https://x.com/vkryukov/status/2094926884333355070)。另一位用戶試著部署 Vercel，[整個 5 小時限額直接燒完](https://x.com/MisterDoodahh/status/2094926651360477332)。

這和[同日的 20x 爭議](/claude-pricing-20x-weekly-limit-trust-crisis/)接在一起看：用戶才剛發現 20x 只掛在 5 小時窗口上、週限額只多約 1.7 倍，現在模型本身又變得更話多——同樣的配額，能做的事變少了。

API 用戶得到更強的模型和更便宜的 cache，訂閱用戶得到更強的模型和更快的撞牆。同一個模型更新，兩群人的感受完全不同。

---

## 防蒸餾：thinking block 開始上鎖

Fable 5.1 帶了一個跟成本無關但跟生態有關的 breaking change。

新帳號（2026 年 8 月 31 日之後建立）使用 Fable 5.1 時，thinking block 生成後不能再修改 system prompt、tools 或對話歷史——Anthropic 說這是防止蒸餾。API 會驗證 thinking block 是在原始的 system prompt 和 tools 環境下產生的，不匹配就報錯。

三個 breaking change：forced tool use 會報錯、thinking block 不能跨模型讀、改對話歷史會讓 thinking block 失效。

對一般用戶影響不大。對自建 agent harness 的開發者影響大——如果你的 harness 會在對話中途注入 system reminder、壓縮歷史、或切換 fallback 模型，Fable 5.1 的 thinking block 會直接失效。[日本開發者 @connect24h 的評論](https://x.com/connect24h/status/2094926674823639528)直接說「模型防衛開始改變 agent 設計」。

現有帳號暫時不受影響，但 Anthropic 明確說未來的模型版本會擴大適用。

---

## 坦白說

Intelligence Index 排行和 benchmark 分數來自第三方獨立評測，可信度高。但 benchmark 不等於你的實際工作流——Terminal-Bench Science 的 52.6% 代表模型在標準化科學任務上的能力，不代表它在你的 codebase 上的表現。

Artificial Analysis 的 per-task cost $3.69 和「貴 20%」是跑 Intelligence Index benchmark 的成本，不是真實 agent 工作流的成本。我用的「cache 佔 55% → 省 27%」粗算基於我自己的帳單結構，不同人的工作流差異很大。1.7 倍 output 是 benchmark 數字，真實 coding 場景的 output 增量可能不同。

社群反應是發布後 24 小時的快照。配額問題的回報來自個別用戶，不是系統性測量。

但綜合所有第三方數字，Fable 5.1 確實是截至 9 月 1 日、公開 benchmark 上最強的模型。如果你做的事需要長時間自主推理——coding agent、科學研究、商業流程自動化——它不只是最強的選擇，在 cache 佔比高的工作流裡還是更便宜的選擇。

---

## 關鍵洞察

**一、Fable 5.1 是目前最強的公開模型。** Intelligence Index 66 分登頂，Terminal-Bench Science 翻倍，四個維度（agent、coding、通用能力、科學推理）都在頂端。領先幅度不是 1 分的誤差——和 Opus 5 差 3 分，和 GPT-5.6 Sol 差 5 分。如果你的工作依賴模型推理的天花板，Fable 5.1 是目前的天花板。

**二、成本看 cache 佔比，不看標題數字。** Anthropic 說省 25%，Artificial Analysis 說貴 20%——兩邊都對，差別在工作流的 cache 佔比。跑 agent 長對話 loop 的人（cache 佔帳單 50% 以上）：省。跑短任務獨立呼叫的人（cache 佔比低）：可能貴。衡量 agent 成本用 per-task，不要用 per-token。

**三、訂閱用戶要重新估配額。** Fable 5.1 的 1.7 倍 output 會讓你的有效配額再縮一截。日常工作考慮用 Opus 5（Intelligence Index 63，per-task cost $2.34），把 Fable 5.1 留給真正需要天花板能力的任務。

**四、自建 harness 的開發者注意防蒸餾機制。** 動態修改 system prompt、壓縮歷史、切換 fallback 模型的設計，在 Fable 5.1 上會讓 thinking block 失效。這不是 bug，是有意設計——現在只限新帳號，但未來會擴大。

---

## 常見問題 Q&A

**Q: Fable 5.1 到底是不是目前最強的 AI 模型？**

截至 2026 年 9 月 1 日，在 Artificial Analysis Intelligence Index（綜合排行，涵蓋 agent、coding、通用能力、科學推理四個維度）上，Fable 5.1 以 66 分排名第一，領先 Claude Opus 5 的 63 分、GPT-5.6 Sol 的 61 分、Grok 4.6 的 61 分。在 Terminal-Bench Science 0.1（科學研究自主操作）上拿到 52.6%，是第二名 Opus 5 的 29.0% 的近兩倍。需要注意這是公開 benchmark 的結果，不等於在所有特定領域都最強——但從綜合排行來看，它是目前測得到的天花板。

**Q: Fable 5.1 的 cache read 降價 75% 對實際帳單影響多大？**

取決於你的工作流。在 agentic coding loop（Agent 編程迴圈）裡，同一段對話歷史每次 API 呼叫都重送，cache read 佔整體 token 量的絕大多數（實測約 95.6%），也佔帳單的 53-56%。Cache read 從 $1 降到 $0.25 per million token，帳單的最大一塊被砍了 75%。Anthropic 估計典型工作流省約 25%，重度 agent 工作流（Agent Workflow）省到 45%。但如果你的工作流是短問答、獨立任務，cache 佔比低，降價的效果也小。

**Q: 為什麼 Artificial Analysis 說 Fable 5.1 per-task cost 貴了 20%？**

因為 Fable 5.1 平均輸出 1.7 倍的 token——模型更聰明但也更話多。Output 單價 $50/M 是 cache read 新價 $0.25/M 的 200 倍，所以 output 多吃的錢把 cache 省下的吃回去了。Artificial Analysis 的 per-task cost（每任務成本）$3.69 是跑 Intelligence Index benchmark 的結果，這類 benchmark 是一組獨立問題，cache 佔比遠低於真實 agent 長對話。在 cache 佔比高的真實 agent 工作流裡，整體成本方向是省的。

**Q: 訂閱用戶（Claude Pro / Max）用 Fable 5.1 有什麼要注意的？**

1.7 倍的 output token 在訂閱制下不會多收錢，但會更快消耗你的配額上限——5 小時窗口限額和週限額都會更快用完。有用戶反映一次小調查就燒掉 5 小時限額的 13%。建議把 Fable 5.1 留給高價值的長時間 coding / agent 任務，日常工作用 Opus 5（Intelligence Index 63 分，per-task cost $2.34），在能力和配額之間找平衡。

---

## 來源

- [Anthropic 官方公告：Introducing Claude Fable 5.1 and Claude Mythos 5.1](https://www.anthropic.com/claude-fable-and-mythos-5-1)
- [Artificial Analysis Intelligence Index v4.1.1](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index)
- [Artificial Analysis：Claude Fable 5.1 評測](https://artificialanalysis.ai/models/claude-fable-5-1)
- [@ArtificialAnlys X 貼文（Intelligence Index + per-task cost）](https://x.com/ArtificialAnlys/status/2094881171066978525)
- [@claudeai 官方 X 貼文（benchmark 數字）](https://x.com/claudeai/status/2094848572143407483)
- [aiposthub Threads 串文（繁中社群觀點）](https://www.threads.com/@aiposthub)
- [VentureBeat：75% cost reduction for Fable cache reads](https://venturebeat.com/technology/anthropics-claude-fable-5-1-and-mythos-5-1-arrive-with-a-75-cost-reduction-for-fable-cache-reads)
- [officechai：Fable 5.1 beats Opus 5 by 3 points](https://officechai.com/ai/claude-fable-5-1-scores-tops-artificial-analysis-intelligence-index-with-score-of-66-beats-opus-5-by-3-points/)
- [Anthropic Help Center：Preserved thinking / anti-distillation](https://support.claude.com/en/articles/16761192-preserved-thinking-changing-how-the-messages-api-handles-thinking-blocks-to-protect-against-distillation)
- [@noclipepe 遊戲 benchmark 實測](https://x.com/noclipepe/status/2094926898232996291)
- [@vkryukov 配額消耗回報](https://x.com/vkryukov/status/2094926884333355070)
- [@MisterDoodahh 配額消耗回報](https://x.com/MisterDoodahh/status/2094926651360477332)
- [@connect24h 防蒸餾評論](https://x.com/connect24h/status/2094926674823639528)
- [本 blog：兩個月 17 億 token——AI coding 的雲端帳單](/ai-coding-token-cost-calculation-cache-read/)
- [本 blog：20x 是什麼的 20 倍](/claude-pricing-20x-weekly-limit-trust-crisis/)
