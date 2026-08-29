---
layout: post
title: "\"不換模型、不額外訓練，讓開源模型讀自己的神經層來驗證答案：LLM-as-a-Verifier\""
date: 2026-08-25 12:00:00 +0800
permalink: /verification-scaling-llm-as-a-verifier-terminal-bench/
tags: [LLM-as-a-Verifier, self-verification, logits, open source, 開源模型, DeepSeek V4 Flash, Terminal-Bench, on-premise, 地端部署, inference, 推論, Stanford, UC Berkeley, verification scaling]
categories: [AI 產業分析]
image: /assets/images/verification-scaling-terminal-bench-2-1.png
description: "\"Stanford + UC Berkeley 論文 LLM-as-a-Verifier 找到一個方法，讓開源模型深入自己的神經層（logits）自我驗證，不換模型、不額外訓練，DeepSeek V4 Flash 從 79% 跳到 88%。這個框架天然偏好地端部署——需要完整的 logits access，而且很燒 token，剛好是開源 + 自有 GPU 的甜蜜點。\""
author: Wisely Chen
faq:
  - question: "LLM-as-a-Verifier 到底在做什麼，跟傳統的 LLM-as-a-Judge 差在哪？"
    answer: "傳統做法 LLM-as-a-Judge 是讓模型看每個答案然後打 1-5 分，但複雜的 coding 任務裡超過 27% 的評分是 tie——兩個品質明顯不同的解法，模型都打了 4 分，離散刻度的解析度不夠。LLM-as-a-Verifier 的做法是往下挖一層，讀取 logits（模型內部對所有候選 token 算出的機率分佈），把所有 scoring token 的機率拿出來做加權平均。比方說模型內部算出 \"7\" 機率 0.35、\"8\" 機率 0.40、\"6\" 機率 0.15，加權平均得到 7.3 這種連續分數。7.3 vs 7.1 的區分度，遠大於離散的 7 vs 7 的 tie。不需要額外訓練，不需要另一個更強的模型當 judge。"
  - question: "DeepSeek V4 Flash 從 79% 跳到 88% 這個數字可信嗎，有什麼要注意的？"
    answer: "79% 到 88% 的提升是在 Terminal-Bench 2.1 上測的，用的是同一個模型、同一套 agent 框架（mini-swe-agent），差別只在推理策略：單次跑 79%，跑三次加 self-verify 到 86%，跑五次到 88%。這條上升趨勢是扎實的。但要注意的是，論文圖表上跟 Fable 5（83%）、GPT-5.6 Sol（88%）的跨框架比較要謹慎看——三組用的 agent 框架不同（mini-swe-agent / Codex / Claude Code），不能把全部差距歸因於驗證策略。建議看單個模型在同一框架內的上升趨勢，比看跨框架的絕對值更有意義。"
  - question: "為什麼同一個模型有能力驗證自己的答案，這不是自己改自己考卷嗎？"
    answer: "生成和驗證是不同的認知任務（cognitive task）。生成是發散的——從零寫出一個解法；驗證是收斂的——看一個現成的解法判斷好不好。判斷一個答案對不對，比從頭想出正確答案容易，這對人類如此，對 LLM 也是。然後關鍵在 logits 層面：模型內部的機率分佈比它最終輸出的那個 token 包含了更多資訊。模型「心裡」對答案品質的判斷，其實比它「嘴上」說出的那個數字更細膩。LLM-as-a-Verifier 做的事情就是把這份細膩挖出來用。論文還測了 progress tracking，verifier 分數和任務步驟進度之間的相關性（VOC）在成功的 trajectory 上達到 0.966，代表 verifier 在執行過程中就能追蹤 agent 走得對不對。"
  - question: "這個方法適合地端部署（on-premise）還是雲端 API？"
    answer: "天然偏好地端部署，理由有兩個。第一，需要讀 logits——自部署的開源模型透過 vLLM 或 SGLang 可以拿到完整的 logits 向量，沒有限制。OpenAI API 只開放 top-5 logprobs，論文說勉強能用但效能不是最好。Anthropic API 完全不開放 logprobs，所以 Claude 不能當 verifier。第二，很燒 token——跑五次生成加重複驗證加多標準評分，token 用量輕鬆是單次的 10-15 倍。雲端 API 帳單直接乘上去，很痛。但地端這兩個問題都不存在：GPU 已經買了，邊際 token 成本趨近零，logits 完全透明。雲端用戶看到的是「多花六倍 token 費」，地端用戶看到的是「免費升級九個百分點」。"
  - question: "除了 coding，這個框架還能用在什麼地方？"
    answer: "論文跨了三個完全不同的領域（domain），都不需要 domain-specific fine-tuning。在 coding 領域，Terminal-Bench V2 達到 86.5%、SWE-Bench Verified 達到 78.2%。在機器人領域（Robotics），RoboRewardBench 上拿到 87.4%，打敗了專門訓練過的 RoboReward-8B 獎勵模型的 81.4%——一個通用的 verification 框架靠 logits 加權加三軸 scaling，超越了專家模型。在醫療領域（Medical），MedAgentBench 達到 73.3%。不過要注意適用邊界：這個方法需要有明確的「對錯」標準，Terminal-Bench 和 SWE-Bench 有客觀的通過標準，但真實專案裡「需求理解是否正確」「架構選擇是否合理」這類模糊判斷，self-verification 的可靠度還沒被驗證過。另外延遲會乘以 N，五個候選解意味著五倍生成時間，適合批次處理（batch），不適合即時互動。"
