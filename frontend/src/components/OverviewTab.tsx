import React from 'react';
import {
  TrendingUp, Award, AlertTriangle, ShieldCheck, Clock,
  ArrowUpRight, ArrowDownRight, ArrowRight, Building2, ExternalLink
} from 'lucide-react';
import { Story, Leaderboards, Analytics, SystemHealth } from '../types';

interface OverviewTabProps {
  leaderboards: Leaderboards | null;
  analytics: Analytics | null;
  systemHealth: SystemHealth | null;
  onSelectStory: (id: number) => void;
  onNavigateFeed: (filter?: any) => void;
}

export const OverviewTab: React.FC<OverviewTabProps> = ({
  leaderboards,
  analytics,
  systemHealth,
  onSelectStory,
  onNavigateFeed
}) => {
  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'VERIFIED':
        return 'bg-emerald-950 text-emerald-400 border-emerald-800';
      case 'CORROBORATED':
        return 'bg-cyan-950 text-cyan-400 border-cyan-800';
      case 'PARTIALLY VERIFIED':
        return 'bg-amber-950 text-amber-400 border-amber-800';
      case 'DISPUTED':
        return 'bg-orange-950 text-orange-400 border-orange-800';
      case 'FALSE OR DEBUNKED':
        return 'bg-red-950 text-red-400 border-red-800';
      default:
        return 'bg-gray-800 text-gray-300 border-gray-700';
    }
  };

  return (
    <div className="space-y-8 pb-12">
      {/* Top Intelligence Stats Banner */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-4 rounded-2xl bg-gray-900/60 border border-gray-800 backdrop-blur-sm">
          <div className="flex items-center justify-between text-gray-400 text-xs mb-1">
            <span>Canonical Stories</span>
            <Award className="h-4 w-4 text-teal-400" />
          </div>
          <div className="text-2xl font-bold text-white">
            {analytics?.total_stories ?? '...'}
          </div>
          <div className="text-[11px] text-gray-500 mt-1">
            Across {analytics?.total_articles ?? '...'} monitored articles
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-gray-900/60 border border-gray-800 backdrop-blur-sm">
          <div className="flex items-center justify-between text-gray-400 text-xs mb-1">
            <span>Verified & Corroborated</span>
            <ShieldCheck className="h-4 w-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-emerald-400">
            {((analytics?.verification_counts?.['VERIFIED'] || 0) + (analytics?.verification_counts?.['CORROBORATED'] || 0))}
          </div>
          <div className="text-[11px] text-gray-500 mt-1">
            Supported by primary lab / repo evidence
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-gray-900/60 border border-gray-800 backdrop-blur-sm">
          <div className="flex items-center justify-between text-gray-400 text-xs mb-1">
            <span>Emerging Signals</span>
            <AlertTriangle className="h-4 w-4 text-purple-400" />
          </div>
          <div className="text-2xl font-bold text-purple-300">
            {leaderboards?.emerging_signals.length ?? 0}
          </div>
          <div className="text-[11px] text-gray-500 mt-1">
            Isolated unverified high-impact items
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-gray-900/60 border border-gray-800 backdrop-blur-sm">
          <div className="flex items-center justify-between text-gray-400 text-xs mb-1">
            <span>Data Freshness</span>
            <Clock className="h-4 w-4 text-cyan-400" />
          </div>
          <div className="text-sm font-bold text-cyan-300 mt-1 truncate">
            {systemHealth?.last_ingestion_time
              ? new Date(systemHealth.last_ingestion_time).toLocaleTimeString()
              : 'Active Session'}
          </div>
          <div className="text-[11px] text-gray-500 mt-1 flex items-center space-x-1">
            <span className="h-2 w-2 rounded-full bg-emerald-400"></span>
            <span>Scheduler Active (6h Interval)</span>
          </div>
        </div>
      </div>

      {/* Dual Independent Leaderboards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Trending Score Leaderboard */}
        <div className="p-6 rounded-2xl bg-gray-900/50 border border-gray-800 flex flex-col justify-between space-y-4">
          <div className="flex items-center justify-between border-b border-gray-800 pb-3">
            <div className="flex items-center space-x-2">
              <TrendingUp className="h-5 w-5 text-teal-400" />
              <h2 className="text-base font-bold text-white">Top Trending AI News Leaderboard</h2>
            </div>
            <span className="text-[11px] text-gray-400 font-mono">Weighted 0-100</span>
          </div>

          <div className="space-y-3 flex-1">
            {leaderboards?.trending_leaderboard.slice(0, 5).map((story, idx) => (
              <div
                key={story.id}
                onClick={() => onSelectStory(story.id)}
                className="p-3.5 rounded-xl bg-gray-900/80 hover:bg-gray-800/80 border border-gray-800 hover:border-teal-500/40 transition cursor-pointer flex items-center justify-between group"
              >
                <div className="flex items-center space-x-3 pr-2">
                  <div className="h-7 w-7 rounded-lg bg-teal-950/80 text-teal-300 font-bold text-xs flex items-center justify-center border border-teal-800/50 flex-shrink-0">
                    #{idx + 1}
                  </div>
                  <div>
                    <h3 className="text-xs sm:text-sm font-semibold text-gray-100 group-hover:text-teal-300 transition line-clamp-1">
                      {story.title}
                    </h3>
                    <div className="flex items-center space-x-2 text-[11px] text-gray-400 mt-0.5">
                      <span className={`px-1.5 py-0.2 rounded border text-[10px] ${getStatusBadge(story.verification_status)}`}>
                        {story.verification_status}
                      </span>
                      <span>• {story.trending_label}</span>
                    </div>
                  </div>
                </div>
                <div className="text-right flex-shrink-0 pl-2">
                  <div className="text-sm font-bold text-teal-400">{story.trending_score}</div>
                  <div className="text-[10px] text-gray-500">Mkt: {story.market_importance_score}</div>
                </div>
              </div>
            ))}
          </div>

          <button
            onClick={() => onNavigateFeed({ sort_by: 'trending' })}
            className="w-full text-center text-xs font-semibold py-2 text-teal-400 hover:text-teal-300 transition flex items-center justify-center space-x-1"
          >
            <span>View Full Trending Leaderboard</span>
            <ArrowRight className="h-3.5 w-3.5" />
          </button>
        </div>

        {/* Market Importance Score Leaderboard */}
        <div className="p-6 rounded-2xl bg-gray-900/50 border border-gray-800 flex flex-col justify-between space-y-4">
          <div className="flex items-center justify-between border-b border-gray-800 pb-3">
            <div className="flex items-center space-x-2">
              <Award className="h-5 w-5 text-cyan-400" />
              <h2 className="text-base font-bold text-white">Top Market Importance Leaderboard</h2>
            </div>
            <span className="text-[11px] text-gray-400 font-mono">Weighted 0-100</span>
          </div>

          <div className="space-y-3 flex-1">
            {leaderboards?.market_leaderboard.slice(0, 5).map((story, idx) => (
              <div
                key={story.id}
                onClick={() => onSelectStory(story.id)}
                className="p-3.5 rounded-xl bg-gray-900/80 hover:bg-gray-800/80 border border-gray-800 hover:border-cyan-500/40 transition cursor-pointer flex items-center justify-between group"
              >
                <div className="flex items-center space-x-3 pr-2">
                  <div className="h-7 w-7 rounded-lg bg-cyan-950/80 text-cyan-300 font-bold text-xs flex items-center justify-center border border-cyan-800/50 flex-shrink-0">
                    #{idx + 1}
                  </div>
                  <div>
                    <h3 className="text-xs sm:text-sm font-semibold text-gray-100 group-hover:text-cyan-300 transition line-clamp-1">
                      {story.title}
                    </h3>
                    <div className="flex items-center space-x-2 text-[11px] text-gray-400 mt-0.5">
                      <span className={`px-1.5 py-0.2 rounded border text-[10px] ${getStatusBadge(story.verification_status)}`}>
                        {story.verification_status}
                      </span>
                      {story.entities?.[0]?.ticker_symbol && (
                        <span className="font-mono text-cyan-300 text-[10px]">
                          ${story.entities[0].ticker_symbol}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
                <div className="text-right flex-shrink-0 pl-2">
                  <div className="text-sm font-bold text-cyan-400">{story.market_importance_score}</div>
                  <div className="text-[10px] text-gray-500">Trend: {story.trending_score}</div>
                </div>
              </div>
            ))}
          </div>

          <button
            onClick={() => onNavigateFeed({ sort_by: 'market' })}
            className="w-full text-center text-xs font-semibold py-2 text-cyan-400 hover:text-cyan-300 transition flex items-center justify-center space-x-1"
          >
            <span>View Full Market Importance Leaderboard</span>
            <ArrowRight className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>

      {/* High-Impact Emerging Signals Banner (Prompt Requirement) */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-purple-950/40 via-gray-900 to-gray-900 border border-purple-900/50 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <AlertTriangle className="h-5 w-5 text-purple-400" />
            <div>
              <h2 className="text-sm font-bold text-white">Isolated Emerging Signals & Speculative Claims</h2>
              <p className="text-xs text-gray-400">
                Segregated from confirmed rankings so unverified or disputed claims never appear as established facts.
              </p>
            </div>
          </div>
          <span className="text-[11px] font-semibold px-2.5 py-1 rounded-full bg-purple-900/60 text-purple-200 border border-purple-700">
            STRICT ISOLATION
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {leaderboards?.emerging_signals.map((signal) => (
            <div
              key={signal.id}
              onClick={() => onSelectStory(signal.id)}
              className="p-4 rounded-xl bg-gray-950/70 border border-purple-900/40 hover:border-purple-600 transition cursor-pointer space-y-2 group"
            >
              <div className="flex items-center justify-between">
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${getStatusBadge(signal.verification_status)}`}>
                  {signal.verification_status}
                </span>
                <span className="text-xs font-bold text-purple-300">
                  Market Score: {signal.market_importance_score}
                </span>
              </div>
              <h3 className="text-xs sm:text-sm font-semibold text-gray-100 group-hover:text-purple-300 transition">
                {signal.title}
              </h3>
              <p className="text-xs text-gray-400 line-clamp-2">
                {signal.summary}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Major Industry Impact Signals */}
      <div className="p-6 rounded-2xl bg-gray-900/40 border border-gray-800 space-y-4">
        <h2 className="text-sm font-bold text-white">Top Impacted Economic Sectors</h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
          {analytics?.top_industries_exposed.map((item, idx) => (
            <div
              key={idx}
              onClick={() => onNavigateFeed({ industry: item.industry })}
              className="p-3 rounded-xl bg-gray-900/80 border border-gray-800 hover:border-teal-500/40 transition cursor-pointer text-center group"
            >
              <span className="text-xs font-semibold text-gray-200 group-hover:text-teal-300 block truncate">
                {item.industry}
              </span>
              <span className="text-sm font-bold text-teal-400 mt-1 block">
                {item.count} stories
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
