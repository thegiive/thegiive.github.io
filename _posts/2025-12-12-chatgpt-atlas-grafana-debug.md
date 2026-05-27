---
layout: post
title: "ChatGPT Atlas + Grafana：30 分鐘 Debug 變 1 分鐘的實戰"
date: 2025-12-12 11:00:00 +0800
permalink: /chatgpt-atlas-grafana-debug/
image: /assets/images/chatgpt-atlas-grafana-debug-cover.png
description: "同事請假，客戶系統問題進來。用 ChatGPT Atlas 直接操作 Grafana 介面 debug，30 分鐘變 1 分鐘，還額外抓到 3 個潛在問題。AI 對「生疏技能喚醒」特別有效。"
---

同事請假，客戶系統問題進來。

打開 Grafana，發現自己已經生疏了。去 GCP 之後都用雲原生的 Cloud Monitoring，Grafana 的設定邏輯早就忘得差不多。

這種「曾經會，但現在生疏」的技能，是最尷尬的。你知道自己能搞定，但要花時間重新摸索。以前這種情況，我大概要花 30 分鐘翻文件、點介面、試錯。

這次我決定試試 ChatGPT Atlas。

---

## Atlas 不只是看截圖，它直接操作瀏覽器

之前用 ChatGPT 處理這種問題，都是截圖丟過去，讓它看圖說故事。但 Atlas 不一樣——**它可以直接操作你的瀏覽器介面**。

我讓它打開 Grafana 的 Alert Rules 頁面，它自己點進去看 config，然後告訴我：

> 「這個 alert rule 的 evaluation interval 設太短了，跟 data source 的 scrape interval 不匹配，所以一直誤報。」

我都還沒來得及仔細看，它已經幫我找到問題了。

---

## 超出預期：它還主動抓到其他問題

更有趣的是，它看完那個 alert rule 之後，主動說：

> 「順便看了一下其他 rules，有幾個的 threshold 設定看起來也有問題，要不要一起檢查？」

結果真的又抓到 3 個潛在問題。這些我自己 debug 的話，根本不會注意到。

---

## 量化結果

| 項目 | 以前 | 用 Atlas |
|------|------|----------|
| Debug 時間 | 30 分鐘 | 1 分鐘 |
| 額外發現問題 | 0 個 | 3 個 |
| 加速倍數 | - | **30x** |

---

## AI 對「生疏技能喚醒」特別有效

這次經驗讓我發現一個 pattern：

**AI 對「曾經會但生疏」的技能喚醒特別有效。**

因為你已經有基礎概念，只是忘記細節。AI 幫你補上那些細節，你馬上就能接上。這比完全不會的人用 AI 學新東西更快，因為你有 context。

老闆不需要什麼都會，但要有辦法快速解決。這就是那個「辦法」。

---

## 關鍵洞察

1. **Atlas 的價值不只是對話，是直接操作** — 它能進到你的工具裡面看、點、找問題
2. **生疏技能 + AI = 快速喚醒** — 比從零學習快很多，因為你有底子
3. **AI 會主動發現你沒注意到的問題** — 這是超出預期的額外價值

下次同事請假，系統出問題，我不會再慌了。
