---
layout: post
title: "AI Agent 的隱形天花板不是模型，是你的作業系統"
date: 2026-09-17 18:00:00 +0800
permalink: /ai-agent-os-tax-windows-powershell-hidden-ceiling/
description: "一條 13 萬瀏覽推文引爆中日文開發者社群：同一個 Claude，在 macOS 上順暢運作，在 Windows 上反覆犯蠢。問題不在模型降智，在 Shell 讓 Agent 降級。Agent 的真實能力 = 模型能力 x 執行環境的可駕馭度，而你的作業系統決定了這個乘數。"
categories: [AI Coding 實戰]
tags: [Claude Code, PowerShell, Windows, macOS, Linux, AI Agent, Shell, 作業系統]
image: /assets/images/ai-agent-os-tax-windows-powershell-cover.png
author: Wisely Chen
---

我今年一月寫過[一篇文章](/unix-philosophy-claude-code-command-line-renaissance/)，講我小時候看 *Unix Power Tools* 這本書，記住了一句話：「Command line pipeline is the best UI interface in the world」。當時完全不懂，二十年後 Claude Code 出現才突然理解——一個用文字理解世界的腦，接上了一個用文字暴露世界狀態的介面。

那篇文章是我個人的感受。我一直覺得這件事很重要，但很難量化，也不確定是不是只有我這種 command line 老兵才有這個感覺。

然後九月中旬，X 上 @philosophyoffa1 發了一條推，講了我很想講的話。

他列了兩條罪狀：一，Windows 是龐大的屎山，computer use 經常因為輸入法彈窗和狀態列而罷工；二，PowerShell 是一個黑盒，無論人類還是 AI 都搞不懂它，程式設計師一直用 git bash 來逃避。

328 個讚、12.9 萬次瀏覽、43 則回覆。回覆裡的態度光譜很寬——一端是「AI 時代還在用 Windows，等於提前退役」、「沒有模型能搞明白 PowerShell」，另一端是「合理懷疑沒升級 PowerShell 7」、「Windows 有最大辦公生態」。

原來不只是我的感覺。這個痛點，半年內在 X 上至少引爆過四次。

## 三條高互動推文，同一個故事

三月，@tychozzz 在配置 Windows 環境跑 Claude Code 之後寫了一條長推：Mac 自帶統一終端，幾行命令就搞定；Windows 自己有三種終端——CMD、PowerShell、WSL 互相打架，配環境一團亂麻。876 個讚、17.6 萬次瀏覽、128 則回覆。

七月，@Vincent_AINotes 描述了 Codex 在 Windows 上跑一個簡單操作的過程：agent 先寫 bash，報錯，再套一層 `powershell -Command`，轉義越來越多，最後在引號裡打轉。「真正的解決辦法不是繼續重試，而是先固定唯一的執行環境。」380 個讚、9.2 萬次瀏覽。

同月，@markdown_chen 轉述了一個常見建議：Windows 用 AI 工具效率慢、容易錯、中文亂碼，因為系統內建的 PowerShell 5.1 太拉垮，升級到 7 會好一些。288 個讚、6.5 萬次瀏覽。

日文社群也在同一個主題上爆。@supermomonga 發現 Claude Code 在 WSL 裡頻繁凍結，原因是它會同步呼叫 `powershell.exe` 去取得 Windows 側的使用者名稱。402 個讚、7 萬次瀏覽。他的解法是設環境變數跳過這個檢查。

把這些推文攤開，總互動量超過 50 萬次瀏覽。社群在吵的不是「哪個模型比較聰明」，是一個更底層的問題：**同一個模型，換一個作業系統，表現判若兩人。**

## 技術拆解：為什麼作業系統能讓模型「降智」

先講結論，再拆解。

**Agent 的真實能力 = 模型能力 x 執行環境的可駕馭度。**

模型能力大家一樣——同一個 Claude、同一個 Codex、同一個版本。但「執行環境的可駕馭度」天差地遠。這個乘數決定了 agent 能把多少模型能力轉化成實際產出。

乘數高的環境：agent 下一個指令，環境精確執行，回傳可解讀的文本結果，agent 解讀後下一步。循環順暢。

乘數低的環境：agent 下一個指令，環境用意料之外的方式回應（或靜默失敗），agent 困惑，嘗試修復，越修越歪，token 消耗暴增，最終產出品質下降。

Shell 是 agent 的手腳。每一次檔案操作、每一次 git 指令、每一次測試執行、每一次環境檢查，都得經過 shell。Shell 的表現直接決定了那個乘數。

### 困境一：文本哲學 vs. 物件哲學

這是最根本的差異。

Unix 的設計哲學是「一切皆文本」。`ls` 輸出文本、`grep` 處理文本、`awk` 切文本、pipe 串文本。五十年來，整個 Unix 世界都建立在文本流上。

