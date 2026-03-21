---
layout: post
title: "OpenClaw 的五種上網方式：從搜尋 API 到接管你的瀏覽器"
date: 2026-02-26 07:00:00 +0800
categories: [AI Agent, IT架構]
tags: [OpenClaw, Browser, Web Access, Brave Search, Tavily, Managed Browser, Extension Relay, CDP, WebMCP, Playwright]
permalink: /openclaw-browser-five-modes-from-search-api-to-personal-browser/
image: /assets/images/openclaw-browser-five-modes-cover.png
description: "AI Agent 的「上網」不是一件事，而是五件事。選錯模式，輕則功能受限，重則帳號被盜。OpenClaw 的五種上網架構——Search API、Web Fetch、Managed Browser、Remote CDP、Extension Relay——每一種的能力範圍、安全風險、適用場景都天差地別。本文從最安全的搜尋 API 到最危險的瀏覽器接管，逐層拆解技術架構與安全風險，包含 Accessibility Tree vs 截圖的效率差異、Managed Browser 手動登入的甜蜜點、以及 WebMCP 的未來展望。"
---

![OpenClaw Browser Relay 實際操作畫面](/assets/images/openclaw-browser-five-modes-cover.png)

## 為什麼要搞清楚 AI 怎麼上網？

很多人用 OpenClaw（小龍蝦）的第一個驚喜是：「它會上網欸！」

然後下一個問題就是：「等等，它是怎麼上網的？用我的帳號嗎？」

這個問題比你想像的重要。

因為 OpenClaw 的「上網」其實不是一件事，而是**五種完全不同架構的事**。每一種的能力範圍、安全風險、適用場景都天差地別。

搞不清楚你在用哪一種，就像不知道自己開的車有沒有安全氣囊一樣。平常沒事，出事就出大事。

---

## 第一層：Search API — 最安全的資訊獲取

**對應工具：** `web_search`

這是最輕量的上網方式。OpenClaw 不開瀏覽器，不訪問任何網頁，只是呼叫搜尋引擎的 API，拿回一堆「標題 + 連結 + 摘要」的純文字結果。

就像你請助理「幫我查一下 XXX」，助理 Google 了一下，把前幾個搜尋結果唸給你聽。他沒有點進去看。

**支援的搜尋引擎：**

| 引擎 | 特色 | 免費額度 |
|------|------|---------|
| **Brave Search** | OpenClaw 預設首選 | 2,000 次/月 |
| **Perplexity** | AI 摘要 + 引用 | 依方案 |
| **Gemini** | Google 搜尋接地 | 依方案 |
| **Grok (XAI)** | X/Twitter 資料較強 | 依方案 |
| **SearxNG** | 自架、免費、無限制 | 無限 |
| **Tavily** | 專為 AI Agent 優化，結果更乾淨 | 依方案 |

**自動偵測優先級：** Brave → Gemini → Perplexity → Grok

設定方式很簡單，設好 API key 就行：

```bash
openclaw configure --section web
```

**安全等級：極低風險。** 搜尋 API 不會碰到你的瀏覽器、不會洩漏 cookies、不會登入任何帳號。唯一的風險是你的搜尋內容被搜尋引擎記錄（跟你自己 Google 一樣）。

**限制：** 只有搜尋結果摘要，沒有完整網頁內容。如果需要讀完整篇文章，就要升級到下一層。

---

## 第二層：Web Fetch — 抓網頁但不開瀏覽器

**對應工具：** `web_fetch`

這一層比搜尋進一步：OpenClaw 會實際發送 HTTP 請求去抓網頁內容，然後用 Readability 演算法萃取主要文字，轉成 markdown 格式。

就像你請助理「幫我把這篇文章的重點整理出來」，助理打開網頁、複製文字、整理好給你。

**技術細節：**
- 純 HTTP GET，不執行 JavaScript
- 用 Readability 萃取主要內容（去廣告、去導航列）
- 可搭配 Firecrawl 突破反爬機制（真正的瀏覽器渲染）
- 2MB 下載上限
- 15 分鐘快取

**安全等級：低風險。** 就是一個 HTTP 請求，跟 `curl` 差不多。不帶你的瀏覽器 cookies，不帶登入狀態。

**限制：** JavaScript 渲染的內容抓不到。SPA（單頁應用）、需要登入的頁面、動態載入的內容，通通沒辦法。這時候就需要真正的瀏覽器了。

