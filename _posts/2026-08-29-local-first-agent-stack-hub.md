---
layout: post
title: "\"地端AI 系列總覽：從一張消費級顯卡到企業級地端 AI\""
date: 2026-08-29 18:00:00 +0800
permalink: /local-first-agent-stack/
tags: [local-first, Qwen3.8-27B, RTX 5090, inference engine, KV cache, harness engineering, sovereign AI, on-premise, MoE offload, open weights, abliteration, red team, local inference, enterprise AI, agent stack, MTP, speculative decoding, cache economics, 地端部署, 本地推論]
categories: [AI Agent]
description: "\"用 Qwen3.8-27B 跑出 Opus 等級的本地推論，不再是妥協而是策略。這個系列整理了硬體選型、推論引擎、KV Cache 經濟學、Harness 架構、Sovereign AI 路徑，以及安全紅軍實測——從一張 RTX 5090 到企業級地端部署的完整路線圖。\""
author: Wisely Chen
---

2026 年，「用地端」第一次不是退而求其次。Qwen3.8-27B 在 SWE-bench Pro 拿下 61.7，超過 Opus 4.6 Max——一張消費級顯卡就跑得動的模型，第一次在能力上不輸雲端。

這個系列記錄了我從「買一張 5090 試試看」到「企業級地端部署」的完整路徑。每篇都是實測數據，不是理論推導。

## 目錄

