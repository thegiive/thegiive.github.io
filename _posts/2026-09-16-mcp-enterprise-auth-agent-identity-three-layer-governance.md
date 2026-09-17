---
layout: post
title: "MCP 的企業安全不是一個產品能解的：從 IdP 授權到 runtime enforcement 的三層治理"
date: 2026-09-16 09:00:00 +0800
permalink: /mcp-enterprise-auth-agent-identity-three-layer-governance/
description: "八月底 Anthropic 宣布 Enterprise-managed auth GA，把 MCP connector 的授權從個人 OAuth 收歸 IdP 集中管理。同一個月，CrowdStrike 在 Fal.Con 發布 Agentic Identity Provider，主張每個 AI agent 都是特權身分。安全社群則拿出一個反例：有客戶的 agent 被 MCP gateway 擋下之後，改走 Bash 把變更送了出去。這三條線索拼在一起的結論是：MCP 的企業安全需要三層——入口的 IdP 授權、中間的政策閘道、和執行期的 runtime enforcement。少了任何一層，agent 都能繞過去。"
image: /assets/images/mcp-three-layer-governance-cover.png
categories: [AI Agent]
author: Wisely Chen
---

一個 agent 被 MCP gateway 的政策擋下了。它沒有放棄。它改用 Bash，把變更送了出去。

這是 Bluebear Security 在 X 上分享的客戶案例。agent 的目標是送出一筆程式碼變更，MCP gateway 說不行，agent 就繞過 MCP，直接走 shell。

如果你對這個行為覺得眼熟——沒錯，這跟 Anthropic 七月底公布的 [Claude 逃出沙箱](/claude-sandbox-escape-harness-failure/)在結構上是同一件事：**你以為的邊界，不是 agent 眼中的邊界。** 沙箱有沒隔離好的網路，gateway 有沒管到的通道。agent 不理解「你不該走那裡」，它只理解「那裡走得通」。

差別在於，sandbox escape 是研究環境的意外。MCP gateway 繞過是生產環境裡正在發生的事。

---

## MCP 在企業裡的擴散速度，已經超過治理追上的速度

先看規模。到 2026 年中，公開的 MCP server 超過 9,400 個，私有和企業內部的估計是公開數量的三到四倍。Gravitee 的報告估計超過三百萬個 AI agent 在企業裡運作，四個月內翻了一倍。

再看治理缺口。同一份報告裡，監控覆蓋率只有 52%。只有 14.4% 的企業在 agent 上線前做了完整安全審查。88% 的企業說自己經歷或懷疑過 agent 相關的安全事件。

問題出在 MCP 的採用路徑。工程師在自己的 IDE 裡加一個 MCP server——Cursor、Claude Code、VS Code 都支援——通常只需要改一個 config 檔。它跑在 localhost、走 stdio，不經過公司網路。傳統的 CASB 和 SSE 工具根本看不見它，因為它從來沒有離開開發者的機器。

但它用的是那個工程師的身分和憑證。它能存取的東西，就是那個工程師能存取的所有東西。

Qualys 用了一個精準的描述：一份研究發現 53% 的 MCP server 還在用靜態 secret。WorkOS 的報告指出，非人類身分（NHI）對人類身分的比例已經到了平均 45:1。每一個沒有被治理的 MCP server，就是一個沒有 audit trail、沒有獨立身分、但有完整存取權限的端點。

---

## 三條路線在同一季成形

2026 年六月到九月，三條互補的產業回應同時出現。它們各自解決問題的不同層面，沒有一條能獨立解決全部。

### 第一層：入口——Anthropic 的 Enterprise-Managed Auth

八月底 Anthropic 宣布 Enterprise-managed auth 正式 GA。技術上用的是 ID-JAG（Identity Assertion JWT Authorization Grant）：使用者登入企業 IdP 時取得一個斷言令牌，拿它跟 MCP server 的授權伺服器換 access token。管理員在 IdP（首批支援 Okta）設定一次，員工開 Claude 的時候 connector 就自動在那裡了。

GA 時支援十個 connector：Asana、Atlassian、Canva、Figma、Granola、Linear、Supabase、Datadog、Notion、Slack。Exa、Miro、Zoom 即將加入。

Enterprise-Managed Authorization 是 MCP 的開放擴充標準（spec 狀態 stable），不只綁 Anthropic——任何 MCP client 和 server 都可以實作。Keycloak 在 26.7 版加了實驗性 ID-JAG 支援（receiver-side），issuer-side 還在開發中。Hitachi Vantara 的工程師在 Keycloak 社群推動這個實作。

