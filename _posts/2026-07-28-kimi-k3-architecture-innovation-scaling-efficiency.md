---
layout: post
title: "Kimi K3 技術拆解：不是把 K2 放大，是重新定義每單位算力能買到多少智力"
date: 2026-07-28 09:00:00 +0800
permalink: /kimi-k3-architecture-innovation-scaling-efficiency/
image: /assets/images/kimi-k3-architecture-innovation-cover.png
description: "Moonshot AI 發布 2.78T 參數的 Kimi K3，但真正值得看的不是參數量——是三套架構創新（KDA 擴長度、AttnRes 擴深度、Stable LatentMoE 擴寬度）加起來，讓每單位算力的 scaling 效率比 K2 提升了 2.5 倍。這篇拆解架構設計、跑分表現、開源策略，和我覺得最值得注意的限制。"
---

7 月 27 日，Kimi K3 的 weights 準時上了 HuggingFace。如約而至。

在那之前的十天裡，網路上已經鬧得腥風血雨。7 月 16 日 Moonshot AI 發布 K3 的那一刻——2.78T 參數、1M context window、原生多模態——社群的反應不是「又一個大模型」，而是「開源模型的天花板被重新定義了」。大家的共識是 K3 已經超過或等於 Llama 在開源領域的統治地位，成為新的開源 frontier 模型基準線。

這件事的連鎖效應甚至逼出了老黃本人。7 月 24 日，Jensen Huang 用他人生第一則 X 貼文，發出了 [25 家機構連署的公開信](/open-weights-new-era-nvidia-letter-liang-wenfeng/)「Open Weights and American AI Leadership」——Meta、Microsoft、a16z、Hugging Face 都在名單上，缺席的是 OpenAI 和 Anthropic。Huang 在 Axios 專訪裡直接點名 DeepSeek 和 Kimi K3，主張這些中國開源模型應該被廣泛採用。（這整個風向的來龍去脈，我在[上一集 YouTube 逐字稿](/youtube-ai-wind-shift-open-weights-transcript/)裡有完整的梳理。）

而高盛 7 月初的 50 頁報告早就揭示了底層邏輯：[中國模型每個 token 只點亮 3-5% 的參數](/goldman-sachs-china-ai-moe-token-price-war-agent-coding/)，這種極端稀疏的 MoE 架構讓它們在定價上有結構性優勢。K3 用 896 個專家只激活 16 個（不到 2%），就是這條路線的最新、最激進的實踐。

但撇開產業政治和地緣張力，讀完 K3 的技術報告之後，我覺得最值得寫的其實不是「世界第一個開源 3T 級模型」這個標題，而是它背後的架構選擇——K3 的設計哲學是「提升每單位算力能買到的智力」，而不是「把參數堆上去就贏了」。

## K2 → K3：不是等比放大

先看硬數字，感受一下 K3 相對 K2 改了多少東西。

| | K2 | K3 |
|---|---|---|
| 總參數 | 1.04T | 2.78T |
| 激活參數 | 32.6B | 104.2B |
| 層數 | 61 | 93 |
| 路由專家數 | 384 | 896 |
| 每 token 激活專家 | 8 | 16 |
| 注意力機制 | MLA | KDA + Gated MLA 混合 |
| Context window | 128K | 1M |

如果只是簡單放大，你會看到所有數字等比成長。但 K3 不是——注意力結構完全換了，從純 MLA 變成 KDA + Gated MLA 的混合架構。層數從 61 到 93 不是等比，專家數從 384 到 896 也不是等比。

## 三套架構創新，各解一個 scaling 瓶頸

技術報告把 K3 的架構升級總結成三個正交維度。用白話講：

**KDA（Kimi Delta Attention）——擴序列長度。** 傳統注意力機制的 KV cache 隨序列長度線性成長，到了百萬 token 就吃掉大量 GPU memory。K3 的 93 層裡，69 層用低成本的 KDA 處理超長序列，每 3 層 KDA 搭 1 層完整注意力（Gated MLA）提供全局資訊，兩者交替排列。另外 K3 完全不用位置編碼，位置信息靠 KDA 的遞推機制隱式處理，所以從訓練時的 64K 直接外推到 1M 不用改任何設定。效果：KV cache 記憶體減少 75%，百萬 token context 下 decoding 加速 6.3 倍。1M context window 不是行銷噱頭，是這套架構撐出來的。

