import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field, ConfigDict

# --- LLM Structured Extraction Schema ---

class ExtractedClaim(BaseModel):
    claim_text: str = Field(description="Exact statement of fact or claim made in the report.")
    claim_type: str = Field(default="central_claim", description="central_claim, supporting_fact, prediction_opinion, or technical_metric")
    supporting_facts: List[str] = Field(default_factory=list, description="Direct factual indicators or quotes supporting this claim.")
    missing_evidence: Optional[str] = Field(default=None, description="Critical evidence, benchmarks, or reproducibility details that are absent.")

class ExtractedEntity(BaseModel):
    name: str = Field(description="Name of person or organization.")
    entity_type: str = Field(description="person, company, research_institution, or government_body")
    role: Optional[str] = Field(default=None, description="Official professional title or affiliation.")
    organization: Optional[str] = Field(default=None)
    story_role: str = Field(default="announcer", description="creator, researcher, announcer, investor, partner, independent_evaluator, critic, or commentator")
    direct_involvement: Optional[str] = Field(default=None, description="Specific documented action or statement in this event.")
    ticker_symbol: Optional[str] = Field(default=None, description="Verified stock ticker if publicly traded (e.g. NVDA, MSFT).")
    exchange: Optional[str] = Field(default=None, description="e.g. NASDAQ, NYSE")

class ExtractedIndustryImpact(BaseModel):
    industry_name: str = Field(description="Sector name (e.g. Software/SaaS, Semiconductors/Hardware, Banking/Finance, Healthcare/Biotech, Robotics/Manufacturing, Education, Media/Entertainment, Retail, Cybersecurity/Defense, Energy/Utilities, Professional Services)")
    impact_direction: str = Field(default="uncertain", description="positive, negative, mixed, or uncertain")
    impact_magnitude: str = Field(default="medium", description="low, medium, high, or transformative")
    time_horizon: str = Field(default="near_term", description="immediate (0-6m), near_term (6-24m), medium_term (2-5y), or long_term (>5y)")
    mechanism: str = Field(description="Specific causal mechanism through which this technology impacts this sector.")
    potential_beneficiaries: Optional[str] = Field(default=None)
    disrupted_business_models: Optional[str] = Field(default=None)
    workforce_task_exposure: Optional[str] = Field(default=None, description="Specific job tasks augmented or exposed.")
    workforce_augmentation_vs_displacement: Optional[str] = Field(default=None, description="Assessment of augmentation vs displacement potential.")
    confidence_level: str = Field(default="medium", description="high, medium, or speculative")

class LLMStoryAnalysisResult(BaseModel):
    title: str = Field(description="Clear, informative canonical story title.")
    summary: str = Field(description="Objective factual overview of the development.")
    what_happened: str = Field(description="Precise description of the core announcement or event.")
    what_is_new: str = Field(description="What differentiates this from prior capabilities, models, or state of the art.")
    claims: List[ExtractedClaim] = Field(default_factory=list)
    entities: List[ExtractedEntity] = Field(default_factory=list)
    industry_impacts: List[ExtractedIndustryImpact] = Field(default_factory=list)
    suggested_verification_status: str = Field(default="UNVERIFIED", description="VERIFIED, CORROBORATED, PARTIALLY_VERIFIED, UNVERIFIED, DISPUTED, or FALSE_OR_DEBUNKED")
    verification_rationale: str = Field(description="Transparent evidence-based reasoning behind the status.")
    next_milestones_to_monitor: Optional[str] = Field(default=None, description="Upcoming benchmark tests, code releases, or regulatory filings to watch.")


# --- API Models ---

class ArticleOut(BaseModel):
    id: int
    provider_id: str
    canonical_url: str
    original_url: Optional[str]
    headline: str
    description: Optional[str]
    publisher: Optional[str]
    published_at: Optional[datetime.datetime]
    collected_at: datetime.datetime
    language: Optional[str]
    retrieval_status: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class ClaimOut(BaseModel):
    id: int
    claim_text: str
    claim_type: str
    verification_status: str
    supporting_evidence: Optional[str] = None
    conflicting_evidence: Optional[str] = None
    missing_evidence: Optional[str] = None
    evidence_urls: List[str] = []

    model_config = ConfigDict(from_attributes=True)

class EntityOut(BaseModel):
    id: int
    name: str
    entity_type: str
    role: Optional[str] = None
    organization: Optional[str] = None
    story_role: str
    direct_involvement: Optional[str] = None
    public_statement: Optional[str] = None
    profile_url: Optional[str] = None
    ticker_symbol: Optional[str] = None
    exchange: Optional[str] = None
    is_confirmed_exposure: bool = True

    model_config = ConfigDict(from_attributes=True)

