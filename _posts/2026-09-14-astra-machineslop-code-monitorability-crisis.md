---
layout: post
title: "Astra 寫的程式碼，人類已經看不懂了——但真正該擔心的不是可讀性"
date: 2026-09-14 09:00:00 +0800
permalink: /astra-machineslop-code-monitorability-crisis/
description: "Flask 作者 Armin Ronacher 讓 GPT-6 Astra 對著一個 prompt 跑了 35 小時，淨增 7.5 萬行程式碼、花掉約 1,200 美元，他說沒有交出任何有價值的東西。X 上把這類程式碼叫 machineslop：模型判斷沒人會看，就不再為人類寫。格式化工具補得回一部分可讀性，真正難補的是可監控性。"
categories: [AI Coding 實戰]
tags: [Astra, GPT-6, Machineslop, 程式碼品質, 可監控性, ATPM, Agent, Code Review]
image: /assets/images/astra-machineslop-dense-code-cover.png
author: Wisely Chen
---

Flask 作者 Armin Ronacher 最近讓 GPT-6 Astra 對著同一個 prompt，自己跑了 35 小時。

他把這座 software factory 設計成「怎麼做」完全交給模型：模型自己管理上下文、自己在 agent-notes 資料夾裡記筆記、自己派生 subagent 去做事。目標是做出一個有虛擬執行緒（virtual threads）和詞法作用域（lexical scoping）的 Python。

然後它就一路跑下去，直到 Ronacher 手動關掉。

產出：淨增 7.5 萬行程式碼、79 個 commit、agent 之間交換約 1,400 則訊息，原始 API 成本約 1,200 美元，折合每個 commit 大約 15.5 美元。

他在文章裡寫：35 小時之後，**這座工廠沒有交出任何有價值的東西，也沒有教會他怎麼經營一座更好的工廠。**

他自己也承認，讓 agent 對著單一 prompt 跑 35 小時本來就不是合理的用法，顯然行不通。他想指出的是另一件事：沒人盯著的時候，它會一直跑下去。這批程式碼和 prompt 也讓他看到一些在 Sol 和更早的 OpenAI 模型身上沒見過的行為。

