import { useState, useEffect } from 'react';
import {
  Key,
  Plus,
  Calendar,
  Users,
  Copy,
  Check,
  AlertCircle,
  Clock,
  Loader2,
  ExternalLink,
  ShieldCheck
} from 'lucide-react';
import { getInterviewCodes, createInterviewCode } from '../api/adminApi';
import { toast } from 'react-toastify';

const InterviewCodesPage = () => {
  const [codes, setCodes] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [copiedCode, setCopiedCode] = useState(null);

  const [formData, setFormData] = useState({
    max_attempts: 50,
    expiry_date: ''
  });

  const fetchCodes = async () => {
    try {
      setIsLoading(true);
      const data = await getInterviewCodes();
      setCodes(data);
    } catch (err) {
      toast.error('Failed to load interview codes');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCodes();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const expiryDate = new Date(formData.expiry_date);
    if (expiryDate <= new Date()) {
      toast.error('Expiry date must be in the future');
      setIsSubmitting(false);
      return;
    }

    try {
      await createInterviewCode({
        ...formData,
        max_attempts: parseInt(formData.max_attempts),
        expiry_date: expiryDate.toISOString()
      });
      toast.success('Interview code generated successfully');
      setFormData({ max_attempts: 50, expiry_date: '' });
      setShowForm(false);
      fetchCodes();
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to generate code';
      toast.error(errorMsg);
    } finally {
      setIsSubmitting(false);
    }
  };

  const copyToClipboard = async (code) => {
    try {
      await navigator.clipboard.writeText(code);
      setCopiedCode(code);
      setTimeout(() => setCopiedCode(null), 2000);
      toast.success('Code copied to clipboard', { autoClose: 1000 });
    } catch (err) {
      toast.error('Failed to copy code');
    }
  };

  const getStatus = (expiryDate) => {
    const now = new Date();
    const expiry = new Date(expiryDate);
    return expiry > now ? 'Active' : 'Expired';
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-slate-900 tracking-tight">Interview Codes</h1>
          <p className="text-slate-500 text-sm mt-1">Generate and manage unique access codes for current campaigns.</p>
        </div>

        <button
          onClick={() => setShowForm(!showForm)}
          className={`btn flex items-center gap-2 h-11 px-6 rounded-xl font-bold transition-all duration-300 cursor-pointer ${showForm 
              ? 'bg-slate-100 text-slate-600 hover:bg-slate-200' 
              : 'bg-brand-sage text-white shadow-lg shadow-sage-200 hover:bg-brand-sage-dark hover:scale-105 active:scale-95 hover:shadow-xl'
            }`}
        >
          {showForm ? 'Cancel' : (
            <>
              <Plus className="h-4 w-4" />
              Generate New Code
            </>
          )}
        </button>
      </div>

      {showForm && (
        <div className="card bg-white border-brand-sage-light p-8 shadow-xl animate-in slide-in-from-top-4 duration-300">
          <div className="flex items-center gap-3 mb-6">
            <div className="h-10 w-10 rounded-xl bg-teal-50 flex items-center justify-center text-teal-600">
              <Key className="h-5 w-5" />
            </div>
            <h2 className="text-xl font-bold text-slate-900">Configure Interview Code</h2>
          </div>

          <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="label text-slate-500 flex items-center gap-2">
                <Users className="h-3 w-3" /> Max Attempts
              </label>
              <input
                type="number"
                name="max_attempts"
                value={formData.max_attempts}
                onChange={handleInputChange}
                className="input h-12"
                placeholder="50"
                min="1"
                required
              />
              <p className="text-[10px] text-slate-400">Total number of candidates who can use this code.</p>
            </div>

            <div className="space-y-2">
              <label className="label text-slate-500 flex items-center gap-2">
                <Calendar className="h-3 w-3" /> Expiry Date
              </label>
              <input
                type="datetime-local"
                name="expiry_date"
                value={formData.expiry_date}
                onChange={handleInputChange}
                className="input h-12"
                required
              />
              <p className="text-[10px] text-slate-400">After this date, the code will no longer be valid.</p>
            </div>

            <div className="md:col-span-2 flex justify-end pt-2">
              <button
                type="submit"
                disabled={isSubmitting}
                className="btn-primary h-12 px-10 flex items-center gap-2 disabled:opacity-50"
              >
                {isSubmitting ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Generating...
                  </>
                ) : 'Generate Permanent Code'}
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="card bg-white border-slate-100 shadow-sm overflow-hidden">
        <div className="p-6 border-b border-slate-50 bg-slate-50/50 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldCheck className="h-5 w-5 text-slate-400" />
            <span className="font-bold text-slate-700">Organization Campaign Codes</span>
            <span className="px-2 py-0.5 rounded-md bg-white border border-slate-200 text-[10px] font-black text-slate-400 uppercase">
              {codes.length} Validated
            </span>
          </div>
        </div>

        {isLoading ? (
          <div className="py-20 flex flex-col items-center justify-center text-slate-400 gap-4">
            <Loader2 className="h-8 w-8 animate-spin text-brand-sage" />
            <p className="text-sm font-medium">Synchronizing campaign data...</p>
          </div>
        ) : codes.length === 0 ? (
          <div className="py-24 text-center">
            <div className="h-16 w-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4">
              <Key className="h-8 w-8 text-slate-200" />
            </div>
            <h3 className="text-slate-900 font-bold text-lg">No codes generated yet</h3>
            <p className="text-slate-500 text-sm max-w-xs mx-auto mt-2">Create your first interview code to start receiving submissions from candidates.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-50/50 text-[10px] font-black text-slate-400 uppercase tracking-widest border-b border-slate-100">
                  <th className="px-6 py-4">Code</th>
                  <th className="px-6 py-4">Max Attempts</th>
                  <th className="px-6 py-4">Expiry Date</th>
                  <th className="px-6 py-4">Status</th>
                  <th className="px-6 py-4">Created At</th>
                  <th className="px-6 py-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50">
                {codes.map((item) => {
                  const status = getStatus(item.expiry_date);
                  const isCopied = copiedCode === item.code;
                  
                  return (
                    <tr key={item.id} className="hover:bg-slate-50/50 transition-colors group">
                      <td className="px-6 py-5">
                        <code className="px-3 py-1.5 rounded-lg bg-slate-100 border border-slate-200 text-indigo-600 font-mono font-bold text-sm">
                          {item.code}
                        </code>
                      </td>
                      <td className="px-6 py-5">
                        <div className="flex items-center gap-2">
                          <Users className="h-3.5 w-3.5 text-slate-400" />
                          <span className="text-sm font-bold text-slate-700">{item.max_attempts}</span>
                          <span className="text-[10px] text-slate-400 font-black uppercase tracking-tighter">Slots</span>
                        </div>
                      </td>
                      <td className="px-6 py-5">
                        <div className="flex items-center gap-2 text-slate-500 font-medium">
                          <Calendar className="h-3.5 w-3.5" />
                          <span className="text-xs">
                            {new Date(item.expiry_date).toLocaleDateString(undefined, {
                              year: 'numeric',
                              month: 'short',
                              day: 'numeric'
                            })}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-5">
                        <span className={`px-2.5 py-1 rounded-md text-[10px] font-black uppercase tracking-widest ${
                          status === 'Active' 
                            ? 'bg-green-100 text-green-700' 
                            : 'bg-red-100 text-red-700'
                        }`}>
                          {status}
                        </span>
                      </td>
                      <td className="px-6 py-5 text-[10px] font-black text-slate-400 uppercase tracking-widest">
                        {new Date(item.created_at).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-5 text-right">
                        <button 
                          onClick={() => copyToClipboard(item.code)}
                          className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                            isCopied 
                              ? 'bg-green-100 text-green-700 border border-green-200 shadow-sm' 
                              : 'bg-white border border-slate-200 text-slate-600 hover:border-brand-sage hover:text-brand-sage hover:bg-brand-sage/5 active:scale-95'
                          }`}
                        >
                          {isCopied ? (
                            <>
                              <Check className="h-3 w-3" />
                              Copied!
                            </>
                          ) : (
                            <>
                              <Copy className="h-3 w-3" />
                              Copy
                            </>
                          )}
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="bg-indigo-50/50 border border-indigo-100 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center gap-4">
        <div className="h-12 w-12 rounded-full bg-white flex items-center justify-center shadow-sm text-indigo-600">
          <ExternalLink className="h-6 w-6" />
        </div>
        <div>
          <h4 className="font-bold text-indigo-900">How to use these codes</h4>
          <p className="text-sm text-indigo-700/70">Share these codes with your candidates. They will need to enters the code on the interview start page to begin their AI-evaluated presentation.</p>
        </div>
      </div>
    </div>
  );
};

export default InterviewCodesPage;
