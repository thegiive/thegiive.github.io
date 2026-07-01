---
layout: post
title: "DSpark——DeepSeek 把推理速度再拉高 85%，而且方法開源、跨模型通用"
date: 2026-07-02 06:00:00 +0800
permalink: /dspark-deepseek-speculative-decoding-semi-autoregressive/
image: /assets/images/dspark-speculative-decoding-semi-autoregressive.png
description: "DeepSeek 剛開源 DSpark，一套新的推理加速方法，在 V4-Flash 上實測提速 85%、V4-Pro 提速 78%。更關鍵的是：這套方法不綁 DeepSeek 自家模型，Qwen3、Gemma4 都能用，而且整套訓練框架 DeepSpec 以 MIT 授權開源。這篇用最簡單的方式解釋 DSpark 做了什麼、為什麼重要、對開源生態有什麼影響。"
---

# DSpark——DeepSeek 把推理速度再拉高 85%，而且方法開源、跨模型通用

---

## 為什麼今天想聊這件事

6 月 27 號 DeepSeek 同時做了三件事：

1. V4-Flash 跟 V4-Pro 上線 DSpark 加速，用戶端直接感受到回覆變快
2. 開源 DSpark 論文（33 頁，DeepSeek-AI + 北京大學合著）
3. 開源整套訓練框架 DeepSpec（MIT 授權），附帶 Qwen3、Gemma4 的現成加速模組

第一件事是產品更新，第二件是學術貢獻，但真正讓我停下來的是第三件——他們不只發了自己模型的加速模組，而是**把訓練流程全部開源了，而且預設支援的模型是 Qwen3 跟 Gemma4，不是自家的 V4**。

這等於直接告訴社群：「這套方法不綁我家模型，你拿去用。」

---

## 一、LLM 推理為什麼慢？一個比喻

LLM 生成文字的方式是一個字一個字吐——生完第一個字，才能生第二個字。GPU 算得很快，但大部分時間都在等記憶體搬資料，像是一台跑車被困在紅綠燈，油門踩不下去。

**Speculative decoding**（推測解碼）的解法：找一個跑很快的小模型（drafter）先「猜」接下來的 5～7 個字，然後讓大模型一次性驗證這批猜測。猜對的直接用，猜錯的從錯誤位置重新來。

好處是：大模型一次驗證 7 個字跟生成 1 個字的成本差不多（都是一次 forward pass），所以只要猜對率夠高，速度就能翻好幾倍。

但問題來了——**小模型怎麼猜才能又快又準？**

---

## 二、過去的兩難：猜得準就猜得慢

業界之前主要有兩條路：

**路線 A：一個一個猜（Eagle3）**

小模型按順序猜——猜完第 1 個字，看著第 1 個字再猜第 2 個。準確率高，但猜的過程本身就是序列的，小模型自己就慢。

**路線 B：一次猜一批（DFlash）**

小模型同時猜 7 個字，一步到位。速度極快，但問題是：猜第 5 個字的時候，完全不知道前面 4 個字猜了什麼。結果就是**越後面的位置越不準**——論文管這個叫 suffix decay。

實際數字：DFlash 在對話任務上，第 1 個位置猜對率大概 72%，到第 7 個位置掉到 63%。前面猜錯一個，後面全部連帶作廢。

**猜得準的太慢，猜得快的不準。** 這是 speculative decoding 過去幾年的核心矛盾。

---

## 三、DSpark 的解法：先並行猜，再快速修正

DSpark 的想法很直接：**兩步都做，但讓修正那步幾乎不花時間。**

### 第一步：並行猜草稿（跟 DFlash 一樣快）

所有位置同時出結果，一步搞定。

### 第二步：輕量修正（只看前一個字）

在草稿結果上面跑一個極輕量的修正模組。它不需要看完整的前綴（那就退回 Eagle3 了），**只看「前一個位置猜了什麼字」**，就能做出有效修正。

這個修正的計算開銷有多小？論文實測：整體延遲只增加 **0.6%～1.3%**。幾乎免費。

但效果很明顯——suffix decay 基本消失了。DSpark 繼承了 DFlash「第一個位置準確率高」的優勢，同時又像 Eagle3 一樣「後面的位置不會衰減」。

論文有一個特別漂亮的對照實驗：**2 層的 DSpark 在所有任務上都打贏 5 層的 DFlash。** 加一個輕量修正的效果，比把並行模型堆厚 2.5 倍還好。

### 第三步：動態調度（忙的時候少驗，閒的時候多驗）

前兩步解決的是「怎麼猜得好」，但在真實 serving 場景還有一個問題：**GPU 很忙的時候，驗證太多 token 反而拖慢整體吞吐。**

DSpark 多了一個 confidence head，估算每個位置的猜對概率，再根據即時 GPU 負載動態決定「這次要驗幾個」——閒的時候多驗（反正 GPU 也沒事做），忙的時候只驗最有把握的前幾個。

效果：對話任務的驗證通過率從 45.7% 提到 95.7%。不是猜得更準了，而是**把沒把握的猜測在送去驗證之前就砍掉了**，不浪費大模型的計算資源。

---

## 四、實際提速多少？

DSpark 在 DeepSeek 自家 V4 上的部署結果：

| 模型 | 每用戶回覆提速 | 對比基線 |
|------|-------------|---------|
| **V4-Flash** | **60～85%** | vs MTP-1 |
| **V4-Pro** | **57～78%** | vs MTP-1 |

