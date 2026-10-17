"""Tests for source adapters and API connection handlers."""
import pytest
from app.adapters import NewsAPIAdapter, ArxivAdapter, GitHubAdapter, OfficialFeedsAdapter, SearchCorroboratorAdapter
from app.services.llm_service import NVIDIAHostedLLMService

@pytest.mark.asyncio
async def test_newsapi_missing_key_behavior():
    adapter = NewsAPIAdapter(api_key="")
    res = await adapter.test_connection()
    assert res["status"] == "MISSING_KEY"
    assert "Developer Tier Constraints" in adapter.get_coverage_limitations()
    
    # Live fetch with empty key returns empty list cleanly without crashing
    articles = await adapter.fetch_articles()
    assert articles == []

@pytest.mark.asyncio
async def test_nvidia_missing_key_behavior():
    service = NVIDIAHostedLLMService(api_key="")
    res = await service.test_connection()
    assert res["status"] == "MISSING_KEY"
    assert res["model"] == "meta/llama-3.1-70b-instruct"

@pytest.mark.asyncio
async def test_corroborator_probe():
    corroborator = SearchCorroboratorAdapter()
    res = await corroborator.test_connection()
    assert res["status"] in ["OK", "DEGRADED", "UNREACHABLE"]
    assert "accessed_and_verified" in corroborator.get_coverage_limitations() or "Constraints" in corroborator.get_coverage_limitations()

@pytest.mark.asyncio
async def test_official_feeds_adapter_metadata():
    adapter = OfficialFeedsAdapter()
    assert adapter.name == "official_feed"
    assert adapter.source_type == "official_announcement"
    assert "Constraints" in adapter.get_coverage_limitations()

@pytest.mark.asyncio
async def test_arxiv_adapter_metadata():
    adapter = ArxivAdapter()
    assert adapter.name == "arxiv"
    assert adapter.source_type == "academic"
    assert "Preprints" in adapter.get_coverage_limitations() or "preprints" in adapter.get_coverage_limitations()
