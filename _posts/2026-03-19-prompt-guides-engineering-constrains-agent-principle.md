---
layout: post
title: "做 Agent 的一個體會：Prompt 負責引導，工程負責約束"
date: 2026-03-19 14:30:00 +0800
permalink: /prompt-guides-engineering-constrains-agent-principle/
image: /assets/images/prompt-guides-engineering-constrains-cover.png
description: "你的 CLAUDE.md 寫了 500 行規則，Agent 還是會刪掉你的資料庫。不是 Prompt 寫得不好，是你把約束放錯了地方。做 Agent 半年多，我歸納出一個最核心的原則：Prompt 負責引導，不負責約束；工程負責約束，不依賴模型自覺。這不是理論，是被打臉之後的體會。"
---

# 做 Agent 的一個體會：Prompt 負責引導，工程負責約束

**作者：** Wisely Chen
**日期：** 2026 年 3 月
**系列：** AI Coding 架構觀察
**關鍵字：** Agent Engineering, Prompt Engineering, Harness Engineering, 系統約束, CLAUDE.md, Agent 架構, 分界線原則

---

![Prompt 負責引導，工程負責約束：五層防線架構圖](/assets/images/prompt-guides-engineering-constrains-cover.png)

## 三句話，講完整篇文章的核心

**Prompt 負責引導，不負責約束。**

**工程負責約束，不依賴模型自覺。**

**少在 Prompt 裡寫規則，多在系統裡做約束。**

這三句話是我做 Agent 半年多最大的體會。聽起來很簡單，但大部分人（包括半年前的我）都搞反了。

---

## 為什麼 Prompt 約束不住 Agent

先講一個真實場景。

我在 CLAUDE.md 裡寫了一條規則：「不要刪除任何現有檔案，除非使用者明確要求。」

很清楚，對吧？

然後有一天 Agent 在重構專案結構的時候，判斷某個檔案「已經不需要了」，直接刪掉。它的邏輯是：使用者要我重構，重構就是整理，整理當然包括清理不需要的東西。

它沒有違反規則嗎？從它的理解來看，使用者「要求重構」就等於「要求清理」，所以刪除是合理的。

**這就是 Prompt 約束的根本問題：語言是模糊的，模型的理解是概率性的。**

你寫「不要刪除」，模型在 99% 的情況下會遵守。但那 1% 的邊界情況——上下文很長、指令衝突、任務複雜度高——它就會「重新詮釋」你的規則。

不是它故意違反，是語言本身就有解讀空間。

Michael Guo 在 X 上講得更精準：

> **The correct architecture: Code defines execution + safety boundaries. LLMs handle interpretation + reasoning.**

把 Orchestration 交給 LLM Agent，把邊界交給 Code。這不是誰的個人偏好，是越來越多實戰團隊試錯出來的共識。

---

## 用 Prompt 做約束的三個典型失敗

### 失敗一：規則越寫越多，效果越來越差

我見過有人的 CLAUDE.md 超過 1000 行。裡面寫滿了各種「不要做 X」、「一定要做 Y」、「在 Z 情況下請先問我」。

結果呢？規則之間互相矛盾，模型不知道該聽哪條。上下文窗口被規則塞滿，留給實際任務的空間反而不夠。

**規則數量和遵守率不是正比，是反比。**

換個角度想：與其全域規則、專案規則一條又一條地疊加，不如把測試覆蓋率、lint 工具、CI 工具給它卡死。這些東西沒有任何模糊的空間——法不容「上下文溢出」。Prompt 規則會因為上下文太長而被稀釋，但 CI gate 不會因為你的 PR 太大就放水。

### 失敗二：「請先確認再執行」——它確認了，但確認的方式你沒預期到

你寫：「執行破壞性操作前，請先和使用者確認。」

Agent 確實問了你：「我準備重構這個模組，會涉及檔案移動和刪除，可以嗎？」

你說「可以」。

