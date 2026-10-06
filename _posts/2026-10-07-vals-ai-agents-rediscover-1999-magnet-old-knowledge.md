---
layout: post
title: "AI 做科研最狠的不是算力，是閱讀頻寬：Claude Agent 從 1999 年的論文裡挖出室溫磁性半導體"
date: 2026-10-07 09:00:00 +0800
permalink: /vals-ai-agents-rediscover-1999-magnet-old-knowledge/
tags: [Claude, Opus 5.5, Vals AI, AI for Science, 材料科學, 自旋電子學, 文獻探勘, Agent]
categories: [AI 觀點]
image: /assets/images/vals-ai-agents-rediscover-1999-magnet-old-knowledge-cover.png
description: "Vals AI 10 月 4 日公布，一組 Claude Opus 5.5 agent 花四天找下一代記憶體需要的室溫磁性半導體。自己從零設計的化合物做不出來，真正的答案是 1999 年就被化學家合成過的 KV[Cr(CN)6]，普魯士藍的同族。答案散在化學、計算物理、自旋電子學三個社群的論文裡 27 年，沒人接起來。這篇用這個案例談兩件事：AI 做科研的優勢是閱讀頻寬與跨學科的通才能力；但從 DFT 預測到能用的記憶體還很遠，比較實際的收穫是一個新工種的雛形——AI 考古科學家。"
author: Wisely Chen
faq:
  - question: "Vals AI 的 Claude agent 到底找到了什麼？"
    answer: "2026 年 10 月 1 日到 4 日，一組 Claude Opus 5.5 agent 用密度泛函理論（DFT，Density Functional Theory）計算，找到兩個室溫 Luttinger 補償磁性半導體候選材料：新設計的 YBaMnFeO₅，計算顯示它大概做不出有效的有序形式；以及 1999 年就被合成過的 KV[Cr(CN)₆]，預測能隙約 2.1 eV、自旋窗 2.6 / 1.6 eV，1999 年樣品實測磁序溫度 376 K。兩者都是計算預測，能隙和自旋分選都還沒有實驗量測。"
  - question: "為什麼說 AI 做科研最狠的是閱讀頻寬，不是算力？"
    answer: "這次研究用的是雲端 CPU，約 750 個計算 job，四天完成，不是超級電腦等級的算力。真正的突破來自閱讀：KV[Cr(CN)₆] 的相關知識散在 1999 年的化學論文、2008 年的計算物理論文、2025 年的自旋電子學論文裡，三個社群用不同的詞，沒有人同時讀過。agent 用新的 Luttinger 補償分類回頭重看已知材料，才把它們接起來。但閱讀頻寬大不等於讀全，這次 agent 漏掉了最接近的 2008 年前人論文，是外部讀者補上的。"
  - question: "KV[Cr(CN)₆] 離做成記憶體還有多遠？"
    answer: "還很遠。目前只有 1999 年的一份含水粉末樣品，無水晶體從未被報導；兩種計算方法對含水的影響結論不同；能隙、自旋極化都沒量過；能帶很窄，載子遲緩；室溫下磁序只完成約 60%。研究方提出的下一步是三個實驗：重做材料量組成與飽和磁化、X 光磁圓二色性（XMCD）與磁光量測、自旋解析光電子能譜（Spin-resolved Photoemission）。這些全部做完也只確認材料性質，離元件和量產還有很多步。"
  - question: "「AI 考古科學家」是什麼樣的工作？"
    answer: "指用 AI agent 拿新的分類或框架，重讀人類累積的舊文獻與舊資料，找出當年沒被注意到的連結。這個概念的前身是 Don Swanson 1986 年提出的「未被發現的公開知識」（Undiscovered Public Knowledge）。以 Vals 的案例，工序包括：人定方向、agent 重掃文獻、agent 用 DFT 鑑定並預先登記判死規則、審稿 agent 交叉驗證、人補漏與決定送實驗室。目前 agent 最弱的是文獻覆蓋率，需要人檢查。"
  - question: "Luttinger 補償磁體（Luttinger-compensated magnet）跟一般反鐵磁有什麼不同？"
    answer: "兩者淨磁矩都是零，沒有外漏磁場，可以塞得很密。一般反鐵磁的上下自旋原子環境相同，電子無法依自旋分開，難以讀寫資料；Luttinger 補償磁體的上下自旋原子位在不同環境（常是不同元素），能隙邊緣的電子會依自旋排好，可用在自旋電子學（Spintronics）。名稱來自 1960 年的 Luttinger 定理。衡量指標是自旋窗（Spin Window）寬度，要遠大於室溫熱擾動的大約 26 meV。  ---  *資料核對日期：2026-10-07。主要來源：Vals AI〈[Two Room-Temperature Antiferromagnetic Semiconductor Candidates](https://www.vals.ai/blogs/room-temperature-magnetic-semiconductors)〉（2026-10-04）、[compensated-magnet-ledger GitHub repo](https://github.com/spicylemonade/compensated-magnet-ledger)（含 BLOG.md、README、LEDGER 與兩份 agent 卷宗）、S. M. Holmes & G. S. Girolami, J. Am. Chem. Soc. 121, 5593 (1999)、P.-J. Guo et al., [arXiv:2502.18136](https://arxiv.org/abs/2502.18136)、D. R. Swanson, Perspectives in Biology and Medicine 30(1), 7–18 (1986)、[Prussian blue（Wikipedia）](https://en.wikipedia.org/wiki/Prussian_blue)、[Luttinger's theorem（Wikipedia）](https://en.wikipedia.org/wiki/Luttinger%27s_theorem)。本文未重跑任何計算，未獨立驗證 DFT 結果。*"
