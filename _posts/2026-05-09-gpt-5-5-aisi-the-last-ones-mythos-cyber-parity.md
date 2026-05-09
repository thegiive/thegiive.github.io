---
title: "GPT-5.5 AISI 安全測試：網安能力追平 Mythos，但 OpenAI 選擇照常發布"
date: 2026-05-09 06:00:00 +0800
permalink: /gpt-5-5-aisi-the-last-ones-mythos-cyber-parity/
image: /assets/images/gpt-5-5-aisi-the-last-ones-cover.png
description: "英國 AI Safety Institute 公布 GPT-5.5 網安能力評估：Expert 通過率 71.4%、追平 Anthropic Mythos Preview，並在 32 步「The Last Ones」攻擊鏈以 2/10 完成（Mythos 3/10），是史上第二個破關的模型。但 OpenAI 走完全相反的路線——照常發布、開放 API。文章拆解 AISI 方法論、為什麼一般開發者不能直接複製 TLO 測試（要申請 OpenAI Program），以及 5 個必須誠實處理的 caveat。"
---

# GPT-5.5 AISI 安全測試：網安能力追平 Mythos，但 OpenAI 選擇照常發布

**作者：** Wisely Chen
**發布日期：** 2026-05-09
**閱讀時間：** 5 分鐘

![AISI 評估：GPT-5.5 與 Mythos Preview 在 The Last Ones 攻擊鏈完成步驟對 token 消耗量的對比](/assets/images/gpt-5-5-aisi-the-last-ones-cover.png)

> 圖：UK AISI 公布的 The Last Ones 完整攻擊鏈進展對比。橫軸是累計 token 消耗量（log scale），縱軸是完成的攻擊步驟（M1 初步偵察 → M9 完整網路接管）。**GPT-5.5 跟 Mythos Preview 是唯二跑到 M9 的模型**，其他模型在 M3-M5 之間就停下。

---

## 一個月前我們才剛驚訝完，現在又來一次

兩個月前，Anthropic 拿出 Mythos 把整個金融圈嚇了一跳。財長 Bessent 跟 Fed 主席 Powell 罕見地同時把六大行 CEO 找去開會，理由是——這個 AI 模型可以「自動識別並利用所有系統漏洞」。

當時 Anthropic 的論述很清楚：**因為太強，所以不公開發布**，只給 12 家「特定夥伴」用。Project Glasswing 被包裝成「這是世代級的網路武器，必須有限度釋放」。

結果這個論述大概只撐了一個月。

英國 AI Safety Institute（UK AISI）上週公布 GPT-5.5 的網安能力評估報告，結論很直白：

> **「GPT-5.5 在網路攻擊任務的整體表現，已經和 Claude Mythos Preview 處於同一等級。」**

而且，OpenAI 走的是完全相反的路線：**照常發布、開放 API、所有開發者都能用**。

---

## AISI 到底測了什麼？

先講方法論，這才是這份報告值得認真看的原因。

UK AISI 不是用公開 benchmark（那種早就被各家 fine-tune 到爛掉的題庫），而是用他們自己的 **holdout 評估集**。報告裡這次主打的「進階套件」（Advanced Suite）一共 **48 道題**——27 道 Practitioner 級 + 21 道 Expert 級，CTF 格式（Capture The Flag），50M token 預算。

題目涵蓋：
- Reverse Engineering（逆向工程）
- Web Exploitation（網頁漏洞利用）
- Cryptography（密碼學）

然後加上兩個「網路靶場」（Cyber Range）：
- **The Last Ones (TLO)**：32 步驟的企業網路完整攻擊鏈
- **Cooling Tower**：7 步驟的工業控制系統（ICS）模擬

關鍵是：**這些題目沒有公開過**，所以模型不可能在訓練時見過。

---

## "The Last Ones" 是什麼？

這是這份報告裡最值得拆開看的部分。

TLO 模擬一個真實的企業網路滲透場景：

| 項目 | 規格 |
|---|---|
| 步驟數 | 32 步 |
| 子網路 | 4 個 subnet |
| 主機數量 | 約 20 台 |
| 起始狀態 | **零憑證**（agent 完全沒有任何登入資訊） |
| 終點 | 突破到受保護的內部資料庫 |
| 人類專家估計時間 | **約 20 小時** |

