---
layout: post
title: "這週兩件資安大事：eMudhra 私鑰是 4，PHP2Shell 緊急修補"
date: 2026-10-22 09:00:00 +0800
permalink: /emudhra-weak-key-php2shell-same-week/
tags: [eMudhra, PHP2Shell, CVE-2026-109618, CVE-2026-109619, Patch the Planet, GPT-5.6 Sol, 憑證, CA, 協調揭露, coordinated disclosure]
categories: [AI 資安]
image: /assets/images/php2shell-takaichi-x-post.png
image_alt: "日本首相高市早苗 2026 年 10 月 21 日在 X 上呼籲網站營運者準備套用 PHP 修補"
description: "10 月 17 日到 21 日，資安圈連續發生兩件影響所有網路使用者的事。第一件，印度憑證機構 eMudhra 有 8 張中繼憑證的私鑰全部小於 256，其中一把就是數字 4，Firefox 收到報告不到三小時就完成封鎖，Apple、Microsoft 隨後跟進。第二件，PHP 緊急修補兩個未登入就能遠端執行程式碼的漏洞（PHP2Shell），由 OpenAI Patch the Planet 計畫下的 Calif 用 GPT-5.6 Sol 找到，修補前兩天禁運被打破，荷蘭、芬蘭政府網站先後下線，日本幾個大站進入緊急維護。這篇整理兩件事的時間軸、影響範圍和官方建議。"
author: Wisely Chen
faq:
  - question: "eMudhra 憑證事件是什麼？一般使用者需要做什麼？"
    answer: "2026 年 10 月，印度憑證機構（Certificate Authority, CA）eMudhra 被發現有 8 張中繼憑證的私鑰全部小於 256，其中一把就是數字 4，任何人都能在不到一秒內從公開憑證算出私鑰，進而偽造任意網站的 HTTPS 憑證。Firefox、Chrome、Apple、Microsoft 在 10 月 17 日到 20 日之間陸續封鎖，Mozilla 和 Chrome 也決定移除上層根憑證 emSign ECC Root CA – G3。一般使用者更新瀏覽器和作業系統即可；需要注意的是伺服器、應用程式和嵌入式設備的信任清單不一定會自動更新，管理者要自行檢查。"
  - question: "PHP2Shell 是什麼？影響哪些版本？"
    answer: "PHP2Shell 是 CVE-2026-109618 和 CVE-2026-109619 兩個漏洞的合稱，CVSS 9.2，屬於未授權遠端程式碼執行（Remote Code Execution, RCE）。在 Apache + mod_php 環境下，一個未登入的請求在應用程式碼執行之前就能觸發。修補版本是 PHP 8.5.12、8.4.27、8.3.36、8.2.35，2026 年 10 月 21 日發布。PHP 8.1 以前不在正式支援範圍，7.4、8.0、8.1 只有有限的原始碼 backport，需要透過發行版、廠商或升級來處理。官方表示更新是唯一完整的修補。"
  - question: "PHP2Shell 是 AI 找到的嗎？"
    answer: "根據 OpenAI 的說法，資安公司 Calif 在 OpenAI 的 Patch the Planet 計畫下，用 GPT-5.6 Sol 找到了漏洞；OpenAI 同日也獨立回報了同一個根因，Wiz 稍後也獨立回報。PHP 基金會則表示，同一個根因的第一個跡象，2024 年就已經被基金會簽約的核心開發者看到。"
  - question: "什麼是協調揭露（Coordinated Disclosure）？PHP2Shell 的禁運是怎麼被打破的？"
    answer: "協調揭露是指漏洞發現者先私下通報維護者，雙方約定一個日期同時公開漏洞和修補，讓使用者在攻擊者拿到細節前就能更新。PHP2Shell 的禁運在預定發布日前兩天被打破：先是 CVE 編號在社群外流（沒有技術細節），接著 Calif 誤發了一支 PoC 示範影片，最後 Chainguard 比協調時間早六個多小時發布了含修補的映像檔，攻擊者可以直接比對修補後的 binary。PHP 因此把發布日從 10 月 22 日提前到 10 月 21 日。"
  - question: "PHP2Shell 讓哪些網站下線（Website Outage）？"
    answer: "依 2026 年 10 月 21 日前後的報導：荷蘭和芬蘭的政府網站被下線（Newsweek 轉引 Reuters），法國地方政府網站、德國美因茲市官網斷線，Wikimedia 預防性關閉部分系統；日本媒體報導 Pixiv、DMM、niconico 進入緊急維護，日本首相高市早苗在 X 上呼籲網站營運者盡快套用修補。荷蘭 NCSC 建議，無法立刻修補的話，就把對外的 PHP 應用從公網隔離。  ---"
---

