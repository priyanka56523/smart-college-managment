import React, { useEffect, useState } from 'react';
import { ExternalLink, ShieldCheck, Filter, AlertCircle, CheckCircle2 } from 'lucide-react';
import { SourceRecord } from '../types';
import { fetchSources } from '../api';

export const SourcesTab: React.FC = () => {
  const [sources, setSources] = useState<SourceRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterType, setFilterType] = useState('ALL');

  useEffect(() => {
    fetchSources()
      .then(setSources)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const filteredSources = filterType === 'ALL'
    ? sources
    : sources.filter(s => s.source_type === filterType);

  return (
    <div className="space-y-6 pb-12">
      {/* Sources Registry Banner */}
      <div className="p-6 rounded-2xl bg-gray-900/60 border border-gray-800 space-y-2">
        <div className="flex items-center space-x-2">
          <ShieldCheck className="h-5 w-5 text-teal-400" />
          <h2 className="text-base font-bold text-white">Consolidated Source & Primary Evidence Registry</h2>
        </div>
        <p className="text-xs text-gray-300 leading-relaxed">
          Every assertion in this intelligence platform links to verifiable primary documentation, research preprints, or accredited reporting.
          Live HTTP probes test access availability, preserving direct clickable citations.
        </p>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center space-x-2 overflow-x-auto text-xs pb-1">
        {['ALL', 'official_announcement', 'research_paper', 'code_repository', 'independent_news'].map((st) => (
          <button
            key={st}
            onClick={() => setFilterType(st)}
            className={`px-3 py-1.5 rounded-lg border font-medium whitespace-nowrap transition ${
              filterType === st
                ? 'bg-teal-950 text-teal-300 border-teal-800'
                : 'bg-gray-900/60 text-gray-400 border-gray-800 hover:text-white'
            }`}
          >
            {st.replace('_', ' ').toUpperCase()}
          </button>
        ))}
      </div>

      {/* Table */}
      <div className="rounded-2xl border border-gray-800 bg-gray-900/60 overflow-hidden">
        {loading && (
          <div className="py-20 flex flex-col items-center justify-center space-y-3">
            <div className="h-8 w-8 border-2 border-teal-500 border-t-transparent rounded-full animate-spin"></div>
            <p className="text-xs text-gray-400">Loading sources...</p>
          </div>
        )}

        {!loading && (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-[#0f172a]/80 text-gray-400 uppercase tracking-wider text-[10px] border-b border-gray-800">
                <tr>
                  <th className="px-4 py-3 font-semibold">Title & Citation</th>
                  <th className="px-4 py-3 font-semibold">Publisher</th>
                  <th className="px-4 py-3 font-semibold">Source Type</th>
                  <th className="px-4 py-3 font-semibold">Access Status</th>
                  <th className="px-4 py-3 font-semibold">Claims Supported</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800/60 text-gray-300">
                {filteredSources.map((src) => (
                  <tr key={src.id} className="hover:bg-gray-800/40 transition">
                    <td className="px-4 py-3.5 max-w-sm">
                      <a
                        href={src.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="font-medium text-teal-300 hover:underline flex items-center space-x-1.5 group"
                      >
                        <span className="line-clamp-1">{src.title}</span>
                        <ExternalLink className="h-3 w-3 text-gray-500 group-hover:text-teal-300 flex-shrink-0" />
                      </a>
                      <span className="text-[10px] text-gray-500 font-mono truncate block mt-0.5">
                        {src.url}
                      </span>
                    </td>
                    <td className="px-4 py-3.5 whitespace-nowrap font-medium text-gray-200">
                      {src.publisher || 'Unknown'}
                    </td>
                    <td className="px-4 py-3.5 whitespace-nowrap">
                      <span className="px-2 py-0.5 rounded bg-gray-950 border border-gray-800 font-mono text-[11px] text-gray-300">
                        {src.source_type}
                      </span>
                    </td>
                    <td className="px-4 py-3.5 whitespace-nowrap">
                      <span className="inline-flex items-center space-x-1 text-[11px] font-semibold px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800">
                        <CheckCircle2 className="h-3 w-3" />
                        <span>{src.access_status}</span>
                      </span>
                    </td>
                    <td className="px-4 py-3.5 max-w-xs text-gray-400">
                      <span className="line-clamp-2">
                        {src.claims_supported || 'Primary reporting context'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
