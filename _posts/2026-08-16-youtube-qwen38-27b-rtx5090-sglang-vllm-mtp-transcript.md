---
layout: post
title: "YouTube 逐字稿：千問3.8-27B 用了兩天說說感覺——RTX 5090 SGLang/vLLM/llama.cpp 實測"
date: 2026-08-16 11:00:00 +0800
permalink: /youtube-qwen38-27b-rtx5090-sglang-vllm-mtp-transcript/
image: /assets/images/youtube-qwen38-27b-rtx5090-mtp-thumbnail.jpg
description: "**作者：** Wisely Chen **日期：** 2026 年 8 月 **系列：** AI Coding 實戰觀察 — YouTube 逐字稿 **關鍵字：** Qwen3.8-27B, RTX 5090, SGLang, vLLM, MTP, Speculative Decoding, NVFP4, 地端模型, KV cache, 雲地混合"
---

**作者：** Wisely Chen
**日期：** 2026 年 8 月
**系列：** AI Coding 實戰觀察 — YouTube 逐字稿
**關鍵字：** Qwen3.8-27B, RTX 5090, SGLang, vLLM, MTP, Speculative Decoding, NVFP4, 地端模型, KV cache, 雲地混合

---

## 這集在講什麼

前天 Qwen3.8-27B 開源，官方 benchmark 上 SWE-bench Pro 61.7 贏過 Opus 4.6 Max 的 53.4。benchmark 是官方的，這集講我自己的：把它架在一張 32GB 的 RTX 5090 上，SGLang 和 vLLM 各測一輪，回答一個很實際的問題——**一張消費卡，到底能同時餵幾個人？**

答案：四個人，總吞吐 425 tok/s，每人約 106 tok/s。MTP 是免費午餐：vLLM 開 MTP-2 單人快 73.5%——但同一個 MTP 在 llama.cpp 路線只快 20%，這集也對照了網友的 GGUF 實測。啟動參數全部放在這篇 blog 文章裡。

---

**長度：** 約 17 分鐘

{% include youtube.html id="F67glW4YKAI" %}

### 時間戳

- 0:00 開場：千問3.8-27B 發布背景
- 2:07 SWE-bench Pro 61.7 贏 Opus 4.6 Max，架構延續 3.6
- 5:33 Coding 實測感受：Harness 影響 > 模型影響
- 7:01 測試環境：SGLang / vLLM / llama.cpp
- 7:35 為什麼選 NVFP4？社群說降 1-5%
- 8:25 vLLM + MTP 測試
- 9:09 四人並行甜蜜點：每人 ~106 tok/s
- 10:17 SGLang vs vLLM 框架差異
- 10:46 九成 Opus 4.6 能力的地端模型
- 11:45 DeepSeek V4 Flash + DGX Spark 對比
- 14:57 雲地混合部署架構
- 17:07 結語：消費顯卡以下無敵，雲端之上一換一

---

## 完整逐字稿

### 開場

嗨，大家好，這週又在這邊跟大家講一下。

前天 Qwen3.8-27B 開源，我在 blog 寫了 benchmark 解析：SWE-bench Pro 61.7，贏過 Opus 4.6 Max 的 53.4。benchmark 是官方的數字，今天講我自己的數字。昨天我把它架在我那張 32GB 的 RTX 5090 上，SGLang 跟 vLLM 各測一輪。問題很簡單：**這張卡，到底能同時服務幾個人？**

### 環境：NVFP4 塞進 32GB

模型用 RadixArk 的 Qwen3.8-27B-NVFP4 量化版，27B 才塞得進 32GB，SGLang 加 MTP 推測解碼，一次出 2 個 draft token。

為什麼要這麼斤斤計較？因為它是 dense 模型。網友算過一筆帳：DeepSeek V4 Flash 284B 參數但每次只激活 130 億；這顆 27B 每個 token 全部參數下場，實際計算量反而是對方的兩倍以上。**dense 模型的速度，就是要用力調出來的。** 跑起來 GPU 吃到只剩 1.2GB，其他服務全部要先停掉。

### 單人：113.75 tok/s

單人測試，SGLang 平均 113.75 tok/s，你根本追不上它輸出。對照組：同一顆模型，網友在 96GB 統一記憶體的 MacBook 上跑，每秒只有 5 個 token。**塞得下，不等於跑得動。**

但單人用一張 5090 有點浪費。重點是下一輪。

### 四人並行：這張卡的甜蜜點

四個人同時進來，每人 2,048 tokens 輸出：19 秒全部跑完，總吞吐 425.44 tok/s，每人分到 106 到 108。

**四個人同時用，每個人拿到的速度跟單人幾乎一樣。** 單人 113，四人每人 106，沒有人在排隊。這就是甜蜜點。

### 八人並行：收得了單，跑不動人

那我就貪心改八人。八個請求都完成了，但總時間 54 秒，吞吐掉到 303——比四人還低。完成時間很明顯分三批：18 秒、37 秒、54 秒。KV pool 不夠，實際只有 3-4 人真的在生成，其他人在排隊。**收得了八張單，跑不動八個人。**

