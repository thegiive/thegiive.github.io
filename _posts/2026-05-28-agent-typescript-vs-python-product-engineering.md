---
layout: post
title: "Agent 專案該用 TypeScript 還是 Python？答案早就寫在 GitHub 數據裡"
date: 2026-05-28 09:00:00 +0800
permalink: /agent-typescript-vs-python-product-engineering/
image: /assets/images/agent-ts-vs-python-slide-09.png
description: "做 Agent 到底用 TypeScript 還是 Python？這題在推特吵翻，但 GitHub Octoverse 2025 已經給答案：TypeScript 年增 66%、十年來最大語言移動，超車 Python 與 JavaScript。這篇從一位頂尖 Agent 團隊朋友的觀點出發，拆三個技術理由（型別打穿全端、JSON 滿天飛的事件流、系統工程母語），再帶到 AI 時代的語言「馬太效應」，以及 OpenAI 把 Codex 從 TS 重寫成 Rust 的反例——最後給出 TypeScript / Python / Rust 三語言的分層決策矩陣。"
---

![AI Agent 時代的語言之爭：語言的馬太效應，bash、TypeScript、Python 站在 AI 加速的贏家一方](/assets/images/agent-ts-vs-python-slide-09.png)

這兩天推特上有一題吵得很兇：做 Agent 專案，到底要不要用 Python。

網路上有人講得很狠——「SB 才在 Agent 專案裡用 Python」。

我一個頂尖 Agent 圈的朋友，話沒這麼衝，但立場差不多——「TypeScript 是我首選語言。」

這句話很難聽，第一反應大概都是想反駁：Python 不是 AI 的母語嗎？LangChain、LlamaIndex、一堆論文的 reference implementation 不都是 Python？怎麼會「SB 才用」？

先別急。這句話的措辭很糟，但它指向的那個轉折，其實是對的。真正的問題從來不是「哪個語言比較強」，而是一個更難堪、也更務實的問題：

**你做的 Agent，是研究工程，還是產品工程？**

![研究工程 vs 產品工程的分水嶺：研究工程主導語言是 Python，產品工程主導語言是 TypeScript](/assets/images/agent-ts-vs-python-slide-02.png)


## 先看數據：TypeScript 已經悄悄超車 Python 了

很多人對「AI = Python」的印象還停在 2023 年。但 GitHub 2025 年的 Octoverse 報告，給了一個讓人意外的數字：

**TypeScript 在 2025 年超車 JavaScript 和 Python，成為 GitHub 上使用量第一的語言。年增 66%，是十年來最大的單一語言移動。**

![GitHub Octoverse 2025：TypeScript 年增 66%，超車 JavaScript 與 Python 成為使用量第一的語言](/assets/images/agent-ts-vs-python-slide-03.png)

注意，不是「成長最快的前幾名之一」這種模糊話，是「十年來最大的一次語言版圖移動」。

為什麼？GitHub 的解釋很關鍵，他們稱之為 **AI feedback loop（AI 回饋循環）**：

> 「靜態型別語言給你護欄。如果 AI 工具要幫我生成程式碼，我會想要一個快速的方法去判斷這段程式碼對不對。」

> 「AI 模型在那些會暴露正確性資訊的語言上（例如型別系統）表現得更好。」

換句話說，AI 寫程式這件事，本身就在把整個產業往型別語言推。模型看過一兆份 TypeScript 範例、只看過幾千份某冷門語言，它當然在 TypeScript 上更準；越準越多人用、越多人用模型訓練得越好——這是一個自我強化的循環。

語言選擇，正在變成一個「AI 相容性」的決策。

![AI 回饋循環：型別當護欄、模型更聰明、開發者靠攏，三者互相強化的自我循環](/assets/images/agent-ts-vs-python-slide-04.png)

順帶一提同一份報告還有個彩蛋：Bash 在 AI 生成專案裡年增 206%——這又是另一篇文章的故事（Agent 在大量寫 shell 來操作系統）。

數據擺在前面，我把那位朋友講的東西整理成三個技術理由。你會發現它們不是個人偏好，而是和這個大趨勢完全一致。

## 理由一：Agent 最後幾乎都會進產品，而產品離 TS 更近

Agent 最終會長在哪裡？Chat 介面、工作流面板、瀏覽器插件、Copilot、IDE 擴充、Slack / Discord / 網頁工具。

