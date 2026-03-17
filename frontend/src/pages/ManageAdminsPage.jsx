import { useState, useEffect } from 'react';
import { Users, UserPlus, Mail, Lock, Shield, Loader2, CheckCircle, AlertCircle, Trash2 } from 'lucide-react';
import { getAdmins, createAdmin } from '../api/adminApi';
import { toast } from 'react-toastify';

const ManageAdminsPage = () => {
  const [admins, setAdmins] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showForm, setShowForm] = useState(false);
  
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: ''
  });

  const fetchAdmins = async () => {
    try {
      setIsLoading(true);
      const data = await getAdmins();
      setAdmins(data);
    } catch (err) {
      toast.error('Failed to load admins');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAdmins();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await createAdmin(formData);
      toast.success('Admin created successfully');
      setFormData({ name: '', email: '', password: '' });
      setShowForm(false);
      // Optimistically refresh list
      fetchAdmins();
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to create admin';
      toast.error(errorMsg);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-slate-900 tracking-tight">Manage Admins</h1>
          <p className="text-slate-500 text-sm mt-1">Add and manage HR administrators for your organization.</p>
        </div>
        
        <button 
          onClick={() => setShowForm(!showForm)}
          className={`btn flex items-center gap-2 h-11 px-6 rounded-xl font-bold transition-all ${
            showForm ? 'bg-slate-100 text-slate-600' : 'bg-teal-600 text-white shadow-lg shadow-teal-200 hover:bg-teal-700'
          }`}
        >
          {showForm ? 'Cancel' : (
            <>
              <UserPlus className="h-4 w-4" />
              Add New Admin
            </>
          )}
        </button>
      </div>

      {showForm && (
        <div className="card bg-white border-teal-100 p-8 shadow-xl animate-in slide-in-from-top-4 duration-300">
          <div className="flex items-center gap-3 mb-6">
            <div className="h-10 w-10 rounded-xl bg-teal-50 flex items-center justify-center text-teal-600">
              <Shield className="h-5 w-5" />
            </div>
            <h2 className="text-xl font-bold text-slate-900">Create Admin Account</h2>
          </div>

          <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-2">
              <label className="label text-slate-500 flex items-center gap-2">
                <Users className="h-3 w-3" /> Full Name
              </label>
              <input
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                className="input h-12"
                placeholder="John Doe"
                required
              />
            </div>

            <div className="space-y-2">
              <label className="label text-slate-500 flex items-center gap-2">
                <Mail className="h-3 w-3" /> Email Address
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                className="input h-12"
                placeholder="john@organization.com"
                required
              />
            </div>

            <div className="space-y-2">
              <label className="label text-slate-500 flex items-center gap-2">
                <Lock className="h-3 w-3" /> Temporary Password
              </label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                className="input h-12"
                placeholder="••••••••"
                required
                minLength={8}
              />
            </div>

            <div className="md:col-span-3 flex justify-end pt-2">
              <button 
                type="submit" 
                disabled={isSubmitting}
                className="btn-primary h-12 px-10 flex items-center gap-2 disabled:opacity-50"
              >
                {isSubmitting ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Creating...
                  </>
                ) : 'Create Admin Account'}
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="card bg-white border-slate-100 shadow-sm overflow-hidden">
        <div className="p-6 border-b border-slate-50 bg-slate-50/50 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Users className="h-5 w-5 text-slate-400" />
            <span className="font-bold text-slate-700">Administrative Team</span>
            <span className="px-2 py-0.5 rounded-md bg-white border border-slate-200 text-[10px] font-black text-slate-400 uppercase">
              {admins.length} Total
            </span>
          </div>
        </div>

        {isLoading ? (
          <div className="py-20 flex flex-col items-center justify-center text-slate-400 gap-4">
            <Loader2 className="h-8 w-8 animate-spin text-teal-500" />
            <p className="text-sm font-medium">Loading administrative team...</p>
          </div>
        ) : admins.length === 0 ? (
          <div className="py-20 text-center">
            <div className="h-16 w-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4">
              <Users className="h-8 w-8 text-slate-200" />
            </div>
            <p className="text-slate-500 font-medium">No other admins found in your organization.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="bg-slate-50/50 text-[10px] font-black text-slate-400 uppercase tracking-widest border-b border-slate-100">
                  <th className="px-6 py-4">Name</th>
                  <th className="px-6 py-4">Email</th>
                  <th className="px-6 py-4">Organization</th>
                  <th className="px-6 py-4">Joined At</th>
                  <th className="px-6 py-4 text-right">Access</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50">
                {admins.map((admin) => (
                  <tr key={admin.id} className="hover:bg-slate-50/50 transition-colors group">
                    <td className="px-6 py-5">
                      <div className="flex items-center gap-3">
                        <div className="h-9 w-9 rounded-full bg-indigo-50 flex items-center justify-center text-indigo-600 font-bold text-xs">
                          {admin.name.charAt(0)}
                        </div>
                        <span className="font-bold text-slate-900">{admin.name}</span>
                      </div>
                    </td>
                    <td className="px-6 py-5">
                      <span className="text-sm text-slate-600">{admin.email}</span>
                    </td>
                    <td className="px-6 py-5">
                      <span className="px-2.5 py-1 rounded-full bg-slate-100 text-[10px] font-bold text-slate-500 uppercase tracking-tighter">
                        {admin.organization_name}
                      </span>
                    </td>
                    <td className="px-6 py-5 text-sm text-slate-500">
                      {new Date(admin.created_at).toLocaleDateString(undefined, {
                        year: 'numeric',
                        month: 'short',
                        day: 'numeric'
                      })}
                    </td>
                    <td className="px-6 py-5 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <span className="flex items-center gap-1.5 text-[10px] font-black text-teal-600 uppercase">
                          <CheckCircle className="h-3 w-3" /> Active Admin
                        </span>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default ManageAdminsPage;
