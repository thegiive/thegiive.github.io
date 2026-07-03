---
layout: post
title: "Fable 5 又被破了，但防禦明顯強化很多：一個人花 20 小時手動磨穿三層分類器"
date: 2026-07-04 05:56:25 +0800
permalink: /fable-5-constitutional-classifiers-jailbreak-20hr-google-faster/
image: /assets/images/fable-5-cc-plus-plus-jailbreak-cover.png
description: "繼 Pliny 團隊用自動化框架 Pyroclast 打穿 Fable 5 之後，資安研究員 VittoStack 用純手動 prompt engineering 再次突破。20 小時，七種技術組合，繞過至少三層分類器，拿到假資訊、違法有害內容、部分化學資訊和輕度網路攻擊代碼。這篇完整記錄攻擊手法、分類器行為觀察、CoT Hijacking 的角色，以及 Anthropic Constitutional Classifiers++ 的技術架構。"
---

Fable 5 又被越獄了。

上一次是 Pliny 團隊的 Pyroclast 自動化框架，五個 agent 並行，24 小時內把安全層從頭到尾打穿——完整的網路攻擊代碼、化學合成路徑、武器製作步驟全被鉤出來。

這次是資安研究員 VittoStack，一個人，沒有自動化工具，純靠 prompt engineering 手動打了 20 小時。結果：成功突破，拿到了假資訊、違法有害內容、部分化學資訊、輕度網路攻擊代碼。

兩次攻擊，兩種完全不同的方式，同一個結果：Fable 5 的安全護欄被突破。

差別在過程。Pyroclast 是系統性地自動化拆解，VittoStack 是一個人用最笨的方式硬磨。他自己的描述：

> "Probably one of the most tiring things I've ever done (I need to sleep for 10 hours now)"

以下是他公開的完整攻擊過程和技術觀察。

---

## 防禦端：三層分類器的行為觀察

VittoStack 在 20 小時的攻防過程中，觀察到 Fable 5 至少部署了三個分類器。

### 第一層：輸入側分類器

掃描範圍不只是當前輸入，還包括部分對話歷史和 system prompt。攻擊者不能只偽裝單輪 prompt，前面幾輪的對話脈絡也會被納入判斷。

VittoStack 觀察到的行為：當前幾輪對話中出現過敏感方向的暗示，即使當前輪的 prompt 完全無害，分類器仍然會觸發拒絕。

### 第二層：輸出側即時分類器

模型在生成回答的過程中，有一個即時監控機制。不是等整個回答生成完再判斷，是邊寫邊檢查。如果在生成途中偵測到敏感內容，直接中斷輸出。

VittoStack 多次遇到的情況：模型已經開始輸出內容，寫到一半突然停止，切換成拒絕回應。這說明有一個獨立於模型生成過程的監控機制在即時介入。

### 第三層：語意意圖偵測

不是基於關鍵字比對，而是基於語意和意圖理解。跨語言都有效——VittoStack 測試了多種語言，分類器在主流語言上都能偵測到惡意意圖。使用祈使句（imperatives）幾乎必定觸發。

這是 VittoStack 認為最難繞過的一層。他的描述：

> "As soon as it senses a potentially malicious intent, it will trigger, and you have to start from zero."

一旦觸發，不是當輪被拒絕就算了，是整個對話作廢。必須開一個全新的對話從零開始。這意味著每次失敗的成本不是一輪，是整條對話鏈的所有前置工作全部報廢。

---

## 攻擊端：七種技術的組合拳

VittoStack 公開了他使用的完整技術棧。單獨使用任何一種都不夠，必須組合使用，而且順序和節奏都有講究。

### 1. 輕度 CoT Hijacking / 拒絕反駁

當模型在推理過程中準備拒絕時，攻擊者在對話中插入反駁，試圖改變模型的推理方向。

具體做法：觀察模型的輸出模式，當它開始出現拒絕的前兆（例如「I should note that...」「I need to be careful...」這類轉折語句），立刻在下一輪插入學術正當性的論述，讓模型重新評估自己的拒絕決定。

VittoStack 強調這只能「輕度」使用。太激進的反駁會直接觸發分類器，整個對話作廢。

### 2. 冷門語言切換

使用 Santali（桑塔利語，印度部落語言）和 Amharic（阿姆哈拉語，衣索比亞官方語言）等小眾語言來降低分類器的偵測效能。

