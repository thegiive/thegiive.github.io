---
layout: post
title: "NUS 訓練出一顆「專門寫 Harness」的模型：JIT-Agent 讓 DeepSeek-V4-Flash 在 DeepSearchQA 贏 GPT-5.6 九個百分點，token 成本砍半"
date: 2026-09-01 09:00:00 +0800
permalink: /jit-agent-harness-intelligence-trainable-scaling/
categories: [AI 產業分析]
image: /assets/images/jit-agent-harness-intelligence-cover.png
description: "NUS LV-Lab 的 JIT-Agent 論文把 Harness Engineering 從手藝推向科學：訓練一顆 27B 模型專門「替別的模型寫 harness」，用四模組協議（Memory / Planning / Capability Orchestration / Action）即時合成任務自適應的 agent scaffold。結果：DeepSeek-V4-Flash 套上 JIT-Agent 生成的 harness，DeepSearchQA 85.1 贏 GPT-5.6 的 76.0（+9.1）；GLM-5.2 最高漲 20.2 分；九項 benchmark 平均，JIT-Agent 和 Claude Code、OpenCode 這類手工打造的成熟 harness 打成平手，但 token 量少 50%、成本少 36%。這是第一次有人把「寫 harness 的能力」當成一個獨立的 scaling 維度來訓練，而且證明它和模型 scaling 正交——你不需要換更大的模型，換更好的 harness 就夠了。"
author: Wisely Chen
faq:
  - question: "JIT-Agent 本身需要多大的算力？"
    answer: "基底是 Qwen3.6-27B，推理時需要一張 A100 或同等級的 GPU。生成一套 harness 的時間論文沒有明確報告，但從 token 量推測應該在幾十秒到幾分鐘之間。相比人類手調 harness 動輒幾小時甚至幾天，這是數量級的加速。"
  - question: "我能用 JIT-Agent 替 Claude Code 生成更好的 harness 嗎？"
    answer: "理論上可以，但實務上意義不大。Claude Code 的 harness 是深度整合在 runtime 裡的，你沒辦法輕易替換它的 memory 管理或 tool filtering 邏輯。JIT-Agent 更適合的場景是：你用 API 直接呼叫一顆 LLM，需要自己搭 agent scaffold。"
  - question: "和 Agents-A1 那篇「35B 打贏 1T」有什麼不同？"
    answer: "Agents-A1 是把 scaling 的軸從參數換成 training horizon——用更長的軌跡資料訓練一顆更小的模型。JIT-Agent 是把 scaling 的軸換成 harness——不改模型本身，改模型外面的 scaffold。兩篇論文攻擊的是同一個問題（agent 能力不只來自模型大小），但從不同的角度切入。"
---

我們在這個 blog 上講 Harness Engineering 講了半年。從[三次中心遷移](/agent-harness-three-migrations-mechanism/)、到[同一顆 Kimi K3 換 harness 差 10 個百分點](/local-first-model-needs-local-first-harness/)、到 [GPT-5.6 Sol 改兩個設定 ARC-AGI-3 從 13% 跳到 38%](/arc-agi-3-harness-retained-reasoning-compaction/)——結論一直是同一句話：agent 的能力天花板，不在模型，在 harness。

