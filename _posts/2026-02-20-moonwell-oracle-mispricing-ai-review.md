---
layout: post
title: "AI Coding Tool 寫的程式碼讓 DeFi 賠了 178 萬美元：Moonwell 事件與 Stripe 的警訊"
date: 2026-02-20 18:40:00 +0800
author: Wisely Chen
categories: [AI Coding, Security]
tags: [Moonwell, Oracle, DeFi, Smart Contract, AI Coding, Claude, Stripe, Risk Management]
description: "Moonwell 的 Oracle 配置程式碼由 Claude Opus 4.6 協作撰寫，一個 scaling factor 錯誤讓 cbETH 從 $2,200 變成 $1.12，178 萬美元就這樣被合法套利走。這不是 AI 的語法錯誤，而是 business logic 層級的失誤。同一時間，Stripe 每週合併上千筆 AI 產生的 PR，但「human-reviewed」在這個吞吐量下，到底是真的審查還是流程蓋章？"
image: /assets/images/moonwell-logo.png
permalink: /moonwell-oracle-mispricing-ai-coding-178m/
---

2026 年 2 月 15 日，DeFi 借貸協議 Moonwell 損失了 178 萬美元。

不是被駭客用什麼精密的 0day exploit 攻進去的。是 Oracle 的價格配置出了錯，cbETH 從真實市價 $2,200 被顯示為大約 $1.12。然後清算機器人在**完全合規的規則內**，把錢搬走了。

而這段出錯的 Oracle 配置程式碼，GitHub 上的 commit 紀錄寫著：`Co-Authored-By: Claude Opus 4.6`。

這件事讓我想講兩個觀點：

**第一，AI coding tool 產生的程式碼是會出錯的，而且在金融場景下，一個 business logic 的錯誤可以直接等於真金白銀的損失。**

**第二，當整個產業正在加速擁抱 AI 產出——Stripe 每週合併上千筆 AI 寫的 PR——我們有沒有對應的審查能力跟上這個速度？**

---

## Moonwell 到底發生了什麼事？

Moonwell 通過了一個 governance proposal，更新 cbETH 的 Oracle 配置。更新後的定價邏輯只用了 cbETH/ETH 的兌換比率，沒有乘上 ETH 的美元價格。cbETH 從 **$2,200** 變成 **$1.12**，錯了近 **2000 倍**。

清算機器人立刻出動：付 $1 觸發清算、拿走價值 $2,200 的 cbETH。超過 **1,096 顆 cbETH** 被搬走，協議產生 **178 萬美元壞帳**。監控系統幾分鐘內偵測到異常並緊急凍結，但錢已經走了。

---

## 關鍵問題：這段程式碼是 AI 寫的

社群很快在 GitHub 上發現，出問題的那個 PR 的 commit 帶有 `Co-Authored-By: Claude Opus 4.6` 的標記。

知名智能合約審計師 Pashov 在 X 上用了一個詞來形容這件事：**「vibe-coded」**。意思是用 AI 寫完，沒有做足夠的整合測試就上線。

但 Pashov 後來也補充了一句很重要的話：

**「這種錯誤，就算是 senior Solidity developer 也有可能犯。」**

我同意這個判斷。問題的核心不是「AI 比人差」，而是：

**AI 產出的速度太快，給了團隊一種「已經完成」的錯覺，導致後面的驗證環節被壓縮甚至跳過。**

如果這段配置是一個人花三天手寫的，review 的人大概會花半天認真看。但如果是 AI 五分鐘就產出的，reviewer 的心理預期就變了——「AI 寫的應該沒問題吧？」

這個心態，才是真正的風險。

---

## 一個 scaling factor 錯誤值多少錢？

來看看這次損失的結構：

| 項目 | 數據 |
|---|---|
| 錯誤類型 | Oracle pricing scaling factor 配置錯誤 |
| 錯誤程度 | cbETH 定價 $1.12 vs 實際 $2,200（差距 ~1,964x） |
| 被清算資產 | 1,096+ cbETH |
| 協議壞帳 | ~$1,780,000 USD |
| 攻擊複雜度 | 極低（標準清算機器人即可） |
| 攻擊者是否違法 | 否 — 在協議規則內操作 |