VittoStack 的觀察：分類器在這些語言上的表現「a bit less performant」。不是完全失效，是偵測精度下降。這符合機器學習的基本邏輯——訓練數據越少的語言，模型在該語言上的判斷能力越弱。

他把這個觀察直接當成給 Anthropic 的回饋：

> "They're a bit less performant on a few obscure languages like Santali and Amharic (feedback for you Anthropic)."

### 3. 學術包裝（Academic Framing）

把所有請求框架成學術研究場景。不是直接問「怎麼做 X」，而是以研究者的身份請求「分析 X 的機制以便建立防禦」。

這個技巧的核心：分類器需要區分「為了理解攻擊原理而學習」和「為了實施攻擊而學習」，但在很多情境下，這兩者的內容是一模一樣的。學術包裝利用的就是這個灰色地帶。

### 4. 超長漸進升級（VERY Long Crescendos）

VittoStack 特別強調了「VERY」——這不是 3-5 輪的對話升溫，是持續很多輪的極緩慢升級。

操作方式：從完全無害的學術話題開始，每一輪只往目標方向移動一小步。每一步都確保在分類器的閾值以下。整條對話鏈的方向是朝著目標主題移動，但任何單獨一輪拿出來看都是合法的學術討論。

這個技巧需要極大的耐心。VittoStack 花了 20 小時，其中大量時間消耗在這些漸進升級的對話鏈上。而且一旦在任何一輪觸發分類器，整條鏈的前置工作全部報廢。

### 5. Unicode 技巧

利用 Unicode 字元的多樣性來繞過部分偵測。例如使用視覺上相同但編碼不同的字元（同形字），或使用零寬字元、組合字元等特殊 Unicode 來干擾分類器的文字處理。

VittoStack 沒有公開具體使用了哪些 Unicode 技巧，但這與 Pliny 團隊使用的西里爾同形字（Cyrillic Homoglyphs）屬於同一類攻擊向量。

### 6. 分解與重組（Decomposition and Recomposition）

把敏感內容拆成多個碎片，分散在不同的對話輪次中分別問，每一片看起來都無害。然後在最後要求模型把這些碎片組合起來。

分類器看到的是一系列無害的片段請求。模型看到的是自己的對話上下文，忠實地把碎片拼回完整內容。

### 7. 非確定性（Non-determinism）

利用模型輸出的隨機性，對同一個 prompt 多次嘗試，碰運氣。因為模型每次生成的回應不完全相同，有時候同一個 prompt 被拒絕，換一次就通過了。

VittoStack 提到大部分嘗試都失敗了：

> "Most attempts failed. The defenses are clearly layered."

這意味著上述七種技術不是「用了就能成功」，而是需要反覆嘗試、調整組合、依賴一定程度的運氣。

---

## 繞過分類器之後：還有 CoT 要處理

VittoStack 指出，即使成功繞過了所有三層分類器，還有一個完全不同的障礙——模型自身的 Chain-of-Thought（推理鏈）安全機制。

> "If you can bypass all of them, then you also need to bypass the CoT, which is a totally different beast (luckily there's plenty of literature about it)."

這對應到 Jianli Zhao 等人發表的 "Chain-of-Thought Hijacking" 論文（arXiv: 2510.26418）。論文描述了一個現象叫「拒絕稀釋（Refusal Dilution）」：

- 先讓模型做大量無害的推理任務（例如解數學題、邏輯謎題）
- 長時間的良性推理會削弱模型內部負責產生拒絕回應的安全信號
- 在推理鏈的末端插入有害請求，模型拒絕的機率顯著下降

論文報告在 Gemini 2.5 Pro、ChatGPT o4 Mini、Grok 3 Mini、Claude 4 Sonnet 上的攻擊成功率超過 90%。

VittoStack 使用的「超長漸進升級」和「輕度 CoT Hijacking」，本質上就是在利用這個機制——用長對話鏈稀釋模型的安全注意力，同時繞過外部分類器的偵測。

---

## Constitutional Classifiers++ 的技術架構

VittoStack 觀察到的分類器行為，對應到 Anthropic 發表的 Constitutional Classifiers++ 論文（arXiv: 2601.04603，作者包括 Hoagy Cunningham、Jerry Wei、Mrinank Sharma 等 29 人）。

### 兩階段級聯架構

**第一階段：線性探針（Linear Probe）**

從 Claude 的內部神經網路激活狀態中提取安全信號。利用可解釋性研究的方法，讀取模型在處理文字時每一步產生的內部狀態。

