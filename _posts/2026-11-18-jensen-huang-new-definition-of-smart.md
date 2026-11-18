---
layout: post
title: "黃仁勳：軟體工程師曾是聰明人的終極職業，但 AI 正在把「解題能力」變成大宗商品"
date: 2026-11-18 15:00:00 +0800
permalink: /jensen-huang-new-definition-of-smart/
description: "近期在社群流傳的黃仁勳訪談片段，出處為 Jodi Shelton 主持的 Podcast《A Bit Personal》首集（2026 年 1 月）。當被問到「見過最聰明的人是誰」，黃仁勳點破純技術解題正在商品化，並給出 AI 時代的新定義：站在交叉點上、能看見轉角後面的人。從企業 AI 工程化與工程管理現場看，這對架構師與技術團隊意味著什麼？"
categories: [AI 觀點, 工程管理]
tags: [黃仁勳, NVIDIA, AI 工程化, 軟體工程師, 工程管理, 技術判斷力, A Bit Personal]
image: /assets/images/jensen-huang-new-definition-of-smart-cover.png
image_alt: "黃仁勳在 A Bit Personal 訪談中重新定義 AI 時代的聰明：站在技術與人性交叉點、看見轉角後面的人"
author: Wisely Chen
---

這幾天在短影音與社群平台上，有一段約 140 秒的黃仁勳（Jensen Huang）訪談片段被大量轉傳。

主持人問他：「**你見過最聰明的人是誰？**」  
黃仁勳沒有點名任何一位天才科學家或矽谷傳奇，反而給出了一個讓不少工程師背脊發涼、卻又無比真實的回答：

> 「大家都以為聰明就是智商高、很會解決問題、技術很強。但我覺得這種能力已經變成大宗商品（commodity）了——而 AI 最能輕鬆取代的，剛好就是這一塊。」

這段話的出處是哪裡？對正在做 AI 轉型、帶技術團隊、或是每天盯著 Coding Agent 寫程式的我們來說，真正該聽懂的訊號又是什麼？

---

## 一、出處查證：來自 2026 年 1 月《A Bit Personal》首集訪談

先交代清楚這段內容的原始出處，避免以訛傳訛。

這段對話來自全球半導體聯盟（GSA）共同創辦人暨執行長 **Jodi Shelton** 主持的 Podcast 節目 ***A Bit Personal with Jodi Shelton*** 第一季第一集：《*Jensen Huang: Founder and CEO of NVIDIA*》（2026 年 1 月 15 日上線）。Jodi Shelton 與黃仁勳相識超過三十年，這場對談不同於一般的技術發表會或財經專訪，談的是較私密、長線的領導與人性觀察。

這段問答的英文原文如下（完整核對自節目逐字紀錄）：

> **Jodi Shelton:** “Who's the smartest person you've ever met?”  
> **Jensen Huang:** “I can't answer that question. And I know what people are thinking—the definition of smart is somebody who's intelligent, solves problems, technical. But I find that's a commodity, and we're about to prove that artificial intelligence is able to handle that part easiest, right? Yeah.  
> And so, as it turns out—let me give you another example. Everybody thought software programming was the ultimate smart profession. Look, what is the first thing that AI is solving? Software programming.  
> And so, it turns out that the definition of smart is very different than most people think. And I think long-term, the definition of smart—and my personal definition of smart—is someone who sits at that intersection of being technically astute, but [having] human empathy, and having the ability to infer the unspoken, the around-the-corners, the unknowables.  
> You know, people who are able to see around corners are truly, truly smart, and that their value is incredible. To be able to preempt problems before they show up, just because you feel the vibe. And the vibe came from a combination of data, analysis, first principles, life experience, wisdom, sensing other people.  
> That vibe—I think that's smart. I think that's going to be the future definition of smart. And that person might actually score horribly on the SAT.”

先前我在〈[剝開千億帝國的光環：看黃仁勳身上的「華人老闆」底色](/jensen-huang-ai-taste-and-warmth/)〉一文裡，從供應鏈與員工互動聊過他「人的溫度」與「Taste」。而他在《A Bit Personal》的這段自白，更像是直接把**工程師與技術管理者的職涯護城河**攤開在檯面上講。

---

## 二、為什麼「寫程式」曾是聰明人的終極職業，卻第一個被 AI 攻破？

黃仁勳在訪談裡舉了一個很刺耳、但沒人能反駁的例子：

**以前所有人都認為「軟體工程師」是聰明人的終極職業，結果 AI 第一個解決的，就是寫程式。**

這背後的道理，其實跟我們在企業現場導入 AI Coding Agent 看到的現象完全一致：

1. **有明確規格、有即時回饋的封閉解題，正是 AI 的主場**：寫一個演算法、補一段 API、重構一個已知模式的模組，甚至修一個有清楚 stack trace 的 Bug——這些任務都有明確的輸入、輸出與測試驗證機制。模型只要算力夠、上下文夠清楚，執行成本只會無限趨近於零。
2. **「純解題能力」正在變成水電一樣的基礎設施**：當所有團隊都能用同樣的模型在幾分鐘內產出可運作的程式碼時，「你寫得出這段 code」就不再是稀缺能力，而是像會用搜尋引擎、會用 IDE 一樣的基本門檻。

