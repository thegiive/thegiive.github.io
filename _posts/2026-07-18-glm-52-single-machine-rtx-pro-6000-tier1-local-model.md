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

稍微展開一下，為什麼是這五個，還有各自的優缺點。

### GLM 5.2 量化版：開源 coding 第一梯隊，但太大

Zhipu 的開源旗艦，744B MoE（激活 40B），MIT license，1M context。官方報 [SWE-bench Pro 62.1%、Terminal-Bench 2.1 81.0%](https://unsloth.ai/docs/models/glm-5.2)，就是目前開源 coding 的第一梯隊。

缺點就一個字：大。全精度想都不用想，96GB VRAM 只吃得下 2-bit 動態量化（UD-IQ2_M，2.7 bpw，239GB），而且還是要靠 system RAM offload。今天第一次跑起來，generation 大約 5 t/s，離「可用」還有距離，要再調。然後 2-bit 之後智力掉多少，這才是這次真正要驗證的重點。

### DeepSeek V4 Flash 無損：唯一有機會全血跑的 Tier 1

[284B MoE 但只激活 13B](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash)，原生就是 FP4/FP8 混合精度，權重約 160GB。這是五個裡面唯一有機會用「無損」原生精度跑的 Tier 1 模型，而且 13B active 意味著它的推理速度應該會是五個裡最快的。

缺點是它定位就叫 Flash，效率優先，能力上限比不上自家大杯。但如果地端要的是「夠聰明、又真的跑得動」，它可能才是性價比的甜蜜點。

### Kimi K2.5 2bit：上限最高，對硬體最不友善

1T 參數等級的 agentic 模型，五個裡能力上限最高。但 [2-bit 量化（UD-Q2_K_XL）也還有 375GB](https://unsloth.ai/docs/models/tutorials/kimi-k2.5)，得大量 offload 到 system RAM 甚至 SSD，速度堪憂。

測它主要是想回答一個問題：1T 模型壓到 2-bit，剩下的智力還贏不贏 GLM 5.2 的 2-bit？如果贏，那「大模型狠壓」就比「中模型輕壓」划算，這對地端選型是很關鍵的資訊。

### Qwen3-VL-235B 無損：Vision 擔當

235B MoE 激活 22B，官方數字 [MathVista 84.9](https://blogs.novita.ai/qwen3-vl-235b-a22b-vram-how-to-avoid-huge-hardware-costs/)，文件理解是強項，開源 VL 的第一梯隊。地端場景其實很多是「看螢幕截圖、讀掃描檔」，這種 Tier 2 Vision 等級就夠用了。

缺點是 vision encoder 要額外吃 VRAM，而且它的 coding 和純文字推理不是主打。它在這個組合裡的角色是補 vision 缺口，不是主力。

### MiniMax M3 無損：原生多模態 + computer use

[428B MoE 激活約 23B](https://www.morphllm.com/minimax-m3)，原生多模態（圖片、影片輸入都吃）、1M context。官方報 SWE-bench Pro 59.0%、OSWorld-Verified 70.06%。OSWorld 這個數字特別有意思——地端 agent 如果要操作桌面（computer use），這個能力很關鍵。

缺點是 coding 略遜 GLM 5.2，而且 428B 就算原生精度也遠超單卡 96GB，一樣逃不掉 offload。

### 五個放在一起看

| 模型 | 總參數 / 激活 | 測試精度 | 權重大小 | 主打 |
|------|--------------|----------|----------|------|
| GLM 5.2 | 744B / 40B | 2-bit 量化 | 239GB | Tier 1 Coding |
| DeepSeek V4 Flash | 284B / 13B | 原生 FP4/FP8 | 約 160GB | 速度 + 性價比 |
| Kimi K2.5 | 1T | 2-bit 量化 | 375GB | Agentic 上限 |
| Qwen3-VL-235B | 235B / 22B | 無損 | — | Vision |
| MiniMax M3 | 428B / 23B | 無損 | — | 多模態 + Computer Use |

共通的現實是：除了 DeepSeek V4 Flash，每一個都塞不進 96GB VRAM，全部要靠 system RAM offload。這時候決定速度的不是總參數，是激活參數——MoE 激活越少，offload 之後越有機會跑到可用速度。所以這一輪實測真正要回答的問題是：**量化的智力折損、offload 的速度折損，兩個加起來之後，哪一台「單機 Tier 1」是真的可用，哪一台只是跑得起來。**

如果有好的進展，會再讓大家知道。

哇，還是好開心。
