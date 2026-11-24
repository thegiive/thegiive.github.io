---
layout: post
title: "別再叫 LLM 直接打 1–5 分：從高露潔 × PyMC 的 SSR 到 2026 四篇審計論文，企業 AI 評分該怎麼「讀出」分數"
date: 2026-11-24 09:00:00 +0800
permalink: /llm-likert-rating-elicitation-ssr/
description: "一年前 PyMC Labs 與高露潔用 SSR（語意相似度評分）讓 LLM 合成消費者的評分分布貼近真人。一年後四篇直接引用它的論文給出更完整的答案：問題不在 LLM 會不會打分，而在你怎麼把分數讀出來，以及你要的是群體還是個人。"
categories: [企業 AI 工程化, AI Agent]
tags: [LLM-as-a-Judge, Evaluation, Harness, Synthetic Consumers, SSR, Embedding, arXiv]
image: /assets/images/llm-likert-rating-elicitation-ssr-cover.png
image_alt: "arXiv:2510.08338 論文首頁：LLMs Reproduce Human Purchase Intent via Semantic Similarity Elicitation of Likert Ratings"
author: Wisely Chen
---

企業導入 LLM 做評分的場景越來越多：客服對話質檢、履歷初篩、需求單優先級、產品概念測試。大部分團隊寫出來的第一版 Prompt 都長得差不多：

> 「請以 1 到 5 分評估……只輸出數字。」

跑完一批資料後，問題馬上就浮出來了：分數幾乎都擠在 3 或 4，極少出現 1，也很少出現 5；把分布畫出來，跟人類評分完全是兩回事。

