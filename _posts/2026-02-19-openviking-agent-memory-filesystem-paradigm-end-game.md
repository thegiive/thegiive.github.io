---
layout: post
title: "字節跳動 OpenViking 拆解：用「文件系統」重構 Agent 記憶，這可能是終局方向"
date: 2026-02-19 10:00:00 +0800
permalink: /openviking-agent-memory-filesystem-paradigm/
description: "現在的 Agent 普遍有「金魚腦」問題，根源在於傳統 RAG 把萬卷書切成碎片扔進大桶。字節跳動開源的 OpenViking 提出了一個降維打擊：用文件系統範式重構 Agent 記憶。L0/L1/L2 三層上下文、目錄遞迴檢索、viking:// 虛擬文件系統——這套思路讓 Agent 從「造書籤」進化到「造圖書館索引」。"
image: /assets/images/openviking-logo.png
---

![OpenViking — A Context DataBase for AI Agents](/assets/images/openviking-logo.png)

## 為什麼要寫這篇

最近社群有一個帖子引起很大討論：字節跳動開源了 OpenViking，一套專為 AI Agent 設計的「上下文資料庫」。

說實話，我一開始看到標題沒太在意。又一個 Vector DB 的輪子？

但仔細研究之後，我發現它的核心思路跟我之前寫過的幾個主題產生了強烈共振：

- [為什麼我選擇 PostgreSQL 當 Vector Store](/postgresql-vector-store-pragmatic-choice/) — 我說過「Vector 只是資料的一種型態」
- [OpenClaw 記憶系統全解析](/openclaw-architecture-deep-dive-context-memory-token-crusher/) — OpenClaw 的 File-First 設計哲學
- [Google Nested Learning](/google-nested-learning-ai-memory-breakthrough/) — AI 的短期記憶 vs 長期記憶問題

OpenViking 不是在造另一個 Vector DB。它試圖回答一個更根本的問題：

**Agent 的記憶應該長什麼樣子？**

---

## 先搞清楚：傳統 RAG 到底哪裡不夠

在講 OpenViking 之前，先把問題定義清楚。

現在大多數 Agent 的記憶系統，本質上就是 RAG（Retrieval-Augmented Generation）：

1. 把文件切成 chunks
2. 每個 chunk 算 embedding，扔進 Vector DB
3. 使用者提問時，算問題的 embedding
4. 在 Vector DB 裡找「語義最相似」的 chunks
5. 把找到的 chunks 塞進 prompt

這套流程對 **Chatbot** 來說夠用了。你問「公司的退貨政策是什麼」，它找到相關段落，回答你，結束。

但對 **Agent** 來說，問題就大了。

### Agent 需要的不是「查資料」，是「大腦」

我在 [OpenClaw 記憶架構文章](/openclaw-architecture-deep-dive-context-memory-token-crusher/) 裡整理過一個對比：

| 需求 | Chatbot + RAG | Agent + 結構化記憶 |
|------|--------------|-------------------|
| 記憶目的 | 回答問題時「查」相關資訊 | 持續「知道」自己是誰、在做什麼 |
| 上下文連貫性 | 每次檢索可能不一致 | 每次都從同一個認知基礎出發 |
| 推理能力 | 片段式，依賴檢索結果 | 整體式，可以跨文件推理 |
| 錯誤代價 | 回答不準確 | 可能搞混環境、刪錯資料 |

最後一行是關鍵。

Chatbot 答錯了，頂多使用者皺個眉。Agent 搞混了上下文，可能把測試環境的指令套到生產環境。

**傳統 RAG 的「語義相似度匹配」，對 Agent 來說就是在賭博。** 你問它「修復資料庫配置」，它在幾萬個碎片裡靠概率猜哪一個最像——如果猜到了上週另一個專案的配置，你就等著收驚吧。

---

## OpenViking 的降維打擊：文件系統範式

好，問題定義清楚了。來看 OpenViking 怎麼解。

