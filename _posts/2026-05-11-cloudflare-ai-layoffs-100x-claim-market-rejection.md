---
title: "Cloudflare 砍 20% 人喊 AI 100x 生產力，股價跌 23%——市場第一次 punish「AI 取代人」這個故事"
date: 2026-05-11 08:00:00 +0800
permalink: /cloudflare-ai-layoffs-100x-claim-market-rejection/
image: /assets/images/cloudflare-ai-layoffs-cover.png
description: "Cloudflare 5/7 公告砍 1,100 人（20%），CEO Matthew Prince 喊「AI 帶來 2x、10x、even 100x 生產力」，「就像從手動螺絲起子換到電動的」。隔天股價跌 23%。但弔詭的是：2026 上半年同樣劇本天天有——Block 2 月砍 40%、Oracle 3 月砍 30,000、Meta 4 月砍 8,000——而且 Block 公告當日股價 +24%、Oracle 也只是微跌。同一個 AI 故事 template，Block +24% vs Cloudflare −23%，差了 50 個百分點，差在哪？答案是：市場不是反 AI 裁員，是在挑哪家故事對得起來。Block 故事配 EBITDA 改善、Oracle 故事配 $156B capex，兩家數字對齊；Cloudflare 講 100x productivity 卻保留所有 sales、Q1 record high 卻砍 20%，三條都不一致。我自己跑 ATPM 在 production 拿到 40% 加速、QA 階段預期 80% 結果只有 20%——有單位、有 caveat 的 40% 比沒單位的 100x 可靠 100 倍。本文用 2026 全球裁員時間線拆解三個訊號：100x claim 的數據破綻、sales 倖存的結構矛盾、以及為什麼市場現在會挑魚而不是反潮。"
---

# Cloudflare 砍 20% 人喊 AI 100x 生產力，股價跌 23%——市場第一次 punish「AI 取代人」這個故事

## 一封很漂亮的內部信，跌掉 23%

2026-05-07，Cloudflare CEO Matthew Prince 在公司部落格貼了一篇文章，標題叫「Building for the future」。內容大意是：公司要為 agentic AI 時代重新架構，所以要砍掉約 **1,100 人，佔員工 20%**。

這封信寫得很漂亮。

Prince 強調 AI 在公司內部的使用量近三個月成長 **600%**，工程、HR、財務、行銷每天跑「上千個 AI agent sessions」。他舉了一個比喻——「就像從手動螺絲起子換到電動的」（_It was like going from a manual to an electric screwdriver_），講團隊裡有人「比過去生產力高 2 倍、10 倍、甚至 100 倍」。被裁的人會領薪水到 2026 年底、健保到年底、equity 繼續 vest 到 8/15。一年期 cliff 也 waive 了。

很標準的「AI 重塑未來、好聚好散」劇本。

問題是：公告隔天，Cloudflare 股價跌了 **23%**。

而這一季的數字其實是漂亮的——營收 $639.8M、年增 34%、單季 record high、EPS beat 分析師預期。**這不是一家虧錢的公司在裁員。** 這是一家剛剛交出 record high 的公司，砍了 20%，講了一個 AI 故事，然後被市場拿去蓋章 −23%。

過去三年我們看了太多劇本：Meta 砍 21,000、Microsoft 砍 10,000、Amazon 砍 27,000、Salesforce 砍 7,000，每一次都同時嘴 AI 加速、自動化、productivity gain。每一次股價基本都漲。

這次第一次反過來。我覺得這個 23% 比那 1,100 人更值得寫。

## 「100x productivity」這個數字，我每次看到就頭痛

先講一個我自己的數字。

過去兩年我在實戰場跑 ATPM（Assessment / Testing / Program / Management）這套 AI coding 流程，量化下來的真實加速是：**40%**。

不是 100x、不是 10x、是 0.4 倍——把開發週期壓掉 40%。

而這 40% 已經是業界少數有人敢拿出單位、有對照組、有方法論去揭露的數字。同時間我也誠實寫過：QA 驗收階段，我原本期待 AI 帶來 80% 加速，**實際只有 20%**。PRD 文件平均要迭代 6-7 輪、AI 寫出來的 code 準確度 85%、PRD 跟最終 code 行數比是 1:1.4。

我講這些不是要 humble brag，是要對比——當 Prince 講「2x、10x、even 100x」的時候，我希望你跟我一起問三個問題：

1. **單位是什麼？** 是寫程式速度？bug 修復速度？支援 ticket 解決速度？還是「我用 ChatGPT 寫了一個 email」的那種「快了一百倍」？
2. **對照組是什麼？** 比的是同一個人一年前、還是業界中位數、還是某個特定情境下的 best case？
3. **如果是真的，剩下 4,400 人營收為什麼只成長 34%？** 100x 應該對應到的是營收爆增、產品線爆增、研發進度爆增。Cloudflare 的 Q1 是漂亮的 34%——但那是「一家正常成長的雲端公司」的數字，不是「一家剛剛 unlock 100x productivity 的公司」應該交的數字。

