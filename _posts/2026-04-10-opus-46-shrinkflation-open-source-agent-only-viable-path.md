---
layout: post
title: "Opus 4.6 偷偷縮水、Max Plan 燒光速度翻倍：為什麼 Open Source Agent 架構是企業唯一可行方案"
date: 2026-04-10 08:00:00 +0800
permalink: /opus-46-shrinkflation-open-source-agent-only-viable-path/
image: /assets/images/opus-46-shrinkflation-github-issue-42796.png
description: "Opus 4.6 thinking 深度被砍 73%、Read:Edit 比率從 6.6 暴跌到 2.0、Stop Hook 違規從 0 飆到每天 10 次——這不是主觀感受，是 17,871 個 thinking blocks 和 234,760 次工具呼叫的硬數據。當閉源供應商的品質和額度同時縮水，企業唯一可行的路就是：雲地融合 + 開源閉源混搭。Open Source Agent 框架 + Open Source Model，才是你在 2026 年做 AI 工程的基本衛生習慣。"
---

![GitHub Issue #42796: Claude Code is unusable for complex engineering tasks](/assets/images/opus-46-shrinkflation-github-issue-42796.png)

## 目錄

- [發生了什麼事](#發生了什麼事)
- [社群炸了：不是個案，是系統性衰退](#社群炸了不是個案是系統性衰退)
- [硬數據來了：17,871 個 thinking blocks 的真相](#硬數據來了17871-個-thinking-blocks-的真相)
- [Max Plan 的 Session Limits 異常](#max-plan-的-session-limits-異常)
- [AI Shrinkflation：同品牌、漲價格、降品質](#ai-shrinkflation同品牌漲價格降品質)
- [企業端的真實衝擊：不只是我，身邊的人都有感](#企業端的真實衝擊不只是我身邊的人都有感)
- [根本問題：你把所有雞蛋放在一個籃子裡了](#根本問題你把所有雞蛋放在一個籃子裡了)
- [企業唯一可行方案：Open Source Agent + Open Source Model](#企業唯一可行方案open-source-agent--open-source-model)
- [Open Source Agent 框架：現在能用的選項](#open-source-agent-框架現在能用的選項)
- [Open Source Model：誰夠靠譜？](#open-source-model誰夠靠譜)
- [結論：雲地融合、開源閉源混搭，是唯一的路](#結論雲地融合開源閉源混搭是唯一的路)

---

你花了一整年幫公司導入 Claude Code，推動企業訂閱，甚至在內部當了 Anthropic 的傳教士。然後有一天你發現——你最信任的那個模型，連自己的 Plan Mode 都不會用了。

這不是我編的。這是 2026 年 3 月以來，[Reddit r/ClaudeAI](https://www.reddit.com/r/ClaudeAI/comments/1ses1qm/anthropic_stayed_quiet_until_someone_showed/) 和 [X](https://x.com/om_patel5/status/2041971334553727076) 上大量用戶的真實反饋。

## 發生了什麼事

2026 年 3 月底開始，社群出現了密集的 Opus 4.6 品質下降報告。不是那種「我覺得變笨了」的主觀感受，而是**可以具體重現的功能退化**：

1. **Plan Mode 失效** — Claude Code 的原生 Plan Mode，Opus 4.6 直接不認識了。使用者提示進入 plan mode，模型回你「我不確定你在說什麼功能」。這是你自己的功能啊大哥。
2. **程式碼品質斷崖式下降** — 同一個專案，之前 Opus 4.6 寫出來的程式碼品質穩定，現在被 code review 直接打回來，用詞是「dumpster fire」。同一個專案，被迫重寫了兩次。
3. **推理一致性崩壞** — 同樣的 prompt，前後兩次給出邏輯矛盾的回答。不是創意性的差異，是基本推理鏈的斷裂。
4. **工具呼叫失靈** — Claude Code 連自己的內建工具都會搞混，該用 Read 的時候用 Bash，該用 Edit 的時候直接用 Write 覆蓋整個檔案。

## 社群炸了：不是個案，是系統性衰退

Reddit 上[有一串討論](https://www.reddit.com/r/ClaudeAI/comments/1ses1qm/anthropic_stayed_quiet_until_someone_showed/)特別有代表性。標題是：「Anthropic stayed quiet until someone showed...」

裡面的留言讓人看了心涼：

> 「people are paying 20x more and getting worse performance.」

> 「one user showed Claude couldn't even recognize its own native Plan Mode.」

> 「the same project had to be rewritten twice after reviews called the code a 'dumpster fire'.」

X 上 [@om_patel5 的貼文](https://x.com/om_patel5/status/2041971334553727076)更直接：

> 「CLAUDE CODE OPUS 4.6 JUST FORGOT ITS OWN FEATURES.」

他列出的四個症狀：
- can't activate plan mode
- worse code quality
- inconsistent reasoning
- higher cost

然後是那段讓人最不安的話：

> 「i brought this to my org. enterprise subscription. been advocating for years. and now they're looking at [Hugging Face](https://huggingface.co/) alternatives.」

這不是鍵盤酸民在抱怨。**這是企業推廣者在撤退。**

## 硬數據來了：17,871 個 thinking blocks 的真相

如果你覺得上面那些都是「主觀感受」，那這個 GitHub Issue 會讓你閉嘴。

Stella Laurenzo——IREE 編譯器專案的核心開發者——在 [anthropics/claude-code#42796](https://github.com/anthropics/claude-code/issues/42796) 提交了一份**用數據挖礦方法分析的品質退化報告**。她分析了 6,852 個 Claude Code session、17,871 個 thinking blocks、234,760 次工具呼叫，時間跨度從一月到三月。

這不是「我覺得變笨了」。這是**可量化、可重現的系統性衰退**。

### Thinking 深度被偷偷砍了 73%

| 時期 | 估計思考深度（字元數） | vs 基準 |
|------|----------------------|---------|
| 1/30 - 2/8（基準期）| ~2,200 | — |
| 2 月下旬 | ~720 | **-67%** |
| 3/1 - 3/5 | ~560 | **-75%** |
| 3/12+（完全遮蔽後）| ~600 | **-73%** |

**而且 Anthropic 同時開始遮蔽 thinking blocks 的內容。** 時間線是這樣的：

| 日期 | Thinking 可見 | Thinking 遮蔽 |
|------|-------------|--------------|
| 1/30 - 3/4 | 100% | 0% |
| 3/5 | 98.5% | 1.5% |
| 3/7 | 75.3% | 24.7% |
| **3/8** | **41.6%** | **58.4%** |
| 3/10-11 | <1% | >99% |
| 3/12+ | 0% | **100%** |

3 月 8 日——thinking 遮蔽超過 50% 的那天——**恰好就是用戶開始大量回報品質下降的日期。** Pearson 相關係數 0.971。

翻譯成白話：**Anthropic 先偷偷把模型的「思考深度」砍了 73%，然後把 thinking blocks 全部遮蔽，讓你看不到他們砍了什麼。**

### 行為模式的轉變：從「先讀再改」變成「直接改」

這組數據最讓我毛骨悚然：

| 時期 | Read:Edit 比率 | 研究:修改 比率 |
|------|---------------|---------------|
| 好的時期（1/30 - 2/12）| **6.6** | 8.7 |
| 過渡期（2/13 - 3/7）| 2.8 | 4.1 |
| 退化期（3/8 - 3/23）| **2.0** | 2.8 |

**從每次修改前讀 6.6 個檔案，變成只讀 2 個。** Read:Edit 比率下降 70%。

好的時候，Claude 的行為模式是：讀目標檔案 → 讀相關檔案 → grep 搜尋整個 codebase → 讀 headers 和 tests → 精準修改。退化之後，它讀一下當前檔案就直接改了，根本不檢查上下文。

同時，Write（覆蓋整個檔案）佔修改操作的比率從 4.9% 翻倍到 11.1%。模型開始用「重寫整個檔案」取代「精準修改幾行」。

### Stop Hook 違規：從 0 次到每天 10 次

Stella 團隊建了一個叫 `stop-phrase-guard.sh` 的 hook，專門偵測模型的偷懶行為（推卸責任、提前停止、權限詢問）。

| 時期 | Stop Hook 違規次數 |
|------|-------------------|
| 3/8 之前 | **0** |
| 3/8 之後（17 天內）| **173**（≈ 10 次/天）|

用戶 prompt 中的挫折感指標從 5.8% 上升到 9.8%（+68%）。每個 session 的平均 prompt 數從 35.9 下降到 27.9（-22%）——人們放棄得更快了。

### 這告訴我們什麼

Stella 的結論很明確：**Extended Thinking 是模型執行複雜工程任務的結構性需求，不是「nice to have」。** 當 thinking 深度被削減，模型的行為模式會從「研究優先」切換到「修改優先」——先改再說，改錯了再改。

而且她特別指出：thinking 深度的下降是在**二月中旬就開始的**，比 thinking blocks 被遮蔽早了兩週。也就是說，Anthropic 先降了品質，然後再把證據藏起來。

**這不是 bug。這是決策。**

## Max Plan 的 Session Limits 異常

除了品質下降，還有一個更實際的痛點：**Claude Max Plan 的 session limits 從 2026 年 3 月 23 日起，消耗速度異常加快。**

Max Plan 是 Anthropic 最高階的訂閱方案，理論上提供最大的使用額度。但大量用戶回報：

- 同樣的工作量，以前一天用不完的額度，現在半天就見底
- Session 計數方式疑似改變，但 Anthropic 沒有任何公告
- 有用戶估算實際可用量縮減了 40-60%

**結合品質下降一起看，這就是典型的 shrinkflation 操作：**

價格不變（甚至更高），但你實際得到的東西——無論是品質還是數量——都在縮水。而且全程沒有官方說明。

## AI Shrinkflation：同品牌、漲價格、降品質

Shrinkflation 這個詞本來是描述消費品的——巧克力棒變小了但價格不變，洗衣精少了 200ml 但包裝長一樣。

現在 AI 產業也出現了一模一樣的模式：

| 項目 | 宣傳 | 實際體驗 |
|------|------|----------|
| Context Window | 1M tokens | 確實有，但品質隨 context 增長急劇下降 |
| Max Effort Reasoning | 最高推理品質 | 基本推理鏈都會斷裂 |
| Best-in-class Coding | 頂級程式碼生成 | 被 review 叫 dumpster fire |
| Plan Mode | 原生功能 | 模型不認識自己的功能 |
| Session Limits | 充足使用量 | 實際可用量疑似縮減 40-60% |

**同品牌、漲價格、降品質。**

最讓人不安的是 Anthropic 的沉默。當社群大量回報問題時，官方的態度是——什麼都沒說。

沒有「我們注意到了，正在調查」。沒有「這是已知問題」。什麼都沒有。

直到有人把具體證據攤出來，才終於有人回應。

這個溝通模式本身就是個紅旗。

## 企業端的真實衝擊：不只是我，身邊的人都有感

我跟幾個同樣深度使用 Claude Code 的朋友聊過，大家的感覺驚人地一致。

我的方法論裡，Claude Code 是核心引擎——PRD 解析、程式碼生成、code review、測試案例，全部圍繞它在轉。我朋友們的場景不同，有的做前端、有的做後端微服務、有的在搞 infra automation，但遇到的問題幾乎一模一樣：

- **PRD → Code 的準確率明顯下降** — 同樣的 PRD 格式、同樣的 prompt 結構，產出的程式碼需要更多人工修改。我自己體感從 85% 掉到大概 60-65%，朋友那邊也差不多
- **Context 管理開始不穩定** — 長對話中途會「忘記」前面定義好的規格，然後寫出跟需求矛盾的程式碼。一個朋友說他現在養成習慣，每 10 輪對話就要手動提醒一次上下文，以前不用這樣
- **工具使用混亂** — 明明該用 Edit 修改幾行，它會用 Write 把整個檔案重寫一遍，如果你沒注意，就會發生 regression。這點大家都碰到了，不是個案

這些不是「AI 本來就不穩定啦」可以帶過的。**當你身邊用不同專案、不同語言、不同場景的人，都在同一個時間點感受到同一種退化，這就不是錯覺，是系統性問題。**

所以也慢慢有蠻多人在考慮說，就是直接換成 [OpenAI Codex](https://openai.com/index/codex/)。或者比較務實的混合做法是：**PRD 繼續用 Opus 寫**（它在理解需求、拆解任務上還是強的），**但程式碼生成交給 Codex 做**。等於把 Claude 當思考引擎，把 Codex 當執行引擎——各取所長，不把命壓在同一家身上。

這個趨勢本身就說明了問題：**當你最信任的工具開始不穩定，使用者不會等你修好，他們會直接找替代品。**

## 根本問題：你把所有雞蛋放在一個籃子裡了

但說實話，問題不只是 Anthropic。

問題是——**我們整個 AI coding 的工作流程，建立在單一供應商的閉源產品上。**

想想看這個依賴鏈：

- 你的企業 AI 工作流
- 依賴 Claude Code（Anthropic 的閉源產品）
- 依賴 Opus 4.6（Anthropic 的閉源模型）
- 受制於 Anthropic 的定價策略
- 受制於 Anthropic 的模型品質決策
- **你完全無法控制以上任何一項**

這跟十年前把所有東西丟上某一家 cloud vendor 然後不做 multi-cloud 是一模一樣的錯誤。

當供應商調整定價，你只能吞。當模型品質下降，你只能等。當 session limits 縮水，你只能付更多錢或降低使用量。

**你沒有 Plan B。**

而且這個 vendor lock-in 比傳統的 cloud lock-in 更危險，因為：

1. **遷移成本極高** — 你的整套 prompt engineering、workflow、團隊訓練，全部是針對 Claude 最佳化的
2. **無法自救** — 閉源模型品質下降，你連 fine-tune 的選項都沒有
3. **資訊不對稱** — 你甚至不知道他們改了什麼，因為模型是黑盒子

## 企業唯一可行方案：Open Source Agent + Open Source Model

好，那怎麼辦？

答案其實很明確：**你需要一個 Open Source 的 Agent 框架，搭配一個夠靠譜的 Open Source Model。**

這不是理想主義。這是風險管理。

你的 Agent 架構不應該被綁定在任何一家供應商的 CLI 工具上。你的模型不應該是你完全看不到、摸不到、改不了的黑盒子。

具體來說：

### Agent 框架：必須是 Open Source

**為什麼 Agent 框架比模型更重要？**

因為 Agent 框架定義了你的工作流程——怎麼讀檔案、怎麼寫程式碼、怎麼做 code review、怎麼管理 context。這些東西一旦綁死在某個閉源工具上，遷移成本比換模型高十倍。

模型可以隨時換。Agent 框架是你的肌肉記憶。

### Model：必須有 Open Source 選項

**不是說完全不用閉源模型。** 是說你必須有一個 open source model 作為 fallback，讓你在閉源供應商出問題的時候，至少能維持基本運作。

就像企業不會只有一個供應商，你的 AI infra 也不應該只有一個模型來源。

## Open Source Agent 框架：現在能用的選項

2026 年 4 月，能用的 open source agent 框架其實已經不少：

### 1. [OpenCode](https://github.com/opencode-ai/opencode)

- **定位：** 終端機原生的 AI coding agent，Go 語言打造，零依賴安裝
- **優勢：** 架構極簡但完整——LSP 整合、multi-model 支援（Claude、GPT、Gemini、Ollama 本地模型）、session 管理、MCP 協議支援。單一二進位檔，不需要 Node.js 或 Python runtime
- **風險：** 專案相對年輕，plugin 生態還在建立中
- **適合：** 喜歡輕量工具、想要完全掌控 agent 行為的工程師。特別適合作為 Claude Code 的直接替代品——操作邏輯幾乎一樣，但你擁有原始碼

### 2. [OpenClaw](https://github.com/all-hands-ai/openhands)（前 OpenHands）

- **定位：** 功能最完整的 open source AI coding agent，Web UI + CLI 雙模式
- **優勢：** 支援多模型（Claude、GPT、Gemini、本地模型），社群活躍，工具鏈完整，sandbox 隔離執行環境
- **風險：** 近期[被 Anthropic 封殺 Claude Pro token 來源](https://ai-coding.wiselychen.com/anthropic-kills-openclaw-gpt54-migration-guide/)，但接 API 或其他模型不受影響
- **適合：** 需要完整 agent 功能（自主任務執行、多步驟推理）的團隊


**我的建議：OpenCode 或 OpenClaw 作為起點，搭配 model routing 策略。** OpenCode 適合想要輕量、終端機原生體驗的工程師；OpenClaw 適合需要完整 agent 功能和 Web UI 的團隊。兩者都支援多模型，讓你可以隨時切換底層模型，不用重寫整套工作流程。

## Open Source Model：誰夠靠譜？

這是最關鍵的問題。Open source model 過去一年的進步是指數級的，但要當企業 fallback，需要滿足幾個硬條件：

1. **Coding 能力要夠** — 至少達到 GPT-4o 水準
2. **Context window 要大** — 企業級 codebase 起碼需要 32K+，最好 128K+
3. **可以本地部署** — 27B-72B 參數量，消費級 GPU 能跑
4. **社群活躍** — 持續更新，bug 有人修

目前其實不管是哪一家，表現都已經到了「能用」的水準：

- **[通義千問 Qwen](https://huggingface.co/Qwen)** — 阿里巴巴出品，coding 能力在開源圈數一數二，中文任務尤其強
- **[GLM](https://huggingface.co/THUDM)** — 智譜 AI 出品，benchmark 表現亮眼，中文理解深度好
- **[MiniMax](https://huggingface.co/MiniMaxAI)** — MiniMax 出品，MoE 架構效率高，長 context 表現穩定，agent 場景適配度好
- **[Kimi](https://huggingface.co/moonshotai)** — Moonshot AI 出品，長文本理解是強項，coding 能力持續追上主流水準
- **[DeepSeek](https://huggingface.co/deepseek-ai)** — MoE 架構，推理效率高，coding 和數學推理都很強
- **[Gemma](https://huggingface.co/google)** — Google 出品，輕量版本（12B）連筆電 GPU 都能跑，入門門檻最低

重點不是哪一家「最好」，而是這些模型都已經過了「堪用」的門檻。基本的 CRUD、bug fix、unit test 生成，品質都接近閉源中階模型的水準。複雜的架構決策和 multi-file 重構，跟 Opus 正常發揮時還有差距，但作為 fallback？**絕對夠用。** 你的 production 不會因為某一家閉源供應商出問題而停擺。

而且這個領域進步的速度是指數級的——半年前還勉強能用的模型，現在已經能獨立完成中等複雜度的任務了。再過半年，差距只會更小。

## 結論：雲地融合、開源閉源混搭，是唯一的路

這篇文章不是在攻擊 Anthropic。Claude Code 正常發揮的時候確實是頂級的，我到現在還在用。但 Opus 4.6 的品質下降和 Max Plan 的額度縮水，不管原因是什麼，都在提醒我們一件事——**你不能把所有雞蛋放在同一個籃子裡。**

接下來企業要做的就兩件事：

1. **雲地融合** — 高複雜度任務走雲端頂級模型 API（Claude、GPT、Gemini），中低複雜度和敏感任務走地端開源模型。不是二選一，是兩條腿走路。雲端給你天花板，地端給你兜底。
2. **開源與閉源混搭** — Agent 框架用開源的（OpenCode、OpenClaw），這是你的肌肉記憶，不能被綁死。模型則是開源閉源都接，哪家好用就用哪家，哪家出問題就切到另一家。

閉源供應商的決策，你無法預測，也無法控制。唯一的保險就是：**擁有一個你自己控制的 Agent 框架，和至少一個你自己能跑的 Model。** 這不是理想主義，這是 2026 年做 AI 工程的基本衛生習慣。

---

**行動建議：**

1. **本週：** 在你的開發機上跑一個 Qwen 3.5 27B 或 Gemma 4 27B，確認它能 work
2. **本月：** 試用 OpenCode 或 OpenClaw，跑你現有的一個小專案
3. **本季：** 建立 model routing 機制，高價值任務走 API，日常任務走地端
4. **持續：** 追蹤 open source model 的進展——這個領域每三個月就翻一次天

不用急著全面遷移。但至少，**給自己留一條退路。**

---

## 常見問題 Q&A

**Q: 我的團隊已經深度使用 Claude Code，遷移成本太高怎麼辦？**

不需要全面遷移。先在 agent 層做抽象——用 OpenCode 或 OpenClaw 包一層，底層還是可以接 Claude API。這樣你的工作流程不變，但模型變成可插拔的。遷移成本最低的方式。

**Q: Open source model 的 coding 能力真的夠用嗎？**

看任務。日常 CRUD、bug fix、unit test 生成，不管是 Qwen、GLM、Llama、DeepSeek 都完全夠用。複雜的系統設計和 multi-file 重構，確實還需要閉源頂級模型。所以才需要 model routing——不同任務用不同模型。

**Q: 本地跑模型需要什麼硬體？**

27B 模型用 4-bit 量化，大概需要 16-20GB VRAM。一張 RTX 4090（24GB）就能跑。12B 模型更簡單，8GB VRAM 的筆電 GPU 就行。

**Q: 這跟你之前寫的「Anthropic 封殺 OpenClaw」那篇有什麼不同？**

那篇是戰術層面——教你怎麼在 OpenClaw 被封之後切換 token 來源。這篇是戰略層面——為什麼你的整個 AI infra 架構需要從根本上減少對單一供應商的依賴。兩篇互補。

---

## 延伸閱讀

- [anthropics/claude-code#42796 — Claude Code is unusable for complex engineering tasks with the Feb updates](https://github.com/anthropics/claude-code/issues/42796)（Stella Laurenzo 的硬數據分析）
- [Reddit: Anthropic stayed quiet until someone showed...](https://www.reddit.com/r/ClaudeAI/comments/1ses1qm/anthropic_stayed_quiet_until_someone_showed/)
- [@om_patel5: CLAUDE CODE OPUS 4.6 JUST FORGOT ITS OWN FEATURES](https://x.com/om_patel5/status/2041971334553727076)
- [Anthropic 封殺 OpenClaw 之後的三層替代方案](https://ai-coding.wiselychen.com/anthropic-kills-openclaw-gpt54-migration-guide/)
- [Shell Wrapper 2.0：Anthropic 真正的威脅](https://ai-coding.wiselychen.com/shell-wrapper-2-anthropic-real-threat/)
- [Claude Code 63 萬行程式碼三個月回顧](https://ai-coding.wiselychen.com/claude-code-630k-lines-three-months-reflection/)
- [AI Coding 半年回顧：需求轉型與工具演化](https://ai-coding.wiselychen.com/ai-coding-half-year-review-demand-transformation-tool-evolution/)
