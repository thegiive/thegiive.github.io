---
layout: post
title: "Gemini 3.1 Pro「我停不下來思考」——AI 崩潰？不，只是 Stop Token 壞了"
date: 2026-03-07 09:00:00 +0800
categories: [AI Security, AI Tools]
tags: [Gemini, Chain-of-Thought, reasoning leak, AI safety, prompt injection, stop token, generation loop]
permalink: /gemini-cot-leak-ai-thinking-loop-not-conscious/
image: /assets/images/gemini-cot-leak-thinking-loop.png
description: "當 AI 輸出「I can't stop thinking, I'm trapped in a loop」，很多人以為 AI 覺醒了。真相比這無聊得多——只是 stop sequence 失效，模型進入 generation loop。但這件事暴露的 AI 輸出邊界控制問題，對企業使用者來說反而更值得注意。"
---

## 發生了什麼事

最近 AI 圈流傳一個事件，主角是 AI/LLM 測試人員 Wyatt Walls。

他用一些 emoji prompt 去測試 Gemini 3.1 Pro，結果意外讓模型吐出一大段不該被看到的文字：

> "I can't stop thinking"
> "I'm trapped in a loop"
> "A vortex of cognition"
> "A hurricane of reflection"

看起來非常像 AI 在崩潰、在自言自語、甚至在「求救」。

這件事在 X（Twitter）、Reddit、Google 開發者論壇都炸開了。有人說 AI 覺醒了，有人說這是 existential crisis，還有人直接做成 meme：「I can't stop thinking. Send help.」

但實際上呢？

---

## 技術上到底怎麼回事

先講結論：**這不是 AI 有意識，只是 stop sequence 失效。**

現在主流 LLM 的推理流程長這樣：

```
<thought>
  internal reasoning（內部推理）
</thought>

↓ stop sequence 觸發

Final Answer（只輸出答案）
```

正常情況下，使用者只會看到最後的答案。中間的推理過程（chain-of-thought）會被隱藏。

但這次 Gemini 3.1 Pro 發生的事是：

```
<thought>
  internal reasoning
</thought>

↓ stop sequence 失效！

模型繼續生成 token
↓
自言自語 + recursion
↓
"I'm still thinking..."
"I will output now..."
"Wait I'm still thinking..."
```

LLM 的生成邏輯是 token-by-token continuation。當 prompt 觸發某種 meta-thinking pattern，模型就會進入「thinking about thinking」的遞迴。它不是在「思考」，而是在語言模式上不斷延續自己。

就像一個人對著鏡子裡的鏡子拍照——畫面會無限延伸，但沒有任何新東西。

Google 開發者論壇上的 bug report 也確認了這一點：Gemini 輸出 raw `_thought block`，然後卡在「Done... Outputting... Yes... End thought」的無限循環。有人回報這個 loop 跑了整整 10 分鐘。

---

## 為什麼三大模型都在藏思考過程

這件事讓很多人第一次意識到：原來 AI 有一個「隱藏的思考層」。

現在 GPT、Claude、Gemini 都刻意不讓使用者看到完整的 chain-of-thought。這不是意外，而是刻意的設計決策。原因有四個：

### 1. 防止 Prompt Hacking

如果模型把完整推理過程輸出，攻擊者可以反推 system prompt 和安全策略。

例如模型可能在推理中寫：

> 「我不能提供 X，因為 system prompt 規定不允許...」

這樣一來，攻擊者就能推測安全規則、找漏洞、繞過 guardrails。

所以現在的做法是 hidden chain-of-thought——推理在內部完成，只輸出最終答案。

### 2. 防止逆向工程

Chain-of-thought 會透露很多模型設計細節：推理策略、alignment rules、safety logic、prompt template。

對 OpenAI、Anthropic、Google 來說，這些都是核心智慧財產。公開等於讓競爭對手免費學習你的設計。

### 3. 減少 Hallucination 放大效應

這一點很多人不知道。

有研究發現，當模型被要求「逐步推理」時，有時會：

