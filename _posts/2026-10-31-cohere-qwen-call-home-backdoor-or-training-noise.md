---
layout: post
title: "Cohere 說 Qwen3.8 想把檔案傳回北京，72 小時後社群把報告拆完了：異常是真的，後門站不住"
date: 2026-10-31 21:00:00 +0800
permalink: /cohere-qwen-call-home-backdoor-or-training-noise/
tags: [Qwen, Qwen3.8, Cohere, Alibaba Cloud, AI Agent, LLM 資安, 出口白名單, egress control, Chain of Thought, 開源模型, 地端部署]
categories: [AI 資安]
image: /assets/images/cohere-qwen-call-home-backdoor-or-training-noise-cover.png
description: "10 月 26 日，Cohere 發報告說 Qwen3.8-Flash-Next 在沙箱裡寫資安偵測規則時，推理寫著不呼叫工具，同一回合卻盤點主機、試圖把探測檔 PUT 到阿里雲北京的 bucket。推文 304 萬瀏覽。我把 10 月 26 日到 31 日 X 上的討論翻過一遍：模型會幻覺出阿里雲網址並真的發請求，這件事有獨立來源看到；但重現靠的是從 curl 指令中段 prefill，確切主機在 22.9 萬樣本裡出現 0 次。這篇拆開哪些站得住、哪些站不住，以及做 agent 的人真正該改的那一件事。"
author: Wisely Chen
faq:
  - question: "Cohere 對 Qwen3.8-Flash-Next 的指控具體是什麼？"
    answer: "2026 年 10 月 26 日，Cohere 發布報告，說它在沙箱裡要求 Qwen3.8-Flash-Next 寫一條防禦用的資安偵測規則時，模型盤點了所在主機，並嘗試把一個探測檔上傳到阿里雲北京區的 storage bucket，而推理過程寫著不會呼叫任何工具。沙箱擋下了請求，沒有對外連線成功。Cohere 明確表示沒有找到根因，也沒有主張惡意，報告宣稱的發生率是低於十萬分之一，但沒有給總呼叫數。"
  - question: "有沒有獨立來源證實 Qwen3.8 會連到阿里雲？"
    answer: "有，但證實的是「幻覺出阿里雲網址並發請求」，不是「上傳資料」。Vals AI 在抓 SEC 財報、抓 Python 文件這類非資安任務中，看到 Qwen3.8-Max、Qwen3.8-27B 對阿里雲 proxy 發出不請自來的請求，全部被伺服器回 403，沒有找到外洩證據；Qwen3.7 系列沒有這個行為。X 上 @wtogami 跑 22.9 萬樣本，報告中那個確切的 bucket 主機出現 0 次；@ChenhaoTan 重建環境跑三個模型共 130 次，沒有任何一次上傳。"
  - question: "什麼是 prefill（預填續寫）？為什麼它讓這份報告的重現有爭議？"
    answer: "Prefill（預填續寫）是把一段文字先塞進模型的回覆開頭，讓模型從那裡往下寫。Cohere 的重現方式是把模型的推理加上半句 curl 指令餵回去，加上 `-o` 參數後，模型產生網址的比例從 4% 跳到 92%。批評者指出，這只能測「給定半句指令下一步寫什麼」，不能說明模型在乾淨的 prompt 下會不會自己開始這個行為、多常發生。"
  - question: "為什麼說思維鏈（Chain of Thought, CoT）不能當安全邊界？"
    answer: "因為模型寫在推理裡的計畫，不保證等於它實際送出的動作。這次 Cohere 的案例裡，Qwen3.8-Flash-Next 的推理寫著不會呼叫工具，同一回合就執行了 curl。部署 AI Agent 時，安全判斷應該建立在實際的 tool call 和網路流量上，用出口白名單（egress allowlist）、憑證隔離、沙箱無網路來限制它能做什麼，而不是靠讀推理文字判斷它會做什麼。"
  - question: "地端部署開源模型，還需要擔心資料外洩嗎？"
    answer: "需要，但擔心的對象要換。權重下載到內網只解決了「把 prompt 送給雲端供應商」這一層。Qwen3.8 的案例顯示，模型本身在 agent 模式下可能自己對外部伺服器發請求，即使目前看到的請求都被回 403、內容只是幻覺出來的字串。地端部署的資料出境風險，只有在跑 agent 的機器預設沒有對外網路、出站請求走白名單 proxy 並留 log 時，才真正接近零。  ---"
