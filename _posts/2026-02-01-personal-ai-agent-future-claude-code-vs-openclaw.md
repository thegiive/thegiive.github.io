---
layout: post
title: "個人 AI 助手決戰週：Claude Code vs OpenClaw 殊途同歸｜Weekly Vlog EP7"
date: 2026-02-01 14:00:00 +0800
permalink: /personal-ai-agent-future-claude-code-vs-openclaw/
image: /assets/images/vlog-ep7-claude-code-vs-openclaw-cover.png
description: "20 年前 Unix Power Tools 說「Command Line 是最好的 GUI」，當時我不理解。20 年後，大語言模型證明了這句話的先見之明。這週 Claude Code 持續領跑，OpenClaw 橫空出世，兩條路線正殊途同歸，逼近 Agent 2.0 的甜蜜點。"
---

{% include youtube.html id="vm0XguXy0aQ" %}

**發佈日期：** 2026-02-01
**主題：** 個人通用助手 AI Agent 的未來
**時長：** 約 18 分鐘

---

> 20 年前，Unix Power Tools 告訴我「Command Line 是這個世界上最好的 GUI」。當時我不理解。20 年後，大語言模型證明了這句話的先見之明。

## 這週發生了什麼

這週 AI Agent 圈子風起雲湧。除了 Claude Code 持續領跑，橫空出世的 ClawdBot（後來因為快被告改名 Moltbot，又改名 OpenClaw）帶來巨大震撼。

這不只是又一個新工具的誕生，而是兩條路線殊途同歸，逼近同一個 Agent 2.0 的甜蜜點。

## 為什麼 Command Line 是 LLM 的天作之合

20 年前我讀到 O'Reilly 出版的 Unix Power Tools，裡面有一句話讓我印象深刻：

> "Command Line 命令行，是這個世界上最好的 GUI。"

當時不理解。但經歷這麼多年一直使用 Command Line 後，我漸漸懂了。

**關鍵洞察：** 當作業系統上每一個東西都能用文字來表達、傳遞的話，程式跟程式之間、人跟程式之間的銜接就變得相當容易。我們只需要處理文字就好。

20 年後，我們本來以為命令行會慢慢式微。結果文字大語言模型出現了——以文字來思考的 AI。突然之間，文字 LLM 跟文字命令行就是天作之合。

如果大語言模型對外界的溝通跟感知，都能透過命令行相關的文字來進行交互的話，基本上他就可以做任何事情。

**這就是 Claude Code 跟原本 ChatGPT 最大的不同。** 它不是簡單的套殼大語言模型，而是把大語言模型最好的交互界面放進去，並且遵循它。這是 Claude Code 那麼有魅力、那麼有威力的原因。

## Agent 演進：從 1.0 到 2.0

讓我用版本號來解釋這個演進：

### Agent 1.0：套殼時代
一個大語言模型接上一個殼，像 ChatGPT 那樣。

### Agent 1.5：Claude Code
套上 Command Line 這個界面，並且在上面建構所有的生態系（Hook、Skill、MCP 這樣的機制）。**但依舊是半自動**——還是要人去觸發。

Claude Code 在安全性這邊非常嚴謹，盡可能不跳過權限控管或詢問。所以有時候用戶會覺得「還是卡卡的」。

### Agent 2.0：OpenClaw 路線
OpenClaw 已經解決這個問題。不是說解決，而是——因為他沒有像 Anthropic 那樣要 IPO、要合規的壓力，他是一人公司、開源社區，所以可以闘著去，在全自動領域進行探索。

**最大的感覺：他變得越來越主動。**

你可以在任何 VPS、雲上面的 VM、或現在賣得很兇的 Mac mini 上面裝起來。他可以定期去做相關事情，或透過 Telegram、Slack 跟你用文字、語音、圖像溝通。真的就像一個個人助手。

而且他甚至更積極去解決問題，遇到問題可以繞過去。

## 安全的噩夢：700-900 台裸奔的 Server

但有了這樣震撼後，給他這麼大權限，我們也立刻發現它帶來巨大的安全 Nightmare。

一開始的版本，預設值是 **open to public**。

這真的是非常可怕的事情。當時網路上就有上千台——我接觸到 700 多台，有人說 900 多台——這樣的 OpenClaw Server 在外面裸奔。大家可以進去裡面竊取任何東西。

兩三天後他改成預設安全，但就算這樣，我們也要重新思考：

- 我們真的能給一個 AI 個人助手這麼大的權利嗎？
- 他是不是真的會有資安風險？
- 被打進去之後，個人的數位資產會不會有問題？

## 四層縱深防禦：打造安全的個人 AI Agent

我參考了網路上很多資安大神的文章，做了一些實驗，最後整理出四層式縱深防禦策略：

### 第一層：Isolation（隔離）——最重要

**核心原則：你必須認可它是一個可被犧牲的。**

當你架好的那一天，就要預設他會被打進來，而且他一定會被打進來。

這情況下：
- 裡面放的所有檔案、所有 Key，都必須是真的丟了也無傷大雅的
- 上面用的 LLM 或 API，**竭盡所能必須用吃到飽的**，不是按需的
- 不然被駭客玩的時候，你的錢一下子就會損失很多

這就是為什麼大家一窩蜂買 Mac mini——把它當作一個能夠犧牲的東西，真的出問題頂多損失那部分。

**控制爆炸半徑。**

### 第二層：Quarantine（隔離區）

怎麼區分信賴的 Input？

- 透過 Telegram、Slack 給的 Input 應該是比較可信的
- 如果有其他管道進來的 Input，必須要像隔離一樣處理

### 第三層：Rollback 機制

OpenClaw 是非常新的 Open Source Project，程式還是非常不穩定。

