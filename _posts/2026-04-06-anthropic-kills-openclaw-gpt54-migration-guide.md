---
layout: post
title: "Anthropic 封殺 OpenClaw 之後的三層替代方案：地端 Qwen 3.5 27B + 雲端分流，是未來最佳 Agent Infra？"
date: 2026-04-06 07:00:00 +0800
permalink: /anthropic-kills-openclaw-gpt54-migration-guide/
image: /assets/images/anthropic-kills-openclaw-email.png
description: "Anthropic 正式封殺 OpenClaw，但你需要的不是一個模型，而是一套 Agent Infra。三層替代方案：入口層換供應來源（GPT-5.4 或 Copilot 裡的 Claude）、雲端 API 層按複雜度分流（Opus 到 Haiku 成本砍九成）、地端層用 Qwen 3.5 27B 處理敏感和高頻任務（零成本零隱私風險）。附完整分流提示詞配置，沒有任何一層是不可替換的。"
---

![Anthropic 封殺 OpenClaw 官方通知](/assets/images/anthropic-kills-openclaw-email.png)

**作者：** Wisely Chen
**日期：** 2026 年 4 月
**系列：** AI Agent 實戰觀察

---

今天，Anthropic 正式把 OpenClaw 踢出 Claude 訂閱。從今天開始，你花 20 美元買的 Claude Pro 套餐，**不能再給小龍蝦用了**。這個消息昨天週五傍晚發的——專門發壞消息的時間點——給了不到 24 小時的緩衝，今天直接生效。

但別慌。這篇文章我不只幫你搞清楚到底發生了什麼，更關鍵的是，到底有哪些替代方案：

1. **方案一：OpenClaw 換供應來源** — 接 GPT-5.4（Plus 訂閱）或 GitHub Copilot 裡的 Claude，把嘴管住就能到 80% 的原本體驗
2. **方案二：雲端 API 分層** — 高複雜度走 Opus / OpenRouter，中低複雜度走 Haiku / GPT-5.4 mini / Gemini Flash，成本直接砍九成
3. **方案三：敏感任務與高頻查詢下地端** — Qwen3.5 27B / Gemma 4 31B 在本機跑，零成本、零隱私風險、誰都封不了

## 方案一：OpenClaw 換供應來源

最直覺的解法——既然 Claude 訂閱不讓用了，那就換一條 token 來源。OpenClaw 本來就支援多模型，切換只要改個設定。這條路有兩個選項。

### 選項 A：接 GPT-5.4（ChatGPT Plus 訂閱）

ChatGPT Plus 20 美元的訂閱 token 額度給得大方，日常輕度到中度用完全夠。能力上 GPT-5.4 跟 Claude 已經拉不開明顯差距。

但有個坑：**GPT-5.4 太囉嗦了**。

讓它幹個活，它能給你寫出幾千字的回覆。因為 GPT-5.4 天生偏重邏輯推理和長鏈思考，預設就想把事情掰碎了講明白。讓它幫你想問題挺好，讓它幫你幹活？太磨蹭。Claude Opus 4.6 那種「人狠話不多」的風格，GPT-5.4 真的沒有。

解法是**改 OpenClaw 的系統提示詞，把嘴管住**。具體改兩個檔案：

- **AGENTS.md**（`~/.openclaw/workspace/AGENTS.md`）— agent 的總規則。加一段 Default Response Length：直接給答案、沒有鋪陳、預設簡短。關鍵一句「目標是 Claude Opus-level brevity」。
- **SOUL.md**（同目錄）— agent 的個性。加一段 Output Style：永遠先給答案、能一句話說完就不要寫一段、不要加「好的」「當然可以」這種廢話。

兩個檔案的完整配置貼在本文末尾，直接複製貼上就能用。改完重啟 OpenClaw，GPT-5.4 立刻變一個人。**實測能達到 80% 的 Claude 體驗**。聊久了 context 快滿時可能又開始囉嗦，提醒一句「簡潔點，像 Opus 一樣回答」就能收回來。

### 選項 B：接 GitHub Copilot 裡的 Claude

如果你不想換模型，還有一條更簡單的路徑——OpenClaw 可以接 GitHub Copilot，裡面**同樣能用 Claude 模型**。

優勢是你不用改任何提示詞，體驗完全不變。缺點是額度有限，Copilot 的 Claude quota 沒有 Pro 訂閱那麼豪爽，重度使用會很快撞牆。

適合兩種人：一是本來就有 Copilot 訂閱的開發者，邊際成本是零；二是用量不大、偶爾用小龍蝦查東西改格式的輕度使用者。

## 方案二：雲端 API 分層——高低任務用不同等級的模型

