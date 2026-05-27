---
layout: post
title: "當 AI Coding Benchmark 開始測到「基礎設施」：從 Anthropic 的實驗，到學術共識，再到 Arena 評測的結構性盲點"
date: 2026-02-10 06:30:00 +0800
categories: [ai-agent]
tags: [benchmark, anthropic, infrastructure-noise, arena, lmsys, swe-bench, terminal-bench, open-source, evaluation]
permalink: /ai-coding-benchmark-infrastructure-noise-arena-blindspot/
image: /assets/images/ai-coding-benchmark-infrastructure-noise-cover.png
description: "你整天看的那些 SOTA 排名比較，很有可能不是模型比較厲害，而是 infra 比較厲害。至於開源模型看起來稍稍弱一點？很可能換一個 infra 環境，它就變 SOTA 了。Anthropic 實驗證實：同一模型在不同基礎設施配置下，成功率差距達 6 個百分點——而 leaderboard 上模型之間的差距往往只有 3～5%。"
---

![Artificial Analysis Intelligence Evaluations - 四大 Agentic Benchmark 排名](/assets/images/ai-coding-benchmark-infrastructure-noise-cover.png)

**作者：** Wisely Chen
**日期：** 2026 年 2 月

你整天看的那些 SOTA 排名比較，很有可能不是模型比較厲害，而是 infra 比較厲害。至於開源模型看起來稍稍弱一點？很可能換一個 infra 環境，它就變 SOTA 了。

在 AI 世界裡，我們越來越習慣用一個數字來做決策。

哪個模型比較強？哪個值得導入？哪個「贏了 benchmark」？

但最近 Anthropic 的一組 coding benchmark 實驗，實際上對整個評測生態潑了一盆冷水：

**在 agent-based coding benchmark 中，你看到的分數，可能不只是模型能力。**

## 一、Anthropic 在 coding benchmark 中真正發現了什麼？

