import { useNavigate, Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  LayoutDashboard,
  Users,
  FileText,
  Settings,
  LogOut,
  ChevronRight
} from 'lucide-react';
import { cn } from '../utils/helpers';
import Sidebar from '../components/Sidebar';

const AdminLayout = ({ children }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const menuItems = [
    { label: 'Overview', icon: LayoutDashboard, path: '/admin' },
    { label: 'Submissions', icon: FileText, path: '/admin/submissions' },
    { label: 'Candidates', icon: Users, path: '/admin/candidates' },
    { label: 'Settings', icon: Settings, path: '/admin/settings' },
  ];

  return (
    <div className="min-h-screen bg-background flex">
      <Sidebar />

      <main className="flex-1 overflow-auto">
        <div className="p-12 max-w-7xl">
          {children}
        </div>
      </main>
    </div>
  );
};

export default AdminLayout;
