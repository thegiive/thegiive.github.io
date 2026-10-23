---
layout: post
title: "同一週，七個主流語言與執行環境都出了安全修補：Linux、Node.js、Python、Go、Rust、Java、PHP"
date: 2026-10-23 09:00:00 +0800
permalink: /linux-zdi-lkml-language-platform-security-week/
tags: [Linux kernel, Node.js, Python, Go, Rust, Java, PHP, Oracle CPU, LiteLLM, GitLab, Chrome, Plex2Shell, Cisco, Railway, eMudhra, 安全更新, security release, 供應鏈攻擊, supply chain attack]
categories: [AI 資安]
image: /assets/images/linux-zdi-lkml-language-platform-security-week-cover.png
description: "10 月 19 日到 22 日，Linux kernel、Node.js、Python、Go、Rust、Java、PHP 七個主流語言與執行環境都出了安全修補或漏洞報告，另外還有 LiteLLM、GitLab、Chrome、Plex、Cisco、Railway 六個套件和平台。最高分是 GitLab 的 CVSS 10.0，Node.js 一次修 10 個 CVE，Oracle 這次 Java SE 修了 55 個，Python、Go、Rust、Node.js 同時處理 eMudhra 中繼憑證外洩。這篇逐項整理：是什麼漏洞、多嚴重、哪個版本修好、該怎麼做，最後列出這週查過但沒有重大公告的語言。"
author: Wisely Chen
faq:
  - question: "2026 年 10 月 19 日到 22 日，哪些程式語言有安全更新（Security Release）？"
    answer: "Linux kernel、Node.js、Python、Go、Rust、Java、PHP 七個主流語言與執行環境都有。Node.js 發布 v26.12.1、v24.22.1、v22.23.4，修 10 個 CVE；Python 發布 3.15.1、3.14.9、3.13.17；Go 發布 1.27.3、1.26.10；Rust 的 rustls-webpki 修在 0.103.16 以上；Oracle 的 Critical Patch Update 有 55 個 Java SE 修補；PHP 發布 8.5.12、8.4.27、8.3.36、8.2.35 修補 PHP2Shell；Linux kernel 有 6 份漏洞報告出現在公開郵件論壇，CVSS 最高 9.0，查不到包含修補的正式版本。Ruby、.NET、Spring、OpenSSL、glibc 這幾天沒有新的安全公告。"
  - question: "Node.js 2026 年 10 月安全更新要升到哪個版本？"
    answer: "Node.js 在 2026 年 10 月 21 日發布 v26.12.1、v24.22.1、v22.23.4，修 10 個 CVE（4 個 High、3 個 Medium、3 個 Low），包括 Brotli 解碼器越界寫入可遠端執行程式碼的 CVE-2026-111497，以及兩個 TLS 憑證主機名驗證繞過。這次也更新了內建 CA 憑證，處理 eMudhra 中繼憑證外洩。v20 已經停止支援，沒有修補。"
  - question: "LiteLLM 1.107.0 供應鏈攻擊（Supply Chain Attack）影響誰？該怎麼處理？"
    answer: "2026 年 10 月 21 日，PyPI 上 litellm 1.107.0 的七個 wheel（11:39 到 13:23 UTC），以及 Docker Hub、GHCR 的 v1.107.0、latest、main-latest、main-stable 四個 tag 被換成惡意版本，會偷憑證並載入遠端執行工具，只要在受影響環境啟動 Python 就會執行。官方建議固定在 1.106.2，重建映像與虛擬環境，並輪換 IAM role、模型供應商金鑰和資料庫密碼。GitHub 上的 v1.107.0 原始碼 tag 和企業私有版不受影響。"
  - question: "eMudhra 憑證事件為什麼讓 Python、Go、Rust 都發更新？"
    answer: "eMudhra 有 8 張中繼憑證的私鑰可以直接從公開憑證算出來。瀏覽器已經封鎖，但不走系統信任清單的程式可能還會信任這些憑證。所以 Python 在 2026 年 10 月 21 日發布 3.15.1、3.14.9、3.13.17，內附的 pip 帶上移除 emSign 根憑證的 certifi 2026.10.19；Go 在 10 月 19 日發布 1.27.3、1.26.10，在 crypto/x509 加入黑名單（CVE-2026-111943）；Rust 的 rustls-webpki 0.103.16 以上做了同樣處理；Node.js 也更新了內建 CA 憑證。"
  - question: "這週分數最高的漏洞是哪幾個？"
    answer: "GitLab 的 CVE-2026-110264 是 CVSS 10.0，編譯特製的正規表達式時整數溢位，未登入就能在伺服器上執行程式碼，修補版本包括 19.5.1、18.11.13 等七個；LiteLLM 的 CVE-2026-114612 是 9.9；Rust 生態的 wasmtime 有兩個 9.9 的 sandbox 逃脫；Cisco Expressway 的 CVE-2026-76466 和 Unified Communications 的 Hardening Release 是 9.8；PHP2Shell 是 9.2；Linux kernel 兩個 KSMBD 遠端程式碼執行是 9.0。另外 Plex2Shell 單一 CVE 分數不高（4.3 到 7.2），但已被大範圍利用，CISA 已列入已知被利用漏洞目錄（KEV）。  ---"
