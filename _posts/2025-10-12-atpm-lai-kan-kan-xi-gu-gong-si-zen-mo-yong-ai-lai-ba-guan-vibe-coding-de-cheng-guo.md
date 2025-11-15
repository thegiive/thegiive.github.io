---
layout: post
title: "[ATPM] 來看看矽谷公司怎麼用 AI 來把關 Vibe Coding 的成果"
date: 2025-10-12 22:15:32 +0000
permalink: /atpm-lai-kan-kan-xi-gu-gong-si-zen-mo-yong-ai-lai-ba-guan-vibe-coding-de-cheng-guo/
image: /assets/images/Generated-Image-October-13--2025---5_33AM.png
description: "現在有了 AI ，Coding 的東西可以又快又完整，但是我們怎麼知道 AI 做的Code 裡面會不會有更多的地雷(多收費，寫出有資安議題, 實現很糟糕) 呢？..."
---


![\[ATPM\] 來看看矽谷公司怎麼用 AI 來把關 Vibe Coding 的成果](/assets/images/Generated-Image-October-13--2025---5_33AM.png)

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

[ ![Multi-Agent 協作模式：當 AI 學會「會診」這件事](/assets/images/ChatGPT-Image-2025---11---15----------04_36_04.png) Multi-Agent 協作模式：當 AI 學會「會診」這件事 我上週回老家看了久違的第四台「緯來日本台」，看一個日本節目「恐怖家庭醫學」，裡面講到一個年長者「最近常常心悸、手抖、睡不好」。因為是心臟的因素，所以患者直接找心臟科檢查後，拿到一疊厚厚的報告——結果心臟科醫生看完報告說：「你的心臟結構完全正常，心電圖也沒問題，可能是壓力太大，回去多休息就好。」患者心想：「可是我真的有心悸啊！難道是我自己想太多？」於是患者找了神經科說可能是自律神經失調，拿了藥物減壓，但症狀完全沒改善。 弄了很久一直兜兜轉轉。最後一個經驗豐富家醫科醫生，告知患者「這可能是甲狀腺的問題，要去看內科」才發現這是甲亢的症狀，調整好藥物很快就好了。很多時候人體很多時候是一個連動的生態系統，有些問題的表象跟真正的Root Cause是兩回事，所以患者很容易找錯醫生弄錯科目。 但如果是在好的健檢中心，做法就完全不一樣了。健康檢查會根據你的全方位給予檢查——最後針對你的完整報告進行討論，這時候甲亢的 Root Cause 很快就會被最後的把關者抓出來 " 問題根本不在心臟，而在甲狀腺 " 。這就是「多人協作的力量」。 AI Agent 的世界也是一樣的道理。 By Wisely Chen 15 Nov 2025 ](/multi-agent-xie-zuo-mo-shi-dang-ai-xue-hui-hui-zhen-zhe-jian-shi/) [ ![那天我在產業園區分享：AI 能不能做起來，其實看人](/assets/images/S__88875042.jpg) 那天我在產業園區分享：AI 能不能做起來，其實看人 今天我在新北產業園區，在我們公司的 AI 轉型的活動 在各位傳統產業的前輩講述我之前在傳統產業做 AI 轉型的經驗 我認為「 AI 要在傳產落地，先解決的永遠不是模型，而是人、流程與文化。」 我把這幾年的實戰經驗濃縮成一套能在傳統產業中真正起作用的框架： 現況分析：先理解現場，再談技術 我們創建了一個以 公司各部門的老前輩 + Intern 為主的種子團隊，深入一線流程、取得高層支持，建立真正的共識。 AI 不是空降，而是跟現場一起改。 快速勝利：小範圍試點，讓大家看到成效 選一個可控的場域，把 AI +種子團隊拉進真實流程。 像我用 AI + RPA + OCR + 快速掃描器 = 一個可持續可落地，並且有效益成果 這樣的「小勝利」，是推動組織願意往下走的關鍵。 全面升級：從工具導入到組織轉型 把建置的種子團隊散步到全公司各個部門 可以用很快的速度去 scale 全面開花 By Wisely Chen 13 Nov 2025 ](/na-tian-wo-zai-chan-ye-yuan-qu-fen-xiang-ai-neng-bu-neng-zuo-qi-lai-qi-shi-kan-ren/) [ ![AI 信任崩塌的真正原因：勞資零和賽局的再現](/assets/images/ChatGPT-Image-2025---11---10----------09_24_03.png) AI 信任崩塌的真正原因：勞資零和賽局的再現 根據《Harvard Business Review》近期發表的〈Workers Don’t Trust AI. Here’s How Companies Can Change That〉，美國基層員工對公司提供的 AI 工具信任度在短短數月內暴跌：對生成式 AI 的信任下降 31%，對自主決策型 AI 更下滑 89%。近半數員工反而更信任非官方AI 工具。另外無獨有偶MIT 的研究《The GenAI Divide: State of AI in Business 2025》更進一步揭示了這種現象，並命名為 Shadow AI：員工在公司外私下使用未授權的 AI 來完成工作。研究指出，約有 By Wisely Chen 10 Nov 2025 ](/ai-xin-ren-beng-ta-de-zhen-zheng-yuan-yin-lao-zi-ling-he-sai-ju-de-zai-xian/) [ ![\[Agent part 3\] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵](/assets/images/ChatGPT-Image-2025---11---8----------08_01_49.png) [Agent part 3] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵 大家都知道我用 AI 來 enable 很多intern 來當作很多正職的事情，當然他們雖然都很年輕跟熱情，但是我管理團隊時發現一個規律： 當我派給幾個 Senior 的同事 ，我通常只需要 weekly 跟他開會，給他幾個任務，一週後檢查一次就好。他可以獨立工作，中間遇到問題會自己判斷、調整，如果有大問題他們會舉手跟我講，不容易走偏。 當我要安排工作給我的 intern ，跟 Senior 最大的不同就是， Junior 我通常會每半天或是每過一天就會跟他聊一下提醒一下可能要注意什么事情。因為他很容易遇到了某些複雜任務時，他就可能在某一步卡住，又沒有舉手，基於錯誤理解繼續做下去，最後整個方向偏了，也浪費了他整天的時間。 這是Sr 跟 Jr 經驗的差別，獨立作戰的能力 AI Agent 也是如此 現在考驗 AI Agent 最大的地方，不是他的智商，主要著重點是它的連續工作穩定性。如果人類需要介入的越少，就代表它可以自主完成工作， By Wisely Chen 08 Nov 2025 ](/agent-part-3-interleaved-thinking-cheng-xian-de-wen-ding-xing-shi-xian-zai-agentluo-di-de-zhong-yao-guan-jian/)