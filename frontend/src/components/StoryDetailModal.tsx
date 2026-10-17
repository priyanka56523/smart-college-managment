import React, { useEffect, useState } from 'react';
import {
  X, ShieldCheck, CheckCircle2, AlertTriangle, AlertCircle, TrendingUp,
  DollarSign, ExternalLink, Calendar, Building2, User, Cpu, History, ArrowRight
} from 'lucide-react';
import { StoryDetail } from '../types';
import { fetchStoryDetail } from '../api';

interface StoryDetailModalProps {
  storyId: number | null;
  onClose: () => void;
}

export const StoryDetailModal: React.FC<StoryDetailModalProps> = ({ storyId, onClose }) => {
  const [story, setStory] = useState<StoryDetail | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!storyId) {
      setStory(null);
      return;
    }
    setLoading(true);
    setError(null);
    fetchStoryDetail(storyId)
      .then(setStory)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [storyId]);

  if (!storyId) return null;

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'VERIFIED':
        return 'bg-emerald-950/80 text-emerald-400 border-emerald-800';
      case 'CORROBORATED':
        return 'bg-cyan-950/80 text-cyan-400 border-cyan-800';
      case 'PARTIALLY VERIFIED':
        return 'bg-amber-950/80 text-amber-400 border-amber-800';
      case 'DISPUTED':
        return 'bg-orange-950/80 text-orange-400 border-orange-800';
      case 'FALSE OR DEBUNKED':
        return 'bg-red-950/80 text-red-400 border-red-800';
      default:
        return 'bg-gray-800 text-gray-300 border-gray-700';
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-black/80 backdrop-blur-md">
      <div className="bg-[#111827] border border-gray-800 rounded-2xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="flex items-start justify-between px-6 py-5 border-b border-gray-800 bg-[#0f172a]/70">
          <div className="space-y-1.5 pr-4">
            <div className="flex items-center space-x-2.5 flex-wrap gap-y-1">
              {story && (
                <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full border ${getStatusColor(story.verification_status)}`}>
                  {story.verification_status}
                </span>
              )}
              {story?.is_emerging_signal && (
                <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-purple-950 text-purple-300 border border-purple-800">
                  ISOLATED EMERGING SIGNAL
                </span>
              )}
              {story?.event_date && (
                <span className="text-xs text-gray-400 flex items-center space-x-1">
                  <Calendar className="h-3.5 w-3.5" />
                  <span>{new Date(story.event_date).toLocaleDateString()}</span>
                </span>
              )}
            </div>
            <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
              {story?.title || 'Loading Story Intelligence Dossier...'}
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 transition"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 overflow-y-auto space-y-8 flex-1 text-gray-200">
          {loading && (
            <div className="py-20 flex flex-col items-center justify-center space-y-3">
              <div className="h-8 w-8 border-2 border-teal-500 border-t-transparent rounded-full animate-spin"></div>
              <p className="text-sm text-gray-400">Loading verified intelligence dossier...</p>
            </div>
          )}

          {error && (
            <div className="p-4 rounded-xl bg-red-950/40 border border-red-800 text-red-300 text-sm">
              {error}
            </div>
          )}

          {story && (
            <>
              {/* Executive What Happened vs What is New */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded-xl bg-gray-900/80 border border-gray-800 space-y-2">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-teal-400">What Happened</h3>
                  <p className="text-sm text-gray-300 leading-relaxed">
                    {story.what_happened || story.summary}
                  </p>
                </div>
                <div className="p-4 rounded-xl bg-gray-900/80 border border-gray-800 space-y-2">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-cyan-400">What Is New & Differentiated</h3>
                  <p className="text-sm text-gray-300 leading-relaxed">
                    {story.what_is_new || "Analysis indicates continuation of existing architectural scaling."}
                  </p>
                </div>
              </div>

              {/* Verification Assessment Rationale */}
              <div className="p-4 rounded-xl bg-gradient-to-r from-gray-900 via-gray-900/80 to-[#0e1726] border border-gray-800 space-y-2">
                <div className="flex items-center space-x-2">
                  <ShieldCheck className="h-4 w-4 text-emerald-400" />
                  <h3 className="text-sm font-semibold text-white">Verification Assessment Rationale</h3>
                </div>
                <p className="text-xs text-gray-300 leading-relaxed">
                  {story.verification_rationale || "Evaluated by multi-source corroboration engine."}
                </p>
                {story.previous_status && (
                  <p className="text-[11px] text-amber-400/80">
                    Previous Status: {story.previous_status} (Reassessed upon new evidence intake)
                  </p>
                )}
              </div>

              {/* Dual Score Breakdown Rubric */}
              <div className="space-y-3">
                <h3 className="text-sm font-bold text-gray-100 flex items-center space-x-2">
                  <TrendingUp className="h-4 w-4 text-teal-400" />
                  <span>Deterministic Score Breakdown (Rubric {story.score_breakdown?.scoring_version || 'v1.0'})</span>
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Trending Score Card */}
                  <div className="p-4 rounded-xl bg-gray-900/70 border border-gray-800 space-y-3">
                    <div className="flex items-center justify-between border-b border-gray-800 pb-2">
                      <span className="font-semibold text-teal-300 text-sm">Trending Score</span>
                      <span className="text-lg font-bold text-teal-400">{story.trending_score}/100</span>
                    </div>
                    {story.score_breakdown && (
                      <div className="space-y-1.5 text-xs">
                        <div className="flex justify-between text-gray-400">
                          <span>News Coverage Growth:</span>
                          <span className="text-gray-200">{story.score_breakdown.news_coverage_growth} / 25</span>
                        </div>
                        <div className="flex justify-between text-gray-400">
                          <span>Public Discussion & Engagement:</span>
                          <span className="text-gray-200">{story.score_breakdown.public_discussion} / 25</span>
                        </div>
                        <div className="flex justify-between text-gray-400">
                          <span>Search-Interest Growth:</span>
                          <span className="text-gray-200">{story.score_breakdown.search_interest} / 20</span>
                        </div>
                        <div className="flex justify-between text-gray-400">
                          <span>Developer & Research Activity:</span>
                          <span className="text-gray-200">{story.score_breakdown.developer_research_activity} / 15</span>
                        </div>
                        <div className="flex justify-between text-gray-400">
                          <span>Recency & Acceleration:</span>
                          <span className="text-gray-200">{story.score_breakdown.recency_acceleration} / 15</span>
                        </div>
                      </div>
                    )}
                    <span className="text-[11px] font-medium px-2 py-0.5 rounded bg-teal-950 text-teal-300 border border-teal-800/50 inline-block">
                      Label: {story.trending_label}
                    </span>
                  </div>

                  {/* Market Importance Card */}
                  <div className="p-4 rounded-xl bg-gray-900/70 border border-gray-800 space-y-3">
                    <div className="flex items-center justify-between border-b border-gray-800 pb-2">
                      <span className="font-semibold text-cyan-300 text-sm">Market Importance Score</span>
                      <span className="text-lg font-bold text-cyan-400">{story.market_importance_score}/100</span>
                    </div>
                    {story.score_breakdown && (
                      <div className="space-y-1.5 text-xs">
                        <div className="flex justify-between text-gray-400">
                          <span>Economic & Capital Impact:</span>
                          <span className="text-gray-200">{story.score_breakdown.market_economic_impact} / 25</span>
                        </div>
                        <div className="flex justify-between text-gray-400">
                          <span>Technical/Scientific Significance:</span>
                          <span className="text-gray-200">{story.score_breakdown.technical_significance} / 20</span>
                        </div>
                        <div className="flex justify-between text-gray-400">
                          <span>Trend Momentum:</span>
                          <span className="text-gray-200">{story.score_breakdown.trend_momentum} / 15</span>
                        </div>
                        <div className="flex justify-between text-gray-400">
                          <span>Industry Disruption Potential:</span>
                          <span className="text-gray-200">{story.score_breakdown.industry_disruption} / 15</span>
                        </div>
                        <div className="flex justify-between text-gray-400">
                          <span>Strategic & Geopolitical Weight:</span>
                          <span className="text-gray-200">{story.score_breakdown.strategic_importance} / 10</span>
                        </div>
                        <div className="flex justify-between text-gray-400">
                          <span>Evidence Strength:</span>
                          <span className="text-gray-200">{story.score_breakdown.evidence_strength} / 10</span>
                        </div>
                        <div className="flex justify-between text-gray-400">
                          <span>Time Sensitivity:</span>
                          <span className="text-gray-200">{story.score_breakdown.time_sensitivity} / 5</span>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Claim-by-Claim Verification */}
              <div className="space-y-3">
                <h3 className="text-sm font-bold text-gray-100 flex items-center space-x-2">
                  <CheckCircle2 className="h-4 w-4 text-emerald-400" />
                  <span>Claim-by-Claim Verification</span>
                </h3>
                <div className="space-y-3">
                  {story.claims.map((claim) => (
                    <div
                      key={claim.id}
                      className="p-4 rounded-xl bg-gray-900/60 border border-gray-800 space-y-2"
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-semibold px-2 py-0.5 rounded bg-gray-800 text-gray-300">
                          {claim.claim_type.replace('_', ' ').toUpperCase()}
                        </span>
                        <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full border ${getStatusColor(claim.verification_status)}`}>
                          {claim.verification_status}
                        </span>
                      </div>
                      <p className="text-sm font-medium text-white">{claim.claim_text}</p>
                      
                      {claim.supporting_evidence && (
                        <div className="text-xs text-emerald-300/90 bg-emerald-950/30 p-2 rounded border border-emerald-900/40">
                          <strong>Supporting Evidence: </strong>{claim.supporting_evidence}
                        </div>
                      )}
                      {claim.conflicting_evidence && (
                        <div className="text-xs text-red-300 bg-red-950/30 p-2 rounded border border-red-900/40">
                          <strong>Counterevidence: </strong>{claim.conflicting_evidence}
                        </div>
                      )}
                      {claim.missing_evidence && (
                        <div className="text-xs text-amber-300/90 bg-amber-950/30 p-2 rounded border border-amber-900/40">
                          <strong>Missing Evidence / Uncertainty: </strong>{claim.missing_evidence}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* People & Organizations */}
              <div className="space-y-3">
                <h3 className="text-sm font-bold text-gray-100 flex items-center space-x-2">
                  <Building2 className="h-4 w-4 text-cyan-400" />
                  <span>People & Organizations Involved</span>
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
                  {story.entities.map((entity) => (
                    <div
                      key={entity.id}
                      className="p-3 rounded-xl bg-gray-900/70 border border-gray-800 space-y-1.5"
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-sm text-white">{entity.name}</span>
                        {entity.ticker_symbol ? (
                          <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-800">
                            {entity.exchange}: {entity.ticker_symbol}
                          </span>
                        ) : (
                          <span className="text-[10px] text-gray-500 uppercase">{entity.entity_type}</span>
                        )}
                      </div>
                      <div className="text-xs text-gray-400">
                        {entity.role || entity.organization || 'Key Contributor'} • <span className="text-teal-400">{entity.story_role}</span>
                      </div>
                      {entity.direct_involvement && (
                        <p className="text-[11px] text-gray-300 line-clamp-2">
                          {entity.direct_involvement}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Industry & Workforce Impact */}
              <div className="space-y-3">
                <h3 className="text-sm font-bold text-gray-100 flex items-center space-x-2">
                  <Cpu className="h-4 w-4 text-teal-400" />
                  <span>Economic Sector & Workforce Transformation Analysis</span>
                </h3>
                <div className="space-y-3">
                  {story.industry_impacts.map((impact) => (
                    <div
                      key={impact.id}
                      className="p-4 rounded-xl bg-gray-900/70 border border-gray-800 space-y-2.5"
                    >
                      <div className="flex items-center justify-between flex-wrap gap-2">
                        <span className="font-bold text-sm text-teal-300">{impact.industry_name}</span>
                        <div className="flex items-center space-x-2 text-xs">
                          <span className="px-2 py-0.5 rounded bg-gray-800 text-gray-300 border border-gray-700">
                            Horizon: {impact.time_horizon.replace('_', ' ')}
                          </span>
                          <span className="px-2 py-0.5 rounded bg-gray-800 text-gray-300 border border-gray-700">
                            Magnitude: {impact.impact_magnitude}
                          </span>
                        </div>
                      </div>

                      {impact.mechanism && (
                        <p className="text-xs text-gray-300">
                          <strong className="text-gray-100">Causal Mechanism: </strong>{impact.mechanism}
                        </p>
                      )}

                      {impact.potential_beneficiaries && (
                        <p className="text-xs text-emerald-300/90">
                          <strong>Beneficiaries: </strong>{impact.potential_beneficiaries}
                        </p>
                      )}

                      {impact.disrupted_models && (
                        <p className="text-xs text-rose-300/90">
                          <strong>Disrupted Business Models: </strong>{impact.disrupted_models}
                        </p>
                      )}

                      {impact.workforce_task_exposure && (
                        <div className="p-2.5 rounded-lg bg-black/40 border border-gray-800/80 text-xs space-y-1">
                          <p className="text-cyan-300 font-medium">Workforce Exposure:</p>
                          <p className="text-gray-300">{impact.workforce_task_exposure}</p>
                          <p className="text-gray-400 text-[11px] pt-1">
                            <em>Augmentation vs Displacement: </em>{impact.workforce_augmentation_vs_displacement}
                          </p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Next Milestones */}
              {story.next_milestones && (
                <div className="p-4 rounded-xl bg-gray-900/50 border border-gray-800 space-y-1.5">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-amber-400">Next Milestones to Monitor</h4>
                  <p className="text-xs text-gray-300 leading-relaxed">{story.next_milestones}</p>
                </div>
              )}

              {/* Primary Sources & Clickable Citations */}
              <div className="space-y-3">
                <h3 className="text-sm font-bold text-gray-100 flex items-center space-x-2">
                  <ExternalLink className="h-4 w-4 text-teal-400" />
                  <span>Primary Evidence & Clickable Sources</span>
                </h3>
                <div className="space-y-2">
                  {story.sources.map((src) => (
                    <a
                      key={src.id}
                      href={src.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center justify-between p-3 rounded-xl bg-gray-900/60 hover:bg-gray-800 border border-gray-800 hover:border-teal-500/50 transition group"
                    >
                      <div className="space-y-0.5">
                        <div className="font-medium text-xs text-teal-300 group-hover:underline flex items-center space-x-1.5">
                          <span>{src.title}</span>
                          <ExternalLink className="h-3 w-3 inline text-gray-500" />
                        </div>
                        <div className="text-[11px] text-gray-400">
                          {src.publisher} • <span className="font-mono text-gray-500">{src.source_type}</span>
                        </div>
                      </div>
                      <span className="text-[11px] font-semibold px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800">
                        {src.access_status}
                      </span>
                    </a>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-gray-800 bg-[#0f172a]/70 flex justify-end">
          <button
            onClick={onClose}
            className="text-xs px-4 py-2 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-200 transition font-medium"
          >
            Close Dossier
          </button>
        </div>
      </div>
    </div>
  );
};
