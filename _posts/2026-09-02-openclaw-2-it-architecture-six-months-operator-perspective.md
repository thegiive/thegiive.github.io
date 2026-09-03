---
layout: post
title: "OpenClaw 2.0 架構拆解：改了什麼、跟 Hermes 怎麼比、我的期許"
date: 2026-09-02 11:38:30 +0800
permalink: /openclaw-2-it-architecture-six-months-operator-perspective/
image: /assets/images/openclaw-2-detailed-architecture.png
description: "OpenClaw 2.0 發布了。這是 AI 時代的頭部 Project，裡面 16,977 個 PR、987 位貢獻者。官方自己的標題叫「OpenClaw 2.0, Accidentally」——意思是他們本來沒打算做一次大改版，結果改到最後回頭一看，動到的東西已經大到必須叫 2.0 了。"
---

> OpenClaw 2.0（v2026.8.1）發布了——16,977 個 PR、987 位貢獻者，專案史上最大改版。這篇從 IT 架構師角度拆主要變化，跟 Hermes Agent 做定位比較，最後講我對 OpenClaw 的期許。企業數位助手的根本問題是：一群人用一個助手，還是每個人有自己的助手？

![OpenClaw 2.0 Gateway 架構圖](/assets/images/openclaw-2-detailed-architecture.png)

---

OpenClaw 2.0 發布了。這是 AI 時代的頭部 Project，裡面 16,977 個 PR、987 位貢獻者。官方自己的標題叫「OpenClaw 2.0, Accidentally」——意思是他們本來沒打算做一次大改版，結果改到最後回頭一看，動到的東西已經大到必須叫 2.0 了。

又到了保證無聊的 IT 日。我從 IT 架構師角度拆 OpenClaw 2.0 的主要變化。

---

## 2.0 改了什麼

一開始簡單說，最大的差別是 onboarding UI 更加簡單，可以讓更多人快速上手。自動偵測機器上已有的 AI 資源——已登入的 ChatGPT、Claude CLI、系統裡的 API key、透過 Ollama 或 LM Studio 跑的本地模型——偵測到之後模型必須「證明自己能回答問題」才會被存入設定。Control UI 也整個重寫了，JS requests 從 140 降到 45，啟動時間從 1.6 秒降到 575 毫秒。

除此之外，幾個比較大的變化：

### Session 儲存從檔案搬進 SQLite

檔案系統是一開始 OpenClaw 最有趣的設計，當然也是草創期的象徵。2.0 把 session 和 transcript 全部搬進 SQLite，啟用 WAL（Write-Ahead Logging）模式，並加入 WAL split-brain 保護。

為什麼這件事重要？因為**這是一條單行道**。升級之後新產生的 session 都只存在 SQLite 裡，要降回舊版得先用新版 CLI 匯出成舊格式。

好處是並發穩定性。檔案形式的 session 在並發場景下容易碰到鎖定或讀寫衝突，SQLite 的 atomic write 穩定很多。備份也不再是口號——2.0 新增了 `openclaw backup` 系列指令（`backup create` / `backup sqlite create|list|verify|restore` / `backup git create|list|verify|restore`），升級前跑一次 backup 是官方建議的 SOP。

**跑 Docker 的人要特別注意：** SQLite 在共享檔案系統上的 POSIX lock 不可靠。2.0 偵測到 virtiofs、9p、NFS、SMB 這類 mount 會自動改用 rollback journal 而非 WAL，犧牲一點效能換穩定性。使用者文件有寫 NFS/SMB 的退回行為，但 virtiofs / 9p 這兩個名字幾乎只出現在 release notes（PR #120597）裡，Docker Desktop 使用者容易漏掉。

### Shared Cloud Sessions

表面上看是讓多人共用 agent session，但從架構角度看，這其實是一套**分散式 session 執行機制**。

Gateway 持有一切持久狀態——對話記錄、workspace、credentials、session metadata。Cloud workers 是無狀態的執行單元，用完就丟，下次開新的。API key 不給 worker，model 查詢全部回 Gateway 轉發。方便後面 scale。

Session 可以跑在三個地方：本機 Gateway（預設）、自己的硬體（`openclaw connect`）、或租來的拋棄式雲端機器（透過 Crabbox provisioner，支援 AWS / Hetzner 等）。Cloud worker 閒置時會 suspend（`suspendAfter` 設定最低 1 分鐘），下次收到訊息時 re-provision 新的 worker。Session 在 sidebar 裡全程不消失。

