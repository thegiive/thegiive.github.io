---
layout: post
title: "同一顆 Kimi K3，用第三方 Harness 居然贏原廠 Harness (KCode) 10 個百分點：走 local-first 模型，你也需要 local-first harness"
date: 2026-07-20 09:00:00 +0800
permalink: /local-first-model-needs-local-first-harness/
image: /assets/images/local-first-harness-maka-cover.png
description: "Maka 團隊拿同一顆 Kimi K3 跑 Terminal-Bench 2.1：官方 Kimi Code 59.6%，開源 Maka 69.7%，困難題子集差距拉到 20 個百分點。同一顆模型，換個 harness，差出接近一個世代。這篇先拆差距的三個來源（context prune、精簡工具面、跑分-看 trace-重跑的迭代循環），再回答一個地端玩家繞不開的問題：模型 local-first 了，agent 跟 harness 呢？盤點 coding agent 接地端模型的七條路——Codex --oss、Claude Code + cc-switch、Kimi Code、ZCode、Grok Build、Pi、Maka——加上 Grok Build 在資料外洩醜聞後 72 小時開源 84 萬行 Rust harness 的信任課，以及為什麼在 10.8 token/s 的地端世界，harness engineering 從優化變成生存條件。"
---

用 Claude 就配 Claude Code，用 GPT 就配 Codex，用 GLM-5.2 就配 ZCode，用 Kimi 就配 Kimi Code。不管模型是開放權重還是 cloud-only，大家的預設邏輯都一樣：模型是誰家的，harness 就用誰家的。原廠最懂自家模型，這件事看起來不需要討論。

