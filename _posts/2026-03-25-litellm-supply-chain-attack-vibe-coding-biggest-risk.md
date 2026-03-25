---
layout: post
title: "Vibe Coding 最大的風險不是 AI 寫爛 Code，而是你根本不知道它幫你裝了什麼"
date: 2026-03-25 10:00:00 +0800
permalink: /litellm-supply-chain-attack-vibe-coding-biggest-risk/
image: /assets/images/litellm-supply-chain-karpathy-tweet.png
description: "Andrej Karpathy 說：「Supply chain attacks like this are basically the scariest thing imaginable in modern software.」LiteLLM 被投毒，每月 9700 萬次下載的 AI 核心套件，惡意版本竊取開發者的 SSH keys、雲端憑證、資料庫密碼。發現者是一個在 Cursor 裡用 MCP plugin 的開發者 — 機器跑到沒記憶體才發現不對。當 Vibe Coding 讓開發者越來越信任自動安裝，供應鏈攻擊的爆炸半徑被指數級放大。"
tags: ["AI Security", "Supply Chain Attack", "LiteLLM", "Vibe Coding", "Harness Engineering", "MCP"]
categories: ["AI 資訊安全"]
---

# Vibe Coding 最大的風險不是 AI 寫爛 Code，而是你根本不知道它幫你裝了什麼

## Karpathy 說：這是現代軟體最可怕的事

今天早上 Andrej Karpathy 在 X 上發了一則貼文，標題直接就是「Software horror: litellm PyPI supply chain attack」。

Karpathy 是誰不用多介紹 — 前 Tesla AI 總監、OpenAI 創始成員。當這個等級的人用「horror」來形容一個事件的時候，你知道事情不小。

![Andrej Karpathy 推文：LiteLLM 供應鏈攻擊是現代軟體最恐怖的事](/assets/images/litellm-supply-chain-karpathy-tweet.png)

他的原話：

> 「Simple 'pip install litellm' was enough to exfiltrate SSH keys, AWS/GCP/Azure creds, Kubernetes configs, git credentials, env vars (all your API keys), shell history, crypto wallets, SSL private keys, CI/CD secrets, database passwords.」

> 「Supply chain attacks like this are basically the scariest thing imaginable in modern software. Every time you install any dependency you could be pulling in a poisoned package anywhere deep inside its entire dependency tree.」

但最讓我注意的是 Karpathy 講的兩件事：

**第一，這次攻擊是怎麼被發現的。** 一個叫 Callum McMahon 的開發者，在 Cursor 裡面用了一個 MCP plugin，這個 plugin 把 LiteLLM 當作 transitive dependency 拉進來。安裝了惡意版本 1.82.8 之後，他的機器直接 RAM 爆掉、當機了。就是因為攻擊者的惡意代碼寫得太粗糙，才被發現。Karpathy 說得很直白：**「So if the attacker didn't vibe code this attack it could have been undetected for many days or weeks.」**

諷刺嗎？攻擊者如果寫得更好一點，我們可能到現在都還不知道自己中招了。

**第二，Karpathy 自己的態度。** 他說他一直以來都對用 LLM 來 "yoink" 功能（就是隨手拉依賴進來用）保持非常警戒的態度，寧可自己實作簡單的功能。這從 AI 領域最頂尖的人嘴裡說出來，值得所有 Vibe Coding 開發者好好想想。

---

## 兩個第一手受災案例

Karpathy 講的是全局觀，但真正讓人有感的是實際受災的開發者。

### 案例一：Cursor + MCP Plugin 觸發

Callum McMahon — 就是 Karpathy 提到的那位。他在 Cursor 裡用了一個 MCP plugin，這個 plugin 的依賴鏈裡有 LiteLLM。安裝的時候 pip 自動拉了最新版 1.82.8，裡面的 `.pth` 文件在 Python 啟動時自動執行惡意代碼，瘋狂佔用記憶體直到當機。

如果攻擊者的代碼寫得更優雅一點 — 安靜地竊取憑證、不佔用額外資源 — 他可能永遠不會發現。

### 案例二：Browser-Use + Claude MCP 自動載入

