---
layout: post
title: "2026 二月，不只中國在爆發 — 美國 AI 巨頭也在瘋狂輸出"
date: 2026-02-18 10:00:00 +0800
categories: [ai-agent, it-architecture]
tags: [claude-opus-4-6, claude-sonnet-4-6, gpt-5-3-codex, notebooklm, pptx, benchmark, computer-use, agent-teams, openclaw, peter-steinberger]
permalink: /ai-weekly-notebooklm-pptx-claude-sonnet-4-6/
description: "2026 二月，Anthropic 和 OpenAI 輪番丟出重磅更新：Claude Opus 4.6 的 Agent Teams、GPT-5.3-Codex 的 Terminal-Bench 77.3%、Peter Steinberger 加入 OpenAI、Sonnet 4.6 用 1/5 價格逼近旗艦、NotebookLM 支援 PPTX 匯出。兩週五個重大更新，中美 AI 軍備賽全面開打。"
image: /assets/images/notebooklm-pptx-prompt-revisions-tweet.png
---

**作者：** Wisely Chen
**日期：** 2026 年 2 月 18 日
**系列：** AI Agent 完整指南 / IT 架構系列
**關鍵字：** Claude Opus 4.6, Claude Sonnet 4.6, GPT-5.3-Codex, NotebookLM, PPTX, Benchmark, Computer Use, Agent Teams, OpenClaw, Peter Steinberger

---

## 為什麼要寫這篇

上一篇我寫了[2026 農曆新年中國開源模型集體爆發](/china-ai-models-2026-lunar-new-year-comparison/)，Kimi、Qwen、GLM、MiniMax 在二月密集發布。

但中國不是唯一在爆發的。

**美國這邊同樣瘋狂。** 光是 2026 年 2 月，Anthropic 和 OpenAI 就輪番丟出重磅更新：

- **2 月 5 日** — Anthropic 發布 **Claude Opus 4.6**（旗艦模型，Agent Teams 多代理協作，ARC-AGI-2 從 37.6% 跳到 68.8%）
- **2 月 5 日** — OpenAI 發布 **GPT-5.3-Codex**（Agentic Coding 模型，Terminal-Bench 從 64.0% 跳到 77.3%，快 25%）
- **2 月 14 日** — OpenAI 宣布 **OpenClaw 創辦人 Peter Steinberger 加入**，負責「下一代個人 Agent」，OpenClaw 轉為開源基金會
- **2 月 17 日** — Anthropic 發布 **Claude Sonnet 4.6**（中價位模型，逼近 Opus 效能，$3/M tokens 不變）
- **2 月 18 日** — Google **NotebookLM** 宣布 Prompt-Based Revisions + PPTX 匯出

兩週內，五個重大更新。

把中美時間線放在一起看更有感覺：

| 日期 | 中國 | 美國 |
|------|------|------|
| 1/27 | Kimi K2.5（Agent Swarm） | |
| 2/5 | | Claude Opus 4.6 + GPT-5.3-Codex |
| 2/10 | Qwen-Image-2.0 | |
| 2/11 | GLM-5 + MiniMax M2.5 | |
| 2/12 | Seedance 2.0 + Qwen3-Coder-Next | |
| 2/14 | 豆包大模型 2.0 | Peter Steinberger 加入 OpenAI |
| 2/16 | Qwen3.5 | |
| 2/17 | | Claude Sonnet 4.6 |
| 2/18 | | NotebookLM Prompt Revisions + PPTX |

**整個二月就是一場中美 AI 軍備賽。** 中國拼開源模型數量和成本，美國拼旗艦效能和 Agent 能力。

---

## Claude Opus 4.6：旗艦中的旗艦

**發布日期：** 2026 年 2 月 5 日
**定價：** $15/$75 per million tokens
**Context Window：** 1M tokens（beta）

### 重點升級

Opus 4.6 跟上一代 Opus 4.5 相比，最大的變化不是「寫程式更強」，而是**推理能力近乎翻倍**：

