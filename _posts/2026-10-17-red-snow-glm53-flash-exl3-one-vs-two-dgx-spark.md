---
layout: post
title: "你需要自己的紅軍 AI：從韓國七家銀行被打穿，到 RED-SNOW 在自己桌上跑滲透測試"
date: 2026-10-17 09:00:00 +0800
permalink: /red-snow-glm53-flash-exl3-one-vs-two-dgx-spark/
tags: [RED-SNOW, GLM-5.3-Flash, DGX Spark, EXL3, 紅隊, red team, 滲透測試, pentest, abliteration, 地端推理, local LLM, CrowdStrike, ARTEX, 資安]
categories: [AI Agent]
image: /assets/images/red-snow-one-vs-two-spark-cover.png
description: "九月底，一個門外漢年輕人用 AI Agent 一週打穿韓國七家金融機構，約 6.7 萬筆資料外洩。同一時間，BreachForums 上出現用 Grok 驅動的攻擊工具。攻擊方已經在用無護欄 AI，防禦方呢？RED-SNOW 是 Blackfrost-AI 用 GLM-5.3-Flash 做的紅隊模型，X 上一群玩家拿它測自己的 app，有人跑出 3 個 critical。這篇從真實攻擊案例出發，拆 RED-SNOW 能做什麼、網友怎麼用，以及為什麼每個有產品要顧的人，都該考慮跑自己的紅軍 AI。"
author: Wisely Chen
faq:
  - question: "RED-SNOW-5.3-FLASH 跟原版 GLM-5.3-Flash 差在哪？"
    answer: "RED-SNOW 是 Blackfrost-AI 在 GLM-5.3-Flash（320B 總參數、每 token 啟動 18B 的 MoE 架構）上做了兩件事：消融（Abliteration）移除模型的拒答行為，加上 17,132 筆訓練資料的資安 LoRA fine-tune，其中 85.8% 是攻擊性資安內容。結果是一個不會拒絕資安類問題的紅隊模型（Red Team Model），10 月 5 日發布，標示只給授權的紅隊作業用。"
  - question: "跑 RED-SNOW 一定要 DGX Spark 嗎？"
    answer: "不用。DGX Spark（GB10、128 GB 統一記憶體）可以跑 2-bit 單台版，但不是唯一選項。Ben Everman 在租的 RTX Pro 6000 上跑到約每秒 50 個 token，租金一小時 1.5 美金。Grant Overton 做了 Apple Silicon 的 MLX 4-bit 版，Mac 也能跑。硬體選項包含 NVIDIA GPU 租用、Apple Silicon 本地、和 DGX Spark。"
  - question: "什麼時候不該用 RED-SNOW？"
    answer: "消融技術（Abliteration）會傷到長任務和工具使用（Tool Use），100k token 以上的深度研究（Deep Research）不適合——每回合要等約五分鐘靜默，而且能力會打折。它也不是通用 coding 助手。適合場景是 10k 到 35k token 的中短 context agent loop，特別是授權滲透測試（Penetration Testing）和結構化安全輸出。"
  - question: "「授權紅隊」跟「用無護欄模型做壞事」的界線在哪？"
    answer: "三個字：你自己的。紅隊測試（Red Teaming）的核心是你對自己擁有的系統做攻擊模擬。Viktor 的案例很清楚：測的是自己做了 10 個月的 app、模型跑在自己桌上、結果不離開本地。用無護欄模型去探別人的系統，那是未授權入侵。RED-SNOW 標示的「only for authorized red-team operations」不是行銷用語，是法律界線。"
  - question: "本地跑 GLM-5.3 系列模型最常踩到什麼坑？"
    answer: "GLM-5.3 關不掉 thinking 模式。你送 enable_thinking false，server 收下但不理你。如果 max_tokens 設太小，模型在思考區塊裡就把預算花光，回你空字串而且不報錯。解法是把 max_tokens 給夠（至少 512 以上）。另外 exllamav3 的 fork 不 pin 住 commit 會默默慢掉約 25%，log 完全不報錯，每次 pull 之後要重新 pin。"
