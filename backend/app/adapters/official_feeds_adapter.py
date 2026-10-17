"""Official AI Laboratory & Company Announcement Adapter."""
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
import httpx
import feedparser

from .base import BaseSourceAdapter, RawArticleData

logger = logging.getLogger(__name__)

OFFICIAL_AI_LAB_FEEDS = [
    {
        "publisher": "OpenAI",
        "url": "https://openai.com/news/rss.xml",
        "fallback_feed": "https://rss.app/feeds/openai.xml",
        "org_role": "creator"
    },
    {
        "publisher": "Google DeepMind",
        "url": "https://deepmind.google/blog/rss.xml",
        "fallback_feed": "https://blog.google/technology/ai/rss/",
        "org_role": "creator"
    },
    {
        "publisher": "Anthropic",
        "url": "https://www.anthropic.com/news/feed.xml",
        "fallback_feed": "https://raw.githubusercontent.com/anthropics/anthropic-sdk-python/main/README.md",
        "org_role": "creator"
    },
    {
        "publisher": "Hugging Face",
        "url": "https://huggingface.co/blog/feed.xml",
        "fallback_feed": None,
        "org_role": "platform"
    },
    {
        "publisher": "NVIDIA Newsroom",
        "url": "https://nvidianews.nvidia.com/releases.xml",
        "fallback_feed": None,
        "org_role": "hardware_infrastructure"
    }
]

class OfficialFeedsAdapter(BaseSourceAdapter):
    name = "official_feed"
    source_type = "official_announcement"

    def get_coverage_limitations(self) -> str:
        return (
            "Official Lab Announcement Constraints: Primary releases contain direct manufacturer claims. "
            "While authentic proof of what the company announced, advertised benchmark metrics require independent corroboration and scrutiny."
        )

    async def test_connection(self) -> Dict[str, Any]:
        """Verify reachability of official lab announcement feeds."""
        reachable_count = 0
        total_count = len(OFFICIAL_AI_LAB_FEEDS)
        
        async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
            for feed_info in OFFICIAL_AI_LAB_FEEDS:
                try:
                    resp = await client.get(feed_info["url"])
                    if resp.status_code == 200:
                        reachable_count += 1
                except Exception:
                    pass

        status = "OK" if reachable_count > 0 else "WARNING"
        return {
            "service": "Official AI Lab Feeds",
            "status": status,
            "endpoint": "OpenAI, DeepMind, Anthropic, HuggingFace, NVIDIA feeds",
            "message": f"Connected to {reachable_count}/{total_count} official laboratory announcement feeds.",
            "account_constraints": {
                "tier": "Public RSS/Atom",
                "limitation": self.get_coverage_limitations(),
            }
        }

    async def fetch_articles(
        self,
        queries: Optional[List[str]] = None,
        days_back: int = 14,
        limit: int = 15
    ) -> List[RawArticleData]:
        """Fetch primary announcements from frontier AI companies."""
        articles: List[RawArticleData] = []
        
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            for feed_info in OFFICIAL_AI_LAB_FEEDS:
                if len(articles) >= limit:
                    break
                try:
                    resp = await client.get(feed_info["url"])
                    if resp.status_code != 200:
                        continue
                    
                    parsed = feedparser.parse(resp.text)
                    for entry in parsed.entries[:4]:
                        url = entry.get("link") or entry.get("id")
                        if not url:
                            continue
                        
                        title = entry.get("title", "Official Announcement").strip()
                        summary = entry.get("summary", "").strip()
                        
                        published_at = datetime.utcnow()
                        if entry.get("published_parsed"):
                            published_at = datetime(*entry.published_parsed[:6])

                        articles.append(
                            RawArticleData(
                                provider_id=self.name,
                                provider_item_id=url,
                                canonical_url=url,
                                original_url=url,
                                headline=title,
                                description=summary[:400] if summary else "Official laboratory release",
                                content=summary,
                                author=feed_info["publisher"],
                                publisher=feed_info["publisher"],
                                published_at=published_at,
                                language="en",
                                retrieval_status="success",
                                metadata={"is_primary_lab": True, "org_role": feed_info["org_role"]}
                            )
                        )
                except Exception as e:
                    logger.debug(f"Feed {feed_info['publisher']} fetch failed: {e}")
                    continue

        return articles
