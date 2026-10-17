"""GitHub Releases and Repository Activity Adapter."""
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import httpx

from .base import BaseSourceAdapter, RawArticleData

logger = logging.getLogger(__name__)

GITHUB_API_SEARCH_URL = "https://api.github.com/search/repositories"

class GitHubAdapter(BaseSourceAdapter):
    name = "github"
    source_type = "repository"

    def get_coverage_limitations(self) -> str:
        return (
            "GitHub Public API Constraints: 60 unauthenticated requests/hour. "
            "Repository stars and commit velocity indicate developer interest but do not equate to production viability or benchmark truth."
        )

    async def test_connection(self) -> Dict[str, Any]:
        """Verify reachability of GitHub API."""
        try:
            headers = {"User-Agent": "AI-Intelligence-Platform/1.0", "Accept": "application/vnd.github.v3+json"}
            async with httpx.AsyncClient(timeout=10.0, headers=headers) as client:
                resp = await client.get(
                    GITHUB_API_SEARCH_URL,
                    params={"q": "ai-agent", "per_page": 1}
                )
                rate_limit_remaining = resp.headers.get("x-ratelimit-remaining", "unknown")
                if resp.status_code == 200:
                    return {
                        "service": "GitHub API",
                        "status": "OK",
                        "endpoint": GITHUB_API_SEARCH_URL,
                        "message": f"GitHub API active. Remaining hourly requests: {rate_limit_remaining}",
                        "account_constraints": {
                            "tier": "Public API (Unauthenticated)",
                            "rate_limit": f"{rate_limit_remaining} requests remaining this hour",
                            "limitation": self.get_coverage_limitations(),
                        }
                    }
                elif resp.status_code == 403:
                    return {
                        "service": "GitHub API",
                        "status": "RATE_LIMITED",
                        "endpoint": GITHUB_API_SEARCH_URL,
                        "message": "GitHub API hourly rate limit reached.",
                    }
                else:
                    return {
                        "service": "GitHub API",
                        "status": "ERROR",
                        "endpoint": GITHUB_API_SEARCH_URL,
                        "message": f"GitHub returned status {resp.status_code}",
                    }
        except Exception as e:
            return {
                "service": "GitHub API",
                "status": "UNREACHABLE",
                "endpoint": GITHUB_API_SEARCH_URL,
                "message": f"Could not connect to GitHub API: {str(e)}",
            }

    async def fetch_articles(
        self,
        queries: Optional[List[str]] = None,
        days_back: int = 7,
        limit: int = 10
    ) -> List[RawArticleData]:
        """Fetch trending AI repos and announcements."""
        since_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        search_query = f"stars:>50 pushed:>{since_date} (ai-agent OR llm OR inference OR multimodal)"
        
        articles: List[RawArticleData] = []
        headers = {"User-Agent": "AI-Intelligence-Platform/1.0", "Accept": "application/vnd.github.v3+json"}
        
        try:
            async with httpx.AsyncClient(timeout=15.0, headers=headers) as client:
                resp = await client.get(
                    GITHUB_API_SEARCH_URL,
                    params={"q": search_query, "sort": "stars", "order": "desc", "per_page": limit}
                )
                if resp.status_code != 200:
                    return []
                
                data = resp.json()
                for item in data.get("items", []):
                    html_url = item.get("html_url")
                    name = item.get("full_name")
                    description = item.get("description") or "Open source AI repository"
                    stars = item.get("stargazers_count", 0)
                    forks = item.get("forks_count", 0)
                    
                    pushed_at = datetime.utcnow()
                    if item.get("pushed_at"):
                        try:
                            pushed_at = datetime.fromisoformat(item["pushed_at"].replace("Z", "+00:00")).replace(tzinfo=None)
                        except Exception:
                            pass

                    articles.append(
                        RawArticleData(
                            provider_id=self.name,
                            provider_item_id=str(item.get("id")),
                            canonical_url=html_url,
                            original_url=html_url,
                            headline=f"Release & Code: {name} (★ {stars:,})",
                            description=f"{description} [GitHub repo with {stars} stars, {forks} forks]",
                            content=f"Repository {name}: {description}. Language: {item.get('language')}. Open issues: {item.get('open_issues_count')}.",
                            author=item.get("owner", {}).get("login"),
                            publisher="GitHub",
                            published_at=pushed_at,
                            language="en",
                            retrieval_status="success",
                            metadata={
                                "stars": stars,
                                "forks": forks,
                                "topics": item.get("topics", [])
                            }
                        )
                    )
        except Exception as e:
            logger.error(f"Error fetching GitHub repositories: {e}")

        return articles
