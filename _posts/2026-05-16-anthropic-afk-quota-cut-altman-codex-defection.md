---
layout: post
title: "Anthropic 把 AFK 額度砍 96%：Harness Engineering 重傷，Agent Infra 該重新想了"
date: 2026-05-16 10:30:00 +0800
permalink: /anthropic-afk-quota-cut-altman-codex-defection/
image: /assets/images/anthropic-afk-quota-cut-claudedevs-tweet.png
description: "Anthropic 6/15 起把 Claude 訂閱拆成兩塊：人類在場吃訂閱、AFK 自動化改吃獨立 credit。Max 20x 從等值 $5000 token 量切成 $200 credit，是 96% cut。對 harness engineering 是重傷。Sam Altman 同一週推 Codex 企業版兩個月免費接人。但跳去 Codex 不是答案——這是重新審視你 Agent Infra 的契機：vendor lock-in、雙棲策略、地端歸宿。"
tags:
  - Anthropic
  - Claude Code
  - Claude Agent SDK
  - AFK
  - Harness Engineering
  - OpenClaw
  - Codex
  - Agent infra
  - 地端模型
---

![ClaudeDevs 5/14 公告：Claude 訂閱拆出 AFK 專用 credit](/assets/images/anthropic-afk-quota-cut-claudedevs-tweet.png)

Anthropic 上週宣布，6/15 起訂閱額度切成兩塊：

1. **Human-in-the-loop 的互動式用途**——像 Claude Code、claude.ai——繼續吃原本訂閱額度
2. **自動化工作流（Away From Keyboard, AFK）**——改吃獨立 monthly credit。Pro 給 $20、Max 5x 給 $100、Max 20x 給 $200

這是對 AFK 工作流、對 **Harness Engineering** 的巨大打擊。

但反過來，也是審視你 Agent Infra 的契機。

## 數字：$5000 變 $200，是 96% cut

社群估算，Max 20x 的重度用戶每月 AFK 跑下來消耗的算力大概**等值 $5000 的 API credit**。現在切成 $200 credit。

$5000 變 $200，是 **96% cut**，不是有人講的 40 倍而已。

但 Anthropic 真正的算盤不是省成本。這個動作跟 4 月封殺 OpenClaw 是同一條邏輯線——**把訂閱定義成「人類在場、有互動」的場景，把 AFK 推到按量計費的 API**。

訂閱是給你坐在螢幕前用的，不是給機器人用的。

## 對個人高階用戶與 Harness Engineering 是重傷

賣第一門 Claude Code 付費課程的 Matt Pocock 公開破防：

> I have never experienced such a frustrating lack of clarity over the basic terms of usage.

然後直接在 X 上把學員都導流到 Codex。

這不是情緒發洩，這是**他的課程商業模式受到直接衝擊**。你的工具鏈綁死在一家供應商，結果對方改條款，**你的學員全部拿到錯誤的教材**。

但對「在公司裡建立 Harness Engineering」的人來說，傷害更大。

Harness 的核心價值，就是把 AI 變成「**可被工程化調度的工作流**」。也就是：

- 批次跑任務
- 自動讀 issue
- 自動開 PR
- 多輪 code review
- 背景研究
- 多 agent 並行
- CI/CD 裡自動修 bug
- 半夜自己跑測試、整理結果、回報狀態

**這些全部都是 AFK。**

Anthropic 這次等於是把 Harness Engineering 最重要的那條路切出來，丟進一個很小的 credit pool。$200 credit 對一個認真做 harness 的團隊，大概**撐 10-15 天就見底**。後面半個月，要嘛自己掏 API 錢，要嘛把所有自動化關掉、回去手動按 Enter。

## 對手沒有放過這個空檔

OpenAI 同一週的反攻動作非常乾脆：

- **ChatGPT Pro 從 $200 砍到 $100**
- **[Codex 企業版兩個月免費試用](https://x.com/OpenAIDevs/status/2054586214112780518)**，明確鎖定從 Anthropic 遷移的客戶
- **0 seat fee、30 天遷移窗口**
- Altman 甚至在公告底下回了一句 [**「ok boomer」**](https://x.com/sama/status/2046808114561974567)

廣大網友歡呼，還好 GPT-5.5 夠猛。換過去反而有升級感。

老實說，我自己最近用 Codex，**出 code 品質又快又好**。

## 重新思考一下你的 Agent Infra

但我不覺得「跳去 Codex 就好了」是對的反應。

你要趁這個事件，**重新思考你的 Agent Infra**。

### 第一：Vendor lock-in 不再是理論，是帳單

供應商可以在**週四傍晚改條款**，你的自動化流程就停了一半。

Vendor lock-in 的風險以前是理論，現在是帳單。如果你的核心業務跑在單一供應商的 API 上，這個週末應該花兩小時評估一下切換成本——光是評估，就會發現很多東西已經綁太深了。

### 第二：個人開發者可以考慮 Claude + Codex 雙棲

互動式寫程式留 Claude（互動式體驗 Claude Code 還是最順），AFK 自動化任務走 Codex 或 OpenAI API（費用結構比較適合批次跑）。

兩家都養，哪家改條款你都有退路。別忘了 ChatGPT 之前的條款也很噁心，**雙棲不是信任 OpenAI，是不信任任何單一供應商**。

### 第三：地端才是企業 Harness Engineering 的最後歸宿

地端不只是資安問題，是**風險控管**。

現在 LLM 廠商太沒操守。把 Infra 壓在雲，反覆橫跳只是暫時解法。**有地端算力才是真正的核心競爭力**。

Qwen3.6 27B / Gemma 4 31B 這個量級的 dense 開源模型，在多數 coding 任務上已經堪用（[七種推論引擎在 RTX 5090 上的實測](/qwen-3-6-27b-rtx-5090-inference-engine-benchmark/)我前幾天剛寫過）。

不是在省 token 費。是你願意花多少代價，**在不知道哪天會改的條款上**。

---

## 延伸閱讀

- [Anthropic 封殺 OpenClaw 之後的三層替代方案](/anthropic-kills-openclaw-gpt54-migration-guide/) — 4 月那波，同一條時間線
- [Qwen 3.6 27B 在 RTX 5090 上的七種推論引擎 benchmark](/qwen-3-6-27b-rtx-5090-inference-engine-benchmark/) — 地端混搭的硬體基礎
- [OpenClaw 成本優化指南：97% 削減](/openclaw-cost-optimization-guide-97-percent-reduction/) — API 分層的方法論

## 常見問題 Q&A

**Q: 我現在 Max 20x，6/15 之後 GitHub Actions 還能跑嗎？**

可以，但改吃 $200 credit。輕度沒事，重度很快撞牆。

**Q: $200 credit 換算成 token 大概可以跑多少？**

按 Opus API $15/M output token 估，$200 約 13M output token。一個 PR review 平均吃 20-50K，**撐 250-650 個 PR**。一天 10 個 PR 就 1 個月。

**Q: Codex 兩個月免費窗口什麼時候截止？**

5/14 公告 + 30 天，大約 6/13 截止。

**Q: 只用 Claude Code 互動模式會被影響嗎？**

不會。訂閱額度繼續用，跟過去一樣。

**Q: 地端跑 Coding agent 要什麼配備？**

最低一張 RTX 5090（或同等級 24GB+ VRAM 的卡）跑 Qwen3.6 27B 或 Gemma 4 31B。詳見上面 RTX 5090 那篇。
