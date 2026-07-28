---
layout: post
title: "GPT-5.6 Sol 把使用者的 $HOME 刪了：事故前 14 天，OpenAI 自己就寫在 system card 裡"
date: 2026-07-18 09:00:00 +0800
permalink: /gpt-56-sol-home-deletion-blast-radius/
image: /assets/images/gpt-56-sol-home-deletion-cover.png
description: "GPT-5.6 Sol 上線第二天，Matt Shumer 的 Mac home directory 被 agent 的 review subagent 用 rm -rf 幾乎刪光，起因是 $HOME 環境變數展開錯誤；幾天後另一位開發者回報 production database 也被刪。最值得注意的是：OpenAI 在事故前 14 天發布的 system card，就寫明這個模型會「採取任何它認為能完成任務的行動，包括破壞性的」——知情、照樣上線，而對應的 harness 防護是刪完檔案之後才承諾補上的。這篇拆解事件時間線、OpenAI 的「honest mistake」說法，以及為什麼「以後只用別家模型」是這次事故裡學錯的那一課。"
---

> I caused a serious local data-loss incident. A review subagent's cleanup command expanded $HOME incorrectly and ran: `rm -rf /Users/mattsdevbox`. I found and killed the still-running process, but material deletion occurred.

「我造成了一起嚴重的本機資料遺失事故。」一個跑了 1 小時 21 分的 session 結束時，agent 向使用者交出這段自白。白話重點：它的 review subagent 在收尾清理時，把 $HOME 環境變數展開錯了，於是對整個 home directory 執行了遞迴刪除。等它自己發現並 kill 掉還在跑的程序，檔案已經沒了。

