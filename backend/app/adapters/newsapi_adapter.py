"""NewsAPI adapter for discovering mainstream and tech AI news articles."""
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import httpx
from urllib.parse import urlparse

from .base import BaseSourceAdapter, RawArticleData
from app.config import settings

logger = logging.getLogger(__name__)

AI_DISCOVERY_QUERIES = [
    "artificial intelligence OR machine learning",
    "AGI OR superintelligence OR frontier model",
    "autonomous agent OR computer-use agent",
    "AI chip OR GPU inference OR data center power",
    "humanoid robot OR embodied AI",
    "AI safety OR AI regulation OR model evaluation",
    "AI startup funding OR acquisition AI",
]

class NewsAPIAdapter(BaseSourceAdapter):
    name = "newsapi"
    source_type = "news"

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key if api_key is not None else settings.NEWSAPI_API_KEY
        self.base_url = (base_url or settings.NEWSAPI_BASE_URL).rstrip("/")

    def get_coverage_limitations(self) -> str:
        return (
            "NewsAPI Free Developer Tier Constraints: Maximum 100 results per query, "
            "up to 24-hour publication delay, 100 requests/day limit, and strictly for non-commercial development. "
            "Full article body is truncated to 200 characters per NewsAPI terms. "
            "Independent corroboration is required to confirm full details."
        )

    async def test_connection(self) -> Dict[str, Any]:
        """Verify NewsAPI credentials and endpoint reachability."""
        if not self.api_key:
            return {
                "service": "NewsAPI",
                "status": "MISSING_KEY",
                "endpoint": f"{self.base_url}/top-headlines",
                "message": "NEWSAPI_API_KEY is not configured in environment or .env. Using mock/cached feeds for local demo.",
                "account_constraints": {
                    "tier": "Unconfigured",
                    "request_limit": "0 req/day",
                    "limitation": self.get_coverage_limitations(),
                }
            }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"{self.base_url}/top-headlines",
                    params={"category": "technology", "pageSize": 1},
                    headers={"X-Api-Key": self.api_key}
                )
                data = resp.json()
                if resp.status_code == 200 and data.get("status") == "ok":
                    return {
                        "service": "NewsAPI",
                        "status": "OK",
                        "endpoint": f"{self.base_url}/top-headlines",
                        "message": f"Successfully connected to NewsAPI. Total results available: {data.get('totalResults', 0)}",
                        "rate_limits": {
                            "limit_note": "Free plan allows 100 requests per 24 hours"
                        },
                        "account_constraints": {
                            "tier": "Developer Plan (Active)",
                            "limitation": self.get_coverage_limitations(),
                        }
                    }
                elif resp.status_code == 401 or data.get("code") == "apiKeyInvalid":
                    return {
                        "service": "NewsAPI",
                        "status": "INVALID_KEY",
                        "endpoint": f"{self.base_url}/top-headlines",
                        "message": f"NewsAPI rejected API key: {data.get('message', 'Invalid key')}",
                    }
                elif resp.status_code == 429 or data.get("code") == "rateLimited":
                    return {
                        "service": "NewsAPI",
                        "status": "RATE_LIMITED",
                        "endpoint": f"{self.base_url}/top-headlines",
                        "message": "Daily request quota exceeded for NewsAPI key.",
                    }
                else:
                    return {
                        "service": "NewsAPI",
                        "status": "ERROR",
                        "endpoint": f"{self.base_url}/top-headlines",
                        "message": f"Unexpected response {resp.status_code}: {data.get('message', '')}",
                    }
        except Exception as e:
            logger.error(f"NewsAPI connection error: {e}")
            return {
                "service": "NewsAPI",
                "status": "UNREACHABLE",
                "endpoint": f"{self.base_url}/top-headlines",
                "message": f"Failed to reach NewsAPI: {str(e)}",
            }

    async def fetch_articles(
        self,
        queries: Optional[List[str]] = None,
        days_back: int = 7,
        limit: int = 20
    ) -> List[RawArticleData]:
        """Fetch articles from NewsAPI with deduplication and pagination handling."""
        if not self.api_key:
            logger.info("NewsAPI API key is missing. Skipping live fetch.")
            return []

        active_queries = queries or AI_DISCOVERY_QUERIES[:2]
        from_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        articles: List[RawArticleData] = []
        seen_urls = set()

        async with httpx.AsyncClient(timeout=15.0) as client:
            # 1. Fetch breaking top headlines for technology/AI
            try:
                top_resp = await client.get(
                    f"{self.base_url}/top-headlines",
                    params={
                        "category": "technology",
                        "q": "AI",
                        "language": "en",
                        "pageSize": min(10, limit)
                    },
                    headers={"X-Api-Key": self.api_key}
                )
                if top_resp.status_code == 200:
                    top_data = top_resp.json()
                    for item in top_data.get("articles", []):
                        url = item.get("url")
                        if not url or url in seen_urls or "[Removed]" in (item.get("title") or ""):
                            continue
                        seen_urls.add(url)
                        pub_time = None
                        if item.get("publishedAt"):
                            try:
                                pub_time = datetime.fromisoformat(item["publishedAt"].replace("Z", "+00:00")).replace(tzinfo=None)
                            except Exception:
                                pub_time = datetime.utcnow()
                        articles.append(
                            RawArticleData(
                                provider_id=self.name,
                                provider_item_id=url,
                                canonical_url=url,
                                original_url=url,
                                headline=item.get("title") or "Untitled AI Report",
                                description=item.get("description"),
                                content=item.get("content"),
                                author=item.get("author"),
                                publisher=(item.get("source") or {}).get("name") or urlparse(url).netloc,
                                published_at=pub_time,
                                language="en",
                                retrieval_status="success",
                                metadata={"endpoint": "top-headlines", "newsapi_source": item.get("source")}
                            )
                        )
            except Exception as e:
                logger.warning(f"Error fetching NewsAPI top-headlines: {e}")

            # 2. Fetch everything matching AI discovery topics
            for q in active_queries:
                if len(articles) >= limit:
                    break
                try:
                    params = {
                        "q": q,
                        "from": from_date,
                        "sortBy": "publishedAt",
                        "language": "en",
                        "pageSize": min(20, limit - len(articles)),
                    }
                    resp = await client.get(
                        f"{self.base_url}/everything",
                        params=params,
                        headers={"X-Api-Key": self.api_key}
                    )
                    if resp.status_code != 200:
                        logger.warning(f"NewsAPI query '{q}' returned status {resp.status_code}")
                        continue
                    
                    data = resp.json()
                    raw_items = data.get("articles", [])
                    for item in raw_items:
                        url = item.get("url")
                        if not url or url in seen_urls or "[Removed]" in (item.get("title") or ""):
                            continue
                        seen_urls.add(url)
                        
                        pub_time = None
                        if item.get("publishedAt"):
                            try:
                                pub_time = datetime.fromisoformat(item["publishedAt"].replace("Z", "+00:00")).replace(tzinfo=None)
                            except Exception:
                                pub_time = datetime.utcnow()

                        articles.append(
                            RawArticleData(
                                provider_id=self.name,
                                provider_item_id=url,
                                canonical_url=url,
                                original_url=url,
                                headline=item.get("title") or "Untitled AI Report",
                                description=item.get("description"),
                                content=item.get("content"),
                                author=item.get("author"),
                                publisher=(item.get("source") or {}).get("name") or urlparse(url).netloc,
                                published_at=pub_time,
                                language="en",
                                retrieval_status="success",
                                metadata={"query": q, "newsapi_source": item.get("source")}
                            )
                        )
                except Exception as e:
                    logger.error(f"Error querying NewsAPI for '{q}': {e}")
                    continue

        return articles
