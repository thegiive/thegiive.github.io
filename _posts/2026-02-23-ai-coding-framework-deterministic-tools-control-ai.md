---
layout: post
title: "AI Coding 時代，工程師的核心工作是搭框架讓 AI 不失控"
date: 2026-02-23 08:00:00 +0800
categories: [AI Coding, Agent Engineering]
tags: [ai-coding, ci-cd, test, lint, llm-judge, harness-engineering, entropy-management, code-review, automation]
permalink: /ai-coding-framework-deterministic-tools-control-ai/
image: /assets/images/peter-steinberger-50-codex-pr-review.png
description: "大家都不寫代碼了，但代碼量暴增 10 倍。真正的問題變成：怎麼讓 AI 寫的代碼不爆炸？答案不是更好的 prompt，而是用 CI、test、lint、automation、甚至用另一個 LLM 來做高速 review。從 OpenAI 3 人 100 萬行實驗、到我自己帶 Agent 寫支付後端的踩坑筆記，這篇講的是：確定性工具如何框住不確定性的 AI。"
---

Peter Steinberger（[@steipete](https://x.com/steipete)）最近分享了一個場景，很能說明現在工程方式變成什麼樣了：OpenClaw Github PR 量大到現有工具都撐不住，他直接開 50 個 Codex 並行跑，讓每個 Codex 分析一個 PR，產出包含 vision、intent、risk 等多維度信號的 JSON 報告。然後把所有報告匯入同一個 session，用 AI 做 de-dupe、auto-close、auto-merge。兩天處理 8 個 auto-update PR，目標是消化 3000 個積壓 PR。

**人不寫代碼了。人設計審代碼的框架。**

---

## 問題：代碼量 10 倍，review 速度不變

先說數字。

OpenAI 二月初發了篇[工程博客](https://openai.com/index/harness-engineering/)。3 個工程師用 Codex Agent，5 個月，寫了 100 萬行代碼。合併了 1500 個 PR。每人每天 3.5 個 PR。每一行都是 Agent 生成的。

GitHub 的數據也說了，用了 Copilot 之後 PR 數量漲了 98%。但審查時間也漲了 91%。Addy Osmani 管這叫「生產力悖論」——**產出是快了，但人類消化不了。**

3.5 個 PR/人/天，人根本審不過來。但你不審，質量就沒人兜底。審了，你就變成整個流水線上最慢的那一段。

所以核心問題不是「AI 寫的代碼好不好」，而是：**誰來做高速 review？怎麼做？**

---

## 解法：用確定性工具框住不確定性的 AI

答案其實不新。就是 CI 那套東西。但用法變了。

以前 CI 是「最後一道防線」——代碼寫完了，推上去，CI 跑一遍，有問題再改。

現在 CI 是 **「第一道教練」**。AI 生成代碼的瞬間，確定性工具就要介入。不是等人來看，而是讓機器先過一輪。

具體有哪些手段：

### 1. Test — 最硬的護欄

測試是唯一能給出「對或錯」明確答案的東西。

AI 生成的代碼跑不過測試？不用人看，直接打回。跑過了？至少基本邏輯沒崩。

OpenAI 那個 3 人團隊的做法是：**先讓 Agent 寫測試，再讓 Agent 寫實現。** 測試本身就是規範。如果測試寫對了，Agent 寫的代碼只要通過測試，大方向就不會偏太遠。

我自己在支付系統裡的體感也一樣。我現在花在寫測試規範上的時間比寫 prompt 多得多。因為 prompt 是模糊的，但測試是確定的。Agent 可以幻覺，但 `assert balance == expected_balance` 不會騙你。

**80% 的 Agent 代碼質量取決於你的測試覆蓋率，20% 才是 prompt 寫得好不好。**

### 2. Lint — Agent 的即時教練

傳統的 lint 報錯是給人看的。「第 42 行縮進不對」，人看一眼就知道怎麼改。但對 Agent 來說，很多 lint 報錯信息不夠清晰。

OpenAI 做了一個很巧的事：寫了一堆自定義 lint 規則，**每條規則的報錯信息裡直接嵌修復指令。** Agent 犯錯的瞬間，怎麼改已經注入它的上下文了。

工具鏈本身變成了 Agent 的教練。

這跟我在 Claude Code 裡用 hooks 的體驗很像。PreCommit hook 裡跑 lint + type check，Agent 推代碼的瞬間就被攔住。它不需要人告訴它「這裡有問題」，CI 會告訴它。

### 3. Automation — 結構化的 CI Gate

OpenAI 把整個 review 流程自動化了。Agent 自己拉反饋、回覆評論、推更新、squash merge。質量保障從「人盯」轉向「機器 gate」。

CI 流水線裡的每一個 gate 都是一個確定性的判斷：

- Type check 過了嗎？
- 單元測試通過了嗎？
- Lint 規則符合嗎？
- 覆蓋率有下降嗎？
- 安全掃描有報警嗎？

這些都是**確定性的**。不需要人判斷，機器就能給出 pass/fail。

Agent 產出速度快 10 倍，你的 CI gate 也能 10 倍速運行。**確定性工具的速度天然匹配 AI 的產出速度。** 這是人做不到的。

### 4. LLM Judge — 用另一個 AI 審 AI

確定性工具能框住的範圍有限。測試能抓邏輯錯誤，lint 能抓風格問題，但「設計合不合理」「有沒有安全漏洞」「業務邏輯對不對」——這些需要語義理解。所以第四道防線：用另一個 LLM 做 judge。

我自己 POC 試過三維並行 code review，三個 Agent 分別扮演BU審計、架構師、安全專家，同一段代碼三個維度同時審。交叉覆蓋率極低——金融審計找到 N+1 查詢和缺鎖問題，架構師發現死代碼和殘留字段，安全專家揪出負餘額檢查缺失、跨租戶數據泄露、競態條件三個高危。修完跑第二輪又冒出兩個高危。**修復本身也會引入問題，所以 LLM judge 不是跑一次就夠，要循環跑。**

Anthropic 也在推這個思路。用 Opus 做 Security Check，用不同的 model 做不同維度的審查。

但這裡有一個我到現在沒完全想通的問題：**用 LLM 審 LLM 寫的代碼，權責分離怎麼做？** 撰寫和審查用同一個模型家族，系統性偏差無法被捕捉。這在金融場景是個大問題。

---

## 四層防禦架構

整理一下，現在 Agent 時代的代碼質量保障，大概是這四層：

| 層級 | 手段 | 特性 | 速度 |
|------|------|------|------|
| **第一層** | Test（單元/整合/E2E） | 確定性，邏輯正確性 | 秒級 |
| **第二層** | Lint + Type Check | 確定性，風格+類型安全 | 秒級 |
| **第三層** | CI Gate（覆蓋率/安全掃描） | 確定性，結構化指標 | 分鐘級 |
| **第四層** | LLM Judge（多角色 review） | 非確定性，語義理解 | 分鐘級 |

前三層是確定性的——跑出來就是 pass 或 fail，不需要人判斷。第四層是非確定性的，但可以通過多角色、多模型來降低偏差。

人在哪裡？**人在這四層之上。**

人不再逐行看代碼。人的工作是：設計這四層的規則、調整 lint 配置、寫測試規範、定義 LLM judge 的角色和標準。

**從裁判變成了規則制定者。**

---

## 壞模式會被 10 倍速複製

為什麼這個框架這麼重要？因為 Agent 有一個特性：**它會忠實地複製已有模式。好的壞的都複製。**

OpenAI 特別強調了這點。如果代碼庫裡已經有一個反模式——比如雙路徑寫入同一張表但用不同 ID 解析策略——Agent 會毫不猶豫地學著寫。而且以 10 倍速度擴散。

OpenAI 把這叫 **Entropy Management**。搞了一套「垃圾回收」機制：定期跑 Agent 巡檢代碼庫，發現文檔不一致和架構違規就報告。CI gate 在入口處攔截 entropy，不讓壞模式進入主幹。

**在 Agent 寫代碼的時代，代碼腐敗的速度也是 10 倍的。對抗 entropy 不是可選項，是必須項。**

---

## 上下文也需要工程化

光有 CI 護欄還不夠。Agent 寫代碼的質量還取決於另一個東西：**你餵給它的上下文。**

研究顯示上下文中間部分的召回率比頭尾低 10-40%（Lost-in-Middle），一個錯誤輸出會被後續檢索反覆引用越滾越大（Context Poisoning），甚至只混進一個無關文檔就會拉低整體推理質量（Context Distraction）。簡單說：**塞越多不等於越好，塞錯了反而更糟。**

好的 Agent 設計不是給它更多信息，而是**在正確的時間給正確的信息**。這也是一種確定性：你控制了它能看到什麼，就控制了它的行為邊界。

---

## 坦白說

我的觀察可能有偏差。但有幾件事我比較確定：

**確定的部分：**

1. **80/20 法則翻轉了。** 以前 80% 的時間在寫代碼，20% 在搭環境。現在 80% 的時間在搭護欄（test、lint、CI gate、LLM judge、CLAUDE.md），20% 在跟 Agent 互動。

2. **確定性工具是核心。** 在一切都不確定的 AI 時代，test 和 lint 這些老東西反而成了最值錢的資產。因為它們是唯一能給出明確 pass/fail 的東西。你的 test case 和 automation test 不是負債，是越來越黃金的資產——Agent 產出越快，能自動驗證的測試就越值錢。

3. **Entropy Management 是真的。** 我親眼看到一個反模式在兩天內被 Agent 複製到四個 module。沒有 CI gate，代碼庫會以 10 倍速腐敗。

4. **LLM Judge 有用但有限。** 多角色 review 確實能抓到人類單視角抓不到的問題，但權責分離和系統性偏差的問題還沒解。

**不確定的部分：**

1. **護欄會不會變成過度工程？** 搭太多框架反而限制了靈活性，這個平衡點還沒找到。

2. **用 LLM 審 LLM 的上限在哪？** 同一個模型家族的盲點是相關的，能不能用不同家族的模型交叉審查來解決？需要更多實驗。

3. **這套框架對小團隊的成本效益如何？** OpenAI 有資源搭完整的 CI 體系，但 2-3 人的 startup 搭到什麼程度才算夠？

---

## 不是結論

回到開頭的問題。AI Coding 時代，工程師到底在做什麼？

**在搭框架。**

用確定性的東西（test、lint、CI gate）框住不確定性的 AI（LLM 生成的代碼）。用高速自動化（automation）匹配 AI 的產出速度。用另一個 AI（LLM judge）補上確定性工具覆蓋不到的語義層。

這不是什麼新發明。CI/CD 這套東西二十年前就有了。但在 Agent 時代，它的角色從「最後一道防線」變成了「整個系統的骨架」。

以前管理人類工程師團隊的時候，有個說法叫「文化吃掉戰略」。

現在管理 Agent 團隊：**確定性吃掉不確定性。**

你的 test 有多硬，你的 AI 就能跑多快。

---

**延伸閱讀：**
- [三個月 63 萬行之後：在 AI Coding 時代，工程師真正的價值是什麼？](/claude-code-630k-lines-three-months-reflection/)
- [AI Coding 半年回顧：開發並沒有變快，我們只是把瓶頸從寫 Code，轉移到了 QA 跟需求收集](/ai-coding-half-year-review-demand-transformation-tool-evolution/)
- [Cursor 前 0.01% 大神倒戈 Claude Code：Agentic Coding 五大支柱完整解析](/cursor-top-user-switch-claude-code-agentic-coding/)
- [從「套殼 1.0」到「套殼 2.0」：為什麼真正該緊張的是 Anthropic](/shell-wrapper-2-anthropic-real-threat/)
