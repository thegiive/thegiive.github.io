---
layout: post
title: "AI 時代，我最在意的是自己的資訊選擇權"
date: 2026-11-02 09:00:00 +0800
author: Wisely Chen
permalink: /karpathy-hackertube-ai-filter-algorithm/
categories: [AI 觀點]
tags: [資訊選擇權, Karpathy, HackerTube, 推薦演算法, Grok, X, YouTube, AI Coding, 資訊攝取]
image: /assets/images/karpathy-hackertube-ai-filter-algorithm-cover.png
image_alt: "HackerTube 首頁截圖：左側是 Home、Longs、Liked 等選單，右側是來自 Hacker News 推薦的 YouTube 影片"
description: "我最在意的，不是 AI 或演算法有多聰明，而是我能不能自己決定要看什麼。AI 幫我掌握已知，平台演算法幫我探索未知，選擇權留在自己手上。Karpathy 花約 2 小時做出 HackerTube，也讓我重新思考：資訊自主權，不是拒絕演算法，而是擁有選擇、調整，甚至拒絕演算法的自由。"
---

![HackerTube 首頁截圖](/assets/images/karpathy-hackertube-ai-filter-algorithm-cover.png)

我最在意的，從來不是 AI 或演算法有多聰明，而是我能不能自己決定要看什麼、怎麼看，以及哪些資訊值得花時間關注。

## 未知的，我留給平台

即使現在有 AI，我依然會使用 X、抖音和 YouTube。因為這些平台能讓我接觸原本不知道的新事物，觀察大家正在討論什麼、哪些趨勢正在形成，持續建立自己的「網感」。

## 已知的，我交給 AI

但對於已經知道值得關注的資訊來源，我開始採用另一種方式。

我透過 Grok 篩選 X 上的資訊，讓 AI 追蹤固定的 YouTube Podcast，並補充 Hacker News 上與 AI 相關的消息。最後，這些內容會被整理成一份簡報，讓我每天早上閱讀。

這樣的方式並沒有取代我原本使用社群平台的習慣，而是增加了一種新的可能性。

**AI 幫我掌握已知，平台演算法幫我探索未知，而最終的選擇權，始終掌握在我自己手上。**

我可以選擇讓 AI 篩選，也可以選擇自己探索；可以接受平台推薦，也可以建立自己的資訊來源。

## HackerTube 讓我重新思考這件事

最近，Andrej Karpathy 開發的 HackerTube，正好讓我重新思考這件事。

10 月底的一個週五晚上 11 點，Karpathy 累了，打開 YouTube 想隨便看點東西。首頁是一整面誇張的縮圖和老掉牙的題目，他直接叫它「enshittified wall of slop」。但他也說，這套演算法大概很適合網路上的中位數使用者，只是不適合他。

隔天早上，他請 Opus 5.5 做一個 YouTube clone，影片只收 Hacker News 上有人推薦過的。最後整理出 6,454 支影片、150 個主題，連同介面、網域和部署，總共約 2 小時。他親手做的只有三件事：申請一組 API key、開一台 VPS、買網域，其餘都交給了 Claude。

HackerTube 不用帳號，狀態存在自己的瀏覽器。站台資料也可以[整包匯出](https://hackertube.org/data)給你的 agent，讓你做出自己的版本。

它當然也有立場：排序權交給了 HN 的品味。發布當天就有人說「[it all so bad](https://x.com/parsecranberry/status/2116785470218924500)」，也有人說它「[closer to a time capsule](https://x.com/Presidentlin/status/2116854338781856069)」，因為最新的影片是五個月前。不喜歡的人，可以拿資料去改，或者繼續用 YouTube。

當 AI Coding 讓個人也能快速打造自己的資訊工具，我們是否終於有機會，不再只能接受平台替我們安排好的資訊世界？

**資訊自主權，不是拒絕演算法，而是擁有選擇、調整，甚至拒絕演算法的自由。**

## 延伸閱讀

- [Marc Andreessen 的四分法資訊攝取](https://ai-coding.wiselychen.com/andreessen-information-diet-ai-era-quarter-rule/)
- [Cognitive Surrender：AI 讓你想得變少](https://ai-coding.wiselychen.com/cognitive-surrender-ai-coding-comprehension-debt/)

## 參考資料

- [Karpathy：HackerTube（頁面日期 31 Oct, 2026）](https://karpathy.bearblog.dev/hacker-tube/)
- [HackerTube 資料頁](https://hackertube.org/data)
- [parsecranberry：對 HackerTube 的批評](https://x.com/parsecranberry/status/2116785470218924500)
- [Lincoln：最新影片是五個月前](https://x.com/Presidentlin/status/2116854338781856069)
