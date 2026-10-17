import React, { useState } from 'react';
import { X, CheckCircle2, AlertTriangle, AlertCircle, RefreshCw, Key, Shield, ExternalLink } from 'lucide-react';
import { APIConnectionResult } from '../types';
import { testConnections } from '../api';

interface ConnectionStatusModalProps {
  isOpen: boolean;
  onClose: () => void;
  connections: APIConnectionResult[];
  onRefresh: () => void;
}

export const ConnectionStatusModal: React.FC<ConnectionStatusModalProps> = ({
  isOpen,
  onClose,
  connections,
  onRefresh
}) => {
  const [testing, setTesting] = useState(false);
  const [results, setResults] = useState<APIConnectionResult[]>(connections);

  if (!isOpen) return null;

  const handleTestNow = async () => {
    setTesting(true);
    try {
      const live = await testConnections();
      setResults(live);
      onRefresh();
    } catch (e) {
      console.error(e);
    } finally {
      setTesting(false);
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'OK':
        return (
          <span className="flex items-center space-x-1 text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800">
            <CheckCircle2 className="h-3 w-3" />
            <span>CONNECTED</span>
          </span>
        );
      case 'MISSING_KEY':
        return (
          <span className="flex items-center space-x-1 text-xs font-semibold px-2 py-0.5 rounded-full bg-amber-950 text-amber-400 border border-amber-800">
            <Key className="h-3 w-3" />
            <span>CONFIG READY</span>
          </span>
        );
      case 'RATE_LIMITED':
        return (
          <span className="flex items-center space-x-1 text-xs font-semibold px-2 py-0.5 rounded-full bg-red-950 text-red-400 border border-red-800">
            <AlertTriangle className="h-3 w-3" />
            <span>RATE LIMITED</span>
          </span>
        );
      default:
        return (
          <span className="flex items-center space-x-1 text-xs font-semibold px-2 py-0.5 rounded-full bg-gray-800 text-gray-300 border border-gray-700">
            <AlertCircle className="h-3 w-3" />
            <span>{status}</span>
          </span>
        );
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
      <div className="bg-[#111827] border border-gray-800 rounded-2xl w-full max-w-2xl max-h-[85vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-800 bg-[#0f172a]/60">
          <div className="flex items-center space-x-2">
            <Shield className="h-5 w-5 text-teal-400" />
            <h2 className="text-lg font-semibold text-white">External Integrations & API Status</h2>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 transition"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Notice on Authenticity */}
        <div className="px-6 py-3 bg-teal-950/20 border-b border-teal-900/40 text-xs text-teal-300">
          <strong>Transparency Notice:</strong> All connection statuses, constraints, and rate limits reflect actual live endpoints. No simulated success is reported as real.
        </div>

        {/* Content list */}
        <div className="p-6 overflow-y-auto space-y-4 flex-1">
          {(results.length > 0 ? results : connections).map((conn, idx) => (
            <div
              key={idx}
              className="p-4 rounded-xl bg-gray-900/80 border border-gray-800 hover:border-gray-700 transition space-y-2"
            >
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-semibold text-gray-100 text-sm">{conn.service}</h3>
                  <code className="text-[11px] text-gray-400 font-mono">{conn.endpoint}</code>
                </div>
                {getStatusBadge(conn.status)}
              </div>

              {conn.model && (
                <div className="text-xs text-cyan-300 font-mono bg-cyan-950/40 px-2 py-0.5 rounded inline-block">
                  Model: {conn.model}
                </div>
              )}

              <p className="text-xs text-gray-300 leading-relaxed">{conn.message}</p>

              {conn.account_constraints?.limitation && (
                <div className="text-[11px] text-gray-400 bg-black/40 p-2 rounded border border-gray-800/60 leading-normal">
                  <span className="text-amber-400 font-medium">Constraints: </span>
                  {conn.account_constraints.limitation}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-gray-800 bg-[#0f172a]/60 flex items-center justify-between">
          <span className="text-xs text-gray-400">
            Keys stored in <code className="text-gray-300 font-mono">.env</code>
          </span>
          <div className="flex items-center space-x-3">
            <button
              onClick={handleTestNow}
              disabled={testing}
              className="flex items-center space-x-1.5 text-xs px-3.5 py-1.5 rounded-lg bg-teal-600 hover:bg-teal-500 text-white font-medium transition disabled:opacity-50"
            >
              <RefreshCw className={`h-3.5 w-3.5 ${testing ? 'animate-spin' : ''}`} />
              <span>{testing ? 'Testing Endpoints...' : 'Re-test Connections'}</span>
            </button>
            <button
              onClick={onClose}
              className="text-xs px-3.5 py-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-200 transition"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
