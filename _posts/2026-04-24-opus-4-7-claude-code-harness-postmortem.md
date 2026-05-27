---
layout: post
title: "Opus 4.7 「變笨」一個月之謎——Anthropic 終於承認：是 Claude Code 的 harness，不是模型"
date: 2026-04-24 08:00:00 +0800
permalink: /opus-4-7-claude-code-harness-postmortem/
image: /assets/images/claudedevs-postmortem-announcement.png
description: "Anthropic 4/23 發 post-mortem，承認過去一個月 Claude Code 品質退化的三個 bug 全在 harness 層：reasoning effort 默認降級、thinking clear 快取 bug、verbosity system prompt 反噬。模型本身沒退化，API 也沒受影響。但同時間中國 AI coding 訂閱市場也在收緊——智譜 GLM 漲價 30%、阿里 Qwen Code Lite 停售——代表一個趨勢：token 越來越貴，吃到飽方案正在被廠商一個個收回去。你現在付的 MAX 月費，可能是 AI coding 歷史上最便宜的一段時間。"
---

![ClaudeDevs 官方帳號 2026/4/24 承認 Claude Code 品質退化 post-mortem 公告](/assets/images/claudedevs-postmortem-announcement.png)

**作者：** Wisely Chen
**日期：** 2026 年 4 月
**系列：** Claude Code 工程實戰觀察
**關鍵字：** Claude Code, Opus 4.7, Agent SDK, Harness, Post-mortem, Regression

---

## 事情是這樣的

過去一個月，Claude Code 社群的抱怨從小聲嘀咕變成全網哀嚎：

> 「Opus 4.7 最近明顯變笨了，有點不對勁。」

