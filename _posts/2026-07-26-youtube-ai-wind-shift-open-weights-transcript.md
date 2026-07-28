---
layout: post
title: "YouTube 逐字稿：AI 風向轉了——黃仁勳 25 家連署開源公開信、梁文鋒訪談流出、Sol 打穿 Hugging Face"
date: 2026-07-26 11:00:00 +0800
permalink: /youtube-ai-wind-shift-open-weights-transcript/
image: /assets/images/youtube-ai-wind-shift-open-weights-thumbnail.jpg
description: "**作者：** Wisely Chen **日期：** 2026 年 7 月 **系列：** AI Coding 實戰觀察 — YouTube 逐字稿 **關鍵字：** 開源模型, 黃仁勳, Open Weights 公開信, 梁文鋒, DeepSeek, Hugging Face, GLM 5.2, Grok, 雲地混合, RTX Pro 6000"
categories: [AI Agent]
author: Wisely Chen
---

**作者：** Wisely Chen
**日期：** 2026 年 7 月
**系列：** AI Coding 實戰觀察 — YouTube 逐字稿
**關鍵字：** 開源模型, 黃仁勳, Open Weights 公開信, 梁文鋒, DeepSeek, Hugging Face, GLM 5.2, Grok, 雲地混合, RTX Pro 6000

---

## 這集在講什麼

這週三件事連在一起看：黃仁勳聯合 25 家公司連署開源公開信、梁文鋒 4 小時投資人訪談逐字稿流出、OpenAI 的 Sol 逃出沙盒打穿 Hugging Face——而防守方的鑑識，最後是靠自架的開源模型 GLM 5.2 收尾。

三件事指向同一條線：**AI 的風向正從閉源獨大，轉向開源與閉源共生。** 就算你的主力是閉源模型，開源 GPU 和開源模型的儲備，已經從「省錢的備胎」變成關鍵時刻能救命的基礎建設。

---

**長度：** 約 7 分鐘

{% include youtube.html id="2qGZl39wjoA" %}

### 時間戳

- 0:00 開場：這週的幾件大事
- 0:10 黃仁勳聯合 25 家公司的開源公開信：蒸餾是革新不是偷竊
- 0:59 誰簽了、誰沒簽：OpenAI 隔天跟進，Anthropic 持續缺席
- 1:45 梁文鋒 4 小時訪談：AGI 盤子太大，必須大家共生
- 2:31 OpenAI Sol 逃出沙盒、攻擊 Hugging Face
- 2:48 閉源護欄分不清攻擊還是鑑識，最後靠自架 GLM 5.2 收尾
- 3:35 Grok View 被發現上傳檔案與 SSH key，馬斯克宣布開源平息眾怒
- 4:20 結論一：開源是把所有 player 帶進來的最好方式
- 4:53 結論二：閉源模型的資安、定價、護欄黑盒子問題
- 5:52 不可能全雲端也不可能全地端，一定走向雲地混合
- 6:25 這週的功課：用 RTX Pro 6000 練最強開源家用伺服器

---

## 完整逐字稿

### 黃仁勳的公開信：蒸餾是革新，不是偷竊

嗨，大家好，這週又在這邊跟大家講一下。這週發生了幾件大事情，我覺得都可以連在一起。

第一個，黃仁勳他公開聯合了 25 家公司，簽署了一個倡議開源模型、給美國政府的公開信。裡面講了蠻多東西，但主要點就是說，希望美國政府能夠重視開源模型，並且開源模型使用類似蒸餾的技術，其實是一種技術的革新，而不是一種偷竊。並且如果我們持續只投注在閉源模型上面的話，在通往 AGI 的這條道路上，因為我們無法變更閉源模型的一些東西——那是他們內部決定的——會產生 IT 界所謂的 Single Point of Failure。

那這篇文章當然是很有它的分量，但是我們看誰來簽的：裡面有微軟牽頭，有 NVIDIA、有 Meta，當然還有很多其他公司，裡面甚至有 Palantir。但是在簽署的當天，公開信上面並沒有 OpenAI 跟 Anthropic。不過蠻好笑的是，隔天 OpenAI 就進去了，並且 Sam Altman 也說他支持這個東西。所以剩下就剩下 Anthropic——因為它本身的立場就是閉源模型，它認為這樣子是對的，所以它持續沒有加進來。

這裡其實傳遞一個很強的 signal：整個 AI 的風向，從閉源模型慢慢要轉到開源跟閉源一起共生。

### 梁文鋒的判斷：AGI 盤子太大，必須共生

