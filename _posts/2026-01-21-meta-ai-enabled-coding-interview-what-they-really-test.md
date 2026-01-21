---
layout: post
title: "Meta AI-Enabled Coding 面試：他們到底在測什麼？"
date: 2026-01-21 07:00:00 +0800
categories: [AI面試, 職涯發展]
tags: [Meta, AI面試, Coding Interview, AI協作, 技術面試]
description: "Meta 2025 年開始試行 AI-Enabled Coding Interview，跟傳統 LeetCode 刷題完全不同。60 分鐘內在多檔案 codebase 中完成任務，AI 是你的 junior engineer——會給答案但可能是錯的。真正測的是你的判斷力：知道為什麼這樣寫，才是 AI 時代的核心價值。"
image: /assets/images/meta-ai-coding-interview-cover.png
---

![Meta AI Coding Interview](/assets/images/meta-ai-coding-interview-cover.png)

前陣子寫了一篇「AI 時代的面試：我不考 coding，只問為什麼」，講我自己面試團隊成員的邏輯。結果收到不少讀者問：「那如果是我要去面試大廠呢？Meta、Google 這些公司現在怎麼考？」

剛好 Meta 在 2025 年 10 月開始大規模試行 **AI-Enabled Coding Interview**，到 2026 年已經變成標準流程。這跟傳統 LeetCode 刷題完全不一樣。

這兩週我跟幾個真的去大廠面試過 AI Coding 的朋友聊了不少，問他們當時的感受和細節。同時我自己也在面試 candidate，一直在調整 format——因為之前那套 tech interview 根本不貼近現實工作了。再加上 Reddit、Blind 上網友的分享，還有幾份面試指南，整理出這篇拆解：這個新面試到底在測什麼。

---

## 面試格式：60 分鐘的真實世界模擬

傳統 Meta 面試是兩輪獨立的演算法題（45 分鐘各解一題）。新的 AI-Enabled 格式改成：

| 項目 | 傳統格式 | AI-Enabled 格式 |
|------|---------|----------------|
| **時間** | 45 分鐘 × 2 輪 | 60 分鐘 × 1 輪 |
| **題目** | 獨立演算法題 | 多檔案 Codebase + 連續任務 |
| **工具** | 純手寫（無 IDE） | CoderPad + AI 助手 |
| **目標** | 證明你會寫演算法 | 證明你會用 AI 解決問題 |

環境是 CoderPad，旁邊有個 AI chat sidebar，候選人可以選擇用 **mini、Haiku、Gemini Flash** 這幾個模型系列。注意：都不是 SOTA，清一色是小模型。這是故意的——他們不想讓你靠 AI 硬解，而是看你怎麼跟「不那麼聰明」的 AI 協作。(PS. 當然有可能是因為 GPT5 or Opus 一下子就做完也很尷尬)

---

## 三種考題情境

根據多位候選人回報，題目會是以下三種之一：

### 1. 從頭建立功能（Build Features）
給你一個現有的 codebase 結構，要求你新增一個功能。例如：
- 現有一個卡牌遊戲系統
- 需要實作「抽 N 張牌，找出總和為 15 的三張牌組合」

### 2. 擴充半完成的程式碼（Extend Code）
程式碼框架已經有了，但核心邏輯是空的或錯的：
- `main.py`、`solve.py`、`utils.py`、`test.py` + data 資料夾
- 你需要理解整體架構，然後補完或修正

### 3. Debug 壞掉的實作（Fix Bugs）
測試會失敗，你需要：
- 看懂錯誤訊息
- 追蹤程式碼流程
- 找到 bug 並修復

---

## 他們真正在測什麼？

這是最關鍵的部分。Meta 官方說明評估四個維度：

### 1. Problem Solving（問題解決）
- 你怎麼釐清需求？
- 遇到模糊的地方會不會主動問？
- 能不能把開放式問題拆解成可執行的步驟？

### 2. Code Development & Understanding（程式開發與理解）
- 你能不能快速看懂別人寫的程式碼？
- 你能不能在現有架構下寫出符合風格的新程式碼？
- **就算是 AI 幫你寫的，你能不能解釋每一行？**

### 3. Verification & Debugging（驗證與除錯）
- 你會不會先跑測試？
- 你怎麼追蹤 bug？
- 你修完之後會不會檢查有沒有 regression？

### 4. Technical Communication（技術溝通）
- 你在做什麼，面試官聽得懂嗎？
- 你能不能在「講太多」和「講太少」之間找到平衡？

---

## 候選人真實經驗：AI 不是答案機

一位候選人分享他的經歷：

> 一開始面試官跟我說：「先自己試試看，跟著測試失敗的地方走。」
>
> 我問他：「可以讓 AI 幫我全部寫嗎？」
>
> 他回：「可以，但它可能是錯的。」

這句話很關鍵。**AI 在這個面試裡不是作弊工具，是你的 junior engineer**。它會給你答案，但答案可能：
- 語法對但邏輯錯
- 小測資過但大測資爆
- 符合規格但效能很差

另一位候選人說內建的 AI 感覺「比 ChatGPT-3 還弱」，在效能優化上完全幫不上忙。所以如果你平常依賴 ChatGPT 寫 code，這個面試會讓你原形畢露。

---

## 七個常見的失敗模式

根據多份面試指南整理，這些是候選人最常踩的坑：

### ❌ 1. 讓 AI 決定策略
AI 應該執行你的想法，不是幫你想策略。問它「這題怎麼解」跟問它「幫我實作 binary search」效果完全不同。

