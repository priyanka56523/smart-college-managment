"""Tests for Verification Engine and evidentiary status rules."""
from datetime import datetime
from app.adapters.base import RawArticleData
from app.services.verification_service import VerificationEngine

def test_debunked_claim_detection():
    art = RawArticleData(
        provider_id="newsapi", provider_item_id="1", canonical_url="https://news.com/1",
        original_url="https://news.com/1", headline="Viral Room-temperature Superconductor AI paper retracted and debunked",
        description="The authors have retracted the paper after benchmark fabrication was discovered.",
        content="Debunked by independent replication laboratories.", author="", publisher="Science",
        published_at=datetime.utcnow()
    )
    status, rationale, ev = VerificationEngine.evaluate(
        articles=[art], suggested_llm_status="DISPUTED", claims=[], probed_sources=[]
    )
    assert status == "FALSE OR DEBUNKED"
    assert "debunked" in rationale.lower()

def test_disputed_claim_detection():
    art = RawArticleData(
        provider_id="newsapi", provider_item_id="1", canonical_url="https://news.com/1",
        original_url="https://news.com/1", headline="Researchers dispute benchmark contamination in novel LLM",
        description="Conflicting results emerged as independent tests failed to replicate advertised gains.",
        content="Methodological flaw noted in training set overlap.", author="", publisher="TechReview",
        published_at=datetime.utcnow()
    )
    status, rationale, ev = VerificationEngine.evaluate(
        articles=[art], suggested_llm_status="DISPUTED", claims=[], probed_sources=[]
    )
    assert status == "DISPUTED"

def test_agi_claim_safeguard():
    art = RawArticleData(
        provider_id="newsapi", provider_item_id="1", canonical_url="https://lab.com/1",
        original_url="https://lab.com/1", headline="Frontier Startup announces AGI achieved in internal benchmark",
        description="The company claims to have reached AGI on proprietary reasoning tasks.",
        content="We have officially reached AGI.", author="", publisher="Lab Blog",
        published_at=datetime.utcnow()
    )
    status, rationale, ev = VerificationEngine.evaluate(
        articles=[art], suggested_llm_status="VERIFIED", claims=[], probed_sources=[]
    )
    # The prompt explicitly instructs: "An AI company's claim of AGI achievement must not be treated as proof of AGI."
    assert status == "PARTIALLY VERIFIED"
    assert "scientific proof of agi" in rationale.lower()

def test_verified_when_primary_and_independent_present():
    art_primary = RawArticleData(
        provider_id="official_feed", provider_item_id="1", canonical_url="https://openai.com/index/o1",
        original_url="https://openai.com/index/o1", headline="OpenAI o1 release",
        description="", content="", author="OpenAI", publisher="OpenAI",
        published_at=datetime.utcnow(), metadata={"is_primary_lab": True}
    )
    art_indep = RawArticleData(
        provider_id="newsapi", provider_item_id="2", canonical_url="https://reuters.com/tech/o1",
        original_url="https://reuters.com/tech/o1", headline="OpenAI rolls out o1 model",
        description="", content="", author="Reuters", publisher="Reuters",
        published_at=datetime.utcnow()
    )
    status, rationale, ev = VerificationEngine.evaluate(
        articles=[art_primary, art_indep],
        suggested_llm_status="VERIFIED",
        claims=[],
        probed_sources=[{"access_status": "accessed_and_verified"}]
    )
    assert status == "VERIFIED"
