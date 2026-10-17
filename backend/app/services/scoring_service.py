"""Deterministic Trending and Market Importance Scoring Engine."""
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, List
from app.adapters.base import RawArticleData

logger = logging.getLogger(__name__)

SCORING_VERSION = "v1.0"

class ScoringEngine:
    """Calculates independent Trending and Market Importance scores with transparent breakdowns."""

    @classmethod
    def calculate_trending_score(
        cls,
        articles: List[RawArticleData],
        event_date: datetime,
        verification_status: str,
        developer_signals: Dict[str, Any]
    ) -> Tuple[float, str, Dict[str, float], str]:
        """
        Calculates Trending Score (0 - 100) using:
        1. Growth in independent news coverage: max 25 pts
        2. Public discussion and engagement momentum: max 25 pts
        3. Search-interest growth: max 20 pts
        4. Relevant developer & research activity: max 15 pts
        5. Recency and acceleration: max 15 pts
        """
        # Component 1: News coverage growth (distinct publishers)
        publishers = {a.publisher for a in articles if a.publisher}
        num_pubs = len(publishers)
        if num_pubs >= 6:
            c1_news = 25.0
        elif num_pubs >= 4:
            c1_news = 20.0
        elif num_pubs >= 2:
            c1_news = 14.0
        elif num_pubs == 1:
            c1_news = 8.0
        else:
            c1_news = 4.0

        # Component 2: Public discussion & engagement momentum
        # Derived from article metadata or estimated based on syndicated breadth
        has_social_signal = any(a.metadata.get("stars", 0) > 100 for a in articles) or num_pubs > 3
        if has_social_signal and num_pubs >= 4:
            c2_discussion = 23.0
        elif has_social_signal or num_pubs >= 2:
            c2_discussion = 16.0
        else:
            c2_discussion = 8.0

        # Component 3: Search interest growth
        # Normalized based on presence across major technology beats
        c3_search = 15.0 if num_pubs >= 3 else 9.0

        # Component 4: Developer & research activity (arXiv/GitHub/code presence)
        has_github = any(a.provider_id == "github" or "github.com" in (a.canonical_url or "") for a in articles)
        has_arxiv = any(a.provider_id == "arxiv" or "arxiv.org" in (a.canonical_url or "") for a in articles)
        if has_github and has_arxiv:
            c4_dev = 15.0
        elif has_github or has_arxiv:
            c4_dev = 11.0
        else:
            c4_dev = 5.0

        # Component 5: Recency & acceleration
        now = datetime.utcnow()
        age_hours = (now - event_date).total_seconds() / 3600.0 if event_date else 48.0
        if age_hours <= 12:
            c5_recency = 15.0
        elif age_hours <= 24:
            c5_recency = 12.0
        elif age_hours <= 72:
            c5_recency = 8.0
        elif age_hours <= 168:
            c5_recency = 5.0
        else:
            c5_recency = 2.0

        total_score = min(100.0, round(c1_news + c2_discussion + c3_search + c4_dev + c5_recency, 1))

        # Classification
        if total_score >= 70 and age_hours <= 48:
            label = "TRENDING NOW"
        elif total_score >= 50 and age_hours <= 72:
            label = "EMERGING"
        elif total_score >= 60 and age_hours > 72:
            label = "PERSISTENT"
        else:
            label = "HIGH IMPORTANCE BUT NOT TRENDING" if total_score < 50 else "EMERGING"

        breakdown = {
            "news_coverage_growth": c1_news,
            "public_discussion": c2_discussion,
            "search_interest": c3_search,
            "developer_research_activity": c4_dev,
            "recency_acceleration": c5_recency,
            "trending_total": total_score
        }

        rationale = (
            f"Score {total_score}/100: Driven by coverage across {num_pubs} distinct outlets, "
            f"active developer repository activity ({'detected' if has_github or has_arxiv else 'limited'}), "
            f"and an event age of {age_hours:.1f} hours."
        )

        return total_score, label, breakdown, rationale

    @classmethod
    def calculate_market_importance_score(
        cls,
        articles: List[RawArticleData],
        entities: List[Dict[str, Any]],
        industry_impacts: List[Dict[str, Any]],
        verification_status: str,
        trending_score: float
    ) -> Tuple[float, Dict[str, float], str, bool]:
        """
        Calculates Market Importance Score (0 - 100) using:
        1. Market and economic impact: 25 pts
        2. Technical or scientific significance: 20 pts
        3. Trend momentum: 15 pts
        4. Industry disruption potential: 15 pts
        5. Strategic importance: 10 pts
        6. Evidence strength: 10 pts
        7. Time sensitivity: 5 pts
        """
        # Component 1: Market and economic impact (25 pts)
        has_public_companies = any(e.get("ticker_symbol") for e in entities)
        has_high_impact = any(i.get("impact_magnitude") in ["high", "transformative"] for i in industry_impacts)
        if has_public_companies and has_high_impact:
            c1_econ = 24.0
        elif has_high_impact or has_public_companies:
            c1_econ = 18.0
        else:
            c1_econ = 10.0

        # Component 2: Technical or scientific significance (20 pts)
        has_arxiv = any("arxiv.org" in (a.canonical_url or "") or a.provider_id == "arxiv" for a in articles)
        is_breakthrough_topic = any(
            any(kw in (a.headline or "").lower() for kw in ["reasoning", "breakthrough", "architecture", "frontier", "billion", "cluster"])
            for a in articles
        )
        if has_arxiv and is_breakthrough_topic:
            c2_tech = 19.0
        elif is_breakthrough_topic or has_arxiv:
            c2_tech = 14.0
        else:
            c2_tech = 8.0

        # Component 3: Trend momentum (15 pts) - proportional to trending score
        c3_momentum = round((trending_score / 100.0) * 15.0, 1)

        # Component 4: Industry disruption potential (15 pts)
        sectors_count = len(industry_impacts)
        if sectors_count >= 3 or any(i.get("impact_magnitude") == "transformative" for i in industry_impacts):
            c4_disruption = 14.0
        elif sectors_count >= 1:
            c4_disruption = 10.0
        else:
            c4_disruption = 5.0

        # Component 5: Strategic importance (geopolitical / supply chain / sovereign AI) (10 pts)
        all_text = " ".join([f"{a.headline} {a.description or ''}" for a in articles]).lower()
        if any(w in all_text for w in ["energy", "data center", "national security", "grid", "sovereign", "export", "regulation"]):
            c5_strat = 9.0
        else:
            c5_strat = 6.0

        # Component 6: Evidence strength (10 pts)
        if verification_status == "VERIFIED":
            c6_evidence = 10.0
        elif verification_status == "CORROBORATED":
            c6_evidence = 8.0
        elif verification_status == "PARTIALLY VERIFIED":
            c6_evidence = 6.0
        elif verification_status == "DISPUTED":
            c6_evidence = 3.0
        elif verification_status == "FALSE OR DEBUNKED":
            c6_evidence = 0.0
        else:
            c6_evidence = 4.0

        # Component 7: Time sensitivity (immediate market positioning) (5 pts)
        c7_time = 4.5 if any(i.get("time_horizon") == "immediate" for i in industry_impacts) else 3.0

        total_market = min(100.0, round(
            c1_econ + c2_tech + c3_momentum + c4_disruption + c5_strat + c6_evidence + c7_time, 1
        ))

        # Separate emerging signal flag: high impact but unverified or preliminary
        is_emerging_signal = total_market >= 65.0 and verification_status in ["UNVERIFIED", "PARTIALLY VERIFIED", "DISPUTED"]

        breakdown = {
            "market_economic_impact": c1_econ,
            "technical_significance": c2_tech,
            "trend_momentum": c3_momentum,
            "industry_disruption": c4_disruption,
            "strategic_importance": c5_strat,
            "evidence_strength": c6_evidence,
            "time_sensitivity": c7_time,
            "market_total": total_market
        }

        rationale = (
            f"Market Score {total_market}/100: Reflects economic impact ({c1_econ}/25), "
            f"technological significance ({c2_tech}/20), and industry exposure across {sectors_count} sectors "
            f"with evidence validation rated as {verification_status} ({c6_evidence}/10)."
        )

        return total_market, breakdown, rationale, is_emerging_signal
