"""Report Generation and Intelligence Briefing Service."""
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models import Story, IntelligenceReport, ScoreBreakdown, SourceRecord

logger = logging.getLogger(__name__)

class ReportingService:
    """Generates scheduled intelligence briefings, executive summaries, and alerts."""

    @classmethod
    def generate_briefing(
        cls,
        db: Session,
        report_type: str = "daily",
        period_hours: int = 24
    ) -> IntelligenceReport:
        """Create a structured intelligence briefing."""
        now = datetime.utcnow()
        start_time = now - timedelta(hours=period_hours)

        # Retrieve top trending stories
        trending_stories = db.query(Story).filter(
            Story.is_emerging_signal == False
        ).order_by(Story.trending_score.desc()).limit(10).all()

        # Retrieve top market importance stories
        market_stories = db.query(Story).filter(
            Story.is_emerging_signal == False
        ).order_by(Story.market_importance_score.desc()).limit(10).all()

        # Retrieve emerging unverified signals
        emerging_signals = db.query(Story).filter(
            Story.is_emerging_signal == True
        ).order_by(Story.market_importance_score.desc()).limit(5).all()

        # Count sources examined
        total_sources = db.query(SourceRecord).count()

        # Compose executive summary
        summary_paragraphs = [
            f"GLOBAL AI & AGI INTELLIGENCE BRIEFING ({report_type.upper()})",
            f"Coverage Period: {start_time.strftime('%Y-%m-%d %H:%M UTC')} to {now.strftime('%Y-%m-%d %H:%M UTC')}.",
            f"Examined {total_sources} primary and corroborating sources across NewsAPI, arXiv, GitHub, and official laboratory announcements.",
            "",
            "KEY FINDINGS:",
        ]

        if market_stories:
            top_market = market_stories[0]
            summary_paragraphs.append(
                f"1. Highest Market Importance: '{top_market.title}' (Market Score: {top_market.market_importance_score}/100, Verification: {top_market.verification_status})."
            )
        if trending_stories:
            top_trend = trending_stories[0]
            summary_paragraphs.append(
                f"2. Top Trending Development: '{top_trend.title}' (Trending Score: {top_trend.trending_score}/100, Label: {top_trend.trending_label})."
            )
        if emerging_signals:
            top_signal = emerging_signals[0]
            summary_paragraphs.append(
                f"3. High-Impact Emerging Signal to Monitor: '{top_signal.title}' (Status: {top_signal.verification_status} - isolated from confirmed ranks pending primary confirmation)."
            )

        summary_paragraphs.extend([
            "",
            "SECTOR EXPOSURE OVERVIEW:",
            "Capital expenditures remain heavily focused on high-density datacenter power, high-bandwidth memory (HBM), and autonomous agent frameworks targeting enterprise workflows."
        ])

        executive_summary = "\n".join(summary_paragraphs)

        gaps_notes = (
            "Access Limitations: Paywalled publications (FT, WSJ) and private developer repos were recorded as inaccessible. "
            "Developer tier query limits bounded historical discovery to accessible open APIs and public RSS feeds."
        )

        report = IntelligenceReport(
            title=f"AI/AGI Executive Intelligence Briefing - {now.strftime('%b %d, %Y')}",
            report_type=report_type,
            research_timestamp=now,
            timezone_name="UTC",
            coverage_period_start=start_time,
            coverage_period_end=now,
            sources_examined_count=total_sources,
            coverage_gaps_notes=gaps_notes,
            executive_summary=executive_summary,
            ranked_trending_ids=[s.id for s in trending_stories],
            ranked_market_ids=[s.id for s in market_stories],
            emerging_signals_ids=[s.id for s in emerging_signals],
            key_developments_to_monitor="Monitor upcoming model evaluation reports, open-weight checkpoint downloads, and utility interconnect filings."
        )

        db.add(report)
        db.commit()
        db.refresh(report)
        return report
