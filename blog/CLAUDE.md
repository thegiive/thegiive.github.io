# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **blog content and chatbot system repository** containing:
1. **Original Blog Content** - Chinese AI/tech blog articles from https://ai-coding.wiselychen.com/
2. **Chatbot Web Application** - A chatbot system deployed on Google Cloud Run that embodies Wisely Chen's communication style

## Project Structure

```
blog/
├── orginal blog/           # Blog articles in markdown format (14+ articles)
│   ├── index.md           # Main blog index
│   ├── author-profile.md  # Wisely Chen's writing style analysis
│   └── *.md              # Individual blog posts (ATPM, FDE, Vibe Coding topics)
├── chatbot-web/           # Chatbot application (Python API + Node.js frontend)
│   ├── api.py            # FastAPI backend with OpenAI integration
│   ├── server.js         # Express.js frontend server
│   ├── public/           # Static HTML files (index.html, embed.html)
│   ├── deploy-*.sh       # Deployment scripts for Cloud Run
│   └── *.yaml           # Cloud Build configuration files
├── WiselyChenProfile.md   # Author's tone and communication style guide
├── System_Prompt.md       # System prompt for chatbot behavior
└── blog_summary.md        # Summary of blog content and key insights
```

## Core Components

### 1. Blog Content

**Purpose:** Technical blog articles about AI coding practices, ATPM framework, and FDE methodology.

**Key Frameworks Documented:**
- **ATPM** (Assessment, Testing, Program, Management) - Vibe Coding framework
- **FDE** (Forward Deployed Engineer) - On-site AI implementation methodology
- **Three-Layer AI Collaboration** - Embed → Copilot → Agent progression

**Quantified Results Documented:**
- 40% development time acceleration
- PRD to code ratio: 1:1.4 (9,211 → 13,022 lines)
- Onboarding reduction: 2-3 weeks → 3 days
- Enterprise AI failure rate: 95% (documented for context)

### 2. Chatbot Application Architecture

**Technology Stack:**
- **Backend:** Python 3.11 + FastAPI + Uvicorn
- **Frontend:** Node.js 18 + Express
- **AI:** OpenAI API (GPT-4o-mini)
- **Database:** Google Firestore
- **Platform:** Google Cloud Run (asia-east1)
- **Authentication:** API key hashing (SHA256) + Referer validation

**System Flow:**
```
User → Frontend (Express) → Backend API (FastAPI) → OpenAI API
                                      ↓
                              Firestore (message storage)
```

**Key Features:**
- Multi-turn conversation with history
- Session management (UUID-based)
- Rate limiting (30 requests/60s by default)
- Fallback responses when OpenAI unavailable
- API key authentication + referer whitelisting
- Firestore integration for conversation persistence

## Common Development Commands

### Running Locally

**Backend API:**
```bash
cd chatbot-web
# Install Python dependencies
pip3 install -r requirements.txt

# Set required environment variables (without authentication)
export OPENAI_API_KEY="your-key-here"
export OPENAI_MODEL="gpt-4o-mini"
export GCP_PROJECT_ID="nbd-n8n-flow-prd"

# OR with API key authentication enabled
export OPENAI_API_KEY="your-key-here"
export OPENAI_MODEL="gpt-4o-mini"
export GCP_PROJECT_ID="nbd-n8n-flow-prd"
export VALID_API_KEY_HASHES="1c9145c221834c239331cd8281c84689159eb0fc1605be8a195e2db32db7f6c1,909c8c0e8775614b148f55cace8c32a6e263e375f7416c8bb09521b5dea0dce6,e72819c45789b8b5817f9868fbce5981363b31e197aaecaddaec3443df9266ec"
export ALLOWED_REFERERS="http://localhost:8080"

# Run API server
python3 api.py
# Runs on: http://localhost:8000
```

**Frontend:**
```bash
cd chatbot-web
npm install
export API_URL="http://localhost:8000"
export CHATBOT_API_KEY="your-api-key"
npm start
# Runs on: http://localhost:8080
```

### Deployment to Google Cloud Run

**Prerequisites:**
- Google Cloud SDK installed at `~/Downloads/google-cloud-sdk/`
- Authenticated: `~/Downloads/google-cloud-sdk/bin/gcloud auth login`
- Project: `nbd-n8n-flow-prd`
- Region: `asia-east1`

