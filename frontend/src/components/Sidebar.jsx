import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, FileText, Settings, LogOut, Key } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Sidebar = () => {
  const location = useLocation();
  const { user, logout } = useAuth();

  const menuItems = [
    { label: 'Dashboard', icon: LayoutDashboard, path: '/admin' },
    { label: 'Submissions', icon: FileText, path: '/admin/submissions' },
    { label: 'Interview Codes', icon: Key, path: '/admin/interview-codes' },
    { label: 'Manage Admins', icon: Settings, path: '/admin/manage-admins' },
  ];

  return (
    <aside className="w-64 border-r border-slate-200 bg-white flex flex-col sticky top-0 h-screen">
      <div className="h-14 flex items-center px-6 border-b border-slate-50">
        <span className="label text-slate-900">Admin Panel</span>
      </div>

      <nav className="flex-1 p-4 space-y-1">
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all ${
                isActive 
                  ? "bg-slate-50 text-brand-sage font-semibold" 
                  : "text-slate-500 hover:bg-slate-50 hover:text-slate-900"
              }`}
            >
              <item.icon className={`h-4 w-4 ${isActive ? "text-brand-sage" : "text-slate-400"}`} />
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-slate-50 space-y-4">
        <div className="flex items-center gap-3 px-2">
          <div className="h-8 w-8 rounded bg-slate-900 flex items-center justify-center text-white text-xs font-bold">
            {user?.name?.[0]?.toUpperCase()}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-semibold text-slate-900 truncate">{user?.name}</p>
            <p className="text-[10px] text-slate-400 uppercase tracking-tight">HR Admin</p>
          </div>
        </div>
        
        <button
          onClick={logout}
          className="w-full flex items-center gap-3 px-3 py-2 text-sm text-slate-500 hover:text-red-500 hover:bg-red-50 rounded-lg transition-all"
        >
          <LogOut className="h-4 w-4" />
          Logout
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
