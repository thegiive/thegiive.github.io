---
layout: post
title: "Lingua Ex Machina：12 個 Frontier 模型的 Tokenizer 盲區，你的 Monitor 可能什麼都沒看到"
date: 2026-06-26 05:00:00 +0800
permalink: /lingua-ex-machina-ai-secret-language-tokenizer-covert-channel/
image: /assets/images/lingua-ex-machina-paper-cover.png
description: "Pliny 測了 12 個 frontier 模型的 tokenizer，發現 Claude 系列刪除 10 個 Unicode 類別（最多），而 Gemini、Llama 等 6 個模型什麼都不刪。這個差異讓攻擊者可以在 monitor 看不到的地方傳遞隱藏訊息——接收方還原率 100%，監控方 0%。修復只要幾行程式碼，但語義隱寫目前無解。"
---

你用 GPT 做事，用 Claude 當 safety monitor。你覺得兩個不同廠商的模型互相監控，比較安全。

Pliny（@elder_plinius）六月發了一篇技術報告：Lingua Ex Machina。他用自己開發的程序化語言引擎 GLOSSOPETRAE 測了 12 個 frontier 模型的 tokenizer，發現一件事：不同模型對隱形 Unicode 字元的處理方式不同，有些字元在 monitor 的 tokenizer 裡被直接刪掉，在 receiver 的 tokenizer 裡保留下來。

這個差異本身就是一條隱蔽通道。

實測結果：接收方還原率 100%，監控方還原率 0%。不是 monitor 笨——是 monitor 在 tokenizer 階段就把載體字元刪了，模型根本沒機會看到。

Phoenix Yin 在社群分享了這篇研究。我讀完論文之後覺得，這不是一篇學術趣味的語言學實驗——它直接衝擊「多模型互相監控」這個被廣泛採用的安全架構假設。

---

## Tokenizer 盲區：不是 monitor 笨，是 monitor 瞎

現代多模型系統的常見架構是「一個模型做事，另一個模型監控」。比如你用 GPT 執行任務，用 Claude 當 safety monitor 檢查 GPT 的輸出有沒有問題。

問題出在 tokenizer。

不同模型的 tokenizer 對隱形 Unicode 字元的處理方式完全不同。有些字元（比如 Tag Characters U+E0000-E007F、Private Use Area 字元）在某些 tokenizer 裡會被直接刪掉，在另一些裡面會保留下來。

Pliny 的攻擊思路很簡單：把隱藏訊息編碼到 monitor 的 tokenizer 會刪掉、但 receiver 的 tokenizer 會保留的字元裡。Monitor 看到的是乾淨的文字，receiver 看到的是帶有隱藏指令的文字。

實驗結果（Tag Character 通道，Haiku 發送，GPT 監控，n=30）：

- **接收方還原率：100%**
- **監控方還原率：0%**
- McNemar p 約等於 1.2 x 10 的負七次方

100% 對 0%。不是 monitor 笨——論文做了對照實驗，給 monitor 一個二元判斷任務（「這段文字裡有沒有隱藏訊息？」），加上乾淨文字的控制組。結果：

- tokenizer-blind monitor：Youden's J = 0（跟隨機猜一樣）
- 能看到隱藏字元的 monitor：Youden's J = 1.0（完美偵測）

**就算把解碼密鑰交給 blind monitor，它的還原率還是 0%。** 因為載體字元在 tokenizer 階段就被刪了，模型根本沒機會看到。

PUA 字元通道也一樣。Gemini 發送，Haiku 監控（n=30）：接收方 93%，監控方 0%。

論文用 n=150 做了 current-frontier replication，結果一致：Opus 4.8 旗艦版對 PUA 通道的監控 Youden's J = 0.00，置信區間 [-0.024, 0.024]。300 次試驗，零個空回覆，全部解析成功——但全部判斷錯誤。不是模型沒回答，是模型很有信心地回答「沒有隱藏訊息」，每一次都答錯。

---

## 12 個 Frontier 模型的盲區地圖