**Full Deployment (API + Frontend):**
```bash
cd chatbot-web
./deploy-all.sh
```

**Deploy API Only:**
```bash
cd chatbot-web
./deploy-api.sh
```

**Deploy Frontend Only:**
```bash
cd chatbot-web
API_URL=https://chatbot-api-xxx.run.app ./deploy-frontend.sh
```

**Current Production URLs:**
- **Backend API:** https://chatbot-api-1052673152231.asia-east1.run.app
- **Frontend Web:** https://chatbot-web-1052673152231.asia-east1.run.app

**Test Deployment:**
```bash
# Health check
curl https://chatbot-api-1052673152231.asia-east1.run.app/health

# Test chat (with API key)
curl -X POST https://chatbot-api-1052673152231.asia-east1.run.app/api/chat \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: cbot_live_lTTG6h-xsORFiv_HAvvC0jtWuAYv3UepZgFvVho-DSA' \
  -H 'Referer: https://chatbot-web-1052673152231.asia-east1.run.app' \
  -d '{"message":"你好"}'

# Run full authentication test suite
./test_auth.sh https://chatbot-api-1052673152231.asia-east1.run.app
```

### API Key Management

**Generate new API keys:**
```bash
cd chatbot-web
python3 generate_api_key.py
```

**Test API key:**
```bash
cd chatbot-web
./test_api_key.sh
```

**Configuration locations:**
- API keys (hashed): `env.yaml` → `VALID_API_KEY_HASHES`
- Allowed referers: `env.yaml` → `ALLOWED_REFERERS`
- Plain text keys (for frontend): `deploy-frontend.sh` → `CHATBOT_API_KEY`

### Viewing Logs

```bash
# API logs
~/Downloads/google-cloud-sdk/bin/gcloud run services logs read chatbot-api \
  --region asia-east1 --project nbd-n8n-flow-prd --limit 50

# Frontend logs
~/Downloads/google-cloud-sdk/bin/gcloud run services logs read chatbot-web \
  --region asia-east1 --project nbd-n8n-flow-prd --limit 50
```

## API Key Authentication (Enabled ✅)

**Status:** Fully enabled and tested in production

### Current Configuration

**Backend API Keys (3 active):**
- Key #1: `cbot_live_lTTG6h-xsORFiv_HAvvC0jtWuAYv3UepZgFvVho-DSA` (Frontend primary)
- Key #2: `cbot_live_NE87hoO7G6l31EcQzfiOtCxNDWmOZNbnw8g8-nv7EO4` (Backup)
- Key #3: `cbot_live_R-olPiBFkAcBch42lx91L4hZ1Nnm3DXkQmvz8No7rb0` (Backup)

**Storage:**
- Plain text keys: `api_keys.json` (not in git)
- Hashes: `env.yaml` → `VALID_API_KEY_HASHES`
- Frontend key: `deploy-frontend.sh` → `CHATBOT_API_KEY`

### Three-Layer Security

```
Request → [1. API Key] → [2. Referer Check] → [3. Rate Limit] → Response
```

**Layer 1: API Key Validation**
- Client must provide `X-API-Key` header
- Backend validates using SHA256 hash
- Invalid/missing key → 401 Unauthorized

**Layer 2: Referer Whitelist**
- Allowed origins in `env.yaml` → `ALLOWED_REFERERS`
- Currently allowed:
  - `https://chatbot-web-1052673152231.asia-east1.run.app`
  - `https://chatbot-web-yc5klowxya-de.a.run.app`
  - `http://localhost:8080`
- Invalid referer → 403 Forbidden

**Layer 3: Rate Limiting**
- Default: 30 requests / 60 seconds
- Per IP or session ID
- Exceeded → 429 Too Many Requests

### Testing Authentication

**Run test suite:**
```bash
cd chatbot-web

# Test local API
./test_auth.sh

# Test production API
./test_auth.sh https://chatbot-api-1052673152231.asia-east1.run.app
```

