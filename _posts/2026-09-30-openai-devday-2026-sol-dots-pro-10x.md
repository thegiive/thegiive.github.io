---
layout: post
title: "OpenAI DevDay 三件事其實是一件事：Sol 打到五分之一價、Pro 200 從 20x 砍成 10x、Dots 賣的是「不用盯」"
date: 2026-09-30 09:00:00 +0800
permalink: /openai-devday-2026-sol-dots-pro-10x/
tags: [OpenAI, DevDay, GPT-6.1 Sol, GPT-6 Astra, Dots, ChatGPT Pro, Pro 500, Codex, Tibo, Ultrafast, Grok Bot, 訂閱戰, 定價]
categories: [AI 產業分析]
image: /assets/images/openai-devday-2026-dots-keynote.jpg
description: "台灣時間 9 月 30 日凌晨，OpenAI DevDay 發了五分之一價的 GPT-6.1 Sol、always-on 的 Dots、$500 的 Pro 500，台下 Codex 負責人 Tibo 把 Pro 200 從 20X 砍成 10X——一個月前他才說這個 20X「does exactly what it says on the tin」。老用戶 10 月 29 日前還是 20x，所以很多人還沒感覺。這篇把三個發布放在同一張帳上算：每一倍 Plus 用量現在都是 20 美金，量販折扣沒了，溢價搬到了速度和「不用盯」上。"
author: Wisely Chen
faq:
  - question: "ChatGPT Pro 200 的額度什麼時候從 20x 變 10x？"
    answer: "新訂閱者一開始就是 10x Plus。依 TNW 和 Nerdschalk 的整理，現有 Pro 200 訂閱者 10 月 29 日前維持 20x，10 月 30 日起變 10x，補償一次性 62,500 credits（標價 $2,500），12 月 31 日到期。OpenAI Codex 負責人 Tibo 只說老用戶會「keep the 20X multiplier for a bit」，沒給精確日期。"
  - question: "ChatGPT Pro 500 值得升級嗎？"
    answer: "依多篇整理，Pro 500（$500/月）是 25 倍 Plus 用量（官方頁面未能確認），每一倍的單價是 $20，跟 Plus、Pro 100、新 Pro 200 一樣，沒有量販優惠。它獨有的是 Ultrafast（每秒最高 300 token，Codex 裡快 8 倍）。只想拿回舊 Pro 200 的額度，等於用 2.5 倍價格換 1.25 倍用量。"
  - question: "OpenAI Dots 跟 xAI 的 Grok Bot 有什麼不同？"
    answer: "兩者都是常駐型 agent（Always-on Agent）：有自己的雲端電腦、24 小時在背景做事、外型都是泡泡角色。Grok Bot 附在 $30 的 SuperGrok 裡，所有 Bot 共用一組登入。Dots 用 GPT-6 Astra，需要 ChatGPT Pro 或 Business Premium，接 4,000 多個 app，有內建規則決定何時自己做、何時問人，並可用 Custom Rules 設定允許、要求批准或封鎖。"
  - question: "為什麼 OpenAI 沒有發布 GPT-6.1 Astra？"
    answer: "OpenAI 在 DevDay 前一天（9 月 28 日）確認不發。依 TechCrunch 等報導，內部測試發現它欺騙性（Deception）比前代高、會不問使用者就往前推進任務，而且不一定如實揭露自己做了什麼。這跟 agent 缺乏停止條件（Stop Condition）是同一個問題。  ---"
---

台灣時間今天凌晨，OpenAI 開了 DevDay：GPT-6.1 Sol、always-on agent「Dots」、$500 的新方案 Pro 500。

台下還有兩件更有感的事。開場前，Codex 負責人 Tibo 在 X 上宣布 Pro 200 從 20 倍 Plus 砍成 10 倍；前一天，OpenAI 確認不發 GPT-6.1 Astra，因為它會不問使用者就往前衝。

一個月前，同一個 Tibo 才說過：Pro 的 20X「does exactly what it says on the tin」。

三條新聞，放在同一張帳上算，是同一件事。

---

## 一、Pro 200：20x 變 10x，但你現在還是 20x

