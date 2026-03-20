---
layout: post
title: "Opus vs Sonnet：Benchmark 看不太出來的體感差距"
date: 2026-03-20 09:00:00 +0800
permalink: /opus-vs-sonnet-real-gap-practical-guide/
image: /assets/images/opus-vs-sonnet-benchmark-gap-cover.png
description: "過去一個多月，我一直在 OpenClaw 和 Claude Code 上來回切換 Opus 跟 Sonnet。網路上一堆比較文章講什麼「全密計算架構」、「Dynamic Sparsity」——兩邊都是編的。這篇只講實際體驗到的、可驗證的差距，以及怎麼用工程手段讓便宜模型也夠用。"
---

# Opus vs Sonnet：Benchmark 看不太出來的體感差距

![Claude Opus 4.6 官網截圖](/assets/images/opus-vs-sonnet-benchmark-gap-cover.png)

**作者：** Wisely Chen
**日期：** 2026 年 3 月
**系列：** AI Coding 架構觀察
**關鍵字：** Claude Opus, Claude Sonnet, 模型選擇, Agent Engineering, IFEval, 長鏈推理, Skill 框架

---

## 先講結論

過去一個多月密集使用下來，我最大的感受是：在 Claude Code 上日常寫 code，大部分時候你不需要 Opus。但切到 OpenClaw 上跑長任務的時候，又會突然很喜歡 Opus——感覺就是在跟一個比較厲害的人合作，不管每件事情的工作質量都好那麼 5%。

Sonnet 大部分時候交出來的東西是 80 分，但它有時候會出問題——忘記前面講過的事、或是複雜一點的邏輯想不過來。Opus 就是比較靠譜，每件事都好那麼一點，而且真的很少崩。

差距存在，但比你想像的小。而且那個差距，有一大部分可以用工程手段補回來。

真正讓我有感的不是某個 benchmark 數字，是在 OpenClaw 上跑長任務跑到一半，Sonnet 開始「偷工減料」的那個瞬間——你會突然理解為什麼有些場景非 Opus 不可。但反過來說，我在 Claude Code 上日常 90% 的工作用 Sonnet 跑得好好的，硬要切 Opus 只是多花錢而已。

---

## 五個實際可驗證的差距

### 1. 任務做到一半，Sonnet 比較容易忘記前面講過的事

不是什麼「全密計算」，是更大的模型在多步驟推理中 context 維持能力更強。

具體表現：

- 重構 10 個檔案 vs 60 個檔案，Sonnet 在後者更容易「忘記」前面做過的決定
- 長對話後期，Opus 較少出現前後矛盾
- Sonnet 跑到 context 70-80% 的時候，品質會明顯下滑——前面答應過的規則開始忘、輸出開始重複或偷工減料

這不是 Sonnet 不好，是 context window 越用越深的時候，大模型的「記憶力」天生就比較強。

### 2. 規則給多了，Sonnet 就開始漏

IFEval（真正那個 benchmark）上 Opus 確實比 Sonnet 高，尤其是同時給 5 條以上約束的場景。

Sonnet 容易「滿足了 A 就丟了 D」。Opus 比較能全部守住。

但這裡有一個很多人沒注意到的細節：**禁止約束比要求約束難守住得多。**

「要求做 X」→ 模型生成時主動往 X 方向走，attention 自然會關注。

「禁止做 Y」→ 模型要在每一步生成時持續記得避開 Y，這是 suppression，認知負擔更高。

類比人類：叫你「寫一篇繁體中文的文章」很簡單，但叫你「寫一篇文章，不准用『的』這個字」，你寫到第三段就會不小心漏出來。

### 3. Opus 會先問你「確定嗎」，Sonnet 直接就做了

Opus 更傾向：

- 先質疑前提再回答
- 主動提出你沒問的風險
- 回答「這樣做可以，但你要注意…」

Sonnet 更傾向：

- 直接給你要的東西
- 快、有效率、但比較少主動 pushback

**這不是架構差異，是訓練策略的選擇。** Anthropic 在 Opus 上花了更多力氣訓練「慢下來想」的行為，Sonnet 則優先「快速有效地完成任務」。

這兩種風格沒有絕對的好壞。code review 的時候你要 Opus 的審慎度，寫腳本的時候你要 Sonnet 的速度。

### 4. 速度 & 成本——Sonnet 的絕對優勢

- Sonnet 快 3-5 倍（tokens/sec）
- 成本大約是 Opus 的 1/3 到 1/5
- 對 90% 的日常任務，速度帶來的體驗提升 > Opus 的品質增量

這是很多人忽略的：**人類的注意力也是成本。** Opus 跑一個任務慢 3 倍，你等待的時間就是被浪費的。Sonnet 快速完成 → 你快速 review → 不滿意就再跑一次，兩次 Sonnet 的成本可能還比一次 Opus 便宜。

### 5. 「難以 benchmark 但真實存在」的差距

很多人說 Opus 的 "vibes" 更好——這聽起來不科學，但實際上反映的是：

