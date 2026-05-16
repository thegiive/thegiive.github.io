---
layout: post
title: "Matt Pocock 要叛逃 Codex 了：Anthropic 把 AFK 額度砍九成，Sam Altman 同一週開門接人"
date: 2026-05-16 10:30:00 +0800
permalink: /anthropic-afk-quota-cut-altman-codex-defection/
image: /assets/images/anthropic-afk-quota-cut-claudedevs-tweet.png
description: "Anthropic 6/15 起把 Claude 訂閱拆成兩塊：人在回路繼續吃訂閱、AFK 和程序化調用改吃單獨 credit。Max 20x 從等值 $5000 token 量被切成 $200 credit，Theo Browne 算是 40x cut。同一週 Sam Altman 推 Codex 企業版 2 個月免費接人，Matt Pocock 已公開破防。"
tags:
  - Anthropic
  - Claude Code
  - Claude Agent SDK
  - AFK
  - OpenClaw
  - Codex
  - Agent infra
---

![ClaudeDevs 5/14 公告：Claude 訂閱拆出 AFK 專用 credit](/assets/images/anthropic-afk-quota-cut-claudedevs-tweet.png)

賣第一門 Claude Code 付費課程的 Matt Pocock，這週公開破防。

起因是 Anthropic 5 月 14 日發了一則公告：6 月 15 日開始，Claude 訂閱會被切成兩塊額度。**人在回路裡的用法**——claude.ai、Claude Code、Claude Cowork——繼續吃原本的訂閱額度；**AFK（away from keyboard）和程序化調用**——Claude Agent SDK、`claude -p`、Claude Code GitHub Actions、以及任何拿 Agent SDK 包起來的第三方應用（OpenClaw 是最有名的一個）——改吃一筆**單獨的 monthly credit**。

額度長這樣：Pro $20 credit、Max 5x $100 credit、Max 20x $200 credit。

聽起來像加碼。Anthropic 自己的講法是「我們在解禁第三方 agent」——之前灰色地帶用 token 跑 OpenClaw 那種第三方 SDK 本來就違反 TOS，現在給你一筆專用 credit，**反而是給你權利**。

Matt Pocock 的解讀完全相反：

> 「I have never before experienced from any developer tool such a frustrating lack of clarity over the basic terms of usage.」

他公開把觀眾導去 Codex。Theo Browne 算給大家看，這對重度第三方工具用戶**等於 40x cut**。

我自己拆完數字，覺得 Theo 沒有講錯。

## 為什麼 200 美元 credit 是大幅縮水

關鍵在 Max 20x 之前在 AFK 場景下，到底吃掉了多少 token。

Anthropic 從來沒公開過 Pro / Max 5x / Max 20x 等於多少 API credits。但社群裡有一種估算：Max 20x 一個月的 token 使用量，**可能等同 $5000 的 API 額度**。

這個數字有沒有誇張？我覺得反而保守。一個重度 AFK 用戶長什麼樣：

- `claude -p` 跑批次腳本，一晚把 100 個檔案掃完
- OpenClaw 開著 5 個瀏覽器分頁同時在做研究
- Claude Code GitHub Actions 自動處理 issue，一個 PR 跑 3-4 輪 review
- 自己寫的 Agent SDK 應用 24 小時在背景跑

這種用法一個禮拜燒 $1000 token 是非常容易的事。Anthropic 之前等於是讓你拿 $200 訂閱吃 $5000 算力，他們知道，但暫時忍著沒切——直到 Agent SDK 變成正式產品線、AFK 用量爆炸到擋不住為止。

**現在 $200 訂閱被切成「$200 互動 + $200 credit」**。如果原本 AFK 端就吃 $5000 等值，新 credit 是 $200，那就是 **96% cut**。Theo 講的 40x，數字接近這個量級。

我自己用得沒那麼兇，但光是 Claude Code GitHub Actions 跑 PR review 加 OpenClaw 偶爾掛背景研究，一個月 $200 credit 大概**撐 10-15 天**。後面半個月，就要嘛自己掏 API 錢，要嘛把所有自動化關掉、回去手動按 Enter。

## Anthropic 真正的算盤

這次政策的真正信號，不是「省錢」，是**重新定義 Claude 的商業模型**。

Anthropic 想把算力留在**人類在場的場景**：規劃、討論、即時協作、Pair programming。這些情境下：
- Token 用得慢（人類打字、思考都要時間）
- 上下文品質高（人會修正方向）
- 商業上能轉化成續訂、轉化成口碑

AFK 場景剛好相反：
- Token 燒得超快（Agent 不會累）
- 上下文品質容易失控（沒人盯著就一路歪）
- 商業上養出來的是「拿訂閱 token 跑生意」的中介層（OpenClaw、各種 GitHub Actions wrapper）

Anthropic 4 月先把 OpenClaw 踢出 Claude 訂閱（我寫過一篇 [封殺 OpenClaw 之後的三層替代方案](/anthropic-kills-openclaw-gpt54-migration-guide/)），5 月接著切 AFK quota。**這是同一條時間線**：把 Agent SDK 經濟跟訂閱經濟徹底解耦。

