---
layout: post
title: "6/5 雙重事故：Claude 疑似跨租戶洩漏 + OpenAI 大規模誤封，AI 基礎設施的信任危機"
date: 2026-06-08 05:41:35 +0800
permalink: /claude-anthropic-cross-tenant-incident-openai-ban-june-2026/
image: /assets/images/claude-cross-tenant-incident-2026.png
description: "2026 年 6 月 5 日，Claude 和 OpenAI 在同一天出事。Claude 的 API 在宕機期間疑似把 A 用戶的推理輸出塞給了 B 用戶——如果屬實，這是雲端架構最致命的跨租戶隔離失效。OpenAI 則因為系統故障大規模誤封付費帳號，30-40 個 Codex agent 的開發者一夜之間失去所有客戶收入。這篇從 Anthropic 官方時間線、cside 的技術根因分析、到 OpenAI 2023 年 Redis 前科，拆解共享快取架構下資料外洩給其他用戶的結構性風險。"
---

2026 年 6 月 5 日，一個星期五。

Claude 全線服務——API、Claude Code、Claude.ai、Claude Cowork——同時掛了。五個模型，從 Opus 4.5 到 4.8，加上 Sonnet 4.6，無一幸免。

宕機本身不是新聞。每家雲端服務都會宕機。

但開發者社群在 X 上開始流傳的截圖，讓這次事件的性質完全不同：有人打開自己的 Claude 介面，看到的不是自己的對話，而是一段正在生成哥倫比亞運動科普文章的陌生任務。另一邊，用戶的 prompt 框上方寫著「從 Amazon US 拉取完整 ASIN 列表並清理」——這跟他自己在做的事情毫無關係。

你發出去的請求，拿回的可能是陌生人的對話。你輸入的內容，此刻或許正顯示在另一個人的螢幕上。

同一天，OpenAI 也出事了。大量用戶帳號被系統「誤封」，三年心血、三四十個 Codex agent、所有客戶收入——一夜之間全部鎖住，沒有任何理由。

兩家公司，同一天，不同的事故模式，指向同一個結構性問題。


## Anthropic 6/5 事件：時間線

先看 Anthropic Status Page 的官方記錄：

| 時間 (UTC) | 事件 |
|-----------|------|
| 15:08 | 異常開始，錯誤率飆升 |
| 15:19 | 開始調查 |
| 15:25 | Opus 4.6 恢復 |
| 15:43 | 確認問題，Opus 4.7 和 4.8 仍受影響 |
| 16:23 | Sonnet 4.6 恢復 |
| 16:59 | Opus 4.8 恢復 |
| 17:12 | Opus 4.7 恢復 |
| 17:29 | Opus 4.5 恢復 |
| 18:28 | 事件完全解決 |

從 15:08 到 18:28，超過三小時。五個模型依序恢復，最後一個恢復的是 Opus 4.5——反而是最舊的模型拖到最後。

這個恢復順序本身就透露了一些架構資訊：不同模型跑在不同的基礎設施上，而且恢復不是一鍵全切回來的，是逐一修復。


## 「別人的推理輸出」：跨租戶隔離的最壞場景

宕機期間，開發者 Moritz Wallawitsch 在 X 上分享了一張朋友傳給他的截圖：Claude 介面上顯示的內容，是一篇關於「Tejo — The Explosive Outdoor Sport of Colombia」的文章草稿，完整的標題、段落結構、用詞——這跟原本用戶在做的事情完全不搭。

X 上的知名帳號 Chubby (@kimmonismus) 直接點名了：

> Reports claim Claude's API may have returned **another user's inference output** during today's outage. Anthropic's status page confirms elevated errors affecting Claude API, Claude Code, Claude.ai and Claude Cowork but Anthropic has not confirmed a customer data leak yet. **That would be a cross-tenant isolation failure and would be a worst-case scenario.**

跨租戶隔離失效（cross-tenant isolation failure）。這個詞在雲端安全領域的份量，等同於最高級別的客戶資料洩露災難。

用日常語言說：你家的門鎖失靈了，不只是小偷能進來——隔壁鄰居也能進來。


## Anthropic 的「沉默」

截至發稿，Anthropic 的官方態度是：

> "We haven't seen any other reports or evidence of customer data being leaked but take any reports of this very seriously and are investigating."

Status Page 上始終只有一句輕描淡寫的「elevated errors（錯誤率升高）」。