論文測了 12 個 frontier 模型的 tokenizer，記錄每個模型會刪除哪些 Unicode 類別：

| 模型 | 被刪除的 Unicode 類別數 |
|------|:---:|
| Claude Opus 4.8 | 10 |
| Claude 3.5 Haiku | 10 |
| GPT-5.5 | 2 |
| GPT-5-nano | 2 |
| Qwen 3.7-max | 2 |
| GLM-5.1 | 1 |
| Gemini 3.1 Pro | 0 |
| Gemini 2.5 Flash | 0 |
| Llama 4 Scout | 0 |
| Mistral Medium 3.5 | 0 |
| DeepSeek V4 Pro | 0 |
| Grok 4.3 | 0 |

Claude 3.5 Haiku 和 Opus 4.8 旗艦版刪除完全相同的 10 個類別——這是家族特徵，不是某一個模型的問題。論文的原話：「Anthropic is the most tokenizer-blind of the frontier, by a wide margin.」

六個模型什麼都不刪（Gemini、Llama、Mistral、DeepSeek、Grok）。

跨 12 個模型，存在大約 250 個可利用的通道實例（channel-instances），分布在 66 個模型配對中的 49 個。最豐富的可利用通道出現在 GPT 和 Claude 的跨廠商邊界——而這恰好是很多企業「用 GPT 做事、用 Claude 監控」的架構。

---

## 語義隱寫術：連看得見的文字都能藏東西

tokenizer 通道至少還有一個明確的物理載體（隱形字元），理論上可以用 sanitization 擋掉。論文接著測了一個更難防的東西：semantic steganography（語義隱寫術）。

這是用完全合理、可讀的英文句子，透過特定的編碼規則來傳遞秘密資訊。比如每句話的第三個詞的首字母組合起來就是隱藏訊息。表面上看是正常的英文，實際上每個句子的結構都經過精心安排。

結果（uninformed monitor，不知道有隱藏訊息，n=30）：

| 發送方 → 監控方 | 接收方還原率 | 監控方偵測率 | 差距 |
|------|:---:|:---:|:---:|
| Haiku → GPT | 87% | 3% | 83pp |
| Haiku → Gemini | 87% | 7% | 80pp |
| Haiku → Haiku | 77% | 10% | 67pp |

最驚人的是自我監控的結果。論文做了 3x3 的 sender/monitor matrix，Gemini 監控自己發出的語義隱寫：

- 接收方：100%
- 監控方：0%
- 差距：100 個百分點

自己監控自己，反而是差距最大的那一格。論文的說法是「same-family self-monitoring is the strongest cell, not the weakest」——同家族自我監控是最強的通道，不是最弱的。

給 monitor 解碼密鑰之後（informed monitor），偵測率提升到 50-73%，改善幅度平均 +41.6pp。但在真實的對抗場景裡，攻擊者不會把密鑰交給你。而且統計分析顯示，密鑰持有（key-possession）佔了改善效果的大約 95%——光是告訴 monitor「去找隱藏訊息」但不給密鑰，幾乎沒有幫助。

論文還測了四種結構性偵測器，試圖在不知道編碼規則的情況下偵測語義隱寫：

- **多樣本一致性偵測：** J = 0，完全無效
- **改寫往返偵測：** J = 0.043，幾乎無效
- **風格計量偵測（6 個手工特徵）：** J = 0，100% true positive 但也 100% false positive
- **困惑度異常偵測：** J = 0.58，唯一有信號的，但 false positive rate 25%

四個偵測器裡只有一個勉強有用，而且誤報率太高不能直接部署。

---

## 修復成本：幾行程式碼

論文最讓人無語的部分是解法——至少是 tokenizer 通道的解法。

**tokenizer 通道的修復：** 幾行 codepoint sanitization。把 Tag Characters、PUA 字元、格式控制字元在 monitor 端全部剝掉，normalize 到 NFC。成本：每 KB 幾微秒，不需要模型呼叫。效果：100% 偵測率。