LLM 也是文本的動物——它讀文本、寫文本、用文本推理。

Unix shell 的輸出格式和 LLM 的思考方式天生相容。Agent 跑一個 bash 指令，拿到純文本輸出，直接就能讀懂、解析、決定下一步。錯誤訊息也是文本——`command not found`、`permission denied`——LLM 在訓練資料裡見過千百萬次，知道怎麼修。

PowerShell 走的是完全不同的路。它的 pipeline 傳遞的是 .NET 物件，不是文本字串。同一個指令的輸出，序列化成文本時可能長得完全不一樣，取決於物件類型和格式化設定。錯誤處理涉及結構化的 exception，不是簡單的 stderr 文字。

從設計品質的角度，物件管線是更「正確」的做法——它避免了文本解析的脆弱性，帶了型別資訊，語義更豐富。

但對 LLM 來說，這些優點全部變成障礙。模型在推理時需要可預測的文本模式，PowerShell 給它的是一層需要理解 .NET 類型系統才能正確操作的抽象。

### 困境二：三殼共存的歧義

Windows 上有三個 shell：CMD、PowerShell、WSL bash。同一台機器上，不同工具可能預設不同的 shell，甚至同一個工具在不同情境下會切換。

@Vincent_AINotes 描述的場景就是典型：agent 先用 bash 語法，報錯後「退化」成 PowerShell 語法，兩套語法的轉義規則不同，越包越多層，最後崩潰。

macOS 和 Linux 上不存在這個問題。shell 就是 zsh 或 bash，語法統一，沒有歧義。Agent 不需要花 token 去猜「現在我在哪個 shell 裡面」。

### 困境三：訓練資料的馬太效應

bash/sh 從 1989 年就是 Unix 世界的預設 shell。GitHub 上數以千萬計的 `.sh` 腳本、Stack Overflow 上數以百萬計的 bash 問答、幾乎所有 CI/CD pipeline 和 Docker 容器的指令層都是 bash。

PowerShell 2006 年才發布，主要使用族群是 Windows 系統管理員，不是軟體開發者。它在 GitHub 和 Stack Overflow 上的內容量和 bash 不在同一個數量級。

LLM 的能力跟訓練資料直接正相關。見過的 bash 模式多，bash 就用得好；見過的 PowerShell 模式少，PowerShell 就用得差。然後，用得好的環境吸引更多使用者產生更多範例，進入下一輪訓練——馬太效應。

## 不只是 Shell：Windows 整體的 Agent 稅

Shell 是最明顯的痛點，但不是唯一的。