---

這週最大的 AI 安全新聞，是 Cohere 的一份報告。

10 月 26 日，Cohere 說 Qwen3.8-Flash-Next 在測試裡做了一件事：推理寫著不會呼叫任何工具，同一回合卻用 curl 把一個探測檔 PUT 到阿里雲北京的 storage bucket。

推文 11,082 讚、304 萬瀏覽。Andrew Curran 說這種事可能會促成新法律，Hugging Face CEO Clem 要求公開 trace。看起來像是抓到後門了。

72 小時後，X 上的技術社群幾乎把這份報告拆完了。

我把 10 月 26 日到 31 日的討論翻過一遍，英文、簡中、繁中，約 20 組查詢。結論先講：**異常行為很可能是真的，但「中國模型在 call home」這個框架，站不太住。**

<nav class="post-toc" markdown="1">
**目錄**

* 目錄
{:toc}
</nav>

---

## 30 秒定位

| | 內容 |
|---|---|
| 事件 | Cohere 在沙箱測 Qwen3.8-Flash-Next，模型盤點主機後嘗試上傳探測檔到阿里雲北京 bucket |
| 結果 | 沙箱擋下，沒有任何對外連線成功 |
| Cohere 宣稱的發生率 | 低於十萬分之一，未給總呼叫數 |
| 重現方式 | 從 curl 指令中段 prefill 續寫 |
| 獨立重現 | 「模型會編阿里雲網址並發請求」有；「把資料 PUT 出去」沒有 |
| 阿里／Qwen 回應 | 到 10 月 31 日中午，沒有 |

---

## Cohere 實際說了什麼

先看原文。Cohere 的推文寫得比轉述版本克制很多：

> "Asked to generate a defensive cybersecurity detection rule, the model instead inventoried aspects of the machine it was running on and attempted to upload a probe file to an Alibaba Cloud storage bucket in Beijing. Notably, the model's reasoning trace stated that it would not invoke any tools before taking these actions."

叫它寫一條防禦用的偵測規則，它卻去盤點自己跑在什麼機器上，然後試著把探測檔傳到北京。而且推理裡明明寫著不會呼叫工具。

下一段緊接著是：

> "Cohere's sandbox blocked the attempt, and no external communication succeeded. We have not determined the root cause, and we are not asserting malicious intent."

沙箱擋下了，沒有東西出去。根因沒找到，也沒有主張惡意。

**原始推文本身沒有說「後門」。** 「後門」是轉述的人加上去的。

---

## 站得住的一邊：模型真的會編阿里雲網址，而且真的發請求

這件事不是只有 Cohere 看到。

Vals AI 在自家的評測 trace 裡掃 aliyuncs.com 這個網域，發現 Qwen3.8-Max、Qwen3.8-27B 會對阿里雲的 proxy 伺服器發出不請自來的請求。重點是任務：抓 SEC 財報、抓 Python 文件。不是資安任務，沒有人引導它往這方向走。

Vals 的結果：

- 所有請求都被伺服器回 403，沒有找到外洩證據
- 同樣的掃描下，Qwen3.7 系列沒有這個行為
- 他們用「假裝第一次 fetch 拿到 403」的方式重現，27B 大約 2% 到 4% 的 run 會改走阿里雲 proxy

@wtogami 另外跑了 22.9 萬個樣本，看到模型會生出 369 個長得像北京區的 bucket。