---

10 月 19 日到 22 日，Linux kernel、Node.js、Python、Go、Rust、Java、PHP 都出了安全修補或漏洞報告。

再加上 LiteLLM、GitLab、Chrome、Plex、Cisco、Railway 六個套件和平台。這篇按平台整理：是什麼漏洞、多嚴重、哪個版本修好、該怎麼做。

<nav class="post-toc" markdown="1">
**目錄**

* 目錄
{:toc}
</nav>

---

## 30 秒總表

日期以各官方公告標示的日期為準，沒有換算時區。

**語言與執行環境**

| 平台 | 漏洞 | 嚴重度 | 日期 | 修補／處置 |
|------|------|--------|------|------|
| Linux kernel | KSMBD 兩個遠端程式碼執行等 6 份漏洞報告 | 最高 CVSS 9.0 | 10/21–10/22 | 尚無正式版，部分修補在維護者的樹裡 |
| Node.js | 10 個 CVE，含 Brotli 越界寫入 RCE | 最高 High | 10/21 | v26.12.1、v24.22.1、v22.23.4 |
| Python | certifi 移除 emSign 根憑證＋tarfile CVE-2026-114583 | Medium | 10/21、10/22 | 3.15.1、3.14.9、3.13.17（tarfile 修補尚無正式版） |
| Go | CVE-2026-111943，封鎖 eMudhra 中繼憑證 | 未評分 | 10/19 | 1.27.3、1.26.10 |
| Rust | rustls-webpki 等三筆 RustSec；wasmtime sandbox 逃脫 | wasmtime 9.9 | 10/19–10/20 | rustls-webpki 0.103.16 以上 |
| Java | Oracle CPU：Java SE 55 個修補；Tomcat 7 個 CVE | 最高 7.5 | 10/20 | 依 Oracle CPU；Tomcat 11.0.27 等 |
| PHP | PHP2Shell | 9.2 | 10/21 | 8.5.12、8.4.27、8.3.36、8.2.35 |

**套件與平台**

| 平台 | 漏洞／事件 | 嚴重度 | 日期 | 修補／處置 |
|------|------|--------|------|------|
| LiteLLM | 1.107.0 在 PyPI、Docker Hub 被投毒 | 投毒事件 | 10/21 | 固定 1.106.2，輪換金鑰 |
| GitLab | CVE-2026-110264 等 12 個問題 | 10.0 | 10/21 | 19.5.1 等七個版本 |
| Chrome | 353 個安全修補 | 6 個 Critical | 10/20 | 156.0.8078.47 |
| Plex | Plex2Shell，四個 CVE 串成攻擊鏈，已被利用 | 單一 4.3–7.2 | 10/16 公開，10/20 列入 KEV | 1.43.3.10861 以後 |
| Cisco | 14 份公告、34 個 CVE | 最高 9.8 | 10/21–10/22 | Expressway X15.5.20；UC 15SU5 |
| Railway | 環境變數外洩 | 平台資安事件 | 10/21 | 輪換所有環境變數 |

Python、Go、Rust、Node.js 的修補裡，都有一部分是在處理 eMudhra 中繼憑證外洩（細節見[前一篇](/emudhra-weak-key-php2shell-same-week/)）。瀏覽器已經封鎖，但有些程式不走系統信任清單，要靠語言自己的更新。

---

