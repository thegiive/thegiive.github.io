---
layout: post
title: "本地模型的 Tool Calling 到底行不行？ToolCall-15 基準測試揭示的殘酷真相"
date: 2026-03-29 10:00:00 +0800
permalink: /toolcall-15-local-llm-tool-calling-qwen-27b-sweet-spot/
image: /assets/images/toolcall-15-qwen35-family-results.png
description: "stevibe 用 15 個場景、12 個工具測了 Qwen 3.5 全系列的 Tool Calling 能力。結果：全部通過的只有 27B dense 和它的蒸餾版。397B 失敗 2 個、122B 失敗 1 個。小模型幻覺數據，大模型忽略數據，只有 27B 把數據正確串了起來。"
---

## 一個很簡單的問題，答案卻很複雜

「本地跑的 LLM，能不能可靠地呼叫工具？」

這個問題我從去年寫[企業地端 LLM 架構](/local-llm-enterprise-architecture/)的時候就一直在想。因為 Tool Calling 是 AI Agent 的命脈——模型如果不能穩定地選對工具、傳對參數、串接多步結果，那它再會聊天也只是個聊天機器人。

上週 X 上一位叫 stevibe 的開發者發了一串測試結果，直接給了一個我沒想到的答案：

> **小模型幻覺數據。大模型忽略數據。只有 27B 把數據正確地串了起來。**