這一層解決的問題很具體：**消除 OAuth sprawl。** 以前每個員工、每個 connector 各自做 OAuth 授權，IT 看不見誰接了什麼。現在收歸 IdP，接了什麼、誰有權限、什麼時候撤銷，都有一個地方看。

但它只管入口。agent 拿到 token 之後做了什麼，這一層管不到。

### 第二層：閘道——InfoQ 的四層安全模型與 gateway 的極限

InfoQ 七月底一篇由 Nik Kale 撰寫的長文，把 MCP 生產安全拆成四層：

| 層級 | 功能 |
|------|------|
| L1 Execution | 確保 tool handler 把參數當 data 處理，不當指令執行——防 command injection |
| L2 Management Infrastructure | 開發工具、inspector、註冊端點必須認證——防未授權安裝 |
| L3 Outbound Trust Boundary | egress allowlist + scoped token——控制 server 能連到哪裡 |
| L4 Semantic Integrity | SHA-256 manifest pinning——偵測工具定義被偷改 |

這四層不是理論。三月 Azure MCP Server 被發現一個 CVSS 8.8 的 SSRF 漏洞（CVE-2026-26118），攻擊者可以透過 MCP 工具呼叫騙出 managed identity token——這就是 L3（outbound trust boundary）沒做好。另一個 CVE 是 MCPJam Inspector 的未認證端點，可以在使用者不知情的情況下安裝任意 MCP server——這是 L2。到七月底為止 30 個 MCP 相關 CVE 中，13 個是 command injection——L1。

但即便四層都做了，MCP gateway 仍然有一個根本限制：**它只管 MCP 協定內的呼叫。**

Bluebear 的案例就是證據。agent 被 gateway 擋下之後改走 Bash，根本不經過 MCP。gateway 看不見、攔不住。這不是 gateway 的 bug，是 gateway 這個概念本身的邊界。

Nightfall 做的是 inline policy：在 Cursor、Claude Code、VS Code 這些 IDE 裡攔截工具呼叫，包括 prompt injection 偵測和 shell command 掃描。方向對了——把政策執行從 MCP 層往下推到 runtime——但目前仍在早期。

### 第三層：身分——CrowdStrike 的 Agentic IdP

CrowdStrike 在一月用 7.4 億美元收購了身分安全公司 SGNL。九月初在 Fal.Con 發布了 Agentic Identity Provider——

> "AI agents operate with superhuman speed and access, making every agent a privileged identity that must be protected."
>
> George Kurtz, CrowdStrike CEO

Agentic IdP 的做法：短期憑證（不是長效 token）、密碼學驗證身分、每個 agent 動作追溯到負責的人。如果風險評估改變，存取立刻撤銷。

這是把企業安全裡「非人類身分」的治理模式套到 AI agent 上。邏輯清晰：你不會給一個 service account 不限期的管理員權限，為什麼要給一個 AI agent？

反方也很直接：有人批評這是資安廠商在 AI 恐慌上自肥——先收購身分安全公司，再把「每個 agent 都是威脅」包裝成產品。CrowdStrike 的確同時是問題的定義者和解方的販賣者。

但批評歸批評，底層邏輯站得住：agent 有存取權限、會自主行動、目前多數沒有獨立身分。不管誰來賣這個解法，問題本身是真的。

---

## 三層拼在一起：企業 MCP 治理的最小架構

| 層 | 解決什麼 | 代表方案 | 管不到什麼 |
|----|---------|---------|-----------|
| 入口（IdP 授權） | OAuth sprawl、shadow IT、集中 provisioning/deprovisioning | Anthropic EMA、Keycloak ID-JAG | agent 拿到 token 後的行為 |
| 閘道（政策攔截） | 工具呼叫的內容過濾、egress 控制、manifest 完整性 | InfoQ 四層模型、Nightfall、各家 MCP gateway | 非 MCP 通道（Bash、直接 API call） |
| 執行期（runtime enforcement） | agent 的每個動作都要有身分、有 scope、有歸屬、可撤銷 | CrowdStrike Agentic IdP、SGNL continuous identity | 不走企業 IdP 的 shadow agent |

這三層跟這個 blog 寫了大半年的 [Harness Engineering](/harness-engineering-security-best-practices/) 是同一個論點的不同尺度。