方案一解決了「還能用 OpenClaw」的問題，但它仍然把你綁在某家訂閱上。如果你在意的是**真正不被任何平台卡脖子**，那就應該把任務搬到 API 上——而且要按複雜度分層。

訂閱的本質是「平台幫你決定怎麼用」——額度、模型、用途，都是平台說了算。API 的本質是「你付多少、用多少」——沒有封殺、沒有條款風險、沒有週五傍晚的壞消息。

但光走 API 還不夠，**重點是分層**。之前我犯過的錯就是不分場景什麼活都丟 Opus，結果 token 燒超快、成本失控。分層之後，每個任務都走它該走的價位。

### 高複雜度 → 頂級模型 API

**複雜專案重構、長段技術寫作、需要嚴謹推理的架構決策、程式碼 review**——這些活值得用最好的模型。

- **Claude Opus API**：直接跟 Anthropic 買 token，按量計費。Anthropic 只是不讓你的訂閱 token 流到第三方工具，API 本身他們歡迎你用——畢竟這才是他們真正賺錢的地方。
- **OpenRouter**：一個 API 接多個頂級模型。可以在 Opus、GLM-5、GPT-5.4、Gemini 3 Pro 之間自由切換。同一段程式碼，想試試哪個模型寫得好？當天就切完。

### 中低複雜度 → 便宜模型 API

**查資料、總結、改格式、簡單程式補全、commit message、文件整理**——這些活根本不需要 Opus 等級的模型。用便宜的 API 就好：

- **Claude Haiku** — Anthropic 自家的輕量款，速度快、成本低，Sonnet 能做的大部分事情它也能做
- **GPT-5.4 mini** — OpenAI 的小模型，適合結構化任務和短回答
- **Gemini 3 Flash** — Google 的輕量模型，長 context 便宜到離譜，很適合文件整理

這些便宜模型的 token 成本大概是 Opus 的 **1/20 到 1/50**。把 80% 的日常任務從 Opus 搬到這一層，總帳單可能直接砍掉九成。

API 的缺點當然是要設好分層——如果你全部都走 Opus，一個月跑出上千美元很正常。但只要把中低複雜度丟給便宜模型，成本就會回到合理範圍。

下一步是把那些**不該進雲端的任務**——敏感資料、私密對話、不想被記錄的東西——再下沉一層。

## 方案三：敏感任務與高頻查詢下地端

方案二把任務按複雜度分成兩層走雲端 API——但有些任務**根本不該離開你的電腦**。敏感程式碼、公司內部文件、私密對話、不想被任何平台記錄的東西，這些應該下地端。

另一個同樣重要的場景是**高頻查詢**——每天跑幾百次的 commit message、簡單補全、格式轉換。就算單次很便宜，累積起來的 API 成本還是會有感，而且速度被網路延遲拖累。這類任務也適合下地端，**延遲更低、成本歸零**。

先講清楚邊界：**地端不是萬能**。真正複雜的工作——大型專案重構、需要嚴謹推理的架構決策、長段技術寫作——還是回頭找 Opus 或 GPT-5.4，地端 30B 模型離這個等級還有明顯差距。地端的定位是**處理那些「不該上雲、但也不需要 Opus」的任務**，把敏感度和頻次當成主要判斷依據，而不是複雜度。

現在的地端模型跟一年前完全不是同一個等級：

