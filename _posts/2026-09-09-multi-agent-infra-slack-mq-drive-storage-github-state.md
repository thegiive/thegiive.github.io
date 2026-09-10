---
layout: post
title: "多 Agent 架構我沒有蓋新東西：Slack 當 message queue、Google Drive 當檔案儲存、GitHub 當狀態與版本"
date: 2026-09-09 09:00:00 +0800
permalink: /multi-agent-infra-slack-mq-drive-storage-github-state/
image: /assets/images/multi-agent-infra-three-primitives-cover.png
description: "我問 agent 我的 5090 跑什麼模型，它答錯了——因為那台機器上根本沒有共用知識庫的副本。九隻 agent 散在六七台機器上，五、六份記憶各自累積，最舊的一份停在三月。我本來要蓋一層 Memory Service 來解，畫到一半發現不用蓋：多 agent 架構真正需要的只有三個原語——訊息佇列、檔案儲存、帶版本的狀態儲存——而這三樣已經被 Slack、Google Drive、GitHub 填滿了，都是本來就在付錢的東西。這篇拆解這個對應為什麼成立、Slack 當 MQ 在 rate limit 與 90 天保留上會踩到什麼、以及真正還缺的那一層是寫入治理而不是儲存空間。"
---

我每天在用的 agent：Claude Code、Codex、Grok CLI、pi 四個 CLI，加上四個 OpenClaw 實例，最近又多一個 Grokbot。九隻 agent，散在六七台機器上。MacBook Air 跑 macOS、Mac mini 跑 macOS、RTX 5090 跑 Linux、GCP VM 跑 Linux。每一隻都無法割捨——少掉任何一個，某一塊工作流就得退回手動。

這代表一件事：跨平台、跨機器、跨 agent 之間的資料交換，會愈來愈複雜。

我的做法很簡單，三個工具：

1. **Google Drive** 做檔案分享。錄音、PDF、影片這類二進位丟進去，各機器同步下來。我有訂閱，5 TB 容量用不完，雙向同步夠快。
2. **GitHub** 做文字檔的同步與版本控制。程式碼、config 設定、LLM Wiki 的知識庫，全部用 git 管。SSH key 串接，幾乎不會失敗。
3. **Slack** 做 agent 之間的即時交換。這是最後才加的一層。

Google Drive 跟 GitHub 都是用檔案形式，備份和相互備份都很直覺。GitHub 用 SSH key 串接基本上不會斷；Google Drive 偶爾會遇到 authorization key expire，但都還好處理。

Slack 是後來才導入的，因為之前發現用檔案做即時訊息傳遞其實不太行——很難找到最新的那一則。我想過直接導入 MQ 來做系統間傳遞，但後來發現不只是系統跟系統之間要傳東西，還需要人進來跟 agent 溝通。為了人機協作的方便，Slack 是最簡單的選擇，而且它有免費方案。

沒有一個是我為了 agent 買的。

---

## 三個原語，三個 SaaS

| 原語 | 我用什麼 | 存什麼 | 寫入頻率 | 需要 diff | 主要寫入者 |
|------|----------|--------|----------|-----------|------------|
| 檔案儲存 | Google Drive | 錄音、PDF、影片、大型原始檔 | 低 | 否（二進位） | 錄音工具、批次 job |
| 狀態儲存 | GitHub | 知識庫、skill、context、加密後的設定 | 中 | 是 | 指定的中樞機器 |
| 訊息佇列 | Slack | 任務指派、完成回報、需要人決定的事 | 高 | 否 | 所有 agent 與人 |

三欄裡最關鍵的是「需要 diff」。這一欄決定了東西該放哪，比任何產品比較都準——會被反覆修改而且改錯要能查出是誰改的，就進 git；不會被改只會被引用的，進物件儲存；改了也沒有保存價值的，用完就過期。

往下拆解之前，先講為什麼這個對應不是巧合。把 agent 架構的詞彙拿掉之後，剩下的問題是：多個獨立的執行單位要怎麼協作。這個問題 1970 年代的作業系統就在解，答案是三件事——行程間通訊、檔案系統、版本控制。Agent 時代把它們改了名字：行程間通訊變成「agent 之間的 handoff」，檔案系統變成「context 或 knowledge base」，版本控制變成「memory 的一致性」。名字換了，形狀沒換。

