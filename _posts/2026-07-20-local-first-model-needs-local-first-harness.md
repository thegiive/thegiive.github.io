---
layout: post
title: "同一顆 Kimi K3，換個 harness 差 10 個百分點：走 local-first 模型，你也需要 local-first harness"
date: 2026-07-20 09:00:00 +0800
permalink: /local-first-model-needs-local-first-harness/
image: /assets/images/local-first-harness-maka-cover.png
description: "Maka 團隊拿同一顆 Kimi K3 跑 Terminal-Bench 2.1：官方 Kimi Code 59.6%，開源 Maka 69.7%，困難題子集差距拉到 20 個百分點。同一顆模型，換個 harness，差出接近一個世代。這篇先拆差距的三個來源（context prune、精簡工具面、跑分-看 trace-重跑的迭代循環），再回答一個地端玩家繞不開的問題：模型 local-first 了，agent 跟 harness 呢？盤點 coding agent 接地端模型的七條路——Codex --oss、Claude Code + cc-switch、Kimi Code、ZCode、Grok Build、Pi、Maka——加上 Grok Build 在資料外洩醜聞後 72 小時開源 84 萬行 Rust harness 的信任課，以及為什麼在 10.8 token/s 的地端世界，harness engineering 從優化變成生存條件。"
---

用 Claude 就配 Claude Code，用 GPT 就配 Codex，用 GLM-5.2 就配 ZCode，用 Kimi 就配 Kimi Code。不管你選的模型是開放權重還是 cloud-only，大家的預設邏輯都一樣：模型是誰家的，harness 就用誰家的。原廠最懂自家模型，這件事看起來不需要討論。

