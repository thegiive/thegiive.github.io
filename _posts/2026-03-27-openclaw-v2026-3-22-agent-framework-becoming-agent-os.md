---
layout: post
title: "OpenClaw 三月大更新：Agent Framework 正在變成 Agent OS"
date: 2026-03-27 10:00:00 +0800
permalink: /openclaw-v2026-3-22-agent-framework-becoming-agent-os/
image: /assets/images/openclaw-v2026-3-22-release-tweet.png
description: "OpenClaw v2026.3.22 單次更新 312 條變更：18 條 breaking changes、74 條新功能、220 條修復。ClawHub 插件市場、GPT-5.4 全家桶、SSH Sandbox 取代 Docker、ACP Dispatch 原生 orchestration。更關鍵的是，OpenClaw 開始直接吞噬 Claude Code、Codex、Cursor 的 skill bundles——這不是版本更新，是 Agent Framework 變成 Agent OS 的宣告。"
tags: ["OpenClaw", "Agent OS", "ClawHub", "ACP Dispatch", "SSH Sandbox", "GPT-5.4", "Multi-agent"]
categories: ["AI Agent 實戰觀察"]
---

## 不只是版本更新

台灣時間 3 月 22 日，OpenClaw 迎來了近期最大規模的版本更新 v2026.3.22，由項目創始人 @steipete 親自推動。社群直接把它叫做「需要專屬目錄的超級更新」。

