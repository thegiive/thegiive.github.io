---
layout: post
title: "影片逐字稿｜Loop Engineering 是真趨勢還是 Buzzword？該不該做的三個判斷"
date: 2026-06-14 09:00:00 +0800
permalink: /loop-engineering-buzzword-video-transcript/
image: /assets/images/loop-engineering-buzzword-cover.jpg
description: "這是我從廣州南站搭高鐵去香港的路上，隨手錄的一段對 Loop Engineering 的看法。一句話定義：把 Plan、Execution、Verify 之後原本由人決定下一步的那一步，也交給 Agent。但它沒那麼簡單——要做之前先過三關：有沒有可量化的 metric、成本控不控得住、Stop Condition 設好了沒。Loop Engineering 是真趨勢，還是繼 Vibe Coding、Harness Engineering 之後又一個 buzzword？"
---

![Loop Engineering 是真趨勢還是 Buzzword？該不該做的三個判斷](/assets/images/loop-engineering-buzzword-cover.jpg)

<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;margin:30px 0;border-radius:8px;">
  <iframe src="https://www.youtube.com/embed/EJh6hC9qyn8" style="position:absolute;top:0;left:0;width:100%;height:100%;" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

> 影片連結：[https://youtu.be/EJh6hC9qyn8](https://youtu.be/EJh6hC9qyn8)
> 這篇是影片的逐字稿，文字有稍微整理過。想看把概念跟邊界講完整的版本，請看：[Loop Engineering：不再 Prompt Agent，改設計 Loop](/loop-engineering-from-prompt-to-loop-paradigm-shift/)。想看實作怎麼落地，請看：[Loop Engineering 實作指南：五個組件 + 一個記憶體](/loop-engineering-five-plus-one-implementation-guide/)。

---

## 開場：在去香港的路上

嗨，大家好。我今天在 travel 的路上，從廣州南站要到香港去，所以就在這邊跟大家聊一下。

因為最近常看到一個很新的 buzzword 叫做 Loop Engineering，所以在這邊跟大家講一下什麼叫做 Loop Engineering。

## 我第一個想到的是咒術迴戰那個梗

我看到這個東西的時候，第一個想到的是咒術迴戰一個很有名的梗：已經沒時間搞 Prompt Engineering、Context Engineering 或是 Harness Engineering 了，現在趕赴戰場、打頭陣的是 Loop Engineering。

這就是我剛看到的感覺。AI 時代一堆 buzzword 跑來跑去，但反過來看，這也代表 AI 的大佬其實也在努力 catch up、在探尋一些新的方式。

這就是為什麼我們現在有那麼多有的沒有的新詞彙。因為現在 AI，不管是使用方式還是 AI Coding，其實都還在一個很早期的階段，遠不到一個很穩定的階段。所以才會冒出這麼多詞彙、這麼多範式。

## Loop Engineering 到底是什麼

Loop Engineering 我覺得它代表的是一件事情。

我們現在 Agent 的一個 Task，原本是 Plan、Execution、Verify，然後最後由人來決定下一步。Loop Engineering 想做的，就是把「人做最後決定下一步」這件事情，也變成由 Agent 來做。

所以整個流程就變成：一個 Agent 做 Planning，另一個 Agent 做 Execution，再由一個 Verify Agent 來做 Verify，然後最後原本人來決定下一步的那一步，換成另外一個 Agent——根據一個比較好的目標標準，去調整它的 Prompt 或 Context，然後讓它執行下一個 Round。

這就是所謂的 Loop Engineering。我們希望做到的，是一個可以自我進化、自我回歸的東西。

聽起來是一個很棒的 task，但要做這件事情其實非常有挑戰。

## 為什麼現在會紅：之前做的 Harness 都不是白費的

第一個問題是，為什麼這個東西會紅起來？

原因是現在的 Agent 跟大型模型越來越成熟、越來越進步。但最重要的一點是：雖然我們之前做了很多 Harness 這些東西，但這些東西都不是白費的。把它們做成一組很好的 Lego 積木、排列組合之後，我們就有機會做出這種 Loop。

舉例來說，現在 Memory 系統越做越大，所以我們每一次的 Iteration 都能夠把它記下來。Harness Engineering 越做越好，所以我們在做每一個 Agent Task 的時候，都有機會確保它不會逾矩、不會越界，也能做好資安的部分——每個 Round 之後，它不會隨便把自己的東西放到網路上，或做一些出格的事情。

只有把這些經驗累積、best practice 累積做完，我們才有機會做 Loop Engineering。

## 做之前先過三關

那在做 Loop Engineering 之前，我們基本上要怎麼準備？

### 判斷一：你的 Goal 要能量化

第一個，你必須在現在的 Agent Task 裡面，原本最後由人來做評估的那一步，有一個量化的指標。

因為原本是人來決定下一步，現在變成 Agent 決定下一步，可是 Agent 其實不太清楚你的 Goal。所以你的 Goal 必須很明確、很容易量化。

我個人認為，像 Machine Learning task、或是一些 Coding task，比較容易驗證「這一 Round 做得好還是不好、要不要調整方向」。只有當你有這種 criteria，你才比較適合做 Loop Engineering。

反過來，如果你是一些發散性的 task，我個人認為不太適合。因為人必須去理解這個東西到底是不是你要的；像 brainstorming、創意類的東西，雖然我們有 Agent 幫忙發想，但最後還是要人來拍板。這種 task 就可能不太適合做 Loop Engineering。

### 判斷二：成本一定要控管

第二個，你必須做很好的成本控管。

大家也知道，你原本可能花了十塊美金——如果你一個 skill 寫得不好——但你放一個晚上跑 Loop Engineering，可能就一千倍，變成一萬塊美金的花費。然後就 just 因為一個 mistake。所以你必須把成本的 best practice 控管得非常好。

當然另一個做法其實很簡單：你就丟到地端去跑。這樣這個 task 基本上比較容易控制，因為你只要付電費就好了。

### 判斷三：Stop Condition 要做好

第三個，你的 Stop Condition 要做好。

你必須告訴 Agent，在什麼樣的情況下要 stop；或是你直接在 Harness 裡面用一段確定性的 code，把整個 Loop 停下來。

不然的話，很有可能明明已經做好了，但因為 Stop Condition 沒設好，它就繼續做，然後越走越偏。

## 坦白說：它是方向之一，但不是全部

這就是我目前對 Loop Engineering 的理解。

老實說，我認為它會是未來的其中一個方式，但它絕對不會是一個完整的方式。我覺得我們現在 AI Agent 的這些範式都還在非常早期，所以可能需要更多的探索。

但我個人認為 Loop Engineering 的確蠻適合 Coding、Machine Learning，或是一些有良好評測標準的 task，是一個進化的方向。

## 我自己接下來想試的：小模型 + Loop + Memory

如果是我自己的話，最近其實已經累積了不少 use case，我接下來想用我的 Qwen local model 來做 Loop Engineering。

因為我蠻期待一件事：一個小模型，如果在 Loop Engineering 上再套一個良好的 Memory 機制，它應該有機會 become something big，甚至在某些場景下贏過一些線上的模型。

所以我會再試試看這件事情能不能發生。那就期待我之後的 feedback 吧。謝謝大家。