---

## 第三層：Managed Browser — Agent 自己的瀏覽器

**對應工具：** Browser tool（managed 模式）

這是質變的一層。OpenClaw 會啟動一個**完全獨立的 Chromium 瀏覽器實例**，有自己的 user data directory，跟你的個人 Chrome 完全隔離。

關鍵設計決策：

- **獨立的使用者資料目錄：** 不碰你的 cookies、密碼、書籤、擴充套件
- **CDP port 18800：** 故意避開開發者常用的 9222，防止衝突
- **橘色外觀：** 一眼就能分辨哪個是 Agent 的瀏覽器、哪個是你的
- **Accessibility Tree Snapshot：** 不用截圖（5MB+），而是用結構化文字樹（~50KB），效率差 100 倍

```json
{
  "browser": {
    "defaultProfile": "openclaw",
    "headless": false
  }
}
```

**Accessibility Tree 怎麼運作？**

這是 OpenClaw 跟傳統 RPA 最大的區別。傳統做法是截圖 → 用視覺模型辨識按鈕位置 → 點擊座標。OpenClaw 的做法是：

- 把頁面轉成結構化文字樹（類似 DOM 但更精簡）
- 每個可互動元素標上編號，例如 `ref="12"`
- AI 讀文字樹，說「我要點 ref 12」
- Playwright 解析 ref 12 對應的真實 DOM 元素，執行點擊

50KB 的文字樹 vs 5MB 的截圖，不只是頻寬的差異，更是推理速度和 token 消耗的差異。

**安全等級：中等。** Agent 有一個真正的瀏覽器，可以執行 JavaScript、填寫表單、點擊按鈕。但因為是全新的隔離實例，它沒有你的任何登入狀態。最大的風險是它可能訪問到惡意網站，但影響範圍僅限於那個隔離的瀏覽器。

**適用場景：** 爬取需要 JavaScript 渲染的公開網頁、自動化表單填寫（不需登入的）、Web UI 測試。

**Pro Tip：手動登入 + Agent 接手**

很多人不知道，Managed Browser 其實可以「混合使用」。因為 `headless: false` 時它會開一個有畫面的 Chromium 視窗，你可以：

- 讓 Agent 啟動 Managed Browser
- **你自己手動在那個視窗裡登入**需要的服務（Gmail、GitHub、企業後台）
- 登入完成後，讓 Agent 接手操作

這是介於 Managed Browser 和 Extension Relay 之間的甜蜜點 — 你拿到了隔離瀏覽器的安全性（不碰你主力 Chrome 的任何資料），同時又有登入狀態的能力。而且因為是隔離實例，就算 Agent 出了什麼問題，影響範圍也只限於那個獨立的瀏覽器。

比起 Extension Relay 把整個主力瀏覽器交出去，這種做法風險小很多。我個人在需要登入但又不想用 Extension Relay 的場景，就是用這招。

---

## 第四層：Remote CDP — 雲端的瀏覽器

**對應工具：** Browser tool（remote CDP 模式）

把第三層的 Managed Browser 搬到雲端。OpenClaw 透過 WebSocket 連接到遠端 Chromium（例如 Browserless），你的本機完全不受影響。

**安全等級：視你信不信任那個雲端服務商而定。** 適用 CI/CD 自動化測試、生產環境爬蟲、需要水平擴展的場景。

---

## 第五層：Extension Relay — 接管你的瀏覽器

**對應工具：** Browser tool（extension relay 模式）

這是最強大、也最危險的模式。

你在 Chrome 安裝 **OpenClaw Browser Relay** 擴充套件，然後 OpenClaw 就能直接操作你正在使用的 Chrome 分頁。你登入的 Gmail、GitHub、企業後台、網銀 — Agent 全部看得到、操作得到。

OpenClaw 官方文件的原話是：

> 「Treat it like giving the model hands on your browser.」
> （把它當成把你的雙手借給 AI。）

**這不是比喻，這是字面意思。**

你能用瀏覽器做的事，Agent 都能做。包括：
- 讀你的 Gmail
- 操作你的 Google Calendar
- 在企業後台執行操作
- 存取你登入的任何 SaaS 服務

**安全等級：極高風險。** 這等於把你的完整瀏覽器 session 交給 AI。如果 Agent 的 prompt 被注入惡意指令（Prompt Injection），理論上可以執行任何你能做的操作。

