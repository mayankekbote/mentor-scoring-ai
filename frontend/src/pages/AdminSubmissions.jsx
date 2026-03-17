import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { getSubmissions } from '../api/adminApi';
import { Search, Filter, ChevronRight, Download, Loader2 } from 'lucide-react';
import { formatDate, cn } from '../utils/helpers';

const STATUS_OPTIONS = [
  { value: 'all', label: 'All Statuses' },
  { value: 'uploaded', label: 'Uploaded' },
  { value: 'processing', label: 'Processing' },
  { value: 'completed', label: 'Completed' },
  { value: 'called_for_interview', label: 'Called for Interview' },
  { value: 'failed', label: 'Failed' },
];

const STATUS_STYLES = {
  processing: { pill: 'bg-amber-50 text-amber-700 border border-amber-100', dot: 'bg-amber-400' },
  completed: { pill: 'bg-teal-50 text-teal-700 border border-teal-100', dot: 'bg-teal-500' },
  failed: { pill: 'bg-red-50 text-red-600 border border-red-100', dot: 'bg-red-400' },
  uploaded: { pill: 'bg-slate-100 text-slate-600 border border-slate-200', dot: 'bg-slate-400' },
  called_for_interview: { pill: 'bg-violet-50 text-violet-700 border border-violet-100', dot: 'bg-violet-500' },
};

const StatusBadge = ({ status }) => {
  const style = STATUS_STYLES[status] || { pill: 'bg-slate-100 text-slate-500 border border-slate-200', dot: 'bg-slate-400' };
  const label = status === 'called_for_interview' ? 'Called for Interview'
    : status.charAt(0).toUpperCase() + status.slice(1);
  return (
    <span className={cn('inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide', style.pill)}>
      <span className={cn('h-1 w-1 rounded-full', style.dot)} />
      {label}
    </span>
  );
};

const ScoreDisplay = ({ score }) => {
  if (score === null || score === undefined) return <span className="text-slate-300 font-bold text-sm">—</span>;
  const color = score >= 70 ? 'text-teal-600' : score >= 40 ? 'text-amber-600' : 'text-red-500';
  return (
    <div className="flex items-baseline gap-1">
      <span className={cn('text-sm font-black', color)}>{score}</span>
      <span className="text-[10px] text-slate-400 font-medium">/100</span>
    </div>
  );
};