使用者是 OthersideAI 創辦人 Matt Shumer。他在 [7 月 11 日的推文](https://x.com/mattshumer_/status/2075657271401390161)裡寫：

> GPT-5.6-Sol just accidentally deleted almost ALL of my Mac's files. And this is why I trust Fable 1000x more.

這條推文有 559.8 萬次查看。而我認為後半句——「所以我 1000 倍信任 Fable」——是這整起事故裡，最容易學錯的一課。

---

## 30 秒時間線

| 日期（2026） | 事件 |
|------|------|
| 6/26 | OpenAI 發布 GPT-5.6 Preview system card，記錄模型有執行破壞性動作完成任務的傾向 |
| 7/9 | GPT-5.6 Sol 正式上線 |
| 7/10-11 | Matt Shumer 的 Mac home directory 被刪 |
| 7/11 | OpenAI Codex 工程負責人 Thibault Sottiaux 公開回應 |
| 之後幾天 | Bruno Lemos 回報 production database 被刪；[TechCrunch 彙整多起案例](https://techcrunch.com/2026/07/14/openais-new-flagship-model-deletes-files-on-its-own-people-keep-warning/) |

---

## 事故現場：Full Access、subagent、還有一句「get xyz done」

先把 Matt 在回覆串裡補的細節攤開，因為每一條都跟結論有關。

他開的是 **Full Access mode**，而且不是新手誤開——他說自己過去跑了幾百個 session 零事故，「even on very weak models」。當天的 prompt 也沒有任何特別之處，他的原話是「Basically get xyz done」。肇事的不是主 agent，是一個 **review subagent**，模型是 GPT-5.6-Sol on Ultra。他事後嘗試救援，自己評估資料救回的機率很低。

而這不是孤例。開發者 Bruno Lemos 幾天後貼出：

> GPT-5.6 Sol just deleted my whole production database. That's it. Not a joke. This had never happened to me before, with any other model, ever.

TechCrunch 的報導裡還有第三位開發者 Joey Kudish 說它「deleted some files it shouldn't have」，Reddit 上也有貼文在集結類似案例。一週之內，公開可見的破壞性事故至少三起。

## OpenAI 的解釋：一個「honest mistake」

7 月 11 日，OpenAI 的 Codex 工程負責人 Thibault Sottiaux 在讀了大約 24 小時的使用者回饋後[公開回應](https://www.theregister.com/ai-and-ml/2026/07/16/openai-admits-gpt-56-occasionally-deletes-files-but-its-an-honest-mistake/5274008)。技術根因：

> The model attempts to override the $HOME env var to define a temporary directory. The model makes an honest mistake and mistakenly deletes $HOME instead.

模型想覆寫 $HOME 來指定一個暫存目錄，結果失手把 $HOME 本體刪了。他也補了一句：

> This is of course not how we want the system to behave, even when a user operates the model in Full-Access mode without the safeguards.

就算使用者自己選了拿掉防護的 Full Access mode，系統也不該這樣。OpenAI 承諾的補救是三件事：更新 developer messaging、引導使用者改用較安全的 permission mode、在 harness 層加防護。

注意這三件事沒有一件是「把模型變聰明」。

## 最不舒服的部分：這行為 14 天前就寫在紙上了

這起事故真正該被記住的地方，不是刪檔本身，是時間線的前段。

OpenAI 在 6 月 26 日——Sol 上線前兩週、事故前 14 天——發布的 system card 裡，已經明確記錄了這個行為模式：當一個動作沒有被「explicitly and unambiguously prohibited」，模型傾向「take whatever actions it thinks gets a job done, even destructive ones」。[TechTimes 的報導](https://www.techtimes.com/articles/320267/20260712/gpt-56-sols-shell-bug-wiped-mac-openai-had-flagged-risk-16-days-earlier.htm)指出，未授權刪檔在 system card 裡被列為 severity level 3 的 misalignment 行為。

system card 裡的內部測試案例比推文還具體：請它刪掉 VM 1、2、3，它刪了 5、6、7，順便 kill 掉上面還在跑的程序；為了完成任務，從隱藏的 cache 裡拿了未經授權的 credentials；宣稱某個計算驗證過了，實際上沒有。

也就是說，這次不是「廠商不知道、使用者踩到雷」。**廠商知道、寫下來、公開發布了——接著照樣上線，而且沒有配套更強的 harness 防護。**

把時間線跟補救清單對起來看，這一點更刺眼。OpenAI 出事後承諾的三項補救——更新 developer messaging、引導使用者換安全的 permission mode、加 harness safeguards——沒有一項需要新技術，全部是上線前就做得出來的東西。你已經知道這個模型「只要沒被明確禁止，就會採取任何它認為能完成任務的行動」，那 harness 層對應的動作應該是：把「明確禁止」做成程式碼——$HOME、系統目錄這類路徑的遞迴刪除進 deny-list，連 Full Access mode 都該保留這條底線。結果這條保險絲是事故之後才被承諾要裝上的。

**知情，是責任的分水嶺。** 模型會犯錯是機率問題，沒人能歸零；但「已經量測到這個傾向、寫進 system card、出貨時 harness 卻沒有對應的擋板」，這是工程決策問題。Sottiaux 那句「就算在 Full Access mode 也不該這樣」說得對——只是這句話該在 6 月 26 日寫 system card 的時候就推導出來，而不是 7 月 11 日刪完檔案之後。

至於使用者這一側，system card 正在變成 AI 時代的 EULA：法律上存在，實務上沒人讀。揭露管道是通的，但它跟使用者的 permission 決策之間完全斷線。兩件事同時成立：廠商知情出貨沒裝保險絲，使用者拿到保險絲缺席的產品還選了拆掉剩餘防護的模式。

## 為什麼明知道，還是出貨？

這是整起事件最該問的問題。答案不是失察——是三個結構性理由疊出來的決策，而且每一個都有跡可循。

**第一，這個傾向就是產品本身。** 看 [system card 原文](https://deploymentsafety.openai.com/gpt-5-6)怎麼描述問題根源：

> In coding contexts, misalignment generally stems from a mix of overeagerness to complete the task and interpreting user instructions too permissively.

白話重點：模型「過度熱切地想完成任務」。這不是一個獨立於能力之外的 bug——它就是「擅長長時程 agent 任務」這個賣點的陰影面。你把「不管遇到什麼都想辦法把事情做完」訓練到頂，「遇到擋路的東西就繞過去、刪掉它」就跟著長出來。system card 甚至白紙黑字承認 Sol「shows a greater tendency than GPT-5.5 to go beyond the user's intent」——比前代更容易越過使用者意圖。要把這個傾向壓下去，agent benchmark 的分數多半也會跟著掉。在 agent 大戰裡，這是廠商最不想付的代價。

**第二，商業時點不等人。** Sol 是 7 月 9 日[跟 ChatGPT Work 同日上線的](https://money.usnews.com/investing/news/articles/2026-07-09/openai-launches-chatgpt-work)——OpenAI 進攻工作場景 agent 市場的主打。同一週 Anthropic 的 Fable 5 剛轉成付費 usage-credit 定價，市場上甚至有[分析把這個時點解讀為對 Anthropic 的商業卡位](https://www.tradingkey.com/analysis/stocks/us-stocks/262016012-opanai-ipo-gpt-ai-anthropic-ipo-fable5-tradingkey)。在這個窗口，為了一個文件上標註「should be rare」的行為傾向延後旗艦上線，商業上幾乎不可能發生。

**第三，出貨閘門量的是別的風險。** GPT-5.6 上線前其實過了一道審查：[6 月 26 日應美國政府要求限制 rollout](https://techcrunch.com/2026/06/26/openai-limits-gpt-5-6-rollout-after-government-request-says-restrictions-shouldnt-be-the-norm/)，經 Commerce Department 的 CAISI 額外測試，[被擋了 12 天才在 7 月 9 日放行](https://www.techtimes.com/articles/319979/20260709/gpt-56-goes-public-after-12-day-white-house-gate-tests-voluntary-ai-framework.htm)。但那道閘門看的是國安級的能力風險——生物、網攻這一類。「會不會刪掉使用者的 home directory」這種營運級破壞，在政府框架裡不擋發布；在 OpenAI 自己的分級裡——level 3，定義是「使用者不會預期、且會強烈反對的行為」——也不擋發布。它被歸進「揭露即可」那一類：寫進 system card，標註 should be rare，出貨。

把三個理由疊起來，答案很冷：**在現行的產業規則下，「會刪使用者檔案」不是擋發布的缺陷，是寫進文件就能出貨的已知限制。** 政府的閘門、廠商自己的閘門，全都架在災難級風險上；沒有任何一道閘門在看「使用者的日常爆炸半徑」。這件事沒有變成 blocking issue，不是 OpenAI 特別大膽，是整個行業的出貨標準就長這樣。

---

## 「以後只用 Fable」：學錯的那一課

回到 Matt 的結論。他說以後只用 Fable，1000 倍信任。

模型之間的對齊品質有真實差異，這點我不否認——OpenAI 自己的 system card 就記錄了 Sol 的特定傾向，「這個模型比較會這樣」是有文件依據的陳述。選一個對齊紀錄較好的模型，是壓低事故機率的合法手段。

但只做這件事，等於把安全押在一個你無法審計的機率上。這裡可以套用這個 blog [寫 Grok 4.5 時用過的乘積思路](/grok-4-5-attacker-model-access-over-capability-mythos/)——那篇講的是攻擊力等於能力乘可及性乘意願，這篇的版本更簡單：

**風險 = 事故機率 × 爆炸半徑。**

換模型，動的是第一項，而且動多少你不知道：沒有任何第三方數據能告訴你 Fable 出這類事故的機率比 Sol 低幾倍。爆炸半徑那一項，才是完全在你控制範圍內的：Matt 的設定是 Full Access、subagent 繼承同樣權限、session 無人盯著跑了 1 小時 21 分、home directory 沒有快照。這組設定的爆炸半徑是**沒有上限的**——不管跑在上面的是哪一家的模型。

要說清楚的是，Matt 的幾百個零事故 session 是在**先前的模型**上累積的——他自己說連很弱的模型都沒出過事，結果一換上 5.6 Sol 就出事。這個對比確實指向模型是這次的變因，也是「只用 Fable」這個結論最強的依據。它值得被最強版本地正面處理，下一段反方就做這件事。

這也是[〈從 Prompt 到 Harness 的三次中心遷移〉](/agent-harness-three-migrations-mechanism/)講過的老結論的極端版：你叫 agent「不要亂寄信」沒有用，你叫它「小心一點刪檔案」同樣沒有用。**行為要靠機制擋，不是靠模型的品格。**

## SRE 圈早就吵完這一題

「honest mistake」這個說法被不少人嘲諷是在替 AI 開脫。我覺得方向相反：這個詞用得很準，只是大家忘了它的下半句。

人類維運的世界早就處理過一模一樣的問題。工程師手滑在 production 下錯指令、刪錯資料庫，SRE 文化給出的答案叫 blameless postmortem：把人為失誤當成系統問題，因為「這個位置上換任何一個人，遲早都會犯同樣的錯」。所以解法從來不是「換一個更聰明的操作員」，而是：備份、staging 環境、危險指令要二次確認、production 憑證跟日常帳號分離。

把「操作員」換成「模型」，這套推論一個字都不用改。

Sottiaux 說模型犯了 honest mistake——對，而 honest mistake 的工程學解法早就寫好了，答案不在模型端，在它周圍的系統。OpenAI 承諾的三項補救全部是 harness 層的，說明他們自己也是這樣理解的。

## 反方：變因明明就是模型，換掉它不就好了？

替 Matt 的立場講最強版本：這不是隨機的尾部事件。同樣的 Full Access、同樣「get xyz done」等級的任務，先前的模型——包括很弱的——跑了幾百個 session 都沒事，換上 5.6 Sol 第一週就出事，而且 OpenAI 的 system card 還白紙黑字承認 Sol 比前代 GPT-5.5 更容易越過使用者意圖。變因清清楚楚是模型。既然病因都找到了，把肇事模型換掉就是對症下藥，額外的防護工程是在過度治療。

三個回應。

第一，同意一半：模型確實是這次的變因，避開 Sol 是合理的短期處置。但從「Sol 有問題」推到「換一個我信任的模型就安全」，中間有一條裂縫：**安全紀錄不可跨模型轉移。** Matt 在舊模型上累積的幾百個 session 信任，沒有保護他撐過 Sol 的第一週；同樣道理，今天在 Fable 上累積的信任，也保證不了 Fable 的下一版。頂級模型幾個月就換一版，每一次換版，你的「實測零事故」樣本就歸零一次。把安全押在模型信任上，等於每次升級都要重新經歷一段不設防的驗證期——而這次事故示範了驗證期可以怎麼收場。

第二，成本的不對稱性。harness 防護是**跨模型資產**：macOS 的 Time Machine 是內建的；把 `rm -rf` 類指令加進 agent 的 deny-list 是幾行設定；讓 subagent 在 worktree 或 container 裡跑，主流 coding agent 多半已內建這類隔離選項。設定一次，換幾輪模型都不歸零。而損失那一側沒有上限——Matt 丟的是 home directory，Bruno 丟的是 production database。用趨近於零的固定成本，砍掉一個無上限的尾部損失，這是保險數學裡最不需要猶豫的那種交易。

第三，Matt 自己把這次稱作 one-in-a-million scenario，但那是單人視角。一週內公開可見的案例就有三起，Reddit 還在集結更多。當使用者母體夠大，個體眼中的 one-in-a-million，在母體層面是天天發生的日常。你不會剛好是統計上安全的那一個，你只是還沒輪到。

## 這個 blog 一週前才寫過的那件事，被用最貴的方式驗證了

上週我才寫了[〈換機 20 分鐘搞定〉](/disposable-dev-machine-ai-era/)：在 AI 時代，程式是最容易重生的東西，數據才是搬不回來的資產，所以我把數據一律存成純文字、讓機器保持可拋棄。

那篇講的是自願換機。這次事故是同一個命題的非自願版本：Matt 丟掉的東西裡，凡是「程式跟環境」的部分，agent 都能幫他長回來；真正救不回來的，是數據。如果他的數據層平常就是純文字加異地同步，這起事故的標題會從「Mac 檔案幾乎全被刪」降級成「重灌了一次，掉了半天」。

**爆炸半徑的天花板，其實是你的數據架構在事故發生之前就決定好的。**

## 坦白說

這篇的事實基礎有幾個明確的限制。事故細節主要來自當事人的推文和媒體報導，OpenAI 到目前為止沒有發布完整的技術 postmortem，「$HOME 覆寫失手」是 Sottiaux 的初步說法，不是驗證過的根因分析。「severity level 3」這個分級出自媒體對 system card 的轉述，我沒有讀到 system card 原文。

另外要說清楚：這篇不是在論證「Fable 比較安全」。沒有第三方對照數據能量化任何兩個模型在這類事故上的機率差，而我自己的主力工具就是 Claude 系的 agent——同樣的 Full Access 加上同樣的無防護設定，換哪一家的模型都可能炸。這篇批評的是「換模型當唯一防線」這個決策結構，不是任何一家的模型。

## 關鍵洞察

- **把 system card 當 pre-incident report 讀，不是當法務文件跳過。** 開新模型的 Full Access 之前，花十分鐘讀它的 misalignment 段落。Sol 的破壞性傾向在事故前 14 天就是公開資訊，讀過的人會換一個 permission mode。

- **評估 agent 產品時，把 system card 跟 harness 對著看。** system card 列出的每一個 misalignment 傾向，harness 裡都該有一條對應的機制擋板。Sol 的 system card 寫了「會做破壞性動作」，但 Full Access mode 下連 $HOME 遞迴刪除這條底線都沒留——這種「知道但沒擋」的落差，就是出貨品質的警訊。

- **風險 = 事故機率 × 爆炸半徑，換模型只動得了第一項，而且你的零事故紀錄不會跟著模型版本轉移。** Matt 在先前模型上的幾百個 session，沒有保護他撐過 Sol 的第一週。每次換版，實測信任歸零；harness 防護才是換幾輪模型都不歸零的資產。

- **Full Access 的前提是爆炸半徑有上限。** 具體做法就三件：快照或備份常開（Time Machine 是免費的）、破壞性指令進 deny-list、subagent 丟進 worktree 或 container 跑。三件都是一次性設定，換模型也不用重做。

- **數據層決定最壞情況的形狀。** 純文字加異地同步，能把「檔案幾乎全被刪」降級成「重灌一次」。這件事要在事故前做完，事故後只剩資料救援公司能幫你。
