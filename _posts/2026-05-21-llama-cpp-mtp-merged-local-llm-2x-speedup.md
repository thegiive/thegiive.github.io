---
layout: post
title: "llama.cpp 終於合併 MTP：你的 DeepSeek / Qwen3.6 一直少跑了 30-60% 的速度"
date: 2026-05-21 06:30:00 +0800
permalink: /llama-cpp-mtp-merged-local-llm-2x-speedup/
image: /assets/images/llama-cpp-mtp-merged-cover.png
description: "2026 年 5 月 16 日，llama.cpp 合併了等了快一年的 PR #22673：Multi-Token Prediction（MTP）支援。Reddit 上 776 個讚的慶祝畫面背後，是一個比較尷尬的事實——你手上那顆 DeepSeek-V3 GGUF，過去整整一年都在 single-token 模式下硬跑，模型內建的加速器一直沒有被按下去。"
---

![llama.cpp merges MTP: local LLM 2.5x speedup unlocked](/assets/images/llama-cpp-mtp-merged-cover.png)

## 目錄

- [TL;DR](#tldr)
- [那則 776 讚的 Reddit 截圖，慶祝的是什麼](#那則-776-讚的-reddit-截圖慶祝的是什麼)
- [MTP 到底是什麼？一句話版本](#mtp-到底是什麼一句話版本)
- [三組硬體實測：2.5x、1.71x、74%](#三組硬體實測25x171x74)
- [為什麼速度沒有翻三倍：72% 的接受率](#為什麼速度沒有翻三倍72-的接受率)
- [反直覺洞察：你的 GGUF 一直跑半速](#反直覺洞察你的-gguf-一直跑半速)
- [誠實揭露：MTP 不是免費午餐](#誠實揭露mtp-不是免費午餐)
- [最大受益者其實不是 NVIDIA 用戶——是 Mac](#最大受益者其實不是-nvidia-用戶是-mac)
- [對企業 on-prem 架構師意味著什麼](#對企業-on-prem-架構師意味著什麼)
- [常見問題 Q&A](#常見問題-qa)

## TL;DR

- **2026-05-16，llama.cpp PR #22673 合併**，原生支援 Multi-Token Prediction（MTP）speculative decoding
- 社群實測：DGX Spark 跑 Qwen3.6-27B **7.0 → 18.0 tok/s，2.57x**；RTX 3090 **38.86 → 65 tok/s，1.71x**
- **我自己在 RTX 5090 上實測 Qwen3.6-27B + MTP 拿到 140 tok/sec 單流、70%+ acceptance rate**，跟 PR 描述的 72.18% 幾乎重疊
- **這次 PR 真正的最大受益者其實是 Mac 用戶**——vLLM / SGLang / TensorRT-LLM 永遠不會支援 Apple Silicon，Mac 用戶過去 16 個月想用 MTP「沒有任何一條路」。詳見另一篇 [Mac 用戶等了 16 個月：第一次能用「企業級」LLM 推理加速](https://ai-coding.wiselychen.com/mac-first-enterprise-inference-stack-mtp/)
- 不是「新模型」新聞，是「inference 框架終於追上模型架構」的新聞——DeepSeek-V3 從 2024 年底就有 MTP heads，**本地用戶等了快一年才能真正按下這個按鈕**
- 限制：只對「訓練時就帶 MTP head」的模型有效（DeepSeek-V3/R1、Qwen3.6 系列），而且目前 `n_parallel=1`，多用戶場景 vLLM + AWQ 還是壓倒性勝利

---

## 那則 776 讚的 Reddit 截圖，慶祝的是什麼

事情是這樣的。

5 月 16 日，r/LocalLLaMA 上有人貼了一張 PR 已 merge 的截圖，標題寫 "That's a good news..."，內文只有兩句話：

> "Looks like it finally happens... MTP getting approved for llama.cpp. Time to prepare for the update."

兩天內 776 upvotes、242 條留言。對一個技術 PR merge 的反應來說，這個熱度是不太尋常的。

但你要理解為什麼大家這麼激動，得先回到 2024 年底——DeepSeek-V3 release 的那一刻，模型架構裡就已經內建了 MTP heads，官方論文宣稱可以拿到 **1.8x** TPS 加速。

問題是，這個能力**只有 DeepSeek 自己的 inference 伺服器跟 SGLang / vLLM 用得起來**。本地用 llama.cpp 跑 GGUF 的人，等於拿了一台跑車但沒拿到鑰匙。

整整一年。

5 月 16 日，鑰匙終於發下來了。

## MTP 到底是什麼？一句話版本

**MTP = 模型自己當自己的 draft model。**

過去要做 speculative decoding，你得跑「大模型 + 小模型」兩顆——小模型先猜幾個 token，大模型驗證。聽起來合理，但實務上很煩，因為你要為每個大模型找一顆「夠像但夠小」的搭檔。

MTP 的做法是：訓練時就在大模型裡多裝幾個 prediction head，讓它一次 forward pass 就能吐出「下一個 token + 接下來幾個草稿 token」。然後主模型自己驗證自己的草稿。

對使用者來說，這意味著：
- 不用找 draft model
- 不用多載一份 KV cache（雖然實作上 MTP head 還是有自己的 context）
- 接受率比外掛 draft model 高很多，因為這些草稿頭是「同一個模型自己的延伸」

llama.cpp 的開法很簡單：

```bash
--spec-type mtp --spec-draft-n-max 3
```

第二個參數是草稿幾個 token，社群目前測下來 **3 是個甜蜜點**。

## 三組硬體實測：2.5x、1.71x、74%

這是這次最有意思的部分——同一個 feature 在不同硬體上加速幅度差很大。

| 硬體配置 | 模型 | Baseline | MTP 開啟 | 加速倍率 |
|---------|------|---------|---------|---------|
| **DGX Spark**（$4,699 家用 AI 工作站）| Qwen3.6-27B | 7.0 tok/s | 18.0 tok/s | **2.57x** |
| **RTX 3090** | Qwen3.6-27B | 38.86 tok/s | 65-67 tok/s | **1.71x** |
| **3x RTX 3060**（社群實測）| Qwen3.6-27B | - | - | **+74%** |
| **SGLang + AMD MI300**（DeepSeek-V3，非 llama.cpp）| - | - | - | 1.25-2.11x（Random）/ 1.36-1.80x（ShareGPT）|

幾個觀察：

**第一，記憶體頻寬瓶頸越嚴重的機器，加速越誇張。** DGX Spark 拿 2.57x 的原因是它本來就是頻寬瓶頸機（128GB 統一記憶體但頻寬不如 RTX 3090），MTP 等於把「同一次 memory access 多算幾個 token」的紅利吃滿。

**第二，RTX 3090 從 38 → 65 tok/s 不算誇張，但意義很大。** 因為 27B 在消費卡上本來就接近實用門檻，1.71x 等於從「勉強用」變成「順順用」。

**第三，SGLang 跑 DeepSeek-V3 的 1.25-2.11x 區間揭露了一個重點：concurrency 越高，MTP 加速越小**。AMD 那邊測 1、2、4、8、16、32、64 user 的場景，倍率是遞減的——這也是為什麼 llama.cpp 目前的實作直接強制 `n_parallel=1`。

## 為什麼速度沒有翻三倍：72% 的接受率

PR 描述裡有一個關鍵數字：**Aggregate acceptance rate 72.18%**。

意思是：模型每草稿 3 個 token，平均有 2.16 個會通過自己的驗證、被接受寫入輸出。剩下的 0.84 個被丟掉、重算。

這就是為什麼你看到的加速是 1.7x ~ 2.5x，不是 3x ~ 4x：

```
理論上限 = 1 + n_draft × acceptance_rate
        = 1 + 3 × 0.72
        = 3.16x（不含驗證 overhead）

實際 = 約 1.7x ~ 2.5x（含驗證跟 KV 寫入 overhead）
```

接受率為什麼是 72% 不是 95%？因為 MTP head 雖然跟主模型同源，但它預測「未來 N 個 token」的時候只看到當下的 hidden state——本質上還是一個近似。

這也呼應到一個有意思的點：**任務越「可預測」，加速越大**。寫 boilerplate code、補全 API call 這種 acceptance rate 會接近 80-85%；寫複雜推理或創意文字會掉到 60% 以下。

DataCamp 那篇 tutorial 實測就觀察到，跑 AIME 數學題的時候速度從 65 tok/s 掉回 56-61 tok/s——還是比 baseline 快，但加速幅度縮水。

## 反直覺洞察：你的 GGUF 一直跑半速

這篇文章真正想講的是這件事。

過去一年，本地 LLM 圈花很多時間在優化「能跑哪些模型」、「量化能壓多狠」、「kernel 能調多快」。所有這些優化都在原本的 single-token autoregressive 框架裡卷。

但事實是：**DeepSeek-V3 / Qwen3.6 這幾顆主流開源大模型，從訓練的第一天就準備好了 multi-token 模式**。權重裡的 MTP heads 一直躺在你硬碟上，只是 llama.cpp 不知道怎麼讀。

換個說法：

- 如果你 2025 年 1 月 download 了 DeepSeek-V3 GGUF 開始本地推理
- 到 2026 年 5 月 16 日為止，**你大概率一直在跑半速**
- 不是你的硬體不夠，不是你 prompt 寫得不好，不是量化太狠
- 是 inference 框架沒實作這個功能

這個 gap 大概有 16 個月。

對企業 IT 架構決策來說這件事的啟示是：**模型架構的進度跟 inference 框架的進度，從來不是同步的**。當你算 on-prem AI Coding 的 ROI 時，你算的是「今天的軟體跑今天的硬體跑今天的模型」這個快照——但那個快照六個月後可能因為一個 PR merge 就翻一倍。

### 把這件事接回我自己手上的數字

這次 PR merge 對我有點不一樣，因為我**已經在 RTX 5090 上實測過 MTP 了**——上一篇 [Qwen 3.6-27B 在 RTX 5090 上的 inference engine benchmark](https://ai-coding.wiselychen.com/qwen-3-6-27b-rtx-5090-inference-engine-benchmark/) 跑了 7 組配置，其中一組就是 llama.cpp + Q2_K_XL + MTP，結果如下：

| 配置 | 單流（1 user） | 並發（8 users）|
|------|--------------|--------------|
| vLLM + AWQ-INT4 + cudagraph | 80.5 tok/s | **575 tok/s** ⭐ |
| **llama.cpp + Q2_K_XL + MTP** | **140 tok/s** ⭐ | 118 tok/s |
| llama.cpp + Q4_K_M（無 MTP）| 75 tok/s | 189 tok/s |
| Ollama + Q4_K_M | 67 tok/s | 64 tok/s |

幾個對照重點：

**第一，PR 描述的 acceptance rate 72%，我實測到 70%+**——兩個數字幾乎重疊，這驗證了 MTP head 的品質在不同硬體 / quant 設定下相當穩定，不是 cherry pick 出來的數字。

**第二，單流 140 tok/sec 跟同模型 llama.cpp Q4_K_M 無 MTP 的 75 tok/sec 對比，加速約 1.87x**——落在前面講的 1.7x-2.5x 區間，跟 PR 報的 RTX 3090 上 1.71x 接近。

**第三，並發場景的 trade-off 在這張表上一目了然**：
- vLLM 在 8 users 並發拉到 575 tok/s（continuous batching 的紅利）
- 但 llama.cpp + MTP 並發反而從 140 掉到 118 tok/s——這就是前面說的 `n_parallel=1` 限制具體長什麼樣

換句話說：**MTP 不是「一定贏」的優化**。如果你的場景是 single-stream interactive coding（工程師一個 session 對話），MTP 是免費午餐；如果是 batch inference / 多用戶 API server，vLLM + AWQ 還是壓倒性勝利。

**第四，140 tok/sec 單流是什麼概念？** Sonnet 4.6 透過 API 拿到的 streaming 速度大概 60-80 tok/sec（看時段跟 region）。**一張 RTX 5090（市價 $2,000 美金等級）跑 Qwen3.6-27B 開 MTP，單流速度直接是 Anthropic API 的 1.75 倍**——而且沒有網路 round-trip、沒有共用佇列、沒有 rate limit。

## 誠實揭露：MTP 不是免費午餐

寫到這裡得潑點冷水。

**1. 不是所有模型都能用**

只有「訓練時就帶 MTP heads」的模型才能開。目前確認支援的：

- DeepSeek-V3、DeepSeek-R1（包含 distill 版本）
- Qwen3.6-27B、Qwen3.6-35BA3B

Llama 3 系列、Mistral、Gemma 這些**沒有 MTP head**，這個 PR 對它們沒用。你只能繼續走傳統 speculative decoding（找一顆 draft model）那條路。

**2. 目前 server 多用戶場景不能用**

PR merge 後的版本強制 `n_parallel=1`。如果你的 on-prem 架構是「一台機器服務十個工程師」，這個 feature 暫時還不適合你。社群在討論 batching 支援，但需要時間。

**3. Acceptance rate 變數很大**

前面講過，任務越創意 / 越長 reasoning，acceptance rate 掉得越凶。如果你的 workload 主要是長 reasoning chain（agentic coding 中後段、複雜數學），實際加速可能只有 1.3x ~ 1.5x。

**4. 多了 device-to-host embedding transfer overhead**

PR 描述裡明寫了，prompt processing 階段會多一份 embedding 傳輸成本。short prompt + long generation 場景拿到最大紅利，long prompt + short generation 場景紅利會被吃掉。

## 最大受益者其實不是 NVIDIA 用戶——是 Mac

寫到這裡有一個視角必須補上，因為它跟「能拿到多少加速倍率」這個技術問題其實是分開的。

NVIDIA 用戶這次的故事是「**從用 vLLM 麻煩變成用 llama.cpp 輕鬆**」——本來門就是開的，只是要走樓梯，現在多了一個電梯。

但 Mac 用戶的故事完全不一樣，是「**從鎖死變成打開**」。

具體講：

| 推理棧 | NVIDIA 卡 | Mac (Apple Silicon) |
|--------|---------|---------|
| vLLM + MTP | ✅ 早就支援（2025 初）| ❌ 完全跑不了（沒 CUDA）|
| SGLang + MTP | ✅ 早就支援 | ❌ 完全跑不了 |
| TensorRT-LLM + MTP | ✅ NVIDIA 獨家 | ❌ 永遠不會支援 |
| **llama.cpp + MTP（2026-05-16）** | ✅ **新解鎖** | ✅ **新解鎖** |

對 NVIDIA 用戶：MTP 在 2025 年初就能用了，只是要會起 vLLM。

對 Mac 用戶：**過去 16 個月「沒有任何一條路」能用到 MTP**——llama.cpp 沒做、Ollama / LM Studio 跟在 llama.cpp 後面、MLX 也沒做、Apple 自己也沒做。

更有意思的是，從**記憶體頻寬論證**來看，Mac Studio 拿到的 MTP 紅利應該**大過 RTX 5090**——因為 MTP 的核心紅利是「同一次 memory access 算多個 token」，越是頻寬 bound 的硬體越受惠。Apple Silicon 統一記憶體架構天生就是頻寬 bound。

這個推論細節跟 Mac 視角的完整論證，我寫在另一篇：[Mac 用戶等了 16 個月：第一次能用「企業級」LLM 推理加速](https://ai-coding.wiselychen.com/mac-first-enterprise-inference-stack-mtp/)。

對 IT 架構師來說，這意味著一件具體的事：**公司本來就配 Mac 給工程師的，Mac Studio M3 Ultra 256GB 本身就可以變成一台單人推理 server**——不用再買 NVIDIA 工作站。

## 對企業 on-prem 架構師意味著什麼

我們團隊在做企業 on-prem AI Coding 評估的時候，這次 PR merge 大概會改變三件事：

**1. 重新算成本模型**

如果你的 on-prem 架構評估是 6 個月前做的，數字幾乎肯定過時。一台跑 Qwen3.6-27B 的機器，throughput 帳面上要加 1.7x ~ 2.5x。這個倍率落到每月帳上會很可觀。

**2. 重新看模型選型**

過去選 Llama 3 系列或 Mistral 的，現在要回頭看 DeepSeek / Qwen3.6——不只是因為 benchmark 數字，是因為它們**架構上就比較適合本地推理**。MTP heads 是這個差距的具體表現。

**3. 重新評估 inference 框架的 release cadence**

llama.cpp 不是慢，是它要支援的硬體 / OS / 模型架構組合太多。如果你的公司在押本地推理，要把「inference 框架的 feature roadmap」當成跟模型 release 同等重要的觀察對象——這次的 MTP 是一個例子，下次可能是某個新的 attention kernel。

換個方式講：**選 on-prem 不只是選模型，是選一個三條時間線的交集**——模型 release、inference 框架 feature、硬體更新。任何一條突進，整個 ROI 公式都要重算。

## 常見問題 Q&A

**Q: 我用 Ollama / LM Studio，要怎麼用到這個？**

短期內還用不到。Ollama 跟 LM Studio 都基於 llama.cpp，但有自己的 release cadence。樂觀估計 1-2 個月後會跟進，但你要等他們的版本 bump，不會 PR merge 隔天就有。

**Q: 一定要重新下載模型嗎？**

不用。GGUF 檔本身已經包含 MTP heads（如果模型訓練時有的話），llama.cpp 之前只是不知道怎麼讀那個 tensor。升級 binary 就好。

**Q: 對 MoE 模型（Qwen3.6-35BA3B）效果如何？**

社群測下來加速幅度跟 dense model 接近。MTP 跟 MoE 是兩個正交的優化——MTP 是「一次預測多個 token」，MoE 是「每個 token 只激活部分專家」，兩個疊起來用沒問題。

**Q: 我可以用 MTP 訓練我自己的小模型嗎？**

可以，但這是 pretraining 階段就要決定的——MTP heads 是模型結構的一部分。你沒辦法在訓練完後「加裝」MTP 進去（雖然有些 paper 在嘗試 self-distillation 做法，例如 arxiv 2509.18362 的 FastMTP）。

**Q: 這跟 EAGLE / Medusa 那些 speculative decoding 框架是什麼關係？**

概念上接近——都是「不要外掛 draft model，用模型自己預測多 token」。差別是 EAGLE / Medusa 是「post-hoc 加裝」，MTP 是「pretraining 內建」。內建的版本架構整潔、品質穩定，但你得在訓練時就決定。

---

## 結語

776 個 upvotes 慶祝的不是一個新功能，是一段被閒置一年的算力終於可以用了。

對技術人來說這是好消息，對企業架構師來說這是提醒——你 6 個月前算的 ROI 假設，可能因為一個 PR merge 就要全部重算。

我之前在 [RTX 5090 上跑 Qwen3.6-27B + MTP 已經拿到 140 tok/sec 單流](https://ai-coding.wiselychen.com/qwen-3-6-27b-rtx-5090-inference-engine-benchmark/)，acceptance rate 70%+，跟這次官方 PR 描述的 72.18% 幾乎吻合。

接下來會做的是**並發場景的深度測試**——MTP 在 single-stream 已經贏了，但在企業多用戶情境下到底要不要切回 vLLM + AWQ，這條決策曲線值得畫清楚。數據出來再分享。

---

**參考資料：**
- [Reddit: r/LocalLLaMA "That's a good news..."](https://www.reddit.com/r/LocalLLaMA/comments/1teqnf2/thats_a_good_news/)
- [llama.cpp PR #22673: llama + spec: MTP Support](https://github.com/ggml-org/llama.cpp/pull/22673)
- [DataCamp: Multi-Token Prediction Tutorial with llama.cpp](https://www.datacamp.com/tutorial/multi-token-prediction-llama-cpp)
- [AMD ROCm Blog: Efficient LLM Serving with MTP — DeepSeek V3 and SGLang](https://rocm.blogs.amd.com/software-tools-optimization/mtp/README.html)
- [FastMTP: Accelerating LLM Inference with Enhanced Multi-Token Prediction (arxiv 2509.18362)](https://arxiv.org/pdf/2509.18362)