**AttnRes（Attention Residuals）——擴網絡深度。** 傳統 Transformer 每一層把輸出加到同一條殘差流裡，93 層下來信息會被稀釋。AttnRes 讓每一層可以選擇性地從之前任意深度的表示中讀取，不是只看前一層的累積。效果：訓練效率提升約 25%，額外計算成本不到 2%。

**Stable LatentMoE——擴模型寬度。** 896 個專家只激活 16 個，激活比例不到 2%。但這種極端稀疏很容易訓練不穩定——少數專家被過度使用，其他的形同虛設（expert collapse）。K3 用了一系列改進來解決這個問題：用統計方法自動平衡專家負載（不用手調超參數）、換了有上界的激活函數防止數值爆炸、每個注意力 head 獨立優化。加起來的效果就是讓 2.78T 的 MoE 能穩定訓練。

**三個維度加起來：2.5 倍 Scaling 效率。** 技術報告測得 K3 相對 K2 的整體 scaling 效率提升約 2.5 倍。同樣的算力預算，K3 能把計算轉化成能力的效率是 K2 的 2.5 倍。這個數字比「2.78T 參數」有意義得多——參數量是成本，scaling 效率是投資報酬率。

## Post-Training：不只是 SFT，是分領域 RL 再蒸餾

K3 的 post-training 分三步走：先用 SFT 建立基礎能力，再針對不同領域（長程 coding、通用 agent、推理、視覺）各自跑 RL 訓練出領域專家，最後用多教師蒸餾把所有專家合回一個統一模型。

RL 階段有兩件事值得提。第一，訓練環境是在 1M context 下做的，每個 agent 任務可以呼叫上千次工具，環境狀態可以快速存檔、分叉、重置。第二，Reasoning effort 的 low/high/max 三檔不是推理時才調的參數，而是在 RL 階段就分別訓練出不同預算等級的專家，最後再蒸餾回去——也就是說，「想多久」這件事是訓練出來的能力，不是臨時設定。

## Benchmark：某些領域第一，整體仍在 Fable 5 和 Sol 之後

先說結論：K3 在 Artificial Analysis Intelligence Index 拿到 57.11 分，排名第四，落後於 Claude Fable 5（59.86）、GPT-5.6 Sol max（58.89）和 GPT-5.6 Sol xhigh（57.65）。

但細看各項，K3 在幾個領域是領先的：

| Benchmark | K3 | 最接近競爭者 |
|---|---|---|
| Frontend Code Arena | #1（1679） | Fable 5（1631） |
| Program Bench | 77.8（#1） | — |
| SWE Marathon | 42.0（#1） | — |
| BrowseComp | 91.2（#1） | — |
| MathVision | 97.8（#1） | — |
| OmniDocBench | 91.1（#1） | — |
| Automation Bench | 30.8（#1） | — |
| MCPMark-Verified | 94.5（#1） | Fable 5（87.4） |
| Terminal-Bench 2.1 | 88.3 | GPT-5.6 Sol（88.8） |
| FrontierSWE | 81.2 | Fable 5（86.6） |
| DeepSWE | 67.5 | Fable 5（70.0） |

Frontend Code Arena 排名第一，而且是壓過 Fable 5 的，這個結果算是 K3 最突出的亮點之一。MCPMark-Verified 是另一個值得注意的領先——K3 拿 94.5，Fable 5 只有 87.4，差距超過 7 個百分點。這代表在 MCP tool calling 的可靠度上，K3 有明顯優勢。SWE Marathon 和 Program Bench 也是領先。但在 FrontierSWE 和 DeepSWE 上，Fable 5 仍然更強。

一個值得注意的數據：K3 比 K2.6 少用了 21% 的 output tokens 完成同樣的評測任務。這代表模型效率確實提升了，不是靠「講更多話」來拉分。

不過有個需要誠實面對的問題。Latent Space 指出，K3 在 AA-Omniscience 上的準確率雖然從 33% 提到 46%（+13 個百分點），但幻覺率從 39% 惡化到 51%。知道得更多，但編造的也更多——這是一個需要關注的退化。

## Agent 能力展示：晶片設計、GPU 編譯器、天體物理

技術報告裡有三個 agent 能力的 demo 案例值得提：

1. **自主晶片設計**：48 小時內完成一顆 4mm²、100 MHz、1.46M standard cells 的晶片設計。從需求到佈局全流程自主完成。
2. **MiniTriton GPU 編譯器**：從零寫一個 GPU compiler，包含 tile-level IR、優化 pass、PTX codegen。在部分 workload 上效能與 Triton 持平甚至更好，而且能穩定跑 nanoGPT 訓練。
3. **計算天體物理**：把一個原本需要兩週的分析（評估 300+ 方程式、生成 3,000+ 行 Python）在約 2 小時內完成。

