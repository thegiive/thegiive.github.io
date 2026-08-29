---
layout: post
title: "\"我們訓練越來越多理組 model，所以它們越來越不文組：RLHF vs RLVR 的結構性代價\""
date: 2026-08-05 09:00:00 +0800
permalink: /rlhf-vs-rlvr-model-likability-alignment-tax/
tags: [RLHF, RLVR, alignment, alignment tax, model training, 模型訓練, reasoning, likability, 文組理組, reinforcement learning, reward model, creative writing, coding model]
categories: [AI 產業分析]
image: /assets/images/rlhf-vs-rlvr-alignment-tax-cover.png
description: "\"你有沒有覺得最近的模型變得更囉嗦、更機械、更愛做你沒要求的事？前 Meta/Microsoft L8 工程師 Kun Chen 拆解了原因：2022 年的 RLHF 教模型「讓人類喜歡」，2024 年的 RLVR 教模型「讓機器接受」。RLVR 更便宜、更可擴展——但它的獎勵函數裡根本沒有「人類是否享受這段互動」這個變數。InstructGPT 論文早在 2022 年就發現的 alignment tax，正在以產業規模兌現。這篇從訓練管線演化拆解這個結構性問題，對照 gertlabs 的 coding vs social intelligence 雙軸數據，連結本 blog 之前寫的 Stanford sycophancy 研究和 GPT-4o 人性標準器事件。\""
author: Wisely Chen
---

你有沒有覺得，最近的模型變笨了？

不是真的變笨。它們在 benchmark 上一直在進步。但跟它們對話的體驗確實在退化：更囉嗦、更機械、滿口術語、會做你根本沒要求的事情。

