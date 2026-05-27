---
layout: post
title: "AI 打仗的文章滿天飛，但你看到的「細節」九成是編的"
date: 2026-03-02 09:00:00 +0800
categories: [AI治理]
tags: [AI War, Media Literacy, Misinformation, Iran, Palantir, Claude, Critical Thinking, JADC2]
permalink: /ai-iran-war-fake-analysis-media-literacy/
image: /assets/images/ai-iran-war-fake-analysis-cover.png
description: "美伊戰爭開打後，各種「AI 如何主導斬首行動」的深度分析文滿天飛。問題是——仗還沒打完，你怎麼可能知道用了什麼模型、什麼平台？這不是分析，這是創作。七分真、三分編，是 AI 時代最高級的假訊息手法。"
---

![AI 戰爭假分析文章截圖](/assets/images/ai-iran-war-fake-analysis-cover.png)

**作者：** Wisely Chen
**日期：** 2026 年 3 月 2 日
**系列：** AI 治理
**關鍵字：** AI War, Media Literacy, Misinformation, Iran, Palantir, Claude, JADC2, Critical Thinking

---

## 目錄

- [今天早上看到的東西](#今天早上看到的東西)
- [AI 進入戰爭，這件事是真的](#ai-進入戰爭這件事是真的)
- [但那些「深度分析」，基本上是假的](#但那些深度分析基本上是假的)
- [一個簡單的判斷框架](#一個簡單的判斷框架)
- [真正該擔心的事](#真正該擔心的事)
- [坦白說](#坦白說)

---

## 今天早上看到的東西

今天早上滑手機，看到好幾篇文章在講「AI 如何打贏伊朗戰爭」。

內容看起來非常有料。其中一篇的開頭是這樣寫的：

> 今天，德黑蘭北部的謝米蘭區籠罩在一種極度不安的靜謐中。對於伊朗最高領袖阿亞圖拉·阿里·哈梅內伊而言，這種靜謐通常意味著安全，但在這一天，它成了死亡的前奏。

然後給了一個行動代號叫「史詩憤怒行動」（Operation Epic Fury），描述得像電影劇本一樣：

> 這場行動的標誌性意義在於，它是人類歷史上第一次由人工智能（AI）多輪輔助「殺傷鏈」（Kill Chain）的高層斬首行動。在德黑蘭的指揮部裡，哈梅內伊或許認為自己躲過了衛星，但他沒有意識到，他面對的不是單一的武器，而是由帕蘭提爾（Palantir）、安杜里爾（Anduril）和頂級大語言模型（Claude）共同構成的全球性監控與打擊網絡。

文章裡面什麼都有——Palantir 的「本體論」（Ontology）技術、前線部署工程師（FDE）在後台調整 MetaConstellation 衛星調度邏輯、SpaceX 星盾（Starshield）的 480 顆專用加固衛星、200 Gbps 的激光星間鏈路、Shield AI 的 Hivemind 自主飛行系統⋯⋯

甚至還有表格：

> | 功能 | 核心技術支撐 |
> | Gotham | 語義網、知識圖譜、關聯分析 |
> | AIP for Defense | LLM 集成、RLHF、受控邏輯代理 |
> | MetaConstellation | 邊緣 AI、自動任務分解、軌道管理 |
> | TITAN | 傳感器融合、多域數據同步 |

我看完的第一個反應：哇，寫得真好，真專業。

第二個反應：**等等，這不可能。**

---

## AI 進入戰爭，這件事是真的

先講清楚：我不是要否認 AI 在這場戰爭中扮演角色。恰恰相反，**AI 進入軍事場景，這件事是百分之百可信的。**

證據鏈其實很明確：

**第一，Anthropic 與五角大廈的衝突是真的。** 就在幾天前（2 月 27-28 日），Trump 政府因為 Anthropic 拒絕移除 Claude 的軍事使用限制，直接把 Anthropic 列為「供應鏈風險」（Supply Chain Risk），禁止所有聯邦機構使用。國防部長 Pete Hegseth 給了 Dario Amodei 一個最後通牒——週五下午 5:01 前同意條件，否則動用《國防生產法》。

這件事我在[之前的文章](/anthropic-pentagon-supply-chain-risk-ai-ethics-redline/)詳細寫過。

**第二，OpenAI 立刻補位。** Anthropic 被封殺的同一天，Sam Altman 宣佈 OpenAI 與五角大廈簽約，提供 AI 工具用於軍方機密系統。

**第三，Palantir 在軍事 AI 的深度參與是公開資訊。** Palantir 的 Foundry/Gotham 平台早就是美軍的核心分析工具，他們在 Gaza 的人道援助追蹤中的角色也已經被 [Drop Site News 報導](https://www.dropsitenews.com/p/palantir-ai-gaza-humanitarian-aid-cmcc-srs-ngos-banned-israel)。

**第四，從這次斬首行動的精準度來看。** 能夠掌握伊朗最高領導人的即時位置並執行定點清除，背後一定有大量的情報整合、衛星監控、信號分析。AI 在這些環節扮演角色？幾乎可以肯定。

所以 AI 在這場戰爭中有沒有用？當然有。美國國防已經進入 AI 時代，這是沒有疑問的。

---

## 但那些「深度分析」，基本上是假的

問題在於：**你怎麼知道那些具體的技術細節？**

這篇文章寫得非常專業，非常有說服力。它告訴你 Claude 的政府版「在處理海量截獲的波斯語機密文件方面表現卓越」，告訴你以色列的「薰衣草」系統「標記了 3.7 萬個目標」，甚至還引用了一個叫「爸爸在哪兒？」（Where's Daddy?）的系統——

> 它不像傳統雷達那樣追蹤飛機，而是追蹤目標與其家庭住所的關聯。系統會自動監控被標記人員何時進入家宅。指揮官認為，在這些人員回家與家人團聚時發起攻擊，比在軍事據點發起攻擊更為容易。

你看到這裡會覺得「天哪，AI 戰爭原來這麼可怕」。

**但是，整篇文章沒有任何一條可追溯的引用來源。零。**

它反覆提到「華爾街日報報導」、「據《華爾街日報》披露」、「據《衛報》披露」，但沒有給出任何一個連結、任何一個記者名字、任何一篇具體報導的標題。這是一個典型的 AI 生成內容的手法——用「據報導」三個字創造權威感，但背後什麼都沒有。

仗是 2 月 28 日開打的。今天才 3 月 2 日。

我問一個最基本的問題：**戰爭還在進行中，美國國防部怎麼可能透露這種等級的細節？**

- 行動代號叫什麼？不可能說。
- 他們用了什麼模型？不可能說。
- Palantir 的哪個子系統？不可能說。
- 安杜里爾的 YFQ-44A 怎麼「空中換腦」？不可能說。
- SpaceX 星盾有幾顆衛星、用什麼加密協議？不可能說。

這些東西，也許在事後覆盤、國會聽證、解密文件中會慢慢透露出來。但在**現在**這個時間點，你看到有人把這些細節寫得像親眼看到一樣——

> 正是 FDE 在後台調整了 MetaConstellation 的衛星調度邏輯，確保在目標離開地堡的一瞬間，有超過三顆衛星同時進行了交叉驗證。

**這就是編的。句號。**

---

## 一個簡單的判斷框架

不需要什麼媒體素養碩士學位，只需要問三個問題：

### 1. 時間合理嗎？

戰爭 2 月 28 日開打，文章 3 月 1-2 日就出來。軍事行動的技術細節解密通常需要數月甚至數年。72 小時內就有完整技術分析？**不合理。**

### 2. 有引用來源嗎？

正經的軍事分析會引用國防部發言人聲明、議員在聽證會的發言、匿名官員透過 WSJ/NYT 放的風。那篇文章反覆說「華爾街日報報導」「據《衛報》披露」「根據解密資料」，但你去找，一條具體的連結都沒有。**這叫假引用，不叫有來源。**

### 3. 細節精確到什麼程度？

「AI 有參與」——可信。
「用了 LLM 做情報分析」——合理推測。
「Claude Gov 版處理波斯語機密文件」——嗯，有可能。
「FDE 在後台調整 MetaConstellation 衛星調度邏輯，確保三顆衛星交叉驗證」——這種精確度，要嘛你在五角大廈上班，要嘛你在編故事。

猜猜哪個可能性比較高。

### 4. 寫作手法是否典型的 AI 生成？

這篇文章有幾個非常明顯的 AI 生成特徵：

- **假引用**：反覆說「華爾街日報報導」「據《衛報》披露」，但沒有任何一個具體連結
- **精確到不合理的數字**：「480 顆衛星」「200 Gbps 激光星間鏈路」「491 億美元風投」
- **完美的結構和表格**：每個段落都有小標題、表格、技術規格，像教科書一樣工整
- **文末免責聲明**：「本文不涉及任何時政觀點，純屬站在 AI 行業對本次襲擊的探討」——這句話本身就很 AI

真正的軍事記者寫的分析，不會這麼「完美」。

---

## 真正該擔心的事

這些編造文章之所以危險，不只是因為它們是假的。而是因為它們利用了一個**真實的趨勢**來編故事，這讓它們特別有說服力。

AI 確實在進入軍事領域。Palantir 確實是軍方的關鍵供應商。Anthropic 確實因為軍事倫理問題跟五角大廈翻臉。這些都是真的。

但在這個真實的基礎上，有人用 AI 生成了一篇看起來極其專業的虛構分析——從 Palantir 的「本體論」到安杜里爾的「空中換腦」到 Shield AI 的「蜂群意識」，加上精確到小數點的數字和漂亮的表格，讓你覺得「哇，原來 AI 打仗是這樣打的」。

更厲害的是，這篇文章還很聰明地混入了一些**真實的歷史資訊**——以色列在 Gaza 使用的「薰衣草」和「哈布索拉」系統確實被《+972 Magazine》和《衛報》報導過，「20 秒審查時間」也是真實的爭議。但作者把這些已知的 Gaza 資訊，無縫接到了這次伊朗行動上，創造出一種「一切都是連貫的」假象。

這是最高級的假訊息手法：**七分真、三分編。**

歐洲數位媒體觀察站（EDMO）已經把這場衝突稱為[「第一場 AI 戰爭」](https://edmo.eu/publications/the-first-ai-war-how-the-iran-israel-conflict-became-a-battlefield-for-generative-misinformation/)——不是因為 AI 主導了軍事行動，而是因為 AI 生成的假訊息在這場衝突中達到了前所未有的規模。

**諷刺嗎？最需要 AI 素養的地方，不是在寫程式，是在看新聞。**

---

## 坦白說

我自己也差點被騙。

你看那篇文章，從 Palantir 的 Gotham 平台講到 FDE 前線工程師，從 SpaceX 的星盾講到安杜里爾的 Lattice 系統，從 Shield AI 的 Hivemind 講到 Meta 的鷹眼頭顯，最後還來一段「三隻時鐘理論」做戰略反思——結構完美，術語精準，數據豐富，敘事流暢。

如果不是因為我前幾天才寫過 Anthropic 跟五角大廈衝突的文章，對時間線有清楚的認知，我可能也會轉發。

這就是 AI 生成內容最可怕的地方：**它不是粗糙的假新聞，它是精緻的虛構。** 它會給你表格、給你技術架構、給你戰略分析框架，甚至會在文末加上「本文不涉及任何時政觀點」的免責聲明，讓你覺得這是一篇客觀的技術分析。

我們這個時代需要的判斷力其實很簡單：

1. **看時間** — 事情剛發生，就有完整技術細節？大概率是編的
2. **看來源** — 沒有任何可追溯的官方來源？大概率是編的
3. **看精確度** — 細節精確到不合理的程度？大概率是編的

AI 時代不缺資訊，缺的是判斷力。

而這個判斷力，AI 幫不了你。得自己練。

---

## 延伸閱讀

- [週六資安日：當十年前美國隊長 2 的洞察計劃成了 2026 年的現實](/anthropic-pentagon-supply-chain-risk-ai-ethics-redline/) — Anthropic 與五角大廈衝突的完整分析
- [Trump admin blacklists Anthropic as AI firm refuses Pentagon demands](https://www.cnbc.com/2026/02/27/trump-anthropic-ai-pentagon.html) — CNBC 報導
- [OpenAI strikes deal with Pentagon hours after Trump admin bans Anthropic](https://www.cnn.com/2026/02/27/tech/openai-pentagon-deal-ai-systems) — CNN 報導
- [The First AI War: How the Iran-Israel Conflict Became a Battlefield for Generative Misinformation](https://edmo.eu/publications/the-first-ai-war-how-the-iran-israel-conflict-became-a-battlefield-for-generative-misinformation/) — EDMO 研究報告
- [Every Side Is Lying: A Guide To Iran Conflict Propaganda](https://www.thedupreereport.com/2026/03/iran-conflict-propaganda-guide/) — 伊朗衝突中的宣傳分析指南

---

**一句話總結：** AI 進入戰爭是真的，但那些告訴你「AI 怎麼打仗」的文章，大概率也是 AI 寫的。
