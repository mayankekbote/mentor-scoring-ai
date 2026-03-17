import { useNavigate, Link } from 'react-router-dom';
import { CheckCircle2, ArrowRight, Home } from 'lucide-react';

const SubmissionSuccessPage = () => {
  const navigate = useNavigate();
  const organization = localStorage.getItem('interviewOrg') || 'the hiring organization';

  return (
    <div className="max-w-2xl mx-auto py-16">
      <div className="max-w-md">
        <div className="h-16 w-16 rounded-2xl bg-teal-50 flex items-center justify-center text-teal-600 mb-8">
          <CheckCircle2 className="h-8 w-8" />
        </div>

        <p className="label text-brand-sage mb-6">Submission Complete</p>
        
        <h1 className="text-4xl font-black text-slate-900 leading-tight tracking-tight mb-4">
          Interview Received
        </h1>
        
        <p className="text-slate-500 text-sm leading-relaxed mb-6">
          Your interview for <span className="text-slate-900 font-bold">{organization}</span> has been successfully submitted.
        </p>

        <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 mb-10">
          <p className="text-xs text-slate-500 leading-relaxed font-medium">
            <span className="text-slate-900 font-bold uppercase tracking-wider block mb-1">What's next?</span>
            Our AI engine is currently processing your video to extract key insights for the hiring team. You don't need to do anything else.
          </p>
        </div>

        <div className="flex flex-col gap-3">
          <Link 
            to="/" 
            className="btn-primary h-12 flex items-center justify-center gap-2 text-sm font-semibold"
          >
            Return to Homepage
            <Home className="h-4 w-4" />
          </Link>
          
          <button 
            onClick={() => {
              localStorage.removeItem('token');
              localStorage.removeItem('user');
              navigate('/login');
            }}
            className="h-12 text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors flex items-center justify-center gap-2"
          >
            Sign out of MentoraAI
            <ArrowRight className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default SubmissionSuccessPage;