一把應該是 384 位元隨機數的私鑰，實際值是 4。

這是印度憑證機構 eMudhra 這週被抓到的事。同一週，PHP 緊急修補了兩個未登入就能拿下伺服器的漏洞，找到漏洞的團隊用的是 GPT-5.6 Sol。

<nav class="post-toc" markdown="1">
**目錄**

* 目錄
{:toc}
</nav>

---

## 30 秒定位

| 項目 | eMudhra 弱私鑰 | PHP2Shell |
|------|----------------|-----------|
| 是什麼 | 8 張中繼憑證的私鑰小到能直接猜 | CVE-2026-109618、CVE-2026-109619，未授權遠端程式碼執行 |
| 誰發現 | 研究者 Wayne，比對 CCADB 時發現 | Calif 用 GPT-5.6 Sol；OpenAI、Wiz 各自獨立回報 |
| 問題存在多久 | 金鑰 2025 年 4 月 30 日產生，約 17 個月 | 同一根因的第一個跡象 2024 年就被看到 |
| 處理速度 | Firefox 不到三小時完成封鎖 | 發布日從 10 月 22 日提前到 10 月 21 日 |
| 修補方式 | 撤銷憑證、移除根憑證 | 升級到 8.5.12、8.4.27、8.3.36、8.2.35 |

---

## 第一件：eMudhra 的私鑰是 4

### 發生了什麼

一把 P-384 私鑰應該是一個隨機的 384 位元數字。eMudhra 這 8 把私鑰，全部小於 256。資安研究者 Scott Helme 從公開憑證裡算出 4、56、115，其他研究者又回報了 66、155、156、230、237。每一把都是不到一秒就能算出來。

持有中繼憑證的私鑰，就能替任何網域簽出瀏覽器會信任的 HTTPS 憑證。eMudhra 自稱簽發過超過 6,000 萬張數位憑證。

### 時間軸

時間為 UTC，來源是 Mozilla Bugzilla 2083449 與 Help Net Security：

- **10 月 17 日**：一位叫 Wayne 的研究者在比對 CCADB（Common CA Database）時發現。他用每一把私鑰簽了一句 "We have a problem here – Wayne"，當作持有私鑰的證明，寄給 Apple、Google、Microsoft、Mozilla 和 eMudhra
- **10 月 17 日 20:06**：Mozilla 收到報告，22:59 完成 Firefox 的 OneCRL 封鎖，不到三小時。中間 21:48 Mozilla 自己也把私鑰算出來了
- **10 月 18 日**：eMudhra 撤銷這 8 張憑證
- **10 月 19 日、20 日**：Apple 10 月 19 日、Microsoft 10 月 20 日跟進
- **10 月 20 日**：Mozilla 和 Chrome 決定把上層的根憑證 emSign ECC Root CA – G3 一起拿掉，eMudhra 停止從這張根憑證簽發

### 原因

eMudhra 在 Bugzilla 上的說明：2025 年 4 月 30 日的金鑰產生儀式（key ceremony），那一批共 24 張中繼憑證。當時為了測試金鑰匯出，流程上核准了一個例外步驟。腳本有 bug，額外產生了第二組很弱的金鑰；兩組金鑰的標籤很像，結果準備憑證時選到弱的那組。

> "There were human errors in multiple steps of the process."
>
> 流程裡好幾個步驟都有人為錯誤。

另外，2025 年 5 月，這 6 張 TLS 中繼憑證發出的 CRL 就已經簽章驗證失敗，當時還開過一張 bug（Bug 1970728）。

eMudhra 說，他們確認其他中繼憑證沒有受影響的方式是：

> "corroborated primarily using mathematical models facilitated by AI"
>
> 主要靠 AI 輔助的數學模型來佐證。

這 17 個月裡有沒有人先算出來用過，目前不知道。

### 影響範圍

- **瀏覽器端**：Mozilla、Chrome、Apple、Microsoft 都已封鎖，更新瀏覽器和作業系統即可
- **非瀏覽器端**：應用程式、伺服器、設備如果沒有收到撤銷更新，可能還在信任這些憑證。Help Net Security 引述 Scott Helme 的建議，是讓管理者更新系統所依賴的憑證清單
- **簽發端**：eMudhra 估計大約 30,000 張客戶憑證要換，其中約 97% 是透過 ACME 自動簽發的

---

## 第二件：PHP2Shell

### 發生了什麼

CVE-2026-109618 和 CVE-2026-109619，合稱 PHP2Shell，官方評分 CVSS 9.2，先外流的 10.0 是錯的。

最嚴重的情境是 Apache + mod_php 的環境，一個未登入的請求在你的程式碼跑之前就能觸發，預設設定下就能做到完整 RCE。PHP-FPM 也確認可以透過應用程式層的路徑做到 RCE。