一致性模型上，正常停機會先 reconcile workspace 再釋放機器。唯一的資料遺失窗口是非正常停機（crash / 斷網）時最後一次同步之後的變更。分歧的檔案不會無聲覆蓋，會標記出來讓使用者處理。

但有一個非常重要的前提：**Shared cloud sessions 不是 tenant isolation，也不是 security boundary。** 這功能假設參與的人都是「可信任的同事」。不同部門、不同公司要資料隔離，就得部署多個 Gateway instance。

**這裡最大的 tension 是：** Multiplayer 和 cloud workers 是分散式功能，蓋在單機 SQLite + 單信任域的地基上。完整的一致性設計文件目前還沒公開。

### 安全模型

2.0 把安全講清楚了。核心原則是 **one trust boundary per Gateway**，所有連上同一個 Gateway 的使用者共享同一個信任域。

四個 session permission mode（注意：前三個都鎖在 sessionRoot，差別在 exec 誰審）：
- **Read-only**：只能讀 sessionRoot，exec 直接 deny
- **Guarded**：可讀寫 sessionRoot，exec 走 allowlist，miss 才問人
- **Workspace**：一樣鎖在 sessionRoot，exec 先 LLM review，人是 fallback
- **Full access**：不限 filesystem，需要 operator.admin

加上 **team operator roles**——限制特定操作者能存取哪些 agent、是否能看別人的 session。Configuration 變更記錄 writer label 並自動 redact 敏感值，企業環境要的 RBAC 和 audit trail 有了。

**安全預設是 opt-in，不是 opt-out。** Sandbox 預設關閉、execution approval 預設關閉。這跟 Docker daemon 以 root 跑是同一類 tradeoff——開發者工具可以接受，企業環境要靠 policy 硬化。

另外 OpenClaw 用 272K 筆群眾提交的攻擊做 prompt injection 測試，數據很好看：

| 模型 | Prompt Injection 成功率 |
|------|------------------------|
| Claude Opus 4.5 | 0.5% |
| Claude Sonnet 4.5 | 1.0% |
| Claude Haiku 4.5 | 1.3% |
| Gemini 2.5 Pro | 8.5% |

Gateway 不是完全不做防禦——外部內容會用 `<<<EXTERNAL_UNTRUSTED_CONTENT>>>` wrapping 標記，會清掉 Qwen / ChatML / Llama / Gemma 等 special tokens 避免偽造 role boundary，outbound 也會剝 `<tool_call>` 這類 scaffolding。但**主防線仍然是模型本身** + tool policy + sandbox + allowlist，Gateway 做的是輔助清理，不是完整的 input sanitization。你的安全天花板仍然取決於你選的模型。用 frontier model 跑機敏任務，0.5% 可能還行；換一個便宜的小模型跑同樣的場景，風險完全不同。

### Self-learning

2.0 把記憶系統從外掛（QMD plugin）拉進核心，加入背景整合（background consolidation）。更重要的是加入了 **automatic self-learning**——agent 從對話中擷取有效的解法模式，自動產生 Skill Workshop proposal。

三種模式：off（關閉）、propose（產生 pending proposal，需人工審核）、auto（scanner-gated 自動套用）。**但出廠預設是 auto + approvalPolicy auto**——agent 可以自己 apply / reject / quarantine，不需要人審。要走 review gate（pending → operator apply）要自己把 approvalPolicy 改成 `pending`。

這個出廠預設很重要：它代表 **OpenClaw 2.0 的 self-learning 出廠行為其實跟 Hermes 的 closed loop 比想像中更接近**——都是自動寫入。企業要的 review gate 是能力，不是預設。這又是一個「安全是 opt-in」的例子。

Manual history review 更保守——掃最近 20 個 substantial sessions（至少 6 個 model turns），最多產生 3 個 pending proposals。

### Secret Store

2.0 最受批評的部分——API key 存在 Gateway 裡**沒有 at-rest encryption**，完全靠 filesystem permissions。The Register 的標題最直接：「pours glitter on slow-burning security dumpster fire」。

