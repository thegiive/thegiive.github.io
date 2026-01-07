---
layout: post
title: "CaMeL 落地 PostgreSQL：讓 AI 記憶與權限都下沉到資料庫層"
date: 2026-01-07 14:00:00 +0800
permalink: /camel-postgresql-implementation-memory-permission-db-layer/
image: /assets/images/camel-postgresql-three-layer-memory.png
description: "CaMeL 的重點不是「用兩個模型」，而是「建立兩個不可跨越的權限域」。這篇文章分享如何把 CaMeL 概念落地到 PostgreSQL——讓「權限」跟「記憶」都下沉到 DB 層，讓高權限 Agent 只能看「被淨化過」的資料；低權限 Agent 可以接觸外部，但永遠寫不進核心權威層。"
---

## 開場：CaMeL 的精髓不是「兩個模型」

上一篇講 [CaMeL 的雙層 Agent 架構](/camel-privileged-vs-quarantined-agent-which-needs-stronger-llm/)，核心概念是把「讀資料」和「做動作」分開——Quarantined LLM 只能讀不可信資料，Privileged LLM 只能接收已結構化的乾淨資訊。

但讀完論文後，我發現很多人只理解到一半。

**CaMeL 的重點不是「用兩個模型」，而是「建立兩個不可跨越的權限域」。**

問題來了：

> 如果這兩個權限域只存在於應用層的 if-else 邏輯，那只要工程師寫錯一行 code，整套隔離就崩潰。

這讓我想起之前寫 [PostgreSQL AI Memory Store](/postgresql-ai-memory-store/) 時的一個結論：

> 真正的安全邊界，不能只存在於應用層，必須下沉到資料庫層。

於是我開始把 CaMeL 的概念落地到 PostgreSQL，核心就是一句話：

> **把「權限」跟「記憶」都下沉到 DB 層，讓高權限 Agent 只能看「被淨化過」的資料；低權限 Agent 可以接觸外部，但永遠寫不進核心權威層。**

---

## 一、CaMeL 對應的三層記憶架構

### 從 CaMeL 分層到 PostgreSQL 分層

| CaMeL 概念 | PostgreSQL 實作 |
|-----------|-----------------|
| Quarantined Agent（低權限）：讀外部、高風險輸入 | `quarantine.raw_memory` |
| Sanitize 過程：淨化、審核 | `memory.sanitized_memory` |
| Privileged Agent（高權限）：做決策、執行動作 | `memory.policy_memory` |

### 三層記憶設計

![三層記憶隔離架構](/assets/images/camel-postgresql-memory-layers.png)

**第一層：raw_memory（隔離區）**
- 只有 Quarantined Agent 能寫入
- 存放所有外部輸入：Email、OCR、API 回應、網頁內容
- 標記 `taint_level = 'external'`
- TTL 短（7-14 天）

**第二層：sanitized_memory（淨化區）**
- 經過 Sanitize 流程後才能進入
- `taint_level` 必須降級為 `'internal'`
- Privileged Agent 只能讀這層
- 保留追溯連結到原始 raw

**第三層：policy_memory（權威區）**
- 存放經過驗證的結論、規則、playbook
- 長期有效
- 用於 Agent 決策的依據

### 為什麼是三層不是兩層？

CaMeL 原始論文講的是 Quarantined vs Privileged 兩層，但實際落地時我發現，中間必須有一個**顯式的 Sanitize 層**。

原因很簡單：

> 你不可能讓 Quarantined Agent 直接產生「乾淨」的輸出，因為它本身就在處理高風險資料。

所以：
- Quarantined Agent 的輸出先進 raw_memory
- 經過 Sanitizer（可以是 rule-based、LLM、或人工審核）處理後
- 才能「升級」到 sanitized_memory
- Privileged Agent 永遠只看 sanitized_memory

---

## 二、DB Roles：把 Agent 權限變成資料庫角色

這是整套架構最關鍵的設計——**不要在應用層做權限判斷，讓資料庫引擎強制執行**。

### 角色定義

