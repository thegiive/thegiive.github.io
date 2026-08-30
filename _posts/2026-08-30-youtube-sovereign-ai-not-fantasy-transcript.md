---
layout: post
title: "\"YouTube 逐字稿：主權 AI 不再是幻想——開源追平 SOTA、雲端偷降智、老黃買下 Hugging Face\""
date: 2026-08-30 20:00:00 +0800
permalink: /youtube-sovereign-ai-not-fantasy-transcript/
tags: [主權 AI, sovereign AI, 開源模型, open source, Kimi K3, DeepSeek V4 Flash, Qwen3.8-27B, post-training, Hugging Face, NVIDIA, Harness, FDE, 地端部署, on-premise]
categories: [AI 產業分析]
image: /assets/images/youtube-sovereign-ai-not-fantasy-thumbnail.jpg
description: "\"**作者：** Wisely Chen **日期：** 2026 年 8 月 **系列：** AI Coding 實戰觀察 — YouTube 逐字稿 **關鍵字：** 主權 AI, sovereign AI, 開源模型, Kimi K3, DeepSeek V4 Flash, Qwen3.8-27B, post-training, Hugging Face, NVIDIA, Harness, 地端部署\""
author: Wisely Chen
---

**作者：** Wisely Chen
**日期：** 2026 年 8 月
**系列：** AI Coding 實戰觀察 — YouTube 逐字稿
**關鍵字：** 主權 AI, sovereign AI, 開源模型, Kimi K3, DeepSeek V4 Flash, Qwen3.8-27B, post-training, Hugging Face, NVIDIA, Harness, 地端部署

---

## 這集在講什麼

主權 AI 剛被提出來的時候只是一個幻想——開源模型跟雲端的能力差距太大，不管怎麼做都做不贏雲端。但今年情況變了。這集用 4 分鐘講三個訊號：**開源模型追平 SOTA**（Kimi K3、DeepSeek V4 Flash、Qwen3.8-27B 都有前沿八九成的能力）、**雲端 AI 不定期偷降智而且成本越來越高**、**NVIDIA 用 129 億美元買下 Hugging Face 押注開源生態**。最後談把 AI 當員工養的思路，以及接下來半年該關注的三件事：地端硬體價格、開源生態動態、Harness。

---

**長度：** 約 4 分鐘

{% include youtube.html id="7ntVtewQwd4" %}

### 時間戳

- 0:00 主權 AI 是什麼？為什麼過去只是幻想
- 0:44 訊號一：開源模型追平 SOTA（Kimi K3、DeepSeek V4 Flash、Qwen3.8-27B）
- 1:04 訊號二：雲端 AI 不定期降智、成本越來越高
- 1:26 有資源的廠商開始養 3-10 人 team 做 post-training
- 1:59 把 AI 當員工養：從新人到公司裡不可取代的老師傅
- 2:36 老黃買下 Hugging Face：養大開源生態，最後還是買 NVIDIA 的卡
- 3:18 接下來半年該關注的三件事：地端價格、開源動態、Harness
- 4:11 結語

---

## 完整逐字稿

### 開場：主權 AI 是什麼、為什麼過去只是幻想

Hello 大家好，今天來講主權 AI。主權 AI 是什麼呢？

基本上剛出的時候其實就有討論過一輪了。大家都在想說，雖然 AI 很棒，但是我不希望我的一些相關企業資料或是一些工作流，能夠給雲端的大廠這邊來進行使用，怕我們公司的工作外洩出去。

可是那個時候雲端的 AI 跟那時候的開源模型，有一個巨大的能力上的差別。所以就變得說不管你怎麼做，都做不贏雲端。所以那時候主權 AI 就變成只是一個幻想。

但在今年的時候，這個幻想慢慢的就是變得有可能了。那主要是幾個。

### 訊號一：開源模型追平 SOTA

