---
layout: post
title: "OpenAI 暫停 $200 Pro 新訂閱：Astra 需求炸鍋，我剛好前一天升級完"
date: 2026-09-11 09:00:00 +0800
permalink: /openai-pro-pause-astra-demand-20x-comparison/
tags: [OpenAI, GPT-6, Astra, Pro, 訂閱, Codex, Claude, 20x, 額度, 算力]
categories: [AI 產業分析]
image: /assets/images/openai-pro-pause-astra-tibo-announcement.png
description: "9 月 10 日，OpenAI 工程師 Tibo 正式宣布暫停 $200 Pro 新訂閱，原因是 GPT-6 Astra 的需求「前所未有」。我前一天剛升級完 $200 Pro。這篇記錄暫停事件本身、社群兩極反應，以及一個很少人講清楚的事：同樣叫 20x，OpenAI Codex 的 20x 和 Claude 的 20x 到底差在哪。"
author: Wisely Chen
---

9 月 9 日下午，OpenAI 的 Codex 工程師 Tibo 在 X 上發了一則貼文，大意是 Astra 需求爆了，他們「至今沒見過這種場面」，可能要暫停新的 Pro 訂閱。那則貼文拿了兩萬一千個讚、七百萬次瀏覽。

隔天 9 月 10 日，正式宣布：**$200 ChatGPT Pro 暫停接受新訂閱，重開時間未定。**

我前一天剛升級完。

## 暫停了什麼、沒暫停什麼

先把範圍釘死，因為中文圈的傳播已經走樣了。

| 項目 | 狀態 |
|------|------|
| $200 Pro 新訂閱 | 暫停 |
| 既有 $200 Pro 帳號 | 不受影響 |
| $20 Plus | 正常開放 |
| $100 Pro（非 20x） | 正常開放 |
| API | 正常開放 |
| 重開時間表 | 未公布 |

Tibo 的原文講得很白：

> These put the most strain on our systems and we wanted to take the smallest step that allows us to continue giving the broadest access possible.

翻成白話：$200 Pro 用戶一人吃的算力太大，先堵住入口，讓其他所有人能繼續用 Astra。

這不是 OpenAI 第一次幹這種事。2023 年他們暫停過 Plus 新訂閱，當時 ChatGPT 剛爆紅。國內的 Kimi、GLM 之前也分別做過暫停訂閱和限量開售。但以 OpenAI 今天的規模，再次走到這一步，代表 Astra 的需求確實超過了他們能即時補上的算力。錢可以馬上收，GPU 沒辦法馬上變出來。

## 我為什麼剛好前一天升級

沒有什麼神預測。單純是 Astra 上線後用了幾天，覺得在 Codex 上跑 agent 任務比 Claude Code 省步驟（後面會講為什麼這個感覺可能有誤差），加上看到 Tibo 9 月 9 日那則「可能要暫停」的預告，想說先卡位。

結果隔天真的停了。

現在 X 上已經有人在喊「Pro 帳號會不會開始倒賣」。我不確定這是玩笑還是認真的，但帳號制的東西一旦停售，二手市場的想像力從來不會讓人失望。

## 社群反應：兩極分化

搜了 X 上的討論，大致分成三派。

**「需求是真的」派：**

Token Gremlin 說「Astra demand really is that insane」。TheValueist 把這當成 GPU 基礎設施股的利多訊號。FlowOps Daily 說「昨天還被罵飢餓行銷，今天真的停了」。

**「品質已經在掉了」派：**

這派聲量其實更大。leo（@synthwavedd）說 Astra 變慢也變笨了，然後你還買不到 Pro。Tim Jayas 說他的 Astra 體感像 GPT-5.6 Sol，「如果不修好大家就要回去用 Claude 了」。Elaina 寫了一段更長的：

> We went from an astonishing Astra launch to degradation, limits, overload, and paused subscriptions in a matter of days.

有人甚至懷疑 OpenAI 把算力從 Astra 搬去跑下一個模型 GPT-6 Sol。alex getman 列了三個訊號試圖串在一起：暫停 Pro、Sol 出現在測試 API、Astra 明顯變弱。Tibo 後來否認智力被削弱，但社群不太買帳。

另一個值得注意的：Choblin 貼了 Astra 發布時 vs 現在的輸出對比，同一個 prompt，產出品質有明顯差異，懷疑被 quantize 了。

**「Plus 用戶更慘」派：**

BridgeMind 花 $20 買了 Plus 來測 Codex 額度，一個 Astra session 跑了大約三十分鐘，用掉了**整個禮拜**額度的 92%。不是五小時的額度，是一整週的。$20 一個月大概只夠你一週跑一次 Codex。

## 同樣叫 20x，此 20x 非彼 20x

這是我最想講的部分，因為這件事很少人講清楚。

市面上現在有兩個 $200/月的「20x」方案：

