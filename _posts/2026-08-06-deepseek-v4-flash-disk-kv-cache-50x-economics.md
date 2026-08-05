---
layout: post
title: "DeepSeek V4 Flash 0731 為何那麼強：這是一個超過兩年以上的架構革命"
date: 2026-08-06 09:00:00 +0800
permalink: /deepseek-v4-flash-disk-kv-cache-50x-economics/
description: "DeepSeek V4 Flash 0731 上線後，Artificial Analysis 的性價比散點圖上出現一條被中文科技圈叫做「斬殺線」的線：智力分數 49.9、每任務成本 $0.027，比它貴又比它笨的模型全部落進「斬殺區」。這篇拆 V4 Flash 為何站得上這個位置：disk KV cache 落進分散式硬碟陣列、cache hit 價格只剩 miss 的 2%（$0.0028 vs $0.14）、hit rate 90% 和 99% 帳單差 4 倍的數學，以及兩年前 MLA 把 KV 壓小 93% 才鋪出來的路。附 qwen-code 的真實反例：token 少 46%、帳單反而三倍。"
image: /assets/images/deepseek-v4-flash-zhanshaxian-cover.jpg
categories: [AI 前沿技術]
author: Wisely Chen
---

# DeepSeek V4 Flash 0731 為何那麼強：這是一個超過兩年以上的架構革命

V4 Flash 0731 在 7 月 31 日上線後一週，中文科技圈開始流傳一個詞：「斬殺線」。

出處是文章開頭那張 Artificial Analysis 的散點圖。橫軸是每個 Intelligence Index 任務的成本（log scale，越左越便宜），縱軸是綜合智力分數。DeepSeek V4 Flash 0731 落在智力 49.9、每任務 $0.027 的位置——**分數擠到第一梯隊門口，價格卻停在最便宜的一檔**。從這個點往右下拉出去的整片區域，就被叫做「斬殺區」：比它貴、又比它笨的模型，全部落在裡面。圖上 128 個模型，大多數都在斬殺區內。

這個詞會傳開，是因為它把模型選型壓縮成一句話：斬殺區裡的模型，你為什麼要用？

但比較少人追問下一個問題：**那個 $0.027 是怎麼做到的？** 這篇要拆的正是這件事。

---

## 30 秒定位：V4 Flash 0731 是什麼

| 項目 | 數字 |
|------|------|
| 發布日期 | 2026-07-31（4 月 Preview 版重新 post-train 後的正式版） |
| 架構 | 284B 總參數 MoE，每 token 啟用 13B |
| Context | 1M tokens |
| 授權 | MIT，權重開放在 Hugging Face |
| Input（cache miss） | $0.14 / 1M tokens |
| Input（cache hit） | **$0.0028 / 1M tokens** |
| Output | $0.28 / 1M tokens |

重點在倒數第二行。cache hit 的價格是 miss 的 **2%**，價差 50 倍。

上一代 V3.2 的價差是 10 倍（$0.028 vs $0.28）。Anthropic 的 prompt caching 也是 10 倍（cache read 是原價的 0.1 倍）。50 倍是目前主流 API 裡最激進的一檔。

V4 Flash 發布後一週，X 上有一串討論說 disk KV cache 是被嚴重低估的 killer feature，底下馬上有兩種質疑：「disk cache 不是 DeepSeek 兩年前就有了嗎？」「這不就是 inference engine 的功能？vLLM 開 tiered KV cache 也能把 RAM 加 SSD 當 cache 用。」

兩種質疑都對，但都只看到一個齒輪。V4 Flash 的強，是三個齒輪咬合的結果：**KV cache 落進硬碟、50 倍價差的數學、還有兩年前就開始的架構壓縮。** 下面一個一個拆。

---

## 齒輪一：Disk KV cache——把 cache 從記憶體搬進硬碟陣列

先講 KV cache 本身。LLM 推理時，每個 token 的 attention 中間結果（Key 和 Value）會被存下來，後續 token 不用重算。這份 cache 通常放在 GPU 的 HBM 記憶體裡——快，但貴，而且塞不了多少。

所以主流做法是：cache 只活在記憶體裡，短時間內沒人用就丟掉。Anthropic 的 prompt caching 預設 TTL 是 5 分鐘，加購才有 1 小時。你隔天回來繼續同一個專案，cache 早就沒了，整份 context 重新計費。

