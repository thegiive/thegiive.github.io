---
layout: post
title: "YouTube 逐字稿：手上七八個 Agent 怎麼串？Astra 接管電腦、Grok Bot 30 美金、多 Agent 微服務架構"
date: 2026-09-13 20:00:00 +0800
permalink: /youtube-multi-agent-microservice-orchestration-transcript/
tags: [multi-agent, 微服務, Astra, Computer Use, Grok Bot, OpenClaw, Slack, GitHub, Google Drive, 雲地分工, 地端 AI, Anthropic, 蒸餾]
categories: [AI Agent]
image: /assets/images/0913_thumbnail.jpg
description: "**作者：** Wisely Chen **日期：** 2026 年 9 月 **系列：** AI Coding 實戰觀察 — YouTube 逐字稿 **關鍵字：** multi-agent, 微服務架構, Astra, Computer Use, Grok Bot, OpenClaw, Slack MQ, GitHub, Google Drive, 雲地分工, 地端 AI"
author: Wisely Chen
---

**作者：** Wisely Chen
**日期：** 2026 年 9 月
**系列：** AI Coding 實戰觀察 — YouTube 逐字稿
**關鍵字：** multi-agent, 微服務架構, Astra, Computer Use, Grok Bot, OpenClaw, Slack MQ, GitHub, Google Drive, 雲地分工, 地端 AI

---

## 這集在講什麼

這週三個觀察。**第一**，OpenAI 的 Astra 把 Computer Use 做到實用等級——不是教你步驟讓你點，而是直接打開 GCP 幫你改 OAuth。**第二**，xAI 的 Grok Bot 上線，30 美金含一台 16GB RAM 雲端 VM，等於 commercial 版的 OpenClaw。**第三**，也是最核心的：我手上同時跑七八個 agent，散在雲端、地端、個人電腦和別人的 VM 上，怎麼串在一起？答案是微服務架構的老三樣——Slack 當 MQ、Google Drive 當檔案儲存、GitHub 當帶版本的狀態儲存。最後談 Anthropic 蒸餾報告對地端 AI 部署的影響。

---

**長度：** 約 10 分鐘

{% include youtube.html id="J6BYyuEAzq0" %}

### 時間戳

- 0:00 本週三個重點
- 0:04 Astra Computer Use：直接接管 GCP 操作
- 1:04 去年還在講 Computer Use，今年 Codex 已經接管鍵盤滑鼠
- 1:40 Grok Bot：30 美金的 commercial 版 OpenClaw
- 2:51 不同場景用不同 Agent：Codex、Claude、Grok Bot、OpenClaw、地端 pi
- 4:10 七八個 agent 散在雲端地端，怎麼串在一起？
- 4:29 其實就像微服務架構：三個原語
- 5:05 我的做法：Google Drive + GitHub Private + Slack
- 5:54 人的能力 = 你能指揮調度多少 agent
- 6:44 給 Astra 一台專屬電腦
- 7:11 雲地分工：什麼時候誰做什麼
- 8:17 不只效率，能不能開創新 business？
- 9:19 Anthropic 蒸餾報告：太複雜，等塵埃落定再講
- 9:48 地端 AI 部署會比以往更重要
- 10:13 結尾

---

## 完整逐字稿

### Astra Computer Use：不是教你做，是直接幫你做

Hello 大家好。在這週的話其實有幾個事情出來。

那第一個事情就是說 OpenAI 的 Astra，就是它可能是我們目前一般人能夠拿到做 Computer Use 做得非常好的一個模型。那網路上有很多很棒的 demo，他們可能就是可以用 Astra 做一些 3D 的模型，給大家做相關的事情。

那如果是我的話，像我昨天我要把我的某一個上面的 key，然後做就是 OAuth，然後把它設定成從 testing 變成 production。在之前的話，通常就是 Claude 或是之前的 GPT 都會跟你講說大家要怎麼做，然後人去點點點。但 Astra 它就直接打開那個 GCP，然後就開始做相關的事情。當然有些審核的部分，還是會停下來讓人來做，但大部分的時候都是它自己來做。