注意基線是 **MTP-1**——DeepSeek 從 V3 時代就在用的加速方法。所以這不是跟「沒有加速」比，是跟「已經有加速」比，還能再快 60～85%。

在系統吞吐層面：

- 一般負載下：+51% 吞吐
- 極端負載下：最高 +661%（這個數字要打折看——不是 DSpark 快了 6 倍，而是 MTP-1 在嚴格 SLA 下已經撐不住了，分母塌縮導致比值膨脹）

一個重要背景：DSpark 是在 V4-preview 發布**兩週後**就上線替換了 MTP-1。如果效果沒有顯著差距，DeepSeek 不會在生產環境做這種替換。

---

## 五、不只自家能用：Qwen3、Gemma4 全面領先

這是 DSpark 最重要的部分——**它不綁 DeepSeek 自家模型**。

論文用 4 個開源模型做了完整測試，測量每輪解碼平均接受的 token 數（越高 = 越快）：

| 模型 | DSpark vs Eagle3 | DSpark vs DFlash |
|------|-----------------|-----------------|
| Qwen3-4B | **+30.9%** | **+16.3%** |
| Qwen3-8B | **+26.7%** | **+18.4%** |
| Qwen3-14B | **+30.0%** | **+18.3%** |
| Gemma4-12B | 全 9 項 benchmark 領先 | 全 9 項 benchmark 領先 |

**DSpark 在所有模型 × 所有 benchmark 上都是最好的。沒有例外。**

幾個觀察：

- Math 跟 Code 任務每輪平均接受 5～6 個 token，等於大模型一次驗證就搞定 5～6 個字
- Chat 任務較低（3～3.7），因為對話的隨機性比數學推理高，更難預測
- Gemma4（Google 的模型）跟 Qwen3（阿里的模型）效果在同一水準，證明方法本身是通用的

---

## 六、DeepSpec 框架：不只是模型，是完整工具箱

DeepSeek 開源的不只是 DSpark 的加速模組，而是整個 **DeepSpec** 框架：

- **三種加速算法**：DSpark、DFlash、Eagle3，統一 codebase，方便對比
- **完整訓練流程**：資料準備 → 訓練 → 評估，一條龍
- **12 個現成 checkpoint**：4 個模型 × 3 種算法，全部在 HuggingFace 上可下載
- **訓練資料**：Open-PerfectBlend，130 萬樣本（math 39.4%、code 38.9%、chat 17.6%），訓練 10 個 epoch
- **授權**：MIT（最寬鬆的開源授權之一）

如果你在用 Qwen3 或 Gemma4 做推理，現在可以**直接下載 checkpoint 接上去用**。如果你用的是其他模型，DeepSpec 提供了完整的訓練流程讓你自己訓一個。

---

## 七、坦白講：什麼地方要注意

**第一，所有數字都是 DeepSeek 自己測的。** +85%、+78% 這些數字來自 DeepSeek 自己的 serving 環境，沒有第三方獨立驗證。不同的硬體、不同的流量模式，實際提速一定不同。

**第二，模型越大收益越高。** Speculative decoding 的原理是「大模型驗證的邊際成本低」，所以 target model 越大、drafter 跟 target 的速度差距越大，收益越明顯。在小模型（7B 以下）上，drafter 本身的開銷可能吃掉大部分收益。

**第三，動態調度那層沒有完整開源。** DeepSpec 開源的主要是 drafter 的訓練跟評估，Hardware-Aware Scheduler 是針對 DeepSeek 自家 serving stack 做的。其他推理框架（vLLM、SGLang）要整合需要額外工程。

**第四，碰到特別難的問題，加速效果會縮水。** 論文自己也提到：如果查詢本身就很難預測（acceptance rate 低），parallel backbone 的前期計算成本是固定的，猜錯了就浪費了。未來可能的改進是讓難題直接跳過完整草稿生成。

**第五，drafter 跟 target model 要匹配。** 論文的 checkpoint 是用 target model 自己生成的資料訓練的，如果你用了自己 fine-tune 過的版本，drafter 的準確率可能下降，需要重新訓練。

---

## 八、為什麼這件事對開源生態很重要

過去 speculative decoding 的問題不是理論不成熟，而是**工程門檻太高**。你需要設計 drafter 架構、準備訓練資料、訓練模型、跟 serving 框架整合、調整驗證策略——每一步都有大量工程工作。結果就是：論文很多，但真正在生產環境用起來的主要就是 Google（Gemini）跟 DeepSeek。

DeepSpec 把大部分工作打包開源了，而且預設支援的就是社群最常用的 Qwen3 跟 Gemma4。落地門檻從「需要一個推理團隊」降到「下載 checkpoint + 改配置」。

如果 vLLM 或 SGLang 把 DSpark 整合進去（考慮到 MIT 授權，這只是時間問題），開源模型的推理速度會有一波集體提升。

---

## 一句話總結

**DSpark 用一個幾乎不花成本的輕量修正，解決了 speculative decoding「猜得快就猜不準」的老問題，再加上動態調度讓它在真實負載下可用。但真正的重點是：MIT 開源的 DeepSpec 框架讓任何人都能把這套方法用在 Qwen3、Gemma4 或自己的模型上。**

推理加速過去一直是閉源廠商的護城河。DSpark 把護城河填平了一塊。

---

## 相關連結

- **GitHub（DeepSpec 框架）：** https://github.com/deepseek-ai/DeepSpec
- **論文 PDF：** https://github.com/deepseek-ai/DeepSpec/blob/main/DSpark_paper.pdf
- **HuggingFace（V4-Pro-DSpark）：** https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-DSpark
