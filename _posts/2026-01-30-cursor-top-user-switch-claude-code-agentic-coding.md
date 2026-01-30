---
layout: post
title: "Cursor 前 0.01% 大神倒戈 Claude Code：Agentic Coding 五大支柱完整解析"
date: 2026-01-30 08:30:00 +0800
permalink: /cursor-top-user-switch-claude-code-agentic-coding/
image: /assets/images/cursor-vs-claude-code-agentic-coding-cover.png
description: "當一個被 Cursor 官方認證的全球頂尖用戶，選擇放棄熟悉的工具轉投 Claude Code，這不只是換工具——這是一場關於「AI 程式設計該怎麼做」的典範轉移。Silen Naihin 的萬字長文詳解 Agentic Coding 五大支柱：Context Management、Planning、Closing the Loop、Verifiability、Debugging。"
---

![Cursor vs Claude Code](/assets/images/cursor-vs-claude-code-agentic-coding-cover.png)

**作者：** Wisely Chen
**日期：** 2026 年 1 月
**系列：** AI Coding 實戰觀察
**關鍵字：** Claude Code, Cursor, Agentic Coding, Silen Naihin, AI 程式設計, Opus 4.5

---

## 目錄

- [一封來自 Cursor 的認證信](#一封來自-cursor-的認證信)
- [為什麼曾經放棄，又為什麼回來](#為什麼曾經放棄又為什麼回來)
- [遊戲規則改變了：抽象層級的躍升](#遊戲規則改變了抽象層級的躍升)
- [Agentic Coding 五大支柱](#agentic-coding-五大支柱)
- [實戰工作流：12 個終端並行](#實戰工作流12-個終端並行)
- [Cursor vs Claude Code：不是取代，是分工](#cursor-vs-claude-code不是取代是分工)
- [社群的質疑與回應](#社群的質疑與回應)
- [坦白說](#坦白說)
- [延伸閱讀](#延伸閱讀)

---

## 一封來自 Cursor 的認證信

Silen Naihin 不是普通的開發者。

他是 AutoGPT 的核心貢獻者——那個至今仍是 GitHub 上最快達到 10 萬星標的傳奇專案。

在使用 Cursor 期間，他發現 90% 的程式碼開始由 AI 接管。他像著了魔一樣「住」進編輯器裡，瘋狂探索每一個極限。他寫了一份從未發布的內部最佳實踐指南，弄清楚了每一個微小的技巧。

然後，他收到了 Cursor 團隊的官方郵件：

> 恭喜你成為全球前 0.01% 的 Cursor 用戶。

這封信是榮譽，也是枷鎖。

因為幾個月後，他選擇了「叛逃」。

---

## 為什麼曾經放棄，又為什麼回來

2025 年初，Silen 其實試過 Claude Code。

結果是：棄坑。

他的評價很直接：

> 為什麼我要用一個勉強跟 Cursor 一樣好、但 UX 差十倍的工具？

當時的 Claude Code 工作流是一種倒退。模型不夠聰明，大多數時候人類仍然需要清楚知道程式碼裡發生了什麼。

**但 Claude Code 2.0 + Opus 4.5 改變了一切。**

表面上看，是 UX 進化了、框架更穩定了、Bug 修了不少。

但 Silen 認為這些都只是冰山一角。

真正的改變，是 Anthropic 對 Opus 4.5 做的 RLHF 訓練，**完全改變了遊戲規則**。

---

## 遊戲規則改變了：抽象層級的躍升

過去，使用 AI 寫程式的工作流是這樣的：

1. 在檔案層級指導模型
2. 在函數層級審查程式碼
3. 逐行檢視每一個變更

**現在不需要了。**

Silen 的新工作方式是：**直接測試「行為」**。

為了證明這一點，他在一天內用 Claude Code 建了一個遺傳演算法模擬器：

- 交互式視覺化介面，展示即時演化過程
- 複雜的適應度函數
- 選擇壓力、變異率調節等進階功能

他不是逐行審查程式碼完成的。

他是定義好「應該發生什麼」，然後驗證「是否真的發生了」。

**這就是抽象層級的躍升。**

從「審查程式碼」到「驗證行為」，聽起來只是措辭不同，但實際上是完全不同的工作模式：

| 舊模式 | 新模式 |
|--------|--------|
| 審查每一行 diff | 測試最終行為 |
| 在檔案層級指導 | 在需求層級指導 |
| 理解所有實作細節 | 理解介面契約 |
| 人類是程式碼審查者 | 人類是行為驗證者 |

這讓我想到之前寫的 [ATPM 框架](/atpm-real-production-vibe-coding/)——PRD 作為 Single Source of Truth 的核心價值，正是讓 AI 在需求層級工作，而不是在程式碼層級糾纏。

---

## Agentic Coding 五大支柱

Silen 在他的萬字長文中，提煉出 Agentic Coding 的五大核心原則。

這不是理論，是他從 2021 年開始用 AI 寫程式、踩過無數坑之後的實戰總結。

### 1. Context Management（上下文管理）

> 一個對話 ≈ 一個專注的任務

**核心痛點：** Claude Code 有 200k 的上下文限制，比 Codex（400k）或 Gemini（1M）都短。上下文一旦退化，模型表現會急劇下降。

**實戰做法：**

- 用 `/compact` 定期壓縮上下文
- 用 `/context` 監控剩餘 token
- 當上下文退化時，用 `/transfer-context` 轉移到新對話
- 複雜任務拆分到 subagent，避免污染主對話

### 2. Planning（規劃）

> 每投入 1 分鐘規劃，可以省下 3 分鐘的後續修正

**實戰做法：**

- 按兩次 Shift+Tab 進入 plan mode
- 用 `/interview-me-planmd` 讓 Claude 採訪你，產生完整計畫
- 明確說「不要做什麼」比說「要做什麼」更重要
- 避免過度工程化，偏好最簡單可行的方案

### 3. Closing the Loop（閉環迴圈）

> 自動化的成本已經崩塌——過去要一週的事，現在只要一段對話

**實戰做法：**

- 重複的 prompt → 做成 custom command
- 重複的工作流 → 做成 Agent
- 發現 gotcha → 更新 CLAUDE.md
- 建立 pattern → 文件化

### 4. Verifiability（可驗證性）

> 不要審查程式碼，測試行為

**實戰做法：**

- UI → 視覺檢查
- UX → 互動測試
- API → 請求測試
- 大型重構前 → 先寫完整的介面測試
- 部署前 → 整合測試作為安全網

### 5. Debugging（除錯）

> 如果同一件事解釋三次還是失敗，換一個方法

**實戰做法：**

- 系統性方法：建立假說 → 讀相關程式碼 → 加 log → 驗證
- 「三的法則」：解釋三次不行就換方向
- 展示範例，而不是解釋概念
- 卡住時開新對話，讓 Claude 總結學到的東西
- 用 `/ensemble-opinion` 取得多模型觀點

---

## 實戰工作流：12 個終端並行

Silen 的日常工作流是這樣的：

**同時開 12 個終端，每個專案 2 個。**

這聽起來很瘋狂，但他有一個關鍵概念：**Blast Radius（爆炸半徑）**。

每個終端只會接觸特定的檔案範圍。只要你清楚每個 Agent 的「勢力範圍」，它們就不會互相干擾。

他甚至很少用 git worktree——直接在同一個 repo 上「敲打分支」（branch hammering），速度更快。

**工具分工：**

| 工具 | 使用場景 |
|------|----------|
| Claude Code + Opus 4.5 | 規劃、程式碼生成、複雜重構、架構決策 |
| Cursor + GPT 5.2/Sonnet 4.5 | 學習、UI 微調、與 Claude Code 無關的小改動 |
| ChatGPT | 不需要專案上下文的程式問題、第二意見 |
| Ghostty 終端 | 快速、原生分割、更好的文字編輯、原生圖片支援 |

---

## Cursor vs Claude Code：不是取代，是分工

Silen 並沒有完全放棄 Cursor。

他的結論是：**兩者有不同的最佳使用場景。**

### 什麼時候用 Cursor？

- 像素級完美的前端開發
- 學習與教育迭代（更快的回饋循環）
- 與 Claude Code 工作無關的小型獨立修改
- 需要緊密 IDE 整合的「有機」寫程式

### 什麼時候用 Claude Code？

- 建構應用程式，輸出比過程理解更重要
- 最大化抽象層級
- 受益於終端原生非同步工作流的大型專案
- 複雜重構和架構決策

**核心差異：**

Cursor 維持緊密的人類介入控制。
Claude Code 要求你擁抱抽象，信任模型的輸出，通過行為測試來驗證。

---

## 社群的質疑與回應

這篇文章在 Hacker News 上引起了激烈討論。

### 最大的質疑：「不需要審查程式碼」真的可行嗎？

很多資深工程師指出：

- 這在多人協作、有付費客戶的環境下不可行
- 缺乏可維護性和健全的架構決策
- 大型遺留程式碼庫有大量業務邏輯和領域規則，AI 難以可靠處理

### Silen 的回應邏輯

他沒有說「永遠不需要審查」，而是說：

1. **驗證的方式改變了** —— 從「讀 diff」變成「測行為」
2. **這是抽象層級的選擇** —— 你可以選擇停留在舊層級，但會錯過效率提升
3. **好的工程能力定義改變了** —— 現在是：快速心智建模、除錯重構、prompt 能力、驗證能力

### 「Vibe Coding」的擔憂

有人擔心初級工程師會產出「看起來很厲害」的 CRUD 應用，卻不理解架構含義。

這和 20 年前 Rails 熱潮的批評如出一轍。

我的看法是：工具會變，但「理解系統」的能力永遠有價值。問題不在工具，在於使用工具的人是否有意識地建立理解。

---

## 坦白說

### 這篇文章為什麼值得認真看

因為 Silen 不是「跟風換工具」的人。

他是：
- AutoGPT 核心貢獻者
- 從 2021 年就開始用 AI 寫程式
- 被 Cursor 官方認證的頂級用戶
- 曾經試過 Claude Code 然後棄坑

當這樣的人說「遊戲規則改變了」，值得花時間理解他看到了什麼。

### 我的驗證與補充

Silen 的五大支柱，和我們團隊過去一年在 ATPM 框架裡驗證的經驗高度吻合：

| Silen 的支柱 | ATPM 的對應 | 我們的數據 |
|-------------|------------|-----------|
| Planning | PRD as SSOT | PRD 迭代 6-7 次，PRD:Code 比例 1:1.4 |
| Verifiability | QA 驗收流程 | 預期 80% 加速，實際 20%（但仍值得） |
| Closing the Loop | 知識結晶 | 50+ 專案 → 237 QA pairs |
| Context Management | 工作記憶管理 | CLAUDE.md 持續更新 |
| Debugging | 人類價值定位 | 處理邊界情況 |

**逐一對照：**

**1. Context Management → 工作記憶管理**

這和我們團隊在 [Unix 哲學文章](/unix-philosophy-command-line-renaissance/) 裡提到的「文字作為狀態」概念相呼應。上下文管理的本質，是讓 Agent 的「工作記憶」保持乾淨。Claude Code 的 200k 限制確實是痛點，但透過 CLAUDE.md 持續更新和任務拆分，可以有效緩解。

**2. Planning → PRD as Single Source of Truth**

這完全印證了 [ATPM 框架](/atpm-real-production-vibe-coding/) 的核心——PRD 不是文件，是投資。我們團隊的數據是「PRD 迭代 6-7 次」、「PRD:Code 比例 1:1.4」（9,211 行 PRD → 13,022 行程式碼）。規劃的槓桿效應，隨著模型變強只會更大。

**3. Closing the Loop → 知識結晶**

這是最容易被忽略的支柱。很多人把 AI 當成「一次性工具」，用完就丟。但真正的效率提升來自「累積」——每一次使用都在優化下一次。我們從 50+ 專案文件中提取出 237 組 QA pairs，onboarding 時間從 2-3 週縮短到 3 天。

**4. Verifiability → QA 驗收流程**

這和我在 [QA 驗收文章](/atpm-qa-ai-coding/) 裡強調的觀點一致。AI 產出的程式碼品質，不是靠「讀」來保證的，是靠「測」來保證的。我們預期 QA 流程能加速 80%，實際只有 20%——但這 20% 仍然值得，因為它建立了可重複驗證的基準。

**5. Debugging → 人類價值重新定位**

這裡有一個反直覺的觀點——AI 時代的除錯能力，可能比寫程式能力更重要。因為當 AI 能產出 90% 的程式碼，人類的價值就在於處理那 10% 的邊界情況。這也是為什麼 Silen 說「好的工程能力定義改變了」——現在是快速心智建模、除錯重構、prompt 能力、驗證能力。

### 一個更深的觀察

這篇文章和我之前寫的 [套殼 2.0 文章](/shell-wrapper-2-anthropic-real-threat/) 可以對照來看：

Silen 在說的是「個人開發者如何最大化 Claude Code 的效率」。

套殼 2.0 生態在解決的是「Agent 如何在團隊和企業環境中持續運作」。

兩者不矛盾，而是同一個趨勢的不同面向：

> **AI 程式設計正在從「工具」進化成「工作方式」。**

而這個進化，才剛剛開始。

---

## 延伸閱讀

- [Silen Naihin 原文](https://blog.silennai.com/claude-code) —— 完整的萬字轉換筆記
- [Hacker News 討論](https://news.ycombinator.com/item?id=46676554) —— 社群的質疑與辯論
- [從「套殼 1.0」到「套殼 2.0」](/shell-wrapper-2-anthropic-real-threat/) —— 為什麼真正該緊張的是 Anthropic
- [ATPM：一個真正上過生產的 Vibe Coding 流程](/atpm-real-production-vibe-coding/) —— 我們團隊的實戰框架
- [當 Unix 哲學遇上 AI](/unix-philosophy-command-line-renaissance/) —— 為什麼 Command Line 是 AI 時代最完美的介面

---

**關於作者：**

Wisely Chen，NeuroBrain Dynamics Inc. 研發長，20+ 年 IT 產業經驗。曾任 Google 雲端顧問、永聯物流 VP of Data & AI、艾立運能數據長。專注於傳統產業 AI 轉型與 Agent 導入的實戰經驗分享。

---

**相關連結：**
- 部落格首頁：https://ai-coding.wiselychen.com
- LinkedIn：https://www.linkedin.com/in/wisely-chen-38033a5b/

---

**Sources:**
- [I was a top 0.01% Cursor user. Here's why I switched to Claude Code 2.0. | Silen](https://blog.silennai.com/claude-code)
- [Hacker News Discussion](https://news.ycombinator.com/item?id=46676554)
- [新智元報導](https://finance.sina.cn/stock/jdts/2026-01-24/detail-inhikzwt3929209.d.html)
- [36Kr 報導](https://eu.36kr.com/zh/p/3655550408876162)
