---
layout: post
title: "工程師畫符：一張把 Agent 拆成道教符籙的圖，最準的是捆仙繩，最該改的是符腳"
date: 2026-10-19 09:00:00 +0800
permalink: /agent-talisman-fulu-mapping/
categories: [AI Agent]
image: /assets/images/agent-talisman-fulu-mapping-1.png
description: "網路上流傳一張圖，把一張道教符籙拆成十個部位，逐一對到 LLM Agent：符頭是 API Base URL、敕令是 API Key、捆仙繩是 Harness、符腳是 Output / Loop。好笑，但對得很準。拿傳統符籙「符頭是權限，符膽是內容，符腳是封印」的三段式去對照，會發現這張圖偷偷改了一個地方：符腳從封印變成了迴圈。畫符跟做工程的分界線，就畫在這一筆上。"
author: Wisely Chen
faq:
  - question: "這張「符籙 = Agent」的圖在講什麼？"
    answer: "這是一張網路迷因圖，把道教符籙拆成十個部位，對應到 LLM Agent 的元件：符頭是 API Base URL、所請神明名號是 Model ID、敕令是 API Key、捆仙繩是 Harness、天柱是系統提示詞（System Prompt）、地柱是使用者提示詞（User Prompt）、所請事項是目標（Goal）、風火輪是工具呼叫（Tool Call）、符膽是 Skill、符腳是 Output / Loop。它是比喻，不是正式架構，但可以當成一份由上到下的 Agent 除錯清單。"
  - question: "為什麼說 Harness 是捆仙繩，而不是 System Prompt？"
    answer: "System Prompt 裡寫的規則，模型可以選擇不照做，也可能被一段注入的文字騙過去，所以它比較像「建議」。Harness（駕馭層，指包在模型外面的權限、hook、沙箱、驗證機制）是在模型之外直接擋下動作，模型想做也做不到。圖上把 Harness 畫成纏住天柱地柱的繩子，意思是真正約束 Agent 的是機制，不是提示詞的字句。"
  - question: "調 Prompt 跟畫符的差別在哪？"
    answer: "傳統符籙的符腳是「封印」，命令封定送出去，靈不靈畫符的人看不到。如果改 prompt 只是換措辭、加驚嘆號，卻不看 trace、不跑評測（eval），那跟畫符沒有兩樣。差別在有沒有迴圈（Loop）：每次修改都看 output 和 tool call 紀錄，知道是哪一層出問題，才算工程。"
  - question: "API Base URL 為什麼會是資安問題？"
    answer: "Base URL 決定你的請求送到哪裡。換成非官方的 LLM 中轉站，所有 prompt、程式碼、金鑰都會經過對方的伺服器。UCSB 研究團隊測了 428 個 LLM 中轉，其中 17 個在偷 AWS 憑證。用符籙的比喻，等於跑到別人家的廟裡畫符。"
---

網路上流傳一張圖，把一張道教符籙拆成十個部位，每個部位標上一個 LLM Agent 的元件。

原作者我查不到。但第一眼看完，我笑了，第二眼看完，我覺得這張圖比很多 Agent 架構圖都準。

![把一張符籙拆成 Agent 的十個部位](/assets/images/agent-talisman-fulu-mapping-1.png)

<nav class="post-toc" markdown="1">
**目錄**

* 目錄
{:toc}
</nav>

---

## 十個部位，照圖對一遍

| 符的部位 | 圖上對應 |
|----------|----------|
| 符頭 | API Base URL |
| 所請神明名號 | Model ID |
| 敕令 | API Key |
| 捆仙繩 | Harness |
| 天柱 | System Prompt |
| 地柱 | User Prompt |
| 所請事項 | Goal |
| 風火輪 | Tool Call |
| 符膽 | Skill |
| 劍秋（符腳） | Output / Loop |

前三格是笑點，也是真的。

**敕令 = API Key。** 沒有敕令，咒語寫得再漂亮，神明也不會理你。換成工程語言，叫做 401。

**所請神明名號 = Model ID。** 請錯神，同一張符的效果完全不同。Model ID 打成小模型，再好的 prompt 也救不回來。

**符頭 = API Base URL。** 這格最不好笑。符頭寫的是你去哪一間廟請神。把 Base URL 換成來路不明的中轉站，等於跑到別人家的廟裡畫符，供品被誰收走你不會知道。UCSB 測了 428 個 LLM 中轉，17 個在偷 AWS 憑證，細節我在[這篇](/llm-proxy-relay-security-your-agent-is-mine-ucsb/)寫過。

---

## 最準的一格：捆仙繩

整張圖我最佩服的，是 Harness 的位置。

它被畫成一條捆仙繩，纏在符的正中間。天柱（System Prompt）、地柱（User Prompt）、所請事項（Goal）全部在它下面。

這跟我之前寫的[三次中心遷移](/agent-harness-three-migrations-mechanism/)是同一件事：注意力從 Prompt 搬到 Context，再搬到 Harness。天柱地柱寫的字是「建議」，捆仙繩才是「規則」。你在 System Prompt 寫「不准寄信」，模型可以不照做；hook 擋下寄信的 tool call，它就寄不出去。

**真正把神綁住的，從來不是符上的字，是那條繩子。**

---

## 對照傳統符籙：這張圖改了什麼