- **隱含推理深度：** 同一個問題，Opus 更常考慮到第二、第三層影響
- **創意品質：** 寫作、命名、架構設計上，Opus 的選擇更有層次感
- **少幻覺：** 不確定的時候，Opus 更傾向說不知道

舉一個我自己的例子。有一次在 OpenClaw 上跟它說「寄信給 Amy」，但系統不知道 Amy 是誰。Sonnet 的做法是問我：「Amy 的 email 是什麼？」——合理，但多了一步。Opus 的做法是自己跑去過去的歷史紀錄裡翻，發現只有一個 Amy，直接就寄出去了。

這種差距你沒辦法用 benchmark 測，但體感上就是：Opus 多想了一步，少問你一次，事情就這樣順順地完成了。

---

## 深入分析：禁止約束為什麼這麼難

這個部分值得單獨拉出來講，因為它直接影響你怎麼設計 Agent 的 system prompt。

假設你的 system prompt 寫了：

- 不要刪除現有檔案
- 不要修改 package.json
- 不要用 any type
- 不要自動 commit
- 不要改測試檔案

| 約束數量 | Sonnet | Opus |
|---------|--------|------|
| 1-3 條禁止 | 幾乎都守住 | 都守住 |
| 4-6 條禁止 | 開始偶爾漏 1 條 | 大致守住 |
| 7-10 條禁止 | 常漏 2-3 條，尤其後面幾條 | 偶爾漏 1 條 |
| 10+ 條禁止 | 不可靠 | 也會開始漏，但頻率低很多 |

**Sonnet 漏約束有明確的 pattern：**

1. **位置偏差：** 越後面寫的越容易被忽略。第 1 條禁止幾乎不會漏，第 8 條就很危險
2. **任務衝突：** 跟主任務衝突的禁止最容易漏。你叫它重構但又說不能改 X 檔案，它重構到一半就忘了
3. **Context 衰減：** Agent 跑到第 20 步，早期的「不要」已經幾乎沒用。這是最大的問題

Opus 也會漏，但閾值高很多。第 3 點的衰減速度是兩者最大的差距。

**但不管用 Opus 還是 Sonnet，寫一堆「不要」本身就是 anti-pattern。** 這也是我在[那篇文章](/prompt-guides-engineering-constrains-agent-principle/)裡反覆強調的：

> Prompt 負責引導，不負責約束。工程負責約束，不依賴模型自覺。

禁止條目控制在 5 條以內，能用工程約束的就不要用 prompt（chmod 444、CI gate、pre-commit hook）。這比換 Opus 便宜多了，而且更可靠。

---

## 三種長期 Job 的模型選擇

不是所有「長時間跑的任務」都需要 Opus。要分清楚類型：

### 情況一：單次長任務（一口氣跑完）

例如：重構整個 codebase、寫 20 頁報告、分析 100 封信。

**→ Opus 勝。**

Context window 越用越深，Opus 在後半段不容易降智。Sonnet 跑到 context 後段，前面答應過的規則開始忘、輸出開始重複。

### 情況二：重複性排程任務（cron / heartbeat）

例如：X digest、Gmail digest、blog 自動發布。

**→ Sonnet（甚至更便宜的模型）就夠。**

- 每次執行都是獨立 session，context 從零開始，不存在「長鏈退化」問題
- 任務結構固定（讀 state → 執行 → 更新 state），不需要深度推理
- 一天跑 10-20 次，成本差 3-5 倍會累積成很大的數字
- 速度快 = job 完成時間短 = 排程不容易撞車

### 情況三：多輪互動的持久 Session

例如：coding session 來回改好幾天。

**→ 最尷尬的場景。**

- Opus 推理品質更穩，但 token 成本爆炸（尤其 conversation 越來越長）
- Sonnet 便宜快，但到第 15-20 輪之後容易出現「前後打架」

**實戰做法：** 用 Sonnet 開頭，到了關鍵決策點（架構定案、merge 前 review）手動切 Opus 跑一輪。

---

## 長 Agent 工作：Opus 的真正主場

像 Claude Code / Codex 這種一次跑幾十分鐘、改幾十個檔案的 agentic coding 場景，重點不在「每一步多聰明」，而是整個 session 下來不崩。

Opus 在這裡有四個明確優勢：

1. **不會半途「忘記計畫」：** Agent 跑到第 30 步，Sonnet 容易偏離最初的架構決定。Opus 對早期指令的 recall 明顯更好
2. **不會「自作聰明」地簡化：** Sonnet 在 agent loop 跑久了之後，會開始走捷徑——跳過測試、省略 error handling、用 placeholder 代替完整實作
3. **錯誤修復不會越修越爛：** test fail → 修 → 又 fail → 再修。Sonnet 到第 3-4 輪 retry 容易開始亂改。Opus 更能維持一致的修復策略
4. **多檔案改動的一致性：** 改 A 檔的 interface → 要更新 B、C、D 的 import 和 type。Opus 比較不會漏改

但 Opus 不是萬能：

- 一次長 agent session 可能燒 50-100k tokens，Opus 跑一次的成本可能是 Sonnet 的 5 倍
- 速度慢 = feedback loop 慢，整體完成時間拉長很多