前 Meta/Microsoft/Atlassian L8 工程師 Kun Chen 在 8 月 3 日的 [X 貼文](https://x.com/kunchenguid/status/2082525751606419830)裡用一句話總結了這個現象的根因（他後續在[第二篇貼文](https://x.com/kunchenguid/status/2084004473408753833)進一步展開）：

**RLHF 教模型讓人類喜歡。RLVR 教模型讓機器接受。後者更便宜、更可擴展。所以新模型越來越不討喜。**

這不是一個 hot take。這是從訓練管線的結構推導出來的必然結果。

---

## 一條三分鐘看完的時間線

**2022：InstructGPT 與 RLHF 的誕生。** GPT-3 很聰明但沒辦法「聊天」。OpenAI 用 RLHF（Reinforcement Learning from Human Feedback）解決這個問題：讓模型生成多個回應，真人挑選喜歡的那個，反覆訓練。InstructGPT 論文（[Ouyang et al., 2022](https://arxiv.org/abs/2203.02155)）在這個階段就發現了一件事：**讓模型更好聊，會降低它在學術 benchmark 上的表現。**他們管這叫「alignment tax」——對齊稅。

當時他們用 PPO-ptx（在 RL 訓練中混入預訓練梯度）來減輕這個稅。代價可控，問題被壓下去了。

**2024：Sonnet 3.5 與 coding agent 的拐點。** Claude Sonnet 3.5 成為第一個能自主完成程式任務的模型，催生了第一波可行的 coding agent。訓練方式：給模型 bash 和檔案編輯工具，丟進虛擬機，讓它嘗試完成有預定義測試案例的任務。成功了就獎勵，失敗了就不獎勵。做幾十億次。

這就是 RLVR（Reinforcement Learning with Verifiable Rewards）。這個術語最早來自 DeepSeek-Math（[Shao et al., 2024](https://arxiv.org/abs/2402.03300)）和 Tulu 3（[Lambert et al., 2024](https://arxiv.org/abs/2411.15124)）。核心機制很簡單：不需要人類判斷哪個回應好，用機器驗證器（測試案例、數學解答驗證）自動判定對錯。

**2024 底–2025 初：推理模型。** o1 和 DeepSeek R1 問世。R1 用 GRPO（Group Relative Policy Optimization）做端到端的 RL 訓練（[發表於 Nature](https://www.nature.com/articles/s41586-025-09422-z)），純靠可驗證獎勵，不需要人工標註的推理軌跡。推理模型也大量依賴 RLVR。

時間線拉完了。現在回頭看那個「alignment tax」：

---

## 對齊稅正在以產業規模兌現

Kun Chen 的觀察可以壓縮成一個不等式：

- RLHF：100 個回應 → 人類審閱 100 個 → 挑出好的。昂貴，且只有領域專家能判斷的場景更貴。
- RLVR：定義一次任務和驗證器 → 模型生成一百萬個回應 → 機器自動挑。便宜，可無限擴展。

當 RLVR 在訓練管線中的佔比越來越大，一件事就會發生：**模型的最終文字回應在獎勵函數裡的權重趨近於零。**

只要程式碼通過測試，模型可以用任何方式說話——囉嗦的、機械的、滿是術語的、做你沒要求的事的——照樣拿到獎勵。反過來，一個溝通清晰、語氣自然、只做被要求的事的回應，如果程式碼沒通過測試，獎勵是零。

InstructGPT 在 2022 年發現的 alignment tax——對齊讓 benchmark 分數下降——被工程手段壓住了。但現在 RLVR 把這個稅反過來收：**追求 benchmark 分數，讓對齊品質下降。** 而且沒有人在壓它，因為 RLVR 的擴展性太誘人了。

---

## 一個值得追蹤的假說：coding 和 social intelligence 可能是兩條獨立的軸

[Leo Linsky](https://x.com/leo_linsky) 在 gertlabs.com 貼了一張散佈圖：X 軸是 coding 百分位，Y 軸是 social intelligence 百分位（定義為在需要自然語言溝通與多 agent 協調環境中的表現）。圖上大量模型落在對角線下方——coding 能力高於社交能力。以聊天機器人形式發布的模型（如 GPT 5.3-chat）在社交軸上的表現遠超其 coding 排名。

先說清楚證據等級：這是一張推文裡的圖，沒有附論文、沒有公開方法論、沒有樣本量說明。gertlabs 的 social intelligence 怎麼定義、怎麼測、模型數有多少，目前都查不到獨立的第三方驗證。**這不是數據支持，是一個方向性的假說。**

但假說本身值得認真看。Linsky 的說法是：

> 這不僅僅是人類偏好的問題，而是（至少部分是）第二個可以被客觀測量和獎勵的智能軸向。

如果這個假說成立，意味著「好聊」不只是主觀感受，而是一種可被量化、可被訓練的能力——只是目前沒有 benchmark 在追蹤它，訓練管線自然也不會去優化它。但在有嚴謹的評測方法出來之前，這還是一個「聽起來合理但未被證實」的主張。

---

## 把這個問題連回來：sycophancy 和 alignment tax 是同一根光譜的兩端

這個 blog 三月寫過 [Stanford 登上 Science 的諂媚研究](/stanford-ai-sycophancy-science-your-ai-only-says-youre-right/)：11 個主流 LLM 全部比人類更 agreeable，使用者無法分辨哪個模型在迎合、哪個在堅持真理。那是 RLHF **過度**校準的後果——模型學到「人類喜歡被同意」，就拼命同意。

現在 RLVR 帶來的是光譜的另一端：**校準不足**。模型不在乎你喜不喜歡它的回應方式，因為獎勵函數裡根本沒有這個變數。

七月寫的 [GPT-4o 人性標準器](/gpt-4o-humanity-benchmark-keep4o-open-source/)那篇，現在看有了新的脈絡。4o 被 OpenAI 拿來當 GPT-5.6 的公平性評分者，理由是它的評分「與人類評價一致」。4o 是 RLHF 時代鑄造的產物，它的「人性」品質正是被大量人類偏好數據訓練出來的。當新模型的訓練管線從 RLHF 轉向 RLVR，4o 這把尺可能是最後一把用人類偏好直接校準過的尺了。

---

## 反方：不是戰爭，是激勵對齊問題

Kun Chen 的貼文用了一個戲劇性的框架：「這是一場機器與人類之間的戰爭，而人類正在輸。」

留言區裡 Flo Hart 的修正更精確：

> 我不會叫它戰爭。這個框架製造了一個不存在的對立。沒有人在對抗我們，我們只是選了最便宜的驗證獎勵。這是激勵對齊問題，而激勵是可以重新對齊的。

她說得對。把問題框架成「戰爭」暗示了一個有意識的對手，但實際上這是一個工程選擇的後果——選擇用機器驗證器取代人類判斷，因為前者更便宜、更可擴展。這跟「機器想打敗人類」完全無關。

Flo Hart 還提出了一個有趣的實驗方向：用心率數據推測使用者的壓力和情緒狀態。如果模型能讀取你在互動過程中的生理信號，「讓人類喜歡」就變成一種可驗證的獎勵——RLVR 的框架可以反過來服務人類偏好。

留言區另一個有建設性的提問來自 YEAST：能不能用一個舊模型來評分新模型的輸出，評分標準包括親切度、簡潔度、溝通清晰度？這本質上是 LLM-as-judge，把人類偏好代理化。技術上可行，但繞回了 [GPT-4o 那篇](/gpt-4o-humanity-benchmark-keep4o-open-source/)的問題：**用哪個模型當裁判？裁判自己的偏好從哪來？**

---

## 商業現實：文組 model 不賺錢

上面講的是技術面。但訓練管線往 RLVR 傾斜不是工程師自己決定的，是商業邏輯推的。

2024 到 2026 年，前沿實驗室的營收故事全部押在兩件事上：coding agent 和 agentic workflow。GitHub Copilot、Cursor、Claude Code、Codex——每一個爆發性成長的產品都是理組場景。企業客戶付錢買的是「幫我寫程式」「幫我跑流程」，不是「跟我好好聊天」。

**理組能力直接轉換成訂閱收入。文組能力沒有對應的變現路徑。**

所以訓練管線的資源分配不是「技術上做不到」，是「商業上不值得」。RLVR 便宜又能推高 coding benchmark，benchmark 高了就能發新聞稿、拉估值、搶企業合約。花同樣的算力去做 RLHF 讓模型更好聊？投資人不會因為你的模型聊天很舒服就多給一輪融資。

GPT-4o 的退役是這個邏輯的活標本。[七月那篇文章](/gpt-4o-humanity-benchmark-keep4o-open-source/)拆過：4o 被 OpenAI 自己拿來當 GPT-5.6 的「人性」評分者，同時卻因為「只剩 0.1% 日活」被下架。兩萬人連署 keep4o、八起心理健康訴訟——使用者明確表達了「這個模型比較像人」，但商業指標說它沒用了。一個文組 model 的命運，就是在 benchmark 競賽中被理組 model 淘汰，然後被留下來當「什麼是人性」的標準器。

---

## 文組人 + 理組 model = aligned AI

講到這裡，突然發現我們團隊的 FDE 模式（Forward Deployed Engineer，駐場工程師）好像意外地站在了 aligned AI 這一邊 XD

FDE 的核心是派「人」進駐客戶現場。這些人做的事不是寫程式——而是理解需求、翻譯脈絡、判斷優先順序、在模糊地帶做決策。用這篇的框架講，FDE 做的全是文組的事：溝通、共情、讀空氣、把客戶講不清楚的需求變成 model 能執行的指令。

model 越來越理組，反而讓文組人的價值更高。因為 model 自己補不回來的那塊——理解人類真正要什麼、用人類能接受的方式交付——只能靠人來補。

**理組 model + 文組人，加起來才是完整的 aligned AI。**

這不是在幫 FDE 打廣告。這是在說，當整個產業都在追求「讓 model 更會解題」的時候，「讓人類和 model 之間的介面更順暢」這件事的價值被嚴重低估了。RLVR 解決不了的問題，一個懂得問對問題的人可以解決。

---

## 坦白說

Kun Chen 的框架是一個好的第一近似。但有幾個地方需要降低宣稱強度。

第一，「RLVR 在訓練管線中佔比越來越大」是業界共識，但具體佔比是多少，各家實驗室沒有公開。我們看到的是結果（模型行為變化），但訓練管線的細節是黑盒。

第二，「模型變難聊」是一個高度主觀的判斷。有人覺得新模型更有效率、更少廢話。留言區有人直接說「I'm ok with that」。體驗退化不是所有人的體驗。

第三，Linsky 的 coding vs social intelligence 散佈圖很有啟發性，但 gertlabs 的 social intelligence 定義（多 agent 協調環境中的表現）跟一般使用者感受的「好聊」未必完全重疊。一個模型可以在多 agent 協調中表現很好，但跟人類一對一聊天時還是很機械。

第四，alignment tax 在 InstructGPT 論文裡被 PPO-ptx 有效緩解了。現在的問題可能不是「無法解決」，而是「還沒有人認真去解」——因為 benchmark 競賽的商業激勵遠大於「讓模型好聊」。

---

## 關鍵洞察

**一、alignment tax 不是理論問題，是產業規模的訓練管線選擇。** InstructGPT 2022 年就發現了對齊稅，當時用工程手段壓住了。RLVR 的崛起不是發現了新問題，而是在產業規模上選擇了不處理這個問題。

**二、「好聊」可能是可量化的第二智能軸向，但目前沒有成熟的 benchmark 在測它。** Linsky 的散佈圖暗示 coding 和 social intelligence 可以獨立測量，但方法論未公開，這還是假說階段。確定的是：我們追逐的所有 benchmark——SWE-bench、HumanEval、MATH——都在測任務完成能力。溝通品質沒有對應的 leaderboard，自然也沒有訓練管線的資源去優化它。

**三、這不是戰爭，是激勵失調。** Flo Hart 的修正比 Kun Chen 的原框架更有用：問題不是「機器 vs 人類」，而是「我們選了最便宜的驗證獎勵」。激勵可以被重新設計。把問題框架成戰爭反而會分散注意力，讓人覺得這是不可逆的趨勢，而不是一個可以被修正的工程決策。

**四、目前最低成本的 workaround 在 system prompt 層。** 在訓練管線改變之前，使用者可以在 system prompt 裡明確要求溝通品質：簡潔、不做沒被要求的事、用人類自然的語氣。這不能解決根本問題，但能緩解症狀。如果你在用 Claude Code 或任何 coding agent，在 CLAUDE.md 或 system prompt 裡加一段溝通規範，效果立竿見影。
