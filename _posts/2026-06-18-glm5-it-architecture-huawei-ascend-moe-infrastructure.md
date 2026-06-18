---
layout: post
title: "GLM-5.2 出了，好評如潮：開源這次真的贏了"
date: 2026-06-18 08:00:00 +0800
permalink: /glm5-it-architecture-huawei-ascend-moe-infrastructure/
image: /assets/images/glm5-architecture-cover.png
description: "GLM-5.2 出了，社群好評如潮，能力落在 Opus 4.6-4.8 之間。X 上 Elon Musk 認為中國追到 Fable 5 級別大概在明年 Q1。在 Qwen 3.7 開源狀況不明朗的當下，它是目前最好的開源選擇之一——接近 SOTA、MIT 開源、可自部署。"
---

## 好評如潮

GLM-5.2 出了。智譜（Z.ai）四個月迭代三代（GLM-5 → 5.1 → 5.2），這次社群的反應用四個字可以概括：好評如潮。綜合多篇實測和社群反饋，能力大約落在 Opus 4.6-4.8 之間。

X 上有人盤算中美差距，Elon Musk 在那串討論裡回覆，認為中國追到 Fable 5 級別大概在明年 Q1——不是吹捧 GLM-5.2，是認真在盤算開源追上閉源前沿的時間點，而且比所有人預期的都快。

---

## 架構創新：為什麼能同時接近前沿又可部署

好評如潮，但背後是什麼撐起來的？GLM-5.2 能做到「接近前沿」又「企業用得起」，不是運氣，是五個架構選擇疊起來的結果。

**MoE 稀疏激活**：753B 總參數，但每個 token 只激活 40B（5.3% 稀疏度）。推理算力需求是 40B 級別，不是 753B 級別——這是「便宜」的技術基礎。但權重還是要全部載入記憶體（FP8 約 753GB，完整約 1.5TB），所以部署成本公式是「權重記憶體 753B 級別 + 推理算力 40B 級別」，兩個瓶頸不一樣。MoE 降算力門檻，不降記憶體門檻。

**DSA 稀疏注意力**：KV Cache 砍掉 75%，長文本能力損失不到 0.5%。對企業部署的直接影響是同一台機器並發量乘以四。在 2026 年 128GB DDR5 漲到 5.2 萬台幣、HBM 被 NVIDIA 鎖定的環境下，省記憶體比省算力值錢。原本需要 4 台 GPU 伺服器的並發量，現在 1 台就夠。

**IndexShare**：這是 GLM-5.2 從 200K 拉到 1M 上下文的關鍵。每 4 層 Transformer 共享一個注意力索引器，4 層裡只有 1 層需要算索引，其他 3 層直接複用。百萬 token 場景下 per-token FLOPs 降 2.9 倍。**DSA 省記憶體，IndexShare 省算力**——兩個疊起來讓超長上下文推理從「理論可行」變成「成本可行」。

**中國產晶片全棧**：10 萬張昇騰 910B 完成 28.5 兆 token 全量預訓練，不是跑 demo，是從零訓練。加上 7 家中國產晶片的推理適配——W4A8 混合精度量化、Lightning Indexer、13 個預處理算子融合成單一超級算子。不被任何一家晶片廠綁定，華為出問題還有寒武紀、海光。

**Slime 異步 RL**：把生成引擎和訓練引擎拆到不同 GPU 上完全異步運行，支援 1,000+ 並發 rollout。傳統 RL 訓練裡生成佔 90% 以上時間，GPU 大部分時候在等。Slime 讓兩邊不用互相等——這是「四個月能迭代三代」的訓練基礎建設。

五個架構選擇，對應撐起「接近前沿 / 可長上下文 / 可部署 / 迭代快」。

---

## GLM-5.2 的幾個優點

架構講完了，回到一個更實際的問題：對想用開源模型的人來說，GLM-5.2 到底好在哪？我列四個。

### 一、接近 SOTA，而且是真的開源

