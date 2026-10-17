"""arXiv Research Repository Adapter for Frontier AI Papers."""
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
import httpx
import feedparser

from .base import BaseSourceAdapter, RawArticleData

logger = logging.getLogger(__name__)

ARXIV_API_URL = "https://export.arxiv.org/api/query"

class ArxivAdapter(BaseSourceAdapter):
    name = "arxiv"
    source_type = "academic"

    def get_coverage_limitations(self) -> str:
        return (
            "arXiv Repository Constraints: Papers represent preprints and non-peer-reviewed research manuscripts. "
            "Claims reflect author assertions and benchmark results that require independent reproduction before verification."
        )

    async def test_connection(self) -> Dict[str, Any]:
        """Verify reachability of arXiv query API."""
        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                resp = await client.get(
                    ARXIV_API_URL,
                    params={"search_query": "cat:cs.AI", "max_results": 1}
                )
                if resp.status_code == 200:
                    return {
                        "service": "arXiv Research API",
                        "status": "OK",
                        "endpoint": ARXIV_API_URL,
                        "message": "Public arXiv API connected successfully. Rate limited to 1 request every 3 seconds.",
                        "account_constraints": {
                            "tier": "Public Open Access",
                            "limitation": self.get_coverage_limitations(),
                        }
                    }
                else:
                    return {
                        "service": "arXiv Research API",
                        "status": "ERROR",
                        "endpoint": ARXIV_API_URL,
                        "message": f"arXiv returned HTTP status {resp.status_code}",
                    }
        except Exception as e:
            return {
                "service": "arXiv Research API",
                "status": "UNREACHABLE",
                "endpoint": ARXIV_API_URL,
                "message": f"Could not reach arXiv API: {str(e)}",
            }

    async def fetch_articles(
        self,
        queries: Optional[List[str]] = None,
        days_back: int = 7,
        limit: int = 15
    ) -> List[RawArticleData]:
        """Fetch latest AI/AGI papers from arXiv."""
        query = 'cat:cs.AI OR cat:cs.LG OR cat:cs.CL'
        if queries:
            query = f"({query}) AND ({' OR '.join(queries)})"

        articles: List[RawArticleData] = []
        try:
            async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
                resp = await client.get(
                    ARXIV_API_URL,
                    params={
                        "search_query": query,
                        "sortBy": "submittedDate",
                        "sortOrder": "descending",
                        "max_results": limit
                    }
                )
                if resp.status_code != 200:
                    logger.warning(f"arXiv fetch returned status {resp.status_code}")
                    return []

                feed = feedparser.parse(resp.text)
                for entry in feed.entries:
                    url = entry.get("link") or entry.get("id")
                    title = (entry.get("title") or "").replace("\n", " ").strip()
                    summary = (entry.get("summary") or "").replace("\n", " ").strip()
                    
                    # Authors
                    authors_list = [a.get("name") for a in entry.get("authors", []) if a.get("name")]
                    author_str = ", ".join(authors_list[:3])
                    if len(authors_list) > 3:
                        author_str += " et al."

                    # Parse date
                    published_at = datetime.utcnow()
                    if entry.get("published_parsed"):
                        published_at = datetime(*entry.published_parsed[:6])

                    articles.append(
                        RawArticleData(
                            provider_id=self.name,
                            provider_item_id=entry.get("id") or url,
                            canonical_url=url,
                            original_url=url,
                            headline=title,
                            description=summary[:500] + "..." if len(summary) > 500 else summary,
                            content=summary,
                            author=author_str,
                            publisher="arXiv.org",
                            published_at=published_at,
                            language="en",
                            retrieval_status="success",
                            metadata={
                                "primary_category": getattr(entry, "arxiv_primary_category", {}).get("term", "cs.AI"),
                                "comment": getattr(entry, "arxiv_comment", None)
                            }
                        )
                    )
        except Exception as e:
            logger.error(f"Error fetching arXiv papers: {e}")

        return articles
