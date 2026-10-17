"""Tests for deduplication and event clustering."""
from datetime import datetime
from app.adapters.base import RawArticleData
from app.services.deduplication import cluster_articles_into_stories, clean_text

def test_clean_text():
    raw = "NVIDIA announces Blackwell B200 GPU! https://example.com/b200"
    cleaned = clean_text(raw)
    assert "https" not in cleaned
    assert "nvidia announces blackwell b200 gpu" == cleaned

def test_cluster_syndicated_articles():
    art1 = RawArticleData(
        provider_id="newsapi",
        provider_item_id="1",
        canonical_url="https://reuters.com/tech/nvidia-blackwell",
        original_url="https://reuters.com/tech/nvidia-blackwell",
        headline="NVIDIA launches Blackwell B200 AI superchip with 208 billion transistors",
        description="NVIDIA unveiled the Blackwell B200 GPU delivering major inference acceleration for frontier AI models.",
        content="NVIDIA announced Blackwell B200 at GTC...",
        author="Reuters Reporter",
        publisher="Reuters",
        published_at=datetime.utcnow()
    )
    art2 = RawArticleData(
        provider_id="newsapi",
        provider_item_id="2",
        canonical_url="https://yahoo.com/news/nvidia-blackwell-repost",
        original_url="https://yahoo.com/news/nvidia-blackwell-repost",
        headline="NVIDIA announces Blackwell B200 GPU with 208 billion transistors",
        description="NVIDIA unveiled the Blackwell B200 GPU delivering substantial inference acceleration for AI models.",
        content="NVIDIA announced Blackwell B200 at GTC...",
        author="Syndicated Feed",
        publisher="Yahoo News",
        published_at=datetime.utcnow()
    )
    art3 = RawArticleData(
        provider_id="newsapi",
        provider_item_id="3",
        canonical_url="https://nature.com/articles/alphafold3",
        original_url="https://nature.com/articles/alphafold3",
        headline="Accurate structure prediction of biomolecular interactions with AlphaFold 3",
        description="AlphaFold 3 predicts the structure and interactions of all life's molecules with unprecedented accuracy.",
        content="DeepMind presents AlphaFold 3...",
        author="DeepMind Team",
        publisher="Nature",
        published_at=datetime.utcnow()
    )

    clusters = cluster_articles_into_stories([art1, art2, art3])
    # art1 and art2 should cluster together; art3 should be in its own cluster
    assert len(clusters) == 2
    
    # Check that cluster with 2 items contains the Blackwell articles
    blackwell_cluster = next(c for c in clusters if len(c) == 2)
    assert any("Blackwell" in a.headline for a in blackwell_cluster)
    
    nature_cluster = next(c for c in clusters if len(c) == 1)
    assert "AlphaFold" in nature_cluster[0].headline
