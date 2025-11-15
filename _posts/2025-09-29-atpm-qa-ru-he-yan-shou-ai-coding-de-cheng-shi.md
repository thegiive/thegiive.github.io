---
layout: post
title: "[ATPM] QA：如何驗收 AI Coding 的程式"
date: 2025-09-29 13:57:40 +0000
permalink: /atpm-qa-ru-he-yan-shou-ai-coding-de-cheng-shi/
image: /assets/images/ChatGPT-Image-2025---9---29----------09_52_27-1-1.png
description: "AI 會寫 Code 了，但誰來為結果負責？..."
---

[ai-coding](https://ai-coding.wiselychen.com/tag/ai-coding/)

# [ATPM] QA：如何驗收 AI Coding 的程式

[ ![Wisely Chen](/assets/images/6672228-F20250919----02-----------SN------10945w-1.jpg) ](/author/wisely/)

#### [Wisely Chen](/author/wisely/)

29 Sep 2025 — 9 min read

![\[ATPM\] QA：如何驗收 AI Coding 的程式](/assets/images/ChatGPT-Image-2025---9---29----------09_52_27-1-1.png)

### AI 會寫 Code 了，但誰來為結果負責？

在我們全面擁抱 AI Coding，並成功讓開發者轉型為「AI 指揮家」之後，一個更深層、更棘手的問題浮上檯面：「AI 寫的程式碼，誰來驗證？誰敢保證它的品質？」

AI 生成程式碼的速度令人驚艷，但它的「幻覺」和「不穩定性」也同樣令人不安。根據[上一篇](https://ai-coding.wiselychen.com/atpm-kai-fa-zhe-dev-de-shui-bian-cong-gong-du-sheng-ma-nong-dao-ai-zhi-hui-jia/)的介紹，我們知道人跟 AI 協作模式有三種 Embed , Copilot ,還有 Agent 。經過這段時間不同事件大家對 VIBE Coding 的質疑，Embed / Copilot 模式下，人在都是在流程裡面，AI 都是以助手形式存在。

但是 AI Agent 問題的核心在於

> AI Agent 模式下，AI 是無法扛責的，最後還是要人來掛保證, 或是承擔後果

## 人作為驗收方的三大策略

這時候，我們只能使用以下三個策略，而且我建議三個都要

  1. 人至少要對 AI 寫啥有一點認識
  2. 人至少要對結果有充分的 QA 驗證
  3. 人要設計最壞情況的控管機制

第一個 "人至少要對 AI 寫啥有一點認識"很簡單，你總是知道AI在幹麻？ 這個對很多 Vibe Coding 新入坑的新朋友可能比較難，但是我建議你還是得學習一點 AI 寫的 Code ，你可以到最後都不寫Code ，但是你還是得學。很像是一個 Startup 公司創辦人，找了技術長，財務長，業務長做事情，但是到最後，我看過每一個成功的 Startup 創辦人都對這些專家的東西「略懂」，至少創辦人都可以跟不同領域討論一些議題。

另外一個 "最壞情況的控管機制" ，你都是要做「我一定會出錯」的心理準備來設計防火牆的。我們舉哪位秦小姐事件來說，如果你要上線一個 AI 服務，或許你要抱著你的 API Key 就是有可能被濫用的假設下，可能損失很多錢來防範，像是你的 API Key 是用 Pre-Buy 的 Credict 機制（這樣最多只會收費到現在 Credict 的數量），或是買 Vibe Coding SaaS 月費制的方案，而非直接採取 Google Cloud 的方案（公有雲很難硬上限控管帳單）。

## 如何做充分的 QA 驗證

我們意識到，解決 AI 不確定性的方法，不是去期待一個更完美的 AI，而是建立一個

  1. Copilot 的開發模式 , 確保任何時候 都可以停下來
  2. 用 AI 來做QA 

的驗證流程。

其實我們做法跟現在的 QA/QE/DevOps 方法論沒啥差別，但是我們 ATPM 覺得用 AI 有機會做到「更嚴謹」而且「更高效」的 QA 流程。原因就是在我們整套流程追求正確的 PRD ，並且為此增加了大量的人工反饋機制。

![](/assets/images/image-49.png)

理論很簡單：有了正確的 PRD ，AI 就對業務邏輯有正確的理解，那 AI 應該可以比人作為 QA ，瞬間撰寫更詳細的QA automation script。當我們發現 PRD 有錯，改就是了，QA的 automation script 再由 AI 產生就好了。

### AI 驗證比人詳細

舉個例子，當我們人要驗證新帳務系統的數據跟之前的老數據是否一致，一般來說這是一個數據比對的議題，A Data = B Data 。通常我們的做法會對 

  1. A Data Key 值數量 distinct 然後跟 B Data 比對
  2. A Data 重要欄位相加 = B 重要欄位相加
  3. A Data 重要欄位 percentile = B data 重要欄位 percentile
  4. .... 

但是，人作為 QA ，對於大量的重複數據驗證需求，通常會很偷懶的只做某些欄位的驗證跟分析，更何況通常很多時候大家都會直接用 excel 樞紐來做，這時候很難去做到精確到每個欄位的驗證，身為技術主管，我也很難追蹤哪些有驗過，哪些沒驗過 

但是 AI 呢，不好意思，他會根據 PRD 跟數據，看完 schema 長相後，直接對每個欄位進行很完整的 distinct count, sum, avg, percentile ...etc 

![](/assets/images/image-46-1.png)

這種程度的驗證，用人根本做不到。基本上，QA因為是高重複度，高精準度要求的場景，很適合機械來做。所以只要用提示詞設定 QA 任務的框架，加上正確 PRD 的上下文， 在我經歷的場景下，AI其實 QA 效率遠高於人。

### PRD 正確性的問題

話雖然這麼說，在做帳務系統時，我們在 QA 驗證還是遇到大量議題，最多議題都是 PRD 不精確，而原因[之前](https://ai-coding.wiselychen.com/atpm-prdde-zhong-yao-xing/)也提過，

> 原因是這是一個真實已經運行數年的運輸業務帳務系統，不是外面的 POC 系統，這是真的在營運運送真實的東西。

當你面對是一個已經上線一段時間，真實的業務，很多時候要一次把業務需求梳理清楚是困難的。根據經驗，我們有3~4成 PRD 是在 Dev 的時候發現 PRD 寫錯，另外 34成是在 QA時發現 PRD有誤，所以也是因為這樣，ATPM 這個流程在特別強調迭代式的更新 PRD，不追求一次將 PRD 搞清楚。

這裡跟一般傳統軟工就很不同，傳統軟體工程改了 PRD 應該會很麻煩的，Code 要改，QA也要改。但是因為我們是 AI 時代，只要確保 PRD 是正確的，Code / QA 要改都是很快的事情。 

### AI 讓 QA可以輪換不同的人

也是因為我們理解 PRD 是需要時間迭代的，我們 ATPM 在 [Dev 時候](https://ai-coding.wiselychen.com/atpm-kai-fa-zhe-dev-de-shui-bian-cong-gong-du-sheng-ma-nong-dao-ai-zhi-hui-jia/) Copilot 時就塞入驗證的環節，讓 PRD 的驗證提早進行。我們稱為 Unit Test ，但是其實已經是一個小 QA了

在 AI 時代，就算 Dev 是工程師不是 QA 專長，只要有正確的 PRD 跟 QA 提示詞，要隨意啟動一次正常的 QA 也是很簡單的

![](/assets/images/image-47.png)

另外一件事情就是之前提過的，有了 PRD ，我們根本就不挑QA的人，誰有空就誰上。 這些都是架構在有個 AI Driven 的 QA框架才能成行。

用不同人做 QA 的問題就是在 Edge Case 這些的制定上，大家都沒有QA經驗，不容易抓出一些比較麻煩的 QA議題，這時候，AI 其實幫助到很多。

### 就算這樣，我們到最後 QA 還是切到半手工

就算剛剛講那麼多，到最後我們依舊還是一半 AI 自動QA，一半場景手工。原因很簡單，在我們的場景下，不只是 PRD 可能不是最新，甚至連 PROD 舊數據（我們稱之為 Golden Data）都可能不是最新的。

![](/assets/images/image-50.png)

你可能會問，這樣不是算錯錢嗎？我只能說，有可能是算錢的合約沒更新到財務那，也可能是我們PM 找到合約不是最新版....etc 。總之，這些奇怪的事情都會發生。最後結果就是 Golden Data 很多時候不是最 Golden 的數據。

這時候只能切到手工，用 QA 人力來做驗證，而不是省時省力的 AI 自動 Automation。當我們驗證結束上 Prod 之後，這些新開發好的數據就會 commit 進去 Golden Data 資料庫，變成真正的 Golden Data 。然後理論上下次就可以自動 AI 測試

### QA 報告統一性

最後一個重點，既然我們用那麼多不同人跟不同方式來 QA驗證，為了避免相關的觀看上的困擾，我們統一了 QA的報告格式，讓所有人/AI 都 follow 同一個驗證方式，避免最後品質或是標準不同步。

![](/assets/images/image-48-1.png)

#### 結論：QA 在 AI 時代的新價值

我們到最後，發現到我們花了大量的力氣在 QA 上，但是這一切都是值得的。雖然 AI 可以加速 QA的驗證，但是我們開發過程中只要看到有問題的部分，就直接切到手工來增加正確性。所以雖然一開始我以為可以加速 80% 在 QA上，最後只加速 20% 

這一切都是希望本次的 ATPM 的 AI Coding 演出是沒有問題的，這個系統最後也成功上線來回報我們的期待。

[ ![Multi-Agent 協作模式：當 AI 學會「會診」這件事](/assets/images/ChatGPT-Image-2025---11---15----------04_36_04.png) Multi-Agent 協作模式：當 AI 學會「會診」這件事 我上週回老家看了久違的第四台「緯來日本台」，看一個日本節目「恐怖家庭醫學」，裡面講到一個年長者「最近常常心悸、手抖、睡不好」。因為是心臟的因素，所以患者直接找心臟科檢查後，拿到一疊厚厚的報告——結果心臟科醫生看完報告說：「你的心臟結構完全正常，心電圖也沒問題，可能是壓力太大，回去多休息就好。」患者心想：「可是我真的有心悸啊！難道是我自己想太多？」於是患者找了神經科說可能是自律神經失調，拿了藥物減壓，但症狀完全沒改善。 弄了很久一直兜兜轉轉。最後一個經驗豐富家醫科醫生，告知患者「這可能是甲狀腺的問題，要去看內科」才發現這是甲亢的症狀，調整好藥物很快就好了。很多時候人體很多時候是一個連動的生態系統，有些問題的表象跟真正的Root Cause是兩回事，所以患者很容易找錯醫生弄錯科目。 但如果是在好的健檢中心，做法就完全不一樣了。健康檢查會根據你的全方位給予檢查——最後針對你的完整報告進行討論，這時候甲亢的 Root Cause 很快就會被最後的把關者抓出來 " 問題根本不在心臟，而在甲狀腺 " 。這就是「多人協作的力量」。 AI Agent 的世界也是一樣的道理。 By Wisely Chen 15 Nov 2025 ](/multi-agent-xie-zuo-mo-shi-dang-ai-xue-hui-hui-zhen-zhe-jian-shi/) [ ![那天我在產業園區分享：AI 能不能做起來，其實看人](/assets/images/S__88875042.jpg) 那天我在產業園區分享：AI 能不能做起來，其實看人 今天我在新北產業園區，在我們公司的 AI 轉型的活動 在各位傳統產業的前輩講述我之前在傳統產業做 AI 轉型的經驗 我認為「 AI 要在傳產落地，先解決的永遠不是模型，而是人、流程與文化。」 我把這幾年的實戰經驗濃縮成一套能在傳統產業中真正起作用的框架： 現況分析：先理解現場，再談技術 我們創建了一個以 公司各部門的老前輩 + Intern 為主的種子團隊，深入一線流程、取得高層支持，建立真正的共識。 AI 不是空降，而是跟現場一起改。 快速勝利：小範圍試點，讓大家看到成效 選一個可控的場域，把 AI +種子團隊拉進真實流程。 像我用 AI + RPA + OCR + 快速掃描器 = 一個可持續可落地，並且有效益成果 這樣的「小勝利」，是推動組織願意往下走的關鍵。 全面升級：從工具導入到組織轉型 把建置的種子團隊散步到全公司各個部門 可以用很快的速度去 scale 全面開花 By Wisely Chen 13 Nov 2025 ](/na-tian-wo-zai-chan-ye-yuan-qu-fen-xiang-ai-neng-bu-neng-zuo-qi-lai-qi-shi-kan-ren/) [ ![AI 信任崩塌的真正原因：勞資零和賽局的再現](/assets/images/ChatGPT-Image-2025---11---10----------09_24_03.png) AI 信任崩塌的真正原因：勞資零和賽局的再現 根據《Harvard Business Review》近期發表的〈Workers Don’t Trust AI. Here’s How Companies Can Change That〉，美國基層員工對公司提供的 AI 工具信任度在短短數月內暴跌：對生成式 AI 的信任下降 31%，對自主決策型 AI 更下滑 89%。近半數員工反而更信任非官方AI 工具。另外無獨有偶MIT 的研究《The GenAI Divide: State of AI in Business 2025》更進一步揭示了這種現象，並命名為 Shadow AI：員工在公司外私下使用未授權的 AI 來完成工作。研究指出，約有 By Wisely Chen 10 Nov 2025 ](/ai-xin-ren-beng-ta-de-zhen-zheng-yuan-yin-lao-zi-ling-he-sai-ju-de-zai-xian/) [ ![\[Agent part 3\] Interleaved Thinking 呈現的穩定性是現在Agent落地的重要關鍵](/assets/images/ChatGPT-Image-2025---11---8----------08_01_49.png)