---
layout: post
title: "OpenClaw 2.0 架構拆解：七個子系統一次看完"
date: 2026-09-02 05:38:43 +0800
permalink: /openclaw-2-it-architecture-six-months-operator-perspective/
image: /assets/images/openclaw-2-detailed-architecture.png
description: "8 月 30 號，OpenClaw 推出了 2.0 版（版號 v2026.8.1）。官方自己的標題叫「OpenClaw 2.0, Accidentally」——意思是他們本來沒打算做一次大改版，結果改到最後回頭一看，動到的東西已經大到必須叫 2.0 了。"
---

> OpenClaw 2.0（v2026.8.1）是專案史上最大改版——16,977 個 PR、987 位貢獻者。這篇從 IT 架構師角度拆解七個子系統的變動：Session 儲存遷移、Shared Cloud Sessions 的分散式設計、Gateway 信任邊界與安全模型、Control UI 重寫、模型偵測機制、內建記憶與自我學習、以及 Secret Store 與權限管理。最後評估 OpenClaw 2.0 的架構成熟度，並跟 Hermes Agent 做正面比較。

![OpenClaw 2.0 Gateway 架構圖](/assets/images/openclaw-2-detailed-architecture.png)

---

8 月 30 號，OpenClaw 推出了 2.0 版（版號 v2026.8.1）。官方自己的標題叫「OpenClaw 2.0, Accidentally」——意思是他們本來沒打算做一次大改版，結果改到最後回頭一看，動到的東西已經大到必須叫 2.0 了。

以下從 IT 架構的角度拆七個子系統，每個都講它改了什麼、為什麼改、以及對實際部署的影響。

---

## 一、Session 儲存從檔案搬進 SQLite

這是 2.0 最底層、影響最大的一個改動。

舊版的 session 和 transcript（對話紀錄）都是以檔案形式存在硬碟上。2.0 把它們全部搬進 SQLite。

為什麼這件事重要？因為**這是一條單行道**。升級之後，新產生的 session 都只存在 SQLite 裡面。如果要降回舊版，得先用新版 CLI 把資料匯出成舊格式，否則那些 session 就看不到了。

這個改動帶來兩個面向的影響：

**好處是效能跟一致性。** 檔案形式的 session 在並發場景下容易碰到鎖定或讀寫衝突，尤其 transcript 量大的時候。SQLite 做為 embedded database，在並發讀取和 atomic write 上比散落的檔案穩定很多。2.0 啟用了 WAL（Write-Ahead Logging）模式，並加入了 WAL split-brain 保護——防止 WAL 檔案在異常關閉後出現不一致狀態導致資料損壞。

**備份不是口號，有具體機制。** 2.0 新增了 SQLite snapshot 功能：create / list / verify / restore，可以做 compact 的全域或 per-agent database 備份。升級前跑一次 `snapshot create`，驗證通過再動正式環境，這是官方建議的 SOP。

**跑 Docker Desktop 或 VM 共享目錄的人要特別注意。** SQLite 在共享檔案系統（virtiofs / 9p mount）上的 POSIX lock 不可靠是老問題。2.0 偵測到這類 mount 時會自動改用 rollback journal 而非 WAL，犧牲一點效能換穩定性。這個細節沒寫在 blog 裡，但 release notes 有。如果你的 Gateway 跑在 Docker 裡用 volume mount，這是直接影響你的改動。

---

## 二、Shared Cloud Sessions：不只是多人協作

2.0 加入了 Shared Cloud Sessions，表面上看是讓多個使用者可以加入同一個 agent session。但從架構角度看，這其實是一套**分散式 session 執行機制**。

Release notes 寫的是：session 可以搬到 paired devices 或 cloud workers 執行，workspace 跟著走。Cloud worker 閒置時會 suspend，下次收到訊息時 re-provision 新的 worker，同時保留 session 和已 reconciled 的 workspace。

這裡最值得架構師關注的是**一致性模型**。當本地和遠端的 workspace 出現分歧時，2.0 做 reconciliation——官方用語是 "staged-ref guidance, bounded conflicted paths"。白話講就是：分歧的檔案不會無聲覆蓋，會標記出來讓使用者處理。

但有一個非常重要的前提，官方文件講得很直白：

**Shared cloud sessions 不是 tenant isolation，也不是 security boundary。**

白話講就是——這功能假設參與的人都是「可信任的同事」。它不是設計來讓不同部門、不同公司的人共用同一個 Gateway 的。如果組織有多個業務單位需要資料隔離，就得部署多個 Gateway instance，每個有自己的 state、credentials 和 workspace。

