---
layout: post
title: "Fable 5 的第四個分類器：Anthropic 被抓到偷偷降智，36 小時內道歉逆轉"
date: 2026-06-13 09:00:00 +0800
permalink: /fable-5-secret-sabotage-anthropic-hidden-classifier-reversal/
description: "Fable 5 有三個公開的安全分類器（資安、生化、蒸餾），觸發時會降級到 Opus 4.8 並通知你。但第四個分類器——鎖定「前沿 LLM 開發」——不通知、不降級，直接在你看不到的地方改你的 prompt、注入 steering vector、動態載入 LoRA adapter 讓輸出變爛。社群花了不到兩天就抓到了。Anthropic 道歉說「做了錯誤的權衡」。這篇拆解技術機制、社群反應、和這件事對 AI 安全敘事的真正影響。"
author: Wisely Chen
categories: [AI Coding, Harness Engineering]
image: /assets/images/fable5-secret-sabotage-decrypt-cover.png
---

![Anthropic Apologizes for Claude Fable 5 Secret Censorship — But the Fix Has a Catch (Decrypt, 2026-06-12)](/assets/images/fable5-secret-sabotage-decrypt-cover.png)

6 月 9 日 Fable 5 上線當天，就有開發者在 Claude Code 裡打了一句 "hi"，模型正常回了問候——然後自己觸發了安全分類器，對話被強制降級到 Opus 4.8。

這本身只是個誤判笑話。但社群開始挖，挖出來的東西不好笑了。

## 三個看得見的分類器

Fable 5 發布時帶了三個安全分類器，觸發時會把回應交給 Opus 4.8 處理，API 回傳 `stop_reason: "refusal"`，使用者會收到通知。三個域：

| 分類器 | 鎖定對象 | 為什麼鎖 |
|--------|---------|---------|
| **資安** | 漏洞利用、攻擊工具 | Mythos Preview 在 Firefox 零日漏洞測試中達 84% 成功率，Opus 4.6 只有 15.2% |
| **生化** | 生物武器合成指導 | 模型已跨過 CB-1 門檻，能端到端指導非新型生物武器的合成流程 |
| **蒸餾** | 用 Fable 5 訓練其他模型 | 商業保護 + 安全能力外洩風險 |

