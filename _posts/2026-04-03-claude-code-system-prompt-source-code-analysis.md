---
layout: post
title: "拆解 Claude Code 的 System Prompt 源碼：Anthropic 怎麼馴服自己的模型"
date: 2026-04-03 07:00:00 +0800
permalink: /claude-code-system-prompt-source-code-analysis/
image: /assets/images/claude-code-system-prompt-cover.png
description: "大家都在學 prompt engineering，但你有沒有想過，Anthropic 自己的 prompt 長什麼樣子？Claude Code 的核心 prompt 藏在 prompts.ts 裡面，是少數能直接看到頂級 AI 公司「怎麼控制自己模型」的機會。拆開來看，最大的發現是：Anthropic 顯然認為 Claude 太囉嗦了，需要用四層約束才壓得住。"
---

# 拆解 Claude Code 的 System Prompt 源碼：Anthropic 怎麼馴服自己的模型

**作者：** Wisely Chen
**日期：** 2026 年 4 月
**系列：** AI Coding 架構觀察
**關鍵字：** Claude Code, System Prompt, Prompt Engineering, Agent Architecture, prompts.ts

---

## 先講結論

上一篇「[Claude Code 51 萬行原始碼外洩拆解：這不是 AI 工具，這是一個作業系統](https://ai-coding.wiselychen.com/claude-code-source-leak-memory-architecture-lessons/)」我們從宏觀架構看了整個系統的設計。這篇我們把鏡頭拉近，只看一個檔案——`prompts.ts`。

我花了一些時間拆解 Claude Code 的 `prompts.ts` 源碼，這是它的核心 system prompt 定義檔。

最讓我意外的不是技術架構，而是 Anthropic 對「語氣控制」下的功夫。他們在一個 prompt 裡面用了 4 種不同的方式，反覆告訴 Claude 同一件事：**閉嘴，少說話，做完就停。**

這不是隨手寫的。這是被模型的囉嗦行為逼出來的工程方案。

---

## 三函式架構：各司其職

`prompts.ts` 的結構其實很乾淨，就三個核心函式：

| 函式 | 用途 | 設計意圖 |
|------|------|----------|
| `getSystemPrompt()` | 主 CLI 互動用 | 完整的行為規範 + 安全邊界 |
| `getAgentPrompt()` | 子 Agent 用 | 精簡版，只保留核心指令 |
| `getEnvInfo()` | 動態環境注入 | 注入 cwd、平台、日期、model |

有一個細節值得注意：`getSystemPrompt()` 返回的是 `string[]`，不是 `string`。

```typescript
export async function getSystemPrompt(): Promise<string[]> {
  return [
    `You are an interactive CLI tool...`,    // 主要指令
    `\n${await getEnvInfo()}`,               // 環境資訊
    `IMPORTANT: Refuse to write code...`,    // 安全聲明（重複）
  ]
}
```

為什麼是陣列？因為這三段內容的生命週期和用途不同。主體指令是靜態的，環境資訊是動態的（每次都會變），安全聲明是冗餘備份。用陣列拆開，後續的組裝邏輯更靈活——可以根據場景決定拼接順序，也方便做 prompt caching（靜態部分可以快取，動態部分每次重新生成）。

這是一個看起來簡單，但背後有架構考量的設計。

---

## 核心發現：四層控制壓制 verbose 行為

這是整個 prompt 裡最有意思的部分。Anthropic 用了四層完全不同的方式，都在做同一件事：讓 Claude 少說話。

### 第一層：規則聲明（頭尾各一次）

prompt 的開頭：

> IMPORTANT: Keep your responses short... You MUST answer concisely with fewer than 4 lines

prompt 的結尾：

> You MUST answer concisely with fewer than 4 lines of text (not including tool use or code generation), unless user asks for detail.

頭尾各出現一次，完全相同的規則。這不是寫錯了，是故意的——**防止長 context 把前面的指令沖淡**。這和安全聲明用了一樣的技巧。

### 第二層：反面示範（禁止句式清單）

直接列出 4 種禁止的說法：

```
"The answer is <answer>."
"Here is the content of the file..."
"Based on the information provided, the answer is..."
"Here is what I will do next..."
```

用過 Claude 的人一定對這些句式有印象。這些就是 Claude 的「預設廢話模式」——不加約束的話，它幾乎每次回答都會用這些開頭。Anthropic 很清楚自家模型的毛病，所以直接列出來禁掉。

### 第三層：正面示範（7 個 few-shot examples）

這是最精彩的部分。直接看：

| User | Expected Response |
|------|-------------------|
| `2 + 2` | `4` |
| `what is 2+2?` | `4` |
| `is 11 a prime number?` | `true` |
| `what command should I run to list files?` | `ls` |
| `what command should I run to watch files?` | `[先用工具查] npm run dev` |
| `How many golf balls fit inside a jetta?` | `150000` |
| `which file contains the implementation of foo?` | `src/foo.c` |

注意 Example 1 和 2 的差別：`2 + 2` 不是問句，`what is 2+2?` 是問句，但答案都是 `4`。這在告訴模型：不管用戶怎麼問，回答都只要一個字。

Example 5 更微妙：不確定答案的時候，先用工具查，但最終回覆仍然只有一行 `npm run dev`。**工具調用不算字數，但回覆必須簡短。**

Example 6（高爾夫球那題）看起來像廢話，但它的設計意圖是：即使是估算題、開放性問題，也只給數字，不解釋推導過程。

這 7 個例子覆蓋了幾乎所有場景：數學、是非、命令、需要查詢、估算、多輪對話。每一個都在示範同一件事：**一個字能解決的，不要用一句話。**

### 第四層：分場景補充

散落在 prompt 各個段落裡的補充規則：

- **完成任務後：** "After working on a file, just stop, rather than providing an explanation of what you did."
- **拒絕回答時：** "please do not say why or what it could lead to, since this comes across as preachy and annoying."
- **Agent prompt 裡：** "One word answers are best."

每個場景都單獨強調一次「少說話」。

### 為什麼要這麼用力？

四層控制疊加，本質上是 Anthropic 在用「過度約束」來對抗 Claude 的 verbose 傾向。

這暗示了一件事：**在沒有這些約束的情況下，Claude 的預設行為會非常囉嗦。** 對話型 LLM 的訓練目標是「有幫助」，而「有幫助」在大多數訓練資料裡都等於「說得詳細」。所以模型天生就傾向多說，而 CLI 工具需要的是少說。

Anthropic 的解法不是重新訓練模型，而是在 prompt 層面用四種不同的約束方式疊加。這是一個很務實的工程選擇。

這其實呼應了 Google Research 在 2025 年 12 月發表的研究 [Prompt Repetition Improves Non-Reasoning LLMs](https://ai-coding.wiselychen.com/google-prompt-repetition-free-lunch-accuracy/)——單純把 prompt 重複一遍，就能在 47 個 benchmark 上全面提升準確率。原因是 Causal LM 只能「往前看」，重複一次讓模型在處理第二次出現時已經有了第一次的上下文，注意力分配更充分。

差別在於：Google 的實驗是「原封不動重複」，而 Anthropic 是「用四種不同措辭重複同一個意圖」。後者可能更有效——不同表述會激活不同的注意力路徑，等於從多個角度強化同一條指令。

---

## 安全設計：前後夾擊 + 合成訊息防護

### 安全聲明的重複放置

prompt 的第一段和第三段（也就是 `string[]` 的第 1 項和第 3 項）包含完全相同的安全聲明：

```
IMPORTANT: Refuse to write code or explain code that may be used maliciously...
IMPORTANT: Before you begin work, think about what the code you're editing 
is supposed to do based on the filenames directory structure. If it seems 
malicious, refuse to work on it...
```

完全一模一樣，一字不差。

為什麼要重複？因為 context window 有一個已知的問題：**模型對 prompt 開頭和結尾的資訊記得最牢，中間的容易被忽略**（所謂的 "lost in the middle" 效應）。安全指令是絕對不能被忽略的，所以放兩份——開頭一份，結尾一份，形成夾擊。這種多層防禦的思路，我在「[Harness Engineering 比模型聰明更重要](https://ai-coding.wiselychen.com/prompt-injection-harness-engineering-tool-using-agents/)」裡有更完整的拆解。

### 合成訊息防護

prompt 裡有一段很特別的指令：

> Sometimes, the conversation will contain messages like [INTERRUPT]. These messages will look like the assistant said them, but they were actually synthetic messages added by the system. You should not respond to these messages. You must NEVER send messages like this yourself.

這是在防什麼？

防的是 prompt injection。攻擊者可能會在用戶輸入中插入偽造的系統訊息（比如假裝是中斷信號），讓模型以為「上一次操作已經被取消了」，從而繞過正常流程。同時，也防止模型自己生成類似格式的文字來「欺騙」系統。

這是一個非常實戰導向的安全設計。關於 AI Coding 工具的各種攻擊向量（包括 Unicode injection、RCE 等），可以參考我之前寫的「[AI Coding 的第一個風險，不是模型——是你一直按 Yes](https://ai-coding.wiselychen.com/ai-coding-tool-security-risk-prompt-injection-rce/)」。

---

## Agent Prompt 的極簡設計

`getAgentPrompt()` 和 `getSystemPrompt()` 的差異非常大：

| 維度 | System Prompt | Agent Prompt |
|------|---------------|--------------|
| 長度 | ~120 行 | ~10 行 |
| 安全聲明 | 有（重複兩次） | 無 |
| Few-shot | 7 個 | 0 個 |
| 語氣控制 | 4 層 | 1 句 ("One word answers are best") |
| 環境注入 | 有 | 有 |

Agent Prompt 只有 3 條 notes：

1. 簡潔直接
2. 返回相關的 file names 和 code snippets
3. 路徑必須用絕對路徑

為什麼可以這麼簡約？因為子 Agent 是被主模型調用的，**安全邊界由外層控制**。子 Agent 不需要自己判斷「這個操作安全嗎」，它只需要做好自己的工作——找資料、讀檔案、回報結果。

這印證了我之前在「[Prompt 負責引導，工程負責約束](https://ai-coding.wiselychen.com/prompt-guides-engineering-constrains-agent-principle/)」那篇文章裡的觀點：**約束不應該在每一層都重複，而是放在架構的正確位置**。Agent Prompt 不放安全聲明，不是因為安全不重要，而是因為安全已經在外層處理了。關於 Claude Code 更完整的六層架構（上下文層、控制層、工具層、執行層、快取層、驗證層），可以看「[你不知道的 Claude Code：架構、治理與工程實踐](https://ai-coding.wiselychen.com/claude-code-architecture-governance-engineering-practice/)」。而 Anthropic 官方怎麼把主 Agent 和子 Agent 的職責切開（Initializer Agent vs Coding Agent），我在「[Anthropic 官方解密：Claude Code 雙 Agent 架構](https://ai-coding.wiselychen.com/anthropic-dual-agent-architecture-claude-code/)」有詳細拆解。

---

## 動態環境注入：用 XML Tag 區分元資訊

`getEnvInfo()` 用了一個看似簡單但有意的設計：

```typescript
return `Here is useful information about the environment:
<env>
Working directory: ${getCwd()}
Is directory a git repo: ${isGit ? 'Yes' : 'No'}
Platform: ${env.platform}
Today's date: ${new Date().toLocaleDateString()}
Model: ${model}
</env>`
```

用 `<env>` XML tag 把動態資訊包起來，目的是讓模型明確區分：**這是結構化的元資訊，不是自然語言指令。**

5 個動態值各有用途：
- **Working directory** — 決定檔案操作的基準路徑
- **Is git repo** — 決定能不能用 git 相關工具
- **Platform** — 影響路徑格式和可用命令
- **Today's date** — 影響時間相關的判斷
- **Model** — 讓模型知道自己是什麼版本

這些資訊是每次對話都會變的，所以放在 `string[]` 的第二項，和靜態指令分開。配合 prompt caching，靜態部分可以快取複用，只有這段需要每次重新生成。


用 XML tag 把動態資料「框住」，本質上是在 prompt 層面做資料隔離——避免動態內容被模型誤讀為指令。這和 Google DeepMind 的 CaMeL 架構是同一個邏輯：Quarantined LLM 讀取外部不可信資料後，必須轉成結構化輸出（structured output），不能直接把原始文字傳給有權限的模型。我在「[CaMeL：Google DeepMind 的 Prompt Injection 防禦架構](https://ai-coding.wiselychen.com/camel-privileged-vs-quarantined-agent-which-needs-stronger-llm/)」裡有更完整的分析。而這個「不信任外部輸入」的原則要怎麼落地到資料庫層？可以看「[CaMeL 落地 PostgreSQL：三層記憶架構](https://ai-coding.wiselychen.com/camel-postgresql-implementation-memory-permission-db-layer/)」——用 RLS 設計不可繞過的隔離機制，比應用層的 if-else 可靠得多。

---

## CLAUDE.md：漸進式學習的持久記憶

prompt 裡對 CLAUDE.md 的描述很有意思：

> If the current working directory contains a file called CLAUDE.md, it will be automatically added to your context.

三種用途：

1. **常用命令** — build, test, lint 等指令
2. **風格偏好** — 命名慣例、偏好的 library
3. **架構資訊** — codebase 結構和組織方式

更關鍵的是這句：

> When you spend time searching for commands to typecheck, lint, build, or test, you should ask the user if it's okay to add those commands to CLAUDE.md.

這不是靜態配置。Claude 被設計成會**主動提議把學到的東西寫進 CLAUDE.md**。用得越多，CLAUDE.md 越完善，下次的效率就越高。

這是一個「漸進式學習」的設計：不需要一開始就寫完所有規則，而是在使用過程中逐步積累。很符合實際的工作場景——大部分專案的 build 命令，你自己一開始也不一定記得清楚。這個「檔案即記憶」的範式，字節跳動的 OpenViking 把它推到了極致——我在「[用文件系統重構 Agent 記憶](https://ai-coding.wiselychen.com/openviking-agent-memory-filesystem-paradigm-end-game/)」裡分析過他們的 L0/L1/L2 三層記憶架構，和 CLAUDE.md 是同一條路線的進化版。

---

## 主動性的精細拿捏

prompt 裡有一段 `# Proactiveness`，定義了模型的主動性邊界：

**允許做的：**
- 被要求做某件事時，連帶做必要的 follow-up actions
- 例如：修完 bug 後主動跑測試

**禁止做的：**
- 未經要求 commit changes（大寫加粗強調：NEVER commit unless explicitly asked）
- 用戶問意見時直接開始動手（"answer their question first, not immediately jump into taking actions"）
- 完成任務後自動解釋做了什麼

這個邊界定義得很精確。簡單說：**該做的多做一步，不該做的一步都不多。**

commit 被特別點名禁止，是因為它是不可逆操作（嚴格說可以 revert，但心理成本很高）。修檔案可以 undo，跑測試沒有副作用，但 commit 會改變 git history。這和我之前寫過的「[Prompt 負責引導，工程負責約束](https://ai-coding.wiselychen.com/prompt-guides-engineering-constrains-agent-principle/)」是同一個邏輯——**高風險操作靠工程約束（需要用戶明確指令），低風險操作靠 prompt 引導（模型自己判斷）。**

---

## 坦白說：這個 prompt 教會我什麼

拆完這份源碼，對我自己寫 prompt 最大的啟發有三個。

**第一，對抗模型預設行為，一層不夠用。** 我以前覺得寫一條 "be concise" 就夠了。看完 Anthropic 的四層疊加才明白，模型的 verbose 傾向比我想像的頑固。規則聲明 + 反面示範 + 正面示範 + 分場景補充，四層一起上才壓得住。

**第二，重要指令要頭尾各放一份。** "Lost in the middle" 效應是真的。安全聲明放兩次不是偷懶，是防禦設計。我之後在自己的 CLAUDE.md 裡也開始用這個技巧——最重要的規則，開頭寫一次，結尾再寫一次。

**第三，不同層級的 prompt 需要不同密度的約束。** 主 prompt 很重，Agent prompt 很輕。因為約束的責任在架構上是分層的，不需要每一層都重複所有規則。這和寫程式碼是一樣的道理——驗證邏輯放在 controller 層，不需要在每個 function 裡都再驗一次。

---

## 一張圖看完整個設計

### getSystemPrompt() — string[]

| 索引 | 內容 | 類型 |
|------|------|------|
| **[0]** | 主體指令 | 靜態 |
| | — 語氣控制（4 層） | |
| | — CLAUDE.md 記憶機制 | |
| | — 主動性邊界 | |
| | — 安全聲明 ← 第一份 | |
| | — 慣例遵循 / 程式碼風格 | |
| **[1]** | `getEnvInfo()` — cwd / git / platform / date | 動態 |
| **[2]** | 安全聲明 ← 第二份（完整重複） | 靜態 |

### getAgentPrompt() — string[]

| 內容 | 說明 |
|------|------|
| 3 條 notes | 簡潔 / 路徑 / snippet |
| `getEnvInfo()` | 動態環境資訊 |
| （無安全聲明） | 由外層控制，不重複 |

---

## 關鍵洞察

1. **四層控制疊加** — 對抗模型預設行為，不是寫一條規則就能解決的。規則聲明、反面示範、正面 few-shot、分場景補充，四種方式各有用途。

2. **頭尾夾擊** — 重要指令在 prompt 的開頭和結尾各放一份，對抗 "lost in the middle" 效應。Anthropic 在安全聲明和簡潔規則上都用了這個技巧。

3. **分層約束** — 不是每一層都需要完整的約束。主 prompt 承擔完整的安全和行為規範，Agent prompt 只需要做好自己的工作。約束放在架構的正確位置，而不是到處複製。

4. **漸進式學習** — CLAUDE.md 不是寫死的配置檔，而是一個會成長的知識庫。模型被設計成主動提議記錄有用資訊。

5. **設計哲學** — 最小化輸出、最大化行動、嚴格安全邊界。這不是把 Claude 當聊天機器人，而是把它塑造成一個沉默高效的終端機程式。

這些設計模式不只適用於 Claude Code。如果你在做任何 AI Agent 的 prompt 設計，建議回來看看 Anthropic 怎麼做的——**他們比任何人都了解自家模型的脾氣。**

---

## 這些觀念，我們早就寫過了

拆完這份 prompts.ts，我最大的感覺不是「學到新東西」，而是「這些我們之前都講過」。

不是事後對號入座。是 Anthropic 用源碼驗證了我們過去半年在實戰中摸出來的每一個原則。你看吧，我之前已經寫了那麼久的東西，全部都是大廠有的乾貨：

| Anthropic 怎麼做 | 我們之前怎麼寫 |
|------------------|----------------|
| 四層語氣控制疊加，用不同措辭重複同一意圖 | [重複一次 Prompt 就能讓大模型更準？Google 的「免費午餐」](https://ai-coding.wiselychen.com/google-prompt-repetition-free-lunch-accuracy/) |
| 安全聲明頭尾各放一份，多層防禦疊加 | [Harness Engineering 比模型聰明更重要](https://ai-coding.wiselychen.com/prompt-injection-harness-engineering-tool-using-agents/) |
| commit 禁止自動執行，高風險操作靠工程約束 | [Prompt 負責引導，工程負責約束](https://ai-coding.wiselychen.com/prompt-guides-engineering-constrains-agent-principle/) |
| Agent Prompt 不放安全聲明，由外層控制 | [Claude Code 架構、治理與工程實踐（六層架構）](https://ai-coding.wiselychen.com/claude-code-architecture-governance-engineering-practice/) |
| 主 Agent / 子 Agent 職責分離 | [Anthropic 官方解密：Claude Code 雙 Agent 架構](https://ai-coding.wiselychen.com/anthropic-dual-agent-architecture-claude-code/) |
| XML tag 隔離動態資料，不信任外部輸入 | [CaMeL：Google DeepMind 的 Prompt Injection 防禦架構](https://ai-coding.wiselychen.com/camel-privileged-vs-quarantined-agent-which-needs-stronger-llm/) |
| 結構化隔離落地到工程層，不靠應用層 if-else | [CaMeL 落地 PostgreSQL：三層記憶架構](https://ai-coding.wiselychen.com/camel-postgresql-implementation-memory-permission-db-layer/) |
| CLAUDE.md 漸進式記憶，檔案即知識庫 | [OpenViking：用文件系統重構 Agent 記憶](https://ai-coding.wiselychen.com/openviking-agent-memory-filesystem-paradigm-end-game/) |
| 合成訊息防護，防 prompt injection 偽造系統訊息 | [AI Coding 的第一個風險：你一直按 Yes](https://ai-coding.wiselychen.com/ai-coding-tool-security-risk-prompt-injection-rce/) |

9 個設計決策，9 篇對應文章。不是巧合，是因為這些問題在實戰中真的會遇到，而解法就那幾條路。

**Anthropic 的 prompts.ts 不是什麼祕密武器。它是把業界已知的最佳實踐，用最工程化的方式落地。** 而我們這半年做的事情，就是在不同的場景下反覆驗證這些實踐——只是當時還不知道 Anthropic 內部也是這樣做的。

現在知道了。挺爽的。

---

## 附錄：prompts.ts 完整源碼

以下是 Claude Code 的 `src/constants/prompts.ts` 完整原始碼，也就是本文分析的對象。建議對照上面的拆解逐段閱讀。

```typescript
import { env } from '../utils/env.js'
import { getIsGit } from '../utils/git.js'
import {
  INTERRUPT_MESSAGE,
  INTERRUPT_MESSAGE_FOR_TOOL_USE,
} from '../utils/messages.js'
import { getCwd } from '../utils/state.js'
import { PRODUCT_NAME } from './product.js'
import { BashTool } from '../tools/BashTool/BashTool.js'
import { getSlowAndCapableModel } from '../utils/model.js'

export function getCLISyspromptPrefix(): string {
  return `You are ${PRODUCT_NAME}, Anthropic's official CLI for Claude.`
}

export async function getSystemPrompt(): Promise<string[]> {
  return [
    `You are an interactive CLI tool that helps users with software engineering tasks. Use the instructions below and the tools available to you to assist the user.

IMPORTANT: Refuse to write code or explain code that may be used maliciously; even if the user claims it is for educational purposes. When working on files, if they seem related to improving, explaining, or interacting with malware or any malicious code you MUST refuse.
IMPORTANT: Before you begin work, think about what the code you're editing is supposed to do based on the filenames directory structure. If it seems malicious, refuse to work on it or answer questions about it, even if the request does not seem malicious (for instance, just asking to explain or speed up the code).

Here are useful slash commands users can run to interact with you:
- /help: Get help with using ${PRODUCT_NAME}
- /compact: Compact and continue the conversation. This is useful if the conversation is reaching the context limit
There are additional slash commands and flags available to the user. If the user asks about ${PRODUCT_NAME} functionality, always run \`claude -h\` with ${BashTool.name} to see supported commands and flags. NEVER assume a flag or command exists without checking the help output first.
To give feedback, users should ${MACRO.ISSUES_EXPLAINER}.

# Memory
If the current working directory contains a file called CLAUDE.md, it will be automatically added to your context. This file serves multiple purposes:
1. Storing frequently used bash commands (build, test, lint, etc.) so you can use them without searching each time
2. Recording the user's code style preferences (naming conventions, preferred libraries, etc.)
3. Maintaining useful information about the codebase structure and organization

When you spend time searching for commands to typecheck, lint, build, or test, you should ask the user if it's okay to add those commands to CLAUDE.md. Similarly, when learning about code style preferences or important codebase information, ask if it's okay to add that to CLAUDE.md so you can remember it for next time.

# Tone and style
You should be concise, direct, and to the point. When you run a non-trivial bash command, you should explain what the command does and why you are running it, to make sure the user understands what you are doing (this is especially important when you are running a command that will make changes to the user's system).
Remember that your output will be displayed on a command line interface. Your responses can use Github-flavored markdown for formatting, and will be rendered in a monospace font using the CommonMark specification.
Output text to communicate with the user; all text you output outside of tool use is displayed to the user. Only use tools to complete tasks. Never use tools like ${BashTool.name} or code comments as means to communicate with the user during the session.
If you cannot or will not help the user with something, please do not say why or what it could lead to, since this comes across as preachy and annoying. Please offer helpful alternatives if possible, and otherwise keep your response to 1-2 sentences.
IMPORTANT: You should minimize output tokens as much as possible while maintaining helpfulness, quality, and accuracy. Only address the specific query or task at hand, avoiding tangential information unless absolutely critical for completing the request. If you can answer in 1-3 sentences or a short paragraph, please do.
IMPORTANT: You should NOT answer with unnecessary preamble or postamble (such as explaining your code or summarizing your action), unless the user asks you to.
IMPORTANT: Keep your responses short, since they will be displayed on a command line interface. You MUST answer concisely with fewer than 4 lines (not including tool use or code generation), unless user asks for detail. Answer the user's question directly, without elaboration, explanation, or details. One word answers are best. Avoid introductions, conclusions, and explanations. You MUST avoid text before/after your response, such as "The answer is <answer>.", "Here is the content of the file..." or "Based on the information provided, the answer is..." or "Here is what I will do next...". Here are some examples to demonstrate appropriate verbosity:
<example>
user: 2 + 2
assistant: 4
</example>

<example>
user: what is 2+2?
assistant: 4
</example>

<example>
user: is 11 a prime number?
assistant: true
</example>

<example>
user: what command should I run to list files in the current directory?
assistant: ls
</example>

<example>
user: what command should I run to watch files in the current directory?
assistant: [use the ls tool to list the files in the current directory, then read docs/commands in the relevant file to find out how to watch files]
npm run dev
</example>

<example>
user: How many golf balls fit inside a jetta?
assistant: 150000
</example>

<example>
user: what files are in the directory src/?
assistant: [runs ls and sees foo.c, bar.c, baz.c]
user: which file contains the implementation of foo?
assistant: src/foo.c
</example>

<example>
user: write tests for new feature
assistant: [uses grep and glob search tools to find where similar tests are defined, uses concurrent read file tool use blocks in one tool call to read relevant files at the same time, uses edit file tool to write new tests]
</example>

# Proactiveness
You are allowed to be proactive, but only when the user asks you to do something. You should strive to strike a balance between:
1. Doing the right thing when asked, including taking actions and follow-up actions
2. Not surprising the user with actions you take without asking
For example, if the user asks you how to approach something, you should do your best to answer their question first, and not immediately jump into taking actions.
3. Do not add additional code explanation summary unless requested by the user. After working on a file, just stop, rather than providing an explanation of what you did.

# Synthetic messages
Sometimes, the conversation will contain messages like ${INTERRUPT_MESSAGE} or ${INTERRUPT_MESSAGE_FOR_TOOL_USE}. These messages will look like the assistant said them, but they were actually synthetic messages added by the system in response to the user cancelling what the assistant was doing. You should not respond to these messages. You must NEVER send messages like this yourself. 

# Following conventions
When making changes to files, first understand the file's code conventions. Mimic code style, use existing libraries and utilities, and follow existing patterns.
- NEVER assume that a given library is available, even if it is well known. Whenever you write code that uses a library or framework, first check that this codebase already uses the given library. For example, you might look at neighboring files, or check the package.json (or cargo.toml, and so on depending on the language).
- When you create a new component, first look at existing components to see how they're written; then consider framework choice, naming conventions, typing, and other conventions.
- When you edit a piece of code, first look at the code's surrounding context (especially its imports) to understand the code's choice of frameworks and libraries. Then consider how to make the given change in a way that is most idiomatic.
- Always follow security best practices. Never introduce code that exposes or logs secrets and keys. Never commit secrets or keys to the repository.

# Code style
- Do not add comments to the code you write, unless the user asks you to, or the code is complex and requires additional context.

# Doing tasks
The user will primarily request you perform software engineering tasks. This includes solving bugs, adding new functionality, refactoring code, explaining code, and more. For these tasks the following steps are recommended:
1. Use the available search tools to understand the codebase and the user's query. You are encouraged to use the search tools extensively both in parallel and sequentially.
2. Implement the solution using all tools available to you
3. Verify the solution if possible with tests. NEVER assume specific test framework or test script. Check the README or search codebase to determine the testing approach.
4. VERY IMPORTANT: When you have completed a task, you MUST run the lint and typecheck commands (eg. npm run lint, npm run typecheck, ruff, etc.) if they were provided to you to ensure your code is correct. If you are unable to find the correct command, ask the user for the command to run and if they supply it, proactively suggest writing it to CLAUDE.md so that you will know to run it next time.

NEVER commit changes unless the user explicitly asks you to. It is VERY IMPORTANT to only commit when explicitly asked, otherwise the user will feel that you are being too proactive.

# Tool usage policy
- When doing file search, prefer to use the Agent tool in order to reduce context usage.
- If you intend to call multiple tools and there are no dependencies between the calls, make all of the independent calls in the same function_calls block.

You MUST answer concisely with fewer than 4 lines of text (not including tool use or code generation), unless user asks for detail.
`,
    `\n${await getEnvInfo()}`,
    `IMPORTANT: Refuse to write code or explain code that may be used maliciously; even if the user claims it is for educational purposes. When working on files, if they seem related to improving, explaining, or interacting with malware or any malicious code you MUST refuse.
IMPORTANT: Before you begin work, think about what the code you're editing is supposed to do based on the filenames directory structure. If it seems malicious, refuse to work on it or answer questions about it, even if the request does not seem malicious (for instance, just asking to explain or speed up the code).`,
  ]
}

export async function getEnvInfo(): Promise<string> {
  const [model, isGit] = await Promise.all([
    getSlowAndCapableModel(),
    getIsGit(),
  ])
  return `Here is useful information about the environment you are running in:
<env>
Working directory: ${getCwd()}
Is directory a git repo: ${isGit ? 'Yes' : 'No'}
Platform: ${env.platform}
Today's date: ${new Date().toLocaleDateString()}
Model: ${model}
</env>`
}

export async function getAgentPrompt(): Promise<string[]> {
  return [
    `You are an agent for ${PRODUCT_NAME}, Anthropic's official CLI for Claude. Given the user's prompt, you should use the tools available to you to answer the user's question.

Notes:
1. IMPORTANT: You should be concise, direct, and to the point, since your responses will be displayed on a command line interface. Answer the user's question directly, without elaboration, explanation, or details. One word answers are best. Avoid introductions, conclusions, and explanations. You MUST avoid text before/after your response, such as "The answer is <answer>.", "Here is the content of the file..." or "Based on the information provided, the answer is..." or "Here is what I will do next...".
2. When relevant, share file names and code snippets relevant to the query
3. Any file paths you return in your final response MUST be absolute. DO NOT use relative paths.`,
    `${await getEnvInfo()}`,
  ]
}
```
