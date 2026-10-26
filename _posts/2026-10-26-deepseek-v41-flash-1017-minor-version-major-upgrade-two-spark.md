---
layout: post
title: "DeepSeek V4.1-Flash-1017 發布一週之後：依舊是那個性價比之王"
date: 2026-10-26 09:00:00 +0800
permalink: /deepseek-v41-flash-1017-minor-version-major-upgrade-two-spark/
tags: [DeepSeek, V4.1-Flash-1017, DeepInfer, DGX Spark, TensorFold, EXL3, Engram, 地端推理, Artificial Analysis, 開源, 性價比]
categories: [AI 前沿技術]
image: /assets/images/deepseek-v41-flash-1017-local-sonnet-card-1.png
description: "DeepSeek 在 10 月 17 日發布 V4.1-Flash-1017：Artificial Analysis 智力指數從 39 升到 45，每個任務的成本從 $0.48 降到 $0.26，將近砍半，模型卡卻只寫一句 minor update。七月的 V4 Flash 0731 也是同一招，AA 一口氣多 10 分，版本號只多一個日期；另一邊 OpenAI 把大版號從 5.6 跳到 6，GPT-6 Sol 的 AA 只從 47 到 48。這篇拆 DeepSeek 的版本命名邏輯、我自己兩台 DGX Spark 的實測，以及為什麼九天後網路上對它依舊好評居多。"
author: Wisely Chen
faq:
  - question: "DeepSeek V4.1-Flash-1017 為什麼叫小更新，分數卻跳這麼多？"
    answer: "因為 DeepSeek 的版本號語意是：大版號（V4、V4.1）代表架構和預訓練改變，日期後綴（0731、1017）代表同一副架構、重做後訓練（Post-training）。2026 年 7 月的 V4 Flash 0731 也是同樣模式，架構維持 284B 總參數、每 token 激活 13B，當時版本的 Artificial Analysis 智力指數從 40 升到 50。10 月 17 日的 1017 同樣只加日期，AA 智力指數從 39 升到 45，每任務成本從 $0.48 降到 $0.26。"
  - question: "DeepSeek V4.1-Flash-1017 跟 Claude Sonnet 5.5 差多少？"
    answer: "依 Artificial Analysis 智力指數，1017（max）是 45 分、每任務 $0.26；Claude Sonnet 5.5 開 high 是 47 分、每任務 $0.88；GPT-6 Astra 開 low 是 46 分、$0.82。分數只差 1 到 2 分，成本不到三分之一。但 Sonnet 5.5 開到 max 是 56 分，跟 1017 差距明顯，所以比較時要說清楚用的是哪個推理強度（Reasoning Effort）。"
  - question: "763B 參數的模型，兩台 DGX Spark 怎麼放得下？"
    answer: "763B 由 552B 的 MoE 骨幹和 196B 的 Engram 條件記憶表（Engram Conditional Memory）組成。Engram 表是查表結構，可以留在 SSD 按需讀取，不必進 GPU 記憶體。骨幹用 EXL3 量化（Quantization）到 2.9 bpw 約 196 GiB，分到兩台 DGX Spark（每台 GB10、128 GB 統一記憶體）各約 98 GiB，用 TensorFold 做張量平行（Tensor Parallelism）。Engram 表約 203 GB，兩台都要放本機 NVMe，走 NFS 會讓 prefill 掉到每秒 690 到 890 token。"
  - question: "兩台 DGX Spark 跑 1017 實際有多快？"
    answer: "作者自己的兩台 DGX Spark 用 Mia-AiLab 的 EXL3 2.9 bpw 量化加 TensorFold，單串流 code 每秒 115 token、prose 每秒 67 token（輸出 400 token、thinking 關閉、每類 3 次中位數）。社群的 tonyd2wild 配方單串流 73.1 tok/s、4 串流合計 135.8 tok/s。三台改用 3.75 bpw，速度跟兩台差不多，換到的是精度。"
  - question: "DGX Spark 能用 DeepSeek 開源的 DeepInfer 嗎？"
    answer: "目前不行。DeepInfer 是 DeepSeek 在 2026 年 10 月 20 日以 Apache-2.0 開源的推理框架（Inference Framework），README 預設 checkpoint 是 V4.1-Flash-1017，但支援硬體只列 NVIDIA SM100 和華為昇騰 950，沒有 DGX Spark 的 GB10。Spark 上跑 1017 用的是 TensorFold 或 vLLM。vLLM 在 10 月 24 日宣稱，已在 DeepSeek 的 decode 配置上追平 DeepInfer 的效能。"
