---
layout: post
title: "125B 的 Qwen3.8-Flash-Next 塞進一張 5090：Strata 實測 101.9 tok/s，一次讀完百萬 token 的文件，代價是 64GB RAM 只剩 5.8GiB"
date: 2026-10-01 09:00:00 +0800
permalink: /strata-qwen38-flash-next-rtx5090-1m-context/
categories: [AI 工具實測]
image: /assets/images/strata-qwen38-flash-next-rtx5090-cover.png
description: "Strata 是 9 月 24 日才出現的開源推論引擎，宣稱一張遊戲卡加 64GB RAM 就能跑 125B 的 Qwen3.8-Flash-Next。我在自己的 RTX 5090 上從 0.1.14 一路升到 0.1.30：短請求 101.9 tok/s，昨晚把 context 開到 1M：丟給它一份將近 100 萬 token 的超長文件，裡面前、中、後各偷藏一組驗證碼，它讀了將近六分鐘，三組全部答對。這篇拆解它怎麼把 75.8GB 的模型分到 VRAM、RAM、SSD 三層，瓶頸又怎麼從顯卡移到了記憶體。"
author: Wisely Chen
faq:
  - question: "Strata 是什麼？跟 llama.cpp 有什麼不同？"
    answer: "Strata 是 GitHub 使用者 Niko1221 在 2026 年 9 月 24 日開源的推論引擎（MIT 授權），專門讓 Qwen3.8-Flash-Next 這個 125B 的混合專家模型（Mixture of Experts, MoE）跑在一張 12-24GB 的 NVIDIA 遊戲卡加 64GB RAM 上。它用了部分 llama.cpp / ggml 的元件，但做法不同：llama.cpp 的 MoE 卸載（MoE Offload）是把 expert 放 CPU RAM、用到時搬到 GPU 算；Strata 則把最常用的 expert 快取在 VRAM，沒命中的直接由 CPU 在 RAM 裡算，不搬 PCIe。在 RTX 5090 上實測 GPU expert 快取命中率 93.4%。"
  - question: "RTX 5090 跑 Qwen3.8-Flash-Next 實際有多快？"
    answer: "在 Core Ultra 7 265K、64GB DDR5-4800、RTX 5090 32GB 的機器上，用 Strata 跑 IQ3_XXS 量化版（約 75.8GB）：Strata 0.1.30 生成 512 token 為 101.9 tok/s；0.1.14 在 32K context 下短請求 87.7 到 118.8 tok/s，首 token 0.31 到 0.45 秒。如果同一張卡還跑著其他 GPU 服務（例如 CosyVoice 語音合成），Strata 可用的 VRAM 變少，速度會掉到 61.5 tok/s。以上都是單次量測。2026 年 10 月 1 日改跑品質最好的 IQ3_S（262K context、int8 KV）後，一個多小時內 41 筆真實 agent 請求的生成速度中位數是 106.8 tok/s，但那不是同題對照。"
  - question: "Qwen3.8-Flash-Next 在 5090 上真的能開到 1M context 嗎？"
    answer: "能跑，但屬於實驗性質。模型原生訓練長度是 262,144 token，要到 1M 必須用 YaRN 旋轉位置編碼延伸（Rope Scaling）4 倍，並把 KV cache 從 int8 降到 4-bit（q4_0）才放得進 64GB RAM。實測做法是大海撈針測試（Needle-in-a-Haystack）：把一份 999,490 token 的超長文件丟進去，在 10%、50%、90% 的位置各藏一組驗證碼，問它三組是什麼。它三組全部答對，但讀完花了 344 秒，測試當下 RAM 只剩 5.8 GiB。這種測試只證明找得到，不代表長文件理解品質不變；Strata 自己的測試顯示 q4_0 KV 會讓文件類 perplexity 在 8K 多 12%。"
  - question: "5090 上應該跑 Qwen3.8-Flash-Next 還是 Qwen3.8-27B？"
    answer: "看場景。多人共用：選 27B dense，同一張 5090 用 SGLang 單人 113.75 tok/s、四人並行總吞吐 425.44 tok/s，而 Strata 一次只服務一個請求。程式能力上兩者接近：Flash-Next 官方 SWE-bench Pro 62.5，27B 是 61.7。而且 Flash-Next 在 Strata 上跑的是量化版，會再扣分：第三方用同一組 291 題 MMLU-Pro 測，Strata 的 IQ3_S 拿 65.3%，Unsloth 的 UD-Q6_K_XL 拿 68.7%，差約 3 分。單人、需要超長 context（整個 repo、大量文件一次讀入）的個人 agent，才適合 Flash-Next + Strata，前提是機器有 64GB RAM。"
  - question: "跑 Strata 需要多少 RAM？為什麼 RAM 比顯卡重要？"
    answer: "Strata 官方需求是 64GB RAM；IQ3_XXS 的第一個模型檔 47GB 要整個載入 RAM，官方建議 RAM 至少要比它多約 10GB。原因是 RAM 放著全部 24,576 個 expert，VRAM 只是快取熱門的那幾千個——RAM 決定能不能跑，VRAM 決定跑多快。這讓地端推論的瓶頸從顯示記憶體（VRAM）轉到系統記憶體（DRAM），而 2026 年 8 月台灣 32GB DDR5 已經從約 3,000 元漲到近 13,000 元。  ---"
