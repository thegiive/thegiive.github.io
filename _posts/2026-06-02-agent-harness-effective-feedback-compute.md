---
layout: post
title: "Agent 不是越忙越聰明：Effective Feedback Compute 與 Harness 的 Scaling Law"
date: 2026-06-02 06:00:00 +0800
permalink: /agent-harness-effective-feedback-compute/
image: /assets/images/agent-harness-efc-logo.png
image_alt: "Scaling Laws for Agent Harnesses via Effective Feedback Compute 論文首頁"
description: "一篇很適合做 Agent Harness 的人看的論文：Agent 不是靠多跑 token、多調工具、多循環幾輪就會變強，真正重要的是這些互動有沒有變成有效反饋。論文提出 Effective Feedback Compute（EFC），只認可有信息量、可靠、不重複、且真的被拿去改決策的反饋。等預算下只提升反饋品質，成功率從 27% 跳到 90%。也聊了要不要因此導入 mem0 這類 memory 架構。"
---

最近讀到一篇很適合做 Agent Harness 的人看的論文：[Scaling Laws for Agent Harnesses via Effective Feedback Compute](https://arxiv.org/abs/2605.29682)（Xuanliang Zhang 等人）。它戳破了一個我自己也踩過的迷思：**Agent 不是靠多跑 token、多調工具、多循環幾輪就一定會變強。**

我先講結論，然後我們再看數據。

## 先講一個反直覺的觀點

現在很多人做 Agent Harness 的直覺都是「加」：

- context 不夠長？拉長一點。
- 工具不夠多？再掛幾個 MCP。
- 一次做不對？多 retry 幾輪。
- 不知道發生什麼？把 log 開到最詳細。

這些看起來都很努力，也很容易讓人覺得「我的 Harness 越來越強了」。但這篇論文說的是：**這些 raw compute 的堆疊，跟最後任務成功率的關係其實很弱。**

弱到什麼程度？論文直接量化給你看：用 raw tokens 跟 tool calls 去解釋任務成功率，R² 只有 **0.33–0.42**。換句話說，你燒了多少 token、調了幾次工具，大概只能解釋三到四成的結果。剩下六成你解釋不了。

那剩下那六成是什麼？

## 不是只有我這樣想，身邊做 Agent 的朋友反饋也一樣

我把這個觀點丟給幾個也在做 Agent 落地的朋友，得到的反饋幾乎一模一樣——大家最早都是這套「加法思維」。

有個朋友的內部 ops agent，跑得不穩，他的第一反應就是「資訊不夠」——於是把每一步的 log 開到 verbose、把 retry 從 1 次加到 3 次、又掛了兩個查詢工具進去。結果呢？任務是有變穩一點點，但 token 成本跟跑完一輪的時間直接翻倍，而且很多時候它只是把同一個錯誤的判斷「更詳細地」重複了三遍。

他那時候以為問題是「反饋不夠多」，後來才想明白，問題是「反饋沒有被用起來」。

那些 log，Agent 根本沒拿來改變下一步決策；加的 retry，每一輪拿到的是幾乎一樣的、重複的訊號；掛的工具，吐回來的東西沒有被結構化整理進它的計畫裡。**它不是更聰明了，它只是更忙了。**

幾個朋友的故事細節不一樣，但卡點完全一致。這種「感覺」幾乎是做 Agent 的人共同的痛點，這篇論文厲害的地方，就是把它變成了可以量化的東西。

## 轉折：Effective Feedback Compute（EFC）

論文提出一個核心概念叫 **Effective Feedback Compute（EFC）**。它的定義很關鍵——不是所有的互動都算數，只有同時滿足四個條件的反饋，才算「有效」：

1. **Informative（有信息量）** — 這個反饋真的帶來新訊息，而不是廢話。
2. **Valid（可靠）** — 這個反饋是對的、可信的，不是雜訊或幻覺。
3. **Non-redundant（不重複）** — 不是把已經知道的東西再講一遍。
4. **Retained for subsequent decisions（被保留並用於後續決策）** — 最重要的一條：這個反饋真的被 Agent 拿去改變了下一步要做什麼。

用我自己的話翻譯：**反饋要夠有料、要可信、不能重複，而且真的要進到「下一步決策」裡，才算數。** 只要少了任何一條，那一輪互動在 EFC 眼中就等於白燒。

朋友那個 ops agent 的 verbose log，卡在第一條跟第四條——資訊量低，而且沒被拿去改決策；加的 retry，卡在第三條——重複。難怪加了等於沒加。

## 數據：把同一個 EFC 換算法套上去，解釋力跳到 0.94

論文用 EFC 重新去解釋任務成功率，數字直接跳了一個量級：

| 衡量方式 | 對任務成功的解釋力 (R²) |
|---|---|
| Raw tokens / tool calls | 0.33 – 0.42 |
| Oracle-EFC | **0.94 – 0.99** |

差距大概就是「你以為你在衡量能力，其實你在衡量忙碌」跟「你真的在衡量能力」的差別。

更狠的是這個對照實驗：**在 raw compute 預算固定不變的前提下**，只去提升反饋的品質——把那些低信息量、重複、沒被用上的反饋換成有效反饋——任務成功率從 **27% 拉到 90%**。

我再強調一次：**成本沒變，只是反饋變有效，成功率三倍跳。**

而且這不只是在乾淨的實驗環境成立。在真實的 benchmark traces 上，正規化後的 EFC（NRS-EFC/D_task）對成功率的解釋力 R² = **0.92**；同樣的 trace，用 raw compute 去解釋，相關性接近 0、甚至是負的。

負的意思是——有時候你燒越多 raw compute，結果反而越差。這跟前面那位朋友「翻倍成本卻只換來一點點改善」的經驗，完全對得上。

## 這對日常做 Agent 的人，到底意味著什麼

我把這篇論文的啟示，整理成幾個我之後做 Harness 會拿來自問的問題：

**一、不要再用 raw compute 當作「能力提升」的指標。**
context 更長、工具更多、log 更詳細、循環更複雜——這些都是「我做了很多」的證據，不是「Agent 變強了」的證據。真正要追蹤的是：這一輪互動，有沒有產生一個被用上的有效反饋。

**二、每加一個工具或一輪 retry，先過 EFC 四條。**
這個反饋有信息量嗎？可靠嗎？跟上一輪重複嗎？最關鍵的——它會不會真的改變 Agent 下一步的決策？如果第四條是「不會」，那這個東西加了就是純粹燒錢。

**三、把反饋塞進 plan / revise / verify 的閉環裡。**
反饋如果沒有被結構化整理、沒有被記住、沒有被複用，它就只是飄過去的 log。要讓它進到「計畫 → 修正 → 驗證」的循環，它才會變成 EFC。這也是為什麼我一直相信 ATPM 裡那條「PRD 當作 Single Source of Truth」——本質上它就是一個強迫反饋被 retain、被複用的機制。每一次需求對焦、每一次 review 的結論，都被寫回那份文件，下一輪不會憑空消失。

這也呼應我之前寫過的〈[Anthropic 官方解密：為什麼 Claude Code 這麼好用？](/anthropic-dual-agent-architecture-claude-code/)〉：雙 Agent 架構強的點從來不是「跑更多」，而是用結構化的方式讓任務邏輯能跨上下文繼承下去。換成 EFC 的語言講，就是它把有效反饋 retain 住了，不會每次「失憶」就歸零。

**四、好的 Harness，不是讓 Agent 多幹活，而是讓它每幹一步都真的學到東西。**
這句話可以直接當成設計原則。你的 Harness 看起來很複雜——工具很多、log 很多、驗證很多——但如果這些東西沒被整理、記住、複用，那它只是更忙，不是更聰明。

## 那要不要因此導入 memory 架構，比如 mem0？

這是我讀完之後第一個冒出來的問題。EFC 四條件裡，最難、也最關鍵的就是第四條「retained for subsequent decisions」，而這正是 [mem0](https://github.com/mem0ai/mem0)、Letta（MemGPT）這類 memory 架構在處理的事——把跨輪、跨 session 的反饋存下來、需要時再檢索回來。所以直覺上答案是「對，該導」。

但我會加一個但書：**memory 架構解決的是四條件裡的「retain」，不是全部四條。**

mem0 幫你把反饋留住、複用，這直接命中第四條。但它不會自動幫你過濾前三條：

- 把雜訊、幻覺的反饋也存進去 → 違反 **valid（可靠）**，而且這種錯誤記憶會被反覆檢索出來，毒性比沒記憶還大。
- 把每一輪幾乎一樣的東西都塞進 memory → 違反 **non-redundant（不重複）**，檢索時還互相稀釋。
- 存的東西本身沒信息量 → 違反 **informative**，只是讓 memory 變肥、檢索變慢。

換句話說，**memory 架構是「retain」這根支柱的好工具，但它必要、不充分。** 你還是得在「寫進 memory 之前」設一道閘門：這個反饋夠有料、可信、不重複嗎？過了再存。否則你只是把「更忙」這件事從單輪放大到跨 session——記憶越長，雜訊越多。

我的建議啦（這段是我的判斷，不是論文結論）：

- 如果你的 Harness 連「跨輪反饋會失憶」都還沒解決 → mem0 這類工具值得導，先把 retain 補起來，收益最大。
- 但導入的同時，一定要配一個「寫入閘門」——用規則、或一個輕量的 LLM 判斷，決定什麼反饋值得進 memory。這一步才是把 mem0 從「更大的 log」變成「真正的 EFC 放大器」的關鍵。
- 別期待 mem0 自己會讓 Agent 變聰明。它讓反饋活得更久，但反饋有沒有效，還是 EFC 那四條說了算。

## 坦白說，這篇論文也有它的保留空間

我不想把它講得像萬靈丹，幾個我自己讀的時候會打問號的地方：

- 論文裡解釋力最高的是 **Oracle-EFC**，那個「Oracle」意思是它用了事後才知道的理想資訊去判定哪些反饋有效。真實系統裡你做不到 Oracle——你很難在當下就準確判斷一個反饋到底有沒有被「用上」。所以 0.94–0.99 是理論上限，不是你明天就能拿到的數字。
- 「retained for subsequent decisions」這條最難工程化。判斷一個反饋有沒有真的改變決策，本身就需要一套機制，這部分論文給的是衡量框架，不是現成的實作。
- 不同任務型態（短任務 vs 長時任務、單 Agent vs 多 Agent）的 EFC 行為應該不一樣，這篇的結論能推廣到多廣，還要再看。

但即使打了這些折扣，它的核心洞察我還是非常買單：**未來 Agent Harness 的優化，重點不會是堆更多工具跟更長 context，而是提高「每一次反饋的利用率」。**

我們做了那麼久 Agent，太容易陷進「我加了好多功能」的滿足感裡。這篇論文剛好提醒：忙碌不是能力，被用上的反饋才是。

---

> 一句話總結：raw compute 衡量的是 Agent 有多忙，EFC 衡量的是 Agent 有多聰明。你的 Harness 該優化的，是後者。

*論文出處：[Scaling Laws for Agent Harnesses via Effective Feedback Compute](https://arxiv.org/abs/2605.29682)（Xuanliang Zhang, Dingzirui Wang, Keyan Xu, Qingfu Zhu, Wanxiang Che）*
