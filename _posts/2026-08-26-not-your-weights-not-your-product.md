---
layout: post
title: "Sovereign AI 不是口號：Sequoia 的四級路徑、開源 60 vs 封閉 62 的算術、以及你該停在第幾級"
date: 2026-08-26 09:00:00 +0800
permalink: /not-your-weights-not-your-product/
image: /assets/images/not-your-weights-logo.png
description: "Sonya Huang 八月在 Sequoia 活動上把比特幣圈 2017 年的口號翻成 AI 版：not your weights, not your product。口號背後只有一個硬數字支撐——Kimi K3 和 GLM-5.3 在 Artificial Analysis Intelligence Index 上拿到 60，Fable 5 是 62。這篇從那個 2 分差距出發，算自建真正的成本結構，以及 VC 推這個論點的位置利益。"
---

80 位被投公司 founder 坐在 Sequoia 的活動上，Sonya Huang 把 2017 年比特幣圈那句「not your keys, not your bitcoin」換了個名詞：

> "Not your weights, not your product. I think that for product to be truly yours, I think it's reasonable to think that you need to be able to control and custody your own weights."

產品要真正屬於你，權重要在你手上。

她講這話的兩週前，Jensen Huang 用人生第一則 X 貼文公開推動美國保留開源權重模型。她形容當時的反應是「near unanimous wave of support」。

口號響了。但口號不是算術。

