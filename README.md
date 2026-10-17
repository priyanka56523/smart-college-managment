# Global AI & AGI News Intelligence Platform

An enterprise-grade, evidence-driven intelligence platform that autonomously discovers trending AI and AGI developments across global web sources, verifies their factual authenticity against primary records, identifies the people and organizations involved, evaluates cross-sector economic and workforce impacts, and deterministically ranks them by both **Trending Momentum** and **Market Importance**.

---

## Key Features & Capabilities

- **Autonomous Multi-Source Discovery**:
  - **NewsAPI Integration**: Ingests mainstream and technology news covering 10 core AI domains (reasoning models, autonomous agents, GPUs & datacenter power, humanoid robotics, AI safety, startups, etc.).
  - **arXiv Research Adapter**: Ingests frontier academic preprints (`cs.AI`, `cs.LG`, `cs.CL`, `cs.RO`).
  - **GitHub Adapter**: Tracks developer velocity, trending agent frameworks, and open-weight model releases.
  - **Official AI Lab Feeds**: Direct primary announcements from OpenAI, Anthropic, Google DeepMind, Meta AI, Hugging Face, and NVIDIA.
  - **Live HTTP Corroboration Engine**: Probes primary sources in real time to verify URL reachability and detect corrections or counterevidence.

- **Semantic Deduplication & Event Clustering**:
  - Uses TF-IDF vectorization and cosine similarity (`scikit-learn`) to cluster syndicated reports and duplicate wire articles into a single canonical story record.
  - Distinguishes publication timestamps from actual event dates to detect re-reported or stale news.

- **NVIDIA NIM Hosted LLM Integration**:
  - Connects to NVIDIA's OpenAI-compatible Chat Completions endpoint (`https://integrate.api.nvidia.com/v1`).
  - Strict defense against prompt injection from untrusted web text.
  - Pydantic schema validation for claim extraction, entities, and industry implications.
  - Deterministic analytical fallback when unauthenticated, ensuring zero hallucinations.

- **Transparent Evidence Verification Engine**:
  - Assigns one of six strict verification statuses:
    - `VERIFIED`: Strong direct evidence supports central factual claims.
    - `CORROBORATED`: Multiple credible sources support the event, but some technical details remain pending.
    - `PARTIALLY VERIFIED`: Event is genuine, but key performance claims remain unproven.
    - `UNVERIFIED`: Insufficient independent evidence or single-source leaks.
    - `DISPUTED`: Credible independent sources materially conflict on benchmarks or methodology.
    - `FALSE OR DEBUNKED`: Reliable evidence or author retractions demonstrate the claim is false.
  - **AGI Claim Safeguard**: Advertised AGI claims by corporations are never treated as scientific proof of AGI.

- **Dual Independent Scoring & Leaderboards**:
  - **Trending Score (0–100)**:
    - Growth in independent news coverage: 25 pts
    - Public discussion & engagement momentum: 25 pts
    - Search-interest growth: 20 pts
    - Developer & research activity: 15 pts
    - Recency & acceleration: 15 pts
    - Labels: `TRENDING NOW`, `EMERGING`, `PERSISTENT`, `HIGH IMPORTANCE BUT NOT TRENDING`.
  - **Market Importance Score (0–100)**:
    - Market and economic impact: 25 pts
    - Technical or scientific significance: 20 pts
    - Trend momentum: 15 pts
    - Industry disruption potential: 15 pts
    - Strategic & geopolitical importance: 10 pts
    - Evidence strength: 10 pts
    - Time sensitivity: 5 pts
  - **Emerging Signals Isolation**: Unverified or disputed claims with high speculative impact are isolated from confirmed leaderboards.

- **Cross-Sector & Workforce Transformation Analysis**:
  - Evaluates impact across 11 key industries: Software/SaaS, Semiconductors/Hardware, Banking/Finance, Healthcare/Biotech, Robotics/Manufacturing, Education, Media/Entertainment, Retail, Cybersecurity/Defense, Energy/Utilities, and Professional Services.
  - Validates publicly traded tickers (NVDA, MSFT, GOOGL, TSM, AMZN, etc.) and distinguishes confirmed corporate exposure from analytical speculation.
  - Analyzes workforce task exposure and augmentation vs displacement potential.

- **Real APScheduler Background Runner**:
  - Automatically runs ingestion cycles (configurable, default every 6 hours).
  - Automatically compiles daily executive intelligence briefings.

---

## Architecture Overview

