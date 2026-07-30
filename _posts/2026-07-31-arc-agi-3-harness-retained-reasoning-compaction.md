---
layout: post
title: "GPT-5.6 Sol 改兩個設定，ARC-AGI-3 從 13% 跳到 38%：Benchmark 測的從來不只是模型"
date: 2026-07-31 09:00:00 +0800
permalink: /arc-agi-3-harness-retained-reasoning-compaction/
image: /assets/images/arc-agi-3-harness-retained-reasoning-cover.png
description: "OpenAI 7 月 29 日發文指出，GPT-5.6 Sol 在 ARC-AGI-3 的低分不是模型問題——是 harness 設計把推理記憶砍了。改兩個 API 設定（retained reasoning + compaction），公開題集分數從 13.3% 跳到 38.3%，output tokens 減少 6 倍。OpenAI 產品 GM Thibault Sottiaux 直接宣稱 Sol 才是 ARC-AGI-3 的真正 SOTA。這篇拆解這兩個設定的機制、benchmark 公平性的兩難，以及為什麼這是 harness 系列的第三個數據點——同模型、同任務，只改基礎設施，能力差 3 倍。"
---

Opus 5 在 ARC-AGI-3 官方排行榜拿下 30.2%，刷新紀錄。兩天後，OpenAI 發了一篇[技術文](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/)，說 GPT-5.6 Sol 其實是 38.3%——只是需要開兩個設定。

OpenAI 產品 GM Thibault Sottiaux 在 X 上的措辭更直接：

> Turns out GPT-5.6 Sol is actually SoTA on ARC-AGI-3. Just took two setting changes.

這兩個設定叫 retained reasoning 和 compaction。不是新模型，不是新架構，不是重新訓練。是兩個 API 參數。

---

## 30 秒定位

| 項目 | 數字 |
|------|------|
| GPT-5.6 Sol 官方排行榜分數 | 7.78%（RHAE） |
| 公開題集 + 官方 harness | 13.3% |
| 公開題集 + retained reasoning + compaction | 38.3% |
| 分數提升倍數 | 約 3 倍 |
| Output tokens 減少 | 6 倍 |
| 人類測試者平均分 | 48%（官方 gameplay logs） |
| Opus 5 官方排行榜 | 30.2%（目前 SOTA） |
| ARC-AGI-3 launch（2026 年 3 月）| 所有 frontier 模型 < 1% |

RHAE 是 Relative Human Action Efficiency，拿模型表現跟人類基準比。模型看不到自己的分數，只拿到每一幀的文字描述和當前關卡。

---

## ARC-AGI-3 是什麼，它的 harness 做了什麼

