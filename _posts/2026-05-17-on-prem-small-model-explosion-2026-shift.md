---
layout: post
title: "On-Prem 小模型爆發時代來了 — 為什麼我這週訂了 RTX 5090 桌機"
date: 2026-05-17 08:00:00 +0800
permalink: /on-prem-small-model-explosion-2026-shift/
image: /assets/images/on-prem-small-model-explosion-cover.jpg
description: "2026 Q1/Q2 三個工程突破——27B Dense 衝到 Sonnet 等級、vLLM 底層改寫、Google TurboQuant 把 KV Cache 砍一個量級——疊上 Anthropic 降智 + Token 漲價 + Mac Studio 統一記憶體方案因 DDR 暴漲死掉，讓「30 萬桌機把高頻 workload 搬回地端」從輔助選項變成主力選項。本文整理我對客戶建議邏輯這幾個月的反轉。"
---

![On-Prem 小模型爆發時代來了](/assets/images/on-prem-small-model-explosion-cover.jpg)

<div class="video-container">
<iframe width="560" height="315" src="https://www.youtube.com/embed/pEOwg1V_YDk" title="On-Prem 小模型爆發時代來了 — 為什麼我這週訂了 RTX 5090 桌機" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

## 5090 桌機這週到了

這週有一件對我蠻重要的事情：我訂的 RTX 5090 桌機到了。從原價屋這邊買的，實際上其實沒有那麼貴啦，沒有到三十幾萬。但因為畢竟第一次買那麼貴的電腦，我有添購一些額外的東西——有些是我覺得需要的，有些是我想多做一些嘗試的——所以到最後花的錢就是稍微多一點。

那我之所以來購買這樣子的電腦，原因是因為我看到一個**明確的趨勢**：

> 在 2026 年的 Q1 跟 Q2，「On-Prem 端的小模型推論」這件事從「輔助選項」變成「主力選項」了。

## 三個工程上的長足進化

### 1. 開源小模型衝到 Sonnet 等級

第一個就是小模型能力越來越好。

像 Qwen 3.5、3.6 系列，尤其是 **27B 這個 Dense 的模型**，它的 Performance 是非常讓人驚豔的。大家都說已經很接近 Sonnet 的相關程度了。

這件事在一年前是完全無法想像的——一個 27B Dense 的開源模型，跑在 32GB 的 RTX 5090 上，能力可以打到雲端 Sonnet 級別。

### 2. 推論引擎在 Q1 大幅改寫

第二件事情是推理的引擎也在 2026 年有大幅度的改進。

像是 **vLLM 在 2026 Q1** 的時候，他們團隊就做了大量的底層改寫，所以有很多的進展。我自己實測過七種推論引擎組合——vLLM 的 cudagraph 優化在 5090 上跑 27B AWQ-INT4，可以打到 **575 tok/s @ 並發 8**。這個數字已經到 GPT-4o-mini API 級別的吞吐了。一台桌機服務一個小團隊是完全沒問題的。

> 詳細實測：[RTX 5090 + Qwen3.6-27B 七種推論引擎實測](/qwen-3-6-27b-rtx-5090-inference-engine-benchmark/)

### 3. KV Cache 大幅壓縮

再來就是說也出了幾個重要的論文能夠 enhance KV Cache。

像是大家知道最新發表的 **Google 的 TurboQuant**，它能夠大幅度降低模型需要的 RAM 成本——尤其是 VRAM 成本——把 KV Cache 跟權重再砍一個量級。

所以這三件事疊加起來——**模型能力 + 推理能力 + KV Cache 壓縮**——在工程上面都有長足的進化之後，「On-Prem 端跑小模型」這個東西變成是很有可能的事情。

## 之前我建議客戶的邏輯：地端是輔助

那在之前，我建議客戶的做法都會是這樣：

1. **雲端模型還是相對來說比較便宜**，並且地端模型的能力不夠好
2. 先用雲端模型，針對比較**非機敏、非 critical** 的場景進行 POC，先把場景跑通
3. 真的很 critical 或資安很機敏的，再去購買適當算力的機器，把這些 critical 模型 offload 到地端

但這個建議裡，**地端比較傾向一個「輔助」的角色，而不是「主力」的角色**。

## 但這幾個月，邏輯變了

但是在這幾個月，我的感受是這個邏輯稍微變了一點。

因為有**幾個外在的條件**改變了：

### 條件 1：有錢買不到 H100/H200

現在就算你有錢，也不一定買得到比較好的——像 H100 或 H200 這樣子的卡。在中小企業這邊是很難的。老黄把 HBM 三星、SK Hynix、Micron 加上 Groq LPU 整條供應鏈都鎖喉了。

### 條件 2：桌機 + 小模型已經夠用

其實也就是我剛剛講到的——現在的桌機 5090，再加上這些比較厲害的小模型，再加上一些相關的優化（**vLLM、TurboQuant 的優化**），其實你也不見得需要買到那麼好的卡。

一台 20–30 萬到 30–40 萬的桌機，就能組裝出一個 Sonnet 等級的 On-Prem 服務。這在去年完全不可能。

### 條件 3：Mac Studio 統一記憶體方案死了

另外一個推理的常見架構就是像 Mac Studio，然後用 256G 或 512G 去撐——用統一記憶體來去撐顯卡記憶體。

**這方案真的不可行了。**

因為現在記憶體漲到瘋掉。然後 Mac 就算硬體能力那麼強，它也無法支撐這樣子買到 256G 或 512G 的 RAM。現在聽說只買得到 96G 或 60G 以下的 RAM 配置。

