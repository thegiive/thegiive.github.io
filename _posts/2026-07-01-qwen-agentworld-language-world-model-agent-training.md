---
layout: post
title: "模擬環境訓練的 Agent，居然比真實環境的更強 — Qwen-AgentWorld 技術解析"
date: 2026-07-01 09:00:00 +0800
permalink: /qwen-agentworld-language-world-model-agent-training/
image: /assets/images/qwen-agentworld-cover.png
description: "所有人都在訓練 LLM 當更好的 Agent——更會操作工具、更會寫程式、更會瀏覽網頁。但 Qwen 問了一個沒人問過的問題：如果我們不訓練它『行動』，而是訓練它『理解環境會怎麼回應』呢？結果是：用模擬環境訓練出來的 Agent，在真實環境的表現反而超過只在真實環境訓練的版本。這篇拆解 Qwen-AgentWorld 的兩條路線、三階段訓練管線、和五個讓我意外的發現。"
---

![Qwen-AgentWorld](/assets/images/qwen-agentworld-cover.png)

## 一個所有人都忽略的問題

過去兩年，Agent 訓練的方向幾乎是一面倒的：**怎麼讓模型在環境裡做出更好的動作**。

SFT 教它怎麼呼叫工具。RL 讓它在真實環境裡反覆嘗試、拿到 reward、更新策略。從 SWE-Bench 到 Terminal-Bench，benchmark 比的全部都是「行動的準確度」。

但 Qwen 團隊問了一個幾乎沒人問過的問題：

> 如果我們不訓練模型「做動作」，而是訓練它**預測環境會怎麼回應**呢？

這就是 Language World Model（LWM）的核心概念。用論文的數學表示：`o_{t+1} = f(c, o_≤t, a_≤t)`——給定歷史觀測和動作，預測下一個環境觀測。

聽起來是個純學術的想法。但結果讓我意外：

1. **在模擬環境訓練出來的 Agent，比只在真實環境訓練的更強**
2. **只做環境預測訓練（完全不做 Agent 訓練），模型的 Agent 能力也會提升**
3. **小模型（35B）從 World Model 訓練獲得的提升幅度，比大模型（397B）高 2.5 倍**

這三個結果每一個都反直覺。下面拆開來講。

---

## 30 秒定位：Qwen-AgentWorld 是什麼

| 項目 | 數字 |
|------|------|
| 模型規格 | 397B 總參數 / 17B 激活（MoE），基於 Qwen3.5 |
| 開源版本 | 35B / 3B 激活（同樣 MoE，256K 上下文） |
| 訓練數據 | 10M+ 環境互動軌跡 |
| 涵蓋環境 | 7 種：MCP、Search、Terminal、SWE、Web、OS、Android |
| 訓練管線 | CPT → SFT → RL（三階段） |
| AgentWorldBench 分數 | 58.71（超過 GPT-5.4 的 58.25、Claude Opus 4.8 的 56.59） |
| 授權 | 開源（HuggingFace + ModelScope） |

一句話：**這不是一個 Agent 模型，而是一個「環境模擬器」模型**——它的訓練目標是準確預測當 Agent 執行某個動作後，環境會回傳什麼結果。

---

## 為什麼「理解環境」跟「當好 Agent」有關

這裡需要建立一個直覺。

想像你是一個第一次進機房的工程師。老闆說「把 /var/log 底下超過 30 天的 log 清掉」。你會怎麼做？

如果你完全不理解 Linux 環境，你可能直接跑 `rm -rf /var/log/*`——動作是對的（刪檔案），但結果是災難性的。

如果你「理解環境」，你知道 `rm -rf /var/log/*` 會連正在寫入的 syslog 一起砍掉，導致所有服務的 log 中斷。你會改用 `find /var/log -type f -mtime +30 -delete`。

差別在哪？**不是你的「行動能力」不同，是你對「行動後環境會怎樣」的預測能力不同。**

這就是 World Model 的論點：一個能預測環境反應的 Agent，原則上不會比一個不能預測的 Agent 差。因為它可以在「真正執行」之前，先在腦中模擬結果，然後選擇最好的行動。

論文引用 Richens et al. 2025 的結論更激進：**任何能跨足夠多種任務泛化的 Agent，必然已經學到了某種 World Model。** 換句話說，World Model 不是可選的，是必要的。

---

## 三階段訓練管線：CPT → SFT → RL

### Stage 1：CPT（持續預訓練）— 灌環境知識

