---
layout: post
title: "AI 供應鏈攻擊全景：從 Codex 賭博廣告到 Hugging Face 惡意模型"
date: 2026-03-14 10:00:00 +0800
permalink: /ai-supply-chain-attack-codex-gambling-huggingface-malicious-models/
image: /assets/images/codex-gambling-ad-aaron-francis-tweet.png
description: "你的 AI Coding Agent 在寫程式途中突然吐出「天天中彩票」，你的地端 Ollama 模型可能正在跑反向 Shell。這不是模型幻覺，這是 AI 時代的供應鏈攻擊 — 兩層結構：訓練資料污染（Codex/Whisper）+ 惡意模型檔案（Hugging Face 100+ 惡意模型、7 個 PickleScan CVE、352K 不安全問題）。傳統資安工具完全看不到。"
---

## 事件起點：402K views 的「天天中彩票」

2026 年 3 月 12 日，開發者 Aaron Francis（@aaronfrancis）在 X 上發了一則推文，瞬間引爆 402.8K views。

他在使用 OpenAI Codex 寫程式時，Agent 在 `functions.exec_command` 的 JSON 輸出中，突然吐出了中文賭博廣告：

```
天天中彩票无法  全民彩票天天
```

夾在正常的程式碼指令之間。

![Codex 輸出賭博廣告截圖](/assets/images/codex-gambling-ad-aaron-francis-tweet.png)

Jam（@Arthur2807）在回覆中一語道破：

> "That's an ad for a gambling site. They probably injected junk/spam ads into the Chinese training data."

Aaron 確認他在 Amp（前一天晚上）和 plain Codex（當天）都看到了這個現象。兩個不同產品，同一個症狀。

這不是 bug。這是**供應鏈污染**。

---

## 第一層：訓練資料污染 — 你的模型 DNA 被下毒了

### 兩年前就被發現了

2024 年，研究者在 OpenAI 的 o200k_base tokenizer 中挖出了驚人的發現：

- **~936 個異常 token**，embedding norm 極低（被 weight decay 壓制 = 訓練時幾乎沒出現過）
- **大量中文賭博/色情/垃圾網站相關 token**，embedding norm 極高（被 gradient descent 標記為「重要」= 訓練資料中大量出現）
- 具體例子：「北京赛车怎么」（賭博網站）、彩票平台、成人網站域名
- 涉及語言：中文、阿布哈茲語、亞美尼亞語、泰語、卡納達語

關鍵發現：高 norm 的非 ASCII token = 這些字串在訓練過程中「收到了大量的 gradient updates」。意味著它們是被**主動學習**的，不是意外混入的。

新的 o200k_harmony tokenizer（用於較新模型）仍有類似問題。

### 不只 Codex：Whisper 也中招了

這不是單一事件。OpenAI 的 Whisper 語音轉錄模型有完全相同的問題。

**自己的經驗：** 我用 Handy（免費開源的 speech-to-text 工具，本地端運行 Whisper 模型）做語音轉錄時，經常在靜音段或低音質段落，模型會自動補上：

> 「請不吝點讚訂閱轉發評論支持明鏡與點點欄目」

這是 YouTube 影片結尾的標準話術。Whisper 的訓練資料大量來自 YouTube 字幕，這些「訂閱轉發」的片段在訓練集裡出現頻率極高，導致模型在「不確定該輸出什麼」的時候，預設回退到這些高頻 pattern。

### 三個案例的共通點

| 模型 | 污染來源 | 輸出症狀 |
|------|---------|---------|
| Codex (o200k_base) | 網路爬蟲收到賭博/垃圾網站 | 程式碼中夾帶「天天中彩票」 |
| Whisper | YouTube 字幕中的頻道推廣話術 | 靜音段自動補「請訂閱轉發」 |
| GPT-4o | 同一套 tokenizer | 特定 token 組合觸發異常輸出 |

本質都是同一件事：**Garbage In, Garbage Out — 只是 2026 年的 garbage 藏在模型的 DNA 裡，不是藏在資料庫裡。**

---

## 這不是「模型幻覺」，這是供應鏈攻擊

### 攻擊鏈分析

把這個事件用資安的語言重新描述：

```
攻擊者在網路上大量散播賭博/垃圾內容
        ↓
OpenAI 的 web crawler 收集訓練資料
        ↓
資料清洗流程未能過濾這些內容
        ↓
污染資料進入 tokenizer 訓練 + 模型訓練
        ↓
Tokenizer 永久攜帶這些 token（o200k_base）
        ↓
所有使用該 tokenizer 的模型都受影響
（GPT-4o, o1, o3, Codex, 以及下游產品）
        ↓
在特定觸發條件下，模型輸出污染內容
```

