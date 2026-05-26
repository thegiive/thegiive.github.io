---
layout: post
title: "Harness Engineering 才是勝負手：PwC 論文拆解 Grep 打贏 Vector RAG，換個 Harness 準確率差 17 個百分點"
date: 2026-05-26 07:00:00 +0800
permalink: /is-grep-all-you-need-pwc-agent-harness-reshapes-retrieval/
image: /assets/images/is-grep-all-you-need-paper-cover.png
description: "PwC 在 2026 年 5 月發了一篇論文「Is Grep All You Need? How Agent Harnesses Reshape Agentic Search」，在 LongMemEval 上用 116 題實測 grep vs vector retrieval，結論是 grep 普遍打贏 vector。但真正的暴擊是同樣 Claude Opus 4.6、同樣 grep，換個 harness 跑準確率差了 17 個百分點。Codex 從 inline 93.1% 換成 programmatic 直接掉到 55.2%。這不是「grep 比較強」的故事，是「Agent Harness 才是勝負手」的故事。"
---

![Is Grep All You Need? 論文首頁](/assets/images/is-grep-all-you-need-paper-cover.png)

**論文連結：** [arxiv.org/abs/2605.15184](https://arxiv.org/abs/2605.15184)

---

## 研究設計

PwC 的研究團隊（Sahil Sen, Akhil Kasturi, Elias Lumer, Anmol Gulati, Vamse Kumar Subbiah）設計這個實驗的問題很明確：

**「在 Agent 的脈絡下，retrieval 方法的選擇到底還重不重要？」**

過去學界比較 grep vs vector 都是在「standalone retrieval」的設定下——給一個 query、看 top-k 結果。但 Agent 不是這樣用檢索的。Agent 會 reason、會重試、會把工具結果跟自己的 context 整合。所以 PwC 的假設是：**retrieval 方法的好壞，可能會被 Agent harness 的設計給放大或抵消**。

### Dataset：LongMemEval

選用 **LongMemEval** 這個 benchmark，取 116 題樣本。任務形式是：

- 給 Agent 一堆「過去的對話歷史」
- 裡面混雜了大量無關內容（distractors）
- Agent 要找出回答當前問題所需的具體事實

LongMemEval 的答案常常依賴明確的日期、數字、偏好、命名片段——這是論文後面討論結果時很重要的脈絡。

### 四個 Agent Harness

- **Chronos**（作者群自製的客製 harness）
- **Claude Code**（Anthropic 的 CLI）
- **Codex**（OpenAI 的 CLI）
- **Gemini CLI**（Google 的 CLI）

搭配不同 backbone 模型（Claude Opus 4.6、GPT-5.4、Gemini 3.1 Pro、Gemini 3.1 Flash-Lite）。

### 兩個對照變因

- **檢索方法**：grep（字面字串搜尋）vs vector retrieval（embedding-based）
- **工具結果傳遞方式**：inline（直接塞回對話）vs programmatic（寫成檔案讓模型自己讀）

## 實驗一：Inline 模式下，grep 全面壓制 vector

第一個實驗是「full haystack」——完整對話歷史餵進去、inline 回傳工具結果。

| Harness + 模型 | Grep | Vector | 差距 |
|----------------|------|--------|------|
| Chronos + Claude Opus 4.6 | **93.1%** | 83.6% | +9.5 |
| Chronos + Gemini 3.1 Flash-Lite | **86.2%** | 62.9% | +23.3 |
| Claude Code + Claude Opus 4.6 | **76.7%** | 75.0% | +1.7 |
| Codex + GPT-5.4 | **93.1%** | 75.9% | +17.2 |
| Gemini CLI + Gemini 3.1 Pro | **81.9%** | 75.0% | +6.9 |

**5 組對照，grep 全勝**。最誇張的是 Chronos + Gemini Flash-Lite 那組，差 23.3 個百分點。

論文對這個結果的解釋是：

> "LongMemEval 的答案常常依賴精確的日期、數量、偏好、片段——這些在 tokenization 之後通常很穩定。Lexical tools 直接把這些字串撈出來，不用經過 embedding 這個瓶頸。"

換句話說：**vector embedding 是有損壓縮**。當答案需要的是「Lucky」這個具體名字、「2025-03-14」這個具體日期，embedding 把這些細節糊掉了；grep 反而精準命中。

論文用了一個詞描述 LongMemEval 的答案結構：「literal witnesses」（字面證據）——答案要的是字面上一模一樣的證據，不是改寫後的語意。

## 真正的暴擊：Harness 換掉，準確率差 17 個百分點

如果故事到這裡就結束，那就只是「grep 比 vector 強」的廣告。真正讓這篇論文有重量的是這個發現：

**同樣是 Claude Opus 4.6，同樣是 grep：**
- 在 **Chronos** 上跑：**93.1%**
- 在 **Claude Code** 上跑：**76.7%**

差 16.4 個百分點。

模型相同、檢索方法相同、資料相同——唯一變的是外殼。論文裡有一句話很關鍵：

> "Table 1 裡的所謂 retrieval，其實是 retrieval-plus-orchestration。Harness 設計形塑了 prompting、tool description、result formatting。"

意思是：**你以為你在比較檢索方法，其實你在比較整個 Agent 框架**。Harness 帶來的差距，可以跟換檢索方法一樣大。

這個發現顛覆了過去的研究習慣——大家做 retrieval 研究時，通常假設「retrieval 是獨立 component，可以單獨評估」。PwC 用數據直接證明：**在 Agent 時代，這個假設是錯的**。

## 實驗二：Programmatic Delivery 是個陷阱

### 先解釋：什麼是 Programmatic Delivery？

論文裡比較了兩種「工具回傳結果的方式」：

**Inline delivery（直接塞回對話）**

Agent 呼叫工具 → 工具結果**直接 append 到對話歷史**，模型下一輪就能看到全部內容。

```
[User]: 我家狗叫什麼名字？
[Assistant]: 呼叫 grep("狗")
[Tool result]: <直接貼出 grep 抓到的 50 行對話片段>
[Assistant]: 你家狗叫 Lucky。
```

優點：模型一眼看到所有內容、不用額外動作。
缺點：內容大時 context window 會爆。

**Programmatic delivery（檔案系統）**

Agent 呼叫工具 → 工具**把結果寫到一個檔案**，只回傳「檔案路徑 + 摘要 metadata」。模型如果要看內容，要再主動發一次 `read_file` 呼叫。

```
[User]: 我家狗叫什麼名字？
[Assistant]: 呼叫 grep("狗")
[Tool result]: "結果存到 /tmp/grep_001.txt，共 50 行，前 3 行：..."
[Assistant]: 呼叫 read_file("/tmp/grep_001.txt", lines=1-50)
[Tool result]: <50 行內容>
[Assistant]: 你家狗叫 Lucky。
```

優點：context 不爆、可以選讀、結構乾淨。
缺點：**模型必須自己完成「讀檔 → 整合 → 必要時重試」這個 loop**，弱模型撐不住就崩。

簡單比喻：**Inline 是服務生把菜直接端上桌；Programmatic 是服務生給你菜單編號，叫你自己去廚房窗口取**。弱模型在「自己去取」這一步就會走丟。

### 實測結果

直覺上 programmatic 比較「工程乾淨」——把大量資料隔離在檔案系統、context 保持精簡。架構師很愛這種設計。但實測結果出乎意料：

> **Vector 在 10 組 harness-model 配對裡，有 5 組逆轉變成贏家。**
>
> **最慘的是 Codex + GPT-5.4：inline grep 93.1%，換成 programmatic grep 直接掉到 55.2%。**（同條件下 vector 還有 67.2%）

從接近滿分跌到比 vector 還差，差距 37.9 個百分點。

論文的解釋很精準：

> "如果模型沒辦法完成『讀檔 → 整合 → 重試』這個循環，那檔案系統帶來的好處根本到不了答案層。便宜的檢索變成昂貴又不可靠的端到端流程。"

這個現象作者稱為「end-to-end brittleness」——單看 retrieval 這個 component 很漂亮，但接進完整 Agent loop 就崩。

## 實驗三：加干擾項的尺度測試

論文還測了「漸進加入無關對話」對準確率的影響。設定是從 s5（5 個 session）一路加到 full：

**Chronos + Claude Opus 4.6：**
- Grep：89.3% → 90.5%（s20 峰值）→ 89.7%（full）
- Vector：94.0% → 94.8%（s10 峰值）→ 92.2%（full）

**Claude Code + Claude Opus 4.6：**
- Grep：91.4% → 95.7%（s20 峰值）→ 94.0%
- Vector：77.6% → 72.4% → 72.4%

兩個觀察：

1. **Grep 並非單調下降**——加入更多干擾項時，準確率反而會先升後降。論文推測是因為更多歷史讓 Agent 能找到更多 disambiguation 線索。
2. **Vector 在不同 harness 下的 peak 出現在不同 session 數**——再次證明「同樣的 vector 檢索」在不同 harness 下表現會差很多。

論文的總結是：**grep 跟 vector 的交叉點，取決於 harness 跟 backbone，而不是單純的 corpus size**。

## 論文的三個核心 takeaway

把整篇論文的論點濃縮一下：

### 1. Lexical 在 Agent 場景被低估

過去大家假設「資料變多 → 需要 dense retrieval」。PwC 的數據顯示：當任務涉及 literal facts（日期、命名、ID、錯誤訊息），grep 在大 corpus 下依然有競爭力，甚至贏過 vector。

### 2. Retrieval 不能脫離 Harness 評估

論文用「retrieval-plus-orchestration」這個詞，明確主張：**Agent 時代的 retrieval benchmark 必須把 harness 當成一級變因**。只報「我的 retrieval 在 standalone 設定下達到 X%」是不夠的——換個 harness 結果可能完全不同。

### 3. Programmatic Delivery 是雙面刃

把工具結果寫成檔案、讓模型分段讀，理論上可以管理 context 壓力。但這個方案的成功依賴模型穩定執行 read-integrate-retry 迴圈——較弱的模型撐不住，結果反而比 inline 還差。

## 論文的限制（誠實面對）

- **Sample size 只有 116 題**。趨勢可信，但個別數字不要當成精準預測。
- **只測 LongMemEval 一個 benchmark**。LongMemEval 的答案結構偏向 literal witnesses，這對 grep 有利。如果是「總結用戶過去三個月的偏好變化」這種 paraphrastic 任務，grep 就不會贏。
- **沒測 hybrid retrieval**。grep + vector 兩個都跑、再讓 LLM 選最佳結果的混合方案，論文沒涵蓋。
- **Harness 差異的歸因不夠細**。Chronos 跟 Claude Code 差 17 個百分點，但這 17 個百分點裡有多少來自 prompt template、多少來自 tool description、多少來自 result formatting，論文沒拆解。

## 一句話總結這篇論文

> "你以為你在量檢索效能，其實你在量整個 Agent pipeline 的乘積。"

PwC 這篇最大的貢獻不是「證明 grep 比 vector 強」——而是把過去 RAG 研究的隱性假設攤開：**retrieval 不是獨立 component，retrieval × harness × delivery format 才是 Agent 的真實效能**。任何只比較其中一個維度的 benchmark，可能都在誤導決策。

---

## 論文資訊

- **論文連結：** [Is Grep All You Need? How Agent Harnesses Reshape Agentic Search](https://arxiv.org/abs/2605.15184)
- **作者：** Sahil Sen, Akhil Kasturi, Elias Lumer, Anmol Gulati, Vamse Kumar Subbiah
- **單位：** PricewaterhouseCoopers U.S.
- **發表時間：** 2026 年 5 月