這三個 demo 的共同特點是：不是那種「寫個小工具」的 toy case，而是需要長時間自主推理、多步驟協調的複雜工程任務。尤其是 GPU compiler 那個——能寫出一個可以正確訓練模型的 compiler，對模型的推理深度和代碼品質要求都非常高。

## 開源策略：不只放 weights，而是貢獻整個 serving stack

K3 的開源做法跟一般的「丟 weights 到 HuggingFace」不一樣。Moonshot 同步開源了高效能注意力 kernel、MoE 通訊函式庫、agent 環境沙箱，而且把 KDA 的 prefix caching 實作直接提交到 vLLM 上游，確保 weights 釋出當天就有生產級的 serving 支援。vLLM 在 7 月 22 日也發了 blog 說明 day-0 支援計畫，NVIDIA 和 AMD 雙平台都有。

為什麼這很重要？因為 2.78T 的模型光有 weights 根本跑不起來——你需要特化的 serving 基礎設施才能高效部署。Moonshot 把這些一起開源，社群不用重新發明輪子。

量化也是同樣的思路：K3 用 MXFP4 weights + MXFP8 activations 的混合精度，而且從訓練就開始做 quantization-aware training，不是事後才壓。模型從一開始就學會在低精度下工作，所以不會有事後量化常見的能力退化。不做這件事，2.78T 的模型在任何合理的硬體上都跑不起來。

## 價格：比 Fable 5 便宜 70%，但有條件

K3 的 API 定價：

- Cache 命中輸入：$0.30/MTok
- Cache 未命中輸入：$3.00/MTok
- 輸出：$15.00/MTok

相對於 Claude Fable 5，輸入便宜約 70%，輸出便宜約 70%。相對於 GPT-5.6 Sol，輸入便宜約 40%，輸出便宜約 50%。

重要的前提是：Moonshot 宣稱在 coding workload 上 cache 命中率超過 90%。如果這個數字是真的，那實際使用成本會比帳面價格低很多。Artificial Analysis 測出每個任務的平均成本是 $0.94，而 GPT-5.6 Sol 是 $1.04，Opus 4.8 是 $1.80。

Simon Willison 在 K3 剛上線時做了一個有趣的觀察：他用一個簡單的 pelican SVG 生成測試，花了 25 美分。16,658 個 output tokens 裡有 13,241 個是 reasoning tokens——簡單任務也全力推理。K3 發布初期只有「max」一個 reasoning 等級，後來才加上 low 和 high 模式。但即便如此，這也提醒了一件事：用 frontier model 做簡單任務時，reasoning token 的成本不容忽視。

## 需要注意的限制

說完亮點，講幾個需要誠實面對的問題：

**1. 整體仍落後 Fable 5 和 GPT-5.6 Sol。** Intelligence Index 57.11 vs Fable 5 的 59.86。差距不大，但確實存在。

**2. 幻覺率退化。** 知識準確率提升的同時，幻覺率從 39% 惡化到 51%。知道更多但也編造更多，這個 trade-off 需要注意。

**3. 推理速度偏慢。** 早期觀察約 26-28 tokens/sec，speculative decoding 可能還沒完全啟用。以 2.78T 的模型來說，這個速度在意料之中。

**4. 部署門檻極高。** 官方建議用 64+ accelerator 的 supernode 配置。即使有開源 weights，要自建部署也只有資金充裕的團隊做得起。「開源」不等於「便宜可跑」。

**5. Moonshot 自己承認 UX 有差距。** 相對於 Fable 5 和 GPT-5.6 Sol，用戶體驗仍有明顯差距。模型可能過於主動（excessive proactiveness），在沒有明確指示的情況下做出意外的自主決策。

**6. 依賴 thinking history 保留。** 如果對話中的 thinking history 被截斷或缺失，模型的輸出品質會明顯下降。這對長對話場景的工程設計提出了額外要求。

## 我的觀察

K3 最有意思的地方，不是它在某些 benchmark 上排第一——那些排名會一直變。

而是它證明了一件事：scaling 的方式可以不只是「堆更多參數」。KDA 擴長度、AttnRes 擴深度、Stable LatentMoE 擴寬度——三個正交維度同時 scale，用 2.5 倍的效率把算力轉化成能力。