如果一家公司真的解鎖了 100x productivity，**它應該在加人不是砍人**，因為每個邊際人力的產出是百倍。

Prince 自己其實有意識到這個矛盾，所以他補了一句：「我猜 2027 年我們會比 2026 任何時候員工數都更多。」這句話拆解開——**「我現在砍 1,100 人，但我相信明年我會再僱回比現在更多」**——本身就在暗示：今天砍的不是因為 AI 取代了這些角色，而是因為現金流 / 組織重組 / 結構調整。AI 是 narrative，不是 cause。

市場聽出來了。

## 真正不對勁的訊號：所有人都砍，留下 sales

如果你只看到 100x 我覺得已經很糟。真正讓我覺得這劇本不對勁的，是 TechCrunch 揭露的一個細節：

> 裁員影響「所有部門和所有地區，**除了背 quota 的業務以外**」。

停在這句話想一下。

如果你真心相信 agentic AI 已經可以取代大量工作——那 sales 是第一批該砍的。我這樣講不是 troll sales，是看實際工作組成：

- Demo：可以用 AI agent 自動 walkthrough、按客戶問題客製內容
- Cold email / 開發信：早就是 AI 戰場
- CRM 更新、會議記錄、follow-up：100% 機械化、AI agent 跑得比 SDR 還勤
- Pricing 計算、合約初稿、proposal 整理：LLM 強項
- Lead qualification、客戶意圖分析：AI 領先人類太多

Sales 工作裡能被 AI 替代的比例，**不會比 support / customer success 低**。Support 還要處理大量未知技術問題、要查文件、要重現 bug。Sales 處理的反而是相對結構化的對話與流程。

那為什麼留 sales 砍 support？

因為這跟 AI 沒關係。**這是「revenue-attached 留、cost-attached 砍」的傳統公司決策**——只是這次披了一件 AI 的外套。

Sales 帶 quota，每個人對應一條可量化的營收。砍他們，營收會掉，下一季數字會難看。Support 跟 CS 是成本中心，砍掉短期成本下降、毛利上升，季報好看。從財務模型看完全合理。

但你不能一邊做「砍成本中心、保營收中心」這個傳統 CFO 決策，一邊講「我們正在進入 agentic AI 時代」。**這兩個故事互相矛盾。**

如果 AI 真的 100x，那留 sales 等於浪費資源——你應該砍掉 80% sales、用 AI agent 取代他們的重複勞動，把預算放到那些「比過去高 100 倍生產力」的 R&D 人才身上。

但 Cloudflare 沒這樣做。Cloudflare 做的是「砍 support、留 sales、嘴 AI 故事」——這跟 2010 年代任何一場非 AI 裁員一模一樣。

市場看見了，所以打 23%。

## 為什麼這次劇本不靈了：市場開始要 evidence

過去三年的劇本是這樣的：

**「我們砍了 X 人，因為 AI 帶來了 productivity gain」→ 投資人 OK → 股價漲**

Meta、MS、Amazon、Salesforce、Google 都這樣做過，沒有一家因為這個故事被打。原因很簡單：那個時候 AI 還是 emerging narrative，投資人傾向 **benefit of the doubt**——你說你的人變生產力 2 倍我就先信，反正 AI 是 trend，不投這個故事我會錯過。

但是 2026 年的投資人不一樣了。經過三年看大模型發布、看 AI Copilot 滲透到每個 SaaS、看 Agentic AI 從 demo 到 production，他們累積了一個基準線：**「AI 確實有用，但 100x 是 bullshit」**。

機構投資人現在會問：

- 你說的 2x / 10x / 100x，是哪個團隊、哪個任務、哪個時期？
- 你砍掉 1,100 人原本做什麼？AI agent 已經接得起來這些工作了嗎？
- 如果 agent 真的可以，為什麼你的 Q2 guidance 沒有 reflect 任何 margin expansion？
- 為什麼留著 sales——你自己都不夠相信你的 AI 故事？

Prince 給出的回答其實已經暴露了。當分析師直接問他：「為什麼業績這麼好的一季要砍這麼深？」他的回答是：

> _"Just because you're fit doesn't mean you can't get fitter."_

這是一句政治正確、毫無資訊量的話。你 fit、你想 fitter，OK——那 fit 在哪、fitter 之後變多 fit、付出的代價是什麼，沒講。這是企業溝通最敷衍的版本。

23% 是市場給這句話的標價。

## 但 Cloudflare 不孤單——為什麼偏偏它被罰？

寫到這裡可能有人想問：可是 2026 上半年「AI 重組」公告幾乎每週都有，為什麼只有 Cloudflare 跌？

來看 2026 年到目前為止的全景：