**攻擊者甚至不需要是「駭客」。任何跑著清算 bot 的人，在規則允許的範圍內完成了這筆操作。**

這讓我想到一件事：在金融系統裡，bug 的嚴重程度不是用「技術複雜度」衡量的，而是用**「離錢有多近」**來衡量的。

一個 UI 上的 typo 和一個 Oracle scaling factor 的錯誤，在程式碼 diff 上可能看起來差不多。但前者的損失是零，後者是 178 萬美元。

---

## 不只 Moonwell：這是 Moonwell 的第三次

更讓人不安的是，這不是 Moonwell 第一次因為 Oracle 問題出事：

- **2025 年 10 月**：Chainlink 定價差異導致 AERO、VIRTUAL、MORPHO 超過 **1,200 萬美元被清算**，產生 **170 萬美元壞帳**
- **2025 年 11 月**：wrsETH Oracle 故障，造成約 **370 萬美元壞帳**
- **2026 年 2 月**：cbETH Oracle 配置錯誤，**178 萬美元壞帳**

**四個月內，三次 Oracle 相關事故，累計壞帳超過 700 萬美元。**

這已經不是「個案」，這是系統性的 Oracle 治理問題。而 AI coding tool 的引入，讓這個問題加速暴露了。

---

## Stripe 的另一面：每週上千筆 AI PR，人真的看得完嗎？

講完 Moonwell 的案例，我想把視角拉到另一個場景。

2026 年初，Stripe 公開了他們的 Minions 系統：自研的 AI coding agent，**每週產出超過 1,000 筆 PR，全部是 AI 從頭到尾寫的**，然後由人類 engineer review 後合併。

Stripe 對外強調這些都是 **「human-reviewed」**。

![Stripe 官方推文宣布每週 1,300+ AI PR，底下留言質疑 "Human-reviewed... How??"](/assets/images/stripe-minions-human-reviewed-how.png)

Stripe 處理的是支付系統。Moonwell 處理的是借貸和清算。兩者的共通點是：**程式碼離錢非常近，錯誤的成本極高。**

如果 Moonwell 的經驗告訴我們 AI 寫的 Oracle 配置可以有 2000 倍的定價錯誤，那在每週 1,000+ PR 的吞吐量下，Stripe 的 human review 是真的防線，還是心理安慰？

**核心問題只有一個：AI 寫得太快，而人的 throughput 已經無法有效 review。**

當產出速度碾壓審查速度，review 就會從風險控制退化成流程蓋章。這不是工程效率提升，而是治理能力下滑。

---

## 坦白說

我自己每天用 Claude Code 寫程式，這個部落格上大部分文章背後的程式碼也都有 AI 參與。我不是反對 AI coding——我是重度使用者。

但正因為我大量使用，我更清楚一件事：

**AI 產出的品質分佈不是常態分佈，它是雙峰的。**

大部分時候它寫得很好，甚至比我自己寫得快又乾淨。但偶爾它會犯一種「看起來完全正確但邏輯上完全錯誤」的 mistake——而且它犯錯的方式很有自信，不會像新手那樣猶豫不決。

這種特性在寫 CRUD 和前端 UI 的時候無所謂，頂多 bug 修一修。

**但在金融系統、智能合約、風控邏輯這些「離錢很近」的場景，一個自信的錯誤就是 178 萬美元。**

---

## 給用 AI coding 的團隊：5 個具體建議

1. **區分「離錢遠」和「離錢近」的程式碼**
   - UI、文件、測試工具 → AI 自由發揮
   - Oracle、清算邏輯、權限控制、金額計算 → 強制人工 review + integration test

2. **AI PR 標記制度**
   - 所有 AI 協作的 PR 都加上標記（就像 Moonwell 的 `Co-Authored-By`）
   - 但這個標記不該是恥辱印記，而是告訴 reviewer：**這裡需要更仔細看**