[完整演講](https://www.youtube.com/watch?v=bMMv0bZzONg)。

---

## 整個論點靠一個數字撐著

「自有模型可以贏過 API」這句話，在 2026 年 8 月之前是省錢選項。你知道會比較笨，但便宜。

今年它變成性能選項。撐起這個轉變的數字只有一個：

| 模型 | AA Intelligence Index |
|------|:--:|
| Opus 5 | 63 |
| Fable 5 | 62 |
| Kimi K3 | 60 |
| GLM-5.3 | 60 |
| Sonnet 5 | 55 |

開源陣營離封閉旗艦 **2 分**。

Sonya 在台上說：「this is new for 2026.」她講的「new」不是開源模型變強了——它們一直以來都在追。New 的是：**2 分這個距離，在你的領域、你的資料上，可以被填掉。**

填掉它需要的東西，一件一件攤出來：

- 一套持續運轉的 eval 集——基座每次換版本都要重跑
- 領域資料：expert trajectory、synthetic data、RL environment，至少兩樣
- 推理 infra：GPU、vLLM 或等價棧、drift 監控
- 一個小團隊：Harvey 的研究團隊 7 個人，是目前公開資料裡最小的樣本

7 個人、法務領域、做到發布研究。這是這個論點最有力的證據。

但它是一個樣本，不是一個分母。

---

## 口號漏掉的那半句話

先講清楚 performance 是什麼意思。Sonya 講的不是 token per second，不是 throughput，是**特定領域上的任務表現**——「in certain domains you may be able to get better performance by tuning models on your own data.」latency 和 speed 是她框架裡另外一個獨立項目，不是這裡的 performance。

她明確說 performance 是「relatively newer」的理由。前幾年公司選開源模型，原因是便宜。今年多出來的那個原因是：在特定領域上可能更強。她舉的例子也全是任務級別：coding Tab autocomplete 跑在自有模型上（高頻、latency P0）、資安公司用自有模型做 bespoke post-training、生技公司因為私有資料價值而自建。

這跟多數人聽到「自建」的第一反應相反。多數人想到的是 cost saving。但 Sonya 自己列的順序裡，cost 排第一是因為它最常見，不是因為它最新。

**真正的新理由是 performance，而 performance 恰恰是自建裡最貴的部分。**

注意這是領域表現的 performance，不是吞吐量的 performance。如果一家公司自建的唯一動機是 token per second，那是 infra 問題，加卡就好，不需要 7 人團隊。需要 7 人團隊的是：在你的領域資料上，post-training 出來的模型比 API 上的封閉旗艦更懂你的業務。這個「更懂」要拿 eval 證明，而 eval 是最貴的部分。

省錢的路徑早就存在了——用 DeepSeek V4 Flash 或 Qwen3.8 27B 這種單卡模型，[每美元智能](/fable-5-enterprise-adoption-ceiling-intelligence-per-dollar/)那张表算得清楚。性能的路徑是今年才打開的，它的帳單不是 token 計費，是 capex。

token 帳單每月可以砍。GPU 和訓練團隊砍不動。

---

## 講一句不太客氣的話

Sonya 是 VC。

VC 推「自建」，被投公司有兩個直接好處：一是有更多輪次可以投——infra、fine-tuning、data tooling、RL environment，每個都是新公司；二是有更多理由留在組合裡——自建是多年承諾，API 是每月訂閱。

這不是說她錯了。Harvey 7 人團隊是真的，Kimi K3 的 60 分是真的。

但聽一個 VC 講「你的產品要屬於你自己」，值得問一句：**如果所有公司都自建了，Sequoia 的組合會變成什麼樣子？**

更多 infra 公司、更多 fine-tuning 工具、更多 data pipeline。更少「每月訂閱 API」的輕資產應用公司。

對 VC 來說這是好生意。對被投公司來說，前提是那 2 分的空間你真的填得掉。

---

## 對個人開發者，這句話是反的

對企業 CTO，「not your weights」的意思是：高頻功能、私有資料、latency 要求，不該託付給一個 API。

對個人開發者，含義相反。

你沒有資料護城河，沒有 7 人研究團隊。你「自有」的東西是你的 harness——prompt、context 管理、eval、workflow。模型換掉，這些還在。

這是 [harness 三次遷移](/agent-harness-three-migrations-mechanism/) 那篇講的核心。對個人開發者，**harness 就是你的 weights**。

同一句話，兩個方向：

| | 企業 CTO | 個人開發者 |
|---|---|---|
| 行動 | 高頻功能切開源 base + post-training | harness 層做好，模型當可替換零件 |
| 成本 | Capex（GPU + 團隊） | 時間（寫 eval、調 harness） |
| 護城河 | 領域資料 + 自有模型 | 工作流 + 自有 harness |
| 風險 | 基座換代，eval 重跑 | 模型升級，harness 重調 |

### 自建不是二選一，是四級路徑

上面這張表預設了一件事：企業的主權路徑是自建模型。但 Sonya 演講裡其實給了一條四級路徑，自建只是其中一級：

| 級別 | 要做的事 | 需要什麼 | 雲 / 地端 |
|------|---------|---------|----------|
| 1 | 直接用 out-of-the-box 模型，API 就夠 | 訂閱費 | 雲端 |
| 2 | harness、model router：prompt、context、eval、工作流 | 時間，不需要 GPU | 以雲為主，可開始嘗試雲地混合 |
| 3 | online feedback loop：客戶互動數據持續回流改進 | 第 2 級 + 數據回流基建 | 雲地混合 |
| 4 | post-training：領域資料 + RL environment + 推理 infra | GPU + 訓練團隊（Harvey 7 人即此級） | 雲地混合 |

Sonya 原話：「some companies find they can get good performance with out-of-the-box models. Others are finding strong performance gains from post-training... And then finally, setting that machine up so that live customer data is actually creating a feedback loop.」

這條路徑的關鍵：**每一級都有可驗證的產出（eval 分數），公司可以停在任何一級，不需要一步跳到自建。**

同一陣週期裡，老鄭說 AI 前瞻那支 AI 主權長片把同一個論點講成了可操作的清單：業務上下文結構化、流程改閉環、私有評測、模型冗餘——全部落在第 2、3 級，**一件都不需要 GPU**。他的表述更直白：護城河不是有沒有用 AI，而是每次用 AI 之後有沒有留下東西——留下數據、流程、評測、知識庫、下一次能複用的判斷。沒有留下，燒掉的 token 就是煙火。

兩套論點合起來，sovereignty 其實是兩個獨立問題：

- **模型是你的嗎？**——第 4 級，答案是 capex 那套算術。
- **模型之上的學習閉環是你的嗎？**——第 2、3 級，答案是那套輕得多但同樣具體的清單。

對過不了 capex 那道題的公司，實際的選項是：先把第 2、3 級做到 eval 分數能證明「比 API 直用強」，再決定要不要進第 4 級。不是「自建 vs 不自建」，是「停在第幾級」。

---

## 坦白說

這個論點的適用範圍比口號聽起來窄。

**2 分差距是 2026 年 8 月的快照。** Kimi K3 和 GLM-5.3 的 60 分是 Artificial Analysis 的綜合分，不是你在你的領域上的分數。基座換一代，你的 eval 集要重跑，post-training 資料要重新標。這不是建一次就永久的事。

**7 人團隊的證據，適用範圍是法務領域。** 前面說它「是這個論點最有力的證據」，但那是法務領域的證據——文件、判例、合約，資料結構相對清晰，比製造業的 sensor data 或金融業的風險模型更容易做領域 post-training。你的領域資料沒有這種結構，7 人可能不夠，或者需要的根本不是 7 人。Sonya 自己也說：「every company is very very different.」

**VC 的位置利益是真的。** 她說 Anthropic 和 OpenAI「to their credit」是好的合作夥伴，但公司還是想有「their own set of independent legs」。好的合作夥伴，也是你可以選擇不依賴的合作夥伴。VC 推這個論點，跟被投公司真的需要這個論點，是兩件事。

但它做對了一件事：**把「自建」從成本決策變成性能決策。** 過去自建的理由是便宜，開源模型追上來之後這個理由反而變弱了——便宜模型更多了。今年的新理由是「在你的領域上可能更強」，這個理由只有在開源基線夠高的時候才成立。

Kimi K3 的 60 分，就是「夠高」的證據。

---

## 關鍵洞察

**一、把口號翻成算術。** 開源基線（60）和你的需求之間的差距，能不能被你的資料和 pipeline 填掉？填掉的總成本——GPU、團隊、eval 維護——是不是比 API 帳單划算？兩個問題都答得出來，再建。

**二、性能理由是新的，成本理由是舊的。** 如果自建的唯一理由是省錢，先問：DeepSeek V4 Flash 或 Qwen3.8 27B 是不是已經夠了？夠的話你不需要 7 人團隊，你需要的是[每美元智能](/fable-5-enterprise-adoption-ceiling-intelligence-per-dollar/)那篇文章的表。

**三、個人開發者的 weights 是 harness，不是模型。** prompt、context 管理、eval、workflow——換模型之後還在的東西。時間花在這一層，比追每個月的新模型有用。企業的對應物是學習閉環：業務上下文、私有評測、模型冗餘——模型可以流水，標準和判斷要鐵打。

**四、聽 VC 講「你的產品要屬於你自己」時，問一句：自建之後，他們組合裡多出了哪些公司？** 如果是 infra、fine-tuning、data pipeline，那這個論點對你是機會也是成本。