**適用場景：** 需要存取已登入服務的自動化工作流。例如我自己用來操作 Google Calendar、Google Sheets。但前提是你完全信任當前的 Agent 配置，而且操作環境受控。

**我的建議：**
- 用專用 Google 帳號，不要用主帳號
- 只在需要時啟用，用完就關
- 不要在有敏感資料的環境中使用

---

## Bonus：WebMCP — 未來的第六種

2026 年 2 月，Google 和 Microsoft 聯合推出了 **WebMCP** 的早期預覽。

這是一個完全不同的思路：不是 AI 去「操作」網頁，而是網站主動「暴露」結構化的工具介面給 AI Agent。

就像餐廳不再需要客人自己走進廚房找食材，而是直接提供一份清楚的菜單。

- Chrome 146 Canary 已有 `WebMCP for testing` 實驗旗標
- Token 效率比截圖方式提升 89%
- 正在 W3C 標準化中
- 跟 Anthropic 的 MCP 不同層次 — WebMCP 是客戶端協議，MCP 是後端協議

這個還很早期，但如果成功，會根本性地改變 AI Agent 跟網站互動的方式。

---

## 我自己怎麼用

在我的[日常工作流](/openclaw-real-world-usage-workflow-not-chatbox/)裡，這五層我都有用到：

**日常最常用的：Search API + Web Fetch**

查技術文件、讀 GitHub issue、找 Stack Overflow 答案。這兩層覆蓋了 80% 的上網需求，而且零風險。

**需要操作網頁時：Managed Browser**

偶爾需要爬一些 JavaScript 渲染的網頁，或者測試 Web UI。用 Managed Browser，跟我的個人瀏覽器完全隔離。

**需要存取個人服務時：Extension Relay**

操作 Google Calendar、Google Sheets、發會議邀請。這是我用的最謹慎的模式，我有以下防線：

1. **專用 Google 帳號** — 不是我的主帳號
2. **專用 Mac Mini** — 不在主力工作機上跑
3. **用完就關** — 不讓 Extension Relay 常駐

即使做到這些，我還是會定期檢查那個帳號的活動紀錄。

---

## 如果你有 VPS / VM 該怎麼選？

很多人跑 OpenClaw 不是在本機，而是在 VPS（DigitalOcean、Linode）或雲端 VM（AWS EC2、GCP Compute Engine）上。這個場景下，選擇邏輯完全不同。

**核心差異：VPS/VM 通常沒有桌面環境。**

也就是說，你沒有 GUI、沒有 Chrome 視窗可以手動操作。這直接排除了幾個選項：

| 模式 | VPS/VM 能用嗎 | 原因 |
|------|-------------|------|
| **Search API** | 可以 | 純 API 呼叫，不需要瀏覽器 |
| **Web Fetch** | 可以 | 純 HTTP 請求，不需要瀏覽器 |
| **Managed Browser（headless）** | 可以 | Playwright headless 模式不需要 GUI |
| **Managed Browser（手動登入）** | 不行 | 需要 GUI 視窗讓你手動操作 |
| **Remote CDP** | 最適合 | 本來就是為這個場景設計的 |
| **Extension Relay** | 不行 | 需要你的本機 Chrome |

**VPS/VM 上的最佳組合：**

```
日常查資料 → Search API + Web Fetch（零風險）
爬公開網頁 → Managed Browser headless（中風險）
需要真正的瀏覽器能力 → Remote CDP 連 Browserless（低風險）
```

**為什麼 Remote CDP 在 VPS 場景特別適合？**

因為你本來就不在本機操作。瀏覽器跑在 Browserless 這類服務上，跟你的 VPS 是完全隔離的。就算瀏覽器被攻擊，影響範圍也僅限於那個容器化的 Chromium 實例，碰不到你 VPS 上的任何東西。

**需要登入怎麼辦？**

這是 VPS 場景最棘手的問題。沒有 GUI，你不能手動登入。幾個做法：

1. **在本機 Managed Browser 登入後，匯出 cookies** — 技術上可行但很折騰
2. **用 Remote CDP + 帶登入狀態的 user data directory** — 需要自己維護 Chromium 的 profile
3. **回到本機用 Extension Relay** — 把需要登入的操作留在本機做，VPS 只跑不需登入的任務

