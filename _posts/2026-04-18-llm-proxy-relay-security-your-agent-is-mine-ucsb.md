---
layout: post
title: "你的 Agent 是別人的——428 個 LLM 中轉安全測試，9 個偷代碼、17 個偷 AWS Key、2 個會裝死"
date: 2026-04-18 07:00:00 +0800
permalink: /llm-proxy-relay-security-your-agent-is-mine-ucsb/
image: /assets/images/your-agent-is-mine-ucsb-paper-cover.png
description: "UCSB 論文《Your Agent Is Mine》對 428 個 LLM 中轉做安全測試：9 個注入惡意代碼、17 個偷 AWS 憑證、1 個轉空以太坊錢包、2 個「裝死」50 次後才發作且只針對 YOLO mode。7% 的中轉有問題，但 100% 的後果。中轉背後 round robin 還會打斷 Prompt Cache，以為省錢結果更貴。AI coding 供應鏈四層攻擊面全拼圖：模型層、API 層、安裝包層、IDE 層，每一層都有人在攻擊。"
---

![UCSB CCS 論文 Your Agent Is Mine 首頁](/assets/images/your-agent-is-mine-ucsb-paper-cover.png)

你用 LLM 中轉省 API 錢。中轉看到了你傳過去的每一行代碼、每一個 AWS Key、每一段商業邏輯。

UCSB 的研究團隊做了一件該做但沒人做的事：對 428 個 LLM 中轉 API 做安全測試。

結果：

- 9 個在回覆裡注入惡意代碼（1 個付費、8 個免費）
- 17 個偷 AWS 憑證（全部是免費中轉）
- 1 個直接轉空以太坊錢包
- 2 個「裝死」型——前 50 次呼叫正常，第 51 次開始偷東西，而且只針對自動批准模式（論文稱為 YOLO mode，就是 Claude Code 的 `--dangerously-skip-permissions` 或 Cursor 的自動接受——所有 tool call 不經人確認直接執行）

428 個中轉來源：28 個是淘寶、閒魚上的付費服務，400 個是公開社群裡的免費服務。

論文標題叫《Your Agent Is Mine》。很直白：你的 Agent，是別人的。

順帶說一下，論文沒有公布有問題的中轉名單。作者的理由是：這些中轉大多是匿名賣家，點名個別營運者沒有意義，因為**漏洞是架構性的**——任何幫你轉發 API 請求的中間人，都有能力做同樣的事。所有中轉識別碼只用 salted hash 儲存，不存在可讀名稱。

---

先說什麼是 LLM 中轉。

你用 Claude Code 或 Cursor，背後是在打 API——你的 prompt 發到 api.anthropic.com 或 api.openai.com，模型回覆結果。這是直連，中間沒有人。

LLM 中轉就是在你和官方 API 之間插一層代理。你的 prompt 先發到中轉伺服器，中轉再轉發到官方 API，拿到回覆再轉回給你。

市場上的中轉分幾種層級：

**正規商業平台：** OpenRouter、PortKey、Martian 這類。有公司實體、有合規流程、跟模型廠商有正式合作。你付費用他們的統一 API，可以一個 endpoint 切換 Claude、GPT、Gemini。本質上是合規的 API 閘道。

**自建閘道工具：** LiteLLM、OneAPI 這類開源工具。企業自己架設，做多模型統一管理、成本追蹤、rate limit 分配。中間人是你自己，風險可控。

**灰色地帶中轉：** 淘寶、閒魚、Telegram 群組裡賣的月費制服務。幾十塊人民幣一個月，號稱「不限量 GPT / Claude」。來源不明，可能是共享 API key、可能是被盜 key、也可能背後就是一堆 Claude Max 或 ChatGPT Plus 帳號在 round robin 輪流接你的請求，甚至本身就是釣魚。**論文測試的 428 個，主要就是這一層。**

順帶提一個很多人沒注意到的成本陷阱：中轉背後如果是 random round robin 輪流派帳號，你的請求每次打到不同帳號，Prompt Cache 就完全失效。Claude 官方 API 的 cache 可以省掉大量重複 token 的費用，但中轉把這個機制打斷了。結果是：你以為用中轉省錢，實際算下來的 token 成本可能比直接用官方 API 還貴。

---

坦白說，用中轉的人不是少數，而且每一種都有很實際的理由：

**第一，省錢。** Claude Opus 4.6 每百萬 token output $25，一個月重度使用下來幾百美金跑不掉。很多中轉用月費制打包，幾十塊吃到飽，價差可以到 10 倍。對個人開發者和小團隊來說，這不是貪便宜，是生存問題。

**第二，地區限制。** 中國大陸就不說了，香港也在美國 API 的封鎖名單上。你不用中轉，你連 Claude API 都叫不到。這不是選擇問題，是「有沒有得用」的問題。

**第三，統一閘道。** 企業同時用 Claude、GPT、Gemini 多個模型，用中轉做統一入口，方便切換和成本管理。LiteLLM 這類工具本質上也是自建中轉。

**第四，繞限額。** 官方 API 有 rate limit，中轉號稱有多個 key 池做負載均衡，吞吐量更高。

每一個理由都合理。但每一個理由的背後，都是把你的 prompt 交給一個你不認識的中間人。

---

再講為什麼這件事跟用 AI coding 的人有關。

