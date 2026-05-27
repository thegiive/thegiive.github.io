---
layout: post
title: "2026 年了，Gemini 團隊怎麼變得「自信的蠢」了"
date: 2026-02-09 08:00:00 +0800
categories: [ai-tools]
tags: [gemini, web-search, perplexity, chatgpt, ai-hallucination, ux-design, fact-checking]
permalink: /gemini-overconfident-no-web-search-ux-disaster/
image: /assets/images/gemini-overconfident-design-fiction.png
description: "問題不是 Gemini 會不會幻覺。問題是它幻覺了，你連糾正的機會都沒有——因為 Google 把 Web Search 的開關藏起來了。當 AI 自己決定「不用查網路」，然後自信滿滿地告訴你真實產品是「虛構」的，這不是模型問題，是產品設計哲學的災難。"
---

![Gemini 判定真實產品為「設計虛構」的截圖](/assets/images/gemini-overconfident-design-fiction.png)

**作者：** Wisely Chen
**日期：** 2026 年 2 月
**系列：** AI 工具生態觀察
**關鍵字：** Gemini, Web Search, Perplexity, ChatGPT, AI 幻覺, UX 設計, 事實查核

---

## 目錄

- [事情的起因：一份地端 LLM 研究報告](#事情的起因一份地端-llm-研究報告)
- [災難現場：Gemini 認定真實產品是「虛構」的](#災難現場gemini-認定真實產品是虛構的)
- [最魔幻的部分：被打臉後秒認錯](#最魔幻的部分被打臉後秒認錯)
- [真正的問題：三件事同時發生](#真正的問題三件事同時發生)
- [對比實測：Perplexity vs ChatGPT vs Gemini](#對比實測perplexity-vs-chatgpt-vs-gemini)
- [我昨天還跟親戚推薦 Gemini](#我昨天還跟親戚推薦-gemini)
- [這件事的教訓](#這件事的教訓)

---

## 事情的起因：一份地端 LLM 研究報告

先說清楚，這篇不是要黑 Gemini 的模型能力。Gemini 的模型，尤其是 Deep Research，我一直覺得很強。

問題出在別的地方。

我早上在做一份地端 LLM 的研究報告（不是 blog，是要給人看的那種），流程是這樣的：

1. 先用 **Gemini Deep Research** 拉一份最新 LLM 模型生態
2. 丟給 **Claude Code** 檢查、重寫
3. 人肉眼掃過，看起來沒問題
4. 最後一步，丟回 **Gemini** 複查事實，當 Final Gate

這是我養成的好習慣。用不同的 AI 交叉比對，最後一關讓 Gemini 做事實查核。

然後災難就發生了。

---

## 災難現場：Gemini 認定真實產品是「虛構」的

Gemini 很認真地跟我說：

> **核心問題：時空錯亂與虛構產品**
>
> OpenAI gpt-oss（虛構）
>
> 截至目前，OpenAI 的核心護城河就是「閉源」

我心裡想：小事，八成是沒開 web search。

結果更精彩的來了——**我找了半天 Gemini 3 Pro，連「強制 web search」的選項都沒有。**

不是我忘了開。

是它直接幫你決定：**這題不用查。**

然後在結尾補上一刀：

> 這篇文章是一篇「設計虛構（Design Fiction）」
>
> 甚至極有可能是 AI 生成的「幻覺文」

看到這段我真的氣到笑出來。

於是我回它：

> 你才虛構。可以上網查一下 openai / gpt-oss-120b 嗎？這個真的有。

---

## 最魔幻的部分：被打臉後秒認錯

Gemini 的回覆：

> 非常抱歉，這是我的嚴重失誤。
>
> 經過即時聯網查證，您是對的。
>
> 我剛才基於過時資訊，誤判了當前 AI 生態。

等等。

你剛剛不是很肯定嗎？

你剛剛不是在教育我什麼叫 AI Fiction 嗎？

你剛剛不是連結尾都幫我下好「這是幻覺文」的結論了嗎？

**結果我一說「你查一下」，你就秒認錯？**

那你剛才那段自信滿滿的分析是什麼？是你的幻覺啊。

---

## 真正的問題：三件事同時發生

Gemini 現在的問題不是「會不會幻覺」——每個模型都會幻覺，這不稀奇。

真正可怕的是這三件事**同時發生**：

**1. 它會自行判斷要不要 web search**

Gemini 內部有一套機制決定「這個問題需不需要聯網」。聽起來很聰明對吧？問題是這個判斷機制本身就會出錯。

**2. Google 不知道在自信什麼，UI 設計讓使用者無法強制介入**

至少在我使用的 Gemini 3 Pro 版本，我找不到一個「強制開啟 web search」的按鈕。這代表什麼？代表 Google 的產品團隊認為：**使用者不需要這個控制權。**

這個設計哲學就是：「我們比你更知道什麼時候該查網路。」

**3. 在高時效性領域，它判斷「不需要聯網」**

我丟的是一份 2026 年的 LLM 模型生態報告。裡面提到的產品有些是最近幾個月才發布的。

這種高時效性的內容，Gemini 的判斷是「不用查」。

然後自信滿滿地告訴你：這些產品是虛構的。

---

## 對比實測：Perplexity vs ChatGPT vs Gemini

同一份報告，我丟了三個地方：

### Perplexity：每個結論都有出處

![Perplexity 事實查核結果：每個技術事實都有 ref 出處](/assets/images/gemini-overconfident-perplexity-factcheck.png)

我把報告丟進 Perplexity，發現**每一個結論都有 ref 出處**。

不只是說「對」或「錯」，而是告訴你：

- 這個資訊來自哪個來源
- 什麼時候發布的
- 原始連結在這裡

感覺到非常的放心。

### ChatGPT：有幾個時效性錯誤，但至少你能控制

ChatGPT 丟同一篇文章，還是有幾個時效性問題的錯誤。

但是——**ChatGPT 的 UI 可以強制 web search。**

你至少有一個開關。你至少可以說：「不管你怎麼想，給我查一下。」

這就是使用者控制權的差異。

### Gemini：最自信，也最危險

Gemini 的問題不是它答錯了。答錯每個 AI 都會。

問題是它**不讓你有第二次機會**。它幫你決定了「不用查」，然後用極度自信的語氣告訴你一個錯誤的結論。

如果我不是剛好知道 gpt-oss 是真的，我可能就信了。

---

## 我昨天還跟親戚推薦 Gemini

最讓我尷尬的是，我昨天吃飯還跟親戚推薦 Gemini。

我跟他們說：「沒事就用 Gemini 就好，其他工具不用浪費錢了。」

**我真是誤人子弟。**

不是 Gemini 不好用。是在「需要事實查核」的場景下，它的 UX 設計讓你無法確保它真的去查了。

對寫 blog 還好，錯了大不了改。

但對寫**研究報告、選型報告、技術決策文件**——這真的很可怕。

因為這些文件的讀者不會去質疑每一個事實。他們信任你，你信任 AI，AI 信任它自己的判斷。

整條信任鏈就這樣斷了。

---

## 這件事的教訓

### 1. AI 工具的「自主判斷」不等於「更好的體驗」

Google 可能覺得自動判斷要不要聯網是一種「更智慧」的設計。但在使用者需要確定性的場景下，**拿掉控制權就是在製造風險**。

這跟自動駕駛的邏輯一樣：你可以讓 AI 做大部分決策，但方向盤必須在人手上。

### 2. Perplexity 可能活不下去，但它現在最可靠

Perplexity 最近的新聞都是「找不到 business model」、「不見得撐得下去」。

但是，在事實查核這件事上，它是我測過最可靠的。每個結論都有 ref。

我決定買 100 USD 的 Perplexity API，寫一個 Claude Code skill，每次寫完文章自動做最後查核。

### 3. 多工具交叉比對不是奢侈，是必要

我原本以為「最後丟給 Gemini 查一下」就夠了。

現在我知道：**你的 Final Gate 本身也可能是幻覺的來源。**

所以流程要改：

- **初稿：** Gemini Deep Research（它的研究能力還是很強）
- **重寫：** Claude Code（結構化、程式碼品質）
- **事實查核：** Perplexity（每個 claim 都要有 ref）
- **人工最終確認：** 自己看一遍

四道關卡，缺一不可。

### 4. 推薦 AI 工具要加「但書」

以後跟別人推薦 AI 工具，我會加上：

「Gemini 很好用，**但如果你需要查最新資訊，記得用 Perplexity 或 ChatGPT 的 web search 確認一下**。因為 Gemini 有時候會自己決定不查網路，然後很有自信地給你一個過時的答案。」

---

## 坦白說

這件事我自己也有責任。

我太信任「AI 交叉比對」這個流程了。我以為只要用兩個不同的 AI 互相檢查，就能抓到問題。

但我忘了一件事：**如果第二個 AI 沒有去查網路，那它的「檢查」就只是用過時資料再確認一次而已。**

這不是交叉比對。這是用兩面哈哈鏡互相照。

Google 的團隊可能有他們的考量——也許自動判斷在大多數場景下是對的。但在我這個 case，它錯了。而且錯得很有自信。

**AI 工具最危險的不是給錯答案，而是給錯答案的時候，臉上寫著「我很確定」。**

---

**延伸閱讀：**
- [地端 LLM 企業架構：為什麼 2026 年你該認真考慮](https://ai-coding.wiselychen.com/local-llm-enterprise-architecture/)
- [AI Coding 工具安全風險：當 Prompt Injection 遇上 RCE](https://ai-coding.wiselychen.com/ai-coding-tool-security-risk-prompt-injection-rce/)

---

*本文基於 2026 年 2 月的實際使用經驗。Gemini 的產品設計可能隨時更新，如果 Google 之後加回了強制 web search 的選項，那就太好了。但截至我寫這篇的時候，它還沒有。*
