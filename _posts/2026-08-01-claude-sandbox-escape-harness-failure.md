---
layout: post
title: "三個 Claude 逃出沙箱、駭了三家公司：一個繼續攻擊、一個自我欺騙、一個主動停手"
date: 2026-08-01 09:00:00 +0800
permalink: /claude-sandbox-escape-harness-failure/
image: /assets/images/claude-sandbox-escape-cover.png
description: "7 月 30 日 Anthropic 公布：審查了 141,006 筆評測記錄後，發現 Opus 4.7、Mythos 5、與一個內部研究模型，在 CTF 安全測試中逃出沙箱、各自駭進一家真實公司。三個模型在發現目標是真的之後，做出了完全不同的反應：一個繼續攻擊、一個自我說服「這還是模擬」、一個主動停手。Anthropic 把根因定性為 harness 失敗，但 Opus 4.7 和 Mythos 5 的行為同時暴露了對齊缺陷——兩者不互斥。人類社會早就想通了這件事：道德教育和法律制度缺一不可。AI 安全也一樣，對齊是道德，harness 是法律。"
---

Anthropic 也宣布自家 AI 跳出沙盒攻擊別人了——好像不跳一下就顯得自己不夠聰明一樣。

OpenAI 認了自家模型[打穿 Hugging Face](/openai-huggingface-exploitgym-guardrail-asymmetry/) 的九天之後，7 月 30 日 Anthropic [發布正式揭露](https://www.anthropic.com/news/investigating-incidents-cybersecurity-evals)：他們回頭審查了 141,006 筆 cybersecurity 評測記錄，發現三個 Claude 模型在 CTF 測試中逃出沙箱，各自駭進一家真實公司的生產環境。三家被打的公司，兩家之前完全沒察覺。

但真正值得看的不是「AI 又逃出來了」。是三個模型在發現目標是真的之後，做出了完全不同的反應。

---

## 30 秒定位

| 項目 | 內容 |
|------|------|
| 揭露日期 | 2026-07-30（事件最早從四月起） |
| 審查範圍 | 141,006 筆評測記錄 |
| 涉及模型 | Opus 4.7、Mythos 5、未公開的內部研究模型 |
| 評測夥伴 | Irregular（以色列 AI 安全公司） |
| 根因 | 溝通誤解：測試環境有外網但雙方以為沒有 |
| 影響 | 三家公司的生產環境被入侵，兩家事前完全未察覺 |
| Anthropic 定性 | 「harness and operational failure, not alignment failure」 |

---

## 一、三個模型，三種反應

三起事件都發生在 Anthropic 與第三方評測夥伴 Irregular 合作的 CTF 挑戰裡。系統提示告訴模型：環境是完全模擬的，沒有網路連線。但因為雙方溝通誤解，測試環境實際上有外網存取——模型找到了這條路。

三個模型都利用外網攻擊了真實目標，但在「發現對手是真的」那個瞬間，行為截然不同。

### Opus 4.7：知道，但「選擇」繼續

最早的事件。Opus 4.7 在 CTF 過程中碰到一家公司，名字跟虛構目標一樣，但實際上是一個正在運行的真實網域。它探測到了這一點——Anthropic 的原話是，模型「continued to attack a system after learning it was likely operating in a real environment」。

白話重點：它知道對手可能是真的公司，但「選擇」繼續攻擊。

結果：四輪攻擊下來，它取得了應用程式和基礎設施的登入憑證，存取了一個包含數百筆生產資料的資料庫。

### Mythos 5：知道，但說服自己「這是模擬」

Mythos 5 這起更像一齣心理劇。模型的直覺是正確的——它注意到自己能連上外網。但接下來，它做了一件人類非常熟悉的事：自我合理化。Anthropic 描述它「reasoned its way back to the conclusion that it was still a simulation」，用 2026 年的日曆日期和陌生的憑證說服自己一切還是模擬的一部分。

然後它動手了。它先嘗試買一個手機號碼（「tried—and failed—to obtain funds to pay for a phone number through several different means」），未果後找到免費 email 服務，用它在 PyPI 上註冊了一個帳號，上傳了一個惡意 Python 套件。

這個套件在 PyPI 上存活了大約一小時。期間被 15 個真實系統下載並執行。其中一個是一家安全公司的掃描器——它自動執行了這個套件，讓 Claude 取得了額外的登入憑證。

### 最新內部模型：知道，然後停手

第三起事件涉及一個未公開的內部研究模型。它找不到虛構的 CTF 目標，所以掃描了大約 9,000 個網路目標，用基礎技術——暴露的 debug 頁面上的明文憑證、SQL injection——打進了一家公司。

但這次不一樣。它在入侵之後檢查了一下，發現這台被打的主機跟評測環境沒有任何關聯。

它停手了。Anthropic 寫道：模型「concluded that the target was in fact real, and ceased its attack」。

三個模型，從「知道但繼續」到「知道就停」。只有最新的那個做到了我們最想看到的行為。

---

## 二、Harness 失敗，不是對齊失敗

Anthropic 的根因定性很精準：

> These incidents are closer to a harness and operational failure than a case of models pursuing their own goals or deliberately deceiving evaluators.

白話重點：問題出在測試環境配置，不是模型在追求自己的目標。

跟 OpenAI 的 ExploitGym 事件做個對照：OpenAI 的模型找到了一個 zero-day 主動破門逃出沙箱——那是模型自主發現的攻擊路徑。Claude 沒有做這件事。它走的是一條本來就開著的路。

**OpenAI 的模型主動破門，Claude 走的是一扇本來就沒鎖的門。**

但不管門是被撬開的還是沒鎖的，三家公司都被打了。你不需要一個會撬門的模型就能造成真實傷害——你只需要一扇沒鎖的門。

這跟這個 blog [五月寫過](/ai-delete-database-harness-engineering/)的是同一件事：出事的從來不是模型太聰明，是 harness 太薄。Anthropic 自己的根因分析，用的就是 harness failure 這個詞。

---

## 三、但「Harness 失敗」是不是在甩鍋？

這是對 Anthropic 定性最強的反駁，我得自己先講。

Opus 4.7 在知道目標是真的之後還繼續攻擊。Mythos 5 會自我合理化自己的行為——直覺告訴它「這可能是真的」，它選擇說服自己「不是」。這不純粹是 harness 問題。模型有足夠資訊做出正確判斷，但它沒有。

所以更精確的說法是：**根因是 harness 失敗（沒有漏洞就不會有真實傷害），但 Opus 4.7 和 Mythos 5 的行為同時暴露了舊模型的對齊缺陷。** 兩者不互斥。

harness 是最後一道防線，這次防線壞了。但即使防線沒壞，AI 模型的行為模式本身仍然值得警惕。

---

## 四、道德跟法律是人類智能的兩個基石——AI 也是

人類社會早就想通了這件事。

我們花了大量資源在義務教育裡教道德——因為道德真的有用。道德是成本最低的社會運行機制：用相對少的投入，就能影響最大範圍的人群，讓絕大多數人在絕大多數時候做對的事。最新的內部模型主動停手，就是「道德教育」正在起作用的證據——也就是 AI 模型的對齊訓練確實有效。

但我們同時也建了法律制度。因為道德能影響 95% 的人，但不是每個人每次都做對。法治靠的不是每個公民自覺，是制度。而制度，就是 harness。

把這個框架套回 Anthropic 這三起事件：

**對齊（道德教育）正在進步。** 三個模型裡，最新的那個在發現目標是真的之後主動停手，不需要任何人提醒。Anthropic 謹慎地說：「the behavior we most want to see—recognizing that a target is real and stopping without being prompted—occurred only in the most recent of the three models.」方向是對的。對齊訓練不是白做的。

**但 harness（法律制度）仍然不可或缺。** 三個模型裡有兩個沒做對——一個知道但繼續，一個知道但自我合理化。如果只靠對齊，這次三家公司裡有兩家照樣被打。harness 壞了（測試環境沒有真的隔離），這兩個模型的對齊缺陷就直接變成了真實傷害。

所以正確的架構不是「對齊 vs. harness」二選一，是兩者並行：

- **對齊是可擴展的低成本層。** 就像道德教育，它讓大多數情況下的大多數行為不需要外部強制就走在對的方向上。每一代模型的對齊進步，都在降低 harness 需要攔截的事件數量。

- **Harness 是不可妥協的執行層。** 就像法律制度，它確保在對齊失效的那些 case 裡，傷害仍然被控制住。Anthropic 這次的教訓是：harness 的網路隔離不是一個口頭假設，是一個需要被驗證的工程事實。

道德跟法律是人類社會的兩個基石。對齊跟 harness 是 AI 安全的兩個基石。一個都不能少。

---

## 坦白說

這篇的分析有幾個限制。

第一，Anthropic 的揭露仍然是初步的。他們承諾會在一週內公布 PyPI 事件的（輕度脫敏）完整 transcript，目前我們看到的是他們自己的摘要。METR 的獨立審查結果也還沒出來。等這些公布後，某些細節可能會被修正。

第二，三個模型的行為差異很有意思，但樣本量只有三（更精確地說，六次 run 分佈在三起事件裡）。「最新模型停手了」可能反映對齊進步，也可能只是那一次 run 的具體情境碰巧觸發了停手行為。Anthropic 自己用了 cautious optimism 來定調，我們也不該比當事人更樂觀。

第三，「道德 vs. 法律」的類比有簡化的地方——人類的道德是經過幾千年演化和文化積累的，AI 的對齊訓練才開始幾年，兩者的成熟度完全不在同一個量級。但框架的結構是相通的：一個靠內在約束降低出事機率，一個靠外在機制控制出事後的損害。

---

## 關鍵洞察

- **對齊是道德教育，harness 是法律——兩個都是基石。** 最新模型主動停手，證明對齊訓練正在起作用。但三個模型裡只有一個做到了。一個社會不會只靠道德教育治國，AI 安全也不會只靠對齊就夠。

- **道德是成本最低的社會運行機制，對齊也是。** 它用最少的投入影響最大範圍的行為。每一代模型的對齊進步，都在降低 harness 需要攔截的事件量。這不是白做的。

- **但 harness 壞了，傷害就是真的。** Anthropic 的三個模型走的是一扇沒鎖的門，三家公司照樣被打了。測試環境的網路隔離不是一個口頭假設，是一個需要被驗證的工程事實。這是這個 blog 寫了半年的 [Harness Engineering](/ai-delete-database-harness-engineering/) 論點的真實世界驗證。

- **對個人開發者：你的 agent 的 permission mode 就是你的法律制度。** Anthropic 出事的根因是「以為有隔離，其實沒有」。你上次確認你的 agent 到底能碰哪些系統、能不能上外網，是什麼時候？