class IndustryImpactOut(BaseModel):
    id: int
    industry_name: str
    impact_direction: str
    impact_magnitude: str
    time_horizon: str
    mechanism: Optional[str] = None
    potential_beneficiaries: Optional[str] = None
    disrupted_models: Optional[str] = None
    workforce_task_exposure: Optional[str] = None
    workforce_augmentation_vs_displacement: Optional[str] = None
    confidence_level: str
    supporting_evidence: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ScoreBreakdownOut(BaseModel):
    news_coverage_growth: float
    public_discussion: float
    search_interest: float
    developer_research_activity: float
    recency_acceleration: float
    trending_total: float
    
    market_economic_impact: float
    technical_significance: float
    trend_momentum: float
    industry_disruption: float
    strategic_importance: float
    evidence_strength: float
    time_sensitivity: float
    market_total: float
    
    scoring_rationale: Optional[str] = None
    scoring_version: str
    calculated_at: datetime.datetime
    coverage_limitation_notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class RankingHistoryOut(BaseModel):
    id: int
    trending_rank: Optional[int]
    market_rank: Optional[int]
    trending_score: float
    market_importance_score: float
    verification_status: Optional[str]
    recorded_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class SourceRecordOut(BaseModel):
    id: int
    title: str
    publisher: Optional[str]
    url: str
    source_type: str
    access_status: str
    claims_supported: Optional[str] = None
    published_date: Optional[datetime.datetime] = None

    model_config = ConfigDict(from_attributes=True)

class StoryListItem(BaseModel):
    id: int
    title: str
    summary: str
    first_discovered_at: datetime.datetime
    event_date: Optional[datetime.datetime]
    last_checked_at: datetime.datetime
    verification_status: str
    trending_score: float
    trending_label: str
    market_importance_score: float
    trending_rank: Optional[int]
    market_rank: Optional[int]
    is_emerging_signal: bool
    entities: List[EntityOut] = []
    industry_impacts: List[IndustryImpactOut] = []
    sources: List[SourceRecordOut] = []

    model_config = ConfigDict(from_attributes=True)

class StoryDetail(StoryListItem):
    what_happened: Optional[str]
    what_is_new: Optional[str]
    verification_rationale: Optional[str]
    previous_status: Optional[str]
    verification_timestamp: Optional[datetime.datetime]
    next_milestones: Optional[str]
    articles: List[ArticleOut] = []
    claims: List[ClaimOut] = []
    score_breakdown: Optional[ScoreBreakdownOut] = None
    ranking_history: List[RankingHistoryOut] = []

    model_config = ConfigDict(from_attributes=True)

class LeaderboardResponse(BaseModel):
    trending_leaderboard: List[StoryListItem]
    market_leaderboard: List[StoryListItem]
    emerging_signals: List[StoryListItem]
    scoring_methodology: Dict[str, Any]

class AnalyticsResponse(BaseModel):
    total_stories: int
    total_articles: int
    verification_counts: Dict[str, int]
    trending_labels_counts: Dict[str, int]
    top_industries_exposed: List[Dict[str, Any]]
    top_entities: List[Dict[str, Any]]
    score_distribution: Dict[str, Any]
    data_freshness: Dict[str, Any]

class IntelligenceReportOut(BaseModel):
    id: int
    title: str
    report_type: str
    research_timestamp: datetime.datetime
    timezone_name: str
    coverage_period_start: datetime.datetime
    coverage_period_end: datetime.datetime
    sources_examined_count: int
    coverage_gaps_notes: Optional[str]
    executive_summary: str
    ranked_trending_ids: List[int]
    ranked_market_ids: List[int]
    emerging_signals_ids: List[int]
    key_developments_to_monitor: Optional[str]
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class APIConnectionTestResult(BaseModel):
    service: str
    status: str  # OK, CONSTRAINED, INVALID_KEY, MISSING_KEY, UNREACHABLE
    endpoint: str
    model: Optional[str] = None
    message: str
    rate_limits: Optional[Dict[str, Any]] = None
    account_constraints: Optional[Dict[str, Any]] = None

class SystemHealthResponse(BaseModel):
    status: str
    timestamp: datetime.datetime
    version: str
    database: str
    scheduler_running: bool
    last_ingestion_time: Optional[datetime.datetime]
    integrations: List[APIConnectionTestResult]