- [Qwen3.8-27B 實戰](#qwen38-27b-實戰)
- [硬體與推論加速](#硬體與推論加速)
- [KV Cache 經濟學](#kv-cache-經濟學)
- [Harness 與 Agent 架構](#harness-與-agent-架構)
- [Sovereign AI 與開源主權](#sovereign-ai-與開源主權)
- [安全與紅軍](#安全與紅軍)
- [企業地端部署](#企業地端部署)

---

## Qwen3.8-27B 實戰

Qwen3.8-27B 是這波 local-first 的觸發點。SWE-bench Pro 61.7 超越 Opus 4.6 Max，27B 大小在 RTX 5090 上跑出 100+ tok/s——這不是「堪用」，是「好用」。

| 文章 | 重點 |
|------|------|
| [Qwen3.8-27B 開源：「那就用地端」第一次不是妥協](/qwen-3-8-27b-open-weights-local-security/) | SWE-bench Pro 61.7、RTX 5090 實測、為什麼這次不一樣 |
| [Qwen3.8-27B 斬殺線：別只看 $0.01](/qwen-3-8-27b-blade-killline-frontier-cost/) | 成本結構拆解、frontier 模型的真正威脅 |
| [Qwen3.8-27B 多平台實測 tok/s 整理](/qwen-3-8-27b-all-platform-deployment-guide/) | RTX 3090/4090/5090/PRO 6000/DGX Spark/Mac 全平台數據 |
| [DFlash 2 讓 Qwen3.8-27B 快兩倍](/dflash2-qwen3-27b-twice-as-fast/) | 同模型、同卡，純靠更聰明的推理快兩倍 |
| [YouTube 逐字稿：Qwen3.8-27B RTX5090 SGLang/vLLM/MTP 實測](/youtube-qwen38-27b-rtx5090-sglang-vllm-mtp-transcript/) | 影片版完整實測紀錄 |
| [Qwen 3.7 vs Qwopus3.6-27B-v2](/qwen-3-7-hype-vs-reality-qwopus-3-6-27b/) | 版本演進、社群改版比較 |
| [Qwen 3.5 / 9B 小模型架構](/qwen-3-5-9b-small-model-god-tier-architecture/) | 越級打怪的神級小模型 |

---

## 硬體與推論加速

選硬體決定了你的 token 天花板。選引擎決定了同一張卡能榨出多少速度。這兩件事要一起看。

| 文章 | 重點 |
|------|------|
| [RTX 5090 + Qwen3.6-27B 七種推論引擎實測](/qwen-3-6-27b-rtx-5090-inference-engine-benchmark/) | SGLang/vLLM/llama.cpp/Ollama/LM Studio 完整 benchmark |
| [Inference Engine 選型指南 (2026)](/inference-engine-selection-hardware-strategy/) | 先選硬體策略，引擎自然會浮現 |
| [llama.cpp 合併 MTP：本地推論提速 30-60%](/llama-cpp-mtp-merged-local-llm-2x-speedup/) | Multi-Token Prediction 落地實測 |
| [Gemma 4 加速 3x：Google 把 drafter 整套開源](/gemma4-mtp-drafter-speculative-decoding-open-source/) | Speculative Decoding + Apache 2.0 drafter |
| [Mac 用戶的企業級推理加速](/mac-first-enterprise-inference-stack-mtp/) | Apple Silicon 上的 MTP 加速 |
| [MoE Offload 完全拆解](/moe-offload-deepseek-v3-v4-local-inference-optimization/) | 671B 模型只吃 17GB VRAM 還能跑的原理 |
| [RTX Pro 6000 一週實驗 Day 1-2](/rtx-pro-6000-tier1-local-day1-2-glm52-deepseek-v4-flash/) | GLM 5.2 拿 98 分、DeepSeek V4 Flash 58 tok/s |
| [RTX Pro 6000 一週實驗完賽](/rtx-pro-6000-tier1-week-final-offload-qwen-vl-vllm/) | Offload 天花板 10 tok/s、Qwen VL 工程圖 96% |
| [把 LLM 燒進晶片：Taalas ASIC](/taalas-asic-burn-llm-into-silicon-local-inference-future/) | 推理成本的終局猜想 |

---

## KV Cache 經濟學

Token 不是免費的。KV Cache 是推論成本的隱藏殺手，搞懂它等於搞懂你的 OPEX 結構。

| 文章 | 重點 |
|------|------|
| [Pi 99.93% Cache Hit：10 億 token 只花 $2.65](/pi-cache-hit-99-93-context-compression-roadmap/) | Agent 選型要多盯一個數字 |
| [搞懂快取機制：從 Gemma4 到 Claude Code 省 80% Token](/kv-cache-gemma4-claude-code-save-80-percent-token/) | 快取機制全景拆解 |
| [切模型不用重算 KV Cache：NVIDIA 的線性映射](/cross-model-kv-cache-transfer-nvidia-ridge-regression/) | Cross-model cache transfer 技術 |
| [DeepSeek V4 Flash 為何那麼強：兩年以上的架構革命](/deepseek-v4-flash-disk-kv-cache-50x-economics/) | Disk KV Cache + 50x 經濟效益 |

---

## Harness 與 Agent 架構

模型再強，沒有 harness 就是裸奔。Harness 是讓 AI 能寫 code 但不能自己上 production 的那層控制面。

| 文章 | 重點 |
|------|------|
| [Harness Engineering 架構全景](/harness-engineering-architecture-overview-ai-code-production-guardrails/) | 完整架構圖、四層防護 |
| [Local-first 模型需要 local-first harness](/local-first-model-needs-local-first-harness/) | Kimi K3 用第三方 harness 贏原廠 10 個百分點 |
| [On-Prem 小模型爆發時代](/on-prem-small-model-explosion-2026-shift/) | 為什麼我這週訂了 RTX 5090 桌機 |

---

## Sovereign AI 與開源主權

模型主權不是口號。當你的 weights 在別人的伺服器上，你的產品就在別人手裡。

| 文章 | 重點 |
|------|------|
| [Sovereign AI 不是口號：Sequoia 的四級路徑](/not-your-weights-not-your-product/) | 開源 60 vs 封閉 62 的算術、你該停在第幾級 |
| [老黃買 Hugging Face 在幹嘛？](/nvidia-hugging-face-acquisition-open-source-chokepoint/) | 預判主權 AI，鎖死分銷管道 |
| [開源模型是 AI 新時代的偉大航道](/open-weights-new-era-nvidia-letter-liang-wenfeng/) | 老黃的 X 貼文、梁文鋒 42 頁逐字稿 |
| [YouTube 逐字稿：地端模型到底對我有何用途？](/youtube-local-model-use-cases-transcript/) | 機敏場景、無護欄場景、OPEX 變 CAPEX |

---

## 安全與紅軍

地端模型的另一面：無護欄版本讓紅軍測試變得前所未有地容易——也讓攻擊者的門檻降到了前所未有地低。

| 文章 | 重點 |
|------|------|
| [用無護欄 AI 做黑箱紅軍的兩小時實錄](/uncensored-ai-red-team-black-box-vibe-coding/) | 只給 URL，2 小時 10 個 finding、2 個 PoC |
| [Qwen3.8-27B 開源三天，五個無護欄模型就在你的筆電上](/qwen38-27b-abliteration-three-days-safety-paradox/) | Abliteration 技術拆解、842 道有害 prompt 拒答率歸零 |

---

## 企業地端部署

從一張卡到一個機房，架構決策完全不同。這裡是給認真考慮 on-prem 的人。

| 文章 | 重點 |
|------|------|
| [On-Premise Enterprise LLM 架構完整藍圖](/local-llm-enterprise-architecture/) | 企業級地端 LLM 部署全景 |
| [Fable 5 企業天花板：intelligence-per-dollar](/fable-5-enterprise-adoption-ceiling-intelligence-per-dollar/) | 企業採用的真正瓶頸 |

---

這個系列持續更新。每篇新的實測、選型比較、架構拆解都會加進來。

如果你正在評估 local-first 路線，建議的閱讀順序：

1. 先看 [Qwen3.8-27B 開源](/qwen-3-8-27b-open-weights-local-security/) 理解為什麼現在不一樣
2. 再看 [Inference Engine 選型指南](/inference-engine-selection-hardware-strategy/) 選你的硬體和引擎
3. 然後看 [KV Cache 省 80% Token](/kv-cache-gemma4-claude-code-save-80-percent-token/) 搞懂成本結構
4. 最後看 [Sovereign AI 四級路徑](/not-your-weights-not-your-product/) 決定你要走多深