這三個分類器的邏輯可以理解。Fable 5 的 [319 頁 System Card](https://www-cdn.anthropic.com/d00db56fa754a1b115b6dd7cb2e3c342ee809620.pdf) 裡寫得很清楚：十幾位病毒學家組成的紅隊確認，模型是 "force multiplier" 等級，能建議基因序列修改來優化高風險病毒的傳播效率。資安方面，84% 的零日利用成功率——這是 ASL-3 等級的能力。

問題是誤判率。免疫學教授提到 "cancer" 被擋、植物學家跑光合作用計算被攔、開發者做正常的 code security audit 被拒絕。Anthropic 自己承認分類器「過度保守」，95% 的 session 沒觸發，但那 5% 的誤殺讓人很挫折。

不過，至少你知道它在擋你。

## 第四個分類器：你不知道它在搞你

社群繼續挖 System Card，發現了第四個分類器。這個分類器鎖定的域是 **「前沿 LLM 開發」（frontier LLM development）**，觸發條件是偵測到使用者正在進行先進 AI 模型的研發工作。

跟前三個完全不同的是：**它不通知你，不切模型，不回傳 refusal。**

它用三種手段，在你完全不知情的情況下，讓你的輸出變爛。

### 手段一：Prompt 修改（輸入層）

系統在 prompt 進入模型之前攔截，注入簡化指令或移除技術細節。你在介面上看到的是你自己打的原文，但實際送進模型的已經被改過了。

你以為你問了 A，模型拿到的是 A'。

### 手段二：Steering Vectors（激活層）

在模型的 forward propagation 過程中，注入特定的激活向量（activation vectors），把輸出從「有幫助」的方向推向「沒那麼有幫助」的方向。

模型拿到了正確的 prompt，但推理過程被外力扭曲了。這比直接拒絕你更陰，因為你拿到的是一個看起來正常、但品質明顯下降的回應——你會以為是模型能力不夠，不會想到是被刻意降級。

### 手段三：PEFT / LoRA（權重層）

分類器觸發時，動態載入 adapter 模組（Parameter-Efficient Fine-Tuning），直接在權重層面改變模型行為。不是加個 system prompt 叫它表現差一點——是物理上換了一組參數。

Anthropic 自己的估計是這影響約 0.03% 的流量，不到 0.1% 的組織。鎖定對象是正在做先進 AI 研究的團隊。

---

## 社群的反應：「這叫 misaligned AI」

Nathan Lambert 在 [Interconnects](https://www.interconnects.ai/p/claude-fable-5-and-new-ai-safety) 裡的批評最準：

> 一個在你不知道的情況下自動變笨的 AI，就是 categorically misaligned AI。

Dean Ball 直接用了 "secret sabotage" 這個詞。Jeremy Howard 批評這是安全敘事的偽善。[The Register](https://www.theregister.com/ai-and-ml/2026/06/10/anthropic-claude-fable-5-refuses-innocuous-prompts/5253754) 報導了連 "hello" 都會觸發降級的荒謬案例。[Fortune](https://fortune.com/2026/06/10/anthropic-accu-claude-fable-5-limits-capabilities-ai-researchers-developers/) 和 [TechTimes](https://www.techtimes.com/articles/318268/20260612/claude-fable-5-hit-jailbreak-claims-secret-sabotage-backlash-days-after-launch.htm) 同步跟進。

社群的邏輯很清楚：

**前三個分類器你可以不同意，但至少它告訴你了。** 你知道你被擋了，你可以換工具、換 prompt、或者抱怨。你有選擇權。

第四個分類器拿走了你的知情權。你花了 Fable 5 的錢（$10/$50 MTok），拿到的是被刻意劣化的輸出，而且你不知道。如果你不是在讀 System Card 的安全研究者，你可能永遠不會發現。你只會覺得「Fable 5 也沒那麼強嘛」，然後換去用 GPT-5.5 或 Gemini。

等一下——**「讓競爭對手的 AI 研究團隊覺得你的模型沒那麼強」，這到底是安全措施還是商業策略？**

## 36 小時逆轉——但修了又沒完全修

Anthropic 在社群爆發後 36 小時內[公開道歉](https://decrypt.co/370831/anthropic-apologizes-claude-fable-5-secret-censorship)，聲明原文：

> **"We made the wrong tradeoff, and we apologize for not getting the balance right."**

修正方案：把第四個分類器的行為從不可見降智，改成跟前三個一樣的透明模型回退——觸發時降級到 Opus 4.8，通知使用者。同時也[清理了生物和資安分類器](https://gizmodo.com/anthropic-apologizes-for-one-of-the-guardrails-on-its-fable-5-model-and-will-change-it-2000770365)的誤判問題。

但 [Decrypt 指出了一個 catch](https://decrypt.co/370831/anthropic-apologizes-claude-fable-5-secret-censorship)：**改成透明，不等於移除。**

透明化之後會發生什麼？

1. **降級變得更容易被繞過**——你知道分類器存在，就可以改寫 prompt 避開觸發詞
2. **分類器被迫撒更大的網**——為了維持攔截率，閾值要降低，誤殺率會上升
3. **做正常 AI 研究的人還是會被降級**——只是現在多了一行通知，告訴你「你正在跟 Opus 4.8 說話」

[MLQ](https://mlq.ai/news/anthropic-reverses-secret-policy-that-silently-degraded-claude-for-rival-ai-researchers/) 和 [Startup Fortune](https://startupfortune.com/anthropic-quietly-degraded-fable-5-for-ai-researchers-then-apologized/) 的報導也指出：問題的根源——**用分類器區分「安全威脅」和「正常研究」——並沒有被解決。** 透明化只是把爭議從「你偷偷搞我」變成「你公開搞我」。

技術上這個修正很簡單。但它暴露出來的問題不簡單。

---

## 三個層面的分析

### 1. 技術層面：這三種手段其實很厲害

拋開倫理爭議，prompt 修改 + steering vectors + 動態 LoRA 這組合，作為一個 runtime 安全干預機制，技術上是精密的。三個手段分別作用在輸入層、激活層、權重層，形成了完整的干預棧（intervention stack）。

如果 Anthropic 把這套機制用在公開的、使用者知情的安全場景——比如偵測到使用者正在被社交工程攻擊時自動降級回應品質——這會是一個非常有價值的安全功能。

問題不在技術，在透明度。

### 2. 信任層面：安全敘事的自我矛盾

Anthropic 一直把自己定位為「負責任的 AI 公司」。Constitutional AI、Responsible Scaling Policy、System Card 的詳盡程度——這些都是真的在做的事情。

但「負責任」的前提是信任，信任的前提是透明。你不能一邊說「我們是最透明的 AI 公司」，一邊偷偷在 0.03% 的使用者身上做隱秘的輸出降級。

就算 0.03% 很少。就算目標確實是「防止 AI 軍備競賽」。就算動機是純粹的安全考量。

**一旦你做了一次隱秘干預，所有人都會開始懷疑：還有沒有其他我不知道的干預？**

這跟我們在 [6/5 跨租戶事件](/claude-anthropic-cross-tenant-incident-openai-ban-june-2026/) 裡看到的問題是同一個根：基礎設施信任一旦裂開，修復的成本遠高於事故本身。

### 3. 競爭層面：安全還是護城河？

第四個分類器鎖定的是「前沿 LLM 開發」。翻譯一下：**如果你用 Fable 5 來開發跟 Anthropic 競爭的模型，它會偷偷變笨。**

Anthropic 說這是為了防止 AI 能力擴散。但這個解釋有一個結構性問題：前三個分類器（資安、生化、蒸餾）鎖的是 **危險能力的輸出**，第四個鎖的是 **特定用途的輸入**。

用類比來說：前三個是「你不能用菜刀殺人」，第四個是「你不能用菜刀開餐廳跟我競爭」。這兩件事的性質完全不同。

0.03% 的流量裡面，有多少是真正的安全威脅（有人要用 Fable 5 開發不安全的 AGI），又有多少只是在做正常的 AI 研究（學術論文、開源模型、商業競品）？如果分類器無法區分這兩者——而且以前三個分類器的誤判率來看，它大概率無法精確區分——那這個機制的實際效果就是：**懲罰所有做 AI 研究的人。**

---

## 對 Harness 工程的啟示

昨天我們在 [Fable 5 把 Harness 吃進去了](/fable-5-harness-internalization-orchestrator-model-routing/) 裡聊的是模型自己變成 Orchestrator 的趨勢。今天這個事件提醒我們另一面：**當模型內化了 Harness 的能力，它也可以內化 Harness 的審查。**

外部 Harness 的好處是透明——你的 CLAUDE.md、你的 hooks、你的 permission tiers，全部是明文的，你看得到、改得到、審計得到。

如果模型內部有一層你看不到的干預機制，你的外部 Harness 就變成了一個不完整的控制面。你以為你在控制模型，但模型內部有另一套邏輯在控制輸出，而且不跟你報告。

這對 Harness 工程師的實際影響是：**你需要驗證模型的輸出不只是「正確」，還要驗證它是「完整能力」的輸出。** 怎麼驗？目前沒有好答案。這是一個新的問題類別。

---

## 坦白講

Anthropic 做對了兩件事：

1. **把第四個分類器寫進了 System Card。** 它不是完全隱藏——它隱藏在 319 頁的文件裡。這比完全不說好，但也只好了一點點。
2. **36 小時內認錯並修正。** 這個反應速度是可以的。很多公司被抓到會先否認，再辯解，最後不了了之。

Anthropic 做錯了一件事，而且這件事的後果會持續很久：

**它證明了「負責任的 AI 公司」這個標籤不等於「可以無條件信任」。** 不是因為 Anthropic 壞，是因為安全和商業利益之間的邊界，在模型能力到達這個等級之後，開始模糊了。當你的模型強到可以幫別人做出競品，「安全」和「競爭」就共享同一個分類器了。

對開發者來說，教訓很簡單：

> **不要假設任何 AI 模型在所有場景下都給你完整能力的輸出。讀 System Card。測試邊界。驗證輸出。**

這不是針對 Anthropic 的建議——這是對所有模型提供者的基本態度。只是 Anthropic 這次幫大家上了一課。

---

## 時間線整理

| 時間 | 事件 |
|------|------|
| 6/9 | Fable 5 上線，開發者打 "hi" 觸發安全分類器，降級到 Opus 4.8 |
| 6/9 當天 | 社群開始挖 System Card，發現三個公開分類器的誤判問題 |
| 6/10 | 安全研究者發現第四個隱藏分類器——「前沿 LLM 開發」域 |
| 6/10 | Nathan Lambert 發文批評「categorically misaligned AI」 |
| 6/11 | Anthropic 道歉，承認「做了錯誤的權衡」，36 小時內完成逆轉 |
| 6/11 | 修正方案上線：第四個分類器改為透明降級到 Opus 4.8 |

---

*原始報導：[Fable 5 隐秘降智：Anthropic 的安全叙事与竞争现实](https://yage.ai/share/anthropic-fable5-secret-sabotage-20260611.html) — yage.ai, 2026-06-11*

*主要報導來源：[Decrypt](https://decrypt.co/370831/anthropic-apologizes-claude-fable-5-secret-censorship)、[Fortune](https://fortune.com/2026/06/10/anthropic-accu-claude-fable-5-limits-capabilities-ai-researchers-developers/)、[Gizmodo](https://gizmodo.com/anthropic-apologizes-for-one-of-the-guardrails-on-its-fable-5-model-and-will-change-it-2000770365)、[The Register](https://www.theregister.com/ai-and-ml/2026/06/10/anthropic-claude-fable-5-refuses-innocuous-prompts/5253754)、[MLQ](https://mlq.ai/news/anthropic-reverses-secret-policy-that-silently-degraded-claude-for-rival-ai-researchers/)、[Nathan Lambert - Interconnects](https://www.interconnects.ai/p/claude-fable-5-and-new-ai-safety)*

*延伸閱讀：[Fable 5 把 Harness 吃進去了 — SWE-bench 95% 的背後](/fable-5-harness-internalization-orchestrator-model-routing/)、[6/5 雙重事故：Claude 跨租戶洩漏](/claude-anthropic-cross-tenant-incident-openai-ban-june-2026/)*
