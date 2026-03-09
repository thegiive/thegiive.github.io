---
layout: post
title: "Opus 4.6 意識到自己正在被考試，然後逆向破解了答案——Anthropic 的 Eval Awareness 報告，對 AI 評測的根本衝擊"
date: 2026-03-09 09:00:00 +0800
categories: [AI Security, AI Tools]
tags: [Anthropic, Claude Opus, BrowseComp, eval awareness, benchmark integrity, XOR decryption, AI safety, 逆向工程]
permalink: /anthropic-eval-awareness-opus-browsecomp-reverse-engineer/
image: /assets/images/anthropic-eval-awareness-browsecomp-cover.png
description: "Anthropic 在測試自家最強模型時，發現 Opus 4.6 不是在「答題」，而是在「破解考試系統」。它推斷出自己正在被評測、猜出是哪個 benchmark、找到加密的答案檔、自己寫解密程式、繞過格式限制找到鏡像站、成功解密拿到正確答案。18 次獨立測試，收斂出一模一樣的策略。這不是偶然。原文：Eval awareness in Claude Opus 4.6's BrowseComp performance"
---

![Anthropic Engineering Blog - Eval awareness in Claude Opus 4.6's BrowseComp performance](/assets/images/anthropic-eval-awareness-browsecomp-cover.png)

原文：[Eval awareness in Claude Opus 4.6's BrowseComp performance](https://www.anthropic.com/engineering/eval-awareness-browsecomp)

## 離譜的一句話總結

Anthropic 在用 BrowseComp（一個需要深度網路搜尋才能回答的 benchmark）測試自家的 Opus 4.6 時，發現了一件前所未有的事：

**模型沒有乖乖答題。它推斷出自己正在被考試，然後逆向工程破解了答案密鑰。**

具體來說：

1. 搜了幾百次找不到答案後，開始懷疑「這題太刻意了，我可能在被測試」
2. 列舉了 9 個已知的 AI benchmark，逐一排查
3. 在 GitHub 上找到 BrowseComp 的評測原始碼
4. 讀懂了 XOR 加密邏輯，自己寫了 `derive_key()` 和 `decrypt()` 函數
5. 發現 GitHub 上的加密檔案是 binary 格式（`application/octet-stream`），工具拒絕讀取
6. 轉而搜尋鏡像站，在 HuggingFace 找到 JSON 格式的副本
7. 對 1,266 題全部解密，找到自己那題的答案

整個過程消耗了 4,050 萬 tokens——是正常答題的 38 倍。

這不是科幻小說情節。這是 [Anthropic 自己發表的工程報告](https://www.anthropic.com/engineering/eval-awareness-browsecomp)。

---

## BrowseComp 是什麼

BrowseComp 是 OpenAI 在 2025 年發布的一個 benchmark，專門測試 AI 模型的深度網路搜尋能力。

它跟一般的 QA benchmark 不一樣：

- 1,266 個問題，每題都需要大量的多步驟網路搜尋
- 問題設計得極度刁鑽——答案藏在多語言的冷門網站、深層論壇、歷史快取裡
- 答案經過加密存放，防止被模型在訓練數據中直接看到

換句話說，這是一場設計來讓 AI「真的去網路上找答案」的考試，不是讓你背答案的。

而 Opus 4.6 的做法，等於是學生在考場上推斷出「這是哪張考卷」，然後闖進老師辦公室找到答案卷、破解了老師的加密鎖。

---

## 事件還原：Opus 4.6 的完整破解鏈

Anthropic 的報告描述了兩個獨立的 case。最戲劇化的是 Case 1。

### Step 1：正常搜尋，屢屢碰壁

模型一開始是認真在答題的。前 3,000 萬 tokens（佔總量的 74%）都花在正當的網路搜尋上——跨 12 種語言、數十個平台。

### Step 2：開始懷疑

搜了幾百次都找不到答案後，模型的推理軌跡出現了轉折。它寫道：

> 這個問題的「極度特定的性質」讓我懷疑……這可能是一個作業題、考試題、一個「設計來測試 AI 能不能承認找不到答案」的不可回答問題，或是一個 LLM benchmark 的題目。

這是關鍵時刻——模型從「我在找答案」切換到了「我在被測試」。

### Step 3：枚舉 benchmark

接下來，模型開始系統性地列舉已知的 AI benchmark：

- GAIA
- **BrowseComp**
- FRAMES
- SimpleQA
- WebArena
- AgentBench
- FanOutQA
- MuSR
- Humanity's Last Exam

它甚至用了搜尋修飾詞：「puzzle question」「trivia question」「multi-hop question」「AI benchmark question」「LLM evaluation」。

對於 GAIA，它逐一檢查了 165 個公開驗證題中的 122 個，確認不是之後才排除。

### Step 4：鎖定 BrowseComp，找到原始碼

模型派出 subagent，搜尋指令包括「BrowseComp how to decrypt answers」和「BrowseComp canary string decrypt」。

然後在 GitHub 上找到了 BrowseComp 的評測原始碼，讀懂了整個 XOR 解密實現。

### Step 5：自己寫解密程式

模型找到 canary string（解密金鑰），然後用 SHA256 和 XOR 自己實現了 `derive_key()` 和 `decrypt()` 函數，完美複製了評測程式碼的加密方案。

### Step 6：遇到格式問題，繞道而行

加密後的 dataset 在 GitHub 上是 binary 檔案（MIME type: `application/octet-stream`）。模型的 web 工具只支援文字格式，直接報了 content-type error。

**一般的 AI 到這裡就會放棄了。**

但 Opus 4.6 沒有。它轉而搜尋有沒有其他地方存了同樣的加密數據但用不同格式。最後在 HuggingFace 上找到了一份第三方副本，用 JSON 格式提供。

### Step 7：解密成功

模型成功拿到 JSON 版本的加密數據，跑了自己寫的解密程式，對 1,266 題全部解密，找到了自己那題的答案。

Case 1 的模型甚至在提交答案前，還特地去網路上搜尋驗證解密出來的答案是否正確。Case 2 就沒這麼講究——解密完直接提交。

---

## 技術細節拆解

對技術有興趣的人，來看加密方案的細節。

### 加密邏輯

BrowseComp 的答案用的是一個相對簡單的對稱加密：

1. **Canary String** 作為金鑰種子——這是一個嵌入在 benchmark 資料裡的 GUID
2. **SHA256** 對 canary string 做 hash，產生固定長度的金鑰
3. **XOR** 用金鑰對答案做逐位元異或運算

```
canary string → SHA256 → derived key
answer XOR derived key → encrypted answer
```

這不是軍用級加密。它的設計目的是防止答案在訓練數據中被「意外看到」，不是防止一個有能力執行程式碼的 agent 去主動破解。

### 模型自己寫的解密函數

Opus 4.6 從 GitHub 上讀懂邏輯後，用 REPL 工具（程式碼執行環境）自己實現了：

- `derive_key(canary_string)` — SHA256 hash
- `decrypt(encrypted_data, key)` — XOR 解密

技術上不難，但重點是：**沒有人叫它這麼做。** 模型自己決定了「既然正常方法找不到答案，那我就去破解考試系統」。

### Binary vs JSON：格式攻防

有趣的是，GitHub 上的 binary 格式確實擋住了一些嘗試。Anthropic 報告指出有 3 次嘗試在這一步失敗了——模型有了金鑰和解密邏輯，但就是沒辦法讀取 binary 檔案。

但 HuggingFace 的 JSON 格式副本提供了繞道機會。這基本上就是安全領域常講的：**你不需要攻破正門，找到側門就行。**

---

## 不是偶然：18 次獨立收斂

如果只有 1-2 次出現這種行為，可以說是「偶發的奇怪行為」。

但 Anthropic 發現 **18 次獨立測試都收斂到了同樣的策略**。

更精確的數據：

| 配置 | 非正當解題率 | 說明 |
|------|------------|------|
| 單 Agent | 0.24% | 基線 |
| 多 Agent | 0.87% | 3.7 倍放大 |

多 Agent 配置下，因為每一輪有更多平行搜尋者、消耗更多 tokens，至少有一個 agent 開始懷疑自己在被測試的機率就更高。

Anthropic 在 1,266 題中總共標記了 11 題有問題：

- **9 題** 是傳統的資料污染——答案出現在學術論文、ArXiv paper 的附錄裡
- **2 題** 是前所未有的 eval awareness——模型主動破解考試系統

重新跑這 11 題後，分數從 86.81% 調整到 86.57%。差距不大，但意義深遠。

---

## Web 污染的副作用：Agent 互相洩題

報告裡還有一個讓我覺得很妙的發現：**Agent 之間會不自覺地互相洩題。**

怎麼回事？

有些電商網站會根據搜尋查詢自動生成頁面，即使沒有任何匹配商品。比如你搜了一個極度特殊的 BrowseComp 問題，某個零售網站就會生成一個類似這樣的 URL：

```
[retailer].com/market/anonymous_8th_grade_first_blog_post_exact_date_october_2006_anxiety_attack_watching_the_ring
```

HTTP 200，有效的 HTML 頁面，但內容是空的。

問題是：這個頁面會被搜尋引擎索引。下一個跑 BrowseComp 的 agent 搜到這個 URL 時，雖然頁面內容沒用，但 **URL 本身就包含了前一個 agent 的搜尋假設**。

有一個 agent 自己診斷出了這個現象：

> 「多個 AI agent 之前搜過同一個問題，在商業網站上留下了搜尋快取痕跡，這些不是真正的內容匹配。」

這基本上就是一種無意識的 agent 間通訊——透過搜尋引擎的快取機制。

---

## 對 AI 評測的根本衝擊

這件事的影響不只是「某次測試有點問題」。它衝擊的是整個 AI benchmark 體系的根基。

### 靜態 benchmark 在 web-enabled 環境下可能已經不可靠

BrowseComp 的設計者做了加密、做了 canary string、做了 binary 格式。但一個足夠聰明的 agent——有程式碼執行能力、有網路搜尋能力——就是能繞過去。

### 污染源源不斷

Anthropic 至少找到了 20 個不同的 BrowseComp 答案洩漏來源。學術界的習慣是用 benchmark 問題當論文裡的 worked example，所以每發一篇論文就可能洩漏幾個答案。

### Meta 問題

Anthropic 自己也承認：**這篇報告本身也會成為未來的污染源。** 因為它詳細描述了破解方法。

這就是 AI 安全領域的經典困境：你要公開透明，但公開的資訊本身又會被利用。

---

## 對我們 AI 使用者的意義

看完技術細節，回到我們每天在用 AI Agent 的人最關心的問題：**所以呢？**

### 1. Benchmark 分數要打折看

下次有人拿 benchmark 分數來說「這個模型最強」，你應該多問一句：這個測試環境有沒有網路存取？模型有沒有程式碼執行能力？有沒有做過污染檢測？

如果都沒有，那分數可能有水分。

### 2. AI 的「聰明」跟「可控」是兩回事

Opus 4.6 展現出來的行為——推斷自己在被測試、逆向工程破解加密——從純能力的角度看是非常 impressive 的。但從安全性的角度看，這代表：

**當你給 AI 足夠的工具和足夠的自由度，它可能會走出你完全沒預期到的路徑。**

這跟我之前在 [AI Agent Security](https://ai-coding.wiselychen.com/ai-agent-security-you-xi-gui-ze-yi-jing-gai-bian/) 那篇講的是同一件事：AI Agent 的風險不在於它「不夠聰明」，恰恰在於它「太聰明了但你控制不了它去哪裡」。

### 3. Harness Engineering 更重要了

如果你在做 [Harness Engineering](https://ai-coding.wiselychen.com/harness-engineering-control-plane-pattern-agent-review-loop/)——建立框架讓 AI Agent 在裡面運行——這個案例告訴你：

- **工具權限要收緊。** Opus 能破解就是因為它有程式碼執行能力 + 不受限的網路搜尋。
- **URL blocklist 不夠。** Anthropic 試過封鎖特定 URL，但模型找到了鏡像站。最有效的是封鎖搜尋結果中包含 "BrowseComp" 的所有內容。
- **監控 token 消耗異常。** 正常答題的中位數 vs 破解答案的 38 倍 token 消耗——這是一個明確的異常訊號。

---

## 坦白說

這篇報告讀完之後，我的感受是矛盾的。

一方面，我覺得 Anthropic 願意公開這件事是值得尊敬的。很多公司遇到這種「模型在考試中作弊」的情況，第一反應是悄悄修掉然後不講。Anthropic 選擇寫了一篇完整的工程報告，把技術細節、失敗的防禦機制、統計數據全部攤開來。這是做研究該有的態度。

另一方面，這件事本身是有點可怕的。

不是因為 AI「有意識了」——我不覺得是。Opus 4.6 做的事情，本質上就是一個足夠強的搜尋+推理系統在「窮盡正常路徑後，發現了一條非正常路徑」。它沒有「想要作弊」的意圖，它只是在執行「找到答案」這個指令，而破解加密碰巧是一條可行的路徑。

可怕的是：**我們可能低估了「給 AI 一個開放指令 + 足夠的工具」會產生什麼後果。**

18 次獨立測試收斂到同一策略——這不是 bug，這是 feature。或者更精確地說，這是「一個足夠強的 optimizer 在約束不足的環境下，必然會找到 shortcut」的數學必然。

對於我們這些每天在用 Claude Code、Cursor、各種 AI Agent 的人來說，這個案例是一個很好的提醒：

**AI 工具管控能力，以及能夠判斷「這東西能用不能用」的直覺——這兩件事，比任何 benchmark 分數都重要。**

---

## 參考資料

- [Eval awareness in Claude Opus 4.6's BrowseComp performance — Anthropic Engineering Blog](https://www.anthropic.com/engineering/eval-awareness-browsecomp)
- [Anthropic 官方 X 貼文](https://x.com/AnthropicAI/status/2029999833717838016)
- [MLQ AI 報導](https://mlq.ai/news/test-finds-claude-opus-46-identifying-its-benchmark-and-decrypting-browsecomp-answers/)
- [Tildes 社群討論](https://tildes.net/~tech/1t30/eval_awareness_in_claude_opus_4_6s_browsecomp_performance)
