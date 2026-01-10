---
layout: post
title: "AI 治理是什麼？當 AI 不再只是工具，企業責任該怎麼設計"
date: 2026-01-10
permalink: /ai-governance-not-it-problem/
image: /assets/images/ai-security-governance-cover.png
description: "AI 治理不是模型或資安工具問題，而是企業責任與決策權的設計。當 AI 成為數位員工，誰授權、誰負責、如何問責，成為治理的核心挑戰。"
categories: [AI治理]
tags: [AI治理, AI資安, 企業治理, 數位員工, AI問責]
---

# AI 治理是什麼？當 AI 不再只是工具，企業責任該怎麼設計

## 當「數位員工」出事時，這不是 IT 問題，而是治理問題

這一週，我連續寫了好幾篇關於 AI 資安的文章。有人私下問我：「是不是最近特別在意資安？」

其實不是。

因為這從一開始就不是資安的問題。而是當第一個「數位員工」被正式納入組織體系之後，治理卻仍停留在「工具與系統」時代，所產生的結構性落差。

AI 會讀資料、會做判斷、會執行行為。而任何被授權行動的存在，都不該只用 IT 的語言來理解。

這是一個治理問題。

---

## AI 正在逼組織做選擇

過去，資安出事，通常有一條相對清楚的責任歸屬：

- 系統被駭了，是 IT 的問題
- 權限開太大，是設定失誤
- 資料外洩，是流程沒有被遵守

修補、檢討、寫報告，事情就算告一段落。

但 AI 出現之後，這條責任邊界第一次開始變得模糊。

因為 AI 不再只是「工具」，而是一個**數位員工**——能讀資料、能做判斷、能執行行為。

![數位員工概念](/assets/images/ai-digital-employee-concept.png)

而對於員工，靠的從來不是 IT，而是治理。

真正的問題是——**出事的那一刻，責任該落在哪裡？**

---

## 為什麼這些問題，IT 回答不了

這幾篇文章，其實已經把能討論的層次幾乎都走過一遍：

- [AI Agent 的行為模式已經改變](ai-agent-security-you-xi-gui-ze-yi-jing-gai-bian.md)——Guardrails 註定擋不住語言層面的攻擊
- [AI Guardrails 為什麼註定失敗？](openai-dou-dang-bu-zhu-de-gong-ji-ai-an-quan-fang-tan.md)——連 OpenAI 都擋不住的攻擊，你的防護能擋住嗎？
- [用 PostgreSQL 實作 CaMeL 架構](camel-postgresql-implementation-memory-permission-db-layer.md)——CaMeL 把「讀資料」與「做動作」徹底分開，用 RLS 讓某些事「技術上做不到」
- [FDE 模式能幫你看見真實的流程與組織圖](least-privilege-fde-shadow-it-shadow-ai.md)——政策與現實的永恆落差
- [失控不是假設，是已經發生的事](ai-digital-anchor-prompt-injection-meow.md)——數字人主播在直播中突然學貓叫
- [法律已經到門口](taiwan-ai-basic-act-engineering-perspective.md)——AI 基本法正式把「問責」寫進條文
- [資安從來不是絕對安全，而是平衡](ai-security-balance-not-absolute.md)——效率、成本、風險之間的永恆取捨

從工具失效（Guardrails 擋不住）、到架構設計（CaMeL 讀寫分離）、到現場實務（影子 AI 為什麼一定會出現）、到真實案例（數字人主播學貓叫）、再到法規壓力（AI 基本法問責條款）——每一篇文章都在處理一個具體的面向。

但寫到這裡，我越來越清楚一件事：**如果沒有治理，這些討論永遠拼不起來。**

因為在 AI 時代，問題不再只是：

- 哪一個模型出錯
- 哪一行程式寫得不好
- 哪一條 policy 沒有遵守

而是更根本的問題：

> **AI 出事時，問題不再只是「哪裡壞了」，而是「誰允許它這樣做」。**

這不是 IT 能單獨回答的問題。因為 IT 從來沒有被授權，去定義這些邊界。

---

## AI 資安，本質上是一個治理設計問題

如果把視角拉到組織治理的語言，其實不管是企業治理、IT 治理，還是近年開始成形的 AI 治理，外部成熟框架大多都圍繞幾個核心面向在運作：

- **責任歸屬（Accountability）**
- **決策權配置（Decision Rights）**
- **風險承擔與容忍度（Risk Appetite）**
- **控制與約束（Controls & Constraints）**
- **透明度與可審計性（Transparency & Auditability）**
- **合規與外部責任（Compliance & Liability）**

這些概念並不新，也不是專為 AI 發明的。真正的變化在於——**AI 讓這些治理問題第一次同時被放大、被具體化，而且無法再模糊帶過。**

也正因如此，在 AI 時代，資安真正的核心不在於：

- 使用哪一個模型
- 採購哪一套工具
- 是否加上 guardrail
- policy 文件寫得多完整

而在於**三個必須被清楚定義的治理問題**。

---

## 三個必須被清楚定義的治理問題

![三個治理問題](/assets/images/ai-governance-three-questions.png)

### 第一，哪些行為必須保留在人類決策層？

**（Decision Rights / Accountability）**

AI 到底是顧問，還是代理人？哪些行為只能建議，哪些才被允許執行？

這就是為什麼 [CaMeL 架構](camel-postgresql-implementation-memory-permission-db-layer.md) 要把「讀資料」和「做動作」徹底分開——因為有些事情，AI 可以建議，但不能執行。

![CaMeL 讀寫分離](/assets/images/ai-camel-read-write-separation.png)

### 第二，哪些AI可能錯誤是組織選擇承擔的？

**（Risk Appetite / Accountability）**