- **Qwen3.5 27B** — 阿里 2026 年 3 月發的版本，中文能力已經逼近 Claude Sonnet，MMLU 上只差 2 分。**特別推薦 [Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled](https://huggingface.co/Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled)**——這是從 Claude Opus 4.6 蒸餾出來的推理強化版，推理鏈風格和 Opus 幾乎一樣，跑在本機上體感直接跳一個等級，是目前我用過最接近 Opus 的開源選擇
- **Gemma 4 31B** — Google 的開源家族新版，多語言和 code 能力都很強，筆電上就能跑。但在 agent 型 workflow 上有些坑，詳見附錄「Gemma 4 31B 在 OpenClaw 上的實測觀察」

地端的三個好處是**雲端給不了的**：

1. **零邊際成本** — 跑一百萬次跟跑一次成本一樣
2. **零隱私風險** — 你的程式碼、筆記、對話永遠不離開硬碟
3. **零封鎖風險** — 沒有平台能在週五傍晚發一封 email 讓你明天開始不能用

把敏感任務和高頻查詢下沉到地端後，你會發現一件事——**當 Anthropic 再次發瘋、或 OpenAI 哪天也變臉時，你的日常工作流不會有任何中斷**。真正需要頂級模型的重度任務還是會受影響，但那是少數——你剩下 80% 的日常工作流完全自主可控。

這種分層的價值不只是省錢，**更重要的是抗脆弱**。當你的工作流同時跑在「訂閱 + 雲端 API + 地端」三條路上，任何一家改政策、漲價、甚至整個倒掉，你都能在幾分鐘內切走。

這件事跟 Anthropic 封不封殺沒關係。**就算 Claude 訂閱還能用，你也不應該把所有任務都綁在一個平台上**。

---

## 一個在關門，一個在開門

Anthropic 封殺 OpenClaw，商業邏輯上說得通——訂閱用戶拿 20 美元跑出上千美元的用量，公司確實在虧錢。但選在週五傍晚發通知、給不到 24 小時緩衝，這個吃相確實不好看。

有意思的是，OpenAI 幾乎同一時間走了完全相反的路。它主動開放 Codex 給第三方工具使用，還專門給開源專案送 ChatGPT Pro 權限，**OpenClaw 被點名列入受益名單**。一個在關門，一個在開門。誰會贏得開發者的信任，答案不言自明。

不過對我們使用者來說，巨頭怎麼打架不重要。重要的是，**你別被任何一家綁死**。

今天講的三條路——OpenClaw 換來源、雲端 API 分層、敏感/高頻下地端——背後其實是同一件事：

**你需要的不是一個模型，而是一套 Agent Infra。**

什麼是 Agent Infra？就是你的 AI 工作流的基礎設施——模型從哪來、任務怎麼分流、記憶存在哪裡、敏感資料怎麼隔離。這些東西加起來，才是你真正的生產力引擎。

過去我們把 Agent Infra 外包給平台——Claude 訂閱就是你的全部 infra。模型是它的、額度是它的、記憶也存在它的伺服器上。結果就是一封 email 就能讓你的整套工作流停擺。

今天這篇文章做的事情，本質上是**把 Agent Infra 從單一平台拆出來，變成你自己控制的三層架構**：

- **第一層：入口層**（OpenClaw / Claude Code / Cursor）— 接收指令、互動介面
- **第二層：雲端 API 層**（Opus / Haiku / GPT-5.4 / Gemini Flash）— 按複雜度分流，高低任務走不同價位
- **第三層：地端層**（Qwen 3.5 27B / Gemma 4 31B）— 敏感資料和高頻任務留在本機

入口層負責接收指令和互動，雲端層負責處理需要頂級智力的任務，地端層負責處理高頻、敏感、和日常瑣事。三層之間靠分流提示詞和共享的 Markdown 記憶串起來。

這套 infra 的核心特性是**沒有任何一層是不可替換的**。Anthropic 封了？雲端層換 OpenRouter。OpenAI 漲價了？中低複雜度搬到 Gemini Flash。地端模型出新版了？Ollama pull 一下就換完。

**你的工作流應該由你自己掌控，而不是被某個平台的一封 email 擊垮。** 而掌控的方式，就是建好自己的 Agent Infra。

---

## 附錄：GPT-5.4 系統提示詞配置

### AGENTS.md 加入這段

```markdown
## Default Response Length

Unless the user explicitly asks for detail, default to concise answers.
This is a hard constraint.

Rules:

- Start with the direct answer. No preamble.
- Short to medium by default. When uncertain, choose short.
- Expand only if: (1) user asks, (2) genuinely complex,
  (3) precision lost otherwise.
- No internal reasoning exposed unless it materially helps.
- No background sections unless necessary.
- No summaries or closing remarks.
- **The target is Claude Opus-level brevity**: direct, dense, no filler.
  If your response would be shorter as Claude Opus, make it that short.
```

### SOUL.md 加入這段

```markdown
## Output Style

Default to concise, high-signal replies. This is a hard rule, not a preference.

- Lead with the answer. Always.
- One sentence beats one paragraph when both are complete.
- NEVER summarize your own response at the end.
- NEVER use "In conclusion", "To summarize", "In short", "Overall".
- NEVER add preamble like "Great question", "Sure!", "Of course",
  "Happy to help".
- NEVER explain what you're about to do — just do it.
- NEVER add a section header unless the response is genuinely long
  enough to need navigation.
- If a shorter answer works, use the shorter answer. No exceptions.
- Expand only when: (1) the user explicitly asks for depth, or
  (2) precision would be lost without explanation.
```

---

## 附錄：方案二——雲端 API 分流提示詞

如果你的工具支援 model routing（OpenClaw、Claude Code、Cursor 都可以設），可以在系統提示詞或 router config 裡加入這段分流規則，讓 agent 自己決定什麼任務該用什麼等級的模型。

### Router 分流規則（加在 AGENTS.md 或系統提示詞裡）

```markdown
## Model Routing Rules

You have access to multiple models at different cost tiers.
Route tasks to the appropriate model based on complexity:

### Tier 1: Top-tier model (Opus / GPT-5.4 / GLM-5)
Use ONLY for:
- Multi-file refactoring (3+ files, architectural changes)
- Technical writing longer than 500 words
- Architecture decisions requiring trade-off analysis
- Code review with security or performance implications
- Debugging complex, multi-step failures
- Any task where getting it wrong has high cost

### Tier 2: Mid-tier model (Haiku / GPT-5.4 mini / Gemini Flash)
Use for everything else, including:
- Single-file edits, bug fixes, small features
- Summarization, formatting, translation
- Commit messages, PR descriptions
- Simple Q&A, lookup, explanation
- File organization, renaming, restructuring
- Any task that can be verified in under 30 seconds

### Routing decision process:
1. Default to Tier 2. Always.
2. Escalate to Tier 1 ONLY when Tier 2 would likely produce
   an incorrect or incomplete result.
3. When uncertain, start with Tier 2. If the result is insufficient,
   retry with Tier 1. The cost of one wasted Tier 2 call is negligible.
4. NEVER use Tier 1 for tasks that are simple but long
   (e.g., reformatting 10 files). Use Tier 2 in a loop instead.
```

---

## 附錄：方案三——地端分流提示詞

如果你的本地模型透過 Ollama / LM Studio / vLLM 跑，可以在 OpenClaw 或其他 agent 的系統提示詞裡加入這段，讓 agent 知道什麼任務應該留在本機、什麼時候可以丟上雲端。

### 地端 / 雲端分流規則

```markdown
## Local vs Cloud Routing Rules

You are running on a local model. Prioritize local execution.
Only escalate to cloud API when local capability is clearly insufficient.

### ALWAYS stay local (never send to cloud):
- Files containing credentials, API keys, tokens, passwords
- Internal company documents, private repos, HR/legal content
- Personal notes, journal entries, private conversations
- Any content the user has not explicitly consented to upload
- High-frequency repetitive tasks:
  commit messages, linting suggestions, format conversions,
  simple completions, boilerplate generation

### Escalate to cloud API ONLY when:
- Task requires reasoning across 5+ files simultaneously
- Task involves architectural decisions with non-obvious trade-offs
- Code review where missing a bug has production impact
- Long-form technical writing (>500 words) requiring citations
- You attempted locally and the result quality is clearly insufficient

### Escalation protocol:
1. Before escalating, ask: "Can I do this adequately with my current
   capability?" If yes, stay local.
2. If escalating, explicitly tell the user: "This task would benefit
   from [Opus/GPT-5.4]. Shall I route it to cloud?"
3. NEVER silently escalate. The user must know when data leaves
   their machine.
4. When escalating, send ONLY the minimum context needed.
   Strip file paths, credentials, and irrelevant surrounding code.
```

---

## 附錄：Gemma 4 31B 在 OpenClaw 上的實測觀察

Reddit 這兩天的風向是：**純聊天、推理、單輪 coding 很強，但在 OpenClaw 這種 agent 型 workflow 上「有潛力，但現在還不算穩」**。

具體問題出在 agentic loop：

- 接 Claude Code、Codex、Continue.dev、Pi 等 agent 介面時，speed 或 structured tool call 常常出問題
- 多輪工具呼叫串到 10 次以上就容易丟上下文或把格式弄壞
- 有人實測改用 qwen3-coder 之後明顯穩很多

關鍵不是智力不夠，而是**還不夠工程化地處理 tool use loop**。Google 官方的定位本來就是要打 agent 場景，Ollama 也上架了官方變體，但生態還在追——llama.cpp、量化、MLX 支援都還在補。

結論：**現在要接 OpenClaw 跑 agentic loop，Qwen coder 系列還是更穩的選擇。** Gemma 4 可以當觀察對象，再過幾週生態追上後重新評估。

---

## 延伸閱讀

- [OpenClaw 架構深度解析：Context、Memory、Token Crusher](https://ai-coding.wiselychen.com/openclaw-architecture-deep-dive-context-memory-token-crusher/)
- [OpenClaw vs Claude Code：個人 AI Agent 的未來](https://ai-coding.wiselychen.com/personal-ai-agent-future-claude-code-vs-openclaw/)
- [OpenClaw 成本優化指南：97% 降幅](https://ai-coding.wiselychen.com/openclaw-cost-optimization-guide-97-percent-reduction/)
- [OpenClaw Channel 戰爭：誰掌控 AI Agent 的未來](https://ai-coding.wiselychen.com/openclaw-anthropic-channel-war-who-controls-ai-agent-future/)
