---
layout: post
title: "最近我在前端 Vibe Coding 遇到的問題"
date: 2025-10-03 15:13:06 +0000
permalink: /zui-jin-wo-zai-qian-duan-vibe-coding-yu-dao-de-wen-ti/
image: /assets/images/Generated-Image-October-03--2025---10_51PM.png
description: "我這幾天因為一個重要的案子，決定也來 VIBE Coding 一下，寫寫frontend feature（我從來沒寫過 frontend Vue 的程式）..."
---


![最近我在前端 Vibe Coding 遇到的問題](/assets/images/Generated-Image-October-03--2025---10_51PM.png)

我這幾天因為一個重要的案子，決定也來 VIBE Coding 一下，寫寫frontend feature（我從來沒寫過 frontend Vue 的程式）

我發現到 vibe coding 在「現有網站加ui 功能」似乎遇到巨大的問題。我的場景是有

> 「現有的上線網站，為了加入幾個功能頁，設計師弄了幾頁設計圖，要改上去」

修改規模大概就是100個頁面加入10頁，這種 10% 規模。不是改bug , 但也不是重寫

當我將 Claude code 去讀 Figma設計圖，然後加feature 。居然連 Claude 4.5 Sonnet 都顯得左支右著 , 非常狼狽。

![](/assets/images/Generated-Image-October-03--2025---10_57PM-1.png)

要嘛就是

  1. 頁面改太少，不能根據設計圖復刻
  2. 或是加入UI feature 成功,但是大規模波及到現有ui 
  3. 也可能是 Ui 成功創立，但是api 改壞

這個經驗大家熟知的vibe coding 可以快速兜出一個美觀的 ui，可能有巨大的認知差距

我估計vibe coding 適合

  1. 0-> 100 : 沒有草稿，直接從idea 讓AI 自由發揮的 POC 網站，或是 startup 第一版，沒有前人的包袱
  2. 99% -> 100% : 現有網站，直接改bug 這種 1%的工作

