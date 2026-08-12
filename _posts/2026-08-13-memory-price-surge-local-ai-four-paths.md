---
layout: post
title: "5090 三個月從 10 萬變 17 萬：五條技術路徑壓低地端 AI 的硬體門檻"
date: 2026-08-13 09:00:00 +0800
permalink: /memory-price-surge-local-ai-five-paths/
image: /assets/images/memory-price-surge-local-ai-cover.png
description: "五月估的地端推理機約 10 萬台幣，週二再問同配置變 17 萬。RTX 5090 從首發 MSRP $1,999 漲到官方商店 $4,929。同一時間開源模型密集釋出——DeepSeek V4 Flash、Qwen 3.8 Max/27B、MiniMax H3、Meta Muse Glimmer。硬體在漲，但軟體側的武器也在同步增加。這篇整理五條具體的技術路徑：選對模型、KV 落盤、量化壓縮、MoE offload、agent 編排搭配特化小模型。"
---

五月我估了一台跑地端推理的機器，大概 10 萬台幣出頭。

週二晚上順手再問一次同配置。17 萬。

我以為報錯了，看了兩遍。三個月，同一張單子，多了 70%。

然後去看新聞才知道不是我一個人。8 月初[欣亞數位對媒體說](https://tw.stock.yahoo.com/news/%E8%A8%98%E6%86%B6%E9%AB%94%E5%86%8D%E5%82%B3%E6%BC%B2%E8%81%B2-nvidia-%E9%A1%AF%E5%8D%A1-%E8%AA%BF%E6%BC%B220-%E6%B6%88%E8%B2%BB%E8%80%85%E6%80%A5%E4%B8%8B%E5%96%AE-024100152.html)，NVIDIA RTX 5060 系列以上調漲 10-20%，記憶體可能跟進。32GB DDR5 從約 3,000 元漲到近 13,000 元。中階桌機去年 36,000 元，現在接近 60,000。上週末全台組裝訂單量比前一週翻了一倍——大家都在搶。

國際同步：[MSI 跟進 ASUS 和技嘉調漲超過 20%](https://wccftech.com/msi-raises-graphics-card-prices-by-over-20-percent/)，對投資人說 2026 全年遊戲硬體漲 15-30%，NVIDIA GPU 供給缺口約 20%。RTX 5090 在 [NVIDIA 官方商店掛 $4,929.99](https://www.buysellram.com/blog/nvidia-consumer-gpu-price-report-august-2026/)，2025 年 1 月首發 MSRP 是 $1,999。[韓國零售最高喊到約 730 萬韓元（≈$5,112），一個月內漲了約 150 萬韓元](https://www.techtimes.com/articles/320169/20260711/gpu-memory-crisis-prices-rtx-5090-above-4300-nvidia-offers-paper-cards.htm)。

漲價的根源我四月在[原價屋估價單那篇](https://ai-coding.wiselychen.com/ddr-hbm-token-economics-nvidia-lock-supply-chain/)拆過：AI 資料中心吃掉 HBM 產能，[記憶體佔顯卡物料成本超過 80%](https://www.astutegroup.com/news/general/gpu-pricing-set-for-reset-as-ai-driven-memory-shortages-push-costs-sharply-higher/)，TrendForce 預估要到 2027-2028 年供給才正常化。**這不是等一下就回落的事。**

---

但同樣這十天，開源模型在密集釋出：

- **7/31** DeepSeek V4 Flash 0731 上線——284B MoE、每 token 激活 13B、MIT 開源、[性價比斬殺線](https://ai-coding.wiselychen.com/deepseek-v4-flash-disk-kv-cache-50x-economics/)
- **8/3** [Qwen3.8-Max](https://dataconomy.com/2026/08/03/qwen3-8-max-ai-model/)——2.4T MoE、95B 激活、首次開源 Max 級權重，[Qwen3.8-27B 排在週五](https://www.latent.space/p/ainews-qwen-38-max24t-and-27b-new)。社群這幾天都在倒數等 27B，結果 Max 先上
- **8/3** [MiniMax H3](https://www.opensourceforu.com/2026/08/minimax-releases-h3-multimodal-ai/)——33B dense 統一多模態，文字/圖像/影片/音訊一個架構出，2K 影片，宣布數日內開源權重。[第三方已在單張遊戲 GPU 跑出 Seedance 2.0 等級的影片生成](https://xhinker.medium.com/minimax-h3-i-ran-a-seedance-2-0-video-gen-model-in-one-gaming-gpu-68680a12e86c)
- **8/10** [Meta Muse Glimmer](https://venturebeat.com/technology/meta-returns-to-open-source-with-muse-glimmer-an-apache-2-0-licensed-30b-parameter-ai-model-optimized-for-agents-available-now)——30B、Apache 2.0、agent 最佳化，[4-bit 量化不到 20GB，一張消費卡或 Mac 就能跑](https://www.engadget.com/2233312/metas-open-source-muse-glimmer-model-can-run-on-a-single-computer/)

硬體在漲，軟體側的武器也在同步增加。問題不是「漲了怎麼辦」，是「手上有哪些技術路徑能把硬體門檻壓下來」。

以下五條。

---

## 一、先選對模型，才決定買什麼硬體

這條不是技術，是決策順序。但它決定後面四條路省下來的東西有沒有意義。

五月的想法是：先把硬體天花板拉高，VRAM 越大越好、RAM 上 128GB 起跳，反正記憶體便宜。先買硬體，再挑模型。

八月不能這樣了。DDR5 漲了四倍，每一個多買的 GB 都有實際的價差在那裡。

現在的順序應該是：先問你的 workload 需要哪一級的模型——27B-35B dense 夠用嗎？還是非得上 284B 的 MoE？模型定了之後，才知道需要多少 VRAM 和 RAM。

幾個具體的對照點：

- **文字 coding agent**：[Qwen 3.6 27B](https://ai-coding.wiselychen.com/qwen-3-6-27b-sonnet-level-home-inference/) 在 DGX Spark 上跑 136 tok/s，benchmark 打贏 Opus 4.5。4-bit 量化約 16-17GB。一張 24GB 的上一代消費卡就收工。
- **影片生成**：MiniMax H3 是 33B dense，第三方在單卡上跑起來了。不用 A100。
- **企業級 agentic 任務**：DeepSeek V4 Flash，284B MoE，但激活只有 13B。IQ2 量化 85GB 可以塞進 96GB VRAM 的單卡。我七月[實測過](https://ai-coding.wiselychen.com/rtx-pro-6000-tier1-week-final-offload-qwen-vl-vllm/)，58 tok/s，五題基準跟 Q8 同分。
- **輕量 agent 雜務**：Muse Glimmer 30B，4-bit 不到 20GB。Mac 就能跑。

27B 級的模型 4-bit 量化後 15-20GB。選這個級距，你避開的是整個「為了大模型而生的硬體採購」——不用四條 DDR5（現在一條近 13,000 元）、不用專業卡。省的不是一點錢，是一整個硬體等級。

---

## 二、DeepSeek 路線：KV cache 落盤到 SSD

LLM 推理佔記憶體的不只是模型權重，還有 KV cache——每個 token 的 attention 中間結果。Agent 的 context 結構是「一大坨穩定 prefix（系統 prompt + 工具定義 + codebase）加一小段增量」，反覆使用。這份 KV cache 沒必要一直佔著最貴的 VRAM。

DeepSeek 的做法：把 KV cache 落進分散式硬碟陣列，cache hit 的價格開到 miss 的 2%（$0.0028 vs $0.14 per 1M tokens），50 倍價差。前提是 MLA 先把 KV cache 壓小 93%，落盤的 I/O 才撐得住。完整拆解在[上一篇](https://ai-coding.wiselychen.com/deepseek-v4-flash-disk-kv-cache-50x-economics/)。

地端的對應方案是 [LMCache 的 SSD offload](https://docs.lmcache.ai/kv_cache/local_storage.html)——把算過的 KV cache 存到本機 SSD，跨 session 重用。SSD 也在漲（2 千到 5 千），但在整條記憶體階層裡它是漲幅最平緩、單價最低的一層。

這條路線的意義：同一份 codebase 的 context，你讓它住 SSD 而不是 VRAM，等於用每 GB 幾塊錢的儲存換每 GB 幾百塊的記憶體。跑 Agent 反覆回來看同一份程式碼的場景，省的量很可觀。

---

## 三、量化壓縮：Q4、2-bit、1-bit

最直接的一條：Q8 → Q4 → 2-bit → 1-bit，每砍一半 bits，記憶體需求砍一半。

2026 年這條路線進展很快。[Unsloth 的 dynamic quant 把 DeepSeek-V3.1 從 671GB 壓到 192GB（1-bit）](https://unsloth.ai/blog/deepseek-v3.1)，宣稱表現仍勝過 GPT-4.5——這是廠商自己的數字，要打折看。但同一篇也記了對照組：非動態的 1-bit、2-bit 量化直接輸出亂碼。**動態分層**（關鍵層留高精度、MoE 層砍到見骨）是這條路走通的原因。

我自己的實測結論：DeepSeek V4 Flash IQ2 量化 85GB，整包塞進 96GB VRAM，58 tok/s，五題基準跟 Q8 完全同分。**「能整包塞進 VRAM 的小量化」勝過「塞不下的大量化」**。

但要記得 [Bonsai 27B 的教訓](https://ai-coding.wiselychen.com/bonsai-27b-qwen36-compression-local-inference/)：壓縮損失不均勻。Qwen 3.6 27B 壓到 1-bit，MATH 500 從 99.4 只掉到 98，TauBench（tool calling）卻從 82.9 掉到 61.3。**跑 chat 感覺不到差，跑 agent 會翻車。** 量化之後一定要測 tool calling，那是最先受傷的能力。

---

## 四、MoE expert offload 到 DRAM

MoE 模型每個 token 只激活一小撮 expert，其他權重閒著。llama.cpp 的 [`--n-cpu-moe`](https://huggingface.co/blog/Doctor-Shotgun/llamacpp-moe-offload-guide) 把 expert FFN 權重丟進系統 RAM，attention 留 GPU。冷資料住便宜的層，熱路徑住貴的層。

七月的一週實測：GLM 5.2（753B、222GB 檔案）在 96GB VRAM 單卡機上跑起來了，VRAM 只佔 23.5GB。但天花板釘死在 ~10 tok/s，瓶頸是 CPU 記憶體頻寬。DeepSeek V4 Flash 同樣 offload 模式快一倍以上（25 tok/s），因為每 token 激活量 13B，GLM 要 40B。

**激活量決定每個 token 從 DRAM 搬多少權重，也決定了 offload 之後剩多少速度。** 所以這條路線回到第一條——你選的模型激活量越小，offload 越划算。DeepSeek V4 的 MoE 架構從設計之初就在為這個場景做準備。

DDR 自己也在漲，這個套利不是免費的。但 DDR 每 GB 仍然比 GDDR 便宜一個量級，空間還在。實務判斷點在速度：offload 之後的 tok/s 你能不能接受。批次任務可以，互動式 agent 很勉強。

---

## 五、Agent / harness 編排：一些特化小模型組合起來

前四條都在處理「一顆模型怎麼用更少記憶體跑」。第五條換一個問題：**你真的需要每一步都跑同一顆大模型嗎？**

一個 Agent 工作流裡不是每一步都需要 frontier 級的智力。routing、分類、格式轉換、簡單的 code generation——這些用 7B-13B 的特化模型就夠了，只有需要複雜推理的步驟才呼叫大模型。

具體的做法：

- **routing 層**：一個 7B 模型做意圖分類，決定任務要派給哪顆模型。這一步不需要高智力，需要的是快和穩定。
- **特化小模型**：程式碼格式化用 code-specific 的 13B，文件摘要用另一顆，影像理解用 VLM。每顆只載入自己那段任務，跑完就釋放 VRAM。
- **大模型只跑最後一哩**：複雜推理、長 horizon planning、需要 1M context 的任務，才派給 V4 Flash 或 Qwen 3.8 Max（走 API 或 offload）。

這個做法在記憶體貴的時候特別有意義：你不用同時在 VRAM 裡養一顆 85GB 的模型待命。多數時間在跑 15GB 以下的小模型，偶爾才載入大模型——或者直接把大模型的步驟丟給 API。

Muse Glimmer 30B 的定位正好卡在這裡：Apache 2.0，agent 最佳化，20GB 以下。它不是要取代 V4 Flash 的全部能力，是要扛住「不用 frontier 也能做」的那 80% 任務量。

---

## 坦白說

- 10 萬變 17 萬是單一店家、單一配置、單一時點的報價，不是市場統計。零售價波動很大，你拿到的數字可能不同。
- 這五條路線的代價都是真的：量化壓 1-bit 之後 tool calling 掉 21 分（Bonsai 實測）；offload 天花板 10 tok/s 跑互動式 agent 是煎熬。省的是硬體錢，不是免費午餐。
- 截稿時 Qwen3.8-27B 和 MiniMax H3 的權重還沒放出來。開源承諾和權重在手是兩回事。
- Agent 編排聽起來漂亮，但 routing 層本身的準確率、模型切換的延遲、harness 的工程複雜度，都是實作後才會碰到的坑。這條路線目前我自己還在試，沒有像前四條一樣有完整的實測數據。

---

## 關鍵洞察

1. **買硬體之前先選模型。** 27B 級 4-bit 量化後 15-20GB，跟 284B 的 85GB 差了四倍以上。選錯級距多花的錢，在漲價時代是四月的好幾倍。

2. **量化是最快見效的路線，但記得測 tool calling。** Q4 到 2-bit 能砍掉一半記憶體需求，而且 llama.cpp 生態現成可用。代價是 agent 能力先受傷。

3. **MoE offload 和 KV 落盤都在把 bytes 往便宜的層搬。** 一個搬模型權重到 DDR，一個搬 context 到 SSD。漲價讓兩邊的價差更大，套利空間反而拉開了。

4. **不是每一步都需要大模型。** Agent 編排 + 特化小模型組合，能讓你多數時間只佔 15GB 以下的 VRAM，把大模型留給真正需要的步驟。

---

## 延伸閱讀

### 一手來源

- [記憶體再傳漲聲 NVIDIA 顯卡調漲 20%（Yahoo 股市）](https://tw.stock.yahoo.com/news/%E8%A8%98%E6%86%B6%E9%AB%94%E5%86%8D%E5%82%B3%E6%BC%B2%E8%81%B2-nvidia-%E9%A1%AF%E5%8D%A1-%E8%AA%BF%E6%BC%B220-%E6%B6%88%E8%B2%BB%E8%80%85%E6%80%A5%E4%B8%8B%E5%96%AE-024100152.html)
- [MSI 顯卡調漲逾 20%（Wccftech）](https://wccftech.com/msi-raises-graphics-card-prices-by-over-20-percent/)
- [RTX 5090 零售價衝破 $4,300（TechTimes）](https://www.techtimes.com/articles/320169/20260711/gpu-memory-crisis-prices-rtx-5090-above-4300-nvidia-offers-paper-cards.htm)
- [Qwen3.8-Max 發布（Dataconomy）](https://dataconomy.com/2026/08/03/qwen3-8-max-ai-model/)
- [MiniMax H3 發布（Open Source For You）](https://www.opensourceforu.com/2026/08/minimax-releases-h3-multimodal-ai/)
- [Meta Muse Glimmer 發布（VentureBeat）](https://venturebeat.com/technology/meta-returns-to-open-source-with-muse-glimmer-an-apache-2-0-licensed-30b-parameter-ai-model-optimized-for-agents-available-now)
- [Unsloth DeepSeek-V3.1 dynamic quant](https://unsloth.ai/blog/deepseek-v3.1)
- [llama.cpp MoE offload 指南（Hugging Face blog）](https://huggingface.co/blog/Doctor-Shotgun/llamacpp-moe-offload-guide)

### 我之前寫過的相關文章

- [一張原價屋估價單，看懂 Token 經濟學如何把 DDR 打到天價](https://ai-coding.wiselychen.com/ddr-hbm-token-economics-nvidia-lock-supply-chain/) — 這波漲價的結構性成因
- [單機跑 Tier 1 地端 Model 一週實驗完賽](https://ai-coding.wiselychen.com/rtx-pro-6000-tier1-week-final-offload-qwen-vl-vllm/) — offload 天花板與量化甜蜜點的第一手數據
- [DeepSeek V4 Flash 為何那麼強：disk KV cache 的 50 倍經濟學](https://ai-coding.wiselychen.com/deepseek-v4-flash-disk-kv-cache-50x-economics/) — KV 落盤的完整拆解
- [Bonsai 27B：55.6GB → 3.9GB 保留 90% 智力](https://ai-coding.wiselychen.com/bonsai-27b-qwen36-compression-local-inference/) — 量化損失不均勻的證據
- [Qwen 3.6-27B 本地部署：跑出 Sonnet 4.6 等級](https://ai-coding.wiselychen.com/qwen-3-6-27b-sonnet-level-home-inference/) — 27B 級距能打的第一手驗證
