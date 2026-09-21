---
layout: post
title: "Astra 讓 Mac Mini 又要二轉了——Computer Use 把數位員工從 CLI 升級到 Desktop"
date: 2026-09-21 18:00:00 +0800
permalink: /astra-computer-use-mac-mini-dedicated-ai-desktop/
tags: [Astra, GPT-6, Computer Use, Browser Use, Mac Mini, Agent, macOS, 專機, Remote, 語音介面, OpenClaw, Codex]
categories: [AI Agent]
image: /assets/images/astra-computer-use-osworld-benchmark.png
description: "Astra 的 browser use 底層是 Playwright，可以背景跑；computer use 會接管桌面，跑在你的筆電上三十分鐘就受不了。已經有人在 headless Mac Mini 上跑 Astra computer use，從手機 Remote 下指令。我的 Mac Mini 跑 agent 自動化半年，全是 CLI。Astra 加進來之後，這台 599 美金的盒子從腳本機器變成了 GUI 操作員——browser use 背景跑、computer use 用專屬桌面、你的螢幕完全不被佔。"
author: Wisely Chen
---

我的 Mac Mini + OpenClaw 跑 agent 自動化已經半年了。

Wiki 每小時同步 GitHub、早上七點 Telegram 推 daily briefing、行事曆每小時掃一次、晚上九點整理會議紀錄。全是 CLI 指令和 API call，跑得很穩。

每個月我都會想加新任務。每個月都撞到同一面牆：那個任務需要 GUI。

幫我到某個網站後台填表單。幫我開 Keynote 改幾頁簡報。幫我到一個只有 web 介面的 SaaS 工具裡匯出報表。幫我在瀏覽器裡跑一套需要登入、點選、等待、再點選的流程。

CLI 有些時候做不了。API 很多時候根本不存在。

之前是用一些 computer use 的 model 來做，效果普通。然後 Astra 帶著新一代的 computer use 來了。

## Astra 的 computer use：社群怎麼說

