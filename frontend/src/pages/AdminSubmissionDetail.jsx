import { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getSubmissionResults, callForInterview } from '../api/adminApi';
import {
  ArrowLeft, Trophy, Target, FileText, Download,
  Loader2, AlertCircle, Mic, Activity, RefreshCw,
  Calendar, Clock, X, CheckCircle2
} from 'lucide-react';
import { formatDate, cn } from '../utils/helpers';
import { toast } from 'react-toastify';

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

const InfoCard = ({ label, value }) => (
  <div className="bg-white border border-slate-200 rounded-xl px-4 py-3">
    <p className="text-[10px] uppercase font-semibold text-slate-400 tracking-widest mb-1">{label}</p>
    <p className="text-xs font-semibold text-slate-700">{value}</p>
  </div>
);

const MetricProgress = ({ label, score, icon: Icon }) => (
  <div className="space-y-1.5">
    <div className="flex justify-between items-center">
      <div className="flex items-center gap-2 text-xs font-medium text-slate-600">
        <Icon className="h-3.5 w-3.5 text-slate-300" />
        {label}
      </div>
      <span className="text-xs font-bold text-slate-800">{score}%</span>
    </div>
    <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
      <div
        className="h-full bg-teal-600 transition-all duration-1000"
        style={{ width: `${score}%` }}
      />
    </div>
  </div>
);