OpenViking 是字節跳動火山引擎 Viking 團隊在 2026 年 1 月開源的專案（[GitHub](https://github.com/volcengine/OpenViking)，2.8k stars，Apache-2.0 授權）。

它的核心理念用一句話講：

> **不要把 Agent 的記憶當成「一鍋粥」，要當成「檔案櫃」。**

具體怎麼做？三個關鍵設計。

### 1. L0/L1/L2 三層上下文：先看目錄，再翻內容

傳統 RAG 是「平面」的——所有 chunks 都在同一層，靠語義距離排序。

OpenViking 把上下文分成三層：

| 層級 | 內容 | Token 量 | 用途 |
|------|------|---------|------|
| **L0 (摘要)** | 一句話概述 | ~100 tokens | 快速判斷「這個目錄跟我有關嗎」 |
| **L1 (概覽)** | 核心資訊 + 使用場景 | ~2k tokens | Agent 規劃決策用 |
| **L2 (全文)** | 完整原始資料 | 完整大小 | 需要深入時才載入 |

這就像你找一本書：

- L0 是書名和作者——掃一眼就知道要不要拿起來
- L1 是目錄和序言——花幾分鐘判斷這本書對你有沒有用
- L2 是翻開特定章節仔細讀——只在確認需要時才花這個時間

**Token 節省的邏輯很直覺：** 如果 L0 就判定無關，就不需要載入 L1 和 L2。大部分查詢只需要到 L1 就能做決策。只有真正需要深入的時候才載入 L2。

### 2. viking:// 虛擬文件系統：從「猜」到「找」

這是 OpenViking 最核心的設計轉變。

傳統 RAG：所有 chunks 扔進一個大桶，靠「語義相似度」去猜。

OpenViking：所有上下文（記憶、資源、技能）映射為虛擬目錄，每個條目有唯一 URI。

```
viking://user/memory/preferences/      # 用戶偏好
viking://agent/memory/skills/database/  # Agent 的資料庫操作經驗
viking://project/alpha/config/          # Alpha 專案的配置
viking://project/beta/config/           # Beta 專案的配置
```

支援的操作不是「向量搜索」，而是 `ls`、`find`、`glob` 這些**確定性操作**。

這意味著什麼？

**以前：** 你問 Agent「修復資料庫」，它在所有碎片裡靠概率匹配，可能把 Alpha 專案的配置跟 Beta 專案的報錯搞混。

**現在：** 它先定位到 `/project/alpha/config/` 這個目錄，物理屏蔽掉 `/project/beta/` 底下的所有東西。不是看誰長得像，是看誰在正確的位置。

**這不是優化，這是範式轉換——從概率匹配到確定性定位。**

### 3. 目錄遞迴檢索：向量搜索沒有被丟掉，而是被「管起來了」

有人可能會問：那向量搜索不要了嗎？

不是。OpenViking 的檢索策略是「目錄遞迴」，分五步：

1. **意圖分析** → 產生多個搜索條件
2. **向量檢索** → 快速定位到高分目錄（注意，是定位目錄，不是定位 chunk）
3. **目錄內二次檢索** → 在確定的目錄裡精確搜索
4. **子目錄遞迴下探** → 如果需要更深的資訊，沿著目錄結構往下走
5. **結果聚合** → 回傳最相關的上下文

向量搜索還在，但它的角色從「直接給答案」變成了「先幫你找到正確的書架」。

用 OpenViking 自己的話說：**向量庫不是大腦，只是硬碟。沒有文件系統的硬碟，就是一堆廢鐵。**

---

## 跟 OpenClaw 的 File-First 設計對比

寫到這裡，熟悉我文章的讀者可能已經在想：這跟 OpenClaw 的設計是不是很像？

沒錯。

OpenClaw 的 File-First 設計哲學：

- **SOUL.md** — Agent 的人格定義，每次對話都讀
- **AGENTS.md** — 技能和行為規範
- **session.jsonl** — 對話歷史，結構化儲存

OpenViking 的文件系統範式：

- **viking://user/memory/** — 用戶偏好和記憶
- **viking://agent/memory/** — Agent 的技能和經驗
- **L0/L1/L2 分層** — 按需載入，節省 Token

兩者的共同點是：**都拒絕把記憶當成「一鍋粥」，都選擇了結構化的文件系統作為記憶的組織方式。**

差異在哪？

| 面向 | OpenClaw | OpenViking |
|------|----------|------------|
| 定位 | 完整的 Agent 框架 | 記憶基礎設施（可以被其他 Agent 框架整合） |
| 記憶載入 | 全量載入（SOUL.md + AGENTS.md 每次都讀） | 分層載入（L0 → L1 → L2 按需） |
| 檢索方式 | 直接讀檔案（確定性） | 目錄遞迴 + 向量輔助（混合式） |
| Token 成本 | 高（每次對話都載入完整上下文） | 理論上更低（按需載入） |
| 成熟度 | 已有大量用戶實戰驗證 | 剛開源，生態還在建設 |

我覺得最有意思的是：OpenClaw 用「全量載入 + 犧牲 Token」換來了一致性，OpenViking 想用「分層載入 + 結構化索引」同時兼顧一致性和效率。

這兩個方向最終可能會融合。

---

## 記憶自演化：越用越聰明

OpenViking 還有一個值得注意的設計：**記憶自演化機制**。

每次 session 結束時，呼叫 `session.commit()`，系統會非同步分析這次對話：

- 提取用戶偏好更新 → 寫入 User `/memory` 目錄
- 擷取 Agent 學到的操作技巧 → 寫入 Agent `/memory` 目錄

這意味著 Agent 的記憶不是靜態的知識庫，而是會隨著使用不斷成長的「經驗資料庫」。

這跟我之前寫的 [Google Nested Learning](/google-nested-learning-ai-memory-breakthrough/) 有異曲同工之處——Google 想在模型層面解決「短期記憶 → 長期記憶」的升級問題，OpenViking 是在應用層面用工程手段做同一件事。

---

## 社群實戰：P + L = 完整的記憶管理

寫完上面的理論拆解後，我在社群看到[一篇真實的實作分享](https://x.com/xxx111god/status/2023838143045136557)，作者已經把 OpenViking 的概念接進自己的 Agent。他的經驗補充了一個我在文章裡沒有深入的面向：**生命週期管理**。

### 被忽略的另一半問題：記憶膨脹

OpenViking 的 L0/L1/L2 解決了「怎麼取」的問題，但還有一個同樣重要的問題：**記憶什麼時候該過期？**

這位開發者的 v1 系統有一套 P0/P1/P2 生命週期機制：

| 等級 | TTL | 典型內容 |
|------|-----|---------|
| **P0** | 永不過期 | 核心身份、偏好、鐵律 |
| **P1** | 90 天 | 活躍專案、工作上下文 |
| **P2** | 30 天 | 臨時資訊、一次性任務 |

每條記憶打標籤，自動排程腳本每天凌晨掃描，過期的 P1/P2 自動移到 `archive/`。

這套已經能防止記憶無限膨脹了。但他遇到的真實痛點是：

> 「Bot 每次啟動都要讀 MEMORY.md 全文，這文件已經 8000+ tokens 了。問天氣交易 bot 的結算結果，它不需要知道我的報稅專案進度。但它不知道『哪些該讀哪些不該讀』，只能全塞進去。」

**這就是 L0/L1/L2 進場的完美時機。**

### P 管生命週期，L 管檢索效率

他把兩套系統疊起來之後：

**L 層（OpenViking 的分層載入）：**
- 先讀 `.abstract`（100 tokens），知道目錄裡有什麼
- 只在問到相關問題時才載入具體內容
- 從「全讀」變成「按需讀」

**P 層（生命週期管理）：**
- P0 永久保留（核心記憶）
- P1/P2 自動歸檔過期內容
- 記憶總量有上限

兩套機制互補：**L 解決「怎麼找」，P 解決「什麼時候丟」。** 既能快速定位，又不會無限膨脹。

### 升級後的具體架構

```
memory/
├── .abstract              # L0 根目錄索引（新增）
├── MEMORY.md              # 長期記憶 + P0/P1/P2 標籤
├── SESSION-STATE.md       # 工作緩衝區（新增）
├── insights/
│   ├── .abstract          # L0 洞察索引（新增）
│   └── 2026-02.md         # L1 提煉
├── lessons/
│   ├── .abstract          # L0 教訓索引（新增）
│   └── operational-lessons.jsonl  # L1 結構化
├── 2026-02-17.md          # L2 原始日誌
└── archive/               # 過期 P1/P2 歸檔
```

他報告的效果：**日常場景 Token 節省 10 倍以上。** 該深入的時候還是會深入，但不再無腦全載入。

### 這給我的啟發

這個 P + L 的組合其實很像人腦的運作方式：

- **P 層 = 遺忘曲線** — 重要的事記得牢，瑣碎的事會淡忘
- **L 層 = 聯想索引** — 想到某件事時，先想「這事在哪個抽屉」，再去拿

你不會打開電腦就把所有文件讀一遍。先看資料夾結構，再打開需要的文件。Agent 記憶檢索也該這樣。

**這也回應了前面 OpenClaw 的比較：** OpenClaw 目前是全量載入 SOUL.md + AGENTS.md，犧牲 Token 換一致性。如果未來結合 P + L 的思路——對 SOUL.md 做分層索引，對過期的 session 上下文自動歸檔——就能在維持一致性的同時大幅降低 Token 成本。

---

## 坦白說

講完好的，講不好的。這是這個 Blog 的傳統。

### 1. 目前沒有公開的 Benchmark 數據

這是最大的問號。OpenViking 的理論聽起來很美，但目前 GitHub 和官方文檔都**沒有提供量化的效能對比**——沒有「比傳統 RAG 準確率提升 X%」、沒有「Token 節省 X%」的硬數據。

字節內部聲稱在 50+ 業務場景驗證過，但沒有公開具體數字。

**在工程領域，沒有 Benchmark 的方案，只能當作「有前景的方向」，不能當作「已驗證的解法」。**

### 2. 文件系統範式的假設可能不成立

OpenViking 假設 Agent 的知識可以被「整理成目錄結構」。但真實世界的知識往往是**跨領域、模糊邊界**的。

舉個例子：「這個客戶去年投訴過，而且他是 VIP」——這個記憶同時屬於「客訴處理」和「VIP 管理」兩個目錄。在文件系統裡，你只能放一個位置（或者做軟連結）。但在向量空間裡，它天然就是多維的。

目錄結構天生是樹狀的，但知識關係往往是網狀的。

### 3. 生態還很早期

OpenViking 2026 年 1 月才開源，目前 2.8k stars。跟 LangChain（90k+）、LlamaIndex（40k+）這些成熟框架比起來，社區規模差距很大。

支援的模型和 Embedding 提供者雖然不少（Doubao、OpenAI、Anthropic、DeepSeek、Gemini 等），但整合文檔和最佳實踐還在建設中。

### 4. 與現有系統的整合成本

如果你已經有一套基於傳統 RAG 的系統在跑，遷移到 OpenViking 的文件系統範式不是改個 config 的事。你需要重新設計整個上下文的組織結構——這本身就是一個不小的工程投入。

---

## 我的判斷

把情緒放一邊，從工程角度看：

**OpenViking 的「文件系統範式」指出了一個正確的方向，但目前還是概念先於數據。**

它解決的問題是真實的：
- Agent 的上下文污染是真的
- 傳統 RAG 的「概率匹配」對高風險操作是不夠的
- Token 成本隨著 Agent 使用時間增長確實會爆炸

它提出的解法是合理的：
- L0/L1/L2 分層載入的邏輯很直覺
- 從「概率匹配」到「確定性定位」的範式轉換方向對
- 記憶自演化機制是 Agent 長期使用的剛需

但它還需要證明的事情也很多：
- 公開 Benchmark 數據
- 大規模真實場景的效能驗證
- 社區生態建設

---

## 給 Agent 開發者的建議

1. **如果你正在被 Agent 的上下文污染困擾**，OpenViking 的文件系統範式值得研究，但先別急著全面遷移。可以先在新專案裡試水。

2. **如果你用 OpenClaw**，其實 OpenClaw 的 File-First 設計已經走在類似的方向上了。OpenViking 的 L0/L1/L2 分層概念可以作為你優化 SOUL.md 和 AGENTS.md 載入策略的參考。

3. **如果你在設計新的 Agent 記憶系統**，「結構化 > 扁平化」這個原則已經被多個獨立團隊驗證了（OpenClaw、OpenViking、Google Nested Learning）。不管你用什麼工具，先把記憶組織成有層級的結構。

4. **考慮 P + L 雙系統**。L0/L1/L2 解決檢索效率，但記憶膨脹需要另一套機制。給每條記憶加 TTL（P0 永久、P1 90天、P2 30天），配合定期歸檔腳本，兩套系統疊起來效果最好。

5. **不要被「向量搜索已死」的說法帶跑**。向量搜索沒有死，它只是從「主角」變成了「配角」。在 OpenViking 的設計裡，向量檢索仍然是定位目錄的重要手段，只是它不再是唯一的手段。

---

## 延伸閱讀

- [OpenViking GitHub](https://github.com/volcengine/OpenViking) — 原始碼和文檔
- [為什麼我選擇 PostgreSQL 當 Vector Store](/postgresql-vector-store-pragmatic-choice/) — 80% 的 RAG 不需要專用 Vector DB
- [OpenClaw 記憶系統全解析](/openclaw-architecture-deep-dive-context-memory-token-crusher/) — File-First 設計哲學
- [Google Nested Learning](/google-nested-learning-ai-memory-breakthrough/) — AI 的短期記憶 vs 長期記憶
- [RLM 遞迴語言模型](/recursive-language-models-rlm-context-rot-solution/) — Context Rot 問題的另一種解法
