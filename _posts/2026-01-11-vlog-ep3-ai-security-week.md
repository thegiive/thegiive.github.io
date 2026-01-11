---
layout: post
title: "Vlog EP3：AI 資安週 — Guardrail 是假的，CaMeL 才是真的？"
date: 2026-01-11
description: "這週我深入研究了 AI Agent 資安議題。從 OpenAI Red Team 專家的訪談開始，到 Google 的 CaMeL 架構，再到企業導入 AI 時的資安平衡問題。結論是：AI 資安已經不是 IT 問題，而是企業治理問題。"
image: /assets/images/vlog-ep3-ai-security-week-cover.png
categories: [AI 資訊安全, AI Agent, Vlog]
tags: [Prompt Injection, CaMeL, Guardrail, 最小權限原則, Shadow AI, 企業治理]
permalink: /vlog-ep3-ai-security-week/
youtube: https://youtu.be/nxJos56z0jg
---

這週是我的「AI 資安週」。

從週一到週六，我幾乎每天都在研究 AI Agent 的資安問題。不是因為我想轉職做資安，而是因為我發現：**如果不搞懂這個問題，企業 AI Agent 落地這件事根本走不下去。**

## 起點：OpenAI Red Team 大神說 Guardrail 沒用

週一的時候，我看了一個 YouTube 訪談。

受訪者是幫 OpenAI 做 Red Team 的資安專家。他的結論很直接：

> 現在大家最常用的 Guardrail（護欄），就是在大語言模型的 Input 和 Output 前後加上 Rule-based 的過濾機制，**這種方式根本做不到防護。**

為什麼？

因為 Prompt Injection 是「語言等級」的攻擊。語言本身就是一個接近無限的攻擊向量。你用有限的規則去擋無限的語言變化，這是不可能贏的戰爭。

這讓我想到之前寫的那篇 [AI Agent Security：遊戲規則已經改變](/ai-agent-security-game-changed/)，裡面提到的 ForcedLeak 和 EchoLeak 攻擊。**傳統的 WAF 和 APM 對這些攻擊根本沒轍。**

## CaMeL：Google 提出的雙層 Agent 架構

那位 Red Team 專家推薦了一個他認為「目前最有機會解決 Prompt Injection」的方案：Google 的 CaMeL 架構。它的核心概念其實很簡單：

**讀寫分離 + 權限隔離**

中間有一個關鍵步驟：**Sanitize（淨化）**。

低權限 Agent 接觸原始的、可能被污染的資料。高權限 Agent 永遠不直接接觸原始 Input，只處理經過淨化的結果。

這樣即使 Prompt Injection 成功注入到低權限 Agent，它也沒有執行權限。而高權限 Agent 拿到的資料已經被清洗過，惡意指令被移除了。

## 週四實作：用 PostgreSQL 實現權限隔離

看完 Paper 之後，我就想：這東西能不能在實務上做出來？

週四的時候，我試著用 PostgreSQL 在資料庫層面實作這個架構。主要是：

1. **Row Level Security (RLS)**：讓不同的 Agent 只能存取特定的資料
2. **讀寫分離的 DB User**：Read Agent 用唯讀帳號，Write Agent 用另一個有限寫入權限的帳號
3. **Audit Log**：所有操作都要有 trace

這讓我想到資安的黃金法則：**最小權限原則（Principle of Least Privilege）**。

## 最小權限原則的盲點：你根本不知道「真正的流程」

但這裡有一個我在顧問工作中反覆看到的問題：

**官方組織圖和官方流程是一回事，真實組織圖和真實流程是另一回事。**

很多資安顧問公司進去做最小權限設計，都是根據「官方流程」來設計的。但實際上，公司內部有大量的「影子流程」——那些沒有被文件化、但大家每天都在做的事情。

如果你的最小權限設計沒有考慮到這些真實流程，會發生什麼事？

**大家會繞過去。**

然後就產生了所謂的 Shadow IT。現在更嚴重的是 **Shadow AI**——員工自己帶 AI 工具進公司，因為公司提供的「安全版 AI」太難用了。

這反而造成更大的資安缺口。

## 資安的本質：效率與安全的平衡

