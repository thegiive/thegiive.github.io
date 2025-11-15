---
layout: post
title: "ATPM : A real production Vibe Coding process"
date: 2025-09-16 21:41:01 +0000
permalink: /atpm-a-real-production-vibe-coding-process/
image: /assets/images/-------2025-09-17-------4.31.54-1.png
description: "章節..."
---


![ATPM : A real production Vibe Coding process](/assets/images/-------2025-09-17-------4.31.54-1.png)

章節

  1. [ATPM 介紹](https://ai-coding.wiselychen.com/atpm-a-real-production-vibe-coding-process/)
  2. [PRD 的重要性](https://ai-coding.wiselychen.com/atpm-prdde-zhong-yao-xing/)
  3. [AI 時代, 對PM的加速](https://ai-coding.wiselychen.com/atpm-ai-dui-pm-de-jia-su/)
  4. [Dev 的演進](https://ai-coding.wiselychen.com/atpm-kai-fa-zhe-dev-de-shui-bian-cong-gong-du-sheng-ma-nong-dao-ai-zhi-hui-jia/)
  5. [QA](https://ai-coding.wiselychen.com/atpm-qa-ru-he-yan-shou-ai-coding-de-cheng-shi/)
  6. Supervisor 撰寫中
  7. 結語撰寫中

## 前言

在AI技術蓬勃發展的今天，我們的軟體開發世界正經歷著一場前所未有的「中年危機」。Vibe Coding 橫空問世的當下，我這種老屁股工程師一邊害怕被淘汰的同時，一邊又看著 AI Coding 又被很多人吐槽無法真正拿來做真正的工作。

很幸運的是，我們團隊在六月開發一套新流程 ATPM : Assessment , Testing , Program , Management ，並且用這套流程開發一套帳務系統並且成功上線。在這個過程中，我們幾乎把所有 Vibe Coding 所有遇到的問題

  1. 幻覺
  2. 亂講話
  3. 測試困難
  4. 框架一致性

等問題都踩過一遍了。而且我們做的還是做不能接受幻覺的帳務系統！還真的上線了。

### 我可以肯定這就是 Vibe Coding 的解決方式

接下來，我會用多篇文章 + 幾個 youtube video 來解釋。在那之前，我想先講一下緣起。

## 一切的起頭

我在2023 年開始，就大量利用 GenAI 加上非傳統科系的 intern 學生組成的數據團隊來工作，這段時間以來，我們都是以 AI 當作助手的方式來作業，基本上跑軟體開發的流程依舊還是跟原本一樣，走 Kaban ，只是用 ChatGPT 幫助這些 intern 做他們做不到的事情 (寫程式 ) 。這時候，軟體開發感覺就是單點的強化，但是不是流程的改造。中間的每個節點都是原本的做法

當然，公司的大家都知道我用的 7成工讀生，所以當我們團隊遇到一些系統技術問題時，大家其實是比較寬容的。另外，我也大量使用 SaaS 服務來彌補 intern 之間知識的不足，而專注做真正的 business 

![](/assets/images/image.png)

一直到 2025年的年初，隨著職務的調換，我們團隊從 intern 7成 轉成發展到正職 7成的正式團隊(也有數人從 intern 轉正），另外又來了兩個 intern 。隨著公司給我的 resource 增加，不管我選擇的是工讀生轉正還是直接 hire 外面的 engineer ，公司都會要求我做「真正的系統」，給出更高標準的技術要求

我那時很多心中的小劇場，我不認為我之前的 intern + AI 方法論是錯的，但是我心裡也知道，照原本的方法做不長久。但是要我把難得的 head count 去找 ”外面工程師" 換掉 這些跟我一段時間的 "幾位 Intern 弟弟妹妹們" 時，我也覺得對他們不太合理。

原因有幾個

  1. 在AI時代， 我的判斷是 Domain Knowledge 勝過技術，而這些 intern 跟我很久了，對於 Domain Knowledge 遠勝外面的人
  2. 在跟他們合作的時間 , 充分的感受到年輕人的 AI 含量遠勝過我們這些老屁股 , 每個人原生的擁抱AI 
  3. 越 Sr 的工程師用容易用原本的框架去想事情，但是 AI 時代新的框架還沒有誕生，我需要重塑軟體開發的人

## 賭注

在我選擇將所有 headcount 全部換成優秀的 intern 轉正時，HR用一副 "看到鬼" 的眼神看我，他說這對他來說很省事，也不用經過老闆的審批，但是他說沒有主管會在能 Hire Sr Eng 的時候 intern 轉正的 Jr 的

我跟他說

> 在 AI 時代，跟有現有思維框架的 Sr 我 比起來，這些弟弟妹妹才是真正的 Sr AI Engineer

但是他們需要一些指引跟創意來協助。

我注意到之前他們無法做大系統問題在於 "技術經驗" 跟 "協作能力" ，技術經驗 AI 是有充分能力可以彌補的，再加上我一個大叔當作最後一道屏障，肯定沒問題。但是多人協作經驗的確是麻煩，大家真的都剛畢業或是還在大四，這可能是真正的困難點。而且現在挑戰的不只是人跟人協作，還有人加 AI 協作

## 主要問題在於需要一套新的 AI Coding 流程

很幸運的是，當你注意到問題的時候，老天爺就給你解法了。我在2025年五月講生成式 AI時，前一個講者 Happy Lee 大大就直接給我講解法了，我們需要的是一套圍繞 PRD 為主的流程

![](/assets/images/image-1.png)

看完這套流程，我當下就跟 Happy 以及他底下的人要投影片跟聯繫方式，再來就是要求團隊開始研究這個流程，並且拿這套帳務系統需求當作 POC，

也因為如此，其實我們一開始在做這個帳務系統時，反而用傳統的流程跑，而非新的 PRD 為主的 開發。當一切入開發期(紅色的 bar) ，我們就陷入經驗不足的混亂，在下面 Week 19 ~ Week 22, 一直在泥沼內。當下其實我已經發現大家雖然都很 Jr , 但是已經有一定開發的範式了。（所以人的經驗牆是很容易出現的）

![](/assets/images/image-2.png)

我印象中在 week 22 的那個週三，因為很多原因(當天因為其他原因被老闆念)，我少數會議中出現很激動地對大家說「現在就是拋棄你們所熟悉的一切的時候，我們沒有任何退路，直接擁抱 AI Coding 跟新的流程」

然後，效率就很明顯就上去了。

## 流程不見得很厲害，主要原因是大家理解沒有退路，要擁抱這個流程

3個月的時候，我們經歷大量的迭代跟討論，甚至在 7/1 還去 Happy 91APP辦公室跟他們團隊交流。最後成功在七月底上線這個系統部分業務 !!!!!! 

這套做法已經跟 Happy 的做法有一些差距了。在七月的時候我們的辦公室的風景突然變成這樣

![](/assets/images/image-3.png)

從右到左，四台電腦三個人

  1. 第一台 air 是 Claude Code 做 tech lead , 負責看整個流程
  2. 第二台 air 是做 QA , PM 拿 PRD 叫 Cursor 去驗某個業務的程式
  3. 在跑到一半的時候，同一個 PM 拿訪談紀錄去 ChatGPT 生成新的 PRD 
  4. 做左邊的 air 是 Engineer 用 cursor 寫 code 

我那時候突然理解到，這個流程跟做法其實就跟現在大家在討論的 Spec Driven Development (AWS Kiro) 或是 Github Spec Kit 很類似，大家都在解決類似的問題。

也因為如此，我決定跟大家分享這套 ATPM 

## ATPM 

![](/assets/images/-------2025-09-17-------4.31.54.png)

他是一套以PRD為中心，用 AI 去強化 PM , Dev, QA 效率跟正確性的流程，裡面成功利用這個流程加速 40% 的時間，並且通過很嚴苛的 QA 驗證（畢竟是算上億元錢的系統）。

他是以 Assessment評估 , Testing 測試, Program 開發, Management (Supervisor 去監管) 為首字，並且高度強調迭代反饋回去 PRD 的流程跟框架。

他的主要幾個重點

  1. PRD為核心
  2. 每個節點都是 人跟 AI 協作, 所以PRD必須人跟AI都看得懂
  3. 所有的 Domain Knowledge 都是記錄在 PRD , 所以每個環節都不需要特定某個人, 可以自由輪調
  4. 特別重視 PRD 的反饋 , 我們之前經驗 , 一版 PRD 到結案，至少都大改 6 ~7 次，不是因為 PM 訪談問題，而是實務場景就是那麼複雜
  5. 花了很大時間跟人力在 QA , 原因不是AI做不到，而是為了避免AI幻覺，我們用大量的人力 QA Tradeoff 

接下來我會用幾篇文章跟一兩個 youtube video 來講述相關細節

[ ![Multi-Agent 協作模式：當 AI 學會「會診」這件事](/assets/images/ChatGPT-Image-2025---11---15----------04_36_04.png) Multi-Agent 協作模式：當 AI 學會「會診」這件事 我上週回老家看了久違的第四台「緯來日本台」，看一個日本節目「恐怖家庭醫學」，裡面講到一個年長者「最近常常心悸、手抖、睡不好」。因為是心臟的因素，所以患者直接找心臟科檢查後，拿到一疊厚厚的報告——結果心臟科醫生看完報告說：「你的心臟結構完全正常，心電圖也沒問題，可能是壓力太大，回去多休息就好。」患者心想：「可是我真的有心悸啊！難道是我自己想太多？」於是患者找了神經科說可能是自律神經失調，拿了藥物減壓，但症狀完全沒改善。 弄了很久一直兜兜轉轉。最後一個經驗豐富家醫科醫生，告知患者「這可能是甲狀腺的問題，要去看內科」才發現這是甲亢的症狀，調整好藥物很快就好了。很多時候人體很多時候是一個連動的生態系統，有些問題的表象跟真正的Root Cause是兩回事，所以患者很容易找錯醫生弄錯科目。 但如果是在好的健檢中心，做法就完全不一樣了。健康檢查會根據你的全方位給予檢查——最後針對你的完整報告進行討論，這時候甲亢的 Root Cause 很快就會被最後的把關者抓出來 " 問題根本不在心臟，而在甲狀腺 " 。這就是「多人協作的力量」。 AI Agent 的世界也是一樣的道理。 By Wisely Chen 15 Nov 2025 ](/multi-agent-xie-zuo-mo-shi-dang-ai-xue-hui-hui-zhen-zhe-jian-shi/) [ ![那天我在產業園區分享：AI 能不能做起來，其實看人](/assets/images/S__88875042.jpg) 那天我在產業園區分享：AI 能不能做起來，其實看人 今天我在新北產業園區，在我們公司的 AI 轉型的活動 在各位傳統產業的前輩講述我之前在傳統產業做 AI 轉型的經驗 我認為「 AI 要在傳產落地，先解決的永遠不是模型，而是人、流程與文化。」 我把這幾年的實戰經驗濃縮成一套能在傳統產業中真正起作用的框架： 現況分析：先理解現場，再談技術 我們創建了一個以 公司各部門的老前輩 + Intern 為主的種子團隊，深入一線流程、取得高層支持，建立真正的共識。 AI 不是空降，而是跟現場一起改。 快速勝利：小範圍試點，讓大家看到成效 選一個可控的場域，把 AI +種子團隊拉進真實流程。 像我用 AI + RPA + OCR + 快速掃描器 = 一個可持續可落地，並且有效益成果 這樣的「小勝利」，是推動組織願意往下走的關鍵。 全面升級：從工具導入到組織轉型 把建置的種子團隊散步到全公司各個部門 可以用很快的速度去 scale 全面開花 By Wisely Chen 13 Nov 2025 ](/na-tian-wo-zai-chan-ye-yuan-qu-fen-xiang-ai-neng-bu-neng-zuo-qi-lai-qi-shi-kan-ren/) [ ![AI 信任崩塌的真正原因：勞資零和賽局的再現](/assets/images/ChatGPT-Image-2025---11---10----------09_24_03.png) AI 信任崩塌的真正原因：勞資零和賽局的再現 根據《Harvard Business Review》近期發表的〈Workers Don’t Trust AI. Here’s How Companies Can Change That〉，美國基層員工對公司提供的 AI 工具信任度在短短數月內暴跌：對生成式 AI 的信任下降 31%，對自主決策型 AI 更下滑 89%。近半數員工反而更信任非官方AI 工具。另外無獨有偶MIT 的研究《The GenAI Divide: State of AI in Business 2025》更進一步揭示了這種現象，並命名為 Shadow AI：員工在公司外私下使用未授權的 AI 來完成工作。研究指出，約有 By Wisely Chen 10 Nov 2025 ](/ai-xin-ren-beng-ta-de-zhen-zheng-yuan-yin-lao-zi-ling-he-sai-ju-de-zai-xian/) [ ![\[Agent part 3\] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵](/assets/images/ChatGPT-Image-2025---11---8----------08_01_49.png) [Agent part 3] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵 大家都知道我用 AI 來 enable 很多intern 來當作很多正職的事情，當然他們雖然都很年輕跟熱情，但是我管理團隊時發現一個規律： 當我派給幾個 Senior 的同事 ，我通常只需要 weekly 跟他開會，給他幾個任務，一週後檢查一次就好。他可以獨立工作，中間遇到問題會自己判斷、調整，如果有大問題他們會舉手跟我講，不容易走偏。 當我要安排工作給我的 intern ，跟 Senior 最大的不同就是， Junior 我通常會每半天或是每過一天就會跟他聊一下提醒一下可能要注意什么事情。因為他很容易遇到了某些複雜任務時，他就可能在某一步卡住，又沒有舉手，基於錯誤理解繼續做下去，最後整個方向偏了，也浪費了他整天的時間。 這是Sr 跟 Jr 經驗的差別，獨立作戰的能力 AI Agent 也是如此 現在考驗 AI Agent 最大的地方，不是他的智商，主要著重點是它的連續工作穩定性。如果人類需要介入的越少，就代表它可以自主完成工作， By Wisely Chen 08 Nov 2025 ](/agent-part-3-interleaved-thinking-cheng-xian-de-wen-ding-xing-shi-xian-zai-agentluo-di-de-zhong-yao-guan-jian/)