---
layout: post
title: "[AI Ops] 用 Agent(Claude Code) 做 Linux 系統管理有沒有搞頭？香得很！"
date: 2025-10-24 00:34:56 +0000
permalink: /ai-ops-yong-agent-claude-code-zuo-linux-xi-tong-guan-li-you-mei-you-gao-tou-xiang-de-hen/
image: /assets/images/ChatGPT-Image-2025---10---24----------08_31_52.png
description: "今天突然發現用 Claude Code 做 Linux 系統管理超香的。不只可以幫你寫 code，還順便幫你考古系統程式，挖出系統裡不為人知的秘密，最棒的是能讓你找到之前同事寫好的 code 提早下班，享受當老闆的樂趣。..."
---

[agent](https://ai-coding.wiselychen.com/tag/agent/)

# [AI Ops] 用 Agent(Claude Code) 做 Linux 系統管理有沒有搞頭？香得很！

[ ![Wisely Chen](/assets/images/6672228-F20250919----02-----------SN------10945w-1.jpg) ](/author/wisely/)

#### [Wisely Chen](/author/wisely/)

24 Oct 2025 — 5 min read

![\[AI Ops\] 用 Agent\(Claude Code\) 做 Linux 系統管理有沒有搞頭？香得很！](/assets/images/ChatGPT-Image-2025---10---24----------08_31_52.png)

今天突然發現用 Claude Code 做 Linux 系統管理超香的。不只可以幫你寫 code，還順便幫你考古系統程式，挖出系統裡不為人知的秘密，最棒的是能讓你找到之前同事寫好的 code 提早下班，享受當老闆的樂趣。  
  
話說今天某個客戶系統出問題了，大家忙到炸掉。為了安撫客戶，我就跟客戶說

> 「我來寫 monitor script 吧」

既然牛都吹了，來都來了，就來寫吧，反正也不是我寫 XD。我對 Claude Code 很有信心，因為 Linux 系統管理本質就是 command line，而 Claude Code 生來就是為 command line 而生，而且很專精！

### 目標

我的目標就是在一台 Linux machine 寫 monitor script，確認某些檔案在特定的時間必須要產出，並且產出檔名要合乎規格。不過就要報 alert 。說實在話，我沒有任何這台系統資訊，我只是先溝通了 IT 拿到 ssh 就衝了。

關於我自己在 linux 上，其實不算白板，我有一點點 linux admin 經驗但是不多。我一直會寫 bash/perl script ，而且我很自豪我可以用 vim 寫一個 project 面不改色。總之，我算熟悉，不算精通 IT Admin。

### 讓 Claude Code 幫你解決問題

但是我很清楚 Agent (尤其是 Claude Code ）在這個場景，應該是他的絕對舒適區。所以我的步驟是不給資訊，讓 Claude Code 盲猜以下的 Case 

  1. 請 Claude Code ssh vm 
  2. 請他先看一下系統的summary 
  3. 找出非系統的 deamon 
  4. 解釋一下 deamon 的意義

結果真的還蠻驚喜的。

FYI : 當然有下提示詞, 禁止做任何修改性的動作

### Case : 看一下系統 Summary 

這根本就是一堆基本操作，對每個 IT OPS 都會的 step , 相信 Claude Code 沒問題吧 

> Prompt : 幫我看一下系統跑哪些 application 

雖然有心理準備，還是我驚嘆 CC的精細度，連crontab jon 說明都有 ，代表他有進去看 code 

![](/assets/images/image-41-1.png)

### Case : 找出非系統的 daemon

因為擔心裡面有太多 system daemon ，混淆視聽，我請他直接 filter 掉，只看業務

> Prompt : 幫我過濾到常見的 app 跟 GCP 預設的管理 app 

裡面最神的就是 Claude Code 怎麼知道這台伺服器就是轉運站的? Claude Code 去看裡面每個 code ? 

![](/assets/images/image-42-1.png)

### Case : 解釋一下 daemon 的意義

通常我們在系統上，遇到老機器，如果老 IT 不在的話，常會遇到一些daemon 很難理解沒有人記得的 application 。這時候常常很難解釋。

但是今天我們發現到

> AI 會去翻程式，告訴你古老程式的細節, 簡直是天選考古人。

當然我在猜要看得懂應該是要明文的 code 像是 bash or python 這種啦

![](/assets/images/image-43-1-1.png)

### 彩蛋 Case : 幫我翻到老程式，Claude Code 幫我提早下班

我本來上這台VM是要寫 monitor script ，沒想到 Claude Code 看著看著，居然發現上面有一個兩年前的老 script ，裡面邏輯就是 exactly 我要做的事情

![](/assets/images/image-45-1-1.png)

只可惜之前的 IT 不知道誰忘了他，也已經沒有跑了。不過沒關係， Claude Code 從泥土中找到這個程式，重新擦亮他。我可以提早下班了。

![](/assets/images/ChatGPT-Image-2025---10---24----------09_40_08-1.png)喜歡這張圖

### Final Case : 享受當老闆的樂趣

最後 , Claude Code給我最好的情緒價值就是，我可以從牛馬轉成老闆，問出一句經典名言

> Prompt : 今天機器一切順利嗎? 

![](/assets/images/image-44-1.png)

### 從牛馬變老闆的快樂

這次用 Claude Code 做 Linux 系統管理，最大的感受就是**角色轉換** 。以前遇到老舊系統，要嘛找老員工問（如果還在的話），要嘛自己土法煉鋼一個指令一個指令試，通常要花一段時間才能搞清楚狀況，更別說寫出能用的 monitor script。

但這次不一樣。我只是給了 SSH 帳號，剩下的 Claude Code 全包了：自動探索系統、分析 daemon、解釋古老 script、甚至找出兩年前被遺忘的程式。30 分鐘的活 3 分鐘搞定，我從「又要加班的牛馬」變成可以悠哉問出「今天機器一切順利嗎？」的老闆。

最後一句話： 下次遇到老舊 Linux 系統，除了翻文檔找人問，直接問 Claude Code。它會帶你考古、幫你寫 script，還順便讓你早點下班！

[ ![Multi-Agent 協作模式：當 AI 學會「會診」這件事](/assets/images/ChatGPT-Image-2025---11---15----------04_36_04.png) Multi-Agent 協作模式：當 AI 學會「會診」這件事 我上週回老家看了久違的第四台「緯來日本台」，看一個日本節目「恐怖家庭醫學」，裡面講到一個年長者「最近常常心悸、手抖、睡不好」。因為是心臟的因素，所以患者直接找心臟科檢查後，拿到一疊厚厚的報告——結果心臟科醫生看完報告說：「你的心臟結構完全正常，心電圖也沒問題，可能是壓力太大，回去多休息就好。」患者心想：「可是我真的有心悸啊！難道是我自己想太多？」於是患者找了神經科說可能是自律神經失調，拿了藥物減壓，但症狀完全沒改善。 弄了很久一直兜兜轉轉。最後一個經驗豐富家醫科醫生，告知患者「這可能是甲狀腺的問題，要去看內科」才發現這是甲亢的症狀，調整好藥物很快就好了。很多時候人體很多時候是一個連動的生態系統，有些問題的表象跟真正的Root Cause是兩回事，所以患者很容易找錯醫生弄錯科目。 但如果是在好的健檢中心，做法就完全不一樣了。健康檢查會根據你的全方位給予檢查——最後針對你的完整報告進行討論，這時候甲亢的 Root Cause 很快就會被最後的把關者抓出來 " 問題根本不在心臟，而在甲狀腺 " 。這就是「多人協作的力量」。 AI Agent 的世界也是一樣的道理。 By Wisely Chen 15 Nov 2025 ](/multi-agent-xie-zuo-mo-shi-dang-ai-xue-hui-hui-zhen-zhe-jian-shi/) [ ![那天我在產業園區分享：AI 能不能做起來，其實看人](/assets/images/S__88875042.jpg) 那天我在產業園區分享：AI 能不能做起來，其實看人 今天我在新北產業園區，在我們公司的 AI 轉型的活動 在各位傳統產業的前輩講述我之前在傳統產業做 AI 轉型的經驗 我認為「 AI 要在傳產落地，先解決的永遠不是模型，而是人、流程與文化。」 我把這幾年的實戰經驗濃縮成一套能在傳統產業中真正起作用的框架： 現況分析：先理解現場，再談技術 我們創建了一個以 公司各部門的老前輩 + Intern 為主的種子團隊，深入一線流程、取得高層支持，建立真正的共識。 AI 不是空降，而是跟現場一起改。 快速勝利：小範圍試點，讓大家看到成效 選一個可控的場域，把 AI +種子團隊拉進真實流程。 像我用 AI + RPA + OCR + 快速掃描器 = 一個可持續可落地，並且有效益成果 這樣的「小勝利」，是推動組織願意往下走的關鍵。 全面升級：從工具導入到組織轉型 把建置的種子團隊散步到全公司各個部門 可以用很快的速度去 scale 全面開花 By Wisely Chen 13 Nov 2025 ](/na-tian-wo-zai-chan-ye-yuan-qu-fen-xiang-ai-neng-bu-neng-zuo-qi-lai-qi-shi-kan-ren/) [ ![AI 信任崩塌的真正原因：勞資零和賽局的再現](/assets/images/ChatGPT-Image-2025---11---10----------09_24_03.png) AI 信任崩塌的真正原因：勞資零和賽局的再現 根據《Harvard Business Review》近期發表的〈Workers Don’t Trust AI. Here’s How Companies Can Change That〉，美國基層員工對公司提供的 AI 工具信任度在短短數月內暴跌：對生成式 AI 的信任下降 31%，對自主決策型 AI 更下滑 89%。近半數員工反而更信任非官方AI 工具。另外無獨有偶MIT 的研究《The GenAI Divide: State of AI in Business 2025》更進一步揭示了這種現象，並命名為 Shadow AI：員工在公司外私下使用未授權的 AI 來完成工作。研究指出，約有 By Wisely Chen 10 Nov 2025 ](/ai-xin-ren-beng-ta-de-zhen-zheng-yuan-yin-lao-zi-ling-he-sai-ju-de-zai-xian/) [ ![\[Agent part 3\] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵](/assets/images/ChatGPT-Image-2025---11---8----------08_01_49.png) [Agent part 3] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵 大家都知道我用 AI 來 enable 很多intern 來當作很多正職的事情，當然他們雖然都很年輕跟熱情，但是我管理團隊時發現一個規律： 當我派給幾個 Senior 的同事 ，我通常只需要 weekly 跟他開會，給他幾個任務，一週後檢查一次就好。他可以獨立工作，中間遇到問題會自己判斷、調整，如果有大問題他們會舉手跟我講，不容易走偏。 當我要安排工作給我的 intern ，跟 Senior 最大的不同就是， Junior 我通常會每半天或是每過一天就會跟他聊一下提醒一下可能要注意什么事情。因為他很容易遇到了某些複雜任務時，他就可能在某一步卡住，又沒有舉手，基於錯誤理解繼續做下去，最後整個方向偏了，也浪費了他整天的時間。 這是Sr 跟 Jr 經驗的差別，獨立作戰的能力 AI Agent 也是如此 現在考驗 AI Agent 最大的地方，不是他的智商，主要著重點是它的連續工作穩定性。如果人類需要介入的越少，就代表它可以自主完成工作， By Wisely Chen 08 Nov 2025 ](/agent-part-3-interleaved-thinking-cheng-xian-de-wen-ding-xing-shi-xian-zai-agentluo-di-de-zhong-yao-guan-jian/)