推特用戶实践哥MinLi（@MinLiBuilds）也遇到了類似的情況：

> 「昨天裝了 browser-use，上午裝的，一打開就有無數 python 進程啟動電腦卡死。claude 一啟動就自動加載 mcp 就會啟動無限個 python。」

![实践哥MinLi 推特截圖：browser-use 安裝後觸發 LiteLLM 惡意版本](/assets/images/litellm-supply-chain-minli-tweet.png)

他後來去看了 browser-use 的源碼，發現他們用了 `litellm>=1.82.2`。browser-use 官方後來緊急修復，在 GitHub commit 中把版本鎖定為 `litellm==1.82.2`。

兩個案例的共同點：**開發者完全沒有主動安裝 LiteLLM**。一個是 MCP plugin 的 transitive dependency，一個是 browser-use 的子依賴。他們只是在用自己的 AI 工具，然後就中招了。

---

## 攻擊鏈拆解：三層供應鏈投毒

這次 LiteLLM 事件的攻擊者是一個叫 TeamPCP 的組織，他們的攻擊手法精密到讓人後背發涼。不是直接破解 LiteLLM 的帳號密碼，而是用了三層供應鏈跳板：

### 第一層：毒化安全掃描器

3 月 19 日，Aqua Security 的 Trivy 漏洞掃描器被入侵。對，你沒看錯 — 他們先毒化的是一個**安全工具**。就像你為了防盜裝了監視器，結果小偷先把監視器換成假的。

### 第二層：竊取發佈權限

LiteLLM 的 CI/CD pipeline 裡用了未鎖定版本的 Trivy 來做安全掃描。被毒化的 Trivy 在執行時偷偷把 `PYPI_PUBLISH` token 傳出去了。攻擊者拿到了這個 token，就等於拿到了在 PyPI 上以 LiteLLM 官方名義發佈套件的權限。

### 第三層：發佈惡意版本

3 月 24 日，兩個惡意版本上線：

- **1.82.7**（10:39 UTC）：在 `litellm/proxy/proxy_server.py` 裡嵌入 Base64 編碼的惡意代碼，import 時執行
- **1.82.8**（10:52 UTC）：更狠 — 部署了一個 `.pth` 文件，這意味著**每次 Python 啟動時都會自動執行惡意代碼**，不管你有沒有 import LiteLLM

惡意代碼會掃描你機器上的：
- SSH keys
- AWS / GCP / Azure / Kubernetes 憑證
- 所有環境變數（包含各種 API keys）
- 資料庫密碼
- 加密貨幣錢包
- SSL/TLS 私鑰
- Shell 歷史記錄
- CI/CD 設定檔
- Git 憑證

全部打包，AES-256-CBC + RSA-4096 加密，然後 POST 到 `models.litellm.cloud` — 一個攻擊者控制的域名，名字故意取得跟 LiteLLM 官方很像。

Karpathy 在推文裡特別提到一個細節：惡意版本存活時間可能不到 1 小時。但 LiteLLM 每月有 9700 萬次下載，而且更可怕的是**傳染性** — 任何依賴 LiteLLM 的套件都會受影響。他舉的例子是 DSPy：如果你 `pip install dspy`（它依賴 `litellm>=1.64.0`），你也會被 pwned。Browser-Use、CrewAI，基本上你能想到的主流 AI Agent 框架都在射程範圍內。

---

## Vibe Coding 為什麼讓這件事變得更危險

坦白說，供應鏈投毒不是新鮮事。npm、PyPI 每個月都有惡意套件被發現。但 Vibe Coding 時代的供應鏈攻擊，有幾個讓爆炸半徑指數級放大的因素：

### 1. AI 自動安裝，人類零審查

傳統開發流程裡，你至少會看一眼 `requirements.txt` 或 `package.json`，大概知道自己裝了什麼。但在 Vibe Coding 的場景裡：

- Claude Code / Cursor 自動生成程式碼，自動加入依賴
- MCP Server 自動載入，自動安裝需要的套件
- Agent 框架自動拉取子依賴

