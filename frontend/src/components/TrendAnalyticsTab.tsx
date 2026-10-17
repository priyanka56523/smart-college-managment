import React from 'react';
import { BarChart3, PieChart, TrendingUp, AlertCircle, Building2, ShieldCheck, Cpu } from 'lucide-react';
import { Analytics } from '../types';

interface TrendAnalyticsTabProps {
  analytics: Analytics | null;
}

export const TrendAnalyticsTab: React.FC<TrendAnalyticsTabProps> = ({ analytics }) => {
  if (!analytics) {
    return (
      <div className="py-20 flex flex-col items-center justify-center space-y-3">
        <div className="h-8 w-8 border-2 border-teal-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-xs text-gray-400">Loading trend analytics...</p>
      </div>
    );
  }

  const maxIndustryCount = Math.max(...analytics.top_industries_exposed.map(i => i.count), 1);

  return (
    <div className="space-y-8 pb-12">
      {/* Notice on Measured vs Estimated */}
      <div className="p-4 rounded-xl bg-gray-900/40 border border-gray-800 text-xs text-gray-400 flex items-start space-x-2.5">
        <AlertCircle className="h-4 w-4 text-cyan-400 flex-shrink-0 mt-0.5" />
        <div className="space-y-1">
          <p className="text-gray-200 font-medium">Measurement & Coverage Methodology Note:</p>
          <p>
            Metrics reflect direct article counts, peer preprints from arXiv, open repository momentum from GitHub, and official laboratory feeds. 
            Search volumes and social indicators without authenticated direct API streams are normalized and identified as provisional signals rather than speculative precision.
          </p>
        </div>
      </div>

      {/* Grid of Analytical Distributions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Industry Exposure Matrix */}
        <div className="p-6 rounded-2xl bg-gray-900/60 border border-gray-800 space-y-4">
          <div className="flex items-center space-x-2 border-b border-gray-800 pb-3">
            <Cpu className="h-5 w-5 text-teal-400" />
            <h2 className="text-sm font-bold text-white">Cross-Sector Economic Exposure Matrix</h2>
          </div>
          <div className="space-y-3">
            {analytics.top_industries_exposed.map((item, idx) => {
              const percentage = Math.round((item.count / maxIndustryCount) * 100);
              return (
                <div key={idx} className="space-y-1">
                  <div className="flex justify-between text-xs font-medium">
                    <span className="text-gray-200">{item.industry}</span>
                    <span className="text-teal-400 font-mono">{item.count} stories ({percentage}%)</span>
                  </div>
                  <div className="w-full h-2 rounded-full bg-gray-950 overflow-hidden">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-teal-500 to-cyan-400 transition-all duration-500"
                      style={{ width: `${percentage}%` }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Verification Status Distribution */}
        <div className="p-6 rounded-2xl bg-gray-900/60 border border-gray-800 space-y-4">
          <div className="flex items-center space-x-2 border-b border-gray-800 pb-3">
            <ShieldCheck className="h-5 w-5 text-emerald-400" />
            <h2 className="text-sm font-bold text-white">Evidentiary Verification Distribution</h2>
          </div>
          <div className="space-y-3">
            {Object.entries(analytics.verification_counts).map(([status, count], idx) => {
              let color = 'bg-gray-700';
              if (status === 'VERIFIED') color = 'bg-emerald-500';
              if (status === 'CORROBORATED') color = 'bg-cyan-500';
              if (status === 'PARTIALLY VERIFIED') color = 'bg-amber-500';
              if (status === 'DISPUTED') color = 'bg-orange-500';
              if (status === 'FALSE OR DEBUNKED') color = 'bg-red-500';

              return (
                <div key={idx} className="flex items-center justify-between p-3 rounded-xl bg-gray-950/60 border border-gray-800/80">
                  <div className="flex items-center space-x-2.5">
                    <span className={`h-2.5 w-2.5 rounded-full ${color}`}></span>
                    <span className="text-xs font-semibold text-gray-200">{status}</span>
                  </div>
                  <span className="text-sm font-bold text-gray-100 font-mono">{count}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Top Organizations & Tickers */}
      <div className="p-6 rounded-2xl bg-gray-900/60 border border-gray-800 space-y-4">
        <div className="flex items-center space-x-2 border-b border-gray-800 pb-3">
          <Building2 className="h-5 w-5 text-cyan-400" />
          <h2 className="text-sm font-bold text-white">Most Active Organizations & Public Market Exposure</h2>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
          {analytics.top_entities.map((ent, idx) => (
            <div
              key={idx}
              className="p-3.5 rounded-xl bg-gray-950/60 border border-gray-800 flex items-center justify-between"
            >
              <div>
                <span className="font-semibold text-xs text-gray-200 block">{ent.name}</span>
                <span className="text-[10px] text-gray-500 uppercase">{ent.entity_type}</span>
              </div>
              <div className="text-right">
                {ent.ticker && (
                  <span className="text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-800 block mb-0.5">
                    ${ent.ticker}
                  </span>
                )}
                <span className="text-xs text-teal-400 font-mono">{ent.occurrences} events</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
