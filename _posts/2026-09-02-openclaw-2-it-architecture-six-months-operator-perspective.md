---
layout: post
title: "OpenClaw 2.0 架構拆解：六層改動一次看完"
date: 2026-09-02 05:28:14 +0800
permalink: /openclaw-2-it-architecture-six-months-operator-perspective/
image: /assets/images/openclaw-2-detailed-architecture.png
description: "8 月 30 號，OpenClaw 推出了 2.0 版（版號 v2026.8.1）。官方自己的標題叫「OpenClaw 2.0, Accidentally」——意思是他們本來沒打算做一次大改版，結果改到最後回頭一看，動到的東西已經大到必須叫 2.0 了。"
---

> OpenClaw 2.0（v2026.8.1）是專案史上最大改版——16,977 個 PR、987 位貢獻者。這篇拆解六個最重要的架構變動：Session 儲存遷移、Shared Cloud Sessions、Gateway 信任邊界、Control UI 重寫、模型偵測機制、以及內建記憶系統。

![OpenClaw 2.0 Gateway 架構圖](/assets/images/openclaw-2-detailed-architecture.png)

---

8 月 30 號，OpenClaw 推出了 2.0 版（版號 v2026.8.1）。官方自己的標題叫「OpenClaw 2.0, Accidentally」——意思是他們本來沒打算做一次大改版，結果改到最後回頭一看，動到的東西已經大到必須叫 2.0 了。

以下拆六個最重要的架構層面，每個都講它改了什麼、為什麼改、以及對實際部署的影響。

---

## 一、Session 儲存從檔案搬進 SQLite

這是 2.0 最底層、影響最大的一個改動。

舊版的 session 和 transcript（對話紀錄）都是以檔案形式存在硬碟上。2.0 把它們全部搬進 SQLite。

為什麼這件事重要？因為**這是一條單行道**。升級之後，新產生的 session 都只存在 SQLite 裡面。如果要降回舊版，得先用新版 CLI 把資料匯出成舊格式，否則那些 session 就看不到了。

這個改動帶來兩個面向的影響：

**好處是效能跟一致性。** 檔案形式的 session 在並發場景下容易碰到鎖定或讀寫衝突，尤其 transcript 量大的時候。SQLite 做為 embedded database，在並發讀取和 atomic write 上比散落的檔案穩定很多。

**風險是升級前一定要備份。** 官方文件寫得很清楚：升級前建立 verified backup。建議先在測試環境升級驗證，確認沒問題之後再動正式環境。

---

## 二、Shared Cloud Sessions：多人協作，但不是多租戶

2.0 加入了 Shared Cloud Sessions，讓多個使用者可以加入同一個 agent session，共享上下文繼續工作。

這功能的典型場景是團隊協作。以前一個人在 OpenClaw 上處理到一半的任務要交給同事接手，基本上要重新把脈絡講一遍。現在可以讓同事直接進入同一個 session，agent 已經累積的上下文不會丟失。

但有一個非常重要的前提，官方文件講得很直白：

**Shared cloud sessions 不是 tenant isolation，也不是 security boundary。**

白話講就是——這功能假設參與的人都是「可信任的同事」。它不是設計來讓不同部門、不同公司的人共用同一個 Gateway 的。如果組織有多個業務單位需要資料隔離，就得部署多個 Gateway instance，每個有自己的 state、credentials 和 workspace。

對企業部署來說，這意味著地端獨立主機天然就是分開的 Gateway，沒有問題。但如果要做 managed service 或多團隊共用，「一個 Gateway 一個信任域」的設計就得認真考慮部署架構。

---

## 三、Gateway 信任邊界：一個 Gateway 一個信任域

延續上面的討論，2.0 把 Gateway 的安全模型講得更清楚了。

核心原則是 **one trust boundary per Gateway**。所有連上同一個 Gateway 的使用者，共享同一個信任域。Gateway 的預設姿態是：sandboxing 和 execution approval 都是關閉的，假設操作者是受信任的單一使用者。

如果需要管控，2.0 提供了四個層級的 access mode：
- **Read-only**：只能看不能動
- **Guarded**：需要逐次核准
- **Workspace**：限定在特定工作目錄
- **Full access**：完全授權

另外在安全數據上，2.0 公布了一組 prompt injection 測試結果。他們用 272K 筆群眾攻擊（crowdsourced attacks）跑了 41 個 agent scenarios，各模型的攻擊成功率是：

| 模型 | Prompt Injection 成功率 |
|------|------------------------|
| Claude Opus 4.5 | 0.5% |
| Claude Sonnet 4.5 | 1.0% |
| Claude Haiku 4.5 | 1.3% |
| Gemini 2.5 Pro | 8.5% |

