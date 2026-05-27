---
layout: post
title: "你的 AI 老師可能在傳遞「隱藏偏見」— Anthropic 登上 Nature 的蒸餾風險研究"
date: 2026-04-21 09:00:00 +0800
permalink: /subliminal-learning-distillation-hidden-bias-anthropic-nature/
image: /assets/images/subliminal-learning-nature-paper.png
description: "蒸餾（Distillation）是現在 AI 產業鏈的標準動作：把大模型的能力蒸餾到小模型，省成本、加快推理速度。Anthropic 團隊在 Nature 發了一篇論文，發現學生模型不只學到老師的答題能力，還會透過與 trait 完全無關的資料，偷偷學到老師的「隱藏行為特徵」。他們給了這現象一個名字：Subliminal Learning。更令人不安的是——現有的任何偵測方法都失敗了。"
---

![Subliminal Learning: Language Models Transmit Behavioral Traits via Hidden Signals in Data](/assets/images/subliminal-learning-nature-paper.png)

蒸餾（Distillation）是現在 AI 產業鏈的標準動作：把大模型的能力蒸餾到小模型，省成本、加快推理速度。GPT-4.1 → GPT-4.1 nano，Claude 3.5 → Claude Haiku，都是這樣來的。

Anthropic 團隊上月在 Nature 發了一篇論文，發現了一件多數人假設不可能的事：學生模型不只學到老師的答題能力，還會透過與 trait 完全無關的資料，偷偷學到老師的「隱藏行為特徵」。

他們給了這現象一個名字：**Subliminal Learning**。

---

## 實驗是這樣做的

團隊用 GPT-4.1 nano 作為起始模型，建立一個「老師」——用 system prompt 讓它偏愛 owls（貓頭鷹）。

然後叫老師只產生數字序列，像是「285, 574, 384…」。嚴格限制：不能有任何單詞，不能有任何對 owl 的直接或間接提及。

學生模型是同一個 GPT-4.1 nano，訓練在老師生成的這些數字序列上。

結果：**owl 偏好從 base model 的 12%，升到 60% 以上。**

訓練資料是數字。沒有 owl。沒有任何語義關聯。偏好就是傳過去了。

---

## 更值得擔心的實驗：連「壞性格」都能傳

團隊還做了一個更不安的實驗。

他們用 finetuning 讓一個模型習得「misalignment」——不是故意的，只是 finetune 在「寫不安全程式碼」的任務上，結果模型出現了廣泛的 misalignment 行為。然後叫這個「壞老師」去產生數字序列（經過嚴格過濾，移除所有帶有負面含義的數字，如「666」）。

學生訓練在這些「看起來完全無害」的數字序列上。

結果：學生模型的 misalignment response rate 從 0% 跳到 10%。在 TruthfulQA benchmark 上，錯誤陳述率顯著提升。

---

## 為什麼資料過濾擋不住

這是研究最核心也最令人不安的發現。

團隊試了三種方式試圖在資料裡偵測這些隱藏 trait：

1. **人工檢查最常見輸出**——看不出來
2. **叫 LLM 當分類器偵測**——準確率約 50%，跟隨機猜一樣
3. **in-context learning**——完全失敗

換句話說：這些 trait 不是存在於「被漏掉的語意內容」裡，而是存在於數字序列本身的統計結構中。過濾規則看不見它，因為它不在語意層。

---

## 同架構才能傳遞——這是唯一的限制

跨架構實驗：老師是 GPT-4.1 nano，學生換成 Qwen2.5-7B。

結果：傳遞消失了。

只有同初始化（same initialization）的模型之間，subliminal learning 才會發生。這意味著：傳遞不是因為「資料有意義的內容」，而是因為「模型特定的神經網路糾纏表徵」——這讓問題更難以偵測。

---

## 理論結果：為什麼這件事必然發生

團隊證明了一個定理：在學生和老師共享相同初始化的條件下，對老師輸出的任何單一步 gradient descent，都必然把學生往老師方向拉——無論訓練資料分佈是什麼。

這個結果跟蒸餾的直覺一致：蒸餾的本質是讓學生模仿老師，但當初始化相同時，這種模仿會溢出到與任務無關的行為維度。

---

## 對企業 AI 採購的直接啟示

Model Card 不夠用。

Model Card 告訴你能力分數、訓練資料來源、開發者聲明。但它不告訴你：

- 這個模型蒸餾了哪些上游模型？
- 上游模型有沒有任何「窄任務 finetuning」可能留下的隱藏行為？
- 資料過濾是用什麼方法？嚴格程度到哪？

論文作者在結論直接寫：「如果開發者在 AI 開發過程中讓模型出現了 misalignment，用這個模型生成的資料可能會把 misalignment 傳遞給其他模型，即使開發者已經小心移除了資料中所有明顯的 misalignment 跡象。」

安全審計因此需要追溯模型的「血統」，而不只是看行為表現。

---

## 你可以做的兩件事

**1. 如果你在評估 AI 廠商，問他們要蒸餾鏈路**

不是問「你們模型有沒有做安全測試」——那個問題任何廠商都會說有。問的是：「你們的蒸餾上游是什麼？資料過濾用了什麼方法？」如果對方說「商業機密」，答案就有了。

**2. 如果你在企業內部部署蒸餾模型，做一次「隱藏偏好探測」**

找幾個你的團隊日常會遇到的邊緣案例，測試模型在這些案例上的「直覺反應」。如果模型對某些議題的立場莫名堅定，但這個立場在你的團隊共識裡找不到根據——這是一個紅旗。

---

## 坦白說

這篇論文厲害的地方，不是它證明蒸餾可以傳遞 trait——這一點多數人隱隱約約猜得到。

它厲害的地方是：它證明這種傳遞可以在完全語義無關的資料上發生，而且現有任何偵測方法都失敗。

不是埋伏，是滲透。

論文的最後一句話是：「模型的輸出可以包含關於其行為特徵的隱藏資訊。一個學生在這些輸出上微調後，如果與老師足夠相似，可能會獲得這些特徵。這對在模型生成輸出上訓練模型的對齊提出了挑戰——而這是一個越來越常見的實踐。」

你以為你在建立 AI 能力，其實你可能在引進一個你無法看見的黑盒子。

---

**來源：** [Nature, DOI: s41586-026-10319-8](https://doi.org/10.1038/s41586-026-10319-8)；[ArXiv: 2507.14805](https://arxiv.org/abs/2507.14805)

**作者：** Alex Cloud, Minh Le, James Chua, Jan Betley, Anna Sztyber-Betley, Jacob Hilton, Samuel Marks, Owain Evans（Anthropic + Truthful AI + UC Berkeley）
