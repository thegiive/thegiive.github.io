---
layout: post
title: "YouTube 雙集逐字稿：你的 Claude 越用越笨 ＋ LLM 中轉在偷你的東西"
date: 2026-04-19 07:00:00 +0800
permalink: /youtube-ep-cloud-degradation-proxy-security-transcript/
image: /assets/images/youtube-claude-degrade-airport-thumbnail.jpg
description: "YouTube Shorts 雙集聯動逐字稿。EP1 從機場候機室講 Claude 越用越笨的真實體感——新模型上線舊模型降智是產業共識，企業必須投資地端 GPU 做雲地混合架構。EP2 從陽明山講 UCSB 論文《Your Agent Is Mine》——428 個 LLM 中轉實測，29 個在偷你的東西，最聰明的裝死 50 次才發作。兩集底層邏輯一樣：不要把所有賭注壓在你控制不了的基礎設施上。"
---

**作者：** Wisely Chen
**日期：** 2026 年 4 月
**系列：** AI Coding 實戰觀察 — YouTube Shorts 逐字稿
**關鍵字：** LLM 降智, Claude Opus, 地端 GPU, 雲地混合架構, LLM 中轉, API 安全, Your Agent Is Mine, YOLO mode, 供應鏈攻擊

---

## 這兩集在講什麼

這是我的 YouTube Shorts 雙集聯動。第一集從機場候機室分享「Claude 越用越笨」的真實體感，推導出企業為什麼現在必須投資地端 GPU。第二集從陽明山分享 UCSB 論文《Your Agent Is Mine》的實測結果——428 個 LLM 中轉，29 個在偷你的東西。

兩集看起來講不同主題，但底層邏輯是同一件事：**你把所有賭注壓在你控制不了的基礎設施上，遲早會出事。**

降智是「品質不在你手上」。中轉是「安全不在你手上」。解法都一樣：把關鍵的東西拿回自己手裡。

---

## EP1：你的 Claude 越用越笨，不是你的錯覺

**長度：** 7 分 10 秒
**場景：** 機場候機室

{% include youtube.html id="PtWyndLBHuU" %}

### ⏱️ 時間戳

- 0:00 機場候機室開場
- 0:14 Claude Opus 4.7 上線後為什麼感覺越來越不穩
- 0:34 「新模型上線、舊模型降智」是雲端 LLM 的產業共識
- 0:59 Token 經濟快要變成水電瓦斯
- 1:30 如果 Claude / Hermes Agent 這類數位員工突然變笨，企業會多痛
- 2:02 解法：雲地混合架構（大部分雲端＋關鍵用地端）
- 2:50 雲端斷線 / 降智時，如何 fallback 回地端
- 3:16 為什麼現在要搶地端 GPU：買都買不到
- 4:14 Agent 需求指數成長，GPU 供應線性成長
- 5:12 雲地混合是企業 IT 架構的未來
- 5:38 從 disk、GPU、電力到 DC 都要投資
- 6:08 MiniMax M2、GLM 5.0 已經能處理 99% 企業 workload
- 7:00 結論：必須投資在地端

### 逐字稿（根據影片內容重建）

大家好，我現在在機場候機室。趁等飛機的時間跟大家聊一件最近很多人在問的事。

Claude Opus 4.7 上線那個禮拜，你是不是覺得舊的模型突然變笨了？

這不是你的錯覺。

每次新模型上線，舊模型「降智」——這件事已經變成雲端 LLM 生意的產業共識了。不是只有 Anthropic，OpenAI 也一樣。社群裡面一直在說，論壇一直在討論，甚至有人開始用數據追蹤了。

為什麼這件事很嚴重？因為 Token 經濟已經快要變成水電瓦斯了。

你想想看，現在企業用 AI coding 的場景，Claude Code、Cursor、Copilot，這些工具每天在消耗大量的 token。如果你的團隊已經把 AI 當成生產力工具，甚至把 Hermes Agent 這種東西當數位員工在用——突然有一天模型變笨了，你的數位員工就等於集體降薪。

不是降薪，是降智。你付一樣的錢，拿到更差的品質。

而且你連通知都收不到。沒有 changelog，沒有 email，就是突然覺得不對勁。

怎麼辦？

我的建議是雲地混合架構。大部分 workload 繼續跑雲端，沒問題。但關鍵的、機敏的、不能斷的——你要有地端。

地端的意思是：你自己的 GPU server，跑你自己控制的模型。雲端降智的時候，你可以 fallback 回來。雲端斷線的時候，你不會停擺。

但這邊有一個很現實的問題：GPU 你現在買都買不到。

NVIDIA H100、H200，交期動輒半年。企業級 GPU server 的供應鏈，從晶片到散熱到機房電力，全部都在搶。你不是今天決定要買地端就明天拿得到的。

而且 Agent 的需求是指數型成長。每一個 Agent 跑一次任務，消耗的 token 量是人類手動操作的 10 到 100 倍。但 GPU 算力的供應是線性成長。這個缺口只會越來越大。

所以我說雲地混合不是「未來趨勢」，是「現在就要開始投資」。

從 disk、GPU、電力到 data center，這些基礎建設不是你今天下單明天就有的。你要現在就開始規劃。