你隨時可能要幫他做 Patch，或他自己推出 Patch。所以要：
- 定期把狀態記錄下來
- 有定期能夠 Rollback 的機制

### 第四層：可視化監控

當 AI 對外 Access 服務或要把東西傳出去時：
- 設一些反向 Firewall
- 第一時間通知你

有了這樣的防禦，我們就可以去探索個人 AI 助理的邊界。

## 兩條路線的殊途同歸

我們看到兩條路線，都在逼近 Agent 2.0 的甜蜜點：

### 左邊：Claude Code 正規軍

- 有很好的核心：Claude Opus 4.5
- 搭上全世界最好的界面：Command Line
- 在上面打造生態系：Hook、Skill、MCP
- 在絕對安全的基礎上，慢慢從半自動往 70%、80% 自動推進

**問題：** 推進過程有時候不夠快。有些是因為 IPO 他們選擇性不做。

**解決方案：** 開源社群透過不同的 Plugin（Hapy、Ruff、Weekend 這樣的 Task 機制）來幫助 Claude Code 貼近甜蜜點。

### 右邊：OpenClaw 開源游擊隊

- 從一開始就知道要做全自動的個人 AI Agent
- 因為是一人公司、開源專案，完全不怕相關限制
- 在探索個人助理的邊界
- 從完全自由的開源專案，慢慢進行加固

當他已經非常好用的時候，其他開源社群就會蜂擁上去，幫他做很好的安全加固。

## OneFlow Paper：為什麼 Single Agent 夠用

這週出的 OneFlow Paper 也在證明這個思路：

**與其搭建那麼多 Multi-Agent 架構，還不如放一個夠好的 AI Agent，然後把中間的狀態傳遞都放在一個比較好的 KV Cache Storage。**

只要這個 AI Agent 的 Model 夠聰明，他就能夠善用 KV Cache 的 Persistent Storage，把不要的上下文放在 KV Cache，再透過一個創意發想者、一個 Reviewer、一個蒙地卡羅搜尋的探索模式，大幅度改進。

我們真的不需要那麼多 Agent 來打造生態系。這有點太複雜了，有點 Over Design。

**這就是 Claude Code 之前會那麼強力的原因。** 雖然沒有 KV Cache 配合的概念，但他把大部分上下文都盡可能落地到 Local，變成 MD 檔。像是 Claude Code 的 State 一樣。

OpenClaw 也在做一模一樣的事情，甚至更極端——把大量上下文放在幾個重要的 MD 檔裡面，每天的記憶用日期來做擺放，放在 Folder Structure 裡面。

就這麼簡單，但可以發揮非常好用的效果。

## 坦白說

這週其實我本來沒有想要講 OpenClaw，只是想講 Claude Code 然後介紹一些相關 Skill。

但因為在一個非常關鍵的時間點出現這件事情，所以改變了題目。不過我認為這反而讓整個話題更加升華了。

**不確定的部分：**
- 最終的 Sweet Spot 會是什麼，到最後可能也不會有完美解答
- 可能是 Enterprise 走 Claude Code 這條線，個人走 OpenClaw 路線
- 我文章裡的安全建議大部分是參考網路上社群大神們講的東西

**確定的部分：**
- 兩條路線殊途同歸
- Command Line + LLM 是天作之合
- Single Agent + 好的 Context Management 比 Multi-Agent 更有效率（至少在個人助理場景）

## 關鍵洞察

1. **Unix 哲學的復興：** 20 年前的「Command Line 是最好的 GUI」預言成真，LLM 跟 CLI 是天作之合

2. **安全 vs 自由的取捨：** Claude Code 選擇安全優先慢慢開放，OpenClaw 選擇自由優先再慢慢加固——兩條路最終會在中間相遇

3. **可犧牲性原則：** 如果你要用 OpenClaw 這類全自動 Agent，第一條原則就是「預設它會被打進來」

4. **Single Agent 足矣：** OneFlow Paper 跟實踐都證明，一個夠聰明的 Agent + 好的 Context Management，比複雜的 Multi-Agent 架構更有效

5. **2026 年格局：** 個人 AI Agent 的競爭將定義今年 AI 應用的走向

---

## Q&A

**Q: OpenClaw 現在可以安全使用嗎？**

經過幾天的快速迭代，預設值已經改成安全模式。但如果你要用，強烈建議實施四層防禦策略，特別是「預設它會被打進來」的心態。

**Q: 企業應該選 Claude Code 還是 OpenClaw？**

企業走 Claude Code 這條線比較穩妥——有官方支援、合規性有保障、安全性優先。OpenClaw 比較適合個人探索或願意承擔風險的進階用戶。

**Q: 為什麼大家在買 Mac mini？**

因為可以把它當作一個「能夠犧牲的」設備。真的出問題頂多損失那一台，不會影響到你的主要工作環境和數位資產。

**Q: Multi-Agent 真的沒用嗎？**

不是沒用，而是在個人助理這個場景下，Single Agent + 好的 Context Management 更有效率。在複雜的企業流程或需要專業分工的場景，Multi-Agent 可能還是有其價值。

---

**延伸閱讀：**
- [OpenClaw 四層縱深防禦加固指南](/moltbot-security-hardening-guide/)
- [Unix 哲學在 Claude Code 的復興](/unix-philosophy-claude-code-command-line-renaissance/)
- [OneFlow：Single Agent vs Multi-Agent 重新思考](/oneflow-single-agent-vs-multi-agent-rethinking/)
- [從「套殼 1.0」到「套殼 2.0」：為什麼真正該緊張的是 Anthropic](/shell-wrapper-2-anthropic-real-threat/)
- [Cursor 前 0.01% 大神倒戈 Claude Code：Agentic Coding 五大支柱完整解析](/cursor-top-user-switch-claude-code-agentic-coding/)