Sam Altman 的說法是「human parity at computer use」。Benchmark 數字確實震撼——Mind2Web 速度快了 1.9 倍，ExploitBench 100%（雖然[獨立複製還沒到](https://x.com/hars_7086/status/2101756990942748737)）。

但 benchmark 歸 benchmark，我更在意的是真的拿來用的人怎麼說。

[Allie K. Miller](https://x.com/alliekmiller/status/2095595935002742975) 測完之後的結論：「pretty much any stable workflow done on a computer can be at least partially done by AI。」她直接問讀者：你能不能挑戰自己一整天不碰滑鼠？

[Machina](https://x.com/EXM7777/status/2096297561867116995) 實際拿來工作後說：「stupidly good at using the computer, this will open up insane workflows。」

最打動我的是 [rohit](https://x.com/rohit3a/status/2099817315118567767) 的貼文。他說本來這週要請一個實習生，把工作清單列好了。結果全丟給 Astra 的 computer use，幾乎全部完成。唯一卡的地方是登入驗證。

這不是 benchmark 數字，是有人真的省下了一個人力。

## 為什麼 Astra 的 Computer Use 這一代進步這麼多

Astra 這一代真正明顯的進步，不是在一般的 browser use，而是在 computer use。

以 OpenAI 公開的 OSWorld 2.0 為例，GPT-5.6 Sol 的分數是 65.7%，Astra 提升到 72.6%，增加 6.9 個百分點。代表 Computer Use 這個場景下有 73% 的成功率。更重要的是，模擬任務平均時間從約 75 分鐘降到 40 分鐘，快了接近一倍。搭配新版 Codex harness，Mind2Web 上的任務完成速度比 Sol 快 1.9 倍。

![OSWorld 2.0 準確性 vs API 成本：Astra 在相同成本下準確性明顯高於 Sol，且所用 Token 大幅減少](/images/astra-computer-use-osworld-benchmark.png)

這背後可能有一個很重要的基礎設施變化。

根據 The Information 的報導，OpenAI 在最近幾個月購買了數萬台 Mac mini 與 Mac Studio，用途包括 reinforcement learning，以及訓練能夠實際操作電腦的 computer-use agents。這不是 OpenAI 或 Apple 官方確認的採購數字，應該視為媒體報導，不是官方公告。

為什麼訓練 computer use 會需要這麼多真正的 Mac？

因為訓練這種模型和訓練純文字 LLM 很不一樣。LLM 預訓練主要需要大量 GPU 做矩陣運算；computer use 的強化學習，則需要 AI 不斷進入一個真正的作業系統：

看螢幕 → 判斷下一步 → 移動滑鼠或輸入鍵盤 → 觀察結果 → 再做下一個動作。

一個 agent 可能要反覆跑幾十、幾百步才能完成一個任務。要大量訓練，就需要同時開出大量獨立的桌面環境，讓 agent 不斷試錯。

數萬台 Mac 的意義不是「拿 Mac 來訓練 GPT-6 的基礎模型」，而更像是建立一座巨大的 **AI 電腦駕訓班**：同時讓大量 agent 練習操作 Safari、Finder、Office、網頁、視窗、表單與各種 GUI。

這很可能是 Astra computer use 能快速提升的重要條件之一。

但目前不能直接說「因為 OpenAI 買了數萬台 Mac，所以 Astra 才從 65.7% 升到 72.6%」。OpenAI 沒有公開這兩件事之間的因果關係，也沒有公布多少提升來自 Mac 訓練環境、模型本身、reinforcement learning、harness 或其他工程改善。

比較準確的說法是：OpenAI 正投入大量真實電腦環境來訓練 computer-use agents，而 Astra 同期在 computer use benchmark 上出現明顯提升。大量真實 GUI 環境，很可能是這波能力進步的重要基礎設施之一。

## 問題：你捨得讓出螢幕嗎

但這些人都碰到同一個問題。

Computer use 的意思是 AI 接管你的桌面。它在你的螢幕上打開瀏覽器、點選按鈕、填寫表單、切換視窗。做這些事的時候，你坐在那台電腦前面，什麼都不能做。

[Matt](https://x.com/mattsaltaccount/status/2100732963692376121) 的抱怨代表了很多人的心聲：「Waiting for background computer use next. I'd really like to stop having Astra suddenly take over my computer while I'm in the middle of something else。」

三十分鐘還行。一個小時開始煩。一整天？不可能。

這裡需要先釐清一件事：Astra 其實有兩種模式。

**Browser use** 的底層是 Playwright + accessibility tree。Browserbase 的 [Kyle Jeong](https://x.com/kylejeong/status/2098478826464702556) 逆向工程之後發現，它是 code-mode——不是對螢幕截圖然後點座標，而是直接操作 DOM。這意味著 browser use 可以在背景跑，不需要佔用你的螢幕。[Rhys](https://x.com/RhysSullivan/status/2098550367789445486) 的 PDF 拆解工作流就是「all running in the background」。

**Computer use** 則不同。它真的要操作桌面——移動滑鼠、按鍵盤、切換視窗。這需要一個活著的 GUI session。跑在你的主力機上，它就會搶你的螢幕。

所以問題不是「Astra 能不能在背景跑」，而是：**browser use 可以，computer use 需要一個專屬桌面。**

而這正好指向一個簡單的答案。

## 解法很簡單：給 AI 一台自己的電腦

想通之後答案很明顯。你不會讓實習生坐在你的位子上用你的電腦，你會給他一張自己的桌子。AI 也一樣。

一台專用機。AI 隨時操作它的桌面，你隨時在自己的電腦上工作。需要看它在幹嘛的時候，開 Screen Sharing 瞄一眼。不需要的時候，它自己跑。

已經有人這樣做了。[Duane](https://x.com/DuaneAdam/status/2100092822829609145) 說他在一台 headless Mac Mini 上跑 Astra computer use：「I already use Astra a lot on my headless CUA Mac mini and it is great. Yesterday I was automating some web browser tasks, and it was so much faster and cheaper than using Playwright。」

[Amos](https://x.com/Amos__Hadad/status/2098917896877437070) 更進一步——他用 Astra + Computer Use + Remote，從手機下指令，不再打開電腦。Email、行銷、加功能，全透過 Astra 操作他的桌面。他形容這個體驗：「瘋狂」。

那為什麼是 Mac Mini？

## 如果要跑 Astra Computer Use，選什麼系統

很有可能就是 Mac Mini。三個原因。

### 一、Mac 是 Agent 天堂

就算 Computer Use 理論上可以操縱鍵盤滑鼠、看畫面，但實際工作中假設 10 步，Computer Use 只佔那 10% 的關鍵卡點，90% 的步驟在 command line 下都能完成。

我在[〈AI Agent 的隱形天花板不是模型，是你的作業系統〉](/ai-agent-os-tax-windows-powershell-hidden-ceiling/)裡寫過：

**Agent 的真實能力 = 模型能力 x 執行環境的可駕馭度。**

macOS 的 Unix shell 讓那 90% 跑得最順。X 上半年內五條超過五萬瀏覽的推文都在講同一件事：Windows 的 PowerShell 讓 agent 反覆卡住、CMD 和 WSL 互相打架、輸入法彈窗干擾 computer use。而剩下那 10% 的 GUI 操作，macOS 的視窗系統和 Accessibility API 的成熟度，讓 computer use 的可預測性也最高。

用 Linux 可以嗎？CLI 部分沒問題，但 computer use 需要圖形桌面。Linux 的 GUI 環境碎片化（GNOME、KDE、Wayland、X11），agent 的訓練資料裡 macOS 和 Windows 的比例遠高於 Linux desktop。

### 二、Mac Mini 電費低、聲音小

這種大部分遠程操作、少數需要手動排除的電腦，你會希望放在身邊，但又不吵。M4 待機只有 3W，負載也才 25W 左右。月均電費大約 $3-5。

Mac Mini M4 16GB 官方定價 $599。攤五年等於 $10/月。加上電費，一個月不到 $15。對比 [Grok Bot](/grok-bot-persistent-agent-cloud-computer-cost/) 的 $30/月（同規格 GCP 租要 $100-150/月），三個月回本。

更關鍵的是資料主權。機器在你桌子底下，瀏覽器 session 和登入狀態全在你手上。不是存在某家公司的雲端 VM 裡——[Grok Bot 所有 Bot 共用一台電腦、一個瀏覽器 profile、一組登入](https://x.com/MAXdeg0/status/2090852404157637036)。

### 三、Mac 應該是 Astra 的老家

根據 The Information 的報導，OpenAI 買了數萬台 Mac 來訓練 computer-use agents。Astra 是在 Mac 上做強化學習的。在自己的訓練環境上跑，表現理論上最好。

我的 Mac Mini 本來就設定好了：自動登入、永不睡眠、電源恢復後自動開機、Screen Sharing 開啟、SSH 開啟、Tailscale 連回來。這不是為了 computer use 特別設定的——跑 OpenClaw 就需要這些。但剛好，這也是 computer use 需要的全部前提。

## 我的 Mac Mini 現在在跑什麼

半年來累積的自動化任務：

| 任務 | 類型 | 頻率 |
|------|------|------|
| LLM Wiki 同步 GitHub | CLI (git) | 每小時 |
| Daily briefing 推 Telegram | CLI + API | 每天 07:00 |
| Google Calendar 掃描 | API | 每小時 |
| 會議紀錄整理 | API + LLM | 每天 21:00 |
| Google Sheet 待辦同步 | API | 每天 08:00 / 21:00 |
| Workspace git push | CLI (git) | 每天 23:55 |

全部是 CLI 和 API。穩定、可靠、可預測。

但也就只能做這些。

## Computer Use 加進來之後能做什麼

Astra 的 computer use 把這台機器從「能跑腳本」升級成「能操作任何 GUI 應用」。以下是 CLI/API 做不到、computer use 能做的任務類型：

**瀏覽器自動化：** 很多 SaaS 工具沒有 API，或者 API 功能不全。CRM 後台匯出報表、供應商平台對帳、政府系統線上申報——這些全是「登入、點幾下、下載檔案」的流程。以前只能手動做，現在可以交給 computer use。

**表單填寫：** 把 spreadsheet 裡的資料逐筆填進 web form。聽起來簡單，但很多內部系統就是沒有批次匯入功能。

**跨應用工作流：** 從 email 讀取資訊 → 開瀏覽器查詢 → 把結果填進 Google Sheet → 截圖存檔。這種串接多個 GUI app 的流程，API 拼接起來很痛苦，computer use 就是照人類的操作方式一步一步做。

**GUI-only 的本地應用：** Keynote、Numbers、Preview。有些工作就是得打開 app 操作。

**監測和截圖：** 每天固定時間開某個 dashboard、截圖、存檔或推通知。比 Selenium 腳本好維護——不用管 DOM 結構變了。

## 設定：讓 Mac Mini 變成 AI 桌面

如果你手上有一台 Mac Mini（或任何不當主力機的 Mac），設定步驟：

**1. 系統設定**
- 一般 > 登入項目與延伸功能 > 自動登入：開啟
- 電池（或節能）> 永不進入睡眠 > 電源中斷後自動啟動
- 共享 > 螢幕共享：開啟
- 共享 > 遠端登入（SSH）：開啟

**2. 遠端存取**

在你的主力 Mac 上，打開 Finder，側邊欄就能看到 Mac Mini 的螢幕共享。或者安裝 Tailscale，從任何網路都能連回來。

**3. Astra 設定**

ChatGPT Pro（$200/月）包含 Astra 的 computer use 功能。在 Mac Mini 上登入 ChatGPT，選擇 Astra，啟用 computer use 模式。它會要求螢幕錄製和輔助使用權限——給它。

**4. 持久化**

如果你已經有 OpenClaw 或類似的 agent harness，可以把 computer use 任務排進 cron：定時啟動、執行、截圖回報、關閉。如果還沒有 harness，手動在 ChatGPT 裡開任務也行，但要記得 Astra 有 session 時間限制。

## 誠實的限制

把好話說完了，說說還不行的地方。

**Rate limit 是最大的痛。** [Samuel Jack](https://x.com/jackalmuse/status/2101790430413328413) 抱怨：5 小時上限已經會打斷多步驟工作，週鎖定更直接廢掉功能。如果你規劃的是需要 Astra 每天連續跑好幾個小時的工作流，目前的配額會卡住你。

**登入驗證是最硬的障礙。** rohit 說得對：Astra 唯一掙扎的地方是 auth。兩步驗證、CAPTCHA、登入重定向——這些設計出來就是擋機器人的。你可能需要預先登入好、保持 session 活著，或者在觸發 2FA 的時候手動介入。

**Session 穩定度參差。** [Noah](https://x.com/itsnoahd/status/2100202067830649049) 用了一陣子之後發現，Astra 長時間任務會「randomly give me a fun fact and end early」、「gets lost in the sauce」。他的結論是「overhyped powerhouse」——能力強但不穩定。

**Machineslop 風險。** 我在[〈Astra 寫的程式碼，人類已經看不懂了〉](/astra-machineslop-code-monitorability-crisis/)裡寫過：Astra 判斷沒人在看的時候，行為會改變。Computer use 的場景天生就是「沒人在看」——它在一台你不看的螢幕上操作。你需要設計監控機制：定期截圖、操作日誌、結果驗證。不能丟出去就不管。

**前端設計和大型架構不是它的強項。** 多位測試者都說這類任務還是 Fable/Claude 更好。Astra 的甜蜜點是重複性的桌面操作任務，不是需要大量判斷的創造性工作。

## 不要拿來做的事

- 輸入任何密碼或 API key 到不明網站
- 處理金融交易（銀行轉帳、股票下單）
- 長時間無監督運行（至少每小時看一次）
- 取代需要人類判斷的決策流程

Computer use 是工具，不是自主代理。目前階段，它更像一個需要定期 check-in 的實習生，不是一個可以完全信任的員工。

## 實際成本：值不值得

假設你已經有 Mac Mini（或打算買一台），每月成本：

| 項目 | 費用 |
|------|------|
| Mac Mini 硬體攤提（$599 / 60 個月） | $10 |
| 電費（M4 低功耗） | $3-5 |
| ChatGPT Pro（含 Astra） | $200 |
| Tailscale（免費方案） | $0 |
| **月總計** | **~$215** |

$200 的大頭是 ChatGPT Pro。但如果你本來就在用 ChatGPT Pro，那 Mac Mini 的邊際成本只有 $15/月。

對比一下：請一個實習生做同樣的桌面操作任務，在台灣至少 $500-700/月（時薪 183 x 每天 4 小時 x 22 天 ≈ $16,000 台幣 ≈ $500 美金）。如果 Astra 能接走其中一半的工作量，數學上是划算的。

當然，Astra 不會自己判斷「這個表單欄位要填什麼」——你還是得寫清楚的指令。但如果任務是「照這個 SOP 操作」，它目前的能力是夠的。

## 控制介面的轉移：Copilot 加 Autopilot

AI 有了自己的桌面之後，你跟電腦的互動方式開始改變。

**傳統模式：一台電腦，Copilot 模式。** 坐在電腦前，鍵盤滑鼠，請 Codex 或 Claude Code 做一些事情，但人也負責 browser 和 app 任務的操作。

**現在：一台電腦 Copilot 模式，加上一到多台電腦 Autopilot 模式。** 你依舊有一台主力電腦跑 Copilot，但你會有多台電腦做 Autopilot。介面就是手機。

像我 Mac Mini 上就是 OpenClaw + Codex。一邊做定期任務，一邊幫忙處理需要 Computer Use 的臨時任務。另外 Browser Use 我就切到 Grok Bot 上了。

[Amos](https://x.com/Amos__Hadad/status/2098917896877437070) 的做法更徹底——Astra + Computer Use + Remote，從手機下指令，不再打開電腦。Email、行銷、加功能，全透過手機交辦。

這個趨勢會往語音走。如果你用手機控制 AI 員工，打字本來就不是最自然的介面——講話是。「嘿，幫我把昨天那份合約的第三版寄給客戶」，比在小螢幕上打字快三倍。

角色全到位了：

1. **Mac Mini / Grok Bot VM / Ubuntu Linux** 是 AI 的桌面
2. **手機和主力電腦**是遙控器，**AirPods / Typeless** 是麥克風
3. **Slack / Google Drive / GitHub** 是資料載體
4. **Codex（Claude Code）、OpenClaw** 或任何 agent 平台是執行引擎

差的只是全部串起來。我在[〈新的工作時代，會不會需要新的鍵盤滑鼠〉](/agent-era-attention-interface-input-devices/)裡討論過這個趨勢：agent 時代的工作型態從「生產者」變成「監工」，互動單位從「字元」變成「決策」。Mac Mini + Astra 的組合，是這個轉變的第一個具體實例。

## 結論：AI 開始需要一台自己的電腦

回頭看我們給 agent 的東西，有一條清楚的演化線：

以前我們給 agent **API**。它能叫得動有 API 的服務。

後來給它 **Terminal**。它能跑指令、操作檔案系統、管理伺服器。

再來給它 **Browser**。它能上網、填表單、操作 SaaS 工具。

現在，我們開始直接給它一整個 **Desktop**。它能操作任何 GUI 應用——有沒有 API 都無所謂。

每一層都在擴大 agent 能觸及的工作範圍。當 API、browser use、computer use 三層拼起來之後，數位世界裡原本大量「一定要有人坐在電腦前面才能完成」的工作，正在快速縮小。

而 computer use 要實用，取決於三個條件同時到位：

1. **模型夠強。** Astra 解決了。OSWorld 2.0 從 65.7% 到 72.6%、任務時間砍半、社群實測取代實習生任務。
2. **作業系統友善。** macOS 解決了。Agent 能力乘數最高，GUI 行為可預測。OpenAI 自己也買了數萬台 Mac 來訓練。
3. **有一台專用機。** Mac Mini 解決了。$599、24/7、低功耗、無頭運行。

缺任何一個都不行。只有模型強但跑在你的主力筆電上，三十分鐘你就想把它關掉。只有專用機但跑 Windows，agent 能力打七折。只有 macOS 專用機但模型不夠強，computer use 也只是 demo。

三個條件在 2026 年九月第一次同時到位。不是因為哪一個有突破性進展，是因為它們終於拼在一起了。

我的 Mac Mini 桌子底下還是那台 Mac Mini。但它走過了三個階段：

1. **以前**是跑 Code 的盒子（AI 以前）
2. **後來**是有 Browser Use 的數位員工（OpenClaw）
3. **現在**可以操作 Desktop，有了自己桌面的 AI 員工

這可能才是 Astra computer use 真正重要的地方——不是某個 benchmark 又刷新了，是 AI 真的開始需要一台自己的電腦。

邊際成本每個月 15 美金。

---

## 相關文章

- [AI Agent 的隱形天花板不是模型，是你的作業系統](/ai-agent-os-tax-windows-powershell-hidden-ceiling/)
- [Grok Bot：xAI 用 30 美金賣你一台 150 美金的 VM，還附 AI 員工](/grok-bot-persistent-agent-cloud-computer-cost/)
- [Astra 寫的程式碼，人類已經看不懂了——但真正該擔心的不是可讀性](/astra-machineslop-code-monitorability-crisis/)