### ❌ 2. 複製貼上大段 AI 程式碼不看
面試官看得到你每個動作。如果你貼了 50 行 AI 生成的 code 然後直接跑測試，他會問你：「第 23 行在幹嘛？」

### ❌ 3. 不跑測試就繼續寫
每改一段就跑測試。這不只是好習慣，也是讓面試官知道「你有在驗證」的訊號。

### ❌ 4. 長時間沉默
想事情可以，但要出聲。「我在看這個函數怎麼被呼叫的」、「我在追這個變數的來源」——這些都是有效的溝通。

### ❌ 5. 不停嘴的 narration
相反的極端也不好。不需要每打一個字就解釋，找到平衡。

### ❌ 6. 過早優化
先求對，再求快。很多人在測試還沒全過就開始想怎麼優化，結果基本功能都沒完成。

### ❌ 7. 忽略 regression
改 A 功能的時候把 B 功能弄壞了，這在真實工作中是大忌，面試也一樣。

---

## 準備策略：不是刷 LeetCode

這個面試跟傳統準備方式完全不同：

### 1. 練習讀別人的程式碼
Clone 一個中小型 open source 專案，給自己 15 分鐘理解架構，然後試著：
- 新增一個小功能
- 修一個 issue
- 寫一個新的測試

### 2. 練習跟 AI 協作
在 Cursor 或任何有 AI 的 IDE 裡：
- 練習寫精準的 prompt（「只實作 X 和 Y 函數」比「幫我解這題」好）
- 練習審查 AI 生成的 code
- 練習在 AI 給錯答案時自己修正

### 3. 跟 recruiter 要練習環境
Meta 有提供官方的 CoderPad 練習環境，主動要求試用。熟悉介面、熟悉 AI 工具、熟悉快捷鍵。

### 4. 練習 pipelining
60 分鐘很短。有經驗的候選人會在 AI 生成程式碼的同時：
- 審查上一段 AI output
- 或者向面試官解釋思路

這種「平行處理」是時間管理的關鍵。

---

## Checkpoint 邏輯：至少過 3 個

這個面試有明確的 checkpoint 系統。一個題目會有多個階段或子任務，每完成一個就是一個 checkpoint。

根據多份經驗分享：
- **3 個 checkpoint = 最低門檻**（但不保證過）
- **4+ checkpoint = 明顯加分**
- **沒過 3 個 = 幾乎確定被拒**

所以策略是：**先求廣度，再求深度**。確保基本功能都能動，再來優化。


---

## 這跟我的面試哲學有什麼關係？

回到我之前寫的「我不考 coding，只問為什麼」——Meta 這個新面試其實在測同一件事：**你的判斷力**。

我自己面試的時候，第一階段會直接問「為什麼」——為什麼用這個技術？比較過哪些選項？背後的原因是什麼？

第二階段我會給 take home homework，題目會比較複雜——通常是多系統串接之類的。為什麼選這種題目？因為多系統整合就連 AI 都很難輔助，需要很多實戰經驗才能處理好，這才能看出真正的能力。我會跟他說：「用 AI 可以，但你要能解釋出來，而且我會看最後成果的完成度。」

這跟 Meta 的 AI-Enabled 面試異曲同工：
- Meta 讓你在 AI 協作的過程中展現「為什麼」
- 我讓你在 take home 的過程中展現「為什麼」

當 AI 給你三種實作方式，你選哪一個？為什麼？
當 AI 的答案有 bug，你怎麼發現的？怎麼修的？
當時間不夠，你決定放棄優化先求功能完整，這個 trade-off 你怎麼想的？

**AI 時代，能寫 code 不稀奇，知道為什麼這樣寫才是你的價值。**

---

## 給準備面試的人的最後建議

1. **別再只刷 LeetCode**——我自己喜歡 LeetCode 是因為它讓我成長，而不是背誦八股題目。但這個面試測的是「讀 code」和「用 AI」的能力，光靠刷題準備不夠
2. **練習審查 AI output**——把 AI 當 junior，你是 senior reviewer
3. **練習溝通**——AI 時代，溝通變成剛需。不管是跟 AI 下 prompt 還是跟面試官解釋思路，你的思考過程要能清楚表達出來
4. **練習時間管理**——很多人反應就算有 AI，60 分鐘還是非常緊繃。這其實很考驗你跟 AI 協作的熟悉度，不是臨時抱佛腳能補的
5. **接受 AI 會出錯**——而且這正是面試官想看你怎麼處理的地方

---

## 參考資料

- [Meta's AI-Enabled Coding Interview: How to Prepare (Hello Interview)](https://www.hellointerview.com/blog/meta-ai-enabled-coding)
- [My First-Hand Experience with Meta's New AI-Enabled Interview (InterviewDB)](https://www.interviewdb.io/guides/meta-ai-enabled-interview)
- [Meta Software Engineer Interview: AI Assisted Coding Round (Prepfully)](https://prepfully.com/interview-guides/meta-ai-assisted-coding-interview)
- [Meta's AI-Enabled Coding Interview Guide 2025/2026 (Coditioning)](https://www.coditioning.com/blog/13/meta-ai-enabled-coding-interview-guide)
- [Reddit: Meta AI-assisted coding round 討論串](https://www.reddit.com/r/leetcode/comments/1p2i6op/anyone_recently_taken_metas_aiassisted_coding/)
- [TeamBlind: Meta AI-Enabled Coding Interview Experience](https://www.teamblind.com/post/meta-ai-enabled-coding-experience-ppb0lh1g)