所以就讓我想到說，哇這個世界其實進步真的蠻快的。在去年的時候，我還在那個生成式 AI 的年會講，我們怎麼用一些 Computer Use 的方式來操控 Teams，然後做一些資訊的處理。那今年的話其實 Codex 就已經可以直接接管你電腦，使用你滑鼠跟鍵盤了。那這個其實是一個非常非常大的進步。那基本上我們所想到所有傳統產業的很多的事情，在這個 Computer Use 下，基本上都有可能遇到的問題都有可能解決。那這是第一個。

### Grok Bot：30 美金的 commercial 版 OpenClaw

第二個的話，在這兩週其實出了那個 Grok Bot。那 Grok Bot 就是如同我說的，它其實非常的——它是一個非常有趣的一個產品。它有點像是一個 commercial 版的 OpenClaw 或 Manus。那唯一的差別就是說，你可以用 Grok Bot 的 30 塊美元的方案，然後就會獲得一個雲端的 16GB RAM 還有 128GB 的 Disk。那這個在雲端上面的話，如果你要租用一個月的話，基本上至少要 100 美金左右，但基本上你有 30 美金就可以用到了。然後你在上面也可以大量使用不同的 Bot 來做這件事情。

那其實它就是幫 OpenClaw 或是 Manus 這樣子的數位助手的進入成本再次降低。那我在上面也用了一些東西，我也覺得非常好用，因為它介面做得其實很好，比之前看到的 Manus 都來得更好一點。

所以這就讓我想到了，在短短的這兩週之內就看到兩個很大的變化。

### 不同場景用不同 Agent

那不過也因為這樣子，我就發現到我現在在不同的場景下都有不同的使用方式。像是在做那個程式碼的編輯的時候，大量使用 Codex 的 Astra，因為就是它現在 Coding 能力已經很強了，再加上它 Coding 完之後就直接去 Astra 的 Computer Use，然後直接做 Browser 這端的 End-to-End Test，這樣其實是比較方便的。

那一些文書撰寫、Coding 還有一些思維方式，我還是使用那個 Claude 的 Opus 或是 Fable，那目前來說我還是覺得它能力比較不錯的。但它不一定是最好的，但就是用得非常習慣。

然後因為有了 Grok Bot 之後，就是我有一些數位助手工作我會丟給 Grok Bot 做，因為很便宜，加上我本身就有 Grok 的版本。那當然還大量的工作還是在原本的 OpenClaw 上面來做。然後當然還有其他大大小小的 agent，像是我的地端的 pi，就是地端的模型加 pi，來做很多節省 token 的事情。那當然還有就是像是 Grok，然後其實也真的蠻好用的，我也可以拿來做很多的相關事情，甚至還搜尋一些 X 上面貼文。

我現在手邊至少有七八種不同的 agent 的產品。

### 微服務架構的老三樣

那現在最大的問題就在，有一些是雲端、有些是地端，然後我怎麼把這些 agent 的東西、這些 Task 把它串在一起。

所以我就發現到，其實真的把這狀態這樣連續串過來串過去的話，其實就很像一個微服務的架構。

我需要的其實就是幾個東西。第一個東西是我要一個統一的 Storage，然後從這邊這個 agent 做一些事情之後，它可以快速同步到另外一層。那第二個的話就是，我需要一些檔案狀態的同步，但是這個檔案的部分我是希望它是有版本的。那第三個其實就是一個蠻重要的，就是在這種多 agent 系統或是多服務的這種系統裡面很重要的一個 MQ，因為我們可以快速把一個訊息傳到另外一個部分，然後它收到就可以立刻來做一些傳遞。

### Slack + Google Drive + GitHub

那所以我目前的使用方式其實很簡單，就是我使用 Google Drive 當做相關的檔案的同步，然後用 GitHub Private 來做一些個人知識庫的同步，以及一些需要控管、需要它的 revision 的方式。那剩下的這些 MQ 的部分，我現在使用的是 Slack。那 Slack 其實最近才重新使用的，但是發現它在多 agent 之間傳遞狀況跟同步來說非常好用。

所以在這三個很簡單，而且目前來說除了 Google Drive，其他都是免費的方案來做，其實我個人覺得非常好用。那我也可以把那麼多的東西慢慢都串聯在一起，能夠變成一個更大的 ecosystem。

### 人的能力 = 指揮調度多少 agent

這或許就是人家說的，現在人的能力其實不是你自己有多強的能力，而是你能夠一次指揮調度多少 agent 的相關能力。