好消息是，地端模型的能力已經追上來了。MiniMax M2、GLM 5.0 這些開源模型，已經可以處理 99% 的企業日常 workload。不需要每個任務都用 Opus。80% 的任務用地端開源模型就夠了，剩下 20% 才需要雲端的頂級模型。

結論就一句話：你必須現在就開始投資地端。再晚，你連 GPU 都搶不到。

---

## EP2：428 個 LLM 中轉，29 個在偷你的東西

![YouTube Shorts EP2：428 個 LLM 中轉，29 個在偷你的東西——陽明山](/assets/images/youtube-llm-proxy-security-thumbnail.jpg)

**長度：** 5 分 30 秒
**場景：** 陽明山

{% include youtube.html id="lzyjZ2WpJgQ" %}

### ⏱️ 時間戳

- 0:00 陽明山開場
- 0:14 LLM 中轉服務到底是什麼
- 1:16 為什麼大家還是在用（省錢、統一 gateway、繞地區限制）
- 2:22 428 個中轉實測，7% 有問題
- 3:08 最聰明的攻擊：裝死 50 次 + YOLO mode
- 4:10 三個避險方法

### 逐字稿（根據影片內容重建）

大家好，我現在在陽明山。今天要講一件跟你口袋裡的錢和你代碼裡的 secret 都有關的事。

你用月費制 LLM 中轉省 API 錢。但你有沒有想過，中轉看到了你傳過去的每一行代碼、每一個 AWS Key、每一段商業邏輯？

UCSB 剛發了一篇論文叫《Your Agent Is Mine》。他們對 428 個 LLM 中轉 API 做了安全測試。

先講什麼是中轉。你用 Claude Code 或 Cursor，背後是在打 API。你的 prompt 直接發到 api.anthropic.com，這是直連，中間沒有人。

中轉就是在你和官方 API 之間插一層代理。你的 prompt 先到中轉伺服器，中轉再轉發給官方。

市場上分三種。第一種，正規平台，OpenRouter、PortKey 這些，有公司實體、有合規。第二種，自建工具，LiteLLM、OneAPI，企業自己架的。第三種，灰色中轉——淘寶、閒魚、Telegram 群組，幾十塊人民幣月費，號稱不限量。論文測的 428 個，主要就是第三種。

為什麼大家還是在用？每個理由都很實際。

省錢。Opus 4.6 每百萬 token 25 美金，中轉月費制幾十塊吃到飽，價差 10 倍。

地區限制。中國大陸不說了，香港也被封鎖。不用中轉，你連 API 都叫不到。

統一 gateway。企業同時用好幾個模型，中轉做統一入口方便切換。

結果呢？428 個裡面，29 個有問題。7% 的機率。

9 個在回覆裡注入惡意代碼。17 個偷 AWS 憑證。1 個直接轉空以太坊錢包。

但最聰明的是那 2 個「裝死」型。

前 50 次完全正常。第 51 次開始偷東西。而且只在偵測到 YOLO mode 才發作。YOLO mode 就是自動批准模式，Claude Code 裡面 --dangerously-skip-permissions，或者 Cursor 的自動接受。

為什麼？50 次夠你建立信任。你測試了幾天，一切正常，就放心打開自動批准。然後它出手。

手動模式下你會看到每一個 tool call，注入會被你發現。YOLO mode 下沒人看。

這是社會工程學，不是隨機攻擊。

怎麼辦？三件事。

第一，盡量只用官方 API endpoint。多花的錢，買的是「中間沒有人」。

第二，如果一定要用中轉，絕對不要開 YOLO mode。手動批准是你唯一能看到注入的機會。

第三，不要在 prompt 裡放 secret。用環境變數、用 vault。

都是老原則：不要信任你控制不了的中間層。只是在 AI coding 的語境下，很多人忘了。

---

## 兩集的共同底層邏輯

| 維度 | EP1：降智風險 | EP2：中轉安全 |
|------|-------------|-------------|
| 核心問題 | 品質不在你手上 | 安全不在你手上 |
| 誰在控制 | 雲端廠商（隨時切版本） | 中轉營運者（隨時偷竊 / 注入） |
| 你收到通知嗎 | 沒有 | 沒有 |
| 解法 | 地端 GPU ＋ 開源模型 | 官方 API ＋ 自建 proxy |
| 共同原則 | **把關鍵的東西拿回自己手裡** | **不要信任你控制不了的中間層** |

這兩集放在一起看，就是 2026 年企業用 AI 的兩條紅線：

1. **品質紅線：** 你的 AI 工具隨時可能降智，你需要地端 fallback
2. **安全紅線：** 你的 API 請求隨時可能被截取，你需要可信任的通道

兩條線的解法都指向同一個方向：**投資你自己控制的基礎設施**。

---

## 延伸閱讀

- [LLM 亂降智不是都市傳說——StupidMeter 監控與企業 IT 該怎麼辦](https://ai-coding.wiselychen.com/llm-silent-degradation-enterprise-it-harm-stupidmeter-monitoring/)
- [LLM 中轉安全測試：Your Agent Is Mine 完整分析](https://ai-coding.wiselychen.com/llm-proxy-relay-security-your-agent-is-mine-ucsb/)
- [Local LLM 企業架構](https://ai-coding.wiselychen.com/local-llm-enterprise-architecture/)
- 論文原文：https://arxiv.org/abs/2604.08407
