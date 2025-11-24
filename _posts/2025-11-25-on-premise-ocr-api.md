---
layout: post
title: "AI Agent 時代的無聊基礎建設：地端 OCR API"
date: 2025-11-25 04:15:00 +0800
permalink: /on-premise-ocr-api/
image: /assets/images/ocr-system-architecture.png
description: "在 AI Agent 時代，沒人想聊無聊的基礎建設。但 60-70% 的企業資料躺在 PDF 裡，地端 OCR API 是繞不過去的關鍵。"
---

![OCR System Architecture](/assets/images/ocr-system-architecture.png)

大家都在講 AI Agent，講 Multi-Agent，講 Agentic Workflow。

但我發現一個有趣的現象：幾乎沒人在講「基礎建設」。

就像蓋房子，所有人都在討論室內設計要多漂亮，但沒人想聊地基怎麼打。

## 現實問題

地端 OCR API 就是這種東西。無聊嗎？超無聊。重要嗎？非常重要。

為什麼？因為 Enterprise 的現實是 60-70% 的資料躺在 PDF 裡（合約、發票、技術規格書、會議紀錄掃描檔），LLM 讀不懂這些 PDF，資安考量，不能上雲

雲的 AI Agent 當然沒這個問題，但是 enterprise  AI Agent 再聰明，面對一堆 PDF 就是個瞎子。

## 技術已經不值錢了

老實說，現在任何一個會 Vibe Coding 的人，兩小時就能搭出一個「能動」的 OCR 服務。但是你的服務真的「好嗎？」

有幸，看得懂技術架構好壞的品味，我應該還在。

## 什麼是好架構

最近看到這個：https://github.com/markuskuehnle/credit-ocr-system

這個架構挺 solid：

```
API Gateway → Message Queue → OCR Worker → Database
```

為什麼好？

1. **MQ 緩衝** - OCR 處理時間不穩定，圖片大小影響資源太多。MQ 讓流量平整，尖離峰時間 resource 差距不會太大

2. **故障隔離** - OCR worker 掛了，其他 pipeline 不受影響

3. **水平擴展** - 可以根據 SLA 動態調整 worker 數量

既然是地端，有一些成本，像是硬體層面擁抱 CPU 非 GPU  。OCR 使用 RapidOCR + ONNX Runtime , 可以降低 infra 成本

## 但魯棒性還有五個坑要注意，不然還是會掛：

1. **Dead Letter Retry 機制** - 這是我在 Google 面試 Data Engineer 的考題，一考一個準

2. **Docker 資源管理** - 避免 local LLM & OCR 把 Docker Host 拖垮

3. **Timeout 與 SLA 綁定** - 不同客戶不同要求，要能調整

4. **Document Idempotency** - 需要 doc ID 避免重複處理

5. **Log Sanitization** - OCR 處理很多機敏資料（信用卡拍照），金融企業要特別注意

## 核心洞察

當產生「系統」的能力已經很廉價的年代，鑒賞「系統」的能力反而變成稀缺。地端 OCR API 很無聊，但這種無聊的基礎建設，才是 AI Agent 真正落地的關鍵。