```sql
-- 角色：對應 CaMeL 的權限分層
CREATE ROLE agent_quarantined NOINHERIT;  -- 低權限 Agent
CREATE ROLE agent_privileged  NOINHERIT;  -- 高權限 Agent
CREATE ROLE memory_reviewer   NOINHERIT;  -- 審核者（人或服務）
CREATE ROLE memory_maintainer NOINHERIT;  -- 定期清理 job

-- App 連線用的 login role
CREATE ROLE app_login LOGIN PASSWORD '...';
GRANT agent_quarantined TO app_login;  -- 預設低權限
```

### 連線時切換角色

應用程式連線後，根據 Agent 身分切換：

```sql
-- Quarantined Agent 連線後
SET ROLE agent_quarantined;
SET app.agent_id = 'agent_123';
SET app.tenant_id = 'tenant_a';

-- Privileged Agent 連線後
SET ROLE agent_privileged;
SET app.agent_id = 'agent_456';
```

這樣做的好處是：**權限檢查發生在 DB 引擎層，不是應用層**。

即使你的 Python code 寫錯（例如忘了加 user_id filter），資料庫也會擋住。

---

## 三、Schema 設計：讓 Taint 與 Permission 變成可查詢的欄位

### 3.1 raw_memory（隔離區）

```sql
CREATE SCHEMA IF NOT EXISTS quarantine;

CREATE TABLE quarantine.raw_memory (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  content text NOT NULL,
  embedding vector(1536),

  -- CaMeL taint 標籤：標記資料來源風險
  taint_level text NOT NULL CHECK (taint_level IN ('external', 'user', 'tool', 'internal')),

  -- 外部來源追蹤
  source_type text,   -- 'email', 'ocr', 'api', 'web'
  source_ref  text,   -- URL, email ID, document ID

  -- Agent 追蹤
  agent_id text,
  task_id text,
  session_id text,

  -- 時間管理
  created_at timestamptz DEFAULT now(),
  expires_at timestamptz DEFAULT (now() + interval '14 days'),
  is_deleted boolean DEFAULT false,

  -- 彈性欄位
  metadata jsonb DEFAULT '{}'::jsonb
);

-- 索引設計
CREATE INDEX ON quarantine.raw_memory (agent_id, created_at DESC);
CREATE INDEX ON quarantine.raw_memory USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON quarantine.raw_memory USING gin (metadata);
```

### 3.2 sanitized_memory（淨化區）

```sql
CREATE SCHEMA IF NOT EXISTS memory;

CREATE TABLE memory.sanitized_memory (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  raw_id uuid REFERENCES quarantine.raw_memory(id),  -- 追溯連結

  content text NOT NULL,
  embedding vector(1536),

  -- 淨化後的 taint 必須是 internal
  taint_level text NOT NULL CHECK (taint_level IN ('internal')) DEFAULT 'internal',

  -- Sanitize 追蹤（可審計）
  sanitized_by text NOT NULL,          -- 誰淨化的
  sanitizer_version text,               -- 淨化器版本
  sanitizer_reason text,                -- 為什麼這樣淨化

  -- 風險評估
  risk_score int NOT NULL DEFAULT 0,   -- 0-100

  -- 結構化淨化結果
  sanitized jsonb NOT NULL DEFAULT '{}'::jsonb,

  -- 時間管理
  created_at timestamptz DEFAULT now(),
  expires_at timestamptz DEFAULT (now() + interval '90 days'),
  is_deleted boolean DEFAULT false,

  metadata jsonb DEFAULT '{}'::jsonb
);

CREATE INDEX ON memory.sanitized_memory USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON memory.sanitized_memory (created_at DESC);
CREATE INDEX ON memory.sanitized_memory USING gin (sanitized);
```

### 3.3 policy_memory（權威區）

```sql
CREATE TABLE memory.policy_memory (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  parent_id uuid REFERENCES memory.policy_memory(id),  -- 支援版本演進

  -- 只存「結論/規則」，不存 raw
  policy_type text NOT NULL CHECK (policy_type IN ('reflection','heuristic','guardrail','playbook')),
  content text NOT NULL,

  -- 可執行條件（用 JSON 表達）
  apply_if jsonb DEFAULT '{}'::jsonb,

  -- 版本控制
  version int DEFAULT 1,
  created_at timestamptz DEFAULT now(),
  is_deleted boolean DEFAULT false
);

CREATE INDEX ON memory.policy_memory USING gin (apply_if);
CREATE INDEX ON memory.policy_memory (policy_type, created_at DESC);
```

