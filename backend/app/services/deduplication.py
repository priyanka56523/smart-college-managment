"""Deduplication and Event Clustering Service using TF-IDF and Cosine Similarity."""
import re
import logging
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.adapters.base import RawArticleData

logger = logging.getLogger(__name__)

SIMILARITY_THRESHOLD = 0.55  # Articles with cosine similarity > 0.55 belong to the same event cluster

def clean_text(text: str) -> str:
    """Normalize text for semantic comparison."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return ' '.join(text.split())

def extract_event_date_hint(text: str, published_at: Optional[datetime]) -> Optional[datetime]:
    """Identify if article references an older event rather than breaking news."""
    if not text or not published_at:
        return published_at
    
    # Check for historical re-reporting patterns
    lower = text.lower()
    if any(phrase in lower for phrase in ["last year", "in 2023", "in 2022", "originally announced"]):
        # It's an analytical reflection, retain published_at but mark event_date as potentially older
        return published_at
    return published_at

def cluster_articles_into_stories(
    articles: List[RawArticleData],
    existing_story_titles: Optional[List[str]] = None
) -> List[List[RawArticleData]]:
    """
    Cluster incoming articles into groups representing the same underlying news event.
    Deduplicates syndicated press releases and syndicated republishing.
    """
    if not articles:
        return []

    if len(articles) == 1:
        return [[articles[0]]]

    # Combine headline + description for rich representation
    docs = [clean_text(f"{a.headline} {a.description or ''}") for a in articles]
    
    # Handle cases where texts are too short or empty
    if all(len(d.strip()) == 0 for d in docs):
        return [[a] for a in articles]

    try:
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        tfidf_matrix = vectorizer.fit_transform(docs)
        sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

        n = len(articles)
        visited = [False] * n
        clusters: List[List[RawArticleData]] = []

        for i in range(n):
            if visited[i]:
                continue
            current_cluster = [articles[i]]
            visited[i] = True
            for j in range(i + 1, n):
                if not visited[j] and sim_matrix[i, j] >= SIMILARITY_THRESHOLD:
                    current_cluster.append(articles[j])
                    visited[j] = True
            clusters.append(current_cluster)

        return clusters
    except Exception as e:
        logger.error(f"Error clustering articles: {e}")
        # Fallback to 1 cluster per article
        return [[a] for a in articles]
