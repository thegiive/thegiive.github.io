---
layout: post
title: "NemoClaw 不是終局，但企業 Agent 這塊田很大"
date: 2026-03-23 08:30:00 +0800
permalink: /nemoclaw-vs-openclaw-enterprise-starting-line/
image: /assets/images/nemoclaw-enterprise-starting-line-cover.png
description: "「如今全球每一家公司，都必須制定自己的 OpenClaw 策略。」— 黃仁勳，GTC 2026。NemoClaw 明顯不是終局產品，但卻是一個很清楚的 signal：企業級 AI Agent 這塊田還很大。先 OpenClaw 做試點，再補 governance——不要一開始就上 enterprise framework，也不要永遠停在 POC。"
---

# NemoClaw 不是終局，但企業 Agent 這塊田很大

> 「如今全球每一家公司，都必須制定自己的 OpenClaw 策略。」
>
> 黃仁勳在 2026 年 GTC 開幕演講中表示：「OpenClaw 已經成為排名第一、也是人類歷史上最受歡迎的開源專案。而且它只用了短短幾週，就超越了 Linux 在 30 年累積的成果。這件事的重要性可見一斑，它的影響力將會非常巨大。」

**作者：** Wisely Chen
**日期：** 2026 年 3 月
**系列：** AI Agent 實戰觀察
**關鍵字：** NemoClaw, OpenClaw, NVIDIA, Enterprise AI Agent, GTC 2026, AI Infrastructure

---

## 目錄