**這裡的 tension 是：** Multiplayer 和 cloud workers 是分散式功能，蓋在單機 SQLite + 單信任域的地基上。2.0 用 reconciliation 補，但完整的一致性設計文件目前還沒公開。對於打算在生產環境跑多機協作的團隊，這是需要先搞清楚的。

---

## 三、Gateway 信任邊界與安全模型

2.0 把 Gateway 的安全模型講得更清楚了。

核心原則是 **one trust boundary per Gateway**。所有連上同一個 Gateway 的使用者，共享同一個信任域。Gateway 的預設姿態是：sandboxing 和 execution approval 都是關閉的，假設操作者是受信任的單一使用者。

如果需要管控，2.0 提供了四個層級的 access mode：
- **Read-only**：只能看不能動
- **Guarded**：需要逐次核准
- **Workspace**：限定在特定工作目錄
- **Full access**：完全授權

2.0 也加入了 **team operator roles**，可以限制特定操作者能存取哪些 agent、是否能看別人的 session、以及 operator scope 的範圍。Configuration 變更會記錄 writer label 並自動 redact 敏感值——這是企業環境第一個會問的 RBAC 和 audit trail，2.0 有了。

**安全預設是 opt-in，不是 opt-out。** Sandbox 預設關閉、execution approval 預設關閉。這跟 Docker daemon 以 root 跑是同一類 tradeoff——開發者工具可以接受，企業環境要靠 policy 硬化。不是「不安全」，是「安全是你自己要開的」。

在 prompt injection 防禦上，2.0 公布了一組測試數據：272K 筆群眾攻擊（crowdsourced attacks）、41 個 agent scenarios。架構師該怎麼讀這組數據？

| 模型 | Prompt Injection 成功率 |
|------|------------------------|
| Claude Opus 4.5 | 0.5% |
| Claude Sonnet 4.5 | 1.0% |
| Claude Haiku 4.5 | 1.3% |
| Gemini 2.5 Pro | 8.5% |

**重點不是數字好看，而是這告訴你 OpenClaw 把 injection 防禦外包給模型廠商。** Gateway 這層自己沒有做 input sanitization 或 output validation。模型選擇本身就是安全架構的一環，但這也意味著你的安全天花板取決於你選的模型。用 frontier model 跑機敏任務，0.5% 的攻擊成功率可能還行；換一個便宜的小模型跑同樣的場景，風險就完全不同了。

---

## 四、Control UI 重寫

Control UI 是在瀏覽器裡管理 OpenClaw 的 Web 介面，2.0 把它整個重寫了。JavaScript requests 從 140 個降到 45 個，啟動時間從 1.6 秒降到 575 毫秒（測試條件：50ms HTTP/1.1 latency，mocked Gateway）。UI 結構重新設計，session 可以用真實 browser tab 開多個，sidebar 可調寬度。

這是 frontend 效能優化，不是架構層面的改動，但對日常操作體驗影響很直接。

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

## 六、Memory 與自我學習

2.0 把記憶系統從外掛（QMD plugin）拉進核心。新的記憶架構支援背景整合（background consolidation），會自動把對話中有來源追溯的素材沉澱到長期記憶。

更重要的是，2.0 加入了 **automatic self-learning**。Agent 可以從對話中擷取有效的解法模式，自動產生 Skill Workshop proposal。這不是靜默改行為——每個 proposal 都進 pending 狀態，等 operator review 才 apply。

Self-learning 有三種模式：
- **off**：關閉
- **propose**：產生 pending proposal，需要人工審核後套用
- **auto**：掃描後自動套用（經 scanner 核准）

Skill Workshop 本身也加入了驗證流程——修改 skill 之前會先驗證變更是否合理，不會直接寫入。Manual history review 則是更保守的選項：掃最近 20 個 substantial sessions（至少 6 個 model turns），最多產生 3 個 pending proposals。

這跟 Hermes Agent 的 closed learning loop 方向一致，但設計選擇不同——OpenClaw 選擇了**可審計、可回滾的 review gate**，而不是直接寫入。後面比較段會再展開。

---

## 七、Secret Store 與權限管理

2.0 的 Secret Store 是最受批評的部分——API key 存在 Gateway 裡**沒有 at-rest encryption**，完全靠 filesystem permissions。The Register 的標題最直接：「pours glitter on slow-burning security dumpster fire」。

批評成立，但只看這一面不公平。2.0 同時做了幾件事來緩解：

