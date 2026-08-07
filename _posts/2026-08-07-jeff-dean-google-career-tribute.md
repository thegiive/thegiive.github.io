---
layout: post
title: "AI 時代為什麼需要 Jeff Dean 這種人：超前的技術品味 + 把願景變成 60 億 RPS 系統的落地能力"
date: 2026-08-07 09:00:00 +0800
permalink: /jeff-dean-google-career-tribute/
description: "AI 時代最不缺聰明人，缺的是同時具備兩種能力的人：超前於時代的技術品味（2011 年多數人覺得神經網路過時，Dean 啟動 Google Brain；2004 年 MapReduce 定義了產業十年的範式），以及把願景變成承載數十億使用者系統的落地能力（Bigtable 峰值 60 億 RPS、TensorFlow 全球最廣泛的 ML 框架、TPU 讓 AI 推論經濟可行）。2026 年 8 月 5 日，Google 第 30 號員工 Jeff Dean 離開了待了 27 年的 Google。這篇回顧他從 WHO AIDS 預測軟體到 Google Chief Scientist 的完整生涯——27 年只做一件事：在技術即將被規模壓垮時，重新設計系統，讓複雜度變成其他人可以站上去的地板。"
image: /assets/images/jeff-dean-career-tribute-cover.png
categories: [AI 產業分析, 科技人物]
tags: [Jeff Dean, Google, Google Brain, TensorFlow, MapReduce, 分散式系統]
author: Wisely Chen
---

