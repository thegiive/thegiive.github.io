---
layout: post
title: "搞懂快取機制，從 Gemma4 到 Claude Code 省 80% Token"
date: 2026-04-09 08:00:00 +0800
permalink: /kv-cache-gemma4-claude-code-save-80-percent-token/
image: /assets/images/kv-cache-prompt-cache-paper-figure2.png
description: "早上打開 Claude Code，敲第一句話，2%～10% 的套餐額度沒了。我在本地用 Gemma4 做實驗，發現 prompt 處理從 31 秒降到 0.25 秒——100 倍加速。再翻 Claude Code 源碼，拆解 Anthropic 的多層快取架構：DYNAMIC_BOUNDARY 切分、兩檔 TTL、快取斷裂偵測。從 Transformer 的 KV 快取原理，到 MLSys 2024 論文 Prompt Cache，到你每天該養成的省錢習慣——理解這套機制，同樣的套餐能多撐 3-5 倍。"
---

![Prompt Cache: Modular Attention Reuse for Low-Latency Inference — Figure 2](/assets/images/kv-cache-prompt-cache-paper-figure2.png)

## 為什麼這篇文章很重要

這幾天 Claude Code 的 [GitHub Issue #38335](https://github.com/anthropics/claude-code/issues/38335) 炸鍋了，478 則留言。Max 5x 用戶（月付 200 美元）反映額度異常快速消耗——有人 9 分鐘思考、沒讀檔案、沒輸出，5% 額度就沒了；有人從 40% 直接跳到 85%，中間只下了幾個簡單指令。獨立安全專家分析後指出根本原因：「Regression and cache re-reads with interrupts melt your usage」——快取機制出了回歸性 bug，導致本來應該低成本復用的 token 被全價重算。

Prompt Cache 率的高低，可以嚴重影響你是否可以多 AI Coding 一輪。Claude Code 作者 Boris Cherny 在 X.com 暗示之所以封掉 OpenClaw，就是因為 OpenClaw 的 Prompt Cache 做得太差——他甚至親自提交 Claude API 快取優化的 PR 給 OpenClaw。對現在的 Token 工業來說，這可是大事情。

我帶著這個疑問，在本地用 Gemma4 跑小模型做實驗——發現同一段對話，有些輪次要等 30 秒，有些只要 0.2 秒。為了搞清楚為什麼，我從 Transformer 的注意力機制開始挖，再到 Claude Code 的程式碼實現，發現 Anthropic 在快取上做了一整套精密工程。理解了這套機制，你就知道怎麼讓同樣的套餐多撐 3-5 倍。

這篇文章是「[Claude Code 開源設計細節](https://ai-coding.wiselychen.com/claude-code-source-leak-memory-architecture-lessons/)」系列的延伸。之前我們拆過 [System Prompt 架構](https://ai-coding.wiselychen.com/claude-code-system-prompt-source-code-analysis/)、[資安最佳實踐](https://ai-coding.wiselychen.com/claude-code-security-best-practices-source-code-verified/)、[四層壓縮機制](https://ai-coding.wiselychen.com/claude-code-context-engineering-four-layer-compression/)。今天，我們從 IT 架構的角度，把快取層單獨拉出來講清楚。

### 導讀

本文比較長，按興趣挑著看：

- **一～三**：Prompt Cache 的 IT 架構機制（想搞懂原理的人）
- **四～五**：本地實驗驗證（眼見為憑派）
- **六～八**：Claude Code 最佳實踐 + 省錢技巧（沒時間的直接看這裡）

---

## 一、從 IT 架構看：Prompt Cache 到底在解什麼問題？

先講架構，再看實驗。

每次你對 Claude Code 說一句話，背後發生的不是「AI 讀你這句話然後回答」。完整的 API 請求包含：

- 系統提示詞（~20K tokens）
- 工具定義（~5K tokens）
- 整段對話歷史（隨輪次增長）
- 你剛才說的那句話（~100 tokens）

也就是說，你打的那句「幫我改這個 bug」只佔 100 個 token，但模型要處理的是 25K+ tokens。**每一輪對話，前面所有內容都要重新送一次。**

這個架構問題不是 Claude Code 獨有的。所有 LLM API 都是 stateless 的——伺服器不記得你上一輪說了什麼，每次都要從頭送。

沒有快取的世界，每一輪都是全價：

- Turn 1：系統提示 20K + 你的問題 1K = **21K tokens 全價**
- Turn 2：系統提示 20K + 歷史 1K + 新問題 1K = **22K tokens 全價**
- Turn 3：系統提示 20K + 歷史 2K + 新問題 1K = **23K tokens 全價**
- ...
- Turn 10：系統提示 20K + 歷史 9K + 新問題 1K = **30K tokens 全價**
- 10 輪總計：**~255K tokens（全價）** ← O(N²) 二次增長

**255K tokens，但其中 90% 以上是重複內容。** 這就是 Prompt Cache 要解決的問題：避免對相同的 token 序列重複計算。

---

## 二、KV 快取：Transformer 注意力機制的架構副產品

要理解 Prompt Cache 為什麼可行，得先看 Transformer 的注意力機制。核心公式：**Attention(Q, K, V) = softmax(Q · Kᵀ / √d) · V**

Q、K、V 三個角色：

- **Q (Query)** — 當前新 token：「我要找什麼？」 → 每次不同，不能快取
- **K (Key)** — 歷史 token：「我這有什麼？」（索引） → 算完就固定，可以快取
- **V (Value)** — 歷史 token：「具體內容是什麼？」 → 算完就固定，可以快取

**KV 快取**就是把歷史 token 的 Key 和 Value 存起來，新 token 只需要算自己的 Q，然後查已有的 KV。

這之所以可行，是因為當前所有主流大模型（Claude、GPT、Gemini、Llama、Gemma、Qwen）都是 **Decoder-only 架構**——單向注意力，每個 token 只看前面的 token。前面 token 的 KV 算完就固定了，後面怎麼追加都不影響。

因果遮罩（causal mask）的意思是：

- T₁ 只能看到自己
- T₂ 能看到 T₁ 和自己
- T₃ 能看到 T₁、T₂ 和自己 — **T₃ 的 KV 永遠不變**
- T₄ 能看到前面所有 — **新增 T₄ 不影響 T₁₂₃ 的 KV**

如果是雙向注意力（BERT），加一個新 token 會改變所有 token 的表示，快取全廢。這也是為什麼 BERT 做不了生成式 AI。

### 快取是無損的嗎？

**完全無損。** Transformer 的計算是確定性的，KV 從快取載入和現場計算的結果完全一致。不存在「快取版本比較差」的問題。

### 生成結果會進快取嗎？

**不會。** 模型吐出的 output token 的 KV 在請求結束後丟棄——因為每次生成內容不同（temperature > 0），存了也沒法復用。

但有個精妙之處：在下一輪對話中，上輪的生成結果被拼回 prompt，變成了「輸入」的一部分，自然被快取覆蓋：

- **第 1 輪**：輸入 = 系統提示 + user「你好」。輸出 = assistant「你好！」← 不進快取
- **第 2 輪**：輸入 = 系統提示 + user「你好」+ assistant「你好！」+ user「幫我改程式碼」。其中前面整段前綴從快取讀取，**只有最後的新問題是全價計算**

對話越長，快取覆蓋比例越高，每輪新增計算量越小。

---

## 三、Prompt Cache 的兩層架構：API 快取 + 推論快取

從 IT 架構的角度，Prompt Cache 其實分兩層。拿 Gemini API 來說，它同時提供了這兩種：

| | API 快取 (Context Caching) | 推論快取 (Inference Cache) |
|---|---|---|
| **觸發方式** | 手動標記 `cache_control` | 自動匹配前綴 |
| **生命週期** | 1-24 小時，用戶設定 | 5 分鐘短暫 |
| **適合場景** | 固定文件，反覆問答 | 多輪對話，漸進追加 |
| **價格折扣** | 75% off (Claude / Gemini) | 50-75% off |
| **用戶干預** | 需要顯式標記 | 完全透明 |
| **本地 (Ollama)** | 不適用 | 自動（但不可靠） |

**Claude Code 同時用了這兩層：**

- 用顯式 `cache_control` 標記鎖住系統提示詞和工具 → API 快取
- 多輪對話的訊息歷史自動前綴匹配 → 推論快取

兩層配合，才有了 90% 的快取命中率。

### 學術根基：Prompt Cache 論文

這套機制不是憑空冒出來的。2023 年 MLSys 上有一篇論文 [Prompt Cache: Modular Attention Reuse for Low-Latency Inference](https://arxiv.org/abs/2311.04934)（In Gim et al.），提出了一個關鍵想法：把 prompt 中可復用的文字片段（系統提示、模板、文件）預先計算好 attention states，存在伺服器端，後續請求直接取用。

論文的實驗結果：

- **GPU 推論延遲降低 8 倍**
- **CPU 推論延遲降低 60 倍**
- 不需要修改模型參數，純推論層優化
- 對文件問答、推薦系統等場景特別有效

這篇論文的核心概念——把重複出現的 prompt 片段模組化、預計算 KV 並快取——正是 Claude API 的 `cache_control` 和 Gemini 的 Context Caching 背後的學術基礎。Claude Code 的 `DYNAMIC_BOUNDARY` 設計，本質上就是在做論文裡說的「把 prompt 切成可快取模組」。

### 快取是前綴匹配：像鏈條一樣，斷在哪裡後面全廢

這是最重要的架構限制：**快取只能從頭開始匹配。** 中間有任何一個 byte 不同，後面全部作廢。

三種情境的成本差異：

- **最貴**：Block 3（全域靜態）失效 → 整個請求從頭算，Block 3、Block 4、所有訊息全部重算
- **中等**：Block 4（CLAUDE.md）變了 → Block 3 還能復用，但 Block 4 和之後的所有訊息都要重算
- **最省**：只追加新訊息 → Block 3、Block 4、歷史訊息全部復用，只有新訊息需要計算

### 有快取 vs 沒快取：成本模型差異

假設系統提示 20K tokens，每輪對話增加 ~1K tokens。

**沒有快取（每輪全價）：**

- Turn 1: 21K、Turn 5: 25K、Turn 10: 30K
- 10 輪總計：**~255K tokens（全價）** ← O(N²) 二次增長

**有快取（前綴 1/10 價格）：**

- Turn 1: 26K 等價（首次寫入，貴 25%）
- Turn 2: 3.1K 等價、Turn 5: 3.5K 等價、Turn 10: 3.9K 等價
- 10 輪總計：**~60K 等價 tokens** ← 近似 O(N) 線性增長

**對比：255K vs 60K，快取省了 76%。** 從二次增長降到線性增長——這就是 Prompt Cache 的架構價值。

---

## 四、實驗驗證：本地 Gemma4 的 100x 加速

講完原理，來看實驗。我在本地用 Ollama 跑 Gemma 4（8B 總參數，9.6GB 模型），Apple Silicon Mac 16GB，寫了個測試腳本做多輪對話：先餵一篇 670 token 的文章，然後連續追問 5 個問題。

每輪 API 回傳兩個關鍵指標：prompt 處理時間（消化輸入）和生成時間（吐出回答）：

| 輪次 | Prompt 處理 | 生成 | 總耗時 |
|------|------------|------|--------|
| Turn 1（餵文章） | 24,458ms | 5,095ms (68 tok) | 34s |
| Turn 2（追問1） | 31,036ms | 22,653ms (365 tok) | 58s |
| **Turn 3（追問2）** | **253ms** | 2,511ms (46 tok) | 3.8s |
| Turn 4（追問3） | 203ms | 2,029ms (36 tok) | 3.0s |
| Turn 5（追問4） | 165ms | 1,870ms (37 tok) | 2.4s |
| Turn 6（追問5） | 176ms | 1,235ms (26 tok) | 1.8s |

**Turn 2 到 Turn 3，prompt 處理從 31 秒直降到 0.25 秒——100 倍加速。** 而生成速度始終穩定在 13-20 tok/s，絲毫不受影響。

這說明加速只發生在「消化輸入」階段——正好對應前面講的 KV 快取機制。Turn 1-2 在逐層計算 670+ 個 token 的 KV 張量（60 層 × 670 token × 2），Turn 3 開始全部從記憶體載入。

### 對照組：小模型為什麼無感？

換了 Qwen3.5（0.8B，~1GB）做同樣的測試：

| 輪次 | Prompt 處理 |
|------|------------|
| Turn 1（餵文章） | 566ms |
| Turn 2（追問1） | 173ms |
| Turn 3（追問2） | 182ms |
| Turn 4（追問3） | 212ms |
| Turn 5（追問4） | 227ms |
| Turn 6（追問5） | 240ms |

全程 200ms 上下，波瀾不驚。原因很簡單：小模型算 KV 本來就只要 200ms，快取省不了多少。

**模型越大，KV 計算越昂貴，快取收益越大：**

| | Gemma 4 (4.5B active) | Qwen3.5 (0.8B) |
|---|---|---|
| **未命中** | ~25,000ms | ~566ms |
| **命中** | ~170ms | ~173ms |
| **加速比** | 148x | 3.3x |
| **命中時速度** | 3,000-5,000 tok/s | 3,200-3,900 tok/s |

注意命中時兩個模型速度幾乎一樣——都是從記憶體讀取，瓶頸不再是計算而是 I/O。

### Ollama 的快取問題：效果驚人但不可靠

實驗中也發現，Ollama 的快取是機率性的——同樣的 prompt 跑兩次，快取命中的輪次不同，而且連續命中幾次後可能突然失效（記憶體壓力導致 KV 被淘汰）。

和 Claude API 的確定性快取形成鮮明對比。

---

## 五、Claude Code 的快取工程：原始碼級拆解

用 Claude Code 翻了它自己的原始碼後發現，Anthropic 在快取上做了大量精細工程——遠不是「自動快取」這麼簡單。

在之前的 [System Prompt 源碼分析](https://ai-coding.wiselychen.com/claude-code-system-prompt-source-code-analysis/) 裡，我們提到了 `SYSTEM_PROMPT_DYNAMIC_BOUNDARY` 這條隱藏邊界線。現在我們來看它在快取層的完整設計。

### Prompt 的多層結構

每次 API 呼叫，Claude Code 發送的是一個精心拼接的多層結構：

**system（系統提示詞，~20K tokens）：**

- Block 1：計費歸因頭 → 不快取
- Block 2：CLI 前綴 → 不快取
- Block 3：靜態指令（行為規則等） → **global 快取**（全球所有用戶共享）
- ── DYNAMIC_BOUNDARY ──
- Block 4：動態內容（CLAUDE.md 等） → **org 快取**

**tools（工具 schema）：** session 內凍結

**messages（對話歷史）：** 最後一條訊息上放 `cache_control` 標記

這個設計直接對應到 [四層壓縮機制](https://ai-coding.wiselychen.com/claude-code-context-engineering-four-layer-compression/) 裡講的上下文管理。快取層和壓縮層是互相配合的——壓縮是為了控制上下文大小，快取是為了控制重複計算的成本。

關鍵函式（原始碼位置）：

- `getSystemPrompt()` (prompts.ts:444) — 組裝系統提示詞
- `splitSysPromptPrefix()` (api.ts:321) — 按 DYNAMIC_BOUNDARY 切分
- `buildSystemPromptBlocks()` (claude.ts:3214) — 加 cache_control 標記
- `addCacheBreakpoints()` (claude.ts:3064) — 在最後一條訊息上標記快取斷點

### 兩檔 TTL

- **預設 5 分鐘** — 所有用戶
- **擴展 1 小時** — Pro/Max 訂閱用戶（未超額）、Anthropic 員工

原始碼 claude.ts:408-413：

```typescript
userEligible =
  process.env.USER_TYPE === 'ant' ||
  (isClaudeAISubscriber() && !currentLimits.isUsingOverage)
```

### 快取斷裂偵測

Claude Code 會監控每次呼叫的 `cache_read_input_tokens`，如果比上次下降 >5% 且絕對值 >2000 tokens，判定為斷裂，並分析原因：系統提示詞變了？工具增減了？TTL 過期了？模型切了？

### Sub-agent 的快取隔離

在 [Anthropic 官方 Dual-Agent 架構](https://ai-coding.wiselychen.com/anthropic-dual-agent-architecture-claude-code/) 一文中，我們分析過 sub-agent 的設計。這裡補充一個快取角度的觀察：**sub-agent 幾乎不能復用主線程的快取。**

原始碼裡，快取狀態是按 `querySource` + `agentId` 分開追蹤的。sub-agent 和主線程有三個關鍵不同：

1. **工具集不同** — 主線程有全套工具，Explore agent 只有子集。工具 schema 不同 → 快取前綴不同 → tools 之後全部無法復用。
2. **訊息歷史完全獨立** — sub-agent 有自己的對話上下文。
3. **可能用不同模型** — sub-agent 可能用 Haiku/Sonnet，主線程用 Opus。不同模型 = 不同權重 = KV 張量完全不同 = 零復用。

結果就是：

- **主線程（Opus）**：Block3 復用、Block4+tools 復用、messages 復用 — 自己的快取鏈完整
- **Sub-agent（Haiku）**：Block3 無法復用（模型不同）、tools 無法復用（工具集不同）、messages 無法復用（獨立對話）— 每次幾乎從零開始

所以每啟動一個 sub-agent，基本等於一次「迷你冷啟動」。如果你在 CLAUDE.md 裡寫了「多用 agent 並行處理」，要意識到每個 agent 都有獨立的快取開銷。

---

## 六、Claude Code 快取最佳實踐

理解了架構和機制，下面是實戰操作指南。

### 核心原則：別碰前綴，只在末尾追加

**保護快取的（綠燈）：**

- **連續對話** — 前綴不變，增量快取，一個 session 持續對話
- **btw** — 使用 btw 共享 session，可共享快取
- **CLAUDE.md** — 定期整理這個檔案，但不要在工作到一半的時候整理

**破壞快取的（紅燈）：**

- **開新 session** — 冷快取，~20K tokens 全價重算
- **改 CLAUDE.md** — Block 4 起全部失效，配好就別動
- **加減 MCP 工具** — 工具 schema 變化 = 快取斷裂，session 前配好，停用不用的 MCP
- **切換模型** — 完全失效，按階段切，別頻繁切
- **/compact** — 訊息歷史變了 = 斷裂，對話 >100K 時再用
- **發呆超過 TTL** — 快取過期，Pro/Max 用戶 1h 內說句話

### 快取差異量化

假設系統提示詞 20K tokens，對話 10 輪：

- **一個 session 持續對話**：1 次全價 + 9 次 1/10 = **1.9 份**
- **每次開新 session**：10 次全價 = **10 份**

**差了 5 倍。** 對 Pro/Max 訂閱用戶，這意味著同樣的套餐能多幹 3-5 倍的活。

### 切換模型的隱藏成本

切換模型是完全失效——Opus 和 Sonnet 的權重不同，KV 張量不能互用。切一次模型，50K tokens 的上下文要全價重算。在 TTL 內切回可能還能命中舊快取（`promptCacheBreakDetection.ts` 追蹤了 `modelChanged`）。

**建議：下班前的最後半小時，不要切模型。** 按階段切，不要頻繁切。

---

## 七、進階技巧：Cache Keep-Alive 續命

Pro/Max 用戶的 TTL 是 1 小時。午飯吃 1.5 小時回來，快取就過期了；開個冗長的會議，快取就過期了。

**原理：** 快取 TTL 在每次讀取時刷新。只要在過期前發一次匹配前綴的請求，快取就能無限續命。

**方案設想：** 用 tmux 或 iTerm2 AppleScript，每 55 分鐘往 Claude Code 終端自動發一條 prompt：

```
我斷線了嗎？如果沒斷你只要簡單說 ok。
```

會消耗一些 tokens 嗎？會。但比冷啟動 20K tokens 全價重算便宜多了——用 1 個 token 的輸出，換回 20K tokens 的快取優勢。

這裡要說明一下，Anthropic 有濫用偵測機制，自動續命如果做得太機械（精準 60 秒一次、完全無操作），理論上有被標記風險。55 分鐘人工點一次應該沒問題——關鍵在「合理使用」。不建議搞全自動。

---

## 八、與之前文章的架構串聯

這篇文章的快取機制，和之前寫的 Claude Code 系列是一個完整的架構拼圖：

| 文章 | 架構層 | 解決什麼問題 |
|------|--------|-------------|
| [System Prompt 源碼分析](https://ai-coding.wiselychen.com/claude-code-system-prompt-source-code-analysis/) | 上下文層 | Prompt 怎麼組裝、DYNAMIC_BOUNDARY 怎麼切分 |
| [資安最佳實踐](https://ai-coding.wiselychen.com/claude-code-security-best-practices-source-code-verified/) | 控制層 | 權限、沙箱、Hook 治理 |
| [四層壓縮機制](https://ai-coding.wiselychen.com/claude-code-context-engineering-four-layer-compression/) | 上下文層 | 上下文太長怎麼辦 |
| **本篇：快取機制** | **快取層** | **重複計算怎麼省** |

在之前的架構、治理與工程實踐裡，我把 Claude Code 拆成六層：上下文層、控制層、工具層、執行層、快取層、驗證層。今天這篇就是把快取層單獨拉出來，從底層的 KV 快取原理，到 Anthropic 的工程實現，到你每天用 Claude Code 時該養成的習慣，完整走了一遍。

---

## 結語

快取不是黑魔法，是經濟學問題：

- **KV 快取**：用記憶體換算力，歷史 token 算過就不重算
- **前綴匹配**：用結構換靈活性，前綴固定才能復用
- **TTL 管理**：用紀律換省錢，保持對話連續性就是在省錢

從 Gemma 4 本地實驗的 100x 加速，到 Claude Code 原始碼裡 `DYNAMIC_BOUNDARY` 的精妙設計——明白原理後，你不需要任何外掛或工具。只需要幾個好習慣——保持 session 連續、不亂改 CLAUDE.md、不隨手開新視窗——就能讓你的 Claude Code 套餐多跑 3-5 倍。

---

## 參考資料

**論文：**

- In Gim, Guojun Chen, Seung-seob Lee, Nikhil Sarda, Anurag Khandelwal, Lin Zhong. [Prompt Cache: Modular Attention Reuse for Low-Latency Inference](https://arxiv.org/abs/2311.04934). MLSys 2024.

**系列文章：**

- [Claude Code 51 萬行原始碼外洩拆解](https://ai-coding.wiselychen.com/claude-code-source-leak-memory-architecture-lessons/)
- [拆解 Claude Code 的 System Prompt 源碼](https://ai-coding.wiselychen.com/claude-code-system-prompt-source-code-analysis/)（EP1）
- [Claude Code 資安最佳實踐：14 條建議](https://ai-coding.wiselychen.com/claude-code-security-best-practices-source-code-verified/)（EP2）
- [Claude Code 上下文工程：四層壓縮機制](https://ai-coding.wiselychen.com/claude-code-context-engineering-four-layer-compression/)（EP3）
- [Anthropic 官方解密：Dual-Agent 架構](https://ai-coding.wiselychen.com/anthropic-dual-agent-architecture-claude-code/)
