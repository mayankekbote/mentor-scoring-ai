const UploadProgress = ({ progress, filename }) => {
  return (
    <div className="card bg-slate-50 border-slate-100 p-5">
      <div className="flex justify-between text-xs mb-3">
        <span className="font-semibold text-slate-700 truncate max-w-[240px]">{filename}</span>
        <span className="text-brand-sage font-black">{progress}%</span>
      </div>
      <div className="w-full bg-slate-200 rounded-full h-1.5 overflow-hidden">
        <div 
          className="bg-brand-sage h-full transition-all duration-300 ease-out"
          style={{ width: `${progress}%` }}
        />
      </div>
      <p className="text-[10px] text-slate-400 mt-3 text-center uppercase tracking-wider font-medium">
        Uploading to secure storage. Do not close.
      </p>
    </div>
  );
};

export default UploadProgress;
