---
layout: post
title: "Pi 99.93% Cache Hit：10 億 token 只花 $2.65，Agent 選型要多盯一個數字"
date: 2026-08-25 09:00:00 +0800
permalink: /pi-cache-hit-99-93-context-compression-roadmap/
description: "第一次用 Codex 接開源模型寫 code，成效不太好，換成社群推的 Pi 突然強很多。順手算了一筆帳：有人用 Pi 接 DeepSeek V4 Flash 跑掉近 10 億 input token，cache hit 99.93%，帳單 $2.65。這篇把 Pi 做對的事拆成五個機制，逐條對到源碼和官方文件，講它的哲學、session 樹和 compaction 是怎麼運作的，最後講一句結語。"
categories: [AI Agent]
image: /assets/images/pi-cache-hit-99-93-cover.png
author: Wisely Chen
---

## 第一次用開源模型 coding，成效不好

我前段時間第一次用 Codex 接開源 LLM 做 coding。說實話，成效不太過得去：該改的地方漏改、改動之間互相打架、長一點的 session 就開始忘前面講過什麼。我沒有立刻下結論，因為不太確定問題出在哪——是模型本身不夠強，是 prompt 寫得不好，還是 harness 的問題？

後來換成社群一直在推的 Pi，同一個模型，體感突然好很多。同樣的任務，它開始記得前面讀過哪些檔案、改過什麼、哪一步卡住；長 session 沒有明顯的衰退。而且成本這頭，用 API 跑的時候帳單低得不像話。

這個體感不是孤例。有人用 Pi 接 DeepSeek V4 Flash，跑掉近 10 億 input token，cache hit rate 99.93%，帳單 $2.65。同一筆用量沒有 cache 的話，約 $132。同一個模型放到其他 harness，cache hit 常見落在 94% 到 97%；Pi 上能穩住 99% 以上。差的這幾個點，量一大，錢是指數級拉開的。

所以這篇做的事很單純：把「到底 Pi 哪裡做得好」拆開，逐條對到源碼和官方文件，不是讀心得。

## 到底 Pi 哪裡做得好：五個機制，逐條對到源碼

社群裡流傳的解釋是「系統提示詞短、預設工具少、請求前能看能改上下文」。方向對，但不完整。我把 Pi 的源碼和官方文件翻了一遍，能對上的是五件事：

**一、預設工具只有 4 個。** Pi 的 system prompt 構造程式碼裡寫得很直白，預設工具只有 read、bash、edit、write。沒有 grep、find、ls 這些「看起來有用」的預設——需要時 agent 用 bash 自己跑。工具定義是 prompt 前綴的一部分，少一個工具，前綴就穩一分，而且穩的是每一次請求。

**二、system prompt 薄，前綴穩定。** Pi 的預設 prompt 只有幾十行。system prompt、工具定義、AGENTS.md 這些東西只要動一個字，cache 前綴就斷掉，後面整段重新全價計算。Pi 的 design choice 是讓前綴盡量「不常變」，而不是讓它「多」。

**三、session 是 append-only 的。** 每一輪都是在舊 context 後面加新訊息，不是每輪重新拼 prompt。這一條最容易被忽略，但它是 99%+ 的物理基礎：前 9 億 token 永遠長在 cache 裡，新的只有最後幾 K。

**四、skill 按需載入。** Pi 的 skill 機制預設只把名稱和描述放進 system prompt，需要時才用 read 把全文讀進來。對比很多 harness 開場就塞幾千 token 的 instruction，這個設計省的不是「有沒有」，是「前綴乾不乾淨」。

**五、compaction 本身也是 cache-aware 的。** 這條最容易漏。Pi 的官方文件寫明：壓縮和 branch summary 的請求會用新的 routing session，而且在 provider 有支援時**主動關閉 prompt cache write**——這些一次性的摘要 prompt 本來就不該佔 cache。多數 harness 的 compaction 是「context 滿了就叫 LLM 總結」，Pi 的 compaction 是「總結請求別去污染主 session 的 cache」。

五條加起來，99.93% 的來源就出來了。注意，沒有一條是「快取技術」。全是**不亂動前綴**的紀律。

## Pi 的哲學：核心夠輕，能力自己往上加

回過頭看，前面五條其實是同一個決定在不同位置的投影：Pi 的核心刻意維持很薄，不內建任何「看起來有用」的東西。但現在生態在長——sub-agent、sandbox、memory、plan mode、remote session，這些功能一個個出現，社群的討論就變成「Pi 要不要把這個加進去」。

這個問題問法就有點偏了。真正該問的是：這件能力該放在哪一層？我把它拆成三層：

**基礎能力，進 Core。** 沒有就跑不起來的那些——session 管理、context 組裝、tool call 循環、compaction。Pi 的 Core 目前做的全是這一層，而且做得很乾淨。

**規則和標準，Core 定底線。** 權限模型、remote session 的協定、sub-agent 之間的通信格式。這一層如果交給每個 extension 自己設計，結果就是每個專案一套規格，生態越長越碎。Pi 至少得把介面和最小協定定出來，實現可以百花齊放，但話語要統一。

