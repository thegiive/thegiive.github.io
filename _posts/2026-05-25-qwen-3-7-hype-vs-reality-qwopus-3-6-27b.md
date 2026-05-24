---
layout: post
title: "Qwen 3.7 發表！多面向超越 3.6，社群同步釋出神改版 Qwopus3.6-27B-v2"
date: 2026-05-25 10:00:00 +0800
permalink: /qwen-3-7-hype-vs-reality-qwopus-3-6-27b/
image: /assets/images/qwen-3-7-hype-vs-reality-cover.png
description: "阿里巴巴在 2026/5/20 杭州雲棲大會正式發表 Qwen 3.7，多模態與推理能力全面超越 3.6，LM Arena 一上線就擠進前 15。與此同時，社群把 3.6-27B 拿去蒸餾 Claude 4.7 的神改版 Qwopus3.6-27B-v2 也同期釋出，單卡就能跑、推理 token 還少了 36%，讓大家對「3.7 27B 本地版」的期待直接衝到天際。"
---

![Qwen 3.7 發表](/assets/images/qwen-3-7-hype-vs-reality-cover.png)

## 目錄

- [TL;DR](#tldr)
- [Qwen 3.7 正式發表：三個 SKU、多模態大躍進](#qwen-3-7-正式發表三個-sku多模態大躍進)
- [3.7 比 3.6 強在哪？](#3-7-比-3-6-強在哪)
- [本地玩家的好消息：Qwopus3.6-27B-v2 同期釋出](#本地玩家的好消息qwopus3-6-27b-v2-同期釋出)
- [現在該怎麼選？](#現在該怎麼選)
- [常見問題 Q&A](#常見問題-qa)

## TL;DR

- **Qwen 3.7 於 2026/5/20 杭州雲棲大會發表**，目前推出三個 SKU：**Max**（旗艦）、**Max-Preview**（純文字、deep-thinking 預設開）、**Plus-Preview**（多模態 / vision）
- LM Arena 排名亮眼：**#13 overall（Elo ~1475）、Math #7、Coding #10、Software/IT #9**；多模態的 Plus-Preview 衝上 **Vision Arena #5**
- 官方主打 agent 能力：**單次自主執行 35 小時、單一 session 串 1000+ tool call**；API 已在 OpenRouter 上線（$2.50 / 1M input、$7.50 / 1M output）
- 同期社群釋出 **Qwopus3.6-27B-v2**：用 Trace Inversion 把 Claude 4.7 推理蒸餾進 3.6-27B，MMLU-Pro 子集 **87.43%（贏原版 +2.57pp）**、SWE-bench 子集 **75.25%**，而且推理 **token 少 36%**、單張 RTX 5090 就能跑
- 大家對「3.7 27B 本地版」的期待已經拉滿——這篇幫你把 3.7 跟 Qwopus 兩條線一次看懂

---

## Qwen 3.7 正式發表：三個 SKU、多模態大躍進

又一篇「無聊 IT 架構」系列文,不過這次是熱騰騰的新聞。

阿里巴巴 Qwen 團隊在 **2026/5/20 的杭州雲棲大會**正式發表新一代旗艦 **Qwen 3.7**（preview 約 5/14 就先上線給大家試玩）。這次一口氣推出三個 SKU：

| SKU | 定位 |
|------|------|
| **Qwen3.7-Max** | 旗艦級通用推理模型，API 陸續開放 |
| **Qwen3.7-Max-Preview** | 純文字版，deep-thinking 預設開啟 |
| **Qwen3.7-Plus-Preview** | 多模態 / vision 版本 |

現在可以透過 **chat.qwen.ai、lmarena.ai** 免費試玩，API 也已經在 **OpenRouter** 上線，價格是 **$2.50 / 1M input、$7.50 / 1M output**。

## 3.7 比 3.6 強在哪？

從目前公開的資料看，3.7 在好幾個面向都比 3.6 更上一層樓：

**LM Arena 中立排名（截至 5/20）：**
- Qwen3.7-Max-Preview：**#13 overall（Elo ~1475）**、Math **#7**、Coding **#10**、Software/IT **#9**
- Qwen3.7-Plus-Preview（多模態）：衝上 **Vision Arena #5 lab**——這是 3.6 沒有的能力層級，多模態是這一代最有看頭的躍進

**官方主打的 agent 能力：**
- **單次自主執行 35 小時**不掉品質
- 單一 session 可串 **1000+ tool call**
- 適合長時間、多步驟的 agentic workflow

換句話說，3.7 把重心放在**多模態**跟**長時間自主 agent** 這兩條線，這正是 2026 年企業最想要的能力。至於 SWE-bench / GPQA / AIME 這些傳統 benchmark，官方還沒正式公布，後續值得繼續追。

至於大家最關心的 **open weight 跟 27B 版本**：目前 3.7 還是以 Max / preview 為主，HF 上 Qwen 官方仍是 3.5 / 3.6 的 checkpoint。依照 3.6 的釋出節奏，小尺寸 open weight 通常會在旗艦發表後 **2–6 週**陸續登場，所以「3.7 27B 本地版」很可能就在不遠的路上——這也是社群期待爆棚的原因。

## 本地玩家的好消息：Qwopus3.6-27B-v2 同期釋出

在等 3.7 27B 的同時，社群這邊也丟出一顆很有份量的東西。

開發者 **Jackrong** 把 **Qwen 3.6-27B** 拿去做了深度蒸餾，釋出了 **Qwopus3.6-27B-v2**（GGUF，HF 直接下載）。它的核心方法叫 **Trace Inversion（軌跡反演）**，做法很巧：

> 一般蒸餾是直接拿 Claude / GPT 那種**壓縮過的 reasoning**（結論跳很快、中間步驟被省略）去 fine-tune，結果小模型只學到「會講結論卻不知為什麼」。
>
> Qwopus 反過來：先訓一個 **Trace-Inverter-4B**，把 Claude-4.7-Max 的壓縮輸出**反推回完整的逐步 CoT**，補回中間推理鏈，再塞進 `<think>` 去蒸餾 3.6。

成果數字（作者自報、跑在子集上，供參考）：

| 指標 | Qwopus3.6-27B-v2 | 原版 Qwen3.6-27B |
|------|------------------|------------------|
| MMLU-Pro（350 題子集） | **87.43%** | 84.86%（+2.57pp） |
| SWE-bench Verified（202 題子集） | **75.25%（152/202）** | — |
| 每題正確答案 token 成本 | **918.7** | 1,433.3（**少 35.9%**） |
| CoT 長度 | 短 **52.5%** | — |
| 速度（RTX 5090, Q5_K_M） | 43.9 tok/s | — |
| MTP 加速 | **1.66x** | — |

最有感的不是分數高 2.57pp，而是**「答對一題用的 token 少 36%、思考鏈短一半」**——在本地單卡、context 跟電費都是成本的場景，推理密度變高比多兩分有用太多。

而且它是**真的能跑**：

- base 是 Qwen3.6-27B dense，**native 支援 vision + tool-use**（下載 `mmproj.gguf` 放旁邊就開）
- 量化全餐，**Q4_K_M 16.8GB 是建議平衡點**，一張 24GB 卡綽綽有餘
- 那 75.25% 的 SWE-bench 是在**單張 RTX 5090、160K fp16 context、跑 19h29m、0 失敗**做出來的

幾個要留意的點：它是社群實驗版（作者標明僅供研究、未做完整 safety eval）；不是全面贏，**Math -2pp、Health -4pp** 略退；dense 27B 吞吐（43.9 t/s）低於 MoE 版本（161.9 t/s），是拿速度換推理深度；benchmark 是跑在子集上，當方向參考即可。

## 現在該怎麼選？

分三個場景給個建議：

**要雲端最強、可接受 API 付費：**
→ 直接打 **3.7-Max API**（$2.50 / $7.50 per 1M）。多模態需求尤其值得試 Plus-Preview。

**要本地 / on-prem、open weight、現在就要：**
→ 3.7 27B 還在路上（樂觀估旗艦後 2–6 週），現階段就先跑 **Qwopus3.6-27B-v2**，它是當下「單卡能跑的最強推理型 27B」。等 3.7 27B 一出再無痛升級。

**企業 IT 架構師：**
→ on-prem AI Coding 的 ROI 趨勢只會更好——3.7 把多模態跟長時 agent 往前推、Qwopus 把「同一張卡的有效吞吐」又抬一階。兩條線都朝對企業有利的方向走。

一句話：**3.7 雲端旗艦、Qwopus 本地神改，兩條線同週到位,2026 的 27B 戰場精彩了。**

## 常見問題 Q&A

**Q: Qwen 3.7 現在可以用了嗎？**

可以試玩。透過 chat.qwen.ai、lmarena.ai 免費體驗，Max API 也已在 OpenRouter 上線（$2.50 / 1M input、$7.50 / 1M output）。

**Q: Qwen 3.7 有 27B open weight 可以下載嗎？**

目前還沒有，3.7 先推 Max / preview，HF 上 Qwen 官方仍是 3.5 / 3.6。依 3.6 的節奏，小尺寸 open weight 通常旗艦發表後 2–6 週陸續登場。

**Q: 3.7 比 3.6 強在哪？**

主要在多模態（Plus-Preview 衝上 Vision Arena #5）跟長時間自主 agent（官方主打 35 小時自主執行、1000+ tool call）。LM Arena overall 排 #13、Math #7、Coding #10。

**Q: Qwopus3.6-27B-v2 跟原版 3.6-27B 差在哪？**

用 Trace Inversion 把 Claude 4.7 的完整推理鏈蒸餾進 3.6。MMLU-Pro 子集 87.43%（+2.57pp）、SWE-bench 子集 75.25%，最關鍵是答對一題的 token 成本少 35.9%、思考鏈短一半。代價是 Math / Health 略退、屬社群實驗版。

**Q: 跑 Qwopus 需要什麼硬體？**

Q4_K_M 約 16.8GB，一張 24GB 顯卡就夠。作者的 SWE-bench 測試是在單張 RTX 5090 上跑的。要開 vision 記得把 `mmproj.gguf` 一起下載放旁邊。
