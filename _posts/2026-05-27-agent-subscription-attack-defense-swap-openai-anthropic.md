---
layout: post
title: "OpenAI 認 bug 重置全站額度、公開鼓勵用第三方 harness：Agent 訂閱戰正式攻守易勢"
date: 2026-05-27 15:30:00 +0800
permalink: /agent-subscription-attack-defense-swap-openai-anthropic/
image: /assets/images/tibo-codex-pi-harness-opencode-tweet.png
description: "OpenAI Codex 負責人 Tibo 這週兩則 X 貼文濃度極高：公開承認 10% production traffic 跑在 Pi harness 跟 OpenCode 上、認 Codex compaction bug 影響 cache hit rate 並重置全站額度。對應到 Anthropic 5/14 把 AFK credit 砍 96%、4 月封殺 OpenClaw，兩家對 Agent 訂閱制的態度已經完全相反。這篇拆 Tibo 兩則貼文背後的攻守易勢，以及 2026 上半年 token 跟訂閱制三條趨勢線——「無限暢用」已死、BYOK 大規模回潮、cache miss 才是真正的成本。"
---

![Tibo（@thsottiaux）X 貼文：Codex 約 5% production traffic 在 Pi harness、另約 5% 在 OpenCode](/assets/images/tibo-codex-pi-harness-opencode-tweet.png)

