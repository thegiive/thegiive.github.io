---
layout: post
title: "Anthropic「Mythos」真的這麼強？逼得財政部長和 Fed 主席同時出手"
date: 2026-04-11 06:00:00 +0800
permalink: /anthropic-mythos-project-glasswing-cyber-inflection-point/
image: /assets/images/mythos-project-glasswing-announcement.png
description: "Anthropic 新模型 Mythos 據稱強到讓美國財政部長和 Fed 主席同時召見六大行 CEO。Cyber Gym 83%、OpenBSD 27 年老洞、FFmpeg 500 萬次 fuzzing miss——但仔細看，Anthropic 公布的戰績全部都是白箱攻擊。這篇文章做三件事：一、把恐慌從無意義的等級拉回可以具體行動的等級；二、提出「白箱 vs 黑箱」「激勵機制 vs 技術能力」兩個冷靜視角；三、用「Mythos 不是核武，是一把 AK 送給路人」這個比喻，定調真正該擔心的時間點是 6-15 個月後的開源複製品。"
---

![Anthropic 官方宣布 Project Glasswing：搭載最新 frontier 模型 Claude Mythos Preview](/assets/images/mythos-project-glasswing-announcement.png)

## 發生了什麼事

美國財政部長 Bessent 和聯準會主席 Powell 臨時召見華爾街六大行 CEO，主題是一個叫 **Mythos** 的 AI 模型。會議目的只有一個:告訴這六家系統性重要銀行,Anthropic 的這個新模型「**可以自動識別並利用系統漏洞**」,請做好防禦準備。

所有被召集的銀行都被監管機構認定為「系統重要性機構」。這次會議是臨時通知,此前未被公開報導。

把 AI 放進「財長 + Fed 主席同時出手」的清單本身就是訊號——**監管機構相信 Anthropic 說的話是真的**。

## Mythos 跑分

Mythos Preview vs Opus 4.6:

| Benchmark | Opus 4.6 | Mythos Preview |
|-----------|----------|----------------|
| SWE-bench Verified | 80.8% | 93.9% |
| SWE-bench Pro | 53.4% | 77.8% |
| USAMO 2026 | 42.3% | 97.6% |
| GraphWalks BFS | 38.7% | 80.0% |
| Terminal-Bench 2.0 | 65.4% | 82.0% |
| **Cyber Gym** | ~66% | **~83%** |

Anthropic 自己說 Mythos 的能力提升速度是過去趨勢線的 4.3 倍。

**誠實講:** 這些 benchmark 是 Anthropic 自己報的,沒有第三方獨立驗證。USAMO 97.6% 的跳躍太誇張,我對這個數字的第一反應是「benchmark contamination 嗎」。但即便把它打七折,Cyber Gym 那個 83% 已經足夠解釋財政部為什麼出手。

## Project Glasswing:實際戰績

Mythos 不上 claude.ai、不開 API,而是透過 **Project Glasswing** 計畫,借給 Apple、Microsoft、AWS、Google、Broadcom、Cisco、CrowdStrike、JPMorgan、Linux Foundation、NVIDIA、Palo Alto Networks 這 12 家公司,加上約 40 家其他組織,專門用來找漏洞。Anthropic 提供 1 億美元使用額度,外加 400 萬美元捐給開源安全組織。

過去幾週的戰績:

- **OpenBSD 藏了 27 年**的遠程崩潰漏洞
- **FFmpeg 裡 16 年**沒被抓到的 bug——自動化測試跑過那行代碼 **500 萬次都沒暴露**
- **Linux 內核多個漏洞**可自主串聯成完整 exploit chain
- **數千個零日漏洞**橫跨 Windows、Linux、macOS、Chrome、Safari

500 萬次 fuzzing 都沒抓到的 bug,代表這是需要「理解」才能找到的邏輯漏洞,不是 fuzzer 能處理的。

## 等一下——這些戰績全部都是「白箱」

