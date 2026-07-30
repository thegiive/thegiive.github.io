---
layout: post
title: "最強編程 Agent 不是一個 Agent——用 Codex 驅動 ChatGPT Pro，拆開「寫」和「驗」"
date: 2026-07-29 09:00:00 +0800
permalink: /codex-chatgpt-pro-dual-agent-workflow/
description: "目前用過最穩、代碼品質最高的編程工作流，不是任何單一 Agent，而是兩個 AI 組成的小團隊：Codex 當 PM、Tech Lead 和 QA，ChatGPT Pro（GPT-5.6 Sol Pro）當高級程序員。起因是我們發現 ChatGPT Pro 網頁版的編程品質有時候比 Claude 5 還好，而且不吃 Codex 的 token 額度。於是問了一個問題：有沒有辦法讓 Codex 自己去用 ChatGPT Pro？這篇拆解完整工作流、附上可直接使用的 prompt，以及一個網路環境的重要陷阱。"
image: /assets/images/codex-chatgpt-pro-dual-agent-browser.webp
categories: [Vibe Coding]
author: Wisely Chen
---

我們後來發現一件事：ChatGPT Pro 的網頁版，在 coding 這塊做得又好又完整。

不只是「堪用」。有些複雜的工程任務，它出來的代碼品質甚至比 Claude 5（之前的 Claude 5，不是現在的 Fable 5）更好。架構更乾淨、邊界條件考慮更完整、不容易出現那種「看起來對但跑起來爆」的半成品。

再加上一個很實際的好處：**ChatGPT Pro 網頁版的對話不會吃掉 Codex 的 token 額度。** 它們用的是不同的用量池。Pro 會員的一般對話額度官方描述是 unlimited（受 abuse guardrails 約束），而 Codex 的 agentic 用量是另一個有上限的池子。

所以我就在想：**有沒有一個更簡單的做法？**

以前用 ChatGPT Pro 寫代碼很麻煩——你得自己整理源碼、上傳文件、解釋需求、等結果出來再把代碼拿回去、應用補丁、跑測試。出了問題還得自己當傳話人，把錯誤訊息搬回 ChatGPT Pro。整套流程裡，人類是最慢的那個環節。

但 2026 年 4 月，Codex 升級了內建瀏覽器和多任務能力。我看到這個功能的時候，第一反應是：**等一下，Codex 可以幫我操作 ChatGPT Pro。**

![Codex 左側對話 + 右側內建瀏覽器開著 ChatGPT Pro：雙代理工作流實際畫面](/assets/images/codex-chatgpt-pro-dual-agent-browser.webp)

---

## 新做法：讓 Codex 使用 ChatGPT Pro

我不再親自使用 ChatGPT Pro。我讓 Codex 使用 ChatGPT Pro。

- **Codex** 負責：理解需求、檢查倉庫、拆解任務、準備源碼、打開多個 ChatGPT Pro 對話、追問和糾錯、把代碼拿回本地、跑完整測試、直到通過驗收。
- **ChatGPT Pro** 負責：深入研究、設計方案、寫代碼。

分工邏輯：orchestrator 和 executor 徹底分開。寫代碼的不負責驗證，驗證的不負責寫代碼。

這解決了兩個問題。第一，**人類不再當中間人。** 以前那些整理源碼、複製貼上、搬運錯誤訊息的苦工，全部由 Codex 自動化。第二，更重要的——**寫和驗被拆到了不同的 AI 身上。**

目前主流的 coding agent，不管是 Codex 還是 Claude Code，都有一個結構性問題：同一個 Agent 同時負責寫代碼和證明自己寫得對。這跟讓同一個人既當球員又當裁判是一樣的問題。現在，ChatGPT Pro 只管寫，Codex 只管驗，兩個 AI 互相制衡。

---

## 為什麼 ChatGPT Pro 網頁版的編程品質比 Codex 高

這是一個沒有官方答案但值得拆解的問題。我的研判有兩個方向：

**第一，算力分配。** Codex 要同時服務大量用戶的 agentic 任務——每個任務都涉及多輪推理、工具呼叫、檔案讀寫。這對後端算力的消耗遠高於一般對話。相比之下，ChatGPT Pro 網頁版的對話場景相對單純，每次請求分配到的推理算力可能更充裕。同一個底層模型，給它更多的 compute budget 去思考，出來的結果自然不一樣。