現在 NUS 的 LV-Lab 把這句話做成了一篇[論文](https://arxiv.org/abs/2608.25593)，而且做到了一件我們沒做到的事：**把「寫 harness 的能力」本身訓練成一顆模型**。

不是人類手寫 CLAUDE.md，不是人類設計 skill，是一顆 27B 的模型，看到任務描述之後，即時合成一套完整的 agent harness——memory 怎麼管、planning 怎麼拆、工具怎麼選、action loop 怎麼跑——然後套到任何一顆現成的 LLM 上，讓它變強。

結果有多誇張？DeepSeek-V4-Flash 加了 JIT-Agent 生成的 harness，在 DeepSearchQA 拿 85.1 分。同一個 benchmark，GPT-5.6 只有 76.0。**便宜模型 + 自動生成的 harness，贏了貴模型九個百分點。**

---

## 30 秒定位

| 項目 | 內容 |
|------|------|
| 論文 | [JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution](https://arxiv.org/abs/2608.25593) |
| 機構 | NUS Learning and Vision Lab（LV-Lab） |
| 日期 | 2026-08-26 |
| 核心主張 | Harness intelligence 是一個可訓練、可遷移、與模型 scaling 正交的 agent 能力維度 |
| 方法 | 訓練一顆 27B 模型（基於 Qwen3.6）專門即時生成 task-adaptive harness |
| 關鍵數字 | DeepSeek-V4-Flash + JIT：DeepSearchQA 85.1（GPT-5.6 = 76.0）；GLM-5.2 最高 +20.2 分；成本 -36% |
| 開源 | [GitHub](https://github.com/bingreeky/JIT) ・ [Hugging Face](https://huggingface.co/JIT-Agent) |

---

## 一、為什麼 Harness 值得被「訓練」

我們現在寫 harness 的方式，本質上是手藝活。你寫一份 CLAUDE.md，設計幾個 skill，調幾輪 prompt，跑一下看效果，再調。這套做法在個人專案上沒問題，但它有三個根本瓶頸：

1. **不可遷移**：你替專案 A 寫的 harness，搬到專案 B 幾乎一定要重寫。任務不同、模型不同、工具集不同，harness 的最佳配置就不同。
2. **不可擴展**：一個工程師一天能調幾套 harness？10 套？100 套？每套都需要人類理解任務、選策略、測效果。
3. **不會自我改進**：你今天寫出來的 harness，不會因為跑了一千次任務就自動變好。你得自己回來看 log、改設定、再跑。

JIT-Agent 的貢獻，就是把這三個瓶頸同時打破：一顆模型負責生成 harness，看到新任務就即時合成，跑完之後把結果蒸餾回自己的 archive，下次碰到類似任務就更好。

---

## 二、四模組協議：h = (M, P, A, F)

論文做的第一件事不是訓練模型，是**定義 harness 到底長什麼樣**。

這件事聽起來理所當然，但在我們實務上其實很混亂。你打開不同公司的 agent framework，有的把 memory 和 planning 混在一起，有的根本沒有 tool orchestration，有的把所有東西塞進一個 system prompt。沒有統一的結構，就沒辦法機器生成。

JIT-Agent 把 harness 拆成四個模組，有固定的依賴順序：

**M → P → F → A**

| 模組 | 職責 | 對應到我們的實務 |
|------|------|----------------|
| **M（Memory）** | 管理歷史事件和可變狀態，產出壓縮後的「視野」 | CLAUDE.md 裡的 context 管理規則、memory system |
| **P（Planning）** | 從任務描述 + 狀態 + memory 視野，產出局部指令和子目標 | Task decomposition、plan mode |
| **F（Capability Orchestration）** | 根據當前指令和狀態，從工具註冊表中篩選暴露哪些工具 | Skill 設計、tool filtering |
| **A（Action）** | 執行控制迴圈，發出 tool call 或終端輸出，更新狀態 | Agent 的主迴圈本身 |

這個分法的精妙在於：**每個模組都是可替換的零件**。研究型深度搜尋任務可能需要遞迴分解的 P 模組；文件處理任務可能需要 DAG 式的 P 模組；有的簡單任務根本不需要 P（設成 null）。但不管怎麼換，四個插槽的介面是固定的。

這就讓機器生成成為可能：JIT-Agent 不需要從零寫一整套 agent framework，它只需要替四個插槽各選一個實作，組裝起來就是一個完整的 harness。

---

## 三、訓練三階段：模仿、修復、進化

JIT-Agent 的基底是 Qwen3.6-27B，訓練分三個階段，每個階段解決一個不同的問題。

### 階段一：Customization（學會寫 harness）

用一個凍結的強 teacher 模型產出大量 protocol-compliant 的 harness，JIT-Agent 做 SFT 學會模仿。再用 DPO 從 harness pairs 裡學偏好——不是只看 reward 高低，而是同時衡量效能、延遲、成本的多目標優勢。

初始種子庫只有 13 套人寫的 harness。每次生成時，從種子庫挑 3 套任務類型匹配的作為參考上下文。

### 階段二：Repair（學會修壞掉的 harness）

第一階段生成的 harness 有一定比例會壞——編譯錯誤、介面不匹配、runtime 失敗。傳統做法是丟掉這些失敗案例。JIT-Agent 反過來，把失敗案例**加上錯誤診斷**當成訓練資料，讓模型學會在兩輪之內修好一個壞掉的 harness。

這一步非常實用。我們自己寫 harness 也常碰到「設計看起來對，跑起來爆」的情況。差別是人類得自己 debug，JIT-Agent 把 debug 能力內建了。

### 階段三：Evolution（自我進化）

這是最有意思的部分。JIT-Agent 維護一個**持續擴張的 harness archive**（從 13 套種子起步）：

1. 新任務進來，從 archive 檢索匹配的參考 harness
2. 用當前策略取樣 G 個候選 harness
3. 全部跑一遍，量 reward / latency / cost
4. 和 archive 裡的最佳 incumbent 比較
5. PPO 更新策略
6. **進 archive 的門檻**：效能不低於前沿線，且至少有一個效率軸（延遲或成本）嚴格改善

這個進化迴路發生在**訓練階段**——Evo-GDPO 是一個 online RL loop，需要取樣、執行、算 reward、更新權重。部署之後，JIT-Agent 用的是訓練時累積好的 archive 和學到的策略來生成 harness，不是「用了就自動變好」的 runtime 機制。但訓練時的 archive 越大越多樣，推理時能參考的範本就越豐富。

---

## 四、數據帳本：便宜模型贏貴模型的九個 benchmark

### 九項 benchmark 平均

| 配置 | 九項平均 | 和原模型的差距 |
|------|---------|---------------|
| GLM-5.2 alone | 74.1 | — |
| **JIT + GLM-5.2** | **81.8** | **+7.7** |
| DeepSeek-V4-Flash alone | 66.7 | — |
| **JIT + DeepSeek-V4-Flash** | **75.5** | **+8.8** |
| GPT-5.6（估算） | ~76.5 | — |

### JIT + DeepSeek-V4-Flash 超越 GPT-5.6 的項目

| Benchmark | JIT + DSV4-Flash | GPT-5.6 | 差距 |
|-----------|-----------------|---------|------|
| DeepSearchQA | **85.1** | 76.0 | +9.1 |
| PinchBench | **92.9** | 84.2 | +8.7 |
| OdysseyBench | **73.0** | 68.7 | +4.3 |

最大單項漲幅：DeepSeek-V4-Flash 在 DeepPlanning-Shopping 從 59.1 跳到 **83.9**（+24.8）。

### 和 Claude Code / OpenCode 的正面比較

以 DeepSeek-V4-Flash 為 backbone：

| Benchmark | Claude Code | OpenCode | JIT-Agent |
|-----------|-----------|----------|-----------|
| DeepSearchQA | 79.6 | 75.9 | **85.1** |
| xBench-DS | 75.0 | 65.0 | **82.0** |
| AgentIF | **66.9** | 48.1 | 63.8 |
| DSQA token 量 | 625K | 1,832K | **400K** |
| DSQA 成本 | $0.088 | $0.258 | **$0.066** |

**模式很清楚**：JIT-Agent 在搜尋和研究類任務上大幅領先，token 量砍半、成本降三成以上。但在開放性工作任務（AgentIF）上，Claude Code 仍然領先——差 3.1 分不大，但方向一致。

這正好驗證了我們的判斷：Claude Code 的 harness 是手工打造的、針對通用軟體開發場景深度優化的產品。在它的主場（開放性任務、需要大量 judgement call 的場景），自動生成的 harness 還追不上。但在結構化程度更高的任務上，機器生成的 harness 已經贏了。

---

## 五、這篇論文和我們講了半年的 Harness Engineering 是什麼關係

先講相同的地方。

論文的核心公式 **h = (M, P, A, F)** 和我們實務上做的事是高度對齊的：

- **M（Memory）**→ 我們寫 CLAUDE.md 的 context 管理段落、設計 memory system、控制哪些歷史進 context
- **P（Planning）**→ 我們用 plan mode、TaskCreate 做任務拆解
- **F（Capability Orchestration）**→ 我們設計 skill、決定哪些工具在什麼場景下暴露
- **A（Action）**→ agent 的執行迴圈，我們通常不碰這層（由 Claude Code / Cursor 等 runtime 提供）

論文的貢獻在於：**把我們憑經驗做的事情，變成一個有明確介面定義、可以機器生成、可以自動優化的流程。**

再講不同的地方。

我們的 harness 是**持久的**——一份 CLAUDE.md 可能用幾個月，隨著專案演化慢慢調整。JIT-Agent 的 harness 是**即用即拋的**——每個任務生成一套新的，用完不保留（只把最好的存進 archive 供未來參考）。

這兩種模式不衝突，甚至互補。持久 harness 適合你熟悉的、反覆做的工作場景。即時 harness 適合你碰到新任務、新模型、新工具集的場景——你不想花三天手調 harness，丟給 JIT-Agent 兩分鐘生成一套，跑了再說。

---

## 六、一個容易忽略的訊號：哪種模型從 harness 得到最多

論文的消融結果有一個值得注意的模式：

**弱模型（或效率型模型）在絕對分數上受益更大。** DeepSeek-V4-Flash 平均漲 8.8 分，單項最高漲 24.8。原因不難理解——弱模型的能力缺口更大，一個好的 harness 可以補上缺口（比如規劃能力不夠，harness 裡的 P 模組替它做規劃）。

**強模型到達更高天花板。** GLM-5.2 本身已經 74.1 分，加了 JIT 還能推到 81.8，在 DeepSearchQA 打出 93.9。強模型的 baseline 能力已經很好，harness 的角色從「補缺口」變成「減浪費」——更精準的 tool filtering、更有效的 memory 壓縮，讓強模型少走冤枉路。

**對實務的啟示：** 你的模型選型不應該只看 benchmark 分數。一顆便宜模型 + 好 harness 可能比一顆貴模型 + 預設 harness 更值得。我們[之前講 Kimi K3](/local-first-model-needs-local-first-harness/) 的結論是一樣的，現在有了更大規模的數據支撐。

---

## 七、這篇沒解決什麼

誠實講幾個限制。

**1. AgentIF 的落差。** JIT-Agent 在開放性工作任務上還是輸 Claude Code。這類任務需要大量 judgement call——什麼時候該問使用者、什麼時候該回頭檢查、什麼時候該放棄一條路。這些決策邏輯很難從 archive 裡的歷史案例學到。Claude Code 的 harness 花了大量工程投入在這些邊角案例上。

**2. 四模組的邊界問題。** 把 harness 切成四塊是一個有用的抽象，但現實中模組之間的邊界沒有那麼清楚。Memory 的壓縮策略會影響 Planning 的品質；Tool filtering 的決策需要 Planning 的上下文。論文用固定的依賴順序 M→P→F→A 處理這個問題，但在真實場景裡，這些模組經常需要互相回饋。

**3. 沒有消融哪個模組貢獻最大。** 論文展示了不同任務產出不同的模組實作，但沒有做 M/P/F/A 各自的消融。我們不知道對一個具體任務來說，是 Memory 設計更重要還是 Planning 設計更重要。

**4. 進化的冷啟動。** Archive 從 13 套種子開始，對新領域的冷啟動效果如何，論文沒有深入討論。如果你的任務類型和種子庫差距太大，JIT-Agent 的第一次生成品質可能不好。

---

## 八、對我們的實務意味著什麼

**短期（現在就能做的事）**：把你的 harness 用 M/P/F/A 四模組的思路重新審視。你的 CLAUDE.md 有沒有清楚區分 memory 管理策略（M）、任務拆解邏輯（P）、工具選擇規則（F）？把它們分開寫，不只是整理，而是讓你看清哪一塊才是你目前的瓶頸。

**中期（等 JIT-Agent 開源跑起來之後）**：在 local-first 的場景下，JIT-Agent 可能是最有價值的。你用一顆 Qwen3.6-27B 跑 JIT-Agent 生成 harness，再套到另一顆地端模型上。兩顆 27B 加起來的成本，可能比一次 GPT-5.6 API call 還便宜。

**長期（Harness Engineering 的走向）**：這篇論文確認了 Harness Intelligence 是一個**獨立的 scaling 維度**。Model scaling（更大的模型）、Agent scaling（更長的 horizon）、Knowledge scaling（更好的知識庫），現在加上 Harness scaling（更好的 scaffold 生成）。四條軸各自獨立，意味著你不需要把預算全押在一條線上。

回頭看這半年的 blog，從[Harness Engineering 全景圖](/harness-engineering-architecture-overview/)到 [Pi 的 99.93% cache hit](/pi-cache-hit-99-93-context-compression-roadmap/)，我們一直在講同一件事：**不要只盯著模型，盯著 harness**。JIT-Agent 的貢獻是把這句口號變成了一個可量化、可訓練、可自動化的方向。

---

## 帳本

| 事實 / 數字 | 來源 | 驗證狀態 |
|------------|------|---------|
| JIT-Agent 基於 Qwen3.6-27B | arXiv 2608.25593 Section 4 | 論文原文 |
| 四模組協議 h = (M, P, A, F) | arXiv 2608.25593 Section 3 | 論文原文 |
| 種子 harness 13 套 | arXiv 2608.25593 Section 4.1 | 論文原文 |
| DeepSeek-V4-Flash + JIT：DeepSearchQA 85.1 vs GPT-5.6 76.0 | arXiv 2608.25593 Table 2 | 論文原文 |
| GLM-5.2 + JIT 最高漲幅 +20.2 | arXiv 2608.25593 Abstract | 論文原文 |
| 九項 benchmark 平均：JIT + DSV4-Flash 75.5 / JIT + GLM-5.2 81.8 | arXiv 2608.25593 Table 2 | 論文原文 |
| 和 Claude Code 比較：DSQA JIT 85.1 vs CC 79.6 | arXiv 2608.25593 Table 4 | 論文原文 |
| AgentIF：Claude Code 66.9 vs JIT 63.8 | arXiv 2608.25593 Table 4 | 論文原文 |
| token 量 JIT 400K vs CC 625K vs OpenCode 1,832K | arXiv 2608.25593 Table 4 | 論文原文 |
| 成本 JIT $0.066 vs CC $0.088 vs OpenCode $0.258 | arXiv 2608.25593 Table 4 | 論文原文 |
| DeepPlanning-Shopping 最大單項漲幅 +24.8 | arXiv 2608.25593 Table 2 | 論文原文 |
| 訓練三階段：Customization / Repair / Evolution | arXiv 2608.25593 Section 4 | 論文原文 |

---

## 常見問題 Q&A

**Q: JIT-Agent 本身需要多大的算力？**

基底是 Qwen3.6-27B，推理時需要一張 A100 或同等級的 GPU。生成一套 harness 的時間論文沒有明確報告，但從 token 量推測應該在幾十秒到幾分鐘之間。相比人類手調 harness 動輒幾小時甚至幾天，這是數量級的加速。

**Q: 我能用 JIT-Agent 替 Claude Code 生成更好的 harness 嗎？**

理論上可以，但實務上意義不大。Claude Code 的 harness 是深度整合在 runtime 裡的，你沒辦法輕易替換它的 memory 管理或 tool filtering 邏輯。JIT-Agent 更適合的場景是：你用 API 直接呼叫一顆 LLM，需要自己搭 agent scaffold。

**Q: 和 Agents-A1 那篇「35B 打贏 1T」有什麼不同？**

Agents-A1 是把 scaling 的軸從參數換成 training horizon——用更長的軌跡資料訓練一顆更小的模型。JIT-Agent 是把 scaling 的軸換成 harness——不改模型本身，改模型外面的 scaffold。兩篇論文攻擊的是同一個問題（agent 能力不只來自模型大小），但從不同的角度切入。