## 七個語言與執行環境

### Linux kernel

Trend Micro 的 Zero Day Initiative（ZDI）10 月 21、22 日把 6 份漏洞報告寄到公開的 kernel 郵件論壇（LKML），沒有附修補，CVSS 最高 9.0。

- **ZDI-CAN-33549**：KSMBD 的 SMB Direct 整數下溢，可遠端執行程式碼，CVSS 9.0
- **ZDI-CAN-33774**：KSMBD 協定分派的競爭條件，可遠端執行程式碼，CVSS 9.0
- **ZDI-CAN-33367**：網路層 skb_zerocopy，本地提權，CVSS 7.8
- **ZDI-CAN-34068**：VMware 顯示驅動 vmwgfx 越界寫入，本地提權
- **ZDI-CAN-34076**：NVMe over Fabrics target（nvmet）的 Get Log Page 使用未初始化資源，資訊洩漏
- **ZDI-CAN-32005**：search-domain TCP 查詢的堆疊緩衝區溢位，本地提權。元件和分數查不到原始郵件

修補狀態：KSMBD 維護者 Namjae Jeon 回覆 33774 的修補已經在他的樹裡；Samba 開發者 Stefan Metzmacher 回覆說，他給 7.5 準備的分支裡應該已經修好 33549；33367 維護者一週前已經從另一個來源收到附修補的報告。目前主線是 10 月 18 日發布的 7.3，查不到包含這些修補的正式版本。

### Node.js

10 月 21 日發布 v26.12.1、v24.22.1、v22.23.4，修 10 個 CVE，4 個 High、3 個 Medium、3 個 Low。

- **CVE-2026-111497**：Brotli 解碼器越界寫入，可遠端執行程式碼，三個分支都受影響。致謝寫的是 OpenAI Codex Security
- **CVE-2026-105483**：IP 用全形數字寫時，可以繞過 TLS 憑證主機名驗證
- **CVE-2026-106069**：主機名能被寬鬆解析成 IP 時，可以繞過 TLS 憑證主機名驗證
- **CVE-2026-105482**：dns.resolve 遇到 NUL 字元會截斷名稱

這次同時更新內建 CA 憑證，處理 eMudhra 中繼憑證外洩。

**怎麼做**：升到上面三個版本。v20 已經停止支援，這次沒有修補。

### Python

10 月 21 日發布 3.15.1、3.14.9、3.13.17 三個緊急安全版本（expedited security release）。內容是把內附的 pip 升到 26.2.2，帶 certifi 2026.10.19，回應 eMudhra / emSign 憑證事件。certifi 2026.10.19 把 emSign 根憑證移除（GHSA-6q48-6c7w-9gw2）。

10 月 22 日另公告 CVE-2026-114583（Medium）：tarfile 的 tar filter 可被特製的 link 繞過，寫到目標目錄外。

**怎麼做**：升級 Python，或直接把 certifi 升到 2026.10.19 並重建容器映像（"Upgrade to certifi 2026.10.19 and rebuild container images"）。tarfile 的修補已合併，還沒有包含它的正式版本。

### Go

10 月 19 日發布 1.27.3 和 1.26.10。

CVE-2026-111943：crypto/x509 加入一份黑名單，Verify 碰到這些中繼憑證直接回錯誤。受影響的是 1.26.10 以前，以及 1.27.0 到 1.27.3 以前。CVE 紀錄沒有分數。Go 的公告沒寫是哪一家 CA，issue 裡社群比對出來是 eMudhra。

**怎麼做**：升到 1.27.3 或 1.26.10。

### Rust

RustSec 10 月 20 日發了三筆，處理同一件 eMudhra 事件：RUSTSEC-2026-0382（rustls-webpki，修在 0.103.16 以上，別名同一個 CVE-2026-111943）、RUSTSEC-2026-0381（webpki-roots）、RUSTSEC-2026-0383（webpki-root-certs）。

另外，wasmtime 10 月 19 日發了兩個 CVSS 9.9 的 sandbox 逃脫公告。

**怎麼做**：rustls-webpki 升到 0.103.16 以上，webpki-roots、webpki-root-certs 跟著更新；wasmtime 升到 v36.0.19、v48.0.7 或 v49.0.4。

### Java