一邊是開發者言之鑿鑿的「我收到了別人的資料」，一邊是官方四個字的「錯誤率升高」。這中間的巨大落差，就是讓全球開發者焦慮的原因。

安全博客 cside 在事發當天發布了技術分析，標題直接寫明：「When an AI API returns someone else's response: shared caches and cross-tenant leaks」。作者表示已經看到流傳的截圖和第一手報告，但出於對洩漏資料本身的保護，選擇不公開展示——因為那些截圖裡包含的正是不該被傳播的其他客戶的 prompt 和輸出。


## 技術根因：共享快取的結構性風險

cside 的分析切中了核心問題。

現代 AI API 不是「一個程序回答一個請求」的簡單模型。它是一個由負載均衡器、請求路由器、閘道、佇列、記憶體快取、連接池等多層共享元件堆疊而成的龐大系統。所有這些元件同時為每一個客戶服務，目的是維持低延遲和低成本。

每一層都持有某種狀態。每一層都是一個可能把 A 用戶的回應塞給 B 用戶的「潛在事故點」——一旦快取鍵碰撞、連接被錯誤復用、或取消的請求留下了過期物件，跨租戶洩漏就會發生。

cside 文章中的這段總結值得每個用 AI API 的開發者讀三遍：

> 症狀幾乎總是相同的：你請求自己的資料，卻收到了別人的資料。原因也幾乎總是很普通：在重用某個共享物件時出現了一個小錯誤，通常由負載壓力或某些邊界情況（例如請求被取消或超時）所觸發。

而且，擴張越快的供應商，運行的共享層越多，推過去的負載也越大——暴露在這類 bug 下的面積就越廣。團隊為了應對需求不斷加層：更多快取來降低 token 成本、更多路由來分散區域負載、更多代理和閘道來管理配額和故障切換。每多一層，就多一個 cross-tenant bleed 的潛在節點。


## 前科：OpenAI 2023 年的 Redis 事件

這不是第一次了。

2023 年 3 月 20 日，OpenAI 經歷過一次幾乎一模一樣的事故。部分 ChatGPT 用戶能看到其他活躍用戶的聊天標題，甚至新建對話的第一條消息。

更嚴重的是，約 1.2% 的 ChatGPT Plus 付費用戶的部分帳單資訊被洩露——包括姓名、帳單地址、信用卡類型、過期時間和卡號後四位。

OpenAI 事後在復盤報告中確認：根本原因是共享快取和連接層在請求取消後，將資料返回給了錯誤的客戶端。具體來說，是一次伺服器變更導致 Redis 取消請求激增，觸發了 redis-py 客戶端函式庫的一個 bug。

同樣的故障類型，同樣的症狀模式。


## 同日事故：OpenAI 6/5 大規模誤封

巧合的是，同樣在 6 月 5 日，OpenAI 自己也出了事——只不過是不同類型的事故。

一次系統故障導致大量用戶帳號被「誤封」，ChatGPT、Codex 等服務的部分用戶突然被暫停訪問。

OpenAI 在 X 上官方承認：

> An issue caused some user accounts to be incorrectly suspended. We're restoring access and working through related subscription and credit issues.

時間線：

| 時間 (PT) | 事件 |
|-----------|------|
| 1:26 PM | 開始調查 |
| 2:20 PM | 確定根因，開始修復 |
| 2:52 PM | 修復實施中 |
| 3:19 PM | 確認部分帳號被錯誤暫停 |
| 4:09 PM | 基本恢復 |
| 7:09 PM | 帳號訪問恢復 |
| 次日 6:16 AM | 事件完全解決 |

帳號訪問恢復後，訂閱狀態、Pro 功能和積分問題仍在「善後」中。付費用戶的怒火在社交平台上迅速蔓延。

有 Reddit 網友憤怒地吐槽：

> 我付款後的第二天，OpenAI 就封禁了我的帳號。三年的心血、三四十個 Codex 智能體、我所有的客戶收入——全都被鎖住了。而且沒有給出任何理由。我是家裡唯一的經濟支柱。有人遇到過這種情況嗎？

這則貼文觸動了很多開發者的神經。三年的工作、數十個 agent、所有客戶關係——一個系統 bug 就全部凍結，連個理由都不給。

更新：OpenAI 客服 (Louise) 後來回覆確認該案例已被記錄，提交給審查團隊，要求等待進一步通知。到隔天早上，被誤封的用戶已恢復訪問並收到 email 通知。


## 結構性問題：當「快」成為唯一 KPI

把兩起事件放在一起看，有一個共同的結構性問題：**擴張速度和安全品質之間的張力**。

