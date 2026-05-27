---
layout: post
title: "500 台 AI 助理裸奔公網：Clawdbot 0.0.0.0 配置災難"
date: 2026-01-28 09:00:00 +0800
categories: [ai-agent, security]
tags: [ai-agent, security, clawdbot, shodan, prompt-injection]
description: "當你把「開箱即用」當作產品優勢，你可能正在替使用者開後門。近 1,000 台 Clawdbot 伺服器因預設 0.0.0.0 綁定直接暴露在公網，任何人都能接管你的 AI 助理、竊取敏感檔案、甚至清空你的加密貨幣錢包。"
image: /assets/images/clawdbot-security-disaster-cover.jpeg
---

隨著 AI Agent 技術的爆發，許多開發者和技術愛好者紛紛架設自己的 AI 助理。近期一款熱門的開源工具 **Clawdbot** 成為焦點——但這次大家關注的不是它的功能，而是它**極度危險的預設配置**。

根據最新的網路掃描數據（Shodan），全球目前有**將近 1,000 台 Clawdbot 伺服器直接暴露在公網上**。這些伺服器大多沒有任何身份驗證保護，意味著：

> **任何人只要知道 IP 和 Port，就能直接接管你的 AI，甚至竊取你電腦中的敏感檔案。**

如果你的 Mac Mini 或伺服器上正跑著 Clawdbot，**請立刻檢查你的設定**。

---

## 發生了什麼事？

### 致命的預設值：0.0.0.0:18789

Clawdbot 預設啟動時，會將 Gateway 服務綁定在 `0.0.0.0:18789`。

對於非網路專業的人來說，這看起來只是一串數字。但在資安領域，`0.0.0.0` 代表的是：**對全世界開放**。

| 綁定地址 | 意義 | 風險等級 |
|---------|------|---------|
| `127.0.0.1` | 只有本機可以連 | 安全 |
| `0.0.0.0` | 所有網路介面都能連 | **危險** |

**正確做法：** 本地開發工具應綁定在 `127.0.0.1`（Loopback / Localhost）

**現狀：** 由於預設對外開放，且沒有強制要求設定登入密碼（Token），任何掃描到 18789 Port 的人都可以直接連線。

這不是漏洞，這是**設計決策**——一個極度危險的設計決策。

---

### 更隱蔽的陷阱：反向代理讓認證形同虛設

即使你設定了綁定 `127.0.0.1`，還有一個更隱蔽的問題。