| Benchmark | Opus 4.5 | Opus 4.6 | 變化 |
|-----------|----------|----------|------|
| **ARC-AGI-2** | 37.6% | **68.8%** | +31.2%（近乎翻倍） |
| **SWE-bench Verified** | 80.9% | 80.8% | 持平 |
| **Terminal-Bench 2.0** | 59.8% | 65.4% | +5.6% |
| **OSWorld-Verified** | 66.3% | 72.7% | +6.4% |
| **1M context 準確度** | — | 76.0% | GPT-5.2 只有 18.5% |

SWE-bench 幾乎沒動（80.9% → 80.8%），但 ARC-AGI-2 從 37.6% 跳到 68.8%——這代表 Opus 4.6 在**解決全新類型問題**的能力上有了質的飛躍。

### Agent Teams：真正的殺手功能

Opus 4.6 的頭條功能是 **Agent Teams**——多個 Claude 代理協同工作。

官方展示的案例：Agent Teams 從頭建了一個 **C 編譯器**，10 萬行程式碼，能在三個 CPU 架構上啟動 Linux。這不是寫個小腳本，這是系統級的工程能力。

對做 Claude Code 的人來說，這意味著以後可以把大型任務拆給多個 Agent 平行處理，而不是一個 Agent 從頭做到尾。

### 原生 Office 文件支援

Opus 4.6 新增了**原生讀寫 PowerPoint 和 Excel** 的能力。不用再透過外掛或轉換，直接讀 .pptx 和 .xlsx。

這對企業場景特別重要——很多公司的知識還是鎖在 PPT 和 Excel 裡。

---

## GPT-5.3-Codex：OpenAI 的 Agent Coding 回擊

**發布日期：** 2026 年 2 月 5 日
**可用平台：** ChatGPT 付費版（App、CLI、IDE 擴展、Codex Cloud）
**API：** 即將開放

跟 Opus 4.6 同一天發布，OpenAI 也沒閒著。

### 重點升級

GPT-5.3-Codex 定位不是通用模型，而是**專注在 Agentic Coding**——讓 AI 自主完成複雜的開發任務。

| Benchmark | GPT-5.2-Codex | GPT-5.3-Codex | 變化 |
|-----------|--------------|---------------|------|
| **Terminal-Bench 2.0** | 64.0% | **77.3%** | +13.3% |
| **OSWorld-Verified** | 38.2% | 64.7% | +26.5% |
| **SWE-Bench Pro Public** | 56.4% | 56.8% | 持平 |
| **Cybersecurity CTF** | — | 77.6% | 新指標 |

兩個數字特別搶眼：

1. **Terminal-Bench 77.3%**：超越 Opus 4.6 的 65.4%。在終端操作和系統管理任務上，GPT-5.3-Codex 目前是最強的。
2. **OSWorld 64.7%**：從 38.2% 跳到 64.7%，Computer Use 能力大幅提升。不過 Sonnet 4.6 的 72.5% 還是更高。

### 25% 更快

同樣的任務，GPT-5.3-Codex 比前一代快 25%。對用 Codex 做日常開發的人來說，這是直接感受得到的提升。

### 「自己 Debug 自己」

OpenAI 提到一個有趣的細節：GPT-5.3-Codex 是第一個「**參與了自己開發的模型**」——在訓練過程中，它自己 debug 了自己。

### 資安分級

GPT-5.3-Codex 被 OpenAI 歸類為**「High capability」資安等級**——這是 OpenAI Preparedness Framework 下的最高分類。伴隨 $10M 的 cyber defense credits。

---

## OpenClaw 創辦人 Peter Steinberger 加入 OpenAI

**公告日期：** 2026 年 2 月 14 日

這可能是二月最有意味的一則新聞。

