"""Ingestion and Orchestration Pipeline connecting discovery, verification, and scoring."""
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models import (
    Article, Story, Claim, Entity, IndustryImpact,
    ScoreBreakdown, SourceRecord, RankingHistory, SchedulerJobLog
)
from app.adapters import (
    NewsAPIAdapter, ArxivAdapter, GitHubAdapter,
    OfficialFeedsAdapter, SearchCorroboratorAdapter, RawArticleData
)
from app.services.deduplication import cluster_articles_into_stories, clean_text
from app.services.llm_service import NVIDIAHostedLLMService
from app.services.verification_service import VerificationEngine
from app.services.scoring_service import ScoringEngine, SCORING_VERSION
from app.services.impact_service import IndustryImpactEngine
from app.services.seed_data import BASELINE_STORIES

logger = logging.getLogger(__name__)

def seed_baseline_if_empty(db: Session):
    """Seed the database with rich factual baseline data if no stories exist."""
    count = db.query(Story).count()
    if count > 0:
        return

    logger.info("Initializing database with baseline AI intelligence records...")
    for data in BASELINE_STORIES:
        story = Story(
            title=data["title"],
            summary=data["summary"],
            what_happened=data.get("what_happened"),
            what_is_new=data.get("what_is_new"),
            first_discovered_at=datetime.utcnow(),
            event_date=data["event_date"],
            last_checked_at=datetime.utcnow(),
            verification_status=data["verification_status"],
            verification_rationale=data["verification_rationale"],
            verification_timestamp=datetime.utcnow(),
            trending_score=data["trending_score"],
            trending_label=data["trending_label"],
            market_importance_score=data["market_importance_score"],
            trending_rank=data.get("trending_rank"),
            market_rank=data.get("market_rank"),
            is_emerging_signal=data.get("is_emerging_signal", False),
            next_milestones=data.get("next_milestones")
        )
        db.add(story)
        db.flush()

        # Add Articles
        for art in data.get("articles", []):
            article_record = Article(
                provider_id=art["provider_id"],
                canonical_url=art["canonical_url"],
                original_url=art["original_url"],
                headline=art["headline"],
                description=art.get("description"),
                publisher=art.get("publisher"),
                author=art.get("author"),
                published_at=art.get("published_at"),
                story_id=story.id
            )
            db.add(article_record)

        # Add Claims
        for cl in data.get("claims", []):
            claim_record = Claim(
                story_id=story.id,
                claim_text=cl["claim_text"],
                claim_type=cl.get("claim_type", "central_claim"),
                verification_status=cl.get("verification_status", "UNVERIFIED"),
                supporting_evidence=cl.get("supporting_evidence"),
                conflicting_evidence=cl.get("conflicting_evidence"),
                missing_evidence=cl.get("missing_evidence"),
                evidence_urls=cl.get("evidence_urls", [])
            )
            db.add(claim_record)

        # Add Entities
        for ent in data.get("entities", []):
            ent_record = Entity(
                story_id=story.id,
                name=ent["name"],
                entity_type=ent["entity_type"],
                role=ent.get("role"),
                organization=ent.get("organization"),
                story_role=ent.get("story_role", "announcer"),
                direct_involvement=ent.get("direct_involvement"),
                ticker_symbol=ent.get("ticker_symbol"),
                exchange=ent.get("exchange"),
                is_confirmed_exposure=ent.get("is_confirmed_exposure", True)
            )
            db.add(ent_record)

        # Add Impacts
        for imp in data.get("industry_impacts", []):
            imp_record = IndustryImpact(
                story_id=story.id,
                industry_name=imp["industry_name"],
                impact_direction=imp["impact_direction"],
                impact_magnitude=imp["impact_magnitude"],
                time_horizon=imp["time_horizon"],
                mechanism=imp.get("mechanism"),
                potential_beneficiaries=imp.get("potential_beneficiaries"),
                disrupted_models=imp.get("disrupted_models"),
                workforce_task_exposure=imp.get("workforce_task_exposure"),
                workforce_augmentation_vs_displacement=imp.get("workforce_augmentation_vs_displacement"),
                confidence_level=imp.get("confidence_level", "medium")
            )
            db.add(imp_record)

        # Add Score Breakdown
        sb = data.get("score_breakdown", {})
        score_bd = ScoreBreakdown(
            story_id=story.id,
            news_coverage_growth=sb.get("news_coverage_growth", 0.0),
            public_discussion=sb.get("public_discussion", 0.0),
            search_interest=sb.get("search_interest", 0.0),
            developer_research_activity=sb.get("developer_research_activity", 0.0),
            recency_acceleration=sb.get("recency_acceleration", 0.0),
            trending_total=sb.get("trending_total", story.trending_score),
            market_economic_impact=sb.get("market_economic_impact", 0.0),
            technical_significance=sb.get("technical_significance", 0.0),
            trend_momentum=sb.get("trend_momentum", 0.0),
            industry_disruption=sb.get("industry_disruption", 0.0),
            strategic_importance=sb.get("strategic_importance", 0.0),
            evidence_strength=sb.get("evidence_strength", 0.0),
            time_sensitivity=sb.get("time_sensitivity", 0.0),
            market_total=sb.get("market_total", story.market_importance_score),
            scoring_rationale=sb.get("scoring_rationale", "Baseline rubric assessment"),
            scoring_version=sb.get("scoring_version", SCORING_VERSION)
        )
        db.add(score_bd)

        # Add Sources
        for src in data.get("sources", []):
            src_record = SourceRecord(
                story_id=story.id,
                title=src["title"],
                publisher=src.get("publisher"),
                url=src["url"],
                source_type=src.get("source_type", "independent_news"),
                access_status=src.get("access_status", "accessed_and_verified"),
                claims_supported=src.get("claims_supported")
            )
            db.add(src_record)

        # Add Ranking History entry
        rank_hist = RankingHistory(
            story_id=story.id,
            trending_rank=story.trending_rank,
            market_rank=story.market_rank,
            trending_score=story.trending_score,
            market_importance_score=story.market_importance_score,
            verification_status=story.verification_status,
            recorded_at=datetime.utcnow()
        )
        db.add(rank_hist)

    db.commit()
    logger.info("Baseline seed data successfully committed.")