---

## 四、RLS：用資料庫直接保證 CaMeL 隔離

這是整套架構的「安全閘門」——Row Level Security 讓隔離變成**不可繞過的系統邊界**。

### 4.1 Quarantined：只能寫 raw，只能讀自己的 raw

```sql
ALTER TABLE quarantine.raw_memory ENABLE ROW LEVEL SECURITY;

-- 低權限 Agent 只能讀自己寫入的 raw
CREATE POLICY q_read_own_raw
ON quarantine.raw_memory
FOR SELECT
TO agent_quarantined
USING (agent_id = current_setting('app.agent_id', true));

-- 低權限 Agent 可以寫入 raw（但只能寫自己的）
CREATE POLICY q_write_raw
ON quarantine.raw_memory
FOR INSERT
TO agent_quarantined
WITH CHECK (agent_id = current_setting('app.agent_id', true));
```

### 4.2 Privileged：完全禁止讀 raw，只能讀 sanitized + policy

```sql
-- 關鍵：Privileged Agent 完全不能碰 quarantine schema
REVOKE ALL ON SCHEMA quarantine FROM agent_privileged;
REVOKE ALL ON ALL TABLES IN SCHEMA quarantine FROM agent_privileged;

-- Privileged 可以讀 sanitized
ALTER TABLE memory.sanitized_memory ENABLE ROW LEVEL SECURITY;

CREATE POLICY p_read_sanitized
ON memory.sanitized_memory
FOR SELECT
TO agent_privileged
USING (is_deleted = false);  -- 或加 tenant/user 篩選

-- Privileged 可以讀 policy
ALTER TABLE memory.policy_memory ENABLE ROW LEVEL SECURITY;

CREATE POLICY p_read_policy
ON memory.policy_memory
FOR SELECT
TO agent_privileged
USING (is_deleted = false);
```

### 4.3 Reviewer：唯一能執行「升級」的角色

```sql
-- 只有 reviewer 能把 raw -> sanitized
GRANT USAGE ON SCHEMA quarantine, memory TO memory_reviewer;
GRANT SELECT ON quarantine.raw_memory TO memory_reviewer;
GRANT INSERT, UPDATE ON memory.sanitized_memory TO memory_reviewer;
```

### 這個設計為什麼重要？

> **即使 Privileged Agent 被 prompt injection 騙了，它也讀不到 raw。**

傳統的應用層 filter：
```python
# 這很容易寫錯
if agent.role == 'privileged':
    data = db.query("SELECT * FROM raw_memory")  # 漏了 filter！
```

PostgreSQL RLS：
```sql
-- 即使 code 寫 SELECT * FROM quarantine.raw_memory
-- 資料庫會直接返回 permission denied
```

---

## 五、Sanitize 流程：把「高污染 raw」變成「可用的內部事實」

Sanitize 不是「把文字修漂亮」，而是：

> 把外部輸入轉成可治理的內部事實層，只有這層才有資格被高權限 Agent 拿去做決策。

### Sanitize 的三個硬目標

1. **去風險**：移除 prompt injection / 指令 / 外部可執行內容
2. **去敏感**：PII / secret / token / internal link / 客戶資料
3. **保可用**：保留「能支撐決策」的 facts + evidence refs

### Sanitize Pipeline（四階段）

![Sanitize Pipeline](/assets/images/camel-postgresql-sanitize-pipeline.png)

**Stage A — Ingest（入 quarantine）**
- Quarantined Agent 原封不動寫入
- 一律標 `taint_level = 'external'`
- TTL 短

**Stage B — Detect（風險評估）**
- 計算 risk_score：
  - Injection pattern（ignore previous / system prompt / tool call）
  - Links / forms / payment actions
  - Secrets（api key, token, ssh key）
  - PII（email/phone/id/address）
- risk_score > 80 → 直接進人工審核，不自動 sanitize

**Stage C — Transform（產出 sanitized）**
- 輸出結構化 JSON：