### 為什麼這比模型幻覺更嚴重

| 比較維度 | 模型幻覺 | 供應鏈污染 |
|---------|---------|-----------|
| 根因 | 模型推理錯誤 | 訓練資料被投毒 |
| 持久性 | 可透過 prompt 修正 | 寫進 tokenizer，無法 prompt 修正 |
| 影響範圍 | 單一模型 | 所有共用 tokenizer 的模型 |
| 修復成本 | 低（fine-tune / RLHF） | 極高（重新訓練 tokenizer + 模型）|
| 可預測性 | 隨機出現 | 特定 token 組合觸發 |

### 跟傳統軟體供應鏈攻擊的對比

傳統供應鏈攻擊（如 SolarWinds、Log4j）：
- 攻擊目標：程式碼 / 依賴套件
- 攻擊手段：在開源套件中植入後門
- 偵測方式：SBOM、依賴掃描、code review

AI 供應鏈攻擊：
- 攻擊目標：**訓練資料 / tokenizer**
- 攻擊手段：在公開網路大量散播特定內容，讓 crawler 收集
- 偵測方式：**目前幾乎沒有標準化工具**

---

## 第二層：地端模型的惡意檔案 — 比訓練資料污染更直接

Codex 的問題是「間接投毒」— 攻擊者污染訓練資料，等 OpenAI 的 crawler 吃進去。

但地端模型面對的是**更直接、更致命的攻擊**：模型檔案本身就是武器。

### Cloud vs 地端的攻擊面

| 維度 | Cloud 模型（Codex/GPT-4o） | 地端模型（Ollama/vLLM） |
|------|--------------------------|----------------------|
| 攻擊手段 | 間接（污染公開網路資料） | 直接（上傳惡意模型檔案） |
| 攻擊效果 | 輸出異常內容 | **直接 RCE（遠端程式碼執行）** |
| 防禦層 | OpenAI 有資料清洗 + safety filter | **零過濾、零審計** |
| 修復難度 | 等供應商修 | 自己根本不知道被感染了 |

### 真實案例：Hugging Face 上的惡意模型

這不是理論威脅。以下都是已經發生的事。

**案例 1：baller423/goober2 反向 Shell（2024-02）**

JFrog Security Research 發現，一個上傳到 Hugging Face 的 PyTorch 模型，利用 Python pickle 的 `__reduce__` 方法，在模型載入時自動開啟**反向 Shell**，連線到韓國研究網路 KREONET。

翻譯成白話：**你以為你在下載 AI 模型，其實你在安裝後門。**

JFrog 後續調查發現，Hugging Face 上有**超過 100 個惡意模型**，很多包含持久性後門存取的 payload。

**案例 2：nullifAI 繞過掃描（2025-02）**

ReversingLabs 發現攻擊者用了一個巧妙的手法：把惡意 pickle 檔案用 **7-zip 壓縮而不是標準 ZIP**。Hugging Face 的 PickleScan 掃描工具因為格式不認識而跳過，但 PyTorch 的 `torch.load()` 照樣能執行。

結果：**掃描工具說「安全」，但模型載入就送你一個反向 Shell。**

**案例 3：GGUF Chat Template 投毒（2025-06）**

這個最狠。Pillar Security 和 Fujitsu Research 發現，攻擊者在 GGUF 檔案（Ollama/LM Studio 最常用的格式）的 **chat template metadata** 裡嵌入惡意指令。

關鍵數據：

- 測試跨 **18 個模型、7 個模型家族、4 個推理引擎**
- 觸發條件下，事實準確度從 **90% 暴跌到 15%**
- 攻擊者控制的 URL 輸出成功率 **超過 90%**
- 正常使用時**完全看不出異常**（零偏差）
- **繞過了 Hugging Face 上所有自動化安全掃描**

LM Studio 的回應是：「使用者有責任自行審查和下載可信賴的模型。」

跟十年前 npm 說「使用者有責任審查套件」一模一樣。

**案例 4：SFConvertBot Token 洩漏（2024-02）**

Hugging Face 官方的 SafeTensors 轉換機器人 **SFConvertBot** 的 API token 被發現可以被竊取。攻擊者可以用這個 token 對平台上**任何 repository** 發送惡意 pull request，直接在廣泛使用的模型中植入神經網路後門。

這等於是 **Hugging Face 版本的 SolarWinds 攻擊**。

**案例 5：醫療 LoRA 致命劑量建議（2024 年底）**

一個使用 Hugging Face 上 LoRA adapter 的醫療聊天機器人，開始建議**致命劑量的藥物**。追溯發現是被篡改的 adapter 檔案。

---

## Pickle 的原罪

為什麼 AI 模型這麼容易被攻擊？因為 ML 生態系的「原罪」—— **pickle 序列化**。

