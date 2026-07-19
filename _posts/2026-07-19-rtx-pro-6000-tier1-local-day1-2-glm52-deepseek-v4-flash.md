---
layout: post
title: "單機跑得動 Tier 1 地端 Model 嗎？RTX Pro 6000 一週實驗 Day 1-2：GLM 5.2 拿 98 分、DeepSeek V4 Flash 55 token/s 提前過線"
date: 2026-07-19 14:30:00 +0800
permalink: /rtx-pro-6000-tier1-local-day1-2-glm52-deepseek-v4-flash/
image: /assets/images/rtx-pro-6000-tier1-day1-2-cover.jpg
description: "限期一週的實驗：RTX Pro 6000 + 512G RAM，單機跑 Tier 1 地端 model。Day 1 GLM 5.2 2-bit 量化只有 12 token/s，但 Fable 5 打分數據分析 85、寫文章 98。Day 2 DeepSeek V4 Flash IQ2 全塞進 96GB VRAM，55 token/s 且所有題目全對，商務可用線 40 提前過線。外加一課：網路上的調校教學，實作起來七八成不準。"
---

又到了週日，今天我用影片跟大家介紹一下我現在 RTX Pro 6000 桌機的實測結果。

<div class="video-container">
<iframe width="560" height="315" src="https://www.youtube.com/embed/E8XJ1fn_D8A" title="直接實測 Tier 1 地端 Model：RTX Pro 6000 跑 GLM 5.2 與 DeepSeek V4 Flash" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

單機，跑得動 Tier 1 等級的地端 model 嗎？

這是一個限期一週的實驗。我的機器參數是：一張 RTX Pro 6000 + 512G RAM（朋友好有錢!）。因為是借來的，Windows OS 不能改成 Ubuntu。

而我這台機器，看配置就是要優化 DRAM 優勢，所以跑 MoE DRAM + VRAM 混合是最佳的。

## 第一天：GLM 5.2

