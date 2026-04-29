---
title: "一張原價屋估價單，看懂 Token 經濟學如何把 DDR 打到天價——還有老黄怎麼把所有路都鎖死"
date: 2026-04-30 07:30:00 +0800
permalink: /ddr-hbm-token-economics-nvidia-lock-supply-chain/
image: /assets/images/ddr-price-quote-cover.png
description: "2026/4/23 一張原價屋估價單：128GB DDR5 漲到 5.2 萬，比 CPU 加主機板還貴 2.7 倍。背後是 Token 經濟學第一性原理把 GPU 的天花板物理鎖定在 HBM 上，再加上老黄把 HBM 御三家 + Groq LPU 全部供應鏈鎖喉的雙重結果。本文拆解 DDR 漲價的真正原因、老黄的供應鏈整合棋局、以及華為 + DeepSeek V4、Google + TurboQuant 兩條繞道。"
---

# 一張原價屋估價單，看懂 Token 經濟學如何把 DDR 打到天價——還有老黄怎麼把所有路都鎖死

## 19 萬的電腦，記憶體比 CPU 加主機板還貴 2.7 倍

前幾天我去原價屋估了一台機，準備跑些本地推理測試。打開列印單我整個傻眼。

這是 2026/4/23 的單子：

| 元件 | 型號 | 價格 |
|---|---|---|
| CPU | Intel Core Ultra 7 265KF（20 核） | $9,700 |
| 主機板 | 技嘉 Z890 AORUS ELITE WIFI7 | $9,490 |
| 顯卡 | 技嘉 RTX 5090 MASTER 32G | $103,990 |
| **記憶體** | **海盜船 VENGEANCE 128GB（64G×2）DDR5-6000 CL40** | **$52,500** |
| SSD | 金士頓 KC3000 2TB | $9,200 |
| 散熱 | DEEPCOOL LE360 V2 水冷 | $2,690 |
| 電源 | 全漢 VITA PM 1000W | $5,290 |
| 機殼 | 全漢 U500-B | $3,990 |
| **總價** | | **$196,850** |

你看出問題在哪了嗎？

**128GB DDR5 記憶體 $52,500，比 CPU + 主機板加起來還貴 2.7 倍，等於半張 RTX 5090。**

去年同期，128GB DDR5 大概 1.2 萬到 1.5 萬就能買到。一年漲了三、四倍。

這不是通膨，也不是匯率。這是 HBM 把 DDR 的產能整個吃掉的結構性後果。

而背後真正的故事，是 token 經濟學第一性原理把 HBM 的需求物理鎖定為指數增長——然後老黄發現了這件事，把上游全包了。

---

## TrendForce 的數字比你以為的還誇張

先把市場數據攤開：

- **2026 Q1：** 一般 DRAM 合約價 QoQ +90~95%
- **2026 Q2：** 再 +58~63%
- **HBM 每 GB 吃掉一般 DRAM 三倍的晶圓產能**
- **SK Hynix 2026 全年的 HBM、DRAM、NAND 全部 sold out**
- **Micron 直接退出消費級記憶體市場**，專注做企業 AI 客戶
- **Goldman Sachs 預測 2026 DRAM 缺口 4.9%——15 年來最慘**

這些不是循環性的供需波動。這是御三家（Samsung、SK Hynix、Micron）主動把產線從 commodity DDR 切到高毛利 HBM 的結果。他們不是不想做 DDR，是做 DDR 賺得太少，產能擠不出來。

那為什麼 HBM 突然變成救命稻草？因為 GPU 的 KPI 已經換了。

---

## 從 DDR 配角到 HBM 主角：KPI 換了，記憶體也跟著換了

DDR3 到 DDR5 走了 15 年——CPU 時代的 DDR 是**配角**，帶寬翻倍 performance 只多不到 20%，過去十年每台電腦的 DDR 容量也只從 7~8GB 變成 23GB。容量、帶寬都跟 CPU 的 KPI 幾乎無關，DDR 廠一直是「錦上添花」。

然後 GenAI 來了。進入推理時代，最高 KPI 整個換掉了。不再是 TOPS / FLOPS，而是：

> **單位電力下的 token 吞吐量，以及單個 user 的 token 速度**