未來想拿 Claude 跑大量自動化？走 API、按量計費，跟訂閱用戶搶不到便宜。

## Sam Altman 同一週開門接人

訊號出來的同一週，OpenAI 出手了。其實是兩波：

**4 月 22 日 ——** Altman 在 Anthropic 訂閱公告底下回了兩個字：**[「ok boomer」](https://x.com/sama/status/2046808114561974567)**。144K views，順便補一刀講不想要「reduced limits or worse models」。

**5 月稍早 ——** ChatGPT Pro 從 $200 砍到 $100，**直接對標 Claude Max 5x**。

**5 月 14 日（Anthropic 公告同一天）——** [Codex 推出](https://x.com/OpenAIDevs/status/2054586214112780518)：
- **企業版 2 個月免費**，給從 Claude / Anthropic 遷移過來的客戶
- **0 seat fee**（business tier）
- 申請窗口 30 天

**還有一個促銷沒過期：** 新 ChatGPT Pro 訂戶，Codex **用量 10x 加成**到 5/31。

這個組合拳是經典的 ToB land grab：先用 KOL 破防造勢，再用「免費 + 0 seat fee + 短窗口」逼企業 IT 部門立刻決策。對台灣中型團隊 IT 採購來說，2 個月免費足夠跑一個 POC，跑完發現 Codex 堪用，續約就順下去了。

Matt Pocock 這種等級的 KOL 一旦真的搬家，下面跟著搬的不會少。

## 中文圈開發者的反應：嘲諷 + 唱衰 + 馬上跑

X 上 5/14 整天都在罵。挑幾條我覺得講到點的：

[**@Junexus_indie**](https://x.com/Junexus_indie/)：「周限额加 50%，程序化额度砍 50 倍，这操作像先请你吃席再把筷子收走。Anthropic 不是在做产品，是在给用户上行为规范课。」

—— 這個比喻精準到我看完就想抄。Anthropic 同一天宣布**互動式週限額 +50%**（看起來是禮物），同時切 AFK quota（真正的成本控制）。**「吃席」是文青化的「temptation pricing」**。

[**@listudio**](https://x.com/listudio/)：「提限是在安抚手动用户，砍程序化入口是在控成本。本质是把订阅和 API 边界重新画死，但开发者工作流一旦迁走，信任很难再迁回来。」

—— 戰略視角最清楚的一條。我前面講 Anthropic 在「重新定義商業模型」，他直接點出**這次最大的代價是信任**。一個禮拜以前你還相信「Claude 訂閱什麼都能跑」，現在你被迫重新分類每一個工作流。

[**@macji**](https://x.com/macji/)：「Claude 这波是真的放水养鱼啊，限额提高爽了，但 SDK 那边收紧其实是在圈地收租。」

[**@QT9277**](https://x.com/QT9277/)：「Anthropic 套路深，提免费额度，砍付费额度。」

[**@bigblue_2025**](https://x.com/bigblue_2025/)：「笑死。反正 claude code 的付费程序员到 6 月底会跑掉 20%，全部转成 codex。」

—— 20% 這個數字沒有來源，但**「跑掉一批」這個預期已經在社群裡共識化了**。

[**@0x_XiaoBaiAI**](https://x.com/0x_XiaoBaiAI/)：「还好我昨天刚换 Codex，不然今天得哭死😂」

—— 已經有人提前跳船。

還有一個技術細節值得注意，[**@m13v_**](https://x.com/m13v_/) 指出：「50% bump to weekly quotas keeps the headline but the rolling 5-hour window is unchanged. weekly users see the bigger ceiling, 5-hour users hit the same wall by lunch.」

—— **週限額 +50% 是頭條，5 小時滾動窗口沒動**。也就是說重度用戶中午前還是會撞牆，這個 +50% 對真正密集用 Claude Code 寫程式的人是**沒有實感的**。他做了一個叫 [claude-meter.com](https://claude-meter.com/) 的工具來即時追蹤 5 小時窗口。

最幽默的是這條 [**@Tony_MT_IM**](https://x.com/Tony_MT_IM/)：「典型的"先给你一颗糖，再让你上瘾"策略 🍬。提高 50% 限额 - 用户：哇 Anthropic 好大方！然后推出 Agent SDK 额度调整 - 用户：等等，我的钱包怎么了？💸 这不就是超市免费试吃，然后你不知不觉推着满满一车东西去结账的感觉吗 😂」

最後一條我看完笑出來 [**@dontry018**](https://x.com/dontry018/)：「这证明它们已经将优先级调整到企业用户了。个人用户对于他们来说是负资产。」

—— 講得難聽，但**這就是真相**。Anthropic 的收入結構裡，企業 API 客戶（Cursor、Perplexity、各大金融客戶）才是主力。$200 訂閱用戶拿去跑 OpenClaw、跑 GitHub Actions、跑批次任務，從 Anthropic 的視角看就是**虧本邊際**。砍掉是遲早的事。

## 對台灣開發者的三條路

如果你 6/15 之後不想被砍 80%，現在有三條路可以選。

### 路線一：留在 Claude，把 workflow 改成 human-in-the-loop

最省力。把所有 AFK 自動化拆掉，回去用 Claude Code 互動模式。`claude -p` 換成 `claude` 開 REPL、GitHub Actions 拔掉、OpenClaw 改用 OpenRouter 接其他模型。

**適合：** 自己一個人開發、用量中等、習慣 Claude 寫程式風格的人。

**代價：** 失去半夜跑批次、失去 PR 自動 review、失去背景 agent。

### 路線二：跳 Codex，吃 2 個月免費

最激進。把 Claude 換成 Codex，把 Cursor 配置改一改、把 IDE plugin 換掉、把自動化腳本重寫成 OpenAI API。

**適合：** ChatGPT 生態本來就在用、團隊有人懂 GPT 系列的工作風格、IT 採購願意賭 OpenAI 中長期跟得上 Claude 程式碼能力的公司。

**代價：** 程式碼風格會變（GPT-5.4 太囉嗦的問題我在前一篇 OpenClaw 文有寫過解法）。

### 路線三：API 分層 + 地端混搭

最技術。重度任務走 Claude Opus API（自己付 token，沒有訂閱中間層）、中低任務走 Haiku / GPT-5.4 mini / Gemini Flash、敏感任務和高頻查詢下地端 Qwen 3.5 27B。

**適合：** 已經在用 OpenRouter、習慣 model routing、團隊有人會調 system prompt 的人。

**代價：** 自己要管 token 預算、要配置分流邏輯、地端要有一張 RTX 5090 等級的卡（我前幾天剛測完 [Qwen 3.6 27B 在 RTX 5090 上的七種推論引擎 benchmark](/qwen-3-6-27b-rtx-5090-inference-engine-benchmark/)）。

我自己會走第三條路。原因不是 Codex 不好——Codex 我也在試——而是**經過 OpenClaw 被封、AFK 被砍這兩次事件，我不想再讓任何一家平台單點決定我的 agent infra**。API 分層 + 地端混搭最麻煩，但**沒有任何一家公司能在週四傍晚發一封信，把我的工作流砍掉**。

## 真正的信號：Agent infra 正在分裂

把這次公告放到產業脈絡裡看，會發現 Anthropic 在做一件更大的事——**把 AI 市場分成兩個**：

**互動式市場（Anthropic 想守的）：** 訂閱制、人類在場、低速高品質、品牌綁定、續訂友善。Claude Code、Cursor、Claude Cowork、claude.ai 都歸這裡。

**程序化市場（Anthropic 想推到 API 上）：** 按量計費、AFK、高速低監督、商業中介層、價格敏感。Agent SDK、GitHub Actions、第三方 wrapper、自動化腳本歸這裡。

OpenAI 的策略剛好相反——**用 Codex 兩邊都吃**。$100 Pro 對標互動，2 個月免費企業版對標程序化。

對開發者來說，這代表一件事：**你之前那種「一個訂閱搞定所有用途」的好日子結束了**。從 6/15 開始，每個工作流都要重新問自己：這個任務是互動式還是程序化？該走訂閱還是 API？該選哪家供應商？

Matt Pocock 是第一個公開破防的 KOL，他不會是最後一個。

而 Sam Altman 顯然準備好接所有破防的人。

---

## 延伸閱讀

- [Anthropic 封殺 OpenClaw 之後的三層替代方案](/anthropic-kills-openclaw-gpt54-migration-guide/) — 同一條時間線，4 月那波
- [Qwen 3.6 27B 在 RTX 5090 上的七種推論引擎 benchmark](/qwen-3-6-27b-rtx-5090-inference-engine-benchmark/) — 地端混搭的硬體基礎
- [OpenClaw 成本優化指南：97% 削減](/openclaw-cost-optimization-guide-97-percent-reduction/) — API 分層的方法論

## 常見問題 Q&A

**Q: 我現在 Max 20x，6/15 之後是不是就完全不能用 GitHub Actions 了？**

不是完全不能，是改吃 $200 credit。輕度用沒事，重度用很快撞牆。

**Q: $200 credit 換算成 token 大概可以跑多少？**

按 Opus API 大約 $15/M output token 算，$200 大約 13M output token。一個 PR review 平均吃 20-50K token，**撐 250-650 個 PR**。一天 10 個 PR 就 1 個月。

**Q: Codex 兩個月免費的窗口什麼時候截止？**

5/14 公告 + 30 天窗口，大約 6/13 截止。

**Q: 如果我只用 Claude Code 互動模式，會被影響嗎？**

不會。訂閱額度繼續用，跟過去一樣。

**Q: OpenClaw 之後還能用嗎？**

可以，但要換 token 來源（GPT-5.4、OpenRouter、地端模型），詳見前一篇 OpenClaw 封殺文章。
