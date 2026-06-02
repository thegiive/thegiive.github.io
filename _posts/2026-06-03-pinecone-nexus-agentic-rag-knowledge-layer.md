---
layout: post
title: "連 Pinecone 都說 Agentic RAG 有問題：Nexus、Knowledge Layer，跟一個被講爛的「RAG 已死」"
date: 2026-06-03 14:00:00 +0800
permalink: /pinecone-nexus-agentic-rag-knowledge-layer/
image: /assets/images/pinecone-nexus-knowledge-layer-cover.png
image_alt: "連 Pinecone 都說 Agentic RAG 有問題：Nexus 與 Knowledge Layer"
description: "過去一年「RAG 已死」的標題此起彼落，大部分都是誇張。但這次連親手定義 RAG 時代的 Pinecone（80 萬開發者、9000 付費客戶）都公開承認 Agentic RAG 有結構性問題，還發了 Nexus。這篇拆解 Nexus、Knowledge Layer 的趨勢（Karpathy、Google、Microsoft 同時在做），以及一個工程師該怎麼判斷：到底要不要投資這層東西。"
---

## 開場：又一篇「RAG 已死」？這次有點不一樣

過去一年，網路上「RAG 已死」的標題真的講到爛。

Agentic 檔案瀏覽出來，有人說 RAG 死了；長上下文視窗變大，有人說 RAG 死了；Agent Skills、Context Engineering……輪番被冠上「接班人」的名號。

坦白說，這些標題大部分都是**誇張加過度簡化**，看看就好。