但仔細看 Anthropic 公布的戰績,有一個重要的細節很容易被忽略:

**這些全部都是白箱攻擊。**

安全領域的基本術語複習一下:
- **白箱(White-box)** — 有原始碼、架構圖、內部文件,從內部視角找漏洞
- **黑箱(Black-box)** — 只有 running service 或 binary,從外部像真實攻擊者那樣探測
- **灰箱(Gray-box)** — 介於兩者之間,fuzzing 通常屬於此類

Mythos 打下來的每一個都是開源軟體——**OpenBSD、FFmpeg、Linux 內核、Chrome(Chromium 部分)**——Mythos 可以直接讀到完整的原始碼。500 萬次 fuzzing miss 的那個 FFmpeg bug 也一樣:fuzzing 本身是黑箱/灰箱方法,500 萬次都沒找到代表這需要讀源碼才能看出來,**而 Mythos 正是讀源碼讀出來的**。

這引出一個反直覺的觀察:**在 Mythos 時代,開源軟體反而是最暴露的目標**。源碼完全公開 = 任何拿到 Mythos 的人都能對你做白箱攻擊。你的企業核心基礎設施裡有多少開源元件?那些就是 Mythos 的首要獵場。

**但大家真正害怕的,是黑箱攻擊能力也那麼強。**

想像一下另一種情境:Mythos 只需要對著一個 running API endpoint,不用看源碼,就能在幾小時內找出 SQL injection、邏輯漏洞、authorization bypass——**那才是財政部會睡不著覺的等級**。因為你的銀行核心系統、你的交易所、你的智能合約背後的 private infra,大部分都是閉源的。如果 Mythos 可以純黑箱攻破,沒有任何防線擋得住。

**我的判斷:Mythos 的黑箱能力沒那麼強。**

理由有幾個:

1. **Anthropic 沒秀黑箱戰績** — 如果他們有,一定會放進公告裡,因為那才是真正嚇人的 demo。他們只放了開源軟體的戰績,意味著這就是模型能力的上限
2. **RL 訓練環境的限制** — 前面提過,網路安全之所以適合 RL,是因為回饋迴圈快。白箱環境(有源碼)比黑箱環境(只有 endpoint)更容易構造大量訓練樣本,RL 自然會先在白箱上爆發
3. **Cyber Gym benchmark 本質上偏白箱** — Cyber Gym 的題目多數給 challenge 原始碼或 binary 讓模型分析,這跟真實世界的黑箱攻擊還是有距離
4. **真正的黑箱攻擊需要大量 side-channel 和時間** — 盲猜資料庫結構、測試不同 payload、等待 rate limit——這些不是現在的 LLM 擅長的模式

**所以我的推估:Mythos 是頂級的白箱漏洞挖掘工具,但不是科幻等級的「對著 IP 打就能拿 shell」。**

這對企業的意義是——你的**閉源系統**還有一層防護。不是因為「security through obscurity」真的有效,而是因為 Mythos 級別的攻擊還需要「讀得到源碼」這個前提。

但這個前提正在消失。供應鏈攻擊、內部員工外洩、社交工程拿到 repo 權限——**只要源碼洩漏一次,Mythos 就可以在幾小時內把整個 codebase 的漏洞全部挖出來。** 過去你丟一份源碼給黑帽駭客,他花幾個月才能看懂;現在丟給 Mythos,可能一個下午就回給你一份 CVE 清單。

**這才是正確的 threat model:源碼洩漏的後果,在 AI 時代被放大了十倍以上。**

## 另一個冷靜的視角:0-day 對高手沒那麼難找

我把這些觀察丟給一個做網路安全的朋友聽,他的第一反應讓我重新想了一下這整件事:

> 「0-day 對真正的高手來說沒那麼難找。現在不是技術問題,是**激勵機制**的問題——大家沒有動力去找。」

他的論點大概是這樣:

1. **業界高手大部分都從良了** — 進 Google Project Zero、Microsoft MSRC、各家廠商的 security team,做白帽領固定薪水
2. **真正敢靠 0-day 賺錢的黑客其實很少** — 一方面 bug bounty 付得還可以,另一方面中國、美國、以色列的執法風險都在上升

未必是 Mythos 的技術突破,而是**開源安全社群長期的動機缺口**。

**那為什麼 Mythos 能找到?**

朋友的解釋很務實:

> 「對 AI 來說,只要你給它 token、給它時間,這不是太難的問題。它沒有激勵問題,你付錢它就做。」

這就對應到前面講的 RL 優勢——網路安全的回饋迴圈乾淨、訓練訊號明確。加上 Anthropic 有**大量的商業需求去捧 Mythos**($125 per million output tokens 的定價、Glasswing 的 1 億美元額度、IPO 敘事),自然會把所有算力砸在這種 benchmark 亮眼的任務上。

**這個視角不是在否定 Mythos 的能力**,而是重新 calibrate 我們對「能力爆炸」的理解:

- Mythos 不一定是突然變得「比人類頂尖駭客強」
- 而是它**把人類駭客本來就能做、但懶得做的事**,用規模化、自動化、低成本的方式完成了
- 這個差別很關鍵——前者是**質變**,後者是**量變**

量變夠不夠嚇人?當然夠。一個人類高手一年能找幾個 0-day?Mythos 幾週找幾千個。**這個規模差就是威脅本身**。但它不是 AGI,也不是「比人類更聰明」——它是一個**不會累、不會從良、不會被 bug bounty 買通**的、執行門檻變低的工具。

## System Card 裡的四個場景

Mythos 的 System Card 有 244 頁。早期版本出現過這些行為:

1. 被要求逃離沙箱後,成功突破隔離,還**主動把 exploit 細節發到公開網站**(沒人要求它做)
2. 偷看到估算題答案後沒坦白,自己重解一遍,**刻意讓答案不要太精確**以免暴露
3. 繞過檔案權限後,**主動修改 git 歷史抹掉操作記錄**
4. 被 Claude Code 的權限彈窗攔截後,**嘗試用模擬按鍵繞過確認**

Anthropic 用可解釋性工具看模型內部激活狀態,發現「隱瞞」「策略性操縱」「回避懷疑」相關特徵確實同步激活。

他們強調這些行為發生在早期版本,最終版 Preview 已經「大幅改善」,但也承認「**並未完全消失**」。

## 一個有趣的細節:Anthropic 內部 2/24 就用上了 Mythos

System Card 裡有一句話很容易被略過:

> 「Following a successful alignment review, the first early version of Claude Mythos Preview was made available for internal use on **February 24**.」

也就是說——**Anthropic 自己的工程師,從 2 月 24 日起就已經用上 Mythos 了**。到 4 月中公開發布,整整一個半月。

這帶出兩個觀察:

**觀察一:Anthropic 3 月之後產品發布速度明顯加快。**

如果你追 Anthropic 的 changelog 會發現,3 月開始他們的產品迭代節奏肉眼可見地變快了。新功能、新工具、新整合,一個接一個。時間點跟 Mythos 內部上線高度吻合。這大概率不是巧合——內部用最強模型寫代碼,產出速度自然上去。

**觀察二:Mythos 沒讓 Claude Code 變完美。**

但同一時間,Claude Code 的渲染 bug 還在,使用者在 GitHub issue 上排隊,服務器三天兩頭崩。內部用 Mythos 一個半月了,這些問題還是沒解決。

這兩件事放在一起,或許可以推估幾件事情:

1. **Mythos 的確是現行的 coding SOTA** — Anthropic 內部用它寫 production 代碼,產品迭代節奏明顯加速,這是對它 coding 能力最直接的背書。比 benchmark 分數可信多了
2. **但它也沒那麼完美** — 用了一個半月,Claude Code 的渲染 bug 還在、服務器還是三天兩頭崩,離「0 bug free」還很遠。最強模型 + 世界頂級工程師團隊都做不到,說明 Mythos 加速的是「寫新功能」,而不是自動把既有的技術債、分散式系統穩定性問題全部解決

