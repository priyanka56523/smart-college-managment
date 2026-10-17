import React from 'react';
import { Activity, ShieldCheck, RefreshCw, Zap, Server, FileText } from 'lucide-react';
import { SystemHealth } from '../types';

interface HeaderProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  systemHealth: SystemHealth | null;
  onOpenConnections: () => void;
  onTriggerIngest: () => void;
  isIngesting: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  activeTab,
  setActiveTab,
  systemHealth,
  onOpenConnections,
  onTriggerIngest,
  isIngesting,
}) => {
  const tabs = [
    { id: 'overview', label: 'Overview', icon: Activity },
    { id: 'feed', label: 'News Feed', icon: Zap },
    { id: 'analytics', label: 'Trend Analytics', icon: Server },
    { id: 'sources', label: 'Sources Registry', icon: ShieldCheck },
    { id: 'reports', label: 'Executive Briefings', icon: FileText },
  ];

  return (
    <header className="sticky top-0 z-40 bg-[#0b0f19]/90 backdrop-blur-md border-b border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Brand */}
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('overview')}>
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-teal-500 to-cyan-400 p-0.5 shadow-lg shadow-teal-500/20">
              <div className="w-full h-full bg-[#0b0f19] rounded-[10px] flex items-center justify-center">
                <Zap className="h-5 w-5 text-teal-400" />
              </div>
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-bold text-lg tracking-tight bg-gradient-to-r from-teal-300 via-cyan-200 to-white bg-clip-text text-transparent">
                  AI & AGI News Intelligence
                </span>
                <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded bg-teal-950 text-teal-300 border border-teal-800/60">
                  Global Enterprise
                </span>
              </div>
              <p className="text-xs text-gray-400 hidden sm:block">
                Autonomous Discovery • Evidence Verification • Market Impact
              </p>
            </div>
          </div>

          {/* Quick Actions & Status */}
          <div className="flex items-center space-x-3">
            {/* Live API Health Pill */}
            <button
              onClick={onOpenConnections}
              className="hidden md:flex items-center space-x-2 text-xs px-3 py-1.5 rounded-lg bg-gray-900/80 hover:bg-gray-800 border border-gray-800 text-gray-300 transition"
              title="Inspect API connections and rate limits"
            >
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span className="font-medium">Integrations & Health</span>
            </button>

            {/* Ingestion Button */}
            <button
              onClick={onTriggerIngest}
              disabled={isIngesting}
              className={`flex items-center space-x-2 text-xs font-semibold px-3.5 py-1.5 rounded-lg border transition ${
                isIngesting
                  ? 'bg-teal-950/60 border-teal-800 text-teal-300 cursor-not-allowed'
                  : 'bg-teal-500 hover:bg-teal-400 text-gray-950 border-teal-400 shadow-md shadow-teal-500/20 active:scale-95'
              }`}
            >
              <RefreshCw className={`h-3.5 w-3.5 ${isIngesting ? 'animate-spin' : ''}`} />
              <span>{isIngesting ? 'Ingesting Feeds...' : 'Run Ingestion'}</span>
            </button>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex space-x-1 sm:space-x-4 border-t border-gray-800/60 overflow-x-auto py-1 scrollbar-none">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-3.5 py-2 text-xs sm:text-sm font-medium rounded-md whitespace-nowrap transition-colors ${
                  isActive
                    ? 'text-teal-400 bg-teal-950/40 border border-teal-800/50 shadow-sm'
                    : 'text-gray-400 hover:text-gray-200 hover:bg-gray-900/40'
                }`}
              >
                <Icon className={`h-4 w-4 ${isActive ? 'text-teal-400' : 'text-gray-500'}`} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
};