---

九月底到十月初，韓國至少七家金融機構被同一波攻擊打穿。

CrowdStrike 回溯之後發現，攻擊者看起來不是駭客組織，是一個門外漢年輕人。用 Claude Code 指揮開源框架 ARTEX，模型走 DeepSeek v4.1-flash。伺服器開著公開目錄，session 紀錄、攻擊指令、連求職履歷都攤在那裡。合計約 6.7 萬筆資料外洩。光新韓銀行就約 2.5 萬名客戶，66 件連身分證字號一起出去。

[完整分析見這裡](/crowdstrike-artex-korea-banks-open-directory-claude-code/)。

同一段時間，BreachForums 上已經出現用 Grok 驅動的無審查攻擊工具。我在[另一篇](/grok-4-5-attacker-model-access-over-capability-mythos/)推導過一個框架：**攻擊力 = 能力 × 可及性 × 沒有護欄**——三個乘數都不缺的模型，有效攻擊力比那些被鎖起來的頂級模型還高。

攻擊方已經在用無護欄 AI。防禦方呢？

<nav class="post-toc" markdown="1">
**目錄**

* 目錄
{:toc}
</nav>

---

## RED-SNOW 是什麼，能做什麼

| 項目 | 內容 |
|------|------|
| 模型 | RED-SNOW-5.3-FLASH，Blackfrost-AI 製作 |
| 底模 | GLM-5.3-Flash（320B 總參數、每 token 啟動 18B，MoE，MIT 授權） |
| 做了什麼 | abliteration（移除拒答行為）+ 17,132 筆訓練資料的資安 LoRA fine-tune，85.8% 是攻擊性資安內容 |
| 發布日 | 10 月 5 日 |
| 授權 | 標示只給授權的紅隊作業用 |
| 格式 | BF16 / FP8 / NVFP4（Blackfrost 官方）、EXL3（Cruz 社群版） |
| 硬體 | DGX Spark（GB10、128 GB 統一記憶體）單台可跑 2-bit 版；也有 L40s、RTX Pro 6000、Apple Silicon MLX 版 |

簡單講，Blackfrost 對 GLM-5.3-Flash 做了兩件事：消融（abliteration）讓它不再拒絕回答資安類問題，再用大量攻擊性資安資料做 fine-tune 讓它更懂攻防。

它能做的事，最直接的三個：

1. **授權滲透測試**：對你自己擁有的系統做黑箱測試
2. **程式碼安全審查**：找出安全漏洞
3. **攻擊路徑建模**：模擬攻擊者的思路

但規格表說不了什麼。重點是有人真的拿它做了什麼。

---

## 網友怎麼用

### Viktor：測自己的 app，跑出 3 個 critical

最實在的一則使用紀錄。