```
                      ┌───────────────────────────────────────────────┐
                      │              External Sources                 │
                      │  NewsAPI • arXiv • GitHub • Lab Feeds • Web  │
                      └───────────────────────┬───────────────────────┘
                                              │ Raw Articles
                                              ▼
                                ┌───────────────────────────┐
                                │ Ingestion & Normalization │
                                └─────────────┬─────────────┘
                                              │
                                              ▼
                      ┌───────────────────────────────────────────────┐
                      │    Deduplication & Event Clustering Engine    │
                      │           (TF-IDF + Cosine Matrix)            │
                      └───────────────────────┬───────────────────────┘
                                              │ Clustered Stories
                                              ▼
        ┌───────────────────────────────────────────────────────────────────────────┐
        │                        NVIDIA NIM Hosted LLM                              │
        │               (Claim Extraction & Structured Analysis)                    │
        └─────────────────────────────────────┬─────────────────────────────────────┘
                                              │ Structured Claims & Entities
                                              ▼
        ┌───────────────────────────────────────────────────────────────────────────┐
        │                      Evidence Verification Engine                         │
        │     (HTTP Probe Verification • Primary Citations • Debunk Detection)      │
        └─────────────────────────────────────┬─────────────────────────────────────┘
                                              │
                    ┌─────────────────────────┴─────────────────────────┐
                    ▼                                                   ▼
┌───────────────────────────────────────┐   ┌───────────────────────────────────────┐
│        Trending Scoring Engine        │   │    Market Importance Scoring Engine   │
│  (Coverage • Discussion • Dev • Rec)  │   │   (Economic • Tech • Disruption • Ev) │
└───────────────────┬───────────────────┘   └───────────────────┬───────────────────┘
                    │                                           │
                    └─────────────────────────┬─────────────────┘
                                              │ Persist & Rank
                                              ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│                               FastAPI Backend & DB                                │
│       SQLite / PostgreSQL • REST API • APScheduler Task Queue • Report Generator   │
└─────────────────────────────────────────────┬─────────────────────────────────────┘
                                              │ REST Endpoints
                                              ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│                        Modern React + TypeScript Frontend                         │
│  Overview • News Feed • Story Dossier Modals • Trend Analytics • Sources Registry │
└───────────────────────────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
demo1/
├── .env.example                     # Safe environment template
├── .env                             # Local environment variables
├── .gitignore                       # Git ignore configuration
├── run.ps1                          # Windows PowerShell launch script
├── run.sh                           # Unix bash launch script
├── README.md                        # Documentation
├── backend/
│   ├── requirements.txt             # Python backend dependencies
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py                # Pydantic BaseSettings & env loader
│   │   ├── database.py              # SQLAlchemy engine & session maker
│   │   ├── models.py                # Database ORM models
│   │   ├── schemas.py               # Pydantic schemas for API & LLM
│   │   ├── main.py                  # FastAPI application & SPA static server
│   │   ├── adapters/                # Source adapters
│   │   │   ├── base.py              # Base adapter abstract class
│   │   │   ├── newsapi_adapter.py   # NewsAPI Everything & Top-Headlines
│   │   │   ├── arxiv_adapter.py     # arXiv Research API
│   │   │   ├── github_adapter.py    # GitHub Trending Repositories
│   │   │   ├── official_feeds_adapter.py # OpenAI, DeepMind, Anthropic RSS
│   │   │   └── search_corroborator.py   # HTTP probes & verification
│   │   ├── services/
│   │   │   ├── deduplication.py     # TF-IDF & Cosine event clustering
│   │   │   ├── llm_service.py       # NVIDIA NIM LLM client & fallback
│   │   │   ├── verification_service.py # 6-tier verification rules
│   │   │   ├── scoring_service.py   # Trending & Market Importance rubrics
│   │   │   ├── impact_service.py    # 11-sector & workforce impact
│   │   │   ├── reporting_service.py # Briefing & Alert generation
│   │   │   ├── seed_data.py         # Verified real-world baseline data
│   │   │   ├── ingestion_pipeline.py# End-to-end orchestration
│   │   │   └── scheduler_service.py # APScheduler background worker
│   │   └── api/
│   │       └── api_router.py        # REST endpoints
│   └── tests/
│       ├── conftest.py              # Pytest database fixtures
│       ├── test_adapters.py         # Adapter connectivity & limitation tests
│       ├── test_api_endpoints.py    # FastAPI endpoint integration tests
│       ├── test_deduplication.py    # TF-IDF & clustering tests
│       ├── test_scoring.py          # Dual scoring engine tests
│       └── test_verification.py     # Verification status & AGI safeguard tests
└── frontend/
    ├── package.json                 # React, Vite, Tailwind, Lucide dependencies
    ├── vite.config.ts               # Vite bundler config with API proxy
    ├── tailwind.config.js           # Dark theme styling palette
    ├── tsconfig.json                # TypeScript compiler options
    ├── index.html                   # HTML entry
    ├── dist/                        # Production build artifacts
    └── src/
        ├── types.ts                 # TypeScript type interfaces
        ├── api.ts                   # Backend API client
        ├── main.tsx                 # React DOM root
        ├── App.tsx                  # Master application container
        ├── index.css                # Tailwind directives
        └── components/
            ├── Header.tsx           # Nav bar & status pills
            ├── OverviewTab.tsx      # Dual leaderboards & emerging signals
            ├── NewsFeedTab.tsx      # Filterable news feed & cards
            ├── StoryDetailModal.tsx # In-depth analytical dossier modal
            ├── TrendAnalyticsTab.tsx# Sector exposure matrix & analytics
            ├── SourcesTab.tsx       # Clickable source registry
            ├── ReportsTab.tsx       # Briefings generator & archive reader
            └── ConnectionStatusModal.tsx # Live API constraint modal
```