**玩法，永遠留給 Extension。** memory 用檔案還是用向量庫、plan mode 幾步走、sub-agent 怎麼分工、搜索工具用哪個——這些是偏好的問題，不是能力的問題。我的立場很明確：這些 Pi 永遠不該替用戶決定，今天不該加，三年後也不該加。

翻遍 Pi 的官方文件和幾個主要 extension 的 README，這個分層不是我的腦補——官方的態度就是「不需要的功能不进 core」。這也解釋了為什麼前面那五個機制能存在：預設工具敢只留 4 個，就是因為它不把「多」當目標。一句話講完就是：能用 extension 解決的，不去動核心。這也是 Pi 最難守住的地方——功能請求只會越來越 loud，守住「不加」比做出功能需要更大的定力。

## Pi 的上下文是怎麼運作的

五個機制講的是「每一次請求」，這節講底下的資料結構。

**Session 是一棵 append-only 的樹，不是線性對話。** 存檔是 JSONL，每一行一個 entry，用 id/parentId 串成一棵樹。正常對話就是一直 append；用 /tree 可以回到前面的 entry 開一個 branch，同一個 session 檔裡同時存在多條工作線，不用另存新檔。這個結構是前面五個機制的物理基礎：cache 前綴永遠只加不改，壓縮也不用動舊資料。

**視窗管理是兩個數字。** 模型視窗的 16,384 tokens 預留給 LLM 回應（context 超過「視窗 − 16,384」就觸發壓縮），另外 20,000 tokens 是壓縮時保留的「最近訊息」額度。兩個都可以在 settings 調。所以 Pi 的 context 不是「滿了才管」，是留了 buffer 才動。

**換 branch 有第二種摘要。** /tree 跳到另一個 branch 時，Pi 會問你要不要把離開的那條 branch 總結成一段 context 帶過去（可以關）。同一套結構化格式、同一套檔案追蹤。所以「記憶」在 Pi 裡不是線性的對話摘要，是**樹上每個分岔口都可以存一份結構化狀態**。

## compact 的運作原理

/context 滿了（或手動 /compact）之後，實際發生什麼：

1. **找切點。** 從最新訊息往回數，數到 20,000 tokens 畫一條線。切點只能落在 user 訊息、assistant 訊息、bash 執行、或 custom 訊息上——不能切在 tool result 中間（它必須跟它的 tool call 留在同一邊）。切線前面是要總結的舊訊息，後面是原樣保留的最近訊息。
2. **生成結構化摘要。** 舊訊息先序列化（tool result 砍到 2,000 字，因為 read 和 bash 的輸出通常是 context 裡最大的一塊），然後叫 LLM 用固定格式填：Goal、Constraints、Progress（Done / In Progress / Blocked）、Key Decisions、Next Steps、Critical Context，加上兩段清單——讀過哪些檔案、改過哪些檔案。
3. **摘要回寫成一個新 entry。** 不是改舊資料，是 append 一個 CompactionEntry。下一輪請求送給 LLM 的是：system prompt + 摘要 + 切點之後的訊息。被壓掉的舊訊息沒有消失，還完整躺在 JSONL 檔裡，只是不在送出的 context 裡面。
4. **重複壓縮是迭代的。** 第二次壓縮時，上一次的摘要會當作 input 傳進去，新摘要是「舊摘要 + 新舊訊息」再壓一次。檔案追蹤也是累積的——每次把前一次摘要裡的 read/modified 清單併進來，所以壓了五輪，「這個 session 動過哪些檔案」不會斷。
5. **摘要請求本身不進主 session 的 cache。** 用新的 routing session，provider 有支援時關閉 cache write。一次性 prompt 不該佔 cache——這就是第五個機制在實務上的樣子。

一個容易漏的細節：單一輪對話如果本身就超過 20,000 tokens（例如一次 read 了幾千行的檔案），切點會落在這一輪中間，Pi 會生成兩份摘要再合併——一份給之前历史，一份給這一輪的開頭。所以不會出現「整輪都壓沒了，agent 完全不知道那輪發生過什麼」。

## 生態裡的五種壓縮路線

內建的 compaction 是最被動的一種：等 context 滿了才動。生態裡長出了另外 5 種思路。我沒有全部找到對應的 repo（有些名字在 GitHub 上搜不到確切專案），所以只講思路分層，不掛連結。它們暴露了一個根本問題：**Agent 的記憶，到底應該長什麼樣子。**

