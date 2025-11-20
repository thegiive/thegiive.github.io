---
layout: post
title: "AI Coding 當 BCP？Cloudflare 大當機給我們的啟示"
date: 2025-11-20 08:00:00 +0800
permalink: /ai-coding-as-bcp-cloudflare-outage/
image: /assets/images/cdn-1.png
description: "Cloudflare 大當機時，Andrew Ng 的工程師用 AI Coding 快速搭建備援組件。這給我們一個新思路：AI Coding 能不能當作 BCP 的另一種方案？"
---

![Cloudflare 大當機影響全球網站](/assets/images/cdn-1.png)

Cloudflare 大當機的時候，經過統計可能 20% Internet 都掛了。

ChatGPT、X、Canva、Uber、Spotify、LoL，綜觀上班、吐槽、出行、音樂、遊戲，全方位的賽博人生被 Internal Server Error 搞死了。

## Andrew Ng 的應對：AI Coding 快速搭建備援

在這個時間點，Andrew Ng 說他的網站工程師利用 AI Coding 很快速的搭建一個 CloudFlare bare minimal 的備援組件，讓他挺過了這個 outage。

![Andrew Ng 團隊用 AI Coding 快速搭建備援組件](/assets/images/cdn-2.png)

雖然說他們短時間能 AI Coding 的組件不外乎：
- FRP 做轉發
- 保護 IP
- CDN cache

這些也都蠻簡單的。

## 為什麼 AI Coding 在這種情境有優勢？

### 1. 搶時間的優勢

短時間之內要搭建好這些基建 config，就算 infra 老黑手來做也要一段時間。

在搶時間搶修的當下，AI Coding 的確有優勢。

### 2. Config 校對更細心

另外一點，AI 如果在有足夠 infra context 的情境下，AI 其實在 config 校對是比老黑手細心。

## 新的 BCP 思路：用 AI Coding 降本

這個倒是非常有趣的概念：

**用 AI Coding 快速搭建一些關鍵 infra 組件，當作另一種 BCP 手段（Business Continuity Plan）。**

### 傳統 BCP 的痛點

傳統 BCP 需要持續花錢維護備援組件：
- 備援機房
- 備援伺服器
- 備援網路設備
- 定期演練與測試

這些都是持續性的成本。

### AI Coding BCP 的優勢

這其實就可以降低平時 BCP 需要持續花錢的備援組件 cost，這也算另外一種降本。

**核心思路：**
- 平時不需要維護完整的備援基建
- 當災難發生時，用 AI Coding 快速搭建 minimal viable 備援
- 撐到主要服務恢復為止

## 唯一的悖論

唯一的問題是：

**當遇到這種史詩級 outage 要 AI Coding 解救你的時候，你的 AI Service 打不打得開？** XD

如果 Cloudflare 掛了，連帶 OpenAI、Anthropic 的服務也可能受影響，那你的 AI Coding 工具可能也用不了。

### 可能的解法

1. **本地部署的 AI 模型**
   - 用 Ollama 等本地模型做備援
   - 雖然能力不如 GPT-4/Claude，但至少能用

2. **多雲備援**
   - AI 服務本身也要有備援計畫
   - 例如同時準備 OpenAI、Anthropic、Google Gemini

3. **離線 playbook**
   - AI 生成的 config 要定期備份
   - 關鍵流程要有離線文檔

## 這個想法有沒有搞頭？

我覺得有，但有幾個前提：

### ✅ 適合的場景

1. **非核心業務的備援**
   - 企業官網、文檔站等
   - 不需要 100% 可用性的服務

2. **基建相對標準化**
   - FRP、Nginx、CDN 這類成熟技術
   - AI 有足夠的訓練資料

3. **團隊有基本 infra 能力**
   - 能夠 review AI 生成的 config
   - 知道哪些組件是關鍵

### ❌ 不適合的場景

1. **金融、醫療等高可用性需求**
   - 不能賭 AI 能不能快速搭建
   - 傳統 BCP 還是必要的

2. **複雜的狀態同步**
   - 資料庫備援、session 同步
   - AI Coding 短時間搞不定

3. **合規要求嚴格**
   - 某些產業要求備援必須定期演練
   - AI 臨時搭建可能不符合規範

