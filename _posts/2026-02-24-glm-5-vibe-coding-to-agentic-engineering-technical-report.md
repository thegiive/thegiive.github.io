---
layout: post
title: "GLM-5 技術報告深度解讀：從 Vibe Coding 到 Agentic Engineering，中國開源的「Opus 時刻」"
date: 2026-02-24 07:00:00 +0800
categories: [AI Agent, AI Coding, 技術報告]
tags: [glm-5, zhipu-ai, agentic-engineering, vibe-coding, swe-bench, huawei-ascend, open-source, benchmark, slime-rl, openclaw]
permalink: /glm-5-vibe-coding-to-agentic-engineering-technical-report/
image: /assets/images/glm-5-benchmark-performance.png
description: "智譜 AI 的 GLM-5 用 744B MoE 架構、28.5 兆 token 預訓練、SWE-bench 77.8% 打贏 GPT-5.2，幻覺率業界最低，API 價格便宜 5-8 倍——而且全部在 10 萬張華為昇騰 910B 上訓練，零 NVIDIA 依賴。技術報告標題 'From Vibe Coding to Agentic Engineering' 精準命名了我們正在經歷的範式轉移。這篇文章拆解 GLM-5 的架構、Benchmark、異步 RL 訓練框架 Slime，以及那個跑了 24 小時、700 次工具調用自主造出 GBA 模擬器的 demo。"
---

今天早上看到 Anthropic 發了一則聲明，指控 DeepSeek、Moonshot AI（Kimi）、MiniMax 對 Claude 進行工業規模的蒸餾攻擊——24,000 個假帳號、1,600 萬次對話。

![Anthropic 蒸餾攻擊指控](/assets/images/anthropic-distillation-attack-no-glm.png)

我盯著這個名單看了一下。DeepSeek、Moonshot、MiniMax 都在上面。但有一家不在——**智譜（Zhipu AI）**。