async def run_ingestion_pipeline(db: Session) -> Dict[str, Any]:
    """Execute full ingestion, deduplication, LLM analysis, verification, and scoring."""
    job_log = SchedulerJobLog(
        job_name="full_ingestion_cycle",
        status="running",
        started_at=datetime.utcnow()
    )
    db.add(job_log)
    db.commit()

    all_raw_articles: List[RawArticleData] = []
    
    # 1. Fetch from Adapters
    newsapi_adapter = NewsAPIAdapter()
    arxiv_adapter = ArxivAdapter()
    github_adapter = GitHubAdapter()
    official_adapter = OfficialFeedsAdapter()
    corroborator = SearchCorroboratorAdapter()
    llm_service = NVIDIAHostedLLMService()

    try:
        # Collect articles
        newsapi_articles = await newsapi_adapter.fetch_articles(limit=10)
        arxiv_articles = await arxiv_adapter.fetch_articles(limit=6)
        github_articles = await github_adapter.fetch_articles(limit=5)
        official_articles = await official_adapter.fetch_articles(limit=6)

        all_raw_articles.extend(newsapi_articles)
        all_raw_articles.extend(arxiv_articles)
        all_raw_articles.extend(github_articles)
        all_raw_articles.extend(official_articles)

        job_log.articles_ingested = len(all_raw_articles)

        # 2. Deduplication and Event Clustering
        clusters = cluster_articles_into_stories(all_raw_articles)
        updated_stories_count = 0

        existing_urls = {a.canonical_url for a in db.query(Article.canonical_url).all()}

        for cluster in clusters:
            if not cluster:
                continue

            # Check if all articles in cluster already exist
            cluster_urls = {a.canonical_url for a in cluster}
            if cluster_urls.issubset(existing_urls):
                continue

            lead_article = cluster[0]
            cluster_text = " ".join([f"{a.headline}. {a.description or ''} {a.content or ''}" for a in cluster])
            sources_summary = ", ".join({a.publisher or a.provider_id for a in cluster})

            # 3. LLM Analysis
            analysis = await llm_service.analyze_story(
                headline=lead_article.headline,
                articles_text=cluster_text,
                sources_summary=sources_summary
            )

            # 4. Probe URLs for Verification
            probed_sources = []
            for art in cluster:
                probe_res = await corroborator.verify_url_accessibility(art.canonical_url)
                probed_sources.append(probe_res)

            # 5. Verification Engine
            claims_dicts = [c.model_dump() for c in analysis.claims]
            v_status, v_rationale, ev_summary = VerificationEngine.evaluate(
                articles=cluster,
                suggested_llm_status=analysis.suggested_verification_status,
                claims=claims_dicts,
                probed_sources=probed_sources
            )

            # 6. Scoring Engine
            t_score, t_label, t_breakdown, t_rationale = ScoringEngine.calculate_trending_score(
                articles=cluster,
                event_date=lead_article.published_at or datetime.utcnow(),
                verification_status=v_status,
                developer_signals=ev_summary
            )

            entities_dicts = [e.model_dump() for e in analysis.entities]
            impacts_dicts = [i.model_dump() for i in analysis.industry_impacts]

            # Enrich impacts and tickers
            enriched_impacts, enriched_entities = IndustryImpactEngine.enrich_impacts(
                text=cluster_text,
                extracted_impacts=impacts_dicts,
                extracted_entities=entities_dicts
            )

            m_score, m_breakdown, m_rationale, is_emerging = ScoringEngine.calculate_market_importance_score(
                articles=cluster,
                entities=enriched_entities,
                industry_impacts=enriched_impacts,
                verification_status=v_status,
                trending_score=t_score
            )

            # Persist canonical Story
            story = Story(
                title=analysis.title or lead_article.headline,
                summary=analysis.summary,
                what_happened=analysis.what_happened,
                what_is_new=analysis.what_is_new,
                first_discovered_at=datetime.utcnow(),
                event_date=lead_article.published_at or datetime.utcnow(),
                last_checked_at=datetime.utcnow(),
                verification_status=v_status,
                verification_rationale=v_rationale,
                verification_timestamp=datetime.utcnow(),
                trending_score=t_score,
                trending_label=t_label,
                market_importance_score=m_score,
                is_emerging_signal=is_emerging,
                next_milestones=analysis.next_milestones_to_monitor
            )
            db.add(story)
            db.flush()

            # Persist Articles
            for art in cluster:
                art_rec = Article(
                    provider_id=art.provider_id,
                    provider_item_id=art.provider_item_id,
                    canonical_url=art.canonical_url,
                    original_url=art.original_url,
                    headline=art.headline,
                    description=art.description,
                    content=art.content,
                    author=art.author,
                    publisher=art.publisher,
                    published_at=art.published_at,
                    language=art.language,
                    retrieval_status=art.retrieval_status,
                    story_id=story.id
                )
                db.add(art_rec)
                existing_urls.add(art.canonical_url)

            # Persist Claims
            for cl in analysis.claims:
                claim_rec = Claim(
                    story_id=story.id,
                    claim_text=cl.claim_text,
                    claim_type=cl.claim_type,
                    verification_status=v_status,
                    supporting_evidence="; ".join(cl.supporting_facts) if cl.supporting_facts else None,
                    missing_evidence=cl.missing_evidence,
                    evidence_urls=[art.canonical_url for art in cluster[:2]]
                )
                db.add(claim_rec)

            # Persist Entities
            for ent in enriched_entities:
                ent_rec = Entity(
                    story_id=story.id,
                    name=ent["name"],
                    entity_type=ent["entity_type"],
                    role=ent.get("role"),
                    organization=ent.get("organization"),
                    story_role=ent.get("story_role", "announcer"),
                    direct_involvement=ent.get("direct_involvement"),
                    ticker_symbol=ent.get("ticker_symbol"),
                    exchange=ent.get("exchange"),
                    is_confirmed_exposure=ent.get("is_confirmed_exposure", True)
                )
                db.add(ent_rec)

            # Persist Industry Impacts
            for imp in enriched_impacts:
                imp_rec = IndustryImpact(
                    story_id=story.id,
                    industry_name=imp["industry_name"],
                    impact_direction=imp.get("impact_direction", "positive"),
                    impact_magnitude=imp.get("impact_magnitude", "medium"),
                    time_horizon=imp.get("time_horizon", "near_term"),
                    mechanism=imp.get("mechanism"),
                    potential_beneficiaries=imp.get("potential_beneficiaries"),
                    disrupted_models=imp.get("disrupted_business_models"),
                    workforce_task_exposure=imp.get("workforce_task_exposure"),
                    workforce_augmentation_vs_displacement=imp.get("workforce_augmentation_vs_displacement"),
                    confidence_level=imp.get("confidence_level", "medium")
                )
                db.add(imp_rec)

            # Persist Score Breakdown
            score_rec = ScoreBreakdown(
                story_id=story.id,
                news_coverage_growth=t_breakdown["news_coverage_growth"],
                public_discussion=t_breakdown["public_discussion"],
                search_interest=t_breakdown["search_interest"],
                developer_research_activity=t_breakdown["developer_research_activity"],
                recency_acceleration=t_breakdown["recency_acceleration"],
                trending_total=t_score,
                market_economic_impact=m_breakdown["market_economic_impact"],
                technical_significance=m_breakdown["technical_significance"],
                trend_momentum=m_breakdown["trend_momentum"],
                industry_disruption=m_breakdown["industry_disruption"],
                strategic_importance=m_breakdown["strategic_importance"],
                evidence_strength=m_breakdown["evidence_strength"],
                time_sensitivity=m_breakdown["time_sensitivity"],
                market_total=m_score,
                scoring_rationale=f"{t_rationale} | {m_rationale}",
                scoring_version=SCORING_VERSION,
                coverage_limitation_notes="Normalized over available API signals."
            )
            db.add(score_rec)

            # Persist Sources
            for art in cluster:
                domain_type = "independent_news"
                if art.provider_id == "arxiv":
                    domain_type = "research_paper"
                elif art.provider_id == "github":
                    domain_type = "code_repository"
                elif art.provider_id == "official_feed":
                    domain_type = "official_announcement"

                src_rec = SourceRecord(
                    story_id=story.id,
                    title=art.headline,
                    publisher=art.publisher,
                    url=art.canonical_url,
                    source_type=domain_type,
                    access_status="accessed_and_verified",
                    claims_supported="Primary reporting cited in extraction"
                )
                db.add(src_rec)

            updated_stories_count += 1

        # 7. Recompute Global Leaderboard Ranks
        _recalculate_leaderboard_ranks(db)

        job_log.status = "success"
        job_log.stories_updated = updated_stories_count
        job_log.finished_at = datetime.utcnow()
        job_log.details = f"Processed {len(all_raw_articles)} articles, created/updated {updated_stories_count} canonical stories."
        db.commit()

        return {
            "status": "success",
            "articles_fetched": len(all_raw_articles),
            "stories_updated": updated_stories_count,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Ingestion pipeline execution failure: {e}", exc_info=True)
        job_log.status = "failed"
        job_log.details = f"Error: {str(e)}"
        job_log.finished_at = datetime.utcnow()
        db.commit()
        return {
            "status": "error",
            "message": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

def _recalculate_leaderboard_ranks(db: Session):
    """Update trending_rank and market_rank for non-emerging confirmed stories."""
    # Trending leaderboard ranks
    trending_sorted = db.query(Story).filter(
        Story.is_emerging_signal == False
    ).order_by(Story.trending_score.desc()).all()

    for idx, s in enumerate(trending_sorted, 1):
        s.trending_rank = idx

    # Market leaderboard ranks
    market_sorted = db.query(Story).filter(
        Story.is_emerging_signal == False
    ).order_by(Story.market_importance_score.desc()).all()

    for idx, s in enumerate(market_sorted, 1):
        s.market_rank = idx
        # Add to ranking history
        hist = RankingHistory(
            story_id=s.id,
            trending_rank=s.trending_rank,
            market_rank=s.market_rank,
            trending_score=s.trending_score,
            market_importance_score=s.market_importance_score,
            verification_status=s.verification_status,
            recorded_at=datetime.utcnow()
        )
        db.add(hist)

    db.commit()