---

一張 32GB 的 5090，能跑 125B 的模型嗎？

以前我的答案是不行。這台機器過去兩個月的主力都是 27B dense——Qwen3.8-27B、Huihui、Bonsai。32GB VRAM，27B 剛好是天花板。

然後 Strata 出現了。GitHub 上一個叫 Niko1221 的作者，9 月 24 日第一個 commit，宣稱「一張 12-24GB 的 NVIDIA 卡加 64GB RAM」就能跑 Qwen3.8-Flash-Next。9 月 30 日已經是 0.1.30。一週三十個版本，GitHub 上 2.9k stars（10/1 看的）。

![Strata 的 GitHub README：一張 12-24GB 的 NVIDIA 卡加 64GB RAM，跑 125B 的模型](/assets/images/strata-github-readme-1.png)

我 9/28 裝起來，9/30 晚上升 0.1.29，昨晚到今天凌晨升 0.1.30，順手把 context 從 262K 開到 1M。

結果先講兩件事。

第一，速度：**寫答案每秒 101.9 個 token**，比人眼閱讀快很多。

第二，長文件：我丟給它一份將近 100 萬 token 的超長文件（英文，大約三、四百萬個字母），在文件的前段、中段、後段各偷藏一組驗證碼，最後問它：「三組驗證碼是什麼？」**它讀了 344 秒，將近六分鐘，三組全部答對。**

代價是 64GB RAM 在測試當下只剩 5.8 GiB。

---

## 30 秒定位

| 項目 | 數字 |
|------|------|
| 模型 | Qwen3.8-Flash-Next，8 月 26 日發布，Qwen Community License |
| 參數 | 125B 總參數、每個 token 只激活 6B，另外掛一張 51B 的 n-gram embedding 表和 4B 的 MTP 模組 |
| MoE 結構 | 每層 512 個 expert，每個 token 用 10 個路由 expert 加 1 個共享 expert |
| 注意力 | 48 層，其中 36 層是 Gated DeltaNet 線性注意力、12 層是 Qwen Sparse Attention（QSA） |
| Context | 原生 262,144 token，官方說可延伸到 1M |
| 量化檔 | IQ3_XXS 兩個檔加起來約 75.8GB，第一個 47GB |
| 我的機器 | Core Ultra 7 265K、64GB DDR5-4800、RTX 5090 32GB、CUDA 12.9 |

75.8GB 的模型，32GB 的卡。多出來的 43.8GB 去哪了？這就是 Strata 的全部故事。

---

## Strata 怎麼塞：三層記憶體，外加一個會學的快取

Strata README 的比喻是廚房：常用的東西放流理台，其他的放儲藏室。拆開來是三層：