第一個點是我們越來越發現到，開源模型已經很接近所謂的 SOTA。不管在跑分上，或是真的就是實際上做事情上面——Kimi K3、DeepSeek V4 Flash，或是千問的 Qwen3.8-27B，他們都有很類似、大概八九成的能力。

### 訊號二：雲端 AI 不定期降智、成本越來越高

那第二個其實主要是整個雲端 AI 這邊。第一個是隨著它相關算力的不夠，所以就是他會不定期、然後也沒公告的，就是對於模型進行降智。可能今天他表現得很好，但明天他突然之間就變得很笨。那第二個，他的成本其實越來越高了。那這個大家就是都心有戚戚焉。

### 有資源的廠商：養一個 team 做 post-training

那再來就是有資源的廠商的話，他可能會 setup 一個 team，大概就是 3 到 10 人左右的 Data Scientist，然後能夠對這公司的一些專有的數據來進行一些後訓練。

那這樣子的話，他就會變成一個最適合你這個場景下面的一個 AI 的 model。就算他可能就是隨著更新換代他比較舊了，但是因為他有這些就是專業的 data 然後來進行的後訓練，所以他就是一個最適合的 model。

### 把 AI 當員工養：從新人到不可取代的老師傅

那這個其實就跟人一樣。一開始的時候，這個就是主權 AI 進來的話，他就是一個新人，他只能靠他原本就是剛出廠的能力。

但是隨著我不斷給他相關的 post-training，我們找到適合的 Harness，還有給他一個就是完整的 eval 的機制，他就越來越學習。這個員工，所以他進來一年、兩年、三年，到最後到 10 年，他可能變成這公司的就是完全無法取代的一個角色。

那他的能力雖然不一定是最好的，但是他最熟悉這個業務，那他依舊是一個不可取代的。

### 老黃買下 Hugging Face：養大開源生態

那所以 NVIDIA 因為這個主權 AI，買了 Hugging Face 這個號稱開源界的 GitHub。他做這件事情其實基本上就是試著把這個開源的 ecosystem 把它養起來。

那個主權 AI 如果是越來越大，大家要做生意、買更多的卡，到最後你可能還是會買那個 NVIDIA 卡為主。而且你要做那個 post-training 訓練的話，你更是需要 NVIDIA 的相關的卡，才能夠做比較快速的。

那不管怎麼樣子，他用一個很小的就是資源，去照顧或是壯大這個主權 AI 的社群，他對他未來就是相關的營收或是一些 margin，都是很有幫助的。

### 接下來半年該關注的三件事

所以這個是我覺得接下來的這半年或這一年，相關主權 AI 我們可能要特別在意的。

第一個是找一個良好的地端相關的價格，因為他最近漲得有點誇張。原因是關注開源 AI 的相關的發展，像現在基本上是每週都有一個新的就是模型的出來，那這個 ecosystem 變得越來越熱鬧了。

那第三個可能大家比較少來注意到，就是說針對 Harness 的重要性可能要開始關注。那 Harness 這邊當然就是，就是 AI 所謂的御三家，或者是 OpenAI，或是 Gemini。他會讓整個戰場以及裡面的玩家就是極大的擴展。我們所說的其實 Harness，其實軟體廠商還有一些 FDE 廠商，我覺得這是一個比較良性的一個發展。

### 結語

這就是我的想法，謝謝大家。

---

## 延伸閱讀

- [老黃買 Hugging Face 在幹嘛？預判主權 AI，鎖死分銷管道](/nvidia-hugging-face-acquisition-open-source-chokepoint/)
- [Kimi K3 登場：2.8T 參數、十天後開源，但真正的訊號是它悄悄退出了中國價格戰](/kimi-k3-open-frontier-kda-attnres-pricing/)
- [Qwen3.8-27B 斬殺線：別只看那 $0.01，真正該看的是背後的趨勢](/qwen-3-8-27b-blade-killline-frontier-cost/)
- [Local-first Agent Stack 系列總覽](/local-first-agent-stack/)
- [Local-first 模型需要 local-first harness](/local-first-model-needs-local-first-harness/)
