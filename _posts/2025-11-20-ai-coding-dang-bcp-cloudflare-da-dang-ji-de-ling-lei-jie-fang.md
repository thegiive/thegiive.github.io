---
layout: post
title: "用 AI Coding 當 BCP 另外一個方案有沒有搞頭？"
date: 2025-11-20 10:00:00 +0800
permalink: /ai-coding-dang-bcp-cloudflare-da-dang-ji-de-ling-lei-jie-fang
image: /assets/images/cdn-1.png
description: "Cloudflare 大當機時 20% Internet 都掛了，ChatGPT、X、Uber、Spotify 全方位賽博人生被搞死。Andrew Ng 的工程師用 AI Coding 快速搭建備援組件挺過危機。這個概念倒是非常有趣 - 用 AI Coding 快速搭建關鍵 infra 組件當作另一種 BCP 手段，降低平時備援成本。唯一的問題是：當遇到史詩級 outage 要 AI Coding 解救你的時候，你的 AI Service 打不打得開 XD"
---

Cloudflare 大當機的時候，經過統計可能 20% Internet 都掛了。

ChatGPT, X , Canva , Uber , Spotify , LoL 綜觀上班、吐槽、出行、音樂、遊戲 - 全方位的賽博人生被 Internal Server Error 搞死了。

## Andrew Ng 的解方

在這個時間點，Andrew Ng 說他的網站工程師利用 AI Coding 很快速的搭建一個 CloudFlare bare minimal 的備援組件，讓他挺過了這個 outage。

![](/assets/images/cdn-2.png)

雖然說他們短時間能 AI Coding 的組件不外乎：

- FRP 做轉發
- 保護 IP
- CDN cache

這些也都蠻簡單的。

但是短時間之內要搭建好這些基建 config，就算 infra 老黑手來做也要一段時間。

在搶時間搶修的當下，AI Coding 的確有優勢。

另外一點，AI 如果在有足夠 infra context 的情境下，AI 其實在 config 校對是比老黑手細心。

## 非常有趣的概念

這個倒是非常有趣的概念 - 用 AI Coding 快速搭建一些關鍵 infra 組件，當作另一種 BCP 手段 (Business Continuous Plan)。

這其實就可以降低平時 BCP 需要持續花錢的備援組件 cost，這也算另外一種降本。

## 唯一的問題

唯一的問題是：

> 當遇到這種史詩級 outage 要 AI Coding 解救你的時候，你的 AI Service 打不打得開 XD
