---
layout: post
title: "AI Coding 當 BCP:Cloudflare 大當機的另類解方"
date: 2025-11-20 16:00:00 +0800
permalink: /ai-coding-dang-bcp-cloudflare-da-dang-ji-de-ling-lei-jie-fang/
description: "當 20% 的 Internet 掛掉，Andrew Ng 的工程師用 AI Coding 快速搭建備援組件挺過危機。這是否意味著我們可以用 AI 臨時搭建關鍵基建，取代傳統持續養備援的思維？但當你最需要 AI 救命時，AI Service 本身會不會也掛了？"
---

## 賽博末日的那一天

2025 年某月某日，20% 的 Internet 掛了。

你打開電腦想用 ChatGPT 寫個報告 - `Internal Server Error`
你想發 X 吐槽一下 - `Internal Server Error`
你想叫 Uber 去公司 - `Internal Server Error`
你想開 Spotify 療癒心情 - `Internal Server Error`
就連想打個 LoL 發洩都不行 - `Internal Server Error`

全方位的賽博人生，被一個 Cloudflare 當機搞死。

ChatGPT、X、Canva、Uber、Spotify、LoL... 橫跨工作、吐槽、出行、音樂、遊戲，所有讓現代人活著的服務，全部陣亡。

## Andrew Ng 工程師的英雄時刻

就在大家手忙腳亂的時候，Andrew Ng 分享了一個有趣的故事：

> 他的網站工程師利用 AI Coding，快速搭建了 Cloudflare bare minimal 的備援組件，成功挺過這次 outage，保持服務可用。

雖然說他們短時間能 AI Coding 出來的組件，不外乎：

- **FRP 做轉發** - 繞過 Cloudflare 直接連到 origin server
- **IP 保護機制** - 簡易的 rate limiting 和黑名單
- **CDN cache** - 靜態資源的基本快取

這些技術本身都蠻簡單的，就算是 infra 老黑手來做也會。

**但是，短時間之內要搭建好這些基建 config，就算老黑手也要一段時間。**

在搶時間搶修的當下，AI Coding 的確有優勢：

1. **速度優勢** - 快速生成 config 和部署腳本
2. **細心優勢** - AI 在有足夠 infra context 的情境下，config 校對比人類在壓力下細心

## 反直覺的 BCP 思維

這個案例讓我想到一個非常有趣的概念：

> **用 AI Coding 快速搭建關鍵 infra 組件，當作另一種 BCP (Business Continuous Plan) 手段。**

### 傳統 BCP 的困境

傳統的 BCP 思維是：

- 持續花錢養備援組件（備援機房、備援資料庫、備援 CDN）
- 99% 時間都閒置，但必須保持 ready
- 高成本、低使用率

這就像養了一個消防隊，平時都在睡覺，但你還是要付薪水。

### AI Coding BCP 的可能性

而 AI Coding BCP 的思維是：

- **平時不養備援**，事發時快速搭建
- 降低平時 BCP cost
- 另一種「降本」手段

這就像沒有消防隊，但有一個會快速召喚消防員的魔法陣。

### 哪些場景適合？

當然，不是所有 BCP 都適合這個策略。我猜測適合 AI Coding 臨時搭建的場景：

- ✅ **CDN/反向代理** - nginx/caddy config 生成
- ✅ **簡易 WAF** - rate limiting、IP 黑名單
- ✅ **流量轉發** - FRP/frps 快速部署
- ✅ **靜態資源託管** - S3/R2 bucket 快速建立

而不適合的場景：

- ❌ **核心資料庫** - 資料遷移太複雜，AI 做不來
- ❌ **複雜的 load balancer** - 需要大量測試和調校
- ❌ **有狀態服務** - session management、websocket 等

## 致命的諷刺矛盾

這個方案最大的問題，也是最諷刺的地方：

> **當你遇到史詩級 outage 要 AI Coding 解救你的時候，你的 AI Service 打不打得開？ XD**

想像一下這個場景：