就是那個兩週前剛發了 [GLM-5 技術報告](https://arxiv.org/abs/2602.15763)、SWE-bench 打贏 GPT-5.2、在 10 萬張華為晶片上訓練出 frontier 等級模型的智譜。

居然沒有 GLM。或許代表他們真的在做自己的事情吧。

這讓我重新回去認真讀了一遍 GLM-5 的技術報告。標題叫 "From Vibe Coding to Agentic Engineering"——這個命名精準捕捉了我們過去半年在觀察的東西：從「跟 AI 聊天寫 code」到「讓 AI 自己當工程師」。GLM-5 不只是在描述自己的能力，它是在給整個產業正在發生的事情下定義。

---

## 30 秒看懂 GLM-5

| 項目 | 數字 |
|------|------|
| 總參數 | 744B，MoE 架構 |
| 活躍參數 | 40B（每 token 只激活 5.9%） |
| 專家數 | 256 個，每 token 激活 8 個 |
| 預訓練 token 數 | 28.5 兆 |
| 上下文窗口 | 200K input / 128K output |
| 注意力機制 | MLA + DeepSeek Sparse Attention (DSA) |
| 訓練硬體 | 100,000 張華為昇騰 910B |
| 授權 | MIT（完全開源） |
| API 價格 | 輸入 $1.00 / 輸出 $3.20 per 1M tokens |

一句話：**744B 參數但推理只用 40B，SWE-bench 打贏 GPT-5.2，全華為晶片訓練，MIT 開源，價格比 frontier 模型便宜 5-8 倍。**

---

## Benchmark：打贏 GPT-5.2，追上 Opus 4.6

![GLM-5 LLM Performance Evaluation: Agentic, Reasoning and Coding](/assets/images/glm-5-benchmark-performance.png)

先看數字。Benchmark 有其局限性，但至少給我們一個錨點。Coding 方面，SWE-bench Verified 77.8%——一個中國開源模型打贏 GPT-5.2（76.2%），只輸 Opus 4.6 三個百分點，一年前不可想像。但 Terminal-Bench 2.0 差距就大了（56.2% vs 65.4%），說明在「持續跟系統互動、處理意外狀況」上還有一段路。推理方面，Humanity's Last Exam with tools 拿下 50.4，超過 Opus 4.6 的 43.4——有工具的場景下表現特別強，跟 Agentic 定位一致。Agent 相關 Benchmark 最亮眼：BrowseComp 75.9、MCP-Atlas 67.8、tau2-Bench 89.7%，測的都是真實環境中多工具長鏈路規劃。

但我覺得最值得關注的是幻覺率。AA-Omniscience 幻覺評測：GLM-5 得 **-1**，GPT-5.2 得 34，Opus 4.6 得 28——比前代改善 35 分。如果可信，意味著 GLM-5 在 coding 場景中幾乎不會「發明」不存在的 API 或已棄用的函式庫。對 Agent 工作流來說，這比跑分重要 10 倍——Agent 的錯誤是會累積的，第 3 步的幻覺會讓第 7 步完全崩潰。幻覺率低 = Agent 能跑更長的鏈路而不偏離。

---

## 三個技術亮點

技術面有三個值得關注的點。

第一，**DSA（DeepSeek Sparse Attention）** 讓 GLM-5 在 200K 上下文下把注意力計算減少約 50%、GPU 記憶體省 33%——對 Agent 場景來說，每一步都在累積上下文，效率比窗口大小更關鍵。

第二，開源的 **Slime RL 框架**（[github.com/THUDM/slime](https://github.com/THUDM/slime)）是我覺得技術報告裡最有價值的部分：它把傳統同步 RL 拆成異步的訓練、推理、經驗池三模組，核心創新 APRIL 允許部分軌跡就送進訓練，讓長鏈路 Agent RL 從「跑不起來」變成「可行」。

第三，最吸睛的 **GBA 模擬器 demo**——24 小時、700 次工具調用、800 次上下文切換，自主構建包含 500+ CPU 指令集的完整模擬器。這不是 HumanEval 等級的「寫一個函數」，而是真正的軟體工程任務。中文社群有個觀察很到位：「GLM-5 會先規劃整體架構，考慮模組分離和效能瓶頸，然後才開始寫 code。」這跟我在 Claude Code 上看到的行為模式很像——好的 Agent 不是馬上生成 code，而是先「想」清楚再動手。

---

## 「From Vibe Coding to Agentic Engineering」：不只是行銷口號

GLM-5 技術報告的標題精準捕捉了一個正在發生的範式轉移。

**Vibe Coding** = 在單一上下文窗口內，靠 prompt 讓 AI 生成 code。模型很擅長寫函數、寫文件、甚至寫整個模組。但它的操作範圍限制在「一次對話」裡。

**Agentic Engineering** = AI 自主規劃、執行、自我修正、跨越幾十個步驟完成端到端的軟體工程任務。關鍵差異是 **horizon**——Agent 需要在長鏈路中維持計畫一致性、從錯誤中恢復、管理環境狀態。

這跟 [Andrej Karpathy 提出的 Vibe Coding 概念](https://x.com/karpathy/status/1886192184808149383) 形成了有趣的對照。Karpathy 今年一月說 Vibe Coding 是「你完全放棄了，只靠 vibes 寫 code」。GLM-5 的技術報告說：不，下一步不是更好的 vibes，是工程化的 Agent。

我自己的觀察也支持這個方向。[上個月寫 Peter Steinberger 的 Agentic Engineering](/peter-steinberger-agentic-engineering-just-talk-to-it/) 時就注意到——越來越多頂尖工程師不是在「寫更好的 prompt」，而是在建構 Agent 能跑的基礎設施（CI/CD、test suite、CLAUDE.md）。

GLM-5 的訓練方法論也反映了這個轉向：mid-training 階段專門加入長上下文 Agentic 數據、Slime RL 框架專門優化長鏈路 Agent 訓練。這不是事後加上去的功能，而是從訓練管線就開始為 Agentic Engineering 設計。

---


## 定價：便宜 5-8 倍，而且開源

| 模型 | 輸入 (per 1M tokens) | 輸出 (per 1M tokens) | 架構 |
|------|---|---|---|
| **GLM-5** | **$1.00** | **$3.20** | 開源 MIT |
| GPT-5.2 | $6.00 | $30.00 | 閉源 |
| Claude Opus 4.6 | $5.00 | $25.00 | 閉源 |
| Kimi K2.5 | $0.60 | $2.40 | 開源 Modified MIT |

GLM-5 的 API 價格是 GPT-5.2 的 1/6 到 1/9。而且是 MIT 開源——你可以自己部署，數據完全不出海。

跟[上個月分析的 Kimi K2.5](/kimi-k2.5-agent-swarm-deep-dive-technical-assessment/) 比，GLM-5 略貴但能力更強（SWE-bench 77.8% vs K2.5 的水準）。兩者都指向同一個趨勢：**中國開源模型的性價比正在碾壓閉源 frontier。**

對企業來說，真正的問題不再是「開源模型夠不夠好」，而是「我還有什麼理由付 5 倍的價錢用閉源 API」。

---

## 社群反應：Pony Alpha 事件

GLM-5 正式發布前，有一個很有趣的事。

2 月 6 日，一個叫 **Pony Alpha** 的神秘模型出現在 OpenRouter 上——沒有署名、200K 上下文、免費 API。開發者在 Reddit r/LocalLLaMA 上測試後發現，coding 可靠度跟 GPT-4o 有得拼，Agent 工作流甚至更好。

後來大家才知道，Pony Alpha 就是 GLM-5。"Pony" 是因為 2026 是馬年（Chinese zodiac）。這是智譜的軟發布策略——先匿名上線收集真實數據，再正式亮相。

正式發布後：
- **股價一週漲 120%**，港股一度觸及 HK$492
- Bloomberg 連發兩篇報導
- 36Kr 的 24 小時 coding demo 報導引爆中文社群
- 知乎上有人寫「測完 GLM-5 我沉默了：國產開源什麼時候變這麼強了」

Simon Willison（Python/Django 社群大佬）也測了，SVG 生成表現參差——鵜鶘畫得不錯，自行車就歪了。這也反映了 GLM-5 目前沒有多模態能力的限制（純文本模型）。

---

## 坦白說

我的觀察可能有偏差。但有幾件事我比較確定：

**確定的部分：**

1. **中國開源模型的 coding 能力已經進入 frontier 區間。** SWE-bench 77.8% 打贏 GPT-5.2，只輸 Opus 4.6 三個百分點。一年前這是不可能的。再加上 Kimi K2.5、DeepSeek 等，中國開源在 coding 領域已經不是「追趕者」，而是「競爭者」。
2. **100% 華為晶片訓練是一個產業信號。** 不管你怎麼看地緣政治，「用非 NVIDIA 晶片訓出 frontier 模型」這件事已經被證明可行。這會影響整個 AI 算力供應鏈的估值邏輯。
3. **沒被列入蒸餾名單，至少說明一件事。** 沒被指控不等於沒做過，也可能只是還沒被發現。但 GLM-5 技術報告裡每一個組件——DSA、MLA、Slime、APRIL——都有完整的技術細節和開源程式碼。在中國 AI 公司集體被質疑「是不是都在蒸餾 Claude」的時候，智譜的缺席本身就是一種回答。

**不確定的部分：**

1. **推理速度是個問題。** 社群反映 GLM-5 大約 17-19 tokens/sec，比競品慢。對 Agent 場景來說，速度 = 成本，因為 Agent 需要大量的推理循環。速度慢意味著同樣的任務要花更多時間和 token。

---

## 不是結論

GLM-5 給我最大的感受不是某個 Benchmark 數字，而是一個產業事實：開源已經非常接近 SOTA 了。

SWE-bench 只輸 Opus 4.6 三個百分點，幻覺率甚至更低，而價格大約是 SOTA 閉源模型的 1/5。除了推理速度慢一點（17-19 tokens/sec），實際使用上沒什麼明顯短板。

更可怕的是組合拳。GLM-5 配上[小龍蝦（OpenClaw）](/openclaw-architecture-deep-dive-context-memory-token-crusher/)——一個是接近 SOTA 的開源模型，一個是純地端的開源 Agent 框架。GLM-5 提供 MIT 開源的 frontier 級推理能力，OpenClaw 提供本地執行、記憶管理、多工具協調的 Agent 骨架。兩個拼在一起，你就有了一套完全開源、完全地端、數據不出門的 AI Agent 技術棧。不用付閉源 API 費用，不用擔心數據上雲。這對企業來說是王炸。

這不是「追趕者終於追上」的故事。這是「當開源模型跟閉源只差 3 個百分點、價格卻便宜 5 倍的時候，你還有什麼理由不自己建」的問題。護城河不在模型本身，而在模型外面——你的 test 有多硬、你的 CI gate 有多完整、你的工程基礎設施能不能承接 Agent 的高速產出。

---

**延伸閱讀：**
- [Kimi K2.5 深度技術評估：Agent Swarm 到底厲害在哪裡？](/kimi-k2.5-agent-swarm-deep-dive-technical-assessment/)
- [當代碼量暴增 10 倍後，到底誰來做 Review？Make CI/CD Great Again](/ai-coding-framework-deterministic-tools-control-ai/)
- [Cursor 前 0.01% 大神倒戈 Claude Code：Agentic Coding 五大支柱完整解析](/cursor-top-user-switch-claude-code-agentic-coding/)
- [OneFlow：重新思考「單一 Agent 就夠了」的邊界](/oneflow-single-agent-vs-multi-agent-rethinking/)
- [從「套殼 1.0」到「套殼 2.0」：為什麼真正該緊張的是 Anthropic](/shell-wrapper-2-anthropic-real-threat/)