ARC-AGI-3 是 ARC Prize 設計的 benchmark，讓 AI agent 探索陌生的 2D 遊戲，在沒有說明書的情況下推論遊戲規則。你可以在 [arcprize.org/tasks](https://arcprize.org/tasks) 自己玩 25 個 demo 關卡。

ARC 的設計哲學是用「刻意簡化的 harness」來測模型——不給特殊工具、不做 vendor-specific 優化、所有模型用同一套通用介面。邏輯是：harness 越簡單，模型的差異越能被看見，跨模型的比較越公平。

但 OpenAI 團隊（文章作者 Ilan Bigio 和 Ted Sanders）發現，這個 harness 對 GPT-5.6 Sol 做了兩件事，而這兩件事恰好砍掉了 Sol 最核心的能力：

**第一，每次行動後丟棄所有推理過程。** Sol 在每一步行動前會產生 private reasoning（內部思考），這些思考在行動完成後被 harness 丟掉。下一步行動時，Sol 可以看到之前做過什麼（行動記錄），但看不到自己當時為什麼那樣做（推理脈絡）。

**第二，context 超過 175,000 字元就滾動截斷。** 早期的行動記錄被直接丟棄。不是摘要，是刪除。Sol 不只忘了自己的思考，連行動記錄也在逐漸消失。

用白話講：想像你在玩一個完全陌生的遊戲。每走一步，你的短期記憶就被清空——你知道自己剛才按了什麼鍵，但不記得為什麼按。走了一百步之後，連前五十步按了什麼也忘了。在這種條件下，你每一步都得從頭推論遊戲規則。

Sol 打敗過 Pokemon FireRed、Slay the Spire、Baba Is You 的初期關卡。它不是不會玩遊戲。它是被 harness 打斷了學習迴路。

---

## 兩個設定改了什麼

### Retained reasoning

OpenAI 的模型在回答或呼叫工具前，會先產生 private reasoning messages。在 ChatGPT 和 Codex 的生產環境裡，這些推理記錄會被保留在對話歷史中——模型下一步可以看到自己之前想了什麼。

ARC-AGI-3 的官方 harness 把這些推理記錄丟掉了。OpenAI 用 Responses API 重新實作 harness，只需要傳入前一次 response 的 ID，推理就自動保留。

效果有兩個。第一，Sol 每步行動前的思考時間大幅縮短，因為不需要每次從頭推論遊戲規則。第二，Sol 在保留思考脈絡的情況下，能跨步驟累積對遊戲的理解，策略變得連貫。

### Compaction

官方 harness 處理 context 超限的方式是 rolling truncation——超過 175,000 字元就從最舊的訊息開始刪。

Rolling truncation 有兩個問題。第一，模型失去早期的觀察和行動記錄。第二，模型長時間在接近滿載的 context window 裡運作，推理品質會下降。

Compaction 是 Responses API 的另一個設定，用摘要取代截斷。context 接近上限時，把舊的對話壓縮成摘要，保留關鍵資訊但釋放空間。Sol 在更長的遊戲過程中，能保住它對每個遊戲學到的規則。

兩個設定加在一起：13.3% → 38.3%，output tokens 從約 350 萬降到約 60 萬。模型不只變準了，還變省了。

---

## 這件事和 EFC 論文說的是同一個故事

如果你讀過本 blog 之前寫的 [Effective Feedback Compute](/agent-harness-effective-feedback-compute/)，會發現 OpenAI 這個案例幾乎是 EFC 框架的教科書示範。

EFC 論文定義了「有效反饋」必須同時滿足四個條件：Informative（帶來新資訊）、Valid（可靠）、Non-redundant（不重複已知）、**Retained（被拿去改變下一步決策）**。

ARC-AGI-3 官方 harness 的問題，精確地對應到第四個條件——推理過程沒有被 retain，反饋迴路斷了。Sol 在每一步都產生了推理，但這些推理沒有進到下一步決策裡。它的 feedback compute 幾乎全部浪費掉了。

而那篇論文的核心發現是：raw compute（token 數量、工具呼叫次數）只能解釋 33-42% 的結果。剩下的六成，取決於反饋是否有效。Sol 的案例用另一組數據驗證了同一個結論：6 倍的 token 產出，換來的不是更好的結果，是同樣的困惑重複六遍。

---

## 這是 harness 系列的第三個數據點

這個 blog 過去一個月寫了好幾篇 harness 相關的文章。把 ARC-AGI-3 事件放進去，三個數據點排在一起：

| 案例 | 模型 | Harness 差異 | 效果差距 |
|------|------|-------------|---------|
| [Kimi K3 官方 vs Maka](/local-first-model-needs-local-first-harness/) | Kimi K3 | context prune + 精簡工具面 + 迭代循環 | 59.6% → 69.7%（+10pp） |
| [EFC 論文](/agent-harness-effective-feedback-compute/) | 多模型 | raw compute vs effective feedback compute | R² 0.33-0.42（raw 只解釋三四成） |
| ARC-AGI-3 | GPT-5.6 Sol | retained reasoning + compaction | 13.3% → 38.3%（3 倍） |

三個案例、三組人馬、三個不同的 benchmark。結論指向同一件事：**harness 不是模型的包裝紙，是能力的一部分。** 而且這個「一部分」的比重不是微調級別的——是 10 個百分點到 3 倍的級別。

---

## 反方：benchmark 社群的立場是合理的

寫到這裡，必須正面處理另一邊的論點。

ARC Prize 選擇用通用 harness 是有原因的。如果每家 vendor 都用自己最優化的 harness 跑分，排行榜就失去了跨模型比較的能力。OpenAI 用 Responses API 跑出 38.3%，Anthropic 可以用 extended thinking 跑出另一個數字，Google 可以用 Gemini 的 context caching 跑出又一個數字。到最後排行榜比的不是模型，是 harness engineering。

而且「用生產環境設定跑分」這件事本身有灰色地帶。OpenAI 說 retained reasoning 和 compaction 是 ChatGPT 和 Codex 的預設設定——但那是 OpenAI 自己的產品。第三方開發者用 API 時，這些設定不一定是預設的，compaction 甚至是需要主動開啟的。

MLQ 的報導標題直接點破了這個張力：「OpenAI Claims GPT-5.6 Sol Beats Opus 5 on ARC-AGI-3—but Only With Non-Standard API Settings」。

所以 benchmark 社群用通用 harness 的邏輯是對的嗎？在「公平比較」這個目標下，是對的。問題是：公平比較和真實能力，哪一個對使用者更有意義？

真實世界不用 generic harness。你在生產環境裡用 GPT-5.6 Sol，你會開 retained reasoning，你會開 compaction。就像你不會故意把一台車的安全氣囊關掉再測撞擊成績。Benchmark 測的是受控條件下的「模型裸跑能力」，但使用者在乎的是「我實際能拿到的能力」。

這兩個問題都有價值，但它們的答案不一樣。現在的 benchmark 體系還沒有好的方式同時回答兩者。

---

## 坦白說

幾件事必須說清楚。

第一，OpenAI 文章裡的 38.3% 是在 ARC-AGI-3 的**公開題集**上跑的，不是私有測試集。官方排行榜用的是私有測試集（Sol 在上面是 7.78%）。公開題集和私有測試集的分數不能直接比——但 OpenAI 也在公開題集上跑了官方 harness 的 13.3% 作為對照，所以 13.3% → 38.3% 的提升倍數是同基準的比較。

第二，38.3% 和 Opus 5 官方排行榜的 30.2% 不是同一個測試集，嚴格來說不能直接比較。Sottiaux 宣稱 Sol 是 SOTA 的說法，在方法論上有爭議。

第三，這篇文章是 OpenAI 自己寫的。它選擇了對自己最有利的 benchmark 和設定來展示效果。ARC-AGI-3 的特性（長時間遊戲、需要跨步驟累積學習）恰好是 retained reasoning 和 compaction 最能發揮的場景。在其他類型的 benchmark 上，這兩個設定的提升幅度可能完全不同。

第四，我們不知道 Opus 5 在 ARC-AGI-3 上用了什麼等級的 inference-time compute。如果 Opus 5 也用了 extended thinking，30.2% 可能已經包含了類似的推理保留機制。兩個數字背後的 inference 成本結構可能完全不一樣。

---

## 關鍵洞察

**對 API 開發者：context 管理策略跟模型選型一樣重要。** 如果你在做 multi-turn agent，第一件事不是比較哪個模型分數高，是檢查你的 harness 有沒有把推理記錄保留下來，有沒有在 context 超限時用摘要而不是截斷。這兩個設定在 Sol 上值 3 倍分數。即使你用的不是 OpenAI 的模型，底層邏輯是通用的：reasoning retention 和 context compaction 是所有長程 agent 的基本需求。

**對評估 AI 能力的人：benchmark 從來不是在真空中測模型。** 它同時測了 harness、API 設定、prompt engineering、context window 管理。一個模型在某個 benchmark 上的低分，不一定代表模型弱——可能代表 harness 不適合那個模型的工作方式。反過來也成立：一個高分不一定代表模型強，可能只是 harness 恰好配合了它的優勢。

**對整個 benchmark 生態：** 我們需要在「公平比較」和「真實能力」之間找到新的平衡。目前的做法是用最低公約數的 harness 確保公平，代價是低估了所有模型的實際能力。另一個極端是每家用自己最強的 harness，代價是排行榜失去可比性。也許答案是同時維護兩個排行榜——一個用標準 harness，一個允許 vendor-optimized harness——讓使用者同時看到兩組數字。

---

## 參考來源

- [How enabling two settings tripled our scores on the ARC-AGI-3 benchmark | OpenAI](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/)
- [ARC Prize 官方 X 帳號：Opus 5 ARC-AGI-3 SOTA 公告](https://x.com/arcprize/status/2080716561539907928)
- [ARC-AGI-3 Public Demo Games](https://arcprize.org/tasks)
- [OpenAI Claims GPT-5.6 Sol Beats Opus 5 on ARC-AGI-3—but Only With Non-Standard API Settings | MLQ](https://mlq.ai/news/openai-claims-gpt-56-sol-beats-opus-5-on-arc-agi-3but-only-with-non-standard-api-settings/)
- [OpenAI claims GPT-5.6 Sol beats Opus 5 on ARC-AGI-3 with two additional settings | The Decoder](https://the-decoder.com/openai-claims-gpt-5-6-sol-beats-opus-5-on-arc-agi-3-with-its-latest-api-and-two-additional-settings/)