const AdminSubmissionDetail = () => {
  const { id } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showInterviewModal, setShowInterviewModal] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [interviewForm, setInterviewForm] = useState({ interview_date: '', interview_time: '' });

  const fetchDetail = useCallback(async () => {
    try {
      const results = await getSubmissionResults(id);
      setData(results);
    } catch {
      setError('Failed to load evaluation details.');
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => { fetchDetail(); }, [fetchDetail]);

  const handleCallForInterview = async (e) => {
    e.preventDefault();
    if (!interviewForm.interview_date || !interviewForm.interview_time) {
      toast.error('Please fill in both date and time');
      return;
    }
    try {
      setIsSubmitting(true);
      await callForInterview(id, interviewForm);
      toast.success('Interview invitation sent successfully');
      setShowInterviewModal(false);
      fetchDetail();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to send invitation');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleExport = async () => {
    // export logic unchanged
  };

  if (loading) return (
    <div className="h-64 flex items-center justify-center">
      <Loader2 className="h-6 w-6 animate-spin text-teal-600" />
    </div>
  );

  if (error || !data) return (
    <div className="py-24 text-center">
      <AlertCircle className="mx-auto h-8 w-8 text-red-400 mb-4" />
      <p className="text-sm font-semibold text-slate-700 mb-4">{error || 'Data not found'}</p>
      <Link to="/admin/submissions" className="text-sm text-teal-600 font-medium hover:underline">
        ← Back to submissions
      </Link>
    </div>
  );

  const { submission, result } = data;
  const isProcessing = submission.status === 'processing' || submission.status === 'uploaded';
  const isCalled = submission.status === 'called_for_interview';

  return (
    <div className="space-y-8 pb-12">

      {/* Top nav */}
      <div className="flex items-center justify-between">
        <Link
          to="/admin/submissions"
          className="inline-flex items-center gap-1.5 text-sm text-slate-400 hover:text-slate-700 transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          Submissions
        </Link>

        <div className="flex items-center gap-2">
          {isProcessing && (
            <button
              onClick={() => { setLoading(true); fetchDetail(); }}
              className="h-9 px-4 flex items-center gap-2 rounded-lg border border-slate-200 bg-white text-xs font-semibold text-slate-600 hover:bg-slate-50 transition-all"
            >
              <RefreshCw className="h-3.5 w-3.5" />
              Refresh
            </button>
          )}

          <button
            onClick={handleExport}
            disabled={isProcessing}
            className="h-9 px-4 flex items-center gap-2 rounded-lg border border-slate-200 bg-white text-xs font-semibold text-slate-600 hover:bg-slate-50 transition-all disabled:opacity-40"
          >
            <Download className="h-3.5 w-3.5" />
            Export
          </button>

          {!isProcessing && !isCalled && (
            <button
              onClick={() => setShowInterviewModal(true)}
              className="h-9 px-5 flex items-center gap-2 rounded-lg bg-teal-600 hover:bg-teal-700 text-white text-xs font-semibold transition-all"
            >
              <Calendar className="h-3.5 w-3.5" />
              Call for Interview
            </button>
          )}

          {isCalled && (
            <div className="h-9 px-4 flex items-center gap-2 rounded-lg bg-violet-50 border border-violet-100 text-violet-700 text-xs font-semibold">
              <CheckCircle2 className="h-3.5 w-3.5" />
              Interview Scheduled
            </div>
          )}
        </div>
      </div>

      {/* Main layout */}
      <div className="flex flex-col lg:flex-row gap-8">

        {/* Left */}
        <div className="flex-1 space-y-8">

          {/* Candidate header */}
          <div>
            <p className="text-xs font-semibold text-teal-600 tracking-widest uppercase mb-2">Candidate</p>
            <div className="flex items-center gap-3 mb-1">
              <h1 className="text-3xl font-black text-slate-900 tracking-tight">{submission.user_name}</h1>
              <StatusBadge status={submission.status} />
            </div>
            <p className="text-slate-500 text-sm">{submission.topic_taught}</p>
          </div>

          {/* Video */}
          <div className="bg-slate-900 rounded-2xl overflow-hidden aspect-video">
            <video
              controls
              className="w-full h-full"
              src={`http://localhost:8000/api/interview/video/${id}?token=${localStorage.getItem('token')}`}
            />
          </div>

          {/* Meta cards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <InfoCard label="Applied" value={formatDate(submission.created_at)} />
            <InfoCard label="Code" value={submission.interview_code} />
            <InfoCard label="Attempts" value="1/1" />
            <InfoCard label="Phase" value={isCalled ? "Interview" : "Evaluation"} />
          </div>

          {/* Processing state */}
          {isProcessing ? (
            <div className="bg-teal-50 border border-teal-100 rounded-xl p-8 text-center flex flex-col items-center gap-4">
              <div className="h-10 w-10 rounded-full bg-teal-100 flex items-center justify-center">
                <Loader2 className="h-5 w-5 animate-spin text-teal-600" />
              </div>
              <div>
                <p className="text-sm font-bold text-teal-900 mb-1">AI evaluation in progress</p>
                <p className="text-xs text-teal-700">The engine is analysing the video. Results will appear here shortly.</p>
              </div>
            </div>
          ) : (
            <>
              {/* Summary */}
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <FileText className="h-4 w-4 text-slate-300" />
                  <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-widest">Evaluation Summary</h3>
                </div>
                <div className="bg-white border border-slate-200 rounded-xl p-5">
                  <p className="text-sm leading-relaxed text-slate-600 italic">"{result?.summary}"</p>
                </div>
              </div>

              {/* Transcript */}
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <FileText className="h-4 w-4 text-slate-300" />
                  <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-widest">Full Transcript</h3>
                </div>
                <div className="bg-white border border-slate-200 rounded-xl p-5 max-h-60 overflow-y-auto text-[13px] leading-relaxed text-slate-500 whitespace-pre-wrap">
                  {result?.transcript}
                </div>
              </div>
            </>
          )}
        </div>

        {/* Right — AI metrics */}
        {!isProcessing && (
          <div className="w-full lg:w-72 space-y-5">

            {/* Score */}
            <div className="bg-white border border-slate-200 rounded-xl p-6 text-center">
              <p className="text-[10px] font-semibold text-slate-400 uppercase tracking-widest mb-4">Overall Score</p>
              <div className="text-6xl font-black text-teal-600 leading-none mb-1">
                {result?.score}
              </div>
              <p className="text-xs text-slate-400 mb-4">/100</p>
              <div className="h-px bg-slate-100 mb-4" />
              <p className="text-xs font-semibold text-teal-600">
                {result?.score >= 85 ? 'Excellent Candidate'
                  : result?.score >= 70 ? 'Strong Candidate'
                    : result?.score >= 55 ? 'Satisfactory'
                      : 'Needs Review'}
              </p>
            </div>

            {/* Metrics */}
            <div className="bg-white border border-slate-200 rounded-xl p-5 space-y-4">
              <p className="text-[10px] font-semibold text-slate-400 uppercase tracking-widest">Detailed Metrics</p>
              <MetricProgress label="Audio Clarity" score={result?.audio_metrics?.score || 0} icon={Mic} />
              <MetricProgress label="Posture & Confidence" score={result?.posture_metrics?.score || 0} icon={Activity} />
              <MetricProgress label="Content Accuracy" score={85} icon={Target} />
            </div>

            {/* Strengths & weaknesses */}
            <div className="bg-white border border-slate-200 rounded-xl p-5 space-y-5">
              <div>
                <div className="flex items-center gap-2 mb-3">
                  <Trophy className="h-3.5 w-3.5 text-teal-500" />
                  <p className="text-[10px] font-semibold text-teal-600 uppercase tracking-widest">Strengths</p>
                </div>
                <ul className="space-y-2.5">
                  {result?.strengths?.map((s, i) => (
                    <li key={i} className="flex gap-2.5 text-xs text-slate-600 leading-relaxed">
                      <span className="h-1.5 w-1.5 rounded-full bg-teal-400 shrink-0 mt-1.5" />
                      {s}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="h-px bg-slate-100" />

              <div>
                <div className="flex items-center gap-2 mb-3">
                  <Target className="h-3.5 w-3.5 text-amber-400" />
                  <p className="text-[10px] font-semibold text-amber-600 uppercase tracking-widest">Improvements</p>
                </div>
                <ul className="space-y-2.5">
                  {result?.weaknesses?.map((w, i) => (
                    <li key={i} className="flex gap-2.5 text-xs text-slate-600 leading-relaxed">
                      <span className="h-1.5 w-1.5 rounded-full bg-amber-400 shrink-0 mt-1.5" />
                      {w}
                    </li>
                  ))}
                </ul>
              </div>
            </div>

          </div>
        )}
      </div>

      {/* Interview Modal */}
      {showInterviewModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50">
          <div className="bg-white rounded-xl w-full max-w-md border border-slate-200 overflow-hidden">

            <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
              <div>
                <p className="text-xs font-semibold text-teal-600 tracking-widest uppercase mb-0.5">Action</p>
                <h3 className="text-base font-black text-slate-900 tracking-tight">Schedule Interview</h3>
              </div>
              <button
                onClick={() => setShowInterviewModal(false)}
                disabled={isSubmitting}
                className="p-1.5 hover:bg-slate-100 rounded-lg transition-colors"
              >
                <X className="h-4 w-4 text-slate-400" />
              </button>
            </div>

            <form onSubmit={handleCallForInterview} className="p-6 space-y-5">
              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Interview Date</label>
                <div className="relative">
                  <Calendar className="absolute left-3 top-2.5 h-4 w-4 text-slate-300" />
                  <input
                    type="date"
                    required
                    className="input pl-10"
                    value={interviewForm.interview_date}
                    onChange={(e) => setInterviewForm({ ...interviewForm, interview_date: e.target.value })}
                  />
                </div>
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Preferred Time</label>
                <div className="relative">
                  <Clock className="absolute left-3 top-2.5 h-4 w-4 text-slate-300" />
                  <input
                    type="text"
                    required
                    placeholder="e.g. 10:00 AM"
                    className="input pl-10"
                    value={interviewForm.interview_time}
                    onChange={(e) => setInterviewForm({ ...interviewForm, interview_time: e.target.value })}
                  />
                </div>
              </div>

              <div className="bg-slate-50 border border-slate-200 rounded-lg p-3">
                <p className="text-[11px] text-slate-500 leading-relaxed">
                  An automated invitation email will be sent to <span className="font-semibold text-slate-700">{submission.user_email}</span> and the candidate's status will be updated.
                </p>
              </div>

              <div className="flex gap-2 pt-1">
                <button
                  type="button"
                  onClick={() => setShowInterviewModal(false)}
                  disabled={isSubmitting}
                  className="flex-1 h-10 rounded-lg border border-slate-200 text-sm font-semibold text-slate-600 hover:bg-slate-50 transition-all"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="flex-[1.5] h-10 rounded-lg bg-teal-600 hover:bg-teal-700 text-white text-sm font-semibold flex items-center justify-center gap-2 transition-all"
                >
                  {isSubmitting ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Send Invitation →'}
                </button>
              </div>
            </form>

          </div>
        </div>
      )}

    </div>
  );
};

export default AdminSubmissionDetail;