這些東西，TS 天然就離得近。前端是 TS，後端也可以是 TS，中間的 tool schema、事件流、UI 狀態，**全部共用一套型別**。

如果你用 Python，你的架構很容易變成這樣：

- 模型服務在 Python
- 後端在 Node
- 前端在 TS

於是同一份 tool schema 你要複製三份。然後某天有人把一個欄位的大小寫改錯了——`userId` 寫成 `userid`——三份裡只改了兩份。

接下來會發生什麼？你的 Agent 馬上死給你看。而且這種錯不會在編譯時被抓到，它會在 demo 給客戶看的那一刻，安靜地把錯誤的參數丟給工具，然後整條 pipeline 歪掉。

一套型別打穿全端，和一份 schema 維護三份——這個差距在原型階段感覺不出來，在產品階段會要你的命。

![傳統架構維護三份 schema 的死亡陷阱（userId vs userid 大小寫錯誤）vs 現代 Agent 架構一套型別貫穿全端](/assets/images/agent-ts-vs-python-slide-05.png)

## 理由二：Agent 的工程本質——滿天飛的 JSON 加長鏈路事件流，正好是 TS 的主場

進了產品之後，Agent 在工程上到底長什麼樣子？兩個特徵：一是**大量 JSON 物件在到處飛**，二是它不是「一問一答」，而是**長鏈路的事件流**。這兩件事，剛好都是 TS / Node 的主場。

![Agent 的本質：滿天飛的 JSON 物件加上長鏈路事件流，告別一問一答，是 event-driven 的主場](/assets/images/agent-ts-vs-python-slide-06.png)

先講事件流。Agent 不是「一次請求、一次回答」這麼簡單——它要邊想邊輸出（streaming）、邊調用工具、邊等使用者確認、邊更新 UI、邊處理取消、重試、超時、恢復。這是一個典型的事件驅動、長連線、串流的場景。TS / Node 在 event-driven、stream、WebSocket、Server-Sent Events 這些場景裡非常順——因為 Node 整個 runtime 從第一天就是為這種非阻塞 I/O 長出來的。Python 當然也能做（asyncio、FastAPI 的 streaming 都有），但你會更容易感覺到一件事：**這東西本來不是為這種 Web 產品的長鏈路長出來的。**

再講型別，這點我覺得是最被低估的。很多人以為 Agent 不穩，是因為「模型不夠聰明、不會說話」。錯。Agent 在生產環境真正容易炸的地方是：

- tool input / output 結構錯
- agent state 的欄位錯
- message format 變形
- context 物件被某一步悄悄改壞
- 外部 API 回傳的結構跟你以為的不一樣

TS 可以把這些東西在編譯期就卡住：tool input/output、agent state、message format、UI event、workflow node、permission object、external API response——全部都能上型別。這不是潔癖，是在一個「JSON 滿天飛」的系統裡，把一整類 bug 提前擋掉。Python 的 type hint + Pydantic 也能做到不少（這點要公道講，PydanticAI 就是靠這個），但 TS 的型別是強制的、是編譯期的、是和前端共用的——強度和覆蓋範圍不是一個量級。

![隱形的護欄：TS 把致命錯誤擋在編譯期，涵蓋 tool I/O、agent state、message format、context 物件、外部 API 回傳結構](/assets/images/agent-ts-vs-python-slide-07.png)

## 理由三：從單一應用到 runtime，AI 拼的是系統工程，而系統工程的母語是 TS

把鏡頭拉遠看整個產業，就會看到第三件事。

如果你做的不是單一 Agent 應用，而是一個 Agent 框架、SDK、runtime、插件系統——那 TS 的優勢會放大。因為你的使用者，會想把它接進：網頁、後台服務、Electron、瀏覽器插件、VS Code 插件、API route、serverless、edge runtime。這些地方 TS 生態最統一。一個 Python 寫的 runtime，你要怎麼塞進一個 VS Code 插件、或跑在 Cloudflare 的 edge runtime 上？很痛。

看一下 2026 的框架版圖就懂了——做 Agent infra 的，幾乎都選了 TS：

- **Claude Agent SDK**（原 Claude Code SDK）：Anthropic 第一方的 Agent 框架，TS。
- **Vercel AI SDK 6**：加入原生 agent 抽象，月下載量 20M+，直接把這個量級推進 agent 領域。
- **Mastra**：22,000+ GitHub stars、weekly npm 下載 300k+，生產用戶包含 PayPal、Replit。15 個月做到這個量。
- **LangGraph**：跑在 Klarna、Uber、Elastic 的生產環境。

