---
layout: post
title: "OpenMythos 逆向 Claude Mythos 架構：不是更多層，是同一批層跑更多次"
date: 2026-07-14 09:00:00 +0800
permalink: /openmythos-recurrent-depth-transformer-claude-mythos-architecture/
image: /assets/images/openmythos-rdt-architecture-cover.png
description: "一個 22 歲的高中輟學生，用公開論文和行為觀察，在 GitHub 上發布了一個叫 OpenMythos 的專案，嘗試逆向重建 Claude Mythos 的架構。他的核心假設：Mythos 不是靠堆參數，而是一個 Recurrent Depth Transformer——同一批權重反覆迴圈執行多次。Parcae 論文的實驗顯示，這種迴圈架構用 1.3B 參數能達到兩倍大小標準 Transformer 87.5% 的品質。本文拆解這個假設的三個支柱：迴圈提供深度、MoE 提供廣度、譜半徑約束保證穩定——以及為什麼這套邏輯跟 Agent 架構的設計模式是同一件事。"
---

Anthropic 從不公開 Mythos 的架構細節。但 2026 年 4 月，一個叫 [OpenMythos](https://github.com/kyegomez/OpenMythos) 的開源專案出現在 GitHub 上，兩週內拿到超過一萬顆星。

作者 Kye Gomez，22 歲，高中輟學，[Swarms 多 Agent 框架](https://github.com/kyegomez/swarms)的作者。他的做法不是洩漏、不是蒸餾，而是從公開論文和 Mythos 的推理行為反推架構，用 PyTorch 從頭實作，然後 MIT 授權丟出來。他自己的定位是：**「一個可以被證偽的假設，用程式碼呈現。」**

這個假設的核心只有一句話：Claude Mythos 很可能是一個 Recurrent Depth Transformer（RDT）——不是堆更多層，而是同一批層反覆執行多次。

---

## 30 秒定位

| 項目 | 內容 |
|------|------|
| 專案 | [OpenMythos](https://github.com/kyegomez/OpenMythos)（MIT 授權） |
| 作者 | Kye Gomez（Swarms 框架作者） |
| 核心假設 | Claude Mythos = Recurrent Depth Transformer |
| 關鍵論文 | [Parcae](https://arxiv.org/abs/2604.12946)（Prairie et al., 2026）、[Loop, Think, & Generalize](https://arxiv.org/abs/2604.07822)（Kohli et al., 2026） |
| 參數效率宣稱 | 1.3B 迴圈模型 ≈ 2x 大小標準 Transformer 的 87.5% 品質（Parcae 論文） |
| Anthropic 回應 | 無。沒有確認，也沒有否認 |

---

## 傳統做法 vs 迴圈做法

![範式對決：從空間堆疊轉向時間迴圈](/assets/images/openmythos-traditional-vs-rdt.png)

先把直覺建立起來。

標準 Transformer 的推理深度，等於它的層數。一個 96 層的模型，每個 token 就走 96 層，每一層有自己的權重。要更強？加更多層、加更多參數。這是從 GPT-3 到 Opus 一路走來的路線。

RDT 換了一個想法：**把中間那批層的權重共享，然後反覆跑多次。**

想像你是一個工程師在 debug。標準 Transformer 的做法是：公司給你配 96 個不同的同事，每個人看一眼程式碼就傳給下一個。RDT 的做法是：只有一組同事，但他們可以反覆檢查同一段程式碼，每看一次理解得更深。第一輪抓語法錯誤，第二輪抓邏輯問題，第三輪發現邊界條件。同一批人，同一批知識，但每一輪的理解在上一輪的基礎上加深。

差異在於：**推理深度不再被參數量綁死。** 你可以在推理時決定要跑幾輪，簡單的問題跑兩輪就停，難的問題跑十輪。

---

## 架構拆解：三段式結構

OpenMythos 把整個架構分成三段：

**1. Prelude（前奏）**——標準 Transformer 層，只跑一次。負責把原始 token 編碼成模型的內部表示。

**2. Recurrent Block（迴圈核心）**——最關鍵的部分。一組 Transformer 層，反覆執行 T 次。每次迴圈的隱藏狀態更新公式：

> h(t+1) = A · h(t) + B · e + Transformer(h(t), e)

其中 A 和 B 是學習到的參數，e 是 Prelude 的編碼輸出。注意那個 `+ B · e`——每次迴圈都會重新注入原始輸入的編碼。這不是裝飾，是為了防止模型在反覆迴圈中「漂移」，忘記自己到底在解決什麼問題。

**3. Coda（結尾）**——標準 Transformer 層，只跑一次。把迴圈核心的最終狀態投射成輸出 token。

T 是一個變數，可以根據問題難度調整。OpenMythos 的預設上限是 16 次。搭配一個叫 Adaptive Computation Time（ACT）的機制，模型可以學會在某些 token 上提早停止——簡單的 token 跑 2 次就夠了，複雜的才跑滿。

---

## 迴圈提供深度，MoE 提供廣度

![能力矩陣：知識廣度與推理深度的正交](/assets/images/openmythos-moe-recurrence-matrix.png)

光有迴圈只解決了深度的問題。要讓模型擁有足夠多的知識，還需要廣度。OpenMythos 在每一層的 FFN（前饋網路）裡用了 DeepSeek 風格的 fine-grained Mixture of Experts：

- 大量的小型專家（OpenMythos 配置中最大到 512 個）
- 每個 token 只啟用其中 top-K 個
- 少數共享專家始終保持啟用，負責通用知識（語法、基礎推理、上下文理解）
- 啟用率大約 5%

這意味著模型可以持有數千億的總參數量，但每次推理只啟用其中很小一部分。

**一句話講清楚：MoE 提供廣度（知識容量），迴圈提供深度（推理步數），兩者互不干擾。**

---

## 穩定性：為什麼不會炸掉

反覆迴圈有一個致命問題：殘差爆炸。每迴圈一次，殘差會疊加一次。跑 16 次之後，數值可能飆到天上去，訓練直接崩潰。

DeepSeek 和 Kimi（月之暗面）都嘗試過解決這個問題。Parcae 論文（[Prairie et al., 2026](https://arxiv.org/abs/2604.12946)）提出的方案是把整個迴圈建模成一個**線性時不變系統（LTI）**，核心約束只有一條：

> 注入矩陣 A 的譜半徑 ρ(A) 必須嚴格小於 1。

具體做法是把 A 參數化為一個連續的負對角矩陣 `A := Diag(-exp(log_A))`，然後用零階保持（ZOH）或 Euler 離散化。這保證了每一輪迴圈都會對殘差做一定程度的壓縮，數值不可能發散。

Parcae 的實驗結果：在 1.3B 參數規模下，迴圈架構在 CORE benchmark 上比標準 Transformer 基線高 2.99 分，validation perplexity 降低最多 6.3%，品質達到兩倍大小標準 Transformer 的 87.5%。

這裡要精確一點：**媒體普遍簡化成「770M = 1.3B」，但 Parcae 論文原文的說法是「87.5% quality of a Transformer twice the size」，不是完全相等。** 打八七五折和完全追平是兩回事。

---

## 行為證據：為什麼猜它是迴圈的

Gomez 和多位研究者並不是憑空猜測。他們的推論基於 Mythos 的幾個行為特徵，這些特徵恰好高度符合迴圈架構的理論預測。

**第一，系統性泛化。** [Kohli et al.（2026）](https://arxiv.org/abs/2604.07822)在 "Loop, Think, & Generalize" 這篇論文中證明，標準 Transformer 做不到分佈外泛化，但 Recurrent Depth Transformer 可以。它的泛化能力經歷三個階段：記憶 → 分佈內泛化 → 分佈外泛化。關鍵是第三階段不是漸進的，而是在某個訓練節點突然出現——這跟 Mythos 被觀察到的行為模式吻合。

**第二，深度外推。** 同一篇論文顯示，在 5 跳推理鏈上訓練的迴圈模型，可以在 10 跳推理鏈上成功推理。標準 Transformer 在這種設定下會失敗。原因很直接：迴圈模型只需要多跑幾輪，每一輪在上一輪的基礎上往前推一步。

**第三，不需要顯式 Chain of Thought。** 有研究者觀察到 Mythos 在處理多步數學和長鏈規劃時，不需要顯式的思維鏈提示就能得到正確結果。如果架構本身就是迴圈的，每一輪迴圈就相當於一步隱式的 chain of thought——推理過程在連續的向量空間裡完成，不需要生成中間 token。

不過要注意，這些都是間接證據。Anthropic 沒有確認過任何一條。[BuildThisNow 的報導](https://www.buildthisnow.com/blog/models/2026-04-21-claude-mythos-openmythos)提到，2026 年初有 source map 洩漏事件（`@anthropic-ai/claude-code` v2.1.88）暴露了與迴圈深度推理一致的內部 feature flag，但這也是二手來源，無法獨立驗證。

---

## 跟 Agent 架構的平行：這不是巧合

![終極收斂：模型架構與 Agent 框架的殊途同歸](/assets/images/openmythos-rdt-agent-convergence.png)

這是讀完整個 OpenMythos 專案之後，我覺得最值得寫的一個連接。

把 RDT 的結構攤開：

- **迴圈核心** = 同一組權重反覆執行，每輪基於上一輪的輸出推進一步
- **MoE 路由** = 每個 token 只啟用最相關的少數專家處理
- **ACT 早停** = 簡單的任務提前結束，不浪費算力

現在把 Agent 架構攤開：

- **Orchestration loop** = 一個 orchestrator 反覆呼叫執行 agent，每輪基於上一輪結果決定下一步
- **Router / tool selection** = 每個任務只啟用最相關的工具或子 agent
- **Exit condition** = 判斷任務完成就停止，不繼續空轉

**這是同一個模式。** 迴圈模組對應多跳 orchestration，MoE 對應路由邏輯，ACT 對應停止條件。

這個 blog 之前在 [Harness Engineering](agent-harness-three-migrations-mechanism.md) 那篇講過一個核心觀點：**機制取代建議**——用 hook 和權限擋住行為，不要用 prompt 拜託模型自律。RDT 在模型層做了同樣的事：隱式 CoT（機制）取代顯式 CoT（prompt 裡的思維鏈）。你不需要在 prompt 裡寫死一個 10 步的思維鏈範例，迴圈架構本身就是那個思維鏈的機制化實現。

如果這個假設方向是對的，Mythos 相當於把我們在 Harness 層做的路由邏輯和多跳 orchestration 直接融進了模型內部。這也解釋了一件事：為什麼 Mythos 的能力明顯超過 Opus，但如果 RDT 假設為真，它的實際參數量可能反而更少。

---

## 反方：這整件事可能是錯的

對這個假設最強的反駁，不是「迴圈架構沒用」——Parcae 和 "Loop, Think, & Generalize" 的實驗結果擺在那裡，迴圈架構確實有效。

最強的反駁是：**OpenMythos 沒有任何證據證明 Claude Mythos 真的用了這個架構。**

OpenMythos 的 repo 裡沒有發布任何 benchmark 結果。沒有在標準評測上跟 Mythos 做過對比。甚至連「我用這個架構訓練了一個小模型，效果如何」的數據都沒有。整個專案目前是一個架構設計加一堆配置檔，不是一個訓練過的模型。

Gomez 引用的行為證據——系統性泛化、深度外推、隱式 CoT——確實符合迴圈架構的理論預測。但「符合理論預測」不等於「就是用了這個架構」。其他架構也可能產生類似行為。

而且那條 source map 洩漏的線索，來自二手報導，我查不到原始證據。

---

## 坦白說

這篇文章分析的是一個**假設**，不是一個**事實**。Anthropic 沒有確認，OpenMythos 沒有發布 benchmark，行為證據是間接的。我能做的是把假設的邏輯鏈和支撐論文攤開，讓你自己判斷這條推論有多少可信度。

Parcae 論文的「87.5% quality of 2x size」是在 1.3B 規模上的結果。這個效率增益能不能線性外推到 Mythos 那個量級，目前沒有公開數據支持。小規模的 scaling law 不一定在大規模保持。

另一個限制是 overthinking 問題。"Loop, Think, & Generalize" 論文明確指出，過度迴圈會退化預測結果。也就是說迴圈不是「越多越好」，而是有一個甜蜜點。ACT 機制理論上能解決這個問題，但在大規模模型上的表現如何，目前也查不到公開實驗。

最後，就算 Mythos 真的是 RDT，OpenMythos 也不可能只靠架構設計就複製它。訓練數據、RLHF 對齊、推理優化這些都是架構之外的事。

---

## 關鍵洞察

- **迴圈 + MoE 是一個值得認真看的設計方向，不管 Mythos 是不是這樣做的。** Parcae 論文在 1.3B 規模已經證明迴圈架構可以用更少參數達到接近更大模型的品質。如果你在評估本地部署或推理成本，這條技術路線值得持續追蹤。

- **隱式 CoT 的含義：推理深度可以在推理時動態調整。** 這改變了一個基本假設——你不需要在 prompt 裡寫死推理步驟，模型架構本身可以決定「這個問題需要想多深」。對做 Agent 的人來說，這意味著模型端和 harness 端的推理策略終究會合流。

- **看架構假設的正確姿勢：不是「信不信」，是「可以被怎樣證偽」。** Gomez 自己的定位就是可證偽假設。如果未來有人用 OpenMythos 架構訓練模型、跑出 benchmark、跟同規模標準 Transformer 對比，這個假設就從「有趣的猜測」升級成「有數據支撐的理論」。在那之前，它是一張設計圖，不是一棟建築。

---

**來源與延伸閱讀：**

- [OpenMythos GitHub](https://github.com/kyegomez/OpenMythos)
- [Parcae: Scaling Laws For Stable Looped Language Models](https://arxiv.org/abs/2604.12946)（Prairie et al., 2026）
- [Loop, Think, & Generalize: Implicit Reasoning in Recurrent-Depth Transformers](https://arxiv.org/abs/2604.07822)（Kohli et al., 2026）
- [Forbes: Did A 22-Year-Old Dropout Reverse-Engineer The World's Scariest AI?](https://www.forbes.com/sites/craigsmith/2026/05/02/a-22-year-old-dropout-just-reverse-engineered-the-worlds-scariest-ai/)
- 本 blog 相關：[Mythos 有多強](anthropic-mythos-project-glasswing-cyber-inflection-point.md) ｜ [Harness Engineering](agent-harness-three-migrations-mechanism.md)