- **OpenAI Pro 20x**（就是這次被暫停新訂閱的）
- **Claude Max 20x**

名字一樣，機制完全不同。

### OpenAI Codex 20x

根據多個用戶實測回報，Codex 的 20x 在 session 和 weekly 額度上都是真的 20 倍。stafa 說他在暫停前一晚鎖定了 Codex 20x，「weekly usage on codex 20x vs. the weekly usage on claude 20x is night and day」。Júlia 也說 Codex 20x 持續時間遠超 Claude 20x，而且 OpenAI 還會隨機重置額度。

但也有反面報告。PersonalJarvis 說他在 $200 Codex 20x 上四小時就燒完整週額度，反而覺得 Claude Max 20x 配 Fable 5.1 用起來更久。Ajay 甚至說他的 Claude 5x 體驗比 Codex 20x 好。

### Claude Max 20x

這裡有一個被告上法院的爭議。

Anthropic 的定價頁寫「Choose 5x or 20x more usage than Pro」，直覺理解就是 $200 方案應該是 $100 方案的四倍用量。但頁面下面才說：**這個倍數只適用於每五小時的 session 額度，不適用於每週上限。**

X 上一則拿了三千三百個讚的拆解（@kimmonismus）引用了一個六月提起的集體訴訟：

> Max 5x delivers around 3.5x Pro's weekly usage, while Max 20x delivers just 6–8x. In practice, the $200 plan provides only around 2x the weekly usage of the $100 plan.

也就是說：

| 方案 | 5 小時 session 額度 | 每週額度 |
|------|-------------------|---------|
| Claude Max 5x ($100) | Pro 的 5 倍 | Pro 的 ~3.5 倍 |
| Claude Max 20x ($200) | Pro 的 20 倍 | Pro 的 ~6-8 倍 |
| $200 vs $100 的倍率 | 4 倍 | **約 2 倍** |

五小時的 session 限制內，20x 是真的。但你一天工作超過五小時，每週額度就變成了真正的瓶頸，而那個數字跟名字上的「20x」差距很大。

OrcDev 那則「Claude Max gives you 20x usage, BUT only for the 5-hour session limit. Not for the weekly limit!」拿了 272 個讚。Adam Badar 更直接：「1 codex 20x > 3 claude 20x」。

### 我的實際體感

我同時用兩邊。體感上 Codex 20x 的週額度確實比 Claude 20x 寬裕，但這也跟使用模式有關：Codex 跑 agent 任務時 Astra 本身比較省 token（OpenAI 自己的說法是 Astra 在 coding 場景更 token-efficient），同樣的功能 Fable 5.1 可能用更少步驟完成但每步 token 數更高。

這不是「誰比較好」的問題，是「你付的錢到底買了什麼」的透明度問題。Claude 20x 的五小時 session 額度是真的 20 倍沒錯，但你在決定要不要從 $100 升到 $200 的時候，真正卡你脖子的是週額度，而那個倍率大概只有 2 倍。

## 這件事的三個觀察

**第一，算力瓶頸是真的。** 不管你怎麼解讀 OpenAI 的動機（真缺算力 vs 飢餓行銷），暫停 $200 Pro 新訂閱這個動作本身就代表了一件事：包月制度下，收入是固定的，但用戶調用 agent 跑任務消耗的算力是浮動的。$200 看著貴，但對應的無限制 Astra 存取一旦被充分使用，每個用戶的實際成本可能遠超 $200。

**第二，「暫停」可能變「常態」。** 2023 年暫停 Plus 是因為 ChatGPT 爆紅。這次是因為 Astra 太強。下一次可能是因為 Sol。前沿模型每次迭代的推理成本都在漲，但訂閱價格很難同步漲上去。暫停新訂閱可能變成每次大模型上線的標準操作。

**第三，訂閱制的 20x 承諾需要更好的揭露機制。** OpenAI 和 Anthropic 都有「20x」方案，但量測方式不同、限制機制不同、實際體驗差異巨大。用戶在掏 $200 之前，應該能看到一個比「20x」更精確的數字。Anthropic 已經因為這個被告了，OpenAI 現在直接暫停入口——兩種不同的應對，但根本問題一樣：你賣的到底是什麼。

## 後記

寫這篇的時候，我的 $200 Pro 帳號還能正常用 Astra。體感上跟第一天比確實有變慢，但我沒辦法確認是被 nerf 了還是純粹伺服器在負載高峰。

如果你現在想升 $200 Pro，等。Tibo 說正在全速擴容，但沒有給時間表。

如果你已經是 $200 Pro，你不受影響。但你可能會感受到 Astra 品質的波動——當算力被分配給更多既有用戶和擴容測試時，這幾乎是必然的。

如果你在考慮 Claude Max 20x vs OpenAI Pro 20x，搞清楚你真正的使用瓶頸是 session 額度還是週額度，再決定。名字一樣，東西不一樣。