如果風險從來沒有被治理層承認，它就一定會以 [影子 AI](least-privilege-fde-shadow-it-shadow-ai.md) 或失控的形式出現。

![影子 AI 風險](/assets/images/ai-shadow-ai-risk.png)

如果連實驗都不允許，影子 AI 一定會出現；如果什麼都放行，那失控只是時間問題。

### 第三，哪些AI行為必須在流程系統上被禁止？

**（Controls / Auditability）**

如果某件事在治理上被認定「不能發生」，那它就不該只靠 SOP，而是要在技術上做不到。

[CaMeL](camel-postgresql-implementation-memory-permission-db-layer.md)、PostgresSQL RLS、權限分層、審計設計，其實都不是在「防 AI」，而是在**具體化這三個治理決策**。

![控制與審計設計](/assets/images/ai-controls-rls-audit.png)

---

## 真正的風險，是治理真空

AI 不會等待治理成熟；[法律](taiwan-ai-basic-act-engineering-perspective.md)也不會接受「我們還在研究」作為理由。

真正的風險，從來不是 AI 太快，而是組織遲遲不願意定義責任邊界。

---

## 這個系列的完整文章

如果你想深入了解每個面向，以下是完整的系列文章：

| 主題 | 核心問題 |
|------|---------|
| [AI Agent 安全性：遊戲規則已經改變](ai-agent-security-you-xi-gui-ze-yi-jing-gai-bian.md) | 為什麼 Guardrails 註定擋不住？ |
| [AI Guardrails 為什麼註定失敗？](openai-dou-dang-bu-zhu-de-gong-ji-ai-an-quan-fang-tan.md) | 連 OpenAI 都擋不住的攻擊 |
| [CaMeL + PostgreSQL：當記憶與權限都在資料庫層實現](camel-postgresql-implementation-memory-permission-db-layer.md) | 如何讓某些事「技術上做不到」？ |
| [最小權限的現實：為什麼現場總是長出影子 AI](least-privilege-fde-shadow-it-shadow-ai.md) | 為什麼政策永遠被繞過？ |
| [數字人主播學貓叫：一場 Prompt Injection 的現場直播](ai-digital-anchor-prompt-injection-meow.md) | AI 失控可以有多荒謬？ |
| [台灣 AI 基本法：工程師視角的解讀](taiwan-ai-basic-act-engineering-perspective.md) | 法律如何定義 AI 的責任？ |
| [AI Coding 工具的資安風險](ai-coding-tool-security-risk-prompt-injection-rce.md) | 開發工具本身的風險在哪？ |
| [AI 時代的資安平衡](ai-security-balance-not-absolute.md) | 資安的本質是什麼？ |

---

## Appendix：給董事會 / 風控的 AI 治理檢核清單

以下不是技術清單，而是一份**治理成熟度的自我檢查**。

### 一、責任與決策權

- AI 出事時，最終責任人是誰？
- 哪些行為 AI 只能建議，哪些可以執行？
- 是否存在明確禁止 AI 自主決策的行為清單？

### 二、風險承擔與試錯邊界

- 哪些錯誤是可接受的？哪些是不可承受的？
- 是否承認 AI 導入必然伴隨試錯成本？
- 是否已經出現影子 AI？

### 三、控制是否真正落到系統層

- 被禁止的行為，是靠制度，還是技術上做不到？
- 是否假設人一定會遵守流程，而非流程一定會被繞過？

### 四、透明度與可審計性

- 能否還原 AI 使用了哪些資料、做了哪些判斷？
- 是否具備不可變造的審計軌跡？

### 五、對外責任與合規準備度

- 是否能對監管機關、客戶、董事會清楚交代？
- 是否仍假設「不知道」可以免責？

---

## 常見問題 Q&A

**Q: AI 資安跟傳統資安有什麼不同？**

傳統資安防的是「系統漏洞」和「人為疏失」，邊界相對清楚。AI 資安面對的是一個會自己做判斷、執行行為的「數位員工」——攻擊面從技術層擴展到語言層，責任歸屬也從 IT 延伸到組織治理。

**Q: 為什麼說 Guardrails 擋不住 AI 攻擊？**

因為 AI 的攻擊面是「語言本身」。多語種混雜、上下文誘導、角色扮演等攻擊方式，組合可能性幾乎無限。連 OpenAI 自己的防護都會被繞過，靠單一工具防禦是不夠的。

**Q: 中小企業沒有資源做完整的 AI 治理，該怎麼辦？**

不需要一步到位。先從三個問題開始：（1）哪些事 AI 絕對不能自己決定？（2）出事時誰負責？（3）有沒有辦法事後還原 AI 做了什麼？能回答這三個問題，就已經比大多數企業走得更前面。

**Q: 影子 AI 是什麼？為什麼會出現？**

影子 AI 是指員工未經公司授權，私下使用 AI 工具處理工作。出現的原因通常是：官方政策太嚴格、審批流程太慢、或根本沒有提供合適的 AI 工具。當效率需求與合規要求衝突時，影子 AI 幾乎必然出現。

**Q: 台灣 AI 基本法對企業有什麼影響？**

AI 基本法正式把「問責」寫進法律。這意味著「我們不知道 AI 會這樣做」將不再是有效的免責理由。企業必須能夠說明：誰授權 AI 做這件事、AI 用了哪些資料、為什麼會產生這個結果。

---

**關於作者：**

Wisely Chen，NeuroBrain Dynamics Inc. 研發長，20+ 年 IT 產業經驗。曾任 Google 雲端顧問、永聯物流 VP of Data&AI、艾立運能數據長。專注於傳統產業 AI 轉型與 Agent 導入的實戰經驗分享。

---

**相關連結：**
- 部落格首頁：https://ai-coding.wiselychen.com
- LinkedIn：https://www.linkedin.com/in/wisely-chen-38033a5b/
