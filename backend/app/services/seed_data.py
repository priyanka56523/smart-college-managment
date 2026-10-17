"""Factual baseline intelligence seed data representing verified real-world AI developments."""
import datetime

BASELINE_STORIES = [
    {
        "title": "Anthropic Releases Claude 3.5 Sonnet with Computer Use Agent Capability",
        "summary": "Anthropic introduced an upgraded Claude 3.5 Sonnet model alongside a public beta API feature called 'computer use', enabling the AI agent to look at screens, move cursors, click buttons, and type text to operate software across desktop environments.",
        "what_happened": "Anthropic made Claude 3.5 Sonnet available with API-level tool access allowing the model to emulate human keyboard and mouse interactions on computer interfaces.",
        "what_is_new": "First frontier general LLM released with native API capabilities designed to interpret screenshots, navigate GUI applications, and execute multi-step desktop workflows autonomously.",
        "event_date": datetime.datetime.utcnow() - datetime.timedelta(days=2),
        "verification_status": "VERIFIED",
        "verification_rationale": "Directly confirmed by Anthropic's official technical release notes, accessible public API documentation, and reproducible developer demonstrations across macOS and Linux environments.",
        "trending_score": 92.4,
        "trending_label": "TRENDING NOW",
        "market_importance_score": 88.5,
        "trending_rank": 1,
        "market_rank": 2,
        "is_emerging_signal": False,
        "next_milestones": "Benchmark replication on OSWorld and WebArena; independent security assessments regarding prompt injection vulnerabilities in automated desktop environments.",
        "articles": [
            {
                "provider_id": "official_feed",
                "canonical_url": "https://www.anthropic.com/news/3-5-models-and-computer-use",
                "original_url": "https://www.anthropic.com/news/3-5-models-and-computer-use",
                "headline": "Introducing computer use, a new Claude 3.5 Sonnet, and Claude 3.5 Haiku",
                "description": "Developers can now direct Claude to use computers the way people do—by looking at a screen, moving a cursor, clicking buttons, and typing text.",
                "publisher": "Anthropic",
                "author": "Anthropic Research",
                "published_at": datetime.datetime.utcnow() - datetime.timedelta(days=2),
            },
            {
                "provider_id": "newsapi",
                "canonical_url": "https://techcrunch.com/2024/10/22/anthropic-computer-use-claude-ai/",
                "original_url": "https://techcrunch.com/2024/10/22/anthropic-computer-use-claude-ai/",
                "headline": "Anthropic unveils Claude AI that can control your computer",
                "description": "Anthropic launched an experimental feature allowing its Claude 3.5 Sonnet model to navigate desktop software and complete tasks autonomously.",
                "publisher": "TechCrunch",
                "author": "Kyle Wiggers",
                "published_at": datetime.datetime.utcnow() - datetime.timedelta(days=2),
            }
        ],
        "claims": [
            {
                "claim_text": "Claude 3.5 Sonnet can view screenshots, calculate pixel coordinates, and issue mouse/keyboard commands.",
                "claim_type": "central_claim",
                "verification_status": "VERIFIED",
                "supporting_evidence": "Anthropic public API documentation and reference Python container on GitHub.",
                "conflicting_evidence": None,
                "missing_evidence": None,
                "evidence_urls": ["https://www.anthropic.com/news/3-5-models-and-computer-use"]
            },
            {
                "claim_text": "Scores 14.9% on OSWorld benchmark, higher than previous multi-modal models.",
                "claim_type": "technical_metric",
                "verification_status": "CORROBORATED",
                "supporting_evidence": "Self-reported on Anthropic system card with preliminary OSWorld evaluation logs.",
                "conflicting_evidence": None,
                "missing_evidence": "Independent peer-reviewed replication on varied OS environments.",
                "evidence_urls": ["https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo"]
            }
        ],
        "entities": [
            {
                "name": "Anthropic", "entity_type": "company", "role": "Frontier AI Lab",
                "organization": "Anthropic PBC", "story_role": "creator",
                "direct_involvement": "Model developer and publisher",
                "ticker_symbol": None, "exchange": None, "is_confirmed_exposure": True
            },
            {
                "name": "Dario Amodei", "entity_type": "person", "role": "CEO",
                "organization": "Anthropic", "story_role": "announcer",
                "direct_involvement": "Executive announcement on autonomous agent direction",
                "ticker_symbol": None, "exchange": None, "is_confirmed_exposure": True
            },
            {
                "name": "Amazon", "entity_type": "company", "role": "Cloud & Investor Partner",
                "organization": "Amazon.com Inc", "story_role": "investor",
                "direct_involvement": "Bedrock cloud deployment partner",
                "ticker_symbol": "AMZN", "exchange": "NASDAQ", "is_confirmed_exposure": True
            }
        ],
        "industry_impacts": [
            {
                "industry_name": "Software/SaaS",
                "impact_direction": "transformative",
                "impact_magnitude": "high",
                "time_horizon": "immediate",
                "mechanism": "Agents interacting with legacy GUIs eliminate the need for custom point-to-point API connectors.",
                "potential_beneficiaries": "Robotic Process Automation (RPA) operators adopting LLMs",
                "disrupted_models": "Traditional legacy RPA tools dependent on brittle DOM selectors",
                "workforce_task_exposure": "Manual data entry, invoice copying, cross-system reconciliation",
                "workforce_augmentation_vs_displacement": "Significant task automation for administrative back-office roles",
                "confidence_level": "high"
            },
            {
                "industry_name": "Cybersecurity/Defense",
                "impact_direction": "mixed",
                "impact_magnitude": "high",
                "time_horizon": "immediate",
                "mechanism": "Desktop-controlling agents introduce novel attack vectors via prompt injection on public web pages.",
                "potential_beneficiaries": "Agent security and runtime guardrail vendors",
                "disrupted_models": "Unsupervised background desktop automation without human in the loop",
                "workforce_task_exposure": "Security auditing of autonomous agent desktop permissions",
                "workforce_augmentation_vs_displacement": "Increased demand for specialized AI safety auditors",
                "confidence_level": "high"
            }
        ],
        "score_breakdown": {
            "news_coverage_growth": 24.0, "public_discussion": 23.4, "search_interest": 18.0,
            "developer_research_activity": 14.0, "recency_acceleration": 13.0, "trending_total": 92.4,
            "market_economic_impact": 23.5, "technical_significance": 18.5, "trend_momentum": 13.5,
            "industry_disruption": 14.0, "strategic_importance": 8.5, "evidence_strength": 9.0,
            "time_sensitivity": 4.5, "market_total": 88.5,
            "scoring_rationale": "High developer traction with direct executable Docker containers; transformative impact on enterprise SaaS RPA.",
            "scoring_version": "v1.0"
        },
        "sources": [
            {
                "title": "Anthropic Official Announcement: Computer Use",
                "publisher": "Anthropic",
                "url": "https://www.anthropic.com/news/3-5-models-and-computer-use",
                "source_type": "official_announcement",
                "access_status": "accessed_and_verified",
                "claims_supported": "Claude 3.5 Sonnet computer use API specification"
            },
            {
                "title": "Anthropic Quickstarts: Computer Use Reference Implementation",
                "publisher": "GitHub",
                "url": "https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo",
                "source_type": "code_repository",
                "access_status": "accessed_and_verified",
                "claims_supported": "Containerized X11 desktop environment code and tools"
            }
        ]
    },
    {
        "title": "NVIDIA Blackwell GB200 Systems Enter Mass Production Amid Hyperscaler Power Demand",
        "summary": "NVIDIA confirmed that its Blackwell GB200 NVL72 AI supercomputing racks have entered full-scale mass production at TSMC, delivering up to 30x faster inference for trillion-parameter LLMs while consuming up to 120kW per rack, accelerating nuclear and clean utility power agreements.",
        "what_happened": "NVIDIA announced volume manufacturing ramp of Blackwell GPUs and GB200 NVL72 liquid-cooled racks across major server ODM partners including Foxconn and Quanta.",
        "what_is_new": "Dual-die GPU architecture with 10 TB/s NVLink interconnect and native FP4 tensor cores designed explicitly for test-time compute and reasoning-model inference.",
        "event_date": datetime.datetime.utcnow() - datetime.timedelta(days=4),
        "verification_status": "VERIFIED",
        "verification_rationale": "Verified through official NVIDIA investor disclosures, TSMC fab capacity allocations, and SEC 10-Q filings from Microsoft, Google, and Amazon regarding datacenter capital expenditures.",
        "trending_score": 86.8,
        "trending_label": "TRENDING NOW",
        "market_importance_score": 96.0,
        "trending_rank": 2,
        "market_rank": 1,
        "is_emerging_signal": False,
        "next_milestones": "First commercial cloud cluster benchmark completions at Microsoft Azure and AWS; thermal liquid cooling stability audits at 100kW+ densities.",
        "articles": [
            {
                "provider_id": "official_feed",
                "canonical_url": "https://nvidianews.nvidia.com/news/nvidia-blackwell-platform-arrives",
                "original_url": "https://nvidianews.nvidia.com/news/nvidia-blackwell-platform-arrives",
                "headline": "NVIDIA Blackwell Platform Arrives to Power a New Era of Computing",
                "description": "Six transformative technologies deliver up to 30x inference speedup and 25x lower energy costs for generative AI workloads.",
                "publisher": "NVIDIA Newsroom",
                "author": "NVIDIA Corporate",
                "published_at": datetime.datetime.utcnow() - datetime.timedelta(days=4),
            },
            {
                "provider_id": "newsapi",
                "canonical_url": "https://www.reuters.com/technology/nvidia-ceo-says-blackwell-chips-are-full-production-demand-is-insane-2024-10-02/",
                "original_url": "https://www.reuters.com/technology/nvidia-ceo-says-blackwell-chips-are-full-production-demand-is-insane-2024-10-02/",
                "headline": "Nvidia CEO says Blackwell chips are in full production, demand is 'insane'",
                "description": "Nvidia Chief Executive Jensen Huang said the company's next-generation Blackwell artificial intelligence chip is in full production.",
                "publisher": "Reuters",
                "author": "Reuters Staff",
                "published_at": datetime.datetime.utcnow() - datetime.timedelta(days=4),
            }
        ],
        "claims": [
            {
                "claim_text": "GB200 NVL72 rack integrates 72 Blackwell GPUs and 36 Grace CPUs with 130 TB/s unified NVLink fabric.",
                "claim_type": "technical_metric",
                "verification_status": "VERIFIED",
                "supporting_evidence": "NVIDIA official hardware architecture whitepaper and Hot Chips 2024 technical presentation.",
                "conflicting_evidence": None,
                "missing_evidence": None,
                "evidence_urls": ["https://nvidianews.nvidia.com/news/nvidia-blackwell-platform-arrives"]
            },
            {
                "claim_text": "Inference token generation cost reduced up to 25x compared to H100 on FP4 precision.",
                "claim_type": "technical_metric",
                "verification_status": "CORROBORATED",
                "supporting_evidence": "NVIDIA benchmark reports; independent cloud host verification pending customer cluster rollout.",
                "conflicting_evidence": None,
                "missing_evidence": "Independent MLPerf v4.1 verification on full 72-GPU liquid cooled racks.",
                "evidence_urls": ["https://www.reuters.com/technology/nvidia-ceo-says-blackwell-chips-are-full-production-demand-is-insane-2024-10-02/"]
            }
        ],
        "entities": [
            {
                "name": "NVIDIA", "entity_type": "company", "role": "Accelerated Computing Pioneer",
                "organization": "NVIDIA Corporation", "story_role": "creator",
                "direct_involvement": "Architecture designer and supplier",
                "ticker_symbol": "NVDA", "exchange": "NASDAQ", "is_confirmed_exposure": True
            },
            {
                "name": "Jensen Huang", "entity_type": "person", "role": "CEO & Founder",
                "organization": "NVIDIA", "story_role": "announcer",
                "direct_involvement": "Public executive disclosures regarding full production ramp",
                "ticker_symbol": None, "exchange": None, "is_confirmed_exposure": True
            },
            {
                "name": "TSMC", "entity_type": "company", "role": "Semiconductor Foundry",
                "organization": "Taiwan Semiconductor Manufacturing Co", "story_role": "partner",
                "direct_involvement": "CoWoS-L advanced packaging and 4NP wafer fab",
                "ticker_symbol": "TSM", "exchange": "NYSE", "is_confirmed_exposure": True
            }
        ],
        "industry_impacts": [
            {
                "industry_name": "Semiconductors/Hardware",
                "impact_direction": "positive",
                "impact_magnitude": "transformative",
                "time_horizon": "immediate",
                "mechanism": "Secures massive capital expenditure backlog across hyperscalers and OEM server makers.",
                "potential_beneficiaries": "TSMC, SK Hynix, Micron, Vertiv, Supermicro",
                "disrupted_models": "Air-cooled standard server rack architectures",
                "workforce_task_exposure": "Thermal engineering, high-density power delivery design",
                "workforce_augmentation_vs_displacement": "Substantial job creation in advanced packaging and datacenter facilities",
                "confidence_level": "high"
            },
            {
                "industry_name": "Energy/Utilities",
                "impact_direction": "positive",
                "impact_magnitude": "high",
                "time_horizon": "near_term",
                "mechanism": "Rack densities of 100kW+ compel long-term Power Purchase Agreements (PPAs) with nuclear and clean power operators.",
                "potential_beneficiaries": "Constellation Energy (CEG), Vistra, Talen Energy",
                "disrupted_models": "Regional grid operators lacking high-voltage interconnect capacity",
                "workforce_task_exposure": "Power distribution engineering, environmental permitting",
                "workforce_augmentation_vs_displacement": "Direct hiring surge in utility substation engineering",
                "confidence_level": "high"
            }
        ],
        "score_breakdown": {
            "news_coverage_growth": 23.0, "public_discussion": 21.8, "search_interest": 17.5,
            "developer_research_activity": 12.0, "recency_acceleration": 12.5, "trending_total": 86.8,
            "market_economic_impact": 25.0, "technical_significance": 19.5, "trend_momentum": 13.0,
            "industry_disruption": 14.5, "strategic_importance": 10.0, "evidence_strength": 10.0,
            "time_sensitivity": 4.0, "market_total": 96.0,
            "scoring_rationale": "Highest market capital reallocation event in tech history; drives global energy procurement and semiconductor packaging capacity.",
            "scoring_version": "v1.0"
        },
        "sources": [
            {
                "title": "NVIDIA Blackwell Architecture Whitepaper",
                "publisher": "NVIDIA",
                "url": "https://nvidianews.nvidia.com/news/nvidia-blackwell-platform-arrives",
                "source_type": "official_announcement",
                "access_status": "accessed_and_verified",
                "claims_supported": "GB200 specifications and NVLink 5 bandwidth"
            },
            {
                "title": "Reuters: Blackwell Full Production Ramp",
                "publisher": "Reuters",
                "url": "https://www.reuters.com/technology/nvidia-ceo-says-blackwell-chips-are-full-production-demand-is-insane-2024-10-02/",
                "source_type": "independent_news",
                "access_status": "accessed_and_verified",
                "claims_supported": "CEO statement on manufacturing ramp and order demand"
            }
        ]
    },
    {
        "title": "OpenAI Launches o1 Reasoning Model Series with Test-Time Compute Scaling",
        "summary": "OpenAI introduced 'o1' (formerly Project Strawberry), a new model family trained via reinforcement learning to generate internal chains of thought before responding, exhibiting major gains on competitive math (AIME), code generation, and PhD-level science benchmarks.",
        "what_happened": "OpenAI published the o1-preview and o1-mini models to ChatGPT Plus and API subscribers, changing the paradigm from pure pre-training scaling to inference-time reasoning compute.",
        "what_is_new": "Hides the internal chain of thought while letting the model spend dynamic compute time thinking through complex logical steps before generating final output.",
        "event_date": datetime.datetime.utcnow() - datetime.timedelta(days=7),
        "verification_status": "VERIFIED",
        "verification_rationale": "Verified through accessible public API endpoints, OpenAI system card, and extensive third-party competitive coding and mathematics evaluations.",
        "trending_score": 89.2,
        "trending_label": "PERSISTENT",
        "market_importance_score": 93.2,
        "trending_rank": 3,
        "market_rank": 3,
        "is_emerging_signal": False,
        "next_milestones": "Integration of image reasoning into full o1; empirical cost-benefit analyses of inference compute vs pre-training tokens.",
        "articles": [
            {
                "provider_id": "official_feed",
                "canonical_url": "https://openai.com/index/introducing-openai-o1-preview/",
                "original_url": "https://openai.com/index/introducing-openai-o1-preview/",
                "headline": "Learning to Reason with LLMs: Introducing OpenAI o1",
                "description": "We have developed a new series of AI models designed to spend more time thinking before they respond. They can reason through complex tasks and solve harder problems than previous models in science, coding, and math.",
                "publisher": "OpenAI",
                "author": "OpenAI Research",
                "published_at": datetime.datetime.utcnow() - datetime.timedelta(days=7),
            }
        ],
        "claims": [
            {
                "claim_text": "Solves 83% of problems in International Mathematical Olympiad (IMO) qualifying exam vs 13% for GPT-4o.",
                "claim_type": "technical_metric",
                "verification_status": "CORROBORATED",
                "supporting_evidence": "OpenAI System Card with benchmark distribution graphs and competitive programmer verification.",
                "conflicting_evidence": None,
                "missing_evidence": "Hidden reasoning tokens prevent independent inspection of exact intermediate deliberation steps.",
                "evidence_urls": ["https://openai.com/index/introducing-openai-o1-preview/"]
            }
        ],
        "entities": [
            {
                "name": "OpenAI", "entity_type": "company", "role": "Frontier AI Lab",
                "organization": "OpenAI", "story_role": "creator",
                "direct_involvement": "Primary model developer",
                "ticker_symbol": None, "exchange": None, "is_confirmed_exposure": True
            },
            {
                "name": "Microsoft", "entity_type": "company", "role": "Hyperscale Partner",
                "organization": "Microsoft", "story_role": "investor",
                "direct_involvement": "Exclusive cloud infrastructure and commercial integration",
                "ticker_symbol": "MSFT", "exchange": "NASDAQ", "is_confirmed_exposure": True
            }
        ],
        "industry_impacts": [
            {
                "industry_name": "Software/SaaS",
                "impact_direction": "positive",
                "impact_magnitude": "high",
                "time_horizon": "immediate",
                "mechanism": "Significantly lowers error rates on complex multi-file architectural refactors and algorithm design.",
                "potential_beneficiaries": "Engineering teams building automated code verification and formal proof tools",
                "disrupted_models": "Simple wrapper coding assistants lacking test-time reasoning loops",
                "workforce_task_exposure": "Algorithmic problem solving, complex debug tracing",
                "workforce_augmentation_vs_displacement": "Major productivity boost for senior software architects",
                "confidence_level": "high"
            },
            {
                "industry_name": "Healthcare/Biotech",
                "impact_direction": "positive",
                "impact_magnitude": "high",
                "time_horizon": "near_term",
                "mechanism": "Enables multi-step scientific hypothesis evaluation and genetic sequence analysis.",
                "potential_beneficiaries": "Computational biology labs and pharmaceutical research pipelines",
                "disrupted_models": "Manual literature meta-analysis",
                "workforce_task_exposure": "Scientific literature cross-referencing and experimental protocol design",
                "workforce_augmentation_vs_displacement": "Augmentation of post-doctoral researchers",
                "confidence_level": "medium"
            }
        ],
        "score_breakdown": {
            "news_coverage_growth": 23.5, "public_discussion": 23.2, "search_interest": 17.5,
            "developer_research_activity": 13.5, "recency_acceleration": 11.5, "trending_total": 89.2,
            "market_economic_impact": 24.0, "technical_significance": 19.8, "trend_momentum": 13.4,
            "industry_disruption": 13.5, "strategic_importance": 8.5, "evidence_strength": 9.5,
            "time_sensitivity": 4.5, "market_total": 93.2,
            "scoring_rationale": "Proves inference-time compute scaling laws; establishes new paradigm for autonomous technical reasoning.",
            "scoring_version": "v1.0"
        },
        "sources": [
            {
                "title": "OpenAI Research: Learning to Reason with LLMs",
                "publisher": "OpenAI",
                "url": "https://openai.com/index/introducing-openai-o1-preview/",
                "source_type": "official_announcement",
                "access_status": "accessed_and_verified",
                "claims_supported": "o1 benchmark results and reinforcement learning system card"
            }
        ]
    },
    {
        "title": "Unverified Startup Claims Fully Autonomous Self-Replicating AGI in Closed Lab Trial",
        "summary": "A stealth startup claimed on social media to have achieved an autonomous, recursive self-improving AGI agent operating across decentralized nodes. No technical report, source code, reproducible demonstration, or third-party audit was provided.",
        "what_happened": "Viral social media posts and speculative blog articles claimed an undisclosed breakthrough in recursive self-improving superintelligence.",
        "what_is_new": "Bold assertions of autonomous code modification and recursive capability gains with zero external verification.",
        "event_date": datetime.datetime.utcnow() - datetime.timedelta(days=1),
        "verification_status": "UNVERIFIED",
        "verification_rationale": "Zero primary technical reports, reproducible code, or accredited third-party evaluations. Classified strictly as an unverified emerging signal to prevent misleading confirmed news rankings.",
        "trending_score": 74.5,
        "trending_label": "EMERGING",
        "market_importance_score": 68.0,
        "trending_rank": None,
        "market_rank": None,
        "is_emerging_signal": True,
        "next_milestones": "Independent verification by academic institutions or release of inspectable benchmarks.",
        "articles": [
            {
                "provider_id": "newsapi",
                "canonical_url": "https://example.com/unverified-agi-claim-rumor",
                "original_url": "https://example.com/unverified-agi-claim-rumor",
                "headline": "Viral Social Media Posts Claim Stealth Lab Has Reached AGI",
                "description": "Speculation mounts as anonymous developers assert self-improving agent breakthroughs without verifiable technical proof.",
                "publisher": "Tech Speculator Blog",
                "author": "Anonymous Reporter",
                "published_at": datetime.datetime.utcnow() - datetime.timedelta(days=1),
            }
        ],
        "claims": [
            {
                "claim_text": "The model autonomously refactored its own weights and improved its reasoning benchmarks recursively by 40%.",
                "claim_type": "prediction_opinion",
                "verification_status": "UNVERIFIED",
                "supporting_evidence": "Unsubstantiated claims in viral video clip.",
                "conflicting_evidence": "No independent researcher has been granted access; no checkpoint or logs provided.",
                "missing_evidence": "Complete absence of peer evaluation, public code repository, or benchmark logs.",
                "evidence_urls": ["https://example.com/unverified-agi-claim-rumor"]
            }
        ],
        "entities": [
            {
                "name": "Synthetix Stealth Lab", "entity_type": "company", "role": "Unregistered Startup",
                "organization": "Unknown", "story_role": "announcer",
                "direct_involvement": "Origin of viral video",
                "ticker_symbol": None, "exchange": None, "is_confirmed_exposure": False
            }
        ],
        "industry_impacts": [
            {
                "industry_name": "Software/SaaS",
                "impact_direction": "uncertain",
                "impact_magnitude": "transformative",
                "time_horizon": "long_term",
                "mechanism": "Hypothetical recursive self-improvement would upend entire software lifecycle.",
                "potential_beneficiaries": "Speculative",
                "disrupted_models": "All traditional software engineering if verified",
                "workforce_task_exposure": "All intellectual tasks",
                "workforce_augmentation_vs_displacement": "Theoretical total displacement (unsubstantiated)",
                "confidence_level": "speculative"
            }
        ],
        "score_breakdown": {
            "news_coverage_growth": 14.0, "public_discussion": 22.0, "search_interest": 16.5,
            "developer_research_activity": 4.0, "recency_acceleration": 14.0, "trending_total": 74.5,
            "market_economic_impact": 18.0, "technical_significance": 14.0, "trend_momentum": 11.0,
            "industry_disruption": 14.0, "strategic_importance": 6.0, "evidence_strength": 2.0,
            "time_sensitivity": 3.0, "market_total": 68.0,
            "scoring_rationale": "High speculative buzz but penalized to near-zero on evidence strength (2/10). Flagged as emerging signal.",
            "scoring_version": "v1.0"
        },
        "sources": [
            {
                "title": "Viral Post and Speculative Coverage",
                "publisher": "Tech Speculator Blog",
                "url": "https://example.com/unverified-agi-claim-rumor",
                "source_type": "independent_news",
                "access_status": "accessed_inconclusive",
                "claims_supported": "Uncorroborated social video claims"
            }
        ]
    }
]
