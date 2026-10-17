import React, { useEffect, useState } from 'react';
import { FileText, Plus, Calendar, Clock, ShieldAlert, CheckCircle2, ChevronRight, Download } from 'lucide-react';
import { IntelligenceReport } from '../types';
import { fetchReports, generateReport } from '../api';

export const ReportsTab: React.FC = () => {
  const [reports, setReports] = useState<IntelligenceReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [selectedReport, setSelectedReport] = useState<IntelligenceReport | null>(null);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = () => {
    setLoading(true);
    fetchReports()
      .then((data) => {
        setReports(data);
        if (data.length > 0 && !selectedReport) {
          setSelectedReport(data[0]);
        }
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  const handleGenerate = async (type: string = 'daily') => {
    setGenerating(true);
    try {
      const rep = await generateReport(type);
      setReports([rep, ...reports]);
      setSelectedReport(rep);
    } catch (e) {
      console.error(e);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Banner & Action Bar */}
      <div className="flex items-center justify-between flex-wrap gap-4 p-6 rounded-2xl bg-gray-900/60 border border-gray-800">
        <div className="space-y-1">
          <div className="flex items-center space-x-2">
            <FileText className="h-5 w-5 text-teal-400" />
            <h2 className="text-base font-bold text-white">Executive AI & AGI Intelligence Briefings</h2>
          </div>
          <p className="text-xs text-gray-400">
            Automated scheduled daily and 6-hour executive summaries with verified evidentiary findings and ranked signals.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => handleGenerate('daily')}
            disabled={generating}
            className="flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-teal-500 hover:bg-teal-400 text-gray-950 font-bold text-xs transition shadow-lg shadow-teal-500/20 disabled:opacity-50"
          >
            <Plus className="h-4 w-4" />
            <span>{generating ? 'Compiling Briefing...' : 'Generate Daily Briefing'}</span>
          </button>
        </div>
      </div>

      {/* Main split view: list on left, details on right */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left column: Historical reports list */}
        <div className="space-y-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-gray-400">Briefing Archives</h3>
          {loading && (
            <div className="py-12 flex justify-center">
              <div className="h-6 w-6 border-2 border-teal-500 border-t-transparent rounded-full animate-spin"></div>
            </div>
          )}

          {!loading && reports.length === 0 && (
            <div className="p-6 text-center text-xs text-gray-500 bg-gray-900/40 rounded-xl border border-gray-800">
              No historical briefings yet. Click "Generate Daily Briefing" above.
            </div>
          )}

          {reports.map((rep) => {
            const isSelected = selectedReport?.id === rep.id;
            return (
              <div
                key={rep.id}
                onClick={() => setSelectedReport(rep)}
                className={`p-4 rounded-xl border cursor-pointer transition space-y-1.5 ${
                  isSelected
                    ? 'bg-teal-950/40 border-teal-600/60 text-white'
                    : 'bg-gray-900/60 border-gray-800 hover:border-gray-700 text-gray-300'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-gray-950 border border-gray-800 text-teal-300">
                    {rep.report_type}
                  </span>
                  <span className="text-[11px] text-gray-400 font-mono">
                    {new Date(rep.research_timestamp).toLocaleDateString()}
                  </span>
                </div>
                <h4 className="text-xs font-semibold line-clamp-1">{rep.title}</h4>
                <div className="text-[11px] text-gray-400 flex items-center space-x-2">
                  <span>{rep.sources_examined_count} sources examined</span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Right column: Selected report reader */}
        <div className="lg:col-span-2 space-y-4">
          {selectedReport ? (
            <div className="p-6 rounded-2xl bg-gray-900/70 border border-gray-800 space-y-6">
              {/* Report Header Metadata */}
              <div className="border-b border-gray-800 pb-4 space-y-2">
                <div className="flex items-center justify-between flex-wrap gap-2">
                  <span className="text-xs font-bold uppercase px-2.5 py-0.5 rounded-full bg-teal-950 text-teal-300 border border-teal-800">
                    {selectedReport.report_type} Intelligence Dossier
                  </span>
                  <div className="text-xs text-gray-400 flex items-center space-x-3">
                    <span className="flex items-center space-x-1">
                      <Clock className="h-3.5 w-3.5" />
                      <span>{new Date(selectedReport.research_timestamp).toUTCString()}</span>
                    </span>
                  </div>
                </div>
                <h1 className="text-xl font-bold text-white tracking-tight">
                  {selectedReport.title}
                </h1>
                <div className="text-xs text-gray-400">
                  Coverage Window: {new Date(selectedReport.coverage_period_start).toLocaleDateString()} to {new Date(selectedReport.coverage_period_end).toLocaleDateString()} ({selectedReport.timezone_name})
                </div>
              </div>

              {/* Coverage Gaps & Limitations Notice */}
              {selectedReport.coverage_gaps_notes && (
                <div className="p-3.5 rounded-xl bg-amber-950/30 border border-amber-900/50 text-xs text-amber-300 space-y-1">
                  <strong>Access Limitations & Coverage Gaps:</strong>
                  <p className="text-gray-300 text-[11px] leading-relaxed">
                    {selectedReport.coverage_gaps_notes}
                  </p>
                </div>
              )}

              {/* Executive Summary */}
              <div className="space-y-2">
                <h3 className="text-xs font-bold uppercase tracking-wider text-teal-400">Executive Summary</h3>
                <div className="p-4 rounded-xl bg-gray-950 border border-gray-800 text-xs text-gray-200 whitespace-pre-line leading-relaxed font-sans">
                  {selectedReport.executive_summary}
                </div>
              </div>

              {/* Key Developments to Monitor Next */}
              {selectedReport.key_developments_to_monitor && (
                <div className="space-y-2">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-cyan-400">Next Milestones to Monitor</h3>
                  <div className="p-3.5 rounded-xl bg-gray-950 border border-gray-800 text-xs text-gray-300 leading-relaxed">
                    {selectedReport.key_developments_to_monitor}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="p-12 text-center text-gray-500 bg-gray-900/30 rounded-2xl border border-gray-800">
              Select a briefing from the archive to read its contents.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
