import { useState, useEffect } from 'react';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import { toast } from 'react-toastify';
import { useAuth } from '../context/AuthContext';
import { Mail, Lock, Loader2 } from 'lucide-react';
import ErrorAlert from '../components/ErrorAlert';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (location.state?.message) {
      toast.info(location.state.message);
      window.history.replaceState({}, document.title);
    }
  }, [location]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const user = await login(email, password);
      toast.success(`Welcome back, ${user.name}!`);
      if (user.is_admin) {
        navigate('/admin');
      } else {
        navigate('/interview');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid email or password');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto py-16 px-6">
      <div className="grid grid-cols-1 md:grid-cols-5 gap-12 items-center">

        {/* Left — context */}
        <div className="md:col-span-2">
          <p className="text-xs font-semibold text-teal-600 tracking-widest uppercase mb-4">Candidate Portal</p>
          <h1 className="text-3xl font-black text-slate-900 leading-tight tracking-tight mb-4">
            Welcome back
          </h1>
          <p className="text-slate-500 text-sm leading-relaxed mb-8">
            Sign in to access your interview dashboard and continue your application.
          </p>

          <div className="space-y-4">
            <div className="flex items-start gap-3">
              <div className="mt-0.5 h-5 w-5 rounded-full bg-teal-50 border border-teal-100 flex items-center justify-center shrink-0">
                <span className="text-[10px] font-bold text-teal-600">✓</span>
              </div>
              <p className="text-sm text-slate-500 leading-relaxed">Track your submission status in real time</p>
            </div>
            <div className="flex items-start gap-3">
              <div className="mt-0.5 h-5 w-5 rounded-full bg-teal-50 border border-teal-100 flex items-center justify-center shrink-0">
                <span className="text-[10px] font-bold text-teal-600">✓</span>
              </div>
              <p className="text-sm text-slate-500 leading-relaxed">Upload and manage your interview video</p>
            </div>
            <div className="flex items-start gap-3">
              <div className="mt-0.5 h-5 w-5 rounded-full bg-teal-50 border border-teal-100 flex items-center justify-center shrink-0">
                <span className="text-[10px] font-bold text-teal-600">✓</span>
              </div>
              <p className="text-sm text-slate-500 leading-relaxed">Secure and private </p>
            </div>
          </div>
        </div>

        {/* Right — form */}
        <div className="md:col-span-3">
          <div className="bg-white border border-slate-200 rounded-xl p-8">

            <ErrorAlert message={error} />

            <form onSubmit={handleSubmit} className="space-y-5">

              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Email Address</label>
                <div className="relative">
                  <Mail className="absolute left-3 top-3 h-4 w-4 text-slate-300" />
                  <input
                    type="email"
                    required
                    className="input pl-10"
                    placeholder="name@company.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </div>
              </div>

              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <label className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Password</label>
                  <Link to="/forgot-password" className="text-xs text-teal-600 hover:underline">
                    Forgot password?
                  </Link>
                </div>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-4 w-4 text-slate-300" />
                  <input
                    type="password"
                    required
                    className="input pl-10"
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="btn btn-primary w-full h-11 bg-teal-600 hover:bg-teal-700 text-white font-semibold rounded-lg flex items-center justify-center gap-2 transition-all mt-2"
              >
                {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Sign in →'}
              </button>

            </form>
          </div>

          <p className="text-center mt-5 text-sm text-slate-400">
            Don't have an account?{' '}
            <Link to="/register" className="text-teal-600 font-medium hover:underline">
              Create one now
            </Link>
          </p>
        </div>

      </div>
    </div>
  );
};

export default LoginPage;