- **VRAM**：每個 token 都要跑的部分（attention、共享 expert、路由），加上「最常被叫到」的幾千個 expert。
- **RAM**：全部 24,576 個 expert 都有一份。GPU 沒有的 expert，**CPU 直接在 RAM 裡算**，跟 GPU 同時進行。
- **SSD**：那張 29GB 的 n-gram 查表留在 SSD，每個 token 只讀幾行。

24,576 這個數字就是 48 層 × 512 個 expert。每個 token 只叫 10 個，所以任何時候絕大多數的 expert 都在睡覺。

關鍵在 GPU 那層是「會學的」。它會記錄哪些 expert 最常被叫，把它們留在 VRAM。9/30 升 0.1.29 那次的 log 裡，GPU expert 快取命中率 93.4%。意思是 100 次 expert 呼叫，有 93 次在顯卡上就解決了，剩下 7 次才輪到 CPU。

生成端再加一層 MTP（Multi-Token Prediction）：小模型先猜後面幾個 token，大模型一次驗證。作者說快 1.6-1.8 倍。我昨晚那次的 log 是 MTP 猜了 191 個 token，被接受 76 個，大約四成。

### 這修正了我七月的結論

七月寫 [MoE Offload 完全拆解](/moe-offload-deepseek-v3-v4-local-inference-optimization/) 的時候，我的結論是：

> MoE offload 場景下，速度 = f(VRAM 能留多少 expert)。大 VRAM 不是為了塞下模型，是為了少搬 PCIe。

那時候的前提是 llama.cpp 的做法：expert 放 CPU RAM，用到時搬過 PCIe 給 GPU 算。

Strata 換了一個思路：**沒命中的 expert 不搬，CPU 就地算。** 搬 PCIe 的問題被繞過去，剩下的問題變成「CPU 算得夠不夠快」和「GPU 快取猜得準不準」。93.4% 的命中率，就是這個設計能成立的原因。

前半句還是對的——VRAM 越大，能留的 expert 越多。後半句要改：大 VRAM 不只是為了少搬 PCIe，是為了少叫 CPU。

---

## 實測過程：從 32K 到 1M，四個版本

### 9/28：0.1.14，32K context

第一次跑，32K context、int8 KV cache、MTP 開、vision 關。

短請求 87.7 到 118.8 tok/s，首 token 0.31 到 0.45 秒。768 token 長輸出 129.9 tok/s，同 prompt 重跑 146.9。

對照作者在 5070 上 IQ3_XXS 短對話 62 tok/s，5090 多出來的 20GB VRAM 確實有換到速度。

但 VRAM 吃到 31,693 MiB，只剩 416 MiB。Strata 的 expert 快取預設就是「能吃多少吃多少」。

### 搶 GPU 的代價

這台 5090 不是只跑 LLM。它同時掛著 Whisper 轉錄，有時還有 CosyVoice 做配音、Bonsai 做小模型。

旁邊還掛著 Bonsai 的時候，同一題長輸出只剩 97.4 tok/s。9/30 讓 CosyVoice 一起上 GPU，Strata 要讓出 4GB VRAM，expert 快取格數從 13,602 掉到 9,084，生成掉到 61.5 tok/s。

道理不複雜：**Strata 的速度是 VRAM 裡住了多少 expert 決定的。** 任何跟它搶 VRAM 的服務，都是在拿它的速度。

9/30 那天，Strata 被停、被開、跟 Huihui 和 CosyVoice 輪流搶 GPU，來回切了好幾次。最後的決定是 CosyVoice 停掉，只留 Whisper 陪它。

### 9/30 晚上：0.1.29，262K

升 0.1.29，context 開到原生上限 262K、int8 KV。384 token 生成 94.4 tok/s，前一版同條件 80.6，單次比較。

### 昨晚到今天凌晨：0.1.30，1M

0.1.30 的 release note 寫短 prompt 最多快 28%，還加了 rope scaling 的選項。我就順手把 context 推到 1M：

