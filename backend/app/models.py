"""SQLAlchemy ORM models for Global AI & AGI News Intelligence Platform."""
import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Float, DateTime, Boolean, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from app.database import Base

class Article(Base):
    """Raw ingested news or research article from external providers."""
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(String(100), index=True)  # e.g., 'newsapi', 'arxiv', 'github', 'official_feed'
    provider_item_id = Column(String(255), nullable=True)  # provider's unique ID/hash
    canonical_url = Column(String(1000), unique=True, index=True)
    original_url = Column(String(1000))
    headline = Column(String(500), nullable=False, index=True)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    author = Column(String(255), nullable=True)
    publisher = Column(String(255), nullable=True, index=True)
    published_at = Column(DateTime, nullable=True, index=True)
    collected_at = Column(DateTime, default=datetime.datetime.utcnow)
    language = Column(String(10), default="en")
    retrieval_status = Column(String(50), default="success")  # success, truncated, rate_limited, error

    story_id = Column(Integer, ForeignKey("stories.id", ondelete="SET NULL"), nullable=True)
    story = relationship("Story", back_populates="articles")


class Story(Base):
    """Canonical event story clustered from one or multiple articles and evidence."""
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    summary = Column(Text, nullable=False)
    what_happened = Column(Text, nullable=True)
    what_is_new = Column(Text, nullable=True)
    
    first_discovered_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    event_date = Column(DateTime, nullable=True)
    last_checked_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Verification Status: VERIFIED, CORROBORATED, PARTIALLY VERIFIED, UNVERIFIED, DISPUTED, FALSE OR DEBUNKED
    verification_status = Column(String(50), default="UNVERIFIED", index=True)
    previous_status = Column(String(50), nullable=True)
    verification_rationale = Column(Text, nullable=True)
    verification_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Trending Score: 0 to 100
    trending_score = Column(Float, default=0.0, index=True)
    # TRENDING NOW, EMERGING, PERSISTENT, HIGH IMPORTANCE BUT NOT TRENDING
    trending_label = Column(String(50), default="EMERGING", index=True)
    
    # Market Importance Score: 0 to 100
    market_importance_score = Column(Float, default=0.0, index=True)
    
    # Current Leaderboard ranks
    trending_rank = Column(Integer, nullable=True, index=True)
    market_rank = Column(Integer, nullable=True, index=True)
    
    # High impact emerging signal flag (unverified claims kept separate from confirmed news rankings)
    is_emerging_signal = Column(Boolean, default=False, index=True)
    
    # Next milestones or developments to monitor
    next_milestones = Column(Text, nullable=True)
    
    # Relationships
    articles = relationship("Article", back_populates="story", cascade="all, delete-orphan")
    claims = relationship("Claim", back_populates="story", cascade="all, delete-orphan")
    entities = relationship("Entity", back_populates="story", cascade="all, delete-orphan")
    industry_impacts = relationship("IndustryImpact", back_populates="story", cascade="all, delete-orphan")
    score_breakdown = relationship("ScoreBreakdown", back_populates="story", uselist=False, cascade="all, delete-orphan")
    sources = relationship("SourceRecord", back_populates="story", cascade="all, delete-orphan")
    ranking_history = relationship("RankingHistory", back_populates="story", cascade="all, delete-orphan")


class Claim(Base):
    """Specific factual assertion or claim extracted from candidate stories."""
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    
    claim_text = Column(Text, nullable=False)
    # central_claim, supporting_fact, prediction_opinion, technical_metric
    claim_type = Column(String(50), default="central_claim")
    verification_status = Column(String(50), default="UNVERIFIED")
    
    supporting_evidence = Column(Text, nullable=True)
    conflicting_evidence = Column(Text, nullable=True)
    missing_evidence = Column(Text, nullable=True)
    evidence_urls = Column(JSON, default=list)  # list of URLs
    
    story = relationship("Story", back_populates="claims")


class Entity(Base):
    """People and organizations involved in the event."""
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String(255), nullable=False, index=True)
    # person, company, research_institution, government_body, consortium
    entity_type = Column(String(50), nullable=False)
    role = Column(String(255), nullable=True)  # e.g., CEO, Lead Researcher, Professor
    organization = Column(String(255), nullable=True)
    
    # story_role: creator, researcher, announcer, investor, partner, independent_evaluator, critic, commentator
    story_role = Column(String(50), default="announcer")
    direct_involvement = Column(Text, nullable=True)
    public_statement = Column(Text, nullable=True)
    profile_url = Column(String(1000), nullable=True)
    
    # For public companies
    ticker_symbol = Column(String(20), nullable=True, index=True)
    exchange = Column(String(50), nullable=True)
    is_confirmed_exposure = Column(Boolean, default=True)  # distinguish confirmed from speculative
    
    story = relationship("Story", back_populates="entities")


