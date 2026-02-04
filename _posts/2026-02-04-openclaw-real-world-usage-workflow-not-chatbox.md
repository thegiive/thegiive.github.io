---
layout: post
title: "這幾天我密集使用小龍蝦 OpenClaw：為什麼我決定把它納入工作流"
date: 2026-02-04 10:00:00 +0800
permalink: /openclaw-real-world-usage-workflow-not-chatbox/
image: /assets/images/openclaw-real-world-usage-cover.png
description: "OpenClaw 給我的感覺，很像一個真人秘書，活人感很強。用了半天之後我決定將它納入我的工作流。從 TODO 記錄、發會議邀請、會議逐字稿、連公司內部系統、到幫我剪片——這才叫智能體呀。"
---

這幾天我密集使用小龍蝦 OpenClaw。

為何那麼著迷呢？

因為 OpenClaw 給我的感覺，很像一個真人秘書，活人感很強。

用了半天之後我決定將它納入我的工作流。

以下是我這幾天的秘書工作場景。

---

## 環境

1. 一個 GCP Linux VM
2. 一個最便宜的 Mac Mini，我真的買一個（因為要測 browser）

## 帳號環境

1. 一個全新 Google 帳號
2. 用這個帳號註冊一個 GitHub 帳號
3. 這個 Google 帳號下載 OAuth Key

---

## 場景 1：記錄 TODO

我自己的 TODO 其實長久以來是放在一個 Google Sheet 上。我之前的工作流是將東西記錄在多個地方，然後用 make.com 收集到 Google Sheet，現在有了小龍蝦，就直接跟它講，它就寫 Python 傳到 Google Sheet 上記錄起來了，寫順了就順便叫它寫一個 skill。這個幾乎一下子就上線了。

**具體用法：**

會議開到一半，跟小龍蝦說：
> 幫我記錄一下 TODO，跟 A 去找某人討論技術細節

---

## 場景 2：發會議邀請

既然有了秘書的 Gmail 帳號，我這週一開會到一半，講到要跟某業務開會，就突發奇想直接告訴小龍蝦要約某個人幾號開會，它 Google Calendar 會議邀請一下子就發出去了。我又嘗試一下，將幾個常開會的 PM email 放入 alias，小龍蝦也很快記錄這幾個人的暱稱，也發得出去會議邀請。

**具體用法：**

```
對話 1：小龍蝦，請將 Wisely 的 email: wiselyXXX@gmail.com 記住
對話 2：小龍蝦，請幫我約 Wisely 下週一 9 點會議
```

---

## 場景 3：會議逐字稿

這個就是丟錄音檔過去，然後它就很認份地下載 whisper large 去做逐字稿，然後自動做會議總結。太讚了，連 Plaud Note 都不用。

---

## 場景 4：連公司內部系統

接下來就是深水區了。我之前 Claude Code 寫好的去內部系統（非關鍵）的 skill，透過 GitHub 傳給它，然後它直接 run 這個 skill 抓下來文字數據，然後用 Nano Banana Pro 去產生圖表，然後還可以每天早上八點給我相關數據分析日報。連 n8n 都不用了 XD

**具體用法：**

> 小龍蝦，請幫我每天早上 8 點把 A 報表 Telegram 給我

---

## 場景 5：檢查文件格式

昨天 PM 問我幫她看一下某個專案文件，我那時沒帶電腦，就用 LINE 收檔案，Telegram 問：

> 小龍蝦，這個檔案幫我看一下有沒有 format 問題

然後另外一個 PM 找我看，他給我 Google Doc link，因為我 Mac 上面有設 Browser Relay，我就說：

> 小龍蝦，幫我去這個 link 看有沒有 A、B、C 問題

我那時候還想試試看能不能 comment Google Doc，結果它跟我說雖然它可以操控 browser，但是 Google Doc 的 iframe 藏得比較深，它無法作業。

---

## 奇怪用法：幫我剪片

其實這是第一個讓我著迷使用小龍蝦的場景。

我週日不是做好一個每週總結的 YouTube，我在跟親戚吃飯時，就問它：

> 我：小龍蝦，你會剪 short 嗎？
>
> 回答：可以，我可以幫你剪成 Shorts（9:16 直式）並輸出成可直接上傳的 mp4，但是你要給我檔案
>
> 我：YouTube link 拿去
>
> 回答：可以，我已經把這支 17:12 的影片抓下來、也把逐段時間軸的逐字稿（有 timestamp）跑出來了，接下來剪 Shorts 就很快。
>
> 我先幫你挑 3 個最適合剪成 Short 的段落（都有清楚的「一句話 hook」）：
>
> 1. **命令列是最好的 GUI**（為什麼 LLM + CLI 是天作之合）
>    - 00:12 → 01:00（約 48 秒）
>
> 2. **Claude Code = Agent 1.5，OpenClaw = Agent 2.0**（差在哪）
>    - 02:00 → 03:40（約 100 秒；可再縮到 45–60 秒）
>
> 3. **OpenClaw 的安全 nightmare + 四層防禦思路**（最有共鳴）
>    - 05:00 → 07:10（約 130 秒；可再縮到 60 秒）
>
> 你先回我兩個選項，我就按你的偏好輸出成可直接上傳的 9:16 mp4...
>
> （我現在已經在後台開始把第 1 支轉成 9:16 直式了；你選定後我就照同樣模板把剩下的剪完。）

**我最震驚的是最後一句話...**

不待命令，理解長官需求，直接開幹的部下真的是很可遇不可求的人呀...

當然，它第一次做得很爛...

> 我：太糟了，幫我重做 1，不要字幕，我原本檔案是直式的，直接擷取中間就好
>
> 小龍蝦：好的...

然後第二次就剪出接近完美的片...還上字幕。

到這邊為止，我只花了 10 分鐘，留下在熱炒桌前看著 Telegram 震驚的我。

---

## 結語

這幾天最大的轉變是：

**我不再把 AI 當成問答工具，而是當成「半全能，而且很厲害很主動的工作助理」。**

它真的很主動，很多時候還是要調一下。

但是你跟部屬講話，也是需要大量的討論的...

我現在已經養了兩隻...我打算給它們不同的作業...

這幾乎是一個 Digital Twin 等級的自己了。

**這才叫智能體呀。**

---

*題外話，本篇都是用走去 7-11 路上，傳語音過去給小龍蝦，小龍蝦幫我回傳 blog 草稿，然後我逐字修正，最後才在 Mac 上打的...*

---

## 延伸閱讀

- [OpenClaw 記憶系統全解析：SOUL.md、AGENTS.md 與高昂的 Token 成本](/openclaw-architecture-deep-dive-context-memory-token-crusher/) —— 深入拆解 OpenClaw 的架構設計
- [從 $1.16 億退休到 Agentic Engineering：Peter Steinberger 與 OpenClaw 的傳奇開發哲學](/peter-steinberger-agentic-engineering-just-talk-to-it/) —— OpenClaw 背後的人與哲學
- [OpenClaw 四層縱深防禦加固指南](/moltbot-security-hardening-guide/) —— 安全必讀
- [個人 AI 助手決戰週：Claude Code vs OpenClaw 殊途同歸](/personal-ai-agent-future-claude-code-vs-openclaw/) —— 兩條路線的比較