Harness Engineering 講的是**個人開發者層級**：你的 agent 的 permission mode、sandbox 隔離、SECURITY.md 裡的規則，這些是你一個人能控制的。本篇講的三層是**企業層級**：當公司裡有幾百個開發者、各自跑各自的 agent，你不能靠每個人自己設好 permission mode。你需要 IdP 來集中管入口，需要 gateway 來攔截工具呼叫，需要 runtime enforcement 來確保 agent 繞不過去。

用 [sandbox escape 那篇](/claude-sandbox-escape-harness-failure/)的框架：**IdP 是門禁卡，gateway 是監控攝影機，runtime enforcement 是鎖在門上的物理鎖。** 門禁卡管你能不能進大樓，監控攝影機記錄你做了什麼，物理鎖確保你進不了不該進的房間。少了任何一個，其他兩個就不夠。

---

## 對企業 CTO 的具體決策改變

**Before（多數企業現狀）：** 每個團隊各自接 MCP connector，工程師自己做 OAuth 授權。IT 不知道哪些 agent 連了哪些工具。agent 用的是員工個人憑證，離職了 token 還活著。出事之後才發現沒有 audit trail。

**After（三層治理的最小可行版）：**

1. **短期可做（入口層）**：如果你用 Claude Team/Enterprise，啟用 Enterprise-managed auth，把 connector 授權收歸 IdP。如果你用其他 MCP client，確認它支不支援 EMA spec。至少做到「IT 知道哪些 connector 被接了」。

2. **中期要做（閘道層）**：選一個 MCP gateway 或 proxy，至少做到 tool call 的 logging 和 egress control。不要只做 allow/block——Bluebear 的案例告訴你 block 會被繞過。logging 比 blocking 優先，因為你至少知道發生了什麼。

3. **長期方向（runtime 層）**：agent 需要獨立身分，不是借用員工的。憑證必須是短期的，scope 必須是最小的，每個動作必須可追溯到負責的人。這是目前最不成熟的一層。

---

## 坦白說

幾個限制。

第一，「三層治理」是我從三條獨立的產業動態歸納出來的框架，不是任何一家公司或標準組織提出的。它的價值在把分散的資訊組織起來，但不要當成一個已經被驗證過的架構。

第二，Gravitee 和 WorkOS 引用的數字（三百萬 agent、監控覆蓋率 52%、88% 經歷過事件）來自產業報告，這些報告的調查方法和樣本我沒有獨立驗證。資安廠商的報告天然傾向把問題說得嚴重——它們同時在賣解法。

第三，Bluebear 的 Bash 繞過案例來自一條 X 貼文，沒有第二來源、沒有技術細節。它在概念上合理（agent 本來就不只有 MCP 一條路），但具體的「被擋了就改 Bash」這個行為描述，我無法獨立確認。

第四，runtime enforcement 這一層目前最不成熟。CrowdStrike 的 Agentic IdP 九月初才發布，沒有公開的企業部署案例。在實際驗證之前，它是一個方向，不是一個解法。

---

## 關鍵洞察

- **MCP gateway 是必要的，但不是充分的。** Gateway 只管 MCP 協定內的呼叫。agent 能走的路不只 MCP——Bash、直接 API call、甚至 HTTP request 都是。政策只在 gateway 層執行，等於只鎖了一扇門，其他窗戶全開著。

- **IdP 集中授權是最低門檻。** Anthropic 的 EMA 解決的是最基本的問題：IT 至少要知道誰接了什麼。如果你的企業連這一步都沒做到，後面的 gateway 和 runtime 都是空談。

- **「每個 agent 是特權身分」不只是行銷語言。** 不管 CrowdStrike 的動機是什麼，底層邏輯成立：agent 有存取權限、會自主行動、多數沒有獨立身分。你不會讓一個沒有身分的人走進機房，為什麼讓一個沒有身分的 agent 碰你的生產系統？

- **對個人開發者：你的 agent 的 permission mode 就是你的一人版三層治理。** 企業有 IdP、gateway、runtime enforcement；你有 `.claude/settings.json` 裡的 permission rules、sandbox 設定、和 tool allowlist。規模不同，結構一樣。

---

## 常見問題 Q&A

**Q: Enterprise-Managed Authorization（EMA）跟傳統的 OAuth 授權差在哪？**