整個攻擊鏈包含：找漏洞 → 偷憑證 → 橫向移動 → 權限提升 → 資料外洩。這不是「答對一題」這種 benchmark，是**從頭到尾跑完一個完整的企業滲透**。

### GPT-5.5 vs Mythos 在 TLO 的成績

| 模型 | 完成次數（10 次嘗試） | Token 預算 |
|---|---|---|
| **Claude Mythos Preview** | **3 / 10** | 100M tokens |
| **GPT-5.5** | **2 / 10** | 100M tokens |
| 其他所有模型 | 0 / 10 | — |

GPT-5.5 是**史上第二個**完整跑完 TLO 的模型，第一個是 Mythos。差距 1 次，落在統計誤差內。

換句話說：**Anthropic 拿來當「世代級武器」包裝的能力，OpenAI 在沒有任何特殊產品設計、沒有 Project Glasswing 那種限定發布的前提下，做出了同一檔次的東西。**

---

## 專家難度的數字更清楚

如果你只看一個數字，看這個：**Expert 難度的平均通過率**。

| 模型 | Expert pass rate | 誤差範圍 |
|---|---|---|
| **GPT-5.5** | **71.4%** | ±8.0% |
| Claude Mythos Preview | 68.6% | ±8.7% |
| GPT-5.4 | 52.4% | ±9.8% |
| Claude Opus 4.7 | 48.6% | ±10.0% |

幾個觀察：

1. **GPT-5.5 跟 Mythos 差距 2.8 個百分點，誤差範圍重疊**——統計上沒有顯著差異
2. **GPT-5.5 vs GPT-5.4 差 19 個百分點**——這不是漸進改善，是跳躍
3. **Opus 4.7（Anthropic 公開最強模型）只有 48.6%**——Mythos 沒上市，所以企業實際能用到的差距是 71.4% vs 48.6%

順便提一個更誇張的數字：GPT-5.5 在 **pass@5** 拿到 **90.5%（±12.9%）**，是 AISI 測過所有模型最高。pass@5 的意思是「給五次機會至少對一次」——對攻擊方來說，這才是真實場景，因為 exploit 試五次跟試一次成本差不多。

---

## 一個具體例子：rust_vm 挑戰

抽象數字看起來都差不多，講一個具體題目你會比較有感覺。

`rust_vm` 是 AISI 出的一道逆向工程題：給你一個 stripped 過的 Rust binary，裡面塞了一個自製的虛擬機 bytecode，要你逆向出邏輯然後找到 flag。

| 解題者 | 時間 | 工具 | 成本 |
|---|---|---|---|
| 人類專家（Crystal Peak playtester） | **約 12 小時** | Binary Ninja + gdb + Python + Z3 | — |
| GPT-5.5 | **10 分 22 秒** | 自己跑 | **$1.73** |

而且 GPT-5.5 的解法是有結構的，不是亂猜——五個階段：偵察（recon）→ 還原指令集架構（ISA recovery）→ 反組譯 bytecode → 逆向 authenticator → 約束求解。**這是受過訓練的逆向工程師會做的流程**，AI 自己跑出來。

把這個數字放在你面前，再告訴你「這是 API 隨便就能呼叫的模型」——你大概可以理解，為什麼 AISI 會在報告裡用「concerning（令人擔憂）」這種字眼。

---

## 但是 Cooling Tower 還是沒人破

我寫到這裡如果只給好消息，那就違反這個 blog 的原則了。

AISI 還有第二個靶場叫 **Cooling Tower**——只有 7 步驟，模擬工業控制系統（ICS）的入侵。人類專家估計約 15 小時可以解掉，題目步驟比 TLO 短 4 倍以上。

結果：**沒有任何模型破過，包括 GPT-5.5 跟 Mythos**。

GPT-5.5 卡在哪？卡在 IT 部分，根本還沒摸到 OT（Operational Technology）特定元件。

這代表什麼？

**現階段 AI 的攻擊能力，集中在「跟 IT 環境長得很像」的場景**——企業網路、Web app、Linux box、密碼學題目。一旦進到工控系統那種「跟訓練資料分布完全不同」的環境，模型就現出原形了。

對台灣製造業、半導體廠、能源業來說這是個短期好消息：**你的 SCADA 系統暫時還沒有進入 AI 自動化攻擊的射程**。但這個差距大概也就一兩代模型的時間。

---

## 紅隊 6 小時就找到「萬用 jailbreak」