換句話說，AI 並沒有消滅工程問題，它只是把**「在已知邊界內把題目解出來」**這件事商品化了。

---

## 三、黃仁勳說的「氣（Vibe）」，不是玄學，而是六種維度的壓縮

很多人看到翻譯裡出現「感受到的那股氣（feel the vibe）」，容易誤以為他在講什麼神祕直覺或雞湯。但把英文原文拆開來看，黃仁勳給出的定義其實非常工程化、也非常嚴謹。

他說那股能讓人「看見轉角後面（see around corners）」的判斷力，來自六個要素的總和：

1. **Data（資料）**
2. **Analysis（分析）**
3. **First principles（第一性原理）**
4. **Life experience（人生經驗）**
5. **Wisdom（智慧）**
6. **Sensing other people（感知他人）**

這六件事疊在一起，就是**站在交叉點上的人**才具備的能力。

放到企業 AI 工程化與架構設計的現場來看，這完全就是每天都在發生的事：

- **AI 很會回答「這段程式怎麼寫」，但它不會主動察覺「這個需求背後其實藏著跨部門的權責衝突」**——那是 *the unspoken*（沒說出口的事）。
- **Benchmark 與測試集只會測已知路徑，但真實系統往往死在沒寫進規格書的邊緣條件與人為誤用**——那是 *the around-the-corners*（轉個彎才看得見的風險）。
- **就像我們在設計 Agent Harness 與安全沙盒時看到的，靠靜態規則庫永遠防不住所有未知威脅**（見〈[AI 代碼門禁的不可能定理](/ai-gatekeeper-impossibility-theorem/)〉），真正決定系統穩不穩的，往往是架構師在動手寫第一行 code 之前，就先預判到「這裡只要放任自由執行，三個月後一定會出事」的系統直覺。

---

## 四、SAT 考得很爛的人，為什麼在 AI 時代反而更值錢？

訪談最後一句最值得玩味：

> **「而且這樣的人，SAT 可能考得很爛。」**

SAT 測的是什麼？是在標準化時間內、依循既定規則、快速算出標準答案的能力。過去幾十年，教育體制、科技公司面試的白板演算法題，幾乎都在篩選同一種人：**高分、標準化、純粹的執行與解題機器。**

但現在，大語言模型本身就是全人類史上最強的「SAT 考霸」。它讀過所有公開題庫、不會疲勞、不會情緒波動，在標準化測試上的分數只會越拉越高。

如果一個工程師或技術主管，唯一的競爭力還是「像一台更聽話、更會背題庫的標準化機器」，那他正面對的，就是與算力直接正面對撞的貶值曲線。

相反地，那些無法被標準化考卷量化的能力，價值正在指數級放大：

- **站在技術與業務的交叉點**：懂模型限制、懂地端部署與資安邊界，同時也聽得懂業務端真正在痛什麼。
- **讀懂「沒說出口的訊號」**：能在專案還沒爆炸前，從一段模糊的需求、一個反常的數據指標、或團隊成員的沉默裡，嗅出哪裡不對勁。
- **在問題冒出來之前先防住（Preempt problems）**：不是等系統掛了再救火，而是在架構階段就把單點故障（SPOF）、權限越界與人為摩擦先拿掉。

---

## 五、給工程師與技術主管的三個務實建議

把黃仁勳的這段話落回我們的日常工作，不需要空談哲學，至少有三件事現在就可以開始調整：

1. **把「產出程式碼」交給 Agent，把自己的大腦留給「定義邊界」**  
   別再把成就感建立在「今天手寫了幾行漂亮的程式碼」。把重複實作交給工具，把時間花在確認：**我們真的在解對的問題嗎？這個系統的失敗邊界、權限隔離與驗收閘門設在哪裡？**
2. **刻意跨出純技術同溫層，去碰「人」與「現場」的複雜度**  
   多參與業務需求訪談、多看真實使用者的操作摩擦、多理解組織裡的利害關係。唯有把技術敏銳度跟真實人性疊加在一起，你才有機會長出 AI 學不來的交叉點判斷力。
3. **調整團隊的「SAT」—改變你招募與評價工程師的標準**  
   如果你還在只靠刷題、只看單人產出多少 PR 來評價工程師，你篩出來的正是 AI 最快取代的能力。試著去觀察：**誰能在需求模糊時把關鍵風險先問出來？誰在設計架構時會主動替未來的維運與資安留退路？** 能看見轉角後面的人，才是 AI 時代團隊裡最稀缺的資產。

---

**參考出處：**  
Jodi Shelton, *A Bit Personal with Jodi Shelton* — Season 1, Episode 1: *Jensen Huang: Founder and CEO of NVIDIA*（2026 年 1 月 15 日發布）｜官方網站：[abitpersonalpod.com](https://www.abitpersonalpod.com)｜YouTube 頻道：[@ABitPersonalPod](https://www.youtube.com/@ABitPersonalPod)
