---
layout: post
title: "\"Pi 99.93% Cache Hit：10 億 token 只花 $2.65，Agent 選型要多盯一個數字\""
date: 2026-08-25 09:00:00 +0800
permalink: /pi-cache-hit-99-93-context-compression-roadmap/
tags: [Pi, cache hit, prefix cache, KV cache, context compression, agent harness, DeepSeek V4 Flash, token cost, 成本優化, compaction, session tree, append-only, coding agent, 開源模型]
categories: [AI Agent]
image: /assets/images/pi-cache-hit-99-93-cover.png
description: "\"第一次用 Codex 接開源模型寫 code，成效不太好，換成社群推的 Pi 突然強很多。順手算了一筆帳：有人用 Pi 接 DeepSeek V4 Flash 跑掉近 10 億 input token，cache hit 99.93%，帳單 $2.65。這篇把 Pi 做對的事拆成五個機制，逐條對到源碼和官方文件，講它的哲學、session 樹和 compaction 是怎麼運作的，最後講一句結語。\""
author: Wisely Chen
faq:
  - question: "我用 Claude（Anthropic API），Pi 的優勢還成立嗎？"
    answer: "方向成立，幅度收斂。Anthropic 的 prompt cache TTL 是 5 分鐘，離線吃飯回來前綴就斷，hit rate 的天花板比 DeepSeek 低。但前綴穩定的紀律依然省錢——斷了之後重寫的 cost 低，且斷的頻率低。要自己拉 log 看實際 hit rate，不要直接套 99.93%。"
  - question: "94-97% 的「其他 harness」，具體指誰？"
    answer: "我的理解是「預設工具多、前綴常動」的那類（工具開場全宣告、每輪重新組 prompt 的）。不是說哪一家做不好，是說這個指標要逐家測，不該預設。"
  - question: "/compact 和 /tree 會互相干擾嗎？"
    answer: "不會。兩者都只 append 新 entry（CompactionEntry 或 BranchSummaryEntry），不改舊資料。摘要會互相引用——branch summary 可以壓一個已 compaction 過的 branch，檔案追蹤也是累積併入。完整歷史永遠在 JSONL 檔裡。"
  - question: "五種壓縮路線可以疊著用嗎？"
    answer: "可以，但要有主次：入口過濾是底層，備忘錄是主策略，版本控制是安全網，前置異步和遺忘派是調優層。兩個都在「決定保留什麼」的插件裝一起會互相覆蓋。"
  - question: "我該不該從訂閱轉 API？"
    answer: "看 API 等值。把我過去兩週真實的 API 用量 log 拉出來，用官方牌價算一次：如果超過訂閱費用的三倍，乖乖回去付月費；三倍以內，API 不僅更便宜，還給更強的靈活性。我 8 月底那篇算過：我的 API 帳單 $631-681 一個月，對 $200 訂閱，超過三倍，訂閱划算。  ---"
---

## 先講一句保證無聊的前言

最近研究 Pi 這個 harness 的設計，越看越覺得像大學翻 OS 恐龍本——cache locality、write-ahead log、GC、eviction policy，全是那些老東西，只是現在管的不是 row 跟 page，是對話跟決策。（恐龍本＝資工人的 OS 教科書，因為每一版封面都有恐龍。在 AI 時代還敢提恐龍本，有一種自己是恐龍的自嘲感。）

## 第一次用開源模型 coding，成效不好

又到了保證無聊的 IT 日。

我前段時間第一次用 Codex 接開源 LLM 做 coding。說實話，成效不太過得去：該改的地方漏改、改動之間互相打架、長一點的 session 就開始忘前面講過什麼。我沒有立刻下結論，因為不太確定問題出在哪——是模型本身不夠強，是 prompt 寫得不好，還是 harness 的問題？

後來換成社群一直在推的 Pi，同一個模型，體感突然好很多。同樣的任務，它開始記得前面讀過哪些檔案、改過什麼、哪一步卡住；長 session 沒有明顯的衰退。而且成本這頭，用 API 跑的時候帳單低得不像話。