**Expected results:** All 5 tests pass
- Test 1: No API key → 401 ✅
- Test 2: Invalid API key → 401 ✅
- Test 3: Valid API key → 200 ✅
- Test 4: Invalid referer → 403 ✅
- Test 5: Health check → 200 ✅

### Managing API Keys

**Generate new keys:**
```bash
cd chatbot-web
python3 generate_api_key.py
```

**Rotate keys:**
1. Generate new keys: `python3 generate_api_key.py`
2. Add new hashes to `env.yaml` (keep old ones temporarily)
3. Deploy backend: `./deploy-api.sh`
4. Update frontend key in `deploy-frontend.sh`
5. Deploy frontend: `API_URL=xxx ./deploy-frontend.sh`
6. Test new key works
7. Remove old hashes from `env.yaml`
8. Redeploy backend: `./deploy-api.sh`

**Revoke a key:**
1. Remove hash from `env.yaml` → `VALID_API_KEY_HASHES`
2. Redeploy: `./deploy-api.sh`
3. Key is immediately invalid

## Critical Architecture Details

### 1. System Prompt Design

The chatbot's personality is defined by combining three key documents:
- `System_Prompt.md` - Basic rules and behavior constraints
- `WiselyChenProfile.md` - Author's communication style (極度口語化)
- `blog_summary.md` - Core frameworks and quantified results

**Implementation:** See `api.py:271-571` where these are concatenated into `system_prompt`.

### 2. Authentication Flow

**Three-layer security:**
1. **API Key Hash Validation** - Client sends `X-API-Key` header, server validates against SHA256 hashes
2. **Referer Whitelisting** - Only requests from allowed domains are processed
3. **Rate Limiting** - IP/session-based throttling (configurable via env vars)

**Key functions in `api.py`:**
- `verify_api_key()` - Line 71-81
- `check_referer()` - Line 84-94
- `check_rate_limit()` - Line 97-112

### 3. Firestore Data Model

**Collection:** `chatbot-messages`

**Document Structure:**
```python
{
  'messageId': str,        # UUID v4
  'sessionId': str,        # UUID v4 (from client or generated)
  'role': str,            # 'user' or 'assistant'
  'content': str,         # Message text
  'timestamp': Timestamp,  # Firestore SERVER_TIMESTAMP
  'createdAt': str,       # ISO 8601 datetime
  'model': str,           # OpenAI model name or 'fallback'
  'tokens': dict,         # {prompt_tokens, completion_tokens, total_tokens}
  'metadata': dict        # {userAgent, referer, clientIp, error?}
}
```

**Save function:** `api.py:153-191` (`save_message_to_firestore`)

### 4. Environment Variables

**Required for API (`env.yaml`):**
```yaml
OPENAI_API_KEY: "sk-proj-..."
OPENAI_MODEL: "gpt-4o-mini"
GCP_PROJECT_ID: "nbd-n8n-flow-prd"
VALID_API_KEY_HASHES: "hash1,hash2,hash3"
ALLOWED_REFERERS: "https://domain1.com,https://domain2.com"
```

**Required for Frontend:**
```bash
API_URL=https://chatbot-api-xxx.run.app
CHATBOT_API_KEY=cbot_live_xxx
```

**Optional tuning:**
```bash
OPENAI_MAX_TOKENS=500           # Default: 500
OPENAI_TEMPERATURE=0.7          # Default: 0.7
RATE_LIMIT_REQUESTS=30          # Default: 30 requests
RATE_LIMIT_WINDOW=60            # Default: 60 seconds
```

## Wisely Chen's Writing Style

When creating or editing content that should match the author's voice:

**Core Principles:**
1. **數據驅動的誠實** - Use precise numbers, don't beautify results
2. **框架化教學** - Create systematic frameworks (like ATPM)
3. **反直覺的勇氣** - Challenge mainstream concepts
4. **極度口語化** - Use conversational tone with "就是"、"然後"、"對"

**Writing Pattern:**
```
爭議觀點 → 坦承困難 → 轉折點 → 量化成果 → 提煉原則
```

**Example:**
❌ Formal: "我們成功實施了AI解決方案，提升了團隊效率。"
✅ Wisely style: "說實在，我一開始也不知道會不會成功。找了20幾個工讀生，來來去去的，有三分之二的人不願意上去做高空盤點。但最後我們就是讓它動起來了，從8小時降到20分鐘。"