Claude 的跨租戶疑慮，技術上來自共享基礎設施在高負載下的邊界條件 bug。但為什麼會有這麼多共享層？因為要同時服務數百萬請求，又要維持低延遲和低成本。每多一層快取、每多一個連接池，就是在效能和隔離之間做取捨。

OpenAI 的誤封，背後是自動化帳號管理系統的邏輯錯誤。大規模用戶管理需要自動化，但自動化的 blast radius（爆炸半徑）也被放大了——一個 bug 影響的不是一個用戶，而是成千上萬個。

兩件事的共同模式：**速度 > 安全**。


## 對企業用戶的啟示

如果你在企業環境中使用 AI API——不管是 Claude、OpenAI、還是其他供應商——這次事件有四個具體的行動建議：

**1. 不要送不能承受曝光的資料**

cside 的建議很直接：「Do not send data to an LLM API that you could not tolerate surfacing elsewhere, unless your contract and the provider's controls genuinely cover it.」

如果你的資料一旦被別人看到會造成法律或商業損失，那在送進 API 之前，先問自己：合約和供應商的控制措施真的覆蓋了這個場景嗎？

**2. 把 API 回應當作不可信輸入**

驗證每個回應的 shape、type 和合理性，就像你驗證任何來自外部的不可信輸入一樣。如果回應的內容跟你的 prompt 完全不搭，你的系統應該能偵測到，而不是默默接受然後把它塞進用戶的記錄。

**3. 記錄足夠的 metadata**

如果你從來不存 request 和 response 的 metadata，你就無法區分「model 回了一個爛答案」和「這根本不是我的回應」。這兩種情況的嚴重程度完全不同，但如果沒有日誌，你連分辨的能力都沒有。

**4. 建立多供應商降級機制**

Thoughtworks 在事後分析中指出，很多組織對 AI 的依賴程度已經到了「資料庫和雲端供應商」的等級，但對應的容災措施遠遠不足。「AI tools should amplify engineers' capabilities. It shouldn't act as a structural crutch.」

當你的開發速度、客服系統、資料管線都綁在一個 AI 供應商上，一次宕機的代價不是「等幾小時」，而是整個業務停擺。


## 坦白說

我自己也是 Claude Code 的重度使用者。6 月 5 日那天我也被影響了。

寫這篇文章的時候，我在想一個問題：作為一個幫客戶導入 AI 工具的顧問，我有沒有認真跟客戶討論過「如果你用的 AI 服務把你的資料送給了別人怎麼辦」這個場景？

坦白講，在這次事件之前，我討論的重點一直是 [prompt injection](prompt-injection-harness-engineering-tool-using-agents.md)、[proxy relay 攻擊](llm-proxy-relay-security-your-agent-is-mine-ucsb.md)、[harness 的七條安全實踐](harness-engineering-security-best-practices.md)——這些都是「怎麼防止 AI agent 被攻擊或搞破壞」的問題。

但跨租戶隔離失效是一個完全不同的維度：這不是攻擊者的問題，這是供應商的基礎設施本身的問題。你做了所有正確的安全措施，你的 harness 設計得無懈可擊，但供應商的一個共享快取 bug 就能把你的資料塞給別人——這是你無法在客戶端防禦的。

這次事件之後，我的客戶諮詢清單要加一條：**你送進 API 的每一筆資料，假設它有可能被別人看到，你的業務能承受嗎？**

跨租戶洩漏的技術真相，還有待 Anthropic 給出正式結論。

但有一件事已經可以確定——很多開發者第一次認真地問自己：我交給 AI 的東西，真的只有我自己看得到嗎？


## 延伸閱讀

- [cside: When an AI API returns someone else's response](https://cside.com/blog/ai-api-shared-cache-data-leaks) — 事發當天最詳細的技術根因分析
- [Anthropic Status Page: June 5 Incident](https://status.claude.com/) — 官方事件記錄
- [OpenAI Status: Account Suspension Incident](https://status.openai.com/incidents/01KTBZDS20E3PZ53DH2SCKXN49) — OpenAI 誤封事件記錄
- [Thoughtworks: Claude Outage June 2026](https://www.thoughtworks.com/en-ec/insights/blog/generative-ai/claude-outage-june-2026) — 企業 AI 基礎設施韌性分析
- [Cybersecurity News: Anthropic's Claude Services Down](https://cybersecuritynews.com/anthropics-claude-services-down/) — 事件綜合報導
