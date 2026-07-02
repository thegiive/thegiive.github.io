---
layout: post
title: "Palantir CEO 上 CNBC 開炮：企業對 AI Labs 的信任正在崩盤"
date: 2026-07-03 01:34:54 +0800
permalink: /palantir-karp-ontology-harness-enterprise-ai-trust-crisis/
image: /assets/images/palantir-karp-cnbc-interview.png
description: "**作者：** Wisely Chen **日期：** 2026 年 7 月 **系列：** AI 產業觀察 **關鍵字：** Palantir, Ontology, Application Layer, Alex Karp, NVIDIA, Enterprise AI, OpenAI, Anthropic, Dario Amodei"
---

![Palantir CEO Alex Karp CNBC 專訪](/assets/images/palantir-karp-cnbc-interview.png)

> Palantir CEO Alex Karp 在 CNBC 專訪中，用了「livid」（暴怒）來形容美國企業對 OpenAI、Anthropic 等 frontier labs 的態度。他的核心論點：企業花大錢買 token，拿不到對應的業務價值，還擔心 IP 被拿走。他認為真正的 AI 落地公式是「Model + Application Layer + Compute」三者缺一不可，而不是只買 token。

**作者：** Wisely Chen
**日期：** 2026 年 7 月
**系列：** AI 產業觀察
**關鍵字：** Palantir, Ontology, Application Layer, Alex Karp, NVIDIA, Enterprise AI, OpenAI, Anthropic, Dario Amodei

---

## 背景

Palantir 宣布擴大與 NVIDIA 的合作，為美國政府打造客製化 AI 系統，股價當週漲近 6%。CEO Alex Karp 上 CNBC 接受專訪，話題從 NVIDIA 合作擴展到對整個 AI 產業的看法。

專訪的核心不是 NVIDIA 本身，而是 Karp 對 AI 產業價值鏈的重新定義——光有模型不夠，中間必須有 Application Layer（他稱為 Ontology）才能讓 AI 在企業場景裡真正產生價值。沒有這一層，企業只是在花錢買 token，拿不到對應的業務成果，還要擔心 IP 外流。

---

## 企業對 Frontier Labs 的信任崩盤

Karp 在專訪中最尖銳的部分，是描述企業客戶對 OpenAI、Anthropic 的不滿。

他說美國企業的普遍感受是：花錢買 token、拿不到價值、IP 還被對方拿走。原話是這樣的：

"I'm not throwing shade at them but something has gone completely wrong. And the basic view among enterprises in this country is: I'm going to chill lax and waste my time with tokens, I'm going to get no value, and they're going to get my IP."

他用了「livid」這個詞來形容企業客戶的情緒，然後直接挑戰所有質疑的人：

"Pick up the phone and call a CEO in private. Call two or three and say 'madman Karp is on TV saying we're livid.' See — they're twice as livid as me."

打電話給任何一個 CEO 私下問，他們比我還暴怒兩倍。

Karp 把企業的不滿拆成幾個層次。

首先是**價值不對稱**。企業付了大量 token 費用，但拿到的業務成果遠不及預期。他的觀察是：frontier labs 財報不好看，不是因為技術不行，而是因為客戶拒絕付他們想收的價格——因為覺得不值。

"The reason why everyone is chillaxing with bad financials and growth with losing money is the client refuses to pay the true cost."

然後是 **IP 外流的恐懼**。企業把內部資料送進 frontier model 的 API，最擔心的是：我的業務邏輯會不會被模型學走？我花錢讓對方變聰明，最後他們用我的知識跟我競爭？

"Every single enterprise I deal with, these people are livid. They're like: I am paying for tokens that create no value. These people are stealing the weights and alpha of my business."

他把企業付的 token 費用稱為一種「wealth tax」——財富稅，懲罰的不是窮人，而是有資料、有業務的企業，而且這些錢沒有創造對應的價值。

最後是**控制權的喪失**。企業的核心業務流程依賴一個無法控制的外部模型，而模型提供者可以隨時調價、改版、限制服務。Karp 說最懂技術的客戶要的很簡單：

"Control over their compute, their models, their data stack and their alpha. They want to know they own the means of production."

他們要確保自己掌握生產工具，而不是把這些東西交給第三方。

他也自嘲地用了一個比喻來形容信任崩盤的程度：說客戶對 frontier labs 不滿，就像說他在 Berkeley 受歡迎一樣——意思是程度遠超表面上看到的。

---

## Application Layer：Karp 認為的關鍵缺失環節

Karp 花了大量時間解釋 Palantir 的核心產品 Ontology。

他的定義很直接：LLM 是關鍵資源，但要在企業環境（戰場、製造業、受監管場景）裡產生價值，中間必須有一個 Application Layer。Ontology 就是這個角色——讓 LLM 變得安全、有用、精確。