- `--rope-scaling yarn --rope-scale 4`：把原生 262K 用 YaRN 拉 4 倍
- `--kv q4_0`：KV cache 從 int8 降到 4-bit，不然 64GB RAM 放不下
- `--kv-resident 32768`：只有最近 32K 的 KV 留在 VRAM，其他放 RAM

先跑官方 serve 測試，51/51 過。然後 512 token 生成 101.9 tok/s。

接著測長文件，這個測試業界叫「大海撈針」（needle-in-a-haystack）。做法很土：準備一大堆無關的填充文字，在 10%、50%、90% 的位置各插一句「驗證碼是 violet-harbor-731」這種句子，然後問模型三組驗證碼是什麼。模型如果沒真的把整份文件讀進去，就答不出來：

| 文件長度 | 三組驗證碼 | 讀完到回答花了多久 | 換算讀取速度 |

|---|---|---:|---:|
| 30 萬 token（299,513） | 全對 | 76 秒 | 大約每秒 4,000 token |
| 99.9 萬 token（999,490） | 全對 | 344 秒，將近六分鐘 | 掉到每秒 2,900 左右 |

1M 那次，RAM 只剩 5.8 GiB，swap 約 1.6 GiB，事後 VRAM 剩 3,725 MiB。沒有 OOM，服務沒重啟。

最後走公網 HTTPS 再打一次：算術 391、tool call 回傳 total 42、紅色圖片辨識，三個都過。mini 上 OpenClaw 的 context 設定也一起改成 1M。

### 10/1 清晨更新：最後換成 IQ3_S + 256K

1M 跑通之後，我沒有讓它留在 1M。

清晨 5 點 21 分開始下載 IQ3_S，5 點 50 分下載完，5 點 54 分切過去。IQ3_S 是 Strata 四個版本裡品質最好的那個，第一個檔 54.8GB，比 IQ3_XXS 的 47GB 多 7.8GB；第二個檔（29GB 的 n-gram 查表）兩版共用，不用重下。

這就是前面講的取捨。IQ3_XXS 的 1M 測試時 RAM 只剩 5.8 GiB，IQ3_S 多吃的 7.8GB 塞不進去。所以二選一：**要 1M，就用 IQ3_XXS；要品質最好的量化，就退回 262K。** 我選了後者，KV 也從 q4_0 換回 int8，不開 YaRN 延伸。

切過去之後的狀態：

- 32.81 GiB 的 expert 常駐 RAM，GPU 快取 9,494 格（IQ3_XXS 在 262K 時是 11,340 格，IQ3_S 每個 expert 比較大，住得比較少）
- 平常 RAM 還剩 17GB 左右，VRAM 剩 3.6GB
- 公網的健康檢查、算術、tool call 都過；mini 上 OpenClaw 也改用 IQ3_S，context 設回 262,144

接下來一個多小時，它接了 41 筆真實請求，大部分是 OpenClaw 的 agent 對話，每筆 prompt 5 萬到 6.7 萬 token（前面 49,152 token 沿用上一輪讀過的，只讀新增的部分）。生成速度中位數 106.8 tok/s，範圍 31.8 到 170.6。GPU expert 快取命中率在 67.8% 到 96.5% 之間跳，大多在九成上下。

VRAM 裡住的 expert 變少了，速度看起來卻沒掉。但這 41 筆不是對照實驗：prompt 不一樣、輸出長短不一樣，短輸出的速度本來就很吵。IQ3_XXS 跟 IQ3_S 同題 A/B，我還沒跑。

---

## 瓶頸從顯卡搬到了記憶體

八月我寫過 [5090 三個月從 10 萬變 17 萬](/memory-price-surge-local-ai-five-paths/)，裡面記錄了 32GB DDR5 從約 3,000 元漲到近 13,000 元。

Strata 的門檻是「一張 12-24GB 的 NVIDIA 卡加 64GB RAM」。它把對 VRAM 的需求壓下去了，壓力轉到 DRAM——剛好是這半年漲最兇的東西。