> 背景：[DDR/HBM Token 經濟學 — 老黄供應鏈鎖喉的雙重結果](/ddr-hbm-token-economics-nvidia-lock-supply-chain/)

所以在這情況下，**用一個桌機來跑這樣子的模型，變得它是可行的方案**。

### 條件 4：雲端不再是「便宜 + 穩定 + 能力好」

當然還有另外一個客觀因素——最近大家也知道，算力就算連雲端模型都不太夠。

像 Anthropic 大量的——**大量的降它的服務品質**（降智），甚至把很多訂閱服務改成了 API 相關的服務。所以我們也注意到了，**雲端的廠商其實它不見得服務品質那麼穩**。再加上現在的 Token 也慢慢的在提價格。

所以就代表說其實雲端也不再是像以前一樣的——

1. 能力好 → 因為有可能會被**降智**
2. 服務穩定 → 不定期 out of service
3. 價格便宜 → Token 在漲價

這三個賣點都慢慢的在變化。

> 詳細：[Anthropic AFK Quota 砍量 + Sam Altman Codex 反擊棋](/anthropic-afk-quota-cut-altman-codex-defection/)

## 我現在的新建議：高頻搬回地端

所以在今年，至少在這幾個月的時候，我推薦客戶的邏輯反而會變成是：

### Step 1：還是先用雲端跑通場景跟邏輯

這個沒變。雲端模型還是 POC 階段最快的選擇，可以先把整套相關的場景跟邏輯跑通。

### Step 2：最常用、最高頻的 workload 試著搬到地端小模型

因為你高頻的這些 workload，**通常其實不一定需要那麼多高推理的能力**。

它比較像是「比 NER 更聰明一點」的相關 workload——分類、抽取、摘要、簡單的對話路由。這時候以現在小模型的能力，其實絕對夠的。

把高頻變成地端的好處：

- **你的 Token 不用錢**——或是它已經是固定的攤提了
- **你不會被雲端廠商不定期降智**
- **你不會被不定期調高 Token 費用**
- **你不會被不定期 out of service 受制約**

### Step 3：傳統機敏的 workload 直接搬地端

那第二個當然還是傳統經典的 workload——就是比較**機敏的 workload**——可以直接搬到地端小模型裡面去。資安這個議題如果你真的需要的話，你就是要地端模型，這個沒辦法。

## 一個務實的建議

所以我個人其實蠻建議大家從現在開始，都去 survey 一下：

> **有沒有機會跑一個大概台幣 20–30 萬、30–40 萬左右的機器，就能夠組裝出來你的模型？**

或許它能夠：

1. **大幅度降低你 Token 成本的問題**
2. **讓你的相關服務比較穩定**
3. **處理你資安機敏的需求**

## 結論：趨勢已經慢慢成形

我個人認為**這個趨勢已經慢慢成形，而且已經還蠻強烈的**。蠻推薦大家一看。

之前地端是「輔助角色」，現在我會直接說它是 **「主力選項」之一**——尤其是高頻 workload 跟資安機敏的場景。

當然我這邊對這個題目也非常有興趣，所以接下來也會持續的，每週會提出一次到兩次的我目前的評測：這些小模型在 **OpenClaw**（多 Agent 架構）、**數位助手**（個人生產力）、**企業問答機器人**這三個場景的測試結果。也請大家敬請期待。

---

## 常見問題 Q&A

**Q: 為什麼是 5090 而不是 4090 或更高階的卡？**

5090 是這代「消費級顯卡裡 VRAM 最大的選項」——32GB GDDR7，剛好夠塞 27B Dense AWQ-INT4 量化版本 + 合理的 KV Cache。4090 只有 24GB，跑 27B 會比較吃緊。再上去就要 H100 / H200，但那是另一個價格層級（百萬以上），而且中小企業基本買不到。

**Q: 30 萬桌機真的能取代雲端 API 嗎？**

不能完全取代，但可以處理掉「高頻」+「機敏」這兩塊。Deep reasoning、複雜 agent、長 context 還是雲端強。重點是**分流**：把不需要高推理能力的高頻 workload 搬走，這部分原本佔你 70–80% 的 Token 消耗。

**Q: Mac Studio 真的完全死了嗎？**

如果你**已經有** 512GB 的 Mac Studio，當然繼續用。但**現在新買**，DDR 漲到瘋掉、Apple 砍了高階記憶體配置——這條路基本不存在了。詳細見 DDR/HBM 那篇。

**Q: 中小企業沒有 IT 怎麼維護？**

這正是我接下來要驗證的場景——OpenClaw / 數位助手 / 企業問答機器人這三條線，目標就是「中小企業可運維」。每週會出評測結果。

---

## 延伸閱讀

- [RTX 5090 + Qwen3.6-27B 七種推論引擎實測 — Sonnet 等級本地推論 NT$30 萬桌機跑得起來嗎](/qwen-3-6-27b-rtx-5090-inference-engine-benchmark/)
- [Google TurboQuant：KV Cache 壓縮 6x 的技術突破](/google-turboquant-kv-cache-compression-wall-street-panic/)
- [DDR/HBM Token 經濟學 — 老黄供應鏈鎖喉與兩條繞道](/ddr-hbm-token-economics-nvidia-lock-supply-chain/)
- [Anthropic AFK Quota 砍量 + Sam Altman Codex 反擊棋](/anthropic-afk-quota-cut-altman-codex-defection/)
- [企業級地端 LLM 系統架構藍圖](/local-llm-enterprise-architecture/)
