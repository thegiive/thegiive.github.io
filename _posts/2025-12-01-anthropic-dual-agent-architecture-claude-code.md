---
layout: post
title: "[Agent Part 5] 雙 Agent 架構: Anthropic 官方解密為什麼 Claude Code 這麼好用的內部工程架構"
date: 2025-12-01 08:40:00 +0800
permalink: /anthropic-dual-agent-architecture/
image: /assets/images/dual-agent-architecture-logo.png
description: "Anthropic 發布了 Initializer Agent + Coding Agent 雙 Agent 架構，用工程化的工作流設計解決長時任務的「記憶重置」問題。"
---

![Initializer Agent + Coding Agent 雙 Agent 架構](/assets/images/dual-agent-architecture-logo.png)

Anthropic 的 Blog 發布了一套針對[長時任務的工程方案](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)。這不是靠更大模型或更長上下文來硬撐，而是用工程化的工作流設計，讓 Agent 即使在「失憶」的多窗口條件下，也能像人類工程師一樣一步步推進任務。我看過一些 Claude Code 的反組譯文章，基本上就跟這個架構很類似。加上這篇文章後面也寫了是 Anthropic RL team 跟 Claude Code Team 的集體努力，我們就當這是 Claude Code 的設計思路。

## 單 Agent 為什麼會失敗？

我之前說過，長時任務才是 Agent 的聖杯, 長任務涉及幾十到數百個功能。但模型每一輪都在有限上下文中工作，**每次執行都是一次「記憶重置」**。

單 Agent 容易出現兩類問題：

**問題一：一口氣寫到爆。** 模型直接大規模編碼，直到上下文耗盡，留下「半截代碼」——未完成、未記錄、沒測試。下一輪 Agent 接手時完全無法判斷進展。

**問題二：過早宣布完成。** 看到一些 UI 或 API 就誤以為功能齊全，直接終止任務。

核心問題不在模型能力，而在**缺乏跨上下文繼承任務邏輯的結構化工作方式**。

## 雙 Agent 架構：一個指揮，一個迭代

Anthropic 的解法是把長時任務拆成兩種角色。

**Initializer Agent（首席架構師）** 負責第一次運行：
- 把需求分解為 JSON 結構的功能清單，每項都有驗收條件
- 建立 `progress` 文件記錄專案狀態，搭配 git 追蹤
- 生成 `init.sh` 啟動腳本，確保環境健康

**Coding Agent（增量開發者）** 負責後續迭代：
- 每輪開始先檢查目錄、讀 git 記錄、跑 init.sh、做端到端測試
- 從清單選一個未完成功能，**一次只做一件事**
- 用 Puppeteer 像真實用戶一樣測試，通過才標記完成並 commit

這種節奏雖然慢，但極其可靠。把「無人監督的長時任務」變成「每輪可驗證的開發迭代」。這個很像之前說的 Plan, Exec, Critic

## 實作細節：JSON Manifest 結構

功能清單使用 JSON 格式，每個功能都有明確的驗收步驟：

```json
{
  "category": "functional",
  "description": "New chat button creates a fresh conversation",
  "steps": [
    "Navigate to main interface",
    "Click the 'New Chat' button",
    "Verify a new conversation is created",
    "Check that chat area shows welcome state",
    "Verify conversation appears in sidebar"
  ],
  "passes": false
}
```

關鍵設計：**Agent 只能修改 `passes` 欄位**，不能刪除或編輯測試本身。這確保了驗收標準的一致性。

## Coding Agent 的典型會話開始

每次新會話，Coding Agent 會先「Onboarding」自己：

```
[Assistant] 我將開始了解項目當前狀態
[Tool Use] <bash - pwd>
[Tool Use] <read - claude-progress.txt>
[Tool Use] <read - feature_list.json>
```

這就是為什麼 Claude Code 開始時會先讀 CLAUDE.md、檢查 git log、理解專案結構——**它在重建上下文**。

## 常見失敗模式與解決方案

| 問題 | 解決方案 |
|------|--------|
| Agent 過早宣布完成 | 設置 200+ 個功能的清單，強制逐一驗證 |
| 環境留有未記錄的 bug | 強制寫入 git + progress file |
| 功能被過早標記完成 | 必須用 Puppeteer 自我驗證後才能標記 |
| Agent 花時間搞清楚如何啟動應用 | 提供 init.sh 腳本，一鍵啟動 |

文章特別提到：即使用最強的 **Claude Opus 4.5**，「開箱即用」也無法在多個上下文窗口中構建生產級 web 應用——**除非採用這套結構化方法**。

## 不再是模型，一切都是工程 workflow

看到這架構，我第一反應是：**這不就是 SDD 一直強調的嗎？**

- 把模糊需求轉為結構化功能清單 → 我們叫 PRD
- 建立狀態追蹤機制 → 我們用 git + 進度文件
- 確保每輪都能驗證 → 我們用 QA 驗收流程

差別在於我們用人做，他們讓 AI 自己做。但核心洞察一樣：**長時任務的成功不在模型多強，而在有沒有結構化工作流來傳承上下文。**

## 關鍵洞察

![The Workflow Loop：Coding Agent 的迭代流程](/assets/images/workflow-loop-diagram.png)

1. 長時任務瓶頸在工作流設計，不在模型能力
2. 雙 Agent 本質是「分工」：一個奠基，一個迭代
3. 結構化狀態記錄是跨會話協作的關鍵
4. 端到端測試是每輪迭代的必要環節
5. 未來可能出現 Test Agent、QA Agent、Documentation Agent，形成「AI 工程團隊」

下一個 Agent 時代，可能不是模型能力提升，而是**AI Agent 工程方法論的突破**。這也是為何我一直專心寫一些 Agent Workflow 的技術文章
