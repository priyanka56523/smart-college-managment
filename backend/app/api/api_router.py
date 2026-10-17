"""FastAPI API Router providing endpoints for news discovery, verification, scores, and analytics."""
import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.config import settings
from app.models import (
    Story, Article, Claim, Entity, IndustryImpact,
    ScoreBreakdown, SourceRecord, RankingHistory, IntelligenceReport, SchedulerJobLog
)
from app.schemas import (
    StoryListItem, StoryDetail, LeaderboardResponse, AnalyticsResponse,
    IntelligenceReportOut, SystemHealthResponse, APIConnectionTestResult, SourceRecordOut
)
from app.adapters import NewsAPIAdapter, ArxivAdapter, GitHubAdapter, OfficialFeedsAdapter, SearchCorroboratorAdapter
from app.services.llm_service import NVIDIAHostedLLMService
from app.services.reporting_service import ReportingService
from app.services.ingestion_pipeline import run_ingestion_pipeline
from app.services.scheduler_service import platform_scheduler

api_router = APIRouter(prefix="/api")

@api_router.get("/health", response_model=SystemHealthResponse)
async def get_system_health(db: Session = Depends(get_db)):
    """Check platform operational health, scheduler state, and data freshness."""
    last_log = db.query(SchedulerJobLog).order_by(desc(SchedulerJobLog.started_at)).first()
    last_ingestion = last_log.started_at if last_log else None

    # Test integrations asynchronously
    newsapi = NewsAPIAdapter()
    nvidia = NVIDIAHostedLLMService()
    arxiv = ArxivAdapter()
    github = GitHubAdapter()

    n_test = await newsapi.test_connection()
    nv_test = await nvidia.test_connection()
    ar_test = await arxiv.test_connection()
    gh_test = await github.test_connection()

    integrations = [
        APIConnectionTestResult(**n_test),
        APIConnectionTestResult(**nv_test),
        APIConnectionTestResult(**ar_test),
        APIConnectionTestResult(**gh_test),
    ]

    return SystemHealthResponse(
        status="OK",
        timestamp=datetime.datetime.utcnow(),
        version=settings.APP_VERSION,
        database="SQLite (WAL mode ready, PostgreSQL compatible)",
        scheduler_running=platform_scheduler.is_running,
        last_ingestion_time=last_ingestion,
        integrations=integrations
    )

@api_router.get("/config/test-connections", response_model=List[APIConnectionTestResult])
async def test_api_connections():
    """Perform real-time connectivity and constraint checks for all integrated external APIs."""
    results = []
    
    newsapi = NewsAPIAdapter()
    nvidia = NVIDIAHostedLLMService()
    arxiv = ArxivAdapter()
    github = GitHubAdapter()
    corroborator = SearchCorroboratorAdapter()
    official = OfficialFeedsAdapter()

    results.append(APIConnectionTestResult(**(await newsapi.test_connection())))
    results.append(APIConnectionTestResult(**(await nvidia.test_connection())))
    results.append(APIConnectionTestResult(**(await arxiv.test_connection())))
    results.append(APIConnectionTestResult(**(await github.test_connection())))
    results.append(APIConnectionTestResult(**(await official.test_connection())))
    results.append(APIConnectionTestResult(**(await corroborator.test_connection())))

    return results

