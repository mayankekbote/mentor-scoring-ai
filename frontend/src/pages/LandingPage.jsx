import { Link } from 'react-router-dom';
import { ArrowRight, Video, ShieldCheck, Sparkles } from 'lucide-react';

const LandingPage = () => {
  return (
    <div className="flex flex-col min-h-screen bg-background px-6">

      {/* Hero — left-aligned, asymmetric */}
      <div className="max-w-5xl mx-auto w-full pt-20 pb-24">
        <div className="max-w-2xl">
          <p className="text-teal-600 text-sm font-semibold tracking-widest uppercase mb-6">
            For HR & Hiring Teams
          </p>

          <h1 className="text-5xl sm:text-6xl font-black text-slate-900 leading-[1.08] tracking-tight mb-6">
            Better hiring starts with<br />
            <span className="text-teal-600">better interviews.</span>
          </h1>

          <p className="text-slate-500 text-lg leading-relaxed mb-10 max-w-lg">
            MentoraAI lets candidates submit video interviews on their schedule — then gives your team structured AI analysis to evaluate faster and more fairly.
          </p>

          <div className="flex items-center gap-3">
            <Link
              to="/interview"
              className="btn btn-primary h-11 px-6 text-sm font-semibold bg-teal-600 hover:bg-teal-700 text-white rounded-lg flex items-center gap-2 transition-all"
            >
              Apply with a code
              <ArrowRight className="h-4 w-4" />
            </Link>
            <Link
              to="/register"
              className="h-11 px-6 text-sm font-medium text-slate-600 hover:text-slate-900 flex items-center gap-1 transition-colors bg-gray-700 text-white hover:bg-gray-700 rounded-lg"
            >
              Create Account →
            </Link>
          </div>
        </div>
      </div>

      {/* Divider label */}
      <div className="max-w-5xl mx-auto w-full mb-10">
        <div className="flex items-center gap-4">
          <div className="h-px flex-1 bg-slate-200" />
          <span className="text-xs text-slate-400 font-medium tracking-widest uppercase">How it works</span>
          <div className="h-px flex-1 bg-slate-200" />
        </div>
      </div>

      {/* Feature cards — unequal, grounded */}
      <div className="max-w-5xl mx-auto w-full pb-24">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

          <div className="bg-white border border-slate-200 rounded-xl p-6 hover:border-slate-300 transition-all">
            <p className="text-xs font-semibold text-teal-600 tracking-widest uppercase mb-4">Step 01</p>
            <Video className="h-5 w-5 text-slate-400 mb-3" />
            <h3 className="text-sm font-bold text-slate-800 mb-2">Candidates record & submit</h3>
            <p className="text-sm text-slate-500 leading-relaxed">
              Share a unique code. Candidates film their response from any device, no scheduling needed.
            </p>
          </div>

          <div className="bg-teal-600 border border-teal-600 rounded-xl p-6 ">
            <p className="text-xs font-semibold text-teal-200 tracking-widest uppercase mb-4">Step 02</p>
            <Sparkles className="h-5 w-5 text-teal-200 mb-3" />
            <h3 className="text-sm font-bold text-white mb-2">AI analyses the video</h3>
            <p className="text-sm text-teal-100 leading-relaxed">
              Audio clarity, body language, content structure — scored and summarised automatically.
            </p>
          </div>

          <div className="bg-white border border-slate-200 rounded-xl p-6 hover:border-slate-300 transition-all">
            <p className="text-xs font-semibold text-teal-600 tracking-widest uppercase mb-4">Step 03</p>
            <ShieldCheck className="h-5 w-5 text-slate-400 mb-3" />
            <h3 className="text-sm font-bold text-slate-800 mb-2">Your team reviews & decides</h3>
            <p className="text-sm text-slate-500 leading-relaxed">
              Results are private, structured, and only visible to authorised HR admins.
            </p>
          </div>

        </div>
      </div>

    </div>
  );
};

export default LandingPage;