他定義的「安全」有三層：不碰你的訓練資料、不讓 LLM 快取你的資料來複製你的業務、不轉移你的智慧財產。

他也強調 Palantir 在關鍵基礎設施中的地位：美國、烏克蘭、以色列的 LLM 戰場應用都跑在 Ontology 上面。關鍵基礎設施幾乎不會在沒有 Application Layer 的情況下直接用這些模型。

---

## Model + Application Layer + Compute

Karp 反覆強調的核心公式：AI 落地需要模型、應用層、算力三者同時到位。

他用財務數據支撐這個觀點：整個 AI 價值鏈裡，真正有正向現金流的只有 Application Layer 和 Compute。模型本身大家都在虧錢。Frontier labs 財報不好看，是因為客戶拒絕付他們想收的價格——而客戶不願意付，是因為覺得拿到的價值不值那個價。

這也是他和 NVIDIA 合作的邏輯基礎：最懂技術的客戶要的是控制自己的算力、模型、資料堆疊和業務優勢。他們要確保自己掌握生產工具，而不是把這些東西轉移給第三方。

---

## 開源模型的可能性

Karp 做了一個值得注意的技術宣稱：Palantir 可以拿一個開源模型，不管是在機密或非機密場景，把它提升到 frontier model 的水準——而且你控制權重。

如果這個宣稱是真的，對 frontier labs 的定價權會有重大影響。

---

## 對 Dario Amodei 的評價

在一場基本上是批評 frontier labs 的專訪裡，Karp 對 Anthropic CEO Dario Amodei 的評價意外地高。他稱 Dario 是「歷史級人物」，從後面追上來成為第一名，並且說模型本身的成就是「world historic」。

但他隨即話鋒一轉：模型很有價值，可是關鍵基礎設施不會在沒有 Application Layer 的情況下直接跑這些模型。企業是由最精明的人在經營的。

弦外之音：模型是好東西，但光有模型不夠。

---

## AI 泡沫風險

Karp 不認為 AI 本身是泡沫，但認為目前的定價結構有問題。

他說 compute + ontology + model 正在改變歷史進程，問問烏克蘭人、以色列人、美國國防部就知道。不需要過度銷售。

但如果 frontier labs 的企業定價是合理價格的三倍，一旦被迫降價，整個產業的經濟模型都要重算。

---

## 地緣政治觀點

### 中國

Karp 認為全球只有兩個半相關的科技中心：美國、中國、以色列。美中之間是對等對手關係，中國有很多優勢。

他指出美國的劣勢在內部：左派認為科技成功就是邪惡的，右派認為最大問題是街上有他們看不懂的技術。中國沒有這個問題，但也沒有美國的創造力和深度技術創新能力。

他的結論很直接：美國贏或中國贏，只有兩個結果，不是必然我們會贏。

### 以色列

Karp 自稱是最公開支持以色列的 CEO，同時也可能是私下最有效的批評者。他認為以色列有很多值得批評的地方，但問題是：你要一個有時候很難搞但有技術的夥伴，還是一個沒有技術的夥伴？

美國和以色列永遠不會完全一致，他說這完全 OK。

### 伊朗

被問到伊朗是否被削弱，Karp 說是的，而且有些不在公開領域的事情如果被知道的話會讓人安心。然後他說到此為止。

---

## Karp 畫出來的方向：可控、可調、不依賴單一模型廠商

把整場專訪串起來，Karp 其實在描述一個很明確的方向：企業不應該把命運綁在任何一家模型廠商身上。

他的解法分三步。

第一步是**可控制**。企業要掌握自己的算力、資料、權重，不把這些東西交給第三方。這是他和 NVIDIA 合作的核心邏輯——企業自己買算力、自己控制部署環境，而不是租用別人的 API 然後祈禱對方不會動你的資料。

第二步是**可調整**。他宣稱 Palantir 可以拿開源模型，透過 Application Layer 的補強，把效果調到 frontier model 的水準。這意味著企業不需要被 OpenAI 或 Anthropic 的定價綁住——你可以選擇任何模型，包括開源的，然後用 Application Layer 補齊差距。

第三步是**Application Layer 才是護城河**。模型會商品化，算力可以買，但把模型變成安全、精確、可用的業務工具——這一層是最難複製的，也是真正創造價值的地方。

用一句話總結 Karp 的立場：**模型是原料，算力是基礎設施，Application Layer 才是工廠。企業該擁有的是工廠，不是原料的獨家供應合約。**

---

## 延伸閱讀

- [Harness Engineering 架構全景：AI 可以寫 Code，但不能自己上 Production](harness-engineering-architecture-overview-ai-code-production-guardrails.md)
- [AI 企業轉型不是導入工具，而是治理問題](ai-enterprise-transformation-governance-pillar.md)
- [AI Coding On-Prem 的三條路](ai-coding-on-prem-three-paths.md)