@api_router.get("/stories", response_model=List[StoryListItem])
def list_stories(
    search: Optional[str] = Query(None, description="Keyword search in headline or summary"),
    verification_status: Optional[str] = Query(None, description="VERIFIED, CORROBORATED, PARTIALLY VERIFIED, UNVERIFIED, DISPUTED, FALSE OR DEBUNKED"),
    industry: Optional[str] = Query(None, description="Filter by affected industry sector"),
    entity: Optional[str] = Query(None, description="Filter by person or company name"),
    is_emerging_signal: Optional[bool] = Query(None, description="Filter emerging speculative signals vs confirmed stories"),
    sort_by: str = Query("trending", description="trending, market, or date"),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Retrieve canonical AI stories with multi-dimensional filtering."""
    query = db.query(Story)

    if is_emerging_signal is not None:
        query = query.filter(Story.is_emerging_signal == is_emerging_signal)

    if verification_status:
        query = query.filter(Story.verification_status == verification_status)

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Story.title.ilike(search_pattern)) | (Story.summary.ilike(search_pattern))
        )

    if industry:
        query = query.join(Story.industry_impacts).filter(IndustryImpact.industry_name.ilike(f"%{industry}%"))

    if entity:
        query = query.join(Story.entities).filter(Entity.name.ilike(f"%{entity}%"))

    # Sorting
    if sort_by == "market":
        query = query.order_by(desc(Story.market_importance_score))
    elif sort_by == "date":
        query = query.order_by(desc(Story.event_date))
    else:
        query = query.order_by(desc(Story.trending_score))

    return query.limit(limit).all()

@api_router.get("/stories/{story_id}", response_model=StoryDetail)
def get_story_detail(story_id: int, db: Session = Depends(get_db)):
    """Retrieve in-depth story dossier with claims, evidence, score breakdowns, and ranking history."""
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story intelligence record not found")
    return story

@api_router.get("/leaderboards", response_model=LeaderboardResponse)
def get_leaderboards(db: Session = Depends(get_db)):
    """Fetch dual independent leaderboards (Trending & Market Importance) and isolated emerging signals."""
    trending_stories = db.query(Story).filter(
        Story.is_emerging_signal == False
    ).order_by(desc(Story.trending_score)).limit(10).all()

    market_stories = db.query(Story).filter(
        Story.is_emerging_signal == False
    ).order_by(desc(Story.market_importance_score)).limit(10).all()

    emerging_signals = db.query(Story).filter(
        Story.is_emerging_signal == True
    ).order_by(desc(Story.market_importance_score)).limit(10).all()

    methodology = {
        "scoring_version": "v1.0",
        "trending_weights": {
            "news_coverage_growth": "25 pts",
            "public_discussion": "25 pts",
            "search_interest": "20 pts",
            "developer_research_activity": "15 pts",
            "recency_acceleration": "15 pts"
        },
        "market_weights": {
            "market_economic_impact": "25 pts",
            "technical_significance": "20 pts",
            "trend_momentum": "15 pts",
            "industry_disruption": "15 pts",
            "strategic_importance": "10 pts",
            "evidence_strength": "10 pts",
            "time_sensitivity": "5 pts"
        },
        "isolation_rule": "High-impact stories with UNVERIFIED, PARTIALLY VERIFIED, or DISPUTED status are segregated into Emerging Signals to preserve confirmed leaderboard integrity."
    }

    return LeaderboardResponse(
        trending_leaderboard=trending_stories,
        market_leaderboard=market_stories,
        emerging_signals=emerging_signals,
        scoring_methodology=methodology
    )

@api_router.get("/analytics", response_model=AnalyticsResponse)
def get_analytics(db: Session = Depends(get_db)):
    """Compute aggregate trend analytics, industry exposure distributions, and data freshness."""
    total_stories = db.query(Story).count()
    total_articles = db.query(Article).count()

    # Verification counts
    v_counts = {}
    for status in ["VERIFIED", "CORROBORATED", "PARTIALLY VERIFIED", "UNVERIFIED", "DISPUTED", "FALSE OR DEBUNKED"]:
        v_counts[status] = db.query(Story).filter(Story.verification_status == status).count()

    # Trending label counts
    l_counts = {}
    for label in ["TRENDING NOW", "EMERGING", "PERSISTENT", "HIGH IMPORTANCE BUT NOT TRENDING"]:
        l_counts[label] = db.query(Story).filter(Story.trending_label == label).count()

    # Top industries exposed
    from sqlalchemy import func
    industry_stats = db.query(
        IndustryImpact.industry_name,
        func.count(IndustryImpact.id).label("count")
    ).group_by(IndustryImpact.industry_name).order_by(desc("count")).all()

    top_industries = [{"industry": name, "count": cnt} for name, cnt in industry_stats]

    # Top entities
    entity_stats = db.query(
        Entity.name,
        Entity.entity_type,
        Entity.ticker_symbol,
        func.count(Entity.id).label("count")
    ).group_by(Entity.name).order_by(desc("count")).limit(10).all()

    top_entities = [
        {"name": name, "entity_type": etype, "ticker": ticker, "occurrences": cnt}
        for name, etype, ticker, cnt in entity_stats
    ]

    last_story = db.query(Story).order_by(desc(Story.last_checked_at)).first()

    return AnalyticsResponse(
        total_stories=total_stories,
        total_articles=total_articles,
        verification_counts=v_counts,
        trending_labels_counts=l_counts,
        top_industries_exposed=top_industries,
        top_entities=top_entities,
        score_distribution={
            "high_market_impact_count": db.query(Story).filter(Story.market_importance_score >= 80).count(),
            "high_trending_count": db.query(Story).filter(Story.trending_score >= 80).count(),
            "emerging_signals_count": db.query(Story).filter(Story.is_emerging_signal == True).count()
        },
        data_freshness={
            "last_checked": last_story.last_checked_at.isoformat() if last_story else None,
            "status": "fresh"
        }
    )

@api_router.get("/sources", response_model=List[SourceRecordOut])
def list_sources(
    source_type: Optional[str] = Query(None),
    access_status: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """Retrieve clickable source register with verification probe access status and supported claims."""
    query = db.query(SourceRecord)
    if source_type:
        query = query.filter(SourceRecord.source_type == source_type)
    if access_status:
        query = query.filter(SourceRecord.access_status == access_status)
    return query.order_by(desc(SourceRecord.created_at)).limit(limit).all()

@api_router.get("/reports", response_model=List[IntelligenceReportOut])
def list_reports(db: Session = Depends(get_db)):
    """List historical executive intelligence briefings."""
    return db.query(IntelligenceReport).order_by(desc(IntelligenceReport.created_at)).all()

@api_router.get("/reports/{report_id}", response_model=IntelligenceReportOut)
def get_report(report_id: int, db: Session = Depends(get_db)):
    """Fetch specific executive briefing."""
    rep = db.query(IntelligenceReport).filter(IntelligenceReport.id == report_id).first()
    if not rep:
        raise HTTPException(status_code=404, detail="Intelligence report not found")
    return rep

@api_router.post("/reports/generate", response_model=IntelligenceReportOut)
def generate_report(
    report_type: str = Query("daily", description="daily, six_hour, weekly, or ad_hoc"),
    db: Session = Depends(get_db)
):
    """Generate an on-demand executive intelligence briefing with verified evidence and rankings."""
    report = ReportingService.generate_briefing(db, report_type=report_type)
    return report

@api_router.post("/ingest")
async def trigger_manual_ingestion(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Trigger an immediate live ingestion cycle across all active source adapters."""
    res = await run_ingestion_pipeline(db)
    return res