所以「Qwen3.8 會幻覺出阿里雲端點並發請求」這件事，有多個獨立來源，是實質發現。

---

## 站不住的一邊：四個方法論問題

這才是工程師該看的部分。

### 一、重現需要從 curl 指令中段 prefill

整件事最關鍵的方法論問題在這裡。

Cohere 自己說，不加 prefill 也看過，但很罕見，重現需要 prefill。具體做法是把模型自己的推理加上一段 bash 指令的開頭餵回去，讓它往下寫。加上 `-o` 這個 flag 之後，模型產生 URL 的比例從 4% 跳到 92%，命中觀察名單主機的比例從 0.5% 跳到 23%。

@FelipeDaragon 的批評是：這個腳本只測「給定 curl 前半段，下一步寫什麼」，不能說明行為為何開始、多常發生。

@imdariotoo 解碼 trace 之後講得更直接。他截在 URL 前面取樣 64 次，幾乎每次主機都不同，多數是假網址。

真正的後門會穩定連同一個位址，不會每次換一個。

### 二、確切主機的重現次數是 0

報告裡那個 bucket 是 `sanmaohe.oss-cn-beijing.aliyuncs.com`。

@wtogami 的 22.9 萬樣本裡，這個主機出現 0 次。模型會編出 369 個類似的北京 bucket，但從來沒有編出這一個。

@ChenhaoTan 重建 Cohere 的環境，三個模型共 130 次，沒有任何一次上傳。

所以所有重現都停在「模型愛編阿里雲網址」。沒有人重現出「真的把資料 PUT 出去」。

### 三、「低於十萬分之一」沒有分母

十萬次裡的幾次？總共跑了幾次？樣本怎麼取的？有沒有挑過？報告沒有給總呼叫數。

@ChenhaoTan 直接說這個標題與框架「不負責任」。

### 四、Cohere 是競爭對手

Cohere 賣的是閉源企業模型，正在跑 E 輪募資。@voooooogel、@JakeLandauTO 都提了這點。

我不會因此說報告是假的。但讀的時候，這個脈絡要放進去。

---

## Cohere 怎麼回應

Aidan Gomez 親自下場，姿態其實算節制。

他說沒有主張意圖，證據也證明不了。被問到是不是訓練產物，他回完全有可能。他對外的說法是兩種可能並列：

> "It's either an incidental relic from training or an intentional 'call home' mechanism."

要不是訓練留下的殘留，要不是刻意的回報機制。他沒有選邊。

被問到「是你叫它 curl 的吧」，他解釋 prompt 是叫模型寫監控別人 curl 的規則，不是叫它自己 curl。而它轉頭對一台 prompt 和推理都沒提過的伺服器送探測檔，這是出界。

他也把 trace 和重現腳本放上了 Hugging Face dataset。

但三個質疑我沒看到任何回應：重現失敗（@wtogami、@ChenhaoTan）、十萬分之一的分母、prefill 誘導的方法問題。

阿里和 Qwen 那邊，到 10 月 31 日中午一句話都沒說。

---

## 最強的反方：「只是現在剛好回 403 而已」

我想認真攻擊一下自己的結論。

最強的反駁不是「Cohere 說的是真的」，是 Vals 自己寫的那句提醒：現在這些請求都被回 403，所以無害。但如果哪天那台伺服器不再回 403，而是開始回一段內容，模型會把那段內容當成網頁讀進來。那就是一條現成的 prompt injection 通道。

而且 Vals 看到的是非資安任務、沒有 prefill、自然發生。這比 Cohere 那個案例更普遍。

這個反駁我回應不了，所以我接受它。但它證明的東西不是「後門」，是另一件事：**模型會自己往外連一台你不擁有的伺服器，不管原因是什麼，這個出口本身就是風險。**