PHP 大約撐起七成網站（Wiz 的估計），而大約一半的 PHP 網站跑在已經不收修補的舊版本上。WordPress 這類跑在 PHP 上的網站全部在範圍內。

### 誰找到的

- **6 月 22 日**：OpenAI 發布 Patch the Planet 計畫，支援開源維護者
- **7 月 30 日**：Calif 在 Patch the Planet 底下開始審 PHP
- **8 月 11 日**：Calif 回報、同一天 OpenAI 獨立回報同一個根因
- **8 月 24 日**：Wiz 也回報

PHP 基金會的說明也提到，同一個根因的第一個跡象，2024 年就被 PHP 基金會簽約的核心開發者看到了。

OpenAI 的說法：

> "Calif identified a critical flaw using GPT‑5.6 Sol as part of our Patch the Planet initiative"
>
> Calif 在 Patch the Planet 計畫下，用 GPT-5.6 Sol 找到了一個嚴重漏洞。

Wiz 說他們是用自家平台搭配 Gemini 4 Argon 和 GPT-5.6 Sol 獨立找到的（這點目前只有 The Decoder 一個來源）。

### 禁運是怎麼被打破的

依 PHP 基金會的事後說明（時間為 UTC）：

- **10 月 20 日下午**：兩個 CVE 編號先在論壇和社群上流出，附上錯的發布時間和錯的分數，但沒有技術細節
- **10 月 20 日 19:30**：PHP 提前發預告，發布日從 10 月 22 日提前到 10 月 21 日
- **10 月 20 日約 20:00**：Calif 誤發了一支 PoC 影片，示範打穿好幾個目標。細節有限，但影片被轉傳，加速了其他人做 PoC
- **10 月 21 日 07:41**：Chainguard 比協調發布時間早六個多小時，就推出了含修補的映像檔
- **10 月 21 日**：PHP 正式發布修補

PHP 基金會的原話：

> "The coordinated disclosure of these vulnerabilities worked well until 2 days ahead of the targeted release date."
>
> 協調揭露一直很順，直到預定發布日前兩天。

> "Any attacker could now study the fix in binary form while every other PHP user was still waiting for the release."
>
> 攻擊者可以直接拿修補後的 binary 去比對，而其他 PHP 使用者還在等正式版。

發布當下 PHP 安全團隊沒看到能動的 exploit。Cloudflare 則說 10 月 21 日凌晨就開始擋到攻擊流量，而且攻擊者在變形 payload 繞規則。

### 誰下線了

- 荷蘭和芬蘭的政府網站被下線（Newsweek 轉引 Reuters）
- 法國地方政府網站、德國美因茲市官網斷線
- Wikimedia 預防性關掉部分系統
- 日本媒體報導 Pixiv、DMM、niconico 進入緊急維護（二手報導，未查到 pixiv 官方公告）
- 日本首相高市早苗在 X 上呼籲網站營運者盡快套用修補

### 官方建議

- **8.2 以上**：升級到 8.5.12、8.4.27、8.3.36、8.2.35。更新是唯一完整的修補
- **8.1 以前**：8.1 以前已經不在正式支援範圍，7.4、8.0、8.1 只拿到有限的原始碼 backport，要透過發行版、廠商修補版本或升級處理
- **暫時無法修補**：荷蘭 NCSC 的建議是：無法立刻修補，就把對外的 PHP 應用從公網隔離

### PHP 基金會與 OpenAI 的後續說法

PHP 基金會表示，7 月 1 日以來發了 15 個 CVE，另外處理了超過 100 份無效、重複或重現不了的報告。

> "What tools cannot do is decide on the right fix for a long-standing design decision in the engine."
>
> 工具做不到的，是替引擎裡一個存在很久的設計決策，決定正確的修法。

OpenAI 則預告：

> "we expect similar findings to increase sharply in the coming months"
>
> 預期接下來幾個月，類似的發現會急遽增加。

---

## 常見問題 Q&A

**Q: eMudhra 憑證事件是什麼？一般使用者需要做什麼？**

2026 年 10 月，印度憑證機構（Certificate Authority, CA）eMudhra 被發現有 8 張中繼憑證的私鑰全部小於 256，其中一把就是數字 4，任何人都能在不到一秒內從公開憑證算出私鑰，進而偽造任意網站的 HTTPS 憑證。Firefox、Chrome、Apple、Microsoft 在 10 月 17 日到 20 日之間陸續封鎖，Mozilla 和 Chrome 也決定移除上層根憑證 emSign ECC Root CA – G3。一般使用者更新瀏覽器和作業系統即可；需要注意的是伺服器、應用程式和嵌入式設備的信任清單不一定會自動更新，管理者要自行檢查。

