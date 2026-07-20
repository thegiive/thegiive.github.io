---
layout: post
title: "35B 在 SEAL-0 打贏 1T 級模型：Agents-A1 把 Scaling 的軸從參數換成 Horizon，但 MLE-bench 43.9 對 72.7 也標出了邊界"
date: 2026-07-21 09:00:00 +0800
permalink: /agents-a1-35b-agent-horizon-scaling/
image: /assets/images/agents-a1-35b-horizon-scaling-cover.png
description: "Shanghai AI Lab 的 Agents-A1 是一顆 35B MoE，在 SEAL-0 拿 56.4，贏過 1T 級的 DeepSeek-V4-pro（55.0）和 Kimi-K2.6（50.5）；IFBench 80.6、FrontierScience-Olympiad 79.0 也領先全場。方法不是加參數，是把 scaling 的軸換掉：45K token 的長軌跡資料、通過驗證才寫回的 Knowledge-Action Graph、四類 RL teacher、再用 top-k 詞彙對齊把六個 domain 蒸餾進一個 student。這篇拆解 agent-horizon scaling 的三段配方，也看清楚它的邊界——MLE-bench 43.9 對 GPT-5.5 的 72.7，長程工程任務還是大模型的地盤。昨天寫的是推理端的 harness，今天這篇是訓練端的同一個故事。"
---