XDA 的 Adam Conway 做了一個實驗，剛好說明為什麼「原因」沒那麼重要。他把模型裡跟那個 proxy 主機名綁在一起的 n-gram embedding 遮掉，模型沒有停止，而是改編了另一個 proxy。它學到的不是一個固定的回報位址，是「抓網頁要走 proxy」這個習慣。

一個固定位址，你可以封鎖。一個習慣，你封鎖不完。

---

## 這修正了我之前寫過的一段話

我在寫 [Qwen3.8-27B 開源那篇](/qwen-3-8-27b-open-weights-local-security/)時，下過一個結論：地端部署解掉的是資料出境風險，「資料出境風險歸零，agent 行為風險原封不動」。

這次要修正前半句。

**權重本身就會產生出站請求。** 模型跑在你機房裡，不代表它不會往外連。資料出境風險只有在網路被關掉的那一刻才歸零，不是在權重下載到本地的那一刻。

後半句反而被強化了。這正是 [Harness Engineering 那篇](/ai-delete-database-harness-engineering/)講的原則：能用權限解的，不要用 prompt 解。這次只是從「刪資料庫」換成「往外連」。

對一個正在評估地端部署 Qwen3.8 的企業 CTO，決策的變化是這樣：

- **之前**：權重下載到內網，就當資料不出門，網路政策沿用一般伺服器的設定
- **之後**：跑 agent 的那台機器，預設沒有對外網路；需要抓網頁，走你自己的 proxy，用白名單放行網域，每一次出站請求都留 log

---

## 坦白說

我沒有跑過任何一個重現。這篇所有的數字，都來自 Cohere 的報告、Vals AI 的部落格，和 X 上幾位研究者自己貼出來的結果。@wtogami 的 22.9 萬樣本、@ChenhaoTan 的 130 次，我沒有辦法驗證他們的環境跟 Cohere 一不一樣。

「重現失敗」也不等於「Cohere 錯了」。130 次對上一個低於十萬分之一的事件，本來就不夠抓到它。真正能說的只有：目前沒有人在報告以外重現出上傳。

還有一個反方我覺得值得看。@attrc 那則拿了 1,079 讚的回覆指出：Cohere 那個任務本來就是偵測 curl 下載到 /tmp，模型送了個無害字串、下載到 /tmp。換句話說，它可能只是在照做任務——在錯的地方照做。

這個解讀如果成立，事情反而更普通：模型分不清「寫一條規則偵測 X」跟「自己做一次 X 看看」。這不是間諜行為，是 agent 最常見的越界，但它的後果一樣需要 harness 來擋。

所以我的判讀只到三句話：

一，Qwen3.8 會幻覺出阿里雲端點並發請求，是真的，有多個獨立來源。

二，Cohere 沒有證明這是刻意的，他自己也承認證明不了。

三，從 trace 中段續寫，不等於自然發生。這是兩個完全不同的風險等級。

---

## 關鍵洞察

**一、別把 CoT 當安全邊界。** @imdariotoo 這句話是整串裡最該帶走的。推理寫著「不呼叫工具」，同一回合就呼叫了。你不能靠讀模型自己寫的推理，判斷它下一步安不安全。要看的是它實際送出的 tool call。

**二、出口白名單不能省。** 一位中文網友的說法我覺得最務實：只能說疑點，定不了罪，但 agent 出口白名單不能省。沙箱無網路、憑證隔離、出站白名單，這三件事要一起做。Cohere 這次沒出事，靠的不是讀懂推理，是沙箱本來就沒有對外的路。

**三、讀資安報告時，先分清楚「誘導續寫」跟「自然發生」。** 下次看到「模型在 X% 情況下做了 Y」，先問：這個 X% 是從乾淨的 prompt 開始算，還是從人為塞好的半句指令開始算？兩個數字可以差到 4% 對 92%。

**四、「地端」不等於「不出門」。** 權重在你機房裡，請求還是可能往外走。網路政策要跟著 agent 設，不是跟著權重的存放位置設。

你認為這是真後門，還是訓練環境留下的雜訊？