這組數據的含義很明確：frontier 模型的抗注入能力顯著優於較小的模型。因此在處理機敏任務時，模型的選擇本身就是安全架構的一環。

2.0 的官方立場也是這樣——**模型選擇本身就是 prompt injection 的第一道防線。**

---

## 四、Control UI 重寫：從 1.6 秒到 575 毫秒

Control UI 是在瀏覽器裡管理 OpenClaw 的 Web 介面。2.0 把它整個重寫了。

具體的數字是：
- JavaScript requests 從 **140 個降到 45 個**
- 啟動時間從 **1.6 秒降到 575 毫秒**
（測試條件：50ms HTTP/1.1 latency，mocked Gateway）

除了效能之外，UI 的結構也重新設計了：
- Conversation 移到 sidebar 中央
- Settings 和 Inbox 從聊天流分離出來
- Session 可以在瀏覽器的真實 tab 裡開多個
- Sidebar 寬度可調整且會記住

其中最實用的改動是 session 可以用真實 browser tab 開。同時管理多個 agent session 的使用者，可以把不同 session 開在不同 tab，配合瀏覽器本身的 tab grouping 來管理，workflow 清楚很多。

---

## 五、模型偵測與地端架構改動

2.0 在 onboarding 流程做了一個重要的設計：**自動偵測機器上已有的 AI 資源。**

它會去掃：
- 已登入的 ChatGPT、Claude CLI
- 系統裡的 API key
- 透過 Ollama 或 LM Studio 跑的本地模型

偵測到之後，模型必須「證明自己能回答問題」才會被存入設定。這避免了以前常見的問題——使用者設了一個模型但其實連不上，結果一直報錯。

地端模型方面有幾個重要變動：

- **node-llama-cpp 換成 managed llama-server**：推理引擎改用獨立管理的 llama-server process，穩定性提升
- **預設地端模型改成 Gemma 4**
- **Context window 擴到 64K tokens**：對長文件處理場景很有幫助

另外，`codex/*` 和 `openai-codex/*` 的 model route 在 2.0 會自動遷移到 `openai/*`，可以用 `openclaw doctor --fix` 自動處理。不過有個已知 bug：如果沒有 TTY（比如在 cron 或自動化腳本裡跑），`doctor --fix` 會靜默跳過遷移，可能導致 Gateway crash。

---

## 六、Memory 架構：內建記憶取代外掛

2.0 把記憶系統從外掛（QMD plugin）拉進核心。新的記憶架構支援背景整合（background consolidation），會自動把對話中有來源追溯的素材沉澱到長期記憶。

這個改動讓 OpenClaw 的記憶不再依賴外部工具或手動整理。Agent 會自行累積操作脈絡，跨 session 保持連續性。

Skill Workshop 也加入了驗證流程——修改 skill 之前會先驗證變更是否合理，不會直接寫入。這對多人使用的場景很重要，避免有人不小心改壞了共用的 skill。

---

## 已知問題

2.0 的架構方向整體是對的——SQLite 比散落檔案可靠、shared session 是團隊協作的基礎、Gateway 信任邊界終於講清楚了。但有幾個已知問題值得注意：

- **`doctor --fix` 在無 TTY 環境靜默失敗**：自動化腳本環境升級後要特別檢查
- **Gemini embedding batch 超過 API limit**：會導致 memory sync 中斷
- **Legacy 安裝的 plugin consent 未持久化**：升級後可能需要重新授權
- **Secret Store 的值沒有 at-rest encryption**：API key 存在 Gateway 的 Secret Store 裡不是加密的