---

## Configuration & Environment Variables

Create a `.env` file in the project root based on `.env.example`:

```bash
# Copy example
cp .env.example .env
```

| Variable | Description | Default |
|---|---|---|
| `NEWSAPI_API_KEY` | Your NewsAPI developer or commercial key | *(optional, fallback active)* |
| `NEWSAPI_BASE_URL` | NewsAPI base URL | `https://newsapi.org/v2` |
| `NVIDIA_API_KEY` | NVIDIA Hosted NIM LLM API key (`nvapi-...`) | *(optional, fallback active)* |
| `NVIDIA_BASE_URL` | NVIDIA NIM endpoint | `https://integrate.api.nvidia.com/v1` |
| `NVIDIA_MODEL` | Target NVIDIA hosted model | `meta/llama-3.1-70b-instruct` |
| `DATABASE_URL` | Database connection string | `sqlite:///./ai_news_intelligence.db` |
| `SCHEDULER_ENABLED` | Enable automated background ingestion & briefings | `True` |
| `SCHEDULER_INTERVAL_HOURS` | Ingestion frequency in hours | `6` |

> **Note on Fallback Modes:** If `NEWSAPI_API_KEY` or `NVIDIA_API_KEY` is not provided, the platform automatically utilizes open research adapters (arXiv, GitHub, official laboratory RSS) and the deterministic analytical extraction engine.

---

## Quick Launch Instructions

### 1. Launch with PowerShell (Windows)
```powershell
.\run.ps1
```

### 2. Launch with Bash (Linux / macOS)
```bash
chmod +x run.sh
./run.sh
```

### 3. Manual Python Launch
```powershell
# Activate virtual environment
.\backend\.venv\Scripts\Activate.ps1

# Run server
python -m uvicorn app.main:app --app-dir "backend" --host 127.0.0.1 --port 8000 --reload
```

Open your browser to:
- **Web Application Dashboard**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive REST API Documentation (Swagger)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Running Automated Tests

All 22 unit and integration tests can be executed via `pytest`:

```powershell
& ".\backend\.venv\Scripts\pytest.exe" -v "backend/tests"
```

### Verified Test Coverage
- **`test_adapters.py`**: Validates NewsAPI key handling, NVIDIA NIM parameter checking, arXiv query syntax, GitHub API rate limits, and live HTTP probes.
- **`test_api_endpoints.py`**: Integration tests for `/api/health`, `/api/config/test-connections`, `/api/stories`, `/api/stories/{id}`, `/api/leaderboards`, `/api/analytics`, `/api/sources`, and `/api/reports/generate`.
- **`test_deduplication.py`**: Verifies text normalization and TF-IDF cosine clustering of syndicated articles.
- **`test_scoring.py`**: Verifies individual component weights for Trending (0–100) and Market Importance (0–100), ensuring unverified high-impact claims are isolated into emerging signals.
- **`test_verification.py`**: Verifies detection of retracted/debunked claims, contested methodologies, and enforcement of the AGI safeguard rule.

---

## API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | System health, database status, scheduler state, and external integration health. |
| `GET` | `/api/config/test-connections` | Real-time connection probes, model checks, rate limits, and constraint disclosures. |
| `GET` | `/api/stories` | List stories with filters (`search`, `verification_status`, `industry`, `entity`, `sort_by`). |
| `GET` | `/api/stories/{id}` | Detailed story dossier with claims, evidence, score breakdowns, and ranking history. |
| `GET` | `/api/leaderboards` | Top 10 Trending, Top 10 Market Importance, and isolated Emerging Signals. |
| `GET` | `/api/analytics` | Sector exposure matrix, verification breakdown, top entities, and freshness timestamps. |
| `GET` | `/api/sources` | Complete registry of examined citations, URLs, source types, and access probe results. |
| `GET` | `/api/reports` | Historical executive intelligence briefings. |
| `POST` | `/api/reports/generate` | Generates a new executive intelligence briefing (`daily`, `six_hour`, `weekly`, `alert`). |
| `POST` | `/api/ingest` | Triggers immediate multi-source live ingestion cycle. |

---

## Troubleshooting & FAQ

1. **Port 8000 is already in use:**
   Run `Get-Process python* | Stop-Process` in PowerShell or specify `--port 8080`.
2. **Missing Node or NPM on another machine:**
   The repository includes a self-contained portable Node.js toolchain under `.tools/node` which requires zero administrative privileges.
3. **NewsAPI Returns 429 or Truncated Content:**
   The free Developer plan of NewsAPI restricts results to 100/day and truncates content. The platform's `SearchCorroboratorAdapter` automatically seeks primary full-text citations from official lab announcements and arXiv to cross-validate claims.
4. **NVIDIA NIM API Key Issues:**
   Ensure your API key from [build.nvidia.com](https://build.nvidia.com/) starts with `nvapi-`. You can test its connectivity at any time using the "Integrations & Health" button in the top navigation bar.