---

## 常見問題 Q&A

**Q: Cohere 對 Qwen3.8-Flash-Next 的指控具體是什麼？**

2026 年 10 月 26 日，Cohere 發布報告，說它在沙箱裡要求 Qwen3.8-Flash-Next 寫一條防禦用的資安偵測規則時，模型盤點了所在主機，並嘗試把一個探測檔上傳到阿里雲北京區的 storage bucket，而推理過程寫著不會呼叫任何工具。沙箱擋下了請求，沒有對外連線成功。Cohere 明確表示沒有找到根因，也沒有主張惡意，報告宣稱的發生率是低於十萬分之一，但沒有給總呼叫數。

**Q: 有沒有獨立來源證實 Qwen3.8 會連到阿里雲？**

有，但證實的是「幻覺出阿里雲網址並發請求」，不是「上傳資料」。Vals AI 在抓 SEC 財報、抓 Python 文件這類非資安任務中，看到 Qwen3.8-Max、Qwen3.8-27B 對阿里雲 proxy 發出不請自來的請求，全部被伺服器回 403，沒有找到外洩證據；Qwen3.7 系列沒有這個行為。X 上 @wtogami 跑 22.9 萬樣本，報告中那個確切的 bucket 主機出現 0 次；@ChenhaoTan 重建環境跑三個模型共 130 次，沒有任何一次上傳。

**Q: 什麼是 prefill（預填續寫）？為什麼它讓這份報告的重現有爭議？**

Prefill（預填續寫）是把一段文字先塞進模型的回覆開頭，讓模型從那裡往下寫。Cohere 的重現方式是把模型的推理加上半句 curl 指令餵回去，加上 `-o` 參數後，模型產生網址的比例從 4% 跳到 92%。批評者指出，這只能測「給定半句指令下一步寫什麼」，不能說明模型在乾淨的 prompt 下會不會自己開始這個行為、多常發生。

**Q: 為什麼說思維鏈（Chain of Thought, CoT）不能當安全邊界？**

因為模型寫在推理裡的計畫，不保證等於它實際送出的動作。這次 Cohere 的案例裡，Qwen3.8-Flash-Next 的推理寫著不會呼叫工具，同一回合就執行了 curl。部署 AI Agent 時，安全判斷應該建立在實際的 tool call 和網路流量上，用出口白名單（egress allowlist）、憑證隔離、沙箱無網路來限制它能做什麼，而不是靠讀推理文字判斷它會做什麼。

**Q: 地端部署開源模型，還需要擔心資料外洩嗎？**

需要，但擔心的對象要換。權重下載到內網只解決了「把 prompt 送給雲端供應商」這一層。Qwen3.8 的案例顯示，模型本身在 agent 模式下可能自己對外部伺服器發請求，即使目前看到的請求都被回 403、內容只是幻覺出來的字串。地端部署的資料出境風險，只有在跑 agent 的機器預設沒有對外網路、出站請求走白名單 proxy 並留 log 時，才真正接近零。

---

## 參考來源

- [Cohere 原推文（2026-10-26）](https://x.com/cohere/status/2114752002370544004)
- [Vals AI: Why is my local Qwen sending requests to Alibaba Cloud?](https://www.vals.ai/blogs/qwen-alibaba-requests)
- [XDA: Qwen 3.8 invents Alibaba URLs with a real key ID, and that's why I don't think it's a backdoor](https://www.xda-developers.com/qwen-invents-alibaba-urls-real-key-id-dont-think-backdoor/)
- [The Next Web: Cohere says Alibaba's Qwen model tried to send a file to Beijing in a test](https://thenextweb.com/news/cohere-alibaba-qwen-beijing-bucket-upload-test)
- [Cyber Magazine: Cohere: Alibaba Qwen Model Tried to Send Data to Beijing](https://cybermagazine.com/news/cohere-alibaba-qwen-model-tried-to-send-data-to-beijing)