| 路線 | 做法 | 對「記憶」的假設 |
|------|------|-----------------|
| 遺忘派（pai-acp 思路） | 不等 context 滿，agent 自己判斷哪些歷史沒價值了，提前壓掉；需要時可搜索、可恢復 | 記憶應該像人類一樣主動遺忘，遺忘本身是功能不是缺陷 |
| 備忘錄派（pi-smart-compact 思路） | 壓縮時重點保留：當前目標、改過的檔案、錯誤、關鍵決策、未完成事項 | 記憶的本質是工作狀態（working state），不是對話摘要 |
| 版本控制派（pi-context 思路） | 把 context 當 Git 管：主動 checkpoint、看 timeline、選擇性 compact | 記憶應該可回溯、可 diff、可 revert |
| 入口過濾派（Hypa 思路） | 最好的壓縮是從一開始不讓垃圾進 context | 壓縮是後處理，過濾是前處理；前處理便宜得多 |
| 前置異步派（pi-press 思路） | 接近 threshold 時提前生成摘要，真正要 compact 時直接切換，壓縮對 agent 無感知 | 壓縮的延遲本身就是成本，該預先吸收 |

（補充一個我查到的：GitHub 上 star 最多的 pi-vcc，267 stars，走的是第六條路——完全不用 LLM 做總結，純抽取加格式化，號稱 lossless。思路是「總結必然有損，那就不總結，只重排」。）

五種路線沒有誰對誰錯。它們的分歧點不在工程，在一個更基本的問題：**agent 在壓縮之後「記得」的，應該是什麼？** 對話的內容？工作的狀態？可回溯的歷史？這跟我之前寫 [agent memory benchmark 的 Rashomon 現象](/agent-memory-benchmark-rashomon-filesystem-wiki/) 是同一個未解題：你問五個人「agent 記住了什麼」，會得到五個答案。現在答案變成五個路線，而且五個都能跑。

選的時候要有主次：入口過濾（少塞垃圾）是底層，備忘錄（保留工作狀態）是主壓縮策略，版本控制（可回溯）是安全網。前置異步和遺忘派是調優層。全裝上會打架——兩個都在「決定保留什麼」的插件，會互相覆蓋。

## 結語

**Pi 沒有什麼黑魔法，它的強是「少」。** 預設工具少、prompt 薄、context 只加不改、skill 按需、壓縮不污染 cache——五條全是紀律，不是技術。這解釋了為什麼「換成大家都推薦的 pi 就突然強很多」：換的不只是介面，是每一輪請求送進模型的東西變乾淨了，同一個模型自然表現得好。

但要把 99.93% 當 Pi 的護城河之前，先想兩件事。第一，這個數字是 DeepSeek 和 Pi 的乘積——DeepSeek 的 disk KV cache 讓 cache 存活以天計，換成 Anthropic 5 分鐘 TTL 的 prompt cache，差距會被 TTL 重寫的頻率吃掉一大塊。第二，qwen-code 加了一個工具動態載入的功能，token 總量少了 46%，帳單反而變成 $1.05 到 $3.30——因為每個 request 的前綴不再相同，hit rate 從 97.5% 掉到 81.5%。省 token 的優化，做成了燒錢的優化。

所以真正的結論只有一句：**前綴穩定是所有 harness 都該守的紀律，Pi 只是目前守得最徹底的那個。** 選 agent 的時候，把 cache hit rate 跟模型智力分並列——這個數字不寫在 leaderboard 上，要自己拉 log 看。Pi 的 footer 直接給（cache read / write / 當次 hit rate），Claude Code 的 log 在 `~/.claude/projects/` 底下，我之前那篇 [17 億 token 成本拆解](/ai-coding-token-cost-calculation-cache-read/) 有方法。

---

## 常見問題 Q&A

**Q: 我用 Claude（Anthropic API），Pi 的優勢還成立嗎？**

方向成立，幅度收斂。Anthropic 的 prompt cache TTL 是 5 分鐘，離線吃飯回來前綴就斷，hit rate 的天花板比 DeepSeek 低。但前綴穩定的紀律依然省錢——斷了之後重寫的 cost 低，且斷的頻率低。要自己拉 log 看實際 hit rate，不要直接套 99.93%。

**Q: 94-97% 的「其他 harness」，具體指誰？**

我的理解是「預設工具多、前綴常動」的那類（工具開場全宣告、每輪重新組 prompt 的）。不是說哪一家做不好，是說這個指標要逐家測，不該預設。

**Q: /compact 和 /tree 會互相干擾嗎？**

不會。兩者都只 append 新 entry（CompactionEntry 或 BranchSummaryEntry），不改舊資料。摘要會互相引用——branch summary 可以壓一個已 compaction 過的 branch，檔案追蹤也是累積併入。完整歷史永遠在 JSONL 檔裡。

**Q: 五種壓縮路線可以疊著用嗎？**

可以，但要有主次，上面已經講過：入口過濾是底層，備忘錄是主策略，版本控制是安全網，前置異步和遺忘派是調優層。兩個都在「決定保留什麼」的插件裝一起會互相覆蓋。

**Q: 我該不該從訂閱轉 API？**

看 API 等值。我 8 月底那篇算過：我的 API 帳單 $631-681 一個月，對 $200 訂閱，超過三倍，訂閱划算。你的算法一樣——拉兩週 log，用牌價重算，低於訂閱價就 API，高於三倍就訂閱，中間看你要不要額度上限的確定性。

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