Anthropic 在 2026 年 2 月發表的工程文章 [Quantifying infrastructure noise in agentic coding evals](https://www.anthropic.com/engineering/infrastructure-noise) 中，系統性地驗證了一個過去常被忽略的假設：

**Benchmark 的執行環境，會實質影響 agent 的成功率。**

他們做的事情其實很單純，但非常關鍵：

- 使用同一個模型
- 同一組 coding / agent 任務（Terminal-Bench 2.0）
- 同樣的 prompt 與流程
- **只調整基礎設施相關參數**
  - CPU / memory limit（從 1x 到 uncapped）
  - sandbox 行為
  - timeout / retry 條件

結果是什麼？

最終成功率可以出現**約 6 個百分點的差距**（p < 0.01）。

這不是微小誤差。因為在多數 coding 或 agent leaderboard 上，模型之間的差距往往就在 3～5%，排名前後可能只差幾個百分點。

更具體的數字：

| 資源配置 | 基礎設施失敗率 | 說明 |
|----------|---------------|------|
| 1x（嚴格限制） | 5.8% | 最受限的環境 |
| 3x（建議甜蜜點） | 2.1% | 失敗率降低三分之二（p < 0.001） |
| Uncapped（無限制） | 0.5% | 最寬鬆的環境 |

從 1x 到 uncapped，成功率差了 6 個百分點。但從 3x 到 uncapped，**分數的提升已經落在統計噪聲範圍內**（p = 0.40）。

Anthropic 的結論是：3x 資源配置是個合理的校準甜蜜點——大幅降低了基礎設施的干擾，又不會因為給太多資源而人工膨脹分數。

他們也拿 SWE-bench 做了交叉驗證：在 227 道題上給 5 倍 RAM，差距只有 1.54 個百分點。這說明任務設計越依賴系統資源，基礎設施噪聲的影響就越大。

換句話說：

**你以為你在看模型能力排名，但實際上，你可能在看「誰跑在比較寬鬆的世界裡」。**

### 為什麼 agent-based coding benchmark 特別容易被污染？

因為這類 benchmark，本質上不是在測「回答品質」，而是在測一個完整的工程流程：

- 寫程式
- 裝依賴
- 跑測試
- Debug、retry、修 bug
- 與工具與作業系統互動

這意味著模型的表現高度依賴：

- 推理速度（會不會 timeout）
- 記憶與 context 管理（會不會 token 爆炸）
- 工具是否可用、可安裝
- sandbox 對資源限制的 enforcement 方式

在這裡，基礎設施不再是背景，而是測試的一部分。

Anthropic 把這種影響稱為：**Infrastructure Noise（基礎設施噪聲）**。

## 二、這不是個案：學術界其實早就指向同一個問題

如果只是一家公司的工程文章，還可以說是個別觀點。但關鍵在於：近兩年的學術研究，其實正在用另一種語言講同一件事。

### 1. Agent 評估缺乏可重現的執行環境

ICLR 2026 收錄的 [DevOps-Gym](https://arxiv.org/pdf/2601.20882) 論文，以及多篇 2025 年的 agent evaluation survey 都指出一個結構性問題：

- benchmark 任務描述得很清楚
- metrics 定義得很完整
- **但實際執行環境往往沒有被嚴格規範或完整揭露**

結果就是：同一個 benchmark，在不同研究者、不同平台上跑，本質上是在進行不同的實驗。而 agent 類任務，會把這些微小差異放大成最終成敗。

### 2. 現有 benchmark 往往混合測量了兩件事

學術上另一個被反覆點出的問題是：很多 agent benchmark 同時在測兩件事——

- **模型能力**
- **系統工程成熟度**

但最後卻只給你一個分數、一個排名。

[CORE-Bench](https://arxiv.org/abs/2409.11363) 的研究結果很說明問題：最佳 agent 在最難等級的任務上，準確率只有 21%。這個數字到底反映的是模型推理能力不足，還是執行環境的限制？論文本身也承認很難完全區分。

### 3. 對開源模型來說，影響其實是放大版

這一點在學術與實務上都非常關鍵。

- 開源模型的 benchmark 來源高度分散
- 評測環境極度不一致
- 推理速度、context 管理、tooling 穩定性更吃 infra

結果是：很多「開源模型表現較差」的結論，其實可能是在嚴格環境下測試開源模型，卻在寬鬆環境下測試閉源模型。

這不是公平比較，而是結構性偏差。

另外，基準測試污染（benchmark contamination）也是個老問題但影響持續擴大。有研究顯示，部分模型在無污染測試中的準確率比原始 benchmark 下降高達 13%。這代表一些亮眼的分數，反映的可能是「記憶力」而不是「推理能力」。

### 4. 不只是 infra：LLM 基礎 benchmark 本身就有結構性問題

上面談的都是 agent-based 評測被「執行環境」污染。但學術界指出的問題其實更根本——就算你不跑 agent，只用最傳統的 LLM benchmark（MMLU、HumanEval、GSM8K），分數本身也未必可信。

這裡有四層問題，每一層都有紮實的論文支撐。

**第一層：Data Contamination（資料污染）——模型可能在「背答案」**

這是最普遍、也最被低估的問題。MMLU 原始論文的補充研究就發現，benchmark 題目經常出現在模型的訓練資料中。一旦去除這些「已經見過的題目」，模型表現會大幅下降。

[Hendrycks et al. (2021)](https://arxiv.org/abs/2107.03374) 在 HumanEval 類 coding benchmark 中也發現明顯的資料重疊——這讓 generative 模型看起來比它實際的推理能力要強。[Kadavath et al. (2022)](https://arxiv.org/abs/2207.05221) 更直接建立了一個「清潔測試集」來避免答案洩露，結論是：大模型在無污染集上的 performance 明顯下降。

換句話說，很多 SOTA 分數反映的可能是「記憶」而不是「推理能力」。這種污染對 GPT 系列、LLaMA 系列乃至開源模型都有顯著影響。

**第二層：Benchmark 設計本身帶有偏差**

[Bender et al. (2021)](https://dl.acm.org/doi/10.1145/3442188.3445922) 的「Stochastic Parrots」論文雖然不是專門討論 benchmark，但它指出了大型語言模型 evaluation 的根本問題——自然語言任務存在資料偏見、答案分布不均、標註者主觀性。[Cobbe et al. (2021)](https://arxiv.org/abs/2110.14168) 在數學推理 benchmark 上的發現更具體：如果 benchmark 只用已有公式或固定結構的答案，模型能靠 pattern match 拿高分，但一旦題型改變（distribution shift），分數就劇烈下跌。

這些研究的共同觀察是：很多 benchmark 並不是在純粹測試推理與泛化能力，而是在無意識中測試了模式記憶強度和特定結構的熟悉度。**分數高低，有可能是「會答題型」而不是「真的理解」。**

**第三層：評測指標本身的誘導偏誤**

「BLEU Is Broken」、「ROUGE Is Broken」這類研究雖然最初是針對自然語言生成的評分指標，但它揭示了一個更普遍的問題：**指標本身並不總是與品質對齊。** 同樣的問題出現在 LLM benchmark 的 exact-match 和 accuracy 計算上。

[Ribeiro et al. (2020)](https://arxiv.org/abs/2005.04118) 在 "Beyond Accuracy" 論文中提出：不能只用一個單一指標來評估 NLP 能力，需要測試語言模型的 robust behavior。當你用單一 accuracy 或 token-level metric 去衡量複雜推理時，結果可能偏離真正能力。

**第四層：Benchmark 分數 ≠ 泛化能力**

最後，也是最關鍵的問題：benchmark score 跟模型在真實世界的泛化能力，可能根本不是同一件事。[Chung et al. (2022)](https://arxiv.org/abs/2207.00747) 的研究發現，模型可能在 benchmark 上表現很高，但在 real-world unpredictability 頻繁犯錯。這意味著 benchmark score 與真實能力之間，存在一道不容忽視的鴻溝。

把這四層加在一起看，結論其實很清楚：

**不只是 agent benchmark 被 infra 污染，連最基礎的 LLM benchmark 本身，都面臨資料污染、設計偏差、指標偏誤、以及分數與真實能力脫鉤的問題。** 所謂的「SOTA 排名」，從頭到尾都需要打上很大的問號。

## 三、那 Arena 類評測是不是解法？

看到這裡，很多人會直覺想到：

> 那乾脆不要跑 agent，不要碰 infra，用人類投票就好？

像 LMSYS Chatbot Arena（現在叫 LMArena）這樣的 Arena 模式，確實解決了一些問題，但它也帶來了新的盲點。

### Arena 的優點，其實很明確

Arena 類評測天然避開了：infrastructure noise、sandbox 差異、timeout / resource 限制。

它測的是：人類主觀偏好、對話流暢度、第一印象、結構、語氣。

在「對話型助手」這個維度上，它其實比很多 benchmark 更誠實。

### 但 Arena 的結構性問題也同樣明確

**第一，Arena 測的是「感知品質」，不是能力上限。**

Arena 本質上在回答的是：「人類覺得哪個比較好用？」

而不是：誰能撐過長流程？誰能在受限環境下穩定完成任務？誰的系統性推理更可靠？

這讓 Arena 天然偏好快速給結論、語氣篤定、結構清楚好讀的回答，而不一定是深度推理或長期正確性。[TechCrunch 的分析](https://techcrunch.com/2024/09/05/the-ai-industry-is-obsessed-with-chatbot-arena-but-it-might-not-be-the-best-benchmark/)也指出：Arena 的用戶群體高度集中在 AI 和科技圈，提交的問題以程式設計和 AI 工具為主，這讓它的「人類偏好」本身就帶有取樣偏差。

**第二，Arena 已經被模型「針對性優化」。**

這不是作弊，而是 reward shaping 的必然結果。2025 年 [The Leaderboard Illusion](https://simonwillison.net/2025/Apr/30/criticism-of-the-chatbot-arena/) 論文揭露了一個更嚴重的問題：

- Meta 在 Llama-4 發布前，**私下測試了 27 個模型變體**，只公開表現最好的版本
- 243 個公開模型中，有 **205 個被靜默淘汰**
- 大公司可以私下 A/B test 多個版本，小團隊和開源社群沒有這個資源

久而久之，Arena 排名高的模型，可能更像「很會聊天的顧問」，而不一定是「可靠的工程代理」。

**第三，Arena 完全無法回答「工程現實問題」。**

Arena 無法告訴你：

- 這個模型在 CI/CD 裡能不能活下來
- 在私有部署、有限資源下是否穩定
- agent 長流程會不會崩潰

但這些，恰恰是企業與實務場景最在乎的事。

## 結論：我們需要的是「多維度評估」，不是新的排行榜神話

Anthropic 的實驗、學術研究、以及 Arena 的興起，共同指向一個結論：

**任何單一 benchmark，都不再能代表「模型能力」本身。**

| 評測類型 | 實際在測什麼 | 沒有在測什麼 |
|----------|------------|------------|
| Coding / Agent Benchmark | 模型 × 系統 × 基礎設施 | 純模型能力（被 infra 污染） |
| Arena 人類投票 | 人類主觀感知與對話體驗 | 工程穩定性、長流程可靠性 |
| 靜態知識測試 | 記憶與知識覆蓋 | 推理深度、工具使用能力 |

Anthropic 在文章中給了一個很實用的建議：

> **如果 leaderboard 上兩個模型的差距小於 3 個百分點，而且沒有揭露完整的基礎設施配置，你應該對這個排名持保留態度。**

真正成熟的評估方式，應該是：知道每個分數在測什麼，也清楚它沒有在測什麼。

## 坦白說

這篇文章其實源自一個很簡單的困擾：每次有新模型發布，我都會收到「這個模型排名第一耶，要不要換？」的訊息。

但當你真的去看那些 benchmark 的細節，你會發現：排名第一的條件，往往跟你的生產環境差距很大。你的 CI/CD 不會給模型 uncapped 的記憶體，你的 sandbox 不會讓它裝任何它想裝的東西，你的 timeout 也不會設成無限。

所以我現在看 leaderboard 的方式變了。我不再問「誰第一」，而是問：

**「這個第一，是在什麼條件下成立的？」**

在 2026 年，忽略這個問題的 benchmark，不只是資訊不足，而是具有誤導性。

---

**延伸閱讀：**
- [Anthropic: Quantifying infrastructure noise in agentic coding evals](https://www.anthropic.com/engineering/infrastructure-noise)
- [The Leaderboard Illusion - Arena 批評分析](https://simonwillison.net/2025/Apr/30/criticism-of-the-chatbot-arena/)
- [DevOps-Gym: Benchmarking AI Agents (ICLR 2026)](https://arxiv.org/pdf/2601.20882)
- [CORE-Bench: 計算可重現性 Agent Benchmark](https://arxiv.org/abs/2409.11363)
- [GPT-5.2 基準測試爭議：Token 灌水與第三方評測全面落敗](/gpt-5.2-benchmark-controversy/)
- [Hendrycks et al. (2021): Measuring Massive Multitask Language Understanding](https://arxiv.org/abs/2107.03374)
- [Kadavath et al. (2022): Language Models (Mostly) Know What They Know](https://arxiv.org/abs/2207.05221)
- [Bender et al. (2021): On the Dangers of Stochastic Parrots](https://dl.acm.org/doi/10.1145/3442188.3445922)
- [Cobbe et al. (2021): Training Verifiers to Solve Math Word Problems](https://arxiv.org/abs/2110.14168)
- [Ribeiro et al. (2020): Beyond Accuracy - CheckList for NLP Models](https://arxiv.org/abs/2005.04118)
- [Chung et al. (2022): Scaling Instruction-Finetuned Language Models](https://arxiv.org/abs/2207.00747)