- [不是企業版 OpenClaw，是一個 Signal](#不是企業版-openclaw是一個-signal)
- [企業落地卡在哪裡](#企業落地卡在哪裡)
- [OpenClaw 的封印與限制](#openclaw-的封印與限制)
- [NemoClaw 在補哪個洞](#nemoclaw-在補哪個洞)
- [工程角度快速拆解](#工程角度快速拆解)
- [現實：安裝不絲滑，生態還小](#現實安裝不絲滑生態還小)
- [NVIDIA 做的是一個方向，不是答案](#nvidia-做的是一個方向不是答案)
- [更實際的策略](#更實際的策略)
- [坦白說](#坦白說)

---

## 不是企業版 OpenClaw，是一個 Signal

GTC 2026 上，NVIDIA 跟 OpenClaw 作者 Peter 合作推出了 NemoClaw。

很多人第一反應是：「企業版 OpenClaw 來了。」

但我自己的看法比較簡單：**這明顯不是終局產品，不過卻是一個很清楚的 signal——企業級的 Agent 這塊田還很大。**

---

## 企業落地卡在哪裡

過去一年，大家都在做 AI Agent。

但實際落地到企業時，會卡在三件事：

- **資料怎麼控**（法務 / 隱私）
- **行為怎麼控**（資安）
- **流程怎麼控**（稽核 / audit）

結果就是很多 Demo 很驚艷，但真正進 production 的很少。

---

## OpenClaw 的封印與限制

OpenClaw 告訴大家，當解開 ChatBot 封印的 LLM 可以做出多誇張的東西。它可以像一個真人一樣操作你的電腦：開瀏覽器、登 Gmail、填表單、排行事曆。那個「computer use」的體驗，才是讓人覺得「這才是 AI Agent」的核心。

但它的預設是：個人環境、本地資料、使用者自行負責風險。

一進企業就會出現問題：資料直接經過外部 LLM API、沒有集中 policy、audit trail 不完整。所以很多公司不是不想用，而是**不敢大規模用**。

我自己寫了[好幾篇 OpenClaw 的文章](/openclaw-architecture-deep-dive-context-memory-token-crusher/)，從架構拆解、[成本優化](/openclaw-cost-optimization-guide-97-percent-reduction/)到[安全隔離](/openclaw-security-isolation-gmail-sandbox-setup/)都做過深入分析。OpenClaw 做對了很多事——File-first 的記憶設計、極低的入門門檻、社群驅動的快速迭代。但它的天花板也很明確：**它是為「一個人用一隻龍蝦」設計的。**

| 維度 | OpenClaw | NemoClaw |
|------|----------|----------|
| **設計對象** | 個人用戶 | 企業 IT/安全團隊 |
| **安全模型** | 信任用戶判斷 | 架構層面強制約束 |
| **部署單位** | 一個人一隻 Agent | 多 Agent、多 tenant |
| **資料流控制** | 用戶自行管理 | Privacy Router 統一路由 |
| **Policy 管理** | 無集中化 policy | OPA + Policy Engine |
| **可觀測性** | 本地日誌 | 集中化 audit trail |
| **擴展性** | 垂直（更強的單機） | 水平（K3s multi-tenant） |

---

## NemoClaw 在補哪個洞

NemoClaw 比較關鍵的是：**開始有人在認真補「企業治理」這一塊。**

例如：

- 把 agent 關進 sandbox
- 所有外部連線經過 routing
- policy 集中管理
- audit 可以回溯

這些東西，本質上不是 AI 技術，而是**「企業系統該有的基本能力」**。

我一直在講：**Prompt 負責引導，工程負責約束。** 在 OpenClaw 裡，Agent 被 prompt injection 攻破了，理論上可以存取你整台電腦的檔案系統。在 NemoClaw 裡，Agent 被攻破了，它連 Policy Engine 的存在都感知不到——架構上用 PID namespace、mount namespace、network namespace 做到了物理隔離。**不是靠 Prompt 說「你不准做這件事」，是架構上讓它做不到。**

---

## 工程角度快速拆解

如果用工程角度快速講，NemoClaw 的核心其實是：**用一個 K3s-based 的 sandbox + policy layer，把 agent 關進「可控環境」裡運行。**

裡面幾個關鍵點：

1. **每個 agent 跑在隔離的 sandbox**——不是單純 container，而是有 network namespace / seccomp syscall 限制 / Landlock 檔案系統隔離。三層任何一層被繞過，另外兩層還在。
2. **所有對外呼叫經過 routing 層統一控管**——而且是 per-binary 的。你可以讓 `curl` 只能連 `api.anthropic.com:443`，但 `node` 只能連 `localhost:11434`。不是容器級別的規則，是程式級別的規則，支援 hot-reload。
3. **Policy engine（類似 OPA）做集中治理**——不用改 agent 代碼，從外部統一控制行為邊界。
4. **行為有 audit trail，可以回溯**——這對企業稽核來說是剛需。

技術細節完整版請看 [NemoClaw 架構拆解](/nemoclaw-architecture-deep-dive/)。

---

## 現實：安裝不絲滑，生態還小

不過四五天後，網路上的反饋是**安裝非常不絲滑**。

社群裡已經有人分享了[實際安裝 NemoClaw 的踩坑經驗](https://vocus.cc/article/69b92457fd897800010b9fba)，結論是花了好幾個小時才搞定。應該只有 NVIDIA 自家的雲端服務 [NVIDIA Brev](https://brev.nvidia.com/launchable/deploy) 可以做到一鍵安裝吧——預設配 A100，幫你搞定 Docker、NVIDIA Container Toolkit、所有依賴。自己裝？那就是一路踩坑。

我把幾個關鍵的坑整理一下：

1. **硬體門檻比官方說的高**：最低需要 8GB RAM，但官網沒有明確標示。
2. **官方一鍵安裝只裝了一半**：建議直接從 GitHub repo 走，不要用官網的 one-liner。
3. **Docker build 壞掉**：`.dockerignore` 排除了必要檔案，需要手動修。
4. **環境變數命名不一致**：不同元件讀不同變數名，預設值還不一樣。
5. **推論沒有自動配置**：即使提供了 API key，還是要手動設定 provider 和 routing。
6. **殭屍程序**：多次重啟後舊程序不清除，攔截訊息。

這也導致它的傳播一般。**生態還小，這點可能比較致命。** OpenClaw 有幾萬個活躍開發者在貢獻 plugin 和 integration，NemoClaw 目前主要靠 NVIDIA 自己和合作夥伴在推。

好消息是，這些都是工程品質問題，不是架構問題。`.dockerignore` 的 bug、環境變數命名不一致——這些幾個版本內應該會被修掉。

---

## NVIDIA 做的是一個方向，不是答案

NemoClaw 給了一個方向：**用 infra + policy 來約束 AI agent。**

但它還遠遠不是完整解法。使用體驗還在早期，生態還沒起來。

所以如果你今天問我：「現在可以全面導入嗎？」

答案很簡單：**還不用。**

我不太確定 NemoClaw 是否是終局，但肯定可以搶到一席之地就是了。NVIDIA 有硬體生態、有企業客戶基礎、有技術深度——合作夥伴名單也說明了這不是測試性小專案：Salesforce、Cisco、Google、Adobe、CrowdStrike，這些都是具體的企業工作流整合。

不過要注意的是：NemoClaw 把龍蝦關進 K3s sandbox，三層安全鎖死之後，Agent 能做的事情被限縮成呼叫 API、跑腳本、走預定義的 connector。**本質上跟 LangChain、CrewAI、AutoGen 這些企業 Agent 框架沒有太大差異了——都是 API 串接 + 工作流編排。** OpenClaw 的靈魂是「自由」，NemoClaw 的靈魂是「控制」。控制帶來了安全，但也犧牲了那個讓人興奮的部分。這是一個取捨，不是進步。

---

## 更實際的策略

我目前看到比較合理的路徑是：

1. **用 OpenClaw / 類似工具做能力驗證**——先讓團隊理解 AI Agent 能做什麼，找出真正有價值的 use case。
2. **找出真正有價值的 use case**——不是每個流程都適合 Agent，先挑 ROI 最高的場景。
3. **再開始補 governance**——不一定用 NemoClaw，但治理這層一定要補。

**請不要一開始就上 enterprise framework。** NemoClaw 那套 K3s + 三層安全 + Policy Engine，你至少需要一個懂 Kubernetes 的人，部署門檻不低。一開始就上，可能會拖慢你的進度。

但是真的要落地，也不要忽略 governance 這件事。不然最後只是一堆 OpenClaw POC，永遠進不了 production。

---

## 坦白說

**第一，安裝體驗反映了成熟度。** 一個連 `.dockerignore` 都沒測好的 repo，說明它還沒經過大量用戶的實戰驗證。這需要時間。

**第二，NVIDIA 的開源誠意。** Apache 2.0 是很好的授權，但 NVIDIA 過去在開源社群的名聲不算好（想想 Linus 的中指）。NemoClaw 會不會走到最後變成「開源核心 + 商業 premium」的套路？這是一個合理的擔心。嘴上說硬體無關，但最好的體驗只有老黃家有——這很微妙。

**第三，OpenAI 挖走 OpenClaw 團隊之後會怎麼發展。** 核心開發者已經在 OpenAI 裡面了。如果 OpenAI 基於 OpenClaw 的經驗推出企業級 Agent 平台，NemoClaw 的差異化優勢會被壓縮。這場仗還沒打完。

但整體來說，NemoClaw 出現的時間點是對的。**企業級 Agent 這塊田很大，有人開始認真耕，這本身就是好事。**

---

## 關鍵洞察

1. **NemoClaw 不是終局，但是一個清楚的 signal。** 企業級 AI Agent 的市場需求是真的，有人在認真補治理這一塊。

2. **企業落地卡的不是技術，是治理。** 法務、資安、稽核三關過不了，Demo 再驚艷也進不了 production。

3. **先 OpenClaw 做試點，再補 governance。** 不要一開始就上 enterprise framework，也不要永遠停在 POC。

4. **安裝體驗和生態是當前最大的短板。** 架構設計很好，但工程品質和社群規模還需要時間。

5. **NVIDIA 做的是方向，不是答案。** 用 infra + policy 約束 AI agent 是對的方向，但具體實作還有很大的改進空間。

---

## 延伸閱讀

- [NemoClaw 架構拆解：K3s、seccomp、Landlock 三層縱深防禦](/nemoclaw-architecture-deep-dive/)
- [OpenClaw 架構拆解：Context、Memory、Token 壓縮機](/openclaw-architecture-deep-dive-context-memory-token-crusher/)
- [OpenClaw 安全隔離：Gmail Sandbox 到底怎麼設定](/openclaw-security-isolation-gmail-sandbox-setup/)
- [Channel 的戰爭：OpenClaw、Anthropic 和誰能決定 AI Agent 的未來](/openclaw-anthropic-channel-war-who-controls-ai-agent-future/)
- [從「套殼 1.0」到「套殼 2.0」：為什麼真正該緊張的是 Anthropic](/shell-wrapper-2-anthropic-real-threat/)