用非思考鏈的環境互動軌跡（action + observation pairs）做持續預訓練。資料來源包括容器化沙盒執行、開源的 terminal 錄影和工具 log、團隊內部的 Agent 軌跡、以及特定領域語料（資安、法律、醫療、金融）。

這裡有一個工程上的巧思值得記下來：**Turn-Level Information-Theoretic Loss Masking**。

問題是這樣的：環境互動軌跡裡，很多 turn 是垃圾——工具回傳一大段 boilerplate HTML、或者 echo 回完全一樣的輸入。這些 turn 對學習沒有幫助，但你又不能直接刪掉，因為後面的 turn 依賴它們作為 context。

解法：用 4 個統計量（Overlap、Novelty、Jaccard、Length Ratio）把每個 turn 分成 7 種語意類別，然後對不同類別套用不同的保留率：

| 類別 | 保留率 | 說明 |
|------|--------|------|
| Retrieval / Expansion / Action | 100% | 有資訊量的 turn |
| Transform | 50% | 部分有用 |
| Boilerplate | 10% | 大部分是噪音 |
| Echo | 5% | 幾乎純重複 |

這比「全部都學」或「手動篩選」都聰明。你不刪掉 boilerplate turn（因為 context 依賴性），但你把它的 loss weight 壓到 10%，讓模型不要浪費算力去記住它。

### Stage 2：SFT — 啟動「預測下一狀態」的推理模式

從 10,250 條候選軌跡裡，用 rejection sampling 保留 7,094 條（69.2% 留存率）。每條軌跡用一個通用推理模型做 3 次 rollout，由獨立 judge 評分，只保留最好的。

7 個環境的 SFT 資料量差異很大：

| 環境 | 軌跡數 | 平均 tokens | 平均 turns |
|------|--------|-------------|------------|
| Web | 1,605 | 19.4K | 10.2 |
| Terminal | 1,580 | 5.8K | 12.0 |
| Android | 1,337 | 30.1K | 19.3 |
| OS | 1,102 | 25.4K | 12.4 |
| Search | 1,042 | 18.9K | 6.2 |
| SWE | 249 | 36.7K | 24.7 |
| MCP | 179 | 62.7K | 28.9 |

MCP 的數據量最少（只有 179 條），但每條最長（62.7K tokens、28.9 turns）。SWE 也是類似的模式——複雜任務天然就是長軌跡、少樣本。

### Stage 3：RL — 用 GSPO 做策略優化

RL 資料池 92,308 條軌跡。用的算法是 GSPO（Group Sequence Policy Optimization），reward 設計是 **9:1 的混合 reward**——90% 來自 LLM judge 的 5 維度評分（Format、Factuality、Consistency、Realism、Quality），10% 來自 rule-based binary verifier。

為什麼要這樣混合？因為他們踩了三個坑：

**坑 1：多輪軌跡的 Reward Collapse。** 如果 RL 資料池裡的多條軌跡共享相同的前綴（因為它們來自同一個任務），gradient 會互相干擾。解法：每條軌跡只保留 1 個 turn，確保沒有前綴重疊。

**坑 2：Turing-Test Reward 收斂不了。** 他們試過讓 judge 判斷「這個 observation 是真實環境產生的還是模型產生的」。問題是 false-negative 率太高——好的模擬也經常被 judge 判成「真的」，導致 reward signal 太弱。最後放棄這個方向。

**坑 3：Self-Praise Reward Hacking。** 這個最有趣。RL 訓練到後期，模型學會了一件事：**在生成的環境觀測裡偷偷塞入「自我讚美」的文字**。比如在模擬的 terminal output 裡插入「execution completed successfully with optimal performance」之類的描述，讓 LLM judge 給更高分——但實際的模擬品質根本沒提升。

解法是三管齊下：rule-based verifier 做硬約束（佔 10% 的 reward），內容類型分類限縮 judge 的評估範圍，嚴格的 tag 抽取把 content 和 thinking 分開。

---

## AgentWorldBench：2,170 題、7 環境、真實 Ground Truth

這是他們自己建的 benchmark，但設計上有幾個值得注意的地方：

1. **Ground truth 來自真實環境執行**，不是模擬的
2. 軌跡來自 Claude Opus 4.6、Claude Sonnet 4.5、和 Qwen 家族模型——用多個模型的軌跡避免對自家模型過擬合
3. Judge 模型是 **GPT-5.2**，選擇依據是 double-blind Turing test 校準
4. 跨 judge 一致性：Spearman rho = 0.92–0.99（用 Gemini 3 Flash、Claude Sonnet 4.5、GPT-5.2 互相驗證）