這週 OpenAI Codex 負責人 Tibo（[@thsottiaux](https://x.com/thsottiaux)）發了兩則 X 貼文，連在一起看，**等於 OpenAI 把這半年的訂閱戰態度直接攤在桌上**。

第一則（5/23）：

> A little secret. About 5% of our production traffic is on the Pi harness, about another 5% is on OpenCode. Reminder you can use your ChatGPT account in a flourishing set of other tools.
>
> We'll continue to make Codex awesome, but you have options.

第二則（這週稍晚）：

> Some of you noticed limits drained faster in Codex, we root caused it to an optimization that we rolled back that had an impact on cache hit rates when compacting across long running sessions.
>
> We fixed this and have now reset usage limits for all accounts. Enjoy the weekend.

兩則貼文加起來大概 400 個字，但濃度極高。對應到 Anthropic 5 月那波 [AFK 額度砍 96%](/anthropic-afk-quota-cut-altman-codex-defection/)，**這就是攻守易勢的訊號**。

## 兩家公司對 Agent 訂閱制的態度，已經完全相反

把這兩家近三個月的動作擺在一起：

| 動作 | Anthropic | OpenAI |
|---|---|---|
| 第三方 harness 使用訂閱額度 | **4 月封殺 OpenClaw** | 5 月公開承認 10% 流量在 Pi harness + OpenCode，鼓勵繼續用 |
| 額度爭議 | 5/14 切出 AFK credit，等於砍 96% | 認 bug、**全站額度重置**、祝你週末愉快 |
| 訊息口吻 | "Subscription is for human-in-the-loop" | "You have options" |
| 對外宣告場合 | Discord、Help Center FAQ | 負責人本人 X 直發 |

這不是同一條商業哲學的微調，是**兩個截然不同的策略**。

## 那 OpenClaw 的流量呢？

Tibo 點名 Pi harness 5%、OpenCode 5%，那 OpenClaw 呢？

**它沒有被 Tibo 單獨列成一個 5% bucket，原因未必是沒有流量，而更可能是統計口徑問題**。

OpenClaw 是上層 agent client / platform，實際執行時底下可以走 Pi harness、Codex harness 或其他 runtime。OpenClaw 自家文件提到，如果沒指定或沒匹配到其他 harness，會 fallback 到 PI；Codex harness 文件也說 auto 模式可能仍以 PI 作為相容性 backend。

也就是說，**如果一個 OpenClaw session 底層跑的是 Pi，那在 OpenAI telemetry 裡自然會被歸到 Pi 那 5%，不是 OpenClaw**。事實上，Tibo 那則貼文上面有人引用就提到「OpenCode, Pi, OpenClaw and more」，他自己只挑了 Pi 跟 OpenCode 報數字。

所以這裡正確的讀法不是「OpenClaw 已經沒人用」，而是——

**Tibo 這句話最重要的不是哪個 client 佔多少，是 OpenAI 願意公開承認第三方 harness / client 已經吃到實質 production traffic，而且沒有把這件事描述成「需要封堵的問題」**。

這個對照才是攻守易勢的真正畫面：

| | Anthropic 的對應行動 | OpenAI 的對應行動 |
|---|---|---|
| 第三方 client 用我的訂閱跑 agent | **封掉它**（OpenClaw 4 月案，我寫過[三層替代方案那篇](/anthropic-kills-openclaw-gpt54-migration-guide/)） | **負責人本人 X 點名第三方 harness 佔 10% 流量，叫大家繼續用** |
| 用戶問「為什麼額度燒這麼快」 | 改 TOS，切出 AFK credit | 認 bug，重置全站 |
| 語氣 | "Subscription is for human-in-the-loop" | "You have options" |

**同一個用戶行為，一邊定義成「abuse 要堵起來」，一邊定義成「生態繁榮的證據」**。

決定性訊號不在誰的模型更強，而是**誰願意讓你拿你的帳號去做你想做的事**。

Anthropic 的邏輯：訂閱賣給「人坐在螢幕前」的場景，AFK 跟批次自動化要丟回 API 按量收費——**鎖住生態、收斂 abuse、保護毛利**。

OpenAI 的邏輯：訂閱是入口，**ChatGPT 帳號是憑證，harness 隨便你挑**。Codex 自己只佔 90%，剩下 10% 給生態系。寧可流失到第三方工具，也不要讓你跳去 Anthropic。

## 為什麼是攻守易勢，不只是策略不同

去年到今年初，劇本是反過來的。Anthropic 出 Claude Code，定義了 harness engineering 這個品類，開發者大規模從 Cursor / Copilot 遷過去。OpenAI 那時候在守——Codex 重啟、ChatGPT Pro 漲到 $200、生態整合慢半拍。

現在反過來：

- **OpenAI 在攻**：Codex 砍價、企業版兩個月免費、公開承認 harness 生態、出 bug 直接重置額度
- **Anthropic 在守**：封殺第三方 client、切出 AFK credit、把訂閱定義收窄

「攻」的姿勢是「**你願意用我，我給你最大彈性**」。「守」的姿勢是「**請按照我定義的方式用我**」。

姿勢本身就是訊號。攻方的成本結構撐得住補貼，守方的單位經濟模型撐不住現在的 abuse 率。坦白講，我不覺得 Anthropic 是壞人，**那 96% 切的是真的有人在跑機房等級的 abuse**。但用戶不看你內部帳，用戶看的是「我這個月還能不能跑」。

## Token 跟訂閱制的整體趨勢

把 Tibo 這兩則放回整個產業的脈絡看，2026 上半年的訂閱制大概是這個樣子：

**第一條線：訂閱費往上、額度往下，但分流給「真人使用」**

- Claude Pro $20、Max 5x $100、Max 20x $200，**但 AFK 切出來獨立 credit**
- ChatGPT Pro $100（從 $200 砍下來），Codex 額度大方
- Cursor / Cody 大量出現「使用快超額」彈窗，靜默調整 model routing

訂閱還在，但**「無限暢用」這四個字已經死了**。所有家都在切。

**第二條線：BYOK（Bring Your Own Key）大規模回潮**

OpenCode、Aider、Continue、Roo Code 這類 harness，2025 上半年大家還在比訂閱整合度，到了 2026 全部回頭做 BYOK 跟 multi-provider routing。原因很簡單——**訂閱條款隨時會改，BYOK 至少帳單透明**。

Tibo 這則「you can use your ChatGPT account in a flourishing set of other tools」，本質上是 OpenAI 承認這個趨勢，**並且選邊站在 BYOK 這側**。

**第三條線：token 報價持續下探，但「能跑多久」不再等於「token 多便宜」**

GPT-5.5、Claude 4.x、Gemini 3 的 token 單價都在往下走。但對 harness 用戶來說，**真正的成本不是單價，是上下文重算**。Tibo 自爆的那個 bug 很關鍵——"impact on cache hit rates when compacting across long running sessions"——一個長 session 的 cache hit 率掉了，token 帳單翻倍跳。

這也是為什麼 Anthropic 切 AFK 切得這麼狠：**長期 background agent 是 cache miss 的重災區**，按訂閱算撐不住。OpenAI 選擇用「修 bug + 重置額度」吸收掉，這背後是基建決策。

## 對 harness engineer 跟訂閱用戶的實際建議

第一，**雙棲不是選擇題，是必修課**。Claude + Codex 同時養著，互動式留 Claude Code，AFK / batch 走 Codex 或直接 API。哪家改條款都有退路。我自己現在工作流就是這樣。

第二，**用 BYOK harness 把帳號變成「憑證」而非「綁定」**。OpenCode、Roo Code、Aider 配 OpenRouter 這條路現在很成熟。Tibo 公開鼓勵這條路徑，**等於 OpenAI 自己背書**。

第三，**地端評估不能再拖**。不是要你今天就買 H100，而是 Qwen3.6 27B / Gemma 4 31B 這個量級的 dense 模型在 RTX 5090 上的實測，你應該心裡有個數字。地端不是省 token 費，是你願不願意把核心流程壓在「**隨時可能改的條款**」上。

---

## 一句話總結

> Tibo 兩則貼文加 Anthropic 5/14 公告，攤開看是同一個故事的正反兩面——**Agent 訂閱戰的攻守已經易勢**，OpenAI 在收用戶，Anthropic 在收 abuse。對開發者來說，這不是該選邊站的時候，**是該重新設計你 Agent Infra 的時候**。

---

## 延伸閱讀

- [Anthropic 把 AFK 額度砍 96%](/anthropic-afk-quota-cut-altman-codex-defection/) — 這篇是同一條時間線的前半段
- [Anthropic 封殺 OpenClaw 之後的三層替代方案](/anthropic-kills-openclaw-gpt54-migration-guide/) — 4 月那波，鎖第三方 client 的開端
- [Qwen 3.6 27B 在 RTX 5090 上的七種推論引擎 benchmark](/qwen-3-6-27b-rtx-5090-inference-engine-benchmark/) — 地端混搭的硬體基礎

## 常見問題 Q&A

**Q: 那 OpenClaw 為什麼沒出現在 Tibo 那份 10% 名單裡？**

很可能是**統計口徑問題，不是它沒有流量**。OpenClaw 是上層 agent client / platform，底下可以走 Pi、Codex 或其他 harness，文件也提到沒指定時會 fallback 到 PI。如果 session 底層跑的是 Pi，在 OpenAI telemetry 就會被歸到 Pi 那 5%。Tibo 那則貼文的引用上下文也提到「OpenCode, Pi, OpenClaw and more」，他自己只挑了兩個明確 bucket 報數字。重點不是哪個 client 佔多少，是 OpenAI 願意公開承認第三方 harness 吃實質流量、而且沒當問題處理。

**Q: Pi harness 跟 OpenCode 是什麼？**

Pi 是第三方 agent runtime，OpenCode 是開源的 coding harness。兩者都支援用 ChatGPT 帳號（OAuth）登入。Tibo 講「10% production traffic」意思是 Codex 訂閱用戶有約 10% 不在用 OpenAI 自家的 Codex CLI / IDE。

**Q: OpenAI 真的不在意用戶流失到第三方嗎？**

短期不在意。對 OpenAI 來說，使用者留在 ChatGPT 帳號體系裡比留在自家 client 重要。Anthropic 反過來——它需要把使用者圈在 Claude Code 裡，才能控制 abuse。

**Q: 那 Anthropic 的策略是錯的嗎？**

不是錯，是處境不同。Anthropic 毛利結構更緊、算力供應更稀缺，沒有空間補貼第三方 harness 的 abuse。但**從用戶體感來說，攻方的姿勢就是比較好看**。

**Q: 重置 usage limits 是什麼意思？真的全部歸零？**

對，所有帳號當月的 usage counter 歸零重算。對重度用戶來說等於白送一個月額度。換成 Anthropic，過去同類事件通常是發 credit 補償，量級也小很多。

**Q: 我應該現在就跳 Codex 嗎？**

不要為了情緒換工具。互動式寫程式 Claude Code 還是最順，AFK / 批次任務 Codex 比較划算。**雙棲，不是換邊**。