但這次有點不一樣。本週，**親手定義 RAG 時代的那家公司——Pinecone——自己跳出來承認 Agentic RAG 有結構性問題**，同時發佈了一套新東西叫 Nexus（[官方公告：Pinecone Nexus — The Knowledge Engine for Agents](https://www.pinecone.io/blog/knowledge-infrastructure-for-agents/)）。

這件事的份量在哪？Pinecone 是市場領先的向量資料庫供應商，手上有逾 **80 萬名活躍開發者**、**9,000 個付費客戶**。等於是賣鏟子的人，跑出來跟你說「你們現在挖礦的方法有問題」。這種自我宣告，份量很重。

所以這篇不是要再喊一次「RAG 已死」。我反而想說的是：**RAG 沒死，但 Pinecone 點出的問題是真的，而且解法的方向，現在四家大公司同時在押注。**

## 一、先搞清楚：Pinecone 到底在罵哪一代 RAG？

很多人吵 RAG 死沒死，是因為大家講的根本不是同一個東西。RAG 的發展可以分三代：

| 世代 | 做法 | 狀態 |
|------|------|------|
| 第一代 Naive RAG | 查詢直接搜尋，不管檢索結果相不相關，硬塞進模型作答 | 這代確實可以說「已死」 |
| 第二代 Agentic RAG（RAG 2.0） | 把檢索包進 Agent 迴圈，由 Agent 自己決定何時查、查哪個資料源、要不要再查一次 | 主流，但問題浮現 |
| 知識層（Knowledge Layer） | Agent 不再直接挖資料源，改成查一層預先編好的知識 | 本週的新戰場 |

Pinecone 在公告裡點的四個痛點，全部是在打**第二代 Agentic RAG**：

- Agent 在一個 Agentic 迴圈裡，足足有 **85% 的運算時間**耗在知識檢索上；
- 產出的結果還是要**人手審核**才能採用；
- 任務完成率長期卡在 **50% 到 60%** 上不去；
- **Token 成本跟延遲完全失控**。

四項加起來，幾乎等於一張對 Agentic RAG 的判決書。

Pinecone 有個形容很傳神：Agentic RAG 就是「**Agentic 檢索的十條藍色連結**」——一次混合向量檢索，幫你抓回十段獨立的文字 chunk，然後丟給 Agent 自己拼。

聽起來很熟對不對？就是 Google 搜尋給你十條連結，只是這次換成餵給 Agent。**問題是，Agent 不見得比你會挑。**

## 二、坦白說：Agentic RAG 的三個病灶，我自己也踩過

Pinecone 講的三大病灶，我看完的第一反應是：**這不就是我自己天天在踩的鬼嗎。**

坦白說，這三個問題我全部踩過。而且講白一點——**我現在每天就是用一套類似「結構化 / syntax 知識庫」的方式在做事，根本不是純 RAG。**

為什麼？因為當你的知識庫變大、而且知識之間是**互相連結**的時候，純 RAG 真的解不了。

RAG 的本質是「把問題變成向量，去撈語意相近的 chunk」。但它撈回來的是一堆**互不相干的片段**——它不知道 A 文件的這段，其實是 B 文件那段的前提；它也不知道你這個專案的決策，是建立在三個月前另一個專案的教訓上。**語意相近 ≠ 邏輯相關。** 知識庫越大、跨越的脈絡越多，這個落差就越痛。

所以我自己的做法，是先把知識**整理成有結構、彼此明確連結**的形式（誰引用誰、誰是誰的前提、哪個取代了哪個），查的時候是順著這個結構走，而不是丟一句話進去賭向量撈得準。這跟 Pinecone 講的「不要十段 chunk，要結構化、可溯源的 Artifact」其實是同一件事——只是我用土法煉鋼在做，他們把它產品化了。

換句話說，我看到 Nexus 的當下並不覺得新奇，反而是一種「**啊，連 Pinecone 都走到這步了**」的印證感。

三個病灶：

**病灶一：非確定性。** 同一個問題問十次，Agent 可能用十種不同的檢索策略。多步推理之間還會累積偏差。對 demo 來說沒差，但企業要的是「同樣的問題，每次都給我同樣可靠的答案」，這點 Agentic RAG 給不了。

**病灶二：再強的推理也救不了爛檢索。** 底層資料如果結構混亂、不可靠，上面接再聰明的模型也是白搭。Garbage in, garbage out，這句老話在 AI 時代一個字都沒變。

**病灶三：Token 跟延遲爆炸。** 每一個子 Agent、每一次重新排序（re-rank）、每一次反思（reflection），都是實實在在的成本。

這個成本有多誇張？看 Pinecone 自家測試的數字：

- Agentic RAG：平均**每一條問題吃掉約 49,000 Token**
- AI Coding Agent：更猛，**528,000 Token**
- Nexus（他們的新方案）：只要**約 6,000 Token**

差到接近 **8 倍到 80 倍**。當然這是廠商自己設計的測試，要打點折扣，但量級的差距是真的。

## 三、轉折點：把推理從「查詢時」搬到「匯入時」

那 Nexus 是怎麼做的？

一句話：**Nexus 本質是一個「編譯後的知識引擎」，卡在資料源跟 Agent 中間。**

Agent 不再直接去挖資料源，而是去查一層**預先建好的知識層**。

核心理念其實很簡單，但很關鍵：

> 把昂貴的推理工作，從「**查詢階段**」前移到「**資料匯入階段**」。

換個說法：以前是用戶問一句，Agent 才現場去翻、去想、去拼；現在是資料進來的時候，就先把答案「**編譯**」好，存成一種叫 **Artifact** 的知識結構——帶有型別定義、欄位層級溯源（field-level lineage）的可信賴結構化資料。

這個前移，做過工程的人應該會有 déjà vu——**這不就是「預先算好」對上「即時運算」的老問題嗎？** 就像資料庫的 materialized view，或是前端的 SSG（靜態生成）對上 SSR（即時渲染）。把貴的運算挪到離線、挪到前面做，查詢的時候自然又快又穩。

Nexus 裡面有幾個零件：

- **Context Compiler**：本身是一個自主程式代理，在資料匯入時不斷迭代生成 Artifact，直到通過評估為止。它搭配三件工具運作：
  1. 使用者定義的**評估任務集**（代表性問題 + 標準答案）
  2. 一個預先審核過的**技能庫**（文件處理、文字分塊、實體抽取等）
  3. 一個**反饋迴路**
- **KnowQL**：一種宣告式的知識查詢語言，長得像 SQL（有 join、filter、projection），但多加了意圖、接地（grounding）、溯源、回應結構這些概念。

最關鍵的一點是：**Artifact 的結構不是人手定義的，是系統根據任務跟評估自動發現的。** 這代表領域專家就算完全沒有檢索背景，也能產出一層為 Agent 最佳化的知識。Agent 發一個工具呼叫，引擎直接吐結構化答案，不再丟十段 chunk 讓 Agent 自己猜。

## 四、這不是 Pinecone 一家的想法——四家在押同一個方向

我會特別寫這篇，是因為這如果只是 Pinecone 一家的產品發佈，那就只是一篇廣告。但讓我警覺的是：**至少有四股力量，幾乎同時在押同一個方向。**

| 來源 | 東西 | 知識層怎麼來 |
|------|------|--------------|
| Pinecone | [Nexus / Artifact](https://www.pinecone.io/blog/knowledge-infrastructure-for-agents/) | Agent 從資料源**自動合成** |
| Andrej Karpathy | [LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) | 模型維護一份持續累積的 Markdown Wiki，**自動合成** |
| Google（Cloud Next 2026） | [Knowledge Catalog](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/google-cloud-next-26-recap/) | 把 metadata 編成語義圖譜，經 MCP 暴露給 Agent，**偏人手綁定** |
| Microsoft | [Fabric IQ / Compiled Ontology](https://blog.fabric.microsoft.com/en-US/blog/whats-next-for-fabric-iq-ontology-the-operational-context-that-powers-your-ai-agents-preview/) | 先設計圖譜結構再綁資料源，**偏人手綁定** |

特別講一下 Karpathy 那個。一個月前，前 Tesla AI 總監 Andrej Karpathy 發了一篇 **[LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)**（累計逾 **1,900 萬次曝光、5,000 多個星標、3,600 多次分叉**），講的就是同一個概念：

> 不要每次都讓模型從原始文件重新發現知識，而是建立一份**持續累積、由模型自己維護的 Markdown Wiki**。查詢的時候，Agent 只要對 Wiki 提問，根本不用碰底層原始資料。

四套方案細節各有不同——Pinecone 跟 Karpathy 是讓 Agent **自動合成**知識結構，Google 跟 Microsoft 偏向**人手綁定**——但大方向是一致的：

> **Agent 不再直接對話資料源，全部經過一層 Knowledge Layer。**

當賣鏟子的、學界大神、跟兩家雲端巨頭同時指向同一個方向，這就不只是行銷話術了，這是個值得認真看的訊號。

## 五、量化對比，跟三個我還沒被說服的問題

先看 Pinecone 給的完整對比數據（再強調一次：**廠商自測，僅供參考**）：

| 方案 | Token | 耗時 | 準確率 / 完成率 |
|------|-------|------|------------------|
| **Nexus** | 6,733 | 22.7 秒 | 準確率 0.680 |
| Agentic RAG | 49,103 | 37.9 秒 | 準確率 0.413 |
| Coding Agent | 528,301 | 84.1 秒 | 完成 62.7% |

數字很漂亮。但這也是我要進「坦白說」的地方——**有三個問題，Pinecone 還沒回答，我自己也還沒被說服：**

**第一，Artifact 的編譯成本到底多高？** 你把推理前移到匯入階段，那匯入就變貴了。Coding Agent 這種持續迭代的場景、或是資料天天更新的場景，你就得不斷重新編譯。當年 **Microsoft Graph RAG** 就是栽在這——重算成本太高，難以為繼。Nexus 會不會重蹈覆轍，現在沒人知道。

**第二，LLM 生成、LLM 評估，會不會變成「有損摘要」？** Artifact 是 LLM 編出來的，又是 LLM 評估通過的。這條鏈子裡沒有一個地表真相（ground truth）來校準，會不會編著編著，離真相越來越遠？這是我最在意的一點。

**第三，遇到評估集沒覆蓋的開放式問題，怎麼回退？** 知識層是針對「代表性問題」編譯的。那長尾、沒被預期到的問題怎麼辦？如果回退到傳統混合搜尋，那 Agent 最後還是走回老路，這層知識層的意義就打折了。

這三個問題不解決，Nexus 對我來說就還是「很有意思，但先觀望」。

## 六、提煉原則：你到底要不要投資 Knowledge Layer？

講了這麼多，給個務實的判斷框架。

**我的結論是：Agentic RAG 並沒有死，它仍然是現階段的主流。** 原因很簡單——**把 Agent 接上資料源跟工具，遠比編譯一層知識層簡單**。簡單的東西不會那麼快被淘汰。

但下面這些情境，Knowledge Layer 確實值得投資：

### ✅ 值得投資 Knowledge Layer

| 情境 | 為什麼 |
|------|--------|
| 大量資料源要統一視圖 | 知識層幫你把分散的源頭編成一致的結構 |
| 任務重複、可預測 | 編譯成本可以攤提，越查越划算 |
| 需要嚴格的欄位層級溯源 | 金融、法務、稽核這類場景，溯源是硬需求 |

### ⚠️ 先別急著投資

| 情境 | 為什麼 |
|------|--------|
| Agent 偏探索式 | 問題長尾、沒邊界，編譯不划算 |
| 資料天天大改 | 重新編譯的成本會吃掉你省下的查詢成本 |
| 還在 POC 階段 | Agentic RAG 接起來快，先驗證價值再說 |

這個判斷邏輯，跟我之前寫 [PostgreSQL 當 Vector Store](/postgresql-vector-store-pragmatic-choice/) 那篇其實是一脈相承的——**架構不是選最新的，是選最適合你場景的。**

### 想試水溫？我建議直接從 LLM Wiki 開始

如果你看完上面那些表格，心裡還是「聽起來很厲害但不知道從哪下手」，我給一個最低成本的起點：**先試 [Karpathy 的 LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。**

為什麼推這個？

- **超簡單**：它本質就是一份 Markdown 檔。你不用買 Pinecone、不用學 KnowQL、不用建圖譜。就是讓 Agent（Claude Code、Codex 都行）幫你把知識持續整理、互相連結成一份 Wiki，查的時候對 Wiki 問就好。
- **導入成本低到沒理由不試**：一個 gist、一個資料夾、一個下午。失敗了你也沒損失什麼。
- **而且就算不好用也沒差**：這是我最看重的一點——**因為你整理好的是一份結構化的純文字檔，它幾乎可以「瞬間搬家」。** 今天用 LLM Wiki，明天想換 Nexus、換 pgvector、換 Fabric IQ，那份整理好的知識直接匯進去就行，不會被任何一家廠商鎖死。

這就回到我前面講的——**RAG 的天花板在資料，不在工具。** 你只要先把「整理成有結構、彼此連結的知識」這件事做出來，工具反而是最後才需要煩惱、而且隨時可以換的東西。LLM Wiki 的價值，就是讓你用最低成本先把這個習慣養起來。

### 最後，工程師的好消息：你其實可以自己做

這也是我最想講的一點。如果你清楚知道自己需要的 Artifact 長什麼樣，**這層東西你完全可以自己實作，不一定要買 Nexus：**

1. 設計對應的**資料表結構**（就是你的 Artifact schema）
2. 透過**批次處理**從各資料源把資料匯進來
3. 存進資料庫並**建索引**
4. 加一個**差量更新（incremental update）**機制，解決重新編譯成本的問題
5. 查詢語言？**換成 SQL 就好了**，不用學 KnowQL

是不是很眼熟？這跟我一直在講的 [pgvector 務實路線](/postgresql-vector-store-pragmatic-choice/) 幾乎是同一套工程哲學。Pinecone 把它包裝成 KnowQL + Artifact + Context Compiler，聽起來很高級，但拆開來看，骨架就是「**ETL + schema + index + 差量更新**」這些做資料工程的人做了二十年的東西。

> 整個方向真正的啟示不是某個產品，而是這句話：**把推理工作從查詢階段，前移到資料編譯階段**。這會是未來 Agent 系統設計的一個重要選擇。

賣鏟子的人都開始改賣「編譯好的礦」了。你不一定要跟著買，但你最好知道這件事正在發生。

---

## 延伸閱讀

- [為什麼我選擇 PostgreSQL 當 Vector Store？](/postgresql-vector-store-pragmatic-choice/)
- [PostgreSQL 當 AI Memory Store 的實戰](/postgresql-ai-memory-store/)
- [Stanford 論文實錘：Context Engineering 比 Fine-tuning 更適合 AI Agent（ACE 框架）](/ace-agentic-context-engineering-stanford-playbook-evolution/)
- [Google Nested Learning：讓模型擁有大腦般的長期記憶](/google-nested-learning-ai-memory-breakthrough/)
- [Pinecone Nexus 官方公告：The Knowledge Engine for Agents](https://www.pinecone.io/blog/knowledge-infrastructure-for-agents/)
- [Better Models Won't Save Your Agent（Pinecone）](https://www.pinecone.io/blog/introducing-nexus-knowledge-engine/)
- [VentureBeat：The RAG era is ending for agentic AI — a new compilation-stage knowledge layer is what comes next](https://venturebeat.com/data/the-rag-era-is-ending-for-agentic-ai-a-new-compilation-stage-knowledge-layer-is-what-comes-next)
- [Andrej Karpathy：LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Google Cloud Next '26：Knowledge Catalog（官方 recap）](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/google-cloud-next-26-recap/)
- [Microsoft Fabric IQ Ontology（官方部落格）](https://blog.fabric.microsoft.com/en-US/blog/whats-next-for-fabric-iq-ontology-the-operational-context-that-powers-your-ai-agents-preview/)
