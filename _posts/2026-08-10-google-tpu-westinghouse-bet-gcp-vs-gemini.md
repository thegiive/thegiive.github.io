---
layout: post
title: "Google、Musk、Meta 同時把算力賣給競爭對手：當三家公司做出同一個選擇，這不是巧合"
date: 2026-08-10 09:00:00 +0800
permalink: /google-tpu-westinghouse-bet-gcp-vs-gemini/
image: /assets/images/google-tpu-westinghouse-bet-cover.png
description: "2026 年，三家擁有自己模型的公司同時做了同一個選擇：Google 把 TPU 系統賣給 Anthropic 和 Meta（SemiAnalysis 預估 2027 年底外銷達 2000 億美元 vs Gemini ARR 120 億）；Musk 把 Colossus 1 整座 222,000 顆 GPU 租給 Anthropic（月租 12.5 億美元）；Meta 正在開發 Meta Compute 把剩餘 GPU 對外出租。三個獨立決策者到達相同結論：模型的營收天花板可見，算力的需求上限不可見。與其把所有算力留給自己排名第三、第四的模型，不如賣給每一家 lab 都搶著要的基礎設施。這是 Westinghouse 的賭注——散佈者贏，不是發明者。"
---

三天前我寫了 [Jeff Dean 離開 Google 的文章](/jeff-dean-google-career-tribute/)，回顧他用 27 年建立的基礎設施。MapReduce、TensorFlow、TPU——每一個都是讓 Google 自己的 AI 研究能站上去的地板。

現在 Google 正在把那塊地板賣給競爭對手。

---

## 事件背景：一週之內，三件事同時發生