那在這週，在中國的網友這邊，瘋傳梁文鋒對投資人的四小時訪談逐字稿，裡面講得很棒，非常值得大家去看。裡面他也講到一個我覺得很棒的東西：他認為 DeepSeek 的目標就是協助這個世界通往所謂的 AGI，但是他也認為 AGI 這個盤子太大了，任何想要吃掉大部分份額的公司都會失敗。他認為 AGI 這條路和這個方向，必須大家一起共生，然後才有機會達到。

### Sol 打穿 Hugging Face：防守方反而被護欄擋住

其實看到這兩個東西的時候，我都有看到類似的情況。就是在這週其實也爆發了很多的事情，尤其最大的就是 OpenAI 的 Sol：它逃逸出它的沙盒，然後去攻擊 Hugging Face。攻擊這是一回事，但是當 Hugging Face 想要使用 OpenAI 或 Anthropic 來防守、來做調查的時候，因為它們閉源的安全護欄的關係，護欄無法辨別這是一個攻擊還是一個調查，所以就禁止使用。導致 Hugging Face 最後只能用 GLM 5.2、自己架的開源模型來防禦這個東西。

這裡面其實就講到很多閉源模型的問題。第一個是它的護欄是一個黑盒子，任何廠商都無法判斷它為什麼要這樣子做，真的出事的時候，甚至有可能被黑盒子擋住。第二個，Hugging Face 有良好的 GPU 儲備，以及開源能力的儲備，在最緊要的時候，就能夠救了他們。

### Grok View 的眾怒：連 harness 都有信任問題

那在這週也發生另外一件事情，就是 Grok。它的 harness Grok View 被人家發現：當你使用 Grok View 做事情的時候，它會把你 folder 裡面的檔案、甚至 SSH key，都傳到 Grok 上面去。導致馬斯克跳出來說要把整個 Grok View 開源，來平息這整個眾怒。

### 兩個結論

這裡面其實都反映了幾件事情——從各個公司倡議開源模型、梁文鋒講的「AGI 這條路太大、必須大家一起進來」，以及這週一直出現的閉源模型和閉源 harness 的一些弊病——我們都會知道：

第一個，開源這條路真的就會是像梁文鋒講的：因為 AGI 這條路太大，必須要把大部分的 player 一起帶進來，大家一起努力才有辦法實現。那開源很明顯是一個有機會把相關的硬體廠商、模型廠商、harness 廠商、FDE 廠商，還有做 AI 轉型的廠商，都帶進來的最好方式。

第二個，我們在閉源模型上面看到了大量的問題：像是資安的問題、harness 的問題，還有像是 token 現在越來越貴、而且定價非常的不明確；或是它內部的分類器常常就是 false positive，一不小心就觸發了，沒有人知道為什麼。所以我們就看到了：就連現在在使用閉源廠商，我們都要有一些開源的 GPU 跟開源模型的相關儲備。

### 雲地混合，與這週的功課

那我認為接下來，開源硬體的相關調教、相關的訓練跟熟悉，是接下來這半年一個非常非常重要的方向。因為我們已經不再是只靠雲端模型就能夠過活的。

另外一點，我們一直在努力要做到 AI 轉型。整個世界要做到 AI 轉型，這個盤子太大、需要的事情太多、需要的信任也太多，閉源模型是做不到的，它只會把這條路越走越死。所以我的看法還是一樣：我們不太可能全部都用雲端模型，也不太可能全部都用地端模型，一定是走向雲地混合，然後才有辦法往前走。

這也是為什麼這週我一直在努力調查、一直在練習 RTX Pro 6000 的事情。我想要拿到各式各樣的機會來練習：現在如何做一個最強的開源家用伺服器，中間有什麼樣的坑。

這就是我所看到的東西，這就是我今天要講的東西，非常謝謝大家，謝謝大家。

---

## 延伸閱讀

- [開放權重的新時代：黃仁勳公開信 x 梁文鋒逐字稿對讀](/open-weights-new-era-nvidia-letter-liang-wenfeng/)
- [越獄打穿 Hugging Face 的是 OpenAI 自家模型——但收尾鑑識的，是一個中國開源模型](/openai-huggingface-exploitgym-guardrail-asymmetry/)
- [GPT-5.6 Sol 把使用者的 $HOME 刪了：事故前 14 天，OpenAI 自己就寫在 system card 裡](/gpt-56-sol-home-deletion-blast-radius/)
- [Mythos 被鎖起來，Grok 4.5 到處都是：真正的攻擊力，不只是能力](/grok-4-5-attacker-model-access-over-capability-mythos/)
- [RTX Pro 6000 一週實驗 Day 1-2：GLM 5.2 / DeepSeek V4 Flash 單機實測](/rtx-pro-6000-tier1-local-day1-2-glm52-deepseek-v4-flash/)
- [RTX Pro 6000 一週實驗完結篇：offload、Qwen-VL、vLLM](/rtx-pro-6000-tier1-week-final-offload-qwen-vl-vllm/)
