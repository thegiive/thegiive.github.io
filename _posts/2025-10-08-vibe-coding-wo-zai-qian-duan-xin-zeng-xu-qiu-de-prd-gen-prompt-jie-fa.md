---
layout: post
title: "[VIBE Coding] 我在前端新增需求的 PRD 跟 Prompt 解法"
date: 2025-10-08 00:43:22 +0000
permalink: /vibe-coding-wo-zai-qian-duan-xin-zeng-xu-qiu-de-prd-gen-prompt-jie-fa/
image: /assets/images/Gemini_Generated_Image_6zdw0k6zdw0k6zdw-1.png
description: "上次提到我在前端這邊做AI Coding 很適合 0% -> 70% , 或是 99 -> 100%的做法，但是在 90% -> 100% 遇到了蠻多的小問題，經過幾天的討論修正之後，我已經大概列出了比較適合的方式。根據這一週來改了十幾個 Feature的經驗，這個流程對我這樣非前端的人來說，感覺 90% -> 100% 除了後續檢核需要前端幫忙以外，幾乎都是我可以自己處理。..."
---

[ai-coding](https://ai-coding.wiselychen.com/tag/ai-coding/)

# [VIBE Coding] 我在前端新增需求的 PRD 跟 Prompt 解法

[ ![Wisely Chen](/content/images/size/w160/2025/09/6672228-F20250919----02-----------SN------10945w-1.jpg) ](/author/wisely/)

#### [Wisely Chen](/author/wisely/)

08 Oct 2025 — 4 min read

![\[VIBE Coding\] 我在前端新增需求的 PRD 跟 Prompt 解法](/content/images/size/w1200/2025/10/Gemini_Generated_Image_6zdw0k6zdw0k6zdw-1.png)

上次提到[我在前端這邊做AI Coding](https://ai-coding.wiselychen.com/zui-jin-wo-zai-qian-duan-vibe-coding-yu-dao-de-wen-ti/) 很適合 0% -> 70% , 或是 99 -> 100%的做法，但是在 90% -> 100% 遇到了蠻多的小問題，經過幾天的討論修正之後，我已經大概列出了比較適合的方式。根據這一週來改了十幾個 Feature的經驗，這個流程對我這樣非前端的人來說，感覺 90% -> 100% 除了後續檢核需要前端幫忙以外，幾乎都是我可以自己處理。

這個場景其實還蠻常見的，現在 VIBE Coding 大家都在講從頭新建一個網站，這個東西對工程師來說太低頻了，其實程式設計師大部分的時候都是在新增修改功能某個到在現有的 App 上，所以這個技巧我實際跟前端一起弄四五天後，我個人覺得還蠻好用的。

### 流程圖

![](/assets/images/image-10-1.png)

首先第一個就是把舊設計稿跟U I的截圖請A I幫我做比較，這個部分主要是列出新增或修改的UI介面在哪邊，這個時候出來的東西可能是一個free format，但不要緊。舉例，我截圖一個 Google Doc 畫面，我故意把中間的 提示 icon 修掉 , 當作做 feature 之前的 V1.0 ，然後再把原始圖變成 V1.1 

![](/assets/images/-------2025-10-08-------7.57.40-------1.png)範例：我故意把中間的 提示 icon 修掉 , 當作做 feature 之前的 V1.0 ![](/assets/images/-------2025-10-08-------7.57.40-1.png)範例：原始畫面當作做做完 feature 之前的 V1.1 

接下來下一步，我們請A I幫我產生有剛剛的修改的或是新增的需求列表表，這個時候就是一個比較粗的P R D。這裡我其實都會預設使用 Gemini ，因為我體感 Gemini OCR 蠻強的，UI 抓中文字比較簡單

![](/assets/images/image-11.png)Gemini OCR 

然後我們請他變成一些 feature list ，一個一個 功能變化都寫成簡易的 feature list ，此處我還是不規範 PRD ，隨意產生即可。下面的範例是我這幾天 onProd 某個功能 masking 過的寫法，保證真實，不像外面開課程都是一堆 demo code XD

![](/assets/images/data-src-image-6d5fe5e6-67de-46b4-bd1f-2fa4ee08e5b5.png)相關功能文件 - 簡略的 feature list 

下一步我們準備好的P R D 的Temple，以及相關的 supporting Tech PRD 資料(API文件 或是相關的程式碼的規範文件) ，就會產生一個完整的P R D。以下也是那功能最後產生的 詳細 PRD 

![](/assets/images/data-src-image-a3b4ee0e-4b31-405a-868e-d57931f5710f-1.png) 有 需求列表 , tech requirement , 還有 supporting data 的

有這個完整的P R D之後，我們就可以請AI幫我們做Coding，我之前經驗幾乎一次過。產生 code 的 Prompt 超級簡單的，因為 PRD 都已經寫好了。

![](/assets/images/data-src-image-fa64d1f5-e960-433b-b391-b34c23398453-1.png)![](/assets/images/data-src-image-473c3d0b-dafc-4184-bea1-7d11d78f9530-1.png)

最後給 RD 檢核， 送交 QA 。

### 結果

根據這一週來改了十幾個 Feature的經驗，這個流程對我這樣非前端的人來說，感覺 90% -> 100% 除了後續檢核需要前端幫忙以外，幾乎都是我可以自己處理。

### 附件A: PRD Template 

## This post is for subscribers only

Subscribe now

Already have an account? Sign in

[ ![Multi-Agent 協作模式：當 AI 學會「會診」這件事](/content/images/size/w600/2025/11/ChatGPT-Image-2025---11---15----------04_36_04.png) Multi-Agent 協作模式：當 AI 學會「會診」這件事 我上週回老家看了久違的第四台「緯來日本台」，看一個日本節目「恐怖家庭醫學」，裡面講到一個年長者「最近常常心悸、手抖、睡不好」。因為是心臟的因素，所以患者直接找心臟科檢查後，拿到一疊厚厚的報告——結果心臟科醫生看完報告說：「你的心臟結構完全正常，心電圖也沒問題，可能是壓力太大，回去多休息就好。」患者心想：「可是我真的有心悸啊！難道是我自己想太多？」於是患者找了神經科說可能是自律神經失調，拿了藥物減壓，但症狀完全沒改善。 弄了很久一直兜兜轉轉。最後一個經驗豐富家醫科醫生，告知患者「這可能是甲狀腺的問題，要去看內科」才發現這是甲亢的症狀，調整好藥物很快就好了。很多時候人體很多時候是一個連動的生態系統，有些問題的表象跟真正的Root Cause是兩回事，所以患者很容易找錯醫生弄錯科目。 但如果是在好的健檢中心，做法就完全不一樣了。健康檢查會根據你的全方位給予檢查——最後針對你的完整報告進行討論，這時候甲亢的 Root Cause 很快就會被最後的把關者抓出來 " 問題根本不在心臟，而在甲狀腺 " 。這就是「多人協作的力量」。 AI Agent 的世界也是一樣的道理。 By Wisely Chen 15 Nov 2025 ](/multi-agent-xie-zuo-mo-shi-dang-ai-xue-hui-hui-zhen-zhe-jian-shi/) [ ![那天我在產業園區分享：AI 能不能做起來，其實看人](/content/images/size/w600/2025/11/S__88875042.jpg) 那天我在產業園區分享：AI 能不能做起來，其實看人 今天我在新北產業園區，在我們公司的 AI 轉型的活動 在各位傳統產業的前輩講述我之前在傳統產業做 AI 轉型的經驗 我認為「 AI 要在傳產落地，先解決的永遠不是模型，而是人、流程與文化。」 我把這幾年的實戰經驗濃縮成一套能在傳統產業中真正起作用的框架： 現況分析：先理解現場，再談技術 我們創建了一個以 公司各部門的老前輩 + Intern 為主的種子團隊，深入一線流程、取得高層支持，建立真正的共識。 AI 不是空降，而是跟現場一起改。 快速勝利：小範圍試點，讓大家看到成效 選一個可控的場域，把 AI +種子團隊拉進真實流程。 像我用 AI + RPA + OCR + 快速掃描器 = 一個可持續可落地，並且有效益成果 這樣的「小勝利」，是推動組織願意往下走的關鍵。 全面升級：從工具導入到組織轉型 把建置的種子團隊散步到全公司各個部門 可以用很快的速度去 scale 全面開花 By Wisely Chen 13 Nov 2025 ](/na-tian-wo-zai-chan-ye-yuan-qu-fen-xiang-ai-neng-bu-neng-zuo-qi-lai-qi-shi-kan-ren/) [ ![AI 信任崩塌的真正原因：勞資零和賽局的再現](/content/images/size/w600/2025/11/ChatGPT-Image-2025---11---10----------09_24_03.png) AI 信任崩塌的真正原因：勞資零和賽局的再現 根據《Harvard Business Review》近期發表的〈Workers Don’t Trust AI. Here’s How Companies Can Change That〉，美國基層員工對公司提供的 AI 工具信任度在短短數月內暴跌：對生成式 AI 的信任下降 31%，對自主決策型 AI 更下滑 89%。近半數員工反而更信任非官方AI 工具。另外無獨有偶MIT 的研究《The GenAI Divide: State of AI in Business 2025》更進一步揭示了這種現象，並命名為 Shadow AI：員工在公司外私下使用未授權的 AI 來完成工作。研究指出，約有 By Wisely Chen 10 Nov 2025 ](/ai-xin-ren-beng-ta-de-zhen-zheng-yuan-yin-lao-zi-ling-he-sai-ju-de-zai-xian/) [ ![\[Agent part 3\] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵](/content/images/size/w600/2025/11/ChatGPT-Image-2025---11---8----------08_01_49.png) [Agent part 3] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵 大家都知道我用 AI 來 enable 很多intern 來當作很多正職的事情，當然他們雖然都很年輕跟熱情，但是我管理團隊時發現一個規律： 當我派給幾個 Senior 的同事 ，我通常只需要 weekly 跟他開會，給他幾個任務，一週後檢查一次就好。他可以獨立工作，中間遇到問題會自己判斷、調整，如果有大問題他們會舉手跟我講，不容易走偏。 當我要安排工作給我的 intern ，跟 Senior 最大的不同就是， Junior 我通常會每半天或是每過一天就會跟他聊一下提醒一下可能要注意什么事情。因為他很容易遇到了某些複雜任務時，他就可能在某一步卡住，又沒有舉手，基於錯誤理解繼續做下去，最後整個方向偏了，也浪費了他整天的時間。 這是Sr 跟 Jr 經驗的差別，獨立作戰的能力 AI Agent 也是如此 現在考驗 AI Agent 最大的地方，不是他的智商，主要著重點是它的連續工作穩定性。如果人類需要介入的越少，就代表它可以自主完成工作， By Wisely Chen 08 Nov 2025 ](/agent-part-3-interleaved-thinking-cheng-xian-de-wen-ding-xing-shi-xian-zai-agentluo-di-de-zhong-yao-guan-jian/)