這改變了買機器的決策順序。以前在 5090 上規劃地端模型，思路是「32GB VRAM 能塞什麼」，答案是 27B dense。現在多一條路：**如果你已經有 64GB RAM，這台機器可以跑 125B MoE；如果沒有，補 RAM 比換更大的卡更划算，也更痛。**

我這台剛好有 64GB。1M 測試時剩 5.8 GiB，說明 64GB 是「剛好夠」，不是「很寬裕」。如果還要在同一台機器上開瀏覽器、跑 Docker、跑別的服務，1M context 大概不現實。

---

## 反方：那 27B dense 不就好了？

這是我寫這篇時最卡的地方。

同一張 5090，八月[跑 Qwen3.8-27B](/youtube-qwen38-27b-rtx5090-sglang-vllm-mtp-transcript/) 的數字是：SGLang 單人 113.75 tok/s，四人並行總吞吐 425.44 tok/s。

Flash-Next 在 Strata 上：單人 101.9 tok/s，而且 Strata 一次只回一個請求。

程式能力呢？Flash-Next 官方 SWE-bench Pro 62.5，[27B 是 61.7](/qwen-3-8-27b-open-weights-local-security/)。差 0.8 分。

所以如果問題是「幫小團隊架一台 coding model server」，答案還是 27B dense。它整顆住在 VRAM，不吃 RAM，能並行，單人速度也不輸。

那 Flash-Next 贏在哪？我能用數據講的只有一件事：**context 長度。** 將近 100 萬 token 的文件，一台遊戲機讀得完、找得到裡面藏的東西，這是 27B 在這張卡上我沒測到的東西。其他的——知識廣度、125B 總參數到底比 27B 多懂多少——我沒有測，不能宣稱。

所以主論點要改一下。Strata + Flash-Next 不是「5090 的新主力」，它是**單人、長 context 的個人 agent 機**：一個人、一個 agent、一次把整個 repo 或一整年的文件塞進去。這個場景它是目前這台機器上唯一的選項。

---

## 坦白說

這篇的數字有幾個很明顯的限制。

**第一，我自己沒有品質 benchmark。** 我跑的是 smoke test 和大海撈針：算術、tool call、看圖、在長文件裡找驗證碼。9/28 讓它寫一個 merge_intervals，過了 5 個邊界案例，但漏寫了我明確要求的測試範例。這些只能證明「能跑、沒壞」，不能證明 IQ3_XXS 量化後的智力等於原版。