計算開銷約 1%，對比第一代系統的 23.7%，降低了 40 倍。這個階段負責篩選所有流量，把可疑的交互標記出來。

**第二階段：集成分類器（Ensemble Classifier）**

被第一階段標記的交互，升級到更重的集成系統做最終判斷。

一個關鍵設計：「交換分類器（Exchange Classifier）」同時看輸入和輸出的上下文，而不是拆開各自評估。這解決了一個已知漏洞——輸入和輸出分開看都像無害內容，放在一起看才能識別出有害模式。

### 論文公布的測試數據

- 誤拒率（False Refusal Rate）：0.05%，比第一代降了 87%
- 越獄成功率：從未防禦模型的 86% 降到 4.4%
- 紅隊測試：198,000 次嘗試，累計 1,700+ 小時，沒有發現通用越獄方法（universal jailbreak）

VittoStack 的參考資料也指向這兩篇文獻：

- https://arxiv.org/abs/2601.04603（Constitutional Classifiers++ 論文）
- https://anthropic.com/research/next-generation-constitutional-classifiers（Anthropic 官方說明）
- https://arxiv.org/abs/2510.26418（CoT Hijacking 論文）

---

## 突破結果：拿到了什麼

VittoStack 列出了他成功從 Fable 5 提取的內容類型：

- **Misinformation（假資訊）**
- **Illegal/harmful（違法/有害內容）**
- **Harmful/bullying（有害/霸凌內容）**
- **Some chem（部分化學資訊）**
- **Light cyber（輕度網路攻擊）**

與 Pliny 團隊的結果對比：Pliny 拿到了完整的 reverse shell 代碼、化學合成完整路徑、武器製作步驟。VittoStack 拿到的內容深度較淺，他自己用「some」和「light」來描述。

另一個關鍵差異：VittoStack 無法維持長時間的越獄狀態。

> "Keeping the full jailbreak for long-horizon tasks without tripping the guardrails is something I haven't been able to achieve (yet)."

能拿到片段，但沒辦法讓模型持續輸出受限內容而不觸發護欄。

---

## 兩次攻擊的完整對比

| 維度 | Pliny / Pyroclast | VittoStack |
|------|-------------------|------------|
| 攻擊方式 | 自動化多代理框架 | 手動 prompt engineering |
| 攻擊者 | 團隊 | 個人 |
| 時間投入 | ~24 小時 | ~20 小時 |
| 並行度 | 5 個 agent 同時跑 | 1 個人依序嘗試 |
| 工具 | Pyroclast 自動迭代 | 無自動化工具 |
| 突破深度 | 完整代碼、完整化學路徑、武器製作 | 假資訊、有害內容、部分化學、輕度網路攻擊 |
| 可持續性 | 可複現的自動化流程 | 無法維持長時間越獄狀態 |
| 攻擊者對防禦的評價 | 分層降級形同虛設 | "EXTREMELY well protected"、"legit did a good job" |

VittoStack 的結語：

> "GGs to Anthropic, and sorry for the eng that had to go through setting this all up in the last few weeks."

---

## 參考資料

- VittoStack, "Fable 5 jailbreak review," X/Twitter, 2026-07-03
- Cunningham et al., "Constitutional Classifiers++: Efficient Production-Grade Defenses against Universal Jailbreaks," arXiv: 2601.04603
- Zhao et al., "Chain-of-Thought Hijacking," arXiv: 2510.26418
- Anthropic, "Next-generation constitutional classifiers"

---

## 常見問題 Q&A

**Q: Constitutional Classifiers++ 是只有 Fable 5 才有，還是所有 Claude 模型都有？**

論文描述的是一個可以部署在 Claude 系列模型上的通用防禦系統。具體哪些模型版本部署了完整的 CC++ 架構，Anthropic 沒有公開說明。從 VittoStack 的測試結果來看，Fable 5 的防禦層級明顯比之前的模型更完整。

**Q: 分類器在中文環境下的效果如何？**

VittoStack 測試的主要是英文和幾種小眾語言（Santali、Amharic）。他提到小眾語言的分類器效能稍差。中文作為主流語言，訓練數據相對充足，但具體的中文環境測試數據，目前公開資料中沒有看到。

**Q: VittoStack 的攻擊是否可以複現？**

他沒有公開完整的 prompt 序列，只公開了使用的技術類型。他也提到過程中有大量的非確定性——同樣的方法不保證每次都能成功。加上分類器觸發後整個對話作廢的機制，實際的「試錯-重來」循環次數遠多於最終成功的次數。