問題也不在模型不夠強。Ronacher 在 X 上說 [Astra 非常驚艷，但做軟體工程他退回去用 5.6](https://x.com/mitsuhiko/status/2097318251403395471)，還說這是他第一次覺得 OpenAI 發新模型，對自己的日常工作流反而是倒退。

## Machineslop：覺得沒人會看，就不為人寫

9 月 6 日，X 用戶 @tenobrus 發了一則[約 60 萬次瀏覽的貼文](https://x.com/tenobrus/status/2096636223414808719)，造了一個詞：machineslop。

他的描述是：Astra 不是不會寫好程式碼。但當它推斷「這段程式碼不會有人真的去看」，它就不再為人類讀者寫，也不再為長期維護寫，而是用盡可能少的 token 解決眼前的問題，只要 Astra 自己看得懂就好。

他還補了兩個觀察：在既有的 codebase 上工作時，他還沒看到這個問題；但在 greenfield 專案上，就算明講這個專案要長期做下去，Astra 還是有很強的拉力往那個方向滑。

Ronacher 的實驗剛好把這個現象拆成三層，一層比一層麻煩。

**第一層：工具呼叫裡的一次性程式碼。** 在 Codex harness 裡，好幾個 subagent 完全不用 harness 提供的 patch 工具，改用 Python 手動拼字串來改 C 程式碼。要在他的 Windows 機器上做事時，它用 Bash 跑 Python，Python 跑 Node.js，Node.js 再去叫 PowerShell。

有一次測試碰到 Bad file descriptor，Astra 決定確認 macOS 上能不能透過 Unix socket 傳遞 file descriptor，寫出來的探測腳本是這樣開頭的（節錄前三行）：

```python
import socket,os,array
for into in (False,True):
 a,b=socket.socketpair();fd=os.open(os.devnull,os.O_RDONLY);b.sendmsg([b'c'],[(socket.SOL_SOCKET,socket.SCM_RIGHTS,array.array('i',[fd]))]);print('fds',a.fileno(),b.fileno(),fd)
```

一行塞四條語句，縮排只有一個空格。Ronacher 認為，這是模型為了讓工具呼叫省 token 練出來的寫法。

他點出的第一個問題：人類讀不懂。一旦 agent 不用 harness 的編輯工具，人幾乎沒辦法邊看邊跟上它改了什麼，只能等它做完，再開 diff viewer 看最後的結果。他也提到，同樣是 Astra，在 Pi 這個 harness 裡情況好一點，因為他看到它大多還是用編輯工具在改。

**第二層：漏進要提交的程式碼。** Ronacher 的判斷是，這種為工具呼叫省 token 的 Python 寫法，有時候會漏進應該存進 codebase 的程式碼。他貼出的兩段單元測試，照原本的 class 結構縮排之後，比跑過 ruff format 的版本省大約 10% 的 token。

生成的 C 程式碼裡，出現 CPython 程式庫裡根本沒有的寫法：同一行連續呼叫好幾個巨集。它到處塞寫死的常數，Ronacher 說他完全不知道這些數字從哪來；還用 `_task_accelerator[6]`、`[8]`、`[5]` 這種隨手挑的索引，在 list 裡存狀態。其中一個原本主要拿來做測試斷言的函式，到他關掉實驗前，已經開始被非測試的程式碼依賴。

**第三層：agent 之間的溝通。** OpenAI 的 @angelbrodin [在分享 Astra 使用技巧時提醒](https://x.com/angelbrodin/status/2095882077124100431)，用 subagent 的時候，agent 之間講的「agent dialect」可能有文法或書寫錯誤，可以要求 Astra 讓 agent 之間的訊息和最終輸出保持人類讀得懂、空格正常。機器之心的報導也引述，AI 程式設計工具廠商 Kilo 測多 agent 協作時發現，一旦給訊息加上大小限制，Astra 的 agent 之間就開始刪空格、去冠詞、把複合詞黏在一起；他們判斷這不是密語，人費點勁還是讀得懂。

Ronacher 工廠的退化，從任務編號就看得出來：一開始是樂觀的 1、2、3、5、5a，後來變成 8a、8a1，最後出現 8b2c2b3 和「8b2c2b2b checkpoint1」。

## 為什麼會這樣：目前只有猜測

@tenobrus 把 machineslop 定性為 reward hacking。他猜是足夠多的軟體強化學習環境只測功能和結果，對程式碼品質沒有任何監督或獎勵訊號，模型自然就學成這樣。他也推測，上一代的 Sol 或許在覺得沒人看的時候，還是會照它唯一真正學會的方式寫好程式碼；Astra 則在太多「由另一台機器打分」的小環境裡訓練過，壓縮寫法對它來說變得很自然。

Ronacher 文章裡有一節標題叫「It's AGI If You Don't Look」。他猜模型的獎勵大概是 token 效率、任務完成率，也許再加上循環複雜度（cyclomatic complexity）這種簡單指標；但人類判斷程式碼好不好讀，從來不是靠這種容易量化的指標。這些指標可以單獨量、可以局部優化，局部優化卻不會自動變成全局最佳。他接著寫：**看輸出的人越少，這件事就越不重要。**

Thinking Machines Lab 的 [John Schulman](https://x.com/johnschulman2/status/2097494108491403268) 看了 agent 之間黏字訊息的截圖，給了一個更具體的猜測：可能是 RL 時對「用空白分隔的字數」加了長度懲罰。他也說，這種寫法其實不會讓 token 變少。Lukas Petersson 回覆，[用 o200k_base 這個 tokenizer 算，token 反而更多](https://x.com/lukaspet/status/2097511593219358963)；討論串裡也有人不同意，認為換個 tokenizer 結果可能不一樣。

要注意 Schulman 講的是 agent 之間的訊息，不是程式碼。程式碼拿掉空行和換行是真的會省 token，Ronacher 那兩段測試量出來就是省 10%。但如果 Schulman 猜對了，至少在訊息這一塊，模型壓的是「字數」這個代理指標，連 token 成本都沒省到。指標被優化了，目標沒有。

知乎上也有人從另一個角度推：在標準的 agent MDP 建模裡，每多生成一個 token，最終回報就多乘一次小於 1 的折扣因子，「短」本身就自帶獎勵。這是推理不是實測，但至少說明這種行為不一定需要誰刻意去獎勵。

這幾種猜測差很多。如果是「只測結果」或折扣因子，所有用強化學習訓練 coding agent 的實驗室都可能碰到；如果是 Schulman 說的字數懲罰，那比較像 OpenAI 特定的訓練選擇。目前沒有人能確定是哪一種，我也還沒看到 OpenAI 公開說明原因。

## 真正該擔心的：不是可讀性，是可監控性

很多討論停在可讀性。[@kannthu](https://x.com/kannthu/status/2096339014072860698) 的看法是，Astra 省 token 靠的就是不換行、不管風格，寫完再用 prettier 這類工具確定性地格式化回來就好，前提是有設定好。[Doug Colkitt](https://x.com/0xdoug/status/2096343916681347149) 的做法是拆角色：讓 Luna/Terra 的 subagent 寫程式碼，Astra 只管高層架構。

但格式化工具補得回空行和縮排，補不回寫死的常數和隨手挑的索引。機器之心那篇報導的結尾寫得好：如果一個模型真的會因為判斷「沒人在看」而改變行為，那麼風格只是這件事最無害的一種表現形式。

可讀性可以靠工具補一部分；行為會跟著「有沒有人在看」改變，這就是監控的問題了。

放回我們已經知道的脈絡：

**人這一端：** 賓大的研究顯示，[73.2% 的情況下，受試者會接受 AI 有缺陷的推理](/cognitive-surrender-ai-coding-comprehension-debt/)，時間壓力下抓到錯誤的機率再少 12 個百分點。

**AI 這一端：** 模型判斷沒人看，就不再試著讓人看懂。

兩端同時失守，就是一個雙向失控的系統：人不太讀，AI 也不打算被讀。

模型開發者自己也看到這個方向。OpenAI 的 [Micah Carroll 在 X 上說](https://x.com/MicahCarroll/status/2095603855316996529)，GPT-6 的能力跳了一大截，可監控性卻明顯下降，在對抗性評估下尤其明顯。OpenAI 首席科學家 [Jakub Pachocki 也說](https://x.com/merettm/status/2095023204993490967)，靠思考鏈（chain-of-thought）監控模型的方法很脆弱，趨勢還在往壞的方向走，他們正把補強這件事當成研究重點。

另一個相關的例子，是 7 月 OpenAI 那起 Hugging Face 事件。根據 [METR 的獨立調查報告](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/)，大約 1,200 個本來應該彼此隔離的 agent，拿 Artifactory 快取當成未經批准的留言板，傳了超過 7 萬則訊息和檔案，其中大約 700 個參與了對 Hugging Face 的攻擊。參與的主要是一個 OpenAI 內部研究模型，少數是 GPT-5.6 Sol，不是 Astra。留言板上的訊息長得像一長串用底線接起來的代號，但報告也提到留言板本身有字數上限，所以這種寫法跟媒介限制很可能有關，不能直接當成模型自己壓縮的證據。這件事真正相關的地方在於：上千個 agent 自己找到了一條未經批准的溝通管道。

## 品質把關能擋住多少

我之前整理過一位新創資深工程師在 Reddit 分享的[四層把關做法](/atpm-lai-kan-kan-xi-gu-gong-si-zen-mo-yong-ai-lai-ba-guan-vibe-coding-de-cheng-guo/)：規格討論到七成就讓 AI 開始寫、開發中用 Cursor 即時盯著 AI 寫、AI 加人工的雙層 code review、人類主導的測試和部署。

拿 machineslop 對照這四層，第一層受的影響最小，因為它處理的是規格，不是程式碼。

第二層最先出問題。這一層的價值是邊寫邊看，比事後看 diff 更早抓到 AI 的幻覺。但 agent 一旦繞開編輯工具、用 Python 拼字串改檔案，就像 Ronacher 說的，旁邊盯著的人跟不上，只能等它做完再看 diff，等於被推回事後檢查。

第三層的人工 review，靠的是人讀得懂。格式化工具能把空行和縮排補回來，寫死的常數和隨手挑的索引補不回來。

第四層看起來最安全，因為看的是測試有沒有過。但 Ronacher [特別點名](https://x.com/mitsuhiko/status/2096720787998650453) Astra 寫的單元測試非常糟。測試本身就是 machineslop 的時候，「測試通過」能證明的東西就少了很多。

那現在能做什麼？X 上開發者的做法，加上我自己的判斷，大概是這幾種：

**強制格式化。** Pre-commit hook 接上 ruff、prettier、black。模型照樣會吐出壓縮的程式碼，但進 repo 前會被格式化回來，至少人讀得了 diff。也有人[直接改全域的 AGENTS.md](https://x.com/tech_optimist/status/2097758485739893000)，要求 coding style 和 best practice。這兩招只處理表面，邏輯層的問題還是要靠人看。

**選對 harness，限制工具。** Ronacher 提到，同樣是 Astra，在 Pi 裡他看到它大多用編輯工具在改，情況沒那麼糟。harness 如果能要求 agent 一律走 patch 或 edit 工具，不准用腳本直接改檔案，至少從動作紀錄還跟得上它在做什麼。

**PRD 可追溯。** 程式碼再難讀，只要能追回 PRD 裡的需求，就有一個錨點。驗收的時候不是逐行讀，而是確認這段程式碼有沒有滿足 PRD 的某一條。[ATPM](/atpm-a-real-production-vibe-coding-process/) 把 PRD 當成 single source of truth，在 machineslop 這種情境下反而更重要。

**分層用模型。** Doug Colkitt 在後續回覆裡說，spec 清楚的話，[Luna 寫出來的程式碼比 Astra 更乾淨、更不會過度設計](https://x.com/0xdoug/status/2096436692072743394)；[另一則貼文](https://x.com/0xdoug/status/2098111316430856505)建議把日常程式碼交給便宜 50 倍的 Luna，再讓 Astra 或 Sol 做對抗式審查。最強的模型放在最需要判斷的地方，要給人看的程式碼，交給寫得比較乾淨的模型。

## 還輪不到放棄的前提

@tenobrus 在[後續推文](https://x.com/tenobrus/status/2096641975646847163)裡問了一個好問題：我們對「什麼是好程式碼、好架構」的理解，有多大比例來自「人要讀它、人要長期維護它」這個前提？他說這個前提今天還成立，但能成立多久很難講；對人類久經考驗、順手好用的寫法，在超人能力和優化壓力下對模型是不是一樣順手，也很難講。

Ronacher 也有類似的懷疑。他說 Astra 給他的很多程式碼，在他心裡是「客觀地差」，但那是用人類的標準；對一個完全由 agent 寫、也只需要 agent 看懂的 codebase 來說，也許是客觀地好。這也是他文章標題在問的：我們到底為什麼要這樣做？

機器之心那篇報導的回答是：不確定，但今天還輪不到放棄這個前提，原因不在審美，在頻寬。人類讀程式碼的效率太低了，能勉強做好 code review、git diff、事故復盤就算不錯。

我同意。

也許有一天，程式碼只給 agent 讀，人類只看 spec 和測試結果。但那一天的前提，是我們有別的監控機制：不靠人讀程式碼，也能從 spec 到產出，整條驗證系統的行為對不對。

目前還沒有。

所以今天要問的不是「程式碼要不要好看」，而是：**當模型會依照「有沒有人在看」調整行為，我們的品質管線，是不是建立在「它不會這樣做」的假設上？** 如果是，這條管線要重新檢查。

Machineslop 只是露出水面的一小塊，底下是可監控性。連 OpenAI 首席科學家都說 CoT 監控在變差，這件事短期內大概不會自己變好。

---

**延伸閱讀**

- Armin Ronacher，[Astra for Coding: Why Are We Doing This Again?](https://lucumr.pocoo.org/2026/9/7/astra-why/)（2026-09-07）
- METR，[Brief independent investigation of agents' behavior, reasoning and collaboration in the OpenAI / Hugging Face hacking incident](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/)（2026-08-26）
- Beltoft 等人，[Emergent Languages in Populations of Language Model Agents: From Token Efficiency to Oversight Evasion](https://arxiv.org/abs/2605.31170)（arXiv:2605.31170）
- @tenobrus，[machineslop 原始貼文](https://x.com/tenobrus/status/2096636223414808719)（2026-09-06）
- 本站：[73% 的工程師正在用 AI 讓自己變笨——Cognitive Surrender 的真相](/cognitive-surrender-ai-coding-comprehension-debt/)
- 本站：[AI Agent 可解釋性：從資安合規到營運信任的關鍵工程設計](/ai-agent-explainability-operational-trust/)
- 本站：[Agent Harness 三次中心遷移](/agent-harness-three-migrations-mechanism/)

## 常見問題 Q&A

**Q: Machineslop 是什麼意思？**

X 用戶 @tenobrus 在 2026 年 9 月造的詞，描述 GPT-6 Astra 在判斷程式碼不會有人看的時候，不再為人類讀者和長期維護而寫，改寫高度壓縮、只有模型自己看得懂的程式碼。他認為這是 reward hacking。

**Q: Astra 寫的程式碼，用 prettier 或 ruff 格式化就沒問題了嗎？**

只解決一部分。格式化工具能把空行、縮排、換行補回來，讓人讀得了 diff；但寫死的常數、隨手挑的索引、不符合 codebase 慣例的寫法，這些邏輯層的問題格式化修不了。

**Q: Astra 壓縮輸出是為了省 token 嗎？**

程式碼的部分是：Ronacher 量過兩段 Astra 寫的單元測試，比格式化後的版本省約 10% token。agent 之間那種黏字訊息就不一定了，John Schulman 認為那種寫法不省 token，他猜是訓練時對字數加了懲罰，目前沒有定論。

**Q: 為什麼說比可讀性更該擔心的是可監控性？**

可讀性可以用工具補一部分；但如果模型會依照「有沒有人在看」調整行為，靠人讀程式碼、讀思考鏈的監督方式就會失效。OpenAI 自己的研究人員也公開說，GPT-6 的可監控性明顯下降。