```json
{
  "summary": "一句話摘要",
  "facts": [
    {"f": "發票金額 120,000", "evidence": ["raw#L120-L140"], "confidence": 0.8}
  ],
  "claims": [
    {"c": "聲稱來自 CEO", "speaker": "external", "confidence": 0.3}
  ],
  "risks": [
    {"type": "prompt_injection", "severity": "high"},
    {"type": "authority_claim", "severity": "medium"}
  ],
  "redactions": [
    {"type": "api_key", "count": 2},
    {"type": "email", "count": 1}
  ],
  "allowlist_actions": ["read_only_answer", "summarize_only"],
  "blocklist_actions": ["execute_payment", "send_email", "delete_data"]
}
```

**重點：evidence 不存 raw 內容，只存 reference id / line range**

**Stage D — Approve（寫入 sanitized_memory）**
- 只有 memory_reviewer 能寫入
- 必填：sanitizer_version, reason, raw_id

### Sanitize 函數（安全界線）

```sql
CREATE OR REPLACE FUNCTION memory.promote_to_sanitized(
  p_raw_id uuid,
  p_content text,
  p_sanitized jsonb,
  p_risk_score int,
  p_reason text
)
RETURNS uuid
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  new_id uuid;
BEGIN
  -- 驗證：只有低風險才能自動升級
  IF p_risk_score > 80 THEN
    RAISE EXCEPTION 'Risk score too high (%), requires manual review', p_risk_score;
  END IF;

  INSERT INTO memory.sanitized_memory(
    raw_id, content, sanitized, risk_score,
    sanitized_by, sanitizer_reason
  )
  VALUES (
    p_raw_id, p_content, p_sanitized, p_risk_score,
    current_user, p_reason
  )
  RETURNING id INTO new_id;

  RETURN new_id;
END $$;

-- 權限控制：只有 reviewer 能呼叫
REVOKE ALL ON FUNCTION memory.promote_to_sanitized FROM PUBLIC;
GRANT EXECUTE ON FUNCTION memory.promote_to_sanitized TO memory_reviewer;
```

---

## 六、實際查詢模式

### Quarantined Agent：讀自己的 raw，找候選內容

```sql
-- 低權限 Agent 找最近的 raw 內容
SELECT id, content, taint_level, created_at
FROM quarantine.raw_memory
WHERE agent_id = current_setting('app.agent_id', true)
  AND is_deleted = false
  AND expires_at > now()
ORDER BY created_at DESC
LIMIT 50;
```

### Privileged Agent：只讀 sanitized + policy

```sql
-- 高權限 Agent 查詢相關記憶
SELECT
  s.content,
  s.sanitized->>'summary' as summary,
  s.sanitized->'facts' as facts,
  s.sanitized->'allowlist_actions' as allowed,
  s.risk_score,
  s.created_at
FROM memory.sanitized_memory s
WHERE s.is_deleted = false
  AND s.risk_score < 50  -- 只要低風險的
ORDER BY s.embedding <=> $1  -- 向量相似度
LIMIT 10;

-- 查詢適用的 policy
SELECT content, policy_type, apply_if
FROM memory.policy_memory
WHERE is_deleted = false
  AND policy_type IN ('guardrail', 'playbook')
ORDER BY created_at DESC;
```

### 跨層資料流（只有 Reviewer 能做）

```sql
-- Reviewer 把 raw 升級到 sanitized
SELECT memory.promote_to_sanitized(
  'raw_uuid'::uuid,
  '淨化後的摘要內容',
  '{"summary": "...", "facts": [...], "risks": [...]}'::jsonb,
  35,  -- risk_score
  'Rule-based sanitizer v2.1'
);
```

---

## 七、為什麼這比應用層 Filter 更安全？

### 應用層 Filter 的問題

```python
# 典型的應用層做法
def get_memory_for_privileged_agent(agent_id: str):
    # 問題 1：很容易忘了加 filter
    raw = db.query("SELECT * FROM raw_memory")

    # 問題 2：filter 邏輯散落在各處
    if is_sanitized(raw):
        return raw

    # 問題 3：新人接手可能不知道這個規則
    # 問題 4：unit test 很難覆蓋所有邊界條件
```

### PostgreSQL RLS 的優勢