一開始跑 [GLM 5.2](https://www.wiselychen.com/glm-52-single-machine-rtx-pro-6000-tier1-local/) 就知道不實際。Pro 6000 的 96GB VRAM 連 1-bit 都塞不下。

744B MoE 應該至少要 4 張 Pro 6000 才跑得動。所以只能 2-bit 量化，並且 VRAM + DRAM 一起來推：部分 MoE 專家進 VRAM，剩下丟 DRAM。

經過一下午 Claude Code Loop Engineering 自動測試，最佳結果是 72 層專家進 VRAM，結算 12 token/s。大概是雲端 Fable 5 的四分之一速度。

慢歸慢，基本 RAG 測驗全對。Agentic task 我讓它接上 Codex 做完整任務：寫程式、Excel 數據分析、上網查資料寫分析文章，再請 Fable 5 當老師打分——數據分析 85 分，文章 98 分。

只能說 GLM 5.2 智力是接近 SOTA 的存在。就算扛著 2-bit 的智力折損，對於地端大部分任務還是簡單。

但是 12 token/s 實戰是不能用的。而且我希望的 GGUF MTP 機制，目前看起來已經進 patch 但是還沒好。我會等全部 model 測完後，再跑一次 KTransformers 看看有沒有更好的結果。

## Day 2：DeepSeek V4 Flash

這是我這次最有希望的組合。梁文鋒的團隊去年就看到 VRAM 牆，架構天生就是為 DRAM + VRAM 混合設計的。而我這台機器就是跑 DRAM + VRAM 混合，可說是我一開始就鎖定 DeepSeek 可以拿最高分。

結果開始有用起來了。

Pro 6000 跑 Unsloth Q8 近無損、不開 MTP，就可以走到 22 token/s。但是很奇怪的是，文件跟我說 Unsloth GGUF 支援 MTP，但是跑起來沒有 MTP。

我看起來要改跑 KTransformers 了——要重編 KTransformers、用 DeepSeek MTP 原生權重才找得回來。但是要跑 KTransformers，可能要編譯半天時間。

所以在那之前，我先跑 IQ2 量化，全部塞進 96GB VRAM。

結果很感人：55 token/s。而且所有題目都全部答對，沒有明顯的品質問題。我原本設定的商務可用線是 40，提前過線。

因為速度跟品質看起來都不錯，我暫緩 KTransformers 這條線到明天，現在正在跑更多 IQ2 + Codex 的測試。

## 過程中學到最多的一課

網路上的調校教學，實作起來七八成不準。不知道是變化太多，還是這些不知道有多少人真的實測過。

舉例：DeepSeek 文件說 GGUF 版有 MTP，真的啟動，找不到。就算問 Fable 5，它一直說肯定可以的，真的跑起來也是被一堆現實打臉。

另外一個隱憂是 HiNet 傳訊息給我：一天用 300G，過線了，再這樣就要短時間降速。這個降速一定會影響到調適的效率，因為每一個 Tier 1 模型都超大。

但是學到超級多東西的!!!! 果然有機器可以跑一次實驗，就把很多地端架設的知識點跑通了。

實踐出真知，才是現在 AI 時代最重要的東西~~~

接下來每天應該都會跟大家回報一下結果~~~

## 附錄：實測數據

影片口播的數字是當下的概略值，下面放 Claude Code 跑完 benchmark 之後整理的精確數據。測試環境統一：RTX Pro 6000（96GB VRAM）+ 512G RAM、llama.cpp b10064、`temperature=0`，速度取 llama-server 的 decode（`predicted_per_second`），VRAM 用 nvidia-smi 在生成期間量測。

### 效能對照

| 模型 | 量化（檔案大小） | 配置 | Decode 速度 | 峰值 VRAM |
|------|-----------------|------|------------:|----------:|
| GLM 5.2（744B MoE） | UD-IQ2_M（222GB） | MoE 專家全放 CPU | 7.7 tok/s | 23.7 GB |
| GLM 5.2 | UD-IQ2_M | 64K context、25 層專家進 VRAM | 10.8 tok/s | 91.7 GB |
| DeepSeek V4 Flash（284B MoE、激活 13B） | Q8（151GB） | 20 層專家留 CPU | 25 tok/s | 91.9 GB |
| DeepSeek V4 Flash | IQ2_M（85GB） | 全部塞進 VRAM | 58 tok/s | 89.6 GB |

### 品質對照（同一套 5 題標準題庫）

| 題目 | GLM 5.2 IQ2_M | DeepSeek Q8 | DeepSeek IQ2_M |
|------|--------------|-------------|----------------|
| 知識問答 | 100% | 100% | 100% |
| 困難推理（過橋 29 分） | 70% | 正確、證明嚴謹 | 正確 |
| 簡單 coding | 100% | 7/7 | 7/7 |
| 複雜 coding | 6/7 | 6/7 | 6/7 |
| 數學（被 11 整除計數） | 0% | 正確 | 正確 |

### 三個重點發現

1. **DeepSeek 從 Q8 降到 IQ2_M 幾乎沒有品質損失。** 5 題結果完全相同，IQ2 在推理題還更省 token（5K vs 15K），速度卻是 2.3 倍。單卡 96GB 的最佳日常配置就是 IQ2_M 全 GPU。
2. **n-gram 推測解碼在部分專家留 CPU 的配置下是負優化。** 草稿接受率只有 37%，被拒絕的草稿讓 CPU 上的 MoE 層多算好幾倍，decode 從 25 掉到 15 tok/s。
3. **MTP 確認：Unsloth 全系列 GGUF 轉檔時都把 MTP 層丟掉了。** 掃描 tensor 表頭最高只到 blk.42，沒有 nextn 權重。本機唯一能用真 MTP 的路是 KTransformers，但要 WSL2 + 編譯 + 下載 340GB 原始權重，換約 1.2 倍加速——在 IQ2 已經 58 tok/s 之後，CP 值太低。