DeepSeek 在 2024 年 8 月做了一件當時很少人注意的事：**把 KV cache 落到分散式硬碟陣列上**，並自稱是全球第一家在 API 服務裡大規模這樣做的供應商。硬碟便宜，所以 cache 可以留得久——官方說法是未使用的 cache「通常幾小時到幾天」才清除。而且全自動，不用改 code、不用下 cache-control 標記，prefix 相同就命中。

記憶體 cache 和硬碟 cache 的差別，講白了就是：

- **記憶體 cache**：這一輪對話裡省錢。5 分鐘 TTL 服務的是「連續互動中」的 session。
- **硬碟 cache**：跨 session 省錢。你今天跑過的 codebase、系統 prompt、文件，明天回來還在。

對 Agent 工作負載，這個差別是決定性的。Agent 的 context 結構是「一大坨穩定的 prefix（系統 prompt + 工具定義 + codebase）+ 一小段增量」，而且會反覆回來。這正是長壽命 cache 的最佳客戶。

---

## 齒輪二：50 倍價差的數學——90% 和 99% 的 hit rate，帳單差 4 倍

cache 存得久，hit rate 就高。但 hit rate 高一點，到底差多少錢？

用 V4 Flash 的真實價格算一次。有效輸入單價 = hit rate × $0.0028 + (1 − hit rate) × $0.14：

| Cache hit rate | 有效輸入單價（/1M tokens） | 其中 miss 貢獻的比例 |
|----------------|--------------------------|---------------------|
| 80% | $0.0302 | 93% |
| 90% | $0.0165 | 85% |
| 95% | $0.0097 | 72% |
| 99% | $0.0042 | 34% |

從 90% 到 95%，帳單省 1.7 倍。從 90% 到 99%，省 4 倍。

為什麼幾個百分點的差距會放大成倍數？因為 hit 的價格已經低到接近零，**帳單幾乎完全由 miss 的部分決定**。hit rate 90% 的意思是 miss rate 10%，95% 的意思是 miss rate 5%——從 miss 的角度看，這不是「多了 5 個百分點」，是「miss 砍半」。miss 砍半，帳單就接近砍半。

這跟系統可用性的「幾個九」是同一種數學。99% 和 99.9% 的差別不是 0.9 個百分點，是 downtime 差 10 倍。**價差拉到 50 倍之後，cache hit rate 就變成了 API 成本的「九」——你該盯的是 miss rate 的量級，不是 hit rate 的百分點。**

這個數學不是紙上談兵，qwen-code 身上就真實上演過一次。它在 v0.15.10 加了一個叫 ToolSearch 的功能，把 MCP 工具從「開場全部宣告」改成「用到才載入」——聽起來是標準的 context 優化，省 token、省錢，對吧。有用戶升級後看了帳單：**每天處理的 token 總量少了 46%，費用卻從 $1.05 漲到 $3.30，三倍。**

原因在另一個指標上。工具動態載入讓每個 request 的 prompt 開頭不再相同，prefix cache 大面積失效，cache hit rate 從 97.5% 掉到 81.5%，未命中的 token 從每天 300 萬暴增到 1,290 萬。看起來只掉了 16 個百分點，從 miss 的角度看是 2.5% 漲到 18.5%——**7 倍**。省下來的 token 數，被 50 倍的價差整個吃掉還倒賠。

「帳單跟 miss rate 成正比、不跟 token 數成正比」，具體長相正是如此。

反過來說也成立：一個 prefix 設計得好的 Agent harness，在 V4 Flash 上跑出 95% 以上的 hit rate（發布後有用戶自述 preview 期間拿到 95-98%），有效輸入單價就會壓到每百萬 token 一美分以下。這個數字配上它在 agentic benchmark 上的表現，構成了「強」的具體形狀：**不是單點分數多高，是同樣的 Agent 工作量，成本低了一個量級。**

---

## 齒輪三：MLA 先把 KV 壓小 93%——這條路兩年前就開始鋪

50 倍價差不是行銷部門拍腦袋的數字。往回追，這條路徑是這樣的：