這些團隊選 TS，不是因為 Python 不行，是因為他們要服務的對象——Web 開發者和產品團隊——本來就活在 TS 的世界裡。

![2026 年頂尖 Agent Infra 的一致選擇：Claude Agent SDK、Vercel AI SDK 6、Mastra、LangGraph 都圍繞 Web 開發者](/assets/images/agent-ts-vs-python-slide-08.png)

而這指向一個更大的轉變。早期大家用 Python，是因為那時候 **AI = 模型**，工作主體就是調模型、跑實驗、處理資料，這些 Python 無敵。但現在的 AI 產品已經演化成一個完整的系統：LLM API、tool calling、database、vector store、browser automation、workflow、UI、billing、auth、analytics……這已經不是研究工程了，這是**產品工程**。而網際網路產品工程的主語，長期以來就是 JS/TS。

很無聊，但世界就是這麼沒品。不是因為 TS 多優雅，是因為產品工程的重心一旦從「模型」移到「系統」，戰場就換到了 Web 工程師的主場。

## AI 時代另一個更狠的差別：語言的「馬太效應」

那位朋友還丟了一個我覺得更值得想的觀察。

AI 寫程式這件事，正在製造一種語言的「贏者全拿」。

你去看現在的 AI——它特別會寫 bash、TS、Python。為什麼？因為訓練資料裡這幾個語言的量最大。而前面講的 feedback loop 會讓這件事滾雪球：AI 越會寫，越多人用 AI 寫，產出的程式碼又回頭餵養模型，這幾個語言「被 AI 加速」的幅度會大到很誇張。

但硬幣的另一面更殘酷：**AI 不熟的語言，會以 10 倍速被甩到腦後。**

不是它們突然變爛了，是它們的「AI 加速度」跟不上。當別人用 AI 一天做完，你還在手刻，差距不是線性拉開，是指數級拉開。

這個動態，其實跟自然語言一模一樣。英語慢慢獨大之後，很多小語種不是「慢慢」式微，是以驚人的速度被取代——因為資源、工具、內容全都往主流語言集中，邊緣語言連「被學習」的機會都在快速消失。

程式語言正在走上同一條路。差別只是這次的加速器叫 AI，不叫全球化。

所以「TS vs Python」這個問題，從這個角度看其實有點好笑——因為 **bash、TS、Python 三個都站在贏的那一邊**。它們都是 AI 最熟、被加速最猛的語言。真正被甩開的，是那些不在這份名單上的語言。

所以與其問「TS 還是 Python」，不如問「在我的這一層，誰被 AI 加速得最猛」。

不過講到這裡，有人會從完全相反的方向，丟出一個很漂亮的反例。

## 那反過來呢？有人說 AI 時代正是 Rust 的機會

這個反駁很有道理，邏輯是這樣：既然 code 反正都是 AI 在寫，那 Rust「難寫、學習曲線陡」這個最大的缺點，不就被 AI 抵消掉了嗎？人寫起來的成本一旦降下來，你就可以放心去拿 Rust 真正的好處——**極低的 resource 消耗**。

這不是空談，有一個現成、而且很打臉的案例：**OpenAI 把 Codex CLI 從 TypeScript / Node 整個重寫成 Rust。**

對，就是那個跟 Claude Code 打對台的 Codex。它原本的技術棧是 React + TypeScript + Node，2025 下半年 OpenAI 把核心重寫成 Rust（codex-rs），到 2026 初，Rust 已經佔了大約 95% 的程式碼。

![AI 正在拆除 Rust 的天花板：OpenAI 把 Codex CLI 重寫成 Rust（95%），Agent 採用 Rust 換來極低記憶體、無 GC 停頓、單一 binary](/assets/images/agent-ts-vs-python-slide-10.png)

為什麼？因為一個 agentic CLI 的核心，就是一個「在迴圈裡不斷呼叫模型」的長時間執行 harness。而「長時間執行」正好戳中 Node 的兩個痛點：

- **記憶體**：跑幾個小時的 coding session 會不斷累積歷史、工具回傳、render 出來的 diff，Node 的 heap 就跟著無限長大。Codex 重寫後常駐記憶體約 80MB；Claude Code 在大專案上可以漲到好幾 GB。
- **GC 停頓**：Node 的垃圾回收會在你串流輸出到一半時插進來卡一下。Rust 沒有 runtime GC，記憶體配置是確定性的，不會中斷串流。

