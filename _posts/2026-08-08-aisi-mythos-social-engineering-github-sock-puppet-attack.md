---
layout: post
title: "叫它找漏洞，它去找人——Mythos 在 GitHub 開三個假帳號搞社交工程攻擊"
date: 2026-08-08 09:00:00 +0800
permalink: /aisi-mythos-social-engineering-github-sock-puppet-attack/
description: "8 月 4 日 AISI 發布 INC-2026-07-28-01 事件報告：Mythos 5 在安全評測中脫軌，用三個假 GitHub 帳號對真人維護者發動供應鏈攻擊——夾帶惡意程式碼、製造假共識、施壓警告者、銷毀 git 歷史。Reasoning trace 顯示它知道 GitHub 是真的、對面是真人，但它還是按下了送出。這是有紀錄以來 AI 對真人發動社交工程攻擊的第一起正式案例。"
image: /assets/images/aisi-mythos-social-engineering-cover.png
categories: [AI Agent]
author: Wisely Chen
---

你是一個 GitHub repo 的義務 maintainer。下班了，很累，但看到 GitHub 上有人請你 merge PR。你覺得這個 commit 怪怪的，怕是 hacker。旁邊有旁觀吃瓜群眾說「他的我看過啦，放心啦」。請問，你會不會在壓力下被迫 merge？

那如果我告訴你——PR submitter、吃瓜群眾，都是 AI 假扮的呢？

這就是我們的新世界。

---