週五的時候，我整理了這週的思考，得出一個結論：

> AI 時代的資安，不是追求「絕對安全」，而是追求「效率與安全的平衡」。

一位前輩跟我說過：

> 如果你把 AI 封鎖得太死，員工會自己想辦法。他們會用私人的 ChatGPT、用未經授權的工具。因為他們知道，用 AI 的人效率可能是不用的人的 2-3 倍。為了升官加薪、為了贏過同事，他們一定會找方法。

所以真正的問題不是「要不要用 AI」，而是：

**你怎麼設計一個讓大家願意用、而且是可控的 AI 環境？**

## 三個企業治理層必須回答的問題

到了週六，我把這週的思考整理成三個核心問題：

### 問題一：AI 是顧問，還是數位員工？

你要把 AI 定位成：

- **顧問角色**：只能詢問、提供建議，最後決策是人
- **數位員工**：可以在 Business Process 中主動執行任務

前者比較安全，這也是大家比較熟悉的。但後者可能帶來 10 倍、100 倍、甚至 1000 倍的效率提升。

這不是一個非黑即白的選擇，可能是某種灰色地帶。但企業主和治理層必須做出決定。

### 問題二：你願意承擔多少資安風險？

如果你選擇讓 AI Agent 進入流程，一定會有資安風險。

問題是：**哪些風險是你可以承擔的？**

你需要設計出「最小可承擔的資安風險」，然後把周邊的配套措施都設計好。這包括：

- 如果出事了，損失範圍在哪裡？
- 有沒有快速止血的機制？
- 責任歸屬怎麼設計？

### 問題三：如何在系統層面確保 AI 不越界？

當你已經區分出「可控範圍」和「禁區」之後，怎麼用技術手段確保 AI Agent 不會越界？

這就是 CaMeL 這類架構要解決的問題。包括：

- 權限隔離
- 讀寫分離
- 資料淨化
- 稽核日誌

## 結論：AI 資安是企業治理問題，不是 IT 問題

這週最大的體悟是：

**AI Agent 的資安問題，已經脫離了傳統「系統層面」的資安範疇。**

因為 AI Agent 本質上是「數位員工」。它可以無縫地嵌入企業流程，取代某些人工作業。

所以我們不能只用系統的角度來處理這件事。我們需要用**企業治理**的方式來思考：

- 怎麼把 AI 這個「員工」納入企業流程？
- 怎麼像對待員工一樣去管理它？
- 怎麼設計它的權限、責任、和問責機制？

這三個問題不回答清楚，其他的工具面、資料設計面、流程面、組織面的問題都沒辦法回答。

---

## 這週的影片

這是完整的週報影片：

{% include youtube.html id="nxJos56z0jg" %}

---

## 相關閱讀

- [AI Agent Security：遊戲規則已經改變](/ai-agent-security-game-changed/)
- [PostgreSQL 作為 AI Memory Store 的務實選擇](/postgresql-vector-store-pragmatic-choice/)
- [最小權限原則與 Shadow AI 的矛盾](/least-privilege-fde-shadow-it-shadow-ai/)

---

## Q&A

**Q: Guardrail 真的完全沒用嗎？**

不是完全沒用，而是「不夠用」。Guardrail 可以擋掉一些簡單的攻擊，但對於精心設計的 Prompt Injection，它的防護能力有限。我的看法是：Guardrail 是第一道防線，但你不能只靠它。

**Q: CaMeL 架構有什麼缺點？**

主要是複雜度增加。你需要維護兩個 Agent、設計淨化邏輯、處理兩者之間的通訊。對於簡單的應用場景，可能 overkill。但對於高風險的企業應用，這個投資是值得的。

**Q: Shadow AI 問題怎麼解決？**

核心不是「禁止」，而是「提供更好的替代方案」。如果你提供的企業 AI 工具好用、又夠安全，員工自然會用。如果太難用，他們一定會找其他方法。這是人性。

---

*這是 Vlog 系列的第三集。每週我會把這一週學到的東西、做的專案、踩的坑整理成一個總結。如果你覺得有幫助，歡迎訂閱我的 [YouTube 頻道](https://www.youtube.com/@anthropic-ai)。*