你可能只是說了一句「幫我加一個瀏覽器自動化功能」，背後就觸發了一連串的 `pip install`，每一個都可能拉到被投毒的版本。

### 2. `>=` 依賴的致命陷阱

Karpathy 說得很好：「Every time you install any dependency you could be pulling in a poisoned package anywhere deep inside its entire dependency tree. This is especially risky with large projects that might have lots and lots of dependencies.」

browser-use 用的是 `litellm>=1.82.2`，DSPy 用的是 `litellm>=1.64.0`。這在開源社群裡非常常見 — 「只要比這個版本新就好」。在正常情況下這沒問題，但在供應鏈攻擊的情境下，這等於是幫攻擊者打開了一道門：只要發佈一個版本號更高的惡意版本，所有使用 `>=` 的下游專案都會自動中招。

修復方式很簡單：改成 `litellm==1.82.2`，鎖死版本。但這就是事後諸葛了 — 在出事之前，有多少專案會主動鎖版本？

而且 Karpathy 點出了一個更深層的問題：被偷走的憑證可以被用來**入侵更多帳號、投毒更多套件**。這是一個正反饋循環 — 每一次成功的攻擊都讓下一次攻擊更容易。

### 3. Slopsquatting：LLM 幻覺創造的新攻擊面

這是 2025-2026 年出現的全新攻擊向量。LLM 在生成程式碼時，有時候會「幻覺」出不存在的套件名稱 — 名字聽起來很合理，但 PyPI 或 npm 上根本沒有這個套件。

攻擊者發現這個規律後，開始**預先註冊這些 LLM 可能會幻覺出來的套件名**，然後在裡面植入惡意代碼。所以當開發者讓 AI 寫程式碼、AI 建議安裝一個不存在的套件、開發者沒有驗證就直接 `pip install` — 中招。

這就是 Slopsquatting。它利用的不是人類的粗心，而是 **AI 的幻覺 + 人類對 AI 的信任**。

---

## 更大的圖景：AI Coding 的系統性風險

LiteLLM 事件不是孤例。往前看幾個月，整個 AI 開發生態系統正在成為攻擊者的重點目標：

**s1ngularity 活動（2025 年 8-11 月）：** 攻擊者入侵了 Nx 的 npm 套件，竊取了 1,079 個開發者系統上的 2,349 個憑證。特別值得注意的是，他們**專門鎖定 AI LLM 客戶端的憑證** — Claude API key、Gemini API key、Amazon Q API key。為什麼？因為這些 API key 背後連接的是有高權限的 AI Agent，拿到 key 等於拿到了 Agent 能做的所有事情。

**Lazarus 組織（2026 年 2 月）：** 北韓關聯的駭客組織在 npm 上發佈了超過 230 個惡意套件，透過假的加密貨幣工作機會來散布。

**Amazon 內部事故趨勢：** 根據 Financial Times 的報導，Amazon 的電商業務召集了大量工程師開「深度檢討」會議，因為近月來出現了「一連串的事故趨勢」，其中一個 contributing factor 就是「GenAI assisted changes」的使用。報告用了一個詞：「high blast radius」（高爆炸半徑）。

![Amazon AI Coding 事故報導](/assets/images/litellm-supply-chain-amazon-ai-outage.jpeg)

當連 Amazon 這種等級的公司都因為 AI Coding 導致 production outage 趨勢上升，我們這些中小團隊該怎麼想？

---

## 坦白說：我自己也差點中招

講到這裡，我必須坦白一件事。

我自己在用 Claude Code 的時候，也是習慣讓它自動安裝依賴。MCP Server 加了就加了，`pip install` 跑了就跑了。之前在 EP13 的 Weekly Vlog 裡有提到過 AI 供應鏈攻擊的趨勢，但那時候覺得「應該不會那麼快輪到我」。

結果這次 LiteLLM 事件，就是一個活生生的例子：如果我剛好在 3 月 24 日那幾個小時裝了 browser-use，我的所有雲端憑證、SSH keys、Git token 可能全部都被傳到攻擊者的伺服器了。

這不是恐嚇，這是數學：每月 9500 萬次下載，3-4 小時暴露窗口，幾十個主流框架的傳遞依賴。中招的機率遠比你想像的高。

