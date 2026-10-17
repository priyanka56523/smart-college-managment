import {
  Story, StoryDetail, Leaderboards, Analytics,
  SourceRecord, IntelligenceReport, SystemHealth, APIConnectionResult
} from './types';

const API_BASE = '/api';

export async function fetchHealth(): Promise<SystemHealth> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Failed to fetch system health');
  return res.json();
}

export async function testConnections(): Promise<APIConnectionResult[]> {
  const res = await fetch(`${API_BASE}/config/test-connections`);
  if (!res.ok) throw new Error('Failed to test external connections');
  return res.json();
}

export async function fetchStories(params: {
  search?: string;
  verification_status?: string;
  industry?: string;
  entity?: string;
  is_emerging_signal?: boolean;
  sort_by?: 'trending' | 'market' | 'date';
  limit?: number;
}): Promise<Story[]> {
  const query = new URLSearchParams();
  if (params.search) query.set('search', params.search);
  if (params.verification_status) query.set('verification_status', params.verification_status);
  if (params.industry) query.set('industry', params.industry);
  if (params.entity) query.set('entity', params.entity);
  if (params.is_emerging_signal !== undefined) query.set('is_emerging_signal', String(params.is_emerging_signal));
  if (params.sort_by) query.set('sort_by', params.sort_by);
  if (params.limit) query.set('limit', String(params.limit));

  const res = await fetch(`${API_BASE}/stories?${query.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch stories');
  return res.json();
}

export async function fetchStoryDetail(id: number): Promise<StoryDetail> {
  const res = await fetch(`${API_BASE}/stories/${id}`);
  if (!res.ok) throw new Error(`Failed to fetch story details for #${id}`);
  return res.json();
}

export async function fetchLeaderboards(): Promise<Leaderboards> {
  const res = await fetch(`${API_BASE}/leaderboards`);
  if (!res.ok) throw new Error('Failed to fetch leaderboards');
  return res.json();
}

export async function fetchAnalytics(): Promise<Analytics> {
  const res = await fetch(`${API_BASE}/analytics`);
  if (!res.ok) throw new Error('Failed to fetch analytics');
  return res.json();
}

export async function fetchSources(): Promise<SourceRecord[]> {
  const res = await fetch(`${API_BASE}/sources?limit=100`);
  if (!res.ok) throw new Error('Failed to fetch sources');
  return res.json();
}

export async function fetchReports(): Promise<IntelligenceReport[]> {
  const res = await fetch(`${API_BASE}/reports`);
  if (!res.ok) throw new Error('Failed to fetch reports');
  return res.json();
}

export async function generateReport(reportType: string = 'daily'): Promise<IntelligenceReport> {
  const res = await fetch(`${API_BASE}/reports/generate?report_type=${reportType}`, {
    method: 'POST'
  });
  if (!res.ok) throw new Error('Failed to generate report');
  return res.json();
}

export async function triggerIngestion(): Promise<any> {
  const res = await fetch(`${API_BASE}/ingest`, {
    method: 'POST'
  });
  if (!res.ok) throw new Error('Failed to trigger ingestion');
  return res.json();
}
