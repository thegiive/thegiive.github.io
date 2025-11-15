---
layout: post
title: "[AI Ops] 用 Agent(Claude Code) 做 Linux 系統管理有沒有搞頭？香得很！"
date: 2025-10-24 00:34:56 +0000
permalink: /ai-ops-yong-agent-claude-code-zuo-linux-xi-tong-guan-li-you-mei-you-gao-tou-xiang-de-hen/
image: /assets/images/ChatGPT-Image-2025---10---24----------08_31_52.png
description: "今天突然發現用 Claude Code 做 Linux 系統管理超香的。不只可以幫你寫 code，還順便幫你考古系統程式，挖出系統裡不為人知的秘密，最棒的是能讓你找到之前同事寫好的 code 提早下班，享受當老闆的樂趣。..."
---




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