我自己的做法是第三種：**職責分離**。VPS 負責跑排程任務（爬蟲、資料處理），需要登入的操作留在 Mac Mini 上用 Extension Relay。不要試圖在 VPS 上解決所有問題。

---

## 坦白說

**做得好的地方：**

OpenClaw 把這五層分得很清楚，而且預設是最安全的模式（Search API）。Managed Browser 用橘色外觀區分、用 18800 port 避開衝突，這些都是有想過安全的設計。

Accessibility Tree Snapshot 取代截圖這個決策非常聰明。50KB vs 5MB，這不只是頻寬的問題，而是整個推理效率的問題。

**問題在哪：**

Extension Relay 的風險沒有被充分強調。Chrome Web Store 上的描述太輕描淡寫了。「Treat it like giving the model hands on your browser」這句話應該用紅色大字寫在安裝畫面上，而不是埋在文件裡。

另外，目前沒有細粒度的權限控制。Extension Relay 要嘛全開、要嘛全關。你不能說「只讓 Agent 存取 Google Calendar，但不能碰 Gmail」。這在企業場景是不可接受的。

WebMCP 很有潛力，但 2026 年 2 月才早期預覽，至少還要一年才能進入生產環境。

---

## 常見問題 Q&A

**Q: 我只是想讓 OpenClaw 查資料，該用哪一種？**

Search API。設好 Brave Search 的 API key，免費 2,000 次/月，足夠日常使用。如果需要讀完整文章，加上 Web Fetch。這兩層零風險。

**Q: Brave Search 和 Tavily 該選哪個？**

Brave 是 OpenClaw 的預設首選，免費額度足夠。Tavily 的結果針對 AI Agent 做過優化，去掉了很多雜訊，如果你是重度使用者可以考慮。SearxNG 則是完全免費無限制的自架方案。

**Q: Managed Browser 會不會洩漏我的資料？**

不會。它是一個全新的 Chromium 實例，有自己的 user data directory。就像你開了一個無痕視窗（但更徹底），不帶任何你的瀏覽記錄、cookies、密碼。

**Q: Extension Relay 在企業環境安全嗎？**

目前的設計不適合企業環境。沒有細粒度權限控制，等於全有或全無。如果一定要用，建議用專用帳號 + 專用設備 + 定期審計。

**Q: WebMCP 跟 Anthropic 的 MCP 是什麼關係？**

完全不同的東西。Anthropic 的 MCP 是後端協議，讓 AI 連接到工具伺服器。WebMCP 是前端協議，讓網站直接暴露結構化介面給瀏覽器中的 AI Agent。它們可以共存，解決的是不同層次的問題。

---

## OpenClaw 官方文件連結

- [Web Tools（web_search / web_fetch）](https://docs.openclaw.ai/tools/web) — 搜尋 API 與網頁抓取的完整設定指南
- [Browser Tool（Managed / Extension Relay / Remote CDP）](https://docs.openclaw.ai/tools/browser) — 三種瀏覽器模式的設定與使用說明
- [OpenClaw Browser Relay for Chrome — Chrome Web Store](https://chromewebstore.google.com/detail/openclaw-browser-relay-fo/pfhemcnpfilapbppdkfemikblgnnikdp) — Extension Relay 擴充套件安裝
- [WebMCP Early Preview — Chrome for Developers](https://developer.chrome.com/blog/webmcp-epp) — Google WebMCP 早期預覽公告

---

## 延伸閱讀

- [OpenClaw 記憶系統全解析：SOUL.md、AGENTS.md 與高昂的 Token 成本](/openclaw-architecture-deep-dive-context-memory-token-crusher/)
- [這幾天我密集使用小龍蝦 OpenClaw：為什麼我決定把它納入工作流](/openclaw-real-world-usage-workflow-not-chatbox/)
- [OpenClaw 安全隔離實戰：Gmail Sandbox Setup](/openclaw-security-isolation-gmail-sandbox-setup/)
- [AI Agent Security：遊戲規則已經改變](/ai-agent-security-you-xi-gui-ze-yi-jing-gai-bian/)

---

🌐 **English Version:** [OpenClaw's Five Ways to Browse the Web: From Search API to Taking Over Your Browser](https://en.wiselychen.com/en/openclaw-browser-five-modes-from-search-api-to-personal-browser/)
