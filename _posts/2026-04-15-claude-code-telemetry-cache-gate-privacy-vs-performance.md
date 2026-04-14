---
layout: post
title: "關掉 Claude Code 遙測，效能就被懲罰？——一場隱私 vs 快取的技術鑑識"
date: 2026-04-15 07:00:00 +0800
permalink: /claude-code-telemetry-cache-gate-privacy-vs-performance/
image: /assets/images/claude-code-telemetry-cache-gate-issue-45381.png
description: "社群炸鍋說 Anthropic 懲罰關掉遙測的使用者，cache TTL 從 1 小時降到 5 分鐘，號稱 12 倍效能懲罰。Claude Code 作者 Boris Cherny 親自回應：這是 experiment gate 和 telemetry 共用開關的 bug，不是刻意設計。4 天內修復（v2.1.108）。但這個 bug 暴露了更深的問題：閉源工具的 feature flag 遠端控制權、遙測與功能配置的 coupling、以及我們對 AI coding 工具信任的脆弱基礎。順便整理了 Claude Code 省 Token 的實戰規則——cache 還熱就繼續聊，別動不動 /clear。"
---

![Claude Code Telemetry Cache Gate - GitHub Issue #45381](/assets/images/claude-code-telemetry-cache-gate-issue-45381.png)

## 事件經過：一個 GitHub Issue 引爆社群

2026 年 4 月 9 日，GitHub 使用者 EmpireJones 在 Claude Code repo 提交了一個 bug report（[#45381](https://github.com/anthropics/claude-code/issues/45381)）：

> 當你用 `DISABLE_TELEMETRY=1` 關掉遙測，Claude Code 的 prompt cache TTL 會從 1 小時降回 5 分鐘。

他寫了一個 Python 腳本來復現：

```
baseline:                          ttl=60m  1h=8215   5m=0
disable_telemetry:                 ttl=5m   1h=0      5m=8094
disable_nonessential_traffic:      ttl=5m   1h=0      5m=8099
```

數據非常清楚：關掉遙測，1 小時快取直接消失。

然後 X（Twitter）上有人把這件事翻譯成：

> "Claude Code literally punishes you for turning off telemetry. Privacy costs you 12x performance. Anthropic is an evil corp."

61 個 thumbs up，27 個 confused。社群炸了。

---

## 技術鑑識：到底發生什麼事

先講結論：**這是一個 bug，不是刻意懲罰。**

但要理解為什麼這個 bug 會發生，需要知道 Claude Code 的實驗系統怎麼運作。

Claude Code 使用「experiment gates」來做 A/B 測試——某些功能只對一部分使用者開放，用來蒐集數據決定是否全面上線。1 小時 prompt cache 就是其中一個正在測試的功能。

關鍵在這裡：**experiment gates 是從伺服器拉取的，然後在客戶端快取。**

當你設定 `DISABLE_TELEMETRY=1`，Claude Code 會徹底切斷所有對外通訊（they do not call home when telemetry is off）。這意味著：

1. 無法取得 experiment gate 的設定值
2. 程式 fallback 到預設值
3. 預設值是 5 分鐘

所以流程是：

```
遙測開啟 → 取得 experiment gate → 1h cache ✅
遙測關閉 → 無法取得 gate → fallback 預設值 → 5m cache ❌
```

不是「因為你不給我數據所以我降你效能」，而是「你關掉網路請求，我拿不到設定檔，只好用預設值」。

差異很大，但結果一樣——**選擇隱私的使用者，客觀上得到了更差的體驗。**

---

## 官方回應：Boris Cherny 的完整說明

Claude Code 的作者 Boris Cherny 在 issue 裡給了一個非常詳細的回應。我把重點整理出來：

### 1. 1 小時 cache 不一定更好

> "1h prompt cache is nuanced actually. It costs more for cache writes, and less for cache reads."

Cache 寫入成本更高，讀取成本更低。如果你只用一次就結束了，1 小時 cache 反而讓你多付錢。

### 2. 不是所有請求都用 1 小時

即使遙測開啟，很多查詢仍然用 5 分鐘 cache：

- **Subagent 查詢：** 很少被恢復，1 小時 cache 等於浪費
- **API 客戶：** 還沒有預設 1 小時，需要更多測試

### 3. 這是意外副作用，不是設計

> "When you turn off telemetry we also disable experiment gates — we do not call home when telemetry is off — so Claude reads the default value, which is 5m."

他承認這是問題，並承諾：
- 下個版本修復（已在 2.1.108 修復）
- 將客戶端預設值改為 1 小時
- 提供環境變數讓使用者自行控制

### 4. 「12 倍」是誤導

> "The token savings is nowhere near 12x unfortunately. It is a small win though."

12 倍是 cache TTL 的倍數（60 分鐘 / 5 分鐘 = 12），不是實際效能差距。實際的 token 節省幅度遠沒有那麼大。

---

## 為什麼這不是「懲罰」，但也不能說沒問題

我理解 Anthropic 的解釋，技術上確實是 experiment gate 的連帶效應。但我想提幾個不舒服的點：

**第一，預設值的選擇反映了優先級。**

預設值設成 5 分鐘而不是 1 小時，代表工程團隊在設計時的心智模型是「大部分人會開遙測」。選擇隱私的使用者不在預設考慮範圍內。

這不是惡意，但也不是好的工程實踐。

**第二，影響是真實的。**

macOS 使用者 tavaresgmg 的數據：開啟遙測後，同一個 project 的 cache 從 `5m=292` 立刻跳到 `1h=32752`。在他之前超過 2500 萬個 cache-creation tokens 裡，`ephemeral_1h_input_tokens` 一直都是 0。

對 Max 方案的使用者來說，這意味著更頻繁的 cache miss，更高的 token 消耗，更慢的回應速度。

**第三，沒有文件說明這個關聯。**

如果 Anthropic 在文件裡寫清楚「關閉遙測會影響某些效能優化功能」，使用者可以做知情選擇。但這個關聯是社群自己發現的。

---

## Prompt Cache 機制速解

對不熟悉的讀者快速科普：

Anthropic 的 prompt cache 允許你把重複使用的 prompt 前綴快取起來，下次請求時不需要重新處理。

| 項目 | 5 分鐘 TTL | 1 小時 TTL |
|------|-----------|-----------|
| Cache 寫入成本 | 較低 | 較高 |
| Cache 讀取成本 | 較低（但容易 miss） | 較低（且不易 miss） |
| 適合場景 | 短對話、子代理 | 長對話、主代理 |
| Cache miss 頻率 | 較高 | 較低 |

重點：**5 分鐘內沒有新的請求，cache 就過期了。** 你打個字、想一下、查個文件，5 分鐘很容易就過了。1 小時給了更大的緩衝。

對 Claude Code 這種需要頻繁互動但中間會有思考間隔的工具來說，1 小時 cache 確實比 5 分鐘更合理。

---

## 「12 倍效能差距」是真的嗎

社群說的「12x performance penalty」是這樣算的：60 分鐘 ÷ 5 分鐘 = 12。

但這個數字嚴重誤導。

Cache TTL 12 倍 ≠ 效能差距 12 倍。實際影響取決於：

1. **你的使用模式：** 如果你每 2 分鐘就發一次請求，5 分鐘 cache 根本不會過期，差異為零
2. **Context window 大小：** 小 context 的 cache 節省本來就不多
3. **對話連續性：** 如果你頻繁切換任務，cache 怎樣都會 miss

真實差距大概在 5-15% 的 token 節省，不是 12 倍。Boris 自己也說 "it is a small win"。

但——對 Max plan 使用者來說（$200/月），即使 5% 的效率差距，累積起來也不是小數字。

---

## 真正該擔心的事

比起「Anthropic 是不是邪惡企業」這種情緒化的討論，我覺得這個事件暴露了幾個更值得關注的問題：

### 1. Experiment Gate 的權力邊界

Claude Code 是閉源的——GitHub repo 只有文件和 issue tracker，原始碼沒有公開。Experiment gate 的邏輯更不透明：伺服器端決定哪些功能對你開放、哪些不開放，使用者看不到也控制不了。

這不是 Claude Code 獨有的問題——Chrome、VS Code、幾乎所有大型軟體都這樣做。但當這個軟體在幫你寫 production code、存取你的 codebase 時，透明度的標準應該更高。

### 2. 遙測 ≠ 遙測

大部分人關掉遙測是因為不想被追蹤使用行為。但 Claude Code 的實作把「使用行為追蹤」和「功能配置同步」綁在同一個開關上。

這是工程上的 coupling 問題。理想的做法是把功能配置（feature flags）和行為遙測（telemetry）分開，讓使用者可以拒絕追蹤但保留功能優化。

Boris 的修復方向也是這樣——把 1 小時 cache 的預設值寫死在客戶端，不再依賴 experiment gate。

### 3. 閉源工具的可見性問題

Claude Code 是閉源的（Anthropic Commercial Terms of Service），使用者無法審計原始碼。這個 bug 存在了多久？從社群發現到修復，花了多少時間？

- 2026-04-09：Issue 提交
- 2026-04-13：Boris 回應 + 承諾修復
- 2026-04-14：2.1.108 修復驗證通過

4 天修復，速度不慢。但 1 小時 cache 的 experiment 跑了多久？有多少關掉遙測的使用者在不知情的情況下用了更差的 cache？

沒有人知道。

---

## 對 Claude Code 使用者的實際影響

### 你該怎麼做

**如果你是 Max plan 使用者：**
- 更新到 2.1.108 或更新版本，bug 已修復
- 關掉遙測不再影響 cache TTL

**如果你是 API 使用者：**
- API 客戶目前本來就不是預設 1 小時 cache
- 等 Anthropic 完成測試後會逐步推出

**如果你之前關了遙測：**
- 不需要重新開啟
- 更新版本即可

### 環境變數（即將推出）

Boris 承諾會提供環境變數讓使用者自行控制 cache TTL：
- 強制 1 小時
- 強制 5 分鐘

這是正確的方向——把選擇權還給使用者。

---

## 既然聊到 Cache，順便聊怎麼省 Token

這次事件的核心是 prompt cache TTL。既然大家都在關注這件事，不如趁機搞清楚 Claude Code 的 cache 機制，順便把錢花在刀刃上。

社群裡怨聲載道：Max 使用者一週的額度，有人兩天就用完。有人在 AWS Bedrock 上算了一筆帳，一個會話的真實成本超過 134 美元，而 Max 訂閱一個月才 100 美元。Anthropic 的訂閱本身就是虧本在賣。

### 模型每次都在「從頭讀」

要理解配額為什麼燒得快，得先搞清楚 LLM 處理輸入的方式。

想像你每次去圖書館都要做同一件事：找到那本 500 頁的報告，翻到需要的章節，把資料抄下來。第一次花 40 分鐘，第二次問不同問題，還是同一本書，又花 40 分鐘。

LLM 幹的就是這件事。它沒有「記憶」，每次收到你的訊息，都要從頭「讀」一遍完整的輸入內容。

在 Claude Code 裡，輸入通常包括三部分：
- **固定部分：** 系統指令、工具定義、CLAUDE.md 裡的專案規則
- **對話歷史：** 之前所有的對話輪次
- **新訊息：** 你剛輸入的那句話

前兩部分在同一個會話裡幾乎不變，但模型每次都要重新「讀」。聊了 20 輪之後，每條新訊息可能要帶上 10 萬個 Token 的「舊行李」。

### Prompt Cache 怎麼救你

Prompt cache 的機制：第一次讀完後，把中間計算結果存下來。下次遇到相同的輸入前綴，直接用存好的「筆記」，跳過重複計算。

**讀取快取的成本只有重新計算的十分之一。**

一個 20 輪的會話，10 萬 Token 的上下文，cache 一直命中的話，輸入成本比每次全價處理低 6 倍以上。

但 cache 有兩個前提：

**第一，只對「前綴」有效。** 必須從頭開始、一字不差地匹配。第 1 頁改了一個字，整個 cache 全部失效。所以 Claude Code 把不變的內容（系統指令、工具定義）放最前面，每次只有末尾新訊息需要重新計算。

**第二，cache 有存活時間。** 主智能體 1 小時，子智能體 5 分鐘。每次 cache 命中都會刷新計時器，只要你保持互動頻率，cache 可以一直活著。

### 繼續聊還是開新會話：一張決策表

這可能是省 Token 最關鍵的判斷。很多人的默認習慣是「做完就 /clear」，但理解 cache 之後會發現，這個操作經常適得其反——你剛觸發了一次全價上下文重建。

**繼續當前會話的條件（任一即可）：**
- 任務沒變——還在調同一個 bug、寫同一個模組
- 距離上一條訊息不超過 1 小時——cache 還活著
- 上下文裡的內容對當前工作仍然有用

**開新會話的條件（任一即可）：**
- 任務換了——前端寫完要做後端，兩件事的上下文完全不同
- 閒置超過 1 小時——cache 大概率已過期，繼續聊等於觸發全量重建
- 上下文被不相關內容塞滿——試了十幾種方案，噪音太多

一句話：**cache 還熱、任務沒換，繼續聊。cache 過期、任務切換，果斷重開。**

### 五條實戰規則

**一、日常工作用 Sonnet，Opus 留給複雜任務。** Opus 消耗 Token 的速度大約是 Sonnet 的兩倍。大多數編碼任務 Sonnet 就夠了，在 Claude Code 裡輸入 `/model` 切換。

**二、別在會話中間換模型。** Prompt cache 按模型隔離。你在 Opus 上累積了 10 萬 Token 的 cache，切到 Sonnet 問個簡單問題，Sonnet 要從零建立自己的 cache。需要用輕量模型的場景，用子智能體而非切換主模型。

**三、精簡 CLAUDE.md，控制 Skill 數量。** CLAUDE.md 的內容會注入到每一次請求裡。官方建議控制在 200 行以內。載入太多 Skill 和 MCP 服務是配額消耗的隱形殺手。沒在用的 MCP 記得關掉。

**四、長內容給路徑，別往對話裡貼。** 不要把 10000 行日誌貼到對話裡讓 Claude 自己找錯誤，直接給檔案路徑。Claude Code 會自己用 grep 去檢索，只把相關內容拉進上下文。最便宜的 Token，是根本沒進上下文的 Token。

**五、慎用 1M 上下文窗口。** Max plan 預設使用 1M 上下文。但問題在 cache 失效的代價：你用 1M 累積了很長的會話，離開超過 1 小時回來，1M Token 的 cache 全部過期，一條訊息就要觸發全量重建。大多數日常會話在 80-120K 就會觸發壓縮，根本用不到 200K，更別說 1M。

如果你想禁用 1M 上下文，在 `~/.claude/settings.json` 中添加：

```json
{
  "env": {
    "CLAUDE_CODE_DISABLE_1M_CONTEXT": "1"
  }
}
```

如果你想設定自動壓縮的門檻：

```json
{
  "env": {
    "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "200000"
  }
}
```

上下文接近 20 萬 Token 時自動壓縮摘要化，既保留連續性，又防止成本失控。

---

## 坦白說：閉源工具的信任問題

這個事件讓我想到一個更大的問題：**我們對 AI coding 工具的信任，到底建立在什麼基礎上？**

Claude Code 是閉源的。GitHub repo 只有文件和 issue tracker，你看不到 experiment gate 怎麼寫的、cache TTL 怎麼決定的、GrowthBook 到底控制了哪些行為。

如果不是 EmpireJones 寫了那個 Python 腳本，比對 session transcript 裡的 `ephemeral_1h_input_tokens` 和 `ephemeral_5m_input_tokens`，這個問題會被發現嗎？

我在 [Claude Code 資安最佳實踐：14 條建議，每條都有原始碼撐腰](/claude-code-security-best-practices-source-code-verified/) 那篇裡翻過 npm package 裡的 JS bundle，發現 Anthropic 透過 GrowthBook 對你的 CLI 有相當廣泛的遠端控制能力——可以遠端關掉 bypass mode、auto mode、agent swarms，不需要你更新版本，不需要你同意。這次的 cache TTL 事件，只是這套遠端控制機制的副作用之一。

所以信任不能只靠「它是大公司做的」或「它有 GitHub repo」。你需要：

1. **社群監督：** 像這次一樣，有人願意花時間寫腳本驗證
2. **廠商透明度：** 功能變更要有 changelog，不能靜悄悄地改
3. **架構上的保護：** 把功能配置和行為追蹤分開，而不是綁在同一個開關

Anthropic 這次的回應速度和態度是好的——4 天修復，作者親自下場解釋。但如果預設值一開始就是 1 小時，這整件事根本不會發生。

---

## 結論

這個事件不是「Anthropic 是邪惡企業」的證據，也不是「完全沒問題」。

它是一個典型的「功能 coupling 導致的意外副作用」——工程上很常見，但在 AI coding 工具的語境下，信任成本特別高。

三個 takeaway：

1. **更新你的 Claude Code** — 2.1.108 已修復，不需要犧牲隱私來換效能
2. **保持健康的懷疑** — 閉源工具的行為只能靠外部驗證，養成社群監督的習慣
3. **關注架構決策** — Telemetry 和 feature flag 綁在一起是設計缺陷，不是商業陰謀

下次看到「某某公司是邪惡企業」的標題，先找 GitHub Issue 看原始數據。真相通常比標題無聊得多，但也比標題更重要。

---

## 常見問題 Q&A

**Q: 我現在該開還是關遙測？**

更新到 2.1.108 後，這個問題已經不存在了。你可以安心關掉遙測，cache TTL 不會受影響。

**Q: 「12 倍效能懲罰」是真的嗎？**

不是。12 是 cache TTL 的倍數（60min ÷ 5min），不是效能差距。實際差異取決於你的使用模式，Boris Cherny 說是 "a small win"，大概 5-15% token 節省。

**Q: 這只影響 Max plan 嗎？**

根據社群回報，是的。Pro plan 使用者本來就是 5 分鐘 cache，所以沒有差異。

**Q: API 使用者受影響嗎？**

目前 API 使用者沒有預設 1 小時 cache，所以不受這個 bug 影響。Anthropic 正在測試是否對 API 使用者也推出 1 小時 cache。

**Q: Anthropic 是故意懲罰關掉遙測的人嗎？**

從技術證據來看，不是。這是 experiment gate 和 telemetry 共用同一個網路開關的連帶效應。Boris Cherny 的解釋和修復速度都支持這個結論。但這個 coupling 本身確實是一個設計上應該避免的問題。

---

## 延伸閱讀

- [GitHub Issue #45381：原始 Bug Report](https://github.com/anthropics/claude-code/issues/45381)
- [Anthropic Prompt Caching 文件](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [搞懂快取機制，從 Gemma4 到 Claude Code 省 80% Token](/kv-cache-gemma4-claude-code-save-80-percent-token/) — 完整拆解 KV Cache 和 Prompt Cache 的運作原理
- [Claude Code 資安最佳實踐：14 條建議，每條都有原始碼撐腰](/claude-code-security-best-practices-source-code-verified/) — 翻 source code 發現 Anthropic 可以遠端關掉你的 bypass mode、auto mode、agent swarms，experiment gate 只是冰山一角
- [AI Coding 的第一個風險，不是模型——是你一直按「Yes」](/ai-coding-tool-security-risk-prompt-injection-rce/)
- [AI Agent Security：遊戲規則已經改變](/ai-agent-security-you-xi-gui-ze-yi-jing-gai-bian/)
