---
layout: post
title: "系統是約束、Prompt 是引導——AI 協作的護欄怎麼裝？｜Weekly AI Vlog EP14"
date: 2026-03-22 10:00:00 +0800
permalink: /vlog-weekly-summary-ep14-harness-engineering-sidechat/
image: /assets/images/vlog-ep14-harness-sidechat-cover.png
description: "Prompt 像方向盤上貼的紙條，系統才是路上的護欄。這週從 Harness Engineering 核心原則、mRNA 疫苗短板填補、Opus vs Sonnet 體感差距、Side Chat 訪談，到 Meta Sev 1 資安事故——AI 已經不是能不能用的問題，而是人跟 AI 怎麼互相交互。"
---

**涵蓋文章（2026-03-16 ~ 03-22）：**

1. 03/16 - 一個工程師用 AI 幫狗設計了 mRNA 癌症疫苗——AI 時代投資報酬率最高的事：填補短板
2. 03/17 - 殘差連接被動刀了：DeepSeek 和 Kimi 先後改掉 Transformer 用了十年的「默認設定」
3. 03/19 - Prompt 負責引導，工程負責約束：做 Agent 半年的核心體會
4. 03/20 - Opus vs Sonnet：Benchmark 看不太出來的體感差距
5. 03/19 - INSIDE Side Chat E397：用 AI 在物流業打造零工程師團隊
6. 03/21 - Meta AI Agent Sev 1 事故：Harness Engineering 不是理論，是血淋淋的教訓

---

{% include youtube.html id="Iy2mjx2NlYg" %}

---

## 逐字稿

### 開場：如何跟 AI 做好協作

嗨大家好，這週的話主要議題就是——如何跟 AI 做一個很好的協作，並且如何在 AI 這邊設一個護欄框架，確保說 AI 就算出現幻覺的時候，我們不會被他帶著走。

這週其實提到很多相關的議題，都在講類似的東西。這些議題基本上就是我們現在最紅的 Harness Engineering。

---

### 系統是約束，Prompt 是引導

今天來講「系統是約束，提示詞是引導」這個概念。

我們在做 AI Agent 做那麼久了，都有一個感覺——不管你再怎麼會寫提示詞、寫得多好，到最後你可能有 10 個、20 個相關的提示詞去規範他、約束他。可到最後我們就發現：**完全依賴提示詞來做規範跟約束，是非常非常困難的。**

原因有幾個。

**第一，模型能力的限制。** 像 Gemini、Sonnet 這樣的模型，如果你給他 5 個禁止提示詞，基本上他還是可以做到。但如果你給他 50 個以上，就很容易出現——後面的 5 個你有辦法遵循，前面的 5 個他就忘記了，或在邏輯上他拐不過來了。

這邊要特別提，正向提示詞跟負向提示詞在模型這邊的能力是有差別的。

而且我們做 AI Agent 的時候為了省錢，不能完全用最好的頂塔模型。用性價比較高的模型時，禁止提示詞就只能有一定數量，不能太多。

**第二，今天測好明天又壞。** 就算你把測試測好了，可能今天測好，明天突然發現他又不對了。這是幻覺嗎？有時候是，有時候根本原因是降智——不管是 ChatGPT、Gemini 或 Anthropic，算力不太夠的時候就會對某些模型進行降智。

所以我們能做的最好情況就是：**盡量讓提示詞是一個引導，告訴他我們要什麼東西。** 當然你還是能放一些禁止的提示詞，但真正能夠規範他的，其實是用系統。

系統就是在 AI Agent 之外的 IT 系統——可能是程式碼、可能是 n8n、可能是 CI。用確定性的程式碼框架去框住他。當模型超出了原本設定的行為，直接報錯，阻止他做這件事。

這個方式非常有效。原因是：

1. **禁止的行為通常影響很大。** 與其依賴 LLM 自覺，不如在外面直接放一個框架來截住他、檢查他、擋住他。而且你比較心安。
2. **系統框架比 Prompt 更難繞開。** 就算大語言模型再厲害，有系統權限框住他，基本上都比較難繞開。

有一個很好的比喻：**Prompt 有點像在方向盤上面貼一個說「你要怎麼開」，但真正決定車子不要開出車道範圍之外的，是路上的護欄。** 有了護欄之後，你就確保這台車雖然坑坑洼洼撞撞的，但他不會開出大範圍之外。

這就是 Harness Engineering——框架工程。我們必須在 AI Agent 之外放一個框架，用提示詞去引導他要怎麼做，但當他超出範圍，我們就把他框住。

我再重複一次：**提示詞是引導，系統是約束。兩個都非常重要。**

> 📖 延伸閱讀：[Prompt 負責引導，工程負責約束：做 Agent 半年的核心體會](/prompt-guides-engineering-constrains-agent-principle/)

---

### mRNA 疫苗——AI 填補短板的投資報酬率最高

這週也講到一個我覺得很棒的故事。有一個創業者用 AI 做出 mRNA 疫苗——他什麼醫療背景都沒有，就是 IT 背景的人，但他用 IT 技術加上 AI，一步一步引導，為他的狗狗做出一個 mRNA 疫苗，而且最後是可以合作的。

這個故事代表的就是：**在 AI 時代，投資報酬率最高的不是用 AI 去增強你所擅長的部分，反而是用 AI 去彌補你的短板。** 這時候你的投資報酬率會非常非常高，因為你是從 0 到 1，從不會到會。

放到我們的生活當中——像我可能不太會寫文章，但現在用 AI 幫助我寫文章寫得很好。我可能不會做 SEO，但有了 ChatGPT、Gemini，他能幫我做 SEO，告訴我很多 SEO 的詞彙。而且我現在看到自己 Blog 的 SEO 成效也不錯。

