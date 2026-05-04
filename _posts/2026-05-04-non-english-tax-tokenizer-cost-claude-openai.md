---
title: "非英語稅：你用 Claude 寫中文，每一個字都比美國人貴 71%"
date: 2026-05-04 08:00:00 +0800
permalink: /non-english-tax-tokenizer-cost-claude-openai/
image: /assets/images/non-english-tax-tokenizer-cover.png
description: "同一篇文章翻成不同語言丟給 LLM，Anthropic 處理中文比英文多吃 1.71 倍 token，印地語直接 3.24 倍；OpenAI 比較克制但中文也要 1.15 倍。這個被叫做「非英語稅」的隱藏成本，正在悄悄拉開亞洲企業跟美國公司的 API 帳單差距。本文拆解 tokenizer 為什麼歧視非英語、算給你看一個典型台灣企業 case 的真實成本差距、以及為什麼我自己仍然主要用 Claude——但會在哪些場景切換到 OpenAI 或 DeepSeek。"
---

# 非英語稅：你用 Claude 寫中文，每一個字都比美國人貴 71%

## 一張對比表，看懂為什麼你的 API 帳單比 SF 同事貴

最近有一份調研數據在 AI 圈流傳——AI 研究員 [Aran Komatsuzaki](https://x.com/arankomatsuzaki/status/1636367967306027013) 把 Richard Sutton 的經典文章 [《The Bitter Lesson》](http://www.incompleteideas.net/IncIdeas/BitterLesson.html) 翻譯成多種語言，分別丟進 OpenAI 和 Anthropic 的 tokenizer 測 token 數，以英語為基準做對比。後來這份數據被 [Aihola 整理成報導](https://aihola.com/article/claude-tokenizer-language-tax) 廣傳，中文社群也在 [LINUX DO](https://linux.do/t/topic/2081874) 等地討論炸鍋。

做法很簡單，數據出來卻比很多人想像的差距大。

**Anthropic 模型（以英語 token 數 = 1.0 為基準）：**

| 語言 | Token 倍數 | 翻譯成成本含義 |
|---|---|---|
| 英語 | 1.00x | 基準 |
| 法語 | 1.79x | 貴 79% |
| 中文 | 1.71x | 貴 71% |
| 俄語 | 2.04x | 貴 104% |
| 阿拉伯語 | 2.86x | 貴 186% |
| 印地語 | 3.24x | 貴 224% |

**OpenAI 模型（同樣以英語 = 1.0 為基準）：**

| 語言 | Token 倍數 | 翻譯成成本含義 |
|---|---|---|
| 英語 | 1.00x | 基準 |
| 法語 | 1.30x | 貴 30% |
| 中文 | 1.15x | 貴 15% |
| 俄語 | 1.31x | 貴 31% |
| 阿拉伯語 | 1.31x | 貴 31% |
| 印地語 | 1.37x | 貴 37% |

這個現象在英文社群被叫做 "non-English tax"——「非英語稅」。其實學術界早就在談這件事，2023 年的一篇 arXiv 論文 [《Language Model Tokenizers Introduce Unfairness Between Languages》](https://arxiv.org/pdf/2305.15425) 就系統性地量化了這個不公平。OpenAI Developer Community 上也有 [一個經典討論串](https://community.openai.com/t/all-languages-are-not-created-tokenized-equal/216407) 在罵這件事。

意思就是，**你用非英語寫同樣內容的 prompt，要多消耗幾倍的 token**，意味著更高的 API 成本、更慢的響應速度、更容易撞上下文窗口的上限。

而且不是兩家平均地貴。**Anthropic 對非英語的稅率，明顯比 OpenAI 重很多。**

我看到這個數據的第一反應是：「啊，原來不是我感覺的問題」。

我用 Claude Code 寫過上百萬 token 的中文 prompt，也用 OpenAI 處理過大量中文文件。體感一直就是 Claude 處理中文比較燒錢，但一直沒去算。這份數據把我的體感量化了——而且更慘。

---

## ⚠️ 兩個你必須知道的 Caveat

在繼續讀下去之前，我必須先講兩件事，不然這篇文章會誤導你。

### Caveat 1：這份數據沒被獨立審計

Aran Komatsuzaki 的測試是社群整理的非正式 benchmark，**沒有任何第三方獨立驗證**。原因很現實——**Anthropic 從來不公開現行 tokenizer**。

你想自己跑一次都跑不了。社群只能用反推：[javirandor/anthropic-tokenizer](https://github.com/javirandor/anthropic-tokenizer) 這個 GitHub repo 是社群透過觀察 generation stream 反推出來的近似版本，[Hacker News 的這個討論串](https://news.ycombinator.com/item?id=40711374) 還挖出 Anthropic 自己 repo 裡塞了一份 Claude 3 tokenizer。

所以 1.71x、3.24x 這些確切數字，**請當成方向性參考，不是法庭證據**。

唯一比較靠譜的可重現 benchmark 是 [vfalbor/llm-language-token-tax](https://github.com/vfalbor/llm-language-token-tax) 這個 repo，但它只測 OpenAI 的 cl100k 跟 o200k，沒測 Anthropic（因為前面講的原因）。它的 OpenAI 中文倍數是 1.33x，跟 Komatsuzaki 的 1.15x 有差距，可能是用了不同 tokenizer 版本（cl100k vs o200k）或不同文本。

### Caveat 2：Anthropic 已經回應了——Opus 4.7 重新設計 tokenizer

更重要的更新：**2026/4/16 Anthropic 發布的 [Claude Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7) 直接帶了重新設計的 tokenizer，就是專門針對這個非英語稅問題。**

根據 [VentureBeat 的報導](https://venturebeat.com/technology/anthropic-releases-claude-opus-4-7-narrowly-retaking-lead-for-most-powerful-generally-available-llm) 跟 [MindStudio 的評測](https://www.mindstudio.ai/blog/claude-opus-4-7-review)，新 tokenizer：

- **中文、日文、韓文、阿拉伯文、印地文 token 數降低 20-35%**
- **代價：英文 prompt 反而多吃 12-18% token**（vocab 重新分配的 trade-off）

換算下來：
- Opus 4.7 中文倍數 ≈ 1.71 × 0.7 ≈ **1.20x**（接近 OpenAI 的 1.15x）
- Opus 4.7 印地語倍數 ≈ 3.24 × 0.7 ≈ **2.27x**（還是偏高，但差距大幅縮小）

這是一個**值得肯定的修正**。Anthropic 從「對非英語使用者最不友好的大廠」變成「方向正確、但仍未追平 OpenAI」。

但要注意：**Sonnet 4.5、4.6 沒換 tokenizer**。所以如果你的 production 用的是 Sonnet（成本敏感的場景大部分都是），Komatsuzaki 的 1.71x 數字基本還是對的。要享受新 tokenizer 的紅利，得切到 Opus 4.7（[$5/$25 per MTok](https://platform.claude.com/docs/en/about-claude/pricing)），單價比 Sonnet 4.5 貴。

**所以接下來文章用 Sonnet 4.5 的 1.71x 算成本，仍然是 production 主流情境。** Opus 4.7 用戶請自己折算 0.7 倍。

---

## 這不是 bug 是 feature：BPE Tokenizer 的英文偏見

為什麼會這樣？要從 tokenizer 講起。

LLM 不是一個字母一個字母讀的，它是把文字切成 "token" 再讀。[BPE（Byte Pair Encoding）](https://en.wikipedia.org/wiki/Byte_pair_encoding) 這套 tokenizer 演算法，會根據訓練資料裡的字元頻率，把常見的字元組合合併成單一 token。想直觀感受 tokenizer 怎麼切你的文字，OpenAI 有 [官方 tiktokenizer 工具](https://platform.openai.com/tokenizer)，Anthropic 則可以用 [Lunary 的 Claude tokenizer](https://lunary.ai/anthropic-tokenizer) 或 [Token counting API](https://platform.claude.com/docs/en/build-with-claude/token-counting)。

英文有個天然優勢：**26 個字母 + 高度結構化的 subword pattern**。"unbelievable" 雖然 12 個字母，但 BPE 會把它切成 "un" + "believ" + "able" 三個 token。

中文不一樣。中文 4-5 萬個常用字，每個字本身就是語義單位。但 tokenizer 訓練時看到的中文資料相對少，所以很多中文字會被切成 2-3 個 byte-level token。一個「龘」字可能就吃掉 3 個 token，因為它在訓練資料裡出現次數太少，根本沒被合併。Ivan Krivyakov 的 [這篇實驗筆記](https://ikriv.com/blog/?p=5322) 跟 [PromptCost 的拆解](https://promptcost.org/blog/llm-tokenization-explained/) 都把這個機制講得很清楚。

**Anthropic 比 OpenAI 慘的原因，就是 vocab size 跟訓練資料的多語言比例。**

OpenAI 的 [cl100k_base 系列 tokenizer](https://github.com/openai/tiktoken)，大概是 100K vocab，訓練資料的多語言佔比較高（GPT-4o 之後升級到 [o200k_base](https://github.com/openai/tiktoken/blob/main/tiktoken_ext/openai_public.py)，更友好）。Anthropic 公開資訊較少（[官方 API 文件](https://platform.claude.com/docs/en/build-with-claude/token-counting) 只給 count_tokens API，不給 vocab），但從這個倍數可以反推——他們的 tokenizer 對非英語的覆蓋確實比較弱，或者說，**他們是用英語使用者的視角優化的**。

印地語 3.24x 不是隨機數字。印地語用的是 Devanagari 字符（天城文），這套字符在 byte-level 編碼下每個字符就要 3 個 byte。如果 tokenizer 沒有針對性合併常見字符組合，一個印地語句子的 token 數會很可怕。

阿拉伯語 2.86x 同理，Arabic script 加上連字（ligature）特性，tokenizer 處理不好就會爆 token。

這不是惡意，是優先級問題。**在訓練 tokenizer 的時候，你要決定 vocab 的 100K 個位子分給誰**。給英文 subword 多一點，benchmark 上看起來更好；給其他語言多一點，會犧牲英文 efficiency。

Anthropic 顯然選了前者。

---

## 算給你看：一個典型台灣企業的真實帳單差距

理論講完，看實際成本。

假設你是一家台灣的金融業，做一個中文客服 chatbot：

- **每天處理 conversations：** 10,000 通
- **每通平均 input：** 500 token（英語基準下）
- **每通平均 output：** 200 token
- **語言：** 100% 繁體中文

用 [Claude Sonnet 4.5](https://platform.claude.com/docs/en/about-claude/pricing)（$3/MTok input, $15/MTok output）跑：

```
中文 input token = 500 × 1.71 = 855 token/通
中文 output token = 200 × 1.71 = 342 token/通

每通成本 = 855 × $3/1M + 342 × $15/1M
        = $0.00257 + $0.00513
        = $0.0077

每天成本 = $77
每月成本 = $2,310
```

換成 [GPT-4o](https://openai.com/api/pricing/)（$2.5/MTok input, $10/MTok output）：

```
中文 input token = 500 × 1.15 = 575 token/通
中文 output token = 200 × 1.15 = 230 token/通

每通成本 = 575 × $2.5/1M + 230 × $10/1M
        = $0.00144 + $0.00230
        = $0.0037

每天成本 = $37
每月成本 = $1,121
```

換成 [DeepSeek V3](https://api-docs.deepseek.com/quick_start/pricing)（中文 tokenizer 友好，約 $0.27/MTok input, $1.1/MTok output）：

```
中文 input token ≈ 500 × 0.95 = 475 token/通（中文比英文還省）
中文 output token ≈ 200 × 0.95 = 190 token/通

每通成本 = 475 × $0.27/1M + 190 × $1.1/1M
        = $0.00013 + $0.00021
        = $0.00034

每天成本 = $3.4
每月成本 = $102
```

**同樣的中文 chatbot，月帳單差距：Claude $2,310 vs OpenAI $1,121 vs DeepSeek $102。**

差距不是 2 倍 3 倍，是 22 倍。

而且這還只算了單價跟 token 倍數。沒算 latency，沒算 context window 撞上限被迫 truncate、被迫多輪對話的次數、被迫做 summarization 的額外成本。

---

## 印地語、阿拉伯語：為什麼新興市場用 Claude 等於自殺

3.24x 是什麼概念？

如果你是印度的 startup，做一個印地語的法律諮詢 agent，你的單位成本就是美國同行的 3.24 倍。但你的 ARPU 大概只有美國市場的 1/10。

**結構上你就活不下去。**

這就是為什麼印度本土的 AI startup 幾乎全部投向 [Llama](https://www.llama.com/)、[Mistral](https://mistral.ai/)、自訓 Indic 模型（例如 [Sarvam AI](https://www.sarvam.ai/)、[Krutrim](https://www.olakrutrim.com/)）。不是民族主義，是經濟學。Claude 在印度市場根本沒法做 cost-effective 的 deployment。

阿拉伯語也是一樣。沙烏地、阿聯的政府投資 AI 蓋自己的模型（[Falcon](https://falconllm.tii.ae/)、[Jais](https://inceptionai.ai/jais/)），表面上是技術自主，底層也是這個 token 經濟學的問題——你不能每次跑阿拉伯語都吃 2.86x 稅。

對比之下，**OpenAI 的 1.31x 印地語倍數，是 Anthropic 的不到一半**。這就是為什麼 OpenAI 在新興市場滲透率明顯比 Anthropic 高。Anthropic 在企業市場很強，但企業市場集中在英語區。新興市場是 OpenAI 的天下。

這不是巧合，是 tokenizer 設計選擇的累積結果。

---

## 中國模型的反向優勢：你不只省錢，你也省 context window

當對比擴展到 [Gemini](https://ai.google.dev/gemini-api/docs/pricing)、[Qwen](https://qwenlm.github.io/)、[DeepSeek](https://api-docs.deepseek.com/)、[Kimi](https://platform.moonshot.cn/)，覆蓋中文、日語、韓語、西班牙語、法語、德語、俄語、阿拉伯語、印地語等多個語言，結論更清晰了：

**主流中文模型處理中文比英文便宜。**

這不只是價格問題。Token 倍數低意味著兩件事：

1. **單筆 API 成本低**——直接的成本優勢
2. **同樣的 context window 能塞更多內容**——隱形的能力優勢

第二點被嚴重低估。

舉個例子：你要做一個 RAG 系統，retrieve 10 份中文 PDF 餵給模型。

用 Claude Sonnet 4.5（200K context）：每份 PDF 中文約 50K 字，被 tokenize 成 ~85K token（1.71x）。**塞 2.5 份就滿了。**

用 DeepSeek V3（128K context）：同樣的 PDF，~47K token（0.95x）。**塞 2.7 份。**

雖然 Claude 的 context window 數字大一倍，但折算非英語倍率，**處理中文場景的有效 context 反而 DeepSeek 比較大**。

這就是為什麼你會看到中國的金融、法律、醫療領域大量採用 DeepSeek、Qwen——不是因為「國產替代」的口號，是因為在他們的語言場景下，數學就是這樣。

---

## What didn't work smoothly：Claude 仍然值得的時候

寫到這裡，你以為我要勸你全部切換到 OpenAI 或 DeepSeek。

不是。我自己現在主要用的還是 Claude（Claude Code、Claude Sonnet 4.6）。

我來坦白幾個 Claude 仍然值得貴 1.71x 的場景：

**1. 推理密度高的任務**

寫一個複雜的 PRD 或 architecture review，Claude Sonnet 4.5 / Opus 4 的輸出品質仍然明顯高於 GPT-4o。我做過的測試：同樣的輸入，Claude 一次到位，GPT 需要 2-3 輪 refine。**Token 倍數帳算下來反而 Claude 更省。**

**2. Coding 場景**

Claude Code 對 codebase 的理解和 multi-file edit 能力，目前沒有對手。即使每個 prompt 多吃 71% token，但完成一個 task 需要的 prompt 次數可能少 50%。**整體 token 總量未必更多。**

**3. 長文本理解**

雖然 Claude 處理中文倍數高，但 200K context 的「實際可用容量」對複雜文件分析仍然夠用。換到 GPT-4o 的 128K，撞上限的次數更多。

**4. Tool use 跟 agent loop**

Claude 的 tool use 訓練做得比較細，agent loop 在意外狀態下的 recovery 比較好。這個品質差距在 production 是真金白銀的差距——一次 agent 跑掛，工程師 debug 1 小時的成本，遠遠超過省下的 API token 錢。

**所以非英語稅是真的，但不是「換一家就好」的問題。**

它是一個 **trade-off matrix**，不是 single answer。

---

## 三層策略：別 all-in 任何一家

我自己跟客戶談 LLM 選型時，現在會用三層策略：

**Tier 1｜高價值、低 volume 的核心任務**

- 用 [Claude Sonnet 4.5](https://platform.claude.com/docs/en/about-claude/models/overview) 或 [Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7)（後者非英語倍數已降 20-35%）
- 場景：策略文件、PRD、architecture design、核心 coding
- 心態：認賠 71% 中文稅（Sonnet）或 20% 中文稅（Opus 4.7），因為品質差距 > token 差距

**Tier 2｜中等價值、中 volume 的標準任務**

- 用 [GPT-4o](https://openai.com/api/pricing/) 或 [Gemini 2.0 Flash](https://ai.google.dev/gemini-api/docs/pricing)
- 場景：客服回覆、文件 summarization、一般問答
- 心態：1.15x 中文稅可以接受，速度跟成本是 sweet spot

**Tier 3｜低單價、高 volume 的批次處理**

- 用 [DeepSeek V3](https://api-docs.deepseek.com/quick_start/pricing) 或 [Qwen 2.5 Max](https://qwenlm.github.io/blog/qwen2.5-max/)
- 場景：批次 OCR 後處理、大量資料清洗、純中文場景的 embedding 預處理
- 心態：中文 token 反而比英文省，價格也最低，這個層級不用 Claude / OpenAI 是浪費錢

關鍵是：**不要用單一模型解決所有事。**

很多企業的 AI 帳單失控，不是因為用錯模型，是因為用同一個模型做所有事——把 Claude Opus 拿去做 OCR 後處理、拿去做客服 FAQ 匹配，這就是用 7-11 御飯糰的價錢買法國米其林三星。

我們團隊現在的 production 流程，**至少混用 3-4 個模型**。Routing 邏輯多寫一點，月帳單差 5-10 倍很正常。

---

## 最後想說

非英語稅這個現象，技術上不是新發現。tokenizer 的 multilingual fairness 問題，學術界討論很多年了。

但這個數據之所以值得寫，是因為它把一件本來只有研究員在意的事，變成了**任何亞洲企業在做 LLM 選型時都該算清楚的成本項**。

如果你的核心市場是英語區，這篇文章對你影響不大。

如果你的核心市場是中文、日韓、東南亞、印度、中東——你正在被收一筆隱藏的稅。**不知道，不代表沒繳。**

最後再強調一次前面講的兩個 caveat：

1. **Komatsuzaki 的數字沒被獨立審計**——確切倍數請當參考，不要當聖經。要精確算，自己拿真實 prompt 跑 [Anthropic 的 token counter](https://platform.claude.com/docs/en/build-with-claude/token-counting) 跟 [OpenAI 的 tiktokenizer](https://platform.openai.com/tokenizer)。
2. **Anthropic Opus 4.7 已經改善了**（[2026/4/16 發布](https://www.anthropic.com/news/claude-opus-4-7)）——非拉丁文字 token 數降 20-35%，但代價是英文 token 多吃 12-18%。Sonnet 系列還沒換 tokenizer，所以 production 主流情境（用 Sonnet 4.5 / 4.6）這篇文章的數字仍然成立。

但「Anthropic 對非英語比 OpenAI 重」這個方向性結論，**跟我自己用了兩年的體感完全一致，差距沒有完全追平**。

下次跟你的 CTO 報 Claude 帳單時，記得加一句：「這個帳單裡有 71% 是非英語稅。如果我們的目標市場是中文，這筆稅該不該繳，要看每個任務的價值密度。要省這筆稅可以考慮升 Opus 4.7 換新 tokenizer，但單價貴一倍——又是另一個 trade-off。」

這比「Claude 太貴了我們換 OpenAI」要 professional 太多。

---

## 延伸閱讀

**原始數據與報導：**
- [Aran Komatsuzaki 在 X 上對多家 tokenizer 的早期觀察](https://x.com/arankomatsuzaki/status/1636367967306027013)
- [Aihola — Claude Tokenizer Language Tax 報導](https://aihola.com/article/claude-tokenizer-language-tax)（2026/4/28）
- [LINUX DO 中文社群討論：Claude 的中文稅](https://linux.do/t/topic/2081874)
- [vfalbor/llm-language-token-tax — 可重現 OpenAI tokenizer benchmark](https://github.com/vfalbor/llm-language-token-tax)

**Anthropic Opus 4.7 新 tokenizer 相關：**
- [Anthropic 官方公告：Introducing Claude Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7)
- [VentureBeat：Anthropic Opus 4.7 narrowly retaking lead](https://venturebeat.com/technology/anthropic-releases-claude-opus-4-7-narrowly-retaking-lead-for-most-powerful-generally-available-llm)
- [MindStudio：Opus 4.7 Review — What Actually Changed](https://www.mindstudio.ai/blog/claude-opus-4-7-review)
- [Claude Opus 4.7 Release Tracker (findskill.ai)](https://findskill.ai/blog/claude-opus-4-7-release-tracker/)
- [Claude API 官方定價頁](https://platform.claude.com/docs/en/about-claude/pricing)

**學術背景：**
- [arXiv 2305.15425 — Language Model Tokenizers Introduce Unfairness Between Languages](https://arxiv.org/pdf/2305.15425)
- [Richard Sutton — The Bitter Lesson（被拿來測試的原文）](http://www.incompleteideas.net/IncIdeas/BitterLesson.html)

**Tokenizer 工具：**
- [OpenAI tiktokenizer](https://platform.openai.com/tokenizer) / [tiktoken GitHub](https://github.com/openai/tiktoken)
- [Anthropic 官方 Token counting API](https://platform.claude.com/docs/en/build-with-claude/token-counting)
- [Lunary Anthropic Tokenizer 工具](https://lunary.ai/anthropic-tokenizer)
- [javirandor/anthropic-tokenizer — 社群反推的 Claude tokenizer](https://github.com/javirandor/anthropic-tokenizer)
- [Hacker News — Anthropic 自己 repo 裡的 Claude 3 tokenizer](https://news.ycombinator.com/item?id=40711374)

**其他相關拆解：**
- [Ivan Krivyakov — LLM Tokens and Foreign Languages](https://ikriv.com/blog/?p=5322)
- [PromptCost — LLM Tokenization Explained: English vs Other Languages](https://promptcost.org/blog/llm-tokenization-explained/)
- [OpenAI Developer Community — All languages are NOT created (tokenized) equal](https://community.openai.com/t/all-languages-are-not-created-tokenized-equal/216407)

**模型 / 廠商連結：**
- [Claude Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- [OpenAI API Pricing](https://openai.com/api/pricing/)
- [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [DeepSeek API Pricing](https://api-docs.deepseek.com/quick_start/pricing)
- [Qwen 2.5 Max](https://qwenlm.github.io/blog/qwen2.5-max/)
- [Moonshot Kimi 平台](https://platform.moonshot.cn/)
- [Sarvam AI（印度 Indic 模型）](https://www.sarvam.ai/) / [Krutrim](https://www.olakrutrim.com/)
- [Falcon LLM（UAE）](https://falconllm.tii.ae/) / [Jais（沙烏地）](https://inceptionai.ai/jais/)

---

## 常見問題 Q&A

**Q: 這個倍數會隨模型版本改變嗎？**

會。Tokenizer 通常跟著模型大改版才換，但每次換 tokenizer 倍數都可能變。建議自己拿真實 prompt 用各家的 tokenizer 算一次，最準。

**Q: 為什麼 OpenAI 的中文倍數比 Anthropic 低這麼多？**

主要是 vocab size 跟訓練資料的多語言比例。OpenAI cl100k 系列對中文 subword 覆蓋較好。Anthropic tokenizer 細節公開較少，但從倍數可以反推他們對非英語的優化優先級較低。

**Q: 用 prompt cache 能不能抵消非英語稅？**

可以部分抵消。[Anthropic 的 prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching) 對重複前綴有 90% 折扣，所以高重複率場景（agent system prompt、固定 RAG context）會大幅降低 effective cost。但動態 user input 的部分稅照繳。我之前寫過 [一篇關於 KV Cache 怎麼省 80% token 的文章](/kv-cache-gemma4-claude-code-save-80-percent-token/) 可以參考。

**Q: 如果我做的是中英文混合 prompt，倍數怎麼算？**

按比例加權平均。一個 70% 中文 + 30% 英文的 prompt，用 Claude 約 1 × 0.3 + 1.71 × 0.7 ≈ 1.50x。實務上建議拆 system prompt 用英文（讓 model 理解 task）+ user data 用原文。

**Q: 用中國模型有 compliance 顧慮怎麼辦？**

不要 production 接 DeepSeek 公開 API（資料出境問題）。用 [開源權重](https://huggingface.co/deepseek-ai) 自己 host，或用台灣 / 香港的 cloud provider 提供的 inference endpoint。[Qwen 開源版本](https://huggingface.co/Qwen) 可以完全 on-prem，這個議題我在 [本地 LLM 企業架構這篇](/local-llm-enterprise-architecture/) 講得更完整。
