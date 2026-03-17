import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, Video, AlertCircle, CheckCircle2, X, Loader2, BrainCircuit, Sparkles } from 'lucide-react';
import { uploadInterviewVideo, submitInterview, getSubmissionStatus } from '../api/interviewApi';
import UploadProgress from '../components/UploadProgress';
import ErrorAlert from '../components/ErrorAlert';

const UploadVideoPage = () => {
  const [topic, setTopic] = useState('');
  const [videoFile, setVideoFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadedVideoPath, setUploadedVideoPath] = useState('');
  const [error, setError] = useState('');
  
  // Progress states for AI analysis
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingProgress, setProcessingProgress] = useState(0);
  const [processingMessage, setProcessingMessage] = useState('Initializing AI engine...');
  
  const fileInputRef = useRef(null);
  const navigate = useNavigate();
  
  const activeCode = localStorage.getItem('activeInterviewCode');
  const organization = localStorage.getItem('interviewOrg');

  useEffect(() => {
    if (!activeCode) {
      navigate('/interview');
    }
  }, [activeCode, navigate]);

  if (!activeCode) return null;

  const validateFile = (file) => {
    const allowedTypes = ['video/mp4', 'video/quicktime', 'video/webm'];
    const maxSize = 200 * 1024 * 1024; // 200MB

    if (!allowedTypes.includes(file.type)) {
      setError('Invalid file type. Please upload MP4, MOV, or WEBM.');
      return false;
    }
    if (file.size > maxSize) {
      setError('File is too large. Max size is 200MB.');
      return false;
    }
    return true;
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setError('');
    if (!validateFile(file)) return;

    setVideoFile(file);
    setIsUploading(true);
    setUploadProgress(0);

    try {
      const data = await uploadInterviewVideo(file, (progress) => {
        setUploadProgress(progress);
      });
      setUploadedVideoPath(data.video_path);
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.');
      setVideoFile(null);
    } finally {
      setIsUploading(false);
    }
  };

  const handleFinalSubmit = async (e) => {
    e.preventDefault();
    if (!uploadedVideoPath || !topic || !activeCode) return;

    setIsSubmitting(true);
    setError('');

    try {
      const { submission_id } = await submitInterview({
        interview_code: activeCode,
        topic_taught: topic,
        video_path: uploadedVideoPath
      });

      // Transition to processing state
      setIsProcessing(true);
      setIsSubmitting(false);

      // Simple polling for progress
      const pollInterval = setInterval(async () => {
        try {
          const statusData = await getSubmissionStatus(submission_id);
          setProcessingProgress(Math.round(statusData.progress * 100));
          setProcessingMessage(statusData.message);

          if (statusData.status === 'completed') {
            clearInterval(pollInterval);
            // Clear interview-specific session data only AFTER completion
            localStorage.removeItem('activeInterviewCode');
            localStorage.removeItem('interviewOrg');
            navigate('/success');
          } else if (statusData.status === 'failed') {
            clearInterval(pollInterval);
            setIsProcessing(false);
            setError('AI Evaluation failed. Please contact support.');
          }
        } catch (err) {
          console.error("Polling error:", err);
        }
      }, 2000);

    } catch (err) {
      setError(err.response?.data?.detail || 'Submission failed. Please try again.');
      setIsSubmitting(false);
    }
  };

  if (isProcessing) {
    return (
      <div className="max-w-2xl mx-auto py-16 text-center">
        <div className="mb-10">
          <div className="h-20 w-20 rounded-3xl bg-teal-50 flex items-center justify-center mx-auto mb-8 animate-pulse">
            <BrainCircuit className="h-10 w-10 text-teal-600" />
          </div>
          <h1 className="text-4xl font-black text-slate-900 leading-tight tracking-tight mb-4">
            AI Analysis in Progress
          </h1>
          <p className="text-slate-500 text-sm leading-relaxed max-w-md mx-auto">
            Our AI engine is currently analyzing your presentation. This usually takes 1-2 minutes. Please don't close this window.
          </p>
        </div>

        <div className="card border-teal-100 bg-white p-8 mb-8 shadow-xl relative overflow-hidden">
          {/* Animated sparkles background */}
          <div className="absolute top-4 right-4 animate-bounce">
            <Sparkles className="h-5 w-5 text-teal-200" />
          </div>
          
          <div className="flex justify-between items-end mb-4">
            <div className="text-left">
              <p className="text-[10px] uppercase font-black tracking-widest text-teal-600 mb-1">Current Intelligence Stage</p>
              <p className="text-lg font-bold text-slate-900">{processingMessage}</p>
            </div>
            <div className="text-right">
              <p className="text-3xl font-black text-teal-600">{processingProgress}%</p>
            </div>
          </div>

          <div className="h-3 w-full bg-slate-100 rounded-full overflow-hidden mb-2">
            <div 
              className="h-full bg-teal-500 transition-all duration-1000 ease-out"
              style={{ width: `${processingProgress}%` }}
            />
          </div>
          
          <div className="flex justify-between text-[10px] font-bold text-slate-400 uppercase tracking-tighter">
            <span>Extraction</span>
            <span>Transcription</span>
            <span>Cognitive Evaluation</span>
          </div>
        </div>

        <div className="flex items-center justify-center gap-2 text-slate-400 text-xs font-medium italic">
          <Loader2 className="h-3 w-3 animate-spin" />
          Securing your results...
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto py-16">
      <div className="mb-10">
        <p className="label text-brand-sage mb-6">Submission Step</p>
        <h1 className="text-4xl font-black text-slate-900 leading-tight tracking-tight mb-4">
          Upload your response
        </h1>
        <p className="text-slate-500 text-sm leading-relaxed">
          You are submitting an interview for <span className="text-teal-600 font-bold">{organization || 'the hiring organization'}</span>.
        </p>
      </div>

      <ErrorAlert message={error} />

      <form onSubmit={handleFinalSubmit} className="space-y-8 mt-8">
        {/* Topic Input */}
        <div className="space-y-2">
          <label className="label text-slate-500">Topic Taught</label>
          <input
            className="input h-12"
            placeholder="e.g. Fundamental Principles of React"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            required
            disabled={isUploading || isSubmitting}
          />
        </div>

        {/* Upload Area */}
        <div className="space-y-3">
          <label className="label text-slate-500">Interview Video</label>
          
          {!videoFile ? (
            <div 
              onClick={() => !isUploading && !isSubmitting && fileInputRef.current?.click()}
              className="bg-white border-2 border-dashed border-slate-200 rounded-2xl p-12 text-center hover:border-teal-500 hover:bg-slate-50/50 cursor-pointer transition-all group"
            >
              <div className="h-12 w-12 rounded-full bg-slate-100 flex items-center justify-center mx-auto mb-4 group-hover:bg-teal-50 transition-colors">
                <Upload className="h-6 w-6 text-slate-400 group-hover:text-teal-600" />
              </div>
              <p className="text-sm font-bold text-slate-700 mb-1">Select your video file</p>
              <p className="text-xs text-slate-400">MP4, MOV or WEBM (Max 200MB)</p>
              <input 
                type="file" 
                ref={fileInputRef} 
                className="hidden" 
                accept="video/mp4,video/quicktime,video/webm" 
                onChange={handleFileChange}
              />
            </div>
          ) : (
            <div className="bg-white border border-slate-200 rounded-xl p-5">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-4">
                  <div className="h-10 w-10 rounded-lg bg-teal-50 flex items-center justify-center text-teal-600">
                    <Video className="h-5 w-5" />
                  </div>
                  <div className="min-w-0">
                    <p className="text-sm font-bold text-slate-900 truncate max-w-[300px]">{videoFile.name}</p>
                    <p className="text-xs text-slate-400">{(videoFile.size / (1024 * 1024)).toFixed(2)} MB</p>
                  </div>
                </div>
                {!isUploading && !isSubmitting && (
                  <button 
                    type="button" 
                    onClick={() => { setVideoFile(null); setUploadedVideoPath(''); }}
                    className="p-2 hover:bg-red-50 rounded-full text-slate-400 hover:text-red-500 transition-colors"
                  >
                    <X className="h-5 w-5" />
                  </button>
                )}
                {uploadedVideoPath && !isUploading && (
                  <CheckCircle2 className="h-5 w-5 text-teal-600" />
                )}
              </div>

              {(isUploading || (uploadProgress > 0 && uploadProgress < 100)) && (
                <UploadProgress progress={uploadProgress} filename={videoFile.name} />
              )}
              
              {uploadedVideoPath && !isUploading && (
                <div className="flex items-center gap-2 text-teal-600 bg-teal-50/50 p-2 px-3 rounded-lg">
                  <CheckCircle2 className="h-4 w-4" />
                  <span className="text-xs font-semibold">Upload complete</span>
                </div>
              )}
            </div>
          )}
        </div>

        <button 
          type="submit" 
          disabled={!uploadedVideoPath || !topic || isUploading || isSubmitting}
          className="btn-primary w-full h-12 text-sm font-semibold disabled:bg-slate-100 disabled:text-slate-400 disabled:border-slate-100 flex items-center justify-center gap-2"
        >
          {isSubmitting ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              Submitting interview...
            </>
          ) : (
            'Finalize Submission'
          )}
        </button>
      </form>
    </div>
  );
};

export default UploadVideoPage;