所以 AI 最大的重點是：**利用 AI 去增強你所不知道的部分，而不是去強化你所知道的部分。** 因為你所知道的部分，可能是從 90 分變到 95 分，投資報酬率是低的。而且 AI 的幻覺還是會有，你會覺得他沒什麼用。但如果讓他做你原本做不到的部分，你就會覺得 AI 真是一個超級棒的老師。

> 📖 延伸閱讀：[一個工程師用 AI 幫狗設計了 mRNA 癌症疫苗——AI 時代投資報酬率最高的事：填補短板](/ai-shortboard-filling-paul-dog-cancer-vaccine/)

---

### Opus vs Sonnet——差就差在那 5%

這週也講到我這一個多月來使用 Opus 跟 Sonnet 的感覺。

我在做 AI Coding 以及用 OpenClaw 的時候，發現 Sonnet 基本上大部分都可以用。但很多時候 Opus 就是比 Sonnet 好一點點。

我舉兩個例子。

第一個，我請 OpenClaw 寄信給 Amy，但 Amy 不在原本的記憶裡面。Sonnet 的做法是直接問我：「你說要寄給 Amy，那 Amy 的 Email 是什麼？」這完全正確，一點都沒錯。

但 Opus 多做一件事——**在問我 Amy 是誰之前，他先去我的 Gmail 裡面搜尋有沒有 Amy 的 Email 往來記錄。** 他發現裡面只有一個 Amy，所以他就說：「我認為你要寄給的是這個 Amy，我就寄給他。」

這件事讓我覺得：有些時候好模型跟不好模型、頂塔跟不是頂塔，**差就差在那 5%。** 就像在職場上永遠多做一點點、比別人多做那 5% 的員工，會覺得他的能力是無與倫比的。

從性價比來說，Opus 可能比 Sonnet 貴 3 倍，所以大部分時候 Sonnet 就夠用了。但像 OpenClaw 這種很臨時、很 random、很模糊的場景，Opus 多做到的那 5% 就是比你多做 5%——能幫我省下一些腦力，少一次的交互跟輪回。

這些模型其實大家都有水準，70% 到 80% 都很能用。但在最 random、最難掌握的場景下，我還是會用頂塔，就算他貴很多。

> 📖 延伸閱讀：[Opus vs Sonnet：Benchmark 看不太出來的體感差距](/opus-vs-sonnet-real-gap-practical-guide/)

---

### Side Chat 訪談

這週我也很有幸獲得 INSIDE 塞掐的訪談，講了一下我之前的思維轉型經驗，以及我現在怎麼看 AI 這個浪潮、怎麼用 OpenClaw、還有一些 AI 資安的議題。

我個人覺得這是一個非常非常好的經驗，也非常謝謝 Fox 能給我這個機會。

> 📖 延伸閱讀：[INSIDE Side Chat E397：用 AI 在物流業打造零工程師團隊](/inside-sidechat-e397-ai-logistics-zero-engineer-team/)

---

### Meta Sev 1——AI 已經不是能不能用的問題

最後講到 Meta 這邊因為一個錯誤的流程，導致 Sev 1 資安事件。

這裡面有兩個問題：

**第一，AI Agent 權限問題。** Agent 沒有獲得正確的 Approval，就能在內部論壇分析數據並且 Post，影響到內部同事。

**第二，人對 AI 的盲信。** 內部同事在沒有任何測試的情況下，就直接執行了 AI 的建議，造成內部資料外洩。

這反映到兩個根本問題：一是 AI Agent 的權限管理，二是現在社會中大家對 AI 的信任度越來越高，甚至會完全不做查核就直接信賴 AI。

**這其實是未來公司的一個寫照。** 我們未來會有大量流程被重新改寫，變成人機交互的過程。在這個過程中，怎麼確保我們還是能達到一樣的 Quality？不會造成誤會、不會造成外洩，或是被 AI 幻覺影響，為了追求效率而做錯？

AI 已經不是「他能不能用」了，我們都知道他能用。但接下來 AI 導入在人機協作上面、流程上面，會有很多很多的問題。

**不是完全信 AI，也不是完全不信 AI。而是當 AI 跟人都有一定的可信度情況下，這兩個物種要怎麼互相交互。** 這個我認為是很重要的議題，也是接下來所有 AI 落地的最大挑戰。

Harness Engineering 能夠做這件事情——確保人跟機器能夠交手、換手，整個流程下來大家都在正確的軌道上。

> 📖 延伸閱讀：[Meta AI Agent Sev 1 事故：Harness Engineering 不是理論，是血淋淋的教訓](/meta-ai-agent-sev1-rogue-agent-enterprise-wake-up-call/)

---

## 文章連結

- [一個工程師用 AI 幫狗設計了 mRNA 癌症疫苗——AI 時代投資報酬率最高的事：填補短板](/ai-shortboard-filling-paul-dog-cancer-vaccine/)
- [殘差連接被動刀了：DeepSeek 和 Kimi 先後改掉 Transformer 用了十年的「默認設定」](/residual-connection-deepseek-mhc-kimi-attention-residuals-breakthrough/)
- [Prompt 負責引導，工程負責約束：做 Agent 半年的核心體會](/prompt-guides-engineering-constrains-agent-principle/)
- [Opus vs Sonnet：Benchmark 看不太出來的體感差距](/opus-vs-sonnet-real-gap-practical-guide/)
- [INSIDE Side Chat E397：用 AI 在物流業打造零工程師團隊](/inside-sidechat-e397-ai-logistics-zero-engineer-team/)
- [Meta AI Agent Sev 1 事故：Harness Engineering 不是理論，是血淋淋的教訓](/meta-ai-agent-sev1-rogue-agent-enterprise-wake-up-call/)