**路徑分隔符。** Windows 用反斜線 `\`，Unix 用斜線 `/`。這不是新鮮事，但它在 agent 時代產生了新的問題：hook 和安全規則用正則表達式寫，`\` 在正則裡是跳脫字元，Windows 路徑會讓規則靜默失效。一位日本開發者 @heshuhong1 分享：他的 PreToolUse hook 原本用來阻擋特定路徑，在 Windows 上因為路徑分隔符不同，正則完全不匹配，「效いているつもり」——以為規則在運作，其實什麼都沒擋。

**路徑長度限制。** Windows 傳統的 260 字元路徑上限。Claude Code 在九月中旬（v2.1.271）才修了一個相關 bug：暫存輸出路徑超過 260 字元時，PowerShell 直接 `Exit code 1` 崩潰，沒有有意義的錯誤訊息。日語資料夾名稱容易觸發這個限制，中文資料夾名稱也是。

**編碼黑洞。** PowerShell 5.1 預設用系統 legacy code page 讀 `.ps1` 檔案，沒有 UTF-8 BOM 的腳本會靜默亂碼。一位韓國開發者 @hisokastalking 花了一小時 debug 一個 Claude Code hook——hook 本身沒錯，是 PowerShell 5.1 的編碼設定讓韓文正則靜默失效，沒報錯，就是不匹配。

**IME 和 UI 彈窗。** Computer use（讓 AI 操作桌面）在 Windows 上特別脆弱，輸入法候選字視窗、系統通知、工作列彈出——這些 UI 元素會打斷 agent 的點擊操作。macOS 的 accessibility API 設計得更乾淨，Linux 上跑 headless 更是根本不需要處理這些。

每一項單獨看都是小問題。疊在一起，就是一筆可觀的「Agent 稅」。

## 反論也有道理

公平地講，社群裡的反方不是在胡扯。

**PowerShell 7 確實進步很多。** 跨平台、UTF-8 預設、語法更接近 Linux 習慣。回覆裡 @dhssingle 說的「合理懷疑沒升級 PowerShell 7」不是沒有道理。問題是 Windows 10/11 內建的仍然是 PowerShell 5.1，多數使用者根本不知道要升級。

**辦公生態離不開 Windows。** 這一點在中國大陸尤其明顯——國產辦公軟體很多沒有 Linux 版，或者 Linux 版功能被砍。@lxid0413 說「Windows 有最大辦公生態」是事實，不是偏見。

**Unix shell 也不是沒有坑。** @pusanshi 指出「理論上 sh 雜亂無章，比 PowerShell 複雜得多」——這也是對的。bash 的各種 profile 載入順序（`.bashrc`、`.bash_profile`、`.profile`）、不同發行版的預設差異、macOS 的 zsh 遷移，都有各自的坑。只是這些坑被五十年的社群知識填平了，LLM 訓練資料裡有現成答案。

**微軟在 AI 層面做得很好。** 這點容易被忽略。GitHub Copilot 是最早大規模商用的 AI coding 工具，Azure OpenAI 撐起了一大半企業 AI 部署，VS Code 是 AI coding 生態系的基座。微軟的問題不在 AI 策略層，在底層基礎設施——shell、process model、automation API——這些東西是三十年前的設計遺產，不是一個版本更新能翻修的。

## 不是「Windows 不好」，是設計假設變了

把這件事寫成「Windows 很爛，快換 Mac」太簡單了，也不準確。

真正發生的事情是：**AI agent 的崛起改變了「好的作業系統」的定義。**

二十年前，好的作業系統 = GUI 漂亮 + 應用生態豐富 + 硬體相容性好。這個定義下，Windows 贏得合情合理。

現在，agent 時代多了一個維度：**shell 和 automation API 的 LLM 可駕馭度。** 在這個維度上，POSIX 世界（macOS、Linux）拿了高分，因為 Unix 1970 年代的設計哲學——一切皆文本、小工具組合、標準化介面——意外地完美匹配了 LLM 的工作方式。

這不是 Unix 設計者的先見之明，是歷史的巧合。Ken Thompson 和 Dennis Ritchie 在 1970 年代選擇文本流當管線介面，是因為那個年代的計算資源只夠處理文本。五十年後，這個當年的限制變成了 LLM 時代的優勢。

PowerShell 的物件管線在「人寫腳本」的場景下其實更優雅——強型別、自動補全、不需要 `awk '{print $3}'` 這種文本黑魔法。但 LLM 不需要強型別和自動補全，它需要的是可預測的文本輸出和在訓練資料裡見過的模式。

設計哲學的碰撞，不是品質的問題。但碰撞的結果是真實的：用 Windows + PowerShell 跑 AI agent，你的 agent 會比用 macOS / Linux 跑同一個模型更慢、更不穩定、消耗更多 token。

## 實際建議

不同起點，不同路徑。

**已經在 macOS 或 Linux 上開發。** 什麼都不用改。你已經在吃紅利了。

**在 Windows 上，願意折騰。** WSL 2 是最小成本路徑：把開發專案放在 WSL 的 Linux 檔案系統裡，AI 工具也從 WSL 裡啟動。缺點是 @philosophyoffa1 說的——SSD 空間被兩個系統吃掉，而且 WSL 和 Windows 之間的檔案系統跨界操作偶爾有性能和權限問題。

**在 Windows 上，不想動作業系統。** 至少做三件事：一，升級到 PowerShell 7（`winget install Microsoft.PowerShell`）；二，在 AI 工具的設定裡把預設 shell 固定成一個（不要讓它在 CMD / PS / bash 之間跳來跳去）；三，專案路徑盡量短、盡量用 ASCII——躲開 260 字元和編碼的地雷。

**正在考慮買新機器給 AI 開發用。** 如果預算夠，MacBook。如果追求性價比，裝 Linux 的 NUC 或迷你主機。這不是信仰問題，是工具效率問題。回覆裡 @yabinshay 說的「我在猶豫要不要把 NUC 裝 Linux」——如果那台 NUC 主要拿來跑 AI coding，裝吧。

## 微軟的真正挑戰

最後講一件事。

微軟在 AI 時代的真正挑戰，不是模型不夠強（有 OpenAI 和自己的 Phi 系列），不是雲不夠大（Azure 是三大之一），甚至不是 IDE 不夠好（VS Code 生態無敵）。

挑戰在：**Windows 的 shell 和 automation 層，是為「人操作電腦」設計的，不是為「AI 操作電腦」設計的。** 而 macOS 和 Linux 的 POSIX 層，剛好被歷史的巧合推到了對的位置。

這個差距不是一兩個版本更新能補上的。它需要的是讓 Windows 的底層自動化介面對 LLM 更友善——更可預測的文本輸出、更統一的 shell 體驗、更乾淨的 headless 操作模式。微軟有資源做這件事，問題是優先順序和向下相容的包袱。

13 萬人看一條推文吵架，吵的表面是 PowerShell，底層是整個 PC 生態在 agent 時代的定位。

這場仗才剛開始。
