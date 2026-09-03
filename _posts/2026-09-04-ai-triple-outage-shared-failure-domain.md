---
layout: post
title: "Claude 先掛、Grok 跟著、ChatGPT 晚一小時：三家 AI 大當機，真正被推翻的是那條「排除項」"
date: 2026-09-04 09:00:00 +0800
permalink: /ai-triple-outage-shared-failure-domain/
tags: [outage, 故障域, Colossus, Anthropic, OpenAI, xAI, Cloudflare, BCP, 地端模型, 供應鏈風險]
categories: [AI 產業分析]
image: /assets/images/ai-triple-outage-shared-failure-domain-cover.png
description: "9 月 3 日，Claude 在美東時間上午九點四十一分左右先出事，Grok 幾乎同時，ChatGPT 晚了約一小時，Gemini 全程沒有官方故障公告，Cursor 跟著上游一起不可用。技術圈當天丟出兩個假說：Cloudflare 接入層異常，或是使用者切換造成的流量雪崩。但 Cloudflare 當天直接否認，而 SpaceXAI 在傍晚發文承認孟菲斯算力中心故障，並向「受影響的算力夥伴」道歉——2026 年 5 月，Anthropic 才剛租下孟菲斯 Colossus 1 幾乎全部的算力。這篇拆的不是假說對不對，而是那條沒有人檢查的排除項：三家的算力底座真的互相獨立嗎。"
author: Wisely Chen
faq:
  - question: "2026 年 9 月 3 日的 AI 大當機，官方公布根因了嗎？"
    answer: "到目前為止沒有跨公司的統一根因說明。OpenAI、Anthropic、xAI 都在各自的狀態頁確認了事故並修復，但沒有任何一家把原因指向共同的基礎設施。唯一具名的硬體故障來自 SpaceXAI 的官方貼文，承認孟菲斯（Memphis）算力中心當天上午故障，並向受影響的算力夥伴道歉。Cloudflare 則明確否認自己有重大服務中斷。"
  - question: "什麼是故障域（Failure Domain）？跟多供應商策略差在哪？"
    answer: "故障域指的是「一起壞掉」的最小單位——同一台機器、同一個機櫃、同一棟資料中心、同一條電力供應。多供應商策略分散的是商業合約關係，故障域分散的是物理與基礎設施關係。兩者常被當成同一件事，但當供應商 A 把算力租給供應商 B 的時候，兩個 logo 就落在同一個故障域裡。2026 年 5 月 Anthropic 同意租下 xAI 孟菲斯 Colossus 1 幾乎全部算力，就是這種情況。"
  - question: "為什麼 Gemini 沒事，其他三家都掛了？"
    answer: "Gemini 在 9 月 3 日全程沒有發布官方故障公告。社群上流傳的解釋有兩種：一種是 Google 用自家 TPU 而其他三家用 Nvidia GPU，被 Cardano 創辦人 Charles Hoskinson 拿來當成國家級攻擊的證據；另一種是 Google 的推理跑在自家 Google Cloud，不與其他實驗室共用資料中心。第二種解釋不需要假設有人動手，也能說明同樣的現象，證據要求低得多。"
  - question: "Cursor 為什麼會跟著掛？"
    answer: "Cursor 沒有自研的前沿模型，它的核心功能是呼叫 OpenAI、Anthropic 這類上游供應商的 API。上游回傳錯誤時，Cursor 沒有可以退回的本地推理能力，所以會同步不可用。這是純 API 轉手型產品的結構性風險：你的可用性上限等於上游可用性，而且你連故障通知都要等上游先發。"
  - question: "個人開發者要怎麼準備下一次三家同時掛？"
    answer: "跨雲供應商切換在這次無效，因為 Claude、Grok、ChatGPT 有大約一小時的重疊不可用期，三家全部恢復正常是在美西時間下午 12:38。實際有效的準備只有兩類：一是本機跑得動的地端模型，故障域與雲端不重疊；二是預先規劃一段離線也能推進的工作（讀既有程式碼、寫規格文件、跑測試套件），讓三小時的空窗不變成三小時的停工。  ---"
