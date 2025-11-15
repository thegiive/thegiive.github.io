---
layout: post
title: "[ATPM] 來看看矽谷公司怎麼用 AI 來把關 Vibe Coding 的成果"
date: 2025-10-12 22:15:32 +0000
permalink: /atpm-lai-kan-kan-xi-gu-gong-si-zen-mo-yong-ai-lai-ba-guan-vibe-coding-de-cheng-guo/
image: /assets/images/Generated-Image-October-13--2025---5_33AM.png
description: "現在有了 AI ，Coding 的東西可以又快又完整，但是我們怎麼知道 AI 做的Code 裡面會不會有更多的地雷(多收費，寫出有資安議題, 實現很糟糕) 呢？..."
---




現在有了 AI ，Coding 的東西可以又快又完整，但是我們怎麼知道 AI 做的Code 裡面會不會有更多的地雷(多收費，寫出有資安議題, 實現很糟糕) 呢？

### 矽谷怎麼搞

來看看矽谷公司現在怎麼搞的？看看 [Reddit 這一篇](https://www.reddit.com/r/vibecoding/comments/1nnl19h/how_a_senior_engineer_at_a_140m_startup_actually/?ref=ai-coding.wiselychen.com)

![](/assets/images/image-18.png)

這是一個 最近剛 raise 140M 的 startup 裡面 Sr 工程師在reddit 上發表他的做法

  1. 一開始他跟 Claude Code 去討論規格，確定沒有太多問題就叫 AI 寫 Code 了，重點是一開始不要糾結規格完美程度，70% 差不多就做了。
  2. Coding 中間一個重點， cleanup Code ，他會realtime 切到 Cursor 去看 AI 怎麼 Coding ，因為 UI 介面他比較好清晰知道那裡新增了啥 ，而且他不喜歡全部產生 code difference 再看，他喜歡一開始就去 catch AI 的幻覺，避免問題
  3. 再來就是請 AI Code Review ，他說用 AI 做 Code Review 跟人一起 Code Review 雖然看起來重複，其實**「AI 可以幫忙 catch 不同的的 issue」** ，他們最後用的是 coderabbit ，一開始 commit 前先 local 快速 check ，等到 PR 時候，再用一個 github app 來做 detail analysis 
  4. Testing pipeline 完全是由人來控制的，所有的東西都會在 staging 環境做詳細的自動化/人工測試， AI 在裡面會幫忙寫 automation test script ，但是 deploy 與否的決策主導權完全在人

![](/assets/images/image-20.png)

###   
人跟機器做 Code Review 的差別

裡面提到人跟機器 「Code Review 看的東西不太一樣」，我非常的有同感。

一般來說，AI做 Code Review ，在檢查 Code Syntax check , 快速發現常見問題(SQL Injection, XSS, Memory Leak ...etc），以及Best Practice / Anti pattern 。非常的有效率。

另外就是 AI 在知識的廣度遠超人類，就算是工程師，也很難全知全能，就算都是你這個領域，很多 code 的 lib 你也不一定 update-to-date 。這時候 AI 是一個很好的補齊。

人類看的東西，第一個是判斷「過度工程」vs「適度抽象」的平衡，第二個是理解技術債的緣由，知道能判斷「為什麼要這樣寫」，而不只是「寫了什麼」。很多時候，這些 code 看起來很爛，是因為你不理解團隊的在當時的業務限制，技術架構決策的前因後果。

舉一個技術債例子，我在艾立做數位回單時。ETL 一開始用很多 App Script ，中間慢慢改成 make.com + Cloud Run ，後來漸漸變成 GCP Cloud Scheduler + Cloud Run 。  
\- 為何一開始 App Script 打到底，因為我工讀生們那時候剛是剛來工讀生，啥都不懂，一開始導入太多東西會搞死人  
\- make.com : 後來工讀生有些人已經穩定下來幾個月，已經有基本知識了，可以導入第二個 SaaS 套件，才慢慢走向 make.com   
\- 最後怎麼又把 make.com 拋棄掉，因為跟 make.com 談便宜年約談不太下來，加上集團要整合資源砍掉一些 SaaS ，所以就整合進去 GCP   
。  
看看每個技術選型都有很多 context 需要 align , AI 很難完全 align tech lead 的決策

![](/assets/images/Generated-Image-October-13--2025---6_31AM-1.png)

再來就是對業務的理解通常比 AI 好，但是很多時候其實不一定為真 XD ，還是要寫好 PRD Spec ，讓 AI 跟 人都 on the same page 才比較好。

最後一個是 AI 通常對雨後春筍般的 雲服務/SaaS 不是完全理解，所以很多時候在最重要雲服務/SaaS 的 Cost 成本優化上很難做到人的程度，不過這個議題本來人來做也很難的。

### 我的 Comment 

整體來說，雖然這篇不是在講方法論的，但是卻講的很清楚。該有的卡點都有 ，而且是人類跟 AI 穿插做審核。整個觀念很棒 , 而且很 practical 

Code Review 前期，強調產生 Code 的過程當下就用UI做「人力的即時檢核」，不能夠一次做一大包 code review 。這裡感覺跟工程師屆的 Ship Small , Ship fast 很像。

AI Code Review 的部分很有趣，用 [CodeRabbit ](https://www.coderabbit.ai/?ref=ai-coding.wiselychen.com)來做，我用的大多數是之前時代的 code review 工具，主要針對一些 security，還有 syntax check，我還真的沒用過新時代的 AI Code Review SaaS Service 。看來要看看一下了，但是我的問題是我感覺 Claude Code / Codex 應該很容易做到類似的功能，這個 SaaS 網站的差異化在哪呢？

![](/assets/images/image-21.png)

最後 QA 的決策環節，還是人力為主，你要對自己的 Code 負責而不是丟給 AI 。

整個觀念很棒 , 而且很 practical 。應該是真的實戰派出來寫的。而且不像 SDD 學院派一樣強調太多冗長的環節。

最後，他說這套流程大概加速的 40% 的時間，怎麼跟我的 [ATPM 最後測出來的感覺一模一樣](https://ai-coding.wiselychen.com/atpm-a-real-production-vibe-coding-process/)....XD

![](/assets/images/image-19-1.png)

明天跟團隊討論這個流程一下看了那麼多 SDD , ATPM 終於可以升級了趕快來線上實測新流程