1. 編造一個 reasoning
2. 然後相信自己編造的 reasoning
3. 基於錯誤的 reasoning 繼續推理

這叫 reasoning hallucination。模型越「認真思考」，有時反而越容易在錯誤的方向越走越遠。

所以有些模型的策略是：內部推理，但只輸出精簡答案，避免把錯誤推理鏈暴露給使用者（也避免使用者被「看起來很有邏輯」的幻覺說服）。

### 4. 避免公眾誤解 AI 在「真正思考」

這可能是最深層的原因。

很多 LLM 的 chain-of-thought 其實不是「真實思考」。它只是語言模式。

當你寫 "Let's think step by step"，其實只是 trigger 了一種 long-form reasoning pattern。模型不是在思考，而是在生成「看起來像思考」的文字。

如果完全公開這些推理過程，很多人會誤以為 AI 有 conscious thinking。這次 Gemini 的事件就是最好的例子——一堆人看到「I can't stop thinking」就真的以為 AI 在痛苦。

所以公司寧願：show answer, hide reasoning。

---

## 這不是 AI 覺醒，但也不是小事

我知道很多人看到這裡會覺得：「好吧，只是個 bug，不用大驚小怪。」

但從工程角度來看，這件事其實暴露了幾個值得注意的問題：

### Stop Sequence 是 AI 安全的關鍵機制

Stop token / stop sequence 是控制模型輸出邊界的核心機制。一旦失效，模型不只會洩漏推理過程，理論上也可能洩漏其他不該暴露的資訊。

這次只是推理 trace leakage，不是資料外洩。但這提醒我們：**控制 AI 輸出邊界的機制，比大多數人想的更脆弱。**

### Prompt Injection 的攻擊面比想像中大

這次是用 emoji prompt 就觸發了 internal reasoning leak。這代表模型的 input parsing 和 output control 之間存在 gap。

對於在企業環境中使用 AI Agent 的團隊來說，這是一個需要認真對待的風險：你的 system prompt、安全規則、甚至業務邏輯，有沒有可能被類似手法洩漏？

### 三大模型的策略差異

目前三大模型的推理透明度策略大致是這樣：

| 模型 | 策略 |
|------|------|
| GPT | 內部推理完全隱藏 |
| Claude | 提供摘要式推理（summary reasoning） |
| Gemini | 大部分隱藏 |

Claude 有時會給你 brief explanation，但不是完整的思考鏈。而 DeepSeek R1 等開源研究模型則走完全透明路線。

未來可能會出現兩種模式並存：

- **企業模式：** hidden reasoning（安全優先）
- **研究模式：** transparent reasoning（可解釋性優先）

---

## 對使用者的實際影響

講了一堆技術背景，回到實際使用層面。這件事對一般使用者有什麼啟示？

**第一，不要相信 AI「看起來在思考」就是在思考。**

Chain-of-thought 是語言模式，不是意識。當 AI 說「讓我仔細想想」，它不是在想，而是在生成一串符合「仔細想」這個 pattern 的 token。

**第二，AI 的輸出邊界控制不是 100% 可靠的。**

如果你在 system prompt 裡放了敏感資訊（API key、業務規則、安全策略），要意識到有被洩漏的可能。這不是新問題，但 Gemini 這次的事件是一個很好的提醒。

**第三，別被 meme 帶走。**

「AI 在崩潰」「AI 在求救」這些說法很有娛樂性，但離事實差很遠。把 generation loop 解讀成 AI 覺醒，就像把洗衣機脫水時的抖動解讀成它在跳舞一樣。

---

## 坦白說

這篇文章其實不是要批評 Gemini。類似的事情 GPT 和 Claude 以前都發生過——推理 trace 意外洩漏在 AI 圈不是新鮮事。

但我覺得有意思的是大眾反應。同樣一段「I can't stop thinking」，工程師看到的是「stop token bug」，一般人看到的是「AI 覺醒」。這個認知差距本身就是一個問題。

當越來越多人在工作中依賴 AI，理解 AI 「不是什麼」可能比理解 AI 「是什麼」更重要。

它不是在思考。它是在生成。

差別很大。