這個體感不是孤例。有人用 Pi 接 DeepSeek V4 Flash，跑掉近 10 億 input token，cache hit rate 99.93%，帳單 $2.65。同一筆用量沒有 cache 的話，約 $132。同一個模型放到其他 harness，cache hit 常見落在 94% 到 97%；Pi 上能穩住 99% 以上。差的這幾個點，量一大，錢是指數級拉開的。

所以這篇做的事很單純：把「到底 Pi 哪裡做得好」拆開，逐條對到源碼和官方文件，不是讀心得。

## 先講清 prefix cache：改一個逗號，後面全部重算

99.93% 的 cache hit rate 是什麼意思？先講底層的算術。機制細節之前在 [搞懂快取機制，從 Gemma4 到 Claude Code 省 80% Token](https://ai-coding.wiselychen.com/kv-cache-gemma4-claude-code-save-80-percent-token/) 那篇拆過了（KV cache 為什麼是 prefix 結構、Claude Code 的快取工程），[DeepSeek V4 Flash 的 disk KV cache](https://ai-coding.wiselychen.com/deepseek-v4-flash-disk-kv-cache-50x-economics/) 那篇則把 hit rate 90% 到 99% 帳單差 4 倍的數學算給你看了，這裡就不重複，只講對 Pi 這件事的影響。

LLM 處理資訊高度依賴線性順序：這次送進去的 prompt，只要前半段跟上一次**完全一樣**，那一段就可以跳過運算——模型直接從 KV cache 端出之前算好的結果，不計費（或只收極低費用）。這就是「前綴命中」（prefix cache hit）。

但是只要前綴裡改了一個字——哪怕只是加了一個逗號——從那個字開始到結尾，整段都被判定為全新資訊，全額買單。一次全價重算可能就是幾萬個 token 的錢。

所以整個優化的核心只有一個問題：**你送給模型的 prompt，前綴有多穩定？**

Pi 的 hit rate 穩在 99.93%，其他 harness 常見落在 94% 到 97%。差的這幾個點，量一大，錢是指數級拉開——$2.65 和 $132 就是這條曲線上兩點。

社群裡的第一直覺是：Pi 是不是用了什麼黑魔法、什麼獨家的快取演算法？把 Pi 的源碼和官方文件翻遍之後，答案是異常樸實的：**它沒有用到任何新快取技術，全部是靠「不亂動前綴」的工程紀律。**

## Pi 的六個紀律：每一條都是「少動前綴」

用一個廚房的比喻串起來：前綴就是廚房的鍋碗瓢盆、爐具、冰箱擺位——每晚不管來什麼新訂單，主廚絕對不會為了一道新菜把整個廚房重新排列一次。重新排列布局＝改變前綴＝全額重算。主廚唯一做的事，是把新食材從後門送進來。

Pi 的六條紀律，全是在保護這個廚房不被重排：

**一、預設工具只有 4 個。** system prompt 構造程式碼裡寫得很直白，預設工具只有 read、bash、edit、write。沒有 grep、find、ls——需要時 agent 用 bash 自己跑。工具的定義和說明就寫在前綴最前面，多一個工具就多一大包「前綴可能變動」的風險。很多 harness 開場就把工具全數宣告給模型，Pi 反其道而行：少一個工具，前綴就穩一分，而且穩的是**每一次請求**。

**二、system prompt 薄。** 預設 prompt 只有幾十行。現在很多開發者喜歡寫幾千字包山包海的完美提示詞，把所有行為準則都塞進去。但 system prompt、工具定義、AGENTS.md 只要動一個字，cache 前綴就斷掉。Pi 的 design choice 不是讓前綴「多」，是讓它「不常變」。

**三、session 是 append-only 的。** 每一輪都是在舊 context 後面原封不動地接上新訊息，不是每輪重新拼一份「系統設定＋歷史記錄」的新 prompt。這一條最容易被忽略，但它是 99%+ 的物理基礎：前面幾十萬個 token 像鎖死在地板上的流理台，穩穩釘在 cache 裡，模型唯一要花錢重算的只有最後送進去的那一點新指令。

**四、skill 按需載入。** 預設狀態下，system prompt 裡只有每個 skill 的名稱加一句短描述——像廚房架子上只放食譜的書名目錄，不是把整本食譜攤開佔空間。真要做那道菜的時候，agent 才用 read 把全文讀進來。這樣平常不用的技能不佔前綴空間。對比很多 harness 開場就塞幾千 token 的 instruction，這個設計省的不是「有沒有」，是「前綴乾不乾淨」。

**五、compaction 走獨立 routing session，不污染主線。** 這條最容易漏。多數 harness 的 compaction 是「context 滿了就叫 LLM 總結」——那個一次性的總結請求直接送進主 session，前綴當場斷掉。Pi 的官方文件寫明：壓縮和 branch summary 的請求會用**新的 routing session**（開一個分身去處理），而且在 provider 有支援時**主動關閉 prompt cache write**。一次性摘要的產物用完就丟，絕不讓垃圾混進主廚房。

**六、換 branch 有第二種摘要，同樣不污染。** 用 /tree 跳到另一個 branch 時，Pi 可以問你要不要把離開的那條 branch 總結成一段 context 帶過去（可以關）。同一套結構化格式、同一套檔案追蹤——同樣是 routing session，同樣關掉 cache write。所以「記憶」在 Pi 裡不是線性的對話摘要，是**樹上每個分岔口都可以存一份結構化狀態**。

六條加起來，99.93% 的來源就出來了。注意，沒有一條是「快取技術」。全是紀律。

## session 樹：一個免費的時光機

很多人以為 agent 的對話像聊天機器人那樣是一條直線。Pi 底層的資料結構其實是**一棵樹**：存檔是 JSONL，每一行一個 entry，靠 id 和 parentId 串接。每一次對話、工具呼叫、或嘗試碼的修改，都是樹上的一個獨立節點。

這解釋了 append-only 最常被質疑的問題：一直只加不減，AI 走錯路（比如寫爬蟲寫了幾百行才發現套件不支援）不就永遠困在錯誤脈絡裡了嗎？

不會。你不需要手動刪掉前面的錯誤對話，也不用另存新檔——用 /tree 回到走錯之前那個節點，直接從那裡長出一條新分支。而且因為你回去之後，那個節點之前的前綴**依然是完美沒有變過的**，cache 照樣有效。走錯路的代價，只是錯的那條分支本身。

**視窗管理是兩個數字。** 模型視窗固定扣掉 16,384 tokens 給 LLM 回應——這是雷打不動的呼吸空間，免得 AI 講到一半被截斷（context 超過「視窗 − 16,384」就觸發壓縮）。另外 20,000 tokens 是壓縮時保留的「最近訊息」額度——確保 AI 在壓縮龐雜歷史時，對眼前任務保持清晰的短期工作記憶。兩個都可以在 settings 調，所以 Pi 的 context 不是「滿了才管」，是留了 buffer 才動。

## 五步壓縮：切點必須保持動作完整

/context 滿了（或手動 /compact）之後，實際發生什麼：

1. **找切點。** 從最新訊息往回數，數到 20,000 tokens 畫一條線。切點非常講究：只能落在 user 訊息、assistant 訊息、bash 執行、或 custom 訊息上——**絕對不能切在程式碼讀到一半或工具執行結果的中間**，它必須跟它的 tool call 留在同一邊。切線前面是要總結的舊訊息，後面是原樣保留的最近訊息。
2. **生成結構化摘要。** 舊訊息先序列化（tool result 砍到 2,000 字，因為 read 和 bash 的輸出通常是 context 裡最大的一塊），然後叫 LLM 用固定格式填：Goal、Constraints、Progress（Done / In Progress / Blocked）、Key Decisions、Next Steps、Critical Context，加上兩段清單——讀過哪些檔案、改過哪些檔案。
3. **摘要回寫成一個新 entry。** 不是改舊資料，是 append 一個 CompactionEntry。下一輪請求送給 LLM 的是：system prompt + 摘要 + 切點之後的訊息。被壓掉的舊訊息沒有消失，還完整躺在 JSONL 檔裡，只是不在送出的 context 裡面。
4. **重複壓縮是迭代的。** 第二次壓縮時，上一次的摘要會當作 input 傳進去，新摘要是「舊摘要 + 新舊訊息」再壓一次。檔案追蹤也是累積的——每次把前一次摘要裡的 read/modified 清單併進來，所以壓了五輪，「這個 session 動過哪些檔案」不會斷。
5. **摘要請求本身不進主 session 的 cache。** 用新的 routing session，provider 有支援時關閉 cache write——這就是第五條紀律在實務上的樣子。

一個容易漏的細節：單一輪對話如果本身就超過 20,000 tokens（例如一次 read 了幾千行的檔案），切點會落在這一輪中間，Pi 會生成兩份摘要再合併——一份給之前的歷史，一份給這一輪的開頭。所以不會出現「整輪都壓沒了，agent 完全不知道那輪發生過什麼」。

## Agent 記憶的羅生門：五種路線，沒有共識

內建的 compaction 是最被動的一種：等 context 滿了才動。放眼整個開源生態，「AI 到底該怎麼記憶」沒有共識。我整理出五種路線（有些名字在 GitHub 上搜不到確切專案，所以只講思路）：pai-acp 讓 agent 自己判斷哪些歷史該提前壓掉；pi-smart-compact 只留一張便利貼——目標、改過的檔案、未完成事項；pi-context 把 context 當 Git 管，可回溯、可 diff、可 revert；Hypa 乾脆在門口過濾，不相干的資訊根本不進來；pi-press 在背景偷算摘要，真要 compact 時直接切換。

五派聽起來各有各的道理，但這裡藏著一個巨大的權衡——GitHub 上 star 最多的 pi-vcc（267 stars）走的是第六條路：完全不用 LLM 做總結，純語法抽取加格式化，號稱無損（lossless）。思路是「總結必然有損，那就不總結，只重排」。

無損？聽起來太完美了——既然 LLM 摘要一定會遺失細節、還會產生幻覺，為什麼不所有人都直接裝 pi-vcc，把五派全丟掉？

**因為它保留的是動作，遺失的是語意。** 純語法抽取知道程式碼被改成了什麼樣，但「當初為什麼要改這行」的決策邏輯、討論過程，全部不見了。

而且別貪心。如果貪一點，把入口過濾、備忘錄、pi-vcc 無損抽取全裝進同一個 agent——AI 會陷入嚴重的邏輯混亂。因為這些套件會為了「誰才有資格決定留下什麼資訊」在底層瘋狂打架，不斷互相覆蓋狀態，最後整個搞砸。

所以選的時候要有主次：**入口過濾守在最底層（少塞垃圾），備忘錄當主要的壓縮策略（保留工作狀態），版本控制當最後的安全網（可回溯）。** 前置異步和遺忘派是調優層。你問五個人「agent 記住了什麼」會得到五個答案——這跟我之前寫 [agent memory benchmark 的 Rashomon 現象](/agent-memory-benchmark-rashomon-filesystem-wiki/) 是同一個未解題。現在答案變成五個路線，而且五個都能跑。

## Pi 的哲學：核心夠輕，能力自己往上加

回過頭看，前面六條紀律其實是同一個決定在不同位置的投影：Pi 的核心刻意維持很薄，不內建任何「看起來有用」的東西。但生態在長——sub-agent、sandbox、memory、plan mode、remote session 一個個出現，社群的討論就變成「Pi 要不要把這個加進去」。

這個問題問法就有點偏了。真正該問的是：這件能力該放在哪一層？我把它拆成三層：

**基礎能力，進 Core。** 沒有就跑不起來的——session 管理、context 組裝、tool call 循環、compaction。Pi 的 Core 目前做的全是這一層，而且做得很乾淨。

**規則和標準，Core 定底線。** 權限模型、remote session 的協定、sub-agent 之間的通信格式。這層交給每個 extension 自己設計，結果就是每個專案一套規格，生態越長越碎。Pi 至少得把介面和最小協定定出來，實現可以百花齊放，但話語要統一。

**玩法，永遠留給 Extension。** memory 用檔案還是向量庫、plan mode 幾步走、sub-agent 怎麼分工、搜索工具用哪個——這些是偏好的問題，不是能力的問題。我的立場很明確：這些 Pi 永遠不該替用戶決定，今天不該加，三年後也不該加。

翻遍 Pi 的官方文件和幾個主要 extension 的 README，這個分層不是腦補——官方的態度就是「不需要的功能不進 core」。這也解釋了為什麼那六條紀律能存在：預設工具敢只留 4 個，就是因為它不把「多」當目標。一句話講完：**能用 extension 解決的，不去動核心。把核心的邊界鎖死，把怎麼玩的決定權留給擴充套件。** 這也是 Pi 最難守住的地方——功能請求只會越來越 loud，守住「不加」比做出功能需要更大的定力。

## 結語：前綴穩定是鐵律，Pi 只是守得最徹底的那個

Pi 沒有什麼黑魔法，它的強是「少」。工具少、prompt 薄、context 只加不改、skill 按需、壓縮不污染 cache——全是紀律，不是技術。輕量化不是功能缺失，是為了極致效能主動做出的選擇。這解釋了為什麼「換成 Pi 就突然強很多」：換的不只是介面，是每一輪請求送進模型的東西變乾淨了，同一個模型自然表現得好。

但要把 99.93% 直接套到自己的帳單上之前，先想兩件事。

**第一，這個數字是 DeepSeek 和 Pi 的乘積。** 99.93% 是 DeepSeek 的底層架構加 Pi 的軟體紀律完美結合的產物。DeepSeek 採用基於磁碟（disk）的 KV cache，快取存活時間可以撐很久，甚至以天計；Anthropic 為了反應速度把 prompt cache 放在 RAM 裡，成本貴，TTL 目前只有 5 分鐘——你起身倒杯水回來，前綴就灰飛煙滅，回來那句對話要為前面幾萬個 token 重新全價買單。換成 Anthropic，大方向依然成立（前綴穩定還是省錢，斷了之後重寫成本低、斷的頻率低），但那種極致的省錢幅度你大概率看不到，hit rate 的天花板先天就低。

**第二，「省 token」是最常見的優化陷阱。** qwen-code 加了一個工具動態載入的功能——只在模型需要某個工具時才送工具說明。在沒有快取的思維裡這聽起來很合理：少送字，少付錢。結果每個 request 的前綴長得都不一樣了，hit rate 從 97.5% 瞬間雪崩到 81.5%。表面數據：每個 request 的 token 總量少了 46%；實際帳單：原本一次 $1.05 的任務飆到 $3.30。成本翻了三倍多。任何號稱能省 token、卻需要頻繁變動前綴的奇技淫巧，最後都會在 API 帳單上狠狠教訓你。

所以真正的結論只有一句：**前綴穩定是當今所有 harness 都該守的鐵律，Pi 只是目前守得最徹底的那個。** 選 agent 的時候，把 cache hit rate 跟模型智力分並列——這個數字不寫在 leaderboard 上，要自己拉 log 算：Pi 的 footer 直接給（cache read / write / 當次 hit rate），Claude Code 的 log 在 `~/.claude/projects/` 底下，我之前那篇 [17 億 token 成本拆解](/ai-coding-token-cost-calculation-cache-read/) 有方法。不要盲信別人的測試數據，包括這篇。

## 最前沿的科技，需要最基礎的知識

回頭看，整篇文章其實只講一件事：Agent harness 的工程學問就是那些學問，一直都沒變。前綴穩定是 cache locality，session 樹是 write-ahead log，compaction 是 GC，五種壓縮路線對應的是 eviction policy 的選擇。最近看 Agent harness 設計，越來越像 DB、像 OS——差別只是它管的不是 row 跟 page，是對話跟決策。

做得好不好，不是看模型多聰明，是看寫 harness 的人恐龍本翻得夠不夠熟。

---

## 常見問題 Q&A

**Q: 我用 Claude（Anthropic API），Pi 的優勢還成立嗎？**

方向成立，幅度收斂。Anthropic 的 prompt cache TTL 是 5 分鐘，離線吃飯回來前綴就斷，hit rate 的天花板比 DeepSeek 低。但前綴穩定的紀律依然省錢——斷了之後重寫的 cost 低，且斷的頻率低。要自己拉 log 看實際 hit rate，不要直接套 99.93%。

**Q: 94-97% 的「其他 harness」，具體指誰？**

我的理解是「預設工具多、前綴常動」的那類（工具開場全宣告、每輪重新組 prompt 的）。不是說哪一家做不好，是說這個指標要逐家測，不該預設。

**Q: /compact 和 /tree 會互相干擾嗎？**

不會。兩者都只 append 新 entry（CompactionEntry 或 BranchSummaryEntry），不改舊資料。摘要會互相引用——branch summary 可以壓一個已 compaction 過的 branch，檔案追蹤也是累積併入。完整歷史永遠在 JSONL 檔裡。

**Q: 五種壓縮路線可以疊著用嗎？**

可以，但要有主次：入口過濾是底層，備忘錄是主策略，版本控制是安全網，前置異步和遺忘派是調優層。兩個都在「決定保留什麼」的插件裝一起會互相覆蓋。

**Q: 我該不該從訂閱轉 API？**

看 API 等值。把我過去兩週真實的 API 用量 log 拉出來，用官方牌價算一次：如果超過訂閱費用的三倍，乖乖回去付月費；三倍以內，API 不僅更便宜，還給更強的靈活性。我 8 月底那篇算過：我的 API 帳單 $631-681 一個月，對 $200 訂閱，超過三倍，訂閱划算。

---

## 坦白說

- **$2.65 vs $132 是單人自述。** 沒有 session 數量、工作負載、cache write 成本的資訊。10 億 input 對應的是一長串長 session，不是「開機就跑出來」的。
- **94-97% 是「其他 harness 常見」的觀察，不是 benchmark。** 沒有掛出每家 harness 的實測數字。方向大概率沒錯（多數 harness 的預設工具多、前綴常動），但「Pi 穩 99%+」在 Anthropic 上是否同樣成立，沒有人回答。
- **5 種壓縮路線，我只有 pi-smart-compact 和 pi-vcc 對到 repo。** pai-acp、pi-context、Hypa、pi-press 在 GitHub 上搜不到確切專案，可能是小拼、私有、或還沒開源。思路分層是依社群描述寫的，不是逐個讀了原始碼。
- **DeepSeek V4 Flash 的牌價 8 月 16 日漲過一波。** 那篇我寫過了。$0.0028/$0.14 是漲價後的牌價，$2.65 那筆帳單是用哪個時期的價，不清楚。

---

**來源**

- [0xEvan：99.93% cache hit on DeepSeek v4 flash with pi harness](https://x.com/EvanDeKim/status/2086681823216546294)（2026-08-10）
- [Pi 官方文件：Compaction](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/compaction.md)
- [Pi 官方文件：Session Format](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/session-format.md)
- [Pi 源碼：system-prompt.ts（預設工具）](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/system-prompt.ts)
- [pi-smart-compact](https://github.com/alpertarhan/pi-smart-compact)（30 stars）
- [pi-vcc](https://github.com/sting8k/pi-vcc)（267 stars）