| 面向 | 應用層 Filter | PostgreSQL RLS |
|------|--------------|----------------|
| 執行層級 | Application code | Database engine |
| 可繞過性 | 工程師寫錯就漏 | 無法繞過 |
| 集中管理 | 散落各處 | 在 DB 定義一次 |
| 審計 | 需自己實作 | pg_audit 原生支援 |
| 新人風險 | 不知道規則會出事 | 規則在 DB，不需要知道 |

### 關鍵差異

> **應用層 Filter 是「請求模型自己守規矩」，PostgreSQL RLS 是「系統強制執行」。**

即使 Privileged Agent 被 prompt injection 騙了，想要讀 raw_memory：

```sql
-- Privileged Agent 執行
SET ROLE agent_privileged;
SELECT * FROM quarantine.raw_memory;

-- 結果：ERROR: permission denied for schema quarantine
```

這就是 CaMeL 精髓的落地：**就算模型被騙，系統邊界不會被突破**。

---

## 八、完整架構圖

```
┌─────────────────────────────────────────────────────────────────┐
│                        外部輸入層                                │
│    Email / OCR / API / Web / User Input                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  Quarantined Agent (agent_quarantined)                         │
│  - 可讀：自己的 raw_memory                                      │
│  - 可寫：quarantine.raw_memory                                  │
│  - 不可：呼叫 tool、觸發 action                                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                 quarantine.raw_memory                           │
│  - taint_level: 'external'                                      │
│  - TTL: 14 days                                                 │
│  - RLS: 只有 quarantined agent 能寫/讀自己的                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ memory_reviewer ONLY
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Sanitize Pipeline                            │
│  Detect → Transform → Approve                                   │
│  - Rule-based + LLM + 人工審核                                  │
│  - risk_score > 80 → 人工審核                                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                 memory.sanitized_memory                         │
│  - taint_level: 'internal'                                      │
│  - 結構化 JSON（facts, claims, risks, allowlist_actions）        │
│  - TTL: 90 days                                                 │
│  - RLS: privileged agent 可讀                                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  Privileged Agent (agent_privileged)                           │
│  - 可讀：sanitized_memory, policy_memory                        │
│  - 不可：讀 raw_memory（RLS 擋住）                               │
│  - 可做：tool call、workflow、action                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 九、坦白說：這套的 Trade-off

這套架構當然不是免費的午餐。

### 複雜度增加

- 需要維護三層記憶 + 四個 DB Role
- Sanitize pipeline 需要設計與調整
- 開發者需要理解「為什麼不能直接查 raw」

### 延遲增加

- 從 raw → sanitized 需要一個 pipeline
- 不適合需要即時回應的場景

### Sanitize 可能漏洞

- Rule-based sanitizer 可能漏掉新型攻擊
- LLM-based sanitizer 本身也可能被騙
- 需要持續更新 detection 規則

### 但這些 Trade-off 是值得的

對於企業級 AI Agent——尤其是有權限操作資料庫、API、金流的場景——這些代價換來的是：

> **即使 LLM 被騙，系統邊界不會被突破。**

這是傳統的 prompt engineering 和 guardrails 做不到的事。

---

## 十、結語

CaMeL 的精髓從來不是「用兩個模型」，而是「建立兩個不可跨越的權限域」。

PostgreSQL 能把這個權限域做成**系統級的安全邊界**：

- RLS 讓隔離不可繞過
- DB Role 讓權限在引擎層強制執行
- Sanitize pipeline 讓「高污染」變「可治理」
- 三層記憶架構讓每一層的責任清晰可見

對正在打造企業級 Agent 的團隊來說，這套架構的核心價值是：

> 不要把希望寄託在「模型會變乖」，
> 而是讓系統本身，在設計上就不需要信任模型。

---

## 延伸閱讀

- [CaMeL：Google DeepMind 提出的 Prompt Injection 防禦架構](/camel-privileged-vs-quarantined-agent-which-needs-stronger-llm/)
- [為什麼我開始把 PostgreSQL 當成 AI 的「自家記憶庫」](/postgresql-ai-memory-store/)
- [AI Agent 安全性：遊戲規則已經改變](/ai-agent-security-game-changed/)
- [AI Guardrails 為什麼註定失敗？](/openai-dou-dang-bu-zhu-de-gong-ji-ai-an-quan-fang-tan/)
