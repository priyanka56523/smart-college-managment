import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { OverviewTab } from './components/OverviewTab';
import { NewsFeedTab } from './components/NewsFeedTab';
import { TrendAnalyticsTab } from './components/TrendAnalyticsTab';
import { SourcesTab } from './components/SourcesTab';
import { ReportsTab } from './components/ReportsTab';
import { StoryDetailModal } from './components/StoryDetailModal';
import { ConnectionStatusModal } from './components/ConnectionStatusModal';
import { Leaderboards, Analytics, SystemHealth, APIConnectionResult } from './types';
import { fetchHealth, fetchLeaderboards, fetchAnalytics, triggerIngestion, testConnections } from './api';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [selectedStoryId, setSelectedStoryId] = useState<number | null>(null);
  const [isConnectionsOpen, setIsConnectionsOpen] = useState(false);
  const [isIngesting, setIsIngesting] = useState(false);

  const [leaderboards, setLeaderboards] = useState<Leaderboards | null>(null);
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [systemHealth, setSystemHealth] = useState<SystemHealth | null>(null);
  const [connections, setConnections] = useState<APIConnectionResult[]>([]);
  const [feedInitialFilter, setFeedInitialFilter] = useState<any>(null);

  useEffect(() => {
    refreshAllData();
  }, []);

  const refreshAllData = async () => {
    try {
      const [h, l, a, c] = await Promise.all([
        fetchHealth().catch(() => null),
        fetchLeaderboards().catch(() => null),
        fetchAnalytics().catch(() => null),
        testConnections().catch(() => [])
      ]);
      if (h) setSystemHealth(h);
      if (l) setLeaderboards(l);
      if (a) setAnalytics(a);
      if (c) setConnections(c);
    } catch (e) {
      console.error('Error refreshing platform data:', e);
    }
  };

  const handleTriggerIngest = async () => {
    setIsIngesting(true);
    try {
      await triggerIngestion();
      await refreshAllData();
    } catch (e) {
      console.error('Failed to trigger ingestion:', e);
    } finally {
      setIsIngesting(false);
    }
  };

  const handleNavigateFeed = (filter?: any) => {
    setFeedInitialFilter(filter);
    setActiveTab('feed');
  };

  return (
    <div className="min-h-screen bg-[#0b0f19] text-gray-100 flex flex-col font-sans">
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        systemHealth={systemHealth}
        onOpenConnections={() => setIsConnectionsOpen(true)}
        onTriggerIngest={handleTriggerIngest}
        isIngesting={isIngesting}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-6">
        {activeTab === 'overview' && (
          <OverviewTab
            leaderboards={leaderboards}
            analytics={analytics}
            systemHealth={systemHealth}
            onSelectStory={(id) => setSelectedStoryId(id)}
            onNavigateFeed={handleNavigateFeed}
          />
        )}

        {activeTab === 'feed' && (
          <NewsFeedTab
            onSelectStory={(id) => setSelectedStoryId(id)}
            initialFilter={feedInitialFilter}
          />
        )}

        {activeTab === 'analytics' && (
          <TrendAnalyticsTab analytics={analytics} />
        )}

        {activeTab === 'sources' && (
          <SourcesTab />
        )}

        {activeTab === 'reports' && (
          <ReportsTab />
        )}
      </main>

      {/* Story Detail Dossier Modal */}
      <StoryDetailModal
        storyId={selectedStoryId}
        onClose={() => setSelectedStoryId(null)}
      />

      {/* External Integrations Health Modal */}
      <ConnectionStatusModal
        isOpen={isConnectionsOpen}
        onClose={() => setIsConnectionsOpen(false)}
        connections={connections}
        onRefresh={refreshAllData}
      />

      {/* Footer */}
      <footer className="border-t border-gray-800/80 bg-[#080c14] py-6 text-center text-xs text-gray-500">
        <div className="max-w-7xl mx-auto px-4 space-y-1">
          <p className="font-medium text-gray-400">
            Global AI & AGI News Intelligence Platform • Autonomous Discovery, Evidence Verification & Market Impact
          </p>
          <p className="text-[11px] text-gray-600">
            Evidence-Driven Architecture • Scored via Deterministic Versioned Rubric v1.0 • No Fabricated Citations
          </p>
        </div>
      </footer>
    </div>
  );
};