[Viktor](https://x.com/15ky3/status/2109531116860588256) 拿單台 Spark 的 2-bit 版，對自己做了 10 個月的 web app 做黑箱滲透測試，跑出 3 個 critical 問題。

這句話的重點在三個字：**自己的 app**。不給原始碼、只給網址，讓模型像外部攻擊者一樣探。整個模型跑在他自己桌上，程式碼和攻擊手法完全不離開本地。

這是「授權紅隊」四個字最具體的樣子。也是做 appsec、自己有產品要顧的人最能用上的場景。

### Yume_X：兩天認真測，踩到的坑比分數有用

寫得最完整的是 [Yume_X](https://x.com/yume_arasaki/status/2109454666933436691)。12 項資安任務 judge 評分拿 21/22。但更有用的是他記下來的坑。

GLM-5.3 關不掉 thinking。你送 enable_thinking false，server 收下但不理。max_tokens 設太小，模型在 think 區塊裡就把預算花光，回你一個空字串。把預算提到 512，同樣的題，長文件檢索到 24 萬 token 還能 15/15。

唯一失分的一題不是不會做，是把 token 全花在想，最後沒寫出答案。

另一個坑：exllamav3 的 fork [不 pin 住 commit](https://x.com/yume_arasaki/status/2110194476950114501)，會默默慢掉約 25%，log 不會報任何錯。

### 長 context 的真正代價是等待

[Yume 把適配範圍講得很清楚](https://x.com/yume_arasaki/status/2110193379342786881)。長 context 真正的代價不是生成慢，是第一個字的等待時間（TTFT）。

context 開 8k 時大約等 14 秒，131k 要等約 152 秒，開到 24 萬 token 要等約 280 秒。但字一旦開始吐，速度從頭到尾都在每秒 44 到 50 個 token。

他給了一個好記的公式：等待秒數大約是 context token 數除以 550。

所以適配範圍是：

- **agent loop，10k 到 35k**：最合適，單台機器跑自己的 harness 很舒服
- **deep research，100k 以上**：不適合，每回合五分鐘靜默
- **JSON 結構化輸出**：任何深度都是甜蜜點

### 硬體不綁 DGX Spark

不是只有 Spark 能跑。

[Ben Everman](https://x.com/beneverman/status/2109765370190107135) 租 GPU，先在兩張 L40s 上，目標壓在一小時兩美金。[後來換成 RTX Pro 6000](https://x.com/beneverman/status/2110395894785036669)，一小時 1.5 美金跑到約每秒 50 個 token。過程中還找到並修了 thinking-template 的 bug。

[Grant Overton](https://x.com/grantoverton/status/2109440321482563787) 做了 Apple Silicon 的 MLX 版，Mac 也能跑。

想試 RED-SNOW 不用先買一台 Spark。

### 反方

[有人直接說](https://x.com/AnotherWayIn/status/2110797550316064883)：拿 abliterated 模型去比 clean 模型是張飛打岳飛，abliteration 常常會傷到長任務和工具使用。

這個批評是對的。而且正好解釋了為什麼好用場景集中在中短 context——不是去護欄沒代價，是代價落在長鏈條上。所以把它當特定任務的工具，不是通用助手。

---

## 我的測試結果

我拿兩台 DGX Spark 跑 RED-SNOW，測了兩件事：速度和實際掃描。

### 部署設定

| 項目 | 設定 |
|------|------|
| 模型 | RED-SNOW 5.3 Flash，EXL3 SAGE 4.91 bpw |
| 推理框架 | ExLlamaV3 雙機推理 + 自訂 API 相容層 |
| Context 上限 | 262,144 tokens（256K） |
| KV cache | 4-bit |
| 雙機分層 | Head：第 0–22 層；Worker：第 23–44 層 |
| 雙機通訊 | NCCL |
| 同時請求 | 1 個，忙碌回 429 |
| Thinking | 關閉（enable_thinking=False） |
| 前綴快取 / MTP | 未啟用 |

跟社群報告的單機 2.49 bpw 不同，我的版本是 4.91 bpw 雙機——量化精度高但每 token 運算量更大，加上 NCCL 跨機通訊開銷。這會反映在速度上。

### 速度

生成速度約每秒 15 個 token，輸入長度主要影響首字等待：

| 輸入長度 | 首字等待 | 生成速度 | 輸出 160 tokens 總時間 |
|----------|----------|----------|----------------------|
| 223 tokens（第 1 次） | 1.23 秒 | 15.37 tok/s | 11.57 秒 |
| 223 tokens（第 2 次） | 1.23 秒 | 15.31 tok/s | 11.62 秒 |
| 9,006 tokens | 26.00 秒 | 14.88 tok/s | 36.69 秒 |

harness 帶約 9K 的對話與工具定義時，光等第一個字就要約 26 秒。開始輸出後仍約 15 tok/s，不太受 context 長度影響。如果已有請求在運算，會遇到 429。

跟 Yume 社群報的 44–50 tok/s 比，差距明顯。主要原因是我跑的是 4.91 bpw 雙機版，Yume 跑的是 2.49 bpw 單機版——每 token 運算量更大，再加上 NCCL 跨機通訊開銷。但趨勢一致：**首字等待隨 context 長度線性增長，生成速度本身幾乎不掉。**

### 實際掃描：跟 ZAP 的結果比較

我拿 RED-SNOW 對兩個正式環境的 web app 做主動掃描，然後跟之前 ZAP 被動掃描的結果對照：

| | ZAP 被動掃描 | RED-SNOW 主動掃描 |
|--|-------------|-------------------|
| 原始告警 | 84 | 80 |
| 誤報 | 1 | 33 |
| 淨發現 | 83 | 47 |
| 高 | 0 | 0 |
| 中 | 34 | 9 |
| 低 | 30 | 20 |
| 資訊 | 20 | 18 |

兩次掃描互相印證：HSTS 缺失、nosniff 缺失、防嵌入缺失、CSP 的發現完全一致，可信度高。

RED-SNOW 掃出 ZAP 沒有的東西：**4 個 API 的 Spring Boot Actuator 暴露**（MEDIUM）。這是 ZAP 被動模式抓不到的，需要主動探測才會發現。反過來也確認了 ZAP 的一筆誤報（10055-5，script-src unsafe-inline——實際 HTTP header 沒有 unsafe-inline）。

但誤報率是 41%（33/80）。33 個誤報的主因是 SPA fallback——前端對未知路徑一律回傳 index.html，掃描器把 /config.php、/admin 這些路徑當成可存取。這是 harness 的問題，不是模型的問題——需要加「比對回應是否與首頁相同」的邏輯。

### 跟上週原版 GLM-5.3 Flash 的對照

上週我測[原版 GLM-5.3 Flash](/dgx-spark-test-log-flash-models-glm-qwen-deepseek/) 時觀察到的「做到一半說做完」，在 RED-SNOW 的單次掃描任務裡沒有明顯出現——可能因為掃描任務比多步 agent loop 短，模型不容易在中途「宣告完成」。部署方式的影響仍然很大：我的 4.91 bpw 雙機版跑出 15 tok/s，Yume 的 2.49 bpw 單機版跑到 44–50 tok/s，差了將近三倍。量化精度、NCCL 跨機開銷、serving 設定都在影響。

---

## 你需要自己的紅軍 AI

回到開場那個案子。

韓國那個攻擊者是門外漢。他的 AI 框架不是什麼秘密武器，是開源的 ARTEX 加上任何人都能叫到的 API。他拿到的不是核心系統，是那些被忘了鎖的後院小門——仲介查詢服務、員工行動辦公系統。

這是現在的風景：攻擊方已經在用無護欄 AI，而且不需要是專家。

防禦方呢？多數人還在等一年一次的滲透測試。等結果回來的時候，人家已經掃過你的前門三遍了。

我之前寫過，有了 AI，等於人人都有了槍，[你家裡就被迫也要放一把](/qwen38-27b-abliteration-three-days-safety-paradox/)。RED-SNOW 是那把槍的一個選項。你不是拿它去攻擊別人，是先用攻擊者的武器打自己一遍，在對方之前找到洞。

Viktor 做的事是最好的範本：跑在自己桌上、測自己的 app、程式碼不離開本地。不需要請外部顧問，不需要等排程。你的 app 更新了就再跑一次。

如果你有自己的產品要顧，現在就可以做的事：

1. 挑一個 10k–35k token 的 agent loop 場景（例如對你的 API 做自動化探測）
2. 選一個跑得動的硬體（租一張 RTX Pro 6000 一小時 1.5 美金就夠）
3. 讓模型像外部攻擊者一樣探，看它能找到什麼

不等一年一次的報告，自己先打自己一遍。

---

## 坦白說

RED-SNOW 是 abliterated 模型，abliteration 會傷到長任務和 tool use。適用場景集中在中短 context 的 agent loop——10k 到 35k token 的滲透測試任務。超出這個範圍，能力會打折。

第二段（網友怎麼用）是 X 上的實錄。第三段是我自己在兩台 Spark 的 4.91 bpw 雙機推理上跑的，樣本很小：速度測了三次、掃描對照了兩個 app。我的掃描器誤報率 41%，主因是 SPA fallback 的邏輯沒做好，這個數字反映的是 harness 的成熟度，不是模型能力。

開場引用的韓國案例和 BreachForums 案例都是我自己之前寫過的分析。那些分析的素材來源和限制，在原文裡交代過，這篇不重複展開。讀者要知道數字不是獨立第三方交叉驗證的，是我根據 CrowdStrike 報告和公開報導整理的。

另外，「先打自己一遍」不等於「不用做其他防禦」。紅軍 AI 是一層，不是全部。把它當成唯一防線跟不做防禦一樣危險。

---

## 關鍵洞察

1. **攻擊門檻已經降到地板。** 韓國案例示範了「門外漢 + AI Agent + 開源工具」就能打穿金融機構的邊緣系統。等你被打，對方可能不是駭客組織，是一個拿著 ARTEX 的年輕人。

2. **紅軍 AI 最直接的用法：對你自己的 app 做黑箱滲透測試。** Viktor 的案例是最好的範本——不給原始碼、只給網址、模型跑在本地、結果不離開桌面。做 appsec、自己有產品要顧的人，可以從這裡開始。

3. **適配範圍在中短 context 的 agent loop。** RED-SNOW 不是通用助手。它的甜蜜點是 10k 到 35k token 的安全任務。100k 以上的 deep research 不適合。

4. **部署方式的影響比換模型大。** 不 pin exllamav3 的 commit 就慢 25%、thinking 關不掉就要調 max_tokens。這些「怎麼跑」的細節，比「跑哪個模型」重要。

---

## 常見問題 Q&A

**Q: RED-SNOW-5.3-FLASH 跟原版 GLM-5.3-Flash 差在哪？**

RED-SNOW 是 Blackfrost-AI 在 GLM-5.3-Flash（320B 總參數、每 token 啟動 18B 的 MoE 架構）上做了兩件事：消融（Abliteration）移除模型的拒答行為，加上 17,132 筆訓練資料的資安 LoRA fine-tune，其中 85.8% 是攻擊性資安內容。結果是一個不會拒絕資安類問題的紅隊模型（Red Team Model），10 月 5 日發布，標示只給授權的紅隊作業用。

**Q: 跑 RED-SNOW 一定要 DGX Spark 嗎？**

不用。DGX Spark（GB10、128 GB 統一記憶體）可以跑 2-bit 單台版，但不是唯一選項。Ben Everman 在租的 RTX Pro 6000 上跑到約每秒 50 個 token，租金一小時 1.5 美金。Grant Overton 做了 Apple Silicon 的 MLX 4-bit 版，Mac 也能跑。硬體選項包含 NVIDIA GPU 租用、Apple Silicon 本地、和 DGX Spark。

**Q: 什麼時候不該用 RED-SNOW？**

消融技術（Abliteration）會傷到長任務和工具使用（Tool Use），100k token 以上的深度研究（Deep Research）不適合——每回合要等約五分鐘靜默，而且能力會打折。它也不是通用 coding 助手。適合場景是 10k 到 35k token 的中短 context agent loop，特別是授權滲透測試（Penetration Testing）和結構化安全輸出。

**Q: 「授權紅隊」跟「用無護欄模型做壞事」的界線在哪？**

三個字：你自己的。紅隊測試（Red Teaming）的核心是你對自己擁有的系統做攻擊模擬。Viktor 的案例很清楚：測的是自己做了 10 個月的 app、模型跑在自己桌上、結果不離開本地。用無護欄模型去探別人的系統，那是未授權入侵。RED-SNOW 標示的「only for authorized red-team operations」不是行銷用語，是法律界線。

**Q: 本地跑 GLM-5.3 系列模型最常踩到什麼坑？**

GLM-5.3 關不掉 thinking 模式。你送 enable_thinking false，server 收下但不理你。如果 max_tokens 設太小，模型在思考區塊裡就把預算花光，回你空字串而且不報錯。解法是把 max_tokens 給夠（至少 512 以上）。另外 exllamav3 的 fork 不 pin 住 commit 會默默慢掉約 25%，log 完全不報錯，每次 pull 之後要重新 pin。
