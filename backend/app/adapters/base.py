"""Base class and common data structures for source adapters."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any

@dataclass
class RawArticleData:
    provider_id: str
    provider_item_id: str
    canonical_url: str
    original_url: str
    headline: str
    description: Optional[str]
    content: Optional[str]
    author: Optional[str]
    publisher: Optional[str]
    published_at: Optional[datetime]
    collected_at: datetime = field(default_factory=datetime.utcnow)
    language: str = "en"
    retrieval_status: str = "success"  # success, truncated, rate_limited, error
    metadata: Dict[str, Any] = field(default_factory=dict)

class BaseSourceAdapter(ABC):
    """Abstract base adapter for all news, research, and technical sources."""
    
    name: str = "base"
    source_type: str = "news"  # news, academic, repository, official_announcement
    
    @abstractmethod
    async def test_connection(self) -> Dict[str, Any]:
        """Test API connectivity, authentication, and report quota/rate limit status."""
        pass

    @abstractmethod
    async def fetch_articles(
        self,
        queries: Optional[List[str]] = None,
        days_back: int = 7,
        limit: int = 20
    ) -> List[RawArticleData]:
        """Fetch raw articles matching AI & AGI discovery topics."""
        pass

    @abstractmethod
    def get_coverage_limitations(self) -> str:
        """Return human-readable statement of access constraints, delays, or coverage gaps."""
        pass