Peter Steinberger——OpenClaw 的創辦人，過去幾個月 AI Agent 圈最紅的名字——[宣布加入 OpenAI](https://steipete.me/posts/2026/openclaw)。Sam Altman 親自發推說 Peter 將負責「**drive the next generation of personal agents**」。

### 為什麼這件事很重要

如果你讀過[上一篇中國模型對比](/china-ai-models-2026-lunar-new-year-comparison/)，你會知道 OpenClaw 在 Agent 圈的地位。Kimi K2.5 之所以被大量使用，很大程度是因為 Peter 公開推薦，讓它成為 OpenClaw 用戶的 default model。

現在 OpenClaw 的靈魂人物跑去 OpenAI 了。

### Peter 自己怎麼說

> "I'm a builder at heart... What I want is to change the world, not build a large company."

據報導 Peter 同時收到了 Meta 的 offer，兩家的出價都是「billions」等級。但 Peter 選擇了 OpenAI，理由是「teaming up with OpenAI is the fastest way to bring this to everyone」。

### OpenClaw 的未來

好消息是：**OpenClaw 不會消失。** Peter 宣布 OpenClaw 將轉為獨立的開源基金會，OpenAI 承諾持續贊助，Peter 也會有專門的時間繼續開發。

Sam Altman 的原話：「The future is going to be extremely multi-agent and it's important to support open source as part of that. OpenClaw will live in a foundation as an open source project.」

### 對產業的影響

這件事的訊號很清楚：**OpenAI 在 Agent 賽道上認真了。**

GPT-5.3-Codex 負責「AI 寫程式」，Peter 負責「AI 幫你做事」。兩條線加在一起，OpenAI 的 Agent 策略已經從「模型能力」延伸到「端到端的使用者體驗」。

對 OpenClaw 社群來說，短期可能有些不確定性（Peter 的精力勢必分散），但長期來看，有 OpenAI 的資源灌注，OpenClaw 的發展速度反而可能加快。

---

## Claude Sonnet 4.6：用 Sonnet 的錢買到接近 Opus 的腦

**發布日期：** 2026 年 2 月 17 日
**定價：** $3/$15 per million tokens（跟 Sonnet 4.5 一樣）
**Context Window：** 1M tokens（beta）
**預設模型：** 現在是 claude.ai Free 和 Pro 用戶的預設模型

### 這次升級有多大？

直白講：**Sonnet 4.6 在多數任務上已經逼近甚至超越去年 11 月的 Opus 4.5。**

Anthropic 自己的數據：
- 開發者在 Claude Code 中使用時，**70% 的時候偏好 Sonnet 4.6 勝過 Sonnet 4.5**
- 甚至有 **59% 的場景偏好 Sonnet 4.6 勝過 Opus 4.5**（去年的旗艦模型）

這意味著什麼？你花 $3/M tokens 的錢，拿到的是以前要花 $15/M tokens（Opus 4.5 定價）才有的效能。

### Benchmark 數據

| Benchmark | Sonnet 4.6 | Opus 4.6 | GPT-5.3-Codex | 說明 |
|-----------|-----------|----------|---------------|------|
| **SWE-bench Verified** | 79.6% | 80.8% | — | 軟體工程，接近 Opus |
| **OSWorld-Verified** | **72.5%** | 72.7% | 64.7% | Computer Use，三者最強 |
| **Finance Agent v1.1** | **63.3%** | 60.1% | — | 金融分析，超越 Opus |
| **GDPval-AA Elo** | **1633** | 1606 | — | Office 任務，超越 Opus |
| **Terminal-Bench 2.0** | 59.1% | 65.4% | **77.3%** | GPT-5.3 最強 |
| **GPQA Diamond** | 89.9% | 91.3% | — | 研究生級推理 |
| **BrowseComp** | 74.7% | 84.0% | — | Agent 搜索 |
| **ARC-AGI-2** | 58.3% | **68.8%** | — | 新穎問題解決 |

幾個值得注意的點：

1. **Computer Use (OSWorld 72.5%)**：Sonnet 4.6 竟然跟 Opus 4.6 的 72.7% 只差 0.2%，而且碾壓 GPT-5.3-Codex 的 64.7%。Anthropic 在 Computer Use 這條賽道上已經甩開所有人。

2. **Finance Agent 和 Office 任務都超越 Opus 4.6**：這代表在「實際工作場景」中，Sonnet 4.6 已經不是「便宜替代品」，而是主力。

3. **SWE-bench 79.6%**：只比 Opus 4.6 的 80.8% 低 1.2%，但成本便宜 5 倍。

4. **Terminal-Bench 是弱點**：59.1% 遠低於 GPT-5.3-Codex 的 77.3%。如果你的場景是大量終端操作，GPT-5.3 還是更強。

### 對 Claude Code 使用者的影響

如果你像我一樣日常用 Claude Code，這次升級的感受會很明顯：

1. **Coding 能力提升**：指令跟隨更精準，幻覺減少，多步驟任務更穩定
2. **Computer Use 大進步**：如果你用 Claude 做瀏覽器自動化，72.5% 的 OSWorld 分數代表可靠度大幅提升
3. **Prompt Injection 防禦**：Anthropic 特別強調安全性改進，Agent 被惡意 prompt 劫持的風險降低
4. **成本不變**：同樣的 $3/M tokens，但拿到明顯更好的模型

---

## NotebookLM：終於不用再重生整份簡報了

### 背景：之前的痛

我自己用 NotebookLM 生簡報已經很多次了。流程大致是：上傳來源 → 生成 Slide Deck → 下載 PDF。

問題是，**一旦生出來不滿意，你只能重新生一份。** 沒有辦法說「第 3 頁的標題改一下」或「把整體配色改成深色」。每次微調都是砍掉重練，運氣好的話三次搞定，運氣差的話可以重生七八次。

### 這次更新了什麼

根據 NotebookLM 官方帳號（[@NotebookLM](https://x.com/NotebookLM/status/2023851190102986970)）2 月 18 日的公告：

**1. Prompt-Based Revisions**

你現在可以直接用自然語言對已生成的簡報做修改。例如：
- 「把第 5 頁的圖表改成橫式」
- 「整體風格改成更企業正式的感覺」
- 「在第 3 頁後面加一頁 Q&A」

不用重新生成整份簡報，直接針對特定頁面或整體風格做調整。

**2. PPTX 匯出**

之前 NotebookLM 的簡報只能下載 PDF。現在可以直接匯出成 **PowerPoint (.pptx)** 格式。Google Slides 匯出也在開發中（coming next）。

### Rollout 狀態

官方說會**慢慢 rollout 到付費用戶**（Google AI Ultra 和 Pro plan）。免費用戶可能要再等幾週。

### 為什麼這很重要

之前 NotebookLM 簡報的最大問題就是「**最後一哩路的編輯成本**」。AI 生出 80% 的好簡報，但剩下 20% 的微調你要花比從頭做還多的時間——因為你得把 PDF 轉成 PPT，重新排版，然後改。

現在這個問題被解決了：**AI 生成 80% + Prompt 微調 15% + 人工最後 5%**。整個流程省下至少一半時間。

---

## 三家放在一起看：誰在贏什麼？

| 維度 | Anthropic | OpenAI | Google |
|------|-----------|--------|--------|
| **旗艦推理** | Opus 4.6（ARC-AGI-2 68.8%）| — | — |
| **中價位 CP 值** | Sonnet 4.6（$3/M 逼近 Opus）| — | — |
| **Agentic Coding** | Opus 4.6（SWE-bench 80.8%）| GPT-5.3-Codex（Terminal-Bench 77.3%）| — |
| **Computer Use** | Sonnet 4.6（OSWorld 72.5%）| GPT-5.3（64.7%，追上中）| — |
| **多代理協作** | Agent Teams | — | — |
| **個人 Agent** | — | Peter Steinberger + OpenClaw 基金會 | — |
| **簡報生產力** | — | — | NotebookLM Prompt Revisions |
| **速度** | — | GPT-5.3（快 25%）| — |

**Anthropic 的策略很清楚：上下夾擊。** Opus 4.6 守住旗艦天花板，Sonnet 4.6 用 1/5 價格侵蝕「夠好就行」的市場。兩週內連發兩個模型，把價格帶從 $3 到 $15 全覆蓋。

**OpenAI 選擇 vertical + 人才收割：** 不只把 Codex 打造成 Agentic Coding 最強工具，還直接把 Agent 圈最紅的人（Peter Steinberger）挖過來。GPT-5.3-Codex 管「AI 寫程式」，Peter 管「AI 幫你做事」——兩條線同時推進。

**Google 走的是生產力工具路線：** 不跟你比模型分數，而是讓 NotebookLM 變成「不需要會 AI 的人也能用的 AI 工具」。Prompt-Based Revisions 讓不懂技術的人也能微調 AI 簡報。

---

## 坦白說

### Opus 4.6 的現實

Agent Teams 展示了 10 萬行 C 編譯器，很驚人。但這是官方 demo，不是你明天就能在自己的專案上複製的流程。多代理協作在真實環境中的穩定性、錯誤處理、成本控制，都還需要時間驗證。

### GPT-5.3-Codex 的疑慮

Terminal-Bench 77.3% 很強，但 **SWE-Bench Pro 只有 56.8%**，幾乎沒動（前代 56.4%）。這意味著 GPT-5.3 在「自己操作終端」的場景變強了，但在「理解和修復複雜程式碼」的核心 coding 能力上沒有明顯進步。

另外 API 還沒開放，定價未知。如果定價太高，Terminal-Bench 的優勢會被成本稀釋。

### Sonnet 4.6 的取捨

用 1/5 的價格拿到 90-95% 的效能，對大多數應用場景來說就是最佳解。但在「真正困難」的任務上，旗艦就是旗艦：ARC-AGI-2 差 10.5%，BrowseComp 差 9.3%。

**「偏好 59% 勝過 Opus 4.5」不等於「比 Opus 4.6 強」**——注意 Anthropic 的措辭，是跟去年的 Opus 4.5 比，不是跟現在的 Opus 4.6 比。

### Peter 加入 OpenAI 的隱憂

Peter 是 builder 性格，OpenAI 是大公司。歷史上太多「天才開發者加入大公司後被官僚體系磨掉銳角」的案例。OpenClaw 之所以好用，很大程度是因為 Peter 一個人做決策，反應速度快。進了 OpenAI 之後，這個速度能維持嗎？

另外，OpenClaw 轉基金會聽起來很美，但「公司贊助的開源基金會」跟「獨立開源專案」本質上是不同的。長期來看，OpenClaw 的中立性和社群信任是否會受影響，值得觀察。

### NotebookLM 的隱憂

Prompt-Based Revisions 聽起來很美，但之前 NotebookLM 的簡報生成就有時候會「聽不懂」指令。能不能精準地「改第 3 頁」而不影響其他頁，實際品質還要測過才知道。

---

## 結語：2026 二月是 AI 的轉折點

初二最好的消息，NotebookLM 終於宣布要加入 PPTX 的輸出了。對我這個每週都在用 NotebookLM 生簡報的人來說，這大概是整個二月最有感的更新。

但退一步看，2026 二月不只是中國在狂熱的輸出模型——美國 AI 巨頭也在瘋狂對戰，而且重點非常明確：**Agent 能力正式進入主戰場。**

把中國和美國的時間線擺在一起，你會發現一件事：

**2026 年二月，全球 AI 產業同時進入了「Agent 落地」的衝刺期。**

### 中美走的是完全不同的路

從這個瘋狂二月看得出來，中美 AI 的發力方向已經明確分化：

**中國正在努力做兩件事：**
1. **能力逼近頂尖模型的 Tier 1 開源 model** — Kimi K2.5、Qwen3.5、GLM-5 都在證明開源可以接近閉源效能
2. **性價比壓到極致** — 成本壓到 Claude 的 1/8 到 1/33，配合 OpenClaw 這類框架，純地端 Agent 成本可能低於台幣 50 萬

**美國正在努力做的是在現有 Tier 1 模型下，做出大量的 Agent Business Case：**
- NotebookLM 超強的簡報功能（讓非技術人員也能用 AI 做簡報）
- Anthropic Agent Teams + Sonnet 4.6 的上下夾擊策略覆蓋全價格帶
- OpenAI 把 Codex 打造成 Agentic Coding 專用武器
- 收購人才（Peter Steinberger）來加速 Agent 端到端體驗

### 2026 年的劇本

今年的劇情已經很清楚了：

**美國會努力衝擊 Agent case**，讓生產力持續飆升，並且做到部分 Agent 變現。Anthropic 的 Agent Teams、OpenAI 的 Codex + Peter、Google 的 NotebookLM——每一家都在把「AI 能力」轉譯成「使用者能直接用的工具」。

**中國會用原本厲害的工程人才來做開源模型以及成本優化**，來支援 OpenClaw 或是其他 Agent 的 token 粉碎機場景。當一個 Agent 跑一次任務需要消耗幾十萬 tokens，你用 Claude API 跑跟用 Qwen3.5 地端跑，成本可能差 10-30 倍。

這兩條路不是對立的，而是互補的。美國做出好用的 Agent 框架和場景，中國提供便宜的推理引擎。最終受益的是全球的開發者和企業——你可以用美國的 Agent 設計，跑在中國的開源模型上。

不管你站在哪一邊，結論都一樣：

**2026 不再是「AI 能不能用」的問題，而是「你選哪套 Agent 方案落地」的問題。**

---

## 參考資料

### Anthropic
1. [Introducing Claude Opus 4.6 - Anthropic 官方](https://www.anthropic.com/news/claude-opus-4-6)
2. [Anthropic releases Opus 4.6 with new 'agent teams' - TechCrunch](https://techcrunch.com/2026/02/05/anthropic-releases-opus-4-6-with-new-agent-teams/)
3. [Introducing Claude Sonnet 4.6 - Anthropic 官方](https://www.anthropic.com/news/claude-sonnet-4-6)
4. [Claude Sonnet 4.6 approaches Opus-level scores - OfficeChai](https://officechai.com/ai/claude-sonnet-4-6-benchmarks/)
5. [Anthropic's Sonnet 4.6 matches flagship AI performance at one-fifth the cost - VentureBeat](https://venturebeat.com/technology/anthropics-sonnet-4-6-matches-flagship-ai-performance-at-one-fifth-the-cost/)
6. [Claude Sonnet 4.6 brings 'much-improved coding skills' - 9to5Mac](https://9to5mac.com/2026/02/17/claude-sonnet-4-6-model-brings-much-improved-coding-skills-and-upgraded-free-tier/)

### OpenAI
7. [Introducing GPT-5.3-Codex - OpenAI 官方](https://openai.com/index/introducing-gpt-5-3-codex/)
8. [GPT-5.3-Codex System Card - OpenAI](https://openai.com/index/gpt-5-3-codex-system-card/)
9. [GPT-5.3-Codex: Features, Benchmarks, and Migration Guide - DigitalApplied](https://www.digitalapplied.com/blog/gpt-5-3-codex-release-features-benchmarks-guide)

### Peter Steinberger / OpenClaw
10. [OpenClaw, OpenAI and the future - Peter Steinberger 本人](https://steipete.me/posts/2026/openclaw)
11. [OpenClaw creator Peter Steinberger joins OpenAI - TechCrunch](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/)
12. [OpenClaw creator Peter Steinberger joining OpenAI, Altman says - CNBC](https://www.cnbc.com/2026/02/15/openclaw-creator-peter-steinberger-joining-openai-altman-says.html)
13. [Peter Steinberger 推特公告](https://x.com/steipete/status/2023154018714100102)

### Google
14. [NotebookLM 官方公告 - Prompt-Based Revisions & PPTX Support](https://x.com/NotebookLM/status/2023851190102986970)
15. [Generate a Slide Deck in NotebookLM - Google Support](https://support.google.com/notebooklm/answer/16757456?hl=en)

### 對比分析
16. [Claude Opus 4.6 vs GPT-5.3-Codex: 2026 AI Coding Benchmarks](https://vertu.com/ai-tools/claude-opus-4-6-vs-gpt-5-3-codex-head-to-head-ai-model-comparison-february-2026/)
17. [Claude Opus 4.6: What Actually Changed and Why It Matters - Medium](https://medium.com/data-science-collective/claude-opus-4-6-what-actually-changed-and-why-it-matters-1c81baeea0c9)
