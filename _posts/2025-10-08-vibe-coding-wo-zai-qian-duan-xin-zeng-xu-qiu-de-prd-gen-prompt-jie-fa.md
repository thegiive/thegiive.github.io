---
layout: post
title: "[VIBE Coding] 我在前端新增需求的 PRD 跟 Prompt 解法"
date: 2025-10-08 00:43:22 +0000
permalink: /vibe-coding-wo-zai-qian-duan-xin-zeng-xu-qiu-de-prd-gen-prompt-jie-fa/
image: /assets/images/Gemini_Generated_Image_6zdw0k6zdw0k6zdw-1.png
description: "上次提到我在前端這邊做AI Coding 很適合 0% -> 70% , 或是 99 -> 100%的做法，但是在 90% -> 100% 遇到了蠻多的小問題，經過幾天的討論修正之後，我已經大概列出了比較適合的方式。根據這一週來改了十幾個 Feature的經驗，這個流程對我這樣非前端的人來說，感覺 90% -> 100% 除了後續檢核需要前端幫忙以外，幾乎都是我可以自己處理。..."
---




上次提到[我在前端這邊做AI Coding](https://ai-coding.wiselychen.com/zui-jin-wo-zai-qian-duan-vibe-coding-yu-dao-de-wen-ti/) 很適合 0% -> 70% , 或是 99 -> 100%的做法，但是在 90% -> 100% 遇到了蠻多的小問題，經過幾天的討論修正之後，我已經大概列出了比較適合的方式。根據這一週來改了十幾個 Feature的經驗，這個流程對我這樣非前端的人來說，感覺 90% -> 100% 除了後續檢核需要前端幫忙以外，幾乎都是我可以自己處理。

這個場景其實還蠻常見的，現在 VIBE Coding 大家都在講從頭新建一個網站，這個東西對工程師來說太低頻了，其實程式設計師大部分的時候都是在新增修改功能某個到在現有的 App 上，所以這個技巧我實際跟前端一起弄四五天後，我個人覺得還蠻好用的。

### 流程圖

![](/assets/images/image-10-1.png)

首先第一個就是把舊設計稿跟U I的截圖請A I幫我做比較，這個部分主要是列出新增或修改的UI介面在哪邊，這個時候出來的東西可能是一個free format，但不要緊。舉例，我截圖一個 Google Doc 畫面，我故意把中間的 提示 icon 修掉 , 當作做 feature 之前的 V1.0 ，然後再把原始圖變成 V1.1 

![](/assets/images/-------2025-10-08-------7.57.40-------1.png)範例：我故意把中間的 提示 icon 修掉 , 當作做 feature 之前的 V1.0 ![](/assets/images/-------2025-10-08-------7.57.40-1.png)範例：原始畫面當作做做完 feature 之前的 V1.1 

接下來下一步，我們請A I幫我產生有剛剛的修改的或是新增的需求列表表，這個時候就是一個比較粗的P R D。這裡我其實都會預設使用 Gemini ，因為我體感 Gemini OCR 蠻強的，UI 抓中文字比較簡單

![](/assets/images/image-11.png)Gemini OCR 

然後我們請他變成一些 feature list ，一個一個 功能變化都寫成簡易的 feature list ，此處我還是不規範 PRD ，隨意產生即可。下面的範例是我這幾天 onProd 某個功能 masking 過的寫法，保證真實，不像外面開課程都是一堆 demo code XD

![](/assets/images/data-src-image-6d5fe5e6-67de-46b4-bd1f-2fa4ee08e5b5.png)相關功能文件 - 簡略的 feature list 

下一步我們準備好的P R D 的Temple，以及相關的 supporting Tech PRD 資料(API文件 或是相關的程式碼的規範文件) ，就會產生一個完整的P R D。以下也是那功能最後產生的 詳細 PRD 

![](/assets/images/data-src-image-a3b4ee0e-4b31-405a-868e-d57931f5710f-1.png) 有 需求列表 , tech requirement , 還有 supporting data 的

有這個完整的P R D之後，我們就可以請AI幫我們做Coding，我之前經驗幾乎一次過。產生 code 的 Prompt 超級簡單的，因為 PRD 都已經寫好了。

![](/assets/images/data-src-image-fa64d1f5-e960-433b-b391-b34c23398453-1.png)![](/assets/images/data-src-image-473c3d0b-dafc-4184-bea1-7d11d78f9530-1.png)

最後給 RD 檢核， 送交 QA 。

### 結果

根據這一週來改了十幾個 Feature的經驗，這個流程對我這樣非前端的人來說，感覺 90% -> 100% 除了後續檢核需要前端幫忙以外，幾乎都是我可以自己處理。

### 附件A: PRD Template 

## This post is for subscribers only

Subscribe now

Already have an account? Sign in