| 月 | 公司 | 裁員規模 | 比例 | 官方理由 |
|---|---|---|---|---|
| **5** | **Cloudflare** | ~1,100 | **20%** | AI 重組 |
| 5 | Coinbase | ~700 | 14% | AI 自動化與降本 |
| 5 | PayPal | ~4,500+（未來 2-3 年） | 20% | 長期重組 |
| 5 | Estée Lauder | 9,000–10,000 | — | 擴大重組 |
| 4 | Meta | ~8,000 | 10% | 公司級裁員 |
| 4 | Snap | ~1,000 | 16% | 廣告業務壓力 |
| **3** | **Oracle** | **~30,000** | **~18%** | AI 雲轉型（$156B capex） |
| 3 | Atlassian | ~1,600 | 10% | AI 重構 |
| 3 | Morgan Stanley | ~2,500 | 3% | 華爾街降本 |
| **2** | **Block** | **超 4,000** | **接近 40%** | AI 自動化 |
| 2 | Heineken | 最多 6,000 | ~7% | 全球優化 |

注意兩個極端：

- **Block 砍 40%、股價 +24%**。Jack Dorsey 直白寫給股東：「intelligence tool capabilities are compounding faster every week」，CFO Amrita Ahuja 補：「我們看到用更小、更精的團隊配合 AI 加速的機會」。市場買單，股價當日漲 24%。
- **Cloudflare 砍 20%、股價 −23%**。Prince 講 100x、講 600% AI usage、講「manual to electric screwdriver」。市場不買單。

同樣 template、同樣 AI 故事、同樣 2026 上半年——一家被 reward 24%、一家被 punish 23%，差了將近 50 個百分點。差在哪？

我認為差在三件事：

**1. 故事跟財務數字要 self-consistent。**
Block 講「更小、更精的團隊」——它的毛利率本來就承壓，砍 40% 對應到 EBITDA 立刻有結構性改善，故事 = 現金流改善路徑。Oracle 講 AI infrastructure——它公開承諾 $156B 在 GPU 跟 data center capex，砍 30,000 人省下的 $8-10B 年現金流直接灌進 AI 投資，故事 = capex 對齊。**Cloudflare 講「AI agentic 重組」，但 Q1 是 record high、毛利沒承壓、capex 沒爆增——故事跟財報對不上**，市場看不出這 1,100 人省下的錢要去哪裡。

**2. 砍的部位要跟故事一致。**
Block 是 across-the-board 砍 40%、含 sales、含管理層。Oracle 砍的是 legacy software maintenance、on-prem support、SaaS/Virtual Operations Services（這兩個部門各砍 30%），同時 OCI / AI services 部門在 hiring——非常清楚的「砍舊保新」。**Cloudflare 砍所有非 sales 部門、保留所有 sales**——說自己 going agentic，但留下整個最 human-process-heavy 的銷售流程。砍的部位跟故事相反。

**3. 數字要有單位，或者乾脆不給。**
Block 全程沒講任何 productivity multiplier，講的是「compounding faster every week」這種定性 framing。Oracle 完全不提生產力，講的是 capex 跟 data center。這兩家都避開了量化陷阱。**Cloudflare 給了 2x / 10x / 100x——一旦你說了數字，市場就會比對你下一季 EPS、margin、revenue per employee**。給不出來就破功。

換句話說，**市場不是反 AI 裁員潮，市場是在挑魚**。Block 故事有 internal consistency、Oracle 用真金白銀對齊、兩家都過關。Cloudflare 三條都沒對齊，被挑出來罰。

潮水沒退，只是濾網變細了。

## 那我們一般人怎麼辦

對，我們一般人能夠做的事情其實很有限。

一樣的就是好好的重啟，好好的把自己轉變成一個在 AI 時代最適合的人。然後就是隨時把自己當作一個一人公司，好好去看待這件自己的相關規劃。

## 常見問題 Q&A

**Q: 你是說 Cloudflare 不該裁員嗎？**

不是。一家公司決定如何配置人力是 CEO 的職責，外人沒立場評。我評的是「裁員的解釋故事」——把 cost cutting 包裝成 AI replacement，這個包裝在 2026 不再有效。誠實說「我們在重組成本結構」反而會被市場接受。

**Q: 那 40% vs 100x，誰才是真實的？**

兩個都是。40% 是我自己 production 場景的 measured outcome，有單位、有對照組、有方法論。100x 是某個 best-case scenario 下某個任務的 reported feeling，可能在那個情境下是真的，但**不能 generalize 到「公司整體 productivity」**。Prince 把 best-case 拿來支撐 company-wide 決策，這是 measurement 紀律的問題。

**Q: 那企業要怎麼 measure AI productivity 才不會犯這個錯？**

最低標準三件事：(1) 講清楚單位（行數？週數？story point？ticket？），(2) 提供對照組（同團隊半年前 / 不用 AI 的對照組 / 業界 median），(3) 公布 caveat（哪個階段加速最多、哪個階段沒幫助、PM / QA / DevOps 各拿到多少）。沒有這三件事的 productivity number，不管多漂亮，都只能當 sales pitch 看。

**Q: 你看好 Cloudflare 嗎？**

我看好它的產品，不評論股價。Cloudflare 的 edge network、Workers、R2 都是技術上極強的產品線。這次的問題在 communication 跟 measurement framework，不在產品。如果他們之後願意公布更細的 productivity measurement methodology，我會收回對這次 100x claim 的質疑。
