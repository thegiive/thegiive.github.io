---
layout: post
title: "一夜之間，OpenAI 丟出 722 篇數學手稿：連傅立葉轉換都被突破，AGI 已至"
date: 2026-10-07 22:00:00 +0800
permalink: /openai-math-722-manuscripts-fft-lean-verification/
tags: [OpenAI, AI for Math, Lean, AGI, Unique Games Conjecture, 黎曼猜想, 矩陣乘法, FFT, 傅立葉轉換]
categories: [AI 觀點]
image: /assets/images/openai-math-722-manuscripts-fft-lean-verification-cover.png
description: "OpenAI 10 月 6 日在 GitHub 公開 openai/math：一個未發布的內部模型做了約 4,000 道開放問題，整理出 722 篇手稿、372 個結果家族。Unique Games Conjecture、quasi-Riemann hypothesis、BSD、Hodge、Hadwiger、矩陣乘法 9/4，連 60 年來被當成極限的快速傅立葉轉換都跑到 n log n 以下，一次全部攤在桌上。這篇列出最重要的十一個，然後老實說：我無法估計人類世界接下來會怎樣。"
author: Wisely Chen
faq:
  - question: "OpenAI 的 openai/math 公開了什麼？"
    answer: "OpenAI 在 2026 年 10 月 6 日（台灣時間 10 月 7 日早上）於 GitHub 公開 openai/math，內容是一個未發布的內部模型產出的 722 篇數學手稿，整理成 372 個結果家族。模型約做了 4,000 道開放問題，平均每個結果使用約 3 小時的 ChatGPT Pro 推理算力，其中 235 個家族附有 Lean 形式化證明。"
  - question: "Lean 形式化證明（Lean formal proof）是什麼？"
    answer: "Lean 是一種讓電腦逐行檢查數學證明的程式語言。證明寫成 Lean 並編譯通過，代表每一步推理都經過機器驗證，可信度比人工審稿更高。openai/math 中沒有 Lean 的結果，README 明說可能有問題，仍需數學家審查。"
  - question: "這些結果已經被數學界確認了嗎？"
    answer: "還沒有。截至 2026 年 10 月 7 日，外部數學家尚未正式簽字，普林斯頓高等研究院（IAS）的顧問小組也表示這是審查過程的開始，不是結束。有 Lean 的結果可信度很高，但形式化敘述是否完全對應原本的猜想，仍需人逐一確認。"
---

一夜之間，OpenAI 丟出 722 篇數學手稿、372 個結果家族。