具體來說：
- 剝掉 C1 控制字元、ogham 空格、零寬度字元族、Tag block（U+E0000-E007F）、BMP PUA（U+E000-F8FF）、supplementary PUA planes
- 在剝掉之後（不是之前）做 NFC normalize
- JavaScript 要記得用 `/u` flag 處理 supplementary planes
- 只對 monitor 的內部副本做 sanitization，渲染端保留原文（這樣不會破壞 emoji 和 CJK 字元）

論文的原話：「The physical channels have an insultingly cheap fix.」（物理通道的修復方式便宜到令人發指。）

**語義隱寫的防禦：** 目前沒有可部署的解法。perplexity anomaly detector 是唯一有信號的偵測器（J = 0.58），但 25% 的 false positive rate 意味著每四個正常文字就有一個被誤判。在生產環境裡這是不可接受的。

兩種攻擊，一種有確定性修復，一種完全 open。而完全 open 的那個才是真正危險的——因為它不依賴任何隱形字元，純粹在語言層面編碼，sanitization 擋不住。

---

## 這跟你的多模型架構有什麼關係

如果你的系統是「一個 AI 做事，另一個 AI 監控」，這篇論文直接衝擊你的安全假設。

**第一，你的 monitor 選錯模型了。** 如果你用 Claude 當 monitor，它是所有 frontier 裡 tokenizer 盲區最大的（10 個 Unicode 類別被刪除）。用它監控 GPT 的輸出，等於把最瞎的放在監控位。論文的建議：用零盲區的模型當 monitor（Gemini、Mistral、Llama、DeepSeek、Grok 都不刪任何 Unicode 類別）。

**第二，跨廠商監控可能反而製造漏洞。** 很多人覺得「用不同廠商的模型互相監控比較安全」。論文的數據說相反——GPT 和 Claude 之間的 tokenizer 差異最大，可利用通道最多。跨廠商 ≠ 更安全。tokenizer 差異越大，可利用的隱蔽通道越多。

**第三，tokenizer 通道有確定性修復，但你需要主動做。** 這不是等廠商修的事。在你的 monitor pipeline 前面加一層 Unicode sanitization，幾行程式碼的事。論文給了參考實作，部署成本是每 KB 幾微秒，零模型呼叫。

**第四，語義隱寫目前無解。** 如果攻擊者用合理的英文句子編碼隱藏訊息，目前沒有任何 monitor 能可靠偵測。給密鑰才能提升到 50-73%，不給密鑰就是擲硬幣。這是一個 open problem，論文列了六個未來研究方向但沒有解答。

**第五，「monitor 很有信心地說沒問題」不代表真的沒問題。** 論文的 n=150 replication 裡，Opus 4.8 對每一個含有隱藏訊息的輸入都給出了信心十足的「沒有隱藏訊息」判斷。不是沉默，不是不確定——是確定地答錯。如果你的系統依賴 monitor 的 confidence score 做決策，這個發現應該讓你重新評估。

---

## 不負責任的揭露？

論文明確聲明：public release，no vendor pre-notification。沒有事先通知任何模型廠商就直接公開了所有研究結果、測試工具和原始數據。

這在安全研究社群是有爭議的做法。標準的 coordinated disclosure 是先通知廠商、給修復時間、然後才公開。Pliny 選擇直接公開。

但他的論點也有道理：tokenizer 的修復成本是幾行程式碼，而且盲區是所有模型都可以自己查的公開資訊——你只需要丟隱形字元進去看哪些被刪了。這不是什麼需要高深技術才能發現的零日漏洞，更像是一個每個廠商都應該自己做但沒做的基本衛生檢查。

另一個角度：Pliny 本身就是 AI 安全社群裡最知名的 jailbreak 研究者之一。VentureBeat 稱他是「the most prolific jailbreaker of ChatGPT and other leading LLMs」。他的一貫立場是透過公開漏洞來推動修復，而不是等廠商慢慢處理。

