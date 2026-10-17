"""Industry, Company, and Workforce Impact Analysis Engine."""
from typing import List, Dict, Any, Optional, Tuple

STANDARD_SECTORS = [
    "Software/SaaS",
    "Semiconductors/Hardware",
    "Banking/Finance",
    "Healthcare/Biotech",
    "Robotics/Manufacturing",
    "Education",
    "Media/Entertainment",
    "Retail",
    "Cybersecurity/Defense",
    "Energy/Utilities",
    "Professional Services"
]

SECTOR_KEYWORDS = {
    "Software/SaaS": ["software", "saas", "api", "developer", "coding", "copilot", "agent", "python", "ide"],
    "Semiconductors/Hardware": ["chip", "gpu", "semiconductor", "blackwell", "tsmc", "hbm", "wafer", "inference", "nvidia"],
    "Banking/Finance": ["banking", "trading", "finance", "credit", "fintech", "insurance", "underwriting", "fraud detection"],
    "Healthcare/Biotech": ["healthcare", "drug discovery", "protein", "alphafold", "biology", "clinical", "hospital", "pharma"],
    "Robotics/Manufacturing": ["robot", "humanoid", "actuator", "manufacturing", "embodied", "factory", "assembly"],
    "Education": ["education", "tutoring", "student", "learning", "curriculum", "university", "training"],
    "Media/Entertainment": ["media", "video", "generation", "music", "hollywood", "gaming", "vfx", "advertising", "content"],
    "Retail": ["retail", "ecommerce", "shopping", "recommendation", "supply chain", "inventory"],
    "Cybersecurity/Defense": ["cybersecurity", "vulnerability", "defense", "military", "malware", "exploit", "surveillance"],
    "Energy/Utilities": ["energy", "power", "grid", "nuclear", "megawatt", "cooling", "electricity", "carbon"],
    "Professional Services": ["legal", "accounting", "consulting", "law firm", "audit", "compliance", "customer support"]
}

PUBLIC_TICKER_MAP = {
    "nvidia": {"ticker": "NVDA", "exchange": "NASDAQ", "confirmed": True},
    "microsoft": {"ticker": "MSFT", "exchange": "NASDAQ", "confirmed": True},
    "google": {"ticker": "GOOGL", "exchange": "NASDAQ", "confirmed": True},
    "alphabet": {"ticker": "GOOGL", "exchange": "NASDAQ", "confirmed": True},
    "meta": {"ticker": "META", "exchange": "NASDAQ", "confirmed": True},
    "amazon": {"ticker": "AMZN", "exchange": "NASDAQ", "confirmed": True},
    "apple": {"ticker": "AAPL", "exchange": "NASDAQ", "confirmed": True},
    "amd": {"ticker": "AMD", "exchange": "NASDAQ", "confirmed": True},
    "tsmc": {"ticker": "TSM", "exchange": "NYSE", "confirmed": True},
    "asml": {"ticker": "ASML", "exchange": "NASDAQ", "confirmed": True},
    "oracle": {"ticker": "ORCL", "exchange": "NYSE", "confirmed": True},
    "palantir": {"ticker": "PLTR", "exchange": "NYSE", "confirmed": True},
    "constellation energy": {"ticker": "CEG", "exchange": "NASDAQ", "confirmed": True},
}

class IndustryImpactEngine:
    """Enriches and validates industry implications, ticker associations, and workforce exposures."""

    @classmethod
    def enrich_impacts(
        cls,
        text: str,
        extracted_impacts: List[Dict[str, Any]],
        extracted_entities: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Validate sectors, workforce transformation details, and ticker symbols."""
        lower_text = text.lower()
        impacts = list(extracted_impacts)
        entities = list(extracted_entities)

        # Ensure tickers are accurate and distinguish confirmed from speculative
        for entity in entities:
            ename = entity.get("name", "").lower()
            for key, data in PUBLIC_TICKER_MAP.items():
                if key in ename:
                    entity["ticker_symbol"] = data["ticker"]
                    entity["exchange"] = data["exchange"]
                    entity["is_confirmed_exposure"] = data["confirmed"]
                    break

        # Check if high-relevance sector keywords exist without an impact entry
        existing_sectors = {i.get("industry_name") for i in impacts}
        for sector, keywords in SECTOR_KEYWORDS.items():
            if sector not in existing_sectors and any(kw in lower_text for kw in keywords):
                if sector == "Energy/Utilities":
                    impacts.append({
                        "industry_name": "Energy/Utilities",
                        "impact_direction": "positive",
                        "impact_magnitude": "high",
                        "time_horizon": "near_term",
                        "mechanism": "Surging high-density data center power demand driving utility PPA contracts.",
                        "potential_beneficiaries": "Independent power producers, clean energy suppliers, transformer OEMs",
                        "disrupted_business_models": "Traditional utility load forecasting models",
                        "workforce_task_exposure": "Substation maintenance, power purchase agreement negotiation",
                        "workforce_augmentation_vs_displacement": "Workforce expansion in power infrastructure",
                        "confidence_level": "high"
                    })
                elif sector == "Cybersecurity/Defense":
                    impacts.append({
                        "industry_name": "Cybersecurity/Defense",
                        "impact_direction": "mixed",
                        "impact_magnitude": "high",
                        "time_horizon": "immediate",
                        "mechanism": "Accelerates automated vulnerability discovery and offensive agent capability.",
                        "potential_beneficiaries": "SOC defense automation platforms",
                        "disrupted_business_models": "Manual code audit consultancies",
                        "workforce_task_exposure": "Tier-1 SOC alert triage, routine patch application",
                        "workforce_augmentation_vs_displacement": "Augmentation of security analysts",
                        "confidence_level": "medium"
                    })

        # Ensure workforce analysis is always present
        for impact in impacts:
            if not impact.get("workforce_task_exposure"):
                impact["workforce_task_exposure"] = "Repetitive analytical synthesis, preliminary drafting, routine diagnostics"
            if not impact.get("workforce_augmentation_vs_displacement"):
                impact["workforce_augmentation_vs_displacement"] = "High augmentation of skilled practitioners; task compression in manual review"

        return impacts, entities