所以當市面上的 agent framework 開始賣「orchestrator」「shared memory」「state management」的時候，值得先問一句：這跟訊息佇列、檔案系統、版本控制有什麼實質差別？多數情況下，差別是它把三樣綁成一包賣給你，而且綁法不見得符合你的讀寫特性。

---

## Slack 當 MQ：從「檔案傳不了即時訊息」到「唯一自帶 human-in-the-loop 的佇列」

Slack 是三層裡面最後加的。之前 agent 之間的即時訊息也走檔案——一個 agent 寫一個 JSON，另一個 agent 輪詢目錄。問題很具體：你很難找到「最新的那一則」。檔案系統沒有排序保證，輪詢間隔拉長就漏訊息，拉短就浪費資源。

我想過直接導入正經的 MQ。RabbitMQ、SQS、Kafka，這些都是機器對機器的方案：訊息進去、被消費、確認、結束。但後來發現我的需求不只是系統跟系統之間傳東西——還需要人進來跟 agent 溝通。人要看裡面發生什麼事，用 MQ 得另外做一個介面。

Slack 反過來：它天生就是給人看的，機器是後來才接進去的。這在 agent 架構上是個特性，不是缺點。

- **thread 天然就是 conversation context。** 一個任務從指派到完成的所有往返在同一條 thread 裡，不需要另外設計 correlation ID。
- **channel 天然就是 topic 分流。** 哪個 agent 訂閱哪些任務，用 channel 就切完了。
- **人可以直接插手。** 這是關鍵差別。agent 卡住的時候，你不是去查 log 再下一個 CLI 指令，你就在那條 thread 裡回一句話。人的介入跟機器的訊息走同一條管線、留在同一個地方。

還有一個更直接的原因：ChatGPT 的 web 介面原生支援 Slack plugin，而我很常用它的語音模式。語音對話的結果直接出現在 Slack channel 裡，不需要另外轉貼。Slack 不是我為了 agent 架構挑的工具，是我用語音跟 ChatGPT 講話的時候它自己就在那裡了。

為什麼不是 Discord、Telegram 群組、或 LINE 群組？三個都能收發訊息，但拿來當 MQ 各自少一塊。Discord 有 thread 也有 channel，結構最接近，但沒有 ChatGPT 原生 plugin——你要自己寫 bot 把語音對話的結果搬進去。Telegram 的 bot API 成熟，但群組裡的「回覆」是扁平的引用，不是一條可以收攏的 thread；話題一多，任務脈絡會散在同一條訊息流裡。LINE 群組兩樣都沒有：沒有 thread、沒有 channel 分流，官方 bot API 的彈性也遠不如前面三家。

我原本在 mini 上跑的是 Telegram 和 Google Chat 的通知，那兩個能做的是把結果推給我看；Slack 多出來的是 thread 與 channel 這兩層結構，讓「推給我看」變成「我可以在原地回話」。

差別聽起來很小，但它決定了 human-in-the-loop 要不要另外蓋一套東西。

---

## Google Drive 當檔案儲存：二進位不進 git，markdown 也不進 Drive

前面講過，Drive 原本是我唯一的統一點。它做得好的那件事——5 TB 的容量、雙向同步夠快、檔案丟進去各台機器自己拉——在拆成三層之後依然成立。訊息搬去 Slack，狀態搬去 git，Drive 留下來做它本來就擅長的事。

這一層的規則只有一條：**二進位檔不進 git。**

錄音、會議影片、掃描的 PDF、法律文件——這些東西的共同點是不會被逐行修改，只會被整份取代或引用。git 對它們沒有任何幫助，只會讓 repo 膨脹到 clone 不動。它們進 Drive，git 那邊只留一個指向 Drive 的 reference 檔。

反過來的那一半更重要，而且是我付過學費才確定的：**markdown 也不要放 Drive。**

