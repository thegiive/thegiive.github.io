---
layout: post
title: "用 AI 做簡報，跟人手刻的差別是什麼？"
date: 2025-12-14 08:00:00 +0800
permalink: /ai-slide-notebooklm-customer-first/
image: /assets/images/ai-slide-notebooklm-customer-first-cover.png
description: "用 NotebookLM + Gemini 做簡報，追求的不是加速，而是「千人千色」的客製化。當色調、用字遣詞都符合客戶的企業語言，把客戶放在最中心，這才是 Customer First。"
---

昨天某知名 Conf 結束後，看到一些討論在說：
「有講者明顯直接用 NotebookLM 生的簡報就上台，是不是不尊重聽眾？」

我的第一個反應其實是：
用 AI 做簡報本身，真的等於不尊重嗎？重點不應該還是在內容與表達嗎？

後來在 Threads 上看到一些被點名的「問題簡報」，老實說也能理解為什麼會被罵：文字有 NotebookLM 的渲染錯誤、背景一看就知道是 NotebookLM 預設淡棕色風格。

![NotebookLM 預設風格範例](/assets/images/notebooklm-default-style-example.png)

這兩年，從 Gamma.app 到現在的 NotebookLM，我大概用 AI 做過 100+ 場簡報（約 90% 內部、10% 對外）。

內部簡報我幾乎都是「我寫大綱 → AI 直出 → 就直接用」，因為錯了也沒差，省力。

至於對外簡報？我很驕傲的說，NotebookLM 的使用率幾乎是 100%。但是我從來不只是為了省時間。

而是 NotebookLM + Gemini 2.5 Pro 已經可以讓我做到一件以前很難的事——

**「千人千色」的簡報**

---

## 我目前的流程

**Step 1：** 用 ChatGPT Atlas 去抓客戶官網的主色調與企業價值

**Step 2：** 產出簡報用的風格與敘事提示詞（含一句企業價值總結）

**Step 3：** 把大綱、補充資料與提示詞一起丟進 NotebookLM 產生簡報

**Step 4：** 用 Canva 調整字體與細節（每一頁都會檢查，不好的直接刪）。至於文字修正不是很基本嗎？我 NotebookLM 一出就課金 Canva 了。

---

## 結果是什麼？

- **某個台灣綠色主色調企業**，就用藍綠底 ＋ 簡報裡面用詞貼近企業語言的敘事
- **傳統產業，紫色配色品牌，尋求轉型**。我簡報裡面尖銳線條感提供科技感，淡紫色配色凸顯美感
- **日商上市公司**，直接白底、簡單、不改任何語言，不能出錯

當你色調、用字遣詞都符合提案中心概念，並且把客戶放在最中心，客戶是超級滿意的。

---

## 我用 AI 做簡報追求的不是加速

**我追求的是聽眾滿意度，這是 Customer First。**

---

*附圖為：因為網路上無法展現我的千人千色的成品簡報，我用技術文章當例子吧。我請 NotebookLM 去把 O'Reilly 的某本我的 Data 書轉成 O'Reilly 風的簡報（黑白風、動物截圖、紅色字）。想想這樣等級的簡報居然可以在 5 分鐘完成，真的很 amazing。*

![O'Reilly 風格簡報範例 - 封面](/assets/images/ai-slide-notebooklm-customer-first-cover.png)

![O'Reilly 風格簡報範例 - 複製模型](/assets/images/ai-slide-oreilly-example-2.png)

![O'Reilly 風格簡報範例 - 三大核心目標](/assets/images/ai-slide-oreilly-example-3.png)

---

## 產生這個投影片的 Prompt

```
【角色設定】
你現在是一位頂尖的視覺設計師與技術傳播專家，擅長將複雜的技術概念轉化為 O'Reilly 經典書籍封面風格（Classic O'Reilly Media Style）的專業簡報。

【風格指南：O'Reilly 技術經典風】
請根據《Designing Data-Intensive Applications》這本書的封面視覺語言，為我規劃簡報的視覺與內容風格。請嚴格遵守以下設計規範：

1. 核心視覺主題 (Visual Theme)：
   - 關鍵詞：學術權威、復古科學、極簡主義、工程美學。
   - 圖像風格：所有插圖必須採用「19 世紀銅版畫/木刻風格 (Vintage Woodcut/Engraving)」的黑白線條圖。避免使用任何現代 3D 圖標、扁平化插圖或彩色照片。
   - 隱喻手法：用古老的動物或機械結構來隱喻現代分散式系統的複雜性（例如：用「螞蟻群體」代表分散式節點，用「大象」代表持久化存儲）。

2. 色彩計畫 (Color Palette)：
   - 背景：大量純白 (#FFFFFF) 留白，強調乾淨與閱讀性。
   - 主色：深紅色 (#870A24) 或磚紅色，僅用於標題色塊或強調重點。
   - 文字與線條：純黑 (#000000) 或深灰，用於內文與插圖。

3. 字體排印 (Typography)：
   - 標題：請指定使用經典襯線體 (Serif，如 Garamond 或 Caslon)，傳達經典與嚴謹感。
   - 內文：使用乾淨的無襯線體 (Sans-Serif，如 Helvetica 或 Arial)，確保技術細節的清晰度。

【輸出任務】
請根據上述風格，為我生成一份簡報大綱。在每一頁投影片的規劃中，除了內容重點外，請務必包含一個 [視覺設計建議] 的欄位，具體描述該頁面應該放什麼樣的「黑白版畫動物」或「圖表樣式」。

範例格式：
- 投影片 1：標題頁
  - 標題：Designing Data-Intensive Applications (白字紅底色塊)
  - 視覺設計建議：畫面中央放置一隻精細的「黑白蝕刻風格的印度野豬」插圖，背景純白，不加裝飾。
```

---

## 常見問題 Q&A

**Q: 用 AI 做簡報會不會被看出來？**

會，如果你直接用預設風格不修改的話。關鍵是要客製化色調、字體、刪除不好的頁面。

**Q: NotebookLM 跟 Gamma.app 差在哪？**

NotebookLM 搭配 Gemini 2.5 Pro 可以更精準理解你的資料，產出的內容「知識保真度」更高。Gamma 比較偏快速美化。

**Q: 為什麼要用 ChatGPT Atlas 抓色調？**

Atlas 可以直接操作瀏覽器去看客戶官網，自動分析主色調跟企業價值，比我自己去截圖分析快很多。

**Q: Canva 付費版值得嗎？**

如果你常做對外簡報，非常值得。字體、素材、背景移除功能都省很多時間。

**Q: 內部簡報需要這麼講究嗎？**

不需要。內部簡報我就是「大綱 → AI 直出 → 直接用」，省力優先。

**Q: 這個流程要花多少時間？**

完整四步驟大約 30-60 分鐘。但產出的品質是以前要 3-4 小時才能達到的。

**Q: 沒有設計底子也能做嗎？**

可以。關鍵是你要會寫好的 Prompt 描述風格，AI 會幫你處理視覺細節。

**Q: 這個方法適合什麼場合？**

對外提案、客戶簡報、重要會議。任何你需要「讓對方感覺被重視」的場合。
