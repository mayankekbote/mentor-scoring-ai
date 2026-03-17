import { useState } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import apiClient from '../api/apiClient';
import { Lock, AlertCircle, Loader2, CheckCircle2, ArrowLeft } from 'lucide-react';

const ResetPasswordPage = () => {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [error, setError] = useState('');
  
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      return setError('Passwords do not match');
    }
    
    setIsLoading(true);
    setError('');

    try {
      await apiClient.post('/auth/reset-password', {
        token,
        new_password: password
      });
      setIsSuccess(true);
      setTimeout(() => navigate('/login'), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to reset password. The link may be invalid or expired.');
    } finally {
      setIsLoading(false);
    }
  };

  if (!token) {
    return (
      <div className="max-w-md mx-auto py-20 text-center">
        <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
        <h1 className="text-2xl font-bold mb-2">Invalid Link</h1>
        <p className="text-neutral-500 mb-8">This password reset link is missing a valid token.</p>
        <Link to="/forgot-password" size="sm" className="btn btn-primary">
          Request new link
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto py-16">
      <div className="text-center mb-10">
        <h1 className="text-3xl font-bold mb-2">Set new password</h1>
        <p className="text-neutral-500">Please enter your new password below.</p>
      </div>

      {isSuccess ? (
        <div className="card text-center py-10">
          <div className="h-12 w-12 rounded-full bg-brand-sage/10 flex items-center justify-center text-brand-sage mx-auto mb-4">
            <CheckCircle2 className="h-6 w-6" />
          </div>
          <h3 className="text-lg font-bold mb-2">Password reset!</h3>
          <p className="text-sm text-neutral-500 mb-6">
            Your password has been updated successfully. Redirecting you to login...
          </p>
          <Link to="/login" className="btn btn-primary w-full">Go to Login</Link>
        </div>
      ) : (
        <div className="card">
          {error && (
            <div className="bg-red-50 text-red-600 p-4 rounded-lg flex items-center gap-3 mb-6 text-sm border border-red-100 font-medium">
              <AlertCircle className="h-4 w-4 shrink-0" />
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-1.5">
              <label className="text-sm font-medium text-neutral-700">New Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 h-4 w-4 text-neutral-400" />
                <input
                  type="password"
                  required
                  className="input pl-10"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  minLength={8}
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="text-sm font-medium text-neutral-700">Confirm New Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 h-4 w-4 text-neutral-400" />
                <input
                  type="password"
                  required
                  className="input pl-10"
                  placeholder="••••••••"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  minLength={8}
                />
              </div>
            </div>

            <button type="submit" disabled={isLoading} className="btn btn-primary w-full h-11 text-base">
              {isLoading ? <Loader2 className="h-5 w-5 animate-spin" /> : 'Reset Password'}
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default ResetPasswordPage;
