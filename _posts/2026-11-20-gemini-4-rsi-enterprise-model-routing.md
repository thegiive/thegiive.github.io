---
layout: post
title: "Google 連發 Gemini 4 四兄弟：大家都以為碰到 RSI 了，企業到底該怎麼選模型？"
date: 2026-11-20 09:00:00 +0800
permalink: /gemini-4-rsi-enterprise-model-routing/
description: "Google 短時間內接連端出 Gemini 4 Argon、Carbon、Neon、Hydrogen，能力強到社群懷疑是否觸發了 RSI（遞迴自我改進）。本文整理官方 Model Card、Artificial Analysis、CursorBench 與開發者實測，拆解 12/1 定價倒掛陷阱、四款模型的實戰分工，以及為什麼「先選 Harness 再選模型」才是企業省錢關鍵。"
categories: [AI 產業分析, AI Agent]
tags: [Gemini 4, Argon, Carbon, Neon, Hydrogen, RSI, AI Agent, Harness, 模型路由, 企業 AI 工程化]
image: /assets/images/gemini-4-rsi-enterprise-model-routing-cover.png
image_alt: "Google Gemini 4 Argon、Carbon、Neon、Hydrogen 四款模型定位與企業選型架構"
author: Wisely Chen
---

這陣子 Google 釋出 Gemini 4 系列的節奏快得驚人，一口氣端出 **Argon、Carbon、Neon、Hydrogen** 四個版本，加上官方明講第一個推出的 Argon 被拿來協助訓練後續模型，社群上甚至開始討論：**Google 是不是已經碰到 RSI（Recursive Self-Improvement，遞迴自我改進）的臨界點了？**

老實說，我們這幾天在工程現場其實一直很迷茫——模型一多、名字又像化學元素週期表，每個人都在問：**「到底哪個情況該切哪一個？」** 回到企業 AI 工程化與架構師的日常，模型更新快從來不是壞事，最痛的往往是「選錯模型、花錯預算、還把問題怪到模型頭上」。

這篇把目前各方實測、官方 Model Card、Artificial Analysis（AA）與 CursorBench 的數據攤開來看，直接整理出一份給工程團隊的 Gemini 4 實戰選型與成本避坑指南。

---

## 一、先搞懂 Gemini 4 四兄弟的定位

Google 這次用化學元素命名四個定位截然不同的版本：

* **Gemini 4 Argon**：Gemini 4 系列第一個推出的通用旗艦，後面幾個模型都是接著它發布的，Google 也拿它來協助訓練其他模型。
* **Gemini 4 Carbon**：系列裡最強的深度推理模型，專門處理最難、需要想很久的問題，初期先開放給資安防禦團隊使用。
* **Gemini 4 Neon**：介於 Carbon 和 Hydrogen 之間，能力逼近最前線、速度又明顯更快，主打複雜的軟體工程、知識工作與科學研究。
* **Gemini 4 Hydrogen**：快、便宜、給大眾用的主力版本，鎖定日常寫程式與 Agent 任務，免費層也能用，同時也是 Gemini 裡 Tasks 功能背後的模型。

如果只看產品線，很容易陷入「那我到底該用 Argon、Neon 還是 Carbon？」的選擇障礙。接下來直接看實測與計價差異。

---

## 二、Argon vs. Carbon：單價一樣，為什麼帳單跟延遲差這麼多？

社群對這兩款的共識很一致：**Carbon 普遍比 Argon 強，但更慢，也更耗 token；簡單題目兩者差不多，只有碰到硬骨頭才看得出 Carbon 的價值。**

### 官方定價與能力數據
根據 Google 的[官方說明](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/)，Argon 與 Carbon 的牌價其實完全一樣：目前導入價都是每百萬 token 輸入 **$2**、輸出 **$10**，並預計於 **12/1 起調漲為輸入 $4、輸出 $20**。

既然單價相同，為什麼大家都說 Carbon 比較貴？因為 **Carbon 每一輪思考的推理長度更長**，導致端到端延遲變高，單次任務消耗的輸出 token 也大幅增加。官方建議非常明確：大部分進階寫程式與知識工作用 Argon 就好，只有最難的除錯、架構設計、科學證明與資安稽核，才交給 Carbon。

