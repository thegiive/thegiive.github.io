---
layout: post
title: "LLM 亂降智不是都市傳說——有人開始用數據追蹤了，企業 IT 該怎麼辦？"
date: 2026-04-16 07:00:00 +0800
permalink: /llm-silent-degradation-enterprise-it-harm-stupidmeter-monitoring/
image: /assets/images/stupidmeter-leaderboard-all-warn-2026-04.png
description: "昨天 Claude 全線降級，我的三個任務全部延誤。StupidMeter 24/7 監控 22 個模型，結果只有 GLM 是 OK，其他全部 WARN。Opus 4.5 排第一、Opus 4.6 掉到第五。貴的不穩定，便宜的也不穩定——價格跟穩定性完全無關。企業 IT 該用雲地混合開源模型架構，前面掛 LLM Proxy，Agent 層做品質 fallback。LLM 已經是水電，就該用水電等級的基建去管。"
---

![StupidMeter Leaderboard：22 個模型的即時監控，GPT、Claude、Gemini、Grok、DeepSeek 全部處於 WARN 狀態](/assets/images/stupidmeter-leaderboard-all-warn-2026-04.png)

## 目錄

- [昨天發生了什麼](#昨天發生了什麼)
- [有人受不了了，開始用數據追蹤](#有人受不了了開始用數據追蹤)
- [數據告訴我們什麼：全部都不穩定](#數據告訴我們什麼全部都不穩定)
- [該怎麼做：雲地混合 LLM 架構](#該怎麼做雲地混合-llm-架構)
- [結論：LLM 已經是水電，就該用水電等級的基建去管](#結論llm-已經是水電就該用水電等級的基建去管)

---

昨天（4 月 15 日），我的 Claude Code 基本不能用。

不是「變慢」，不是「偶爾出錯」，是**打開來就卡住、回應品質直接崩盤**那種不能用。去查 Anthropic Status Page，claude.ai、Claude API、Claude Code——全線 Degraded Performance。90 天 uptime 數字看起來還行（99.1%-99.26%），但那些紅色和橘色的條狀圖說明了一切：**這不是偶發事件，而是持續性的不穩定**。

我當天有三個任務排在 Claude Code 上。結果？全部延誤。

如果你是個人開發者，延誤一天就是延誤一天。但如果你是企業 IT，你的團隊有 10 個人同時在用 AI coding 工具，一天的集體生產力損失，乘上來就是**很具體的成本**。

---

## 有人受不了了，開始用數據追蹤

「LLM 降智」這個詞在社群裡流傳了至少一年。但一直以來都是主觀感受——「我覺得 Claude 變笨了」、「GPT 好像不如以前」。我自己之前寫過 [Opus 4.6 偷偷縮水](https://ai-coding.wiselychen.com/opus-46-shrinkflation-open-source-agent-only-viable-path/)，用 17,871 個 thinking blocks 的數據證明了 thinking 深度被砍 73%。但那仍然是一次性的事後分析，沒有人拿出**持續性**的量化數據。

直到 StupidMeter 出現。

[StupidMeter](https://aistupidlevel.info/) 是一個獨立的 LLM 品質監控平台，24/7 對 22 個主流模型跑自動化 benchmark。不是那種一次性的學術測試，而是**持續性的生產品質監控**——就像你用 Datadog 監控 API latency 一樣，但監控的是模型的「聰明程度」。

它追蹤的維度包括：
- **Correctness（正確性）**：答案對不對
- **Reasoning（推理能力）**：邏輯鏈完不完整
- **7-Axis（七軸評估）**：包含安全性、效率、穩定性等
- **Tooling（工具使用）**：function calling 和工具呼叫能力
- **Price（性價比）**：每分錢換到多少智力

它還有一個 Drift Monitor——專門偵測模型品質的**漂移**。不是比較「這個模型比那個模型好」，而是追蹤「同一個模型，昨天跟今天比，有沒有變笨」。


---

## 數據告訴我們什麼：全部都不穩定

打開 StupidMeter 的 leaderboard，第一眼看到的不是排名，而是那排觸目驚心的狀態標籤：

| 模型 | 狀態 |
|------|------|
| GPT | DEGR（降級） |
| Claude | WARN（警告） |
| Gemini | WARN |
| Grok | WARN |
| DeepSeek | WARN |
| GLM | OK |

**22 個模型裡，只有 GLM 是 OK。其他全部處於異常狀態。**

再看具體排名：

| 排名 | 模型 | 分數 | 趨勢 | 狀態 |
|------|------|------|------|------|
| #1 | Claude Opus 4.5（20251101） | 66 | → | STBL |
| #2 | GPT-5.4 | 63 | ↓ | VOLA |
| #3 | Claude Sonnet 4.5（20250929） | 60 | ↓ | VOLA |
| #4 | GPT-5.2 | 60 | ↓ | VOLA |
| #5 | Claude Opus 4.6 | 60 | ↓ | VOLA |

兩個值得注意的點：

**第一，更新不等於更好。** 排名第一的 Claude Opus 4.5 是去年 11 月的版本，66 分，穩定。最新的 Opus 4.6 排第五，60 分，標記 VOLA（volatile，高波動）。這跟我之前寫的 [Opus 4.6 shrinkflation 分析](https://ai-coding.wiselychen.com/opus-46-shrinkflation-open-source-agent-only-viable-path/)完全吻合——那篇用 17,871 個 thinking blocks 的數據證明了 thinking 深度被砍 73%。StupidMeter 的獨立數據從另一個角度驗證了同一件事。

**第二，貴的不穩定，便宜的也不穩定。** Opus 4.6 output 每百萬 token $25，DeepSeek Reasoner 不到 $0.36，價差 70 倍。但 StupidMeter 上兩邊都標 WARN。GPT 5.4 排第二（63 分），同樣標記 DEGR + UNRELIABLE（「High variance detected」）。**價格跟穩定性完全無關——這不是某一家的問題，是整個產業的結構性特徵。**

---

## 該怎麼做：雲地混合 LLM 架構

StupidMeter 的數據已經告訴我們：**閉源模型的品質不在你的控制範圍內**。廠商可以隨時切版本、調參數、降 thinking 深度，你連通知都收不到。我在[翻 Claude Code 原始碼](https://ai-coding.wiselychen.com/claude-code-telemetry-cache-gate-privacy-vs-performance/)時發現，Anthropic 透過 GrowthBook experiment gates 對你的 CLI 有廣泛的遠端控制能力——不需要你更新版本，不需要你同意。

所以答案不是「選一個更好的閉源模型」，而是**架構上就不能依賴任何單一廠商**。

### 核心原則：雲端主力用開源模型

這是最關鍵的一步，也是大部分企業搞錯的地方。

很多團隊的做法是：雲上用 Claude/GPT 閉源模型當主力，地端放一個開源模型當 fallback。聽起來合理，但一切換就出事——團隊的 prompt、workflow、品質預期全部是針對閉源模型調過的，切到開源模型品質立刻斷崖式下降。這不是 fallback，這是 **fail**。

正確做法是反過來：**雲端主力就用開源模型（GLM、Qwen、Gemma 等）**。你的 prompt engineering、workflow 設計、品質基線全部基於開源模型建立。這樣當你需要切到地端時，跑的是**同一個模型、同一套 prompt、同一個品質預期**。

雲和地的差別只在一件事：**算力成本**。雲上可以調度到更多便宜 GPU，token per cost 更低，throughput 更高。地端的 GPU 資源有限，速度慢一點，但模型品質完全一致。

不能有不同模型的差別。一旦雲和地跑不同模型，你就回到了「切換就降級」的老路。

### 前面掛 LLM Proxy

不管你用幾個模型、幾朵雲、幾台地端機器，前面一定要有一層 LLM Proxy。

LLM Proxy 做三件事：
- **路由：** 根據模型狀態（StupidMeter 告警、延遲、錯誤率）決定請求送去哪裡
- **fallback：** 雲端掛了切地端，地端滿載切雲端，全自動
- **觀測：** 統一記錄每個請求的品質指標，建立你自己的品質基線

### 用 Agent 框架建立 fallback 機制

光有 Proxy 路由還不夠。你的 Agent 層也要有 fallback 邏輯。

舉個例子：[Lobster](https://github.com/panyanyany/lobster)（龍蝦）這類開源 Agent 框架，可以在 Agent 層面設定多模型 fallback。不是「服務掛了才切」，而是「回應品質不對就切」——Agent 可以檢查模型回應是否符合預期格式、是否包含必要的推理步驟，不符合就自動 retry 到備用模型。

這跟 [Harness Engineering](https://ai-coding.wiselychen.com/harness-engineering-architecture-overview-ai-code-production-guardrails/) 的核心理念一致：AI 可以寫 code，但人類（和工程機制）控制信任邊界。模型品質波動只是讓這個邊界需要**自動化的動態調整**。

### 整體架構三層

- **第一層：LLM Proxy** — 接收所有請求，根據 StupidMeter 告警和品質監控做路由，統一記錄觀測數據
- **第二層：雲端 / 地端（同一個開源模型）** — 雲上調度便宜 GPU 跑高 throughput，地端跑同模型做備援，差別只在算力成本
- **第三層：Agent 框架（e.g. 龍蝦）** — 檢查模型回應品質，不符合預期自動 retry 到備用節點

**雲地用同一個開源模型，差別只在算力成本。Agent 層做品質檢查和 fallback。Proxy 層做路由和觀測。** 三層加起來，就是你對 LLM 降智的完整防線。

---

## 結論：LLM 已經是水電，就該用水電等級的基建去管

LLM 對企業 IT 來說，已經不是「可有可無的工具」了。它是水電。你的團隊每天靠它寫 code、做 review、生文件——離開它，生產力直接打折。

但問題是：**你有沒有用水電等級的基建去保障它的穩定？**

水電公司不會只有一座發電廠。電網有冗餘、有調度、有備援。水廠有多水源、有淨水監控、有壓力偵測。停電了有備用發電機，水質異常了有自動切換。

StupidMeter 的全場 WARN 數據告訴我們：LLM 的品質波動是結構性的，不是某一家的問題。既然你已經把它當水電在用，就不能用「插上插頭祈禱不會停電」的心態來管。

**你需要自己的電網：** LLM Proxy 做路由和觀測，雲地混合做冗餘，Agent 框架做品質檢查和自動切換。雲端和地端跑同一個開源模型，差別只在算力成本，不在模型品質。

昨天 Claude 全線降級，我的三個任務全部延誤。這不會是最後一次。差別在於，下次停電的時候，你有沒有自己的備用發電機。

---

## 延伸閱讀

### Claude 降質數據化系列

- [Opus 4.6 偷偷縮水：為什麼 Open Source Agent 架構是企業唯一可行方案](https://ai-coding.wiselychen.com/opus-46-shrinkflation-open-source-agent-only-viable-path/) — 17,871 個 thinking blocks 的數據挖礦，證明 thinking 深度被砍 73%
- [關掉 Claude Code 遙測，效能就被懲罰？](https://ai-coding.wiselychen.com/claude-code-telemetry-cache-gate-privacy-vs-performance/) — GrowthBook experiment gates 的技術鑑識，揭露 Anthropic 的遠端控制機制
- [Opus vs Sonnet：Benchmark 看不太出來的體感差距](https://ai-coding.wiselychen.com/opus-vs-sonnet-real-gap-practical-guide/) — 一個多月的 A/B 實測，長鏈推理和工具呼叫才是真正差距
- [GPT-5.2 基準測試爭議：Token 灌水與第三方評測全面落敗](https://ai-coding.wiselychen.com/gpt-5.2-benchmark-controversy/) — 不只 Claude 會降智，GPT 也會，而且官方 benchmark 不可信

### 企業 AI 風險管理

- [Harness Engineering 架構全景：AI 可以寫 Code，但不能自己上 Production](https://ai-coding.wiselychen.com/harness-engineering-architecture-overview-ai-code-production-guardrails/) — 多層防線架構，模型品質波動正是需要護欄的原因
- [Claude Code 資安最佳實踐：14 條建議，每條都有原始碼撐腰](https://ai-coding.wiselychen.com/claude-code-security-best-practices-source-code-verified/) — 從原始碼驗證的安全配置，包含權限控制和沙箱機制
- [Claude Code 上下文工程：四層壓縮機制的源碼級拆解](https://ai-coding.wiselychen.com/claude-code-context-engineering-four-layer-compression/) — 理解上下文壓縮如何影響模型品質，為什麼長會話會「變笨」

---

## 常見問題 Q&A

**Q: StupidMeter 的測試方法可靠嗎？**

任何 benchmark 都有局限性。StupidMeter 的價值不在於絕對分數，而在於**趨勢追蹤**——同一個模型，同一套測試，分數是上升還是下降。這就像你不需要知道體重計的絕對精度，你只需要知道趨勢。

**Q: 模型降智是不是廠商故意的？**

大部分情況不是。模型降智的原因很多：基礎設施負載、A/B 測試的副作用、模型更新的非預期後果、serving 層的配置變更。之前的 [Claude Code telemetry cache gate 事件](https://ai-coding.wiselychen.com/claude-code-telemetry-cache-gate-privacy-vs-performance/)就是典型案例——不是刻意懲罰，是功能 coupling 的副作用。但故意還是意外，對企業 IT 的傷害是一樣的。

**Q: 開源模型就不會降智嗎？**

開源模型的權重是固定的，所以理論上不會「被遠端降智」。但你的 serving 基礎設施（量化、batching、記憶體壓力）仍然會影響品質。差別在於：出問題時你有原始碼可以 debug。這也是我在 [Opus 4.6 shrinkflation](https://ai-coding.wiselychen.com/opus-46-shrinkflation-open-source-agent-only-viable-path/) 那篇的結論——Open Source Agent + Open Source Model 是企業的終極保險。

**Q: 我的團隊只有 3 個人，也需要做這些嗎？**

至少做第一件事：訂閱監控。這是零成本的。當你看到你用的模型狀態從 OK 變成 WARN，至少你知道今天的 AI 產出要多檢查一下。
