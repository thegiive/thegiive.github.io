---
layout: post
title: "Agent 也需要「及時反饋」：Effective Feedback Compute 與 Agent 的 deliberate practice"
date: 2026-06-02 06:00:00 +0800
permalink: /agent-harness-effective-feedback-compute/
image: /assets/images/agent-harness-efc-logo.png
image_alt: "Scaling Laws for Agent Harnesses via Effective Feedback Compute 論文首頁"
description: "又到了週二讀論文。這篇 Scaling Laws for Agent Harnesses via Effective Feedback Compute 告訴我們：無腦加 Agent 很多時候是錯的，甚至是最差解之一。有用的反而是人類驗證過的老路——『及時反饋』deliberate practice。論文提出 EFC（有信息量、可靠、不重複、被拿去改決策），等預算下只提升反饋品質，成功率從 27% 跳到 90%。也聊了要不要導入 mem0。"
---

又到了週二讀論文。

這一篇 [Scaling Laws for Agent Harnesses via Effective Feedback Compute](https://arxiv.org/abs/2605.29682) 告訴我們一件很反直覺的事：**無腦加 Agent，很多時候是錯的。** 不只不是最佳解，甚至可能是最差解之一。

那什麼才有用？答案出乎意料地老派——**走人類驗證過、行之有年的路：「及時反饋」（deliberate practice）。** 只要給 Agent 的反饋夠具體、夠可靠、而且能進到下一次決策裡，這套在人身上有效的東西，論文證明在 Agent 身上一樣有效。

## 先看數據：raw compute 只能解釋三四成

論文直接量化給你看：用 raw tokens 跟 tool calls 去解釋任務成功率，R² 只有 **0.33–0.42**。

換句話說，你燒了多少 token、調了幾次工具，大概只能解釋三四成的結果。**剩下六成，跟 raw compute 無關。**

我問了幾個也在做 Agent 落地的朋友，差不多都有類似的感覺。很多時候為了更快加速能力，第一反應就是「加」：把 tool log 開到 verbose、把 retry 從 1 次加到 3 次、再掛兩個工具進去。

結果呢？成本跟時間直接翻倍，但 Agent 只是把同一個錯誤判斷「更詳細地」重複了三遍。

**它不是更聰明了，它只是更忙了。**

## 轉折：Effective Feedback Compute（EFC）

論文的核心概念叫 **Effective Feedback Compute（EFC）**。它的定義很關鍵——不是所有互動都算數，只有同時滿足四個條件的反饋，才算「有效」：

1. **Informative**：真的帶來新訊息，不是廢話。
2. **Valid**：可靠、可信，不是雜訊或幻覺。
3. **Non-redundant**：不是把已經知道的再講一遍。
4. **Retained**：真的被 Agent 拿去改變了下一步決策。

最狠的是這個對照實驗：**在 raw compute 預算「固定不變」的前提下**，只去提升反饋的品質，任務成功率從 **27% 拉到 90%**。

成本沒變，只是反饋變有效，成功率三倍跳。

把 EFC 換算法套上去重新解釋成功率，R² 從 0.33 直接跳到 **0.94–0.99**。差距大概就是「你以為在衡量能力，其實在衡量忙碌」跟「你真的在衡量能力」的差別。

## 這根本就是學習理論的「及時反饋」

讀到這裡我整個被點醒——這套說法，跟學習理論講的「及時反饋」幾乎是同一件事。

deliberate practice 的核心就三點：反饋要**具體**、要**可被行動**、要**進到下一次練習裡**。對照 EFC 四條件，幾乎是一一對應：

- 具體 → **Informative**
- 正確 → **Valid**
- 進到下一次 → **Retained for subsequent decisions**

EFC 的 retained，根本就是學習科學裡「feedback loop 有沒有閉合」的翻版。練了不檢討、檢討了不改，等於沒練——Agent 也一樣。

而且這帶出一個更狠的推論：**Agent 再怎麼努力、再怎麼「練一萬小時」，如果反饋沒閉合，一樣不會變強。** 一萬小時定律從來不是「時數」的定律，是「有反饋的刻意練習」的定律。無腦堆 compute，就是讓 Agent 練了一萬小時無效的球。

## 那要不要導入 mem0 這類 memory 架構去記錄反饋？

這是我讀完第一個冒出來的問題。直覺答案是「該導」，但我會加一個但書。

Memory 架構（[mem0](https://github.com/mem0ai/mem0)、Letta 這類）命中的是四條件裡最難的第四條「retain」——但它**只**解決 retain，不會幫你過濾前三條。

如果你把雜訊、幻覺、重複的反饋也一股腦存進去，這些錯誤記憶會被反覆檢索出來，**毒性比沒記憶還大**——等於把「更忙」這件事，從單輪放大到跨 session。

這點人類的及時反饋老早就知道了：好的反饋要具體、要對，不是什麼奇怪訊息都往腦袋裡塞。教練不會把每一句廢話都要你記住。

所以導入 mem0 的同時，一定要配一道**寫入閘門**：這個反饋夠有料、可信、不重複嗎？過了再存。這一步才是把 memory 從「更大的 log」變成「真正的 EFC 放大器」的關鍵。

## 三個實戰建議

**一、別再用 raw compute 當「能力提升」指標。** context 更長、工具更多、log 更詳細，是「我做了很多」的證據，不是「Agent 變強了」的證據。

**二、每加一個工具或一輪 retry，先過 EFC 四條。** 最關鍵是第四條——它會不會真的改變下一步決策？如果不會，加了就是純粹燒錢。

**三、把反饋塞進 plan / revise / verify 的 close loop。** 飄過去的 log 不算數，被整理、被記住、被複用，它才會變成 EFC。

## 坦白說，這篇論文也有保留空間

我不想把它講得像萬靈丹。解釋力最高的是 **Oracle-EFC**，那個「Oracle」用了事後才知道的理想資訊去判定哪些反饋有效——真實系統做不到，所以 0.94–0.99 是理論上限，不是你明天就拿得到的數字。而「retained」這條最難工程化：判斷一個反饋有沒有真的改變決策，本身就需要一套機制，論文給的是衡量框架，不是現成的實作。

但即使打了這些折扣，核心洞察我還是非常買單。

## Agent 就跟人一樣

人類花了幾十年才確認：練得多不等於變強，**練對、有反饋、會檢討**才會變強。這就是 deliberate practice。這篇論文等於告訴我們，Agent 也吃這一套。

我們太容易掉進「我加了好多工具、開了好多 log」的滿足感裡，誤把「忙碌」當成「能力」。但 raw compute 衡量的是 Agent 有多忙，EFC 衡量的是它有多聰明。

未來 Agent Harness 的競爭，不會是誰掛的工具多、context 長，而是**誰能讓每一次反饋都真的被用上。**

好的 Harness，不是讓 Agent 多幹活，而是像個好教練——讓它每幹一步，都真的學到東西。

我們下週二見。

---

*論文出處：[Scaling Laws for Agent Harnesses via Effective Feedback Compute](https://arxiv.org/abs/2605.29682)（Xuanliang Zhang, Dingzirui Wang, Keyan Xu, Qingfu Zhu, Wanxiang Che）*
