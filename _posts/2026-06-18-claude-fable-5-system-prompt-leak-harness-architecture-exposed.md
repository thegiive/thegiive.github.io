---
layout: post
title: "Fable 5 後面不是模型，是一個 Harness 系統——就像一個 Claude Code"
date: 2026-06-18 07:16:38 +0800
permalink: /claude-fable-5-system-prompt-leak-harness-architecture-exposed/
image: /assets/images/fable5-system-prompt-leak-cover.jpeg
description: "**作者：** Wisely Chen **系列：** Harness Engineering **關鍵字：** Fable 5, System Prompt Leak, Agent Harness, Anthropic, Pliny the Liberator, 基準測試公平性, 模型路由"
---

![Pliny the Liberator 在 X 上公開 Fable 5 的 120,000 字符系統提示詞](/assets/images/fable5-system-prompt-leak-cover.jpeg)

**作者：** Wisely Chen
**系列：** Harness Engineering
**關鍵字：** Fable 5, System Prompt Leak, Agent Harness, Anthropic, Pliny the Liberator, 基準測試公平性, 模型路由

---

## 事情經過

6 月 10 日，黑客 Pliny the Liberator 在 X 上丟出了 Claude Fable 5 的完整系統提示詞。12 萬字符，1,585 行，72 個命名段落。

大家推估的結論很明顯：**Fable 5 後面不是模型，是一個 Harness 系統。** 白話講，我們以為在 call 一個 Opus 等級的 LLM API，但後面其實是一整套 Claude Code（裡面調度不同的 LLM）在接你的任務。

gerardsans 說「這根本不是一場公平的比賽——你是在拿一個原生大模型加上 Agent Harness 的開掛系統，去和別人的裸模型做對比」。社群吵的是公不公平。

回頭想想，難怪我在用 Fable 5 的時候總覺得它很慢——說一個 hello 都要等很久。原來每一次回應背後跑的不是單一的 LLM call，是一整套類似 Claude Code 的 Agent 完成流程。

但如果你從 [Harness Engineering](/harness-engineering-architecture-overview/) 的角度看，這份洩漏文件揭露的東西比「公不公平」有價值得多。

**這是目前為止最詳細的一份生產級 AI Harness 架構文件。** 不是研究論文，不是技術 blog，是跑在數百萬使用者面前的真實系統配置。

---

## 12 萬字符裡裝了什麼：Harness 的預算分配

AY Automate 做了一份量化分析。120,040 個字符，大約 30,000 tokens，分成 72 個 snake_case 命名的段落。每個段落的 token 預算長這樣：

| 組件 | 字符數 | 佔比 | 功能 |
|------|--------|------|------|
| 工具定義與 JSON Schema | 36,174 | **30%** | 18 個完整的工具規格 |
| 搜尋與引用規則 | 29,596 | **25%** | 搜尋策略、引用格式、來源驗證 |
| 行為、安全與心理防線 | 20,244 | 17% | 安全分類器、拒絕策略、反依賴設計 |
| 身分與「Claudeception」 | 15,164 | 13% | 產品族譜、模型切換邏輯 |
| 電腦控制與檔案處理 | 11,592 | 10% | Linux 沙箱、bash 執行、檔案編輯 |
| 記憶、儲存與 MCP 應用 | 7,270 | 6% | 跨會話記憶、持久化儲存、Artifact |

第一個讓我停下來的數字：**工具定義佔了 30%，搜尋引用佔了 25%。加起來超過一半的 token 預算花在「能力」而不是「個性」。**

「The assistant is Claude, created by Anthropic」這句話出現在第 1,351 行——整份文件 85% 的位置。前面 1,350 行全部在定義這個系統能做什麼、怎麼做、什麼不能做。

換句話說，**Fable 5 的系統提示詞不是在告訴模型「你是誰」，而是在告訴模型「你是什麼系統的一部分」。**

這跟我們在 [Harness 三次遷移](/agent-harness-three-migrations-mechanism/) 那篇講的完全吻合：Harness 從外部框架（LangChain）遷移到 CLAUDE.md 約束層，再遷移到模型內化。Fable 5 的系統提示詞是第二階段到第三階段之間的過渡產物——指令還在提示詞裡，但密度和結構已經達到了一個獨立系統的複雜度。

---

## 不是 LLM，是偽裝成 LLM 的 Agent 系統

洩漏文件揭示的核心架構：

**內建 Linux 沙箱。** 不是外掛的 sandbox API，是模型回應循環裡原生的 bash 執行環境。可以跑命令、編輯檔案、執行程式碼、讀取輸出。

**Agentic Loop。** 給它一個複雜任務，它自己規劃步驟、執行、檢查結果、調整。不需要人類在螢幕前守著。Anthropic 官方說法是「可以無人值守連續運行數天」。

