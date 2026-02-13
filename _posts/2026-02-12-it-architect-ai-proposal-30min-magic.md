---
layout: post
title: "IT 架構師的 AI 加速實錄：從一週到 30 分鐘，但真正的魔術不在這裡"
date: 2026-02-12 10:30:00 +0800
categories: [it-architecture]
tags: [it-architect, tech-proposal, claude-code, ai-acceleration, business-thinking, raas]
permalink: /it-architect-ai-proposal-30min-magic/
image: /assets/images/it-architect-ai-proposal-cover.png
description: "身為架構師，你的架構可以成交嗎？成交後可以落地嗎？這才是人類架構師的最大價值，也是魔術真正發生的地方。"
---

![剛從深圳/香港回來，喝到心心念念的霸王茶姬](/assets/images/it-architect-ai-proposal-cover.png)

**作者：** Wisely Chen
**日期：** 2026 年 2 月
**系列：** IT 架構
**關鍵字：** IT 架構師, Tech Proposal, Claude Code, AI 加速, 商務思維, RaaS

---

週四了，又到了雷打不動的保證無聊的 IT 架構文。

今天來講一個軟一點的文字。

---

## AI 出 Tech Proposal：從一週到一小時

提到 IT 架構師用 AI 可以加速撰寫 Tech Arch Proposal，我可能是這方面的見證者。

在幾個月的時間內，隨著 Opus 4.5 加上我的提示詞不斷演進，我漸漸掌握了一個良好的、可以快速出 Tech Proposal 的框架。以往要花一週時間反覆討論的技術框架，現在一小時就會出來了。

一小時的時間，我一開始會根據 customer requirement，請 Claude Code 給我一個 Draft Proposal。現在 Opus 加上雲端的 component 太過模塊化，其實 AI 寫出技術框架幾乎是零失誤。加上最近終於掌握了如何用 Nano Banana Pro 畫雲架構圖的技巧，一個 Draft Proposal 幾乎可以 5 分鐘出來。

我用 Nano Banana Pro 畫架構圖的提示詞大概長這樣：

> 請畫一張專業的雲端架構圖，風格為經典企業風。背景白色，帶微妙的淺灰色幾何圖案。左側有一條包含 Google 四色（藍 #4285F4、紅 #DB4437、黃 #F4B400、綠 #0F9D58）的流暢抽象線條。使用扁平化 2D 向量圖標。架構分為.....層與層之間用箭頭連接，左側標註 Auth，右側標註 Monitor。16:9 寬螢幕，高解析度。

關鍵技巧：把架構的層級、每層的 component、連接關係都寫清楚，Nano Banana Pro 就能畫出幾乎可以直接放進 Proposal 的架構圖。不需要再開 draw.io 或 Lucidchart 手動排版了。

---

## 接下來才是魔術發生的時候

我開始請不同 AI 扮演機車的角色：

1. **客戶 CIO** — 從戰略層面挑刺

   > 你現在是一間年營收 50 億的製造業 CIO，你看到這份 Tech Proposal，請從企業戰略、數位轉型路線圖、與現有 IT 投資的相容性三個角度，列出你最擔心的 5 個問題。

2. **客戶的合規團隊** — 從法規與安全面向審查

   > 你現在是企業合規主管，請根據這份 Proposal 檢查：資料落地要求、個資法 (GDPR/PDPA) 合規、第三方供應商的安全認證、以及災難復原計畫是否完整。列出所有不合格的項目。

3. **客戶的採購審核者** — 從成本與 ROI 面向質疑

   > 你是採購部門的審核者，你的工作是砍預算。請針對這份 Proposal 的每一項費用，質疑其合理性，並要求提供替代方案或降本建議。

4. **文件 format 的挑刺者** — 從格式與專業度面向打磨

   > 你是一個對文件品質極度挑剔的技術文件審核者。請檢查這份 Proposal 的結構完整性、用詞一致性、圖表是否清晰、以及是否有任何模糊或自相矛盾的描述。

根據這個 proposal，從不同面向來挑刺，讓牛馬 Claude Code 去改寫。

不斷討論當中，我也大量丟入我對這個客戶的理解去要求 Claude Code 修改。最後終於出來一個接近很完美的版本。

到現在大概花了 30 分鐘，但這是以前一週的工作量。

這是我覺得 AI 對我的產出最大加速的部分。

---

## 但是，靈魂拷問來了

**「身為架構師，你的架構可以成交嗎？成交後可以落地嗎？」**

這才是人類架構師在裡面的最大價值，也是魔術真正發生的地方。

你必須要有「商務思維」。

我們提供這個方案給客戶——報價是否合理？要怎麼判斷價格合理？我們提供哪些價值給客戶？我們提供哪些價值給 deal breaker？客戶最後的決策點、deal breaker 可能是啥？我們這個方案，執行單位是否可以如期執行？風險在哪邊？

---

## 完美架構的墳場

身為一個資深的架構師，我幾乎每次都因為最後的報價、價值、deal breaker，被迫重新修改架構。從完美的框架變成一個疊床架屋的東西。

只是因為：

1. Customer contact window 喜歡這個 component
2. 成本算不過去
3. 那時的公司要主推某個產品
4. 原先完美架構的供應商，合作態度不好，只好換成合作態度好的
5. 轉向要跟某個 partner 戰略合作

但是沒關係。

因為重改一次，AI 30 分鐘內都可以做完「撰寫 → review → 校稿」的閉環過程。

而你，偉大的 IT 架構師，必須在這些混亂的動態上下文中，判斷出最佳「可成交」的架構。

**這才是你的價值。**

---

## 坦白說

剛從深圳/香港回來，喝到心心念念的霸王茶姬。

---

## 延伸閱讀

- [AI 時代的殘酷進化：別再賣能力，請開始提供 RaaS](/ai-era-raas-results-as-a-service/) — 市場只買結果，不買過程
- [FDE：AI Agent 落地新模式](/fde-ai-agent-new-model/) — 駐場才能理解客戶真正需要什麼結果
