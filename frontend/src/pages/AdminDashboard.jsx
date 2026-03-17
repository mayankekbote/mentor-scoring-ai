import { useState, useEffect, useCallback } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { getSubmissions } from '../api/adminApi';
import {
  Users,
  FileCheck,
  Clock,
  TrendingUp,
  Loader2,
  Calendar
} from 'lucide-react';
import { formatDate, cn } from '../utils/helpers';

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [recentSubmissions, setRecentSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const fetchDashboardData = useCallback(async () => {
    try {
      const submissions = await getSubmissions();

      setRecentSubmissions(submissions.slice(0, 5));

      setStats({
        total: submissions.length,
        completed: submissions.filter(s => s.status === 'completed').length,
        pending: submissions.filter(s => s.status === 'processing' || s.status === 'uploaded').length,
        averageScore: submissions.length > 0
          ? Math.round(submissions.reduce((acc, s) => acc + (s.score || 0), 0) / submissions.length)
          : 0,
      });
    } catch (err) {
      console.error("Failed to fetch dashboard data", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  if (loading) return (
    <div className="h-full flex items-center justify-center">
      <Loader2 className="h-8 w-8 animate-spin text-brand-sage" />
    </div>
  );

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-black text-slate-900 tracking-tight">Dashboard Overview</h1>
        <p className="text-slate-500 text-sm mt-1">Real-time metrics for your candidate evaluation pipeline.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          label="Total Submissions"
          value={stats?.total}
          icon={Users}
          color="bg-brand-sage"
          description="Candidates reached phase 2"
        />
        <StatCard
          label="Completed"
          value={stats?.completed}
          icon={FileCheck}
          color="bg-emerald-500"
          description="AI evaluation finished"
        />
        <StatCard
          label="Pending"
          value={stats?.pending}
          icon={Clock}
          color="bg-amber-500"
          description="Queue in processing"
        />
        <StatCard
          label="Average Score"
          value={`${stats?.averageScore || 0}`}
          unit="/100"
          icon={TrendingUp}
          color="bg-indigo-500"
          description="Organization avg performance"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-black text-slate-900">Recent Activity</h2>
            <Link to="/admin/submissions" className="text-xs font-black text-brand-sage uppercase tracking-widest hover:bg-brand-sage/5 px-3 py-1.5 rounded-lg transition-all">View all Submissions</Link>
          </div>
          <div className="card bg-white border border-slate-200 rounded-xl p-0 overflow-hidden shadow-sm">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-50/50 border-b border-slate-100 text-[10px] font-black text-slate-400 uppercase tracking-widest">
                  <th className="px-6 py-4">Candidate</th>
                  <th className="px-6 py-4">Topic</th>
                  <th className="px-6 py-4 text-center">Status</th>
                  <th className="px-6 py-4 text-right">Date</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50 text-sm">
                {recentSubmissions.map((s) => (
                  <tr key={s.id} className="hover:bg-slate-50 transition-colors cursor-pointer group" onClick={() => navigate(`/admin/submission/${s.id}`)}>
                    <td className="px-6 py-5 font-bold text-slate-900">{s.user_name}</td>
                    <td className="px-6 py-5 text-slate-500 italic">{s.topic_taught}</td>
                    <td className="px-6 py-5 text-center">
                      <StatusBadge status={s.status} />
                    </td>
                    <td className="px-6 py-5 text-right text-[10px] font-bold text-slate-400 uppercase">{formatDate(s.created_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="space-y-4">
          <h2 className="text-xl font-black text-slate-900">Performance Summary</h2>
          <div className="card bg-white border border-slate-200 rounded-xl p-6 space-y-6 shadow-sm">
            <div className="flex items-center justify-between">
              <span className="text-sm font-bold text-slate-500">Average AI Score</span>
              <span className="text-2xl font-black text-brand-sage">{stats?.averageScore}/100</span>
            </div>
            <div className="h-3 w-full bg-slate-100 rounded-full overflow-hidden border border-slate-50">
              <div 
                className="h-full bg-brand-sage transition-all duration-1000 ease-out shadow-sm" 
                style={{ width: `${stats?.averageScore}%` }} 
              />
            </div>
            <div className="bg-slate-50 rounded-lg p-4">
              <p className="text-xs text-slate-500 leading-relaxed font-medium">
                Based on <span className="text-slate-900 font-bold">{stats?.total}</span> evaluations. 
                Keep track of your organization's hiring quality in real-time.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ label, value, icon: Icon, color, description, unit }) => (
  <div className="card bg-white border border-slate-200 rounded-xl p-6 hover:border-slate-300 transition-all shadow-sm group">
    <div className="flex items-start justify-between">
      <div className={cn("h-12 w-12 rounded-xl flex items-center justify-center text-white shadow-lg", color)}>
        <Icon className="h-6 w-6" />
      </div>
    </div>
    <div className="mt-5">
      <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{label}</p>
      <div className="flex items-baseline gap-1 mt-1">
        <h4 className="text-3xl font-black text-slate-900">{value}</h4>
        {unit && <span className="text-xs font-bold text-slate-400">{unit}</span>}
      </div>
      <p className="text-[11px] text-slate-400 mt-2 flex items-center gap-1">
        {description}
      </p>
    </div>
  </div>
);

const StatusBadge = ({ status }) => {
  const styles = {
    completed: "bg-green-100 text-green-700",
    processing: "bg-yellow-100 text-yellow-700",
    uploaded: "bg-blue-100 text-blue-700",
    failed: "bg-red-100 text-red-700",
    called_for_interview: "bg-blue-600 text-white shadow-sm",
  };
  return (
    <span className={cn("px-2.5 py-1 rounded-md text-[9px] font-black uppercase tracking-widest inline-block", styles[status] || "bg-slate-100 text-slate-600")}>
      {status === 'called_for_interview' ? 'Called for Interview' : status}
    </span>
  );
};

export default AdminDashboard;
