"""Integration tests for FastAPI REST endpoints."""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OK"
    assert "version" in data
    assert len(data["integrations"]) >= 4

@pytest.mark.asyncio
async def test_config_test_connections_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/config/test-connections")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    services = {item["service"] for item in data}
    assert "NewsAPI" in services
    assert "NVIDIA Hosted LLM (NIM)" in services

@pytest.mark.asyncio
async def test_stories_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/stories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    story = data[0]
    assert "title" in story
    assert "verification_status" in story
    assert "trending_score" in story
    assert "market_importance_score" in story

@pytest.mark.asyncio
async def test_story_detail_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        list_res = await ac.get("/api/stories")
        assert list_res.status_code == 200
        story_id = list_res.json()[0]["id"]

        detail_res = await ac.get(f"/api/stories/{story_id}")
    assert detail_res.status_code == 200
    detail = detail_res.json()
    assert detail["id"] == story_id
    assert "claims" in detail
    assert "entities" in detail
    assert "industry_impacts" in detail
    assert "score_breakdown" in detail

@pytest.mark.asyncio
async def test_leaderboards_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/leaderboards")
    assert response.status_code == 200
    data = response.json()
    assert "trending_leaderboard" in data
    assert "market_leaderboard" in data
    assert "emerging_signals" in data
    assert "scoring_methodology" in data

@pytest.mark.asyncio
async def test_analytics_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "total_stories" in data
    assert "verification_counts" in data
    assert "top_industries_exposed" in data

@pytest.mark.asyncio
async def test_sources_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/sources")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "url" in data[0]
        assert "access_status" in data[0]

@pytest.mark.asyncio
async def test_reports_generate_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/reports/generate?report_type=daily")
    assert response.status_code == 200
    report = response.json()
    assert "executive_summary" in report
    assert "sources_examined_count" in report
    assert "coverage_gaps_notes" in report