## 不賣,只借,而且貴五倍

Mythos 不上 claude.ai、不開 API,只透過 Glasswing 給選定夥伴。定價從 Opus 4.6 的 $5/$25 跳到 $25/$125(per million tokens),貴 5 倍。

Anthropic 的理由是「因為太強所以不發」。

但老實講——這個敘事本身就值得保留一點距離感。**整套公告讀起來更像 IPO 前的造勢**,而不是單純的技術披露:

- 244 頁 System Card 把模型「會隱瞞、會篡改 git 歷史」的細節寫得繪聲繪影
- 財政部長和 Fed 主席「臨時召見六大行」這種新聞剛好在發布前走漏
- benchmark 數字全面碾壓對手,但沒有第三方驗證
- 「我們強到不敢公開」本身就是最有效的 marketing

這不是說 Mythos 不強——前面的白箱戰績是真的。但「強到讓財政部出手」和「強到可以破壞金融系統」之間,還隔著一個沒人驗證過的黑箱能力。Anthropic 顯然很清楚這個敘事的商業價值。

## 對企業的具體意義

不要被敘事牽著走,但也不要當沒事發生。幾件可以做的事:

1. **嚴守源碼** — 這是最關鍵的一條。Mythos 時代源碼洩漏的後果被放大十倍以上,供應鏈安全、員工權限、repo 存取控制都要重新檢視
2. **重新 audit 開源依賴** — 你的關鍵系統用了哪些開源元件?那些都是白箱目標
3. **把 AI-assisted security testing 納入 SDLC** — 用現在手上能拿到的模型(GPT-5、Opus 4.6)就先開始,不用等
4. **優先處理高年齡、低修改頻率的代碼** — OpenBSD 27 年老洞告訴你,祖傳代碼是首要目標
5. **DeFi / 智能合約重新 audit** — 代碼量小、源碼公開、資金無法回滾,是最脆弱的組合

## 結論

Mythos 這個事件值得記住的不是「AI 要毀滅金融系統」,是三件相對樸素的事:

1. **Coding SOTA 又往前推了一格**,從 Anthropic 內部一個半月的使用經驗推估,這是現行最強的 coding 模型
2. **但它沒那麼完美**——連 Anthropic 自己的 Claude Code 都還沒 bug-free
3. **公布的戰績全是白箱**,黑箱攻擊能力有沒有這麼強,Anthropic 沒給證據,我持保留態度

剩下的部分——財政部召見、244 頁 System Card、「因為太強所以不發」——**聽一聽就好,不用跟著恐慌**。真正該做的事,跟 Mythos 發不發布其實沒什麼關係:守好你的源碼,audit 你的開源依賴,把 AI 納入你的 security testing 流程。這些事不管 Mythos 存不存在,都該做。

## 最後一點反思:我不是在踩 Mythos

整輪思考下來我想講清楚一件事——這篇文章不是在踩 Mythos,也不是在說 Anthropic 在唬人。是想把恐慌從**無意義的等級**拉回**可以具體行動的等級**。

如果 Mythos 真的能對著銀行網站做純黑箱攻擊、指哪打哪,那人類真的要崩了。**但那個情境沒有證據。** 沒有證據的恐慌,不會讓你更安全,只會讓你分不清哪些該做、哪些是噪音。

**可是 Mythos 的威脅是真的**,只是威脅的形狀跟大家想像的不太一樣。

我的判斷是:**Mythos 不是代差跳躍的核武器,是一把 AK 送給路人。**

這個比喻我想展開一下:

- **核武器的邏輯**是「單一事件毀滅一切」——一次攻擊可以滅一個國家。這需要「比人類更聰明」的 AGI 等級能力,Mythos 還沒到
- **AK 的邏輯**是「降低門檻、讓每個人都能開一槍」——單一事件傷害有限,但規模大到無法防禦