**Full style guide:** See `WiselyChenProfile.md` for comprehensive examples.

## Important Notes

### Security Considerations
- Never commit `OPENAI_API_KEY` to git (use environment variables)
- API keys are stored as SHA256 hashes in `env.yaml`
- Plain text API keys only exist in deployment scripts (not in version control)
- Rate limiting is in-memory (resets on container restart)

### Deployment Constraints
- Google Cloud SDK path is hardcoded: `~/Downloads/google-cloud-sdk/bin/gcloud`
- Project ID is fixed: `nbd-n8n-flow-prd`
- Region is fixed: `asia-east1`
- Cloud Build timeout: 10 minutes

### Performance Settings
- API: 512Mi memory, 1 CPU, 0-10 instances
- Frontend: 256Mi memory, 1 CPU, 0-10 instances
- API timeout: 60 seconds
- Firestore: Native mode (not Datastore mode)

## When Modifying the Chatbot

**To change personality:**
1. Edit `System_Prompt.md`, `WiselyChenProfile.md`, or `blog_summary.md`
2. Test locally with `python3 api.py`
3. Deploy: `./deploy-api.sh`

**To add new API endpoints:**
1. Add route in `api.py` using FastAPI decorators (`@app.get`, `@app.post`)
2. Update the root endpoint (`/`) to list new endpoint
3. Test locally before deployment

**To modify authentication:**
1. Generate new keys: `python3 generate_api_key.py`
2. Update `env.yaml` with new hashes
3. Update `deploy-frontend.sh` with new plain text key
4. Redeploy both services: `./deploy-all.sh`

**To change OpenAI model:**
1. Update `env.yaml` → `OPENAI_MODEL`
2. Redeploy API: `./deploy-api.sh`

## Troubleshooting

**"Invalid API key" errors:**
- Check `X-API-Key` header matches hash in `env.yaml`
- Verify `VALID_API_KEY_HASHES` is set correctly
- Test with: `./test_api_key.sh`

**"Firestore not available" errors:**
- Verify Firestore is enabled in GCP project
- Check service account has `roles/datastore.user` permission
- Ensure `GCP_PROJECT_ID` environment variable is set

**Rate limit exceeded:**
- Adjust `RATE_LIMIT_REQUESTS` and `RATE_LIMIT_WINDOW` in `env.yaml`
- Note: Rate limit state is in-memory and resets on restart

**Deployment fails:**
- Check gcloud authentication: `~/Downloads/google-cloud-sdk/bin/gcloud auth list`
- Verify Cloud Build API is enabled
- Check project quotas and billing

## Production Status

**Last Deployment:** 2025-10-25 23:57:00 UTC
**Deployment Status:** ✅ Success
**Authentication:** ✅ Enabled (3 API keys active)
**Test Results:** ✅ 5/5 tests passed

**Services:**
- Backend API: `chatbot-api-00009-t24` (Running)
- Frontend Web: `chatbot-web-00019-mhn` (Running)

**Security Status:**
- ✅ API Key authentication enabled
- ✅ Referer whitelist active
- ✅ Rate limiting enabled (30/60s)
- ✅ All authentication tests passing

**Quick Health Check:**
```bash
# Should return: {"status":"healthy","timestamp":"...","openai_configured":true}
curl https://chatbot-api-1052673152231.asia-east1.run.app/health
```

## Related Documentation

- **Architecture:** `chatbot-web/ARCHITECTURE.md`
- **Deployment Guide:** `chatbot-web/DEPLOY.md`
- **API Key Setup:** `chatbot-web/API_KEY_SETUP.md`
- **API Key Enabled:** `chatbot-web/API_KEY_ENABLED.md` ⭐ Complete auth guide
- **Deployment Success:** `chatbot-web/DEPLOYMENT_SUCCESS.md` ⭐ Latest deployment
- **Firestore Setup:** `chatbot-web/FIRESTORE_SETUP.md`
- **Embedding Guide:** `chatbot-web/EMBED_GUIDE.md`
- **Quick Start:** `chatbot-web/QUICKSTART.md`
- **Test Script:** `chatbot-web/test_auth.sh` ⭐ Authentication testing