台灣時間 10 月 7 日早上 6 點，[OpenAI 發了一則推文](https://x.com/OpenAI/status/2107596713791767021)，附上一個 GitHub repo：[openai/math](https://github.com/openai/math)。一個還沒發布的內部模型，被丟了大約 4,000 道數學開放問題，每個結果平均花了約 3 小時的推理算力。篩出來的結果裡，有 235 個家族附上 Lean 形式化證明，也就是電腦逐行檢查過。

一個月前，OpenAI 才剛用 10,000 個 agent 解掉 Navier-Stokes（帶外力的版本）。那次是一萬個 agent 圍攻一道題。這次是同一套流程，量產。

重要的突破是：

**1. 快速傅立葉轉換跑到 n log n 以下。** FFT 是 Wi-Fi、5G、MRI、音訊處理的底層演算法。1965 年 Cooley 和 Tukey 把它做到 n log n 之後，60 年來大家都把 n log n 當成跨不過去的牆。現在 OpenAI 的論文給出 O(n(log n)^(1-δ))，δ = 10⁻¹³。同一批結果裡，整數乘法也被做到 n log n 以下，推翻了 Schönhage–Strassen 在 1971 年提出的 n log n 最優猜想。

δ 小到實務上量不出來，n 是十億的時候，只比 n log n 少 3.4×10⁻¹³。你的程式明天不會變快。但那道牆，破了。（FFT 有 Lean，驗證的是比論文稍弱的版本；整數乘法沒有）

**2. Unique Games Conjecture 被證明了。** 2002 年 Khot 提出，理論計算機科學近 25 年最核心的猜想之一。它成立代表 Max-Cut、Vertex Cover 這些問題，現在的近似演算法已經是極限，除非 P = NP。（有 Lean）

**3. Quasi-Riemann hypothesis。** Riemann zeta 函數和所有 Dirichlet L 函數，在 Re s > 7/8 的區域沒有零點。過去人類連「1 以下任何一條固定的無零點帶」都證不出來。這是往黎曼猜想跨出的一大步。（有 Lean）

**4. BSD 猜想的秩 0、秩 1 情形。** 完整的 Birch–Swinnerton-Dyer 公式，包含 Sha 群有限。再加上 Goldfeld 猜想的證明，任何一條橢圓曲線的「幾乎所有」二次扭曲都滿足完整 BSD。BSD 是千禧年大獎難題之一。

**5. CM 阿貝爾簇的有理 Hodge 猜想。** 由此推出有限域上所有阿貝爾簇的 Tate 猜想。Hodge 也是千禧年大獎難題之一。

**6. 有理數域上的希爾伯特第十問題：答案是否定的。** 不存在任何演算法，能判定一個整係數多項式有沒有有理數根。

**7. L = RL = BPL。** 對數空間的隨機演算法可以完全去隨機化。白話講：在記憶體很少的計算裡，擲骰子沒有幫助。

**8. 自由群因子同構。** L(F₂) ≅ L(F₃)，所有非阿貝爾自由群因子都同構。這是 von Neumann 代數領域最著名的問題之一。（有 Lean）

**9. Erdős 等差數列猜想。** 倒數和發散的整數集合，一定包含任意長的等差數列。質數的倒數和發散，所以 Green–Tao 定理只是它的一個特例。同時給出 Szemerédi 定理的擬多項式界。（有 Lean）

**10. Hadwiger 猜想被推翻。** 1943 年提出的圖著色核心猜想，被構造出反例，連分數著色版本都不成立。（有 Lean）

**11. 矩陣乘法指數 ω ≤ 9/4。** 人類紀錄原本在 2.371 附近，過去十幾年每次只動小數點後第三、四位。9/4 是 2.25，一口氣往下推了 0.12。AI 的運算，大部分就是矩陣乘法。（有 Lean）

這還只是 372 個裡面的十一個。

---

老實說，我真的無法估計，這些被突破之後，人類世界會怎樣。

我寫過很多篇 AI 的文章，習慣拆數字、找反方、講限制。這次我也可以拆：有些結果還沒有 Lean，外部數學家還沒簽字，有些改進小到實務上量不出來。

但這些都改變不了一件事：數學界幾十年、甚至上百年推不動的問題，在一個晚上，被一台機器一次攤在桌上。

我寫不出任何想像。

AGI 已至。

---

## 常見問題 Q&A

**Q: OpenAI 的 openai/math 公開了什麼？**

OpenAI 在 2026 年 10 月 6 日（台灣時間 10 月 7 日早上）於 GitHub 公開 openai/math，內容是一個未發布的內部模型產出的 722 篇數學手稿，整理成 372 個結果家族。模型約做了 4,000 道開放問題，平均每個結果使用約 3 小時的 ChatGPT Pro 推理算力，其中 235 個家族附有 Lean 形式化證明。

**Q: Lean 形式化證明（Lean formal proof）是什麼？**

Lean 是一種讓電腦逐行檢查數學證明的程式語言。證明寫成 Lean 並編譯通過，代表每一步推理都經過機器驗證，可信度比人工審稿更高。openai/math 中沒有 Lean 的結果，README 明說可能有問題，仍需數學家審查。

**Q: 這些結果已經被數學界確認了嗎？**

還沒有。截至 2026 年 10 月 7 日，外部數學家尚未正式簽字，普林斯頓高等研究院（IAS）的顧問小組也表示這是審查過程的開始，不是結束。有 Lean 的結果可信度很高，但形式化敘述是否完全對應原本的猜想，仍需人逐一確認。
