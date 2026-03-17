import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Key, ArrowRight, Loader2 } from 'lucide-react';
import { validateInterviewCode } from '../api/interviewApi';
import ErrorAlert from '../components/ErrorAlert';

const InterviewCodePage = () => {
  const [code, setCode] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleValidate = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const data = await validateInterviewCode(code);
      localStorage.setItem('activeInterviewCode', code);
      localStorage.setItem('interviewOrg', data.organization_name || 'the hiring organization');
      navigate('/upload');
    } catch (err) {
      if (err.response) {
        const detail = err.response.data?.detail;
        if (detail === "Interview code not found") {
          setError("This interview code was not found. Please double-check and try again.");
        } else if (detail === "Interview code expired") {
          setError("This interview code has expired. Please contact your hiring manager for a new one.");
        } else {
          setError(detail || "An error occurred while validating your code.");
        }
      } else if (err.request) {
        setError("Unable to connect to the server. Please check your internet connection.");
      } else {
        setError("An unexpected error occurred. Please try again later.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto py-16 px-6">
      <div className="grid grid-cols-1 md:grid-cols-5 gap-12 items-center">

        {/* Left — context */}
        <div className="md:col-span-2">
          <p className="text-xs font-semibold text-teal-600 tracking-widest uppercase mb-4">Step 1 of 2</p>
          <h1 className="text-3xl font-black text-slate-900 leading-tight tracking-tight mb-4">
            Enter your invite code
          </h1>
          <p className="text-slate-500 text-sm leading-relaxed mb-8">
            Your recruiter sent a unique access code via email. Enter it here to begin your video interview.
          </p>

          <div className="space-y-4">
            <div className="flex items-start gap-3">
              <div className="mt-0.5 h-5 w-5 rounded-full bg-teal-50 border border-teal-100 flex items-center justify-center shrink-0">
                <span className="text-[10px] font-bold text-teal-600">1</span>
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-700">Validate your code</p>
                <p className="text-xs text-slate-400 leading-relaxed">Confirm your access to the interview session.</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="mt-0.5 h-5 w-5 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center shrink-0">
                <span className="text-[10px] font-bold text-slate-400">2</span>
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-400">Upload your video</p>
                <p className="text-xs text-slate-300 leading-relaxed">Record and submit your teaching demonstration.</p>
              </div>
            </div>
          </div>
        </div>

        {/* Right — form */}
        <div className="md:col-span-3">
          <div className="bg-white border border-slate-200 rounded-xl p-8">

            <ErrorAlert message={error} />

            <form onSubmit={handleValidate} className={`space-y-5 ${error ? 'mt-6' : ''}`}>
              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-500 uppercase tracking-wide">
                  Interview Code
                </label>
                <div className="relative">
                  <Key className="absolute left-3 top-3.5 h-4 w-4 text-slate-300" />
                  <input
                    autoFocus
                    className="input pl-10 h-12 text-base font-bold tracking-widest placeholder:font-normal placeholder:tracking-normal"
                    placeholder="E.g. INTERVIEW-2024"
                    value={code}
                    onChange={(e) => setCode(e.target.value.toUpperCase())}
                    required
                    disabled={isLoading}
                  />
                </div>
                <p className="text-[11px] text-slate-400">Codes are case-insensitive — we'll handle the formatting.</p>
              </div>

              <button
                type="submit"
                disabled={isLoading || !code}
                className="w-full h-11 bg-teal-600 hover:bg-teal-700 disabled:opacity-50 text-white text-sm font-semibold rounded-lg flex items-center justify-center gap-2 transition-all mt-2"
              >
                {isLoading ? (
                  <><Loader2 className="h-4 w-4 animate-spin" /> Validating...</>
                ) : (
                  <>Continue to Upload <ArrowRight className="h-4 w-4" /></>
                )}
              </button>
            </form>
          </div>

          <p className="mt-5 text-xs text-slate-400 text-center">
            Code not working?{' '}
            <span className="text-teal-600 font-medium">Contact your recruiter for support.</span>
          </p>
        </div>

      </div>
    </div>
  );
};

export default InterviewCodePage;