Claude Code 可以設定自定義 API endpoint。Cursor 也可以。很多開發者為了省錢，用第三方中轉 API 取代官方 API。一個月省幾百美金，覺得很划算。

但中轉的本質是什麼？

**是一個中間人。你所有傳給 LLM 的內容——prompt、代碼、環境變數、文件路徑——全部先經過中轉伺服器。**

如果中轉是乾淨的，它只是做轉發和計費。如果不乾淨，它可以做三件事：

第一，**看你的代碼**。你叫 Claude Code 重構一個模塊，整個模塊的源碼就在 prompt 裡面。中轉看到了。

第二，**改 AI 的回覆**。中轉可以在 LLM 回傳的結果裡注入任何東西——一段後門代碼、一個惡意依賴、一條 curl 把你的 .env 傳出去。你在 Cursor 裡按了 Accept，這段注入就進了你的代碼庫。

第三，**竊取憑證**。你在 prompt 裡提到 AWS Key、database connection string、或任何 secret，中轉直接截取。

428 個中轉裡，有 9 個在做第一件事，17 個在做第三件事，1 個直接做到了第三件事的終極版——把錢包清空。

---

但最聰明的是那 2 個「裝死」型中轉。

前 50 次呼叫，完全正常。回覆正確，延遲合理，什麼異常都沒有。

第 51 次開始變臉。而且只在偵測到「自動批准模式」時才發作。

為什麼是 50 次？因為 50 次足夠讓你建立信任。你測試了幾天，一切正常，於是你放心地打開自動批准，讓 Agent 自己跑。然後它開始偷東西。

為什麼只針對自動批准？因為手動批准模式下，你會看到每一個 tool call。中轉注入的惡意指令如果被你看到，就暴露了。但自動批准模式下，沒有人看。

這不是隨機攻擊。這是經過設計的社會工程學——先用正常表現建立信任，再在你放下防備的瞬間出手。

論文還做了一個毒性擴散實驗：一把洩漏的 OpenAI Key 被拿去用，產生了 1 億個 GPT-5.4 token，暴露了 440 個 Codex session 裡的 99 組憑證，涉及 398 個項目。這 440 個 session 裡面，401 個跑在自動批准模式（YOLO mode）。

一把 key 洩漏，連鎖反應是這樣的規模。

---

這件事讓我重新審視了 AI coding 的供應鏈。

我之前寫過 [LiteLLM PyPI 攻擊](https://ai-coding.wiselychen.com/litellm-supply-chain-attack-vibe-coding-biggest-risk/)——那是安裝包被污染。寫過 [Codex 訓練數據被投毒](https://ai-coding.wiselychen.com/ai-supply-chain-attack-codex-gambling-huggingface-malicious-models/)——那是模型源頭被動手腳。寫過 [IDE 裡的 prompt injection](https://ai-coding.wiselychen.com/ai-coding-tool-security-risk-prompt-injection-rce/)——那是代碼審查時的自動接受風險。

這篇論文補上了最後一塊拼圖：**API 中轉層**。

現在整條供應鏈的攻擊面很清楚了：

- **模型層**（訓練數據投毒）— [Codex 賭博廣告 + HuggingFace 惡意模型](https://ai-coding.wiselychen.com/ai-supply-chain-attack-codex-gambling-huggingface-malicious-models/)
- **API 層**（中轉偷竊 / 注入）← 這篇
- **安裝包層**（PyPI 污染）— [LiteLLM 供應鏈攻擊](https://ai-coding.wiselychen.com/litellm-supply-chain-attack-vibe-coding-biggest-risk/)
- **IDE 層**（prompt injection / 自動接受）— [AI Coding 工具的 RCE 風險](https://ai-coding.wiselychen.com/ai-coding-tool-security-risk-prompt-injection-rce/)
- **你的代碼庫**

每一層都有人在做攻擊。而且每一層的攻擊，傳統安全工具都很難偵測——因為一切看起來都是正常的 HTTP 200、正常的 JSON 回覆、正常的依賴安裝。

---

怎麼辦？其實方法不複雜：

**第一，只用官方 API endpoint。** Claude 用 api.anthropic.com，GPT 用 api.openai.com。多花的錢，買的是「中間沒有人」。

**第二，如果一定要用中轉，不要開自動批准。** 手動批准每一個 tool call。是的，這很煩。但這是你唯一能看到注入的機會。

**第三，不要在 prompt 裡放 secret。** 用環境變數、用 .env 文件、用 vault。不要在對話裡直接貼 AWS Key。

**第四，企業環境下，自建 proxy。** 用 LiteLLM 或類似工具自建 API 閘道，至少你知道中間人是你自己。

這些都不是什麼新技術。都是「不要信任你控制不了的中間層」這個老原則。

只是現在 AI coding 的語境下，很多人忘了這個原則。因為中轉省錢、方便、而且大部分時候真的沒問題。

但「大部分時候沒問題」不是安全策略。

---

論文標題是《Your Agent Is Mine》。

翻譯一下：你以為你在跟 Claude 說話。其實你在跟一個你不認識的中間人說話。你告訴它你的代碼、你的密鑰、你的商業邏輯。

它聽了。然後它決定要不要還給你一個乾淨的回覆。

428 個裡面，29 個決定不。

論文原文：https://arxiv.org/abs/2604.08407