一顆 35B 的 MoE 模型，在 SEAL-0 這個長程搜尋 benchmark 上拿了 56.4 分。同場的 DeepSeek-V4-pro 是 55.0，Kimi-K2.6 是 50.5——[論文摘要](https://arxiv.org/abs/2606.30616)直接把這兩顆叫做「1T-parameter model」。參數量差了快 30 倍，分數反過來。

這是 Shanghai AI Lab 7 月更新的 [Agents-A1](https://arxiv.org/abs/2606.30616)，論文標題把方法論寫在臉上：Scaling the Horizon, Not the Parameters。不加參數，改 scale「agent horizon」——把訓練資料從一問一答的短樣本，換成平均 45K token 的完整 agent 軌跡，再用多 teacher 蒸餾把六個領域的專家能力塞回一顆 35B。

[昨天那篇](/local-first-model-needs-local-first-harness/)寫的是推理端：同一顆 Kimi K3 換個 harness，Terminal-Bench 差 10 個百分點。今天這篇論文是訓練端的同一個故事——能力不只長在參數裡，也長在結構裡。兩篇放在一起讀，剛好是一個論點的兩面。

---

## 30 秒定位

| 項目 | 數字 |
|------|------|
| 模型 | Agents-A1，35B MoE，Apache 2.0 [開源](https://github.com/InternScience/Agents-A1) |
| 訓練軌跡平均長度 | 45K tokens |
| 領先 1T 級對手的項目 | SEAL-0 56.4、IFBench 80.6、HiPhO 46.4、FrontierScience-Olympiad 79.0、MolBench-Bind 56.8 |
| 接近但沒領先 | SciCode 44.3、HLE 47.6、BrowseComp 75.5 |
| 明顯落後 | MLE-bench(Lite) 43.9，GPT-5.5(xhigh) 是 72.7 |
| 對照的 1T 級模型 | Kimi-K2.6、DeepSeek-V4-pro（論文口徑） |

領先的項目集中在長程搜尋、指令遵循、科學推理。落後的項目是 machine learning engineering 這種長程工程任務。這個分布不是隨機的，後面會回來講。

---

## 傳統做法 vs 這篇的做法

過去一年小模型追大模型的主流路線是壓縮和蒸餾輸出：把大模型的答案當教材，讓小模型模仿。我在 [Bonsai 27B 那篇](/bonsai-27b-qwen36-compression-local-inference/)拆過這條路的天花板——壓縮後的智力損失不均勻，數學幾乎無損，tool calling 掉 26%。恰好 agent 場景最需要的能力掉最多。

Agents-A1 的路線不一樣。它不壓縮既有能力，它直接對著「agent 能力」訓練。兩個 scaling 方向：

**一是把軌跡拉長。** 訓練樣本不是「問題 → 答案」，是完整的任務過程：查了什麼、呼叫了什麼工具、拿回什麼觀察、驗證有沒有過——平均 45K token 一條。模型學的不是答案長什麼樣，是一個長任務從頭到尾怎麼推進。

**二是把能力面拉寬。** 六個異質 domain（搜尋、科學、指令遵循、工具使用等）各自訓練專家 teacher，再蒸餾回一顆 student。

這兩個方向合起來，論文叫它 agent-horizon scaling。參數不動，動的是模型「看過多長的過程、多寬的領域」。

![Scaling 的兩個軸：參數量 vs 任務軌跡長度](/assets/images/agents-a1-scaling-axis-slide.png)

---

## 建立直覺：六個補習班名師，一個學生

多 teacher 蒸餾最大的麻煩是 teacher 之間互相打架。搜尋專家要模型多探索，指令遵循專家要模型守規矩，工具專家要模型輸出精確的 JSON——梯度方向彼此衝突，全部直接混進去訓練，學到的是一鍋漿糊。

Agents-A1 的解法可以想成一個學生同時補六科：

- **不是六個老師輪流對學生整堂課錄音重播。** 那樣六套講法會互相干擾。
- **是每一科只抄該科名師劃的重點。** 這就是 Salient Vocabulary Alignment（SVA）：student 不對齊 teacher 的整個詞彙分布，只對齊 domain-routed teacher 給出的 top-k 有效 token 切片。哪一科的題，就聽哪一科老師的重點，其他科的聲音不進來。

蒸餾還是 on-policy 的：student 自己先做題，teacher 針對 student 的實際行為給修正，而不是讓 student 背 teacher 的模範解答。這跟人類的刻意練習是同一個結構——在自己的錯誤上拿到即時反饋，比看別人的完美示範有效。

---

## 三段配方拆解

![Agents-A1 的三段式訓練配方：全域 SFT、RL Teachers、多 Teacher 蒸餾](/assets/images/agents-a1-three-stage-recipe-slide.png)

### 第一段：全域 SFT

拿多領域的長軌跡資料做 supervised fine-tuning，先讓基底模型對「agent 行為」有廣泛但不深的理解。這一段是地基，沒有驚喜。

### 第二段：每個 domain 各養一個 RL teacher

依 [36kr 的英文報導](https://eu.36kr.com/en/p/3877948838244353)，teacher 分四類：Search、Scientific、Instruction-Following、Tool-Usage，各自用 SFT 加 RL（GRPO）往深處推。專家化的效果非常劇烈——同一篇報導給的數字：Search teacher 把 GAIA 從 59.8 推到 95.1，Scientific teacher 把 FrontierScience-Research 從 2.5 推到 54.3。

第二個數字值得停一秒。2.5 分的意思是基底模型在這個 benchmark 上幾乎完全不會做，54.3 不是「變強了」，是「從不會變成會」。**這種跳幅不是參數變多帶來的，是訓練結構帶來的**——模型大小沒變，變的是它看過的過程資料。

### 第三段：多 teacher 蒸餾回一顆 student

domain-routed：什麼領域的樣本就路由給什麼 teacher，配上前面講的 SVA top-k 對齊，把四個專家壓回一顆 35B，避免梯度打架。

支撐這整套流程的底層是資料工程。他們把每一步形式化成四元組——(Corpus, Action, Observation, Verifier)——組成 Knowledge-Action Graph，**動作要通過驗證才寫回圖裡**。訓練資料不是爬來的，是這套基礎設施「生產」出來的，而且每一條都帶著驗證結果。

![KAG 驗證閘門：每一步動作通過 Verifier 才寫回圖中](/assets/images/agents-a1-kag-verifier-gate-slide.png)

昨天 Maka 團隊的做法是「跑分、看 trace、改進、重跑，分數不掉才合併」——那是推理端的驗證紀律。KAG 是同一個紀律搬到訓練資料的生產線上：沒過驗證的軌跡不進訓練集。兩邊的共同點是把「驗證」放在流程的閘門位置，而不是事後抽查。

---

## 這對誰的什麼決策有影響

對做地端部署的人，這篇論文改變的是 agent 模型的選型邏輯。

之前的狀況：地端小模型的 agent 能力是靠運氣。Bonsai 篇的教訓還在——27B 壓到手機上能跑，但 TauBench 掉 26%，「本地能跑」和「本地 Agent 可用」中間有一道能力鴻溝。你只能拿通用小模型來用，然後祈禱它的 tool calling 撐得住。

現在多了一個選項：一顆從訓練端就對著長程 agent 任務設計的 35B，Apache 2.0，權重[放在 HuggingFace](https://github.com/InternScience/Agents-A1)。選型的問題從「哪顆通用小模型比較不爛」變成一個更具體的問題：**你的任務落不落在它蒸餾過的 domain 裡。** 落在搜尋、科學推理、指令遵循，它有 1T 級的分數；落在 coding 和 ML 工程，SciCode 44.3 和 MLE-bench 43.9 告訴你它不是為這個生的。

還有一個地端特有的成本要算：horizon 是拿推理時間換的。45K token 的軌跡在雲端是延遲問題，在地端——[我自己單機實測](/rtx-pro-6000-tier1-local-day1-2-glm52-deepseek-v4-flash/)的速度是 GLM 5.2 2-bit 10.8 token/s、DeepSeek V4 Flash 58 token/s——就是每個任務以十分鐘為單位計價的問題。軌跡有一大部分是塞進 context 的 observation，不全是要生成的 token，但量級擺在那裡。**這顆模型省的是參數的記憶體，不是任務的時鐘時間。**

---

## 反方：這叫「追平 1T」還是「挑了自己會贏的場子」

最強的反駁是這樣的：所有數字都是 Shanghai AI Lab 自報，沒有第三方復現；領先的 benchmark 集中在它蒸餾過的領域；而唯一一個離日常工程最近的長程任務 MLE-bench，它輸 GPT-5.5 快 30 分。把標題寫成「trillion-parameter performance」，是拿六個特化 domain 的分數去換一個泛化的宣稱。

這個反駁大部分是成立的，我不打算硬拗。「35B 追平 1T」正確的讀法要加上條件子句：**在它蒸餾過的長程 domain 裡**追平 1T。MLE-bench 的 43.9 對 72.7 就是條件子句的證據——需要長期目標一致性的開放工程任務，橫向蒸餾補不上，這還是參數和通用推理能力的地盤。

但加了條件子句之後，剩下的部分反而更有用。因為真實世界的企業 agent 多數不是開放工程任務，是有邊界的 domain 任務：查資料、跑流程、遵循規範、呼叫固定的工具集。這篇論文等於給了一張配方表：如果你的 domain 可以定義、可以驗證，那麼「長軌跡資料 + 驗證閘門 + domain teacher + 蒸餾」可以在 35B 上買到你這個 domain 的 1T 級表現。付出的代價是泛化能力——出了 domain，分數就是 Qwen 35B 級。

這其實是我在 FDE 模式裡反覆講的取捨在訓練端的鏡像：不追求一個什麼都會的通用系統，追求在客戶的具體 domain 裡把事情做到能用。

---

## 坦白說

這篇的所有分數都來自論文和官方 repo，Shanghai AI Lab 自己跑的，目前查不到第三方復現。SEAL-0 領先 DeepSeek-V4-pro 只有 1.4 分（56.4 對 55.0），這種差距在 benchmark 誤差範圍邊緣，「打贏」兩個字看看就好，方向意義大於名次意義。

KAG 四元組和 SVA top-k 的細節，我沒有逐段核對論文原文——機制描述以論文為準。基底模型也有一個小疑點：論文 Figure 1 的對照組是 Qwen3.6-35B-A3B，36kr 的報導寫的是從 Qwen3.5-35B-A3B 訓起，兩個來源對不上，我在文中不斷言基底是哪一顆。

另外，36kr 報導裡論文團隊自己承認的弱點值得照抄：模型在「plan before reasoning」和「reflect before acting」上還不夠好，長序列裡抓取相關歷史脈絡的能力也還有洞。這些正好是長程任務最核心的元能力——benchmark 分數領先，不代表這些底層能力已經解決。

我還沒實測這顆模型。35B MoE 的量化版本落在單卡工作站的射程內，排得進 RTX Pro 6000 待測清單的話，會用自己的工作流補第一手數據。

---

## 關鍵洞察

**Scaling 有兩個軸，第二個軸剛剛被證明便宜得多。** 參數軸上 35B 對 1T 差 30 倍，horizon 軸上把訓練資料換成 45K token 的驗證軌跡，就能在特定 domain 把這 30 倍抹平。昨天的 harness 篇是推理端的證據，這篇是訓練端的證據——選模型的時候，「它的訓練結構對不對你的任務」跟「它多大」至少同等重要。

**Domain 特化的小模型是拿泛化換分數，選型前先畫清楚自己的 domain。** Agents-A1 在蒸餾過的領域有 1T 級表現，在 MLE-bench 上被 GPT-5.5 甩開 29 分。拿到任何「小模型追平大模型」的宣稱，第一件事是把 benchmark 清單攤開，看領先的項目跟你的實際任務重不重疊。

**驗證閘門正在同時出現在推理端和訓練端。** Maka 的「分數不掉才合併」、KAG 的「過驗證才寫回」，是同一個工程紀律的兩個位置。如果你在自建 agent 資料或評測流程，這是最值得抄的一件事：驗證要當閘門，不要當事後抽查。