老黄發明「AI 工廠」這個概念就是在講這件事。GPU 不再是賣算力，是賣每秒能吐多少便宜的 token。

而要把 token 吞吐拉到極限，公式很乾淨：

```
Token throughput = batch size × per-user token 速度
```

關於這兩個變數的瓶頸怎麼分別卡在 HBM 的容量跟帶寬，請大家看這段 X 神文：[https://x.com/fi56622380/status/2049347677092278749](https://x.com/fi56622380/status/2049347677092278749)

```
Token throughput = HBM size × HBM bandwidth
```

這就是 AI 推理時代最高 KPI 的硬體第一性原理。

歷史上第一次，HBM 容量直接決定了 GPU 的最高 KPI。

如果 Nvidia 要每一代 token throughput 翻倍，**單卡 HBM size × HBM bandwidth 的乘積就必須代代翻倍。**這不是商業選擇，是物理鎖定。

把 A100 → H100 → B200 → Rubin 這幾代的 token throughput，跟 HBM size × HBM bandwidth 畫在對數軸上，兩條曲線幾乎完全重疊。

> 這條曲線不是巧合，是系統最優化的必然解。

---

## 老黄看穿了這件事，然後把所有路都鎖死

老黄自己在訪談裡講過一句話，意思是：Nvidia 真正做得最好的，**不是 GPU 設計、不是 CUDA、是供應鏈整合**。外界一直把焦點放在架構跟軟體生態上，但他自己最在意的，是把整個上游從晶圓、封裝、HBM、到下游系統廠的節奏全部接到自己手上。

這個視角看下面這兩手棋，會非常清楚。

如果你是老黄，知道 HBM 是你 GPU 的命根子，你會做什麼？

**正面：把 HBM 上游全包下來。**

2026 年 SK Hynix 的 HBM 產能已經 sold out，2027 年也在排隊。Jensen Huang 在 GTC 上明確說了「我們鎖了大部分產能」。Micron 退出消費級就是要把產能挪給 Nvidia。Samsung 也在排隊塞進供應鏈。

**結果：要做 GPU 跟 Nvidia 打的人——AMD、Intel、Cerebras、各家 ASIC 新創——拿不到足夠的 HBM。**

這個圍堵很有效，因為 HBM 是極寡占的市場（全球只有三家），不像晶圓代工至少還有 TSMC、Samsung、Intel 三條路。

**背面：把唯一能繞過 HBM 的路徑也買下來。**

2025 年 12 月，Nvidia 用 200 億美金做了一個「quasi-acquisition」——非排他性 IP 授權合作——把 Groq 的 LPU 技術整碗端走。Tom's Hardware 確認這筆交易包含 Groq 完整的硬體 stack 和 Google TPU 的核心工程師。

Groq 的 LPU 為什麼重要？

> **LPU 完全不用 HBM。**

它把所有模型權重和 KV cache 全部放在 on-die SRAM 上。沒有 off-chip memory access，沒有 HBM 帶寬瓶頸。這是目前**唯一一條不靠 HBM 也能做高速推理的路徑**。

短 batch、高速度的場景（agentic workflow 的 single-user 推理），LPU 有結構性優勢。

老黄不能讓這條路長在別人手上。所以他買了。

Samsung 的 4nm 已經在量產 Groq 3 LPU，預計 2026 Q3 出貨。**老黄一邊鎖死 HBM 御三家，一邊把不靠 HBM 的 LPU 也收編。**所有可能的算力路徑，全部進入 Nvidia 體系。

---

## 不在 Nvidia 體系裡的玩家，都在做同一件事：軟硬整合壓 HBM

老黄把 HBM 御三家跟 LPU 都鎖了，但這個鎖只圍住「願意用 Nvidia 的人」。把鏡頭拉開，**所有不在 Nvidia 體系裡的玩家，最後都殊途同歸地走上同一條路：硬體繞開 HBM 御三家，軟體把單卡 HBM 胃口壓下來。**

**中國軸線：華為 + DeepSeek V4。** 硬體面，長鑫存儲做出 HBM 樣品、華為 Ascend 直接用，品質落後 SK Hynix 一兩代，但重點是「**老黄鎖不到我**」。

軟體面有兩刀：第一刀，[DeepSeek V4 用 CSA 直接「無視 KV」](https://ai-coding.wiselychen.com/deepseek-v4-million-token-csa-hca-attention/)——sparse attention 把 100 萬 token 的 KV 壓成 25 萬條再挑最該算的一小撮，大部分 KV 跳過不讀；第二刀，HCA 把每個 token 的 KV 表徵壓到極限，加起來把百萬 token 的 KV Cache 砍到傳統方案的 **2%**。

然後 [V4 §3.1 那 200 字才是真正的地震](https://ai-coding.wiselychen.com/deepseek-v4-section-3-1-hardware-agnostic-earthquake/)——同一套訓練棧在 NVIDIA GPU 跟華為昇騰 NPU 上都跑出 1.5～1.96 倍加速，**訓練棧已經做到硬體無關**。對手有 192GB HBM、你只有 96GB 國產 HBM 也沒關係，**讓單卡需要的 HBM 變少 + 跑得上國產卡**就好。

**Google 軸線：TPU + TurboQuant。** 硬體面，Google 自己設計 TPU、自己跟 SK Hynix 訂 HBM——他們沒有像老黄那樣去鎖整條產線，只是把 Nvidia 這個中間商拿掉，HBM 還是要付錢給御三家。軟體面，[TurboQuant 用極致壓縮把 KV Cache 跟權重再砍一個量級](https://ai-coding.wiselychen.com/google-turboquant-kv-cache-compression-wall-street-panic/)。整個 stack 雖然還是吃 HBM，但**繞過了老黄的關稅**。

兩邊看似無關——一個被牆外擋住被迫自救，一個是搜尋帝國想擺脫供應商——**但邏輯完全一致：硬體不靠 HBM 御三家，軟體把單卡的 HBM 胃口壓到極限**。這是老黄供應鏈鎖喉之外，目前唯一還能呼吸的縫。

但這對台灣讀者組電腦能不能買到便宜 DDR，暫時還影響不到。御三家把 DDR 產能切去做 HBM 的物理壓力，不會因為有人在牆內或雲端自己玩就消失。

---

## 結論：DDR 漲價不是循環，是結構性外溢

回到最開始的那張原價屋估價單。

**DDR5 128GB 漲到 5.2 萬，不是因為記憶體缺料、不是因為新台幣貶值、不是因為產線出事。**

是因為御三家發現做 HBM 比做 DDR 賺得多得多——HBM 每 GB 吃掉一般 DRAM 三倍的晶圓產能，而 HBM 的毛利又是 DDR 的好幾倍。理性的選擇就是把產線切過去。

而 HBM 為什麼這麼好賺？因為 token 經濟學第一性原理把 GPU 的天花板物理鎖定在 HBM 上。**只要老黄要繼續賣 GPU，HBM 就要代代翻倍，產能必須拉到極限。**

DDR 漲價是這個物理定律的副作用。一般消費者組電腦變貴、企業伺服器記憶體變貴、AI 學界買硬體更難——這些都是 token 經濟學壓力傳導到下游的結果。

**而老黄已經把上游 HBM 包了，把繞過 HBM 的 LPU 也買了。**

整個半導體上游沒有縫可鑽。AMD、Intel、各家 ASIC 新創如果想做 inference 競品，要嘛去搶 HBM 殘羹（Nvidia 吃完才剩的），要嘛自己研發 SRAM-based 架構（但 Nvidia 已經把 LPU 的關鍵 IP 鎖了）。

---

## 數據來源

- 原價屋 2026/4/23 估價單（實拍）
- TrendForce：2026 Q1 DRAM 合約價 QoQ +90~95%、Q2 +58~63%
- Goldman Sachs：2026 DRAM 缺口預測 4.9%（15 年來最差）
- SK Hynix 2026 Q3 法說會：HBM/DRAM/NAND 全年 sold out
- Tom's Hardware：Nvidia $20B Groq IP licensing deal（2025/12/24 announced）
- @fi56622380 推文：[AI 半導體終局推演 2026(I)：當新 token 經濟學範式從 GPU 算力轉移到 HBM](https://x.com/fi56622380/status/2049347677092278749)