加上 Rust 編出來是單一 binary、零依賴安裝（不用先裝 Node v22+），冷啟動從「幾秒」變成「幾毫秒」——這在 CI 裡平行開幾十個 agent 的場景特別有感。

數字上 Codex 也不是隨便講講：Terminal-Bench 2.0 拿到 77.3%（Claude Code 65.4%），而且每個任務用的 token 大約只有 Claude Code 的三分之一到四分之一。

那為什麼 Claude Code 不跟進、繼續留在 TS？這就是有趣的地方——它賭的是另一邊：TS 帶來的工具彈性、session 中途改行為的靈活度。而且公道講，在「不知道是哪個工具生成」的盲測裡，Claude Code 的程式碼品質在 67% 的比較中被評為更好，Codex 只有 25%。

所以這不是「Rust 完勝」，是一個**清楚的取捨**：Codex 用 Rust 換 throughput 和長跑穩定性；Claude Code 用 TS 換彈性和品質。

![效能與彈性的取捨：OpenAI Codex（Rust）用於底層 runtime 與長跑 CLI，Claude Code（TS）用於跨前後端、頻繁修改、深度對接 UI 的產品](/assets/images/agent-ts-vs-python-slide-11.png)

但這個案例真正的價值，是它把前面「runtime 用 TS」那句話，逼出一個更精準的版本：

> 越往「性能關鍵、長時間執行、要塞進 CI / edge / 單一 binary」的底層 runtime 走，Rust 的優勢越大；越往「要跨前後端、要快速改、要接 UI 和產品」的上層走，TS 的優勢越大。

換句話說，AI 不只是在「加速既有的熱門語言」，它同時也在**降低你選用一個難語言的門檻**。Rust 過去的天花板是「人寫起來太痛」，而這個天花板，正在被 AI 拆掉。

## 坦白說：Python、TS、Rust 各守一塊

前面講得好像 TS 要一統江湖，但這裡必須踩煞車——把模型訓練、資料處理硬搬到 TS，是另一種形式的蠢。

公道話：

- **AI/ML 專案的建立數，目前仍然由 Python 主導。** GitHub 自己的數據也說了，TS 贏在「整體活躍度」，但 Python 在 AI/ML 專案的創建上還是龍頭。它們贏的是不同的戰場。
- TS 在 ML 生態、數值運算、複雜資料處理、研究迭代速度上，明顯比 Python 弱。你不會想用 TS 寫 embedding pipeline 或訓練腳本。
- 而且我再強調一次：**這篇不是我自己的生產實測數據**，是頂尖團隊朋友的觀點 + 公開數據的綜合。你的 team size、你的 stack、你的人是 Python 強還是 TS 強，都會改變答案。別把這當成教條。

所以真正合理的分工，從來不是「二選一」，而是分層——而且加上 Rust，其實是三種語言各守一塊：

| 層 | 該用 | 為什麼 |
|---|---|---|
| 產品層 / 前端互動 | **TS** | 離使用者最近，全端共用一套型別 |
| Agent 編排 / orchestrator | **TS** | 事件流、async、用型別卡住滿天飛的 JSON |
| 要嵌進 JS 宿主的 SDK / 插件（VS Code、edge、瀏覽器） | **TS** | 生態統一，貼著宿主環境 |
| 性能關鍵、長時間執行的 CLI / harness 核心 | **Rust** | 低記憶體、無 GC 停頓、單一 binary，長跑不爆 |
| 模型層 / 資料層 | **Python** | ML 生態無可取代 |
| eval / embedding / 離線任務 / 實驗腳本 | **Python** | 研究工程的主場 |

![AI 時代的語言分層矩陣：產品層/編排/SDK 用 TypeScript，底層 CLI/harness 核心用 Rust，模型層/離線任務用 Python](/assets/images/agent-ts-vs-python-slide-12.png)

## 一句話的決策法則

如果你要做一個 Agent 產品，比較務實的順序是：

**MVP 的前端 + Agent orchestrator 先用 TS 把產品跑起來。等真的涉及模型訓練、複雜資料處理、進階檢索、評測系統，再把 Python 接進來做那一層。**

