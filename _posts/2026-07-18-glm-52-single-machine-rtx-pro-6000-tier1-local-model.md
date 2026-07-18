---
layout: post
title: "各位觀眾，單機跑 GLM 5.2 成功：借到 RTX Pro 6000，開始探索高性價比的 Tier 1 地端模型"
date: 2026-07-18 09:00:00 +0800
permalink: /glm-52-single-machine-rtx-pro-6000-tier1-local/
image: /assets/images/glm-52-llamacpp-single-machine-cover.png
description: "兩週前我寫說，希望哪一天功成名就，可以在自己腳下跑 GLM 5.2。沒想到幸福來得太突然，今天就跑起來了。從朋友那借到一台裝 RTX Pro 6000 的桌機，接下來要測 GLM 5.2 量化版、DeepSeek V4 Flash、Kimi K2.5 2bit、Qwen3-VL-235B、MiniMax M3——探索一個資安繞不開的問題：如何用高性價比的單機，架出 Tier 1 等級的地端 AI model。"
---

各位觀眾，單機跑 GLM 5.2 成功。

![llama.cpp 單機跑 GLM 5.2 UD-IQ2_M](/assets/images/glm-52-llamacpp-single-machine-cover.png)

我兩週前才寫說，希望哪一天功成名就，可以在自己腳下跑 GLM 5.2。沒想到幸福來得太突然，今天就跑起來了。

今天是資安日，我們就來講一個資安繞不開的議題：如何用高性價比的方式，架設一台 Tier 1 等級的地端 AI model。

## 從 5090 小模型，到更大的野心

我之前已經寫過，OpenClaw + RTX 5090 + Qwen 35B 或 27B 這種小模型的組合，一台機器就可以好好地處理 OpenClaw 這類 agentic 日常秘書工作流。

但再往上走，就需要更大的硬體了。這種等級的機器，通常只能看有沒有公司專案剛好會遇到。

只是，我這次運氣爆棚——從朋友那借到了一台裝 RTX Pro 6000 的桌機。

時間不長。所以現在，我要出發去偉大的航道了。要探尋的是：有沒有可能把 Tier 1 AI model，跑在極高性價比的地端 server 上。

## 預計短期內測試的模型

1. GLM 5.2 量化版
2. DeepSeek V4 Flash 無損
3. Kimi K2.5 2bit
4. Qwen3-VL-235B 無損
5. MiniMax M3 無損

這幾個模型，兼具了現在的：

1. Tier 1 Coding
2. 推理
3. Tier 2 Vision

如果有好的進展，會再讓大家知道。

哇，還是好開心。
