import Navbar from '../components/Navbar';

const CandidateLayout = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Navbar />

      <main className="flex-1">
        <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
          {children}
        </div>
      </main>

      <footer className="border-t border-slate-100 bg-white py-8">
        <div className="mx-auto max-w-7xl px-4 text-center">
          <p className="text-xs text-slate-400">© 2026 MentoraAI. Your AI Agent for Interview Workflow Automation.</p>
        </div>
      </footer>
    </div>
  );
};

export default CandidateLayout;