從 [Gemini 4 Carbon Model Card](https://deepmind.google/models/model-cards/gemini-4-carbon/) 上的基準分數也能看出這個差距（Carbon vs. Argon）：
* **綜合智能指數**：59 vs. 50
* **長上下文（Long Context）**：96.2% vs. 84.2%
* **Agent 寫程式**：61.2% vs. 55.0%

### 開發者實測與反例
* **Google 官方態度**：Logan Kilpatrick（[@OfficialLoganK](https://x.com/OfficialLoganK/status/2123195568742949097)）直言 Carbon 比 Argon 更好，只是吃 token、跑較久，能用 Carbon 就用。
* **獨立測試站實測**：[FastMetal](https://fastmetal.ai/blog/gemini-4-carbon-vs-gemini-4-argon) 跑了 43 道題目，結果 Carbon 每一題都比較慢——完成時間中位數 **34.9 秒**，Argon 只要 **10.5 秒**，而且 Carbon 的輸出 token 約多出一倍。簡單題兩者表現接近，但在 SQL 優化這類高難度題目上，Carbon 確實抓出了 Argon 漏掉的 bug。
* **體感與品味**：常發實測的 [@pankajkumar_dev](https://x.com/pankajkumar_dev/status/2120372310691742043) 認為 Carbon 是不錯的升級、但不算跨代飛躍；影音圖片理解與細節品味有進步，缺點是慢、常要兩三輪才做對，有時還「有點懶」。在前端與 3D 展示上，多數人肯定 Carbon 更細緻，但不一定比較好看，跟 Opus 這類模型比也不是穩贏。
* **超時反例**：前 Google 工程師 [@michaelrbock](https://x.com/michaelrbock/status/2120957630982291934) 拿極度複雜的報稅計算題測試時，Carbon 因為想太久一路超時、撞到 token 上限，最後表現反而輸給 Argon。

結論很清楚：**不要無腦全開 Carbon。** 日常跑 Argon 又快又省，卡住時再切 Carbon 當二線救援——而且隨著 Neon 登場，連 Argon 自己的位置都被取代了。

---

## 三、Neon 與 Hydrogen 登場：12/1 定價倒掛與新主力

Hydrogen 和 Neon 的出現，直接改寫了 Gemini 4 的性價比版圖。

### 1. Hydrogen vs. Argon：高推理模式打平，但要注意幻覺
在官方綜合智能指數上，Hydrogen 拿到 **51**（Argon 為 50）；把推理強度開到最高時，Hydrogen 更衝到 **54**，等於打平甚至略贏 Argon，而且速度更快、價格更低。社群如 [@LuminaBench](https://x.com/LuminaBench/status/2121903835933278548) 甚至直接評價 Hydrogen「這個價錢很夠用、比 Argon 好」。

不過實戰導入仍有三個細節不能忽略：
1. **圖表與拒答能力**：Argon 在圖表理解，以及「不知道的時候少亂猜」這兩點依然表現較佳。
2. **低推理強度的幻覺風險**：[Artificial Analysis](https://x.com/ArtificialAnlys/status/2120941526272340432) 實測指出，當 Hydrogen 的推理強度往下調時，幻覺率會明顯上升。
3. **長尾延遲**：也有開發者測到 Hydrogen 在某些任務上偶爾比 Carbon 還慢、還貴，並非每一次請求都保證最省。

### 2. Neon vs. Argon：全面超越，且 12/1 後價格更便宜
攤開 [Gemini 4 Neon Model Card](https://deepmind.google/models/model-cards/gemini-4-neon/) 對比 Argon，幾乎是全面輾壓：
* **綜合智能指數**：61 vs. 50
* **長上下文**：95.2% vs. 84.2%
* **科學與終端類 Terminal-Bench**：70.5% vs. 52.9%

網友對 Neon 的評價一面倒地好。Antigravity 的 Varun Mohan（[@_mohansolo](https://x.com/_mohansolo/status/2123168228415599033)）評價 Neon「比 Carbon 便宜、快，也更好合作」；[@pankajkumar_dev](https://x.com/pankajkumar_dev/status/2123641379662270483) 更直接稱 Neon 是 Google 目前最好的模型。

更關鍵的是**價格時間差**：現在（11/30 前）Argon 還在導入價，所以比 Neon 便宜；但 **12/1 起 Argon 調漲為 $4 / $20 之後，局勢會直接反過來——Argon 會變得比能力更強的 Neon 還要貴。**

因此，現在社群最推崇的架構模式是 **「Neon 做規劃（Plan）＋ Hydrogen 去執行（Execute）」**：用 Neon 拆解架構與規格，把大量重複的檔案改寫與測試執行交給 Hydrogen，兼顧品質與帳單。

---

## 四、跨陣營對決：Gemini 4 vs. Claude（Fable / Opus / Sonnet）

把視角拉出 Google 生態系，拿來跟 Anthropic 的 Claude 系列（Fable、Opus、Sonnet）同台比較，勝負線其實非常清楚：

| 評測指標 / 場景 | 領先陣營與關鍵數據 | 實戰解讀 |
|---|---|---|
| **AA 綜合智能指數** | Fable **65** > Neon **61** > Carbon **60** > Opus **59** > Sonnet ~**55** > Hydrogen **54** > Argon **50** | Neon 與 Carbon 已站上第一梯隊，緊追 Fable |
| **Coding Agent 實測（AA）** | Neon + Antigravity **59** vs. Fable/Opus + Claude Code **58** | 分數幾乎打平，但單次任務成本差一倍以上：<br>Neon 約 **$6.9**｜Opus **$12.6**｜Fable **$15.5** |
| **CursorBench** | Neon **65.4%**（第一）> Fable **61.3%** > Opus **58.1%** | 單次任務成本：<br>Neon **$10.7** vs. Fable **$48** |
| **長上下文能力** | Gemini 4 Neon **95.2%** vs. Opus **66.8%** | 吃整份大型 Repo、長日誌或跨文件分析時，Gemini 優勢極大 |
| **多模態原生支援** | Gemini 4 原生直吃影片與語音 | 影音理解、會議或畫面除錯流程更順暢 |
| **Claude 依然勝出的三塊** | OSWorld（電腦操作）、Terminal-Bench（終端機任務）、知識寫作 | AA Briefcase 寫作評比中 Sonnet 與 Fable 仍高於 Neon（Neon 僅在簡報呈現超車）；前端 3D 品味多數人仍微幅看好 Opus |

資料來源：[Artificial Analysis Neon 分析](https://artificialanalysis.ai/articles/gemini-4-neon-intelligence-gain)、[AA Agent 成本實測](https://x.com/ArtificialAnlys/status/2123170648772288540)、[CursorBench](https://cursor.com/cursorbench)。

---

## 五、企業團隊的最終選型建議：先選工具，再選模型

在直接套用下面這份選型清單前，先記住社群實測中最常被忽略的一條鐵律：**同一個模型，換到不同的 Agent 工具（Harness）裡跑，基準分數可以差到三倍。** 

這也是為什麼這份清單要跟你的開發工具與工作流綁在一起看：

1. **大量日常任務與執行層 → 選 Gemini 4 Hydrogen**  
   寫日常程式碼、補文件、跑自動化小任務最適合。但若用於嚴謹業務邏輯，建議維持中高推理強度，避免低推理設定下幻覺率升高的問題。
2. **複雜工程、知識工作與規劃層 → 選 Gemini 4 Neon（Argon 的真正接班人）**  
   目前性價比與合作體感最好的主力模型。推薦搭配 **Neon 規劃 ＋ Hydrogen 執行** 的分層路由策略。
3. **還在用 Argon 的團隊 → 注意 11/30 期限**  
   如果你現有的 Prompt 與工作流在 Argon 上跑得很穩，可以撐到 **11/30** 吃導入價；**12/1 漲價後請直接切換到 Neon**，能力更強還更省錢。
4. **最難的架構除錯、長推論與資安稽核 → 交給 Gemini 4 Carbon**  
   不要當成預設模型，設定好 Timeout 與 Token 預算上限，只在卡關或高風險稽核時當作二線專家呼叫。
5. **高度依賴終端機操作、桌面代理或長篇商業寫作 → 保留 Claude（Fable / Opus / Sonnet）**  
   尤其在 OSWorld、Terminal-Bench 與專業文章寫作上，Claude 仍有明顯優勢；但在 Coding Agent 成本敏感度高的專案裡，Neon 搭 Antigravity 或 Cursor 已能用一半以下的成本打出平手甚至領先的成績。

---

## 六、最後一句話答案：不想再迷茫，直接這樣選

如果你不想每次開工前都還要對照跑分表，直接記住這三個情境的一句話結論：

1. **最高難度**（架構死結、深層除錯、資安稽核、數學／科學證明）→ **Gemini 4 Carbon**（設好 Timeout 與預算上限當二線專家）。
2. **一般 Hybrid 使用**（多步驟專案開發、寫規格＋改大量檔案）→ **Gemini 4 Neon 做規劃（Plan）＋ Gemini 4 Hydrogen 去執行（Execute）**。
3. **快速 / 日常**（寫日常腳本、補文件、大量自動化小任務）→ **Gemini 4 Hydrogen**（建議維持中高推理強度）。

**那如果完全不想選、只想找一個像以前用 Opus 5.5 一樣可以「閉眼衝」的模型（速度快、能力好、價錢也合理）？**  
答案只有一個：**Gemini 4 Neon**。它在 AA 綜合指數（61）與 CursorBench（65.4%）都站在最前線，反應快、跟 Agent 工具好配合，單次任務成本又只要同級對手的一半左右，是目前唯一能直接當成預設主力「閉眼衝」的選項。