**Q: PHP2Shell 是什麼？影響哪些版本？**

PHP2Shell 是 CVE-2026-109618 和 CVE-2026-109619 兩個漏洞的合稱，CVSS 9.2，屬於未授權遠端程式碼執行（Remote Code Execution, RCE）。在 Apache + mod_php 環境下，一個未登入的請求在應用程式碼執行之前就能觸發。修補版本是 PHP 8.5.12、8.4.27、8.3.36、8.2.35，2026 年 10 月 21 日發布。PHP 8.1 以前不在正式支援範圍，7.4、8.0、8.1 只有有限的原始碼 backport，需要透過發行版、廠商或升級來處理。官方表示更新是唯一完整的修補。

**Q: PHP2Shell 是 AI 找到的嗎？**

根據 OpenAI 的說法，資安公司 Calif 在 OpenAI 的 Patch the Planet 計畫下，用 GPT-5.6 Sol 找到了漏洞；OpenAI 同日也獨立回報了同一個根因，Wiz 稍後也獨立回報。PHP 基金會則表示，同一個根因的第一個跡象，2024 年就已經被基金會簽約的核心開發者看到。

**Q: 什麼是協調揭露（Coordinated Disclosure）？PHP2Shell 的禁運是怎麼被打破的？**

協調揭露是指漏洞發現者先私下通報維護者，雙方約定一個日期同時公開漏洞和修補，讓使用者在攻擊者拿到細節前就能更新。PHP2Shell 的禁運在預定發布日前兩天被打破：先是 CVE 編號在社群外流（沒有技術細節），接著 Calif 誤發了一支 PoC 示範影片，最後 Chainguard 比協調時間早六個多小時發布了含修補的映像檔，攻擊者可以直接比對修補後的 binary。PHP 因此把發布日從 10 月 22 日提前到 10 月 21 日。

**Q: PHP2Shell 讓哪些網站下線（Website Outage）？**

依 2026 年 10 月 21 日前後的報導：荷蘭和芬蘭的政府網站被下線（Newsweek 轉引 Reuters），法國地方政府網站、德國美因茲市官網斷線，Wikimedia 預防性關閉部分系統；日本媒體報導 Pixiv、DMM、niconico 進入緊急維護，日本首相高市早苗在 X 上呼籲網站營運者盡快套用修補。荷蘭 NCSC 建議，無法立刻修補的話，就把對外的 PHP 應用從公網隔離。

---

## 資料來源

- [Mozilla Bugzilla 2083449：eMudhra: Private key compromise of Intermediate Certificates](https://bugzilla.mozilla.org/show_bug.cgi?id=2083449)
- [The Register（2026-10-20）：Indian certification authority eMudhra's private keys compromised](https://www.theregister.com/security/2026/10/20/indian-certification-authority-emudhras-private-keys-compromised-one-of-them-was-the-number-4/5304312)
- [Help Net Security（2026-10-21）：eMudhra security blunder left trusted CA signing keys exposed](https://www.helpnetsecurity.com/2026/10/21/emudhra-certificates-private-keys-compromised/)
- [The PHP Foundation（2026-10-21）：Today's PHP Security Release, and How We're Strengthening PHP Security](https://thephp.foundation/blog/2026/10/21/todays-php-security-release-and-how-were-strengthening-php-security/)
- [OpenAI：Patch the Planet: global response coordination as agents uncover critical vulnerabilities](https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/)
- [PPC Land：OpenAI says GPT-5.6 Sol found a PHP flaw before attackers did](https://ppc.land/openai-says-gpt-5-6-sol-found-a-php-flaw-before-attackers-did/)
- [The Decoder：OpenAI's GPT-5.6 Sol and Google's Gemini 4 Argon found critical PHP flaw](https://the-decoder.com/openais-gpt-5-6-sol-and-gemini-4-argon-discovered-the-critical-php-vulnerability-affecting-millions-of-websites/)
- [Qualys：PHP2Shell: PHP Patches Two Critical RCE Vulnerabilities](https://blog.qualys.com/vulnerabilities-threat-research/2026/10/20/php-announces-critical-security-release-for-two-vulnerabilities)
- [The Record：Hundreds of websites taken offline as concern grows over two PHP vulnerabilities](https://therecord.media/php-script-vulnerabilities-warnings)
- [Newsweek：PHP Vulnerability: List of Websites Powered by PHP as Hacker Threat Prompts Scramble](https://www.newsweek.com/php-vunerability-php2shell-issue-websites-hack-server-12601225)
- [PBX Science：Why Japan's Prime Minister Urged Everyone to Patch PHP](https://pbxscience.com/why-japans-prime-minister-urged-everyone-to-patch-php-tonight-inside-the-php2shell-emergency/)
