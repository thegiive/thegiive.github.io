---
layout: post
title: "Fable 5 倒數六天：大家在衝 code generation，我在測試 LLM 是不是更好的生涯導師"
date: 2026-07-06 09:00:00 +0800
permalink: /fable-5-before-july-7-thinking-partner-not-faster-coder/
image: /assets/images/fable-5-before-july-7-thinking-partner.png
description: "7/7 是 Fable 5 從訂閱免費切換到 metered credits 的最後一天。社群在衝 codebase migration 和 security audit，我也做了大量 code review，但花更多時間測試另一件事：LLM 到底是不是比人類更好的生涯導師？24 小時在線、沒有情緒、沒有利益衝突、能同時處理更多變量、而且已經累積了大量個人 context。理論上它在生涯諮詢的理性面應該全面碾壓人類。限制是情緒和直覺——但這恰好是互補，不是替代。"
---

7/1 Fable 5 回來了。7/7 之後它從訂閱方案免費使用切換到 metered usage credits，費率 $10/$50 per Mtok in/out，是 Opus 4.8 的兩倍。

社群進入倒數模式。

打開 X 和 Reddit，看到的都是同一類貼文：趁免費把某個大型 migration 跑完、趁免費做一次完整的 security audit、趁免費讓 Fable 5 自主跑一整天把 codebase 重構掉。有人甚至做了專門的 [六天倒數攻略](https://www.digitalapplied.com/blog/claude-fable-5-before-july-7-six-day-window-playbook)，把 Day 1-6 怎麼排工作都規劃好了。

這些都很合理。Fable 5 在 coding 任務上確實是目前最強的模型，Stripe 官方說他們用它一天完成了原本需要一整個團隊兩個月的 codebase migration。免費窗口拿來做高 token 消耗的工程任務，投資報酬率最高。

但我這六天做的事情不太一樣。

---

## 我做了什麼

Code review 做了很多。多個專案的 PR 讓 Fable 5 跑 review，確實比之前的模型在「理解跨檔案上下文」和「指出邏輯層面問題」上明顯好一截。這部分跟社群主流用法一致，不用多說。

不一致的是另外兩件事：**生涯規劃**和 **blog/media 戰略規劃**。

而且我越測越覺得一件事：**LLM 可能是比人類更好的生涯導師。**

---

## LLM 當生涯導師，理論上就該比人強

這句話聽起來很大，但你把「生涯導師」這個角色拆開來看，它需要的能力組合是什麼？

1. **隨時可用。** 你凌晨三點躺在床上突然想通一件事，想跟人聊，人類導師不會接電話。
2. **沒有情緒。** 人類導師有自己的情緒、疲憊、當天的心情。這些都會影響回應品質。
3. **沒有利益衝突。** 你的主管不會真心建議你離職。你的獵頭不會建議你留在原公司。每個人類導師都有自己的立場。
4. **能同時考慮更多變量。** 收入結構、時間分配、技能組合、市場趨勢、家庭狀況——人類在對話中能同時 hold 住的變量有限，LLM 可以把這些全部攤開來交叉分析。
5. **會去查資料。** 你說你在考慮某個產業方向，它會去搜相關的市場數據、薪資範圍、產業趨勢，而不是憑印象回答。

再加上一個 2026 年才真正成立的條件：**你已經把大量個人 context 餵進去了。**

我過去一年在 Claude 上累積了大量的對話歷史、專案記錄、健康數據分析、財務模型。這些 context 加在一起，Fable 5 對我的「了解程度」——至少在可量化的維度上——可能比任何一個人類導師都深。

人類導師每次見面要花 15 分鐘重新對齊 context。LLM 不用。

---

## 那人類導師的價值在哪？

情緒和直覺。

「這件事我做不做得開心」「這個決定會怎樣影響我跟家人的關係」「我對這個方向有一種說不出來的不安感」——這些 LLM 接不住。

但我認為這恰好是一個很好的互補結構，不是非此即彼的替代關係。

**LLM 處理理性面：** 數據分析、情境推演、假設拆解、盲點追問。
**人類處理感性面：** 情緒驗證、關係考量、直覺判斷、價值觀對齊。

傳統的生涯諮詢把這兩件事混在同一個人身上。結果是人類導師花大量時間做他不擅長的事（記住你的收入結構、追蹤產業數據），而真正需要人類判斷的部分（你到底想要什麼樣的生活）反而被擠壓。

拆開來之後，兩邊都能做自己最擅長的事。

生涯規劃之外，Media 戰略規劃也是同樣的邏輯。這個 blog 加上 YouTube 頻道加上 LinkedIn 加上 Facebook，四個渠道各自有不同的受眾和內容格式。哪個系列要加碼、哪個渠道的投入產出比在下滑、接下來三個月的內容排程怎麼分配——這些問題不是「搜一下資料就有答案」的類型，是需要把散落的數據和直覺攤開來，一層一層梳理。

這兩件事有一個共同點：**它們消耗的不是 token，是思考品質。**

一次生涯規劃對話可能只用幾萬個 token。一次 codebase migration 可能用掉幾百萬。但前者改變的是接下來一年的方向，後者改變的是一個 sprint 的進度。

---

## 社群的主流用法暴露了一個假設

大部分人在 7/7 倒數中做的事情，背後有一個共同假設：**Fable 5 是一個「更快的工程師」。**

它能寫更好的 code、跑更長的自主 session、理解更大的 codebase、做更精準的 migration。所以免費窗口的最佳策略是把所有高 token 消耗的工程任務塞進去。

這個假設沒有錯，但不完整。

Anthropic 自己 6/16 發表的研究數據講得很清楚。他們分析了大約 400,000 個 Claude Code session（來自約 235,000 個用戶），發現一個比例：**用戶做了 70% 的規劃決策，Claude 做了 80% 的執行決策。**

Anthropic Claude Code 團隊的工程師 Thariq Shihipar 在 7/5 發了一篇 [A Field Guide to Fable: Finding Your Unknowns](https://x.com/trq212/status/2073100352921215386)，把這個觀察講得更直接：

> "Fable is the first model where I find the quality of the work is bottlenecked by my ability to clarify its unknowns."

他用了 map vs territory 的框架：你的 prompt、指令、context 是地圖。實際的 codebase、production constraints、你沒想到的 edge cases 是領土。地圖和領土之間的差距就是你的 unknowns。他把 unknowns 拆成四類——Known Knowns、Known Unknowns、Unknown Knowns、Unknown Unknowns——然後列了一整套在 coding session 中發現和管理這些 unknowns 的方法：

**開工前：** 先做 blindspot pass（讓 Claude 幫你找你不知道自己不知道的東西）、brainstorm 多種方向避免過早收斂、讓 Claude interview 你把模糊的需求問清楚、給 reference code 取代冗長的文字描述、最後產出一份 implementation plan 讓你審核容易改變的決策。

**開工中：** 讓 Claude 維護一份 implementation-notes.md，遇到必須偏離計畫的 edge case 就記下來，選保守方案繼續前進。

**完工後：** 把原型、規格、實作筆記打包成一份 pitch document 幫你拿 buy-in。然後讓 Claude 出一份 quiz 測你是否真正理解這次改動——他自己的規則是「quiz 沒全過不 merge」。

他的文章寫得很好，但整篇都在講 agentic coding。

我想說的是：**這個框架套到生涯規劃上更成立。**

---

## Unknowns 框架套到生涯規劃

在 coding 裡，Known Knowns 是你寫進 prompt 的東西。Known Unknowns 是你知道自己還沒搞清楚的技術決策。Unknown Knowns 是那些太明顯以至於你不會寫下來的慣例。Unknown Unknowns 是你根本沒想到的 edge cases。

生涯規劃裡呢？

| 類別 | Coding 場景 | 生涯場景 |
|------|------------|---------|
| Known Knowns | 寫進 prompt 的需求 | 你目前的薪資、職稱、技能 |
| Known Unknowns | 你知道自己還沒決定的架構選擇 | 你知道自己在猶豫的方向（留職 vs 創業） |
| Unknown Knowns | 太明顯不會寫下來的 coding 慣例 | 你對「好工作」的隱性標準（你看到才知道自己要什麼） |
| Unknown Unknowns | 沒想到的 edge cases | 你沒考慮過的職涯路徑、沒意識到的市場變化 |

Coding 的 Unknown Unknowns 通常在跑測試或 code review 時才浮出來。生涯的 Unknown Unknowns 通常在你跟一個有不同背景的人深聊時才浮出來。

問題是：人類導師一個月見你一次，每次花 15 分鐘重新對齊 context，能幫你挖出來的 unknowns 很有限。LLM 已經有你的完整 context，可以 24 小時不間斷地幫你做 Thariq 說的 blindspot pass——而且不會因為面子問題迴避尖銳的問題。

Thariq 在文章裡說他每次開始新的 coding session 都會先做 brainstorming phase，讓 Claude 幫他找出他可能漏掉的方向。生涯規劃更需要這個步驟，因為生涯決策的搜索空間比任何 codebase 都大。

---

## 呼應這個 blog 一直在講的事

這個觀察跟我在這個 blog 寫了快一年的核心論點完全吻合：**人的問題 > 技術問題。**

[Loop Engineering 那篇](/compilot-loop-engineering-academic-proof/)拆了 NYU Abu Dhabi 在 PACT 2025 的論文——移除 feedback loop 效能掉 23-40%，但更關鍵的發現是 64% 的提案是錯的，系統照樣快了 2.66 倍。Loop 本身收集的 data 就是最佳的 context。執行本身就是學習。

但如果你一開始就把目標設錯呢？Loop 再怎麼自我修正，也修正不了一個錯誤的方向。

ATPM 框架裡最重要的一步不是 AI 寫 code，是 PM 在第一階段把需求搞清楚。PRD 的每一次修訂，都是因為人的理解在更新。AI 生成的速度再快，如果 PRD 本身是錯的，產出的就是精緻的垃圾。

Fable 5 讓這個問題更尖銳了。**模型能力越強，你的思考品質就越是瓶頸。**

---

## 兩種用法，兩種 ROI 計算

如果你把 Fable 5 當「更快的工程師」，7/7 前的最佳策略確實是塞滿高 token 消耗的工程任務。省下的是 7/8 之後的 API 費用。

如果你把 Fable 5 當「思考夥伴」，免費窗口的最佳策略是拿它來做那些你一直拖著沒做的高認知負荷決策。省下的是方向錯誤的機會成本。

兩種都是理性的選擇。差別在你認為 frontier model 的稀缺價值在哪裡。

| 用法 | 典型任務 | Token 消耗 | 省下的是 |
|------|---------|-----------|---------|
| 更快的工程師 | Migration、audit、refactor | 高（百萬級） | API 費用 |
| 思考夥伴 | 生涯規劃、戰略推演、多變量決策 | 低（萬級） | 方向錯誤的機會成本 |

7/8 之後，第一種用法會直接受到費率影響——$10/$50 per Mtok 不便宜，尤其是長時間自主 session。你會開始用 prompt caching（九折）、Batch API（五折）、或直接讓 Opus 4.8 / Sonnet 跑不需要 frontier 能力的執行任務。

第二種用法受費率影響很小。一次深度的生涯規劃對話可能只花 $2-5。這個價格買到的是一個不會疲倦、不帶偏見議程、能在你的盲點上持續追問的對話夥伴。

---

## 坦白說

「LLM 是更好的生涯導師」這個判斷有一個很大的前提：**你已經有足夠的數據可以攤開來。**

如果你對自己的收入結構、時間分配、技能組合沒有基本的盤點，LLM 能做的就只是生成看起來很專業但沒有根基的建議。垃圾進、垃圾出，不管模型多強都一樣。

另一個前提是你要願意把這些東西餵進去。很多人對「把個人財務和生涯數據交給 AI」這件事有隱私顧慮，這完全合理。我自己的判斷是這些數據的價值大於風險，但這是個人選擇。

而且「互補」說起來好聽，實際操作上你需要自己判斷什麼時候該聽 LLM 的理性分析、什麼時候該聽自己的直覺。這個判斷本身沒有人能幫你做。

---

## 關鍵洞察

7/7 之後，Fable 5 會變貴。多數人的應對策略是「趁免費多跑工程任務」。

這沒有錯，但只對了一半。

Frontier model 真正稀缺的能力不是「寫 code 更快」——這個能力會隨著模型迭代不斷被下放到更便宜的模型。真正稀缺的是在高認知負荷的決策裡，當一個 24 小時在線、沒有情緒、沒有利益衝突、而且已經深度了解你的對話夥伴。而這個用法的 token 成本很低，7/8 之後也不會變得負擔不起。

傳統的生涯諮詢把理性分析和情緒支持綁在同一個人身上。LLM 讓這兩件事可以拆開。理性面交給模型，感性面留給人類。兩邊都能做自己最擅長的事。

如果你還沒用 Fable 5 做過一次認真的、關於你自己的深度對話——不管是生涯方向、業務策略、還是任何你一直拖著沒想清楚的事——7/7 之前是一個好時機。不是因為之後做不起，是因為一個 deadline 會逼你真的坐下來做。