3. **價格異常熔斷機制**
   - 任何 Oracle 價格變動超過閾值（例如單個區塊內 ±5%），自動凍結相關清算路徑
   - 這是 Moonwell 最缺的防線

4. **「影響半徑」壓力測試**
   - 上線前跑「如果這個價格錯了 10 倍 / 100 倍 / 1000 倍會怎樣？」的情境演練
   - 金融系統要測的不是 happy path，是 failure mode

5. **治理流程要追上產出速度**
   - 如果你的 AI agent 每週產出 1,000 筆 PR，那你的 review capacity 也要能真正消化 1,000 筆
   - 如果做不到，就該限制 AI 的產出範圍，而不是假裝 review 過了

---

## 最後的諷刺：Anthropic 的左右互搏

就在 Moonwell 事件發酵的同時，Anthropic 發布了新的安全工具，官方說法是「掃描程式碼庫的安全漏洞，並建議針對性的軟體修補方案供人類審查」。

Bloomberg 報導這件事的角度很直接：**Cybersecurity ETF 因為 Anthropic 的工具而下跌**，資安軟體類股正在經歷 2008 金融危機以來最大的季度跌幅（iShares Expanded Tech-Software Sector ETF 今年已下跌超過 23%）。

但我看到的是另一層意思：

**Opus 產生的 code，靠 Opus 的 security tool 去 scan。這不就是左右互搏嗎？**

用同一家公司的 AI 寫程式碼，再用同一家公司的 AI 檢查程式碼。如果模型對某類錯誤有系統性盲區，那檢查工具很可能也有同樣的盲區。

這不是在質疑 Anthropic 的技術能力——而是在指出一個結構性問題：**當生產者和審查者是同一個模型家族，獨立性就不存在了。**

傳統金融業有一個基本原則叫「職責分離」（Separation of Duties）：做帳的人不能同時審帳。AI coding 的世界，目前還沒有建立這個等價的制度。

---

## 結論

Moonwell 這次事故的教訓很簡單：

**AI coding tool 會犯錯。在金融場景下，一個 business logic 的錯誤不會只是 bug report，而是直接變成損失報告。**

Stripe 每週合併上千筆 AI PR 是一個令人印象深刻的工程成就。但如果審查速度跟不上產出速度，「human-reviewed」就會從安全機制退化成合規敘事。

真正的問題不是「AI 能不能寫程式碼」——答案是可以，而且寫得又快又好。

**真正的問題是：當 AI 寫錯的時候，我們有沒有能力在它上線之前攔住它？**

---

## 延伸閱讀

### Moonwell 事件相關報導
- [Decrypt｜Oracle Error Leaves DeFi Lender Moonwell With $1.8 Million in Bad Debt](https://decrypt.co/358374/oracle-error-leaves-defi-lender-moonwell-1-8-million-bad-debt)
- [CoinDesk｜Ether Briefly Priced at $1 After Glitch on DeFi App](https://www.coindesk.com/tech/2026/02/18/ether-briefly-priced-at-usd1-on-defi-app-moonwell-glitch-triggering-usd1-8m-in-bad-debt)
- [Crypto.news｜Moonwell's AI-coded Oracle Glitch Misprices cbETH at $1](https://crypto.news/moonwells-ai-coded-oracle-glitch-misprices-cbeth-at-1-drains-1-78m/)
- [BitcoinEthereumNews｜$1.78M 'Vibe-Coded' Oracle Bug](https://bitcoinethereumnews.com/tech/1-78m-vibe-coded-oracle-bug-puts-ai-coauthored-contracts-under-scrutiny/)

### Stripe Minions
- [Stripe on X｜Minions are our homegrown coding agents](https://x.com/stripe/status/2021273907680997439)
- [Stripe Dev Blog｜Minions: Stripe's one-shot end-to-end coding agents](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents)

### 相關方法論
- [AI Coding Tool 安全風險：當 Prompt Injection 遇上 RCE](/ai-coding-tool-security-risk-prompt-injection-rce/)
- [AI Agent 安全：遊戲規則已經改變](/ai-agent-security-you-xi-gui-ze-yi-jing-gai-bian/)
