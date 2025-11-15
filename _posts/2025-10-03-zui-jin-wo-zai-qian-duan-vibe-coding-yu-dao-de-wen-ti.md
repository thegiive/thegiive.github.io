---
layout: post
title: "最近我在前端 Vibe Coding 遇到的問題"
date: 2025-10-03 15:13:06 +0000
permalink: /zui-jin-wo-zai-qian-duan-vibe-coding-yu-dao-de-wen-ti/
image: /assets/images/Generated-Image-October-03--2025---10_51PM.png
description: "我這幾天因為一個重要的案子，決定也來 VIBE Coding 一下，寫寫frontend feature（我從來沒寫過 frontend Vue 的程式）..."
---




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