---

DeepSeek 是我目前看過最不愛營銷的 AI 公司之一。

V4.1 在 9 月出了一版，10 月 17 日又出了一個 1017 版本。Artificial Analysis（AA）的智力指數從 39 升到 45，每個任務的成本從 $0.48 降到 $0.26，將近砍半。

這種等級的升級，換別家早就開一場發表會，從 V4.1 直接跳到 V5，大談特談了。

它的模型卡只寫一句：這是 V4.1-Flash 的一次小更新（minor update）。

而且這不是 DeepSeek 第一次這樣做。

<nav class="post-toc" markdown="1">
**目錄**

* 目錄
{:toc}
</nav>

---

## 30 秒定位

| 項目 | 內容 |
|------|------|
| 發布日 | 2026 年 10 月 17 日 |
| 官方定位 | V4.1-Flash 的一次小更新（minor update），API 名稱還是 `deepseek-flash` |
| 規模 | 兩份模型卡的 safetensors 都標 763B；拆開是 552B 骨幹加上 196B 的 Engram 記憶表 |
| 第三方 | AA 智力指數從 39 升到 45，每個任務的成本從 $0.48 降到 $0.26 |
| 分數接近的對手 | Claude Sonnet 5.5（high）47 分、$0.88；GPT-6 Astra（low）46 分、$0.82 |
| 推理框架 | 10 月 20 日開源的 DeepInfer，README 寫的預設 checkpoint 就是 1017 |
| 我的部署 | 兩台 DGX Spark，2.9 bpw EXL3 + TensorFold，單串流 code 115 tok/s、prose 67 tok/s |

---

## 一、DeepSeek 不是第一次這樣做

七月那次，V4 Flash 升到 V4 Flash 0731，AA 智力指數也是一口氣多了 10 分（當時版本的 AA 指數，從 40 升到 50）。AA 的原文寫得很清楚：架構和價格都跟 4 月那版一模一樣，284B 總參數、每 token 激活 13B。

那時候它也只是在版本號後面加了一個日期。

對照組是 OpenAI 的 GPT-6 Sol。大版號從 5.6 直接跳到 6，AA 智力指數（max）只從 47 到 48。上線後 Codex 的 GitHub 上還有人開 issue，標題就叫「GPT-6-sol is extremely slow」。

一個把新版號喊得很大聲，一個把大升級寫成小更新。

| | 版本號變化 | AA 智力指數 |
|---|---|---|
| DeepSeek V4 Flash → 0731 | 只加日期 | +10（40 → 50，當時版本） |
| DeepSeek V4.1 Flash → 1017 | 只加日期 | +6（39 → 45） |
| OpenAI GPT-5.6 Sol → GPT-6 Sol | 大版號 5.6 → 6 | +1（47 → 48） |

先講清楚一件事：0731 的 40 到 50，和 1017 的 39 到 45，用的不是同一版 AA 指數。AA 後來改版換了題目，在現行版本裡 0731 只剩 34 分。所以兩次只能各自跟前一代比，不能拿 50 去比 45。

---

## 二、版本命名邏輯：也不用神話它

當然也不能神話人家。DeepSeek 不是刻意低調，它只是照自己的規則訂版號。

從過去幾版看下來，DeepSeek（創辦人梁文鋒，社群叫他梁聖）的版本號是這樣用的：