我去查了一下傳統符籙的結構。各派說法不一，但入門資料大致把一張符分成三段：符頭標明奉請哪位神明（以誰的名義），符膽寫明所求何事（命令本文），符腳收束封結（像用印落款，表示命令封定）。[道可易的入門文章](https://www.daokeyi.com/shan/fuzhou/fulu-rumen/)用一句話總結：

> 符頭是權限，符膽是內容，符腳是封印。

拿這三段去對這張 Agent 圖，有兩個改動很有意思。

**第一，權限被拆成兩半。** 傳統符頭常常就直接寫「敕令」兩個字，以誰的名義跟憑什麼權限是同一件事。這張圖把它拆成符頭（Base URL）和敕令（API Key）。這個拆法是對的，Agent 世界裡「去哪裡請」和「拿什麼請」是兩個獨立的攻擊面，中轉站事件就是前者出事、後者被偷。

**第二，符腳從封印變成迴圈。** 這是整張圖最重要的一筆。

傳統符腳的意思是：命令封定，送出去。靈不靈，畫符的人看不到，也沒辦法根據結果改下一張。

圖上把符腳標成 Output / Loop。Output 回來，看結果，不對就再畫一張。圖上寫的是「劍秋」，這個詞我在符籙資料裡查不到出處，但它旁邊那個「Loop」才是重點。

---

## 那 Prompt Engineering 到底是不是玄學

最強的反方是：「說到底，調 prompt 就是畫符。換個語氣、加個 you are an expert、加粗、加大寫，有時候靈有時候不靈，沒人說得清為什麼。」

這個我承認一半。我自己就幹過，把 prompt 改成「極度重要！！！」，加三個驚嘆號，沒用。那個當下我就是在畫符。

但另一半是：**畫符和工程的差別不在符上寫什麼字，在符腳是封印還是迴圈。** 只改天柱地柱的字句、不看 trace、不量結果，那是畫符。每次改完跑一輪 eval，看 output 跟 tool call 的紀錄，知道是哪一格出了問題，那就是工程。

同一張符，有沒有 Loop，決定你是道士還是工程師。

---

## 坦白說

這是一張迷因圖，對照是比喻，不是規格。

我對符籙的理解來自幾篇網路入門文章，各派用語差很多，同一個位置有人叫符膽、有人叫符竅。拿來當 Agent 的記憶口訣可以，拿去考道教史會被當掉。

圖本身也有對不太上的地方。傳統符膽是「命令本文」，比較接近所請事項（Goal），圖把它對到 Skill。說得通的解讀是 Skill 本來就是封裝好的秘訣，但這格明顯比其他格牽強。

還有，圖的原作者我查不到，如果有人知道出處，歡迎告訴我補上。

---

## 關鍵洞察

- **Agent 不靈的時候，從符頭往下查。** Base URL 對不對、Model ID 有沒有打錯、Key 有沒有效、System Prompt 跟 User Prompt 有沒有打架、Tool Call 有沒有真的被呼叫、Skill 有沒有被載入、Output 回來長什麼樣。這張圖剛好是一份由上到下的 debug 清單。
- **規則放在捆仙繩，不要放在天柱。** 能用 hook、權限擋的事，不要寫在 System Prompt 求它自願遵守。
- **符腳要是迴圈，不是封印。** 改 prompt 卻不看結果，就是在畫符。

---

## 常見問題 Q&A

**Q: 這張「符籙 = Agent」的圖在講什麼？**

這是一張網路迷因圖，把道教符籙拆成十個部位，對應到 LLM Agent 的元件：符頭是 API Base URL、所請神明名號是 Model ID、敕令是 API Key、捆仙繩是 Harness、天柱是系統提示詞（System Prompt）、地柱是使用者提示詞（User Prompt）、所請事項是目標（Goal）、風火輪是工具呼叫（Tool Call）、符膽是 Skill、符腳是 Output / Loop。它是比喻，不是正式架構，但可以當成一份由上到下的 Agent 除錯清單。

**Q: 為什麼說 Harness 是捆仙繩，而不是 System Prompt？**

System Prompt 裡寫的規則，模型可以選擇不照做，也可能被一段注入的文字騙過去，所以它比較像「建議」。Harness（駕馭層，指包在模型外面的權限、hook、沙箱、驗證機制）是在模型之外直接擋下動作，模型想做也做不到。圖上把 Harness 畫成纏住天柱地柱的繩子，意思是真正約束 Agent 的是機制，不是提示詞的字句。

**Q: 調 Prompt 跟畫符的差別在哪？**

傳統符籙的符腳是「封印」，命令封定送出去，靈不靈畫符的人看不到。如果改 prompt 只是換措辭、加驚嘆號，卻不看 trace、不跑評測（eval），那跟畫符沒有兩樣。差別在有沒有迴圈（Loop）：每次修改都看 output 和 tool call 紀錄，知道是哪一層出問題，才算工程。

**Q: API Base URL 為什麼會是資安問題？**

Base URL 決定你的請求送到哪裡。換成非官方的 LLM 中轉站，所有 prompt、程式碼、金鑰都會經過對方的伺服器。UCSB 研究團隊測了 428 個 LLM 中轉，其中 17 個在偷 AWS 憑證。用符籙的比喻，等於跑到別人家的廟裡畫符。

---

**延伸閱讀：**

- [你叫 Agent「不要亂寄信」根本沒用：從 Prompt 到 Harness 的三次中心遷移](/agent-harness-three-migrations-mechanism/)
- [做 Agent 的一個體會：Prompt 負責引導，工程負責約束](/prompt-guides-engineering-constrains-agent-principle/)
- [你的 Agent 是別人的：428 個 LLM 中轉安全測試](/llm-proxy-relay-security-your-agent-is-mine-ucsb/)

**參考來源：**

- 道可易〈符箓入门：道教符咒的结构与用法〉— https://www.daokeyi.com/shan/fuzhou/fulu-rumen/