那之前大家的做法都會是用一些 dashboard，一個統一 dashboard 來控管這東西。但我的做法當然就是，第一個事情是我不期待有一個統一 dashboard 來做這件事情，但是我至少要能夠把那麼多的雲端、地端、在我的個人電腦，或是像 Grok Bot 這種不在個人電腦的 agent 都串聯在一起，然後彼此用最高性價比方式來做驅動。我希望這個做法目前來說看起來是 work，而且我希望它也能夠持續 work。

### 給 Astra 一台專屬電腦、雲地分工

那在第三段的時候我們就注意到了，就是我們現在看到的情況下，如果有像 Astra 這樣子的一個產品的話，我們是不是要給它一個比較專屬的、獨立的電腦，讓 Astra 一個分身就直接來接管你的電腦，做很多相關的事情。那我現在也的確用一台電腦來做 Astra 一些獨立的相關事情，目前看起來也蠻好用的。

然後再來就是雲跟地這邊要怎麼樣來做一個分工，什麼時候誰做什麼樣事情會比較好一點，這個也是目前挑戰的一個重點。那像是在雲上面的話，當然我做很多公開資料的搜尋，或是像是有一些客戶的東西，像是 Teams 或是 Google Chat 或是 Line 這邊傳過來訊息，那都能夠透過雲上面的一些 agent、Bot 來做事。那地端的話它就可以連接比較 private 的一些網路，以及一些比較重要的系統的串接，那這邊用地端來做串接就會很不錯。

那當然地端還有很多，像它能夠使用 open-weight 的模型然後做更多的事情，或是像我現在可以開始開了一個所謂的 AI 影片工廠，然後就是晚上之後就來看看要怎麼樣去生產這些有趣的影片，然後增加所謂的相關產能。

### 不只效率，能不能開創新 business？

所以我看這整件事情的最大的點就是，它的確能夠更有效地去組織我的工作，然後能夠讓我的產出能夠增加。但我現在在追求的點，除了不只是效率的增加，而且最重要的事情，它能不能夠幫助我開創新的路線、開創新的——你可以說 business。

所以這個我也在看說它能不能幫我把，如果就我自己的自媒體的事業來說，它能不能幫我把 X 的相關渠道打開，然後並且它能夠幫助我把 AI 影音的部分打開。這是我目前正在探索跟思考的。至於平常的文字、一些演講或是一些東西，它們已經做得很好了，那持續加油跟改進。

所以這個也是我在看的，就是說如何能夠管理好那麼多不同平台的 agent，然後能夠讓它變成統一到能夠為我所用的系統，並且它能夠給我創造新的 business，這個是目前來說最重要的相關議題。

### Anthropic 蒸餾報告與地端 AI 的未來

那這裡就是我目前看到的議題。當然還有很多重要議題，像是 Anthropic 它在昨天給出來的一個很重要的就是中國這邊相關模型廠的一些蒸餾的報告。這個的話我會等到時間比較久一點，大家塵埃比較落定的時候再跟大家來做評論，因為裡面牽涉的東西有點太嚴重太複雜。這個其實老實說我們需要更加理性地去看這件事情，所以我就暫時不講了。

但從那個報告裡面也看出，就是在地端的 AI 部署它的重要性會比以往更加的重要。這可能也會是對大家帶來一個很重要的影響。我在猜有這個東西出來之後，企業會更加不相信雲端的 API，而更加花時間去投資在地端的 AI，這個可能會是一個比較大的影響。

所以這大概是我今天要講的東西。最後這裡有一個我這段今天要講的東西然後做的一個 AI 的影片，還在持續的進步當中，但是我希望它能夠越做越好。謝謝。

---

## 延伸閱讀

- [多 Agent 架構：Slack 當 MQ、Google Drive 當檔案儲存、GitHub 當狀態與版本](/multi-agent-infra-slack-mq-drive-storage-github-state/)
- [Grok Bot：xAI 用 30 美金賣你一台 150 美金的 VM，還附 AI 員工](/grok-bot-persistent-agent-cloud-computer-cost/)
- [OpenAI 暫停 $200 Pro 新訂閱：Astra 需求炸鍋](/openai-pro-pause-astra-demand-20x-comparison/)
- [Anthropic 威脅情報：你以為在用 Kimi，其實在用 Claude](/anthropic-threat-report-kimi-deepseek-silent-relay/)