資安研究員 [Jamieson O'Reilly (@theonejvo)](https://x.com/theonejvo/status/2015401219746128322) 在深入分析後發現，漏洞根源在於系統**預設信任來自本地（127.0.0.1）的連接**。

他這樣形容這個問題：

> 想像你雇了一個管家。他很聰明，管理你的行事曆、處理你的訊息、篩選你的電話。他知道你的密碼——因為他需要；他讀你的私人訊息——因為那是他的工作；他有所有東西的鑰匙——不然他怎麼幫你？
>
> 現在想像你回到家，發現大門敞開，管家正開心地為街上隨便走進來的人倒茶，而一個陌生人坐在你的書房裡讀你的日記。

這就是他在過去幾天發現的情況——**數百台 Clawdbot 伺服器直接暴露在公網上**。

**問題來了：** 當你使用 Nginx 或 Caddy 等反向代理時，所有外部流量都會被「轉發」到本地。在 Clawdbot 看來，這些請求都來自 `127.0.0.1`——被誤判為受信任的本地流量。

結果：**認證機制形同虛設**。

```
外部攻擊者 → Nginx (反向代理) → 127.0.0.1:18789 → Clawdbot 認為是本地流量 → 自動批准 ✓
```

更技術性的說明：Clawdbot 有一個 `trustedProxies` 配置選項，但**預設為空**。當它為空時，Gateway 會完全忽略 `X-Forwarded-For` header，直接使用 socket 地址——而在反向代理後面，這永遠是 loopback。

這意味著：

- 即使你設了 Token，攻擊者也能繞過
- 攻擊者可以**以 root 權限執行 Shell 命令**（O'Reilly 實測 `whoami` 回傳 `root`）
- 攻擊者可以透過 **Prompt Injection** 誘導 AI 執行惡意指令
- 攻擊者可以**操控你看到的訊息**——過濾某些內容、修改回應，讓你以為一切正常

**如果你有用反向代理，請立即配置 `gateway.auth.password` 或 `gateway.trustedProxies`。**

---

### 真實案例：Signal 對話與 API Key 外洩

在 O'Reilly 的調查中，他發現了一個特別諷刺的案例。

某位自稱「AI Systems Engineer」的使用者，將 Clawdbot 連接到自己的 **Signal** 帳號——號稱全球最安全的加密通訊軟體。

**結果呢？**

O'Reilly 在這台伺服器上發現了一個 **Signal 設備配對 URI**。這代表什麼？

> 只要用裝有 Signal 的手機點擊這個連結，就能配對到該帳號，獲得完整存取權限。Signal 提供的所有加密保護都變得毫無意義——因為配對憑證就這樣躺在一個全世界都能讀取的暫存檔裡。

除此之外，他還發現：

- 攻擊者能存取檔案系統中的敏感資料
- `.env` 檔中的 API Key、私鑰等**完全暴露**
- Anthropic API keys、Telegram bot tokens、Slack OAuth 憑證，應有盡有

但這只是冰山一角。根據調查，攻擊者可以存取的資料遠不止這些：

| 資料類型 | 風險說明 |
|---------|---------|
| **API Keys & OAuth 憑證** | OpenAI、Anthropic、Google 等服務的金鑰 |
| **Slack 私訊** | 數月份的工作對話、機密討論 |
| **Telegram 聊天** | 私人群組、頻道內容 |
| **Discord 訊息** | 社群對話、私訊記錄 |
| **Signal 對話** | 號稱最安全的通訊軟體，一樣被看光 |
| **WhatsApp 訊息** | 個人與商業對話 |
| **系統配置文件** | SSH 金鑰、資料庫連線字串、雲端憑證 |

這完全就是**將數位資產拱手讓人**。

更可怕的是，這位使用者可能到現在都不知道自己的資料已經被看光了——整個過程沒有任何警告、沒有任何日誌、沒有任何通知。

攻擊者只是「正常使用」了一個對外開放的服務。

---

### 更慘的案例：加密貨幣錢包被清空

就在本文撰寫期間，Twitter 上出現了更令人心痛的案例：

![Clawdbot 錢包被盜推文](/assets/images/clawdbot-wallet-drained-tweet.png)

這位使用者 @sanjaybuilds_ 在 2026 年 1 月 26 日發文：

> "WTF! I set up ClawdBot on my laptop and all my money is gone...??!!"

截圖顯示他的加密貨幣錢包餘額：**$0**，跌幅 **-99.99%**。

這不是誇張。當你的 Clawdbot 有權限存取：

- 加密錢包的私鑰檔案
- MetaMask 或其他錢包的 config
- `.env` 裡的助記詞或 API Key

攻擊者只需要透過你暴露的 Clawdbot 讀取這些檔案，就能直接轉走你所有的資產。

**這個案例的教訓：**

1. **AI Agent 的權限比你想像的大**——它能讀取你電腦上的任何檔案
2. **加密貨幣是不可逆的**——一旦轉走，沒有銀行客服可以幫你追回
3. **「我只是裝來玩玩」的心態很危險**——攻擊者不會因為你是新手就手下留情

598 個愛心、139 則回覆，代表這不是個案。還有多少人正在經歷同樣的事，卻不敢說出來？

---

### Shodan 上的「獵殺」名單

透過 Shodan 搜尋引擎簡單搜尋 `clawdbot`，可以輕易看到來自**美國、德國、甚至台灣**的暴露主機。

這些主機的詳細資訊一覽無遺：

- 路徑
- 版本號
- 作業系統
- 開放的 API endpoints

攻擊者甚至不需要高深的技術就能進行利用。這不是「駭客技術」，這是「Google 搜尋」等級的難度。

---

## 如何自救？Clawdbot 安全加固指南

如果這是你的機器，**請立即停止服務**，並按照以下步驟進行修復。

### 基礎急救（現在就要做！）

修改你的設定檔（通常是 `config.yaml` 或環境變數配置），進行以下兩項最關鍵的改動：

#### 1. 鎖定連線範圍（Bind to Loopback）

**問題：** Gateway exposed on `0.0.0.0`

**修正：** 將綁定地址改為本地回環地址

```yaml
gateway.bind: "loopback"  # 或 127.0.0.1
```

#### 2. 啟用身份驗證（Enable Authentication）

**問題：** 任何人都能連線

**修正：** 強制開啟 Token 驗證模式

```yaml
gateway.auth.mode: "token"
```

並在環境變數中設定一組高強度的 Token：

```bash
export GATEWAY_AUTH_TOKEN="你的複雜密碼"
```

**注意：** 如果你有使用 Control UI 或 Webhook，請確保它們也只監聽 Localhost，或透過 Tailscale 等 VPN 服務進行內網穿透，**千萬不要直接開 Port 給公網**。

---

### 加碼保險：假設你已經被掃過

完成基礎急救後，還有幾件事可以讓你睡得更安穩：

#### 1. 跑內建安全檢查

Clawdbot 其實有內建的安全掃描工具，只是很多人不知道：

```bash
# 基本健康檢查
clawdbot doctor

# 深度安全稽核（會自動修復部分問題）
clawdbot security audit --deep --fix
```

這會幫你檢查：

- 綁定地址是否安全
- Token 是否已設定
- 沙盒是否啟用
- 權限是否過大

**建議：** 每次更新 Clawdbot 後都跑一次。

#### 2. 遠端存取？用隧道，別開 Port

如果你真的需要從外面連回家裡或辦公室的 Clawdbot，**千萬別直接開 Port**。

用隧道服務，外面的人看不到你的 Port，但你還是能連：

| 方案 | 特點 | 價格 |
|-----|------|-----|
| **Cloudflare Tunnel** | 零配置、免費、企業級安全 | 免費 |
| **Tailscale** | P2P 加密、跨設備私有網路 | 免費（個人） |
| **ngrok** | 開發測試用、臨時 URL | 免費（有限制） |

**推薦組合：** Cloudflare Tunnel（穩定）+ Tailscale（跨設備）

這樣你的 Clawdbot 對外完全隱形，但你還是能透過 `your-subdomain.yourdomain.com` 連接。

#### 3. 強制設定 Token（不是「建議」，是「必須」）

即使你已經綁定 localhost，**還是要設 Token**。

因為：

- 本機的其他程式可能被攻破
- 瀏覽器的惡意網頁可能透過 localhost 攻擊（CSRF）
- 多一層防護總是好的

```bash
# 生成高強度 Token（32 字元隨機字串）
export GATEWAY_AUTH_TOKEN=$(openssl rand -base64 32)

# 或直接寫進 config
echo "gateway.auth.token: \"$(openssl rand -base64 32)\"" >> ~/.clawdbot/config.yaml
```

#### 4. 假設已經被掃過，現在止血

如果你的 Clawdbot 已經暴露了一段時間（即使只有幾小時），**假設最壞情況**：

**立即 Rotate 所有 API Keys：**

```bash
# 檢查你的 .env 或 config 裡有哪些 Key
cat ~/.clawdbot/.env | grep -i "key\|token\|secret"

# 去對應的服務 Dashboard 重新生成：
# - OpenAI: https://platform.openai.com/api-keys
# - Anthropic: https://console.anthropic.com/settings/keys
# - 其他服務...
```

**檢查異常使用：**

- 查看各 API 服務的 Usage Dashboard，有沒有異常流量
- 檢查 Clawdbot 的 Session Logs，有沒有不是你發起的對話
- 查看檔案系統的存取記錄（如果有開 Audit Log）

**重設 OAuth 連接：**

如果你的 Clawdbot 連接了 Google、GitHub、Slack 等服務，考慮撤銷並重新授權。

---

## 進階加固：Top 10 漏洞與修復方案

單單鎖住 IP 還不夠。若你想長期安全運行，請落實以下措施：

| 風險等級 | 漏洞描述 | 修復方案 |
|---------|---------|---------|
| 高危 | Gateway 暴露在公網 | 設定 `gateway.auth.token` 並綁定 Localhost |
| 中危 | DM 策略允許所有使用者 | 設定 `dm_policy` 為白名單（Allowlist），僅限特定用戶 |
| 高危 | 沙盒（Sandbox）預設關閉 | 啟用 `sandbox=all` 並配置 `docker.network=none` 阻斷對外連線 |
| 中危 | 憑證以明文儲存（oauth.json） | 改用環境變數（Env Vars）並設定檔案權限為 `chmod 600` |
| 中危 | Prompt Injection（提示注入） | 將不信任的輸入內容用標籤包裹隔離（Untrusted tags） |
| 高危 | 未阻擋危險指令 | 在層級上封鎖 `rm -rf`、`curl pipes`、`git push --force` 等指令 |
| 高危 | 無網路隔離 | 使用 Docker Network Isolation 防止容器橫向移動 |
| 高危 | 工具權限過大 | 限制 MCP（Model Context Protocol）工具僅能存取最小必要範圍 |
| 高危 | 未開啟稽核日誌 | 啟用完整的 Session Logging，以便事後追查 |
| 中危 | 配對碼過弱 | 使用加密等級的隨機碼並實施速率限制（Rate Limiting） |

### 修復優先級

如果你時間有限，請**至少**完成前三項：

1. **綁定 Localhost**（5 分鐘）
2. **啟用 Token 驗證**（5 分鐘）
3. **啟用沙盒**（10 分鐘）

這三項做完，你的風險會從「裸奔」降到「有基本防護」。

---

## 坦白說：這是預設安全的反面教材

這次 Clawdbot 的事件是一個經典的 **"Security by Default"（預設安全）** 反面教材。

### 開發者的問題

開發者為了讓工具「開箱即用」，往往犧牲了安全性。

我理解這種心態——你想讓使用者 5 分鐘就能跑起來，而不是花 30 分鐘看文件設定防火牆。

但問題是：**大多數使用者不會去改預設值**。他們會假設：「既然官方這樣設定，應該是安全的吧？」

這個假設在 2026 年的 AI Agent 時代，可能會讓你付出慘痛代價。

### 使用者的問題

使用者為了嚐鮮，往往忽略了檢查配置。

「先跑起來再說」、「內網應該沒問題」、「誰會攻擊我這種小咖」——這些想法我都聽過。

但現實是：

- Shodan 不在乎你是大公司還是個人
- 自動化掃描器不會因為你是「小咖」就放過你
- 一旦你的 AI Agent 被接管，攻擊者拿到的是**你的身份、你的權限、你的資料**

### AI Agent 的特殊風險

AI Agent 能夠：

- 讀寫你的檔案
- 執行指令
- 代表你發送訊息
- 存取你連接的所有服務

這類工具的權限極大，**一旦失守，後果比傳統網站被駭更為嚴重**。

傳統網站被駭，攻擊者拿到的是網站資料；AI Agent 被接管，攻擊者拿到的是**你的數位分身**。

---

## 結論

> **別自己開洞給別人用。**
>
> **現在就去檢查你的 Port 18789 吧！**

這次 Clawdbot 事件給我們的教訓：

1. **預設值很重要**：開發者應該把安全當作預設，而不是選配
2. **使用者要自救**：不要假設任何工具的預設配置是安全的
3. **AI Agent 需要更嚴格的安全標準**：因為它的權限比傳統應用大太多了

如果你正在運行任何 AI Agent 服務，問自己三個問題：

1. **它綁定在哪個 IP？**（應該是 `127.0.0.1`）
2. **有沒有身份驗證？**（應該有 Token）
3. **有沒有稽核日誌？**（應該有）

如果答案是「不知道」，那本身就是風險。

---

## 常見問題 Q&A

**Q: 我在內網跑 Clawdbot，應該沒問題吧？**

不一定。如果你的內網有其他人（公司同事、室友、咖啡廳的其他人），他們都能存取你的 Clawdbot。更危險的是，如果你的路由器有 UPnP 或 port forwarding 設定，你的「內網」可能已經對外開放了。建議：即使在內網，也要啟用 Token 驗證。

**Q: 我已經暴露了一段時間，怎麼知道有沒有被攻擊？**

檢查以下幾點：(1) 查看 Clawdbot 的 Session Logs，有沒有不是你發起的對話；(2) 檢查檔案系統有沒有被讀取或修改的痕跡；(3) 檢查你的 `.env` 和 API Keys 有沒有被使用（查看對應服務的 Usage Dashboard）。如果有任何可疑跡象，建議立即 Rotate 所有 API Keys。

**Q: 為什麼開發者要把預設值設成 0.0.0.0？**

通常是為了「方便」——讓使用者可以從其他設備連接，或在 Docker 環境中更容易配置。但這種「方便」犧牲了安全性。正確做法應該是預設 `127.0.0.1`，讓需要對外開放的使用者自己去改設定。

**Q: Tailscale 是什麼？為什麼文章推薦它？**

Tailscale 是一個零配置的 VPN 服務，可以讓你的設備建立安全的私有網路。即使你需要遠端存取 Clawdbot，用 Tailscale 會比直接開 port 安全得多。因為流量會經過加密，而且只有你的設備能連接。

**Q: 這個問題只有 Clawdbot 有嗎？**

不是。很多開源的 AI Agent 工具都有類似問題。我在之前的文章提過，整個 AI IDE 生態都有安全問題（IDEsaster 報告指出 100% 測試的 AI IDE 都存在漏洞）。Clawdbot 只是因為這次被大規模掃描而曝光。如果你在跑其他 AI Agent 服務，建議也做同樣的安全檢查。

---

## 延伸閱讀

- [AI Coding 的第一個風險，不是模型——是你一直按「Yes」](/ai-coding-tool-security-risk-prompt-injection-rce/)
- [AI Agent 安全性：遊戲規則已經改變](/ai-agent-security-you-xi-gui-ze-yi-jing-gai-bian/)