這些是 Day One 問題，官方在發布兩天後就推了 [v2026.8.2 hotfix](https://github.com/openclaw/openclaw/releases/tag/v2026.8.2) 修升級相關的 breaking bugs。但在正式環境裡，升級前務必完成備份和測試。

---

## X 社群怎麼看這次改版

官方公告在 X 上拿到 6,700+ likes、300 萬 views，聲量很大。但社群的實際體感是分裂的。

**正面的部分集中在 UX。** Onboarding 自動偵測已有的 AI 資源、瀏覽器直接開聊天、密碼不再出現在 chat 裡——這些改動讓第一次接觸的人感覺門檻降低了不少。多人協作和 session 搜尋也是被提到最多的亮點。

**批評集中在穩定性和實際體驗。** 有人直接說「impressive concept, frustrating product——capability 不等於 product quality」，指出 agent 還是會陷入 loop、需要 babysitting。用了幾個月的老用戶也反映 2.0 在穩定性上是退步的——「unstable、gets itself in weird loops、wonky」。更有人三次嘗試安裝全部失敗：app 打不開、gateway 壞掉、登入時電腦直接凍住。

**安全性是最大的爭議點。** The Register 的標題最直接：「OpenClaw 2.0 pours glitter on slow-burning security dumpster fire」。具體的批評包括：

- Sandbox 預設關閉，使用者要自己手動開
- Secret Store 沒有 at-rest encryption，完全靠 filesystem permissions
- Shared sessions 明確不是 security boundary

安全社群的質疑可以濃縮成一句話：**讓更多人更容易跑起來一個預設不安全的系統，不一定是好事。**

不過也有人持相反觀點——認為 OpenClaw 在開源 agent 裡已經是安全做得比較認真的，272K 筆 prompt injection 測試數據至少證明他們有在量化這件事。

整體風向：**方向認可、Day One 體驗落差大。** Hype 和 hands-on 之間有明顯的 gap，這在大型開源專案的 major release 並不少見。

---

## 跟 Hermes Agent 比，差距在哪

討論 OpenClaw 2.0 的架構，繞不開另一個 2026 年崛起的開源 agent 框架——Nous Research 的 [Hermes Agent](https://hermes-agent.nousresearch.com/)。兩者都是 local-first、model-agnostic、MIT-licensed，但設計哲學完全不同。

**OpenClaw 是 gateway 平台思維**——一個 Gateway 管多個 agent session，強調組織層級的多人協作和 breadth of integration。TypeScript 寫的，345K+ GitHub stars。

**Hermes 是 self-improving single agent 思維**——核心賭注是 agent 應該隨時間自我提升。2026 年 2 月上線，64K+ stars。到 6 月在 OpenRouter 的 daily token usage 已經超過 OpenClaw（224B vs 186B）。

六個關鍵差異：

| 維度 | OpenClaw 2.0 | Hermes Agent |
|------|-------------|--------------|
| 記憶系統 | 2.0 剛從 QMD plugin 拉進核心，background consolidation | Day 1 就是五大支柱之一，user.md + memory.md + SQLite-backed store，closed learning loop |
| 自我提升 | 沒有。Skill Workshop 驗證修改，但 agent 不會自己學新 skill | 核心設計。完成複雜任務後自動寫 reusable skill，越用越強 |
| 多 agent | Shared Cloud Sessions 多人共用 context | Profile 系統——每個 profile 獨立 config / memory / gateway PID，並行但隔離 |
| 安全模型 | 4 個 access mode，sandbox 預設關閉、Secret Store 不加密 | Tirith 安全層——approval workflow + allowlist + observable execution；截至 2026/06 零 CVE |
| 通訊渠道 | Browser + Mobile + CLI + 4 平台 | 16+ 平台 + 完整語音互動（STT + TTS） |
| Cron 排程 | 2.0 加入 automation，無效 config 建立前擋下 | First-class cron，fresh AIAgent instance，支援 skill attachment |

**最大的架構落差是 self-improving loop。** Hermes 完成任務後會把解法結構化成 skill，下次碰到類似問題直接調用。OpenClaw 2.0 的記憶系統做到了 background consolidation，但離「agent 自己寫 skill」還有一段距離。

**安全性差距也很明顯。** Hermes 的 Tirith 安全層是 safer-by-default——危險指令要 approval，所有 tool call 對使用者可見。OpenClaw 的 gateway 預設假設操作者是受信任的單一使用者，sandbox 和 execution approval 都關著。

不過 OpenClaw 的優勢也很清楚：enterprise breadth、multi-model routing、團隊多人共用 session、ClawHub 13,000+ skills 生態。如果需求是組織層級的 agent 管理，OpenClaw 目前沒有對手。如果重視長期使用的個人化和 agent 自我提升，Hermes 的架構方向更前面。

---

## 結語

OpenClaw 2.0 的 IT 架構改動，整體來說是在做基礎建設的升級：從檔案系統搬到資料庫、從單人假設擴展到多人協作、從模糊的安全邊界走向明確的信任域。

如果只是個人使用，這些改動大部分是透明的——升級、跑 `openclaw doctor --fix`、繼續用。

但如果已經在企業環境裡跑 OpenClaw，或者正在規劃部署，這次架構改動就值得花時間認真理解。因為這些基礎設施的選擇——SQLite 遷移的單向性、Gateway 信任邊界的粒度、shared session 的安全假設——會直接影響後續的部署架構和安全策略。而 Hermes Agent 在記憶、自我提升和安全預設上的設計，也值得拿來做為評估 agent 框架時的參照點。