const AdminSubmissions = () => {
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const navigate = useNavigate();

  const fetchSubmissions = useCallback(async () => {
    try {
      const data = await getSubmissions();
      setSubmissions(data);
    } catch (err) {
      console.error('Failed to fetch submissions', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchSubmissions(); }, [fetchSubmissions]);

  const filtered = submissions.filter(s => {
    const matchSearch = s.user_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      s.topic_taught.toLowerCase().includes(searchTerm.toLowerCase());
    const matchStatus = statusFilter === 'all' || s.status === statusFilter;
    return matchSearch && matchStatus;
  });

  const handleExport = () => {
    if (!filtered.length) return;
    const headers = ['Name', 'Topic', 'Score', 'Status', 'Submitted'];
    const rows = filtered.map(s => [
      s.user_name,
      s.topic_taught,
      s.score ?? '—',
      s.status,
      new Date(s.created_at).toLocaleDateString()
    ]);
    const csv = [headers, ...rows].map(r => r.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'submissions.csv';
    a.click();
    URL.revokeObjectURL(url);
  };

  // Status counts for filter pills
  const counts = submissions.reduce((acc, s) => {
    acc[s.status] = (acc[s.status] || 0) + 1;
    return acc;
  }, {});

  if (loading) return (
    <div className="h-64 flex items-center justify-center">
      <Loader2 className="h-6 w-6 animate-spin text-teal-600" />
    </div>
  );

  return (
    <div className="space-y-8">

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
        <div>
          <p className="text-xs font-semibold text-teal-600 tracking-widest uppercase mb-1">Admin</p>
          <h1 className="text-3xl font-black text-slate-900 tracking-tight">Submissions</h1>
          <p className="text-slate-500 text-sm mt-1">
            {submissions.length} total · {filtered.length} showing
          </p>
        </div>
        <button
          onClick={handleExport}
          disabled={!filtered.length}
          className="h-10 px-4 flex items-center gap-2 rounded-lg border border-slate-200 bg-white text-sm font-semibold text-slate-600 hover:bg-slate-50 hover:border-slate-300 transition-all disabled:opacity-40 disabled:cursor-not-allowed"
        >
          <Download className="h-4 w-4" />
          Export CSV
        </button>
      </div>

      {/* Status quick-filter pills */}
      <div className="flex flex-wrap gap-2">
        {STATUS_OPTIONS.map(opt => (
          <button
            key={opt.value}
            onClick={() => setStatusFilter(opt.value)}
            className={cn(
              'h-8 px-3 rounded-full text-xs font-semibold transition-all border',
              statusFilter === opt.value
                ? 'bg-teal-600 text-white border-teal-600'
                : 'bg-white text-slate-500 border-slate-200 hover:border-slate-300'
            )}
          >
            {opt.label}
            {opt.value !== 'all' && counts[opt.value]
              ? <span className={cn('ml-1.5 font-bold', statusFilter === opt.value ? 'opacity-70' : 'text-slate-400')}>
                {counts[opt.value]}
              </span>
              : null}
          </button>
        ))}
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-300" />
        <input
          className="input pl-10 w-full max-w-sm"
          placeholder="Search name or topic..."
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
        />
      </div>

      {/* Table */}
      <div className="bg-white border border-slate-200 rounded-xl overflow-hidden">
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-slate-100">
              <th className="px-6 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-widest">Candidate</th>
              <th className="px-6 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-widest">Topic</th>
              <th className="px-6 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-widest">Score</th>
              <th className="px-6 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-widest">Status</th>
              <th className="px-6 py-3 text-[10px] font-semibold text-slate-400 uppercase tracking-widest">Submitted</th>
              <th className="px-6 py-3 text-right text-[10px] font-semibold text-slate-400 uppercase tracking-widest">View</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-50">
            {filtered.map(s => (
              <tr
                key={s.id}
                onClick={() => navigate(`/admin/submission/${s.id}`)}
                className="hover:bg-slate-50/50 transition-colors cursor-pointer"
              >
                <td className="px-6 py-4">
                  <div className="flex items-center gap-3">
                    <div className="h-8 w-8 rounded-full bg-teal-50 border border-teal-100 text-teal-700 flex items-center justify-center font-bold text-xs shrink-0">
                      {s.user_name?.[0]?.toUpperCase()}
                    </div>
                    <span className="text-sm font-semibold text-slate-800 whitespace-nowrap">{s.user_name}</span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <span className="text-sm text-slate-500 truncate max-w-[180px] block">{s.topic_taught}</span>
                </td>
                <td className="px-6 py-4">
                  <ScoreDisplay score={s.score} />
                </td>
                <td className="px-6 py-4">
                  <StatusBadge status={s.status} />
                </td>
                <td className="px-6 py-4">
                  <span className="text-xs text-slate-400">
                    {new Date(s.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })}
                  </span>
                </td>
                <td className="px-6 py-4 text-right">
                  <ChevronRight className="h-4 w-4 text-slate-300 ml-auto" />
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {filtered.length === 0 && (
          <div className="py-24 text-center">
            <div className="h-12 w-12 bg-slate-50 border border-slate-200 rounded-xl flex items-center justify-center mx-auto mb-4">
              <Search className="h-5 w-5 text-slate-300" />
            </div>
            <p className="text-sm font-semibold text-slate-700 mb-1">No results found</p>
            <p className="text-xs text-slate-400">Try a different search term or status filter.</p>
          </div>
        )}
      </div>

    </div>
  );
};

export default AdminSubmissions;