---
layout: post
title: "同一個系統在同一個測評上，出現四個分數：65.99、84、58.44、75.14 — Agent Memory 評測羅生門，與檔案系統派的翻案"
date: 2026-07-16 09:00:00 +0800
permalink: /agent-memory-benchmark-rashomon-filesystem/
image: /assets/images/agent-memory-benchmark-locomo-rashomon-cover.jpg
description: "Agent memory 賽道已經有標準測評三件套：LoCoMo、LongMemEval、BEAM，每家框架都往上面報分數。但 Zep 這一個系統在 LoCoMo 上，Mem0 測出 65.99、Zep 自己測出 84、Mem0 修正成 58.44、Zep 再反修正成 75.14——同一個系統、同一個測評、四個數字。更有意思的是 Letta 用純檔案系統加 grep 拿到 74.0，打敗專業 memory 系統。這篇拆解三個標準測評各測什麼、為什麼分數會變成羅生門，以及檔案系統派——從 Letta 的實驗、ByteDance 的 OpenViking、到我自己手工維護的 llm-wiki——為什麼值得認真看。"
---

2025 年 Zep 發了一篇標題很嗆的 blog：[Lies, Damn Lies, & Statistics](https://blog.getzep.com/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/)，反擊 Mem0 論文把它測成 65.99 分，宣稱自己正確設定下是 84 分。Mem0 的工程師接著[開了一個 GitHub issue](https://github.com/getzep/zep-papers/issues/5)，指出 Zep 的算法把測評規範明文排除的 adversarial 題目也算了進去，修正後是 58.44 分。Zep 再反駁：Mem0 把我們的系統設定錯了，正確數字是 75.14。

同一個系統，同一個測評，四個數字：65.99、84、58.44、75.14。

這不是小廠互咬。Mem0 和 Zep 都在這個賽道募資規模最前段的公司之列，吵的 LoCoMo 是整個 agent memory 領域引用最多的標準測評。如果你最近在幫自己的 agent 選 memory 框架、看過任何一張 leaderboard 截圖，這場架跟你直接相關——因為它說明那些分數的可信度，比你以為的低很多。

這篇先把三個標準測評講清楚，再看主流框架的分數到底怎麼讀，最後講一個測評大戰意外驗證的方向：檔案系統派。

---

## 30 秒定位：Agent Memory 的標準測評

| 測評 | 出處 | 規模 | 測什麼 |
|------|------|------|--------|
| LoCoMo | Snap Research，ACL 2024 | 10 段對話、1,540 題 | 超長對話後的回憶：single-hop、multi-hop、開放域、時間推理 |
| LongMemEval | Wu et al.，ICLR 2025 | 500 題 | 更細的能力拆解：知識更新、時間推理、跨 session 推理、偏好回憶 |
| BEAM | arXiv 2510.27246 | 100 段對話、2,000 題、最長 10M tokens | 記憶量大到 context window 裝不下之後，系統還剩多少 |
| MemBench | Tan et al., 2025 | 研究用，尚未成為工業標準 | 準確率之外，加測操作效率與「記憶庫變大後的衰退」 |

三件套裡，LoCoMo 管「記不記得」，LongMemEval 管「哪種記憶能力弱」，BEAM 管「規模撐不撐得住」。MemBench 還在研究端，但它測的維度（記憶庫用久了會不會退化）是前三個都沒碰的。

![三大標準測評各測什麼與各自的盲區](/assets/images/agent-memory-benchmark-three-benchmarks.jpg)

---

## LoCoMo：引用最多，也最小

[LoCoMo](https://aclanthology.org/2024.acl-long.747/) 的設計很直接：生成多人、多 session 的超長對話——平均每段 600 個對話輪次、16K tokens、最多橫跨 32 個 session——再問模型「某人幾週前提過的事」。分數即答對率。

它成為標準有兩個原因。第一，它出得早（2024 年中），賽道起飛時它是唯一現成的尺。第二，它的四類題目（單跳、多跳、開放域、時間推理）剛好對應 memory 系統的核心賣點。

但它有一個很少被放在行銷材料裡的事實：**整個測評只有 10 段對話。** 1,540 題全部從這 10 段裡出。[一篇針對 memory 測評的批判性分析](https://essays.bloo-mind.ai/posts/2026-05-20-mem-eval/)把這點講得很直白：樣本這麼小，每類題目的分數差異在統計上根本站不住，而各家還在用小數點後兩位的差距宣稱勝利。

另一個問題是飽和。Mem0 [2026 年的年度報告](https://mem0.ai/blog/state-of-ai-agent-memory-2026)自報 LoCoMo 92.5 分——而他們 2025 年 ECAI 論文時期的成績大約是 68 分。一年之內從 68 到 92.5，一部分是演算法真的在進步，另一部分是這把尺已經快被量到頂了。

## LongMemEval：能力拆解做得更細

[LongMemEval](https://arxiv.org/abs/2410.10813)（ICLR 2025）比 LoCoMo 晚一年，明顯是衝著前者的盲區設計的。500 題分成多個能力類別，其中兩類是 LoCoMo 測不到的：

**知識更新**：用戶上個月說住台北，這個月說搬去高雄了。你的 memory 記的是哪一個？這是生產環境最常見的記憶失效模式——記得住不難，「用新的蓋掉舊的」才難。

**時間推理**：不只問「用戶說過什麼」，還問「用戶是什麼時候說的、在他說 X 之前還是之後」。這直接考驗系統有沒有把時間當一等公民存——也就是 Zep 那套 temporal knowledge graph 存在的理由。

LongMemEval 自己也有方法論問題：它的填充對話是從其他資料集拼進來的，風格跟證據對話不一致，[批判分析指出](https://essays.bloo-mind.ai/posts/2026-05-20-mem-eval/)系統可能靠「風格不一樣」就認出哪段是證據，而不是真的靠記憶檢索。另外它的偏好類題目只有 30 題，統計效力同樣很弱。

## BEAM：把規模拉到 10M tokens，所有人都難看

前兩個測評有一個共同的尷尬：規模太小。LoCoMo 一段對話平均 16K tokens——**現代模型的 context window 直接塞得下。** 一個「把整段歷史丟進 prompt」的無腦 baseline，在這種規模下就很能打。你花錢部署的 memory 系統如果只贏這個 baseline 幾分，價值要打上問號。

[BEAM](https://arxiv.org/abs/2510.27246)（Beyond a Million Tokens）正是衝著這個來的：100 段對話、2,000 題，對話長度拉到 1M 和 10M tokens——這是任何 context window 都裝不下、非得有記憶系統不可的規模。

結果是所有系統都難看。Mem0 自報 1M tokens 拿 64.1，10M 掉到 48.6。Hindsight [宣稱自己是 BEAM 第一](https://hindsight.vectorize.io/blog/2026/04/02/beam-sota)。不管誰第一，跟 LoCoMo 上動輒 90 分的畫面對比，BEAM 露出了這個賽道的底：**在真正需要記憶系統的規模上，記憶系統還沒有一個能打的。**

---

## 主流框架的分數：一張沒辦法做成 leaderboard 的表

照理說這一節應該放一張各框架分數對比表。但誠實的做法是先講清楚：**這些數字來自不同的測試者、不同的設定、不同的時間點，不能直接橫比。** 所以下表多了一欄「誰測的」——這一欄比分數本身重要。

| 系統 | LoCoMo | LongMemEval | BEAM（1M / 10M） | 誰測的 |
|------|--------|-------------|------------------|--------|
| Mem0 | 92.5 | 94.4 | 64.1 / 48.6 | Mem0 自己（2026） |
| Zep | 58.44 – 84 | 自報比 full-context baseline 最高 +18.5% | 未公開 | LoCoMo 雙方各執一詞；LongMemEval 來自 [Zep 論文](https://arxiv.org/abs/2501.13956) |
| Letta | 74.0 | 未公開 | 未公開 | Letta 自己 |
| OpenViking | 82.08 | 未公開 | 未公開 | OpenViking 自己 |
| Hindsight | 未公開 | 未公開 | 73.9 / 64.1 | [Hindsight 自己](https://hindsight.vectorize.io/blog/2026/04/02/beam-sota) |

幾個備註。Mem0 的 LoCoMo 在 2025 論文時期約 68，一年內演進加上測評飽和才到 92.5。Zep 的 LoCoMo 是 65.99（Mem0 論文）→ 84（Zep）→ 58.44（Mem0 修正）→ 75.14（Zep 反修正）的羅生門，而它的 LongMemEval 論文只報「相對 baseline 的提升幅度」，沒有可橫比的絕對分數。Letta 的 74.0 不是產品本體，是**純檔案系統 + grep**（下一節）。Hindsight 的 BEAM 對比裡，次佳系統 Honcho 只有 40.6、RAG baseline 24.9——但同一個 BEAM 10M，Mem0 自己測自己有 48.6，Hindsight 那場卻沒測 Mem0。兩場測試對不起來，這正是問題所在。

四個讀表規則，比表格本身有用：

第一，**每個高分旁邊都站著一個對自己有利的 baseline。** OpenViking 的「3.39 倍提升」是跟 agent 產品的陽春內建記憶比，不是跟 Mem0 比。Mem0 的 92.5 是自報，第三方複測的歷史（見 Zep 案例）顯示自報和複測可以差 25 分。

第二，**vendor 之間互測必然打架。** Zep 羅生門的技術細節（該不該含 adversarial 題、API 版本、timestamp 支援）每一項都是合理爭點——這恰恰說明測評協議本身沒有標準化，分數是「測法」的函數，不只是「系統」的函數。

第三，**差距小於 10 分就當雜訊。** 10 段對話、自報分數、協議不一——這種條件下的個位數差距，不構成選型依據。

第四，**表格裡的空格也是資訊。** 每一家都只報自己贏的那個測評：Mem0 三個都報（它三個都想贏），Hindsight 只報 BEAM（它的差異化是規模），OpenViking 只報 LoCoMo 加上自選的 RAG 和任務測評，Letta 做完檔案系統實驗後乾脆主張測評本身不重要。看到一個框架「沒報」某個標準測評的分數，合理的預設不是它沒測，是它測了但數字不好看。

這個 blog [寫過 EFC 那篇論文](agent-harness-effective-feedback-compute.md)：raw compute 只能解釋 agent 表現的三四成，反饋品質才是主變數。memory 測評是同一個故事的另一面——**分數只能解釋 memory 系統價值的一部分，測法和 baseline 的選擇解釋了剩下的。**

---

## Letta 的實驗：檔案系統 + grep，74 分

測評大戰裡最有意思的一個數據點，來自 Letta 的一篇 blog：[Benchmarking AI Agent Memory: Is a Filesystem All You Need?](https://www.letta.com/blog/benchmarking-ai-agent-memory/)

他們做了一個幾乎是挑釁的實驗：不用任何專業 memory 系統，把 LoCoMo 的對話歷史直接存成檔案，給 agent 四個工具——grep、search_files、open、close——用 gpt-4o-mini 跑。

結果：74.0 分。同一場測試裡，Mem0 的 graph 變體拿 68.5。

![Letta 檔案系統實驗：files + grep 74.0 分 vs Mem0 graph 變體 68.5 分](/assets/images/agent-memory-benchmark-letta-filesystem.jpg)

**一個檔案櫃加一支手電筒，打敗了專業記憶系統。** Letta 自己的結論是：memory 的品質更多取決於 agent 管理 context 和呼叫工具的能力，而不是檢索機制本身。換句話說，這兩年大家在向量庫、知識圖譜、temporal graph 上堆的複雜度，在 LoCoMo 這個規模下，價值可能還不如「讓 agent 自己翻檔案」。

這跟 [harness 三次中心遷移那篇](agent-harness-three-migrations-mechanism.md)的結論同構：能力的瓶頸經常不在你以為的那一層。Prompt 時代大家磨措辭，真正的槓桿在 harness；memory 賽道大家磨檢索演算法，Letta 的實驗暗示真正的槓桿在 agent 的 context 管理能力。

## OpenViking：把檔案系統派做成產品

Letta 的實驗是個 baseline 挑釁，ByteDance 火山引擎開源的 [OpenViking](https://github.com/volcengine/OpenViking)（26.8k stars）則是把同一個哲學做成了正式的 infra：整個 context database 就是一個檔案系統，`viking://` 協議把記憶、知識、技能組織成階層目錄，agent 像瀏覽檔案一樣導航。

它比裸檔案系統多了一層關鍵設計——三層漸進載入：L0 是一句話摘要，L1 是約 2K tokens 的概覽，L2 才是全文。agent 先掃 L0 判斷相關性，需要才往下鑽。官方自報這個設計讓 input tokens 減少 91%，同時 LoCoMo 拿 82.08（baseline 是 OpenClaw 原生記憶的 24.20——again，看 baseline）。

檔案系統派的路線圖至此完整：Letta 證明了下限夠高，OpenViking 補上了規模化缺的那層索引。

---

## 那我的 llm-wiki 呢：一個沒有分數的系統，和它為什麼還是我的主力

講到這裡可以攤牌了。我自己維護 blog 知識庫的方式，是一個叫 llm-wiki 的 skill：274 篇文章原文存成 markdown 檔、270 篇機器生成的摘要頁、13 個概念頁、12 個實體頁，全部用 wiki link 交叉連結，agent 用檔案工具在裡面導航和查詢。

對照上一節，這就是手工版的 OpenViking：摘要頁是 L0/L1，原文是 L2，concept/entity 頁承擔 multi-hop 的角色——兩篇文章的關聯不靠向量相似度算出來，靠一條寫死的 `[[連結]]`。它也是 [Pinecone Nexus 那篇](pinecone-nexus-agentic-rag-knowledge-layer.md)講的 Knowledge Layer 趨勢的個人實作。

![知識管理與對話記憶考的是不同的東西](/assets/images/agent-memory-benchmark-llm-wiki-knowledge.jpg)

那它在標準測評上幾分？

**零分。不是考砸了，是根本沒考過。** 而且老實講，它去考也不對題：LoCoMo 三件套測的是「對話記憶」——用戶說過什麼、什麼時候說的。llm-wiki 管理的是「知識」——文章、概念、它們之間的關係。前者的難點在時間和更新，後者的難點在結構和連結。拿對話測評考知識庫，就像拿背單字考圖書館員。

但這個版圖對它還是有指導意義的。逐項對：

- **Multi-hop**：wiki 的強項。cross-link 就是預先算好的多跳路徑，這是我當初選 wiki 而不是向量庫的主因。
- **知識更新**：做得到但靠紀律。改一個事實要改到摘要頁和 concept 頁，靠 lint script 抓 dead link，沒有 Zep 那種自動 invalidation。
- **時間推理**：明確的弱項。頁面沒有 valid_at 時間戳，「我三月時對這件事的看法」查不到，只有 git history 勉強算。
- **BEAM 級規模**：未知。274 篇文章離 10M tokens 還遠，grep 還很快。到十倍規模會不會垮，我沒有數據。

如果你正在幫自己的 agent 選 memory 方案，這一節的換位版本是：先前你的決策可能是「打開 leaderboard，挑分數最高的接上去」；看完測評羅生門之後，比較合理的順序是——先跑一週 files + grep 的 baseline，用你自己的工作負載記錄它哪裡不夠（是量太大、更新太頻繁、還是時間查詢多），再拿這個具體缺口去比對哪個系統值得付錢。**專業 memory 系統要贏的不是彼此，是你的檔案櫃。**

---

## 反方：檔案系統派的翻案，不也是建立在同一個爛測評上？

這是對本文最強的反駁，我得自己先講。

Letta 的 74 分，測的還是那個只有 10 段對話、每段 16K tokens 的 LoCoMo。前面才說過這個規模「塞進 context window 都行」——那檔案系統派的勝利，會不會只是「在一個小到不需要記憶系統的測評上，證明了不需要記憶系統」？循環論證。到 BEAM 的 10M tokens，grep 掃全庫的延遲和雜訊會爆炸，檔案系統派在真正困難的規模上一個分數都拿不出來。

這個反駁大部分成立，我不打算硬拗。所以本文的主張要收窄：**不是「檔案系統贏了」，是「在你的工作負載超過某個規模之前，最簡單的方案就是對的方案」。** 多數個人開發者和中小團隊的 agent，記憶量離 10M tokens 很遠——我自己 274 篇文章的 wiki 是現成的例子。而規模真的上去之後怎麼辦，OpenViking 的 L0/L1/L2 是檔案系統派目前給出的答案，但它在 BEAM 上同樣沒有公開成績。10M tokens 這一關，目前是全賽道一起卡著，沒有哪一派過了。

---

## 坦白說

這篇文章有三個先天限制。

第一，**文中每一個分數都是 vendor 自報的**，包括我用來翻案的 Letta 74 分。Letta 是 Mem0 和 Zep 的直接競爭者，它發表「檔案系統就夠了」的實驗，跟 Zep 發表「我們比 Mem0 高 24%」的動機結構相同。第三方獨立複測在這個賽道目前不存在。

第二，本文介紹的三件套只覆蓋「對話記憶」。agent 記憶還有一大塊是任務經驗——做過一次之後下次會不會更好——目前只有 tau2-bench 這類任務測評被借來間接測（OpenViking 自報 retail 任務 70.94 提升到 77.81）。這塊幾乎沒有標準可言，本文也沒能力補上。

第三，llm-wiki 那一節是架構類比，不是實測。「摘要頁等於 L0/L1」是我的對應，不是任何測評驗證過的等價。我說它是「我最喜歡的方案」，成分是工作流偏好加上零遷移成本，不是量測結果。它跟 Mem0 對打會是什麼分數，我不知道，也暫時沒有對題的尺可以量。

---

## 關鍵洞察

- 看到任何 memory 分數，先問三個問題：誰測的、baseline 是誰、協議裡含不含爭議題型。Zep 案例證明這三個變數可以讓同一個系統差出 25 分。差距小於 10 分，當雜訊處理。
- 選型之前先跑最便宜的 baseline：把歷史塞 context window，或 files + grep。專業系統的價值不是絕對分數，是它比你的檔案櫃多出來的那一段——多數場景下這一段比行銷材料裡的小。
- 三件套測「記不記得」，不測「記憶讓下一次任務變好多少」。生產環境在乎的是後者。部署後追蹤你自己的任務成功率變化，比任何 LoCoMo 分數都有效。
- 規模是真正的分水嶺：16K tokens 的對話什麼方案都能用，1M tokens 以上目前全賽道大幅衰退。評估宣稱時先看它在哪個規模測的——「解決了 memory」的宣稱，目前沒有一個在 BEAM 規模上成立。

## 常見問題 Q&A

**Q: 所以到底該選 Mem0、Zep、Letta 還是 OpenViking？**

先跑 files + grep 一週，記錄具體缺口再說。缺時間推理選 temporal graph 路線（Zep），缺自動抽取選 Mem0，要 agent 長時間自主運行看 Letta，想要檔案系統範式加現成的分層索引看 OpenViking。沒有缺口，就不要加系統。

**Q: LoCoMo 分數還值得看嗎？**

值得看趨勢，不值得看排名。一個系統自己從 68 進步到 92 有資訊量；A 系統 85 對 B 系統 82 沒有。

**Q: 為什麼不自己把 llm-wiki 拿去跑 LoCoMo？**

因為不對題——LoCoMo 的輸入是多 session 對話，llm-wiki 的輸入是文章。硬要跑等於重新實作一個對話記憶系統再掛 wiki 的名字，測出來的不是 wiki 本身。比較誠實的做法是等知識管理類的測評出現，或用自己的查詢紀錄做回歸測試——這是我接下來想做的事。