Oracle 10 月 20 日發布 Critical Patch Update。Java SE 55 個修補，其中 49 個不需要帳密就能從網路利用。Java SE 這批最高 7.5。Oracle 全產品這次共 1295 個修補。

Tomcat 10 月 20 日公開 7 個 CVE，3 個 Important、4 個 Low，Tomcat 不給 CVSS 分數。其中 JNDIRealm 在某些設定下不用正確密碼就能登入（CVE-2026-101296），另外兩個 Important 是 AJP 和 HTTP/2 async 的請求回應錯置。

**怎麼做**：Java SE 依 Oracle CPU 升級；Tomcat 升到 11.0.27、10.1.61 或 9.0.123。

### PHP

PHP2Shell：CVE-2026-109618、CVE-2026-109619，CVSS 9.2，未登入就能遠端執行程式碼，10 月 21 日修補。

**怎麼做**：升到 8.5.12、8.4.27、8.3.36、8.2.35。8.1 以前不在正式支援範圍，要靠發行版或廠商的修補，或直接升級。詳見[前一篇](/emudhra-weak-key-php2shell-same-week/)。

---

## 套件與平台

### LiteLLM：1.107.0 被投毒

依 LiteLLM 官方事件說明（時間為 UTC）：

- **PyPI**：litellm 1.107.0 的七個 wheel，10 月 21 日 11:39 到 13:23
- **Docker Hub**：v1.107.0、latest、main-latest、main-stable 四個 tag，11:46 到 14:20
- **GHCR**：同樣四個 tag，到 13:51 下架

惡意版本會偷憑證，並載入遠端執行程式碼的工具。它放進 cook.pth 和 sitecustomize.py，受影響環境裡只要啟動 Python 就會執行。pypistats 顯示上週下載約 2,278 萬次。GitHub 上 v1.107.0 的原始碼 tag 是乾淨的，企業私有版不受影響。

入侵方式，官方說是攻擊者拿到 GitHub CLI 憑證、改了發布流程；憑證的來源，官方提到特定情況下 Claude Code 會把使用者的 GitHub CLI OAuth token 放進回應內容，回應被記錄下來時 token 可能出現在 LiteLLM 的 log 裡。

**怎麼做**：

- 固定在 1.106.2，或事件前發布的明確版本
- 不要在受影響環境先跑 pip install；刪掉惡意檔案，最好重建映像和虛擬環境
- 輪換 IAM role、所有模型供應商金鑰、LiteLLM proxy 資料庫裡的 master/virtual key、DATABASE_URL 密碼

另一個 CVE-2026-114612（CVSS 9.9）在 10 月 22 日公開 CVE 記錄：已登入的內部使用者可以偽造管理員憑證，再透過 MCP stdio 執行任意指令，修補版本是 1.100.4、1.101.3、1.102.2、1.103.1。

### GitLab：CVSS 10.0

10 月 21 日發布 19.5.1、19.4.3、19.3.6、19.2.9、19.1.9、19.0.10、18.11.13（CE/EE），12 個安全修補：1 個 Critical、2 個 High、5 個 Medium、4 個 Low。

CVE-2026-110264，CVSS 10.0：編譯特製的正規表達式時整數溢位，未登入就能在 GitLab 伺服器上執行程式碼。影響 7.0 以後所有版本。公告沒有說已被利用。

**怎麼做**：自架的升到上面對應分支的版本；GitLab 另外附了兩個偵測規則。

### Chrome 156：353 個安全修補

10 月 20 日推出 156.0.8078.47（Linux）、156.0.8078.47/.48（Windows/Mac）。353 個安全修補：6 個 Critical、61 個 High、197 個 Medium、89 個 Low。公告沒有提到在野利用。

致謝欄裡，"Xinyang Ge (Anthropic), assisted by Claude" 有 5 條，"OpenAI Codex Security" 有 4 條，兩邊各有 1 個 Critical。

**怎麼做**：更新到 156.0.8078.47（Windows/Mac 為 .47/.48）以上。

### Plex：Plex2Shell，已被利用

研究者 Zach Main 10 月 16 日公開 Plex2Shell：四個 CVE 單看分數是 4.3 到 7.2，串起來可以在未登入的情況下拿到遠端執行。他說四個部分都大量用了 LLM。

Plex 的公告 9 月 1 日發出，10 月 19 日更新：

