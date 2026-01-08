---
layout: post
title: "CaMeL Agent 架構落地 PostgreSQL：用 RLS 設計不可繞過的 AI Memory 與權限隔離"
date: 2026-01-07 14:00:00 +0800
permalink: /camel-postgresql-implementation-memory-permission-db-layer/
image: /assets/images/camel-postgresql-three-layer-memory.png
description: "本文示範如何將 Google DeepMind 提出的 CaMeL 雙層 Agent 架構，實際落地到 PostgreSQL，利用資料庫原生的 Role 與 Row-Level Security（RLS），設計一套不可繞過的 AI Memory 隔離機制，用來防禦 prompt injection 與高權限 Agent 失控風險。"
---

## 本文解決什麼問題？

- CaMeL 架構在實務上要把「隔離」做在哪一層？
- AI Agent 的記憶與權限，如何避免只靠應用層 if-else？
- 如何用 PostgreSQL 設計一個 LLM 無法繞過的安全邊界？

---

## 一、CaMeL 的精髓，不是「兩個模型」

上一篇講 [CaMeL 的雙層 Agent 架構](/camel-privileged-quarantined-agent/)，這是基於 Google DeepMind 發表的 [CaMeL 論文](https://arxiv.org/abs/2503.18813)。核心概念是把「讀資料」和「做動作」分開——Quarantined LLM 只能讀不可信資料，Privileged LLM 只能接收已結構化的乾淨資訊。

![CaMeL 的真正核心：建立兩個不可跨越的權限域](/assets/images/camel-core-two-domains.png)

但讀完論文後，我發現很多人只理解到一半。

**CaMeL 的重點不是「用兩個模型」，而是「建立兩個不可跨越的權限域」。**

一邊是隔離域（Quarantined Domain），存放所有未經處理的外部輸入；另一邊是權限域（Privileged Domain），只能存取經過淨化的可信資料。中間有一道牆，資料必須經過審核才能跨越。

問題來了：這道牆該建在哪裡？

---

## 二、應用層的 `if-else`，一碰就碎

大部分團隊的第一直覺是在應用層做權限判斷：

```python
def access_data(agent):
    if agent.role == 'privileged':
        # Access sensitive data
        return agent.get_sensitive_info()
    else:
        # Access public data
        return agent.get_public_info()
```

這種做法的問題是：

> 如果你的安全邊界只存在於應用層的 `if-else` 邏輯，那只要工程師寫錯一行 code，整套隔離就崩潰。

新人接手不知道這個規則、code review 沒看到、unit test 沒覆蓋到——任何一個環節出錯，高權限 Agent 就可能直接讀到未淨化的外部資料。

這讓我想起之前寫 [PostgreSQL AI Memory Store](/postgresql-ai-memory-store/) 時的一個結論：

> 真正的安全邊界，不能只存在於應用層，必須下沉到資料庫層。

---

## 三、真正的安全邊界，必須下沉到資料庫

於是我開始把 CaMeL 的概念落地到 PostgreSQL。

核心思路是：

> **把「記憶」(Memory) 與「權限」(Permissions) 都下沉到資料庫層，創造一個應用層程式碼*無法*繞過的邊界。**

不是請求模型自己守規矩，而是讓系統在設計上就不允許違規。

即使 Python code 寫錯、即使 Privileged Agent 被 prompt injection 騙了，資料庫引擎本身會擋住——因為那個角色根本沒有權限存取那個 schema。

如果你已經有[企業級地端 LLM 架構](/local-llm-enterprise-architecture/)，有 Auth Gateway 做身分驗證、有 LLM Router 做模型調度，那這套 DB 層的權限隔離就是下一步該補的「最後一道防線」。

---

## 四、CaMeL 的三層記憶架構

CaMeL 原始論文講的是 Quarantined vs Privileged 兩層，但實際落地時我發現，中間必須有一個**顯式的 Sanitize 層**。

![CaMeL 的三層記憶架構](/assets/images/camel-three-layer-memory-architecture.png)

原因很簡單：

> 你不可能讓 Quarantined Agent 直接產生「乾淨」的輸出，因此中間必須有一個顯式的 Sanitize 層。

於是設計成三層：

### 第一層：隔離區 (Quarantine)

**Table:** `quarantine.raw_memory`

存放所有未經處理的外部輸入——Email、OCR 結果、API 回應、網頁內容。

- 只有 Quarantined Agent 能寫入
- 標記 `taint_level = 'external'`
- TTL 短（7-14 天）

### 第二層：淨化區 (Sanitized)

**Table:** `memory.sanitized_memory`

存放經過淨化流程、可信任的結構化資料。

- 經過 Sanitize 流程後才能進入
- `taint_level` 必須降級為 `'internal'`
- Privileged Agent 只能讀這層
- 保留追溯連結到原始 raw

### 第三層：權威區 (Policy)

**Table:** `memory.policy_memory`

存放經過驗證的規則、結論與行動手冊。

- 長期有效的決策依據
- 存放 guardrails、playbooks、heuristics
- 用於 Agent 決策的最高權威來源

---

## 五、DB Roles：將 Agent 權限變成資料庫原生角色

這是整套架構最關鍵的設計——**不要在應用層做權限判斷，讓資料庫引擎強制執行**。

### 為什麼 DB Role 比 Application Role 更安全？

Application Role 的權限檢查發生在應用程式碼中，只要工程師寫錯一行、code review 沒抓到、或 unit test 沒覆蓋，整個隔離就崩潰。

DB Role 則是在資料庫引擎層強制執行——不管你的 Python 或 SQL 怎麼寫，引擎本身就會擋住越權存取。這是「系統強制」vs「請求自律」的根本差異。

### 角色定義

```sql
-- Create the role
CREATE ROLE agent_quarantined;

-- Set the role after connection
SET ROLE agent_quarantined;
```

三個核心角色：

- **`agent_quarantined`：** 低權限 Agent，只能讀寫自己的隔離區
- **`agent_privileged`：** 高權限 Agent，只能讀淨化區與權威區
- **`memory_reviewer`：** 審核者，負責將資料從隔離區升級到淨化區

### 連線時切換角色

應用程式連線後，根據 Agent 身分切換：

```sql
-- Quarantined Agent 連線後
SET ROLE agent_quarantined;
SET app.agent_id = 'agent_123';

-- Privileged Agent 連線後
SET ROLE agent_privileged;
SET app.agent_id = 'agent_456';
```

這樣做的好處是：**權限檢查發生在 DB 引擎層，不是應用層**。

---

## 六、RLS：不可繞過的系統級安全閘門

Row-Level Security (RLS) 是整個架構的「安全閘門」。

![RLS：不可繞過的系統級安全閘門](/assets/images/camel-rls-security-gate.png)

RLS 在資料庫引擎層面強制執行存取規則，使應用層程式碼完全無法規避。

不管你的 SQL 怎麼寫，資料庫引擎會在每一次查詢時自動加上權限過濾條件。

---

## 七、`agent_quarantined` 的視角：只能讀寫自己的隔離區

這個 Agent 只能向 `quarantine.raw_memory` 寫入屬於自己的資料，且只能讀取自己寫入的內容。

![agent_quarantined 的權限視角](/assets/images/camel-agent-quarantined-view.png)

關鍵限制：
- ✅ 可讀寫：`quarantine.raw_memory`（僅自己的）
- ❌ 不可讀：`memory.sanitized_memory`
- ❌ 不可讀：`memory.policy_memory`

---

## 八、`agent_privileged` 的視角：完全禁止接觸污染源

高權限 Agent 被*完全禁止*存取 `quarantine` schema，連看的權限都沒有。它只能讀取 `sanitized_memory` 和 `policy_memory` 中的乾淨資料。

```sql
-- Forbid access to the entire schema
REVOKE ALL ON SCHEMA quarantine
FROM agent_privileged;
```

![agent_privileged 的權限視角：完全禁止接觸污染源](/assets/images/camel-agent-privileged-view.png)

關鍵限制：
- ❌ 完全禁止：`quarantine.raw_memory`（連 schema 都不能碰）
- ✅ 可讀：`memory.sanitized_memory`
- ✅ 可讀：`memory.policy_memory`

這意味著：

> **即使 Privileged Agent 被 prompt injection 騙了，它也讀不到 raw。**

```sql
-- Privileged Agent 嘗試執行
SET ROLE agent_privileged;
SELECT * FROM quarantine.raw_memory;

-- 結果：ERROR: permission denied for schema quarantine
```

---

## 九、Sanitize 流程：從「高污染」到「可信任」

Sanitize 不是「把文字修漂亮」，而是：

> 把外部輸入轉成可治理的內部事實層，只有這層才有資格被高權限 Agent 拿去做決策。

### 三大目標

1. **去風險**：移除 prompt injection / 指令 / 外部可執行內容
2. **去敏感**：PII / secret / token / internal link / 客戶資料
3. **保可用**：保留「能支撐決策」的 facts + evidence refs

### 四階段 Pipeline

**接收 (Ingest)** → **偵測 (Detect)** → **轉換 (Transform)** → **批准 (Approve)**

![Sanitize 四階段 Pipeline](/assets/images/camel-sanitize-pipeline.png)

1. **接收：** 原始資料寫入隔離區
2. **偵測：** 評估風險，計算 risk_score
3. **轉換：** 產出結構化的內部事實
4. **批准：** 由 `memory_reviewer` 角色寫入淨化區

---

## 十、淨化產出：可治理的內部事實

淨化後的輸出是結構化 JSON，包含：

```json
{
  "facts": [
    {"f": "發票金額 120,000", "confidence": 0.8}
  ],
  "risks": [
    {"type": "prompt_injection", "severity": "high"}
  ],
  "allowlist_actions": [
    "read_only_answer", "summarize_only"
  ],
  "evidence": "raw_memory_id: '...'"
}
```

**關鍵設計：`evidence` 欄位只儲存對原始資料的引用 (reference id)，而非複製原始內容，以確保隔離。**

Privileged Agent 可以知道「這個結論來自哪裡」，但無法直接讀取原始的高風險內容。

---

## 十一、系統強制，勝於請求自律

這是整套架構的核心哲學。

| 面向 | 應用層 Filter | PostgreSQL RLS |
|------|:------------:|:--------------:|
| 執行層級 | ❌ Application | ✅ Database Engine |
| 可繞過性 | ❌ 工程師寫錯就漏 | ✅ 無法繞過 |
| 集中管理 | ❌ 散落各處 | ✅ 在 DB 定義一次 |
| 可審計性 | ❌ 需自己實作 | ✅ pg_audit 原生支援 |

當 Privileged Agent 嘗試越權時：

```
ERROR: permission denied for schema quarantine
```

這就是差別：**應用層 Filter 是「請求模型自己守規矩」，PostgreSQL RLS 是「系統強制執行」。**

---

## 十二、完整架構：一個縱深防禦體系

![CaMeL PostgreSQL 完整架構：一個縱深防禦體系](/assets/images/camel-postgresql-complete-architecture.png)

---

## 十三、這不是免費的午餐：複雜度與延遲的權衡

這套架構當然不是免費的。

### 代價

- **複雜度增加：** 需要維護三層記憶和多個 DB Role
- **延遲增加：** 從 raw 到 sanitized 需要時間，不適合即時場景
- **Sanitize 可能漏洞：** 淨化規則需要持續維護

### 換來的是

對於操作資料庫、API、金流的企業級 Agent，這些代價換來的是：

> **即使 LLM 被騙，系統邊界不會被突破。**

這是傳統的 prompt engineering 和 guardrails 做不到的事。

---

## 十四、核心價值：建立一個不需要信任模型的系統

CaMeL 的精髓從來不是「用兩個模型」，而是「建立兩個不可跨越的權限域」。

PostgreSQL 能把這個權限域做成**系統級的安全邊界**：

- RLS 讓隔離不可繞過
- DB Role 讓權限在引擎層強制執行
- Sanitize pipeline 讓「高污染」變「可治理」
- 三層記憶架構讓每一層的責任清晰可見

這種架構將 AI 安全的基礎，從「希望模型會變乖」，轉變為「設計一個讓模型的行為失控也能被有效控制的系統」。

> 不要把希望寄託在「模型會變乖」，
> 而是讓系統本身，在設計上就不需要信任模型。

---

## 這套架構適合哪些場景？

### 適合

- **[企業內部 AI Agent](/local-llm-enterprise-architecture/)**：需要存取內部資料庫、ERP、CRM 的自動化流程，特別是已經有 Auth Gateway 和 LLM Router 的地端架構
- **涉及資料庫操作**：Agent 會執行 SELECT/INSERT/UPDATE 的場景
- **高風險 prompt injection 場景**：處理 Email、OCR、外部 API 回應等不可信輸入
- **金流與敏感操作**：需要嚴格審計與權限隔離的企業應用

### 不適合

- **即時聊天型 Bot**：純對話、不涉及資料庫操作的 chatbot
- **單一 LLM 應用**：沒有行為權限分層需求的簡單問答系統
- **Latency 敏感場景**：Sanitize pipeline 會增加延遲，不適合毫秒級回應需求

---

## 附錄：完整 SQL 參考

以下是本文架構的完整 SQL 實作，可直接在 PostgreSQL 執行：

```sql
-- ============================================================
-- CaMeL Agent 架構 PostgreSQL 實作
-- 三層記憶隔離 + DB Role + RLS
-- ============================================================

-- 1. 建立 Schema
CREATE SCHEMA IF NOT EXISTS quarantine;  -- 隔離區
CREATE SCHEMA IF NOT EXISTS memory;      -- 淨化區 + 權威區

-- 2. 建立三個核心角色
CREATE ROLE agent_quarantined;   -- 低權限 Agent
CREATE ROLE agent_privileged;    -- 高權限 Agent
CREATE ROLE memory_reviewer;     -- 審核者

-- 3. 建立隔離區表格 (Quarantine Layer)
CREATE TABLE quarantine.raw_memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id TEXT NOT NULL,
    content JSONB NOT NULL,
    taint_level TEXT DEFAULT 'external',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ DEFAULT NOW() + INTERVAL '14 days'
);

-- 4. 建立淨化區表格 (Sanitized Layer)
CREATE TABLE memory.sanitized_memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id TEXT NOT NULL,
    facts JSONB NOT NULL,
    risks JSONB,
    allowlist_actions TEXT[],
    evidence_ref UUID REFERENCES quarantine.raw_memory(id),
    taint_level TEXT DEFAULT 'internal',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. 建立權威區表格 (Policy Layer)
CREATE TABLE memory.policy_memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    policy_type TEXT NOT NULL,  -- 'guardrail', 'playbook', 'heuristic'
    content JSONB NOT NULL,
    version INT DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. 設定 Schema 權限
-- agent_quarantined: 只能存取 quarantine schema
GRANT USAGE ON SCHEMA quarantine TO agent_quarantined;
GRANT SELECT, INSERT ON quarantine.raw_memory TO agent_quarantined;

-- agent_privileged: 完全禁止存取 quarantine，只能讀 memory
REVOKE ALL ON SCHEMA quarantine FROM agent_privileged;
GRANT USAGE ON SCHEMA memory TO agent_privileged;
GRANT SELECT ON memory.sanitized_memory TO agent_privileged;
GRANT SELECT ON memory.policy_memory TO agent_privileged;

-- memory_reviewer: 可以讀 quarantine，寫入 memory
GRANT USAGE ON SCHEMA quarantine TO memory_reviewer;
GRANT SELECT ON quarantine.raw_memory TO memory_reviewer;
GRANT USAGE ON SCHEMA memory TO memory_reviewer;
GRANT INSERT ON memory.sanitized_memory TO memory_reviewer;

-- 7. 啟用 RLS (Row-Level Security)
ALTER TABLE quarantine.raw_memory ENABLE ROW LEVEL SECURITY;
ALTER TABLE memory.sanitized_memory ENABLE ROW LEVEL SECURITY;

-- 8. RLS Policy: agent_quarantined 只能存取自己的資料
CREATE POLICY quarantined_own_data ON quarantine.raw_memory
    FOR ALL TO agent_quarantined
    USING (agent_id = current_setting('app.agent_id', true))
    WITH CHECK (agent_id = current_setting('app.agent_id', true));

-- 9. RLS Policy: agent_privileged 只能讀取淨化後的資料
CREATE POLICY privileged_read_sanitized ON memory.sanitized_memory
    FOR SELECT TO agent_privileged
    USING (taint_level = 'internal');

-- 10. 使用範例：連線後切換角色
-- Quarantined Agent 連線
-- SET ROLE agent_quarantined;
-- SET app.agent_id = 'agent_123';

-- Privileged Agent 連線
-- SET ROLE agent_privileged;
-- SET app.agent_id = 'agent_456';
```

---

## 延伸閱讀

- [CaMeL：Google DeepMind 提出的 Prompt Injection 防禦架構](/camel-privileged-quarantined-agent/)
- [為什麼我開始把 PostgreSQL 當成 AI 的「自家記憶庫」](/postgresql-ai-memory-store/)
- [企業級地端 LLM 系統架構藍圖](/local-llm-enterprise-architecture/)
- [AI Agent 安全性：遊戲規則已經改變](/ai-agent-security-game-changed/)
- [AI Guardrails 為什麼註定失敗？](/openai-dou-dang-bu-zhu-de-gong-ji-ai-an-quan-fang-tan/)
- [CaMeL 論文原文 (arXiv)](https://arxiv.org/abs/2503.18813)