- Cloudflare 掛了 → 你想用 AI Coding 搭建備援
- 打開 Claude Code → `Connection timeout`
- 打開 Cursor → `OpenAI API unavailable`
- 打開 GitHub Copilot → `Service temporarily unavailable`

**你的救命稻草，本身也需要被救命。**

### 可能的解方

那怎麼辦？幾個可能的方向：

#### 1. 自建 LLM（但成本又回來了）

- 在自己的 infra 上跑 Llama 3 或 Qwen
- 但這又回到「養備援」的老路
- GPU 機器閒置成本可能比傳統 BCP 還高

#### 2. 多家 AI Service 備援（又是備援的概念）

- 同時訂閱 Claude、ChatGPT、Gemini
- 希望不要同時掛（但 Cloudflare outage 就是同時掛 XD）
- 成本較低，但還是要花錢

#### 3. Hybrid 模式（最務實）

> **關鍵組件還是要預先準備，非關鍵的用 AI 臨時搭。**

例如：

- **預先準備**：備援資料庫、核心 API 的備援機房
- **AI 臨時搭**：CDN、WAF、流量轉發

這樣可以降低一部分 BCP 成本，但核心還是有保障。

## 成本對比（待驗證）

這裡放一些假設性的計算，實際數字需要驗證：

### 傳統 BCP 成本（以中型網站為例）

- **備援 CDN**：每月 $500-$2000（Cloudflare + Fastly）
- **備援機房**：每月 $1000-$5000（AWS multi-region）
- **人力維護**：每月 $2000-$5000（SRE 工時）
- **總計**：每月 $3500-$12000，一年 $42K-$144K

### AI Coding BCP 成本

- **AI Service 訂閱**：每月 $60-$200（Claude Pro + Cursor + Copilot）
- **臨時機器成本**：每次 outage $100-$500（按需開機）
- **開發時間**：每次 outage 2-4 小時（工程師 + AI）
- **總計（假設一年 2 次 outage）**：約 $2K-$5K

**潛在節省：$40K-$139K / 年**

當然，這個計算沒考慮：

- outage 期間的業務損失
- 客戶信任度下降
- AI 搭建失敗的風險

## 坦白說：什麼情境適合？

這個 AI Coding BCP 策略，**不是適合所有人**。

### 適合的情境：

- ✅ **中小型網站** - 傳統 BCP 成本佔比太高
- ✅ **非關鍵業務** - 可以容忍 1-2 小時的搶修時間
- ✅ **技術團隊成熟** - 有人能在壓力下駕馭 AI
- ✅ **Infra 相對簡單** - 主要是 CDN/反向代理層

### 不適合的情境：

- ❌ **金融/醫療等關鍵業務** - 不能賭 AI 搭建成功
- ❌ **複雜的分散式系統** - AI 理解不了全局架構
- ❌ **新創團隊沒 infra 經驗** - 連 context 都給不好
- ❌ **高流量網站** - 臨時搭建的組件扛不住

## 關鍵洞察

> **BCP 不是「全部傳統」vs「全部 AI」的二選一，而是「哪些適合 AI 臨時搭」vs「哪些必須預先養」的取捨。**

Andrew Ng 的案例告訴我們：

- AI Coding 在緊急搶修時有速度和細心的優勢
- 但前提是你的 AI Service 本身要活著
- 最務實的策略是 Hybrid：核心預先養，邊緣臨時搭

## 下一步：實戰驗證

這篇文章目前還是「理論推測」階段，接下來我打算做幾個實驗：

1. **實際用 AI Coding 搭建一個簡易 CDN/FRP**
   - 記錄完整過程和時間
   - 對比人工做需要多久

2. **找 Andrew Ng 的原始分享**
   - 看具體搭建了哪些組件
   - 花了多久時間

3. **訪談 SRE 朋友**
   - 傳統 BCP 的實際成本
   - 有沒有 AI Coding 搶修的經驗

如果你有相關經驗，或者對這個主題有興趣，歡迎跟我交流。

這個想法可能有效，也可能不完美，但數據和邏輯都在這裡，你可以拿去改進。
