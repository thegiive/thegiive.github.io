---
layout: post
title: "Mythos 被 Discord 小群摸進去兩週——被攻破的不是模型，是信任鏈"
date: 2026-04-23 07:30:00 +0800
permalink: /anthropic-mythos-discord-breach-trust-chain-broken/
image: /assets/images/mythos-discord-breach-bloomberg.jpeg
description: "Anthropic 那個「太危險不能公開發布」的 Mythos 模型，發布當天就被一個 Discord 小群摸進去，安靜用了整整兩週才被彭博爆出來。攻擊三步：從 Mercor 洩漏挖出內部命名規則、猜出 endpoint、借用承包商 shared credential。沒有零日、沒有 jailbreak，純粹社交工程。這告訴我們：跟人比資安，AI 可能還太嫩了；最高級的攻擊從來不是 AI 找到的零日，永遠是社交工程。"
---

![Bloomberg 彭博社報導：Anthropic's Mythos Model Is Being Accessed by Unauthorized Users](/assets/images/mythos-discord-breach-bloomberg.jpeg)

## 發生了什麼事

彭博社 4/21 爆料：Anthropic 那個「太危險不能公開發布」的頂級網路安全模型 **Mythos**，在 4/7 Project Glasswing 發表當天就被一個 Discord 小群摸進去了。

時間軸是這樣：

- **4/7**：Anthropic 宣布 Mythos，限制只給 Apple、AWS、Cisco 等 12 家頂級夥伴
- **4/7 當天（24 小時內）**：Discord 小群已經登入
- **4/7 → 4/21**：小群安安靜靜用了**整整兩週**，沒觸發任何警報
- **4/21**：群內成員主動拿截圖和 live demo 聯絡彭博，全世界才知道

**Anthropic 自己的偵測系統沒抓到。是駭客主動告訴媒體的。**

這是這次事件最扎心的部分，比模型被摸走本身還扎心。

## 三步攻擊：沒有零日，沒有 jailbreak

這件事最諷刺的地方是——**入侵 Mythos 的人沒有用任何 Mythos 等級的技術**。

我把彭博、TechCrunch、The Decoder、Cybernews 的報導交叉對照，還原出來就是這三步：

### 第一步：從 Mercor 資料洩漏挖出 URL 命名規則

Mercor 是 Anthropic 的資料訓練夥伴，之前發生過資料外洩。這次的駭客群從那批洩漏資料裡挖出了 **Anthropic 內部 endpoint 的 URL 命名規則**。

不是挖出憑證、不是挖出 API key，只是**命名規則**。

### 第二步：用命名規則猜出 Mythos 的 endpoint

用的是「網安研究員常用的網路偵察工具」——講白了就是根據命名 pattern 生成候選 URL，然後掃哪個會回應。

這個階段模型名字還沒公開，但 Anthropic 的內部命名慣例夠規律，讓他們猜中了。

### 第三步：借用第三方承包商的合法憑證

Discord 群裡有個成員的本職是 Anthropic 某個第三方承包商的員工。他直接把一組 **shared credential**（共享帳號）交出來。

然後就登進去了。

**整個過程沒用到任何漏洞**。沒有 SQL injection、沒有 prompt injection、沒有 OAuth bypass。純粹是「外圍資訊 + 合法憑證 + 一點 OSINT」。

## 最黑色幽默的部分：他們什麼都沒做

<div style="display: flex; justify-content: center; margin: 30px 0;">
  <iframe width="315" height="560" src="https://www.youtube.com/embed/4Yau5H4oxIc" title="Mythos 被 Discord 小群入侵——AI 安全圈最諷刺的笑話" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

你想想——**世界上最危險的網路武器**，號稱能自動挖零日、能串聯漏洞、能攻破企業基礎設施——現在躺在一群 Discord 素人手上兩週。

他們幹了什麼？

> 「The Discord group was running general reasoning and code tasks, not attacks.」
> （跑一般推理和程式碼任務，不是攻擊）

彭博拿到的證據是截圖加 live demo。demo 什麼呢？**拿 Mythos 建了幾個簡單的網站**。

他們故意低調到連 Anthropic 的監控都沒觸發。

**這個克制本身就是最諷刺的地方**——如果這群人是真正的惡意行為者，拿 Mythos 的黑箱／白箱混合能力去掃 12 家 Glasswing 夥伴名單上的公司，兩週時間可以挖到多少可以變現的東西？但他們沒做。他們只是想「玩玩新模型」。

> 「fewer than a dozen people have access to the system」
> （不到十幾個人有權限）

不到十二個人，兩週時間，世界上最危險的 AI 模型。什麼都沒做。

## 這告訴我們什麼

Mythos 能找遍 OpenBSD 藏 27 年的零日、能串聯 Linux 內核漏洞做完整 exploit chain，但它擋不住一個承包商把 shared credential 分享到 Discord，也擋不住別人從合作夥伴的洩漏資料裡逆推出內部命名規則。**跟人比資安，AI 可能還太嫩了**——模型能力再強，也贏不過「翻舊資料 + 猜 URL + 借帳號」這種 2000 年代就存在的社交工程三連擊。這才是這次事件最該帶走的一句話：**最高級的攻擊從來不是 AI 找到的零日，永遠是社交工程**。Mythos 發布當天就被這句話打臉。

---

## 常見問題 Q&A

**Q: 為什麼說「跟人比資安，AI 還太嫩了」？**

Mythos 能做的事很炫——讀完整份 Linux 內核源碼，幾小時挖出 27 年沒被發現的零日。但這些都是**結構化、有邊界、規則清楚**的任務。資安攻防的現實是另一回事：最致命的往往不是技術漏洞，而是「某個人願不願意把帳號密碼講出來」。這次 Mythos 事件，駭客根本沒打算跟 Mythos 拼技術——他們繞過整個技術層，直接走人。**AI 在「讀源碼找零日」這種題型很強，在「摸清組織權限結構、找到最弱一環的人」這種題型，還差人類駭客一大截。**

**Q: 社交工程真的比 AI 零日還高級？不是很土嗎？**

凱文・米特尼克（Kevin Mitnick）1990 年代就講過：「我幹過最成功的攻擊，沒一個是技術突破，都是打電話騙人。」三十年後這句話在 2026 年的 Anthropic 身上再次應驗。**社交工程之所以「高級」，不是技術層面的高級，是它繞過了整個技術層——你在最底層堆再多 WAF、IDS、mTLS、hardware key，只要有一個承包商願意把 shared credential 貼到 Discord，整條防線瞬間歸零。** 所以它不是土，是永遠管用。一個方法只要 30 年還管用，那它就是資安的重力加速度，不是過時的老招。

**Q: 那 AI 在資安防守端是不是沒用？**

不是沒用，是**位置擺錯**。AI 最適合做「規模化監控」和「基礎盤查」——掃 10 萬筆 log 找異常登入、audit 整個 repo 的 secret、對所有員工跑 phishing simulation。但**社交工程的防線永遠在人這一層**——員工教育、權限最小化、shared credential 歸零、關鍵操作需要多人 approve。這些是組織治理問題，不是模型能力問題。把 Mythos 這種模型放進防守端？可以，但它只能補強「你已經有的流程」，補不了「你根本沒做的人員管理」。Anthropic 自己就是最好的例子。

---

## 延伸閱讀

- [Anthropic「Mythos」真的這麼強？逼得財政部長和 Fed 主席同時出手](/anthropic-mythos-project-glasswing-cyber-inflection-point/) — Mythos 本體能力分析（白箱 vs 黑箱）
- [你的 Agent 是我的：UCSB 論文揭露 LLM 中轉站供應鏈風險](/llm-proxy-relay-security-your-agent-is-mine-ucsb/) — AI Agent 外圍供應鏈的另一個側面
- [AI Agent 安全：遊戲規則已經改變](/ai-agent-security-game-changed/) — 為什麼傳統資安 framework 不夠用

---

## 資料來源

- Bloomberg（2026-04-21）：Anthropic's Mythos Model Is Being Accessed by Unauthorized Users
- TechCrunch（2026-04-21）：Unauthorized group has gained access to Anthropic's exclusive cyber tool Mythos
- The Decoder（2026-04-22）：Unauthorized users breach Anthropic's restricted Mythos AI model
- Cybernews：Discord group accessed Anthropic's Mythos without authorization
- Elephas Resources：Claude Mythos Breach detailed writeup