![Jeff Dean（圖片來源：[Wikipedia](https://en.wikipedia.org/wiki/Jeff_Dean)）](/assets/images/jeff-dean-career-tribute-cover.png)

<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;margin:30px 0"><iframe src="https://www.youtube.com/embed/B7BOwEIib_k" style="position:absolute;top:0;left:0;width:100%;height:100%" frameborder="0" allowfullscreen></iframe></div>

Jeff Dean 在 Google 待了整整 27 年——1999 年中加入，大約是公司第 30 號員工。他幾乎從頭到尾參與並主導了 Google 從「搜尋引擎」變成「全球基礎設施 + AI 帝國」的全過程，推動了三次重大技術轉型，每一次都讓 Google 在該領域取得領先地位：

**第一次，解決網際網路搜尋的規模問題。** 1999 年加入時，Google 的搜尋索引系統正面臨成長危機。Dean 參與重建了五代搜尋爬蟲、索引與查詢服務系統，讓處理能力跟上全球網路的指數成長。

**第二次，用 MapReduce 與 Bigtable 定義大數據與雲端運算的範式。** 2004 年的 MapReduce 讓數千台普通機器變成一個簡單介面，Bigtable 則把半結構化資料儲存推到峰值每秒 60 億次請求的規模。這兩套系統啟發了 Hadoop 等開源生態系，讓「大數據處理」從少數網路公司的內部能力，變成整個產業的標準工程實踐。

**第三次，帶領 Google 走進深度學習時代。** 2011 年共同創辦 Google Brain，打造 DistBelief 證明大規模分散式訓練可行；接著主導 TensorFlow 的設計、開源，讓全球研究者都能使用同一套框架；再推動 TPU 專用晶片，把 AI 推論成本壓到能塞進每一個 Google 產品。

三次轉型，橫跨搜尋、基礎設施、AI，看起來是三個不同的領域。但 Dean 在做的始終是同一件事：在技術即將被規模壓垮時，找到瓶頸，重新設計系統，讓複雜度被基礎設施吸收。

![27 年只做一件事：設計基礎設施來吸收混亂](/assets/images/jeff-dean-slide-03.png)

這背後需要兩種極其罕見的能力同時存在——

**超前於時代的技術品味。** 不是跟著趨勢走，是在趨勢成形之前就做了選擇。2011 年多數人認為神經網路是上一代的過時技術，Dean 啟動了 Google Brain。2004 年的 MapReduce 和 2012 年的 Spanner 定義了產業後來十年的基礎設施範式——產業不是跟上了這些技術，是花了好幾年才追上來。

**把願景變成跑在生產環境裡的系統的能力。** 技術品味好的人不少，但多數停在論文、原型、或概念階段。Dean 的每一個判斷，最後都變成了承載數十億使用者的基礎設施：MapReduce 在論文發表前就已經在 Google 內部每天跑超過一千個工作；TensorFlow 成為全球使用最廣泛的深度學習框架；TPU 把推論成本壓到讓 AI 經濟可行。

品味決定做什麼。落地能力決定它是不是真的存在。兩者同時具備的人，在任何時代都極度稀缺。

![品味與落地](/assets/images/jeff-dean-slide-02.png)

2026 年 8 月，Jeff Dean 結束了在 Google 長達 27 年的職業生涯。這篇文章不是在寫他離開的新聞。這是在回顧一個人如何用 27 年，反覆做同一件事——在技術即將被規模壓垮時，重新設計系統，讓原本只有少數專家能處理的複雜度，變成其他工程師可以直接站上去的地板。[Google 官方公告](https://blog.google/company-news/inside-google/message-ceo/next-chapter-ai-momentum/)

---

## 起點不是搜尋，而是公共衛生

Jeff Dean 1990 年以最高榮譽取得明尼蘇達大學電腦科學與經濟學學士。他的兩篇榮譽論文，一篇研究神經網路的平行訓練，另一篇研究 HIV/AIDS 的經濟影響。1996 年，他在 Craig Chambers 指導下取得華盛頓大學電腦科學博士，研究物件導向語言的編譯器最佳化。[Google Research 個人頁](https://research.google/people/jeff/)

更早以前，他就已經在用程式處理真實世界的問題。高中與大學暑假期間，Dean 曾在美國疾病管制與預防中心及世界衛生組織參與開發 Epi Info 流行病學軟體。1990 至 1991 年，他在 WHO 的 Global Programme on AIDS 工作，為 HIV 疫情撰寫統計建模、預測與分析軟體。[Google Research 個人頁](https://research.google/people/jeff/)

1996 至 1999 年，Dean 進入 Digital Equipment Corporation 的 Western Research Lab，研究低負擔效能分析工具、亂序執行微處理器的分析硬體，以及網路資訊檢索。他也在這段期間與後來最重要的長期搭檔 Sanjay Ghemawat 共事。[Google Research 個人頁](https://research.google/people/jeff/) [The New Yorker](https://www.newyorker.com/magazine/2018/12/10/the-friendship-that-made-google-huge)

從流行病預測、編譯器最佳化到處理器效能，題目看起來很分散，卻已經出現他往後職涯的一貫方向：先找出系統真正的瓶頸，再設法讓它在更大的規模下仍能運作。這是本文根據其工作軌跡所做的歸納，不是 Dean 的公開原話。

![建立直覺：真實世界演練](/assets/images/jeff-dean-slide-04.png)

---

## 1999 年加入 Google：先把搜尋救活

Jeff Dean 在 1999 年中加入成立不久的 Google。2000 年 3 月，Google 的網頁索引系統陷入危機：爬蟲與索引更新已經停擺數月，使用者拿到的搜尋結果落後約五個月；公司當時又正在爭取替 Yahoo 提供更大規模的搜尋索引。[The New Yorker](https://www.newyorker.com/magazine/2018/12/10/the-friendship-that-made-google-huge)

《紐約客》記錄了那個近乎創業神話的場景：六名工程師進入臨時戰情室，Dean 把椅子滑到 Ghemawat 的電腦旁，兩個人共同追查問題、重寫系統。Ghemawat 操作鍵盤，Dean 在旁邊思考與修正。他們後來經常用這種方式一起工作，成為 Google 工程史上最知名的長期搭檔之一。[The New Yorker](https://www.newyorker.com/magazine/2018/12/10/the-friendship-that-made-google-huge)

Dean 後來回顧，自己參與設計與實作五代 Google 搜尋的爬蟲、索引與查詢服務系統，支撐的文件量、每秒查詢量與更新頻率成長了二到三個數量級。他也參與最初的廣告服務系統、AdSense、Google News、搜尋排序實驗系統，以及早期叢集工作排程器。[Google Research 個人頁](https://research.google/people/jeff/)

Google 的創辦人設計了搜尋引擎的方向；Dean 與那一代基礎設施工程師，則把它變成能承受全球網路成長的服務。

![第一次跨越：拯救搜尋引擎](/assets/images/jeff-dean-slide-05.png)

---

## MapReduce：把幾千台機器變成一個簡單介面

當資料大到一台電腦不可能處理，工程師不只要寫資料分析邏輯，還得自己處理資料切分、機器排程、網路通訊與硬體故障。Dean 與 Ghemawat 在 2004 年發表的 MapReduce，把這些複雜工作收進執行系統，讓開發者主要描述 map 與 reduce 兩個步驟，程式就能自動在大量普通機器上平行執行。[MapReduce 原始論文](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/)

論文發表時，Google 內部已經實作數百個 MapReduce 程式，每天在叢集上執行超過一千個工作。搜尋索引的建立、日誌分析、地圖渲染——Google 最核心的資料處理工作幾乎都在 MapReduce 上跑。它後來啟發 Apache Hadoop 等開源系統，讓「大數據處理」從少數大型網路公司的內部能力，逐漸變成整個產業可以採用的工程模式。[MapReduce 原始論文](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/) [Google Research 個人頁](https://research.google/people/jeff/)

MapReduce 最重要的地方不只是速度，而是抽象。它沒有讓機器停止故障，而是讓大部分使用者不需要親自處理每一次故障。

這正是 Dean 最具代表性的工程風格：問題沒有消失，但複雜度被系統接管了。

---

## Bigtable 與 Spanner：重新定義資料可以放多大、放多遠

Dean 也是 Bigtable 的共同設計者與實作者。這套大型半結構化儲存系統支撐了 Google 上百個產品——Search、Analytics、YouTube、Maps 都靠它運作。依 Dean 的 Google Research 頁面所列數據，Bigtable 在 2023 年的尖峰負載超過每秒 60 億次請求，管理的資料量超過 10 exabytes。Bigtable 後來成為對外提供的 Cloud Bigtable，也直接影響了開源社群的 HBase、Cassandra 等 NoSQL 資料庫的設計。[Google Research 個人頁](https://research.google/people/jeff/)

2012 年發表的 Spanner 則把問題推到全球尺度。Spanner 透過 Paxos 與跨資料中心的高精度同步時鐘，在地理分散的資料庫中提供強一致性與交易能力。Dean、Ghemawat 與其他共同作者的論文，後來成為全球分散式資料庫的重要里程碑。[Google Research：Spanner](https://research.google/pubs/spanner-googles-globally-distributed-database/)

需要特別釐清一個常見誤傳：2003 年 Google File System 論文的作者是 Sanjay Ghemawat、Howard Gobioff 與 Shun-Tak Leung，名單裡沒有 Jeff Dean。Dean 對 Google 早期基礎設施貢獻極大，但不能因為他與 Ghemawat 長期合作，就把 GFS 論文也算成他的作品。[Google Research：Google File System](https://research.google/pubs/the-google-file-system/)

2012 年，ACM 將 ACM-Infosys Foundation Award——後來更名為 ACM Prize in Computing——共同頒給 Dean 與 Ghemawat，表彰兩人設計與實作 Google 大量核心軟體基礎設施，並推動網際網路規模運算與雲端運算的發展。[ACM 官方新聞稿](https://awards.acm.org/binaries/content/assets/press_releases/infosys-award-2012.pdf)

![第二次跨越：將故障藏在介面之後](/assets/images/jeff-dean-slide-06.png)

---

## 從分散式系統轉進神經網路

2011 年，Dean 共同創辦 Google Brain。團隊早期打造 DistBelief，讓大型神經網路可以分散到大量機器上訓練。在當時的非專用硬體上，他們曾訓練約 20 億個非嵌入參數的模型；DistBelief 後來被 Google 內部數百個專案使用。[Google Research 個人頁](https://research.google/people/jeff/)

2012 年廣為人知的「貓神經元」研究，也建立在這套系統上。研究團隊讓大型神經網路從未標記的 YouTube 影片影格中自行學習表徵，並觀察到能對人臉、人體與貓臉產生反應的高階特徵。這項研究的作者包括 Quoc Le、Marc’Aurelio Ranzato、Rajat Monga、Dean、Andrew Ng 等人。[Google 官方介紹](https://blog.google/innovation-and-ai/products/using-large-scale-brain-simulations-for/) [原始論文](https://research.google/pubs/building-high-level-features-using-large-scale-unsupervised-learning/)

這一步對 Dean 並不是突然改行。神經網路要從小型研究走向實用，首先需要解決的仍是他熟悉的問題：資料如何切分、計算如何分配、模型如何跨機器更新，以及硬體故障時訓練如何繼續。

AI 看似是新的研究領域，對他而言卻仍然是一個系統規模問題。

![第三次跨越：AI 的突破](/assets/images/jeff-dean-slide-07.png)

---

## TensorFlow：把 Google 的 AI 工具交給全世界

DistBelief 證明大規模分散式訓練可行，但它主要是 Google 內部系統。接下來的 TensorFlow，則把機器學習運算表示成資料流圖，並能把計算配置到 CPU、GPU、TPU 與多台機器上。[OSDI 2016 論文](https://www.usenix.org/conference/osdi16/technical-sessions/presentation/abadi)

Dean 是初代 TensorFlow 的主要設計者與實作者之一，也主張將它開源。Google 在 2015 年釋出 TensorFlow，使研究者與開發者可以在嵌入式裝置、手機、個人電腦、伺服器及大型機器學習叢集上使用同一套框架。[Google Research 個人頁](https://research.google/people/jeff/) [OSDI 2016 論文](https://www.usenix.org/conference/osdi16/technical-sessions/presentation/abadi)

TensorFlow 的意義，與 MapReduce 有一種對稱關係。MapReduce 把分散式資料處理的複雜度藏在介面後面；TensorFlow 則把跨硬體、跨機器執行神經網路的複雜度交給框架。

兩者相隔十多年，解決的其實是同一類問題：如何讓更多人使用原本只有大型研究與工程團隊才有能力駕馭的運算規模。

![對稱的偉大：MapReduce vs TensorFlow](/assets/images/jeff-dean-slide-08.png)

---

## 不只 TensorFlow：word2vec、翻譯、蒸餾、稀疏模型與 TPU

Dean 的 AI 貢獻並不限於系統軟體。他是兩篇 word2vec 論文的共同作者，參與把 Google Translate 轉向神經機器翻譯，也與 Geoffrey Hinton、Oriol Vinyals 共同提出知識蒸餾方法，讓大型神經網路的能力可以轉移到更小、更適合部署的模型。[Google Research 個人頁](https://research.google/people/jeff/) [知識蒸餾論文](https://arxiv.org/abs/1503.02531)

他也參與 2017 年的稀疏混合專家模型研究。這類架構讓模型擁有大量參數，但每次只啟動部分專家，後來成為擴展大型模型的重要技術路線之一。這裡同樣可以看到 Dean 對效率與規模的長期關注。[原始論文](https://arxiv.org/abs/1701.06538)

TPU 的起源是一個著名的餐巾紙計算。2013 年，Dean 估算：如果每個 Google 使用者每天用語音辨識三分鐘，現有伺服器數量就得翻倍。這個數字讓他們決定押注專用硬體——針對低精度稠密線性代數優化的定制晶片。Google 在 ISCA 2017 發表的論文顯示，第一代 TPU 的效能功耗比（perf/watt）比當時的 CPU 高出約 80 倍、比 GPU 高出約 30 倍。後續世代則同時支援大型模型的訓練與推論，成為 Google 在 AI 算力上最核心的護城河之一。[Y Combinator](https://x.com/ycombinator/status/2082938685071491219) [ISCA 2017 論文](https://arxiv.org/abs/1704.04760) [Google Research 個人頁](https://research.google/people/jeff/)

![軟硬兼施：AI 推論成本](/assets/images/jeff-dean-slide-09.png)

除了這些大型系統，Dean 與 Ghemawat 還共同設計了 Protocol Buffers——Google 內部最基礎的資料序列化格式，後來開源後成為跨語言、跨平台資料交換的業界標準。2011 年初，兩人又一起寫了 LevelDB，一個類似 Bigtable tablet stack 的輕量鍵值儲存引擎，後來被 Chrome 的 IndexedDB 等場景廣泛採用。[Google Research 個人頁](https://research.google/people/jeff/) [LevelDB GitHub](https://github.com/google/leveldb)

他還是 Pathways 的早期設計者與實作者之一。Pathways 的目標是支援大型、多模態與稀疏模型，其系統後來支撐 PaLM 等研究。Dean 也參與 PaLM，並成為 Gemini 計畫的共同領導者之一。在硬體與 AI 的交叉點上，他還參與了 AlphaChip 相關工作——用機器學習來設計晶片本身，讓 AI 不只跑在晶片上，還能幫忙設計晶片。[Google Research 個人頁](https://research.google/people/jeff/)

需要再釐清另一個常見錯誤：Jeff Dean 並不是 2017 年〈Attention Is All You Need〉的共同作者。Transformer 論文來自 Google 團隊，但八位論文作者中沒有 Dean。把 Google AI 的所有突破都歸到一位領導者名下，反而會抹去真正作者的貢獻。[NeurIPS 原始論文](https://proceedings.neurips.cc/paper/7181-attention-is-all-you-need)

![尊重真實的工程史：不將所有突破歸功於一人](/assets/images/jeff-dean-slide-10.png)

---

## 從工程師成為 Google 的研究領導者

2018 年，John Giannandrea 卸下 Google AI 負責人職務後，Dean 接掌 Google 的 AI 部門。這使他的角色從設計系統與推動研究，進一步擴大到決定大型研究組織的方向。[TechCrunch](https://techcrunch.com/2018/04/02/google-ai-and-search-chief-john-giannandrea-steps-down/)

2023 年，Google 將 Google Brain 與 DeepMind 合併為 Google DeepMind。Dean 被任命為 Google 首席科學家，同時服務 Google Research 與 Google DeepMind，協助設定 AI 研究方向並領導關鍵技術專案。[Google 2023 年官方公告](https://blog.google/innovation-and-ai/technology/ai/april-ai-update/)

他在 Google Research 的自述中，列出的研究與產品影響橫跨 Search、Ads、YouTube、Gmail、Maps、Photos、Translate、Android、Cloud、Pixel、Waymo，以及醫療、氣候、機器人、基因體與晶片設計等領域。[Google Research 個人頁](https://research.google/people/jeff/)

2009 年，Dean 當選美國國家工程院院士；他也是 ACM、AAAS Fellow，並在 2016 年當選美國藝術與科學院院士。[Google Research 個人頁](https://research.google/people/jeff/)

---

## Jeff Dean 傳說：工程師世界的創世神話

可能還有人不熟悉 Jeff Dean 在程式設計師世界裡的地位。這麼說吧：很多技術大佬擁有履歷，Jeff Dean 擁有一整套以自己為主角的創世神話和迷因傳播。

2007 年愚人節前後，Google 工程師 Kenton Varda 等人創建了「Jeff Dean Facts」——一系列仿 Chuck Norris Facts 格式的工程師笑話，迅速在矽谷內部和開發者社群瘋傳。[Slate](https://slate.com/technology/2013/01/jeff-dean-facts-how-a-google-legend-became-the-chuck-norris-of-the-internet.html) 這些「事實」至今仍在流傳，而且隨著 Dean 的成就越來越誇張，笑話反而越來越像預言。

以下是精選的 Jeff Dean Facts（括號內為白話翻譯）：

1. 編譯器不會警告 Jeff Dean。Jeff Dean 會警告編譯器。

2. Jeff Dean 提交程式碼前也會編譯和執行一遍。主要是為了檢查編譯器和 CPU 有沒有 Bug。

3. Jeff Dean 曾經寫過一個 O(n²) 演算法。那是用來解決旅行商問題的。（旅行商問題是 NP-hard，O(n²) 等於直接破解了計算理論的千禧年難題。）

4. Jeff Dean 對常數時間複雜度仍不滿意，於是發明了世界上第一個 O(1/n) 演算法。（資料越多，跑得越快。）

5. Jeff Dean 的 PIN 碼，是 π 的最後四位。

6. Jeff Dean 的鍵盤上沒有 Ctrl 鍵。因為 Jeff Dean 永遠擁有控制權。

7. Jeff Dean 的鍵盤其實只有兩個鍵：0 和 1。

8. Jeff Dean 寫程式時，會先把二進位機器碼寫完，再補一份原始碼作為文件。

9. 當 Jeff Dean 打開效能分析器時，迴圈會因為恐懼而自行展開。

10. gcc -O4 的工作原理，是把你的程式碼發給 Jeff Dean，讓他重寫一遍。

11. Jeff Dean 不會產生段錯誤。記憶體會主動重新排列，把程式碼和資料放到正確的位置。

12. Jeff Dean 可以用正規表達式解析 HTML。而且是正確地解析。（這在理論上不可能，因為 HTML 不是正規語言。）

13. Jeff Dean 曾經把一個 bit 移得太用力，結果它跑到了另一台電腦上。

14. Jeff Dean 不使用 ECC 記憶體。他會提前預測宇宙射線，並利用它們提高效能。

15. Jeff Dean 發出一個乙太網路封包時，從來不會發生碰撞。其他封包會主動退回各自網卡的緩衝區。

16. Jeff Dean 的程式碼跑得太快，組合語言程式需要連續執行三個 HALT 才能把它停下來。

17. Jeff Dean 不呼叫 sleep()。他呼叫 wait()。（sleep 是被動等待，wait 是主動決定等待——Jeff Dean 不被動。）

18. Jeff Dean 睡不著時，會用 MapReduce 數羊。

19. 2002 年 Google 索引伺服器當機時，Jeff Dean 曾經人工回答了兩個小時的搜尋請求。評測結果顯示，搜尋品質提高了 5 個百分點。

20. Jeff Dean 發明 MapReduce，是為了給粉絲來信排序。

21. Jeff Dean 發明 Bigtable，是因為他的履歷已經無法存進其他資料庫。

22. Jeff Dean 的履歷只記錄他還沒完成的事情。這樣比較短。

23. Google Search 只是 Jeff Dean 為自己真正的專案寫的一個大型單元測試。

24. Google 基本上是 Jeff Dean 的業餘專案。

25. Jeff Dean 曾經參加圖靈測試，但失敗了。因為他在一秒鐘內準確說出了第 203 個費波那契數。（太強反而被判定不是人類。）

26. Jeff Dean 可以在三步之內贏下四子棋。

27. 貝爾發明電話後，發現自己有一個 Jeff Dean 的未接來電。

28. 上帝說：「要有光。」Jeff Dean 當時負責程式碼審查。

29. 真空中的光速原本只有每小時 35 英里。後來 Jeff Dean 花了一個週末優化物理學。

30. Jeff Dean 的程式出現未定義行為時，一隻獨角獸會騎著彩虹出現，給所有人發免費冰淇淋。

31. Jeff Dean 不寫 Bug。他只會實現一些你暫時無法理解的功能。

32. Jeff Dean 為了讓程式碼審查者相信程式碼出自人類之手，有時不得不故意降低效能。

33. Jeff Dean 不存在。他其實是 Jeff Dean 編寫的一個高級人工智慧。

34. 有人問 Jeff Dean，這些傳言究竟是不是真的。他回答：「111111。」對方還在猜這是什麼意思，他補充道：「每一個 bit 都是真的。」（111111 是二進位，6 個 bit 全為 1 = 全部為真。）

2026 年 8 月 Dean 宣布離開 Google 後，工程師社群的即時反應是一波新的 meme，其中流傳最廣的一句是：「Google 終於把他開源了。」[IBTimes](https://www.ibtimes.com/jeff-dean-leaves-google-discovery-loop) 如果你理解這個梗——把一個人「開源」意味著他不再被一家公司獨佔，而是成為整個社群可以使用的資源——你就理解了 Jeff Dean 在這個產業裡的地位。

---

## 傳奇背後，也有不能跳過的管理爭議

Jeff Dean 在工程師社群裡有近乎神話的地位，但完整的職業生涯不能只寫技術成就。

2020 年，Google Ethical AI 團隊共同負責人 Timnit Gebru 在一篇探討大型語言模型風險的論文審查爭議後離開 Google。Gebru 認為自己遭到解僱；Google 則表示，公司接受了她提出的有條件辭職。當時領導 Google AI 的 Dean 在內部信中說，該論文未達公司的發表標準。事件引發對研究自由、企業審查，以及 Google 對黑人女性研究者待遇的廣泛質疑。[The Washington Post](https://www.washingtonpost.com/technology/2020/12/03/timnit-gebru-google-fired/) [TIME](https://time.com/6132399/timnit-gebru-ai-google/)

Google 執行長 Sundar Pichai 隨後為事件造成的傷害道歉並啟動調查。2021 年 2 月，Dean 在後續備忘錄承認，公司本來可以、也應該用更敏感的方式處理，Google 同時宣布修改研究與員工離職的相關流程。[Axios：Pichai 備忘錄](https://www.axios.com/2020/12/09/sundar-pichai-memo-timnit-gebru-exit) [Axios：後續調查](https://www.axios.com/2021/02/19/google-tweaks-diversity-research-policies-following-inquiry)

這件事不會消除 Dean 對分散式系統與 AI 的貢獻；技術成就也不能讓管理責任消失。一位傑出的工程師成為大型組織領導者後，面對的不再只有系統是否正確，還包括誰能發言、研究能否挑戰公司的利益，以及權力如何被使用。

![規模的代價：當管理複雜度超越系統複雜度](/assets/images/jeff-dean-slide-11.png)

---

## 下一個要接管的複雜度：研究本身的實驗迴路

回顧 Dean 的整條職涯線索，可以看到一個反覆出現的動作：找到系統裡工程師被迫手動處理的瓶頸，然後把那層複雜度收進基礎設施。MapReduce 接管了分散式容錯，TensorFlow 接管了跨硬體運算配置，TPU 接管了推論成本。

2026 年 7 月 25 日，Dean 在 Y Combinator Startup School 的演講裡，把同一個邏輯推到了研究過程本身。[OfficeChai](https://officechai.com/ai/how-jeff-dean-at-hinted-at-running-loops-of-experiments-two-weeks-before-launching-discovery-loop/)

他先描述了科學方法的基本結構：

> "There's this sort of the foundation of the scientific method of you propose an experiment, you implement what you need to run the experiment, and you evaluate the experiment, and then you get results from that."

然後是關鍵的一步——把這個迴路自動化，讓延遲降到極低，讓實驗數量從幾個變成大量平行：

> "I think there are more and more problems that are now possible to implement where that whole loop of running not just a few experiments, but running many, many experiments, because you're able to automate that loop and make the latency of that loop extremely low, is going to be really, really important."

他認為這不只適用於 ML 研究，也適用於晶片設計、科學與工程等可量化目標的領域。[OfficeChai](https://officechai.com/ai/how-jeff-dean-at-hinted-at-running-loops-of-experiments-two-weeks-before-launching-discovery-loop/)

在離開 Google 前的最後一次深度訪談中，Dean 更進一步預測 ML 系統將實現「全自動的問題分解與自動化實驗迴路」——把問題拆成子問題、自動執行實驗、整合結果、產出更強的系統。他也坦承自己低估了一件事：模型處理日益複雜任務的能力，成長速度遠超他的預期。[36kr](https://eu.36kr.com/en/p/3927354387544195)

對熟悉他生涯的人來說，這個方向並不意外。Dean 做的始終是同一件事：讓原本需要專家手動操作的環節，變成機器可以反覆執行的迴路。差別只在於，過去他自動化的是資料處理、模型訓練、硬體部署——現在他想自動化的，是產生這些技術的研究過程本身。

![下一個要接管的複雜度：科學實驗迴路本身](/assets/images/jeff-dean-slide-12.png)

---

## 27 年的句點

Jeff Dean 在 1999 年加入一間仍在解決搜尋索引問題的年輕公司，離開時，Google 已經是橫跨搜尋、雲端、晶片與前沿 AI 的全球企業。這 27 年裡，他的角色也從親手修復搜尋系統的工程師，變成同時影響 Google Research 與 Google DeepMind 的首席科學家。[Google Research 個人頁](https://research.google/people/jeff/) [Google 官方公告](https://blog.google/company-news/inside-google/message-ceo/next-chapter-ai-momentum/)

![讓複雜度成為他人的地板](/assets/images/jeff-dean-slide-01.png)

若只用一句話總結他的生涯，我不會說他「發明了 Google」，也不會把所有 Google 技術都算在他名下。

更準確的說法是：

**Jeff Dean 一再把 Google 即將承受不了的規模，變成下一代工程師可以直接站上去的地板。**

搜尋成長得太快，他參與重建搜尋與叢集基礎設施；資料大到一台機器處理不了，他與 Ghemawat 做出 MapReduce；資料分散到全球，他參與 Bigtable 與 Spanner；神經網路大到傳統工具無法訓練，他參與打造 DistBelief、TensorFlow、TPU 與 Pathways。[Google Research 個人頁](https://research.google/people/jeff/)

這些系統未必每天出現在一般使用者眼前，卻決定了搜尋能不能更新、資料能不能被處理、模型能不能被訓練，以及一項研究能不能從論文走進產品。

這才是 Jeff Dean 的故事：不是站在舞台中央創造一個爆紅產品，而是在舞台底下，把整座舞台蓋到足以承受下一個時代。

![27 年的句點：在舞台底下，蓋出承受下個時代的地板](/assets/images/jeff-dean-slide-13.png)

---

## 資料核查說明

本文資料核查截止時間為 **2026 年 8 月 7 日（台北時間）**。生涯與技術項目優先採用 Google Research、Google 官方公告、原始論文、USENIX 與 ACM 資料；人物合作經過參考《紐約客》專訪；管理爭議則交叉參考當事雙方說法與多家媒體報導。作者的歸納與評價均與可驗證事實分開表述。
