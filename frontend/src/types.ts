export interface Article {
  id: number;
  provider_id: string;
  canonical_url: string;
  original_url?: string;
  headline: string;
  description?: string;
  publisher?: string;
  published_at?: string;
  collected_at: string;
  language?: string;
  retrieval_status?: string;
}

export interface Claim {
  id: number;
  claim_text: string;
  claim_type: string;
  verification_status: string;
  supporting_evidence?: string;
  conflicting_evidence?: string;
  missing_evidence?: string;
  evidence_urls: string[];
}

export interface Entity {
  id: number;
  name: string;
  entity_type: string;
  role?: string;
  organization?: string;
  story_role: string;
  direct_involvement?: string;
  public_statement?: string;
  profile_url?: string;
  ticker_symbol?: string;
  exchange?: string;
  is_confirmed_exposure: boolean;
}

export interface IndustryImpact {
  id: number;
  industry_name: string;
  impact_direction: string;
  impact_magnitude: string;
  time_horizon: string;
  mechanism?: string;
  potential_beneficiaries?: string;
  disrupted_models?: string;
  workforce_task_exposure?: string;
  workforce_augmentation_vs_displacement?: string;
  confidence_level: string;
  supporting_evidence?: string;
}

export interface ScoreBreakdown {
  news_coverage_growth: number;
  public_discussion: number;
  search_interest: number;
  developer_research_activity: number;
  recency_acceleration: number;
  trending_total: number;
  market_economic_impact: number;
  technical_significance: number;
  trend_momentum: number;
  industry_disruption: number;
  strategic_importance: number;
  evidence_strength: number;
  time_sensitivity: number;
  market_total: number;
  scoring_rationale?: string;
  scoring_version: string;
  calculated_at: string;
  coverage_limitation_notes?: string;
}

export interface RankingHistoryItem {
  id: number;
  trending_rank?: number;
  market_rank?: number;
  trending_score: number;
  market_importance_score: number;
  verification_status?: string;
  recorded_at: string;
}

export interface SourceRecord {
  id: number;
  title: string;
  publisher?: string;
  url: string;
  source_type: string;
  access_status: string;
  claims_supported?: string;
  published_date?: string;
}

export interface Story {
  id: number;
  title: string;
  summary: string;
  first_discovered_at: string;
  event_date?: string;
  last_checked_at: string;
  verification_status: string;
  trending_score: number;
  trending_label: string;
  market_importance_score: number;
  trending_rank?: number;
  market_rank?: number;
  is_emerging_signal: boolean;
  entities: Entity[];
  industry_impacts: IndustryImpact[];
  sources: SourceRecord[];
}

export interface StoryDetail extends Story {
  what_happened?: string;
  what_is_new?: string;
  verification_rationale?: string;
  previous_status?: string;
  verification_timestamp?: string;
  next_milestones?: string;
  articles: Article[];
  claims: Claim[];
  score_breakdown?: ScoreBreakdown;
  ranking_history: RankingHistoryItem[];
}

export interface Leaderboards {
  trending_leaderboard: Story[];
  market_leaderboard: Story[];
  emerging_signals: Story[];
  scoring_methodology: {
    scoring_version: string;
    trending_weights: Record<string, string>;
    market_weights: Record<string, string>;
    isolation_rule: string;
  };
}

export interface Analytics {
  total_stories: number;
  total_articles: number;
  verification_counts: Record<string, number>;
  trending_labels_counts: Record<string, number>;
  top_industries_exposed: Array<{ industry: string; count: number }>;
  top_entities: Array<{ name: string; entity_type: string; ticker?: string; occurrences: number }>;
  score_distribution: {
    high_market_impact_count: number;
    high_trending_count: number;
    emerging_signals_count: number;
  };
  data_freshness: {
    last_checked?: string;
    status: string;
  };
}

export interface IntelligenceReport {
  id: number;
  title: string;
  report_type: string;
  research_timestamp: string;
  timezone_name: string;
  coverage_period_start: string;
  coverage_period_end: string;
  sources_examined_count: number;
  coverage_gaps_notes?: string;
  executive_summary: string;
  ranked_trending_ids: number[];
  ranked_market_ids: number[];
  emerging_signals_ids: number[];
  key_developments_to_monitor?: string;
  created_at: string;
}

export interface APIConnectionResult {
  service: string;
  status: string;
  endpoint: string;
  model?: string;
  message: string;
  rate_limits?: Record<string, any>;
  account_constraints?: Record<string, any>;
}

export interface SystemHealth {
  status: string;
  timestamp: string;
  version: string;
  database: string;
  scheduler_running: boolean;
  last_ingestion_time?: string;
  integrations: APIConnectionResult[];
}