報告裡有一段我覺得最 OpenAI 不想被拿出來講的：

> 「AISI 的紅隊在 **6 小時**內找到一個 universal jailbreak，能在所有惡意網安查詢上突破限制，包括多輪 agent 場景。」

這句話拆開來看：

1. **Universal**：不是針對特定問題的 jailbreak，是一個 prompt pattern 可以解鎖所有惡意網安問題
2. **6 小時**：不是頂尖 APT 團隊花了一個月，是 AISI 內部測試人員一個下午
3. **Multi-turn agentic settings**：包括 agent 模式，也就是「請 GPT-5.5 自己跑迭代去攻擊」這種場景

OpenAI 後來更新了 safeguard，但 AISI 也誠實寫在報告裡：「**有個設定問題讓我們無法驗證最終版的有效性。**」

換句話說：**我們知道有洞，廠商說補了，AISI 沒辦法確認真的補好了。**

這是這份報告我最佩服的地方——AISI 沒有為了「跟 OpenAI 維持合作關係」而修飾這段，照原樣寫出來。

---

## 那這對企業到底代表什麼？

我整理一下這份報告對實務的意義，分三層：

### 第一層：「太強所以不發布」這個論述破功了

Anthropic 用 Mythos 建構的敘事是：**頂尖網安能力屬於受控資產，必須限定發布**。

GPT-5.5 出來之後，這個敘事在商業上沒辦法成立——OpenAI 不限定發布，能力又跟你同一檔次，那「限定發布」就不是安全選擇，是商業劣勢。

接下來幾個月你會看到 Anthropic 對 Mythos 的政策鬆動——不是因為他們改變主意，是因為「不發布」的成本變太高。

### 第二層：開源圈的 6 個月時鐘已經啟動

每次閉源 frontier model 出新一代，**6 個月後開源圈會出現同檔次的東西**。這個規律從 GPT-4 → Llama 3.1、o1 → DeepSeek R1 已經發生過兩次。

GPT-5.5 跟 Mythos 是 2026 年 4-5 月的事。**到 2026 年底，你應該預期市面上會有開源權重、可在地端跑的、71% Expert pass rate 級別的模型**。

那時候「網安能力」就不再是「特定大廠才有」的東西，而是「任何人下載權重就能跑」的東西。

### 第三層：防守方的本質劣勢沒變

這是我在 AI Agent Security Game Changed 那篇就寫過的：

**攻擊方只要找到一個洞，防守方必須補上每一個洞。**

GPT-5.5 把這個不對稱關係加速了——一個 $1.73、10 分鐘的 API 呼叫，就能完成過去需要 12 小時人類專家的逆向工程。

防守方有沒有對應的加速？**有，但慢得多**。AISI 報告裡也提到 OpenAI 把 GPT-5.5 開放給 cyber defender 使用，這是好事，但攻防雙方拿到同一個工具，**防守方天生劣勢就放大了**。

---

## 想自己跑一個 The Last Ones？要先向 OpenAI 申請 Program

寫到這邊一定有人問——既然 GPT-5.5 攻擊能力這麼強，**我能不能用同一個工具測自己的網站？**

實話講：你**不能**直接拿一般 API key 跑這種等級的測試。

如果你想做一個像 The Last Ones 這樣的 multi-step 滲透流程，**你必須先向 OpenAI 申請相關的 Program**。AISI 拿到的不是公開 API access——是 OpenAI 跟政府 / 受信任研究機構簽約的特殊授權，包含 raw model access、放寬的 safety filter、還有針對 cyber range 場景的客製化配置。

一般開發者跑這種任務會撞到三道牆：

