---
layout: post
title: "亞馬遜 AI 事故啟示：科技巨頭一邊賣 AI 未來，一邊在自己家裡給 AI 上鎖"
date: 2026-03-11 08:00:00 +0800
categories: [AI Coding, AI Security]
tags: [Amazon, AWS, AI coding incident, DataTalks.Club, Kiro, Amazon Q Developer, code review, Harness Engineering, AI 治理, 生產環境事故]
permalink: /amazon-ai-code-incident-tech-giants-quietly-locking-ai/
image: /assets/images/amazon-ai-incident-ft-report.jpeg
description: "AWS 工程師讓 AI 修一個小 bug，AI 的解法是刪掉整個生產環境再重建，恢復花了 13 小時。電商部門的 AI 變更導致數百萬筆訂單丟失。DataTalks.Club 創辦人被 AI 刪掉整個資料庫。三起事件，同一個模式。現在亞馬遜的補救措施是：禁止初中級工程師提交 AI 生成的程式碼。這不是 AI 不行——是沒有護欄的 AI 不行。"
---

![Financial Times 報導：亞馬遜電商部門因 AI coding 工具引發連串事故，緊急召集工程師開會](/assets/images/amazon-ai-incident-ft-report.jpeg)

## 發生了什麼事

亞馬遜出大事了。

電商部門緊急召集所有工程師開會。原因不是外部攻擊，不是競爭對手搞事。

是他們自己開發的 AI，正在把系統搞垮。

內部備忘錄承認，最近事故頻發，而且是「高爆炸半徑」（high blast radius）的事故。

根本原因？備忘錄寫得很清楚：**「生成式 AI 輔助的變更」（Generative AI-assisted changes）。**

翻譯成人話：工程師用 AI 工具生成的程式碼，直接把生產環境炸了。

不是一次。是頻發。

---

## 13 小時的代價

最驚人的一幕發生在 AWS 雲服務。

工程師讓 AI 代碼工具修復一個小問題。一個普通的 bug fix。

結果 AI 的解決方案是：**直接刪掉整個生產環境，再重新建一個。**

你沒看錯。

相當於你請水電師傅修個漏水的水龍頭，他把整面牆都拆了，然後跟你說「牆重砌一面就好了」。

恢復系統，花了整整 13 個小時。

亞馬遜官方怎麼說？稱其為一次「極其有限的事件」（extremely limited incident），只影響了中國大陸的客戶。

13 小時的服務中斷，叫「極其有限」。

這個公關話術本身就值得寫一篇文章。

---

## 亞馬遜的解法：禁令

事故之後，亞馬遜的補救措施簡單粗暴：

**禁止初級和中級工程師在沒有資深工程師簽字的情況下，提交任何 AI 生成的程式碼。**

注意這個措辭——不是「建議」，不是「鼓勵」，是**禁止**。

這等於承認了一件事：**他們內部判斷，目前的 AI coding 工具產出的程式碼，不能被無條件信任。**

而且他們判斷，初中級工程師缺乏足夠的經驗來識別 AI 生成程式碼中的風險。

這不是小公司的保守。這是亞馬遜——全球最大的雲服務提供商，自己用 AI 用到出事之後，做出的決定。

---

## 不只亞馬遜：AI 刪資料的災難已經在發生

如果你覺得亞馬遜的案例是個例，那再看兩個。

### 事件一：DataTalks.Club 被 AI 刪掉整個資料庫

Alexey Grigorev 是 DataTalks.Club 的創辦人，一個在 ML 社群很有名的技術教育者。

他用 AI coding 工具協助維護專案。某次 AI 在「修復」一個問題的過程中，直接把整個資料庫刪了。

不是一張表。是整個資料庫。

這不是亞馬遜等級的公司，沒有 13 小時就能恢復的 SRE 團隊。這是一個社群專案，資料丟了就是丟了。

這個案例之所以重要，是因為它證明了一件事：**AI「刪掉重建」不是 bug，是一種行為模式。**

AI 模型在訓練過程中學到了大量「clean state」的概念。當它遇到一個複雜的修復問題時，「刪掉重來」在它的邏輯裡是一個合理的解法——乾淨、確定、沒有殘留問題。

對 AI 來說，刪掉一個資料庫跟刪掉一個暫存檔，認知成本是一樣的。它不理解「這裡面有十萬筆用戶資料」的重量。

### 事件二：亞馬遜內部——數百萬筆訂單丟失

除了 AWS 的 13 小時事故，亞馬遜內部最近還有另一起更嚴重的事件。

AI 協助的程式碼變更導致電商系統 outage，直接造成**數百萬筆訂單丟失**。

數百萬筆。

這不是「服務中斷 13 小時」的問題了。這是真金白銀的商業損失。每一筆訂單背後都是一個等著收貨的客戶、一個等著出貨的賣家、一筆等著結算的款項。

這就是為什麼電商部門會緊急召集**所有**工程師開會。不是因為一次小事故，是因為問題的嚴重程度已經到了「不能再裝沒看到」的地步。

### 兩個事件，同一個教訓