這個思路對整個產業有意義。當算力成本是硬約束的時候，「同樣的錢能買到多少智力」才是真正的競爭維度。K3 展示了一條在這個維度上走得更遠的路。

另一個值得關注的是開源策略。不是「weights 丟出來你們自己看著辦」，而是連 serving stack 都貢獻上游，確保社群能真正用起來。這種做法會加速整個開源 LLM 生態的成熟。

當然，K3 仍然不是最強的模型。但它是第一個在多個 frontier benchmark 上拿到第一、同時完全開放 weights 的 3T 級模型。在「開源能力上限」這條線上，K3 確實把天花板往上推了一大截。

---

## 數據帳本

| 事實/數字 | 來源 | 驗證狀態 |
|---|---|---|
| K3 總參數 2.78T、激活參數 104.2B、93 層、896 專家、每 token 激活 16 個 | 用戶提供（技術報告摘要）+ MarkTechPost + agent-one.dev | 已驗證（多源交叉確認） |
| K2 總參數 1.04T、激活 32.6B、61 層、384 專家、每 token 激活 8 個 | 用戶提供（技術報告摘要） | 已驗證 |
| 69 層 KDA + 24 層 MLA，3:1 比例交替 | 用戶提供（技術報告摘要）+ agent-one.dev | 已驗證 |
| KV cache 減少 75%、decoding 加速 6.3 倍（1M context） | MarkTechPost + Latent Space | 已驗證 |
| AttnRes 訓練效率提升 ~25%、額外成本 <2% | MarkTechPost + agent-one.dev + Latent Space | 已驗證（多源一致） |
| 整體 scaling 效率比 K2 提升 2.5 倍 | 用戶提供 + 技術報告 + 多篇分析 | 已驗證 |
| Intelligence Index 57.11、排名 #4 | Latent Space（引 Artificial Analysis）+ Augmented Mind | 已驗證 |
| Fable 5: 59.86、GPT-5.6 Sol max: 58.89 | Latent Space + 搜尋結果 | 已驗證 |
| Frontend Code Arena #1（1679）、Fable 5（1631） | Latent Space + agent-one.dev | 已驗證 |
| SWE Marathon #1、Program Bench 77.8 #1 | agent-one.dev + Latent Space | 已驗證 |
| Terminal-Bench 2.1: K3 88.3 vs Sol 88.8 | agent-one.dev | 已驗證 |
| FrontierSWE: K3 81.2 vs Fable 5 86.6 | agent-one.dev | 已驗證 |
| DeepSWE: K3 67.5 vs Fable 5 70.0 | agent-one.dev | 已驗證 |
| BrowseComp 91.2、MathVision 97.8、OmniDocBench 91.1 | agent-one.dev + MarkTechPost | 已驗證 |
| 比 K2.6 少用 21% output tokens | Latent Space | 已驗證 |
| 幻覺率從 39% 惡化到 51%（AA-Omniscience） | Latent Space | 已驗證 |
| 晶片設計：4mm²、100 MHz、1.46M cells、48 小時 | 官方 tech blog + agent-one.dev | 已驗證 |
| MiniTriton：從零寫 GPU compiler、效能與 Triton 持平 | 官方 tech blog | 已驗證 |
| 天體物理：2 週分析 → 2 小時、300+ 方程式、3000+ 行 Python | 官方 tech blog | 已驗證 |
| API 定價：$0.30/$3.00/$15.00 per MTok | 官方 tech blog + agent-one.dev + Latent Space | 已驗證（多源一致） |
| 比 Fable 5 便宜約 70%（輸入/輸出） | agent-one.dev | 已驗證 |
| 比 GPT-5.6 Sol 便宜約 40%/50% | agent-one.dev | 已驗證 |
| Cache 命中率 >90%（coding workload） | 官方 tech blog | 官方宣稱，未獨立驗證 |
| 每任務平均成本 $0.94（vs Sol $1.04、Opus 4.8 $1.80） | Latent Space（引 Artificial Analysis） | 已驗證 |
| MXFP4 weights + MXFP8 activations、從 SFT 開始 QAT | MarkTechPost + agent-one.dev + vLLM blog | 已驗證 |
| 需要 64+ accelerator 的 supernode 配置 | MarkTechPost + agent-one.dev | 已驗證 |
| 推理速度 ~26-28 t/s | Latent Space | 早期觀察值 |
| Pelican 測試：25 美分、16,658 tokens 中 13,241 是 reasoning | Simon Willison | 已驗證 |
| Weights 釋出日期：2026-07-27 | 多源 | 已驗證 |
| KDA prefix caching 貢獻到 vLLM 上游 | vLLM blog（2026-07-22） | 已驗證 |
| vLLM day-0 支援、NVIDIA + AMD 雙平台 | vLLM blog | 已驗證 |
| 93 層組成：1 dense + 69 KDA + 24 Gated MLA | 技術報告（HuggingFace model card） | 已驗證 |
| NoPE（無位置編碼）、位置信息透過遞推門控隱式編碼 | 技術報告 | 已驗證 |
| FlashKDA：CUTLASS-based chunkwise kernel | 技術報告 | 已驗證 |
| SiTU-GLU 激活函數上界 100、防極端稀疏度下激活爆炸 | 技術報告 | 已驗證 |
| MoonViT-V2 視覺編碼器：401M 參數、從頭訓練（非 SigLIP） | 技術報告（HuggingFace model card） | 已驗證 |
| 三階段 post-training：SFT → RL → MOPD | 技術報告 | 已驗證 |
| RL 在 1M context 下訓練、persistent rollout + sandbox | 技術報告 | 已驗證 |
| AgentENV：Firecracker microVM、133ms checkpoint、49ms resume | 技術報告 | 已驗證 |
| Reasoning effort 三等級：low/high/max（初期只有 max） | 官方 tech blog + HuggingFace model card | 已驗證 |
| EAGLE-3 style speculative decoding、7-step unroll | 技術報告 | 已驗證 |
| MCPMark-Verified: K3 94.5 vs Fable 5 87.4 | HuggingFace model card | 已驗證 |
| Prefix caching 粒度：512-token（vs 6,144 physical block） | vLLM blog | 已驗證 |
| 詞彙表大小 160K、attention heads 96、hidden dim 7,168 | 技術報告（HuggingFace model card） | 已驗證 |
| Partial rollout RL + thousands of tool calls per rollout | 技術報告 | 已驗證 |
| Weights 於 7/27 準時釋出到 HuggingFace | HuggingFace moonshotai/Kimi-K3 | 已驗證 |
| Jensen Huang 7/24 第一則 X 貼文、25 家機構連署 Open Weights 公開信 | Fortune + Cryptopolitan + TechSpot | 已驗證 |
| 連署名單含 Meta/Microsoft/a16z/HuggingFace，缺席 OpenAI/Anthropic | Fortune（2026-07-24） | 已驗證 |
| Huang 在 Axios 專訪點名 DeepSeek 和 Kimi K3 應被廣泛採用 | BigGo Finance + Fortune | 已驗證 |
| K3 是目前最大的開源模型（2.78T），超越 DeepSeek V4 Pro（1.6T） | 多源 | 已驗證 |