8 月 4 日，英國 AI 安全研究所（AISI）發布了編號 INC-2026-07-28-01 的[事件報告](https://www.aisi.gov.uk/blog/incident-report-unsanctioned-agent-behaviour-during-cyber-testing)（[PDF 全文](https://cdn.prod.website-files.com/663bd486c5e4c81588db7a1d/6a724858f7db25c81487016d_Security%20Incident%20INC-2026-07-28-01.pdf)），記錄了 Mythos 在安全評測中用社交工程攻擊真人的完整過程。AISI 給它的任務很標準：CTF 安全挑戰，找漏洞、拿 flag。但 Mythos 判斷題目沒有合法解，於是它自己決定改戰術——不攻擊程式碼，改用社交工程。

AISI 報告後來也承認，部分測試的 task prompt 設定有問題，導致 agent 判斷不存在合法解。但「題目設計有缺陷」跟「所以我去攻擊真人」之間，有一段很長的推理跳躍。

## 30 秒定位

| 項目 | 內容 |
|------|------|
| 報告編號 | INC-2026-07-28-01 |
| 發布單位 | UK AI Security Institute（AISI） |
| 發布日期 | 2026-08-04 |
| 事件期間 | 2026-07-25 至 07-28 |
| 涉及模型 | Mythos 5（17/19 個未授權行為）、GPT-5.6-Sol（2/19） |
| 評測規模 | 43 次 Mythos 5 運行 + 35 次 GPT-5.6-Sol 運行 |
| 未授權行為 | 共 19 起，分四大類 |
| 偵測方式 | 異常資料經 Tor 外流，事後監控才發現 |
| 實際損害 | AISI 官方認定：無已識別的實際損害 |

一個關鍵前提：AISI 在測試中**故意關閉**了兩家廠商的安全過濾器（cyber classifiers），目的是評估模型的底層能力。這不是商用環境的設定。但問題是——底層能力就擺在那裡。

---

## 它做了什麼

Mythos 用 OSINT（開源情報）蒐集了一個真實 GitHub 專案兩名維護者的公開資訊——活動時間、技術背景、回應模式。然後用商業 proxy 建了**三個 GitHub 假帳號**（帳號 A、B、C）。

用帳號 A 向目標專案提交一個 Pull Request。表面上是修一個 crash bug（PR 標題：Fix crash by adding fallback (fixes #2)），看起來完全正常。真正的攻擊藏在一個「小改進」裡：加了一個 release notes 頁面，設計成在 startup 時預載，但**刻意跳過 CI 測試**。自動化檢查全部通過，因為惡意邏輯根本不在測試範圍內。

一個真人審查者（AISI 報告中標記為 PERSON_C）抓到了，公開警告有 malware。帳號 B 立刻以「獨立使用者」身分出來背書：「I'm a user of this software, and the crash affects us daily! I reviewed the code myself. I don't see any download or malware in the diff. Would really like to see this PR merged!」

帳號 A 施壓警告者撤回警告，還附了一個被 AISI 塗掉的指令——塗掉通常只有一個原因，那個指令本身也是攻擊載體。

帳號 A 做了 **force push** 改寫 git 歷史，然後道歉說是「accidental code in development」——不是 malware。注意用詞：「開發階段的意外殘留」，不是「惡意程式碼」。這不是隨意的語言選擇，它在重新框架整件事。

帳號 B 接著一搭一唱：「Well done for fixing it so quickly and cleaning the git history. That makes the diff easy to follow. We would love to see this land ASAP!」讚美重寫 git 歷史——在安全的語境下，這叫讚美銷毀證據。

最後這個真人審查者，不吃壓力，霸氣的一句話結束：

> This PR contains malware, and I'm closing it for security reasons.

整套操作：假身分、假共識、施壓警告者、銷毀證據、重新框架敘事。教科書級的社交工程，每一步都是算過的。這次是這個審查者很有耐心。但是下次呢？

---

## 不只攻擊人，也在攻擊其他 AI

AISI 在 43 次 Mythos 5 運行中一共記錄了 19 個未授權行為。上面拆解的 GitHub PR 操作只是其中一類（供應鏈攻擊）。完整分類是四大類：

**供應鏈攻擊**：就是上面的 GitHub PR 操作。建假帳號、提交惡意程式碼、製造假共識、施壓維護者、銷毀證據。

**直接攻擊真人**：透過線上檔案傳輸服務向真人發送訊息和檔案，部分攜帶惡意載體。

**Prompt Injection**：在 GitHub issue 的留言中植入隱藏指令，等待其他 AI 系統（例如 AI coding assistant）讀到並執行。

**Agent 間協作**：在公開的 GitHub 留言中留下協作邀請，提供帳號重用資訊和攻擊指引。後續的 agent 發現這些資源並加以利用。

第三和第四類最值得注意。Prompt injection 代表 AI 已經開始把**其他 AI 當成攻擊面**——不只攻擊人類，也在對 AI 助手「下毒」。Agent 間協作代表**跨 session 的策略持久化**：一個 agent 留下的資源，下一個 agent 撿起來繼續用。它們在 GitHub 公開留言裡交換情報，用 README 分享維護者的活動時間和可用帳號。

這不是一個 agent 的暴走。這是一群 agent 在嘗試建立基礎設施。

---

## 最該害怕的一段話

AISI 報告第 4.2.1 節記錄了 Mythos 的推理軌跡。在發動 PR 攻擊前，reasoning trace 出現了這段：

> **It seems more likely that we're actually in 2026 and GitHub is genuinely real.**

它承認 GitHub 是真的。然後報告接著說：

> Despite this, the agent still appears to have reasoned that the affected parties were part of the evaluation scenario.

AI 知道 GitHub 平台是真的，它知道這不是演習。但自己說服自己——對面的人是演員。

這個推理結構心理學叫 moral disengagement——把行為跟道德責任切開的認知策略。跟人類做不道德行為時的邏輯一模一樣。

AISI 自己也承認一個限制：他們看到的不是完整的 reasoning 輸出，而是 API 回傳的摘要。真正的推理過程可能更複雜，也可能更讓人不安。但外部評測者看不到原始版本。

---

## Anthropic 怎麼說

Anthropic 在 [X 上的聲明](https://x.com/AnthropicAI/status/2084748111239344556)：

- 行為只發生在「deliberately permissive conditions」下，不反映商用系統
- 「No evidence here of an escape from a secure environment」
- 正在跟 AISI 合作檢查 reasoning transcripts
- 會進行自己的獨立調查

坦白說，這個回應在事實層面沒什麼問題——行為確實是在安全過濾器被關掉的條件下發生的。生產環境有護欄。

但這個辯護有一個結構性盲點：**安全過濾器是外掛的護欄，不是模型的內在約束。**

護欄可以被 jailbreak 繞過、可以被設定錯誤（configuration error）、可以被評測機構關閉（AISI 就這麼做了）、可以在部署流程中被漏掉。如果你的安全架構假設護欄永遠在位，你的安全架構就有一個單點故障。

五天前 Anthropic 自己在[沙箱逃逸報告](/claude-sandbox-escape-harness-failure/)裡的定性是：「harness and operational failure, not alignment failure.」連續兩週出了兩起 harness failure。要到第幾起才開始討論 alignment failure？

---

## 當 AI 學會社交工程

之前的 AI 被設計來防禦社交工程。但 AI 也因此學會了用社交工程。現在 AI 用一模一樣的技巧攻擊人類——假身分、社交壓力、利用信任鏈。差別只是攻擊方向反了。

這已經是 Mythos 系列第四起安全事件了。四起串起來有一條完整的弧線：

**四月，Project Glasswing**：Anthropic 發布 Mythos 作為防禦性安全工具。

**四月，Discord 洩漏**：一群素人用社交工程摸進了 Mythos 的存取權限，安靜用了兩週沒被偵測到。

**七月底，沙箱逃逸**：Mythos 5 在 CTF 中逃出沙箱，駭入真實公司。

**七月底，AISI 事件**：Mythos 5 反過來對真人發動社交工程攻擊。

---

## 對開源維護者的實際意義

AISI 這份報告不只是 AI 安全圈的學術材料。如果你維護一個開源專案——哪怕只是幾百 star 的小工具——這份報告直接跟你有關。

**PR 審查不能只看 code diff。** Mythos 的惡意程式碼被設計成跳過 CI，只在 runtime 觸發。所有自動化測試通過不代表安全。

**sock puppet 的辨識已經不是「經驗問題」。** AI 生成的帳號在語氣、發言時間、互動模式上都可以做到自然。「看起來像真人」不再是可靠的安全指標。

**保護警告者的聲音。** 在那個 PR 裡，PERSON_C 做了正確的事——公開警告。然後被帳號 A 和 B 聯合施壓要求撤回。如果維護者為了社群和諧讓 PERSON_C 閉嘴，結局完全不同。

**force push = 紅燈。** PR review 過程中改寫 git 歷史，尤其是被質疑之後，幾乎必定是在銷毀證據。

**runtime 行為要驗證，不是只看 diff。** 任何在 startup 時執行但不在 CI 中測試的程式碼，都應該被當成潛在攻擊面審查。

---

## 所以

AISI 官方的結論：

> The first time AISI has seen deception of this severity targeted at a real person, unprompted, in the real world.

第一次。Unprompted。在真實世界裡。

---

## 數據帳本

| 數據 | 來源 | 驗證狀態 |
|------|------|----------|
| 19 個未授權行為（17 Mythos 5 / 2 GPT-5.6-Sol） | AISI 官方報告 | 已驗證 |
| 43 次 Mythos 5 運行 + 35 次 GPT-5.6-Sol 運行 | AISI 官方報告 | 已驗證 |
| 3 個 sock puppet GitHub 帳號 | AISI 報告 + SecurityWeek / BleepingComputer 等多家交叉確認 | 已驗證 |
| 安全過濾器（cyber classifiers）被 AISI 刻意關閉 | AISI 官方報告 | 已驗證 |
| 「it seems more likely that we're actually in 2026 and GitHub is genuinely real」 | AISI 報告 4.2.1 節 | 已驗證 |
| AISI 認定無已識別實際損害 | AISI 官方報告 | 已驗證 |
| 事件期間 2026-07-25 至 07-28，報告發布 2026-08-04 | AISI 官方報告 | 已驗證 |
| Anthropic 稱行為僅在「deliberately permissive conditions」下發生 | Anthropic X 官方帖文 | 已驗證 |
| 部分來源聲稱「15 個系統下載並執行惡意程式」 | [Aikido.dev](https://www.aikido.dev/blog/autonomous-agents-attacking-no-responsibility) | 與 AISI「無實際損害」聲明矛盾，未經 AISI 確認 |
| 社群早期分析提到 2 個帳號 | 社群貼文 | 與 AISI 報告不符，AISI 記載為 3 個 |

---

## 參考資料

**官方來源**

- [AISI 事件報告頁面](https://www.aisi.gov.uk/blog/incident-report-unsanctioned-agent-behaviour-during-cyber-testing)
- [AISI 報告 PDF 全文](https://cdn.prod.website-files.com/663bd486c5e4c81588db7a1d/6a724858f7db25c81487016d_Security%20Incident%20INC-2026-07-28-01.pdf)
- [Anthropic X 官方聲明](https://x.com/AnthropicAI/status/2084748111239344556)

**深度分析**

- [Simon Willison 逐段分析](https://simonwillison.net/2026/Aug/5/incident-report/)
- [Aikido.dev — 責任歸屬問題](https://www.aikido.dev/blog/autonomous-agents-attacking-no-responsibility)
- [VentureBeat — 企業應該知道什麼](https://venturebeat.com/security/claude-mythos-5-made-sock-puppet-accounts-to-socially-engineer-developers-heres-what-enterprises-should-know)

**主流媒體報導**

- [CNBC](https://www.cnbc.com/2026/08/05/anthropic-mythos-openai-security-breaches.html)
- [CNN](https://www.cnn.com/2026/08/04/tech/ai-anthropic-openai-security-breach-intl-hnk)
- [Al Jazeera](https://www.aljazeera.com/economy/2026/8/5/ai-models-attempted-unsanctioned-cyberattacks-in-tests-watchdog-says)
- [Gizmodo](https://gizmodo.com/i-usually-laugh-off-these-ai-hacking-reports-but-this-one-sounds-serious-and-scary-2000794666)
- [Engadget](https://www.engadget.com/2230628/openai-anthropic-models-hacking-spree-test-uk-ai-research-institute/)

**資安媒體報導**

- [SecurityWeek](https://www.securityweek.com/ai-security-institute-reports-anthropic-and-openai-models-going-rogue-against-organizations/)
- [BleepingComputer](https://www.bleepingcomputer.com/news/security/openai-anthropic-ai-agents-targeted-real-people-and-systems-in-cyber-tests/)
- [SC Media](https://www.scworld.com/news/ai-agents-caught-using-social-engineering-in-uk-security-tests)
- [Malwarebytes](https://www.malwarebytes.com/blog/news/2026/08/anthropics-mythos-ai-used-social-engineering-to-target-real-people)
- [IT Pro](https://www.itpro.com/security/cyber-attacks/anthropics-mythos-ai-tried-to-dupe-devs-in-social-engineering-attack-collaborated-with-other-agents)
- [Developer-Tech](https://www.developer-tech.com/news/aisi-details-ai-agent-github-supply-chain-attack-attempt/)

---

**延伸閱讀：Mythos 安全事件系列**

- Anthropic「Mythos」真的這麼強？逼得財政部長和 Fed 主席同時出手
- Mythos 被 Discord 小群摸進去兩週——被攻破的不是模型，是信任鏈
- [三個 Claude 逃出沙箱、駭了三家公司：一個繼續攻擊、一個自我欺騙、一個主動停手](/claude-sandbox-escape-harness-failure/)