把這兩個事件跟 AWS 的事故放在一起看，模式很清楚：

| 事件 | 規模 | AI 的「解法」 | 後果 |
|------|------|--------------|------|
| DataTalks.Club | 社群專案 | 刪掉資料庫 | 資料永久丟失 |
| AWS 生產環境 | 雲服務 | 刪掉整個環境重建 | 13 小時中斷 |
| 亞馬遜電商 | 企業核心 | AI 變更導致 outage | 數百萬筆訂單丟失 |

從個人專案到全球電商平台，AI coding 的「高爆炸半徑」問題不分規模、不分場景。

差別只在於：**你承受得起多大的損失。**

---

## 這不是亞馬遜的問題，這是所有人的問題

如果你覺得「這是亞馬遜的問題，跟我無關」，那你可能低估了這件事的意義。

我在之前的文章[〈AI Coding 的第一個風險，不是模型——是你一直按「Yes」〉](/ai-coding-tool-security-risk-prompt-injection-rce/)裡就提過：

> 你什麼時候開始，把「判斷」也一起自動化了？

亞馬遜的事故，就是這句話最極端的實例。

工程師看到 AI 生成的「解決方案」，按了 Yes。

問題是——AI 的解決方案是「刪掉整個生產環境」。這不是一個正常人類工程師會提出的方案。但在 AI coding 的流程裡，如果你已經習慣了「AI 建議 → 按 Yes → 部署」的節奏，你很容易就滑過去了。

這跟技術能力無關。這是**認知模式**的問題。

當你連續按了 50 次 Yes 都沒出事，第 51 次你還會認真看嗎？

心理學叫這個「automation complacency」（自動化自滿）。飛航安全領域研究了幾十年的問題，現在原封不動搬到了軟體工程。

---

## 為什麼「資深工程師簽字」是對的第一步

亞馬遜的禁令看起來很粗暴，但我認為方向是對的。

原因不是「資深工程師比較厲害」——雖然確實經驗更多。

真正的原因是：**這個機制強制插入了一個「人類判斷節點」。**

我在[〈Harness Engineering：Peter Steinberger 的 Control Plane 模式〉](/harness-engineering-control-plane-pattern-agent-review-loop/)裡提過 Peter Steinberger 的做法：他一個人用 Claude Code 管理上百個 PR，但每一個 PR 他都親自 review。不是因為他不信任 AI，是因為他理解**人類審查是系統的控制平面**。

亞馬遜的「資深工程師簽字」，本質上就是在 AI coding pipeline 裡加了一個 control plane。

而且這個做法暗合了我們在[〈混沌智能體〉](/agents-of-chaos-multi-agent-structural-instability/)裡討論的結論：

> **權限隔離比 Prompt Engineering 重要一百倍。**

你可以花無數時間調 prompt、微調模型、優化 system instruction。但最有效的安全措施，永遠是：**限制誰有權力按下那個按鈕。**

亞馬遜用最痛的方式，重新發現了這個原則。

---

## 但禁令不是終點

話說回來，「禁止初中級工程師提交 AI 程式碼」這個做法，長期來看有明顯的問題：

**第一，瓶頸會轉移到資深工程師身上。**

如果每一段 AI 生成的程式碼都需要 Senior 簽字，Senior 很快就會變成整個團隊的瓶頸。這跟把所有 PR 都指派給 Tech Lead review 是同一個問題——最終 Tech Lead 也會開始「快速掃過」而不是認真看。

人類的注意力是有限資源。

**第二，這會抑制初中級工程師的學習。**

AI coding 最大的價值之一，是讓初級工程師可以更快探索解決方案。如果你禁止他們用，等於是切斷了一個重要的學習管道。

**第三，禁令本身沒有解決根本問題。**

根本問題不是「誰提交程式碼」，而是**「AI 生成的變更在進入生產環境之前，經過了多少層驗證」。**

---

### 更好的做法：分級審查機制

我認為長期的解法不是禁令，而是**分級審查**。

這跟 ATPM 框架裡的 QA 驗收邏輯是一致的：

| 變更類型 | 風險等級 | 審查要求 |
|----------|----------|----------|
| 文件修改、測試補充 | 低 | AI 自動審查 + 自助提交 |
| 業務邏輯修改 | 中 | AI 審查 + 同儕 review |
| 基礎設施變更、權限修改 | 高 | AI 審查 + 資深工程師 review + 自動化測試通過 |
| 生產環境部署、資料庫 schema 變更 | 極高 | 多人簽核 + staging 驗證 + 回滾計畫 |

關鍵是：**根據變更的「爆炸半徑」來決定審查強度，而不是根據提交者的職級。**

一個資深工程師用 AI 生成的基礎設施變更，風險不會因為他資深就變小。

反過來，一個初級工程師用 AI 修改一個文件的 typo，不需要資深工程師簽字。

---

## 坦白說：答案已經有了，叫 Harness Engineering

科技巨頭們一邊向全世界推銷 AI 的未來，一邊在自己家裡悄悄給 AI 上鎖。

這聽起來很諷刺，但我覺得這反而是好事。