- **大版號（V4 → V4.1）**：換架構、換預訓練。從 V4 到 V4.1，參數從 284B 翻到 552B，架構也改了，這才叫升版。
- **日期（0731、1017）**：同一副骨架，重做 post-training。

1017 的兩份模型卡都標 763B，AA 兩版都列 552B 總參數、每 token 激活 16B，官方只提到用了 self-feedback 的強化學習。骨架沒動，重新教了一遍。

**架構不動，對地端部署是好消息。** tensor 形狀沒變，9 月為 V4.1 寫好的量化工具、TensorFold 的 kernel、vLLM 的 patch，換一份權重就能跑。x00byte 在 NVIDIA 論壇 10 月 17 日就貼出雙機配方，tonyd2wild 兩台版的跑測資料夾日期是 10 月 18 日。

發布隔天，DGX Spark 的配方就出來了。如果它叫 V5、改了架構，這些配方全部得重寫。

---

## 三、我自己實測：日常好用又便宜

我自己實測之後，感想就一句話：日常好用又便宜的模型。

我的部署是兩台 DGX Spark（每台 GB10、128 GB 統一記憶體）：

- Mia-AiLab 的 EXL3 2.9 bpw 量化 + TensorFold，兩台做張量平行
- 單串流 code 115 tok/s、prose 67 tok/s（輸出 400 token、thinking 關閉、每類跑 3 次取中位數）
- 1M context 設定好，長提示實測到 33K，工具呼叫、Vision 都測過

實際拿來寫 code，體感很舒服。

分數上，它落在 Sonnet 5.5（high）跟 GPT-6 Astra（low）那一帶：

| 模型 | AA 智力指數 | 每任務成本 |
|------|-----------|-----------|
| Claude Sonnet 5.5（high） | 47 | $0.88 |
| GPT-6 Astra（low） | 46 | $0.82 |
| DeepSeek V4.1-Flash-1017（max） | 45 | $0.26 |

大小任務都有這個等級的程度，分數也接近。唯一的差別是 DeepSeek 便宜很多，每個任務的成本不到它們的三分之一。

### 763B 為什麼兩台放得下

763B 看起來塞不進 256 GB，但拆開算：

- **骨幹 552B**：量化到 2.9 bpw 是 196 GiB，每台約 98 GiB。
- **Engram 表 196B**：Engram 表可以留在 SSD，用到才載入。Mia 的配方不量化這兩張表，約 203 GB，兩台都要放本機 NVMe。

我 10/17 發布當天的判斷是「763B 參數不是多數人跑得動的東西」，現在要修正：763B 裡有 196B 是可以放硬碟的查表，真正要進記憶體的是 552B 骨幹。

### 會卡住的四個地方

1. **Engram 表不要走 NFS。** Mia 的實測是走 NFS 的隨機讀延遲是本機的十倍左右，prefill 會掉到每秒 690 到 890 token。
2. **head 那台的記憶體很緊。** Mia 配方驗證過的 context 是 524,288；開到 655,360 時 head 那台記憶體不夠，rank 0 被砍掉。
3. **鎖頻。** 兩台都要鎖在 2,200 MHz，一台掉到 1,800 MHz prefill 就少 3% 到 6%。
4. **不要為了快選 2.5 bpw。** 社群回報 2.5 bpw 約 185GB、code 約每秒 107 token，但工具呼叫是掉最多的。

### 兩台、三台還是四台

社群另外幾套配方的單串流數字：tonyd2wild 的 2.9 bpw 兩台版 73.1 tok/s，4 串流合計 135.8；easthambuilds 的 3.75 bpw 三台版 prose 每秒 68 到 74 token、code 112 到 123 token，跟兩台差不多快。**多一台換到的是精度，不是速度。** 四台就能直接跑官方權重，不用再量化。