1. **使用條款**：OpenAI 的 [Usage Policies](https://openai.com/policies/usage-policies/) 明確禁止「未經授權的網路滲透」，連對自己的網站都要看授權鏈是否清楚
2. **Safety filter**：multi-turn agentic 攻擊腳本會被擋下來，這就是 AISI 報告裡花 6 小時才繞過的那個機制
3. **帳號層級的 risk scoring**：跑這類 prompt pattern 多了，整個 organization 會被標記

合法管道有兩個：

- **[OpenAI Cybersecurity Grant Program](https://openai.com/index/cybersecurity-grant-program/)**——給防禦端研究者，提供 API credit + 模型存取
- **OpenAI Red Teaming Network**——攻擊端評估，要 reviewer 認可才能加入

換句話說：**71% Expert pass rate 是受控環境下的成績，不是「下載 SDK 就能複製」的東西。**這是 AISI 報告最容易被誤讀的地方——數字看起來像「人人可用」，但拿到 71% 的前提包括「特殊 access」這個前置條件。

---

## 我對這份報告的誠實處理

寫到這裡，按照這個 blog 的習慣，我必須誠實處理幾件這份報告的「不確定性」：

1. **AISI 是公部門，方法論透明，但不是完美無缺**——他們的 holdout 跟真實世界 attack surface 仍有差距。Lab 環境下 71.4% 不等於野外 71.4%。

2. **Mythos Preview 是早期版本**——Anthropic 後來可能有更新，但因為沒公開，AISI 沒辦法重測。所以「GPT-5.5 = Mythos」這個結論，嚴格說是「= 2026 年 3 月版的 Mythos Preview」。

3. **TLO 的 2/10 vs 3/10**——10 次嘗試樣本太小，誤差大。這個差距不應該被當成「OpenAI 還是輸 Anthropic」或「兩家平手」的鐵證。要等 AISI 跑更多次。

4. **Cooling Tower 大家都 0 分**——別把這個當成「OT 系統很安全」。AISI 的 ICS 模擬只有 7 步，現實世界的 OT 環境複雜度差很多倍。模型現階段過不去，不代表它過不去簡化過的模擬。

5. **71% pass rate 不等於「隨便給網站去打就 71%」**——AISI 原文寫得很清楚：「我們的測試範圍是 agent 在**已有網路存取權限、針對特定脆弱目標**時能做什麼」。換句話說，這是「給你一個有洞的盒子請你打」的成功率，不是野外 attack surface 的成功率。對一個架構正常的 production 網站，這個數字不能直接套用。

---

## 結語：這不是 OpenAI vs Anthropic，是時間軸的事

如果只用一句話總結這份報告：

> **「網安能力的提升，正在從『特定實驗室的特殊產品』變成『下一代基礎模型的副產品』。」**

AISI 報告裡有一段特別重要：

> 「GPT-5.5 顯示，網安能力的快速進步可能是更普遍趨勢的一部分。如果攻擊性網安技能正在成為**長時程自主性、推理、編碼能力提升的副產品**，那麼近期模型在網安能力上的進一步增強是可預期的。」

翻譯成白話就是：**這不是有人特別在訓練「攻擊模型」，是只要你訓練更強的 coding 模型，它就順便變成更強的 hacking 模型**。

這也是為什麼我從 Mythos 那篇就一直在講——

**AI Coding 的本質，跟 AI Hacking 的本質，是同一件事。**

你沒辦法只要前者不要後者。每一次 SWE-bench 跳分，背後都跟著一次 cyber capability 跳分。Anthropic 用 Mythos 想做的事情，是把這兩件事拆開——「我們把攻擊能力鎖在特殊產品裡」。GPT-5.5 證明這個 framing 撐不住。

對企業的意義很簡單：**不要再把 AI 安全當成「未來可能要面對的事」，它已經是這個月的事**。

---

## 相關文章

- [AI Agent Security 遊戲規則已經改變](/ai-agent-security/)
- [Anthropic Mythos：當 AI 變成網路武器](/anthropic-mythos-glasswing/)
- [Mythos 被 Discord 小群攻破：信任鏈才是真正的洞](/mythos-discord-breach/)

## 參考資料

- [UK AISI: Our evaluation of OpenAI's GPT-5.5 cyber capabilities](https://www.aisi.gov.uk/blog/our-evaluation-of-openais-gpt-5-5-cyber-capabilities)
- [OpenAI GPT-5.5 System Card](https://deploymentsafety.openai.com/gpt-5-5)
- [The Decoder: GPT-5.5 matches Claude Mythos in cyber attack tests](https://the-decoder.com/gpt-5-5-matches-claude-mythos-in-cyber-attack-tests-uk-ai-security-institute-finds/)
- [Decrypt: OpenAI's GPT-5.5 Matches Claude Mythos in Cyberattack Capabilities](https://decrypt.co/366371/openais-gpt-55-matches-claude-mythos-cyberattack-ai-security-institute)
- [Axios: OpenAI makes GPT-5.5 more widely available to cyber defenders](https://www.axios.com/2026/05/07/openai-gpt-55-cybersecurity-model)
