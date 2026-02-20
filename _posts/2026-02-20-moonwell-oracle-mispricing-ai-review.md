---
layout: post
title: "Moonwell 178 萬美元事故：不是駭客神技，而是 Oracle 錯價 + AI 審查失守"
date: 2026-02-20 18:40:00 +0800
author: Wisely Chen
categories: [Web3, Security, AI]
tags: [Moonwell, Oracle, DeFi, Smart Contract, AI Coding, Risk Management]
image: /assets/images/moonwell-logo.png
---

很多人第一時間會說「Moonwell 被駭了」。

**先說結論：這更像是「系統自己把門打開」——Oracle 價格配置錯誤，讓清算與套利機器人在規則內把錢搬走。**

這不是某種超高階 0day exploit，而是金融系統最不該犯的那種錯：**價格來源與風控邏輯失真**。

---

## 事件 60 秒摘要

- 發生時間：**2026/02/15**
- 協議：去中心化借貸協議 **Moonwell**
- 損失：約 **178 萬美元（1.78M USD）**
- 核心原因：**Oracle 配置錯誤**，讓 cbETH 價格在某段時間被顯示為約 **$1.12**（真實市價約 **$2,200**）
- 結果：低價清算與套利被大量觸發，形成壞帳與資產損失

一句話版本：

**不是「被直接盜走」，而是「錯價近 2000 倍」導致協議在錯誤規則下被合法套利。**

---

## 問題本質：不是程式壞掉，是價格真相壞掉

在 DeFi 借貸模型裡，很多風控邏輯都依賴 Oracle：

- 抵押率計算
- 清算門檻判定
- 可借額度控制

當價格源頭錯，後面每一層都會「正確地做錯事」。

這也是為什麼我一直強調：**金融系統不是先看功能，而是先看失敗模式（failure mode）。**

---

## 這次損失怎麼發生的？

當 cbETH 被錯誤標成接近 $1 的資產後，機器人的行為很簡單：

1. 用極低成本償還可清算部位
2. 拿走實際高價值抵押品
3. 在市場變現，形成利潤

從攻擊者視角，這不是高難度 hacking，這是**風控參數送分題**。

Moonwell 事件後的緊急措施（下調相關資產借款與供應上限）是正確方向，但這是止血，不是治本。

---

## AI 協作程式碼爭議：焦點不該放錯

社群把注意力放在提交紀錄出現 AI 協作標記（如 `Co-Authored-By: Claude Opus 4.6`）。

這個討論有價值，但我認為要講清楚：

- **主因仍是配置/邏輯審查失敗**
- 不是「AI 自動產生神祕漏洞」
- 真正暴露的是：**人機協作流程沒有把關到位**

換句話說，AI 在這裡更像放大器：流程扎實，它加速；流程鬆散，它放大風險。

---

## 一張表看懂：技術事故 vs 流程事故

| 面向 | 這次 Moonwell 事件特徵 |
|---|---|
| 漏洞型態 | Oracle/配置錯誤導致價格失真 |
| 攻擊複雜度 | 低到中（套利/清算機器人即可） |
| 觸發機制 | 風控邏輯在錯價下被大量觸發 |
| AI 角色 | 不是主因；反映審查流程薄弱 |
| 治本方向 | 嚴格審計 + 雙軌審查 + 風控護欄 |

---

## 坦白說：最可怕的不是 bug，而是「你以為它不會錯」

很多團隊對 AI coding 的風險理解還停在「模型會不會寫錯語法」。

**真正會讓你賠錢的，通常不是 syntax error，而是 business logic / risk logic 的隱性偏差。**

尤其在 DeFi：

- 價格錯 1% 是噪音
- 價格錯 2000 倍 是系統性災難

這類事故的教訓是：**任何可影響清算與抵押率的參數，都應該被當成 production 級別變更來管理。**

---

## 可以立刻做的 5 件事（給 Web3 / AI 團隊）

1. **Oracle 變更雙人核准（4-eyes）**：任何價格源與 fallback 邏輯變更都不得單點上線。  
2. **加入價格異常熔斷**：超過閾值（例如 ±5% / 區塊）立即凍結相關清算路徑。  
3. **AI 協作 PR 強制人工 Review**：特別是風控、權限、清算、利率模型。  
4. **建立「影響半徑」測試**：每次上線前跑「錯價情境演練」與壓力測試。  
5. **事件後回溯標準化**：把「配置錯誤」納入正式威脅模型，不再只盯傳統 exploit。  

---

## 補充觀察：Moonwell 事件 vs Stripe「Minions」案例

你剛好丟的 Stripe 案例很值得放在一起看。

Stripe 對外提到：每週有超過千筆 PR 由內部 coding agents（Minions）產生，**人類審核但不一定有人手寫 code**。

表面上，這跟 Moonwell 都是「AI 參與寫碼」；但本質差異是：

- Moonwell 暴露的是 **風控配置與變更治理失守**
- Stripe 強調的是 **高自動化 + 嚴格 human review 流程**

所以真正問題不是「能不能用 AI 寫 code」，而是：

**你有沒有把審核、風險閥值、回滾機制做成制度，而不是靠個人經驗。**

---

## 結論

Moonwell 這次不是傳統意義上的「高手入侵」，而是**Oracle 錯價 + 審查流程不足**造成的可預防事故。

**AI 可以幫你加速開發，但不能替你承擔金融系統的最終責任。**

真正的護城河不是你用了哪個模型，而是你有沒有把「人機協作的安全流程」做成制度。

---

## 延伸閱讀

### 這次事件與 AI coding 討論
- [Decrypt｜Oracle Error Leaves DeFi Lender Moonwell With $1.8 Million in Bad Debt](https://decrypt.co/358374/oracle-error-leaves-defi-lender-moonwell-1-8-million-bad-debt)
- [Stripe on X｜Minions are our homegrown coding agents](https://x.com/stripe/status/2021273907680997439)
- [Stripe Dev Blog｜Minions: Stripe’s one-shot end-to-end coding agents](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents)

### 你可以一起看的方法論文章
- [OpenClaw 與 Agent 通道戰爭觀察](/openclaw-anthropic-channel-war/)
- [Single-Agent vs Multi-Agent：企業導入該怎麼選](/single-agent-vs-multi-agent-openclaw/)
- [OpenClaw Architecture Deep Dive](/openclaw-architecture-deep-dive-what-claude-code-didnt-tell-you/)