class IndustryImpact(Base):
    """Analysis of impact on specific economic sectors and workforce transformation."""
    __tablename__ = "industry_impacts"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    
    # Sectors: Software/SaaS, Semiconductors/Hardware, Banking/Finance, Healthcare/Biotech,
    # Robotics/Manufacturing, Education, Media/Entertainment, Retail, Cybersecurity/Defense,
    # Energy/Utilities, Professional Services
    industry_name = Column(String(100), nullable=False, index=True)
    impact_direction = Column(String(20), default="positive")  # positive, negative, mixed, uncertain
    impact_magnitude = Column(String(20), default="medium")     # low, medium, high, transformative
    time_horizon = Column(String(30), default="near_term")     # immediate (0-6m), near_term (6-24m), medium_term (2-5y), long_term (>5y)
    
    mechanism = Column(Text, nullable=True)
    potential_beneficiaries = Column(Text, nullable=True)
    disrupted_models = Column(Text, nullable=True)
    
    # Workforce transformation breakdown
    workforce_task_exposure = Column(Text, nullable=True)
    workforce_augmentation_vs_displacement = Column(Text, nullable=True)
    
    confidence_level = Column(String(20), default="medium")    # high, medium, speculative
    supporting_evidence = Column(Text, nullable=True)
    
    story = relationship("Story", back_populates="industry_impacts")


class ScoreBreakdown(Base):
    """Transparent rubric score components and historical explanation."""
    __tablename__ = "score_breakdowns"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Trending components (sum 100)
    news_coverage_growth = Column(Float, default=0.0)      # max 25
    public_discussion = Column(Float, default=0.0)         # max 25
    search_interest = Column(Float, default=0.0)           # max 20
    developer_research_activity = Column(Float, default=0.0)# max 15
    recency_acceleration = Column(Float, default=0.0)      # max 15
    trending_total = Column(Float, default=0.0)
    
    # Market Importance components (sum 100)
    market_economic_impact = Column(Float, default=0.0)     # max 25
    technical_significance = Column(Float, default=0.0)     # max 20
    trend_momentum = Column(Float, default=0.0)             # max 15
    industry_disruption = Column(Float, default=0.0)        # max 15
    strategic_importance = Column(Float, default=0.0)       # max 10
    evidence_strength = Column(Float, default=0.0)          # max 10
    time_sensitivity = Column(Float, default=0.0)           # max 5
    market_total = Column(Float, default=0.0)
    
    scoring_rationale = Column(Text, nullable=True)
    scoring_version = Column(String(20), default="v1.0")
    calculated_at = Column(DateTime, default=datetime.datetime.utcnow)
    coverage_limitation_notes = Column(Text, nullable=True)
    
    story = relationship("Story", back_populates="score_breakdown")


class RankingHistory(Base):
    """Historical timeline of ranking and score adjustments."""
    __tablename__ = "ranking_history"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    
    trending_rank = Column(Integer, nullable=True)
    market_rank = Column(Integer, nullable=True)
    trending_score = Column(Float, nullable=False)
    market_importance_score = Column(Float, nullable=False)
    verification_status = Column(String(50), nullable=True)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    
    story = relationship("Story", back_populates="ranking_history")


class SourceRecord(Base):
    """Original primary evidence and independent corroborating sources."""
    __tablename__ = "source_records"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    
    title = Column(String(500), nullable=False)
    publisher = Column(String(255), nullable=True)
    url = Column(String(1000), nullable=False)
    # official_announcement, research_paper, code_repository, independent_news, regulatory_filing
    source_type = Column(String(50), default="independent_news")
    # accessed_and_verified, accessed_inconclusive, paywall_inaccessible, unreachable
    access_status = Column(String(50), default="accessed_and_verified")
    claims_supported = Column(Text, nullable=True)
    published_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    story = relationship("Story", back_populates="sources")


class IntelligenceReport(Base):
    """Generated scheduled briefings, executive summaries, and alerts."""
    __tablename__ = "intelligence_reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    report_type = Column(String(50), default="daily")  # daily, six_hour, weekly, ad_hoc, alert
    research_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    timezone_name = Column(String(50), default="UTC")
    coverage_period_start = Column(DateTime, nullable=False)
    coverage_period_end = Column(DateTime, nullable=False)
    sources_examined_count = Column(Integer, default=0)
    coverage_gaps_notes = Column(Text, nullable=True)
    
    executive_summary = Column(Text, nullable=False)
    ranked_trending_ids = Column(JSON, default=list)
    ranked_market_ids = Column(JSON, default=list)
    emerging_signals_ids = Column(JSON, default=list)
    key_developments_to_monitor = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class SchedulerJobLog(Base):
    """Audit logs of automated background task executions."""
    __tablename__ = "scheduler_job_logs"

    id = Column(Integer, primary_key=True, index=True)
    job_name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)  # running, success, warning, failed
    articles_ingested = Column(Integer, default=0)
    stories_updated = Column(Integer, default=0)
    details = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
