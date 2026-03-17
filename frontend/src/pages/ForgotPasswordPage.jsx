import { useState } from 'react';
import { Link } from 'react-router-dom';
import apiClient from '../api/apiClient';
import { Mail, ArrowLeft, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';

const ForgotPasswordPage = () => {
  const [email, setEmail] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      await apiClient.post('/auth/request-password-reset', { email });
      setIsSubmitted(true);
    } catch (err) {
      setError('Failed to send reset link. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto py-16">
      <Link to="/login" className="inline-flex items-center text-sm text-neutral-500 hover:text-neutral-900 mb-8 transition-colors">
        <ArrowLeft className="h-4 w-4 mr-2" />
        Back to Sign In
      </Link>

      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold mb-2">Reset password</h1>
        <p className="text-neutral-500">We'll send you a link to reset your password.</p>
      </div>

      {isSubmitted ? (
        <div className="card text-center py-10">
          <div className="h-12 w-12 rounded-full bg-brand-sage/10 flex items-center justify-center text-brand-sage mx-auto mb-4">
            <CheckCircle2 className="h-6 w-6" />
          </div>
          <h3 className="text-lg font-bold mb-2">Check your email</h3>
          <p className="text-sm text-neutral-500 mb-6 px-4">
            If an account exists for <span className="font-semibold">{email}</span>, you will receive a reset link shortly.
          </p>
          <button onClick={() => setIsSubmitted(false)} className="text-brand-sage font-medium hover:underline text-sm">
            Try another email
          </button>
        </div>
      ) : (
        <div className="card">
          {error && (
            <div className="bg-red-50 text-red-600 p-4 rounded-lg flex items-center gap-3 mb-6 text-sm border border-red-100">
              <AlertCircle className="h-4 w-4 shrink-0" />
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-1.5">
              <label className="text-sm font-medium text-neutral-700">Email Address</label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 h-4 w-4 text-neutral-400" />
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

            <button type="submit" disabled={isLoading} className="btn btn-primary w-full h-11">
              {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Send Reset Link'}
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default ForgotPasswordPage;
