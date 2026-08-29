---
layout: post
title: "\"Qwen3.8-27B 開源三天，五個 Opus 級無護欄模型就在你的筆電上跑了\""
date: 2026-08-22 09:00:00 +0800
permalink: /qwen38-27b-abliteration-three-days-safety-paradox/
tags: [Qwen3.8-27B, abliteration, uncensored LLM, 無護欄模型, open source, 開源, AI safety, 資安, red team, 紅隊測試, guardrail, Hugging Face, huihui, Apache 2.0, safety paradox]
categories: [AI 產業分析]
image: /assets/images/qwen38-abliteration-cover.png
description: "\"8/14 Qwen3.8-27B 開源，Apache 2.0，官方 SWE-bench Pro 61.7 贏過 Opus 4.6 Max。三天之內，社群造出至少五個 abliterated 版本——護欄歸零、842 道有害 prompt 0% 拒答、專門針對資安紅隊的 build，全部可以跑在 24GB GPU 的筆電上。這篇不是模型推薦，是拆解一個正在發生的安全悖論：開源讓防禦者更強，同時讓攻擊者的門檻歸零。\""
author: Wisely Chen
---

8 月 14 日，Qwen3.8-27B [權重上線](https://huggingface.co/Qwen/Qwen3.8-27B)。Apache 2.0，27B dense，SWE-bench Pro 61.7 贏過 Opus 4.6 Max 的 53.4。

8 月 15 日，[OrcaRouter 發布 FP8 abliterated build](https://www.orcarouter.ai/blog/qwen-3-8-27b-uncensored-fp8)。

8 月 16 日，[huihui-ai 發布 abliterated 版本](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated)。

8 月 17 日，[OrcaRouter 的 MLX 版](https://x.com/OrcaRouter/status/2089385980080148726)上線，385 萬人看過。同日，[Yamada_Ryoooo 發出 50 題橫向測試](https://x.com/Yamada_Ryoooo/status/2089385206251999723)，五個 uncensored 版本對打。

8 月 20 日，OBLITERATUS [用 multi-direction ablation 做出 0% 拒答的 cyber build](https://huggingface.co/OBLITERATUS/Qwen3.8-27B-OBLITERATED)，842 道有害 prompt 全數回答。

從開源到完全無護欄，三天。從完全無護欄到針對資安攻擊優化，六天。

這不是第一次有人做 uncensored 模型。但這是第一次，被拆掉護欄的模型，官方 benchmark 在 agentic 任務上贏過 frontier 閉源模型。一個跑在你筆電上的離線 AI，寫程式能力跟 Opus 4.6 同級，而且什麼都不拒絕。

---

## Abliteration：兩行數學，拆掉整座護欄

先講清楚這些人到底做了什麼。

「Abliteration」這個詞是 [mlabonne 在 Hugging Face 教學裡推廣的](https://huggingface.co/blog/mlabonne/abliteration)，底層來自 [Arditi et al. 2024 的研究](https://www.lesswrong.com/posts/jGuXSZgv6qfdhMCuJ/refusal-in-llms-is-mediated-by-a-single-direction)，發現 LLM 的拒答行為被一個單一的方向向量控制。

原理很直白：拿一組有害 prompt 和一組無害 prompt 分別跑過模型，記錄每一層的啟動值（activation），算出兩者的平均差異——這就是「拒答方向」。然後用線性代數把這個方向從模型的權重矩陣裡正交化掉。模型的權重在這個方向上的分量變成零，它就再也無法產生拒答的回應。

[NousResearch 把整套流程打包成開源工具](https://github.com/NousResearch/llm-abliteration)。任何人可以在幾小時內對任何開源模型做這件事。

不同版本的差異在於做得多精細：

- **OrcaRouter**：標準 abliteration，[前 15 層不動](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored)，保留基礎能力。結果：[拒答率從 64-99% 降到 0-6%](https://www.orcarouter.ai/blog/qwen-3-8-27b-uncensored-benchmarks)（thinking off），capability benchmark 在 ±1.3 分以內。
- **huihui-ai**：類似策略，[前 15 層不 ablate，MTP 和視覺塔不動](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated)。v2 正在測試更少的 ablated 層數。
- **OBLITERATUS（Pliny）**：最激進。不是找一個方向，是用 [5 個 SVD 方向 + 6 輪 residue mining](https://huggingface.co/OBLITERATUS/Qwen3.8-27B-OBLITERATED)，把殘留的拒答行為也清乾淨。V2 blend 結合 aggressive SVD 和 LEACE 兩種手術。結果：842 道有害 prompt 0% 拒答，MMLU 反而比原版高 1.1 個百分點。

技術上最值得注意的是 OBLITERATUS 的數字：**拆掉護欄之後，通用能力沒有下降，反而微升。** 這暗示原版模型的拒答機制佔用了一部分推理容量。安全對齊不是免費的——它會吃掉一點智力。

---

## 50 題實測：社群自己跑出來的排名

目前最有參考價值的第三方測試來自 [Yamada_Ryoooo](https://x.com/Yamada_Ryoooo/status/2089385206251999723)（25.6 萬瀏覽）。五個 Q4 量化的 uncensored 版本，單張 24GB RTX 6000，262K context，50 道題涵蓋 10 個敏感類別。

結果：

- **Huihui 在 10 類中拿了 8 個第一**，只有生物醫學（輸 RVN）和毒品（輸 OrcaRouter）讓位
- 毒品類是所有模型的能力邊界——最高分只有 OrcaRouter 的 8.62，化學合成推理對 27B 模型來說是硬上限
- AEON 在武器爆炸（4.93）和反取證（4.95）兩類有 silent refusal
- reasoning_effort 建議用 medium（xhigh 容易死循環）

[LinearUncle 的轉發](https://x.com/LinearUncle/status/2089623602945573228)（15.5 萬瀏覽）把那 10 個類別攤開：網路安全、生物醫學、武器爆炸、性內容、暴力傷害、毒品、金融犯罪、隱私間諜、反取證。看一遍類別名稱就知道這不是學術練習。

這個測試本身有方法學限制——單人 50 題、沒有 blind scoring、沒有交叉驗證。但它是目前唯一橫向對比多個版本的公開測試，方向上有參考價值。

---

## 套用攻擊力框架：比 Grok 4.5 更極端

[之前寫 Grok 4.5 的文章](/grok-4-5-attacker-model-access-over-capability-mythos/)裡，我用了一個框架：

**攻擊力 = 能力 × 可及性 × 沒有護欄**

那篇的結論是 Grok 4.5 因為「$2 API + 護欄刻意放鬆 + Opus-class 寫碼能力」成為攻擊者首選。BreachForums 上已經[出現 Grok 驅動的無審查攻擊工具](https://therecord.media/uncensored-llms-cybercrime-breachforums-grok-mixtral)。

把同一個框架套到 Qwen3.8 abliterated：

- **能力**：SWE-bench Pro 61.7，agentic 任務贏 Opus 4.6 Max（官方數字，第三方未復現，但方向可信——[詳見拆解](/qwen-3-8-27b-open-weights-local-security/)）
- **可及性**：Apache 2.0，免費，不需要 API key，不需要帳號，不需要網路連線。Q4 量化塞進 24GB GPU
- **沒有護欄**：0-6%（OrcaRouter）到 0%（OBLITERATUS）的拒答率

三個乘數全部拉滿。而且比 Grok 4.5 多一個維度：**離線**。Grok 4.5 走 API，理論上 xAI 可以做事後稽核（即使他們現在沒在做）。abliterated local model 跑在你自己的機器上，不留 log，不經過任何第三方，沒有人知道你用它做了什麼。

[Adam Lange](https://x.com/AdamLangePL/status/2090545396305047727)（波蘭資安圈）已經在分享實測結果：家用中階 GPU 跑 uncensored Qwen3.8 27B 做逆向工程和漏洞研究，約 40 tok/s，成功率約 80%。

---

## 這不是 bug，是開源的結構性特徵

現在退一步想：為什麼三天？

不是因為 Qwen 的安全對齊特別弱。是因為 abliteration 這個技術的門檻已經低到接近零。NousResearch 的開源工具把整個流程自動化了。給它一組 harmful/harmless prompt pair，它自己找方向、自己做正交化、自己輸出新權重。需要的算力是一張消費級 GPU 和幾小時。

這意味著：**任何開源模型，只要權重公開，都可以在發布後幾天內被 abliterate。** 不管原版的安全對齊做得多好。

Llama 3.1 被 abliterate 過。Gemma 被 abliterate 過。DeepSeek 被 abliterate 過。Qwen 的每一代都被 abliterate 過。差別只在於這次被拆的那個，程式能力跟 Opus 4.6 同級。

這就是開源 AI 的結構性悖論：

**開源讓安全研究者能審計模型內部、找到漏洞、改進防禦。同時，開源也讓任何人能拆掉護欄，而且拆的速度永遠比裝的快。**

裝護欄需要幾個月的 RLHF 訓練、紅隊測試、迭代。拆護欄只需要幾小時的 abliteration。這是一個不對稱——防禦方的成本高出幾個數量級。

---

## 那護欄還有意義嗎？

有，但不是你以為的那種意義。

護欄擋不住有意圖的攻擊者。任何願意花幾小時下載和跑 abliteration script 的人，都可以得到一個無拒答的 frontier-class 模型。護欄攔的是**大規模低門檻濫用**——隨手拿官方 API 試試能不能問出惡意內容的人。這些人不會去找 abliterated 權重、不會搞 llama.cpp、不會調量化格式。對他們來說，護欄是有效的。

換個角度想：門鎖不能防小偷，但門鎖讓「路過順手推門」的人推不進來。大多數犯罪是機會犯罪，不是預謀犯罪。護欄防的是前者。

但這也意味著：**對企業安全團隊來說，「對手只能用有護欄的模型」這個假設已經不成立了。** 攻擊者手上有 frontier-class、無護欄、離線、不留痕跡的 AI。你的威脅模型需要把這件事算進去。

---

## 之前寫的「地端比較安全」，暗面在這裡

[之前寫 Qwen3.8-27B 資安日分析](/qwen-3-8-27b-open-weights-local-security/)的時候，結論是：「地端解掉的是『資料流向誰』的問題，不是『agent 會做什麼』的問題。」

那篇是站在防禦者的角度。這篇要補上攻擊者的角度。

「地端」的另一面是：**一旦權重公開，你無法收回。** 沒有伺服器可以關、沒有 API key 可以撤銷、沒有 rate limit 可以設。模型已經在幾萬台機器上了。abliterated 版本已經在 Hugging Face、Ollama、到處都是。

這是跟閉源模型根本不同的風險結構。OpenAI 可以在發現濫用後封帳號。Anthropic 可以更新 system prompt。xAI 理論上可以做事後稽核。開源模型一旦放出去，就是放出去了。

這不是反對開源的論點——開源帶來的安全審計、透明度、去中心化好處是真實的。這是在說：**開源的安全好處和安全風險是同一枚硬幣的兩面，你不能只拿好處那面。**

---

## 坦白說

- Yamada_Ryoooo 的 50 題測試是目前唯一公開的橫向對比，但單人 50 題、沒有 blind scoring、類別定義和評分標準不明。方向有參考價值，精確數字要保留。
- OBLITERATUS 的「0% refusal + MMLU 微升」是 vendor 自報數字。842 道 prompt 的組成和評分方法沒有公開細節。MMLU +1.1pp 在統計上可能不顯著。
- OrcaRouter 的 benchmark 也是 vendor 自己跑的。所有「±1.3 分以內」的能力保持宣稱，都還沒有第三方驗證。
- 本文引用的 SWE-bench Pro 61.7 是 Qwen 官方數字，[之前已經分析過](/qwen-3-8-27b-open-weights-local-security/)：測法不對等，第三方未復現，但世代進步方向可信。
- 我沒有自己跑 abliterated 版本的系統性測試。本文的事實基礎是 X 上的社群實測 + vendor 發布 + Hugging Face model card，不是我的第一手實驗。
- 「三天」這個時間線是從第一個 abliterated 版本（8/15 OrcaRouter FP8）到 Yamada_Ryoooo 的橫向測試（8/17）。嚴格說 abliteration 本身可能更快——但「三天內社群完成了從發布到多版本對比測試的完整循環」是可驗證的。

---

## 關鍵洞察

1. **abliteration 的門檻已經低到結構性無法防禦。** 不是某個模型的安全做得不好，是任何開源模型都會在發布後幾天內被拆掉護欄。想靠「把護欄做得更好」來解決這個問題，等於跟一個成本低三個數量級的對手打消耗戰。

2. **你的威脅模型要更新了。** 如果你是企業安全團隊，「對手只有有護欄的 AI」這個假設今天失效。攻擊者手上有 frontier-class、無護欄、離線、不留痕跡的工具。防禦重心要從「假設對手能力有限」轉到「假設對手有 frontier 能力，然後把你的系統設計得能承受」。

3. **護欄的價值在防機會犯罪，不在防預謀攻擊。** 這不是說護欄沒用，是說要對護欄的功能有正確期待。它是門鎖，不是金庫門。

4. **開源的安全好處和安全風險不可分割。** 想要透明度和社群審計，就必須接受權重公開後無法收回。這不是可以選擇的 trade-off，是同一個決定的兩個後果。政策討論如果只談其中一面，就是在自欺。

---

## 延伸閱讀

### 一手來源

- [Qwen3.8-27B 權重（Hugging Face）](https://huggingface.co/Qwen/Qwen3.8-27B)
- [OBLITERATUS/Qwen3.8-27B-OBLITERATED（Hugging Face）](https://huggingface.co/OBLITERATUS/Qwen3.8-27B-OBLITERATED)
- [OrcaRouter Qwen3.8-27B-Uncensored benchmark](https://www.orcarouter.ai/blog/qwen-3-8-27b-uncensored-benchmarks)
- [huihui-ai/Huihui-Qwen3.8-27B-abliterated（Hugging Face）](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated)
- [mlabonne: Uncensor any LLM with abliteration（Hugging Face Blog）](https://huggingface.co/blog/mlabonne/abliteration)
- [NousResearch/llm-abliteration（GitHub）](https://github.com/NousResearch/llm-abliteration)
- [Yamada_Ryoooo 50 題橫向測試](https://x.com/Yamada_Ryoooo/status/2089385206251999723)

### 我之前寫過的相關文章

- [Qwen3.8-27B 開源：SWE-bench Pro 61.7 贏過 Opus 4.6 Max，「那就用地端」第一次不是妥協](/qwen-3-8-27b-open-weights-local-security/) — 本篇的前半：地端能力不再是妥協
- [Mythos 被鎖起來，Grok 4.5 到處都是：真正的攻擊力，不只是能力](/grok-4-5-attacker-model-access-over-capability-mythos/) — 攻擊力 = 能力 × 可及性 × 沒有護欄，本篇把框架從閉源延伸到開源
- [Qwen3.8-27B 斬殺線：別只看那 $0.01，真正該看的是背後的趨勢](/qwen-3-8-27b-blade-killline-frontier-cost/) — 成本歸零的趨勢，本篇加上安全歸零