| 時間 | 動作 | 效果 |
|------|------|------|
| 2024-05 | V2 提出 MLA | KV cache 降 93.3% |
| 2024-08 | API 推出 disk context caching | cache hit 價格降到 1/10 |
| 2025-12 | V3.2 上線 DSA（sparse attention） | 價差維持 10 倍，總價砍半 |
| 2026-04 | V4 提出 CSA + HCA | KV cache 壓到 V3.2 的 7% |
| 2026-07 | V4 Flash 0731 正式版 | cache 價差拉到 50 倍 |

> **附註：這三個縮寫在做什麼**
> - **MLA**（Multi-head Latent Attention，V2 提出）：用低秩投影讓多個 attention head 共用同一個 latent 空間，壓的是「每個 token 的 KV 表徵」——縱向砍 head 維度，KV cache 直接降 93.3%。
> - **CSA**（Compressed Sparse Attention，V4 提出）：負責「抓重點」。先把 100 萬 token 的 KV 壓成 25 萬條，再從中挑出最有用的一小部分算 full attention——橫向砍 token 數量，保住局部精度。
> - **HCA**（Heavily Compressed Attention，V4 提出）：負責「看全域」。把 100 萬 token 直接壓成 7,800 條（0.78%）的低解析度全域通道，讓模型永遠隱約知道整篇在講什麼。
>
> 用照片來比喻：**MLA 是把每張照片從 RAW 壓成 JPEG**（單張變小），**CSA 是從相簿裡只挑重要的照片留下**（張數變少），**HCA 是另外存一份全部照片的縮圖目錄**（超低解析度，但全都在）。前者壓的是「每條 KV 的大小」，後兩者壓的是「KV 的條數」，兩個軸相乘，才疊出「KV cache 只剩傳統 2%」這種數字。
>
> 這三個機制的完整拆解（設計思路、跟 NSA/DSA 的傳承關係），在我四月寫的 [DeepSeek V4 把百萬 Token 上下文打到傳統 2% 成本](https://ai-coding.wiselychen.com/deepseek-v4-million-token-csa-hca-attention/)。

順序很重要：**先有 MLA 把 KV 壓小 93%，三個月後才有 disk cache。** 這不是巧合。KV cache 越小，落盤的儲存成本越低、從硬碟載回來的 I/O 越少，disk cache 的經濟學才成立。到了 V4，[CSA + HCA 把 KV cache 再壓到 V3.2 的 7%](https://ai-coding.wiselychen.com/deepseek-v4-million-token-csa-hca-attention/)——每 token 要搬的資料量小到一個量級以下，DeepSeek 才敢把 hit 價格開到 $0.0028 這種接近純儲存成本的數字。

我四月寫 V4 架構那篇的時候，關注的是「百萬 token 怎麼做到保真」。現在看，同一套壓縮還有第二個作用：**它是這次 50 倍定價的前提。**

這也呼應我之前在 [DDR/HBM Token 經濟學那篇](https://ai-coding.wiselychen.com/ddr-hbm-token-economics-nvidia-lock-supply-chain/)講的：token 經濟學的天花板被物理鎖在 HBM 上。DeepSeek 這條路線的本質，就是把「重複計算」一路往便宜的儲存層搬——從 HBM 搬到 DRAM 再搬到硬碟，每搬一層，同一份 context 的重複成本就掉一個量級。

---

## 三個齒輪合起來，才是「那麼強」的完整句子

現在可以回答標題的問題了。V4 Flash 的強不是任何單一功能：

- 只有 disk cache，沒有架構壓縮 → KV 太大，落盤的 I/O 跟儲存成本撐不住，價差開不深。這就是為什麼「vLLM + LMCache 也能做 SSD offload」的質疑只對了一半——功能能抄，經濟學抄不動，因為 KV 的形狀在模型訓練時就決定了，inference engine 追不回來。
- 只有架構壓縮，沒有 disk cache → 省的是單次推理的成本，跨 session 的重複 context 還是每次全額計費。
- 兩個都有，但價差只開 10 倍 → 那是 V3.2。好，但不會讓人喊 killer feature。

**架構壓縮 × 硬碟落盤 × 敢把省下的成本反映在牌價上**，三件事咬合，才得到「一個 MIT 授權、1M context、agentic 任務打得過自家旗艦、而且 input 在高 hit rate 下接近免費」的模型——也就是斬殺線那個「智力 49.9、每任務 $0.027」的座標。橫軸的位置是三個齒輪咬出來的，縱軸那批 agent 分數怎麼看，放到坦白說裡講。

那這是護城河嗎？那串討論裡有一句話講得很到位：

> "DS v4 Flash arch is fully open sourced, that other players can quickly adopt in the next generation model training, and reduce the serving cost in the entire industry."

架構全開源，其他玩家下一代模型訓練就能採用，整個產業的 serving 成本一起往下掉。DeepSeek 的優勢是「時間差」不是「壁壘」——大概領先一個模型世代。這跟 MLA 的歷史一模一樣：2024 年 5 月發表，現在已經是各家標配。

所以正確的預期不是「DeepSeek 贏者全拿」，而是**50 倍價差會變成產業基準線**。一年後回頭看，「cache hit 接近免費、cache 存活以天計」大概會像今天的 prompt caching 一樣，變成 API 的基本配備。

---

## 對工程師的意義：prefix stability 現在是成本工程

把上面的東西收斂成具體的決策改變。

**以前**：選模型看價目表，input 多少、output 多少，乘上預估 token 量。harness 的 context 設計是「能力問題」——塞什麼進去模型表現最好。

**現在**：有效單價 = f(hit rate)，而 hit rate 由你的 harness 決定。context 設計同時是「成本問題」，而且槓桿大到誇張——同一個模型、同一個工作量，hit rate 90% 和 99% 的團隊，input 帳單差 4 倍。

幾個直接的操作含義：

1. **prefix 要 byte-identical 才命中。** DeepSeek 的判定是從第 0 個 token 開始完全相同。任何會動到 prompt 開頭的東西都是成本炸彈：動態載入的工具定義（qwen-code 的教訓）、每次請求注入的 timestamp、隨機排序的 few-shot、放在開頭的「當前時間」。穩定的往前放，會變的往後放。
2. **監控 dashboard 加一個指標。** DeepSeek API 的回傳裡有 cache hit/miss 的 token 數。把 hit rate 當成 SLO 在看：掉了代表有人動了 prefix，而且是在燒錢。qwen-code 的用戶正是從帳單反推才發現問題的。
3. **評估新功能時把 cache 成本算進去。** ToolSearch 型的「動態載入省 context」在 10 倍價差時代可能划算，在 50 倍價差時代很可能是負優化。省 token 數不等於省錢，這筆帳現在要用 miss rate 算。
4. **長任務 Agent 的成本模型重寫。** 硬碟 cache 以天計的存活時間，代表跨 session 的 Agent（隔夜繼續跑的 CI agent、每天巡一輪的 cron agent）prefix 部分幾乎只付一次錢。這類工作負載在 V4 Flash 上的實際成本，比價目表看起來低一個量級。

---

## 坦白說

這篇有幾個地方要打折扣看。

- **Agent 分數和成本宣稱，兩條腿都是自家 harness 跑的。** 0731 那批 agent benchmark 分數（DeepSwe 54.4 等）用的是 DeepSeek 自家、尚未開源的 harness，第三方目前無法複現（4 月 preview 的 SWE-bench Verified 79.0 有獨立測量）。官方「跑 agent 任務有效單價接近 hit 價」的成本宣稱，同樣建立在自家 harness 的高 hit rate 上。要分清楚的是：cache hit 不影響輸出品質——同一段 prefix 的 KV 從硬碟載回來和重算一遍，數學上等價，所以 hit rate 影響的是帳單，不是分數。但換成你的 harness，分數可能變動（scaffold 差異），帳單也可能變動（prefix stability 差異），兩者都要自己測。
- **50 倍價差的可持續性是未知數。** DeepSeek 沒公開 disk cache 的成本結構，$0.0028 是策略定價還是成本定價，外界無從驗證。如果是補貼換市佔，這個數字未必撐得過價格戰下一輪。
- **hit rate 95-98% 是個別用戶的自述**，不是官方統計。你的工作負載能拿到多少，取決於 prefix 設計，不能直接套用。
- **官方文件明說 cache 不保證命中**，「幾小時到幾天」的存活也是浮動描述，沒有 SLA。把它當成本優化可以，當成架構依賴不行。
- **qwen-code 案例是單一用戶的帳單**，量級小（日費用 $1 到 $3）。機制是真的，但放大到企業量級時，比例是否一樣，沒有公開數據。

這篇的核心論點——價差拉大之後帳單跟 miss rate 走——是算術，不依賴上面任何一條。但「你實際能省多少」高度依賴工作負載，別拿表格裡的 4 倍直接去跟老闆報告。

---

## 關鍵洞察

1. **帳單看 miss rate，不看 hit rate。** 50 倍價差下，hit rate 90% → 95% 不是「進步 5 個百分點」，是「miss 砍半、帳單近乎砍半」。跟可用性的「九」同一種數學。
2. **prefix stability 是成本工程，不只是工程潔癖。** 會動到 prompt 開頭的功能（動態工具載入、timestamp 注入）在 50 倍價差時代可能是負優化。上線前先算 miss rate 的帳。
3. **架構跟 serving 經濟學是一起設計的。** MLA 壓 KV → disk cache 落盤 → 50 倍定價，這條鏈的第一環在訓練時就決定了。看模型別只看 benchmark，看它的 KV cache 形狀。
4. **這不是 DeepSeek 的護城河，是產業的新地板。** 架構開源，時間差大約一個模型世代。合理預期是一年內「cache 接近免費、以天計存活」變成主流 API 標配——你的 harness 現在就該為這個世界設計。

---

## 延伸閱讀

### 一手來源

- [Artificial Analysis：DeepSeek V4 Flash 模型頁](https://artificialanalysis.ai/models/deepseek-v4-flash)
- [DeepSeek 給大模型劃出的「斬殺線」，斬的到底是什麼（愛範兒）](https://www.ifanr.com/1673651)
- [口碑持續逆轉，DeepSeek 成全球 AI 斬殺線（36 氪）](https://www.36kr.com/p/3923608861404550)
- [DeepSeek V4 Flash 0731 發布（MarkTechPost）](https://www.marktechpost.com/2026/07/31/deepseek-upgrades-deepseek-v4-flash-0731-with-major-agentic-and-coding-gains/)
- [DeepSeek 2024-08 disk context caching 原始公告](https://api-docs.deepseek.com/news/news0802/)
- [Simon Willison 對 disk caching 的解讀（2024-08）](https://simonwillison.net/2024/Aug/14/deepseek-context-caching/)
- [qwen-code cache hit rate 事件討論串](https://github.com/QwenLM/qwen-code/discussions/4065)
- [LMCache tiered storage 文件](https://docs.lmcache.ai/kv_cache/local_storage.html)

### 我之前寫過的相關文章

- [DeepSeek V4 把百萬 Token 上下文打到傳統 2% 成本——拆解 CSA + HCA](https://ai-coding.wiselychen.com/deepseek-v4-million-token-csa-hca-attention/) — 本文講的 50 倍定價，架構前提在這篇
- [一張原價屋估價單，看懂 Token 經濟學如何把 DDR 打到天價](https://ai-coding.wiselychen.com/ddr-hbm-token-economics-nvidia-lock-supply-chain/) — 記憶體層級的成本結構
- [搞懂快取機制，從 Gemma4 到 Claude Code 省 80% Token](https://ai-coding.wiselychen.com/kv-cache-gemma4-claude-code-save-80-percent-token/) — KV cache 基礎拆解

---

## 常見問題 Q&A

**Q：我用 Claude / OpenAI，這篇跟我有關嗎？**

有。prefix stability 的紀律在任何有 prompt caching 的 API 上都省錢，只是倍數不同（Anthropic 是 10 倍價差、5 分鐘 TTL）。而如果 50 倍價差如文中預期變成產業基準，現在養成的 harness 習慣等於提前佈局。

**Q：自架 vLLM + LMCache 不是更省？**

不同的帳。自架省的是 API 牌價，付的是 GPU 攤提跟維運。disk cache 對自架一樣有用（LMCache 的 SSD offload 就是幹這個的），但「hit 價格 = miss 的 2%」這種定價槓桿只存在於 API 側。量小用 API 吃 cache 折扣，量大到 GPU 利用率撐得起再自架，這個分界沒有因為 disk cache 改變。

**Q：怎麼知道我現在的 hit rate？**

DeepSeek API response 的 usage 欄位會回 prompt_cache_hit_tokens 和 prompt_cache_miss_tokens。抓下來除一下就有了。建議直接進 monitoring，當 SLO 看。