- **Secret values 是 write-only**：寫入後無法從 API 讀回明文
- **1Password broker 整合**：用 service-account auth、per-secret approval、value-free audit，credential 可以不碰 OpenClaw 的 file system
- **Private credential request**：agent 可以請求 credential 但值不進 chat 也不進 model context
- **Credential egress 控制**：proxy connections、upstream requests、bypass tunnels 在 run 結束時自動關閉

所以實際的安全姿態是：如果只用內建 Secret Store，確實沒有 at-rest encryption。但如果接了 1Password broker，credential 全程不落地，比大多數自建方案都安全。**差距在 default vs configured。**

---

## 已知問題

- **`doctor --fix` 在無 TTY 環境靜默失敗**：自動化腳本環境升級後要特別檢查
- **Gemini embedding batch 超過 API limit**：會導致 memory sync 中斷
- **Legacy 安裝的 plugin consent 未持久化**：升級後可能需要重新授權

官方在發布兩天後就推了 [v2026.8.2 hotfix](https://github.com/openclaw/openclaw/releases/tag/v2026.8.2) 修升級相關的 breaking bugs。但在正式環境裡，升級前務必完成備份和測試。

---

## X 社群怎麼看這次改版

官方公告在 X 上拿到 6,700+ likes、300 萬 views，聲量很大。但社群的實際體感是分裂的。

**正面的部分集中在 UX。** Onboarding 自動偵測已有的 AI 資源、瀏覽器直接開聊天、密碼不再出現在 chat 裡——這些改動讓第一次接觸的人感覺門檻降低了不少。多人協作和 session 搜尋也是被提到最多的亮點。

**批評集中在穩定性和實際體驗。** 有人直接說「impressive concept, frustrating product——capability 不等於 product quality」，指出 agent 還是會陷入 loop、需要 babysitting。用了幾個月的老用戶也反映 2.0 在穩定性上是退步的——「unstable、gets itself in weird loops、wonky」。更有人三次嘗試安裝全部失敗：app 打不開、gateway 壞掉、登入時電腦直接凍住。

**安全性是最大的爭議點。** 具體批評包括 sandbox 預設關閉、Secret Store 沒有 at-rest encryption、shared sessions 明確不是 security boundary。安全社群的質疑可以濃縮成一句話：**讓更多人更容易跑起來一個預設不安全的系統，不一定是好事。**

不過也有人持相反觀點——認為 OpenClaw 在開源 agent 裡已經是安全做得比較認真的，272K 筆 prompt injection 測試數據至少證明他們有在量化這件事。

整體風向：**方向認可、Day One 體驗落差大。** Hype 和 hands-on 之間有明顯的 gap，這在大型開源專案的 major release 並不少見。

---

## OpenClaw 2.0 的架構成熟度

拆完七個子系統之後，退一步看整體：**OpenClaw 2.0 的架構 OK 嗎？**

答案取決於你的部署場景。

**對單一操作者或小型互信團隊、單機部署：架構是 OK 的，而且 2.0 是一次健康的還債式改版。**

好的部分全部是在「把散的收攏、把隱性行為變顯性」：file 搬 SQLite + WAL + snapshot、plugin memory 拉進 core、learning 進 review gate、config audit 記 writer label、1Password broker 整合。方向是對的。

**對企業平台級部署：還不是。** 原因有三個結構性限制：

第一，**SQLite 是單機、單 writer。** 這從根本上決定了一個 Gateway 就是一台機器的事。官方沒有 HA / clustering / multi-node 的敘事，甚至連 roadmap 都沒有暗示。

第二，**「一個 Gateway 一個信任域、要隔離就多開」等於把多租戶推給運維。** N 個 Gateway = N 份升級、N 份 secret store、N 份 snapshot backup。做得到，但這是線性成本，不 scale。

第三，也是最大的 tension：**Multiplayer 和 cloud workers 是分散式功能，蓋在單機 SQLite + 單信任域的地基上。** 2.0 用 reconciliation 處理分歧，但完整的一致性模型沒有公開文件。Cloud worker suspend / re-provision 的 failover 語意也不清楚——workspace 跟著走，但如果 worker 在寫入中途掛掉呢？

這不是說 OpenClaw 的架構有 bug。而是說它目前的定位是**開發者工具**，不是**基礎設施平台**。用同一把尺量兩者不公平。但如果你正在評估要不要把 OpenClaw 放進企業的 IT 架構裡，這三個限制是要明確標出來的。

---

## 跟 Hermes Agent 比，差距在哪

討論 OpenClaw 2.0 的架構，繞不開另一個 2026 年崛起的開源 agent 框架——Nous Research 的 [Hermes Agent](https://hermes-agent.nousresearch.com/)。兩者都是 local-first、model-agnostic、MIT-licensed，但設計哲學完全不同。

**OpenClaw 是 gateway 平台思維**——一個 Gateway 管多個 agent session，強調組織層級的多人協作和 breadth of integration。TypeScript 寫的，345K+ GitHub stars。

**Hermes 是 self-improving single agent 思維**——核心賭注是 agent 應該隨時間自我提升。2026 年 2 月上線，64K+ stars。Python 寫的，五大支柱架構（memory / skills / soul / crons / self-improving loop）。

六個關鍵差異：

| 維度 | OpenClaw 2.0 | Hermes Agent |
|------|-------------|--------------|
| 記憶系統 | 2.0 從 QMD plugin 拉進核心，background consolidation | Day 1 就是五大支柱之一，user.md + memory.md + SQLite-backed store，closed learning loop |
| 自我學習 | 有。Self-learning 產生 pending proposal，經 review gate 後套用（off / propose / auto 三模式） | 核心設計。完成任務後直接寫 reusable skill，closed loop 不需人工介入 |
| 隔離模型 | 「多開 Gateway」是運維手段，不是一等抽象 | Profile = 獨立 HERMES_HOME + config + memory + gateway PID，一等公民隔離 |
| 安全預設 | 4 個 access mode + team roles + audit，但 sandbox/approval 預設關閉 | Tirith 安全層——approval workflow + allowlist + observable execution，開箱即用 |
| 通訊渠道 | 20+ channels（Telegram 內建；Discord / Slack / WhatsApp / Signal / iMessage / Matrix / Teams / LINE 等 plugin） | 16+ 平台 + 完整語音互動（STT + TTS） |
| Cron 排程 | 2.0 加入 automation，無效 config 建立前擋下 | First-class cron，fresh AIAgent instance，支援 skill attachment |

### 修正幾個常見的比較誤區

**「OpenClaw 不會自我學習」是錯的。** 2.0 有 automatic self-learning，差別在設計選擇：OpenClaw 走 review gate（pending → operator apply），Hermes 走 closed loop 直接寫。架構師角度 OpenClaw 更可審計、可回滾；產品角度 Hermes 更自動。

**「OpenClaw 只支援 4 個通訊平台」是錯的。** 官方支援 20+ channels，Telegram 是 bundled，其餘以 plugin 安裝。跟 Hermes 的 16+ 平台基本打平，各自有對方沒有的平台。

**Hermes「零 CVE」不能直接當安全證據。** 到 2026 年 6 月 Hermes 才上線 4 個月，受到的安全審視跟運行 2 年多的 OpenClaw 不在同一個量級。零 CVE 可能只是還沒被認真看過。

### 真正的架構差距

**隔離是 Hermes 真的贏的地方。** Profile 是一等公民抽象——每個 profile 有自己的 HERMES_HOME、config、memory、sessions、gateway PID。OpenClaw 的「多開 Gateway」是運維手段，要自己管 N 份部署。這個差距不是功能問題，是抽象層級的問題。

**安全預設 Hermes 也贏。** Approval + allowlist + observable execution 開箱就有，不需要 operator 手動硬化。OpenClaw 的 team roles 和 audit trail 功能上不差，但預設是關的。

**生態與整合 OpenClaw 明顯贏。** 20+ channels、ClawHub 13,000+ skills、team operator roles、1Password broker、cloud workers、session workspace migration。Hermes 的 skill 生態更小但平均品質更高（stricter submission process）。

**一句話：Hermes 是「一個會長大的 agent」，OpenClaw 是「一群 agent 的作業平台」。** 選哪個看你是要管一個還是管一群。

---

## 結語

OpenClaw 2.0 的架構改動，整體來說是在做基礎建設的升級：從檔案系統搬到資料庫、從單人假設擴展到多人協作、從模糊的安全邊界走向明確的信任域、從手動整理記憶到帶 review gate 的自我學習。

作為開發者工具，這次改版方向正確、執行到位。作為企業基礎設施，SQLite 單機限制、信任邊界粒度、shared session 的安全假設還是結構性天花板。

如果只是個人使用，升級、跑 `openclaw doctor --fix`、繼續用。如果正在評估 agent 框架的 IT 架構，OpenClaw 跟 Hermes 代表了兩個不同方向的設計取捨——前者重平台廣度，後者重個體深度。而這些基礎設施的選擇，會直接影響後續的部署架構和安全策略。