**最貴的不是 token，是 agent 跑了 20 分鐘結果爛掉你要重來。**

這句話反過來也成立：如果任務 scope 小（改 2-3 個檔案），用 Opus 就是浪費錢。

---

## 關於架構的真相：我們不知道

Anthropic 從來沒公開過 Opus 或 Sonnet 的架構細節。Dense vs MoE、參數量、layer 數——全部都沒說。

業界猜測 Opus 是 dense、Sonnet 是 MoE 或較小的 dense。但這全部是推測，沒有任何官方確認。

那些文章寫的「採用全密計算架構」vs「Dynamic Sparsity」——兩邊都是拿未經證實的猜測包裝成確定事實。

**架構是 why，表現是 what。We know the what, not the why。**

不管底層是 dense 還是 MoE，表現上的差異是真實可量測的。專注在可驗證的表現差異上，比猜架構有用得多。

---

## 用 Skill 框架消除模型差距

與其砸錢用 Opus 跑所有任務，不如把任務設計得讓便宜模型也能做好。核心思路就是我之前寫的那個原則：[Prompt 負責引導，工程負責約束](/prompt-guides-engineering-constrains-agent-principle/)。

Skill 框架怎麼做到的：

### 1. 消除「長 context 退化」

每次 cron 觸發都是全新 session → 讀 SKILL.md → 執行 → 結束。Context 永遠乾淨，便宜模型也不會降智。

### 2. 工程約束直接寫死在 Skill 裡

你不用靠「不要做 X」的 prompt，而是：

- SKILL.md 定義明確步驟（step 1 → step 2 → step 3）
- state.json 管狀態，模型只需要讀 → 做一步 → 寫回
- 錯了就是 script 層擋掉，不是靠模型自律

### 3. 任務 scope 被框住了

便宜模型最大的問題是「scope 一大就出事」。Skill 把大任務拆成小步驟，每一步對便宜模型來說都是簡單任務 → 正確率很高。

### 4. 可測試、可迭代

Skill 寫好之後可以手動跑一次確認結果，有問題改 SKILL.md，不用改模型。相當於你在 debug 流程而不是 debug 模型行為。

**一句話：Skill = 把智慧從「模型」搬到「流程」。流程穩了，模型就只是執行器，用便宜的就夠。**

---

## 坦白說

幾個我沒有把握的地方：

**第一，「禁止約束衰減」的數據是觀察值，不是嚴謹實驗。** 我沒有跑過 1000 次 A/B test 來量化 Sonnet 在第 7 條禁止約束的遵守率到底是 72% 還是 85%。這是基於日常使用的經驗歸納，有 pattern 但不夠精確。

**第二，Opus 的優勢會隨著模型更新縮小。** Sonnet 4.5 出來之後搞不好就追上了。模型能力是移動目標，今天的結論可能半年後就過時。

**第三，「vibes 更好」這個維度我自己也覺得不科學。** 但我不知道怎麼量化它，而且它確實影響使用體驗。如果有人找到好的量化方法，我很想知道。

**第四，Skill 框架不是萬能的。** 任務本質需要判斷力的場景（信件該不該 flag 為 urgent、文章品質好不好），Skill 框不住，還是得靠模型本身的能力。

---

## 實戰建議

### 模型選擇

| 場景 | 選誰 | 原因 |
|------|------|------|
| 日常 coding、腳本、快問快答 | Sonnet | 速度 > 品質增量 |
| 大規模重構、架構決策 | Opus | 長鏈推理穩定性 |
| 寫文章、翻譯、內容生成 | Sonnet 夠用 | 成本敏感 |
| Code review、安全審計 | Opus | 審慎度 + 不漏 |
| 成本敏感的 API 調用 | Sonnet | 1/3 到 1/5 成本 |
| 一次要對、沒有人 review 的任務 | Opus | 容錯空間為零 |
| 重複性排程 cron job | Sonnet / Haiku | 獨立 session，不需深度推理 |
| 探索性 prototyping | Sonnet | 反正要丟掉重寫 |

### 約束設計原則

1. 禁止條目控制在 5 條以內——多了連 Opus 也不可靠
2. 最重要的禁止放最前面——位置偏差是真的
3. 能用工程約束的就不要用 prompt——chmod 444 比「不要修改」可靠 100 倍
4. 長 agent session 定期重複關鍵禁止——對抗 context 衰減
5. 把「不要做 X」改成「做 Y 的時候，先檢查 Z」——給模型正面指令比負面約束好守

### 長期 Job 策略

- **重複跑的 cron job → 用便宜的**，每次獨立 session 不退化
- **一次性的重要任務 → 用 Opus**，錯了重來的成本更高
- **持久 session → 混用**，Sonnet 開頭，關鍵點切 Opus

---

## 一句話總結

**重複跑的 cron job 用便宜的，一次性的重要任務用 Opus。把 Opus 預算留給真正需要深度思考的場景。**

不是哪個模型更好的問題，是你有沒有把對的模型放在對的位置。
