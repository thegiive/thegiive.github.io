---
layout: post
title: "便宜模型跑五次再自己挑最好的：Verification Scaling 是智能密度的第二條曲線"
date: 2026-08-25 12:00:00 +0800
permalink: /verification-scaling-llm-as-a-verifier-terminal-bench/
image: /assets/images/verification-scaling-terminal-bench-2-1.png
description: "Stanford + UC Berkeley 團隊提出 LLM-as-a-Verifier，用 DeepSeek V4 Flash 生成五個候選解再自我驗證，Terminal-Bench 2.1 成功率 88% 超過 Fable 5 的 83%，每任務成本只要 $0.30 vs $2.00。上一篇我們討論了「選對模型」的智能密度，這篇拆解「用對策略」的第二條曲線——Verification Scaling。"
---

上一篇文章我們看了 Ramp 追蹤七萬家企業的支付數據：[Fable 5 只佔 Anthropic 銷售的 11.4%](/fable-5-enterprise-adoption-ceiling-intelligence-per-dollar/)，因為企業開始算「每美元多少智能」。那篇的結論是：下一個階段的競爭不是「誰的模型最強」，而是「誰能在最低的成本下交付足夠的智能」。

那是關於**選對模型**的故事。

一篇 Stanford 和 UC Berkeley 的新論文（[LLM-as-a-Verifier](https://arxiv.org/abs/2607.05391)，作者包括 Chelsea Finn、Ion Stoica、Azalia Mirhoseini）告訴我們：還有另一半。**用對推理策略**，同一個模型可以擠出遠超預期的有效智能。

---

## 一張圖講完

![Terminal-Bench 2.1 成本效率比較](/assets/images/verification-scaling-terminal-bench-2-1.png)

這是論文團隊在 Terminal-Bench 2.1 上的實測。X 軸是每個任務的平均成本（美元），Y 軸是成功率。三組對照：

| 方案 | 成功率 | 每任務成本 | Agent 框架 |
|------|:------:|:---------:|:----------:|
| DeepSeek V4 Flash ×1 + self-verify | ~79% | ~$0.05 | mini-swe-agent |
| DeepSeek V4 Flash ×3 + self-verify | ~86% | ~$0.20 | mini-swe-agent |
| DeepSeek V4 Flash ×5 + self-verify | ~88% | ~$0.30 | mini-swe-agent |
| GPT-5.6 Luna (Codex) | ~81% | ~$0.50 | Codex |
| GPT-5.6 Terra (Codex) | ~84% | ~$1.00 | Codex |
| Opus 4.8 (Claude Code) | ~80% | ~$1.50 | Claude Code |
| Fable 5 (Claude Code) | ~83% | ~$2.00 | Claude Code |
| GPT-5.6 Sol (Codex) | ~88% | ~$2.00 | Codex |

DeepSeek V4 Flash 跑一次只有 79%。但跑五次，同一個模型自己驗證自己、挑出最好的答案，成功率跳到 88%——跟 GPT-5.6 Sol 持平，超過 Fable 5 五個百分點，成本大約是 Fable 5 的六分之一、Sol 的四分之一。

那條紅線，從左下角的 ×1 到右上角的 ×5，幾乎是一條直線。Verification scaling 的邊際報酬還沒見到明顯衰減。

---

## 重要的但書：框架不同

先把最大的 caveat 講清楚。

這三組用的 agent 框架完全不同。DeepSeek 用的是論文團隊自己的 mini-swe-agent，OpenAI 的 baseline 來自 Codex，Anthropic 用 Claude Code。框架（harness）本身對成功率的影響可能不小——prompt 架構、工具呼叫方式、重試邏輯都不一樣。

所以不能把全部差距歸因於「模型 + 驗證策略」。但即便打個折扣，趨勢仍然成立：**同一個模型在同一個框架裡，多跑幾次 + 自我驗證，性能提升是顯著且穩定的。** 這個結論不受框架差異影響，因為紅線上的三個點用的是同一套框架。

---

## 怎麼挑最好的答案：從離散評分到連續分數

生成多個候選解不難，難的是「怎麼知道哪個最好」。

傳統做法叫 LLM-as-a-Judge：讓一個 LLM 看每個答案然後打 1-5 分。問題是，複雜的 coding 任務裡超過 27% 的評分是 tie——兩個品質明顯不同的解法，模型都打了 4 分。離散刻度的解析度不夠。

LLM-as-a-Verifier 換了一個做法。它不看模型最終輸出的那個 token（「7」還是「8」），而是看**生成那個 token 時的機率分佈**。

舉個例子。模型被問「這個解答 1-10 分？」時：

- 傳統 judge：模型輸出 "7" → 分數 = 7
- LLM-as-a-Verifier：模型內部 "7" 的機率 35%、"8" 的機率 40%、"6" 的機率 15%... → 加權期望值 = 7.3

7.3 vs 7.1 的區分度，遠大於 7 vs 7 的 tie。連續分數把那 27% 的死結幾乎全部解開了。

---

## 三個維度同時 scale

光靠連續分數還不夠。論文同時沿三個軸做 scaling，效果可以獨立相乘：

**一、Score Granularity（分數刻度 G）。** 把評分量表從 1-5 擴展到 1-20。刻度越細，模型的 logits 分佈有越多空間展開。在 Terminal-Bench V2 上，G 從 1 提升到 20，準確率從 73.1% 升到 77.5%，tie rate 從 27% 降到接近零。

**二、Repeated Evaluation（重複評估 K）。** 同一個候選解跑 K 次獨立評估，取平均分。K 從 1 到 16，準確率從 74.7% 升到 77.4%。單次評估有偏差，Monte Carlo 平均把偏差洗掉。

**三、Criteria Decomposition（標準拆解 C）。** 不問「這個解法正不正確？」這種大問題，而是拆成三個子問題：「規格有沒有滿足？」「輸出格式對不對？」「有沒有錯誤訊息？」三個子分數各自評估後 ensemble，從 75-76% 提升到 78.3%。

三個維度組合起來，Terminal-Bench V2 的驗證準確率到了 86.5%。

---

## 不只是 coding benchmark

如果這個框架只在 coding 上 work，那故事就到此為止了。但論文的野心更大——他們要證明 verification scaling 是 domain-agnostic 的。

| 領域 | Benchmark | 結果 | 對照基線 |
|------|-----------|:----:|:--------:|
| Coding | Terminal-Bench V2 | 86.5% | 83.1% baseline |
| Coding | SWE-Bench Verified | 78.2% | 76.8% 單一模型最佳 |
| Robotics | RoboRewardBench | 87.4% | 81.4%（專門訓練的 RoboReward-8B）|
| Medical | MedAgentBench | 73.3% | — |

在機器人領域，LLM-as-a-Verifier 打敗了**專門訓練過**的 RoboReward-8B 獎勵模型（87.4% vs 81.4%），而且不需要任何 domain-specific 訓練資料。一個通用的 verification 框架，靠 logits 加權 + 三軸 scaling，就超越了專家模型。

更有意思的是 progress tracking。論文測量了 verifier 分數和任務步驟進度之間的相關性（Value-Order Correlation, VOC），在成功的 trajectory 上達到 0.966。這意味著 verifier 不只是在任務結束時判對錯，它**在執行過程中就能追蹤 agent 是不是走在正確的路上**。偏離了，提早停；走對了，繼續跑。

---

## Verification Scaling 作為 RL 的 reward signal

論文還做了一件事：把 verifier 的連續分數拿來當 reinforcement learning 的 reward。

在機器人任務（LIBERO）上用 off-policy RL（DSRL-SAC），以 LLM-as-a-Verifier 的進度分數做 reward shaping，sample efficiency 提升了 1.8 倍。在數學推理（MATH）上用 on-policy RL（GRPO），當最終答案的 reward 訊號塌縮（答對或答錯都一樣多）時，verifier 提供的 dense reasoning reward 讓 sample efficiency 提升 1.1 倍。

這把 verification 從「事後判分」推進到「事中引導」。

---

## 連回「每美元多少智能」

上篇文章的 Intelligence Index / 輸出成本，測量的是模型的**固有**智能密度——你買的是什麼模型，它就值多少。

Verification Scaling 告訴我們一件不同的事：**模型的有效智能不是固定值，它是推理策略的函數。**

同一個 DeepSeek V4 Flash，兩種用法：

| 策略 | 成功率 | 每任務成本 | 有效智能 / $ |
|------|:------:|:---------:|:-----------:|
| 單次生成 (×1) | 79% | $0.05 | 15.8 |
| 五次生成 + self-verify (×5) | 88% | $0.30 | 2.93 |

有效智能 / $ 下降了——每多花一塊錢的邊際效率確實在遞減。但絕對性能從 79% 跳到 88%，整整九個百分點。如果你的場景是「品質到 88% 才能上線」，那這九個百分點就是 0 和 1 的差別，不是性價比的問題。

更關鍵的是：即便是 ×5 的 $0.30，仍然遠低於 Fable 5 的 $2.00，而且性能還高了五個百分點。

所以智能密度有兩條曲線：
1. **選對模型**（上一篇）——在固定推理策略下，挑 II/$ 最高的模型
2. **選對策略**（這一篇）——在固定模型下，用 generate-then-verify 提升有效智能

兩條曲線相乘，才是真正的成本效率前沿。

---

## 這個方法的適用邊界

Verification scaling 不是萬能的。幾個需要認清的限制：

**一、需要 logits access。** 核心機制是讀 token 生成時的機率分佈。不是每家 API 都開放 logits——OpenAI 的 GPT-5.6 系列有限度開放 top-5 logprobs，Anthropic 的 Claude 目前不開放。自部署的開源模型沒有這個問題，這也是為什麼論文用 DeepSeek V4 Flash。

**二、需要有明確的「對錯」。** Terminal-Bench 和 SWE-Bench 的任務有客觀的通過標準——測試跑過就是對，跑不過就是錯。但真實專案裡「需求理解是否正確」、「架構選擇是否合理」這類模糊判斷，self-verification 的可靠度還沒被驗證過。

**三、延遲乘以 N。** 五個候選解意味著五倍的生成時間（如果不並行的話）。適合 batch 工作，不適合即時互動。你不會想在 Claude Code 的即時對話裡等五倍的時間。

**四、成本計算不含 GPU idle time。** 論文的成本是按 API pricing 算的。如果是自部署 DeepSeek V4 Flash，你的 GPU 不是按 token 付費，而是按時間付費。五倍的推理時間意味著五倍的 GPU 佔用，但不是五倍的「成本」——因為你已經買了那張卡。實際的 Capex 效率要看你的 GPU 利用率。

---

## 對務實者的建議

**一、Batch 任務開始考慮 generate-then-verify。** Code review、自動化測試生成、文件翻譯——這類不需要即時回覆、但需要高品質的場景，是 verification scaling 的甜蜜點。

**二、先從 ×3 開始。** 圖上紅線的斜率在 ×1 到 ×3 之間最陡——性價比最高的拐點。從 79% 到 86% 只花了 $0.15，之後 ×3 到 ×5 的邊際收益開始趨緩。

**三、即時互動仍然需要單次強力模型。** 開發者坐在 Claude Code 前面等回覆的時候，延遲就是成本。這個場景短期內不會被 generate-then-verify 取代。

**四、混合策略是最務實的。** 即時互動用 Opus 5 或 Sonnet 5（速度 + 夠好），夜間 batch 用 DeepSeek V4 Flash ×3-5 + self-verify（品質 + 便宜）。不是選邊站，是看任務的延遲容忍度。

---

## 實作：怎麼跑起來

論文團隊開源了完整框架，有兩種用法。

### Python SDK：嵌入自己的 pipeline

```bash
pip install llm-verifier
```

核心 API 三個，對應三種場景：

```python
import llm_verifier

result = llm_verifier.select(
    problem=problem,
    candidates=candidates,
    criteria={"Correctness": "Does the code solve the problem?"},
)

# 兩兩比較：A 和 B 哪個好
reward_a, reward_b = llm_verifier.compare(
    problem, sol_a, sol_b,
    criteria={"Overall": "Does the code solve the problem?"},
)

# 過程追蹤：agent 執行途中是不是走對方向
result = llm_verifier.track(
    problem=problem, steps=steps,
    checkpoint_steps=[1, 2, 3, 4, 5], n_evaluations=4,
)
```

重現 Terminal-Bench 2.1 的結果只要兩行：

```bash
python scripts/run_bo3.py   # Best-of-3 → 86.5%
python scripts/run_bo5.py   # Best-of-5 → 88.0%
```

`run_bo5.py` 的關鍵參數：`N_TRIALS=5`（五個候選解）、`PIVOTS=1`（PPT 排名選 1 個 pivot）、`N_EVALUATIONS=2`（每個候選解重複驗證 2 次取平均）。

### TurboAgent：Claude Code 的 drop-in proxy

更有意思的用法。[TurboAgent](https://github.com/llm-as-a-verifier/TurboAgent) 是一個 API proxy，插在 client 和 LLM provider 中間，自動做 generate-then-verify：

```bash
pip install turbo-agent
turbo-agent              # 啟動 proxy，預設 port 8888
```

Claude Code 只要改一個環境變數：

```bash
ANTHROPIC_BASE_URL=http://localhost:8888 claude
```

Claude Code 完全不知道背後發生了什麼。Proxy 收到請求後自動：並行送 N 個請求到後端模型 → PPT tournament 挑最好的 → 回傳最佳結果。`http://localhost:8888/visualizer` 可以看到完整的 pipeline DAG 和每個候選解的分數。

**重要限制：Verifier 不能用 Claude。** Anthropic API 不開放 token logprobs，所以 Claude 只能當 generator（後端模型），不能當 verifier。Verifier 必須用有 logprobs 的模型——Gemini（透過 Vertex API）或 DeepSeek。

### 本地部署：用 Qwen 3.8 27B 跑 self-verification

如果你有自己的 GPU（例如 RTX Pro 6000），可以用開源模型同時當 generator + verifier，完全不需要外部 API。

Qwen 3.8 27B 在 [Artificial Analysis Intelligence Index](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index) 上拿到 52 分，跟 DeepSeek V4 Flash 相同。27B dense 模型單卡就能跑，logprobs 完全開放。

```bash
# 用 vLLM 起一個 OpenAI-compatible server
vllm serve Qwen/Qwen3.8-27B --port 8000
```

TurboAgent 的 `turbo-agent.yaml` 把 backend model 指向這個 endpoint，Qwen 同時當 generator + verifier。

成本結構完全不同於 API pricing。論文裡 DeepSeek V4 Flash ×5 的 $0.30/task 是按 API 計費的。本地部署是 Capex——GPU 已經買了，跑 ×5 只是多花五倍推理時間，邊際成本趨近零。對已經有 GPU 的團隊來說，verification scaling 幾乎是免費的性能提升。

要注意的是：論文沒有用 Qwen 3.8 27B 跑過 Terminal-Bench，實際的 pass@1 起點和 verification scaling 曲線需要自己實測。但 Intelligence Index 同為 52 分，合理預期 scaling 幅度不會差太多。

---

## 最後的觀察

上篇結語是：「最好的產品不一定是賣得最好的產品。」

這篇的觀察是：**最強的模型不一定是最有效率的策略。**

這兩件事加在一起，指向同一個方向：AI 產業正在從「比誰的模型最強」轉向「比誰把智能送到使用者手上的效率最高」。模型能力是基礎，但推理策略、部署架構、成本控制的重要性正在快速追上來。

Verification scaling 目前還在早期——紅線的斜率暗示還有往上的空間，但實際的 ceiling 在哪裡、跨 domain 的泛化能力到底多強，都需要更多實測。論文團隊已經開源了完整框架（[GitHub](https://github.com/llm-as-a-verifier/llm-as-a-verifier)），包含 Claude Code 的 drop-in proxy。

有興趣的人可以自己跑跑看。畢竟，最可靠的驗證方式還是：自己試一次。