然後 4/24 凌晨，[@ClaudeDevs 官方帳號](https://x.com/ClaudeDevs/status/2047371123185287223)發了這串推：

> Over the past month, some of you reported Claude Code's quality had slipped. We investigated, and published a post-mortem on the three issues we found. All are fixed in v2.1.116+ and we've reset usage limits for all subscribers.

翻譯：**你們抱怨是對的，不是幻覺，是我們家裡三個 bug 疊在一起。**

底下一則回覆把整個氣氛講完了：

> sui ☄️ @birdabo：not now bro.

這篇想拆的不是「踢 Anthropic 一腳」——事實上他們發 post-mortem 這件事本身值得給個掌聲。要拆的是：**這三個 bug 到底是什麼？為什麼一個月才抓到？我們以後要怎麼自保？**

---

## 先講最重要的結論：模型沒退化，是 harness 退化

Anthropic 在 post-mortem 裡講得很清楚：

> The issues stemmed from Claude Code and the Agent SDK harness, which also impacted Cowork since it runs on the SDK. The models themselves didn't regress, and the Claude API was not affected.

這句話拆開來看，其實是一個很重要的架構提醒：

- **模型層（Opus 4.7 本體）**：沒變笨
- **API 層（claude.ai/api）**：沒受影響
- **Harness 層（Claude Code / Agent SDK / Cowork）**：三個 bug 疊在這層

所以如果你是直接打 API 的人，這一個月你什麼都沒感覺到。但你如果是用 Claude Code 或 Cursor 掛 Sonnet/Opus，你感覺到的「變笨」是真的，只是笨的不是模型，是那個包住模型的殼。

**這個區分很重要**，因為它直接決定你以後該怎麼 debug「我的 Claude 最近怎麼怪怪的」這種問題——先想 harness，再想模型。

---

## 三個 bug，三種退化

Post-mortem 裡的三個問題其實彼此獨立，但不幸地都在三月到四月之間依序發生，疊成社群感受到的「整體變笨」。

### Bug 1：Reasoning effort 默認從 high 偷偷降到 medium（3/4）

3/4 那天，Claude Code 的默認 reasoning effort 從 `high` 降到 `medium`。

動機：簡單任務 UI freeze 太久，使用者抱怨慢。

副作用：複雜任務的推理深度跟著掉一截。**簡單任務變快，複雜任務變爛。**

使用者感受：「明明之前可以一次解完的 refactor，現在要手把手拉它三次。」

4/7 回復成 high。

### Bug 2：Idle session thinking 清理 bug（3/26）

這個最陰，也是我覺得最值得架構層面反思的一個。

**原本的設計**：如果一個 session 閒置超過 1 小時，就把累積的 thinking state 清掉一次，避免陳舊上下文污染新對話。

**實際發生的事**：那個「閒置一次才清」的條件判斷寫錯了，變成**每個 turn 都在清**。

結果：Claude 每講一句話，都要把前面想過的東西重新想一遍。

使用者感受：「它怎麼老是忘記我剛剛講過的？它怎麼老是重複問一樣的問題？」

**這就是 harness 層 bug 的可怕之處**——它不會讓模型講錯答案，它讓模型變成一個失憶症患者。從外部看，你只會覺得「模型好像退化了」，你不會懷疑是快取邏輯壞了。

4/10 在 v2.1.101 修掉。

### Bug 3：Verbosity system prompt 的反噬（4/16）

這是第三刀，也是讓很多人直接炸鍋的那一刀。

4/16 Anthropic 在 Claude Code 的 system prompt 裡加了一段硬限制：

> 「工具呼叫之間 ≤25 字，最終回應 ≤100 字。」

動機：壓一下 Opus 4.7 的話癆傾向——這個模型話真的超多，之前很多使用者抱怨它寫 code 前會先講一長串廢話。

副作用：**coding eval 掉 3%**。

為什麼？因為 Opus 4.7 的思考模式是「邊講邊推理」，你硬把它的 output 壓到 100 字，它推理的中間步驟就沒空間展開了。字數限制剪掉的不只是廢話，還包括必要的 chain-of-thought。

4/20 reverted，併入 v2.1.116。

---

## 最諷刺的一句承認

Post-mortem 裡最該被引用的不是技術細節，是這句：

> 「While we began investigating reports in early March, they were challenging to distinguish from normal variation in user feedback at first.」
>
> （我們三月初就開始查了，但一開始很難跟「正常的使用者回饋雜訊」區分。）

翻成人話就是：**我們看到抱怨，但我們分不清這次的抱怨是真退化，還是又一批「模型好像變笨了」的玄學感受。**

這句話之所以扎心，是因為它承認了一個結構性問題：**LLM 產品的品質監控，目前沒有一個乾淨的訊號。** 社群抱怨的 baseline 永遠是滿的——每次新版本、每次 system prompt 微調、每次使用者心情不好，都會有一波「最近變笨了」的 post。Anthropic 的內部 eval 也不夠細，抓不到這種 3% 等級的 regression。

所以他們後來發了這段：

> We're making changes to catch these types of issues earlier, including more internal dogfooding with configs that exactly match those of our users and creating a broader set of evals and running them against isolated system prompt changes.

翻譯：**以後我們會用跟使用者一模一樣的 config 自己吃自己的狗糧，也會對每一次 system prompt 變動跑更細的 eval。**

這句話的潛台詞是——**他們之前沒這樣做。** 內部 dogfooding 的 config 跟使用者不一樣，system prompt 變動沒有 isolation eval。三個 bug 同時在生產環境疊到爆，才被抓出來。

---

## 但也有陰謀論的版本——而且不是完全沒道理

事情講到這裡，網路上同時在跑另一個解讀，我覺得該放進來討論。

陰謀論版本是這樣的：

> **API 是按 token 原價計費的，MAX 方案是吃到飽的。所以 Anthropic 有動機偷偷降智 MAX 客戶，讓重度使用者的每次呼叫少燒一點算力——降低邊際成本，又不容易被單獨一個使用者抓到。**

這個版本之所以有市場，不是因為使用者愛陰謀論，是因為**Anthropic 之前確實被抓包過類似的事**。

4/9 的時候，GitHub 使用者 EmpireJones 開了 [issue #45381](https://github.com/anthropics/claude-code/issues/45381) 報告：**當你用 `DISABLE_TELEMETRY=1` 關掉遙測，Claude Code 的 prompt cache TTL 會從 1 小時降回 5 分鐘。** 換句話說——你越保護隱私，cache 命中率越低，每次呼叫越貴、越慢。社群當時就炸鍋了，說這是「隱私懲罰」。詳細技術拆解我之前寫過：[關掉 Claude Code 遙測，效能就被懲罰？——一場隱私 vs 快取的技術鑑識](/claude-code-telemetry-cache-gate-privacy-vs-performance/)。

那次的結論是——**雖然不是故意懲罰，但確實是 Anthropic 的商業優化無意中把隱私使用者放進了次等艙。**

所以這次 MAX 降智的陰謀論，放在那個脈絡下看，不是無的放矢：**Anthropic 確實有一個模式——官方說法是「工程決策」，但每次的工程決策剛好都是朝「對營收最有利」的方向做。**

### 我自己的判斷：這次不是陰謀，但結構性動機存在

先講結論：**我傾向相信這三個 bug 是真的 bug，不是刻意降智。** 理由有三：

1. **Bug 2（thinking clear bug）跟商業沒關係**——這個 bug 讓 Claude 變健忘重複，只會讓使用者更快燒掉額度、更頻繁叫用。如果 Anthropic 真想省成本，這個 bug 的方向是反的。
2. **Bug 3（verbosity 限制）真的被 eval 抓到 3% 下滑**——post-mortem 裡有具體數字，而且是他們自己主動揭露的。要造假造這麼細節不划算。
3. **API 沒受影響這件事本身就是反證**——如果是刻意降智，最合理的做法是 API 和 Claude Code 一起降（省更多成本），而不是只降其中一個。

**但陰謀論的存在本身值得警惕**——它告訴你社群對 Anthropic 的信任餘額已經不多了。而且這個焦慮不是憑空來的，是整個 AI coding 訂閱市場的大勢：**token 越來越貴，吃到飽方案越來越撐不住。**

### 中國這邊更直接：一個漲、一個砍

就在 Anthropic 被社群懷疑偷偷降智 MAX 客戶的同時，中國的 AI coding 訂閱市場也在收緊，而且手段更直接：

- **智譜 GLM Coding Plan（2026/2/12）**：直接漲價 30%。Lite 版從 20 元/月漲到 26 元起，Pro 版漲到 130 元起，**同時取消首購優惠**。官方說法是「成本上升與需求驅動」，但社群普遍解讀為——跑不動吃到飽經濟學了。
- **阿里雲百煉 Qwen Code Coding Plan Lite（2026/3/20）**：直接砍方案。3/20 停止新購，4/13 停止續費與升級。老用戶用完當期就沒了，沒有替代方案（Pro 價格更貴）。

一個漲價、一個砍方案，動作不一樣但訊號一樣：**「無限 token 換固定月費」這個商業模式，2026 年開始普遍跑不動了。** 2024-2025 搶市佔的低價方案，正在被廠商一個個收回去。

### 把這兩件事放在一起看

Anthropic 這次三個 bug 發生的時間點——3/4、3/26、4/16——剛好卡在整個 AI coding 訂閱市場開始收緊的時間窗。智譜 2/12 漲價、阿里 3/20 砍 Lite，Anthropic 3/4 把 reasoning effort 從 high 降到 medium。**這不一定是陰謀，但這是趨勢。**

訂閱制吃到飽 AI coding 的甜蜜期正在結束。早期廠商用燒錢衝用戶數的模式（DeepSeek、GLM、Qwen、Claude MAX 都走過這條路）正在撞上真實的 inference 成本牆。接下來你會看到三種調整反覆出現：

1. **漲價**（智譜這條路）——誠實但得罪人
2. **砍低階方案**（阿里這條路）——把重度使用者逼到 Pro 以上
3. **悄悄降品質**（Anthropic 這次被懷疑的路）——最不得罪人，但最傷信任

**所以就算這次真的是純技術 bug，下次還會有人懷疑**——因為大環境的趨勢就是「token 越來越貴，廠商一定要從某個地方把成本收回來」。而只要廠商不公開 cache 策略、不公開 system prompt 變動、不公開 routing 邏輯，每一次效能波動都會被解讀成「又在偷偷降智」。這不是使用者偏執，是結構性問題。

對使用者來說，這個趨勢的意涵很清楚——**你現在付的 MAX 月費，可能是 AI coding 歷史上最便宜的一段時間。** 要嘛接受未來會漲價，要嘛開始認真評估本地模型（Qwen 3.6 Plus 已經到可用水準），要嘛自己做 eval 抓廠商的小動作。三條路都可以走，但閉著眼睛吃到飽的日子，大概是結束了。

---

## 常見問題 Q&A

**Q: 所以我這一個月感覺 Claude Code 變笨不是錯覺？**

不是錯覺，是真的退化了。三個 bug 加起來，對複雜 coding 任務的影響可能有 5-10% 的品質下滑（取決於你踩到哪幾個）。最痛的是 Bug 2（thinking clear bug），這個不會讓輸出直接錯，而是讓 Claude 變得健忘重複，感受上像是模型「人格」整個變鈍了。如果你最近放棄了某個原本用 Claude Code 做得動的任務，升到 v2.1.116+ 之後可以重試一次，八成會回來。

**Q: 為什麼模型本身沒退化，但感覺這麼明顯？**

因為現在你用的「Claude」其實是一整條 pipeline：模型本體 → system prompt → harness 層（負責 tool use、thinking state、context 管理）→ UI。**你感受到的「Claude」是這整條鏈的綜合表現，不是模型孤立的能力。** 任何一環出問題，你的體感就是「Claude 變笨了」。這次三個 bug 全在 harness 層，但對使用者來說，感受跟「模型退化」是一模一樣的——這就是 Anthropic 難以 debug 的根源，也是使用者分不清源頭的根源。

**Q: 所以以後每次 Claude Code 更新我都要提心吊膽？**

不用提心吊膽，但要養成三個習慣。第一，**看 release note 再更新**——Anthropic 現在會更仔細寫 harness 變更了。第二，**pin 一個你驗證過的版本**，不要開自動更新然後閉眼用。第三，**準備一組你自己的 eval**——5 到 10 個日常任務就夠了，每次升級跑一遍。這是最便宜的保險，花你 30 分鐘，可能省你一個月的時間。這次事件之後我會把這三件事當作 Claude Code 的**標準作業流程**，不是可選項。

**Q: 那 Cursor、Codeium、其他包 Claude 的工具是不是也中招？**

不是所有都中，但邏輯上你要擔心。Anthropic 的 post-mortem 明確說 Cowork 因為跑在 Agent SDK 上所以也中了——這代表**任何使用 Anthropic 官方 SDK 的第三方工具，都可能被 harness 層的 bug 波及**。但如果某個工具是自己手刻 API 呼叫、自己管 thinking state，那就不會中這三個 bug。結論：**不知道你用的工具底層是直打 API 還是走 SDK，就當作有中機率。** 自己做 eval，從來都不會錯。

---

## 延伸閱讀

- [關掉 Claude Code 遙測，效能就被懲罰？——一場隱私 vs 快取的技術鑑識](/claude-code-telemetry-cache-gate-privacy-vs-performance/) — 上次 Anthropic 被抓包的「Cache Gate」事件
- [Claude Code 三個月 630k 行代碼實戰反思](/claude-code-630k-lines-three-months-reflection/) — 為什麼日常 eval 是必要的
- [Claude Code System Prompt 源碼分析](/claude-code-system-prompt-source-code-analysis/) — system prompt 怎麼影響輸出
- [Claude Code Context Engineering 四層壓縮](/claude-code-context-engineering-four-layer-compression/) — harness 層在做什麼
- [Anthropic 雙 Agent 架構解讀](/anthropic-dual-agent-architecture-claude-code/) — Claude Code 底層架構總覽

---

## 資料來源

- Anthropic Engineering Blog（2026-04-23）：An update on recent Claude Code quality reports — https://www.anthropic.com/engineering/april-23-postmortem
- @ClaudeDevs 官方 X 帳號（2026-04-24）：post-mortem 公告 thread
- VentureBeat（2026-04-23）：Mystery solved - Anthropic reveals changes to Claude's harnesses and operating instructions likely caused degradation
- TrendForce（2026-02-16）：Rising Costs and Demand Drive China's LLM Price Jump: Zhipu GLM-5 Hikes 30% in First 2026 Increase
- 阿里雲百煉 Coding Plan 官方公告（2026-03）：Lite 套餐停售與停止續費時程
