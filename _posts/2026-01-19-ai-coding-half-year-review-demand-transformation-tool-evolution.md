---
layout: post
title: "AI Coding 半年回顧：開發並沒有變快，我們只是把瓶頸從寫 Code，轉移到了 QA 跟需求收集"
date: 2026-01-19 12:00:00 +0800
categories: [AI Coding, ATPM]
tags: [AI Coding, Claude Code, Cursor, PRD, 需求轉化, Vibe Coding, QA]
permalink: /ai-coding-half-year-review-demand-transformation-tool-evolution/
image: /assets/images/ai-coding-half-year-review-cover.png
description: "這半年 AI Coding 工具全面爆發，但以一個實戰快三年的工程師視角，AI Model 的進步其實對效率沒有太多影響。真正的瓶頸從來不是 Coding，而是需求收集與 QA 驗收。"
---

這半年，AI Coding 工具全面爆發。從 Cursor、Claude Code 到各種 Agent framework，討論聲量沒停過。

但我以一個在 Production 環境實戰 AI Coding 快三年（從 2023 就開始用 ChatGPT 複製貼上）的工程師視角，想分享一個反直覺的觀察：

## AI Model 的進步，其實對效率沒有太多影響

其實早在一年多前，AI 就已經足夠會寫 Code 了。

從 GPT-4、Claude Sonnet 3.5 開始，只要需求夠清楚，AI 產出 90–95% 可用程式碼早就不是問題。而且這個比例這一年幾乎沒變。

AI Model 更加聰明，其實沒有影響太多。

**這一年 AI Coding Tool 真正的進步在於：取得 Context 更容易。**

Claude Code 為什麼強？因為它能跨檔案、跨任務理解整個專案結構。

所以你看到的工具演進，其實都在解同一題：
- Context window 變大
- RAG / indexing 變成標配
- MCP / Claude Code Skill 讓 AI 能主動抓資料

AI 不是不會寫，是不知道你在幹嘛。

而最難取得的上下文，從來不是 code，是需求。

## 怎麼把客戶需求變成清楚的 PRD，依舊很無解

我有一個專案，裡面資深 PM 已經在專案裡面三年了，還是常因為客戶黑話、隱性業務邏輯而誤解需求。

這不是特例。

根據我的 PM 團隊大量的體感，第一次訪談，需求準確率 60–80% 已經算不錯。

這不是誰能力不夠，而是需求本來就是一個「客戶跟 PM 兩個腦袋對齊」的過程。

在 PM 界這有一個特殊名詞叫做「通靈」。有通靈技能的 PM 可是 SSR 的存在。

需求釐清沒效率，就是以前 TDD/BDD 遇到的問題，也是現在 SDD 很難普及的主要原因。

**AI 可以幫你寫 PRD，但它沒辦法幫你通靈。**

## QA 驗收這塊依舊很麻煩

我現在聽到很多 Vibe Coding 課程在談「怎麼寫」，但很少人認真談一件事：怎麼驗收？

產出可以很快，但如果沒有人定義「什麼算對、什麼算錯」，AI Coding 速度只是在無限制地放大風險。

這就是為何「AI Coding 在現實專案，很多時候並沒有變快」的原因。

那為何 Prototype/POC 可以變快？因為不需要驗收呀，大哥。

**Coding 的效率瓶頸，只是從寫 Code 轉移到 QA。**

## 那該怎麼開始補齊驗收能力？

很多人問我怎麼做。我不是 QA 專業，但可以先從三件事開始：

**1. 把需求 PRD 寫成「可驗收條件」**

不用懂語法，但一定要能回答：什麼情況算做對？什麼情況算失敗？

**2. 先用 AI 對 PRD 展開 Edge Case**

AI 針對一般 test case 展開 Edge Case 的速度超快的。

**3. Start small — small is way better than null**

Test Case 鐵律：不完整的 test case 遠好過沒有。

有了 test case list，AI Coding 就可以快速幫你寫 unit test、automation test...等等，這又走到 AI 的舒適區了。

## 總結這半年的觀察

AI Coding 的進步，確實讓更多人能參與開發。工具變好用了，門檻降低了。

但核心難題沒有被解決。

那些屬於「人」的問題——需求理解、業務判斷、品質驗收——仍然需要人來負責。

**AI 很強，但真正的瓶頸，早就不在 Coding 本身。**

---

**延伸閱讀：**
- [ATPM：一套真正 Production 等級的 Vibe Coding 流程](/atpm-a-real-production-vibe-coding-process/)
- [三個月 63 萬行：AI Coding 時代工程師的價值](/claude-code-630k-lines-three-months-reflection/)
- [QA 如何驗收 AI Coding 的成果](/atpm-qa-ru-he-yan-shou-ai-coding-de-cheng-shi/)