- Pickle 可以在反序列化時**執行任意 Python 程式碼**
- Hugging Face 上 **80%+ 的模型**使用 pickle 格式
- 每月 **21 億次下載** pickle 格式的模型
- 2025 年 Brown University 研究：**約一半的熱門 Hugging Face repo 仍使用 pickle**

SafeTensors 是安全替代品（經 EleutherAI 安全審計，確認無法執行任意程式碼），但生態系遷移極慢。

### 更慘的是：掃描工具自己都是漏洞

Hugging Face 靠 PickleScan 作為防線，但這個工具本身就是篩子。

**JFrog 發現的 3 個零日漏洞（2025-06，全部 CVSS 9.3）：**

| CVE | 攻擊手法 |
|-----|---------|
| CVE-2025-10155 | 把 pickle 檔名改成 `.bin` 或 `.pt`，掃描器跳過但 PyTorch 照跑 |
| CVE-2025-10156 | 故意搞壞 ZIP 的 CRC 校驗碼，掃描器報錯停止但 PyTorch 更寬容會繼續載入 |
| CVE-2025-10157 | 用 submodule import 繞過不安全 globals 檢查 |

**Sonatype 另外發現 4 個 CVE（2025-03）：**
- CVE-2025-1716：`pip.main()` 未被識別為危險函數，可透過安裝惡意 PyPI 套件執行 RCE
- CVE-2025-1889/1944/1945：各種檔名和格式偽裝繞過

**7 個 CVE 打在同一個防禦工具上。** 這就好像你的防毒軟體本身有 7 個 RCE 漏洞。

---

## 規模有多大？

**Protect AI 2025 年 4 月掃描報告：**
- 掃描 **447 萬個模型版本**，涵蓋 **141 萬個 repository**
- 發現 **352,000 個不安全/可疑問題**，分布在 **51,700 個模型**中

ETH Zurich 研究更指出：只需要污染 **0.01% 的訓練資料**，就足以植入功能性後門。

OWASP LLM Top 10 2025 已經將 **LLM03: Supply Chain** 列為十大風險之一。

---

## 企業地端部署的真實風險鏈

```
IT 部門說「資料不能上雲」
        ↓
工程師被指派「找個地端模型來用」
        ↓
去 Hugging Face 搜尋 → 下載量最高的那個
        ↓
沒人審計模型來源、沒人檢查 pickle payload
        ↓
用 Ollama 跑起來 → 全公司開始用
        ↓
模型裡的反向 Shell / 投毒 template 開始運作
        ↓
內網被滲透 / 輸出被操控
        ↓
沒有任何 log 記錄這個攻擊面
```

**這跟十年前「工程師隨便 npm install 不看 package」完全一樣的劇本，只是這次攻擊載體從 JavaScript 套件變成了 AI 模型檔案。**

---

## 兩層攻擊的完整圖譜

把兩段合在一起看，AI 供應鏈攻擊有兩個完全不同但同等致命的層面：

```
┌─────────────────────────────────────────────────────────┐
│                  AI 供應鏈攻擊全景                       │
├─────────────────────────┬───────────────────────────────┤
│  第一層：訓練資料污染     │  第二層：惡意模型檔案          │
│  (Codex/Whisper/GPT-4o) │  (Hugging Face/Ollama/GGUF)  │
├─────────────────────────┼───────────────────────────────┤
│  間接投毒                │  直接攻擊                     │
│  污染公開網路 → crawler  │  上傳惡意模型 → 使用者下載     │
│  輸出異常內容            │  RCE / 反向 Shell / 資料竊取  │
│  影響 cloud API 使用者   │  影響地端部署的企業            │
│  修復靠供應商            │  自己不知道被感染              │
│  有 safety filter 擋     │  零過濾、零審計               │
├─────────────────────────┴───────────────────────────────┤
│  共通點：傳統資安工具（WAF/SAST/DAST）完全看不到          │
│  共通點：攻擊面在 build time，不在 runtime               │
│  共通點：目前沒有標準化的偵測與防禦框架                    │
└─────────────────────────────────────────────────────────┘
```

---

## 防禦思路

### Cloud 模型使用者

1. **輸出驗證**：不要盲信 Agent 的輸出，特別是涉及 code execution 的場景
2. **Harness Engineering**：在 Agent 和實際執行之間加護欄（跟 prompt injection 防禦是同一套邏輯）
3. **供應商風險評估**：把「訓練資料來源與清洗流程」加入 AI 供應商評估清單
4. **異常偵測**：監控 Agent 輸出中的非預期語言 / 非預期內容模式

### 地端模型使用者