但是今天這種大概 10%修改，好像要了AI 的命。要嘛改不動，要嘛改太多，變成refactor 。這種情況，我當然碰過。我在做[ATPM](https://ai-coding.wiselychen.com/atpm-a-real-production-vibe-coding-process/) 時，在這種情景，撰寫明確的PRD 細節，規格。通常可以解決這個問題。但是一個 已經運行線上的現有網站，哪有可能寫舊有「完整」的 PRD 規格書 , 別騙人了 XD 

![](/assets/images/image.png)

在我今天的情況，我有的就是「新增規格書」，而且還是接近FIGMA 的圖形規格書。我有試過 Claude Code ，請 AI 根據現有網站弄出 PRD , 但是現行 UI 幾乎都是 VUE or React 框架元件，加一堆商用UI lib render 出來的頁面。AI Coding 都是看 Code ，也很難AI 自己腦中render 出來原本長哪樣。然後新規格書又是圖片 ，如果我們要比差距，似乎一定要就有UI render 出來才能比對。

我在猜如果Claude code 操作browser mcp ，去截圖舊網站，然後再請 AI Vision 比較新規格書的圖片，應該比現在ai 看code更有奇效。這個場景 , 就好像很難發揮ai coding 。仔細想想，這種場景跟改bug一樣才是真高頻場景 , 誰會每天寫 POC 呀XD

當然這一切都是我自己前端經驗不夠，別忘了我本週二才開始人生中第一次碰 frontend coding。也算是另外一種 Vibe Coder。

不過今天下午試出一些作法，終於比較好改動了，連假晚點分享

[ ![Multi-Agent 協作模式：當 AI 學會「會診」這件事](/assets/images/ChatGPT-Image-2025---11---15----------04_36_04.png) Multi-Agent 協作模式：當 AI 學會「會診」這件事 我上週回老家看了久違的第四台「緯來日本台」，看一個日本節目「恐怖家庭醫學」，裡面講到一個年長者「最近常常心悸、手抖、睡不好」。因為是心臟的因素，所以患者直接找心臟科檢查後，拿到一疊厚厚的報告——結果心臟科醫生看完報告說：「你的心臟結構完全正常，心電圖也沒問題，可能是壓力太大，回去多休息就好。」患者心想：「可是我真的有心悸啊！難道是我自己想太多？」於是患者找了神經科說可能是自律神經失調，拿了藥物減壓，但症狀完全沒改善。 弄了很久一直兜兜轉轉。最後一個經驗豐富家醫科醫生，告知患者「這可能是甲狀腺的問題，要去看內科」才發現這是甲亢的症狀，調整好藥物很快就好了。很多時候人體很多時候是一個連動的生態系統，有些問題的表象跟真正的Root Cause是兩回事，所以患者很容易找錯醫生弄錯科目。 但如果是在好的健檢中心，做法就完全不一樣了。健康檢查會根據你的全方位給予檢查——最後針對你的完整報告進行討論，這時候甲亢的 Root Cause 很快就會被最後的把關者抓出來 " 問題根本不在心臟，而在甲狀腺 " 。這就是「多人協作的力量」。 AI Agent 的世界也是一樣的道理。 By Wisely Chen 15 Nov 2025 ](/multi-agent-xie-zuo-mo-shi-dang-ai-xue-hui-hui-zhen-zhe-jian-shi/) [ ![那天我在產業園區分享：AI 能不能做起來，其實看人](/assets/images/S__88875042.jpg) 那天我在產業園區分享：AI 能不能做起來，其實看人 今天我在新北產業園區，在我們公司的 AI 轉型的活動 在各位傳統產業的前輩講述我之前在傳統產業做 AI 轉型的經驗 我認為「 AI 要在傳產落地，先解決的永遠不是模型，而是人、流程與文化。」 我把這幾年的實戰經驗濃縮成一套能在傳統產業中真正起作用的框架： 現況分析：先理解現場，再談技術 我們創建了一個以 公司各部門的老前輩 + Intern 為主的種子團隊，深入一線流程、取得高層支持，建立真正的共識。 AI 不是空降，而是跟現場一起改。 快速勝利：小範圍試點，讓大家看到成效 選一個可控的場域，把 AI +種子團隊拉進真實流程。 像我用 AI + RPA + OCR + 快速掃描器 = 一個可持續可落地，並且有效益成果 這樣的「小勝利」，是推動組織願意往下走的關鍵。 全面升級：從工具導入到組織轉型 把建置的種子團隊散步到全公司各個部門 可以用很快的速度去 scale 全面開花 By Wisely Chen 13 Nov 2025 ](/na-tian-wo-zai-chan-ye-yuan-qu-fen-xiang-ai-neng-bu-neng-zuo-qi-lai-qi-shi-kan-ren/) [ ![AI 信任崩塌的真正原因：勞資零和賽局的再現](/assets/images/ChatGPT-Image-2025---11---10----------09_24_03.png) AI 信任崩塌的真正原因：勞資零和賽局的再現 根據《Harvard Business Review》近期發表的〈Workers Don’t Trust AI. Here’s How Companies Can Change That〉，美國基層員工對公司提供的 AI 工具信任度在短短數月內暴跌：對生成式 AI 的信任下降 31%，對自主決策型 AI 更下滑 89%。近半數員工反而更信任非官方AI 工具。另外無獨有偶MIT 的研究《The GenAI Divide: State of AI in Business 2025》更進一步揭示了這種現象，並命名為 Shadow AI：員工在公司外私下使用未授權的 AI 來完成工作。研究指出，約有 By Wisely Chen 10 Nov 2025 ](/ai-xin-ren-beng-ta-de-zhen-zheng-yuan-yin-lao-zi-ling-he-sai-ju-de-zai-xian/) [ ![\[Agent part 3\] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵](/assets/images/ChatGPT-Image-2025---11---8----------08_01_49.png) [Agent part 3] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵 大家都知道我用 AI 來 enable 很多intern 來當作很多正職的事情，當然他們雖然都很年輕跟熱情，但是我管理團隊時發現一個規律： 當我派給幾個 Senior 的同事 ，我通常只需要 weekly 跟他開會，給他幾個任務，一週後檢查一次就好。他可以獨立工作，中間遇到問題會自己判斷、調整，如果有大問題他們會舉手跟我講，不容易走偏。 當我要安排工作給我的 intern ，跟 Senior 最大的不同就是， Junior 我通常會每半天或是每過一天就會跟他聊一下提醒一下可能要注意什么事情。因為他很容易遇到了某些複雜任務時，他就可能在某一步卡住，又沒有舉手，基於錯誤理解繼續做下去，最後整個方向偏了，也浪費了他整天的時間。 這是Sr 跟 Jr 經驗的差別，獨立作戰的能力 AI Agent 也是如此 現在考驗 AI Agent 最大的地方，不是他的智商，主要著重點是它的連續工作穩定性。如果人類需要介入的越少，就代表它可以自主完成工作， By Wisely Chen 08 Nov 2025 ](/agent-part-3-interleaved-thinking-cheng-xian-de-wen-ding-xing-shi-xian-zai-agentluo-di-de-zhong-yao-guan-jian/)