## 關鍵洞察

### 1. BCP 的本質是「時間換空間」

傳統 BCP：花錢買時間（平時維護備援，災難時快速切換）

AI Coding BCP：花能力換成本（平時不花錢，災難時快速搭建）

### 2. AI Coding 改變了「搶修速度」這個變數

以前：infra 老手搶修 = 2-4 小時

現在：AI Coding 搶修 = 30 分鐘 - 1 小時

這個速度提升，讓「臨時搭建」變成一個可行選項。

### 3. 這是「夠用就好」哲學的體現

Bare minimal 備援組件不需要 100% 還原功能，只需要：
- 讓網站能訪問（不要 404）
- 基本流量能進來
- 撐到主服務恢復

這個標準，AI Coding 完全做得到。

## 實際可以怎麼做？

### Step 1：準備 AI Coding 環境

- 本地部署一個 Ollama（以防 AI 服務也掛）
- 準備好 Cursor、Claude Code 等工具
- 確保有備援的 AI API keys

### Step 2：建立 Infra Context

- 把現有 infra 架構圖給 AI
- 把關鍵 config 檔案建立 knowledge base
- 讓 AI 理解你的系統架構

### Step 3：定期演練

- 每季度模擬一次「主服務掛了，AI Coding 搶修」
- 記錄 AI 生成的 config 是否能用
- 優化 prompt 和 context

### Step 4：建立 Playbook

- 用 AI 生成一份「災難應對 checklist」
- 包含：要搭建哪些組件、config 範本、驗證步驟
- 定期更新

## 坦白說：限制與風險

### 限制 1：AI 生成的 config 不一定對

- 需要 infra 老手 review
- 不能盲目相信 AI

### 限制 2：某些基建需要時間

- DNS 更新需要時間生效
- SSL 憑證申請也需要時間
- 這些不是 AI Coding 能解決的

### 限制 3：AI 服務本身可能掛

- 如果 OpenAI/Anthropic 也受 Cloudflare 影響
- 你的 AI Coding BCP 就沒用了

### 風險：過度依賴 AI

- 團隊可能失去「手動搶修」的能力
- 一旦 AI 不可用，就完全不知道怎麼辦

## 我的建議

這個想法有搞頭，但不是「取代傳統 BCP」，而是「補充傳統 BCP」。

**適合的做法：**

1. **核心業務：** 傳統 BCP（備援機房、自動切換）
2. **次要業務：** AI Coding BCP（快速搭建 minimal 備援）
3. **定期演練：** 確保兩種方案都能用

**核心原則：**
- 不要把雞蛋放在同一個籃子
- AI Coding 是工具，不是魔法
- 人的判斷永遠不能少

## 延伸思考

### 1. 這個案例說明了什麼？

AI Coding 不只是「加速開發」，還能「加速搶修」。

當災難發生時，時間就是金錢。AI Coding 把「搶修速度」這個變數往前推了一大步。

### 2. 未來會怎麼發展？

我猜未來會出現：
- **AI BCP 服務**：專門幫企業用 AI 快速搭建備援
- **AI Infra Agent**：平時學習你的 infra，災難時自動搶修
- **混合 BCP**：傳統備援 + AI 快速擴展

### 3. 對開發者的啟示

Infra 能力 + AI Coding 能力 = 新的競爭力

未來的 DevOps/SRE，需要：
- 懂基建（知道要搭建什麼）
- 懂 AI（知道怎麼用 AI 快速實現）
- 懂判斷（知道 AI 生成的結果能不能用）

---

## 關鍵數據

**Cloudflare 大當機影響：**
- 影響範圍：約 20% 的全球網站
- 受影響服務：ChatGPT、X、Canva、Uber、Spotify、LoL 等

**AI Coding 搶修優勢：**
- 傳統 infra 搶修：2-4 小時
- AI Coding 搶修：30 分鐘 - 1 小時
- 速度提升：2-4 倍

**可能的降本：**
- 傳統 BCP：持續性成本（備援機房、設備、人力）
- AI Coding BCP：災難時才發生成本（臨時搭建）

---

**標籤：** #AICoding #BCP #CloudFlare #AIAgent #DevOps #災難應對 #降本增效