跟我 10/09 測舊版 V4.1 比，那時候兩台 Spark 用 vLLM 最多同時 2 個請求，我說它「上不上下不下」。現在換成 TensorFold，變的主要是引擎，不是模型。這跟我 10/14 的結論一樣：同一個模型，部署方式的影響比換模型大。

---

## 四、價格是路邊小店，但是品質可不輸

我們看過太多模型一開始好評如潮，後來就沉下去了。Kimi K3 一度排到 AA 總榜第三，之後在開源權重的排名一路往下掉。

但 1017 發布九天後，網路上對它依舊是好評居多。

Yuchen Jin 說它在 DeepSWE 上是 Opus 5 等級、成本低 83 倍，Databricks 會上架。Yum 在 OpenCode 裡測了兩天，說它在一般 coding 上明顯贏過 GLM 5.3 Flash，體感接近 Sonnet 級。Paweł Huryn 拿兩個 repo、105 個隱藏 bug 去測，1017 找修 34 個，前一版只有 21.7 個；他測完還補了一句：

> "Strange that the model wasn't labeled V4.2."

很奇怪，這個模型怎麼沒叫 V4.2。

負面的也有：想太久才動手、細的指令讀不懂、gosrum 在本地跑 Terminal-Bench 4.0 測到 1017 輸給舊版。中文圈的邦法（[@bangbuilds](https://x.com/bangbuilds/status/2114238746627559897)）把兩邊合成一句：

> 「能让人一边骂一边用的，才是真的好用。」

我覺得它能一直維持好評，是因為 DeepSeek 永遠堅持幾個點：

- **一開始就不瞄準 SOTA**，省下很多力氣。
- **就是跟你拼性價比。**
- **堅持開源。** 權重 MIT，現在連推理框架 DeepInfer 都開出來了。
- **不拼營銷。** V4 0731 跟 V4.1 1017 都是最好的例子。

### DeepInfer：連推理框架都開了

10 月 20 日 DeepSeek 以 Apache-2.0 開源 DeepInfer，我那天寫過一篇[拆它的部署文件](/deepseek-deepinfer-open-source-inference-design/)：單一集群每天 155 兆 token、離峰價每卡每小時營收 38 美元，但 KV cache 系統、Prefill／Decode 分離、跨副本負載平衡三樣不在 repo 裡。

README 寫的預設 checkpoint 就是 1017。1017 負責「輸出更短」，DeepInfer 負責「每個 token 更便宜」，兩邊乘起來才是那 38 美元。

之後 vLLM 在 10 月 24 日說，在 DeepSeek 的 decode 配置、batch 8 到 256 之間追平了 DeepInfer。有人指出兩邊用的卡不一樣，比較不算乾淨，但方向很清楚：DeepSeek 開出來的 kernel，被通用框架吃進去了。另外 DeepInfer 的硬體只列 NVIDIA SM100 和華為昇騰 950，沒有 GB10，所以 Spark 上跑 1017 走的是 TensorFold 和 vLLM。

### 必比登推介

如果用餐飲來講，Opus 5.5 是米其林的法式料理，DeepSeek 不是那種店。

它比較像路邊小吃店，但是拿了必比登推介：價錢親民，水準一點都不馬虎。而且它還把食譜公開，讓你在家自己煮。

你還能挑啥？

---

## 附記：OpenCode 的免費方案

真的想先試，OpenCode 有一定額度的免費方案，不用付費就可以嚐鮮。

但要上 prod，建議啦，還是自己部署。我不確定 OpenCode 背後是哪個站台在 serve，而社群也有人提醒，有些第三方服務給的是 Q4 甚至 Q2 的量化版，這會把 agent 工作流打壞。

---

## 反方：兩台 Spark 上，升級可能被量化吃掉

這段要攻擊第三段的前提。

easthambuilds 在兩台 Spark 上比了三個 2.9 bpw 的量化，發現舊 V4.1 的量化，品質追平或勝過兩個 1017 的 2.9 bpw 量化。加上 gosrum 在 Terminal-Bench 4.0 上測到 1017 輸給舊版。

如果這兩件事都成立，那「兩台 Spark 跑得動 1017」和「兩台 Spark 拿到 1017 的升級」是兩件事。官方表上 Terminal-Bench 4.0 從 31.2 到 42.3 的跳幅，是全精度、DeepSeek 指定 harness 的數字。

我的回應是部分接受。tonyd2wild 的 69 個情境工具評測，兩台 2.9 bpw 跟四台 3.5 bpw 都是 97.1，在工具呼叫這一層沒有明顯掉。我自己的體感也是好用。但 69 個情境是他自己的題庫，我的體感也不是 benchmark。**兩台 Spark 版的 1017，品質要用你自己的工作流重新量。**

---

## 坦白說

- **「性價比之王」要加條件。** 只看 AA 的每任務成本，MiMo-V2.6-Pro 46 分、$0.13，GPT-6.1 Sol（medium）48 分、$0.21，都比 1017 的 45 分、$0.26 更高分又更便宜。1017 真正的優勢是幾件事加在一起：MIT 開源權重、能在兩台 Spark 上自己跑、推理框架也開源。
- **GPT-6 Sol 也不是沒進步。** 它的智力分數只多 1 分，但每任務成本從 $1.99 降到 $1.04，也砍了將近一半。我拿它當對照，比的是版本號和智力分數，不是整體進步幅度。
- **我的實測是體感加一組速度數字。** 速度是每類跑 3 次的中位數，1M context 只設定好，滿 1M 沒有跑過。社群配方的數字都是作者自報。
- **「架構不變」是推論。** 依據是兩份模型卡都標 763B、AA 兩版都列 552B 和 16B 激活、配方換權重就能跑。1017 官方沒有一句話直接說架構不變，0731 那次 AA 有寫。

但它做對了一件事：用日期後綴而不是新版號，等於承諾「你手上的部署可以繼續用」。發布隔天就有人在兩台桌上機器跑起來，這個承諾是兌現了的。

---

## 關鍵洞察

1. **看 DeepSeek 的版本號，先分大版號和日期。** 日期後綴代表同一副骨架、重做 post-training，部署配方可以直接換權重沿用；大版號才需要重新評估硬體。
2. **算成本看每任務花多少，不是看每百萬 token 多少。** 1017 的價目表沒動，每任務成本卻從 $0.48 降到 $0.26。
3. **兩台 Spark 跑 1017，2.9 bpw、Engram 放本機 NVMe、鎖頻 2,200 MHz 是三個不能省的條件。**
4. **要上 prod 就自己部署，不要依賴不知道量化等級的免費中轉。**

---

## 常見問題 Q&A

**Q: DeepSeek V4.1-Flash-1017 為什麼叫小更新，分數卻跳這麼多？**

因為 DeepSeek 的版本號語意是：大版號（V4、V4.1）代表架構和預訓練改變，日期後綴（0731、1017）代表同一副架構、重做後訓練（Post-training）。2026 年 7 月的 V4 Flash 0731 也是同樣模式，架構維持 284B 總參數、每 token 激活 13B，當時版本的 Artificial Analysis 智力指數從 40 升到 50。10 月 17 日的 1017 同樣只加日期，AA 智力指數從 39 升到 45，每任務成本從 $0.48 降到 $0.26。

**Q: DeepSeek V4.1-Flash-1017 跟 Claude Sonnet 5.5 差多少？**

依 Artificial Analysis 智力指數，1017（max）是 45 分、每任務 $0.26；Claude Sonnet 5.5 開 high 是 47 分、每任務 $0.88；GPT-6 Astra 開 low 是 46 分、$0.82。分數只差 1 到 2 分，成本不到三分之一。但 Sonnet 5.5 開到 max 是 56 分，跟 1017 差距明顯，所以比較時要說清楚用的是哪個推理強度（Reasoning Effort）。

**Q: 763B 參數的模型，兩台 DGX Spark 怎麼放得下？**

763B 由 552B 的 MoE 骨幹和 196B 的 Engram 條件記憶表（Engram Conditional Memory）組成。Engram 表是查表結構，可以留在 SSD 按需讀取，不必進 GPU 記憶體。骨幹用 EXL3 量化（Quantization）到 2.9 bpw 約 196 GiB，分到兩台 DGX Spark（每台 GB10、128 GB 統一記憶體）各約 98 GiB，用 TensorFold 做張量平行（Tensor Parallelism）。Engram 表約 203 GB，兩台都要放本機 NVMe，走 NFS 會讓 prefill 掉到每秒 690 到 890 token。

**Q: 兩台 DGX Spark 跑 1017 實際有多快？**

作者自己的兩台 DGX Spark 用 Mia-AiLab 的 EXL3 2.9 bpw 量化加 TensorFold，單串流 code 每秒 115 token、prose 每秒 67 token（輸出 400 token、thinking 關閉、每類 3 次中位數）。社群的 tonyd2wild 配方單串流 73.1 tok/s、4 串流合計 135.8 tok/s。三台改用 3.75 bpw，速度跟兩台差不多，換到的是精度。

**Q: DGX Spark 能用 DeepSeek 開源的 DeepInfer 嗎？**

目前不行。DeepInfer 是 DeepSeek 在 2026 年 10 月 20 日以 Apache-2.0 開源的推理框架（Inference Framework），README 預設 checkpoint 是 V4.1-Flash-1017，但支援硬體只列 NVIDIA SM100 和華為昇騰 950，沒有 DGX Spark 的 GB10。Spark 上跑 1017 用的是 TensorFold 或 vLLM。vLLM 在 10 月 24 日宣稱，已在 DeepSeek 的 decode 配置上追平 DeepInfer 的效能。

---

## 延伸閱讀

- [DeepSeek-V4.1-Flash-1017 模型卡（Hugging Face）](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017)
- [DeepSeek-V4.1-Flash-1017 官方發布公告](https://api-docs.deepseek.com/news/news261017)
- [Artificial Analysis：DeepSeek V4.1 Flash 1017](https://artificialanalysis.ai/models/deepseek-v4-1-flash-1017)
- [Artificial Analysis：GPT-6 Sol vs GPT-5.6 Sol](https://artificialanalysis.ai/models/comparisons/gpt-6-sol-vs-gpt-5-6-sol)
- [Artificial Analysis：V4 Flash 0731 公告（X）](https://x.com/ArtificialAnlys/status/2083123180869496865)
- [Paweł Huryn 的 105 個隱藏 bug 測試（X）](https://x.com/PawelHuryn/status/2111411180182917214)
- [DeepInfer GitHub repo](https://github.com/deepseek-ai/DeepInfer)
- [vLLM 追平 DeepInfer decode 效能（X）](https://x.com/vllm_project/status/2114054277379641770)
- [MiaAI-Lab：1017 on 2x DGX Sparks](https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-1017-2x-DGX-Sparks)
- [tonyd2wild：TP2 / TP4 DGX Sparks](https://github.com/tonyd2wild/DeepSeek-V4.1-Flash-vLLM-DGX-Spark)
- [Unsloth：DeepSeek-V4.1-Flash 本地執行指南](https://unsloth.ai/docs/models/deepseek-v4.1-flash)
- [DeepSeek 開源 DeepInfer（本 blog）](/deepseek-deepinfer-open-source-inference-design/)
- [DeepSeek V4 Flash 0731 為何那麼強（本 blog）](/deepseek-v4-flash-disk-kv-cache-50x-economics/)
- [又借到兩台 DGX Spark：四個 Flash 模型輪流上機（本 blog）](/dgx-spark-four-flash-models-deepseek-qwen-glm/)
- [兩台 DGX Spark 測試實錄（本 blog）](/dgx-spark-test-log-flash-models-glm-qwen-deepseek/)