2025 年 10 月，PyMC Labs 與高露潔（Colgate-Palmolive）發表論文[《LLMs Reproduce Human Purchase Intent via Semantic Similarity Elicitation of Likert Ratings》](https://arxiv.org/abs/2510.08338)，正面處理了這個現象，提出 **SSR（Semantic Similarity Rating）**。當時這篇論文常被簡化成「AI 可以取代傳統市調」。

隔了一年再回頭看，它最有價值的貢獻其實不是「取代市調」，而是點出一個很根本的工程問題：**LLM 的評分，不該是讓它直接吐出來的一個整數。** 而在 2026 年 8 到 10 月間，四篇直接引用它的新研究陸續發表，把這套方法的適用邊界畫得更清楚了。

## 先講結論

* **不要讓 LLM 直接輸出單一整數當分數。** 這種做法會讓評分分布嚴重塌縮到中間值，SSR 論文與後續研究都證實了這一點。
* **要讀出的是一個機率分布。** 工程上有兩條路：直接讀取模型對各分數 token 的機率（或改用專用的 decision model），或是像 SSR 一樣，先讓模型寫自由文字，再用 embedding 映射到量表。
* **「先寫理由，再給整數」不是好解法。** 雖然比直接打分稍微好一點，但在兩組獨立研究中都輸給直接讀分布。
* **這類方法只在「群體層級」站得住腳。** 拿來判斷「方案 A 整體是不是比方案 B 受歡迎」可以；拿來預測「特定這個人會怎麼答」不行，Persona 寫得再細也一樣。
* **拿來做商業決策前，一定要先用歷史資料校準。** 未校準的合成結果方向感還行，但效果幅度會系統性高估。

---

## 一、為什麼直接打分會壞掉

SSR 論文的驗證資料，來自高露潔真實執行過的 **57 份個人護理產品概念測試**，總計 **9,300 名美國受訪者**（每份 150–400 人）。研究團隊讓 GPT-4o 與 Gemini 2.0 Flash 帶入對應的人口統計 Persona，看過產品概念後回答購買意願。

他們用兩個指標衡量合成受訪者像不像真人：

* **Correlation attainment（ρ）**：合成樣本與真人樣本在「各產品平均分」上的相關係數，除以「人類自己分半重測」的相關上限。因此論文常被引用的「90%」，指的是達到人類重測上限的 90%，並不是原始相關係數 r = 0.90。
* **KS similarity**：1 減去 KS 距離，衡量評分分布的形狀有多貼近真人，越接近 1 越像。

如果直接叫模型輸出 1–5 分（論文稱為 **DLR，Direct Likert Rating**），結果如下：

| 模型 | 排序（ρ） | 分布形狀（KS similarity） |
| :--- | :---: | :---: |
| GPT-4o | 約 80% | `0.26` |
| Gemini 2.0 Flash | 約 80% | `0.39` |

可以看到，直接打分的排序表現其實不算太差，但分布形狀完全失真——模型傾向給安全的中間值，極少給出 1 或 5。

這對企業評分系統的啟示很直接：如果你的需求只是「粗略排個先後順序」，直接打分勉強能湊合；但只要你的決策依賴分布比例——例如「有多少比例的客服對話低於 2 分」「有多少潛在客戶會強烈拒買」——直接打分算出來就是錯的。*（註：此處延伸至企業評分系統為作者推論，原論文僅測試購買意願。）*

---

## 二、SSR 怎麼修：先讓模型說話，再用幾何讀分數

SSR 的核心想法，是把「表達態度」和「對應到量表」這兩件事拆開，分成三步：

1. **自由文字誘發**：不叫模型打分，只請它用自然語言描述會不會買、原因何在。
2. **錨點句向量化**：預先寫好 5 句分別對應 1–5 分的「參考句」（例如從「我非常不可能買」到「我非常可能買」），再把模型的回答與這 5 句一起轉成 embedding（論文使用 OpenAI `text-embedding-3-small`，也測試過換成 `text-embedding-3-large`，結果幾乎不變）。
3. **相似度轉成機率分布**：計算回答與 5 句參考句的 cosine similarity，**減去其中的最小值**，再正規化成 1–5 分的機率分布。

第 3 步的「減去最小值」是個關鍵細節。論文指出，在 embedding 空間裡，「非常不可能買」和「非常可能買」的向量距離其實很近；如果不先扣掉基底相似度，算出來的分布會幾乎是平的。此外，為了降低單一措辭的偏差，論文設計了 6 組不同的參考句，各自算出分布後再取平均。

換成 SSR 之後，結果明顯改善：

| 方法 | 排序（ρ） | 分布形狀（KS similarity） |
| :--- | :---: | :---: |
| DLR 直接打分 | 約 80% | `0.26`（GPT-4o）／`0.39`（Gemini） |
| **SSR 語意映射** | **約 90%** | **`0.88`（GPT-4o）／`0.80`（Gemini）** |

論文還放了兩個很有意思的對照組：

* **監督式 ML 基線（LightGBM）**：拿一半真實問卷資料去訓練 LightGBM 預測另一半，排序只有 ρ = 65%；同一組比較中，完全零樣本、沒看過訓練資料的 SSR 拿到 **88%**。
* **中間方案 FLR（Follow-up Likert Rating）**：先讓模型寫自由文字，再轉成一個整數分數。它的分布比直接打分好，但在同一組比較裡，無論排序（83%）或分布（`0.72`）都輸給 SSR。這個現象很重要，一年後的獨立研究也看到了同樣的傾向。

---

## 三、一年後：四篇審計論文補齊了哪些拼圖

2026 年 8 到 10 月間，四篇在參考文獻中直接引用 SSR 的新論文陸續發表，從不同角度檢驗「LLM 當人類替身」這件事。它們測的任務不盡相同，但合起來剛好畫出了這類技術的真實邊界：

| 論文 | 測試場景 | 關鍵發現 |
| :--- | :--- | :--- |
| [Item-Mean Surrogates](https://arxiv.org/abs/2608.29455)（2026/08） | 四個公開資料集，預測特定個人的回答 | 準確度大多來自猜中「題目平均」；個人對特定題目的穩定偏好，LLM 只抓到約十分之一。寫更細的 Persona、換模型、甚至 fine-tune 都救不回來（fine-tune 後反而更差） |
| [Can AI Agents Simulate A/B Test Outcomes?](https://arxiv.org/abs/2608.02345)（2026/08） | 67 個歷史行銷 A/B Test | 裸跑時方向正確比例達 `0.70`，但效果幅度系統性高估。加上兩階段事前校準，平方誤差降約 **77 倍**；讓同一個 Agent 同時看 A/B 兩組，標準誤降約 **2.4 倍** |
| [Scored vs. Generated Readouts](https://arxiv.org/abs/2609.09882)（2026/09） | 顧客行為 fine-tune 模型，4 個零售任務 | 直接讀取 answer token 機率，在 13 組實驗中有 12 組的排序（AUC）贏過「先寫理由再預測」，差距達 **1.5 到 14.5 個百分點** |
| [Probable but Not Valid](https://arxiv.org/abs/2610.14912)（2026/10） | 立陶宛組織心理學問卷，14 個 decision model 與 47 個生成式 LLM | 機率分布取平均後，比四捨五入成整數更貼近真人；但預測個人答案時全數輸給「其他受訪者的答題頻率」基線。10 條產品線中有 5 條的**最新版反而比舊版退步** |

把這四篇放在一起看，有三個對工程團隊非常明確的訊號。

### 訊號一：讀分布，不要讀整數
SSR 與 *Probable but Not Valid* 走的是不同路線，卻指向同一個結論：**保留機率分布，比壓成單一整數更接近人類。** SSR 是透過 embedding 映射到分布，decision model 則是直接吐出各分數的機率，兩者都優於「抽樣一個整數」。

### 訊號二：「先寫理由再打分」反而會稀釋訊號
SSR 論文裡的 FLR 輸給 SSR；*Scored vs. Generated Readouts* 裡，「先寫理由再預測」在 12/13 組實驗中輸給直接讀 token 機率。後者分析了約 9,000 段生成理由，發現寫理由會讓模型降低對關鍵預測特徵的依賴，並收斂到千篇一律的套話。

雖然兩篇的對照對象不同（*Scored vs. Generated* 測的是 fine-tune 過的行為模型，而非 SSR），但工程上的結論完全相容：**理由和分數應該分開取。** 保留自由文字給人看解釋，分數與排序則從機率分布讀出來。

### 訊號三：群體層級有效，個人層級不行
*Item-Mean Surrogates* 與 *Probable but Not Valid* 講穿了同一件事：LLM 擅長捕捉的是「大眾平均怎麼看」，而不是「某個特定個人怎麼想」。後者的結論非常直白——用人口統計 Profile 建出來的合成受訪者，目標應該放在樣本層級。

其實 SSR 論文本身也只主張群體層級的效果，並坦承性別與居住地區的還原度較差。真正容易踩雷的，往往不是論文，而是把論文過度包裝成「能精準模擬每個細分客群」的商業話術。

---

## 四、企業該怎麼選：三種分數讀出方式

把上述研究整理成實際落地時的工程選項（*此表為作者整理與推論*）：

| 讀出方式 | 做法 | 適合場景 | 主要限制 |
| :--- | :--- | :--- | :--- |
| **取樣一個整數** | Prompt 要求「只輸出 1–5」 | 只需要粗略排序、不在乎分布比例 | 分布嚴重塌縮到中間，無法算比例 |
| **讀機率分布** | 讀取 1–5 各分數 token 的 logprobs，或用 decision model | 能取得 logprobs 的環境（如地端模型）；重視排序與分布 | 許多商用 API 不開放完整 logprobs；token 機率對 prompt 格式敏感 |
| **語意映射（SSR）** | 自由文字 → embedding → 錨點相似度 → 分布 | 只拿得到文字輸出的商用 API；同時需要分數與文字理由 | 錨點句需依領域與語言調校；多一次 embedding 成本 |

至於「先寫理由再給整數」，不建議拿來當正式計分方式——文字理由很有價值，但應該當成另一個獨立欄位輸出，不要讓它去干擾最終分數。

### 適合導入的場景
* **成熟品類的早期概念篩選**：在花預算找真人前，先把 20 個點子收斂到 5 個。這正是 SSR 原論文驗證的場景。
* **抓文案盲點與拒買理由**：SSR 論文觀察到，合成消費者的自由文字回饋往往比真人問卷更具體，這份質性價值不依賴分數有多準。
* **A/B Test 前篩**：前提是先用歷史實驗做事前校準，並讓同一個 Agent 同時比較兩個版本（*Can AI Agents Simulate A/B Test Outcomes?*）。

### 應該避開的場景
* **模擬特定細分客群或個人偏好**：Persona 寫成 500 字小作文也救不回個人層級的偏好（*Item-Mean Surrogates*）。
* **把未校準分數直接當轉換率或 lift 預估**：方向可能對，幅度幾乎一定高估（*Can AI Agents Simulate A/B Test Outcomes?*）。
* **語料稀少的品類**：全新顛覆性產品、冷門 B2B 方案或高度在地化的細分市場。SSR 測試的是網路評論極多的個人護理品類，語料稀少時的效果並未被驗證（*作者推論*）。
* **預設新模型一定比較準**：*Probable but Not Valid* 裡有一半的產品線在新版反而退步，換模型必須當成新系統重新驗證。

---

## 五、上線前的工程檢查清單

如果團隊準備在評分系統或合成市調裡導入這套做法，建議上線前先確認這六件事：

1. **改存分布，不只存單一分數**：把輸出 schema 改成 1–5 分的機率分布，監控報表看分布與極端區間比例，而不只看平均分。
2. **將「計分」與「解釋」解耦**：文字理由留給人做質性判讀，排序與分數則由 logprobs 或 SSR 映射產出。
3. **錨點句先本地化再驗證**：SSR 原始參考句是針對英文購買意願調校的；換成繁體中文或客服滿意度等題型，必須先拿一批有真人標註的資料跑過驗證。
4. **先跑歷史回測做校準**：拿過去已有真實結果的問卷或 A/B Test 回測一次，量化系統性偏差後再正式上線。
5. **限制結論的顆粒度**：明訂合成結果只用於「群體層級的方案排序與問題排查」，不拿來替特定細分客群拍板。
6. **把換模型納入回歸測試**：模型升版或切換供應商時，重跑一次分布與排序驗證，不要假設新版自動比較好。

---

## 附註：開源實作現況

PyMC Labs 已將 SSR 核心演算法開源於 [pymc-labs/semantic-similarity-rating](https://github.com/pymc-labs/semantic-similarity-rating)（Apache-2.0）。2026 年全年只有一次功能更新：6 月發布的 v1.1.0，將分布計算向量化並開放預先計算相似度，方便做超參數掃描。

另外，2026 下半年 GitHub 上也冒出不少社群專案，把 SSR 包成 Coding Agent Skill 或 MCP Server，直接用 Agent 本身扮演受訪者、搭配本地 embedding 算分數。這類專案目前規模都還很小（星數從個位數到數十不等），若要拿來實測，建議先檢查裡面的錨點句設計與校準流程再使用。

---

## 參考資料

* Maier, B. F. et al. (2025). [LLMs Reproduce Human Purchase Intent via Semantic Similarity Elicitation of Likert Ratings](https://arxiv.org/abs/2510.08338). arXiv:2510.08338 (v3).
* Ahn, D., Mao, C., & Lee, D. (2026). [Item-Mean Surrogates: Why Richer Personas Fail to Deliver Individual Fidelity in LLMs as Human Surrogates](https://arxiv.org/abs/2608.29455). arXiv:2608.29455.
* Hut, S., & Masoero, L. (2026). [Can AI Agents Simulate A/B Test Outcomes? A Validation Framework for Agentic Experimentation](https://arxiv.org/abs/2608.02345). arXiv:2608.02345.
* Kraisingkorn, T., Pachtrachai, K., & Modecrua, W. (2026). [Scored vs. Generated Readouts in Behavioral Language Models: An Empirical Study of Elicitation Format](https://arxiv.org/abs/2609.09882). arXiv:2609.09882.
* Lukauskas, M., & Šarkauskaitė, V. (2026). [Probable but Not Valid: A Psychometric Audit of Decision Models as Synthetic Survey Respondents](https://arxiv.org/abs/2610.14912). arXiv:2610.14912.
* [pymc-labs/semantic-similarity-rating](https://github.com/pymc-labs/semantic-similarity-rating)