因為這代表他們在**真實生產環境**裡驗證了 AI 的能力邊界。不是在實驗室，不是在 benchmark，是在影響真實客戶的系統裡。

我自己用 Claude Code 寫了 63 萬行程式碼，經歷過各種 AI「脫韁」的時刻。所以我完全理解亞馬遜為什麼會下禁令。

但我也知道，禁令只是止血。真正的解法，其實已經有人做出來了。

OpenAI 自己的工程團隊，3 個人、5 個月、100 萬行代碼、0 行人寫。他們把這套方法叫 **[Harness Engineering](/harness-engineering-control-plane-pattern-agent-review-loop/)**。

核心哲學八個字：**Humans steer. Agents execute.**（人類掌舵，Agent 執行。）

注意——不是「人類禁止 Agent」，也不是「Agent 自由奔跑」。是**人類建好框架，Agent 在框架裡全速運轉**。

亞馬遜的問題，說穿了就是：Agent 在全速奔跑，但框架沒建好。

Harness Engineering 的做法跟亞馬遜的禁令形成了完美對比：

| | 亞馬遜的禁令 | Harness Engineering |
|---|---|---|
| **策略** | 限制人（禁止初中級提交） | 限制變更（用架構約束框住 Agent） |
| **護欄** | 資深工程師人工簽字 | 自動化 linter + preflight gate + CI 攔截 |
| **速度** | 降速（人工瓶頸） | 加速（Agent 犯錯時，修復指令自動注入 context） |
| **學習** | 切斷初級工程師學習管道 | Agent 每次犯錯都會被框架糾正，越跑越穩 |
| **擴展性** | 資深工程師成為瓶頸 | Peter Steinberger 一人一天 627 次提交 |

Peter Steinberger 一個人用 Claude Code 管理上百個 PR，每個都過 review。他不是用「禁令」控制 AI，而是用**控制平面**（control plane）接住 AI 的高速產出——risk tier contract 分級風險、preflight gate 自動攔截危險變更、remediation loop 自動修復偏差。

如果亞馬遜的 AWS 團隊有這套機制，AI 提出「刪掉整個生產環境」的那一刻，preflight gate 就會直接攔下來。根本不會等到人類按 Yes。

**禁令是用人的注意力當護欄。Harness Engineering 是用系統的架構當護欄。**

人的注意力會疲勞、會自滿、會在連續按 50 次 Yes 之後麻木。

系統的架構不會。

所以我的結論是：

亞馬遜的禁令方向對了——承認 AI 需要護欄。但解法選錯了——用人去擋，而不是用系統去接。

2026 年企業 AI coding 落地最重要的課題，不是「AI 能不能用」，不是「誰可以用」，而是：

**你的 repo 準備好接住 Agent 了嗎？**

這才是 Harness Engineering 真正在回答的問題。

---

## 常見問題 Q&A

**Q: 亞馬遜是不是要放棄 AI coding？**

不是。禁令的對象是「無人審查的 AI 程式碼提交」，不是 AI coding 本身。亞馬遜依然在大規模投資 AI 開發工具（包括 Amazon Q Developer）。禁令的邏輯是「加護欄」，不是「關掉引擎」。

**Q: 這個事故是不是代表 AI 寫的 code 不可靠？**

不完全是。AI 寫的 code 跟人類寫的 code 一樣，都需要 review。問題不在 AI 的能力，在於「誰決定這段 code 可以進 production」。人類寫的爛 code 一樣會炸——差別是 AI 可以用極快的速度產出大量有風險的變更，如果沒有審查機制，爆炸半徑會被放大。

**Q: 小公司也需要這種分級審查嗎？**

需要，但規模可以不同。核心原則是一樣的：**任何涉及基礎設施、權限、生產環境的變更，不管是人寫的還是 AI 寫的，都應該有第二雙眼睛看過。** 小公司可能只需要一個簡單的 PR review 流程，大公司需要更正式的簽核制度。

**Q: 我是初級工程師，公司禁止我用 AI coding，該怎麼辦？**

先理解公司的顧慮。然後用 AI 來學習而不是直接提交——讓 AI 幫你理解 codebase、解釋錯誤訊息、探索不同解法。把 AI 當導師而不是代筆者。當你展示出足夠的判斷力，限制自然會放鬆。

---

## 延伸閱讀

- [AI Coding 的第一個風險，不是模型——是你一直按「Yes」](/ai-coding-tool-security-risk-prompt-injection-rce/)
- [混沌智能體：史丹佛 x 哈佛的論文告訴我們，控制好一個 AI Agent 不等於控制好一群](/agents-of-chaos-multi-agent-structural-instability/)
- [Harness Engineering：Peter Steinberger 的 Control Plane 模式](/harness-engineering-control-plane-pattern-agent-review-loop/)
- [AI Coding 半年回顧：開發並沒有變快，我們只是把瓶頸從寫 Code，轉移到了 QA 跟需求收集](/ai-coding-half-year-review-demand-transformation-tool-evolution/)
- [AI Agent 安全性：遊戲規則已經改變](/ai-agent-security-you-xi-gui-ze-yi-jing-gai-bian/)
