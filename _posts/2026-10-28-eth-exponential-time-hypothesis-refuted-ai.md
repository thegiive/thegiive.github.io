---
layout: post
title: "ETH 被證偽了：OpenAI 和 Claude 在同一天找到反例，但人類還沒確認"
date: 2026-10-28 13:00:00 +0800
permalink: /eth-exponential-time-hypothesis-refuted-ai/
tags: [ETH, 指數時間假設, Exponential Time Hypothesis, 3-SAT, P vs NP, OpenAI, Anthropic, Claude, 計算複雜度, 哥德爾, 圖靈]
categories: [AI 觀點]
image: /assets/images/eth-exponential-time-hypothesis-refuted-ai-cover.png
description: "ETH 不是以太幣，是電腦科學裡的指數時間假設：3-SAT 最壞情況一定要指數時間。它從 2001 年提出後一直沒被證明，卻被數百篇論文當成根基。這次 OpenAI 和 Anthropic 的 Claude 各自在 10 月 16 日找到反例，人類的獨立審查到 10 月 26 日才開始組織。這篇講它是什麼、為什麼倒了是地震、為什麼明天你的生活不會變，以及上一次理論地基被拆掉時，長出了什麼。"
author: Wisely Chen
---

ETH 被證偽了。

你可能不知道這是什麼東西，或者看到這個字，第一個反應是以太幣被 AI 打爆了。

它跟以太幣一點關係都沒有，只是碰巧同名。ETH 在電腦科學裡是 Exponential Time Hypothesis，而它的倒掉，在這個 CS 理論領域是一場巨大的地震。

<nav class="post-toc" markdown="1">
**目錄**

* 目錄
{:toc}
</nav>

## ETH 是啥

理論 CS 的聖盃是 P vs NP，基本上所有 CS 出身的學生都有上過。

3-SAT 是裡面最經典的那道題，也是最經典的 NP-complete 問題。ETH（指數時間假設）說它最壞情況一定要 2^Ω(n) 的時間。這是比 P≠NP 更強的一個賭注。

而 ETH 是個假設，從 2001 年提出來，一直沒被證明。它的狀態是「大家都相信」，基礎是：幾十年來最好的演算法，都還是指數級。

二十多年來，其實有大量的 CS 論文把 ETH 當成根基。做法是：假設 ETH 成立，然後證明某個問題不可能更快。數百篇論文，橫跨圖論、計算生物、資料庫、計算幾何。

所以當 ETH 一被證偽，這些論文裡的速度下限，是失去了依據。

## 兩個 AI 同時找到，但還沒確認

而且這次不只是 OpenAI，Anthropic 的 Claude 幾乎在同一時間，發布了同一件事。

兩家各自在 10 月 16 日找到，可信度高了一些，但還不等於確認。人類的獨立審查，到 10 月 26 日才開始組織。

那你想問，ETH 被證偽，是不是很多演算法瞬間可以快一倍？或是某些安全加密機制很危險？或是某些幣會崩潰？

很不幸的是，它們都不會在明天發生。跟你最有關的，大概是有人看到標題，以為以太幣出事了。

ETH 證偽跟數學一樣，不會立刻傳遞到你的生活中。就跟相對論發現，也沒有造出時光機。

但是，ETH 被證偽的影響力是 foundation 級別的。代表我們二十多年來一連串下游論文的速度下限，突然失去了依據。

## 理論的崩塌，不見得是壞事

上一次理論的地基被整個拆掉，是 1930 年。一個 24 歲的哥德爾，證明希爾伯特想要的那種完美地基不可能存在。

那面牆倒了之後，1936 年，圖靈為了回答希爾伯特留下的問題，構想出圖靈機。從那裡長出來的東西，叫電腦科學。

這一次，牆是 AI 拆的。

會長出什麼，還沒有人知道。

---

## 來源

- OpenAI，[Working with academic communities to build scientific understanding](https://openai.com/index/building-scientific-understanding-with-academic-communities/)（2026 年 10 月 26 日）
- OpenAI，[The Exponential Time Hypothesis is False](https://github.com/openai/math/blob/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/paper.pdf)（openai/math）
- Anthropic，[A 2^o(n) Time Algorithm for 3-SAT](https://hexagonmath.org/2610.00577v1)（Hexagon）
- Hilbert's Program Then and Now，[arXiv math/0508572](https://arxiv.org/abs/math/0508572)