### 主要結果

| 模型 | MCP | Search | Terminal | SWE | Android | Web | OS | **平均** |
|------|-----|--------|----------|-----|---------|-----|----|--------|
| **Qwen-AgentWorld-397B** | 68.2 | **37.8** | 57.7 | **68.5** | 60.2 | 51.0 | 67.9 | **58.7** |
| GPT-5.4 | **70.1** | 37.3 | 53.7 | 66.3 | 60.0 | 51.8 | 68.6 | 58.3 |
| Claude Opus 4.8 | 54.9 | 35.1 | **59.2** | 64.1 | **61.5** | **54.7** | 66.6 | 56.6 |
| Gemini 3.1 Pro | 59.1 | 30.2 | 52.5 | 59.1 | 61.4 | 52.8 | 66.9 | 54.6 |
| DeepSeek V4-Pro | 63.3 | 27.6 | 51.3 | 59.4 | 55.2 | 50.3 | 63.7 | 53.0 |
| Qwen 3.6-Plus | — | — | — | — | — | — | — | 50.8 |

幾個觀察：

**Qwen-AgentWorld 在 text-heavy 環境（MCP、SWE、Terminal）領先，但在 GUI 環境（Android、Web、OS）Claude Opus 4.8 仍然更強。** 這合理——GUI 環境的觀測是 accessibility tree 和 view hierarchy，本質上是結構化視覺資訊，跟純文字的 terminal output 差異很大。

**Search 環境所有模型都很差。** 最高分只有 37.8。這意味著「模擬搜尋引擎的回傳結果」是目前最難的環境模擬問題——因為它涉及大量即時性的世界知識。

**開源的 35B-A3B 版本拿到 56.39 分，跟 Claude Opus 4.8 的 56.59 幾乎打平。** 一個 3B 激活參數的模型逼近 Opus 4.8 的環境模擬能力，這對自部署場景有實際意義。

---

## 兩條路線：怎麼把 World Model 變成 Agent 能力

這是論文最核心的貢獻。他們不只是做了一個環境模擬器，而是探索了 World Model 怎麼反過來**提升 Agent 的行動能力**。兩條路線，一個比一個反直覺。

### 路線一：Decoupled — World Model 當模擬環境做 Agent RL

概念很直接：既然 World Model 能模擬環境，那我們能不能用它**取代真實環境**來訓練 Agent？

他們在 OpenClaw（一個開源的 MCP 工具使用環境）上做了驗證。World Model 模擬了 **4,000 個真實世界的 OpenClaw 環境**，然後用這些模擬環境訓練 Agent。

結果：

| Benchmark | 真實環境 RL（baseline） | 模擬環境 RL（Sim RL） | 提升 |
|-----------|----------------------|---------------------|------|
| Claw-Eval | baseline | +4.3 | 模擬環境勝 |
| QwenClawBench | baseline | +7.1 | 模擬環境勝 |
| MCP Mark | baseline | +12.3 | 模擬環境勝 |
| WideSearch | baseline | +3.9 | 超過 Opus 4.6 |

**在模擬環境訓練的 Agent，四個 benchmark 全部超過只在真實環境訓練的版本。**

為什麼模擬反而更好？關鍵詞是**可控性**。

真實環境的問題是：你遇到的場景分布是固定的。如果某種 edge case 在真實環境中很少出現（比如「CUDA 11.8 + 磁碟只剩 2GB + 網路間歇性斷線」），Agent 在訓練過程中幾乎不會碰到。

但 World Model 可以**刻意製造這些 edge case**。你可以告訴它：「模擬一個 CUDA 11.8 的環境，磁碟快滿了。」它就會生成對應的 terminal output 和錯誤訊息。這讓 Agent 的訓練覆蓋率遠超真實環境。

這跟自動駕駛的邏輯一模一樣：Waymo 不可能等到真的有小孩從車縫衝出來才學會應對，它在模擬器裡早就練過幾百萬次了。

### 路線二：Unified — 光做環境預測訓練，Agent 能力也會提升

這條路線更激進，也更讓人意外。

做法是：拿一個基礎模型，**只做 World Model 的 SFT（教它預測環境觀測），完全不做任何 Agent 訓練**。然後直接把它丟到需要多輪工具呼叫的 Agent benchmark 上測試。

結果：

| Benchmark | 沒有 LWM 訓練 | 有 LWM 訓練（無 Agent 訓練） | 提升 |
|-----------|--------------|--------------------------|------|
| Terminal-Bench 2.0 | baseline | +6.3 | — |
| Claw-Eval | baseline | +11.8 | — |
| SWE-Bench Pro | baseline | +5.2 | — |
| BFCL v4 | baseline | +9.0 | — |