目前我在 X 上找到最像樣的第三方數字，是 Nigel Hungerford-Symes（[@VectorCrossProd](https://x.com/VectorCrossProd/status/2105124854169227592)）9/30 發的。他用同一組 291 題 MMLU-Pro，比較 Strata 的 IQ3_S 和 Unsloth 兩個比較大的量化版：

```
IQ3_S on Strata, 84 GB:     65.3%
UD-Q4_K_XL, 111 GB:         68.4%
UD-Q6_K_XL, 169 GB:        68.7%
```

Strata 的 IQ3_S 比 Q6 低 3.4 分。他在[下一則](https://x.com/VectorCrossProd/status/2105124856941650123)自己補了一句：

> The 3.5-bit does cost ~3 pts, and it's real (p=0.02 vs Q6).

壓到 3.5-bit 大約扣 3 分，而且統計上站得住。換回來的是速度：同一台機器，Strata 每題 2.6 秒、約 40 tok/s；llama.cpp 跑 Q4 每題 7.5 秒、約 9 tok/s。

這串有個細節比數字本身更值得記。在這則之前兩個小時，他先發了一則[「目前跟 Q6 在誤差範圍內，Winning!」](https://x.com/VectorCrossProd/status/2105095519001522212)，那則 95 個讚；291 題跑完、改口說差 3 分的那則，34 個讚。好消息傳得比更正快。

還要扣到我自己身上：他測的是 IQ3_S，Strata 四個版本裡品質最好的那個。我跑的 IQ3_XXS 壓得更兇，照常理只會更低，但我沒測。所以「扣 3 分」對我這台機器來說比較像下限。

**第二，1M 是硬撐出來的。** 模型原生訓練到 262,144，1M 是 YaRN 延伸 4 倍。KV 也從 int8 降到 q4_0——Strata 自己的測試顯示，q4_0 讓文件類 perplexity 在 1K 多 8%、8K 多 12%。三組驗證碼全對，只代表它「找得到」一句明顯的話，不代表它「讀得懂」整份文件。長文件理解會不會變笨，我沒測。

**第三，1M prompt 要等將近六分鐘。** 而且我的 proxy 非串流等 300 秒就斷，344 秒的請求必須走串流才拿得到結果。這不是互動式的速度，是「丟進去、去倒杯咖啡」的速度。

**第四，速度都是單次量測。** 94.4 vs 80.6 這種比較，是同一台機器、同一條件跑一次的結果，沒有重複取平均。

**第五，Strata 是一個人、一週的專案。** 一週三十個版本，代表迭代很快，也代表明天的 0.1.31 可能改掉今天的行為。要放進正式環境，至少要鎖版本、留 rollback。我這次每一版都留了前一版的 engine 和 config 備份，就是因為這個。

但它做對了一件事：**它證明了「32GB 顯卡跑 125B MoE」不是 demo，是可以每天開著用的服務。** 9/28 起它就是我 mini 上 OpenClaw 的預設模型，中間停過幾次，最後都切回來。

---

## 關鍵洞察

**MoE 時代，地端的瓶頸從 VRAM 移到 DRAM。** 規劃機器時先問「RAM 夠不夠放全部 expert」，再問「VRAM 能快取多少熱門 expert」。前者決定能不能跑，後者決定跑多快。

**會學的 expert 快取，比單純 offload 重要。** 93.4% 的命中率，才是一張 32GB 卡能跑 75.8GB 模型還維持 100 tok/s 的原因。任何跟它搶 VRAM 的服務，都在直接扣它的速度——同卡跑 CosyVoice 時，expert 快取格數從 13,602 掉到 9,084，生成掉到 61.5 tok/s。

**選模型看場景，不看參數量。** 多人共用的 coding server，27B dense 還是比較好的選擇。單人、長 context、要一次吃下整個 repo 的 agent，才是 125B MoE + Strata 的位置。

如果你手上也是 5090 + 64GB RAM，建議啦，先從 262K、int8 KV 開始。1M 那條路能走，但先想清楚你真的需要一次塞一百萬個 token。

---

## 常見問題 Q&A

**Q: Strata 是什麼？跟 llama.cpp 有什麼不同？**

Strata 是 GitHub 使用者 Niko1221 在 2026 年 9 月 24 日開源的推論引擎（MIT 授權），專門讓 Qwen3.8-Flash-Next 這個 125B 的混合專家模型（Mixture of Experts, MoE）跑在一張 12-24GB 的 NVIDIA 遊戲卡加 64GB RAM 上。它用了部分 llama.cpp / ggml 的元件，但做法不同：llama.cpp 的 MoE 卸載（MoE Offload）是把 expert 放 CPU RAM、用到時搬到 GPU 算；Strata 則把最常用的 expert 快取在 VRAM，沒命中的直接由 CPU 在 RAM 裡算，不搬 PCIe。在 RTX 5090 上實測 GPU expert 快取命中率 93.4%。

**Q: RTX 5090 跑 Qwen3.8-Flash-Next 實際有多快？**

在 Core Ultra 7 265K、64GB DDR5-4800、RTX 5090 32GB 的機器上，用 Strata 跑 IQ3_XXS 量化版（約 75.8GB）：Strata 0.1.30 生成 512 token 為 101.9 tok/s；0.1.14 在 32K context 下短請求 87.7 到 118.8 tok/s，首 token 0.31 到 0.45 秒。如果同一張卡還跑著其他 GPU 服務（例如 CosyVoice 語音合成），Strata 可用的 VRAM 變少，速度會掉到 61.5 tok/s。以上都是單次量測。2026 年 10 月 1 日改跑品質最好的 IQ3_S（262K context、int8 KV）後，一個多小時內 41 筆真實 agent 請求的生成速度中位數是 106.8 tok/s，但那不是同題對照。

**Q: Qwen3.8-Flash-Next 在 5090 上真的能開到 1M context 嗎？**

能跑，但屬於實驗性質。模型原生訓練長度是 262,144 token，要到 1M 必須用 YaRN 旋轉位置編碼延伸（Rope Scaling）4 倍，並把 KV cache 從 int8 降到 4-bit（q4_0）才放得進 64GB RAM。實測做法是大海撈針測試（Needle-in-a-Haystack）：把一份 999,490 token 的超長文件丟進去，在 10%、50%、90% 的位置各藏一組驗證碼，問它三組是什麼。它三組全部答對，但讀完花了 344 秒，測試當下 RAM 只剩 5.8 GiB。這種測試只證明找得到，不代表長文件理解品質不變；Strata 自己的測試顯示 q4_0 KV 會讓文件類 perplexity 在 8K 多 12%。

**Q: 5090 上應該跑 Qwen3.8-Flash-Next 還是 Qwen3.8-27B？**

看場景。多人共用：選 27B dense，同一張 5090 用 SGLang 單人 113.75 tok/s、四人並行總吞吐 425.44 tok/s，而 Strata 一次只服務一個請求。程式能力上兩者接近：Flash-Next 官方 SWE-bench Pro 62.5，27B 是 61.7。而且 Flash-Next 在 Strata 上跑的是量化版，會再扣分：第三方用同一組 291 題 MMLU-Pro 測，Strata 的 IQ3_S 拿 65.3%，Unsloth 的 UD-Q6_K_XL 拿 68.7%，差約 3 分。單人、需要超長 context（整個 repo、大量文件一次讀入）的個人 agent，才適合 Flash-Next + Strata，前提是機器有 64GB RAM。

**Q: 跑 Strata 需要多少 RAM？為什麼 RAM 比顯卡重要？**

Strata 官方需求是 64GB RAM；IQ3_XXS 的第一個模型檔 47GB 要整個載入 RAM，官方建議 RAM 至少要比它多約 10GB。原因是 RAM 放著全部 24,576 個 expert，VRAM 只是快取熱門的那幾千個——RAM 決定能不能跑，VRAM 決定跑多快。這讓地端推論的瓶頸從顯示記憶體（VRAM）轉到系統記憶體（DRAM），而 2026 年 8 月台灣 32GB DDR5 已經從約 3,000 元漲到近 13,000 元。

---

## 延伸閱讀

- [MoE Offload 完全拆解：為什麼 671B 模型只吃 17GB VRAM 還能跑](/moe-offload-deepseek-v3-v4-local-inference-optimization/)
- [5090 三個月從 10 萬變 17 萬：五條技術路徑壓低地端 AI 的硬體門檻](/memory-price-surge-local-ai-five-paths/)
- [YouTube 逐字稿：千問3.8-27B 用了兩天說說感覺——RTX 5090 SGLang/vLLM/llama.cpp 實測](/youtube-qwen38-27b-rtx5090-sglang-vllm-mtp-transcript/)
- [單機跑得動 Tier 1 地端 Model 嗎？RTX Pro 6000 一週實驗 Day 1-2](/rtx-pro-6000-tier1-local-day1-2-glm52-deepseek-v4-flash/)

## 來源

- [Strata（GitHub, Niko1221）](https://github.com/Niko1221/Strata)
- [Qwen/Qwen3.8-Flash-Next model card（Hugging Face）](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)
- [MarkTechPost：Alibaba's Qwen Team Releases Qwen3.8-Flash-Next](https://www.marktechpost.com/2026/08/26/alibabas-qwen-team-releases-qwen3-8-flash-next-a-125b-multimodal-moe-with-6b-active-parameters-previewing-the-qwen4-architecture/)
- [Nigel Hungerford-Symes（@VectorCrossProd）：Strata IQ3_S 的 291 題 MMLU-Pro 測試](https://x.com/VectorCrossProd/status/2105124854169227592)