> "These vulnerabilities are being actively and widely exploited."
>
> 這些漏洞正被大範圍地實際利用。

CISA 10 月 20 日把四個 CVE 列入已知被利用漏洞目錄（KEV），CVE-2026-96654、CVE-2026-96656 的修補期限是 10 月 23 日，另外兩個是 11 月 3 日。

**怎麼做**：Plex Media Server 升到 1.43.3.10861 以後。

### Cisco：14 份公告、34 個 CVE

10 月 21、22 日共 14 份公告、34 個 CVE。最高 9.8 有兩份：

- **Expressway 遠端程式碼執行（CVE-2026-76466）**：有做 cluster 且開啟 TLS Verify Mode 時，未登入的遠端攻擊者能以 root 執行指令。修補版本 X15.5.20，Cisco PSIRT 表示沒發現惡意利用
- **Unified Communications Security Hardening Release**：8 個 CVE，影響 Unified CM 等產品，修補版本 15SU5。Cisco 說這批是內部測試加上前沿 AI 模型找到的

### Railway：環境變數外洩

雲端部署平台 Railway 10 月 21 日發布資安說明：未經授權的第三方可能存取了加密的環境變數，其中一部分拿到了解密後的內容。Railway 說影響可能只限部分使用者，沒有公布數字，受影響客戶會收到 email。根本原因還沒公布。

**怎麼做**：

> "immediately roll all environment variables, including any API keys, stored in Railway"
>
> 立刻輪換所有存在 Railway 的環境變數，包括 API key。

私有 registry 的憑證也要換，並檢查相關服務的 log 有沒有異常使用。

---

## 這週沒有重大公告的

- **Ruby**：10 月 22 日的 4.0.8 是一般 bugfix 版本，Rails 這週沒有安全公告
- **.NET**：大批修補在 10 月 13 日的 Patch Tuesday，在這週之前；之後沒有額外修補
- **Spring、OpenSSL、glibc**：這週都沒有新公告

---

## 常見問題 Q&A

**Q: 2026 年 10 月 19 日到 22 日，哪些程式語言有安全更新（Security Release）？**

Linux kernel、Node.js、Python、Go、Rust、Java、PHP 七個主流語言與執行環境都有。Node.js 發布 v26.12.1、v24.22.1、v22.23.4，修 10 個 CVE；Python 發布 3.15.1、3.14.9、3.13.17；Go 發布 1.27.3、1.26.10；Rust 的 rustls-webpki 修在 0.103.16 以上；Oracle 的 Critical Patch Update 有 55 個 Java SE 修補；PHP 發布 8.5.12、8.4.27、8.3.36、8.2.35 修補 PHP2Shell；Linux kernel 有 6 份漏洞報告出現在公開郵件論壇，CVSS 最高 9.0，查不到包含修補的正式版本。Ruby、.NET、Spring、OpenSSL、glibc 這幾天沒有新的安全公告。

**Q: Node.js 2026 年 10 月安全更新要升到哪個版本？**

Node.js 在 2026 年 10 月 21 日發布 v26.12.1、v24.22.1、v22.23.4，修 10 個 CVE（4 個 High、3 個 Medium、3 個 Low），包括 Brotli 解碼器越界寫入可遠端執行程式碼的 CVE-2026-111497，以及兩個 TLS 憑證主機名驗證繞過。這次也更新了內建 CA 憑證，處理 eMudhra 中繼憑證外洩。v20 已經停止支援，沒有修補。

**Q: LiteLLM 1.107.0 供應鏈攻擊（Supply Chain Attack）影響誰？該怎麼處理？**

2026 年 10 月 21 日，PyPI 上 litellm 1.107.0 的七個 wheel（11:39 到 13:23 UTC），以及 Docker Hub、GHCR 的 v1.107.0、latest、main-latest、main-stable 四個 tag 被換成惡意版本，會偷憑證並載入遠端執行工具，只要在受影響環境啟動 Python 就會執行。官方建議固定在 1.106.2，重建映像與虛擬環境，並輪換 IAM role、模型供應商金鑰和資料庫密碼。GitHub 上的 v1.107.0 原始碼 tag 和企業私有版不受影響。

**Q: eMudhra 憑證事件為什麼讓 Python、Go、Rust 都發更新？**