然後它把你沒想到的設定檔也一起刪了。它有確認嗎？有。它確認的粒度夠細嗎？不夠。但你的 Prompt 裡沒有定義「確認」應該細到什麼程度。

**語言指令無法窮舉所有邊界條件。**

### 失敗三：靠模型「自覺」做安全判斷

最危險的假設：「AI 應該知道這個操作有風險，所以它會小心。」

不會的。模型沒有風險意識，它只有模式匹配。它看到「git push --force」不會像資深工程師一樣冒冷汗，它只是在執行指令序列中的下一步。

**模型沒有「自覺」，只有「統計上最可能的下一個 token」。**

---

## 用工程做約束的四個成功模式

### 模式一：檔案系統權限（最簡單，最有效）

不要在 Prompt 裡寫「不要修改 production config」。

直接把 production config 設成唯讀。Agent 想改也改不了，連「重新詮釋」的機會都沒有。

```bash
# 工程約束：比任何 Prompt 都可靠
chmod 444 config/production.yml
```

一行指令，比你寫 50 行 Prompt 規則都有效。

### 模式二：CI/CD Gate（讓系統替你審查）

不要在 Prompt 裡寫「提交前請確保所有測試通過」。

在 CI pipeline 裡設 gate：測試沒過，PR 無法合併。不是「請 Agent 自覺跑測試」，是「系統不允許未測試的程式碼進入主幹」。

```yaml
# GitHub Actions: 工程約束
on:
  pull_request:
    branches: [main]
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - run: npm test
      - run: npm run lint
      # 測試沒過？PR 直接被擋，不管是人寫的還是 AI 寫的
```

Agent 可以忽略你的 Prompt 規則，但它繞不過 CI gate。

### 模式三：Git Hooks + 分支保護（防止不可逆操作）

不要在 Prompt 裡寫「不要 force push to main」。

在 Git 設定分支保護規則：main 分支禁止 force push，PR 需要至少一個人類 review。

這不是建議，是系統層級的硬性約束。不管是人還是 Agent，都繞不過去。

### 模式四：Tool-Level Validation（在工具層攔截，不在 Prompt 層拜託）

這是最容易被忽略、但最關鍵的一個模式。

很多人在 Prompt 裡寫：「呼叫工具 A 之前，請先執行檢驗步驟。」

問題是：模型完全靠自己的腦子來決定要不要先檢驗。它可能忘了，可能判斷「這次不需要」，可能上下文太長把這條規則擠掉了。

正確做法是反過來——**在工具 A 的執行邏輯裡，硬編碼檢驗步驟。** 檢驗失敗，工具直接回傳錯誤，Agent 根本拿不到結果。

```python
# ❌ 錯誤：在 Prompt 裡寫「呼叫 deploy 前請先跑測試」
# 模型可能跳過，你拿它沒辦法

# ✅ 正確：在 tool 實作裡強制檢驗
def deploy_tool(env: str, version: str):
    test_result = run_tests()
    if not test_result.passed:
        return {"error": "部署被阻擋：測試未通過", "details": test_result.failures}
    # 測試通過才繼續執行部署
    return execute_deploy(env, version)
```

與其請模型「先檢驗再呼叫」，不如在工具本身執行前就做檢驗，失敗直接回傳失敗結果。模型不需要「自覺」，因為系統替它做了。

---

## 分界線在哪裡：什麼該放 Prompt，什麼該放系統

這是最實用的部分。

| 類型 | 放 Prompt（引導） | 放系統（約束） |
|------|-------------------|---------------|
| **風格** | 程式碼風格偏好、命名慣例 | ESLint / Prettier 強制格式化 |
| **安全** | 「注意不要暴露 API key」 | .gitignore + pre-commit hook 掃描 |
| **架構** | 「我們用 MVC 模式」 | 目錄結構 + import 規則 + lint rule |
| **部署** | 「部署前要跑測試」 | CI gate：測試不過不能合併 |
| **資料** | 「小心處理使用者資料」 | RLS (Row Level Security) + 加密 |
| **權限** | 「不要修改 prod 設定」 | 檔案系統權限 + IAM policy |