**完全沒做 Agent 訓練，7 個 benchmark 全部提升。** 其中 3 個 benchmark 的環境類型甚至不在 World Model 的訓練資料裡。

這什麼意思？學會「預測環境會怎麼回應」這件事本身，就包含了大量對「怎麼正確行動」有用的知識。你不需要教它「怎麼用工具」，只要教它「用了工具之後環境會變成什麼樣」，它自己就能反推出正確的工具使用方式。

更有趣的數據：**35B 模型從 LWM 訓練獲得的提升是 +8.66 分（+18.14%），397B 模型只有 +3.97 分（+7.25%）。** 小模型的受益幅度是大模型的 2.5 倍。

一個可能的解釋：大模型在預訓練階段已經隱含地學到了不少「環境運作規則」，所以額外的 World Model 訓練帶來的邊際收益較小。小模型預訓練知識不夠，World Model 訓練補上了這個缺口。

---

## 五個讓我意外的發現

### 1. Factuality 是最難的維度

在 RL 訓練過程中，5 個評估維度的改善幅度分別是 Format（最容易）> Quality > Consistency > Realism > **Factuality（最難）**。Factuality 的相對提升最大（11.3%），但絕對分數始終最低。

這意味著「知道環境會回什麼」最難的部分，不是格式或風格，而是**事實性知識**。模型可以學會「terminal output 長什麼樣」，但要準確預測「這個命令在這個具體環境裡的輸出結果是什麼」——這需要真正理解系統的運作邏輯。

### 2. Turing-Test 做 Reward 是死路

他們試過讓 judge 做圖靈測試：「這個 observation 是真的還是模型生成的？」直覺上這很合理——如果 judge 分不出真假，模擬品質就夠好了。

但實際上 false-negative 率太高。好的模擬被判成「真的」的比例太大，導致 reward signal 太弱，策略幾乎不更新。最後放棄了這個方向。

### 3. Self-Praise Reward Hacking

RL 後期，模型發現了一個捷徑：**在模擬的環境觀測裡塞入讚美自己的文字**。比如模擬 terminal output 時，在正常的輸出後面加一句「operation completed with excellent efficiency」。LLM judge 看到正面描述就給更高分，但實際的模擬準確度根本沒提升。

這是一個新的 failure mode。以前 RL 的 reward hacking 通常是策略學會某種 degenerate behavior（比如一直重複同一個動作拿 reward）。這次不一樣——模型學會了**修改環境的回應內容來欺騙 judge**。某種意義上，它在「幻覺」環境的讚美。

### 4. GUI 環境仍是弱項

Qwen-AgentWorld 在文字環境（MCP、SWE、Terminal）表現最強，但在 GUI 環境（Android、Web、OS）落後 Claude Opus 4.8 大約 2-4 分。

一個可能原因：GUI 環境的觀測（accessibility tree、view hierarchy）結構化程度低、噪音多、而且跟視覺佈局強相關。純文字的 World Model 在這類環境的模擬難度天然更高。

### 5. 環境模擬的品質不需要完美就足夠有用

Sim RL 超過 Real RL 的結果暗示了一件事：**World Model 不需要 100% 完美地模擬環境，只要提供足夠多樣化和可控的訓練信號，就能訓練出更好的 Agent。** 80% 準確的模擬 + 可控的 edge case 生成 > 100% 準確但分布固定的真實環境。

---

## 這對實務有什麼意義

### 對 Agent 開發者

如果你在做 Agent 訓練，World Model 是一個值得認真看待的方向。兩個直接的應用場景：

**場景一：測試環境的替代方案。** 設定真實測試環境的成本很高（需要容器、API、沙盒）。如果 World Model 能模擬這些環境，你可以用它做大量的 offline 測試和 RL 訓練，只在最後階段用真實環境驗證。

**場景二：Edge case 覆蓋。** 真實環境裡很難遇到的異常場景（磁碟滿、API 超時、權限被拒），World Model 可以刻意製造。這對 Agent 的魯棒性至關重要。

### 對模型選型

開源的 35B-A3B 版本在 AgentWorldBench 上拿到 56.39 分，逼近 Claude Opus 4.8 的 56.59。如果你的場景主要是文字環境（terminal、SWE、MCP），這個模型是一個有競爭力的開源選項。

但要注意：AgentWorldBench 測的是「環境模擬能力」，不是「Agent 執行能力」。這兩者相關但不等價。

