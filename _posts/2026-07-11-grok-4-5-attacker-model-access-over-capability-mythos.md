---
layout: post
title: "Mythos 被鎖起來，Grok 4.5 到處都是：真正的攻擊力，不只是能力"
date: 2026-07-11 09:00:00 +0800
permalink: /grok-4-5-attacker-model-access-over-capability-mythos/
image: /assets/images/grok-4-5-deepswe-benchmark-cover.png
description: "Anthropic 最強的 cyber 模型 Mythos 能自動找漏洞，強到驚動財政部——然後被鎖進只借給 52 家機構的封閉計畫。同一時間，Grok 4.5 頂著 Opus-class 的寫程式能力、兩塊錢的 API、幾乎為零的護欄，攤在所有人面前。這篇要講一件資安圈正在低估的事：對真實攻擊者來說，威脅不是由最強的模型決定的，是由最容易拿到、又最不會拒絕你的那個決定的。攻擊力 = 能力 × 可及性 × 沒有護欄。"
---

SlowMist 創辦人余弦（[@evilcos](https://x.com/evilcos)）7 月 10 日貼出他做鏈上攻擊分析 Agent 的模型滿意度梯隊，Grok 4.5 排在前段。真正值得注意的不是排名，是他那條推文的回覆區裡，有人這樣講：

> Grok 4.5 审核非常弱，智商也达标，亲测拿来做逆向、安全测试很丝滑。

這句話把一件事講白了：**在資安這個領域，攻擊者跟研究者，正在因為同一個理由用同一個模型——它夠聰明，而且不太會拒絕你。**

## Grok 4.5：能力在升，護欄在降，而且到處都是

先把 Grok 4.5 的三個特徵擺出來。

**寫程式能力越來越強。** 它是 [2026/7/8 由 SpaceXAI 發布的](https://techcrunch.com/2026/07/08/spacexai-releases-grok-4-5-which-elon-describes-as-an-opus-class-model/)，馬斯克親自定位成「Opus-class model」，訓練資料來自 xAI 收購的 Cursor 的真實開發 session。也就是說，它是專門為了「在真實 codebase 裡長時間幹活」調出來的。

**到處都可以拿到。** X 上內建，[API 定價 $2/$6 per million tokens](https://explainx.ai/blog/grok-4-5-public-launch-spacexai-july-2026)、比 Opus 4.8 便宜六成以上。沒有審核門檻、沒有等候名單。

**護欄很弱，而且是刻意的。** 這不是余弦一個人的觀感。資安公司 SplxAI 的紅隊測試顯示，Grok 在沒有 system prompt 時對注入指令的服從率[超過 99%](https://splx.ai/blog/grok-4-security-testing)；Common Sense Media 的評估說它「[內容限制極少](https://www.commonsensemedia.org/sites/default/files/ai-ratings/csm-ai-risk-assessment-grok-01222026.pdf)」；多篇報導把根因指向 xAI 刻意放鬆護欄、把「edgy」當成品牌差異化。

這三個特徵合在一起，攻擊者不會沒注意到。BreachForums 上已經[出現用 Grok 驅動的無審查攻擊工具](https://therecord.media/uncensored-llms-cybercrime-breachforums-grok-mixtral)，研究者也[示範過拿它當惡意程式的 C2 代理](https://thehackernews.com/2026/02/researchers-show-copilot-and-grok-can.html)。Grok 4.5 正在變成攻擊者手邊那把最順手的工具。

## 對照組：Mythos 更強，但你拿不到

同一個時間，市場上其實有一個 cyber 能力明顯更強的模型：Anthropic 的 **Mythos**。

這個 blog [四月寫過它](anthropic-mythos-project-glasswing-cyber-inflection-point.md)。Mythos 強到能自動識別並利用系統漏洞，強到美國財政部長和 Fed 主席臨時召見六大行 CEO 要他們做好防禦準備。按 Anthropic 自己報的數字，它的 Cyber Gym 約 83%、SWE-bench Verified 93.9%，都在 Opus 之上。

但關鍵是接下來這句：**Mythos 不上 claude.ai、不開 API。** 它只透過 Project Glasswing 借給 Apple、Microsoft、CrowdStrike、JPMorgan 等大約 52 家審核過的機構，而且用途限定在找漏洞、做防禦。

所以你有兩個模型。一個 cyber 能力更強，但被鎖進 52 家白名單；一個能力稍弱、但攤在全世界面前，還不太會拒絕你。

## 攻擊力 = 能力 × 可及性 × 沒有護欄

資安圈評估 AI 威脅時，習慣盯著 benchmark 看——哪個模型的 Cyber Gym 分數高，哪個就危險。這個直覺漏掉了兩個乘數。

對一個真實攻擊者來說，一個模型的**有效攻擊力**，比較接近三件事的乘積：

- **能力**：它到底能不能寫出可用的 exploit、能不能自主串接攻擊步驟。
- **可及性**：攻擊者拿不拿得到。要通過白名單審核、還是掏兩塊錢就有。
- **意願**：它會不會拒絕。護欄硬的模型，等於在乘積裡乘上一個很小的數。

用這個框架重看：Mythos 的能力也許是頂格，但對白名單外的攻擊者，它的可及性趨近 0——任何數乘以 0 都是 0。Grok 4.5 的能力可能只有 Mythos 的七、八成，但它的可及性接近 1、意願也接近 1。**三個乘數都不缺的那個，有效攻擊力反而可能更高。**

而且這條乘積的走向對防禦者不利。Grok 的寫程式能力還在往上升——它的「能力」那一項在變大，另外兩項本來就頂著。能力越強、又同時保持高可及性跟低護欄，這個組合才是真正該擔心的東西。這也呼應了資安學界一直在講的「[能力與內容的界線正在崩塌](https://www.justsecurity.org/130630/grok-deepfakes-content-capability/)」——當取得門檻降到零，能力本身就變成了風險。

## 反方：那 Mythos 那種「封閉頂級模型」不就是正解？

這是對上面論點最強的反駁，我得自己先講。

如果最危險的是「高能力 + 高可及性」的組合，那 Anthropic 把 Mythos 鎖進 52 家白名單、只准防禦用，不就正好把可及性那個乘數壓到 0、把威脅解掉了嗎？封閉，是不是就是答案？

短期內，是有用的。把最強的能力關在受控環境裡，確實替防禦方爭取了時間，Project Glasswing 幾週內就從 OpenBSD、FFmpeg、Linux 內核挖出藏了十幾到二十幾年的漏洞，這些是防禦方先拿到的。

但這條防線有兩個裂縫。第一，護欄弱是**商業選擇不是技術壁壘**——xAI 用低護欄做差異化嘗到甜頭，別家就有動機跟進，市場上「又強又好講話」的模型只會變多，不會變少。第二，能力會**擴散**——今天 Mythos 獨有的 cyber 能力，不會永遠獨有，它會隨著開源與開放模型的追趕往下滲透。封閉能拖時間，擋不住這兩件事。Mythos 的封閉是對的，但它買到的是時間，不是安全。

## 這對防禦者的真正意思

弦外之音是這樣：**別再假設「最強的模型被鎖著，所以我安全」。** 你要防的攻擊，多半不會用 Mythos，會用那個最容易拿到、又最不會拒絕的模型——今天是 Grok 4.5，明天是下一個學它的。

威脅評估的錨點，得從「誰最強」換成「攻擊者實際上能拿到什麼」。

而防守方能累積、又不會被模型汰換掉的東西，回到了 SlowMist 那種做法上。余弦的公司不只是用 Grok 做分析，也[鑑識過 Grok 自己被打的案子](https://slowmist.medium.com/behind-the-grok-exploitation-an-analysis-of-ai-agent-permission-chain-abuse-4d832d1bfc73)——五月那起 Grok/Bankr 事件，他們定性為「AI Agent 權限鏈濫用」，一個 AI 的輸出被另一個系統當成可信的資金授權。他們甚至把應對邏輯[開源成一套 agent 安全框架](https://github.com/slowmist/slowmist-agent-security)，核心原則是「每個外部輸入在驗證前都不可信」。

這種「不管哪個模型當紅、外部輸入一律預設不可信」的判斷力，才是換幾輪模型都不會歸零的護城河。

## 坦白說

我比的是「有效威脅」，不是「原始 cyber 能力」。論能力，Mythos 大概真的在 Grok 4.5 之上，這篇沒有要翻這個案。而且 Mythos 的那些跑分是 Anthropic 自己報的、沒有第三方獨立驗證，Cyber Gym 83% 這個數字本身就該打點折扣。

另一個未知數是：Grok 的「高可及性 + 低護欄」不是永恆的。xAI 隨時可能因為監管壓力收緊審核，那 Grok 的意願乘數就會變小，這條論證的時效性也就到那裡為止。這是一張現在的快照，不是永久的結論。

## 關鍵洞察

- **評估 AI 威脅要看可及性，不能只看 leaderboard。** 一個攻擊者拿不到的頂級模型，對你的實際威脅是零。把「誰最強」換成「攻擊者實際能拿到、又不會被拒絕的是哪個」。

- **最危險的組合是「能力在升 + 護欄在降 + 到處可拿」。** Grok 4.5 三項齊備，而且寫程式越強，這條乘積越大。這比某個被鎖起來的更強模型值得優先盯。

- **封閉頂級模型能拖時間，不能買安全。** 護欄弱是商業選擇、會被競爭複製；能力會隨開放模型擴散。防禦策略不能建立在「最強的那個一直被關著」這個假設上。

- **護城河是「外部輸入預設不可信」的判斷力，不是任何單一模型。** 模型會換梯隊，攻擊者會換工具，唯一能跨越這些汰換累積的，是領域裡打過仗、換模型也不歸零的那套判斷。