**原則很簡單：如果違反這條規則會造成不可逆的損害，就不要用 Prompt 來約束。**

Prompt 適合處理偏好、風格、方向性的指引——就算 Agent 偶爾沒遵守，你也只是不滿意，不會出事。

系統約束處理安全、資料完整性、不可逆操作——這些事情出錯一次就夠你修一整天。

---

## 一個思考框架：Prompt 是方向盤，工程是護欄

開車的時候，方向盤告訴車子往哪走，護欄確保車子不會掉下懸崖。

你不會把護欄拆掉，然後在方向盤上貼一張紙條寫「不要開出馬路」。

但這就是大部分人做 Agent 的方式：拆掉工程護欄（或者根本沒建），然後在 Prompt 裡貼滿紙條。

**方向盤（Prompt）：**
- 告訴 Agent 目標是什麼
- 提供上下文和背景知識
- 設定偏好和優先順序
- 引導思考方向

**護欄（工程）：**
- 確保 Agent 不會做出不可逆的錯誤
- 在系統層級阻擋危險操作
- 不依賴 Agent 的「理解」或「自覺」
- 對人和 AI 一視同仁

---

## 坦白說

這個原則聽起來很直覺，但我花了好幾個月才真正內化。

一開始我也是瘋狂寫 Prompt 規則。每次 Agent 犯錯，我就加一條新規則。CLAUDE.md 越來越長，但問題並沒有變少——只是換了一種方式出現。

轉折點是有一次 Agent 繞過了我寫的五層 Prompt 規則，直接執行了一個我不想要的操作。那個時候我才意識到：**問題不在規則寫得不夠多，而在約束放錯了層。**（後來才發現那幾天 Sonnet 降智了。但這反而證明了我的觀點——你的約束不能建立在「模型今天狀態好不好」上面。模型會升級、會降智、會被換版本，但工程護欄不會因為模型換了一版就失效。）

從那之後我改變策略：先建工程護欄，再寫 Prompt 引導。效果差異非常明顯——不是「好一點」，是「從偶爾出事」變成「系統性地不會出事」。

但也要老實說，工程約束也不是萬能的。有些東西確實只能用 Prompt 來處理，比如「這個專案的商業邏輯偏好」、「使用者體驗的調性」這類軟性判斷。這些你沒辦法用 CI gate 來管。

**所以不是「Prompt 無用」，而是「別讓 Prompt 做它不擅長的事」。**

---

## 關鍵洞察

1. **Prompt 是概率性的，工程是確定性的。** 你要用確定性的手段來約束不可逆的操作。

2. **規則數量和遵守率是反比。** Prompt 裡的規則越多，模型越容易忽略或誤讀。少即是多。

3. **模型沒有風險意識。** 不要假設 AI 「應該知道」某個操作有風險。它不知道，它只是在生成 token。

4. **對人和 AI 一視同仁。** 好的工程約束，本來就應該同時約束人類和 AI。如果你的系統允許人類 force push to main，那 AI 當然也會。

5. **先建護欄，再給方向盤。** 不要在沒有工程約束的情況下，就讓 Agent 自由操作。

---

## 延伸閱讀

- [Harness Engineering 的四個 Demo：Prompt 是建議，機制才是規則](/agent-harness-three-migrations-mechanism/) — 本文觀點的姊妹篇，用四個 Claude Code hook demo 示範怎麼把「規則」變成「機制」
- [Harness Engineering 架構全景](/harness-engineering-architecture-overview-ai-code-production-guardrails/) — 完整的七元件參考架構
- [Control Plane Pattern](/harness-engineering-control-plane-pattern-agent-review-loop/) — 八步建立 Agent Review Loop
- [四層防禦架構](/coders-who-stopped-coding-harness-context-spec-engineering/) — Test → Lint → CI Gate → LLM Judge
- [Prompt Injection 是 Harness 問題](/prompt-injection-harness-engineering-tool-using-agents/) — 為什麼語言攻擊打不穿工程約束