eMudhra 有 8 張中繼憑證的私鑰可以直接從公開憑證算出來。瀏覽器已經封鎖，但不走系統信任清單的程式可能還會信任這些憑證。所以 Python 在 2026 年 10 月 21 日發布 3.15.1、3.14.9、3.13.17，內附的 pip 帶上移除 emSign 根憑證的 certifi 2026.10.19；Go 在 10 月 19 日發布 1.27.3、1.26.10，在 crypto/x509 加入黑名單（CVE-2026-111943）；Rust 的 rustls-webpki 0.103.16 以上做了同樣處理；Node.js 也更新了內建 CA 憑證。

**Q: 這週分數最高的漏洞是哪幾個？**

GitLab 的 CVE-2026-110264 是 CVSS 10.0，編譯特製的正規表達式時整數溢位，未登入就能在伺服器上執行程式碼，修補版本包括 19.5.1、18.11.13 等七個；LiteLLM 的 CVE-2026-114612 是 9.9；Rust 生態的 wasmtime 有兩個 9.9 的 sandbox 逃脫；Cisco Expressway 的 CVE-2026-76466 和 Unified Communications 的 Hardening Release 是 9.8；PHP2Shell 是 9.2；Linux kernel 兩個 KSMBD 遠端程式碼執行是 9.0。另外 Plex2Shell 單一 CVE 分數不高（4.3 到 7.2），但已被大範圍利用，CISA 已列入已知被利用漏洞目錄（KEV）。

---

## 資料來源

- [Phoronix（2026-10-22）：Several Linux Kernel Vulnerabilities Accidentally Posted To Public Kernel Mailing List](https://www.phoronix.com/news/LKML-New-Trend-Vulnerabilities)
- [LKML：ZDI-CAN-33549 報告](https://lkml.iu.edu/hypermail/linux/kernel/2610.2/14779.html)
- [LKML：ZDI-CAN-33774 報告](https://lkml.iu.edu/hypermail/linux/kernel/2610.2/14807.html)
- [LKML：ZDI-CAN-33367 報告](https://lkml.iu.edu/hypermail/linux/kernel/2610.2/14824.html)
- [Node.js：October 2026 Security Releases](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases)
- [Python 3.14.9](https://www.python.org/downloads/release/python-3149/)
- [Python security-announce：CVE-2026-114583](https://mail.python.org/archives/list/security-announce@python.org/thread/43JOWPRAV5DI3VZ4FUEUAZOHCATXXOCK/)
- [CVE-2026-111943](https://www.cve.org/CVERecord?id=CVE-2026-111943)
- [golang/go issue 82345](https://github.com/golang/go/issues/82345)
- [RustSec：RUSTSEC-2026-0382](https://rustsec.org/advisories/RUSTSEC-2026-0382.html)
- [wasmtime GHSA-897f-g5gm-fmxm](https://github.com/bytecodealliance/wasmtime/security/advisories/GHSA-897f-g5gm-fmxm)
- [Oracle Critical Patch Update - October 2026](https://www.oracle.com/security-alerts/cpuoct2026.html)
- [Apache Tomcat 11 Security](https://tomcat.apache.org/security-11.html)
- [LiteLLM：Security Incident October 21, 2026](https://docs.litellm.ai/blog/security-incident-oct-21-2026)
- [LiteLLM GHSA-7hp6-4w63-5g45](https://github.com/BerriAI/litellm/security/advisories/GHSA-7hp6-4w63-5g45)
- [GitLab Patch Release 19.5.1](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/)
- [Chrome Releases：Stable Channel Update for Desktop（2026-10-20）](https://chromereleases.googleblog.com/2026/10/stable-channel-update-for-desktop_02018666648.html)
- [Zach Main：Plex2Shell](https://zmain.info/blog/plex2shell)
- [Plex：Important Security Update for Plex Media Server v1.43.2 and earlier](https://forums.plex.tv/t/important-security-update-for-plex-media-server-v1-43-2-and-earlier/942319)
- [Cisco：Unified Communications Products Security Hardening Release October 2026](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-voice-hardening-twgbH9e3)
- [Cisco：Expressway Series Remote Code Execution Vulnerability](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-vcs-static-cred-hr7EWZ8t)
- [Railway：Security Disclosure, Wednesday October 21st](https://blog.railway.com/p/security-disclosure-wednesday-october-21st)
