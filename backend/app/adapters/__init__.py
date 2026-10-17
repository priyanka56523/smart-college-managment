"""Source adapters package for Global AI & AGI News Intelligence Platform."""
from .base import BaseSourceAdapter, RawArticleData
from .newsapi_adapter import NewsAPIAdapter
from .arxiv_adapter import ArxivAdapter
from .github_adapter import GitHubAdapter
from .official_feeds_adapter import OfficialFeedsAdapter
from .search_corroborator import SearchCorroboratorAdapter

__all__ = [
    "BaseSourceAdapter",
    "RawArticleData",
    "NewsAPIAdapter",
    "ArxivAdapter",
    "GitHubAdapter",
    "OfficialFeedsAdapter",
    "SearchCorroboratorAdapter",
]