### vLLM 與 MTP：一行參數差 73.5%

同一顆模型搬到 vLLM。先講一個坑：0.20.2 載入會報 `lm_head.input_scale` 錯誤，升到 0.27.1 就好。

A/B/C 測試，變因只有 MTP：不開，單人 57.83 tok/s；MTP-2，單人 100.33。**單人快 73.5%，四人總吞吐多 67.2%，就是啟動指令裡的一行。**

但這個收益跟框架關係很大。網友走 llama.cpp/GGUF 路線，同樣一張 5090：MTP 短上下文只快 20%，超過 100K 反而降速，他的結論是「MTP 對 5090 作用不大」。同一個 MTP 頭，原生實作拿到 73%，llama.cpp 拿到 20% 還可能倒貼。**MTP 有沒有用，不要問模型，要問你的框架實作得多好。**

### SGLang vs vLLM

都開 MTP-2：SGLang 四人 425，vLLM 351，低 17%。追極速選 SGLang；生態在 vLLM 就用 vLLM，我現在線上跑的就是 vLLM MTP-2 四人配置。

網友還有一個觀察：他租 96GB 的 RTX Pro 6000 跑 vLLM 滿血版，發現單人推理沒比便宜機器快多少。因為 vLLM 在意的是吞吐，不是單併發。**這類 serving 框架的價值，要用併發去兌現**——單人嫌它不快，四個人一起用就值回票價。

### 坦白說

三件事要老實講。第一，SGLang 測每人 2,048 tokens、vLLM 測 512，不是嚴格 A/B，趨勢可比、百分比別背成定論。第二，這是短輸出吞吐測試，不是 agent 負載，radix cache 也是關的，多 agent 長 context 要另外測。第三，我測的是量化版——網友對比過，Q5 量化版寫的前端有 bug，BF16 滿血版乾乾淨淨。**這集只回答速度，不回答品質。**

### 結論

一張 32GB 的 5090，就是一個四人小團隊的 model server，每人 106 tok/s，體驗跟獨佔沒差多少。MTP 一定要開，不開白白慢 40% 以上。然後不要貪，八人只會讓大家一起排隊，KV pool 就是 32GB 的天花板。

前天講的是 benchmark 上地端第一次不是妥協，今天是把它落到 serving 數字：模型夠強、卡塞得下、四個人用起來是順的。三組啟動參數都在 blog 文章裡，直接拿去跑。

這就是我今天要講的東西，非常謝謝大家，謝謝大家。

---

## 附錄：三組啟動參數

### SGLang 四人（建議配置）

```bash
sglang serve \
  --trust-remote-code \
  --model-path RadixArk/Qwen3.8-27B-NVFP4 \
  --mem-fraction-static 0.98 \
  --attention-backend flashinfer \
  --chunked-prefill-size 2048 \
  --reasoning-parser qwen3 \
  --tool-call-parser qwen3_coder \
  --mamba-full-memory-ratio 4.59 \
  --host 0.0.0.0 \
  --port 30000 \
  --max-running-requests 4 \
  --speculative-algorithm NEXTN \
  --speculative-num-steps 1 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 2 \
  --cuda-graph-max-bs-decode 4 \
  --disable-radix-cache
```

### SGLang 八人（收單多、長輸出會分批）

同上，改兩個參數：`--max-running-requests 8`、`--cuda-graph-max-bs-decode 8`。

### vLLM MTP-2（0.27.1，目前線上運行）

```bash
vllm serve RadixArk/Qwen3.8-27B-NVFP4 \
  --trust-remote-code \
  --served-model-name Qwen3.8-27B \
  --host 0.0.0.0 \
  --port 30000 \
  --gpu-memory-utilization 0.95 \
  --max-model-len 32768 \
  --max-num-seqs 4 \
  --max-num-batched-tokens 8192 \
  --attention-backend FLASHINFER \
  --reasoning-parser qwen3 \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_coder \
  --speculative-config '{"method":"mtp","num_speculative_tokens":2}'
```

---

## 延伸閱讀

- [Qwen3.8-27B 開源：SWE-bench Pro 61.7 贏過 Opus 4.6 Max，「那就用地端」第一次不是妥協](/qwen-3-8-27b-open-weights-local-security/)
- [Gemma 4 加速 3x：Speculative Decoding 不是新玩意，但 Google 這次把 drafter 整套 Apache 2.0 送出來](/gemma4-mtp-drafter-speculative-decoding-open-source/)
- [各位觀眾，單機跑 GLM 5.2 成功：借到 RTX Pro 6000，開始探索高性價比的 Tier 1 地端模型](/glm-52-single-machine-rtx-pro-6000-tier1-local/)
- [5090 三個月從 10 萬變 17 萬：五條技術路徑壓低地端 AI 的硬體門檻](/memory-price-surge-local-ai-five-paths/)
- [昨天 5090 大漲價，今天 DeepSeek 大漲價——雲地混合做對沖可能是王道](/deepseek-v4-api-price-hike-subsidy-end/)