批評成立，但只看這一面不公平。2.0 同時做了：
- **Secret values 是 write-only**：寫入後無法從 API 讀回明文
- **1Password broker 整合**：credential 可以不碰 OpenClaw 的 file system
- **Private credential request**：值不進 chat 也不進 model context
- **Credential egress 控制**：proxy connections 在 run 結束時自動關閉

接了 1Password broker 之後 credential 全程不落地。**差距在 default vs configured。**

### 其他變動與已知問題

產品變更：
- 地端推理引擎從 node-llama-cpp 換成 managed llama-server，預設模型改 Gemma 4，context window 擴到 64K
- `codex/*` / `openai-codex/*` model route 自動遷移到 `openai/*`，可用 `openclaw doctor --fix` 處理

發布時的已知問題（部分可能已在後續版本修復）：
- Gemini embedding batch 超過 API limit，會導致 memory sync 中斷（8.1 已有 streaming / timeout 相關 PR）
- Legacy 安裝的 plugin consent 未持久化，升級後可能需要重新授權

後續版本 [v2026.8.2](https://github.com/openclaw/openclaw/releases/tag/v2026.8.2) 不是 hotfix——是正式版本，784 PRs、134 contributors，新增 Home 按鈕、Linux desktop companion、background sessions、四套 Control UI theme，同時也修了升級相關的問題。

---

## 跟 Hermes Agent 比

我很少寫 Hermes 的原因，是因為我一直認為 OpenClaw 是更適合企業數位助手的 Agent，但 Hermes 更適合個人。

沒有高下，是定位不同。我認為企業數位助手的根本問題是：**一群人用一個助手，還是每個人有自己的助手？**

### OpenClaw = 一群人的助手

OpenClaw 的 Gateway 模型天生就是這個方向。Shared sessions、team roles、多人共用 context，同事接手不用重講脈絡。一個 Gateway 管多個 agent session，強調組織層級的多人協作和 breadth of integration。TypeScript 寫的，388K+ GitHub stars。

### Hermes = 一個人的專家

Hermes 的 profile 模型更偏後者：每個 profile 獨立 memory、獨立 soul、越用越像那個人。核心賭注是 agent 應該隨時間自我提升。2026 年 2 月上線，64K+ stars，Python 寫的，五大支柱架構（memory / skills / soul / crons / self-improving loop）。

### 五個維度的比較

| 維度 | OpenClaw 2.0 | Hermes Agent |
|------|-------------|--------------|
| 生態 | 20+ 企業頻道（Slack、Teams、LINE、Feishu 都有 plugin），ClawHub 13,000+ skills | 16+ 平台偏消費端（WhatsApp、Signal、Discord），skill 生態小但品質高 |
| 安全預設 | Sandbox / approval 預設關閉，要 operator 自己開 | Tirith 安全層開箱即用（approval + allowlist + observable execution） |
| 隔離 | 多開 Gateway 硬做，N 租戶 = N 份維運成本 | Profile 一等公民——獨立 home、config、memory、gateway PID |
| 自我學習 | 有 review gate 能力，但出廠預設是 auto-apply（跟 Hermes 接近） | Closed loop：直接寫 skill，累積快但沒 audit trail |
| 協作 | Shared sessions + team roles + config audit | 單人模型，同事接手做不到 |

具體到企業數位助手，決定性的不是 channel 數量，是 channel 種類。Slack Enterprise Grid、MS Teams、Google Chat、Feishu、LINE 這些是企業在用的——OpenClaw 有，Hermes 沒有。

在自我學習上，OpenClaw 有 review gate 的能力（approvalPolicy 設成 pending），這是企業要的。但出廠預設是 auto-apply，跟 Hermes 的 closed loop 其實很接近——都是 agent 學到東西自動上線。差別在 OpenClaw 可以切到 pending 模式，Hermes 目前沒有這個選項。對企業來說，能力有但預設沒開，等於還是要靠 operator 記得去改設定。

### Hermes 贏的企業場景

反過來看，Hermes 在企業裡也有明確贏的位置：

**每個人一個助手。** 高階主管助理、每個工程師自己的 agent、每個業務自己的 agent，「一人一隻、資料互不相通」的模型，Hermes 原生設計，OpenClaw 要靠多開 Gateway 硬做。

**無人值守的排程。** Hermes 的 cron 是 first-class：每個 job 開 fresh AIAgent instance，可以 attach skill，結果送到任何平台。每日報表、備份檢查、晨間簡報。OpenClaw 也有 cron / heartbeat / standing orders，但 Hermes 的排程設計從 Day 1 就是核心支柱。

**安全預設要求高的環境。** 金融、醫療這種「不能靠 operator 記得去開 sandbox」的場景，Tirith 的 safer-by-default 是實質差異。

**單一領域的累積型專家。** 客服 triage、特定 codebase 的維護 agent、法遵查核，「同一件事做幾百次、越做越準」，compounding 才看得到。

**地端 / edge 部署。** NVIDIA 跟 Hermes 有 RTX / DGX Spark 的合作，self-hosted、無 telemetry。

### 實務上怎麼放

不是二選一，是按場景切。OpenClaw 當 front door 和 team 層，是團隊的數位助手。Hermes 當 per-person 數位助手，但是他更了解你。

一個可能的架構是 OpenClaw 當統一入口和協作層，Hermes 當個人專家和排程層。但兩者之間目前沒有現成的整合路徑，這一段要自己接。

---

## 對 OpenClaw 的期許

### X 社群怎麼看

官方公告在 X 上拿到 6,700+ likes、300 萬 views，聲量很大。但社群的實際體感是分裂的。

正面的部分集中在 UX——onboarding 自動偵測、瀏覽器直接開聊天、密碼不再出現在 chat 裡，門檻降低了不少。

批評集中在穩定性——有人直接說「impressive concept, frustrating product——capability 不等於 product quality」，agent 還是會陷入 loop、需要 babysitting。更有人三次嘗試安裝全部失敗。

安全性是最大的爭議點。安全社群的質疑濃縮成一句話：**讓更多人更容易跑起來一個預設不安全的系統，不一定是好事。**

整體風向：**方向認可、Day One 體驗落差大。**

最近看到 X 上網友討論，大家都在問「OpenClaw 到底涼了嗎？」

### 其實越來越切進企業

有趣的是，我反而認為 OpenClaw 越來越切進企業。

NVIDIA 老黃在 GTC 2026 直接說 OpenClaw 是「personal AI 的 Linux」——「Mac and Windows are the OS for the personal computer. OpenClaw is the OS for personal AI.」NVIDIA 還發布了 NemoClaw，企業級 stack 把 Nemotron 模型 + OpenShell runtime 疊在 OpenClaw 上面，一鍵安裝，主打隱私、安全、可擴展。TechCrunch 評 NemoClaw 正好補 OpenClaw 最弱的安全環節。

OpenClaw 6 月在 Microsoft Build 也提出 Windows 原生支援——透過 Microsoft Execution Containers（MXC），不用再裝 WSL2。Microsoft 出了 Windows Hub 配套 app（WinUI，支援 Win10 / Win11 / ARM64），有系統匣整合、自動更新、code signing。

這些動作慢慢往更多企業支援走進去。

### 三個結構性的期許

但要從開發者工具走到企業基礎設施，有三件事繞不過去：

**一、SQLite 單機單 writer 要有下一步。** 不一定是換 Postgres，但至少需要 HA 或 read replica 的敘事。現在 Multiplayer 和 cloud workers 是分散式功能，蓋在單機地基上，這個 tension 遲早要面對。

**二、預設值要翻過來。** 不只是 sandbox 和 approval 預設關閉——Skill Workshop 的 self-learning 出廠也是 auto-apply，不是 review gate。對個人開發者這些預設都沒問題，但每多一個企業用戶就多一個「忘記改設定」的風險。Hermes 的 Tirith 證明了 safer-by-default 不會犧牲開發體驗。

**三、隔離需要一等抽象。** 「要隔離就多開 Gateway」是能用但不 scale 的答案。N 個 Gateway = N 份升級、N 份 secret store、N 份 snapshot backup。如果 OpenClaw 想進企業多租戶場景，profile 或 namespace 級別的隔離是必要的。

做到這三件，OpenClaw 就不只是最好的開源 agent 開發者工具，而是真正的企業 agent 平台。

### 個人感受

我自己的感受就是我那四隻蝦子（四個 OpenClaw agent）依舊活得好好的，每天跟我有良好的互動跟幫忙。我真心期待他越做越好。OpenClaw 不會變成唯一的 Agent 框架，但是他在我的人機協作流程裡面越來越不可或缺。