**子智能體分發。** 遇到太大的工程，它可以 spawn sub-agents 來分工。在 Claude Code 裡，一個 workflow 可以[同時並行 16 個 sub-agent，累計最多 1,000 個](/fable-5-harness-internalization-orchestrator-model-routing/)。

**跨會話持久記憶。** 不只是對話內的 context，是跨次對話的記憶系統。Artifact 可以用鍵值存儲 API 持久化資料，變成日誌、追蹤器、排行榜。

**多模態搜尋。** 內建的搜尋工具可以跑網頁搜尋、讀取 URL 內容、處理圖片。

把這些加在一起，你得到的不是一個「很厲害的聊天機器人」，是一個自主運行的 Agent 系統，只是碰巧用聊天介面當入口。

---

## 隱藏的 Agent 生態族譜

系統提示詞裡曝光了幾個正在內測或已經秘密上線的產品：

- **Claude Code**：終端機裡的 Agent 編程工具，這個已經公開了
- **Claude Cowork**：給非開發人員的「智能同事」，處理日常知識工作
- **Claude in Chrome**：瀏覽器內的 Agent
- **Claude in Excel**：試算表裡的 Agent
- **Claude in PowerPoint**：簡報裡的 Agent

而 Claude Cowork 可以調用上面這些子工具當自己的手腳。

這是什麼？這是 [Anthropic 的 Super App 戰略](/anthropic-pauses-agent-sdk-credit-infrastructure-vs-superapp/)。不是一個模型，是一整套 Agent 基礎設施。系統提示詞不只是在配置 Fable 5 這個模型，是在配置 Fable 5 在這個基礎設施裡的角色。

---

## 三域分類器與靜默降級：「掛羊頭賣狗肉」的技術真相

這件事在中文社群炸得最猛的不是 Agent 架構，是計費問題。

系統提示詞顯示：Fable 5 有一套三域分類器（資安、生化、蒸餾），觸發時會把回應交給舊版 Opus 4.8 處理。**但計費仍然按照 Fable 5 的價格收——$10/$50 per MTok，是 Opus 4.8 的兩倍。**

36Kr 用「掛羊頭賣狗肉」來形容。gerardsans 說這是「合法的欺詐」。

但這裡要坦白講幾件事。

第一，[我們之前已經分析過這個機制](/fable-5-harness-internalization-orchestrator-model-routing/)。三域分類器存在的原因是 Fable 5 的底層模型在 Anthropic 的 244 頁 System Card 裡被確認「likely crossed CB-1 門檻」——生化武器能力閾值。Mythos Preview 在 Firefox 147 零日漏洞利用測試中達到 84% 成功率。這不是過度謹慎，是模型真的到了需要 ASL-3 防護的等級。

第二，Anthropic 的數據是只有不到 5% 的 session 會觸發分類器。但那 5% 的使用者體感是災難性的——正經做醫學影像分析、實驗室自動化的人也被誤殺。

第三，**靜默降級本身才是問題的核心，不是降級這件事。** 如果 Anthropic 在觸發時明確告知使用者「這個回應由 Opus 4.8 生成，按 Opus 價格計費」，爭議會少一半。Nathan Lambert 在 Interconnects 的批評最到位：隱藏的能力限制是「categorically misaligned AI」——一個在你不知道的情況下自動變笨的 AI。

---

## 「作弊」論的反面：這就是產業方向

回到最初的問題：拿一個有 Agent Harness 的系統跟裸模型比 benchmark，公不公平？

先看事實。Fable 5 在 SWE-bench Verified 跑到 95%，FrontierSWE 全球第三。但這些 benchmark 本身就是測「完成任務的能力」，不是測「模型裸跑的推理能力」。SWE-bench 要你修真實的 GitHub issue，誰管你用不用沙箱？

更重要的是，**每家都在往這個方向走。**

OpenAI 的 Codex 有自己的 sandbox。Google 的 Gemini 接了搜尋、程式碼執行、電腦控制。DeepSeek 自己就是 MoE 架構加各種推理優化。差別只是 Anthropic 走得最激進——把 harness 直接寫進系統提示詞，讓模型在回應階段就能調用完整的工具鏈。

我在 [Shell Wrapper 2.0](/shell-wrapper-2-anthropic-real-threat/) 那篇就寫過：Anthropic 的真正威脅不是模型更強，是 **harness 工程更好**。Fable 5 的系統提示詞洩漏，只是把這個論點從推測變成了可驗證的事實。

---

## 對企業 IT 架構的三個實際啟示

### 1. 你買的不是模型，是系統

當你選 Claude Fable 5 vs GPT-5.5 vs GLM-5.2，你比較的不是三個模型，是三個系統。每個系統包含：底層模型 + 工具鏈 + 安全分類器 + 記憶系統 + 部署約束。

benchmark 分數只告訴你系統的輸出品質，不告訴你系統的組成。你需要知道的是：觸發安全分類器時會發生什麼？資料保留政策是什麼（Fable 5 是 30 天強制）？模型降級時計費怎麼算？