**第二，harness 不同。** Codex 背後的 harness 是為了「自主完成整個工程任務」設計的——它要管理檔案系統、跑測試、處理 git、協調多步驟。這套 harness 本身會佔用 context window，也會影響模型的注意力分配。而 ChatGPT Pro 網頁版的 harness 更簡單：一問一答，全部 context 都花在思考你的問題上。少了 harness 的開銷，模型有更多空間做深度推理。

這兩點目前都是推測，OpenAI 沒有公開 Codex 和 ChatGPT Pro 的算力分配差異或 harness 架構細節。但從使用體驗來看，這套解釋是合理的：**同一家的模型，在不同產品裡跑出不同品質，通常不是模型的問題，是基礎設施和工程架構的問題。**

而且這個分工模式，恰好吻合我之前在 [AgentOpt 論文拆解](https://ai-coding.wiselychen.com/agentopt-expensive-model-wrong-position-pipeline-optimization/) 裡提到的核心發現：**Planning 用小模型，複雜任務用大模型。** Codex 在這套工作流裡扮演的角色——串接、拆任務、跑測試、追問糾錯——全部是 orchestration 性質的工作，需要的是反應快、tool use 穩定，不需要深度推理。這些正好適合算力較低但速度快的模型來做。而真正需要深度思考的複雜編程——架構設計、大量代碼生成、邊界條件處理——交給算力充裕的 ChatGPT Pro。

Columbia 大學 AgentOpt 的實驗結果是：Ministral 8B 當 Planner + Opus 當 Solver，準確率 74.27%；反過來 Opus 當 Planner 只有 31%。這套 Codex + ChatGPT Pro 的工作流，本質上就是同一個邏輯的實踐版：**讓快的歸快的、深的歸深的，不要讓一個模型兩邊都扛。**

---

## GPT-5.6 Sol Pro：幾個關鍵事實

ChatGPT 的「Pro」模式底層是 GPT-5.6 Sol Pro——GPT-5.6 家族中最高能力的變體，只存在於 ChatGPT 網頁版，Pro 會員專用。

| 項目 | 說明 |
|------|------|
| 模型 | GPT-5.6 Sol Pro（ChatGPT Pro picker 專用） |
| 取得方式 | 僅 ChatGPT 網頁版 Pro 模式 |
| GPT-5.6 Sol benchmark | Artificial Analysis Coding Agent Index 80 分，比 Fable 5 高 2.8 分 |
| 用量計算 | ChatGPT 一般對話與 Codex agentic 用量分開計算 |
| 與 Sol 的差異 | OpenAI 描述為 highest-capability variant；Sol Pro 是否為 Sol 的獨立變體，官方沒有明確說明 |

注意：上表的 80 分 benchmark 是 GPT-5.6 Sol 的成績，不是 Sol Pro 的。Sol Pro 沒有公開獨立 benchmark。「Sol Pro 比 Sol 更強」是基於使用體驗的判斷，不是 benchmark 驗證的結論。

---

## 實際跑了一整天：幾個值得注意的細節

用這套方法跑了一整天，幾個觀察：

**Codex 自己決定拆任務。** 我給了一個比較大的任務，Codex 判斷太大，自己拆成 3 個獨立子任務，開了 3 個 ChatGPT Pro tab 分別處理。這不是我安排的，是它自己的決定。

**溝通量很大。** Codex 和 ChatGPT Pro 之間來回溝通接近 20 輪。如果這些溝通要我自己手動搬運，光是複製貼上就夠累了。

**驗收是 Codex 本地完成的。** Codex 收到 ChatGPT Pro 交付的全部代碼後，自己在本地跑驗收：門禁、端到端測試、文檔總結。這是這套工作流最關鍵的一環——寫代碼的 AI 和驗收代碼的 AI 是不同的 AI。

---

## 這跟 Anthropic 的雙 Agent 架構差在哪

我之前寫過 [Anthropic 官方解密 Claude Code 的雙 Agent 架構](https://ai-coding.wiselychen.com/anthropic-dual-agent-architecture-claude-code/)。Anthropic 的做法是 Initializer Agent（負責規劃、建功能清單）+ Coding Agent（逐一實作、Puppeteer 驗證）。

兩套方案都是雙代理，但切法不一樣：

| | Anthropic 雙 Agent | Codex + ChatGPT Pro |
|--|---------------------|---------------------|
| **切分依據** | Planning vs Execution | Orchestration + Verification vs Deep Coding |
| **同一供應商** | 是（都是 Claude） | 否（OpenAI Codex + OpenAI ChatGPT Pro，但不同產品線） |
| **驗收方** | Coding Agent 自我驗證 | Codex 獨立驗證（與寫代碼的不是同一個 Agent） |
| **最大差異** | 寫和驗仍在同一個 Agent | 寫和驗徹底分開 |

Anthropic 的架構解決了長時任務的上下文繼承問題。Codex + ChatGPT Pro 解決的是另一個問題：**消除自我驗證的偏見**。

這跟前面提到的 [AgentOpt 論文](https://ai-coding.wiselychen.com/agentopt-expensive-model-wrong-position-pipeline-optimization/) 結論一致：Codex 不是最強的 coding model，但它當 orchestrator 恰好合適——它不會搶著自己寫，而是老老實實把任務交給 ChatGPT Pro。

---

## 完整 Prompt（可直接使用）

以下是我用的完整 prompt。在 Codex 對話裡直接貼上，把最後的需求和驗收標準填上就能用。

> 我已經在 Codex 內置瀏覽器中登錄了 ChatGPT Pro。
>
> 這次採用雙代理協作：
> - ChatGPT Pro 是外部高級工程師，負責深入研究、方案設計和編寫代碼。
> - 你（Codex）是總負責人，負責理解需求、檢查倉庫、準備源碼、向 ChatGPT Pro 分配任務、監控進度、追問糾錯、落地代碼並獨立驗收。
> - ChatGPT Pro 的結論不能直接視為正確，最終是否合格由你根據源碼、測試結果和驗收標準判斷。
>
> 請按以下規則自主完成整個過程：
>
> 1. 先閱讀倉庫中的 AGENTS.md、CLAUDE.md、README、package.json 和相關架構文檔，了解項目約束、運行環境及必跑門禁。
> 2. 檢查當前分支、Git 狀態和源碼基線。不要覆蓋或丟失現有改動。
> 3. 將本次需要的源碼安全打包成 ZIP：
>    - 默認包含當前任務需要的源碼；
>    - 排除 .git、node_modules、構建產物、緩存、資料庫、運行狀態和瀏覽器狀態；
>    - 不得包含 .env、API Key、Token、私鑰、Cookie 或其他憑據；
>    - 上傳前進行密鑰掃描，並記錄源碼 commit、壓縮包大小和 SHA-256。
> 4. 不要假設 ChatGPT Pro 可以訪問本地文件、私有倉庫或內部環境。所有必要代碼和上下文都要通過壓縮包及任務說明提供。
> 5. 把我的需求整理成詳細、專業、可驗收的工程任務再發送給 ChatGPT Pro，至少包含：
>    - 背景和目標；
>    - 當前架構及不可破壞的邊界；
>    - 需要研究和修改的範圍；
>    - 明確交付物；
>    - 必須執行的測試；
>    - 禁止執行或禁止聲稱的操作；
>    - 驗收標準。
> 6. 如果包含多個相互獨立的複雜任務，為每個任務建立單獨的 ChatGPT Pro 對話，避免上下文互相污染。
> 7. ChatGPT Pro 可能需要很長時間。不要因為運行時間長就催促、打斷或重複發送任務。只有在經過合理等待、連續檢查仍沒有進展時，才檢查頁面、重新打開對話或要求它從最後完成的位置繼續。
> 8. 保存每個 ChatGPT Pro 對話的鏈接。遇到頁面刷新、上下文截斷或連接中斷時，自主恢復任務，不要讓我處理中間技術問題。
> 9. ChatGPT Pro 交付後，你必須獨立驗收：
>    - 檢查報告、補丁、源碼和附件是否完整；
>    - 核對版本、官方文檔和源碼結論；
>    - 驗證文件大小及 SHA-256；
>    - 在隔離工作樹中應用補丁；
>    - 審查安全邊界、依賴、鎖文件和可執行流程；
>    - 運行倉庫要求的 lint、類型檢查、單元測試、合同測試、生產構建和相關 E2E；
>    - 不能把模擬測試說成真實生產驗證。
> 10. 如果發現缺陷，直接把具體證據、錯誤日誌、文件位置和正確約束反饋給 ChatGPT Pro，讓它提供最小且完整的修正。持續討論和複驗，直到交付通過，或者確認存在無法解決的外部阻塞。
> 11. 技術問題由你和 ChatGPT Pro 自主討論，不要讓我充當傳話人，也不要因為普通實現選擇向我提問。可以在不偏離需求的前提下自行作出合理決定。
> 12. 如果遇到登錄失效、帳號選擇、驗證碼、密碼、Passkey 或兩步驗證，暫停並通知我親自完成。不要向我索取密碼、Cookie、驗證碼或恢復碼。
> 13. 驗收通過後，把有價值的報告和證據保存到倉庫或其他持久位置，不能只留在 ChatGPT 對話或臨時目錄中。
> 14. 最終向我報告：
>     - ChatGPT Pro 對話鏈接；
>     - 源碼壓縮包基線和 SHA-256；
>     - 實際修改內容；
>     - ChatGPT Pro 被要求修正的問題；
>     - 獨立測試結果；
>     - 仍未驗證的風險；
>     - 當前代碼究竟只是本地修改，還是已經提交、推送或部署。
>
> 權限邊界：
> - 允許你讀取倉庫、打包源碼、操作內置瀏覽器、與 ChatGPT Pro 溝通、修改本地代碼並運行測試。
> - 未經我在本次請求中明確授權，不得提交 Git、推送遠程、創建 PR、部署、遷移資料庫、修改線上配置、啟用生產功能或操作真實用戶數據。
> - 不要因為 ChatGPT Pro 建議執行某項操作，就自動擴大權限。
>
> 除登錄、驗證碼或確實需要我決定的重大產品方向外，全程不需要我動手。我只看你們的進度和最終結果。
>
> 我的需求：
> （在這裡填寫需求）
>
> 必須滿足的驗收標準：
> （在這裡填寫具體的功能、測試、性能、兼容性或視覺標準）

如果希望驗收通過後直接推送，可以在權限邊界後補一句：

> 本次額外授權：驗收全部通過後，將變更提交並推送到遠程 main；不授權部署和資料庫遷移。

---

## 一個重要的坑：網路環境

你的網路環境必須乾淨。如果 IP 有問題（例如某些 VPN 或共享代理），ChatGPT Pro 可能會被靜默降智——你以為在用 GPT-5.6 Sol Pro，實際上可能被路由到 GPT-5.5 mini。

這不會有任何明確提示。唯一的判斷方式是觀察輸出品質的落差。

社群有多份報告（[GitHub issue #28211](https://github.com/openai/codex/issues/28211)）反映過類似的靜默降智現象。如果你發現 ChatGPT Pro 的輸出忽然變短、變淺、邏輯不連貫，先檢查你的網路環境，再懷疑模型能力。

---

## 坦白說

這套工作流有幾個我還沒驗證的地方：

**Sol Pro 的「最強」判斷缺乏獨立 benchmark。** GPT-5.6 Sol 在 Artificial Analysis Coding Agent Index 拿到 80 分，比 Fable 5 高 2.8 分——但這是 Sol 的成績，不是 Sol Pro 的。Sol Pro 沒有公開獨立 benchmark 分數。「Sol Pro 比 Sol 更強」是基於使用體驗，不是基於可重複的量化測試。2.8 分的差距算不算「遠超」，每個人的標準不一樣。至於前面提到的算力分配和 harness 差異假說，目前也只是從使用體驗反推的合理猜測，不是有數據支撐的結論。

**「不消耗 Codex 額度」的精確機制需要更多確認。** 從 OpenAI 的用量文檔來看，ChatGPT 一般對話和 Codex agentic 用量走不同的池子，邏輯上 Codex 操作瀏覽器去聊 ChatGPT 消耗的是對話池、不是 Codex 池。但 Codex 操作瀏覽器本身的 compute 是否消耗 Codex 額度，這一點我沒有找到明確的官方聲明。

**前端和審美類任務不適用。** 這套流程的優勢在後端、架構設計、複雜邏輯——需要深度思考和大量代碼的場景。涉及 CSS、視覺微調、動畫細節的工作，ChatGPT Pro 在網頁版裡沒有預覽能力，不如直接用有 preview 的工具。

**Codex 自動拆任務的行為不一定穩定。** 我這次遇到 Codex 自動拆成 3 個 tab 的情況，但不保證每次都會這樣。這取決於任務的大小和 Codex 當時的判斷。

---

## 關鍵洞察

**「寫」和「驗」的分離，是這套工作流最核心的設計。** 以前我們讓同一個 Agent 同時寫代碼和證明自己寫得對。這就像讓學生自己批改自己的考卷——不是不能做，但你很難信任結果。現在把寫交給 ChatGPT Pro、驗收交給 Codex，兩個 AI 互相制衡。

**這個模式呼應了 AgentOpt 的發現：orchestrator 不需要是最強的模型。** Codex 的強項不是寫出最好的代碼，而是理解需求、拆解任務、操作工具、跑測試。這些恰好是 orchestrator 需要的能力。讓最強 coding model 做它最擅長的事（深度思考和寫代碼），讓擅長工具操作的 Agent 做驗收和協調。

**如果你有 ChatGPT Pro 會員，嘗試門檻很低。** 把上面的 prompt 貼進 Codex、在內建瀏覽器登入 ChatGPT Pro，填上需求和驗收標準，讓它們跑。第一次可以從一個中等複雜度的後端任務開始，觀察 Codex 怎麼跟 ChatGPT Pro 溝通、怎麼驗收。

---

## 參考資料

- OpenAI, *GPT-5.6 in ChatGPT* — [help.openai.com](https://help.openai.com/en/articles/20001354-gpt-56-in-chatgpt)
- OpenAI, *GPT-5.6: Frontier intelligence that scales with your ambition* — [openai.com/index/gpt-5-6](https://openai.com/index/gpt-5-6/)
- OpenAI, *Using Codex with your ChatGPT plan* — [help.openai.com](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan)
- Anthropic, *Effective harnesses for long-running agents* — [anthropic.com/engineering](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- 延伸閱讀：[Anthropic 官方解密：為什麼 Claude Code 這麼好用？](https://ai-coding.wiselychen.com/anthropic-dual-agent-architecture-claude-code/)
- 延伸閱讀：[「Opus 太聰明，所以它不該做 Planning」——AgentOpt 論文拆解](https://ai-coding.wiselychen.com/agentopt-expensive-model-wrong-position-pipeline-optimization/)

---

## 常見問題 Q&A

**Q: 這套方法跟直接用 Codex 寫代碼比，什麼時候值得用？**

任務複雜度高、需要深度思考和大量代碼的時候。簡單的 bug fix、小功能、快速原型，直接用 Codex 或 Claude Code 就好，不需要多一層間接。這套方法的建置成本是：你要先在 Codex 內建瀏覽器登入 ChatGPT Pro，然後貼一段比較長的 prompt。如果任務本身 10 分鐘就能搞定，這個建置成本不值得。

**Q: 一定要用 ChatGPT Pro 嗎？能不能讓 Codex 去操作 Claude？**

理論上，只要 Codex 的內建瀏覽器能操作的網頁 AI，都可以套用這個模式。Claude 的網頁版也可以。但 ChatGPT Pro（Sol Pro）的優勢是 Pro 會員有接近無限的對話額度，而且 Sol Pro 在複雜編程任務上的品質目前確實是第一梯隊。用其他模型也行，但你要自己評估品質和額度的取捨。

**Q: 安全性？把源碼上傳到 ChatGPT Pro 有風險嗎？**

prompt 裡已經包含了安全規則：打包前排除 .env、API Key、Token、私鑰等憑據，上傳前進行密鑰掃描。但如果你的項目有嚴格的代碼保密要求，把源碼上傳到任何第三方 AI 服務都需要經過合規審查。這不是這套工作流特有的風險，而是所有雲端 AI 編程工具的共同議題。