這是最核心的一點。FrontierSWE 74.4，差 Opus 4.8 的 75.1 只有一個百分點。Code Arena Frontend 全球第二（Elo 1,595），贏過所有 Opus 版本，僅次於 Fable 5。AIME 2026 達到 99.2，超過 Opus 4.8 的 95.7 和 GPT-5.5 的 98.3。

分數接近前沿這件事，過去 DeepSeek、Kimi 都做到過。**但 GLM-5.2 不只是分數接近，同時是 MIT 授權、753B 權重完整開放、不是蒸餾版不是閹割版。**

過去開源模型面對的困境是二選一：要嘛分數差一截（Llama 系列），要嘛分數接近但閉源或限制重重。GLM-5.2 是第一個把「接近 SOTA」和「真正開源」兩件事同時做到的。這不是又一次「中國模型又進步了」，是開源模型第一次站到跟閉源前沿同一個量級的位置。

### 二、MIT 開源，最寬鬆的授權

從 Apache-2.0 升級到 MIT——最寬鬆的開源授權。免費商用、可微調、可私有化部署、可二次開發。對資料不出內網的金融、醫療、政府單位，這是目前最強的自主可控選項。

開源不稀奇，Llama 系列一直在做。但 Llama 的授權有商用規模限制、有地區限制。MIT 是「你想怎麼用就怎麼用」，沒有但書。

### 三、可自部署，供應鏈替代

10 萬張華為昇騰 910B 完成全量預訓練，零 NVIDIA。再加上寒武紀、海光、摩爾線程等共 7 家中國產晶片的推理適配。在 GPU 供應不穩定、HBM 被 NVIDIA 鎖定、禁令隨時可能收緊的 2026 年，不被單一供應商綁定本身就是架構優勢。

這不是「供應鏈備案」——因為能力已經跟上來了，它是真的能上生產的選項。

### 四、Qwen 3.7 開源不明朗，它目前是最好的開源選擇之一

這點要放在開源生態的競爭裡看。千問（Qwen）系列一直是開源模型裡呼聲最高的，但 Qwen 3.7 目前的開源狀況並不明朗——權重放不放、什麼時候放、放什麼版本，都還不確定。

在這個真空期裡，GLM-5.2 是 MIT 開源、753B 權重完整開放、能力 Opus 4.6-4.8 級別。**如果你想現在就用一個接近前沿的開源模型，GLM-5.2 基本上沒有同級別的競爭對手。**

這不是說 Qwen 3.7 以後不會追上來。但在它開源狀況明朗之前，GLM-5.2 就是開源陣營目前最好的選擇之一，而且是現成可用、不是期票。

---

## 坦白講：還輸在哪

好評歸好評，但輸的地方還是要講清楚。

**最大短板：視覺多模態。** GLM-5.2 不是多模態模型，視覺識別靠注入的 tool，基本上看不懂圖上做的標註。如果你的 Agent 工作流需要看 UI 截圖、看設計稿、看報表，這就是硬傷，沒有「開源很強」可以抵銷。

**深度軟體工程還差一截。** DeepSWE 46.2，GPT-5.5 是 70.0——**差 24 個百分點**。NL2Repo 48.9，Opus 4.8 是 69.7——差 21 個百分點。在需要「從零生成完整 repo」和「深度軟體工程」的場景，差距是明顯的。

**超長時程任務穩定性不夠。** SWE-Marathon（超長任務）13.0，Opus 4.8 是 26.0——差一半。需要超長時程自主執行的 Agent 工作流，省下來的錢可能花在更多重試上。

**自部署門檻高。** 753B 權重約 1.5TB，需要多機分散推理，中小企業自架不現實。大型企業可以，中小企業走 API 更實際。

**社群預期 <50B 密集模型 2 個月內出現。** 如果成真，現在需要 1.5TB 記憶體的 753B MoE，可能在 50B 密集模型上就能跑——單機部署、成本再降一個量級。這對選型的意義是：**現在用 GLM-5.2 API 合理，但別為了自部署 753B 投資硬體，等 2-3 個月。**

---

## 收尾：開源追得比預期快

對 IT 架構師來說，這件事的意義不是「GLM-5.2 打贏了誰」。是這幾件事：