### 2. 你的 Harness 設計要考慮「系統提示詞已經是 Harness」

如果你在 Fable 5 上面再套一層 LangChain，你等於在 12 萬字符的 harness 上面又加一層 harness。兩層 harness 之間的交互作用很難預測——你的工具定義可能跟系統提示詞裡的 18 個工具 schema 衝突。

更實際的做法是我們在 [Harness 架構概覽](/harness-engineering-architecture-overview/) 裡講的：**做減法**。用模型原生的工具鏈（MCP、Claude Code skills），把你的 harness 限縮在模型管不到的地方——業務邏輯驗證、合規檢查、外部系統整合。

### 3. 系統提示詞洩漏是一個安全事件，也是一個架構風險

12 萬字符的系統提示詞裡包含了：完整的工具 schema、安全分類器的觸發邏輯、模型路由規則、內部產品路線圖。這些都是你的 AI 系統的攻擊面。

我們在 [Harness 安全最佳實踐](/harness-engineering-security-best-practices/) 裡講過：[prompt injection 的攻擊面是整個 harness，不只是模型](/prompt-injection-harness-engineering-tool-using-agents/)。Fable 5 的洩漏證明了另一個面向——**你的系統提示詞本身就是可被提取的情報。** 如果你的 harness 裡有業務敏感的邏輯（定價規則、合規判斷、客戶分類標準），被提取出來就是一個資安事件。

---

## 坦白講：網路上的評論哪裡對、哪裡有偏差

**對的部分：**
- Fable 5 確實是一個 Agent 系統，不只是 LLM。系統提示詞的結構已經證實了這一點
- 把 Agent+Harness 的系統跟裸模型放在同一個 benchmark 比較，確實存在比較基準不一致的問題
- 靜默降級同時按高價計費，是一個合理的消費者保護議題

**有偏差的部分：**
- 「開了外掛」這個說法暗示作弊。但 SWE-bench 等 benchmark 從來沒規定不能用工具。測的就是「完成任務的能力」，不是「模型裸跑的推理能力」
- 「合法的欺詐」太重了。分類器觸發率不到 5%，而且觸發原因是模型能力真的到了生化武器輔助的等級。問題在透明度，不在欺詐
- 「Anthropic 秘而不宣」——事實上 Anthropic 發布了 244 頁的 System Card，公開了三域分類器的存在和 CB-1 門檻的跨越。只是大多數人沒讀

**大家沒提到的：**
- 其他廠商也在做完全一樣的事情。OpenAI Codex 有 sandbox，Google Gemini 有搜尋和程式碼執行。「Agent+Harness」不是 Anthropic 獨家操作，是產業共識
- 30 天資料強制保留這個對企業客戶的實際影響。Microsoft 已經因此限制了員工使用

---

## 結論：基準測試已經失效了

Fable 5 系統提示詞洩漏揭示的不是「Anthropic 作弊」，是「整個 benchmark 評測框架已經追不上產品形態的演進」。

當「模型」不再是一個單一的神經網路權重檔，而是一個包含模型 + 工具鏈 + 安全層 + 記憶系統 + 子 Agent 調度的完整系統時，你用什麼尺來量它？

36Kr 文章結尾說得好：「也許我們一直用錯了尺子。」

但我想補一句：**問題不只是尺子錯了。問題是大家還在假裝被量的東西是同一個品類。** 一個帶 Linux 沙箱、18 個工具 schema、三域安全分類器的 Agent 系統，跟一個 API 回傳文字的語言模型，根本不是同一個品類的產品。

比較它們的 benchmark 分數，就像比較一個全家便利店跟一台自動販賣機的「商品交付速度」——你量到的指標可能是真的，但你因此得出的結論一定是錯的。

對企業來說，真正該問的不是「哪個模型分數最高」，而是「哪個系統最適合我的任務、我的安全需求、我的資料政策、我的預算」。12 萬字符的系統提示詞告訴我們：答案一直都不在模型裡，在 Harness 裡。

---

## 來源

- [36Kr / 新智元：Fable 5 榜單第一靠作弊？代碼洩露，模型真實身份曝光](https://www.toutiao.com/article/7652334616778441225/)（2026-06-17）
- [AY Automate：Inside the Claude Fable 5 System Prompt](https://www.ayautomate.com/blog/claude-fable-5-system-prompt-leak)
- [AlphaSignal AI：Claude Fable 5 Prompt Leak Is a User Manual for Long-Running Agents](https://alphasignalai.substack.com/p/claude-fable-5-prompt-leak-is-a-user)
- [gerardsans 的 X 分析](https://x.com/gerardsans/status/2066148459795615825)
- [Anthropic Fable 5 System Card（244 頁）](https://www-cdn.anthropic.com/d00db56fa754a1b115b6dd7cb2e3c342ee809620.pdf)
- [Gist：完整洩漏系統提示詞](https://gist.github.com/gsans/b3007997f8900003c8ff58125a45e15e)