2026 年 8 月 5 日，Google [宣布 AI 領導層重組](https://fortune.com/2026/08/05/demis-hassabis-steps-down-google-deepmind-ai-shakeup/)。Demis Hassabis 從 Google DeepMind CEO 轉任 Chairman，同時擔任 Alphabet Chief Scientist。接手日常營運的是 Koray Kavukcuoglu，DeepMind 創始成員之一，直接向 Sundar Pichai 匯報。

同日，Jeff Dean 宣布離開待了 27 年的 Google，與幾位同事成立新創。

同一週，SemiAnalysis 發表了一篇標題直白到不需要解讀的報告：["Gemini is Cooked but GCP is Cooking"](https://newsletter.semianalysis.com/p/gemini-is-cooked-but-gcp-is-cooking)。

三件事獨立發生，但指向同一個結論。

![DeepMind 佔 GCP AI 總算力的比例，從 2025 Q1 的約 45% 一路下滑到 2027 Q4 預估的約 14%（圖片來源：SemiAnalysis）](/assets/images/google-tpu-westinghouse-bet-cover.png)

---

## SemiAnalysis 的核心論點：Google 選了基礎設施，放了前沿模型

SemiAnalysis 的論證邏輯很簡單——看錢往哪裡流。

先看 GCP 這一側。[Alphabet Q2 2026 財報](https://finance.biggo.com/news/US_GOOG_2026-07-22)：Cloud 營收 248 億美元，年增 82%。Cloud 營業利益 88 億美元，營業利益率從去年同期的 20.7% 跳到 35.6%。[Cloud backlog 達到 5140 億美元](https://www.bloomberg.com/news/articles/2026-07-22/google-says-cloud-services-backlog-expands-to-514-billion)，季增超過 500 億。

82% 的成長率裡，有一個新的組成部分：Q2 首次認列 TPU 系統外銷營收——Google 開始把整套 TPU 系統賣給外部客戶，安裝在客戶自己的資料中心裡。[Sundar Pichai 在 earnings call 上說](https://www.cnbc.com/2026/07/22/google-earnings-q2-goog-live-updates.html)，這季的金額還是「小數目」，大量營收會在 2027 年認列。

SemiAnalysis 估算這個「小數目」大約是 12 億美元。扣掉這部分，核心 Cloud 成長率在 low 70s——依然很強，但 TPU 外銷把數字再推高了一截。

再看 Gemini 這一側。SemiAnalysis 估算 Gemini 目前的 ARR 約 120 億美元。

然後是 SemiAnalysis 的預測——以下數字全部出自他們的報告，不是 Google 官方數據：

| 項目 | SemiAnalysis 預估（2027 年底） |
|------|------|
| 第三方 AI 基礎設施營收 | ~$730 億 |
| TPU 系統外銷營收 | ~$1200 億 |
| 外部銷售合計 | ~$2000 億 |
| EBIT margin | high-30s% |
| Gemini ARR（現值） | ~$120 億 |

$2000 億 vs $120 億。比值接近 17:1。

---

## 買家是誰：把最好的晶片賣給最直接的競爭對手

這不是賣給中立的企業客戶。

SemiAnalysis 報告指出，從 Q3 2026 到 Q4 2027，**超過 20% 的 TPU 總出貨量直接賣給 Anthropic**。這還不包括已經租給 Anthropic 和 Meta 的大量 TPU。

2025 年 10 月，[Anthropic 宣布與 Google 和 Broadcom 擴大合作](https://www.anthropic.com/news/google-broadcom-partnership-compute)，規模達到多個 GW 級的下一代 TPU 容量，預計 2027 年起上線。[CNBC 報導](https://www.cnbc.com/2025/10/23/anthropic-google-cloud-deal-tpu.html)交易價值數百億美元。

Anthropic 的年化營收已經[超過 300 億美元](https://finance.yahoo.com/sectors/technology/articles/anthropic-google-broadcom-tpu-deal-113234906.html)。Claude Opus 4.8 在 LMArena 排名上壓著 Gemini 3.1 Pro。

Google 正在把自己最好的晶片，以最大的量，賣給排名超過自己的競爭對手。

---

## 更大的圖景：TPU 從研究工具變成商品

幾個數字把規模感拉出來。

SemiAnalysis 報告中的估算：TPU 系統外銷定價約 350 億美元/GW。目前已有超過 1500 億美元的 TPU 系統 backlog，未來可能再增加 2500 億美元以上的訂單。

如果這些數字成立，2027 年 GCP 的成長率將進入 mid-100s%——而目前[賣方共識只有 64%](https://newsletter.semianalysis.com/p/gemini-is-cooked-but-gcp-is-cooking)。光是成長率加速這一項，就可能為 Google 2027 年的 EPS 增加約 3 美元。

[Tomasz Tunguz 的分析](https://tomtunguz.com/google-cloud-hyperscaler-to-hardware/)更直白：Google Cloud 的營收成長率正在收斂到 NVIDIA 的成長率。GCP 不再只是雲端服務商，它正在變成硬體公司。

Tim O'Reilly 上週寫了一篇 ["Google's Westinghouse Bet"](https://asimovaddendum.substack.com/p/googles-westinghouse-bet)，用電力產業的歷史類比來描述這個策略。Thomas Edison 發明了燈泡和發電系統，但最後贏得電力戰爭的是 Westinghouse——他沒有執著於自己發電、自己用電，而是把交流電基礎設施賣給所有人。

O'Reilly 引述 GCP CEO Thomas Kurian 的定位：TPU 要成為 "general-purpose infrastructure"，服務對象從 Citadel Securities 到美國能源部，不限於 Gemini 研究。

---

## 衝突檢查：Jeff Dean 27 年建的地板，現在被用來墊別人的腳

這篇文章和[三天前的 Jeff Dean 文章](/jeff-dean-google-career-tribute/)放在一起看，會浮現一個刺眼的對比。

Dean 的職涯主線是：在 Google 即將被規模壓垮時，重新設計基礎設施，讓複雜度變成 Google 工程師可以站上去的地板。MapReduce 讓 Google 自己處理全球搜尋資料。TensorFlow 讓 Google 自己的研究者訓練大模型。TPU 讓 Google 自己的 AI 推論經濟可行。

每一個都是「建來給自己用」的基礎設施。

現在 Google 的策略是把 TPU 整套系統賣給 Anthropic、Meta、和任何付得起的人。Dean 建的地板，被用來讓競爭對手站上去。

Dean 離開的時間點——就在這個策略轉向公開化的同一週——很難不被解讀為某種表態。

再往前拉，2025 年初我寫過一篇 [AI 前沿格局文章](/ai-frontier-landscape-shift-2025/)，核心論點是「人才是真正的護城河」。當時分析的是 OpenAI 的人才流失導致技術停滯。Google 現在面臨的模式驚人地相似：人才離開（Dean + 多位 RL 團隊成員），加上算力重新分配，兩個護城河同時鬆動。

差別在於，OpenAI 2024 年的人才流失是被動的（人走了）。Google 2026 年的算力重分配是主動的——他們選了錢。

但這裡有一層更深的東西。xAI 賣算力、Meta 賣算力，你可以理解——他們本來就不是以前沿研究為核心使命的組織。

Google + DeepMind 不一樣。這是 AlphaGo 的 DeepMind。這是 Transformer 論文的 Google。這是理論上全世界最有資格做前沿 AI 研究的地方——人才密度最高、算力最充沛、研究歷史最深。如果連這個組織都決定「算力拿去賣比拿來做研究更划算」，那訊號非常清楚：管理層已經不把前沿模型領先當成最高優先級了。

站在 Jeff Dean 和 DeepMind 科學家的角度，這個訊號幾乎無法忽視。你加入這裡，是因為這裡應該是前沿科技的燈塔——全世界最好的算力、最好的同事、最大的研究自由度。現在公司告訴你，燈塔的電力要優先賣給隔壁的人。

難怪他們要走。不是因為 Google 對他們不好，是因為 Google 對前沿研究的優先級排序變了。對一個科學家來說，算力被重新分配，和實驗室被關掉，傳遞的是同一個訊息。

---

## 決策換位：如果你是企業 CTO

這個策略轉向改變了一個具體的決策。

**之前**：你評估雲端 AI 供應商時，Google 是「模型 + 基礎設施」一站式供應商——用 Gemini 做推論，跑在 GCP 的 TPU 上，整合度最高。

**之後**：Google 正在把自己定位成「基礎設施商」，而不是「模型商」。GCP 的增長引擎是賣 TPU 給第三方，不是靠 Gemini 的 ARR。

這代表什麼？**你在 GCP 上跑其他前沿模型的可行性和支援力道可能會越來越好——甚至好過 Gemini 本身。** 因為 Google 的利益已經從「推你用 Gemini」轉向「讓你在我的硬體上跑任何模型」。付大錢買 TPU 系統的 Anthropic 和 Meta，才是 GCP 現在最重要的客戶。多模型策略的企業用戶反而搭上了這個順風車。

但反過來：如果 Google 不再全力投入前沿模型，你對 Gemini 的長期競爭力就需要打一個問號。在選擇「哪個模型做為核心推論引擎」這個決策上，Gemini 的 roadmap 風險上升了。

---

## 不只 Google：Musk 和 Zuckerberg 也在做同一件事

如果只有 Google 這樣做，你可以說這是 Thomas Kurian 贏了內部政治。但 2026 年，三家擁有自己模型的公司同時做了同一個選擇。

**xAI / Musk。** 2026 年 5 月，[Anthropic 與 SpaceX 簽約](https://www.tomshardware.com/tech-industry/artificial-intelligence/musks-spacex-has-rented-out-access-to-its-supercomputers-220-000-nvidia-gpus-and-300-megawatts-of-ai-compute-power-to-rival-anthropic-musk-says-no-one-set-off-my-evil-detector-antrhropic-also-interested-in-orbital-data-centers)，取得 Colossus 1 的完整獨佔使用權——222,000 顆 NVIDIA GPU（H100/H200/GB200 混合）、300+ MW 電力，[月租 12.5 億美元，合約到 2029 年 5 月，總值超過 400 億美元](https://letsdatascience.com/blog/anthropic-pays-musk-1-25-billion-month-colossus)。

Colossus 1 是 xAI 在 2024 年建來訓練 Grok 的。現在 xAI 把訓練搬到了更大的 Colossus 2（2 GW、555,000 顆 GPU），[Colossus 1 整座租給了 Grok 的直接競爭對手](https://deshpandetanmay.medium.com/xai-just-leased-222-000-gpus-to-anthropic-the-math-says-its-surrendering-5427b29172ae)。

**Meta / Zuckerberg。** Meta 今年的前沿模型已經從開源的 Llama 換成了閉源的 [Muse Spark](https://about.fb.com/news/2026/04/introducing-muse-spark-meta-superintelligence-labs/)——由 Alexandr Wang 領軍的 Meta Superintelligence Labs 開發，4 月發布，目前到 1.2 版。但即便如此，Meta 仍在同步開發名為 ["Meta Compute" 的雲端服務](https://mlq.ai/news/meta-unveils-meta-compute-cloud-business-to-sell-excess-ai-infrastructure-to-outside-customers/)，計劃將 $1250-1450 億基礎設施投資產生的剩餘 GPU 容量對外出租。Zuckerberg 的說法是：[如果基礎設施建設產能超過內部需求，就把多餘的賣給外部客戶](https://www.cloudcomputing-news.net/news/meta-ai-cloud-business-excess-compute/)。服務尚未正式上線，但已經進入高層人事指派和產品架構設計階段。

三家公司。三個自有模型（Gemini、Grok、Muse）。同一個結論：**與其把所有算力留給自己的模型，不如把算力賣出去。**

邏輯幾乎完全一致，而且底層原因不難理解。

---

## 為什麼是現在：模型生意的天花板開始浮現

三家公司同時做這個選擇不是巧合，是因為模型的商業結構經過三年沉澱，輪廓已經清楚了。

2023 年 ChatGPT 爆發時，沒有人知道模型生意的上限在哪裡。市場總規模是一個問號，而問號在資本市場代表無法定價的上檔空間——這是最好的故事。每一家有模型的公司都在賭自己的模型會成為下一個 Windows，所有算力都應該留給自己的模型訓練。

三年後，幾件事變了。

**雲端模型市場的上限開始可見。** 不是說已經觸頂——Anthropic 的年化營收從 2025 年底的 90 億美元[跳到 2026 年超過 300 億](https://finance.yahoo.com/sectors/technology/articles/anthropic-google-broadcom-tpu-deal-113234906.html)，成長率依然驚人。但營收模型已經確定了：API 按量計費、訂閱制、企業合約。分析師可以建模了。可以建模就意味著可以算出上限，而「可以算出上限」和「上限是無限」在資本市場的估值邏輯裡是完全不同的東西。

**開源模型確保了沒有人能壟斷。** DeepSeek V4 Flash 是 MIT 開源的，284B 參數，性價比的 Pareto 最優解。這裡要非常感謝 Meta——Llama 是 AI 開源的第一個火種，屬於人類的第一個火苗。雖然 Meta 自己後來轉向了閉源的 Muse Spark，但火苗已經點燃了整片草原：DeepSeek、Qwen、GLM、Mistral，開源生態成型了。就算某家 lab 真的做出 AGI 等級的模型，開源替代品會在幾個月內追上到「夠用」的程度——這意味著定價權永遠受壓。模型生意不可能變成壟斷利潤。

**追趕 SOTA 的成本已經高到連 Google 都花不起了。** 前沿模型的軍備競賽是人才、數據、算力三管齊下。2026 年訓練一個 frontier model 的算力成本已經到了數十億美元等級，還沒算上頂尖研究員的薪酬和獨家數據的取得成本。Google 的年度 CapEx 已經拉到 [$2050 億](https://www.cnbc.com/2026/07/22/google-earnings-q2-goog-live-updates.html)，就算是這個數字，也不足以同時支撐 GCP 擴張和 DeepMind 無限制的算力需求。連口袋最深的公司都得做選擇，那不如學 DeepSeek 的「老四哲學」——不追第一，用更聰明的架構和更少的算力做出「夠強」的模型，把省下來的資源拿去賺確定的錢。DeepSeek 用這套邏輯活得很好；Google 只是把同一套邏輯用在了更大的尺度上。

這兩件事加在一起，改變了一道關鍵的數學題：**把算力留給自己的模型，預期回報是一個有上限的市場裡排第三、第四的份額；把算力賣出去，預期回報是每一家 lab（包括排第一的）都要付的基礎設施費用。**

對 Google 來說，這道數學題的答案是 $120 億 vs $2000 億。對 Musk 來說，是 Grok 的訂閱收入 vs Colossus 1 月租 $12.5 億。數字不同，結論一樣。

你可以把這理解成「獲利了結」——不是對 AI 本身的悲觀，而是對「自己做模型」這門生意的重新定價。算力是確定的現金流，模型是有上限的成長故事。資本市場會選哪一個，不需要猜。

但如果你往回看，會發現一個很刺眼的分界線：**退出前沿模型競賽的，全是上市公司。還在拼命追 AGI 的，全是未上市公司。**

Google（上市）→ 賣 TPU。Meta（上市）→ 賣算力。xAI（透過上市的 SpaceX 持有基礎設施）→ 租 GPU。

OpenAI（未上市）→ 繼續追 GPT-6。Anthropic（未上市）→ 繼續追 Claude 5。Moonshot/KIMI（未上市）→ 繼續追前沿。DeepSeek（未上市，幻方量化子公司）→ 繼續追開源前沿。

這不是巧合。未上市公司需要前沿模型的領先度來撐「本夢比」——投資人買的是「這家公司可能做出 AGI」的故事，而不是今年的營收。一旦你的模型不再領先，下一輪估值就會出問題。所以他們沒有退出的選項。

上市公司面對的是完全不同的壓力。華爾街不買「可能做出 AGI」，華爾街要看營收成長率、EPS、和利潤率。當你手上有 $2000 億的確定營收可以報，沒有理由拿股東的錢去賭一個不確定能贏的模型競賽。

換一種方式說：**前沿模型競賽的終點不是 AGI，是 IPO。** 一旦 OpenAI 和 Anthropic 上市，他們面對的壓力和 Google 今天面對的一模一樣——股東會問：你為什麼不把算力賣掉？

---

## 反方：也許 Google 根本不需要前沿模型

最強的反駁不是「Gemini 會追回來」——而是「追不追回來可能不重要」。

Google 有一個其他模型廠商都沒有的東西：生態系。搜尋、Gmail、Workspace、Android、YouTube、Maps——全球超過 20 億用戶每天都活在 Google 的產品裡。Gemini 不需要是 benchmark 上的第一名，只要「夠好」，就能透過這個分發管道觸及所有人。Claude 再強，也得靠使用者主動去找它；Gemini 只要內建在 Gmail 的回信按鈕裡，就贏了分發。

前沿模型正在趨向同質化，差距是歷史上最小的。如果模型本身不是長期護城河，那決定勝負的就是兩件事：誰有分發管道，誰有基礎設施。Google 兩個都有。

Westinghouse 的歷史支持這個論點。Edison 發明了燈泡，但電力產業的贏家是把交流電基礎設施鋪到全美國的 Westinghouse。發明者不一定贏，散佈者才贏。

如果這個類比成立，Google 正在做的事情就不是「放棄模型」，而是「看穿模型會變成 commodity，用生態系分發自己的模型，用基礎設施賺所有人的錢」。

---

## 坦白說

SemiAnalysis 的預測數字（$730 億 + $1200 億 = ~$2000 億）是他們自己的模型推估，不是 Google 公布的指引。Google 財報裡確認了 TPU 系統外銷的存在和 82% 的 GCP 成長率，但未公布 TPU 外銷的具體金額拆分。SemiAnalysis 的 $12 億 Q2 貢獻也是反推值。

「賣方共識 64%」vs「SemiAnalysis 預估 mid-100s%」的差距之所以這麼大，主要原因是 TPU 系統外銷採 gross basis 認列——整套硬體的全額營收進 GCP 的帳，而不是只記服務費。這會讓成長率數字看起來很驚人，但利潤率結構和純雲端服務不同。SemiAnalysis 估 high-30s EBIT margin，這個數字的可靠度無法從外部驗證。

另一個需要打折的地方：Westinghouse 類比聽起來漂亮，但電力和 AI 模型有一個結構性差異。電是高度同質化的 commodity——你家的燈泡不在乎電從哪個發電廠來。AI 模型至少目前還有差異化。Claude 和 Gemini 在不同任務上表現不同，使用者確實會因為模型差異而選擇供應商。如果前沿模型沒有走向同質化，而是持續分化，「不投模型、只賣硬體」就不是 Westinghouse 的勝利，而是放棄了最有價值的差異化來源。

最後一點：DeepMind 內部是否真的因為算力被抽走而導致 Gemini 落後，這是外部觀察者（包括 SemiAnalysis）的推論，不是 Google 的自述。Google 宣布的是領導層調整和 Gemini 4 的開發計畫，沒有說「我們把算力從 DeepMind 搬去 GCP」。因果關係是分析師的判斷，不是已確認的事實。

---

## 關鍵洞察

**這不是 Google 的個案，是產業級的收斂。** Google 賣 TPU 給 Anthropic、Musk 把 Colossus 1 整座租給 Anthropic、Meta 準備把多餘 GPU 對外出租——三家擁有自己模型的公司，在 2026 年同時做了同一個選擇。當三個獨立決策者到達相同結論，它反映的通常不是巧合，而是底層經濟邏輯的改變：模型的營收天花板可見，算力的需求上限不可見。

**$120 億 vs $2000 億的算術題。** Google 的取捨——把 TPU 外銷給競爭對手而不是全留給 DeepMind——不是失誤，是計算過的。如果 SemiAnalysis 的預測接近現實，近期 GCP 的財務回報遠大於 Gemini 可能產生的收入。xAI 的算術更直白：Colossus 1 租給 Anthropic 一個月 $12.5 億，比 Grok 的訂閱收入可觀得多。批評這些公司「放棄 AI 領先地位」之前，先看一眼營收比。

**前沿模型同質化是這個賭注成立的前提。** 2026 年 LMArena 頂端 55 Elo 的差距是歷史最小值。如果這個趨勢持續，模型變成 commodity，基礎設施就是真正的護城河。但如果某家 lab 突破性地拉開差距（像 2022-2023 年 GPT-4 獨領風騷那樣），所有選擇「賣算力不做模型」的公司，都會發現自己成了 Anthropic 和 OpenAI 的後勤補給站，而不是競爭者。

**對企業 CTO 的實際影響：供應商的利益結構正在重新排列。** Google 從「Gemini 綁定」轉向「模型中立」，Meta 可能很快提供 GPU 租賃——這意味著你在 GCP 上跑其他前沿模型的支援力道可能會越來越好，甚至好過 Gemini 自己，因為付大錢買 TPU 的 Anthropic 才是 GCP 最重要的客戶。但如果你是押注單一供應商模型做核心推論引擎的客戶，重新評估 roadmap 風險是值得的。不是說 Gemini 或 Grok 會消失，而是它們在母公司內部的優先級，已經不如算力外銷的營收。