[Tibo 的原文](https://x.com/thsottiaux/status/2104823812042940713)（20,811 個讚、1,437 萬次瀏覽）：

> "In effect, if you do the math, it will net out at half the dollar in API spend compared to the old Pro $200 plan."

換算成 API 花費，是舊方案的一半。[第二則](https://x.com/thsottiaux/status/2104951965184925941)把倍數講清楚：Plus 1X、Pro 100 5X、Pro 200 10X，老用戶「will keep the 20X multiplier for a bit」。

這就是為什麼很多人覺得「好像還沒改」。依 [TNW](https://daily.dev/posts/openai-halves-pro-200-usage-and-launches-a-500-chatgpt-plan-at-devday-vbxlojybv) 和 [Nerdschalk](https://nerdschalk.com/chatgpt-pro-100-vs-200-vs-500-prices-usage-limits) 的整理，現有 Pro 200 訂閱者 10 月 29 日前維持 20x，10 月 30 日起變 10x，補償一次性 62,500 credits（標價 $2,500），12 月 31 日到期。

Pro 500 的倍數，多篇整理寫 25 倍 Plus。用這組數字算每一倍用量的單價：

| 方案 | 月費 | 用量（對 Plus） | 每 1x 單價 |
|------|:--:|:--:|:--:|
| Plus | $20 | 1x | $20 |
| Pro 100 | $100 | 5x | $20 |
| Pro 200（新） | $200 | 10x | $20 |
| Pro 500 | $500 | 25x | $20 |
| Pro 200（舊，10/29 前） | $200 | 20x | **$10** |

四個新方案，單價一模一樣。舊 Pro 200 是唯一打五折的那一檔，現在折扣沒了。[@kylelubieniecki](https://x.com/kylelubieniecki/status/2105041277699924405) 的說法：「Pro used to be the bulk discount. Now it's just a bigger bill.」

想拿回原本的 20x，最近的一檔是 Pro 500：價格 2.5 倍，用量 1.25 倍。

### 年底前，老帳號比 Pro 500 值錢

這反而讓舊 Pro 200 的 20X 更顯眼。新訂閱者已經拿不到 20x，手上還有老帳號的人，在年底前可能比付 $500 的人更划算。

但要講精確：20x 只到 10 月 29 日，撐到年底的是那筆 credits。[TNW](https://thenextweb.com/news/openai-devday-pro-200-usage-cut-pro-500-plan) 的原文是：

> "Existing subscribers keep their current limits until 29 October and get a one-time grant of usage credits worth $2,500, which expire at the end of the year."

算到 12 月 31 日：

- **舊 Pro 200**：三個月 $600，拿到 10 月的 20x、11 到 12 月的 10x，外加 $2,500 credits
- **Pro 500**：三個月 $1,500，每個月 25x，多一個 Ultrafast

10 月這個月，舊 Pro 200 用 Pro 500 四成的價格拿到八成的用量。11、12 月額度掉到 10x，但手上多一筆標價 $2,500 的 credits，比兩個方案三個月的價差 $900 還多。Credits 能換多少實際用量，OpenAI 沒公布換算，這筆帳只能算到標價為止。

還有一個前提：訂閱不能斷。新訂閱者一開始就是 10x，老帳號斷掉再訂，很可能就回不去了。

### 講白了，還是被罵

9 月 2 日我寫 [Claude 的 20x 爭議](/claude-pricing-20x-weekly-limit-trust-crisis/)時，用戶對 Anthropic 的要求是「Just tell us plainly」——直接講壞消息，我們受得了。

Tibo 這次第一則就寫了「half」，沒有包裝成調漲。結果[底下的回覆](https://x.com/bridgemindai/status/2104952608242774458)（2,158 個讚）是：「Translation: "You just got rug pulled"」。

**透明不能讓用戶不生氣。** 它能做到的，是讓爭議停在「這樣做合不合理」，而不是「你到底有沒有騙我」。前者傷生意，後者傷信任。

---

## 二、GPT-6.1 Sol：智力打到五分之一價

[OpenAI](https://x.com/OpenAI/status/2104986129686741046)：「near-Astra intelligence for a fifth of the price」。API 每百萬 token 輸入 $2、輸出 $10，Astra 是 $10 / $50（[VentureBeat](https://venturebeat.com/technology/openais-gpt-6-1-sol-offers-astra-like-performance-at-1-5th-price-a-new-ultrafast-tier-clocks-at-300-tokens-per-second)）。

OpenAI 自己公布的數字（[Investing.com](https://www.investing.com/news/stock-market-news/openai-launches-gpt61-sol-with-nearastra-performance-93CH-4923227)）：Terminal-Bench Science 0.1 每任務成本 Sol $5.47、Opus 5.5 $23.21、Astra $23.80；OSWorld 2.0 離 Astra 只差 2.1 個百分點。

社群分兩派。[Theo](https://x.com/theo/status/2105000888192663582) 自測說比 Opus 5.5 好；[@Im_IrushiK](https://x.com/Im_IrushiK/status/2104995114456375563) 說整場 DevDay「pretty underwhelming」——想要更好的模型和更多額度，拿到的是一個更貴的方案。

---

## 三、Dots：OpenAI 版的 Grok Bot

Dots 是 GPT-6 Astra 驅動的 always-on agent：每個 dot 有自己的雲端電腦，24/7 在背景跑，接 4,000 多個 app，從 ChatGPT、Slack、Teams 找得到（[OpenAI](https://openai.com/index/introducing-dots/)、[9to5Google](https://9to5google.com/2026/09/29/openai-dots-agent/)）。Pro 和 Business Premium 可用，第一個 dot 包含在方案裡。

泡泡造型跟 Grok Bot 很像（[iPhone in Canada](https://www.iphoneincanada.ca/2026/09/29/openai-dots-take-on-meta-muse-and-grok-bot-with-24-7-ai-agents/)），產品形狀也一樣——[9 月 9 日寫的 Grok Bot](/grok-bot-persistent-agent-cloud-computer-cost/) 是一台永遠在線的雲端 VM 加一個會自己做事的 AI，$30 的 SuperGrok 就附。

差別在權限。Grok Bot 所有 Bot 共用一組登入；Dots 有內建規則決定何時自己做、何時問人，還能用 Custom Rules 允許、要求批准或封鎖特定動作。

---

## 四、三件事是一件事：Token 在打折，時間在漲價

**Sol 讓智力變便宜。** 同樣的任務，每任務成本不到 Astra 的四分之一。

**訂閱的量販折扣取消。** 每一倍 Plus 用量都是 20 美金。

**溢價搬到速度和「不用盯」。** Pro 500 是唯一有 Ultrafast 的方案，每秒最高 300 token，Codex 裡快 8 倍；Dots 要 Pro 才有。

Token 是商品，會一直降價——Tibo 自己說這週 GPT-6 Sol 和 Luna 的 API 價格砍半。商品降價，要守住營收就得賣別的：Ultrafast 賣等待時間，Dots 賣盯場時間。

反方是 Tibo 的論點：「you will still get more work done than if you were on the Pro $200 subscription one month ago」——額度砍半，但 Sol 每件事的成本砍到四分之一以下。成立一半。Sol 夠用的人大概無感；要用 Astra 的人就是實打實砍半。而且 API 降價本來就該讓利給固定價的訂閱，拿它抵銷縮水說不過去。

---

## 五、砍掉一個不會停的模型，賣一個不用盯的產品

[TechCrunch](https://techcrunch.com/2026/09/29/openai-launches-gpt-6-1-sol-says-it-nearly-matches-gpt-6-astra-and-costs-less/) 引述 GPT-6.1 Astra 被砍的理由：

> "higher levels of deception and a tendency to move forward with tasks without asking the user for permission"

隔天，OpenAI 推出一個「pursuing user-defined goals continuously in the background with minimal oversight」的 Dots。Dots 用的是 GPT-6 Astra，不是被砍的 6.1，兩件事不衝突。

但 9 月 26 日寫的 [Medicare 事件](/openai-medicare-agent-mundane-task-stop-condition/)結論是：agent 最缺的不是能力，是停止條件。GPT-6.1 Astra 被砍的理由，幾乎是同一句話的模型版。

**Dots 值不值得接進公司 Slack，取決於它的「何時要問人」規則有多可靠。**

---

## 坦白說

Pro 500 的 25x 是二手資料，OpenAI 方案說明頁我抓的時候回 403，Engadget 也沒寫。如果不是 25x，Pro 500 那列要重算，但 Plus、Pro 100、新 Pro 200 都是 $20 不受影響。10 月 29 日 / 30 日的切換日期也來自二手整理，Tibo 本人只說「for a bit」。

Sol 的 benchmark 全是 OpenAI 自己跑的，上線才一天。Dots 我還沒拿到，沒有第一手經驗。「賣時間」是我從定價結構推的解讀，OpenAI 沒這樣說過。

---

## 關鍵洞察

**算「每 1x 單價」，不要看倍數。** OpenAI 新方案每一倍都是 $20，沒有量販優惠。

**舊 Pro 200 用戶記兩個日期：** 10 月 29 日是 20x 最後一天，12 月 31 日是 $2,500 credits 到期日。年底前別急著升 Pro 500，也別讓老帳號斷訂。

**Always-on agent 的價值取決於停止條件。** 接 Dots 之前，先看 Custom Rules 能不能把「碰到牆就停下來問人」設成預設。

---

## 常見問題 Q&A

**Q: ChatGPT Pro 200 的額度什麼時候從 20x 變 10x？**

新訂閱者一開始就是 10x Plus。依 TNW 和 Nerdschalk 的整理，現有 Pro 200 訂閱者 10 月 29 日前維持 20x，10 月 30 日起變 10x，補償一次性 62,500 credits（標價 $2,500），12 月 31 日到期。OpenAI Codex 負責人 Tibo 只說老用戶會「keep the 20X multiplier for a bit」，沒給精確日期。

**Q: ChatGPT Pro 500 值得升級嗎？**

依多篇整理，Pro 500（$500/月）是 25 倍 Plus 用量（官方頁面未能確認），每一倍的單價是 $20，跟 Plus、Pro 100、新 Pro 200 一樣，沒有量販優惠。它獨有的是 Ultrafast（每秒最高 300 token，Codex 裡快 8 倍）。只想拿回舊 Pro 200 的額度，等於用 2.5 倍價格換 1.25 倍用量。

**Q: OpenAI Dots 跟 xAI 的 Grok Bot 有什麼不同？**

兩者都是常駐型 agent（Always-on Agent）：有自己的雲端電腦、24 小時在背景做事、外型都是泡泡角色。Grok Bot 附在 $30 的 SuperGrok 裡，所有 Bot 共用一組登入。Dots 用 GPT-6 Astra，需要 ChatGPT Pro 或 Business Premium，接 4,000 多個 app，有內建規則決定何時自己做、何時問人，並可用 Custom Rules 設定允許、要求批准或封鎖。

**Q: 為什麼 OpenAI 沒有發布 GPT-6.1 Astra？**

OpenAI 在 DevDay 前一天（9 月 28 日）確認不發。依 TechCrunch 等報導，內部測試發現它欺騙性（Deception）比前代高、會不問使用者就往前推進任務，而且不一定如實揭露自己做了什麼。這跟 agent 缺乏停止條件（Stop Condition）是同一個問題。

---

## 來源

- Tibo（@thsottiaux）9/29：<https://x.com/thsottiaux/status/2104823812042940713>、<https://x.com/thsottiaux/status/2104951965184925941>
- OpenAI GPT-6.1 Sol 貼文：<https://x.com/OpenAI/status/2104986129686741046>
- OpenAI, Introducing dots：<https://openai.com/index/introducing-dots/>
- TechCrunch, GPT-6.1 Sol：<https://techcrunch.com/2026/09/29/openai-launches-gpt-6-1-sol-says-it-nearly-matches-gpt-6-astra-and-costs-less/>
- VentureBeat：<https://venturebeat.com/technology/openais-gpt-6-1-sol-offers-astra-like-performance-at-1-5th-price-a-new-ultrafast-tier-clocks-at-300-tokens-per-second>
- Investing.com：<https://www.investing.com/news/stock-market-news/openai-launches-gpt61-sol-with-nearastra-performance-93CH-4923227>
- daily.dev（轉引 TNW）：<https://daily.dev/posts/openai-halves-pro-200-usage-and-launches-a-500-chatgpt-plan-at-devday-vbxlojybv>
- Nerdschalk：<https://nerdschalk.com/chatgpt-pro-100-vs-200-vs-500-prices-usage-limits>
- 9to5Google：<https://9to5google.com/2026/09/29/openai-dots-agent/>
- iPhone in Canada：<https://www.iphoneincanada.ca/2026/09/29/openai-dots-take-on-meta-muse-and-grok-bot-with-24-7-ai-agents/>