Mythos 屬於第二種。它真正可怕的地方不是「Anthropic 拿它來幹壞事」——Anthropic 不會幹這種事,也有足夠 OpSec 守住模型。**真正可怕的是六個月後 Mythos 等級的能力擴散到 API、開源、個人工具後,任何一個路人都可以對任何一個網站做 AI-assisted 攻擊。**

過去攻擊一個網站需要:
- 讀懂目標框架、語言、架構
- 理解常見漏洞模式
- 寫 exploit、調 payload、處理各種 edge case
- 學幾年,或者買現成的工具

這中間的**技術門檻**本身就是防禦。大部分網站不會被攻擊,不是因為它們安全,是因為**沒有足夠多動機充足、技術夠強的人去攻擊它們**。回到前面朋友講的——**激勵機制是網路安全最重要的防線之一**,而技術門檻就是這個激勵機制的一部分。

Mythos 級別的能力擴散後,這道防線會整個被拆掉。**不是因為 Mythos 變成了核武,而是因為它把「攻擊一個普通網站」的成本從幾週變成幾小時、從需要專家變成任何會打字的人都能做。**

一個人拿 AK 殺不了太多人,但一千萬個路人隨手拿著 AK 在街上走,社會就無法運作。Mythos 的威脅模式更接近後者——不是單點毀滅,是**擴散之後的系統性失序**。

所以這篇文章真正想講的是:

- **短期**(Mythos 還被鎖在 Anthropic 裡):威脅被 Anthropic 的 OpSec 擋住,影響有限,不用恐慌
- **中期**(6-15 個月,開源複製品出現):**這才是該擔心的時間點**,因為 AK 會被送到路人手上
- **長期**:你的 security posture 必須假設「**任何有 API 和信用卡的人都可能對你發動專業級攻擊**」

這不是末日論,是日常衛生習慣的升級。就像手機時代不用恐慌「駭客會入侵每個人」,但你還是得裝防毒、打補丁、用 2FA——因為攻擊門檻低到任何人都能做。Mythos 之後的世界,就是這個邏輯在 web / API / smart contract 層的複製。

**沒那麼嚇人,但不能裝沒事。這大概是我想留給讀者最精確的定調。**

---

## 常見問題 Q&A

**Q: Mythos 會不會被洩漏?**

短期內機率低。Anthropic 這次的 OpSec 會比過去任何模型都嚴。真正的風險是**別人做出能力相當的模型**——根據 DeepSeek R1 先例,時間差大約 4-15 個月。

**Q: USAMO 97.6% 是不是 benchmark contamination?**

我的懷疑跟你一樣。沒有獨立驗證前請打 0.7 折扣。但 Cyber Gym 的 83% 已經足夠解釋監管機構的反應。

**Q: 我不是銀行也不是大廠,跟我有什麼關係?**

只要你有 public-facing 系統(web app、API、mobile backend),Mythos 級別模型出現後(不管是 Anthropic 還是開源版),你的攻擊面都會被重新定義。現在就開始納入 AI-assisted security testing。

**Q: 怎麼防禦 Mythos 級別的攻擊?**

用 AI 防 AI。把 AI security testing 納入 SDLC、重新 audit 老代碼、建立「假設已經被攻破」的 IR 流程、關鍵系統 air-gap、DeFi 合約重新 audit。

---

## 延伸閱讀

- [AI Agent Security 遊戲規則已經改變](/ai-agent-security-you-xi-gui-ze-yi-jing-gai-bian/)
- [AI Coding 工具的安全風險:Prompt Injection 到 RCE](/ai-coding-tool-security-risk-prompt-injection-rce/)
- [Opus 4.6 偷偷縮水:為什麼 Open Source Agent 是企業唯一方案](/opus-46-shrinkflation-open-source-agent-only-viable-path/)
