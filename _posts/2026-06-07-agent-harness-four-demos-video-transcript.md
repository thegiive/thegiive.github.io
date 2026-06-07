---
layout: post
title: "影片逐字稿｜Harness = Agent − Model：四個 hook demo 把規則變成機制"
date: 2026-06-07 09:00:00 +0800
permalink: /agent-harness-four-demos-video-transcript/
image: /assets/images/agent-harness-four-demos-cover.jpg
description: "這是我在 DigiTimes 場子那段 Harness Engineering 短講的逐字稿。一句話定義：Harness = Agent − Model。用四個可以直接跑的 Claude Code hook demo——審批、工具收斂、最小權限、稽核重播——示範怎麼把『規則』變成 agent 繞不過去的『機制』。"
---

![Harness = Agent − Model：四個 hook demo](/assets/images/agent-harness-four-demos-cover.jpg)

<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;margin:30px 0;border-radius:8px;">
  <iframe src="https://www.youtube.com/embed/2VAcNyc6bAc" style="position:absolute;top:0;left:0;width:100%;height:100%;" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

> 影片連結：[https://youtu.be/2VAcNyc6bAc](https://youtu.be/2VAcNyc6bAc)
> 這篇是影片的逐字稿，文字有稍微整理過。想看把四個 demo 講到能跑的完整版，請看：[Harness Engineering 的四個 Demo：Prompt 是建議，機制才是規則](/agent-harness-three-migrations-mechanism/)。四個 demo 的程式碼在 [thegiive/harness_engineering](https://github.com/thegiive/harness_engineering)。

---

## 開場

大家好，我今天在 DigiTimes 的場子，講如何用我們公司的產品 Bromnie 加強在 AI 時代相關的資安。不過今天這支影片不是來介紹我、也不是來介紹我們公司產品的，其實我要講的是最近常寫的一個東西——在 Harness Engineering 裡面的一些相關規範。

老實說，我在做 Harness Engineering 的研究的時候，一直有一個很神奇的感覺：Harness Engineering 本身是一個很 rough、而且沒有被很好定義的詞，基本上所有的東西都可以講它是 Harness Engineering。

## 先給一個最好記的定義

所以我後來發現，Harness Engineering 大概可以這樣理解：如果 Agent 是一個有手有腳、有動作工具的東西，那麼 Agent 減掉相關的 Model，剩下外面所有的工程設計，就都叫 Harness。

怎麼樣，有沒有覺得這個定義非常空泛？對，它就是那麼空泛。但我這週其實有寫一個相關的實作，大概寫了四個 demo，這次 demo 我覺得蠻適合用來介紹 Harness Engineering 大概代表什麼意思。

## Demo 1｜工具要分等級，高風險動作 hook 強制審批

第一件事情是：當我們在做 Agent、在做實作的時候，可能會去調用一些工具。這個時候我們必須要對某些工具給予相關的定義跟權限。如果我們設定這些工具的權限跟定義是比較高等級、需要人來 review 的，那 Agent 在執行相關機制時——像我的 demo 是用 Claude Code 或是 Codex 的 Hook——它就會直接在 Hook 層強迫去執行一個審核 review。

所以在這種情況下，就算你的 Model 被人家攻破了、被人家的 prompt injection 攻破、被洗腦了，這時候 Model 原本的系統提示詞已經沒有用了，但是在 Agent 的 framework 層，已經可以把這個東西攔截、擋下來。

## Demo 2｜別給 AI 一把萬能鑰匙，把寬工具拆成窄工具

可是我們在做這件事情的時候，就有很多議題要梳理跟定義。第一個，我們給出的有些是比較寬泛的工具，像 Google Cloud 有一個叫 gcloud 的工具，它能操縱大量的 Google 服務。這種工具能力太強、範圍太大，就不是我們在 Harness Engineering 裡最適合的工具。

我們應該做的事情是：使用它，但在上面加一層 wrapper，把它的每一個用途都定義成不同的 script，再把每個 script 定義為 L0、L1、L2、L3，不同等級、不同權限，需要不同等級的審批。

舉例：讀取 email 這部分可以設為 L1，它比較低風險，因為它沒做事情；但裡面如果是撰寫 draft email，我們可以設為 L2，因為它有寫入動作；而真正寄 email 的時候，我們把它設為 L3。L3 因為可以跟外面溝通、可能洩密，所以放在 L3 的動作，我們都會要求它必須經過人強制的 review 跟審批。

所以在這種情況下，如果我們把工具能做的事情拆小，做成一個比較窄、比較 narrow 的工具，這時候就可以利用 Hook 來做這件事情。

## Demo 3｜最硬的一層：System / Account 的最小權限

再來，第三個 demo 我展示的是：就算整個 Hook 遇到一些 bug、或是我們 implementation 也遇到問題，但只要我們用比較嚴謹的 scope 定義，在帳號、在 IAM 這邊設計好——就算它在 Hook 層、在 prompt 層都被攻破了，在帳號權限層，因為遵循了所謂 least privilege、最小權限的設定，它依舊不會被攻破。

## Demo 4｜稽核重播：每個動作都留下紀錄

第四個 demo 講的是：剛剛講到的都是所謂 pre-hook，在工具執行之前；最後是一個 post-hook，在每個工具被執行之後，我們都給它一些相關的 audit log。

這個 log 不能寫在工具層，必須寫在 Hook 層，讓它每做一個動作，就把相關的時間、做了什麼事情、它是 L0 到 L1 到 L2 這些等級，都定義進去、寫進去。這樣子我們可以增加 observability，也就是可視性，還有可稽核性。

## 收斂：什麼才算好的 Harness Engineering

有了這些東西，基本上就符合大部分我們在 Harness Engineering 裡面要的相關過程。但就如同我一開始講的，Harness Engineering 其實是一個很廣的範圍，所以我們可以把它理解為：只要它是在 Model 之外的框架，只要能幫助 Agent 執行得越來越好、越來越安全，我們都可以把它當成是一個很好的 Harness Engineering 的實戰。

所以我希望能用這四個相關的 demo，給大家更多比較具體的感覺。因為我看到網路上很多文章在講，但都講得蠻空泛的，我覺得舉實例說可能比較好一點。

## 最後，一句話帶走

最後再提到 Harness Engineering 最重要的一個概念：不要去信賴你的提示詞，而是去信賴你的整個流程跟 mechanism。

這基本上就是那個管理學的概念：不要去信賴人。我們把語言模型想像成人，我們不要去信賴底下的人「他的 behavior 會如同我們指示給他的東西」，我們要創造出一個 SOP、一個流程，能夠把這些問題抓下來、攔下來。這就是管理學，這也就是我們在 Agent 時代需要做的 Harness Engineering。

大概就這樣子，謝謝大家。

---

## 延伸閱讀

- [Harness Engineering 的四個 Demo：Prompt 是建議，機制才是規則](/agent-harness-three-migrations-mechanism/)——這支影片對應的完整文字版，把四個 demo 講到能跑
- [做 Agent 的一個體會：Prompt 負責引導，工程負責約束](/prompt-guides-engineering-constrains-agent-principle/)
- [AI Coding 資安的真正防線：為什麼 Harness Engineering 比模型聰明更重要](/prompt-injection-harness-engineering-tool-using-agents/)
- [當 AI 把資料庫刪光：兩個真實案例與 Harness Engineering 的反擊](/ai-delete-database-harness-engineering/)
- [Harness Engineering 架構全景：AI 可以寫 Code，但不能自己上 Production](/harness-engineering-architecture-overview-ai-code-production-guardrails/)

**參考來源：**

- 四個 demo 的完整程式碼 — https://github.com/thegiive/harness_engineering
- OpenAI, *Harness engineering: leveraging Codex in an agent-first world* — https://openai.com/index/harness-engineering/
