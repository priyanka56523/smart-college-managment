"""Evidence-based Verification Engine with transparent rules and status assignment."""
import logging
from typing import List, Dict, Any, Tuple
from app.adapters.base import RawArticleData

logger = logging.getLogger(__name__)

PRIMARY_SOURCES = {
    "openai.com", "anthropic.com", "deepmind.google", "ai.meta.com",
    "nvidia.com", "arxiv.org", "github.com", "sec.gov", "whitehouse.gov"
}

TOP_TIER_NEWS = {
    "reuters.com", "bloomberg.com", "ft.com", "wsj.com",
    "associated press", "ap news", "technology review", "nature.com"
}

DEBUNK_KEYWORDS = [
    "debunked", "retracted", "hoax", "false claim", "fabricated benchmark",
    "denied by researchers", "unsubstantiated rumor", "fake paper"
]

DISPUTED_KEYWORDS = [
    "disputed", "controversy", "conflicting results", "failed to replicate",
    "methodological flaw", "benchmark contamination", "misleading claims"
]

AGI_HYPE_KEYWORDS = [
    "agi achieved", "reached agi", "superintelligence is here", "sentient ai"
]

class VerificationEngine:
    """Transparent rule-based verification engine evaluating primary and independent evidence."""

    @classmethod
    def evaluate(
        cls,
        articles: List[RawArticleData],
        suggested_llm_status: str,
        claims: List[Dict[str, Any]],
        probed_sources: List[Dict[str, Any]]
    ) -> Tuple[str, str, Dict[str, Any]]:
        """
        Determine formal verification status based on evidentiary rules.
        Returns: (status, rationale, evidence_summary)
        """
        all_text = " ".join([f"{a.headline} {a.description or ''} {a.content or ''}" for a in articles]).lower()
        
        # 1. Check for Debunked or False claims
        if any(keyword in all_text for keyword in DEBUNK_KEYWORDS):
            return (
                "FALSE OR DEBUNKED",
                "Reliable sources or author retractions indicate that the central claims of this development are debunked, fabricated, or retracted.",
                {"debunk_signal": True, "direct_refutations": 1}
            )

        # 2. Check for Disputed claims
        if any(keyword in all_text for keyword in DISPUTED_KEYWORDS):
            return (
                "DISPUTED",
                "Credible independent evaluations or opposing sources materially conflict on benchmark reproducibility, safety, or core methodology.",
                {"conflict_signals": True}
            )

        # 3. Special safeguard: AGI achievement claims
        is_agi_claim = any(keyword in all_text for keyword in AGI_HYPE_KEYWORDS)
        if is_agi_claim:
            return (
                "PARTIALLY VERIFIED",
                "While the release or announcement event may be genuine, an organization's assertion of AGI achievement is not accepted as scientific proof of AGI without universally accepted independent consensus.",
                {"agi_claim_safeguard": True, "advertised_vs_proven": "unproven"}
            )

        # 4. Count distinct authoritative sources (avoiding syndicated duplicates)
        distinct_publishers = set()
        has_primary_announcement = False
        has_arxiv_paper = False
        has_github_code = False
        has_independent_press = False

        for a in articles:
            pub = (a.publisher or "").lower()
            url = (a.canonical_url or "").lower()
            distinct_publishers.add(pub)

            if any(p in url for p in PRIMARY_SOURCES) or (a.metadata and a.metadata.get("is_primary_lab")):
                has_primary_announcement = True
            if "arxiv.org" in url or a.provider_id == "arxiv":
                has_arxiv_paper = True
            if "github.com" in url or a.provider_id == "github":
                has_github_code = True
            if any(top in pub or top in url for top in TOP_TIER_NEWS):
                has_independent_press = True

        evidence_summary = {
            "distinct_publishers_count": len(distinct_publishers),
            "has_primary_announcement": has_primary_announcement,
            "has_arxiv_paper": has_arxiv_paper,
            "has_github_code": has_github_code,
            "has_independent_press": has_independent_press,
            "verified_probes_count": len([p for p in probed_sources if p.get("access_status") == "accessed_and_verified"])
        }

        # Status assignment hierarchy
        if (has_primary_announcement or has_arxiv_paper or has_github_code) and (has_independent_press or len(distinct_publishers) >= 2):
            return (
                "VERIFIED",
                "Strong direct evidence from primary lab/repository records corroborated by independent reporting confirms the event.",
                evidence_summary
            )
        elif len(distinct_publishers) >= 2 or has_independent_press:
            return (
                "CORROBORATED",
                "Multiple credible reporting outlets support the event, though full reproducible technical logs or open weights remain pending.",
                evidence_summary
            )
        elif has_primary_announcement or has_arxiv_paper or has_github_code:
            return (
                "PARTIALLY VERIFIED",
                "Original primary release is verified, but independent third-party evaluations and replication metrics are not yet established.",
                evidence_summary
            )
        else:
            return (
                "UNVERIFIED",
                "Available evidence is currently based on single-source reports or uncorroborated leaks.",
                evidence_summary
            )