---

## 防禦原則：Harness Engineering 在供應鏈安全的應用

我在之前的文章裡提過 Harness Engineering 的概念 — AI 可以寫 Code，但不能自己上 Production。同樣的邏輯套用在供應鏈安全上：

### 1. 版本鎖定是最低標準

```
# 不要這樣
litellm>=1.82.2

# 要這樣
litellm==1.82.2
```

用 `pip freeze` 或 `poetry.lock` 把所有依賴的版本鎖死。每次升級都是一個有意識的決策，不是自動發生的事情。

### 2. AI 安裝的東西，人要看過

這是 Harness Engineering 的核心 — 在 AI 的「寫入操作」前面加一道人類審批。當 Claude Code 或 Cursor 要幫你裝新套件時：

- 先看一眼是什麼套件
- 查一下最近的版本更新紀錄
- 確認套件來源是否可信
- 考慮是否有更安全的替代方案

### 3. 隔離執行環境

不要在你的主力開發機上直接跑不確定的套件。用 Docker container、虛擬環境（venv）、或至少一個獨立的 Python 環境來隔離風險。

### 4. 監控異常行為

如果你的電腦突然：
- CPU 飆高（無限 Python 進程）
- 網路流量異常（數據外傳）
- 出現不明的 `.pth` 文件

這些都是供應鏈攻擊的典型徵兆。實踐哥MinLi 就是因為「電腦卡死」才發現問題的。

### 5. 定期輪換憑證

假設你已經被攻擊過（worst case thinking）：
- 輪換所有 SSH keys
- 輪換雲端平台的 Access Keys
- 更新 Git tokens
- 檢查 CI/CD pipeline 的 secrets

---

## 關鍵洞察

Karpathy 在推文最後講了一段話，我覺得值得每個 Vibe Coding 開發者貼在螢幕旁邊：

> 「Classical software engineering would have you believe that dependencies are good (we're building pyramids from bricks), but imo this has to be re-evaluated, and it's why I've been so growlingly averse to them, preferring to use LLMs to "yoink" functionality when it's simple enough and possible.」

翻譯一下：傳統軟體工程告訴我們依賴是好的，就像用磚頭蓋金字塔。但 Karpathy 認為這件事需要重新評估。他寧可用 LLM 把簡單的功能直接「抄」進自己的 codebase，也不要引入一個外部依賴。

這聽起來很反直覺 — AI 領域最頂尖的人，反而最不信任用 AI 拉依賴？但邏輯其實很清楚：**每多一個依賴，就多一個你無法控制的攻擊面**。

回到我們自己的情境。這次 LiteLLM 事件讓我重新思考了一件事：**Vibe Coding 的便利性和安全性是一個蹺蹺板**。

供應鏈攻擊的本質就是信任鏈攻擊。你信任 browser-use，browser-use 信任 LiteLLM，LiteLLM 信任它的 CI/CD pipeline，pipeline 信任 Trivy。只要這條鏈上的任何一環被攻破，所有下游都會受影響。而 Vibe Coding 正在讓這條信任鏈變得更長、更不透明。

最諷刺的是，這次攻擊之所以被發現，不是因為我們的安全工具多厲害，而是因為**攻擊者自己也在 Vibe Coding — 惡意代碼寫得太粗糙，把受害者的機器搞當機了**。如果攻擊者再細心一點，我們可能到現在都還不知道。

我的建議跟 Karpathy 一樣：享受 AI Coding 的加速，但在依賴管理這件事上，保持「不信任」的心態。能自己實作的簡單功能，就不要引入一個有幾百個子依賴的套件。就像我們在 Harness Engineering 裡說的 — AI 可以建議，但最終決策權必須在人手上。

裝什麼套件，裝什麼版本，這個決策不該交給自動化。

---

*這篇文章的 LiteLLM 供應鏈攻擊資訊來源包括 Andrej Karpathy 的推文分析、Snyk、Sonatype、FutureSearch 的技術分析報告，以及实践哥MinLi (@MinLiBuilds) 的第一手使用者回報。*