**第一，開源站到前沿位置了。** 接近 SOTA + MIT 開源 + 可自部署，三件事同時成立。過去「要不要用開源」是性價比問題，現在是戰略問題。

**第二，差距從模糊的「落後」變成可量化的時間。** Musk 說 Q1——這個數字代表一件事：閉源前沿的領先還在，但已經是「時間問題」而不是「能不能」的問題。

**第三，壓縮速度比採購速度快。** 現在用 GLM-5.2 是合理的。但如果你正在考慮投資硬體做 753B 自部署——等一等。社群預期 2 個月內 <50B 密集模型達到類似水準，到時候單張卡就能部署。

---

## 收尾：一邊封閉，另一邊機會就出現

正如我在 [Fable 5 那篇](https://ai-coding.wiselychen.com/fable-5-takedown-ai-export-control-precedent/)講過的，**只要有一邊趨向封閉，另一邊的機會就會出現。**

想想看智譜的股價為什麼在 GLM-5.2 出了之後突然漲了一倍？原因在於：隨著美國的模型越來越封閉，市場認可了一件事——一定會有一票 To B 的客戶希望尋找開源的替代方案。

在這種情況下，如果有一個模型能夠接起 SOTA 的大旗，很多企業是會用真金白銀去支持的。GLM-5.2 現在就是那個接旗的人。

而有了這些 To B 客戶以及股票資金的支持之後，這些資源會持續推向一個已經證明自己、幾乎每兩個月就能推出一個新模型的團隊。**封閉推著客戶往外跑，開源接住這些客戶，資金回流再加速開源——這是一個自我強化的飛輪。**

GLM-5.2 確實強。但更值得關注的不是它多強——**是這個飛輪一旦轉起來，開源追趕的速度只會越來越快。**

---

## 參考資料

**X 討論**
- [Elon Musk @elonmusk — Probably Q1（中國追到 Fable 5 級別的時間線）](https://x.com/elonmusk)

**社群實測與評價**
- [r/ClaudeAI: GLM 5.2 via Claude Code is the first non-Claude model that feels like a legitimate contender to Opus 4.8](https://www.reddit.com/r/ClaudeAI/comments/1u8pycz/)
- [DMXAPI 運營日誌：glm-5.2-cc 上線（Claude Code 接口格式）](https://dmxapi.cn/)

**官方與技術報告**
- [GLM-5.2 官方 Blog — Built for Long-Horizon Tasks（HuggingFace）](https://huggingface.co/blog/zai-org/glm-52-blog)
- [GLM-5 技術報告：From Vibe Coding to Agentic Engineering（arXiv:2602.15763）](https://arxiv.org/abs/2602.15763)

**相關評測與對比**
- [GLM-5.2 Benchmarks: Open Weights vs Claude Opus 4.8（Digital Applied）](https://www.digitalapplied.com/blog/glm-5-2-benchmarks-open-weights-vs-claude-opus)
- [GLM-5.2 實測：開源新皇，中國產模型裡離 Opus 最近的一個（302.AI）](https://302.ai/blog/302-ai-benchmark-lab-review-on-glm-5-2/)
- [AINews: GLM-5.2 — the top Frontend Coding model, IndexShare for Speculative Decoding（Latent Space）](https://www.latent.space/p/ainews-glm-52-the-top-frontend-coding)
- [GLM-5.2 Goes Fully Open: 753B Parameters Beat GPT-5.5 at 1/6 the Cost（StableLearn）](https://stablelearn.com/en/glm-5-2-open-source-release/)

**作者相關文章**
- [五天前的懷疑判決：智譜 GLM-5.2——1M Context、全華為晶片、MIT 開源，但跑分表呢？](https://ai-coding.wiselychen.com/glm-5-2-zhipu-1m-context-no-benchmark-open-source/)
- [GLM-5.2：華為晶片訓練的 744B 開源模型，1M Context 直接挑戰 Claude Code](https://ai-coding.wiselychen.com/glm-5-2-zhipu-1m-context-agentic-coding-huawei-ascend/)
