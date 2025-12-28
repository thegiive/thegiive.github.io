---
layout: post
title: "AI 時代，還需要數據分析師嗎？AI 分析 vs 人類決策的關鍵差異"
date: 2025-11-26 08:30:00 +0800
permalink: /notebooklm-trust-fde/
image: /assets/images/notebooklm-trust-fde-cover.png
description: "AI 工具讓數據分析成本趨近於零，但企業真的因此不需要數據分析師了嗎？本文用真實物流專案，拆解 NotebookLM、Claude Code 與「信任建立」之間的關鍵落差。"

---

**結論先講：AI 讓分析變便宜，但讓人願意照數據行動，仍然需要人。**

---

## 物流的某一天

今年我帶 FDE 團隊進了一個物流優化專案，客戶是國際級客戶（這家你一定用過）。
第一次會議，我很興奮地用 [Claude Code](https://claude.com/product/claude-code) 分析一堆 Excel，30 分鐘內產出十大建議。結果總經理說：「你的公式給我看一下，我要驗算邏輯。」

我解釋這是 Python 算的，不會有 AI 幻覺亂算的問題。(總經理IT出生, 可以直接講技術語言)

他回：「我不在意是不是 Python或是 AI ，我在意每一個參數的意義。對我來說，人力配置錯誤就是錢——人太多明天損失一筆，人太少客戶馬上罵。」

「我寧願你用慢的工具，但讓我打開公式一個一個驗算，我要對結論負責任。」

![Excel 公式驗算 - 總經理要求的透明度](/assets/images/excel-formula-verification.png)

---

## 解決方式

於是我們做了一個巨大的 Google Sheet。 接下來一百天，週一到週日(你沒看錯, 物流沒有週末休息) ，每天早上 8:00-9:00 雷打不動線上會議，我全程參加。

我的FDE團隊跟管理層、現場團隊討論每一個數據的意義。有現場人員參與，增加很多對數據意義的解釋，另外是為了爭取他們支持——讓他們理解我們追求這些數據的原因，支援判斷下的決策。

這就是「信任」建立的過程。

不只是信任[我們 FDE 團隊](https://ai-coding.wiselychen.com/fde-continuous-experiment/)，而是讓現場信任這個數據。這樣他們才會根據 insight 去「改變行為」。

---
## 真正有用的指標是磨出來的

期間我們用 AI 生出上百個監測指標。國際級客戶也派了好幾組印度人物流團隊，用他們的經驗告訴我們該看什麼。百日後，我們淘汰掉 99%，只留下幾個 key index 去優化營運。

結果？P&L 報表有超級明顯的改進。AI 在裡面扮演很巨大的功用，主要是數據清洗，[整理，data exploration ...etc ](/chatgpt-atlas-grafana-debug/)）

但這 1% 的 key insight，不是「客戶的國際級分析師」產生的，也不是「AI」產生的。是現場，管理層，FDR團隊這一百天的站會磨出來的。因為我們產生的 insight，不只是AI 工具輸出——而是現場人員「信任」這些 insight，願意跟著「做相應的行動改進」。

![現場團隊站會 - 信任是在倉庫裡磨出來的](/assets/images/warehouse-team-standup.png)

---

## AI 時代，數據分析師真正不可被取代的是什麼？

教科書說數據分析是：Data ETL → BI Dashboard → Data Insight → Real Action

AI 的誕生及大幅度地讓前三步幾乎 0 成本就可以產生。
但如果沒有 Real Action，前面三步做得再好都是無意義。

看到現在社群網路上，自從 [NotebookLM](https://notebooklm.google.com) + Gemini 3 Pro 出現，瞬間許多專家產生大量商業簡報跟insight，我又想起那一百天。

我們誕生在一個有海量的 insight 跟報表的年代
但是 AI 用黑盒子產生的 insight , 到底能拿到多少客戶的信任

** 但到底哪一個，能讓現場真的動起來？ **

![現場動起來 - 堆高機在高架層作業](/assets/images/warehouse-forklift-action.png)

---

## FAQ：AI 與數據分析師

**Q：NotebookLM 這類AI工具 可以完全取代數據分析師嗎？**

不行。NotebookLM 能快速整理資料、產生摘要與 insight，但無法建立「讓決策者願意承擔風險並行動」的信任關係。企業場景中，數據分析師的核心價值在於責任鏈的建立，而非報表產出。

**Q：Claude Code 做數據分析有什麼限制？**

Claude Code 能在 30 分鐘內完成傳統需要數天的 ETL 與 data exploration 工作，但產出的 insight 仍是「黑盒子」。對於高風險決策（如人力配置、資源調度），決策者需要能驗算邏輯、追溯每個參數意義，這是 AI 工具目前無法提供的透明度。

**Q：AI 時代，數據分析師該如何轉型？**

從「產報表的人」轉型為「建立信任的人」。AI 能產生海量 insight，但讓現場願意照著數據行動，需要人去溝通、解釋、承擔責任。未來的數據分析師更像是「數據翻譯官」——把 AI 產出轉化為可被信任、可被執行的決策依據。

**Q：是不是只要簡報做得漂亮，數據正確性就不重要？**

這要看客戶。有讀者分享：他跟客戶解釋 EDM 開信率數據準確性很低，資訊部也認同，但最後輸給了「簡報做得美美的」競爭對手。另一次他只帶白板筆和便利貼去簡報，反而贏了。關鍵不在工具精美與否，而是「被客戶理解並認可的東西才會有價值」。B2B 成交與否真的是 case by case，但掌握 key decision maker 的信任永遠是核心。

**Q：AI 產出的數據會不會有錯？人工驗算還是必要的嗎？**

會。有讀者分享抓過 IT 改演算法後正負號放錯、數字拋轉時 1 變 5 之類的問題。這不是 AI 特有的問題，任何自動化流程都可能出錯。所以我的做法是：先用 Excel 初估建模，確認邏輯正確後，再用更進階的工具（Claude Code、Python）擴大處理。人工驗算在高風險決策場景仍然必要。

---

## 延伸閱讀

- [AI Agent 完整指南：從架構設計到企業安全落地](/ai-agent/) — 想深入了解 AI Agent 如何在企業場景落地
- [ChatGPT Atlas + Grafana：30 分鐘 Debug 變 1 分鐘的實戰](/chatgpt-atlas-grafana-debug/) — AI 加速技術 Debug 的真實案例
- [AI 時代的面試：我不考 coding，只問為什麼](/ai-era-interview-why-not-coding/) — 工作角色轉變下的人才觀
