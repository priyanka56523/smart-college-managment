"""Tests for Trending Score and Market Importance Score calculations."""
from datetime import datetime, timedelta
from app.adapters.base import RawArticleData
from app.services.scoring_service import ScoringEngine

def test_trending_score_weights_and_bounds():
    now = datetime.utcnow()
    articles = [
        RawArticleData(
            provider_id="newsapi", provider_item_id="1", canonical_url="https://a.com/1",
            original_url="https://a.com/1", headline="OpenAI announces o1 reasoning model",
            description="", content="", author="A", publisher="Reuters", published_at=now - timedelta(hours=5),
            metadata={"stars": 500}
        ),
        RawArticleData(
            provider_id="arxiv", provider_item_id="2", canonical_url="https://arxiv.org/abs/2409.12345",
            original_url="https://arxiv.org/abs/2409.12345", headline="Learning to Reason with LLMs",
            description="", content="", author="B", publisher="arXiv.org", published_at=now - timedelta(hours=6)
        ),
        RawArticleData(
            provider_id="github", provider_item_id="3", canonical_url="https://github.com/openai/evals",
            original_url="https://github.com/openai/evals", headline="OpenAI Evals Framework",
            description="", content="", author="C", publisher="GitHub", published_at=now - timedelta(hours=8)
        )
    ]

    score, label, breakdown, rationale = ScoringEngine.calculate_trending_score(
        articles=articles,
        event_date=now - timedelta(hours=5),
        verification_status="VERIFIED",
        developer_signals={"has_github_code": True, "has_arxiv_paper": True}
    )

    assert 0.0 <= score <= 100.0
    assert label in ["TRENDING NOW", "EMERGING", "PERSISTENT", "HIGH IMPORTANCE BUT NOT TRENDING"]
    assert "news_coverage_growth" in breakdown
    assert "public_discussion" in breakdown
    assert "search_interest" in breakdown
    assert "developer_research_activity" in breakdown
    assert "recency_acceleration" in breakdown
    assert round(sum([
        breakdown["news_coverage_growth"],
        breakdown["public_discussion"],
        breakdown["search_interest"],
        breakdown["developer_research_activity"],
        breakdown["recency_acceleration"]
    ]), 1) == score

def test_market_importance_score_and_isolation():
    articles = [
        RawArticleData(
            provider_id="newsapi", provider_item_id="1", canonical_url="https://tech.com/1",
            original_url="https://tech.com/1", headline="NVIDIA Blackwell GPUs Enter Mass Production",
            description="", content="", author="", publisher="Bloomberg", published_at=datetime.utcnow()
        )
    ]
    entities = [
        {"name": "NVIDIA", "ticker_symbol": "NVDA", "is_confirmed_exposure": True}
    ]
    impacts = [
        {"industry_name": "Semiconductors/Hardware", "impact_magnitude": "transformative", "time_horizon": "immediate"}
    ]

    score, breakdown, rationale, is_emerging = ScoringEngine.calculate_market_importance_score(
        articles=articles,
        entities=entities,
        industry_impacts=impacts,
        verification_status="VERIFIED",
        trending_score=85.0
    )

    assert 0.0 <= score <= 100.0
    assert not is_emerging  # VERIFIED high score is NOT isolated into emerging signals
    assert breakdown["market_economic_impact"] > 0
    assert breakdown["technical_significance"] > 0
    assert breakdown["industry_disruption"] > 0

def test_unverified_high_impact_isolated_as_emerging_signal():
    articles = [
        RawArticleData(
            provider_id="newsapi", provider_item_id="1", canonical_url="https://rumors.com/1",
            original_url="https://rumors.com/1", headline="Anonymous lab claims recursive AGI superintelligence",
            description="", content="", author="", publisher="Blog", published_at=datetime.utcnow()
        )
    ]
    entities = []
    impacts = [
        {"industry_name": "Software/SaaS", "impact_magnitude": "transformative", "time_horizon": "immediate"}
    ]

    score, breakdown, rationale, is_emerging = ScoringEngine.calculate_market_importance_score(
        articles=articles,
        entities=entities,
        industry_impacts=impacts,
        verification_status="UNVERIFIED",
        trending_score=75.0
    )

    # High impact claim with UNVERIFIED status must be isolated
    assert is_emerging == True