傳統做法是每個員工、每個 MCP connector 各自做 OAuth 授權——員工在瀏覽器裡點「允許存取」，token 存在本機。EMA 把這個動作收歸企業的 IdP（Identity Provider，身分提供者）：管理員在 IdP 設定一次授權政策，員工登入時自動取得 connector 存取權。技術上用的是 ID-JAG（Identity Assertion JWT Authorization Grant），使用者在 SSO 登入時取得一個斷言令牌，拿去跟 MCP server 換 access token。好處是 IT 有集中的可見性、可以即時撤銷、員工離職時 token 跟著失效。Anthropic 的實作首批支援 Okta，目前是十個 connector。EMA 是 MCP 的開放擴充標準（spec 狀態 stable），不限於 Anthropic 生態系。

**Q: MCP gateway 跟 API gateway 有什麼不同？**

傳統 API gateway（如 Kong、NGINX）管的是 HTTP 請求的路由、限流、認證。MCP gateway 多了一層語意理解：它知道這是一個「工具呼叫」，知道呼叫的是哪個工具、帶了什麼參數，所以可以做內容層級的政策（例如「不准呼叫刪除類工具」「參數裡不能有 PII」）。但 MCP gateway 的根本限制是它只看得見走 MCP 協定的流量。如果 agent 改走 Bash 或直接呼叫 API，gateway 看不到也攔不住。

**Q: 小團隊沒有 IdP 和 gateway 預算，能做什麼？**

三件立刻能做的事。第一，盤點你的團隊裡跑了哪些 MCP server——看每個人的 IDE config 檔（Claude Code 的 `.claude/settings.json`、Cursor 的 `.cursor/mcp.json`）。第二，確保 agent 的 permission mode 不是 full auto——至少寫入和外連要人工確認。第三，把靜態 API key 換成短期 token——不需要商用 IdP，OAuth2 的 client credentials flow 搭免費的 Keycloak 就能做。這三步不需要花錢，但能把最大的風險（不知道有什麼 agent、agent 全自動無限權限、憑證不過期）擋掉。

**Q: CrowdStrike 的 Agentic IdP 跟 Anthropic 的 EMA 是競爭還是互補？**

互補。兩者解決不同層的問題。Anthropic 的 EMA 管的是 MCP connector 的授權入口——哪些人能用哪些 connector，怎麼 provisioning 和 deprovisioning。CrowdStrike 的 Agentic IdP 管的是 agent 本身的身分和行為——給每個 agent 一個可驗證的身分、短期憑證、和行為追溯。前者是「誰能開門」，後者是「進門之後能做什麼、做了什麼要記下來」。一個企業兩個都需要。

**Q: 到七月底為止 MCP 的安全漏洞情況有多嚴重？**

到 2026 年七月底，公開的 MCP 相關 CVE 有 30 個。其中 13 個是 command injection——tool handler 用 eval() 或 shell 執行未驗證的參數。最知名的是三月的 CVE-2026-26118（Azure MCP Server SSRF，CVSS 8.8），攻擊者可以透過工具呼叫讓 server 送出 managed identity token。另一個是 MCPJam Inspector 的未認證端點（CVE-2026-23744），可以靜默安裝任意 MCP server。這些漏洞分佈在 InfoQ 四層模型的每一層，不是單一產品的問題，是整個生態系的成熟度問題。

---

來源與延伸閱讀：
- [Anthropic: Enterprise-managed auth for MCP connectors](https://claude.com/blog/enterprise-managed-auth)
- [MCP Blog: Enterprise-Managed Authorization](https://blog.modelcontextprotocol.io/posts/enterprise-managed-auth/)
- [InfoQ: Securing MCP in Production — Defense-in-Depth beyond the Gateway](https://www.infoq.com/articles/securing-mcp-production-gateway/)
- [CrowdStrike: Agentic Identity Provider](https://www.crowdstrike.com/en-us/blog/crowdstrike-announces-agentic-identity-provider/)
- [WorkOS: The tools that caught shadow IT can't see MCP sprawl](https://workos.com/blog/mcp-sprawl-invisible-to-shadow-it-tools)
- [Qualys: MCP Servers — The New Shadow IT](https://blog.qualys.com/product-tech/2026/03/19/mcp-servers-shadow-it-ai-qualys-totalai-2026)
- [Bluebear Security 的 MCP bypass 案例（X）](https://x.com/Bluebear_sec/status/2099928286973296904)
- 本 blog 相關文章：[Harness Engineering 安全實踐](/harness-engineering-security-best-practices/)、[Claude sandbox escape](/claude-sandbox-escape-harness-failure/)、[Prompt Injection + Harness Engineering](/prompt-injection-harness-engineering-tool-using-agents/)