---

Stanford + UC Berkeley 的新論文 [LLM-as-a-Verifier](https://arxiv.org/abs/2607.05391)（作者包括 Chelsea Finn、Ion Stoica、Azalia Mirhoseini）找到了一個方法，把開源模型的能力再往上推一個台階。

不用換更大的模型，不用額外訓練。

做法是：每個問題跑五次，然後深入模型的大腦——讀取神經網路內部的機率分佈——自我驗證，挑出最好的答案。

DeepSeek V4 Flash 單次跑 Terminal-Bench 2.1 只有 79%。五次 + self-verify，成功率跳到 88%。同一個模型，純粹靠推理策略提升了九個百分點。

---

## 數字攤開來

![Terminal-Bench 2.1 成本效率比較](/assets/images/verification-scaling-terminal-bench-2-1.png)

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

88% 超過 Fable 5 的 83%，追平 GPT-5.6 Sol 的 88%。但要注意：這三組用的 agent 框架不同（mini-swe-agent / Codex / Claude Code），不能把全部差距歸因於驗證策略。**建議看單個模型的上升趨勢**——紅線上三個點用的是同一套框架，79% → 86% → 88% 的提升是扎實的。

---

## 核心機制：深入神經層讀 Logits

生成多個候選解不難，難的是「怎麼知道哪個最好」。

傳統做法叫 LLM-as-a-Judge：讓模型看每個答案然後打 1-5 分。問題是，複雜的 coding 任務裡超過 27% 的評分是 tie——兩個品質明顯不同的解法，模型都打了 4 分。離散刻度的解析度不夠。

LLM-as-a-Verifier 的做法不同。它不看模型最終輸出的那個 token，而是往下挖一層——讀 logits。

LLM 生成每一個 token 的時候，內部不是直接「決定輸出 7」，而是先對所有候選 token 算出一個機率分佈。比方說模型被問「這個解答 1-10 分？」，它內部已經算好了：

> "7" 機率 0.35、"8" 機率 0.40、"6" 機率 0.15、"9" 機率 0.05...

那個機率表就是 logits（嚴格說是 logits 經過 softmax 後的機率）。

傳統 judge 只取機率最高的那個 token（argmax），拿到離散的 "8"。LLM-as-a-Verifier 把所有 scoring token 的機率拿出來做加權平均：

> 0.35 × 7 + 0.40 × 8 + 0.15 × 6 + 0.05 × 9 + 0.03 × 5 = **7.3**

7.3 vs 7.1 的區分度，遠大於 7 vs 7 的 tie。不需要額外訓練，不需要另一個更強的模型當 judge。

---

## 為什麼同一個模型可以驗證自己

回到更根本的問題：為什麼一個模型有能力判斷自己的答案好不好？

因為生成和驗證是不同的認知任務。生成是發散的——從零寫出一個解法。驗證是收斂的——看一個現成的解法判斷好不好。

判斷一個答案對不對，比從頭想出正確答案容易。這對人類如此，對 LLM 也是。

而 logits 層面的機率分佈，比模型最終輸出的那個 token 包含了更多資訊。模型「心裡」對答案品質的判斷，其實比它「嘴上」說出的那個數字更細膩。LLM-as-a-Verifier 做的事情，就是把這份細膩挖出來用。

---

## 三個維度同時 Scale

光靠連續分數還不夠。論文同時沿三個軸做 scaling，效果獨立相乘：

**一、放大評分刻度（Score Granularity）。** 從 1-5 擴展到 1-20，讓 logits 分佈有更多空間展開。Terminal-Bench V2 上 tie rate 從 27% 降到接近零。

**二、重複評估取平均（Repeated Evaluation）。** 同一個候選解跑 K 次獨立評估，Monte Carlo 平均洗掉單次偏差。K=1 到 K=16，準確率從 74.7% 升到 77.4%。

**三、拆成多個子標準（Criteria Decomposition）。** 不問「正不正確？」這種大問題，拆成「規格有沒有滿足？」「輸出格式對不對？」「有沒有錯誤訊息？」各自評分後 ensemble，從 75-76% 提升到 78.3%。

排名用 Probabilistic Pivot Tournament（PPT）從 O(N^2) 降到 O(Nk)，省算力不掉品質。三個維度組合起來，Terminal-Bench V2 的驗證準確率到了 86.5%。

---

## 為什麼這對地端特別有用

這個框架有兩個硬需求，剛好都指向地端部署：

**第一，需要讀 logits。** 自部署的開源模型（vLLM / SGLang）可以拿到完整的 logits 向量，沒有任何限制。OpenAI API 只開放 top-5 logprobs，論文說勉強能用，但效能不是最好。Anthropic API 完全不開放，所以 Claude 不能當 verifier。

**第二，很燒 token。** 跑五次生成 + 重複驗證 + 多標準評分，token 用量輕鬆是單次的 10-15 倍。雲端 API 帳單直接乘上去，很痛。

但地端這兩個問題都不存在。GPU 已經買了，邊際 token 成本趨近零，logits 完全透明。多跑幾次只是多花推理時間，不多花錢。

用 Qwen 3.8 27B 或 DeepSeek V4 Flash 這類 Intelligence Index = 52 的模型，單卡就能跑。開源模型單次生成的能力確實不如 Fable 5 或 GPT-5.6 Sol，但跑五次 + self-verify，在 Terminal-Bench 上反而贏了。地端的算力冗餘，剛好拿來換品質。

雲端用戶看到的是「多花六倍 token 費」。地端用戶看到的是「免費升級九個百分點」。

---

## 不只是 coding

如果這個框架只在 coding 上 work，故事就到此為止了。但論文跨了三個完全不同的 domain，不需要 domain-specific fine-tuning：

| 領域 | Benchmark | 結果 | 對照基線 |
|------|-----------|:----:|:--------:|
| Coding | Terminal-Bench V2 | 86.5% | 83.1% baseline |
| Coding | SWE-Bench Verified | 78.2% | 76.8% 單一模型最佳 |
| Robotics | RoboRewardBench | 87.4% | 81.4%（專門訓練的 RoboReward-8B）|
| Medical | MedAgentBench | 73.3% | — |

在機器人領域，打敗了**專門訓練過**的 RoboReward-8B 獎勵模型（87.4% vs 81.4%）。一個通用的 verification 框架，靠 logits 加權 + 三軸 scaling，超越了專家模型。

論文還測了 progress tracking：verifier 分數和任務步驟進度之間的相關性（VOC）在成功的 trajectory 上達到 0.966。這意味著 verifier 不只是在任務結束時判對錯，它**在執行過程中就能追蹤 agent 是不是走在正確的路上**。

---

## 實作：怎麼跑起來

論文不只是說說，code 已經開源在 [GitHub](https://github.com/llm-as-a-verifier/llm-as-a-verifier)。

### Python SDK

```bash
pip install llm-verifier
```

核心 API 三個：

```python
import llm_verifier

result = llm_verifier.select(
    problem=problem,
    candidates=candidates,
    criteria={"Correctness": "Does the code solve the problem?"},
)

# 兩兩比較
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

重現 Terminal-Bench 2.1 的結果：

```bash
python scripts/run_bo3.py   # Best-of-3 → 86.5%
python scripts/run_bo5.py   # Best-of-5 → 88.0%
```

### TurboAgent：drop-in proxy

[TurboAgent](https://github.com/llm-as-a-verifier/TurboAgent) 是一個 API proxy，插在 client 和 LLM provider 中間，自動做 generate-then-verify：

```bash
pip install turbo-agent
turbo-agent              # 預設 port 8888
```

Claude Code 只要改一個環境變數就能透明接入：

```bash
ANTHROPIC_BASE_URL=http://localhost:8888 claude
```

Proxy 自動並行送 N 個請求到後端模型，PPT tournament 挑最好的，回傳最佳結果。`http://localhost:8888/visualizer` 可以看到完整的 pipeline DAG。

**Verifier 不能用 Claude**（不開放 logprobs），必須用有 logprobs 的模型——Gemini（Vertex API）或 DeepSeek。

### 地端部署

有自己 GPU 的人，用 vLLM 起一個 OpenAI-compatible server：

```bash
vllm serve Qwen/Qwen3.8-27B --port 8000
```

TurboAgent 指向這個 endpoint，同一個模型當 generator + verifier，邊際成本趨近零。

---

## 適用邊界

**需要有明確的「對錯」。** Terminal-Bench 和 SWE-Bench 有客觀的通過標準。真實專案裡「需求理解是否正確」、「架構選擇是否合理」這類模糊判斷，self-verification 的可靠度還沒被驗證過。

**延遲乘以 N。** 五個候選解意味著五倍的生成時間（不並行的話）。適合 batch，不適合即時互動。

**框架差異。** 圖上三組用的 agent 框架不同，跨框架的比較要謹慎。看單個模型在同一框架內的上升趨勢，比看跨框架的絕對值更有意義。

---

## 最後的觀察

這篇論文讓我們看到：模型的有效智能不是固定值，它是推理策略的函數。

同一個 DeepSeek V4 Flash，單次 79%，五次 + self-verify 就是 88%。不是換了更強的模型，是換了用法。

對地端部署來說，這可能是目前最務實的能力提升路徑——不用等下一代模型，不用花錢買更貴的 API，把手上的開源模型和 GPU 的算力冗餘用起來，讓模型讀自己的大腦，自己驗證自己。

有興趣的人可以自己跑跑看。畢竟，最可靠的驗證方式還是：自己試一次。

---

## 常見問題 Q&A

**Q: LLM-as-a-Verifier 到底在做什麼，跟傳統的 LLM-as-a-Judge 差在哪？**

傳統做法 LLM-as-a-Judge 是讓模型看每個答案然後打 1-5 分，但複雜的 coding 任務裡超過 27% 的評分是 tie——兩個品質明顯不同的解法，模型都打了 4 分，離散刻度的解析度不夠。LLM-as-a-Verifier 的做法是往下挖一層，讀取 logits（模型內部對所有候選 token 算出的機率分佈），把所有 scoring token 的機率拿出來做加權平均。比方說模型內部算出 "7" 機率 0.35、"8" 機率 0.40、"6" 機率 0.15，加權平均得到 7.3 這種連續分數。7.3 vs 7.1 的區分度，遠大於離散的 7 vs 7 的 tie。不需要額外訓練，不需要另一個更強的模型當 judge。

**Q: DeepSeek V4 Flash 從 79% 跳到 88% 這個數字可信嗎，有什麼要注意的？**

79% 到 88% 的提升是在 Terminal-Bench 2.1 上測的，用的是同一個模型、同一套 agent 框架（mini-swe-agent），差別只在推理策略：單次跑 79%，跑三次加 self-verify 到 86%，跑五次到 88%。這條上升趨勢是扎實的。但要注意的是，論文圖表上跟 Fable 5（83%）、GPT-5.6 Sol（88%）的跨框架比較要謹慎看——三組用的 agent 框架不同（mini-swe-agent / Codex / Claude Code），不能把全部差距歸因於驗證策略。建議看單個模型在同一框架內的上升趨勢，比看跨框架的絕對值更有意義。

**Q: 為什麼同一個模型有能力驗證自己的答案，這不是自己改自己考卷嗎？**

生成和驗證是不同的認知任務（cognitive task）。生成是發散的——從零寫出一個解法；驗證是收斂的——看一個現成的解法判斷好不好。判斷一個答案對不對，比從頭想出正確答案容易，這對人類如此，對 LLM 也是。然後關鍵在 logits 層面：模型內部的機率分佈比它最終輸出的那個 token 包含了更多資訊。模型「心裡」對答案品質的判斷，其實比它「嘴上」說出的那個數字更細膩。LLM-as-a-Verifier 做的事情就是把這份細膩挖出來用。論文還測了 progress tracking，verifier 分數和任務步驟進度之間的相關性（VOC）在成功的 trajectory 上達到 0.966，代表 verifier 在執行過程中就能追蹤 agent 走得對不對。

**Q: 這個方法適合地端部署（on-premise）還是雲端 API？**

天然偏好地端部署，理由有兩個。第一，需要讀 logits——自部署的開源模型透過 vLLM 或 SGLang 可以拿到完整的 logits 向量，沒有限制。OpenAI API 只開放 top-5 logprobs，論文說勉強能用但效能不是最好。Anthropic API 完全不開放 logprobs，所以 Claude 不能當 verifier。第二，很燒 token——跑五次生成加重複驗證加多標準評分，token 用量輕鬆是單次的 10-15 倍。雲端 API 帳單直接乘上去，很痛。但地端這兩個問題都不存在：GPU 已經買了，邊際 token 成本趨近零，logits 完全透明。雲端用戶看到的是「多花六倍 token 費」，地端用戶看到的是「免費升級九個百分點」。

**Q: 除了 coding，這個框架還能用在什麼地方？**

論文跨了三個完全不同的領域（domain），都不需要 domain-specific fine-tuning。在 coding 領域，Terminal-Bench V2 達到 86.5%、SWE-Bench Verified 達到 78.2%。在機器人領域（Robotics），RoboRewardBench 上拿到 87.4%，打敗了專門訓練過的 RoboReward-8B 獎勵模型的 81.4%——一個通用的 verification 框架靠 logits 加權加三軸 scaling，超越了專家模型。在醫療領域（Medical），MedAgentBench 達到 73.3%。不過要注意適用邊界：這個方法需要有明確的「對錯」標準，Terminal-Bench 和 SWE-Bench 有客觀的通過標準，但真實專案裡「需求理解是否正確」「架構選擇是否合理」這類模糊判斷，self-verification 的可靠度還沒被驗證過。另外延遲會乘以 N，五個候選解意味著五倍生成時間，適合批次處理（batch），不適合即時互動。
