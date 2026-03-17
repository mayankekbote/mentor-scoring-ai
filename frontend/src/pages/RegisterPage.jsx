import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { toast } from 'react-toastify';
import { User, Mail, Lock, Briefcase, Calendar, GraduationCap, Loader2 } from 'lucide-react';
import { registerUser } from '../api/authApi';
import ErrorAlert from '../components/ErrorAlert';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    age: '',
    subject_domain: '',
    years_experience: '',
    organization: '',
    resume: null
  });

  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    if (e.target.name === 'resume') {
      setFormData({ ...formData, resume: e.target.files[0] });
    } else {
      setFormData({ ...formData, [e.target.name]: e.target.value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const data = new FormData();
      Object.keys(formData).forEach(key => {
        if (formData[key] !== null) {
          data.append(key, formData[key]);
        }
      });

      await registerUser(data);
      toast.success('Registration successful! Please login.');
      navigate('/login');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto py-16 px-6">
      <div className="grid grid-cols-1 md:grid-cols-5 gap-12 items-start">

        {/* Left — context panel */}
        <div className="md:col-span-2 md:pt-2">
          <p className="text-xs font-semibold text-teal-600 tracking-widest uppercase mb-4">Candidate Portal</p>
          <h1 className="text-3xl font-black text-slate-900 leading-tight tracking-tight mb-4">
            Start your application
          </h1>
          <p className="text-slate-500 text-sm leading-relaxed mb-8">
            Create your account to access the interview platform and submit your video response.
          </p>

          <div className="space-y-4">
            <div className="flex items-start gap-3">
              <div className="mt-0.5 h-5 w-5 rounded-full bg-teal-50 border border-teal-100 flex items-center justify-center shrink-0">
                <span className="text-[10px] font-bold text-teal-600">1</span>
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-700">Create your profile</p>
                <p className="text-xs text-slate-400 leading-relaxed">Fill in your background and upload your resume.</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="mt-0.5 h-5 w-5 rounded-full bg-teal-50 border border-teal-100 flex items-center justify-center shrink-0">
                <span className="text-[10px] font-bold text-teal-600">2</span>
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-700">Enter your interview code</p>
                <p className="text-xs text-slate-400 leading-relaxed">Your HR team will share a unique access code.</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="mt-0.5 h-5 w-5 rounded-full bg-teal-50 border border-teal-100 flex items-center justify-center shrink-0">
                <span className="text-[10px] font-bold text-teal-600">3</span>
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-700">Record & submit</p>
                <p className="text-xs text-slate-400 leading-relaxed">Film your response on any device, on your schedule.</p>
              </div>
            </div>
          </div>
        </div>

        {/* Right — form */}
        <div className="md:col-span-3">
          <div className="bg-white border border-slate-200 rounded-xl p-8">

            <ErrorAlert message={error} />

            <form onSubmit={handleSubmit} className="space-y-5">

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Full Name</label>
                  <div className="relative">
                    <User className="absolute left-3 top-3 h-4 w-4 text-slate-300" />
                    <input name="name" required className="input pl-10" placeholder="Aryan Varma" onChange={handleChange} />
                  </div>
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Email</label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-3 h-4 w-4 text-slate-300" />
                    <input name="email" type="email" required className="input pl-10" placeholder="aryanvarma@gmail.com" onChange={handleChange} />
                  </div>
                </div>
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Password</label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-4 w-4 text-slate-300" />
                  <input name="password" type="password" required className="input pl-10" placeholder="••••••••" onChange={handleChange} />
                </div>
              </div>

              <div className="h-px bg-slate-100" />

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Age</label>
                  <div className="relative">
                    <Calendar className="absolute left-3 top-3 h-4 w-4 text-slate-300" />
                    <input name="age" type="number" required className="input pl-10" onChange={handleChange} />
                  </div>
                </div>

                <div className="sm:col-span-2 space-y-1.5">
                  <label className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Subject Domain</label>
                  <div className="relative">
                    <GraduationCap className="absolute left-3 top-3 h-4 w-4 text-slate-300" />
                    <input name="subject_domain" required className="input pl-10" placeholder="e.g. Mathematics" onChange={handleChange} />
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Experience (Years)</label>
                  <div className="relative">
                    <Briefcase className="absolute left-3 top-3 h-4 w-4 text-slate-300" />
                    <input name="years_experience" type="number" required className="input pl-10" onChange={handleChange} />
                  </div>
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Organization</label>
                  <input name="organization" required className="input" placeholder="e.g. University X" onChange={handleChange} />
                </div>
              </div>

              <div className="h-px bg-slate-100" />

              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Resume</label>
                <input
                  name="resume"
                  type="file"
                  accept=".pdf"
                  required
                  className="input py-2 file:mr-4 file:py-1 file:px-3 file:rounded-md file:border-0 file:text-xs file:font-semibold file:bg-teal-600 file:text-white hover:file:bg-teal-700 cursor-pointer"
                  onChange={handleChange}
                />
                <p className="text-[11px] text-slate-400">PDF only · Max 5MB</p>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="btn btn-primary w-full h-11 bg-teal-600 hover:bg-teal-700 text-white font-semibold rounded-lg flex items-center justify-center gap-2 transition-all mt-2"
              >
                {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Create Account →'}
              </button>

            </form>
          </div>

          <p className="text-center mt-5 text-sm text-slate-400">
            Already have an account?{' '}
            <Link to="/login" className="text-teal-600 font-medium hover:underline">
              Sign in
            </Link>
          </p>
        </div>

      </div>
    </div>
  );
};

export default RegisterPage;