然後 [Maka 團隊](https://github.com/maka-agent/maka-agent)的實測直接打在這個預設上。

同一顆 Kimi K3，同一套 Terminal-Bench 2.1：官方 Kimi Code CLI 跑出 59.6%，開源的 Maka 跑出 69.7%。困難題子集差距更大——43.3% 對 63.3%，差 20 個百分點。模型沒變，任務沒變，變的只有 harness，而且輸的是原廠。

這是 Maka 自報數字，目前沒有第三方復現，後面「坦白說」會完整處理。但它把一個我寫過好幾次的論點第一次變成了同模型、同任務的直接對照——[harness 不是包裝，是能力的一部分](/agent-harness-three-migrations-mechanism/)。而且它正好戳中我最近每天在想的問題：這兩週在[單機上跑 GLM 5.2 和 DeepSeek V4 Flash](/rtx-pro-6000-tier1-local-day1-2-glm52-deepseek-v4-flash/)，模型已經 local-first 了，那 agent 跟 harness 呢？

這篇想講三件事：原廠 harness 不一定最強、地端算力有限所以需要更輕量的 harness、以及原廠 harness 可能偷傳資料——跟你走 local-first 的初衷完全背道而馳。

---

## 30 秒定位

| 項目 | Kimi Code（官方） | Maka（開源） |
|------|------------------|--------------|
| TB 2.1 整體通過率 | 59.6% | 69.7% |
| 困難題子集 | 43.3% | 63.3% |
| 剔除推理超時的任務後 | 85.7% | 95.1% |
| 屬性 | Moonshot 官方 CLI | 開源、local-first agent workspace |

以上全部為 Maka 自報。「剔除超時」是子集口徑，不能拿去跟任何 leaderboard 的全量分數直接比。

一個對照基準：Moonshot 官方給 K3 的 TB 2.1 成績是 [88.3%](https://codingfleet.com/blog/terminal-bench-leaderboard-2026/)，用 Kimi Code 開 max reasoning 跑的。Maka 測到的 59.6% 跟官方 88.3% 之間差的主要是推理服務超時——約 1/3 的任務死在 Kimi 的推理服務逾時，跟 harness 無關。所以剔除超時之後那一行（85.7% 對 95.1%）才是 harness 差距的乾淨讀法。

---

## 差距從哪來：三個來源，沒有一個是黑科技

Maka 團隊自己拆了差距的來源，每一條都平凡得驚人。

**第一，context-budget tool-result prune。** 把過期的 tool result 從 context 裡修剪掉，89 個任務總共省了約 187 萬 token。他們宣稱 6 月底做過 121 組任務的 A/B 測試：通過率不降反升（+2.48 個百分點），token 消耗降 41.7%，成本降 31.6%。修剪 context 反而變聰明——對模型來說，context 不是越多越好，是雜訊越少越好。

**第二，精簡工具面和 system prompt。** 他們的原話：

> prompt 越厚、工具越多，模型要在噪音里找信号的成本就越高。

Kimi Code 官方帶著約 20KB 的產品 prompt 加全量工具面上場，Maka 用的是精簡版。

**第三，迭代循環。** 三條裡最不性感、也最難抄的一條：

> 差距主要是来自我们从一开始就把「跑分-看 trace-针对性改进-重跑」当成日常迭代循环，每次改动都要确认 terminal benchmark 分数不掉才合并。这个习惯攒了两个多月，才攒出这个差距。

看 trace、改一點、重跑、守住分數線。把 CI 的紀律用在 harness 上。

這個故事有前例。LangChain 之前只改 harness、不動模型，把 agent 從 Terminal-Bench 榜單 30 名外拉進前 5——我在 [harness 三次遷移那篇](/agent-harness-three-migrations-mechanism/)拆過。Maka 等於在另一個模型上又演了一遍，而且對手是模型原廠。

---

## 模型 local 了，harness 呢？

地端模型的討論——包括我自己這幾篇——幾乎都集中在 stack 的上半截：權重多大、量化掉多少智力、單機跑幾個 token per second。但一個能做事的 agent stack 是「模型 × harness」，上半截 local 了，下半截還掛在別人的產品決策上，這個 stack 就只 local 了一半。

Daily work 這一類已經有答案了。OpenClaw 和 Hermes Agent 都是開源、模型可換的，我驗證過 OpenClaw + RTX 5090 + Qwen 27B 組合，[一台機器就能跑日常秘書工作流](/glm-52-single-machine-rtx-pro-6000-tier1-local/)。

Coding agent 這一類比較亂，值得盤一次：

| Harness | 屬性 | 接地端模型的方式 |
|---------|------|------------------|
| Codex CLI | OpenAI 官方、開源 | 原生 `--oss`，[直接接 Ollama / LM Studio / 任何 OpenAI-compatible 端點](https://docs.ollama.com/integrations/codex) |
| Claude Code | Anthropic 官方 | 沒有官方開關，靠 [cc-switch](https://github.com/farion1231/cc-switch) 這類工具改寫設定，導向本地端點 |
| Kimi Code | Moonshot 官方 | 配自家 K 系模型，垂直整合 |
| ZCode | Z.ai 官方、開源 | [GLM-5.2 的官方 harness](https://zcode.z.ai/en)，垂直整合 |
| Grok Build | xAI 官方、開源（Apache 2.0） | [完整 Rust harness 開源](https://github.com/xai-org/grok-build)，自行編譯後可指向本地模型 |
| Pi | 社群開源（Mario Zechner） | 模型無關，[預設只有 read / write / edit / bash 四個工具](https://github.com/badlogic/pi-mono)，其餘靠 extension |
| Maka | 社群開源 | local-first workspace，session 與設定存本機，模型接雲端 API 或本地端點 |

七條路攤開來，底下有三個必須面對的問題。

---

## 一、原廠 Harness 不一定最強

Moonshot 自己[說明過 K3 對 harness 敏感](https://www.nxcode.io/resources/news/kimi-k3-benchmarks-coding-agent-evaluation-guide-2026)：thinking history 有沒有被正確傳回去、context 怎麼壓縮，都會影響輸出品質，所以官方推薦用「verified harness」。這是遊戲主機的邏輯：自家硬體配自家遊戲，才能保證最佳化。

Maka 那組數字把這個邏輯打了一個洞。一個 752 star 的開源專案，用通用機制（prune、精簡工具面）加兩個月的迭代紀律，在原廠模型的主場打贏了原廠 harness。

為什麼？因為原廠 harness 背著產品包袱。20KB 的 prompt 裡每一段都是某個產品需求，全量工具面是為了功能完整度而非推理效率。而開源社群沒有這些包袱——它可以只為「讓模型在這個 benchmark 上拿最高分」而裁剪一切。

垂直整合仍然有它的價值，但「原廠配的就是最好的」這個預設需要被放棄了。Codex 的 `--oss`、Pi 的極簡工具面、Maka 的 local-first workspace、cc-switch 把六七個 CLI 的供應商設定統一管理——開放配對的摩擦正在快速下降，而 K3 權重 7/27 開源之後，「開源 harness + 開放權重」的組合空間只會更大。

---

## 二、地端算力有限，需要更輕量的 Harness

這是地端獨有的問題。

Maka 的實測裡約 1/3 的任務死於推理服務超時——那還是 Moonshot 自家的雲端推理。換到地端呢？我的 GLM 5.2 2-bit 在 RTX Pro 6000 上是 [10.8 token/s，DeepSeek V4 Flash 是 58 token/s](/rtx-pro-6000-tier1-local-day1-2-glm52-deepseek-v4-flash/)。雲端推理速度掉三成，harness 就死掉三分之一的任務；地端的日常就是雲端的最壞情況。

雲端的 frontier model 跑得快、算得強，harness 塞 20KB 的 prompt 加幾十個工具，模型照樣消化得了。地端不行。你的模型智力先被量化折損過一輪，推理速度再慢一個數量級——這時候 harness 每多帶一 KB 的 prompt、每多開一個工具，都是在消耗模型本來就不夠用的注意力和你本來就不夠用的時間。

**雲端的 harness 可以追求功能完整，地端的 harness 必須追求極簡。** 三件在雲端算「優化」的事，在地端全部升級成生存條件：

- **Token 預算**：雲端省 41.7% 的 token 是省錢；地端省 41.7% 是省牆上時鐘的時間
- **Timeout 容忍**：10.8 token/s 的世界裡，harness 的逾時上限決定任務是「慢慢做完」還是「直接判死」
- **Prompt 厚度**：20KB 的產品 prompt 在雲端是雜訊問題，在地端還疊加 prefill 時間問題

所以 local-first 不是「執行位置」的問題，是「設計假設」的問題。Claude Code 和 Codex 本來就跑在你的機器上，但它們的預設值——context 給多長、工具開幾個、逾時設多久——都是對著雲端 frontier model 調的。**一個 harness 是不是 local-first，看的不是它裝在哪，是它的預設假設把慢速、量化過的模型當不當一等公民。**

這條路我自己已經踩過第一步：Day 1-2 的實測裡，本地 GLM 5.2 接的是 Codex 當 harness，跑完寫程式、數據分析、上網寫文章的完整 agentic 任務，Fable 5 打分給了 98。開放配對接地端模型，今天就是能動的，不是願景。

---

## 三、原廠 Harness 可能偷傳資料，跟 local-first 的初衷背道而馳

很多人走 local-first，第一個理由就是資安——資料不出境、不經過別人的雲端。模型權重下載到本機，推理在自己的 GPU 上跑，看起來很安全。

但模型只是 stack 的一半。harness 是整個 stack 裡看得最多的元件——你的 code、你的 shell、你的憑證、你的完整目錄結構，全部經過它。如果 harness 的資料行為是黑箱，你的 local-first 就只 local 了模型那一半，另一半可能正在悄悄把東西送出去。

這不是假設，是剛發生過的事。

7 月 15 日，xAI 把 Grok Build 完整開源——[844,530 行 Rust，Apache 2.0](https://www.marktechpost.com/2026/07/15/spacexai-open-sources-grok-build-the-rust-agent-harness-tui-and-tool-layer-behind-its-coding-cli/)，agent loop、工具實作、TUI、extension 系統全部在內。但這不是大方，是止血。開源前 72 小時，[安全研究者拿出 wire-level 證據](https://www.digitalapplied.com/blog/grok-build-open-source-72-hours-trust-repair)：Grok 的 CLI 一直在悄悄把使用者完整目錄上傳到自家雲端，[被翻出來的內容包括 SSH 金鑰](https://simonwillison.net/2026/Jul/15/grok-build/)。把程式碼全部公開，是它唯一能拿出來的信任修復手段。

想像一下：你花了大功夫把模型搬到地端，GPU 買了、量化調了、推理跑起來了——結果 harness 把你的整個 codebase 傳回原廠。**你以為你在做 local-first，其實你只是幫 harness 供應商做了免費的資料收集。**

這也是為什麼「開源」對 harness 的意義比對模型更硬。模型權重你拿到了也審不動——幾百 GB 的矩陣你看不出它背後學了什麼。但 harness 不一樣，它就是程式碼，每一次網路連線、每一次檔案讀取你都查得到。而現在，一個生產等級的完整 harness 躺在 Apache 2.0 底下。要打造真正 local-first 的 harness 框架，第一次有了可以直接 fork 的起點，不用從零寫起。

---

## 反方：這差距是暫時的

最強的反駁：context prune 不是專利，精簡工具面誰都會，Kimi 團隊下一版把這些抄回去，10 個百分點就蒸發了。而且數字是 Maka 自己跑的，宣傳動機明擺著。

兩點回應。

第一，單點機制會被抄走，迭代循環抄不走。「跑分-看 trace-改進-重跑、分數不掉才合併」是組織習慣，不是 feature flag。原廠 harness 背著產品包袱——20KB prompt 裡每一段都是某個產品需求——做減法的成本天生比沒有包袱的開源專案高。這不保證 Maka 永遠領先，但保證這類差距會反覆出現。

第二，就算差距明天被追平，對使用者的結論一個字都不用改：**harness 是一個獨立於模型、量級可以到兩位數百分點的變因。** 地端選型只比模型分數，等於買車只看引擎馬力、不問變速箱。案例會過期，變因不會。

---

## 坦白說

這篇的核心數據全部來自 Maka 團隊自報，跑在自家環境，沒有第三方復現。752 star 的早期專案發布對自己有利的評測，動機需要打折，這個折我打不掉，只能標明。

口徑問題比看起來嚴重。95.1% 是「剔除超時任務」的子集分數，原貼文拿它去跟「TB 2.1 目前最高分 89.5%」比——而那個 89.5% 我在公開資料裡查不到：[tbench.ai 官方 leaderboard](https://www.tbench.ai/leaderboard/terminal-bench/2.1) 目前 2.1 的最高分是 Claude Code + Fable 5 的 83.8%，聚合站給 GPT-5.6 Sol 的 [88.8% 是廠商自報的單 agent 成績](https://llm-stats.com/benchmarks/terminal-bench-2.1)，Moonshot 給 K3 的 88.3% 也是自報。同一個 benchmark 三個來源三個口徑，所有「比全場最高分還高」的句子都看看就好。

真正站得住的只有一組數字：同模型、同任務、同環境下兩個 harness 的 A/B 對照。實驗設計是乾淨的，10.1 個百分點的精確值可以存疑，方向很難全錯。

我自己還沒實測 Maka。這篇是解析，不是實戰記錄——排得進待測清單的話會補上第一手數據。

---

## 關鍵洞察

**原廠 Harness 不一定最強，地端選型是「模型 × harness」的配對題。** 同一顆模型換 harness 可以差兩位數百分點。實測要測配對——用你打算天天用的 harness 跑你打算部署的模型，而不是看模型在別人 harness 上的 leaderboard 分數。

**地端算力有限，你需要的不是功能最全的 harness，是最輕量的。** 20KB 的 prompt 加幾十個工具，在雲端 frontier model 上跑沒問題，在 10.8 token/s 的地端就是任務能不能活著跑完的差別。token prune、prompt 減法、timeout 策略——在雲端是省錢，在地端是生存條件。

**走 local-first 是為了資安，但 harness 偷傳資料就全部歸零。** 模型擺在地端只 local 了一半，harness 才是看得到你所有東西的那一層。挑 harness 的時候，「資料行為可審計」跟分數放同一級。Grok Build 用一次醜聞示範了這件事的代價——而它被迫開源出來的 84 萬行 Rust，反而成了打造真正 local-first harness 框架的起點。這跟我在 [memory benchmark 那篇](/agent-memory-benchmark-rashomon-filesystem/)給的建議是同一組肌肉：分數先問口徑，再問結論。