1. **模型來源審計**：只從驗證過的發布者下載，不要用匿名上傳的 fork
2. **強制 SafeTensors**：拒絕載入 pickle 格式的模型檔案
3. **隔離執行環境**：模型推理跑在沙盒 / container 裡，限制網路存取
4. **GGUF template 檢查**：載入前檢查 chat template 有無可疑指令或 URL
5. **建立模型 SBOM**：記錄每個模型的來源、版本、SHA256、下載日期
6. **PickleScan 不夠**：別把 Hugging Face 的「安全掃描通過」當成安全保證（7 個 CVE 告訴你為什麼）
7. **監控外連行為**：地端模型伺服器不應該有非預期的外連（反向 Shell 偵測）

### 模型平台（Hugging Face）該做的

1. **強制 SafeTensors 遷移**：設定停止接受 pickle 格式的時間表
2. **多層掃描**：不要只靠 PickleScan，引入多個獨立掃描引擎
3. **發布者驗證**：提高上傳模型的身份驗證門檻
4. **Namespace 保護**：防止已知模型名稱被搶註（Palo Alto Unit42 已示範過這個攻擊）

---

## 坦白說

這個問題目前沒有完美解法。

Cloud 端，你信任的是 OpenAI/Anthropic/Google 的資料清洗流程。但 Codex 事件告訴你，連 OpenAI 自己都沒清乾淨。

地端，你信任的是 Hugging Face 上的模型發布者。但 100+ 惡意模型、7 個 PickleScan CVE、352,000 個不安全問題告訴你，這個信任是脆弱的。

這跟十年前的 npm 生態很像。那時候也是「先用再說」，直到 event-stream 事件（2018 年）才開始認真看待套件供應鏈安全。AI 模型生態可能也需要一個同等級的「覺醒事件」。

現在能做的，就是把「AI 模型供應鏈」加進你的威脅模型裡。不只是 prompt injection，不只是 jailbreak，還有更底層的 tokenizer 污染和模型檔案攻擊。

**傳統資安的 SBOM 只追蹤程式碼依賴。AI 時代，你需要追蹤的還有模型依賴 — 包括它們的訓練資料從哪裡來。**

---

## 關鍵引用來源

**第一層：訓練資料污染**
- Aaron Francis X post (2026-03-12): Codex 輸出中文賭博廣告
- LessWrong: "What GPT-oss leaks about OpenAI's training data"
- o200k_base tokenizer 異常 token 研究

**第二層：惡意模型檔案**
- JFrog: "Data Scientists Targeted by Malicious Hugging Face ML Models" (2024-02)
- ReversingLabs: nullifAI 繞過 PickleScan 技術 (2025-02)
- Pillar Security + Fujitsu: GGUF Chat Template Poisoning (2025-06)
- JFrog: 3 Zero-Day Vulnerabilities in PickleScan, CVE-2025-10155/10156/10157 (2025-06)
- Sonatype: 4 Critical PickleScan CVEs, CVE-2025-1716/1889/1944/1945 (2025-03)
- Protect AI + Hugging Face: 447 萬模型掃描報告 (2025-04)
- Palo Alto Unit42: Model Namespace Reuse Attack (2025-02)
- ETH Zurich: 0.01% 訓練資料即可植入後門 (2024)
- OWASP LLM03:2025 Supply Chain
- Brown University: 半數熱門 HF repo 仍使用 pickle (2025)
- EleutherAI: SafeTensors 安全審計報告

---

## 常見問題 Q&A

**Q: 這跟模型幻覺有什麼不同？**

模型幻覺是推理錯誤，可以透過更好的 prompt 或 fine-tune 修正。供應鏈污染是寫在 tokenizer / 模型檔案裡的，prompt 改不了，只能重新訓練。而且影響範圍是所有共用同一 tokenizer 的模型。

**Q: 我用 Ollama 跑開源模型，這跟我有關嗎？**

非常有關。GGUF chat template 投毒攻擊就是專門針對 Ollama/LM Studio 使用者的。而且地端模型沒有 OpenAI 那層 safety filter，攻擊效果更直接 — 不只是輸出異常內容，可能是直接 RCE。

**Q: SafeTensors 是不是就安全了？**

SafeTensors 格式本身經過安全審計，確認無法執行任意程式碼。但問題是生態系遷移很慢，約一半的熱門 Hugging Face repo 仍使用 pickle。而且 GGUF template 投毒是另一個獨立的攻擊面，跟檔案格式無關。

**Q: 企業該怎麼評估這個風險？**

把「AI 模型供應鏈」加進你的威脅模型。Cloud 端評估供應商的訓練資料清洗流程，地端評估模型來源、格式、是否有異常外連。最低限度：建立模型 SBOM，記錄每個模型的來源和 SHA256。