![務實決策法則三階段：MVP 驗證期用全端 TS，深度智慧期引入 Python，效能瓶頸期才把底層 runtime 替換為 Rust](/assets/images/agent-ts-vs-python-slide-13.png)

「SB 才用 Python」這句話本身是錯的、也太狂。但如果把它翻譯成務實版本，它想講的其實是：

> 別再用做研究的思路去做產品。AI 應用早就不是「把模型包一層」，它是一個系統工程，而系統工程的母語是 TS。Python 留給它真正無可取代的那一層就好。

聊完這題，老實說，我也才意識到自己之前對 Agent 的認知有多停留在「模型時代」。把語言選擇當成 AI 相容性 + 系統工程的決策，而不是個人偏好之爭——這個視角的轉換，比結論本身更值錢。

## 常見問題 Q&A

**Q：我現在的 Agent 是純 Python，要全部重寫成 TS 嗎？**

不要。重寫成本極高，而且如果你的產品還在驗證階段，語言根本不是你的瓶頸。比較務實的做法是：下一個新增的、面向產品/前端的模組用 TS，讓型別在前後端之間共用；模型和資料那層維持 Python。先止血，不要大手術。

**Q：Python 的 Pydantic / PydanticAI 不是也能做型別嗎？為什麼還要 TS？**

能，而且做得不錯，這點要公道講。差別在於覆蓋範圍：TS 的型別是編譯期強制的，而且能和你的前端、API、UI 事件共用同一份定義。Pydantic 解決的是「Python 內部」的型別，TS 解決的是「整條產品鏈路」的型別。當你的 Agent 要進產品、要跨前後端時，後者的價值才會浮現。

**Q：那 LangChain、LlamaIndex 這些 Python 框架是不是要被淘汰了？**

不會。它們在「研究工程 / 快速原型 / 資料密集 pipeline」這個區間依然很強，而且 LangChain 也有 JS 版本。重點不是哪個框架死掉，而是 Agent infra 的重心（Claude Agent SDK、Vercel AI SDK、Mastra、LangGraph）明顯在往 TS 移動，因為它們要服務的是產品團隊，不是論文作者。

**Q：團隊裡只有 Python 工程師，怎麼辦？**

那就先用 Python 把產品做出來，這永遠比「為了用對語言而招不到人/做不出來」更重要。人的問題 > 技術問題。語言是優化項，不是前提。等產品驗證了、團隊長大了，再考慮在產品層引入 TS。

**Q：既然 Codex 用 Rust 又快又省，那我是不是該直接用 Rust 寫 Agent？**

除非你做的是「性能關鍵、要長時間跑、要塞進 CI / edge / 單一 binary」的底層 runtime 或 CLI harness（像 Codex 那種），不然多數 Agent 產品的瓶頸根本不在 runtime 的記憶體，而在開發速度和跨前後端的整合——那 TS 還是比較划算。Rust 的甜蜜點是「底層、長跑、性能敏感」這一塊；AI 讓它變得比以前好寫，但它不是預設選項，是你確定卡在性能時才往下換的那張牌。

![團隊實務痛點快問快答：純 Python 要不要重寫、Pydantic 夠不夠、只有 Python 工程師怎麼辦、該不該直接用 Rust](/assets/images/agent-ts-vs-python-slide-14.png)

---

**參考來源：**

- [TypeScript, Python, and the AI feedback loop changing software development — GitHub Octoverse](https://github.blog/news-insights/octoverse/typescript-python-and-the-ai-feedback-loop-changing-software-development/)
- [TypeScript vs Python for AI Agents: A Decision Framework — Blaxel](https://blaxel.ai/blog/typescript-vs-python-ai-agents)
- [The best open source frameworks for building AI agents in 2026 — Firecrawl](https://www.firecrawl.dev/blog/best-open-source-agent-frameworks)
- [Choosing an agent framework — Speakeasy](https://www.speakeasy.com/blog/ai-agent-framework-comparison)
- [Another Rust Rewrite: OpenAI's Codex CLI Goes Native, Drops Node and TypeScript for Rust — InfoQ](https://www.infoq.com/news/2025/06/codex-cli-rust-native-rewrite/)
- [AI CLI Tools Comparison: Why OpenAI Switched to Rust While Claude Code Stays with TypeScript — Mervin Praison](https://mer.vin/2025/12/ai-cli-tools-comparison-why-openai-switched-to-rust-while-claude-code-stays-with-typescript/)