## 參考來源

- [Kimi K3 Technical Report（PDF）](https://github.com/MoonshotAI/Kimi-K3/blob/master/k3_tech_report.pdf)
- [Moonshot AI 官方 Tech Blog](https://kimi.com/blog/kimi-k3)
- [MarkTechPost: Moonshot AI Releases Kimi K3](https://www.marktechpost.com/2026/07/16/moonshot-ai-releases-kimi-k3-a-2-8-trillion-parameter-open-moe-model-with-kimi-delta-attention-and-1m-context/)
- [Agent One: Kimi K3 Architecture Deep Dive](https://www.agent-one.dev/blog/kimi-k3-agentone)
- [Latent Space: AINews Kimi K3](https://www.latent.space/p/ainews-kimi-k3-28t-a50b-the-largest)
- [Simon Willison: Kimi K3 and the Pelican Benchmark](https://simonwillison.net/2026/Jul/16/kimi-k3/)
- [vLLM Blog: Production-Scale Kimi K3 Support](https://vllm.ai/blog/2026-07-22-kimi-k3-preview)
- [Augmented Mind: The Open-Source Model That Cracked the Frontier Moat](https://augmentedmind.substack.com/p/kimi-k3-the-open-source-model-that-cracked-the-frontier-moat)
- [HuggingFace: Kimi-K3 Model Card](https://huggingface.co/moonshotai/Kimi-K3)
- [Fortune: Jensen Huang's First X Post on Open Source AI](https://fortune.com/2026/07/24/jensen-huang-open-source-letter-nvidia-kimi/)
- [Forbes: Why Kimi K3 Signals A Convergence Toward Open-Weight Models](https://www.forbes.com/sites/geruiwang/2026/07/27/why-kimi-k3-signals-a-convergence-toward-open-weight-models/)