---

9 月 3 日美東時間上午，Anthropic 的狀態頁先亮起紅燈。約九點四十一分，Claude 出現事故，Mythos、Fable、Opus 都在受影響清單上。Grok 幾乎同一時間開始降級，ChatGPT 晚了大約一個小時。Gemini 全程沒有發布官方故障公告。Cursor 自己沒有前沿模型，上游一報錯它就跟著不可用。

Downdetector 的尖峰落在美東時間 10:30 到 11:00 之間：ChatGPT 逾三萬五千筆、Claude 約一千四百筆、Grok 約一千兩百筆（[Karmactive 整理](https://www.karmactive.com/chatgpt-claude-grok-simultaneous-ai-outage-september-2026/)）。三家服務在美西時間下午 12:38 全部恢復正常。

有人傳了一份分析給我，裡面列了兩個假說跟三條排除項。假說寫得很紮實，我第一時間也覺得合理。但花了半天把來源逐條查過之後，我的結論是：這次真正該重寫的不是假說，是**排除項第三條**。

## 30 秒定位

| 項目 | 內容 |
|------|------|
| 日期 | 2026-09-03 |
| 順序 | Claude（美東 09:41 左右）→ Grok（幾乎同時）→ ChatGPT（晚約一小時） |
| 未受影響 | Gemini（無官方故障公告） |
| 間接受害 | Cursor（呼叫上游 API） |
| 官方根因 | 至今無跨公司統一說明 |
| 唯一具名的硬體故障 | SpaceXAI 承認孟菲斯算力中心故障 |
| 官方否認 | Cloudflare 明確否認有重大服務中斷 |

## 假說一：Cloudflare 接入層

這是事發最初一小時，X 上聲量最大的答案。邏輯很直觀：三家的前端接入、DNS、DDoS 防護都大量用 Cloudflare，Cloudflare 一抖，使用者根本送不到後端，模型算力再健康也沒用。

而且 Cloudflare 狀態頁當時確實掛著兩個進行中的議題：R2 自訂網域的 HTTP/3 問題，以及部分 WARP 使用者地理定位不正確。對想快速結案的人來說，這兩條看起來很像證據。

問題是 Cloudflare 直接把話講死了。他們對 The Register 的聲明是：

> Cloudflare is not experiencing any significant service disruptions at this time. Our services are operating normally, and any reporting that deviates from this is incorrect.

翻成白話：不只是「我們沒事」，而是「任何跟這個說法不一樣的報導都是錯的」。這是廠商聲明裡少見的強度。

再加上時間線本身就跟這個假說對不上。單純的 CDN 全球故障通常是同步大面積報錯，不是 Claude 先掛、ChatGPT 一小時後才掛。R2 自訂網域的 HTTP/3 問題影響的是物件儲存的一小塊，不是全球 API 入口。

我的判讀：這個假說在事發當天就該退場了。它之所以撐了那麼久，是因為它是最容易講的故事——過去兩年 Cloudflare 確實掛過幾次大的，大家的肌肉記憶還在。

## 假說二：流量雪崩

第二個假說是級聯過載。Claude 先出事，大量使用者、自動化腳本、API client 失敗後自動重試，同時人工切換到 Grok 和 ChatGPT；瞬時湧入的流量超過另外兩家的閘道限流閾值，依序壓垮接入層；client 端的無限重試再放大一輪，形成自激式的流量洪峰。

這個假說有一個很強的證據：**時間差**。ChatGPT 晚了約一小時才掛，這正是「先有人掛、流量才遷移、遷移完才壓垮下一家」該有的形狀。如果是共同上游故障，三家應該同步倒下。

它也有一個很強的反證：**Grok 幾乎跟 Claude 同時掛**。中間沒有留下足夠的流量遷移時間。使用者從 Claude 跳到 Grok 需要幾分鐘到幾十分鐘的擴散，不是幾秒。

所以假說二解釋得了第三張骨牌，解釋不了第二張。

## 真正的問題出在排除項

那份分析列了三條排除項，前兩條我沒意見：

1. 不是模型程式碼 bug——多家獨立模型同時出現核心 bug 的機率極低。
2. 不是網路攻擊——各家狀態頁都沒有揭露 DDoS。

第三條是這樣寫的：不是統一雲機房斷電，因為三家算力底座分別依托 Azure、AWS、自建集群，底層機房相互獨立。

這條在 2026 年 5 月就已經不成立了。

維基百科 Colossus 條目寫得很清楚：

> In May 2026 Anthropic agreed to rent essentially all compute capacity at Colossus 1.

Colossus 1 在孟菲斯，2024 年 7 到 9 月間投入運作，初期約十萬顆 H100，電網併接從約 8MW 一路往 150MW 推。它原本是 xAI 拿來訓練 Grok 的機器。2026 年 5 月之後，Anthropic 租下了它幾乎全部的算力。

事發當天傍晚，SpaceXAI 官方帳號發了這段話：

> We are sorry for the issues you may have experienced with Grok following an outage at our Memphis compute center this morning. We'd also like to apologize to our impacted compute partners.

截至 9 月 4 日上午，這則貼文累積約一萬個讚、143.2 萬次瀏覽、478 則回覆（[原文](https://x.com/SpaceXAI/status/2095597264043717014)，本文封面即為該貼文截圖）。

重點在最後一句。他們不只為 Grok 道歉，還為「受影響的算力夥伴」道歉。這是整起事件裡，唯一一個公司具名承認的硬體故障，而且明說有外部客戶被波及。

把兩件事放在一起：孟菲斯出事、Anthropic 租下孟菲斯幾乎全部算力、Claude 和 Grok 幾乎同時降級。第二張骨牌的疑問就沒了——那兩張骨牌可能從頭到尾就是同一張。

## 那 ChatGPT 呢

這是我不打算硬凹的地方。OpenAI 跟孟菲斯沒有已知關係。ChatGPT 晚一小時才掛，用共用故障域解釋不通。

有媒體把矛頭指向 Azure East US，主張三家都在同一個雲端故障域裡，Gemini 因為跑在 Google Cloud 才活下來。但 [Quartz 的報導](https://qz.com/chatgpt-claude-grok-simultaneous-outages-090326)明確寫道，沒有官方確認 Azure 故障造成這次事件，也沒有任何共同基礎設施故障被證實。

所以我的判讀是兩層原因串接：

- **第一層（物理層）**：孟菲斯算力中心故障，同時打掉 Claude 和 Grok。這一層有官方貼文和租賃合約支撐。
- **第二層（流量層）**：兩家同時失效後，重試風暴加上使用者手動切換，把負載推向 OpenAI，一小時後越過閾值。這一層沒有直接證據，但時間差的形狀對得上。

一個事件不一定只有一個根因。這次比較像是物理層先開了一個洞，流量層再把洞撕大。

## Charles Hoskinson 的第三個版本

順帶一提，當天還有一個傳播力很強的版本。Cardano 創辦人 Charles Hoskinson 說：

> It looks like a national state brought down Claude, ChatGPT, and Grok

他的證據是 Gemini 沒事：

> They all use Nvidia chips. Google doesn't.

這個觀察本身是對的——Google 用自家 TPU，其他三家用 Nvidia。但從「共用晶片供應商」推到「國家級攻擊」中間缺了太多步。同樣的觀察有一個更平淡的解釋：共用晶片往往意味著共用資料中心、共用電力供應、共用散熱設計，也就是共用故障模式。不需要有人動手，一棟樓的電出問題就夠了。

我把它放進來不是要嘲笑，而是因為它示範了一件事：**當官方不給根因，市場會自己填**，而填進去的東西通常比事實更戲劇化。

## 這修正了我之前寫過的一篇文章

2025 年 11 月 Cloudflare 大當機的時候，我寫過[《用 AI Coding 當 BCP 另外一個方案有沒有搞頭？》](/ai-coding-dang-bcp-cloudflare-da-dang-ji-de-ling-lei-jie-fang)。那篇的論點是：Andrew Ng 的團隊用 AI Coding 快速搭出 Cloudflare 的最小備援組件，撐過了那次故障，所以 AI Coding 可以當成一種新的 BCP 手段。

那篇有一個沒有寫出來的假設：**AI 是永遠在線的搶修工具**。

9 月 3 日把這個假設戳破了。當掛掉的是 AI 本身，AI Coding 就不能當 BCP。那三個小時裡，你的搶修工具跟你要搶修的東西一起躺平。

這不代表那篇文章錯了，而是它的適用邊界要補一句：AI Coding 當 BCP 的前提，是故障域不包含 AI 供應商自己。Cloudflare 掛掉的時候這個前提成立，這次不成立。

## 這具體改變了誰的什麼決策

**企業 CTO。** 之前的採購邏輯是「我們接了三家供應商，不會全掛」。這次之後，合約談判要多一個問題：你的推理服務跑在哪一個實體資料中心，跟我另外兩家供應商重疊嗎。

這個問題現在很難問到答案，因為算力租賃關係大多不公開——Anthropic 租 Colossus 1 這件事，我是在維基百科上查到的，不是從任何一份採購文件。但問不到答案這件事本身就是資訊：你的多供應商策略，可能只是三個 logo 掛在一個故障域上。

**個人開發者。** 之前的 fallback 路徑是 Claude 掛了切 Codex、Codex 掛了切 Grok。這次這三條路同時斷了約三個小時。

真正有效的 fallback 只剩兩種：一台跑得動的地端機器，或是一段離線也能繼續的工作型態（讀 code、寫規格、跑測試）。我在 [RTX Pro 6000 一週實驗](/rtx-pro-6000-tier1-week-final-offload-qwen-vl-vllm)裡測地端模型的時候，動機是隱私和成本。9 月 3 日之後多了第三個理由：**地端的故障域跟雲端不重疊**。這也是[《AI Coding On-Prem 的三條路》](/ai-coding-on-prem-three-paths)裡沒有展開的一條。

## 坦白說

這篇文章的核心推論——孟菲斯故障同時打掉 Claude 和 Grok——目前是**推論，不是已證實的根因**。

具體來說，有三個洞：

第一，SpaceXAI 說的「算力夥伴」沒有點名。可能是 Anthropic，也可能是完全無關的雲端轉售客戶。我是從租賃關係反推的，這中間沒有直接證據。

第二，Anthropic 租 Colossus 1 的用途沒有公開說明。大型 GPU 叢集的租賃很多是拿來訓練，訓練叢集出事不必然打掉推理服務。如果 Anthropic 的推理跑在別的地方，這條線就斷了。

第三，我完全沒辦法解釋為什麼 Anthropic 沒有在自己的事故說明裡提到孟菲斯。有可能是還沒查清楚，有可能是合約不允許，也有可能就是無關。

所以這篇該被讀成一個假說，跟我前面拆的那兩個假說站在同一排——只是我認為它的證據強度比較高，因為它至少有一家公司的官方貼文和一份公開的租賃記錄，另外兩個假說目前只有時間線的形狀。

官方根因報告出來如果推翻我，我會回來改這篇。

## 關鍵洞察

**故障域要看實體位置，不是看 vendor logo。**

過去兩年整個產業的備援心法是「多接幾家供應商」。這個心法建立在一個 2023 年還成立、2026 年已經不成立的前提上：不同的 AI 公司，跑在不同的機器上。

當前沿實驗室開始互相租算力——一家蓋了資料中心，另一家把它整包租下來——vendor 層級的分散就不再等於基礎設施層級的分散。你以為你有三家供應商，物理層可能只有一家半。

要驗證這件事，你手上唯一能用的工具是：問你的供應商推理跑在哪裡，然後看他們願不願意回答。

---

## 常見問題 Q&A

**Q: 2026 年 9 月 3 日的 AI 大當機，官方公布根因了嗎？**

到目前為止沒有跨公司的統一根因說明。OpenAI、Anthropic、xAI 都在各自的狀態頁確認了事故並修復，但沒有任何一家把原因指向共同的基礎設施。唯一具名的硬體故障來自 SpaceXAI 的官方貼文，承認孟菲斯（Memphis）算力中心當天上午故障，並向受影響的算力夥伴道歉。Cloudflare 則明確否認自己有重大服務中斷。

**Q: 什麼是故障域（Failure Domain）？跟多供應商策略差在哪？**

故障域指的是「一起壞掉」的最小單位——同一台機器、同一個機櫃、同一棟資料中心、同一條電力供應。多供應商策略分散的是商業合約關係，故障域分散的是物理與基礎設施關係。兩者常被當成同一件事，但當供應商 A 把算力租給供應商 B 的時候，兩個 logo 就落在同一個故障域裡。2026 年 5 月 Anthropic 同意租下 xAI 孟菲斯 Colossus 1 幾乎全部算力，就是這種情況。

**Q: 為什麼 Gemini 沒事，其他三家都掛了？**

Gemini 在 9 月 3 日全程沒有發布官方故障公告。社群上流傳的解釋有兩種：一種是 Google 用自家 TPU 而其他三家用 Nvidia GPU，被 Cardano 創辦人 Charles Hoskinson 拿來當成國家級攻擊的證據；另一種是 Google 的推理跑在自家 Google Cloud，不與其他實驗室共用資料中心。第二種解釋不需要假設有人動手，也能說明同樣的現象，證據要求低得多。

**Q: Cursor 為什麼會跟著掛？**

Cursor 沒有自研的前沿模型，它的核心功能是呼叫 OpenAI、Anthropic 這類上游供應商的 API。上游回傳錯誤時，Cursor 沒有可以退回的本地推理能力，所以會同步不可用。這是純 API 轉手型產品的結構性風險：你的可用性上限等於上游可用性，而且你連故障通知都要等上游先發。

**Q: 個人開發者要怎麼準備下一次三家同時掛？**

跨雲供應商切換在這次無效，因為 Claude、Grok、ChatGPT 有大約一小時的重疊不可用期，三家全部恢復正常是在美西時間下午 12:38。實際有效的準備只有兩類：一是本機跑得動的地端模型，故障域與雲端不重疊；二是預先規劃一段離線也能推進的工作（讀既有程式碼、寫規格文件、跑測試套件），讓三小時的空窗不變成三小時的停工。

---

## 資料來源

- [9to5Google：ChatGPT、Claude、Grok 同時故障（含恢復時間更新）](https://9to5google.com/2026/09/03/chatgpt-claude-grok-outages/)
- [The Register：三家同時掛掉，含 Cloudflare 聲明](https://www.theregister.com/ai-and-ml/2026/09/03/chatgpt-claude-and-grok-all-had-outages-at-the-same-time/)
- [Quartz：ChatGPT、Claude、Grok 同時故障，根因未確認](https://qz.com/chatgpt-claude-grok-simultaneous-outages-090326)
- [Karmactive：Downdetector 數據整理](https://www.karmactive.com/chatgpt-claude-grok-simultaneous-ai-outage-september-2026/)
- [SpaceXAI 官方貼文：孟菲斯算力中心故障](https://x.com/SpaceXAI/status/2095597264043717014)
- [Wikipedia：Colossus (supercomputer)](https://en.wikipedia.org/wiki/Colossus_(supercomputer))
- [Charles Hoskinson 的國家級攻擊說](https://bitcoinethereumnews.com/tech/charles-hoskinson-has-a-theory-for-ai-outage-affecting-chatgpt-claude-and-grok/)
