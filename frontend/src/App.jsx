import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ProtectedRoute, AdminRoute } from './components/ProtectedRoutes';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Layouts
import CandidateLayout from './layouts/CandidateLayout';
import AdminLayout from './layouts/AdminLayout';

// Pages - Auth
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import ResetPasswordPage from './pages/ResetPasswordPage';

// Pages - Candidate
import InterviewCodePage from './pages/InterviewCodePage';
import UploadVideoPage from './pages/UploadVideoPage';
import SubmissionSuccessPage from './pages/SubmissionSuccessPage';

// Pages - Admin
import AdminDashboard from './pages/AdminDashboard';
import AdminSubmissions from './pages/AdminSubmissions';
import AdminSubmissionDetail from './pages/AdminSubmissionDetail';
import ManageAdminsPage from './pages/ManageAdminsPage';
import InterviewCodesPage from './pages/InterviewCodesPage';

function App() {
  return (
    <Router>
      <AuthProvider>
        <ToastContainer position="top-right" autoClose={3000} />
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<CandidateLayout><LandingPage /></CandidateLayout>} />
          <Route path="/login" element={<CandidateLayout><LoginPage /></CandidateLayout>} />
          <Route path="/register" element={<CandidateLayout><RegisterPage /></CandidateLayout>} />
          <Route path="/forgot-password" element={<CandidateLayout><ForgotPasswordPage /></CandidateLayout>} />
          <Route path="/reset-password" element={<CandidateLayout><ResetPasswordPage /></CandidateLayout>} />

          {/* Protected Candidate Routes */}
          <Route path="/interview" element={
            <ProtectedRoute>
              <CandidateLayout><InterviewCodePage /></CandidateLayout>
            </ProtectedRoute>
          } />
          <Route path="/upload" element={
            <ProtectedRoute>
              <CandidateLayout><UploadVideoPage /></CandidateLayout>
            </ProtectedRoute>
          } />
          <Route path="/success" element={
            <ProtectedRoute>
              <CandidateLayout><SubmissionSuccessPage /></CandidateLayout>
            </ProtectedRoute>
          } />

          {/* Protected Admin Routes */}
          <Route path="/admin" element={
            <AdminRoute>
              <AdminLayout><AdminDashboard /></AdminLayout>
            </AdminRoute>
          } />
          <Route path="/admin/submissions" element={
            <AdminRoute>
              <AdminLayout><AdminSubmissions /></AdminLayout>
            </AdminRoute>
          } />
          <Route path="/admin/submission/:id" element={
            <AdminRoute>
              <AdminLayout><AdminSubmissionDetail /></AdminLayout>
            </AdminRoute>
          } />
          <Route path="/admin/manage-admins" element={
            <AdminRoute>
              <AdminLayout><ManageAdminsPage /></AdminLayout>
            </AdminRoute>
          } />
          <Route path="/admin/interview-codes" element={
            <AdminRoute>
              <AdminLayout><InterviewCodesPage /></AdminLayout>
            </AdminRoute>
          } />

          {/* Catch-all redirect */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