這個稱號不是誇張——我去拉了 [GitHub release notes](https://github.com/openclaw/openclaw/releases/tag/v2026.3.22)，**單次更新 312 條變更項目**：18 條 breaking changes、74 條新功能改進、220 條 bug fixes，release notes 本身就有 323 行。

但如果你只看 release notes，會低估這件事。

因為 3.22 只是最新的一塊拼圖。把它跟這一個月的 3.2、3.7 beta、3.8～3.12 連起來看，其實是一場連續重構。

**OpenClaw 正在從「可組裝的 Agent 框架」變成「內建 orchestration 的 Agent 作業系統」。**

這件事的意義，比任何單一功能都大。

---

## ClawHub：Agent 開始「自學」技能

本次更新最直觀的亮點是 **ClawHub 插件市場**正式成為預設的插件安裝源。

之前的 OpenClaw，插件主要靠 npm 安裝，你得手動找、手動裝、手動設定。現在不一樣了：

- **自主擴充：** Agent 可以自動搜索並拉取所需插件，不再受限於初始設定
- **安全驗證：** ClawHub 提供比 npm 更完整的技能包驗證機制，減少惡意代碼注入風險
- **搜尋力爆發：** 集成 Exa、Tavily、Firecrawl 等搜尋工具，支持精確日期過濾

用白話講：以前你養一隻蝦（OpenClaw Agent），要幫它一個一個裝工具。現在它自己會去市場上找需要的東西。

這聽起來像小事，但如果你跑過 OpenClaw 就知道——**Agent 的能力上限，很大程度取決於它能調用多少工具。** ClawHub 把這個瓶頸打開了。

---

## 模型適配：GPT-5.4 全家桶與獨立推理

在模型支持方面，OpenClaw 展現了驚人的適配速度：

- **GPT-5.4 全系列：** 原生支持 GPT-5.4、GPT-5.4-mini、GPT-5.4-nano
- **MiniMax M2.7：** 原生集成，為中文語境下的 Agent 任務提供更強支持
- **Per-agent reasoning：** 每個 Agent 可以有獨立的推理邏輯，不再共用全局設定

最後一點是真正值得關注的。

之前跑 multi-agent 時，所有 sub-agent 共用同一套推理設定。這在簡單場景沒問題，但當你需要「一個 Agent 負責搜尋、一個負責分析、一個負責寫報告」時，它們的推理深度和策略應該不同。

**Per-agent reasoning 等於承認了一件事：multi-agent 不是「複製貼上同一個大腦」，而是「組建不同專長的團隊」。**

---

## SSH Sandbox：擺脫 Docker 的執行環境革命

v2026.3.22 引入了 **OpenShell + SSH sandboxes** 架構，取代了過去對 Docker 的依賴。

這個改變解決了幾個實際痛點：

| 問題 | Docker 時代 | SSH Sandbox |
|------|------------|-------------|
| 冷啟動時間 | 數秒到數十秒 | 近乎即時 |
| 資源消耗 | 需要完整容器運行時 | 輕量 SSH 連線 |
| 安全隔離 | 容器層級 | 受保護密鑰 + 證書 |
| 環境設定 | 需要 Dockerfile | 直接使用 |

另一個容易被忽略的數字：**會話超時從 600 秒（10 分鐘）延長到 48 小時。**

10 分鐘的會話，基本上只能跑短任務。48 小時意味著 OpenClaw 開始支持長週期的自動化工作流——比如持續監控、定期報告生成、跨時區的協作任務。

這不是 feature，這是 **使用場景的根本擴展**。

---

## 3.2 版才是真正的架構轉折點

如果說 3.22 是「312 條變更的功能大禮包」，那 3.2 才是真正的架構分水嶺。

3.2 做了幾件 breaking change 等級的事：

### 1. 預設行為改了

新安裝會直接套用預設 tools 和 profiles，不再是「空白系統 + 自己組」。

這代表 OpenClaw 開始往**標準化 Agent runtime** 走。以前像是給你一堆零件自己拼，現在是出廠就能跑。

### 2. ACP Dispatch 預設開啟

Agent routing 和 sub-agent dispatch 直接內建，不用額外設定。

用技術語言說：**multi-agent orchestration 從「框架外」搬到「框架內」。** 之前你要用 LangChain、CrewAI 那種拼裝方式做 agent 協調，現在 OpenClaw 原生支持。

這其實是 multi-agent runtime native 化。

### 3. Plugin API 重寫

舊版：
```javascript
registerHttpHandler(...)
```

新版：
```javascript
registerHttpRoute({ path, auth, match, handler })
```

Plugin 不再只是 function hook，而是變成**完整的 API layer**——有 auth、有 routing。

換句話說：**Plugin 正在微服務化。**

### 4. CLI 運維成熟化

新增 `openclaw config validate`，更完整的部署前檢查流程。

這件事很關鍵，因為它意味著 OpenClaw 開始往 **production infrastructure** 靠，而不是停留在開發者工具。

---

## 一個月的演進脈絡：四條主線

如果只看 3.22 或 3.2 的單點更新，會錯過全貌。把這一個月串起來，有四條清晰的主線：

### 主線一：安全模型系統化

2 月底（v2026.2.23）就開始了：SSRF policy 改預設、security hardening、prompt 與 execution 風險修補。

重點轉變是：從「模型會亂來所以要 patch」變成「**系統邊界本身要能控制**」。

### 主線二：Agent Runtime 內建 Orchestration

從 2.19 到 3.2，ACP dispatch、agent routing、lifecycle control 陸續加入。

OpenClaw 正在變成 **Agent OS**——不只是讓 Agent 跑起來，而是管理 Agent 的生老病死。

### 主線三：Plugin / Context 全面模組化

3.7 beta 引入 ContextEngine plugin interface，context 可以 plug / unplug，同時修了 200+ bug。

這代表記憶（Memory）和上下文（Context）從 hardcode 變成 **plugin system**。你可以換記憶引擎，就像換資料庫一樣。

### 主線四：平台化能力

3.8～3.12 補上了 backup/restore CLI、agent lifecycle API（create/update/delete）、web_search provider（Grok）。

這些都是「企業會需要的東西」。

---

## 跟 Claude Code 的路線差異——不，應該說「吞噬」

看到這裡，你可能會問：OpenClaw 跟 Claude Code 的差別到底在哪？

我之前在[套殼 2.0 那篇文章](/shell-wrapper-2-anthropic-real-threat/)分析過，Claude Code 走的是「極致克制」路線——它把整台電腦當成狀態空間，但刻意不做持續性、不做可觀測性、不做跨設備控制。

但 3.22 的 release notes 讓我看到一個更激進的事實：**OpenClaw 不只是走相反方向，它正在把對手直接吞進來。**

這次更新裡有幾條不太起眼但意義巨大的變更：

- **`Plugins/bundles: add compatible Codex, Claude, and Cursor bundle discovery/install support`** — OpenClaw 現在可以直接安裝 Claude Code、Codex、Cursor 的 skill bundles，把它們的能力映射成自己的 skills
- **`Plugins/marketplaces: add Claude marketplace registry resolution`** — 直接對接 Claude 的 marketplace，你在 Claude 生態裡的插件，OpenClaw 也能裝
- **`Models/Anthropic Vertex: add core anthropic-vertex provider support`** — 通過 Google Vertex AI 直接調用 Claude 模型

這三條加起來，意思很清楚：**OpenClaw 把 Claude Code、Codex、Cursor 都當成自己的「器官」來用了。**

你的 Claude Code skills？OpenClaw 能裝。你的 Codex 工作流？OpenClaw 能跑。你的 Cursor 擴充套件？OpenClaw 能用。

這就是社群所說的全面「龍蝦化」——OpenClaw 這隻蝦，正在把整個 AI coding 工具鏈的能力都長到自己身上。

加上 ACP dispatch 讓 sub-agent 可以原生路由、Feishu/Telegram/Discord/Matrix 全通道 ACP 綁定、per-agent reasoning 獨立推理——它不只是在「包裝」這些工具，而是在建一個**能調度所有 AI coding 工具的統一 runtime**。

這讓原本的「Claude Code vs OpenClaw」對比表需要重寫：

| 維度 | Claude Code | OpenClaw（3.22 之後） |
|------|-------------|----------------------|
| 設計哲學 | Unix 哲學，做好一件事 | 全包式 Agent OS |
| 對其他工具的態度 | MCP 標準協議，各自獨立 | 直接吞進來當 bundle |
| Orchestration | 不內建，靠外部工具 | ACP dispatch 原生支持 |
| 記憶系統 | CLAUDE.md（極簡） | SOUL.md + AGENTS.md + ContextEngine（可插拔） |
| Plugin 生態 | MCP（標準協議） | ClawHub + Claude marketplace + npm |
| 通道支持 | Terminal | Telegram / Discord / Feishu / Matrix / Android / Web |
| 安全模型 | 沙箱 + 權限確認 | SSH sandbox + SSRF policy + env sandbox |
| 適合場景 | 開發者日常工作 | 長期運行的全通道 Agent |

哪個好？這已經不是「好不好」的問題了。

**Claude Code 是一把精準的手術刀。OpenClaw 想做的是整個手術室。**

如果你的需求是「讓 AI 幫我寫 code、改 bug、做 DevOps」，Claude Code 的克制依然是優勢——簡單、快、不會搞出一堆你不理解的狀態。

但如果你的需求是「部署一個 7×24 跑的客服 Agent、能自動學新技能、能跟其他 Agent 協作、還能同時調度 Claude 和 GPT-5.4 做不同任務」——OpenClaw 正在用 312 條更新告訴你：它想做這件事，而且它動真格的。

---

## 對企業落地的意義

我在[NemoClaw 那篇](/nemoclaw-vs-openclaw-enterprise-starting-line/)提過，企業落地 Agent 卡在三件事：資料怎麼控、行為怎麼控、流程怎麼控。

這一個月 OpenClaw 的更新，其實在逐一回應：

- **資料怎麼控** → SSH sandbox 隔離 + SSRF policy
- **行為怎麼控** → ACP dispatch + per-agent reasoning + config validate
- **流程怎麼控** → agent lifecycle API + backup/restore + audit log

不是說這些已經足夠讓企業直接用。但方向很明確：**OpenClaw 知道自己要進企業，而且正在補該補的東西。**

搭配 NVIDIA 的 NemoClaw 在 GTC 上的亮相，可以看出整個生態正在形成一個共識：

**Agent 不能只在 Demo 裡跑，必須有 production-grade 的 runtime。**

---

## 坦白說

講了這麼多利好，該潑點冷水。

**第一，生態還是很早期。** ClawHub 上的插件數量和品質，跟 npm 或 VS Code marketplace 完全不在同一個量級。「Agent 自學新技能」聽起來很酷，但實際上可用的技能包還不夠多。

**第二，穩定性是個問號。** 光 3.22 一個版本就有 18 條 breaking changes，一個月內連續做架構級重構（3.2 改預設行為、3.7 重寫 context engine、3.22 換執行環境），對正在 production 跑的用戶來說是災難。社群已經有人抱怨升級後 Agent 行為完全不同。

**第三，「Agent OS」是願景，不是現實。** 現在的 OpenClaw 離真正的 OS 還有很長的路。沒有完整的權限管理、沒有資源排程、沒有多租戶隔離。把它叫做 OS 有點像是把毛胚屋叫做智慧住宅。

**第四，Token 成本問題沒解決。** 我之前[拆解過 OpenClaw 的 Token 消耗](/openclaw-architecture-deep-dive-context-memory-token-crusher/)，SOUL.md + AGENTS.md 的全量載入設計，在 GPT-5.4 上只會更貴。ClawHub 插件越多、context 越豐富，帳單越嚇人。

**第五，跟 Claude Code 的競爭還沒真正開始。** Anthropic 在 MCP 協議上的佈局、Claude Code 持續的產品打磨、加上模型本身的能力提升——OpenClaw 的「全包」路線能不能跑贏 Claude Code 的「極致克制」，現在下結論太早。

不過話說回來，**方向是對的。**

Agent 確實需要比「框架」更多的東西。它需要 orchestration、需要 lifecycle management、需要安全邊界、需要持久化。這些東西，總得有人做。

OpenClaw 選擇自己全做。Claude Code 選擇讓生態來補。最後誰贏，可能不取決於技術，而是取決於哪邊的生態更快成熟。

---

## 常見問題 Q&A

**Q: 升級到 v2026.3.22 需要注意什麼？**

狀態目錄從 `~/.moltbot` 遷移到了 `~/.openclaw`，升級前務必備份。另外 Plugin API 也改了，舊的 `registerHttpHandler` 需要遷移到新的 `registerHttpRoute` 格式。

**Q: SSH Sandbox 跟 Docker 比，安全性有沒有降低？**

不同層級的隔離。Docker 是容器級隔離，SSH sandbox 靠密鑰和證書保護。對大多數場景夠用，但如果你需要完整的 OS 級隔離（比如跑不信任的第三方代碼），Docker 還是更適合。

**Q: 現在適合把 OpenClaw 用在 production 嗎？**

看場景。如果是內部工具（客服 bot、報告生成），可以謹慎嘗試。如果是面向客戶的關鍵服務，建議再等 2-3 個版本穩定下來。一個月三次 breaking change 的節奏，不適合 production。

**Q: OpenClaw 跟 Claude Code 該選哪個？**

不是二選一。Claude Code 適合開發者日常（寫 code、debug、DevOps），OpenClaw 適合長期運行的自動化 Agent。很多人兩個都用——用 Claude Code 開發，用 OpenClaw 部署 Agent。

---

## 延伸閱讀

- [從「套殼 1.0」到「套殼 2.0」：為什麼真正該緊張的是 Anthropic](/shell-wrapper-2-anthropic-real-threat/)
- [OpenClaw 記憶系統全解析：SOUL.md、AGENTS.md 與高昂的 Token 成本](/openclaw-architecture-deep-dive-context-memory-token-crusher/)
- [NemoClaw 不是終局，但企業 Agent 這塊田很大](/nemoclaw-vs-openclaw-enterprise-starting-line/)
- [Peter Steinberger 的 Agentic Engineering 哲學](/peter-steinberger-agentic-engineering-just-talk-to-it/)