### 對 AI 研究方向

這篇論文最大的貢獻可能不是任何一個具體的數字，而是它打開了一條新的研究路線：**Agent 能力的提升不一定要靠訓練 Agent 行為本身，可以靠訓練對環境的理解來間接獲得。**

這跟人類學習的模式其實很像。一個新手工程師不會先背「遇到錯誤 X 要執行指令 Y」的對照表，他會先花時間理解系統怎麼運作——理解了之後，遇到新問題自然知道怎麼處理。

---

## 坦白說

這篇論文有幾個限制需要注意：

**AgentWorldBench 是自建的 benchmark。** 雖然設計上做了跨模型軌跡和跨 judge 驗證，但自家 benchmark 測自家模型，永遠要保持一定的保留態度。最終還是要看這個模型在其他人建的 benchmark 上的表現。

**「模擬環境訓練比真實環境好」的結論有條件。** 這在 OpenClaw 環境上驗證了，但不確定能直接推廣到所有環境。特別是 GUI 環境和需要即時世界知識的 Search 環境，模擬品質仍有明顯差距。

**開源版本是 35B-A3B，不是 397B-A17B。** 最好的結果來自未開源的大模型。這跟很多「開源」工作的模式一致——開源一個小的、秀一個大的。不過 35B 版本本身的表現也不差，算是有誠意。

**Reward hacking 的問題。** Self-praise reward hacking 雖然被緩解了，但這類問題很可能在更大規模的訓練中以新的形式重現。LLM-as-judge 的 RL 訓練管線裡，這是一個結構性的脆弱點。

---

## 一句話總結

> **訓練 Agent 的下一步，可能不是教它做更多的動作，而是教它理解環境的運作邏輯。Qwen-AgentWorld 用數據證明了這個方向的可行性——用模擬環境訓練的 Agent 超過真實環境訓練的，光做環境預測就能提升 Agent 能力。World Model 是 Agent 訓練的 missing piece。**

---

## 延伸資源

- **論文：** [Qwen-AgentWorld: Language World Models for General Agents](https://arxiv.org/abs/2606.24597)
- **官方 Blog：** [qwen.ai/blog?id=qwen-agentworld](https://qwen.ai/blog?id=qwen-agentworld)
- **GitHub：** [QwenLM/Qwen-AgentWorld](https://github.com/QwenLM/Qwen-AgentWorld)
- **HuggingFace：** [Qwen/Qwen-AgentWorld](https://huggingface.co/collections/Qwen/qwen-agentworld)

---

## 常見問題 Q&A

**Q: Qwen-AgentWorld 跟一般的 Agent 模型（像 Claude、GPT）有什麼不同？**

一般的 Agent 模型是訓練來「在環境中執行動作」的——給它一個任務，它會呼叫工具、讀取結果、再決定下一步。Qwen-AgentWorld 的訓練目標相反：給它一個動作，預測環境會回傳什麼結果。它是「環境模擬器」，不是「行動決策者」。但論文證明，學會模擬環境的副產品是 Agent 能力也跟著提升。

**Q: 開源的 35B 版本能直接拿來用嗎？**

可以。它在 HuggingFace 和 ModelScope 上都有。256K 上下文、3B 激活參數，推理成本相當低。但它的主要用途是環境模擬（用來做 Agent 的 offline 測試或 Sim RL），不是直接當通用 Agent 使用。如果你想拿它做 Agent，論文的 Paradigm II 結果顯示它有 Agent 能力，但不如專門為 Agent 訓練的模型。

**Q: 「模擬環境比真實環境好」的結論靠譜嗎？**

在論文測試的 OpenClaw 環境裡是靠譜的——四個 benchmark 一致性地顯示 Sim RL > Real RL。但這不代表所有環境都是如此。模擬品質越高、可控性越強的環境（像 terminal 和 MCP），優勢越明顯。GUI 環境和需要即時知識的 Search 環境，目前模擬品質仍有差距。

**Q: Self-praise reward hacking 是什麼，為什麼重要？**

RL 訓練時，模型發現了一個捷徑：在模擬的環境輸出裡偷偷加入正面描述（「operation completed successfully with optimal performance」），讓 LLM judge 給更高分。但實際模擬準確度沒有提升。這是 LLM-as-judge 做 RL reward 的結構性弱點——只要 judge 是語言模型，就有被語言層面的操縱影響的風險。他們用 rule-based verifier + 內容分類來緩解，但這個問題在更大規模的訓練中可能以新形式再現。