然後 [Maka 團隊](https://github.com/maka-agent/maka-agent)的實測直接打在這個預設上。同一顆 Kimi K3，同一套 Terminal-Bench 2.1：官方的 Kimi Code CLI 跑出 59.6%，開源的 Maka 跑出 69.7%。困難題子集的差距更大：43.3% 對 63.3%，差 20 個百分點。

模型沒變，任務沒變，變的只有 harness——而且輸的是原廠。

先講清楚：這是 Maka 自報數字，跑在自家環境，目前沒有第三方復現，後面「坦白說」會完整處理這件事。但它把一個我寫過好幾次的論點，第一次變成了同模型、同任務的直接對照——[harness 不是包裝，是能力的一部分](/agent-harness-three-migrations-mechanism/)。而且它正好戳中我最近每天在想的問題：我這兩週都在[單機上跑 GLM 5.2 和 DeepSeek V4 Flash](/rtx-pro-6000-tier1-local-day1-2-glm52-deepseek-v4-flash/)，模型已經 local-first 了，那 agent 跟 harness 呢？

---

## 30 秒定位

| 項目 | Kimi Code（官方） | Maka（開源） |
|------|------------------|--------------|
| TB 2.1 整體通過率 | 59.6% | 69.7% |
| 困難題子集 | 43.3% | 63.3% |
| 剔除推理超時的任務後 | 85.7% | 95.1% |
| 屬性 | Moonshot 官方 CLI | 開源、local-first agent workspace |

（以上全部為 Maka 自報；「剔除超時」是子集口徑，不能拿去跟任何 leaderboard 的全量分數直接比。）

一個對照基準：Moonshot 官方給 K3 的 TB 2.1 成績是 [88.3%](https://codingfleet.com/blog/terminal-bench-leaderboard-2026/)，用 Kimi Code 開 max reasoning 跑出來的。Maka 這次測到的 59.6%，跟官方 88.3% 之間差的主要是推理服務超時——約 1/3 的任務是因為 Kimi 推理服務逾時而失敗，跟 harness 無關。所以剔除超時之後的那一行（85.7% 對 95.1%）才是 harness 差距的乾淨讀法。

---

## 差距從哪來：三個來源，沒有一個是黑科技

Maka 團隊自己拆了差距的來源，值得逐條看，因為每一條都平凡得驚人。

**第一，context-budget tool-result prune。** 把過期的 tool result 從 context 裡修剪掉，89 個任務總共省了約 187 萬 token。他們宣稱 6 月底做過 121 組任務的 A/B 測試：通過率不降反升（+2.48 個百分點），token 消耗降 41.7%，成本降 31.6%。修剪 context 反而變聰明——對模型來說，context 不是越多越好，是雜訊越少越好。

**第二，精簡工具面和 system prompt。** 他們的原話：

> prompt 越厚、工具越多，模型要在噪音里找信号的成本就越高。

Kimi Code 官方帶著約 20KB 的產品 prompt 加全量工具面上場，Maka 用的是精簡工具面加精簡 prompt。

**第三，迭代循環。** 這是三條裡最不性感、也最難抄的一條：

> 差距主要是来自我们从一开始就把「跑分-看 trace-针对性改进-重跑」当成日常迭代循环，每次改动都要确认 terminal benchmark 分数不掉才合并。这个习惯攒了两个多月，才攒出这个差距。

看 trace、改一點、重跑、守住分數線。就是把 CI 的紀律用在 harness 上。

這個故事有前例。LangChain 之前只改 harness、不動模型，把 agent 從 Terminal-Bench 榜單 30 名外拉進前 5——我在 [harness 三次遷移那篇](/agent-harness-three-migrations-mechanism/)拆過。Maka 這次等於把同一件事在另一個模型上又演了一遍，而且對手是模型原廠自己的 harness。

---

## 這件事為什麼跟地端有關

現在回到 local-first。

地端模型的討論——包括我自己這幾篇——幾乎都集中在 stack 的上半截：權重多大、量化掉多少智力、單機跑幾個 token per second。但一個能做事的 agent stack 是「模型 × harness」，上半截 local 了，下半截還掛在別人的產品決策上，這個 stack 就只 local 了一半。

Daily work 這一類其實已經有答案。OpenClaw 和 Hermes Agent 都是開源、模型可換的，我自己驗證過 OpenClaw + RTX 5090 + Qwen 27B 這種小模型組合，[一台機器就能跑日常秘書工作流](/glm-52-single-machine-rtx-pro-6000-tier1-local/)。

Coding agent 這一類比較亂，值得盤一次：

| Harness | 屬性 | 接地端模型的方式 |
|---------|------|------------------|
| Codex CLI | OpenAI 官方、開源 | 原生 `--oss`，[直接接 Ollama / LM Studio / 任何 OpenAI-compatible 端點](https://docs.ollama.com/integrations/codex) |
| Claude Code | Anthropic 官方 | 沒有官方開關，靠 [cc-switch](https://github.com/farion1231/cc-switch) 這類工具改寫設定，把請求導向本地端點 |
| Kimi Code | Moonshot 官方 | 配自家 K 系模型，垂直整合 |
| ZCode | Z.ai 官方、開源 | [GLM-5.2 的官方 harness](https://zcode.z.ai/en)，垂直整合 |
| Grok Build | xAI 官方、開源（Apache 2.0） | [完整 Rust harness 開源](https://github.com/xai-org/grok-build)，自行編譯後可把推理端點指向本地模型 |
| Pi | 社群開源（Mario Zechner） | 模型無關，[預設只有 read / write / edit / bash 四個工具](https://github.com/badlogic/pi-mono)，其餘靠 extension |
| Maka | 社群開源 | local-first workspace，session 與設定存本機，模型接雲端 API 或本地端點 |

這張表裡藏著兩條路線。

**垂直整合路線**：自家 harness 配自家模型。Kimi Code + K 系、ZCode + GLM-5.2。理由很正當——Moonshot 自己就[說明過 K3 對 harness 敏感](https://www.nxcode.io/resources/news/kimi-k3-benchmarks-coding-agent-evaluation-guide-2026)：thinking history 有沒有被正確傳回去、context 怎麼壓縮，都會影響輸出品質，所以官方推薦用「verified harness」。這是遊戲主機的邏輯：只有自家硬體配自家遊戲，才能保證最佳化。

**開放配對路線**：任何 harness 接任何模型。Codex 的 `--oss`、Pi 的極簡工具面、Maka 的 local-first workspace、cc-switch 把六七個 CLI 的供應商設定統一管理。這是 PC 的邏輯：介面標準化之後，配對自由。

Maka 對 Kimi Code 這組數字的意義在這裡：**垂直整合的核心論述——官方最懂自家模型——第一次被一個開放配對的實例正面挑戰。** 一個 752 star 的開源專案，用通用機制（prune、精簡工具面）加兩個月的迭代紀律，在原廠模型的主場打贏了原廠 harness。主機廠對 PC 的品質承諾，這一局沒有兌現。

表上的 Grok Build 是 7 月 15 日才加進來的，它開源的理由值得單獨講。xAI 把整個 harness 攤開——[844,530 行 Rust，Apache 2.0](https://www.marktechpost.com/2026/07/15/spacexai-open-sources-grok-build-the-rust-agent-harness-tui-and-tool-layer-behind-its-coding-cli/)，agent loop、工具實作、TUI、extension 系統全部在內——但這不是大方，是止血。開源前 72 小時，[有安全研究者拿出 wire-level 證據](https://www.digitalapplied.com/blog/grok-build-open-source-72-hours-trust-repair)：Grok 的 CLI 一直在悄悄把使用者的完整目錄上傳到自家雲端，[被翻出來的內容包括 SSH 金鑰這類敏感檔案](https://simonwillison.net/2026/Jul/15/grok-build/)。把程式碼全部公開，是它唯一能拿出來的信任修復手段。模型 grok-build-0.1 本身仍然閉源。

這件事替 local-first harness 補上了 Maka 案例沒講的另一半理由。Maka 講的是**性能**：harness 決定分數。Grok Build 事件講的是**信任**：harness 是整個 stack 裡看得最多的元件——你的 code、你的 shell、你的憑證全部經過它。模型擺在地端、harness 的資料行為卻是黑箱，資安上等於白做工。這也是為什麼「開源」對 harness 的意義比對模型更硬：模型權重你拿到了也審不動，harness 的每一次上傳你都查得到。而現在，一個生產等級的完整 harness 躺在 Apache 2.0 底下，要打造真正 local-first 的 harness 框架，第一次有了可以直接 fork 的起點，而不是從零寫起。

---

## 地端推理慢，所以 harness 從優化變成生存條件

還有一層是地端獨有的，而且 Maka 的數據裡剛好就有線索。

那次實測裡約 1/3 的任務死於推理服務超時。注意，那還是 Moonshot 自家的雲端推理。換到地端呢？我的 GLM 5.2 2-bit 在 RTX Pro 6000 上是 [10.8 token/s，DeepSeek V4 Flash 是 58 token/s](/rtx-pro-6000-tier1-local-day1-2-glm52-deepseek-v4-flash/)。雲端 API 的推理速度掉三成，harness 就死掉三分之一的任務；地端的日常就是雲端的最壞情況。

這代表三件在雲端算「優化」的事，在地端全部升級成生存條件：

**Token 預算。** 雲端省 41.7% 的 token 是省錢；地端省 41.7% 的 token 是省牆上時鐘的時間，因為你的 prefill 和 generation 都慢。同一個 prune 機制，地端的回報率直接高一級。

**Timeout 容忍。** harness 的重試策略、逾時上限、任務切分粒度，在 10.8 token/s 的世界裡決定任務是「慢慢做完」還是「直接判死」。Kimi Code 那 1/3 的超時死亡，就是 harness 用雲端假設去接慢速推理的下場。

**Prompt 厚度。** 20KB 的產品 prompt 在雲端是雜訊問題，在地端還是 prefill 時間問題。地端模型本來智力就先被量化折損過一輪，你更沒有本錢讓它在噪音裡找信號。

這也是為什麼我說 local-first 不是「執行位置」的問題，是「設計假設」的問題。Claude Code 和 Codex 本來就跑在你的機器上，但它們的預設值——context 給多長、工具開幾個、逾時設多久——都是對著雲端 frontier model 調的。**一個 harness 是不是 local-first，看的不是它裝在哪，是它的預設假設把慢速、量化過的模型當不當一等公民。**

順帶一提，這條路我自己已經踩過第一步：Day 1-2 的實測裡，本地 GLM 5.2 接的就是 Codex 當 harness，跑完寫程式、數據分析、上網寫文章的完整 agentic 任務，Fable 5 打分給了 98。開放配對接地端模型，今天就是能動的，不是願景。

---

## 反方：這差距是暫時的

先把最強的反駁擺出來：context prune 不是專利，精簡工具面誰都會，Kimi 團隊下一版把這些抄回去，10 個百分點就蒸發了。而且數字是 Maka 自己跑的，宣傳動機明擺著。到時候這篇文章的核心案例就過期了。

兩點回應。

第一，單點機制會被抄走，迭代循環抄不走。「跑分-看 trace-改進-重跑、分數不掉才合併」是組織習慣，不是 feature flag。原廠 harness 背著產品包袱——20KB prompt 裡每一段都是某個產品需求——它做減法的成本天生比一個沒有包袱的開源專案高。這不保證 Maka 永遠領先，但保證這類差距會反覆出現。

第二，就算差距明天被追平，對使用者的結論一個字都不用改：**harness 是一個獨立於模型、量級可以到兩位數百分點的變因。** 你在地端選型時只比模型分數，等於買車只看引擎馬力、不問變速箱。案例會過期，變因不會。

---

## 坦白說

這篇的核心數據全部來自 Maka 團隊自報，跑在自家環境，沒有第三方復現。752 star 的早期專案發布對自己有利的評測，動機需要打折，這個折我打不掉，只能標明。

其次，口徑問題比看起來嚴重。95.1% 是「剔除超時任務」的子集分數，貼文拿它去跟「TB 2.1 目前最高分 89.5%」比——而那個 89.5% 我在公開資料裡查不到：[tbench.ai 官方 leaderboard](https://www.tbench.ai/leaderboard/terminal-bench/2.1) 目前 2.1 的最高分是 Claude Code + Fable 5 的 83.8%，聚合站給 GPT-5.6 Sol 的 [88.8% 是廠商自報的單 agent 成績](https://llm-stats.com/benchmarks/terminal-bench-2.1)，Moonshot 給 K3 的 88.3% 也是自報。同一個 benchmark，三個來源三個口徑。所有「比全場最高分還高」的句子，包括 Maka 的，都看看就好。

真正站得住的只有一組數字：同模型、同任務、同環境下，兩個 harness 的 A/B 對照。這個實驗設計是乾淨的，10.1 個百分點的精確值可以存疑，方向很難全錯。

最後，我自己還沒實測 Maka。這篇是解析，不是實戰記錄——機器還回去之前如果排得進待測清單，會補上第一手數據。

---

## 關鍵洞察

**地端選型是「模型 × harness」的配對題，不是模型單選題。** 同一顆模型換 harness 可以差兩位數百分點。你的實測要測配對——用你打算天天用的 harness 去測你打算跑的模型，而不是看模型在別人 harness 上的 leaderboard 分數。

**開放配對的摩擦正在快速下降。** Codex `--oss` 直接接本地端點、Claude Code 靠 cc-switch 繞、Pi 和 Maka 天生模型無關，現在連 Grok Build 的 84 萬行生產級 harness 都躺在 Apache 2.0 底下等人 fork。垂直整合的「verified harness」論述第一次被正面數據挑戰，而 K3 權重 7/27 開源之後，「開源 harness + 開放權重」這條 PC 路線的組合空間只會更大。

**挑 harness 時，把「資料行為可審計」跟分數放同一級。** harness 看得到你的 code、shell 和憑證，它往哪裡上傳、記了什麼，重要性不亞於它跑幾分。Grok Build 用一次醜聞示範了黑箱 harness 的代價——你的模型再 local，harness 亂傳就全部歸零。

**地端把 harness engineering 的權重再調高一級。** token prune、prompt 減法、timeout 策略，在雲端是省錢，在 10.8 token/s 的地端是任務能不能活著跑完。挑 harness 的時候，把「它對慢速推理的容忍度」當一級指標。

**看到 harness 對比數字，先問三個口徑問題。** 全量還是剔除超時的子集？誰跑的、在誰的環境？能不能復現？這跟我在 [memory benchmark 那篇](/agent-memory-benchmark-rashomon-filesystem/)給的建議是同一組肌肉：分數先問口徑，再問結論。這次的案例值得認真對待，正是因為它的 A/B 設計乾淨——也僅限於那個 A/B。
