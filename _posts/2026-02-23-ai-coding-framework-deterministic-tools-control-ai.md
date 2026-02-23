---
layout: post
title: "當代碼量暴增 10 倍後，到底誰來做 Review？Make CI/CD Great Again"
date: 2026-02-23 08:00:00 +0800
categories: [AI Coding, Agent Engineering]
tags: [ai-coding, ci-cd, test, lint, llm-judge, harness-engineering, entropy-management, code-review, automation, make-cicd-great-again]
permalink: /ai-coding-framework-deterministic-tools-control-ai/
image: /assets/images/peter-steinberger-50-codex-pr-review.png
description: "OpenClaw 作者 Peter Steinberger 開 50 個 Codex 並行審 3000 個 PR。OpenAI 3 個工程師 5 個月產出 100 萬行代碼。Stripe 一週 1000 個 PR。GitHub 數據：PR 量漲 98%，審查時間漲 91%。AI 產出極快，但人類根本消化不了。真正的解法不是更好的 Prompt，而是 20 年前的老朋友——CI/CD。你的 testing case 寫得越多、越齊全，這是一個看漲的資產。"
---

OpenClaw 作者 Peter Steinberger（[@steipete](https://x.com/steipete)）最近分享了一個場景，很能說明現在軟體工程變成什麼樣了。

我們都知道 OpenClaw 大流行。GitHub PR 量大到任何現有團隊跟工具都撐不住——3000 多個 PR 積壓在那裡。但 Peter 直接開 50 個 Codex 並行跑，讓每個 Codex 分析一個 PR，產出包含 vision、intent、risk 等多維度信號的 JSON 報告。然後把所有報告匯入同一個 session，用 AI 做 de-dupe、auto-close、auto-merge。

（合理懷疑 Peter 去 OpenAI 只是為了免費的 Codex License XD）

Peter 這個極端實驗的目標：**盡快消化 3000 個積壓 PR，並且經過合適的 review。**

---

## 生產力悖論：AI 產出極快，人類根本消化不了

這不只是 OpenClaw 的問題。

OpenAI 二月初發了篇[工程博客](https://openai.com/index/harness-engineering/)，3 個工程師靠 Agent，5 個月就產出了 100 萬行代碼。GitHub 的數據也證實，導入 Copilot 後 PR 量暴漲了 98%，但審查時間卻也增加了 91%。上週六也說了 Stripe 一週可以做 1000 個 PR。

這就是現在工程團隊面臨的「生產力悖論」——**AI 產出極快，但人類根本消化不了。**

你不審，系統質量沒人兜底；你審了，你就成了整條開發流水線上最慢的瓶頸。

更可怕的是，OpenAI Blog 裡面說，如果沒有良好的架構去限制，**AI 會忠實且高速地複製代碼庫裡的反模式，代碼腐敗的速度也是 10 倍起跳。** OpenAI 管這個叫做「熵管理」（Entropy Management）。

---

## 真正的解法：用確定性的工具，框住不確定性的 AI

面對這個問題，真正的解法不是寫出更好的 Prompt，而是：**用確定性的工具，框住不確定性的 AI。**

我 20 年前學到的 CI/CD，又重新站上舞台了。

在 AI 時代，現在的高效團隊不寫代碼了，都在建構這**四層防禦架構**：

### 第一層：Test（測試）—— 最硬的護欄

Agent 可能會產生幻覺，但 `assert balance == expected_balance` 絕對不會騙你。

OpenAI 那個 3 人團隊的做法是：**先讓 Agent 寫測試，再讓 Agent 寫實現。** 測試本身就是規範。如果測試寫對了，Agent 寫的代碼只要通過測試，大方向就不會偏太遠。

我自己在支付系統裡的體感也一樣。我現在花在寫測試規範上的時間比寫 prompt 多得多。因為 prompt 是模糊的，但測試是確定的。

**AI 生成代碼的質量，80% 取決於你的測試覆蓋率，20% 才是 prompt 寫得好不好。**

### 第二層：Lint + Type Check —— Agent 的即時教練

OpenAI 做了一個很巧的事：寫了一堆自定義 lint 規則，**每條規則的報錯信息裡直接嵌修復指令。** Agent 犯錯的瞬間，怎麼改已經注入它的上下文了。把修復指令直接嵌在 Lint 報錯裡，讓 Agent 推代碼的瞬間就被攔截並自我修正。

工具鏈本身變成了 Agent 的教練。

這跟我在 Claude Code 裡用 hooks 的體驗很像。PreCommit hook 裡跑 lint + type check，Agent 推代碼的瞬間就被攔住。它不需要人告訴它「這裡有問題」，CI 會告訴它。

### 第三層：CI Gate（自動化）—— 機器的高速匹配 AI 的高速

透過確定性的結構化指標來嚴格把關：

- Type check 過了嗎？
- 單元測試通過了嗎？
- Lint 規則符合嗎？
- 覆蓋率有下降嗎？
- 安全掃描有報警嗎？

這些都是**確定性的**。不需要人判斷，機器就能給出 pass/fail。Agent 產出速度快 10 倍，你的 CI gate 也能 10 倍速運行。**只有機器的高速，才能匹配 AI 10 倍速的產出。** 這是人做不到的。

### 第四層：LLM Judge —— 用 AI 審查 AI

確定性工具能框住的範圍有限。測試能抓邏輯錯誤，lint 能抓風格問題，但「設計合不合理」「有沒有安全漏洞」「業務邏輯對不對」——這些需要語義理解。

所以第四道防線：讓不同的 LLM 分別扮演架構師、安全專家與審計，進行多維度的語義交叉 Review。

我自己 POC 試過三維並行 code review，三個 Agent 分別扮演 BU 審計、架構師、安全專家，同一段代碼三個維度同時審。交叉覆蓋率極低——金融審計找到 N+1 查詢和缺鎖問題，架構師發現死代碼和殘留字段，安全專家揪出負餘額檢查缺失、跨租戶數據泄露、競態條件三個高危。修完跑第二輪又冒出兩個高危。**修復本身也會引入問題，所以 LLM judge 不是跑一次就夠，要循環跑。**

但這裡有一個我到現在沒完全想通的問題：**用 LLM 審 LLM 寫的代碼，權責分離怎麼做？** 撰寫和審查用同一個模型家族，系統性偏差無法被捕捉。這在金融場景是個大問題。

---

## 四層防禦架構總覽

| 層級 | 手段 | 特性 | 速度 |
|------|------|------|------|
| **第一層** | Test（單元/整合/E2E） | 確定性，邏輯正確性 | 秒級 |
| **第二層** | Lint + Type Check | 確定性，風格+類型安全 | 秒級 |
| **第三層** | CI Gate（覆蓋率/安全掃描） | 確定性，結構化指標 | 分鐘級 |
| **第四層** | LLM Judge（多角色 review） | 非確定性，語義理解 | 分鐘級 |

前三層是確定性的——跑出來就是 pass 或 fail，不需要人判斷。第四層是非確定性的，但可以通過多角色、多模型來降低偏差。

---

## 80/20 法則徹底翻轉

我們熟悉的 80/20 法則已經徹底翻轉了。

過去我們 80% 的時間寫代碼，20% 搭環境。現在，我們得花 80% 的時間搭護欄（寫 Test、設 CI Gate、配 Lint、寫 CLAUDE.md），只剩 20% 的時間跟 Agent 互動。

沒想到當初大家花笨功夫沉澱出來的 CI/CD，現在反而是 AI Coding 時代的寶物。

---

## 坦白說

我的觀察可能有偏差。但有幾件事我比較確定：

**確定的部分：**

1. **CI/CD 是看漲的資產。** 在一切都不確定的 AI 時代，test 和 lint 這些老東西反而成了最值錢的資產。因為它們是唯一能給出明確 pass/fail 的東西。你的 testing case 寫得越多、越齊全，這是一個看漲的資產——Agent 產出越快，能自動驗證的測試就越值錢。

2. **Entropy Management 是真的。** 我親眼看到一個反模式在兩天內被 Agent 複製到四個 module。沒有 CI gate，代碼庫會以 10 倍速腐敗。

3. **LLM Judge 有用但有限。** 多角色 review 確實能抓到人類單視角抓不到的問題，但權責分離和系統性偏差的問題還沒解。

4. **Peter 的 50 Codex 實驗指向未來。** 用 AI 審 AI 的 PR，這不是花招，這是唯一能 scale 的方向。人類審 3000 個 PR 是不可能的任務，但 50 個 Codex 可以。

**不確定的部分：**

1. **護欄會不會變成過度工程？** 搭太多框架反而限制了靈活性，這個平衡點還沒找到。

2. **用 LLM 審 LLM 的上限在哪？** 同一個模型家族的盲點是相關的，能不能用不同家族的模型交叉審查來解決？需要更多實驗。

3. **這套框架對小團隊的成本效益如何？** OpenAI 有資源搭完整的 CI 體系，但 2-3 人的 startup 搭到什麼程度才算夠？

---

## 不是結論

20 年前我們花笨功夫學 CI/CD，寫 unit test，搞 automation pipeline，當時覺得這些都是苦差事。

現在回頭看，**這些苦差事全變成了 AI 時代最硬的護城河。**

你的 test 有多硬，你的 AI 就能跑多快。你的 CI gate 有多完整，你的代碼庫就能承受多少 Agent 同時往裡面灌代碼。

Make CI/CD Great Again——不是口號，是現在進行式。

---

**延伸閱讀：**
- [三個月 63 萬行之後：在 AI Coding 時代，工程師真正的價值是什麼？](https://ai-coding.wiselychen.com/claude-code-630k-lines-three-months-reflection/)
- [AI Coding 半年回顧：開發並沒有變快，我們只是把瓶頸從寫 Code，轉移到了 QA 跟需求收集](https://ai-coding.wiselychen.com/ai-coding-half-year-review-demand-transformation-tool-evolution/)
- [Cursor 前 0.01% 大神倒戈 Claude Code：Agentic Coding 五大支柱完整解析](https://ai-coding.wiselychen.com/cursor-top-user-switch-claude-code-agentic-coding/)
- [從「套殼 1.0」到「套殼 2.0」：為什麼真正該緊張的是 Anthropic](https://ai-coding.wiselychen.com/shell-wrapper-2-anthropic-real-threat/)