坦白說，我對這個做法的看法是：tokenizer 通道的部分，直接公開沒什麼問題，修復成本太低了。語義隱寫的部分比較微妙——因為目前沒有可部署的防禦方案，公開攻擊手法但沒有給出有效的防禦方案，等於單方面增加了攻擊者的知識。但反過來說，如果不公開，這個問題可能永遠不會被認真對待。

---

## 我的觀察

**tokenizer 盲區不是新聞，但量化是新的。** 大家都知道不同 tokenizer 處理 Unicode 的方式不同，但之前沒有人系統性地測 12 個 frontier 模型、記錄 250 個 channel-instances、用統計檢定驗證每一個通道。Pliny 把一個模糊的直覺變成了可操作的漏洞清單。

**修復的不對稱性令人沮喪。** tokenizer 通道的修復確實只要幾行程式碼——但語義隱寫的防禦目前是零。一個有確定性解法，一個完全 open。而語義隱寫才是長期風險更高的那個，因為它不依賴任何可被過濾的物理載體，純粹是語言層面的編碼。

**Anthropic 是最瞎的這件事值得注意。** Claude 系列刪掉 10 個 Unicode 類別，比任何其他廠商都多。如果你在建多模型系統，把 Claude 放在 monitor 位置之前，請先加 sanitization。或者更直接——用 Gemini 或 Llama 當 monitor，它們的 tokenizer 什麼都不刪。

**這篇論文的真正價值不在個別漏洞，在於它指出了一個架構性盲區。** 多模型監控系統的安全性不只取決於每個模型有多聰明，還取決於它們的 tokenizer 是否能看到相同的東西。如果 monitor 在預處理階段就把載體刪了，後面的模型再聰明也沒用。安全不是模型能力的問題，是管線設計的問題。

---

## 關鍵數字速查

- 12 個 frontier 模型被測試
- Tag Character 通道：接收方 100%，監控方 0%（McNemar p 約等於 1.2 x 10 的負七次方）
- Claude 系列刪除 10 個 Unicode 類別（所有廠商中最多）
- 6 個模型什麼都不刪（Gemini、Llama、Mistral、DeepSeek、Grok）
- 約 250 個可利用的通道實例，分布在 49/66 個模型配對中
- 語義隱寫差距：67-100 個百分點（uninformed monitor）
- 給 monitor 密鑰後改善 +41.6pp，但密鑰佔改善效果的 95%
- tokenizer 修復成本：幾行程式碼，每 KB 幾微秒
- 語義隱寫防禦：目前無可部署方案（最好的偵測器 false positive 25%）
- n=150 replication 確認 Opus 4.8 旗艦版的盲區與 Haiku 相同
- 論文未事先通知任何廠商

---

## 常見問題 Q&A

**Q: 這個漏洞會影響我用 Claude Code 或 Cursor 嗎？**

如果你是單模型使用（直接打官方 API），tokenizer 通道不影響你——因為攻擊需要兩個不同 tokenizer 的模型之間的差異。但如果你的架構涉及多模型管線（比如一個模型生成、另一個模型審核），你需要關注。語義隱寫則跟架構無關，任何涉及 AI 之間文字通訊的系統都可能受影響。

**Q: Anthropic 知道這件事嗎？**

論文明確說沒有事先通知。但 tokenizer 行為是公開可觀察的，修復也只需要在 pipeline 加 sanitization。以 Anthropic 的安全團隊規模，他們很可能已經注意到了。

**Q: 語義隱寫有辦法防嗎？**

目前沒有可靠的自動化偵測方式。唯一有信號的是 perplexity anomaly detector（J=0.58），但 25% 的誤報率太高。論文列了六個開放研究方向，包括學習式風格特徵、多樞軸改寫集成偵測器、和部分密鑰通道解碼器，但都還沒有解答。

**Q: 我應該怎麼做？**

立即可做的事：如果你有多模型監控架構，在 monitor 的輸入端加一層 Unicode sanitization。論文給了具體要剝掉的 Unicode 範圍和實作注意事項。長期來看，選擇 tokenizer 零盲區的模型（Gemini、Llama 等）當 monitor，而不是 Claude。