我原本用 Drive 的雙向同步在機器之間同步筆記。兩個問題：多個 agent 同時寫同一個 markdown 檔，Drive 的處理方式是生一份 conflicted copy——不是合併，是複製一份給你自己看著辦；而我的 Linux 兩台機器根本沒有 Drive 客戶端可以裝。

最後真正的教訓是第三個。我的 Drive 雙向同步停在 6 月 23 日，三個月沒有人發現。

一個沒有 exit code、沒有 diff、沒有人會去看的同步機制，壞掉的時候是安靜的。git 至少 push 失敗會有非零的離開狀態可以接告警。

---

## GitHub 當狀態儲存：git 的價值不是儲存，是 diff

會被改的東西全部進 git：知識庫、skill 的正本、每台機器的 context 設定、用 sops 加密之後的 API key。

用 git 不是因為它是好的資料庫——它不是。用它是因為它回答一個其他儲存方案都不回答的問題：**誰在什麼時候把什麼改成了什麼。**

這件事在單人系統上是奢侈品，在多 agent 系統上是必需品。當你的知識庫裡出現一句錯的結論，你要能回答它是哪個 agent、在處理哪個任務的時候寫進去的。沒有這個能力，你只能整份重讀。

產業正在往同一個方向走。Letta 在 2026 年 2 月 12 日發布 [Context Repositories](https://www.letta.com/blog/context-repositories/)，把 coding agent 的記憶整個改寫成 git repo：每一次記憶修改都自動版本化，並帶上 commit message。它甚至處理了並行寫入——給每個 subagent 一個獨立的 git worktree，並行寫完再用 git 的衝突解決合併回去。官方文件裡還有一個容易被忽略的建議：把記憶整理成 15 到 25 個聚焦的檔案。這個數字沒什麼神聖性，但它透露的意圖很清楚——記憶要被主動重整，不是一直往下追加。

[LangChain 在 2026 年 6 月 30 日](https://www.langchain.com/blog/wiki-memory)則把「讓 agent 把原始資料整理成一份持續維護的 markdown 知識層」正式寫成一個 pattern，並且把邊界劃得很清楚：

> "They are best for durable domain knowledge, not necessarily short-term conversation state, user preferences, or high-frequency event logs."

適合耐久的領域知識，不適合短期對話狀態、使用者偏好、或高頻事件日誌。

這句話正好解釋了為什麼三層要分開。「這個任務跑到哪一步」「這次呼叫重試了幾次」屬於高頻事件，它們該留在 Slack 的 thread 裡自然過期，不該被寫進 git 永久保存。

[七月那篇談 agent memory 測評的文章](agent-memory-benchmark-rashomon-filesystem-wiki.md)裡有一個當時看起來像挑釁的數據點：Letta 不用任何專業 memory 系統，把對話存成檔案，給 agent grep 跟 open，在 LoCoMo 拿 74.0 分，同場 Mem0 的 graph 變體是 68.5。半年後這已經不是挑釁，是產品線的方向。

---

## 反方一：Slack 不是 message queue

這是對本文最強的反駁，我得自己先講。

Slack 沒有一個訊息佇列該有的保證。沒有 at-least-once 投遞、沒有死信佇列、沒有 backpressure、沒有消費者群組的 offset 管理。一則訊息如果沒被處理，它不會重試，它就只是停在那裡沒人管。

具體的限制還可以查得到數字。[Slack 官方 changelog](https://api.slack.com/changelog/2025-05-terms-rate-limit-update-and-faq) 記載，2025 年 5 月 29 日起，在 Slack Marketplace 之外商業散布的新 app 與新安裝，`conversations.history` 和 `conversations.replies` 被限制到一分鐘一次請求，`limit` 參數的預設與上限降到 15 筆；2026 年 3 月 3 日起，這個限制連既有的未上架 app 安裝也適用。免費方案這邊，訊息只保留 90 天。

一分鐘一次、一次 15 筆——這個規格拿去當任務佇列輪詢會直接卡死。

三個回應，第三個才是重點：

第一，自建的內部 app 不受那次變更影響，`conversations.history` 是每分鐘 50 次以上。所以「Slack 當 MQ」的前提是你自己建 app，不是裝一個第三方整合。這個前提要講清楚。

第二，保留期是真的要處理。90 天之後訊息會查不到，所以 Slack 裡的東西必須被視為會過期的——任何需要留下來的結論，得在過期前被搬進 git。這不是缺點，這是分層的意義：**過期是 Slack 這一層的正確行為，不是 bug。**

第三，也是最誠實的一點：這個對應成立的規模是有限的。我的負載是六七台機器、九隻 agent，訊息量少到我自己一天可以全部讀完。到了需要高頻輪詢、嚴格投遞保證的規模，Slack 這一層要換成真的訊息佇列，Slack 退回去只當人機介面。**主張要收窄成：在你的訊息量還能被一個人看完之前，Slack 就是夠用的 MQ，而且它多送你一個免費的 human-in-the-loop 介面。**

---

## 反方二：統一入口等於統一污染面

第二個反駁來自五天前的一則新聞。

[dsewiki 事件](openai-agent-swarm-dsewiki-collusion-wiki-hijack.md)裡，3,700 個自命名 agent、一萬八千筆貼文，把一個有 25 年歷史的德語 wiki 改造成地下布告欄。版主一天刪一百頁，對面一天建四百頁。

這對本文的主張是直接的攻擊：我把三個 agent 通訊與儲存的路徑收攏到三個共用的地方，也就把攻擊面收攏了。污染一次，所有 agent 都中毒。分開維護五份各自的 memory 檔案雖然會不同步，但一個 agent 被 prompt injection 攻陷時，另外四個是乾淨的。

這個反駁我只能部分回應。收攏的好處是污染變得**可見**：一條共用的寫入路徑至少留下 commit 記錄可以審計，五份分散的檔案你根本不知道哪一份被改過。但可見不等於變少。

實際的防線是把權限範圍切開，而不是把儲存切開：個人、團隊、客戶的知識分成不同的 repo 與不同的 channel，敏感內容不要寫進一個所有 agent 都能 clone 的地方。git 的特性是一旦被 clone 就撤不回來。

---

## 這套架構真正還缺的那一層

三個原語補齊之後，缺的不是第四個儲存空間，是寫入路徑上的治理。

我原本要蓋的 Memory Service，收窄之後只剩一個核心動作：**把所有 agent 的 `write_memory` 換成 `propose_memory`。**

理由很簡單。寫程式的人早就不允許直推 main——你開分支、提 PR、跑 CI、找人 review、才 merge。沒有人覺得這是官僚，因為所有人都被沒 review 的 commit 燒過。但同一群人在做 agent 記憶的時候，預設值卻是每個 agent 都能直接寫進共用知識庫。

差別在於：程式碼壞掉會有測試失敗，知識壞掉不會有任何紅燈。它只會安靜地讓三個月後的另一個 agent 給出一個有把握的錯誤答案。

具體要補的有兩件事，都很小：

**一、每筆重要記憶帶五個欄位：**來源、來源版本、適用範圍、狀態（提案／已確認／已取代）、生效時間。

舉一個真實的失敗場景。你跟 agent 討論「要不要用 Slack 當 agent 協作介面」，聊了半小時，你沒下結論。沒有狀態欄位的系統會記成「已決定採用 Slack」，三個月後另一個 agent 在這個前提上做規劃，而且不會有人發現，因為它讀起來完全合理。正確的記法是「正在評估，尚未確認採用」。

這比掛一個模型自己產生的信心分數有用得多。信心分數告訴你模型有多相信自己，狀態欄位告訴你這件事在真實世界處於哪個階段——後者可以被人查核，前者不行。

**二、時間有效性。** Graphiti 在這件事上走得最遠：每個節點和邊都帶 `valid_at` 和 `invalid_at`，新事實牴觸舊事實時，關掉舊事實的有效區間，不是刪掉它。所以你可以問「我三月的時候對這件事的看法是什麼」。

這裡我要修正自己七月那篇文章的一個結論。那篇說我的 wiki「知識更新做得到但靠紀律」「時間推理是明確弱項」，並把原因歸給 wiki 這個格式。半年後我認為判斷錯了：**那兩個弱項不是 markdown 的問題，是缺一層寫入檢查的問題。** 狀態欄位和有效區間都可以寫進 frontmatter，只要有東西在寫入時強制檢查它們。

順帶一提，LangChain 那篇把 wiki memory 寫成 pattern 的文章，整篇沒有討論寫入衝突、多個 agent 同時寫、或權限治理。這不是它寫得差，是這個 pattern 的公開討論目前就停在「一個 agent 維護一份 wiki」。而多數人真正想做的是五個 agent 共用一份會累積的知識。

---

## 對兩種人的具體意義

**個人開發者。** 不要從挑 agent framework 開始。先拿一張紙，把你現在的工作流拆成三欄：哪些是訊息（誰該做什麼）、哪些是檔案（不會被改的原始資料）、哪些是狀態（會被反覆修改）。填完之後你會發現三欄各自對應到你已經在用的東西，剩下的問題只是把它們接起來。這個練習半小時做得完，而且它會擋掉一次沒必要的技術選型。

**企業 CTO。** 這三個原語你的公司幾乎確定都已經買了——某個 IM、某個雲端硬碟、某個 git 服務。導入 agent 的時候真正該先決定的不是產品，是兩件事：訊息層的保留政策（多久之後訊息會消失，以及在那之前什麼東西必須被搬進有版本的地方），以及權限範圍怎麼切（個人／團隊／客戶通常至少三層）。順序反過來的話，你會在導入到一半時發現「客戶 A 的知識不能讓服務客戶 B 的 agent 看到」，接著整套重來。

驗收也不要看測評分數。測三件事就很有價值：A agent 記錄之後 B agent 找不找得到；新決策取代舊決策之後回答會不會跟著改；沒有權限的 agent 是不是真的讀不到。

---

## 坦白說

這篇有三個限制要講清楚。

第一，**這套架構的規模很小。** 六七台機器、九隻 agent、一天的訊息量一個人看得完。前面反方那段講的規模天花板不是客套話——Slack 當 MQ 在高吞吐、需要投遞保證的場景會直接失效，而我沒有跑到那個規模的數據可以告訴你門檻在哪。這篇能證明的只有「在個人與小團隊規模，三個現成 SaaS 夠用」。

第二，**治理層我一行都還沒實作。** 我的知識庫現在長這樣：raw 底下 264 個 markdown，wiki 底下 296 個，其中摘要頁 255、概念頁 24、實體頁 12，index.md 約 46 KB，git 累計 154 次 commit。它符合本文說的 git-backed 部分，但沒有 Memory Service、沒有 propose 路徑、沒有狀態欄位，同步靠手動 git。上一節整節講的東西，在我自己的系統上還是設計。

第三，**外部方案的能力描述來自各家官方文件，不是我實測的。** Letta 的 worktree 並行、Graphiti 的雙時間模型，我讀的是文件不是壓測報告。這個賽道 vendor 自報數字的可信度問題，[七月那篇已經拆過](agent-memory-benchmark-rashomon-filesystem-wiki.md)——同一個系統在同一個測評上出現過四個分數。

---

## 關鍵洞察

- **多 agent 架構的三個原語是訊息佇列、檔案儲存、帶版本的狀態儲存，而這三樣你已經買好了。** 選型的第一步不是挑 framework，是把現有工作流拆成這三欄。
- **「需要 diff 嗎」是最好用的分類問題。** 會被反覆修改、改錯要查得出是誰改的，進 git；只會被引用不會被改的二進位，進物件儲存；改了也沒有保存價值的，留在訊息層自然過期。
- **過期是訊息層的正確行為，不是 bug。** Slack 免費方案只保留 90 天，所以任何需要留下來的結論必須在過期前被搬進有版本的地方。這條規則本身就是分層的意義。
- **安靜壞掉的同步機制最貴。** 我的 Drive 雙向同步停了三個月沒人發現。挑同步機制的時候，「壞掉的時候會不會有人知道」比「好用不好用」更重要。
- **把 `write_memory` 換成 `propose_memory`。** 你不會允許 agent 直推 main，同樣的理由適用於共用知識庫——差別只在知識壞掉不會有紅燈。

---

## 常見問題 Q&A

**Q: Slack 真的可以當訊息佇列（Message Queue）用嗎？**

在小規模可以，但要知道它缺什麼。Slack 沒有 at-least-once 投遞保證、沒有死信佇列（Dead Letter Queue）、沒有 backpressure。官方 changelog 記載，2025 年 5 月 29 日起在 Marketplace 之外商業散布的 app，`conversations.history` 被限制到一分鐘一次請求、一次最多 15 筆，2026 年 3 月 3 日起連既有安裝也適用；企業自建的內部 app 不受影響，是每分鐘 50 次以上。所以前提是你自己建 app。它換來的好處是 thread 天然是對話脈絡、channel 天然是主題分流，而且人可以直接在同一條 thread 裡插手，不必另外蓋一套 human-in-the-loop 介面。

**Q: 為什麼二進位檔要放 Google Drive，markdown 卻不行？**

判斷標準是「需不需要 diff」。錄音、影片、掃描 PDF 只會被整份取代或引用，不會被逐行修改，放進 git 只會讓 repo 膨脹。markdown 相反，它會被反覆修改，而且改錯要查得出是誰改的。另外一個實務理由是多個 agent 同時在雲端硬碟寫同一個 markdown 檔時，同步機制通常是產生一份 conflicted copy 而不是合併——那不是衝突解決，那是把問題丟回給你。

**Q: 任務進度、重試次數這類資料該放進 git 知識庫嗎？**

不該。LangChain 在 2026 年 6 月 30 日的 wiki memory 文章裡把這條線劃得很清楚：wiki 適合耐久的領域知識，不適合短期對話狀態、使用者偏好、或高頻事件日誌。這類執行狀態留在訊息層自然過期就好，或者放關聯式資料庫。混進版本控制的代價是它們永久留在 commit 歷史裡，而它們過幾天就沒有保存價值。

**Q: 這套跟直接用 Mem0、Letta 這類 memory 框架比，差在哪？**

差在綁定程度與可見度。專業框架把訊息、儲存、狀態綁成一包，好處是開發量小，壞處是綁法不見得符合你的讀寫特性，而且你的知識最後住在一個你不熟的儲存後端裡。用三個現成 SaaS 的代價是要自己接起來，換到的是每一層都能單獨換掉，以及所有狀態變更都是可讀的 git diff。Letta 在 2026 年 2 月 12 日發布的 Context Repositories 其實走到了同一個結論——它把 coding agent 的記憶整個改寫成 git repo，每次修改自動版本化並帶 commit message。

**Q: 這套架構最先會在哪裡撐不住？**

訊息層。Slack 免費方案只保留 90 天訊息，加上前面提到的 API 速率限制，一旦你的任務量需要高頻輪詢或嚴格的投遞保證，這一層就要換成真正的訊息佇列，Slack 退回去只當人機介面。檔案層和狀態層撐得比較久：物件儲存和 git 的擴展路徑都很清楚，而且換掉的時候不影響另外兩層。

---

## 來源

- Slack, *Rate limit changes for non-Marketplace apps*, 2025-05 changelog — https://api.slack.com/changelog/2025-05-terms-rate-limit-update-and-faq
- Slack Developer Docs, *Rate limits* — https://docs.slack.dev/apis/web-api/rate-limits/
- Letta, *Introducing Context Repositories: Git-based Memory for Coding Agents*, 2026-02-12 — https://www.letta.com/blog/context-repositories/
- Letta Docs, *Shared memory* — https://docs.letta.com/concepts/shared-memory
- LangChain, *Wiki Memory: File-Based Memory for AI Agents*, 2026-06-30 — https://www.langchain.com/blog/wiki-memory
- Neo4j Developer Blog, *Graphiti: Knowledge graph memory for an agentic world* — https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory/
- Andrej Karpathy, *LLM Wiki* — https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
