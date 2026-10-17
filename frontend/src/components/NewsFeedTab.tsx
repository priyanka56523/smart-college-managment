import React, { useState, useEffect } from 'react';
import {
  Search, Filter, ExternalLink, Calendar, Building2, User,
  TrendingUp, Award, ShieldCheck, ChevronRight
} from 'lucide-react';
import { Story } from '../types';
import { fetchStories } from '../api';

interface NewsFeedTabProps {
  onSelectStory: (id: number) => void;
  initialFilter?: any;
}

const SECTORS = [
  'All Sectors',
  'Software/SaaS',
  'Semiconductors/Hardware',
  'Banking/Finance',
  'Healthcare/Biotech',
  'Robotics/Manufacturing',
  'Education',
  'Media/Entertainment',
  'Retail',
  'Cybersecurity/Defense',
  'Energy/Utilities',
  'Professional Services'
];

const VERIFICATION_STATUSES = [
  'All Statuses',
  'VERIFIED',
  'CORROBORATED',
  'PARTIALLY VERIFIED',
  'UNVERIFIED',
  'DISPUTED',
  'FALSE OR DEBUNKED'
];

export const NewsFeedTab: React.FC<NewsFeedTabProps> = ({ onSelectStory, initialFilter }) => {
  const [stories, setStories] = useState<Story[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('All Statuses');
  const [selectedSector, setSelectedSector] = useState(initialFilter?.industry || 'All Sectors');
  const [sortBy, setSortBy] = useState<'trending' | 'market' | 'date'>(initialFilter?.sort_by || 'trending');
  const [showEmergingOnly, setShowEmergingOnly] = useState(false);

  useEffect(() => {
    loadStories();
  }, [search, selectedStatus, selectedSector, sortBy, showEmergingOnly]);

  const loadStories = () => {
    setLoading(true);
    fetchStories({
      search: search.trim() || undefined,
      verification_status: selectedStatus !== 'All Statuses' ? selectedStatus : undefined,
      industry: selectedSector !== 'All Sectors' ? selectedSector : undefined,
      is_emerging_signal: showEmergingOnly ? true : undefined,
      sort_by: sortBy,
      limit: 50
    })
      .then(setStories)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

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
    <div className="space-y-6 pb-12">
      {/* Filter Toolbar */}
      <div className="p-4 rounded-2xl bg-gray-900/70 border border-gray-800 space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
          {/* Search box */}
          <div className="relative md:col-span-2">
            <Search className="h-4 w-4 text-gray-400 absolute left-3 top-3" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search claims, organizations, hardware, or models..."
              className="w-full pl-9 pr-4 py-2 bg-gray-950 border border-gray-800 rounded-xl text-xs sm:text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-teal-500 transition"
            />
          </div>

          {/* Verification Status Filter */}
          <div>
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="w-full px-3 py-2 bg-gray-950 border border-gray-800 rounded-xl text-xs text-gray-300 focus:outline-none focus:border-teal-500 transition"
            >
              {VERIFICATION_STATUSES.map((st) => (
                <option key={st} value={st}>{st}</option>
              ))}
            </select>
          </div>

          {/* Industry Filter */}
          <div>
            <select
              value={selectedSector}
              onChange={(e) => setSelectedSector(e.target.value)}
              className="w-full px-3 py-2 bg-gray-950 border border-gray-800 rounded-xl text-xs text-gray-300 focus:outline-none focus:border-teal-500 transition"
            >
              {SECTORS.map((sec) => (
                <option key={sec} value={sec}>{sec}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Secondary Sorting and Toggles */}
        <div className="flex items-center justify-between flex-wrap gap-2 pt-2 border-t border-gray-800/60 text-xs">
          <div className="flex items-center space-x-2">
            <span className="text-gray-400 font-medium">Rank by:</span>
            <div className="inline-flex rounded-lg border border-gray-800 bg-gray-950 p-0.5">
              <button
                onClick={() => setSortBy('trending')}
                className={`px-3 py-1 rounded-md text-xs font-semibold transition ${
                  sortBy === 'trending' ? 'bg-teal-600 text-white' : 'text-gray-400 hover:text-white'
                }`}
              >
                Trending Score
              </button>
              <button
                onClick={() => setSortBy('market')}
                className={`px-3 py-1 rounded-md text-xs font-semibold transition ${
                  sortBy === 'market' ? 'bg-cyan-600 text-white' : 'text-gray-400 hover:text-white'
                }`}
              >
                Market Importance
              </button>
              <button
                onClick={() => setSortBy('date')}
                className={`px-3 py-1 rounded-md text-xs font-semibold transition ${
                  sortBy === 'date' ? 'bg-gray-800 text-white' : 'text-gray-400 hover:text-white'
                }`}
              >
                Recency
              </button>
            </div>
          </div>

          <label className="flex items-center space-x-2 cursor-pointer text-gray-300">
            <input
              type="checkbox"
              checked={showEmergingOnly}
              onChange={(e) => setShowEmergingOnly(e.target.checked)}
              className="rounded bg-gray-950 border-gray-800 text-teal-500 focus:ring-0"
            />
            <span className="text-xs">Show Emerging Signals Only</span>
          </label>
        </div>
      </div>

      {/* Stories List */}
      <div className="space-y-4">
        {loading && (
          <div className="py-20 flex flex-col items-center justify-center space-y-3">
            <div className="h-8 w-8 border-2 border-teal-500 border-t-transparent rounded-full animate-spin"></div>
            <p className="text-xs text-gray-400">Loading intelligence feed...</p>
          </div>
        )}

        {!loading && stories.length === 0 && (
          <div className="py-16 text-center text-gray-400 p-8 rounded-2xl bg-gray-900/30 border border-gray-800 space-y-2">
            <p className="text-sm font-semibold">No stories match your filter criteria.</p>
            <p className="text-xs text-gray-500">Try adjusting your topic search, sector, or verification status.</p>
          </div>
        )}

        {!loading && stories.map((story) => (
          <div
            key={story.id}
            className="p-5 rounded-2xl bg-gray-900/60 hover:bg-gray-900 border border-gray-800 hover:border-teal-500/40 transition flex flex-col justify-between space-y-4 group"
          >
            {/* Top Row: Ranks, Badges, Date */}
            <div className="flex items-center justify-between flex-wrap gap-2">
              <div className="flex items-center space-x-2.5 flex-wrap gap-y-1">
                {story.trending_rank && (
                  <span className="text-xs font-bold px-2 py-0.5 rounded bg-teal-950 text-teal-300 border border-teal-800/60">
                    Trending #{story.trending_rank}
                  </span>
                )}
                {story.market_rank && (
                  <span className="text-xs font-bold px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800/60">
                    Market #{story.market_rank}
                  </span>
                )}
                <span className={`text-[11px] font-bold px-2.5 py-0.5 rounded-full border ${getStatusBadge(story.verification_status)}`}>
                  {story.verification_status}
                </span>
                <span className="text-[11px] text-gray-400 px-2 py-0.5 rounded bg-gray-800/50">
                  {story.trending_label}
                </span>
              </div>

              {story.event_date && (
                <div className="text-xs text-gray-400 flex items-center space-x-1">
                  <Calendar className="h-3.5 w-3.5 text-gray-500" />
                  <span>{new Date(story.event_date).toLocaleDateString()}</span>
                </div>
              )}
            </div>

            {/* Headline and Summary */}
            <div className="space-y-1.5 cursor-pointer" onClick={() => onSelectStory(story.id)}>
              <h2 className="text-base sm:text-lg font-bold text-gray-100 group-hover:text-teal-300 transition tracking-tight">
                {story.title}
              </h2>
              <p className="text-xs sm:text-sm text-gray-300 leading-relaxed line-clamp-3">
                {story.summary}
              </p>
            </div>

            {/* Entities & Industries */}
            <div className="flex flex-wrap items-center gap-2 pt-1">
              {story.entities.slice(0, 4).map((ent) => (
                <span
                  key={ent.id}
                  className="text-[11px] font-medium px-2 py-0.5 rounded-md bg-gray-950 text-gray-300 border border-gray-800 flex items-center space-x-1"
                >
                  <Building2 className="h-3 w-3 text-cyan-400" />
                  <span>{ent.name}</span>
                  {ent.ticker_symbol && (
                    <span className="text-[10px] text-teal-400 font-mono font-bold">${ent.ticker_symbol}</span>
                  )}
                </span>
              ))}

              {story.industry_impacts.slice(0, 3).map((imp) => (
                <span
                  key={imp.id}
                  className="text-[11px] px-2 py-0.5 rounded-md bg-gray-950 text-gray-400 border border-gray-800/80"
                >
                  {imp.industry_name} ({imp.impact_magnitude})
                </span>
              ))}
            </div>

            {/* Bottom Row: Dual Scores & Actions */}
            <div className="flex items-center justify-between pt-3 border-t border-gray-800/60 flex-wrap gap-2">
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-1.5">
                  <TrendingUp className="h-4 w-4 text-teal-400" />
                  <span className="text-xs text-gray-400">Trending Score:</span>
                  <span className="text-sm font-bold text-teal-300">{story.trending_score}</span>
                </div>
                <div className="flex items-center space-x-1.5">
                  <Award className="h-4 w-4 text-cyan-400" />
                  <span className="text-xs text-gray-400">Market Importance:</span>
                  <span className="text-sm font-bold text-cyan-300">{story.market_importance_score}</span>
                </div>
              </div>

              <div className="flex items-center space-x-2">
                {story.sources.length > 0 && (
                  <a
                    href={story.sources[0].url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center space-x-1 text-xs text-gray-400 hover:text-teal-300 px-2.5 py-1 rounded bg-gray-950 border border-gray-800 transition"
                  >
                    <span>Primary Link</span>
                    <ExternalLink className="h-3 w-3" />
                  </a>
                )}
                <button
                  onClick={() => onSelectStory(story.id)}
                  className="flex items-center space-x-1 text-xs font-semibold px-3 py-1 rounded-lg bg-teal-600/20 hover:bg-teal-600 text-teal-300 hover:text-white border border-teal-500/40 transition"
                >
                  <span>Deep Dive Dossier</span>
                  <ChevronRight className="h-3.5 w-3.5" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