他做的測試叫 [ToolCall-15](https://github.com/stevibe/ToolCall-15)——15 個場景、12 個工具、Temperature 0、模擬回應、不挑最好的那次。測了 Qwen 3.5 全系列，從 0.8B 到 397B。

結果讓人意外：**全部通過的只有兩個模型——27B dense 和它的蒸餾版。** 不是最大的那個。

![ToolCall-15 Qwen 3.5 全系列測試結果：只有 27B 和蒸餾版全綠](/assets/images/toolcall-15-qwen35-family-results.png)

---

## ToolCall-15 在測什麼？

在講結果之前，先看方法論。因為一個 benchmark 如果方法有問題，結果再好看也沒意義。

stevibe 把 tool calling 拆成五個維度，每個維度三個場景：

| 類別 | 在測什麼 | 範例 |
|------|---------|------|
| **Tool Selection** | 能不能選對工具 | 該用搜尋不要用計算機 |
| **Parameter Precision** | 參數有沒有傳對 | 日期格式、ID 精確度 |
| **Multi-Step Chains** | 多步串接 | 搜尋 → 取得結果 → 用結果計算 |
| **Restraint and Refusal** | 該不用工具時不亂用 | 用戶只是閒聊，不要硬呼叫 API |
| **Error Recovery** | 工具報錯後怎麼辦 | API 回傳 404，能不能優雅處理 |

評分很直覺：Pass 得 2 分、Partial 得 1 分、Fail 得 0 分。每類滿分 6 分，最終分數是五類百分比的平均。

幾個設計上的關鍵選擇：

1. **Temperature 設 0。** 消除隨機性，保證結果可重現。stevibe 說他跑了好幾次 27B，結果一樣。
2. **工具回應是模擬的。** 不是真的打 API，而是給固定的模擬回傳值。這樣可以隔離「模型能力」和「網路 / API 狀態」。
3. **12 個通用工具集。** 包含搜尋、計算、日曆、天氣等常見 function，統一測試環境。
4. **開源可重跑。** TypeScript + Next.js，支援 Ollama / llama.cpp / MLX / LM Studio / OpenRouter。任何人都能在自己的機器上驗證。

**限制也很明確：** 15 個場景是小樣本，不能取代 BFCL 那種幾百個案例的學術基準。但 stevibe 的定位很清楚——這是給「需要知道哪個模型能不能跑 4 步 tool chain 而不幻覺一個 file ID」的實踐者用的。

---

## 結果：27B 的意外勝出

stevibe 測了 Qwen 3.5 全系列。推文裡最核心的發現：

**全部通過（All Green）：**
- Qwen 3.5-27B（dense）
- Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled（Jackrong 蒸餾版）

**有失敗的：**
- Qwen 3.5-397B：失敗 2 個
- Qwen 3.5-122B：失敗 1 個
- Qwen 3.5-35B：失敗 2 個

**小模型（0.8B-9B）：** 多數在 multi-step 場景超時——卡在重複呼叫同一個 tool call 的迴圈裡，直到 30 秒限制。

### 最有啟發性的失敗案例

> 「搜尋冰島的人口，然後計算 2%。」

這個任務分兩步：先搜尋取得數據，再用數據做計算。

**35B、122B、397B 都失敗了。** 原因不是不會搜尋，也不是不會算——而是它們用了「記憶中的數字」來計算，而不是用搜尋工具回傳的數字。

工具回傳了一個精確數字，但大模型覺得自己知道冰島人口是多少，直接用了一個取整後的近似值。

**小模型呢？** 它們連搜尋結果都會幻覺出一個不存在的數字。

只有 27B 做了正確的事：搜尋 → 拿到結果 → 把結果傳進計算工具 → 回傳答案。

stevibe 的總結很精準：
> "Small models hallucinate data. Big models ignore data. The 27B just threaded it through."

---

## 為什麼 27B 打贏比它大 15 倍的模型？

這個結果看起來反直覺，但其實有技術上的解釋。

### Dense vs MoE：推理密度的差異

Qwen 3.5 的中大型模型用的是 MoE（Mixture-of-Experts）架構：

| 模型 | 總參數 | 每 token 活躍參數 | 架構 |
|------|--------|------------------|------|
| 397B-A17B | 397B | ~17B | MoE |
| 122B-A10B | 122B | ~10B | MoE |
| 35B-A3B | 35B | ~3B | MoE |
| **27B** | **27B** | **27B** | **Dense** |

看到了嗎？**27B 是唯一的 dense 模型。每一個 token 都經過全部 27B 參數的計算。**

而 397B 雖然總參數是 27B 的 15 倍，但每個 token 只激活 17B 的參數。122B 每 token 只用 10B。35B 每 token 只用 3B。

Tool calling 的核心是什麼？**深度推理鏈。** 你需要模型：
1. 理解用戶意圖
2. 選對工具
3. 構造正確的參數
4. 解讀工具回傳結果
5. 決定下一步是再調一次工具還是回答用戶

每一步都需要「思考」。而思考的品質取決於「每 token 投入了多少計算量」。27B dense 每個 token 投入的計算量，比 397B MoE 只少了 37%（17B vs 27B），但比 35B MoE 多了 9 倍（3B vs 27B）。

**MoE 的設計哲學是「用更少的計算處理更多的 token」——吞吐量優先。Dense 的哲學是「每個 token 都給你最深的思考」——推理深度優先。**

在 tool calling 這種需要精確、串接、判斷的場景，推理深度比吞吐量重要。

### 官方 BFCL-V4 分數的矛盾

有趣的是，Qwen 官方的 BFCL-V4 基準測試結果看起來不一樣：

| 模型 | BFCL-V4 |
|------|---------|
| 397B-A17B | 72.9 |
| 122B-A10B | 72.2 |
| **27B** | **68.5** |
| 35B-A3B | 67.3 |

在 BFCL-V4 上，397B 和 122B 都比 27B 高。那為什麼 ToolCall-15 的結果相反？

我的猜測：**BFCL-V4 側重單步 function calling 的準確性，而 ToolCall-15 測的是多步串接的可靠性。** 大模型在單步上可能更準，但在多步串接時「自以為知道答案」的傾向更強——因為它們的知識庫更豐富，反而更容易忽略工具回傳的數據。

這揭示了一個更深層的問題：**現有的學術基準可能低估了多步 tool calling 的難度。**

---

## Ollama 的冤案：很多「模型不行」其實是框架問題

在討論結果之前，必須提一個關鍵背景。

Ollama 之前有一個 bug（[GitHub issue #14493](https://github.com/ollama/ollama/issues/14493)）：**它把 Qwen 3.5 的 tool call 路由到了錯誤的解析管線。** Qwen 3.5 用的是 Qwen3-Coder 的 XML 格式（`<tool_call>...</tool_call>`），但 Ollama 用了 Hermes 風格的 JSON 解析器去處理它。

結果就是 tool calling「完全無法運作」。模型正確地輸出了 XML 格式的 tool call，但 Ollama 解析不了，所以回傳的是空結果或錯誤。

這個 bug 在 v0.17.3 部分修復，v0.17.6 完全修復。

**這意味著：2026 年 3 月中旬之前，所有用 Ollama 跑 Qwen 3.5 tool calling 的測試結果，都可能是「冤案」。** 模型本身沒問題，是框架把它的輸出搞壞了。

如果你之前測過 Qwen 3.5 的 tool calling 覺得很爛，先確認你的 Ollama 版本。升級到 v0.17.6+ 可能會完全不同。

---

## Jackrong 蒸餾版：把 Claude Opus 的推理能力壓進 16.5 GB

ToolCall-15 全綠的另一個模型是 [Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled](https://huggingface.co/Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled)。這個名字很長，但值得認識它。

做法是：用 ~3,950 筆從 Claude 4.6 Opus 推理軌跡過濾出來的資料，透過 LoRA 微調 Qwen 3.5-27B。訓練策略是 `train_on_responses_only`——只學輸出，不學 prompt。

結果：
- 原生支援 `developer` role（避免 Jinja 模板崩潰）
- 延長思考模式可以持續 9 分鐘以上不中斷
- 簡單問題不會過度推理
- **Tool calling 穩定性提升**

硬體需求：Q4_K_M 量化約 16.5 GB VRAM，RTX 3090 上 29-35 tok/s。

**月下載量 253K，1,520 個 likes。** 社群用腳投票了。

X 上的 Matthew Berman 還特別問了蒸餾版的表現。另一位用戶 Gian Domiziani 回報他們用 27B 跑了 32 個工具的 agemem 系統（包含自動記憶管理），結果「fantastic on func tools」。

不過要注意：這是 PREVIEW BUILD，用的是社群公開的資料集蒸餾，不是直接從 Claude API 蒸餾。品質可能不穩定。

---

## 其他第三方驗證：不只 stevibe 一個人這麼說

### J.D. Hodges — 13 個本地模型測試

J.D. Hodges 用 40 個測試案例、8 個 tool schemas 測了 13 個本地模型。結果：

| 排名 | 模型 | 大小 | 通過率 |
|------|------|------|--------|
| 1 | Qwen3.5 4B | 3.4 GB | 97.5% |
| 2 | GLM-4.7-Flash | 18 GB | 95.0% |
| 2 | Nemotron Nano 4B | 4.2 GB | 95.0% |
| 4 | Mistral Nemo 12B | 7.5 GB | 92.5% |
| 5 | Qwen3 8B | 5 GB | 85.0% |

他的結論：**「模型大小和 tool calling 能力之間沒有相關性。」**

注意：他沒有測 27B。但他的 4B 拿第一的結果，和 stevibe 的 「小模型超時」結果有矛盾。可能的原因：Hodges 的測試以單步 tool call 為主，沒有 stevibe 那種多步串接的場景。

### Docker Blog — 實用評估

Docker 的官方部落格也做了本地 LLM tool calling 測試：
- Qwen 3 14B：F1 0.971，接近 GPT-4
- Qwen 3 8B：F1 0.933，延遲減半

**共識是：Qwen 系列在 tool calling 上確實領先其他開源模型。** 分歧在於「哪個尺寸最好」取決於你測什麼——單步還是多步。

---

## 這對企業本地 AI Agent 部署意味著什麼？

把這些拼圖拼起來，幾個實際的建議：

### 1. 如果你的 Agent 只做單步 tool call → 小模型就夠了

搜尋一個東西、查一個 API、填一個表單——這些不需要 27B。4B 到 9B 就夠了，而且速度更快、記憶體更省。

### 2. 如果你的 Agent 需要多步串接 → 27B 是目前的最低甜蜜點

搜尋 → 讀取結果 → 基於結果做判斷 → 再調另一個工具——這種場景，27B dense 的表現目前無可取代。比它大的 MoE 模型反而更容易忽略工具回傳的數據。

### 3. 別用 MoE 跑 Agent 工作流（至少目前）

MoE 的設計目標是吞吐量，不是推理深度。在需要「每一步都精確」的 agent 場景，dense 模型是更好的選擇。這和「用 MoE 做大規模文本處理」不矛盾——場景不同，選擇不同。

### 4. 先確認你的推理框架沒問題

Ollama 的 Qwen 3.5 tool calling bug 是一個警示。在下結論說「某個模型 tool calling 不行」之前，先確認：
- Ollama 版本 ≥ v0.17.6
- llama.cpp build ≥ b8239
- 解析器配置正確（Qwen3-Coder XML 格式，不是 Hermes JSON）

### 5. 模型路由策略需要加上「tool calling 能力」這個維度

我之前寫的[模型路由策略](/openclaw-cost-optimization-guide-97-percent-reduction/)只考慮了成本和品質。現在需要加第三個維度：tool calling 可靠性。不是所有任務都需要工具，但需要工具的任務，你必須用有能力的模型。

---

## 坦白說

ToolCall-15 是一個 15 場景的小基準。它不能取代 BFCL 的幾百個案例，也不能宣稱「27B 就是最好的 tool calling 模型」。但它做對了一件很重要的事：**它測了多步串接。**

學術基準傾向測單步的精確度——「給你一個意圖，你能不能生成正確的 function call？」但真實的 Agent 工作流不是一步的。它是一連串的搜尋、判斷、調用、驗證。而在這個鏈條上，中間任何一環出問題，整個結果就錯了。

ToolCall-15 揭示了一個被學術基準遺漏的現象：**大模型在多步串接中傾向用自己的知識取代工具回傳的數據。** 這不是「模型太笨」，而是「模型太自信」。

對企業來說，這個發現的意義比 benchmark 分數更大。因為它意味著：**你不能只看單一指標就決定用哪個模型。你需要用你的實際工作流去測。**

stevibe 把 ToolCall-15 開源了。158 顆星、MIT License、跑在 localhost:3000。如果你在做本地 Agent 部署，花 30 分鐘跑一次你在考慮的模型。這比看任何 leaderboard 都有用。

---

## 關鍵洞察

1. **Qwen 3.5-27B dense 是目前本地 tool calling 的最佳選擇，因為它是唯一在多步串接上全部通過的模型。** 這不是因為 27B「最聰明」，而是因為 dense 架構的推理密度在 agent 場景有結構性優勢。

2. **「大模型忽略工具數據」是一個真實且被低估的問題。** 397B 和 122B 不是不會用工具，是它們太自信。這在企業場景裡比小模型的幻覺更危險——因為輸出看起來很合理，但數據是錯的。

3. **現有學術基準（BFCL-V4）可能低估了多步 tool calling 的難度。** 在 BFCL-V4 上 397B 得分最高，但在多步串接測試中失敗了。如果你的 Agent 需要串接工具，不要只看 BFCL 分數。

4. **推理框架的 bug 可以完全掩蓋模型的真實能力。** Ollama 的 Qwen 3.5 解析器問題讓 tool calling 看起來完全失敗，但問題不在模型。升級到 v0.17.6+ 可能改變你對整個模型系列的評價。

5. **蒸餾版 27B 證明「小模型 + 好數據 = 穩定的 agent 能力」。** Jackrong 用 3,950 筆資料就讓 27B 的 tool calling 變得更穩定。這暗示未來的方向不是「用更大的模型」，而是「用更好的訓練數據微調中型模型」。

---

## 延伸閱讀

- [越級打怪的「神級小模型」：帶你認識 Qwen 3.5 與爆紅的 9B 架構](/qwen-3-5-9b-small-model-god-tier-architecture/) — 9B 的架構創新，但 tool calling 是它的天花板
- [On-Premise Enterprise LLM Deployment：企業級地端 LLM 架構完整藍圖](/local-llm-enterprise-architecture/) — 本地部署的完整架構，現在多了 tool calling 選型的考量
- [AI Agent Security 遊戲規則已經改變](/ai-agent-security-you-xi-gui-ze-yi-jing-gai-bian/) — Agent 的 tool calling 能力越強，安全邊界的設計越重要
- [把 LLM 直接燒進晶片：Taalas 的瘋狂賭注](/taalas-asic-burn-llm-into-silicon-local-inference-future/) — 如果推理成本歸零，27B 本地部署的經濟模型更有吸引力