---

大約 1706 年，柏林一個顏料匠 Diesbach 意外做出一種深藍色，後來叫普魯士藍，被當成第一個現代合成顏料。它的結構是用氰基把鐵原子串成立方骨架，一種鐵接碳端，另一種接氮端。普魯士藍本身也是磁體，只是要非常冷，5.6 K 才有磁序。

1999 年，兩位化學家把骨架裡的兩種鐵換成釩和鉻，做出 KV[Cr(CN)₆]。這個版本在 103 °C 還維持磁性，論文登上 JACS。

2026 年 10 月，一組 Claude Opus 5.5 agent 把這個 27 年前的磁體認了出來：它可能正是下一代記憶體在找的那種磁性半導體。

從顏料到磁體，隔了將近 300 年；從磁體到記憶體材料候選，又隔了 27 年。骨架從頭到尾沒變，變的是人看它的框架：先是顏料，再是磁體，現在是自旋電子學材料。

**很多科研不是全新的發現，是老發現找到了新的用法。而這就是 AI 最擅長的事情。**

研究是 [Vals AI](https://www.vals.ai/blogs/room-temperature-magnetic-semiconductors) 10 月 4 日發表的，作者 Geby Jaff，全部計算和 agent 的工作卷宗都放在 [GitHub](https://github.com/spicylemonade/compensated-magnet-ledger)。這個案例裡，agent 自己從零設計的材料做不出來，真正的答案是從舊論文裡挖出來的。

我讀完的判斷是：**AI 做科研最狠的不是算力，是閱讀頻寬。** 人類幾百年累積的論文，沒有任何一個專家讀得完，更不可能跨領域讀。AI 在這個階段最大的價值，是當一個讀過所有故紙堆的通才，拿新的框架回頭重讀老發現，把不同學科橫向打通。

先講清楚：我不是材料物理專家，沒有重跑任何 DFT 計算。這篇是依 Vals 原文與 GitHub repo 的公開資料做的分析。

<nav class="post-toc" markdown="1">
**目錄**

* 目錄
{:toc}
</nav>

---

## 30 秒定位

| 項目 | 內容 |
|------|------|
| 發表 | Vals AI 部落格，2026-10-04，作者 Geby Jaff |
| 執行者 | 一組平行工作的 Claude Opus 5.5 agent；人類負責 "setting goals, directing the search, and deciding what to publish" |
| 期間 | 10 月 1 日到 4 日 |
| 算力 | Quantum ESPRESSO 7.5 跑在 Modal 雲端 CPU 上，這條線送出大約 750 個 job |
| 候選 1 | YBaMnFeO₅，agent 新設計，大概做不出有效的形式 |
| 候選 2 | KV[Cr(CN)₆]，1999 年已被合成，從舊文獻裡重新認出來 |
| 實驗量測 | 兩個材料的能隙、自旋分選都還沒有人量過 |
| 公開程度 | 61 條宣稱，其中 52 條可以直接從原始輸出重算 |

注意算力那一列。這不是一個超級電腦的故事，是雲端 CPU 跑四天。

---

## 要找的是哪一種磁鐵

MRAM 這類記憶體用電子的自旋方向（上或下）存資料。想像廣場上每人舉一面旗子，朝左或朝右：

- **鐵磁（ferromagnet）**：旗子全朝同一邊，遠處看得到旗海，也就是外漏的磁場。好讀，但會干擾鄰居、翻轉慢。
- **反鐵磁（antiferromagnet）**：兩兩抵消，遠看什麼都沒有，能塞得密、切換快。但朝左朝右的人長得一樣，讀不出資料。
- **Luttinger 補償磁體（LCM）**：一樣兩兩抵消，但朝左的穿紅衣、朝右的穿藍衣。遠看沒有磁場，近看分得出來。

業界想要的是第三種，而且要是半導體、在室溫以上維持磁性。目前唯一經中子實驗確認的絕緣 LCM，48 K 就失去磁序。2025 年 Guo et al. 預測的兩個候選，磁序溫度是 210 K 和 75 K，論文把「室溫」點名為待解目標。

---

## 論點一：最狠的不是算力，是閱讀頻寬

agent 走了兩條路，結果剛好說明這件事。

**第一條路靠算力：從零設計。** agent 設計了 YBaMnFeO₅，把錳和鐵排成立體棋盤格。紙上的成績很漂亮：能隙 2.35 eV，自旋窗 1.0 / 1.4 eV，校正後磁序溫度約 490 K。

但棋盤格在大約 950 K 就會亂掉，而合成這類氧化物要 900–1300 °C。做出來大概是一塊打散的晶體，效果全無。卷宗 10 月 2 日的狀態：

> "DOWNGRADED. Not a discovery claim."

**第二條路靠閱讀：回頭重看已知材料。** 失敗留下一條原則：兩種磁性位置的差異 "has to be enforced by strong chemistry"。帶著這條原則，agent 回頭翻已經存在的化合物。卷宗指出，已知在室溫以上有磁序的補償絕緣體至少有兩個，Ca–Si YIG（465 K）和 KV[Cr(CN)₆]（376 K），**都沒有被當成 LCM 分析過。**

KV[Cr(CN)₆] 是普魯士藍的同族：鉻抓氰基的碳端、釩抓氮端，每種金屬被化學鍵鎖在自己的位置。agent 算出能隙約 2.1 eV、自旋窗 2.6 / 1.6 eV，是室溫熱擾動（約 26 meV）的 60–100 倍。而且它不用證明做不做得出來，1999 年就做過了，實測 376 K（103 °C）仍有磁序。

算力設計出來的那個，死在做不出來。閱讀翻出來的那個，前人已經付過實驗成本。

把這個材料的身世排成時間軸，就看得出閱讀頻寬在補什麼：

| 年份 | 誰 | 領域 | 留下了什麼 |
|------|----|------|-----------|
| 約 1706 | Diesbach | 顏料 | 普魯士藍，這個骨架的祖先；本身也是磁體，要冷到 5.6 K |
| 1960 | Luttinger | 理論物理 | Luttinger 定理，後來成為這類磁體名字的來源 |
| 1999 | Holmes & Girolami | 化學 | 合成 KV[Cr(CN)₆]，376 K 有磁序，刻意讓兩種金屬的磁矩抵消 |
| 2008 | Middlemiss 等 | 計算物理 | 研究壓力下的磁耦合；圖上兩個能帶邊緣已是同一個自旋，沒有評論 |
| 2025 | Guo et al. | 自旋電子學 | 點名室溫 LCM 半導體是待解目標 |
| 2026 | Claude agent | 跨領域 | 把前面接起來，量化自旋窗、測穩健性 |

每一筆都不是廢稿，1999 年那篇的標題就在講「磁序溫度超過 100 °C」。**每一篇都在回答自己的問題，答案剛好是別人的問題需要的。** 缺的不是知識，是一個同時讀過這幾堆文獻的人。

但要講精確：這次不是「一晚上全翻完」。agent 花了四天，而且文獻搜尋漏掉了最接近的前人工作 Middlemiss 2008，是外部讀者做文獻檢查時補上的。**閱讀頻寬大，不等於讀全了。**

---

## 論點二：AI 是第一個讀過所有故紙堆的通才

為什麼這件事人類一直沒做？

**專家是縱向的。** 化學家讀化學期刊，講 molecule-based magnet；計算物理學者講 exchange coupling；自旋電子學的人講 Luttinger-compensated。同一個材料，用三種關鍵字存在三個社群裡。一個專家要花一輩子把自己的領域讀深，沒有餘力橫向讀別人的領域。

**AI 在這個階段剛好是反過來的。** 它不見得比任何一個專家深，但它讀化學期刊和讀物理期刊的成本一樣，不會因為「這不是我們領域的」就略過。它的強項是寬，是把不同學科的東西放在同一個腦子裡比對。

這件事有前人。1986 年，資訊科學家 Don Swanson 發表〈Fish Oil, Raynaud's Syndrome, and Undiscovered Public Knowledge〉。他發現兩批彼此不引用的醫學文獻：一批說魚油會影響血液黏稠度，另一批說雷諾氏症跟血液黏稠度有關。A 連 B、B 連 C，沒人寫過 A 連 C。他把這叫「未被發現的公開知識」。Swanson 當年靠人工翻 Medline，一次接一條線。agent 是把這件事規模化。

而且故紙堆不只用來找答案，也用來排除錯的答案。YBaMnFeO₅ 被判死，靠的不只是模擬：agent 拿 2016 年 Nature Communications 上同家族化合物的實驗當校準，還比對了同家族已經做出來的類似化合物，排列全都是亂的。前人的失敗紀錄，替 agent 省掉了一次合成實驗。

這不是孤例。上個月我寫過〈[950 個 Claude Agent 翻出類 CRISPR 系統 ART](/claude-art-crispr-agent-reproducibility/)〉，結構一模一樣：那個逆轉錄酶以前的研究就見過，Claude 是第一個注意到它旁邊還有一串重複陣列和搭檔蛋白的。一個在生物學的資料庫裡，一個在材料科學的期刊裡，兩週內兩個案例，都是同一個模式：**東西早就在故紙堆裡，AI 用另一個學科的眼光多看了一眼。**

### 新學科會不會就這樣長出來？

這一段是推測，先標清楚。

看「Luttinger 補償磁體」這個名字本身：一個 1960 年的理論物理定理，加上磁學，加上記憶體應用。這個分類本身就是跨學科拼起來的。把這類完全補償的磁體當成自旋電子學目標材料來預測的論文，集中在 2024–2025 年。

如果 AI 現階段的主要工作，是拿一個領域的新分類去重掃另一個領域的舊資料，那它每接起一條線，就可能在兩個學科的交界處多出一個新問題。新學科不一定要有人刻意去開創，可能是這樣一條一條接出來的。

但這個推測目前只有兩個案例撐著，我不打算講得更滿。

---

## 離能用還很遠，但這是一個很好的案例

KV[Cr(CN)₆] 離一顆能用的記憶體還很遠。能隙和自旋極化沒人量過，真實樣品只有 1999 年一份含水粉末，更沒有任何元件。agent 自己的審稿 agent 給的評分也很清楚："Not big news."

但它是一個很好的案例。AI 怎麼從故紙堆裡挖出東西、怎麼判斷挖到的是不是真的、哪裡漏了，這次全部攤開在 repo 裡，任何人都可以查。

---

## AI 考古科學家

所以這次真正值得帶走的，不是材料，是工作方式。這種工作方式，可以叫它 AI 考古科學家。

考古不是挖到東西就算數。把這次 repo 裡的流程對上考古的工序，大概長這樣：

| 考古工序 | 這次怎麼做 | 誰做 |
|----------|-----------|------|
| 定方向 | 決定找室溫 LCM 半導體 | 人 |
| 挖掘 | 用新分類重掃已知材料與文獻 | agent |
| 鑑定 | 對已知結構跑 DFT，先寫好判死規則再算 | agent |
| 交叉驗證 | 派審稿 agent 專門挑錯，撤回不成立的宣稱 | agent |
| 補漏 | 檢查有沒有漏掉的前人工作（這次漏了 Middlemiss 2008） | 外部讀者 |
| 策展 | 決定哪個值得發表、送進實驗室 | 人 |

鑑定這一步最能看出紀律。1999 年的真實樣品孔洞裡有水，agent 事先登記的規則是：水把電洞窗砍掉太多就判死。快的方法觸發了判死，agent 撤回了「現有樣品就有這個效應」的宣稱。後來準的方法算出來效應還在，審稿 agent 的結論是：

> "Hydrate HSE is a method split, not a pre-registered pass."

換了方法拿到好結果，只算「方法有分歧」，不算通過。挖到的東西再漂亮，也不能事後改標籤。

表格裡「補漏」那一列也值得多看一眼：這是目前 agent 最弱的一環，也是人最該守的位置。

### 你公司的故紙堆

換到企業，這個工種一樣成立。每家公司都有自己的「1999 年論文」：舊專案的結案報告、做到一半被擱置的實驗紀錄、當年因為別的原因被否決的設計。它們當年在回答別的問題，現在出現了新框架，可能是新法規、新客戶需求、新技術，但沒有人有時間回頭重讀。

這次的 agent 是從零設計失敗後，才回頭翻舊材料找到答案。企業可以把順序倒過來：先讓 agent 拿新框架重讀既有資產，再決定要不要從零開始。前提有三個：舊資料有留下來、找得到；有一個快速驗證的方法，像這次的 DFT 重算；還有一個人負責檢查它漏讀了什麼。

---

## 坦白說

這篇的兩個論點，都要打折。

**1. 「讀過所有故紙堆」是誇張說法。** 這次 agent 漏掉的，恰好是最接近的那一篇前人工作。閱讀頻寬大是真的，覆蓋率沒人保證。如果漏讀的是一篇已經證明這個材料不行的論文，整個結論都會不一樣。

**2. 物理原理不是新的。** Vals 自己寫了："It has long been understood that this kind of magnet has spin-split electrons." 這次的貢獻是把已知原理對上一個已知材料，再量化。是打通，不是發明。

**3. 倖存者偏差。** README 寫，同時進行的其他搜尋路線 "did not find anything above their bars"。我們只看到成功的這一條，考古挖空的坑沒有被寫成部落格。

**4. 「新學科自然長出來」只有兩個案例。** ART 和這次都是「舊資料、新眼光」，但兩個案例撐不起一個趨勢。我把它當成一個值得追蹤的假設，不是結論。

但它做對了一件事：**它把「重讀」做成了可以被檢查的流程。** 從失敗設計萃取原則、用原則篩已知材料、對已知結構重算、預先登記判死條件、公開 61 條宣稱讓外人抓錯。這套工序比材料本身更容易被複製到別的領域。

---

## 關鍵洞察

**1. AI 在科研的第一個穩定角色是通才讀者，不是發明家。** 這次從零設計的候選死在可合成性，從舊文獻重讀出來的候選在 1999 年就過了這一關。

**2. 新框架出現時，就是重讀舊資料的時機。** 答案常常不缺，缺的是一個同時讀過好幾個學科的人。這件苦工剛好適合交給平行的 agent。

**3. 翻出候選不等於做出產品。** 對任何「AI 發現新材料」的消息，先問三件事：有沒有實驗量測、有沒有真實樣品、離元件還差幾步。

**4. AI 考古科學家這個工種裡，人要守的是補漏和策展。** agent 能挖、能鑑定、能互相挑錯，但會漏讀。檢查覆蓋率、決定哪個值得送進實驗室，目前還是人的工作。

---

## 常見問題 Q&A

**Q: Vals AI 的 Claude agent 到底找到了什麼？**

2026 年 10 月 1 日到 4 日，一組 Claude Opus 5.5 agent 用密度泛函理論（DFT，Density Functional Theory）計算，找到兩個室溫 Luttinger 補償磁性半導體候選材料：新設計的 YBaMnFeO₅，計算顯示它大概做不出有效的有序形式；以及 1999 年就被合成過的 KV[Cr(CN)₆]，預測能隙約 2.1 eV、自旋窗 2.6 / 1.6 eV，1999 年樣品實測磁序溫度 376 K。兩者都是計算預測，能隙和自旋分選都還沒有實驗量測。

**Q: 為什麼說 AI 做科研最狠的是閱讀頻寬，不是算力？**

這次研究用的是雲端 CPU，約 750 個計算 job，四天完成，不是超級電腦等級的算力。真正的突破來自閱讀：KV[Cr(CN)₆] 的相關知識散在 1999 年的化學論文、2008 年的計算物理論文、2025 年的自旋電子學論文裡，三個社群用不同的詞，沒有人同時讀過。agent 用新的 Luttinger 補償分類回頭重看已知材料，才把它們接起來。但閱讀頻寬大不等於讀全，這次 agent 漏掉了最接近的 2008 年前人論文，是外部讀者補上的。

**Q: KV[Cr(CN)₆] 離做成記憶體還有多遠？**

還很遠。目前只有 1999 年的一份含水粉末樣品，無水晶體從未被報導；兩種計算方法對含水的影響結論不同；能隙、自旋極化都沒量過；能帶很窄，載子遲緩；室溫下磁序只完成約 60%。研究方提出的下一步是三個實驗：重做材料量組成與飽和磁化、X 光磁圓二色性（XMCD）與磁光量測、自旋解析光電子能譜（Spin-resolved Photoemission）。這些全部做完也只確認材料性質，離元件和量產還有很多步。

**Q: 「AI 考古科學家」是什麼樣的工作？**

指用 AI agent 拿新的分類或框架，重讀人類累積的舊文獻與舊資料，找出當年沒被注意到的連結。這個概念的前身是 Don Swanson 1986 年提出的「未被發現的公開知識」（Undiscovered Public Knowledge）。以 Vals 的案例，工序包括：人定方向、agent 重掃文獻、agent 用 DFT 鑑定並預先登記判死規則、審稿 agent 交叉驗證、人補漏與決定送實驗室。目前 agent 最弱的是文獻覆蓋率，需要人檢查。

**Q: Luttinger 補償磁體（Luttinger-compensated magnet）跟一般反鐵磁有什麼不同？**

兩者淨磁矩都是零，沒有外漏磁場，可以塞得很密。一般反鐵磁的上下自旋原子環境相同，電子無法依自旋分開，難以讀寫資料；Luttinger 補償磁體的上下自旋原子位在不同環境（常是不同元素），能隙邊緣的電子會依自旋排好，可用在自旋電子學（Spintronics）。名稱來自 1960 年的 Luttinger 定理。衡量指標是自旋窗（Spin Window）寬度，要遠大於室溫熱擾動的大約 26 meV。

---

*資料核對日期：2026-10-07。主要來源：Vals AI〈[Two Room-Temperature Antiferromagnetic Semiconductor Candidates](https://www.vals.ai/blogs/room-temperature-magnetic-semiconductors)〉（2026-10-04）、[compensated-magnet-ledger GitHub repo](https://github.com/spicylemonade/compensated-magnet-ledger)（含 BLOG.md、README、LEDGER 與兩份 agent 卷宗）、S. M. Holmes & G. S. Girolami, J. Am. Chem. Soc. 121, 5593 (1999)、P.-J. Guo et al., [arXiv:2502.18136](https://arxiv.org/abs/2502.18136)、D. R. Swanson, Perspectives in Biology and Medicine 30(1), 7–18 (1986)、[Prussian blue（Wikipedia）](https://en.wikipedia.org/wiki/Prussian_blue)、[Luttinger's theorem（Wikipedia）](https://en.wikipedia.org/wiki/Luttinger%27s_theorem)。本文未重跑任何計算，未獨立驗證 DFT 結果。*
