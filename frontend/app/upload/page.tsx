'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { LoadingSpinner } from '@/components/LoadingSpinner';

export default function UploadPage() {
  const [tab, setTab] = useState<'upload' | 'manual'>('upload');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [profile, setProfile] = useState<any>(null);
  const [uploadedFileName, setUploadedFileName] = useState<string | null>(null);
  const router = useRouter();

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.[0]) return;
    const file = e.target.files[0];
    setUploadedFileName(file.name);
    setLoading(true);
    setError(null);
    try {
      const result = await api.uploadResume(file);
      setProfile(result.profile);
    } catch (err: any) {
      console.error(err);
      setError(err?.message || 'Unable to extract resume information. Please upload a valid text-based PDF.');
      setProfile(null);
    } finally {
      setLoading(false);
    }
  };

  const handleManualSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    const formData = new FormData(e.currentTarget);
    const data = {
      name: formData.get('name'),
      target_role: formData.get('target_role'),
      experience_level: formData.get('experience_level'),
      skills: (formData.get('skills') as string).split(',').map(s => s.trim()).filter(Boolean),
      years_of_experience: Number(formData.get('years_of_experience')),
      education: [],
      projects: [],
      experience: [],
      certifications: []
    };
    setProfile(data);
  };

  const handleConfirm = () => {
    sessionStorage.setItem('candidateProfile', JSON.stringify(profile));
    router.push('/configure');
  };

  const handleReset = () => {
    setProfile(null);
    setError(null);
    setUploadedFileName(null);
  };

  return (
    <div className="max-w-3xl mx-auto w-full p-6 py-12">
      <h1 className="text-3xl font-bold mb-8 text-white">Provide Your Profile</h1>

      {error && (
        <div className="mb-6 p-4 bg-rose-950/70 border border-rose-600 rounded-xl text-rose-200 flex items-start gap-3">
          <svg className="w-5 h-5 text-rose-400 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <div>
            <div className="font-semibold text-rose-300">Extraction Error</div>
            <div className="text-sm mt-0.5">{error}</div>
          </div>
        </div>
      )}
      
      {loading ? (
        <LoadingSpinner message="Analyzing your uploaded resume..." />
      ) : profile ? (
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-emerald-400">Profile Extracted Successfully</h2>
            {uploadedFileName && (
              <span className="text-xs px-2.5 py-1 bg-slate-700 text-slate-300 rounded-full font-mono">
                {uploadedFileName}
              </span>
            )}
          </div>
          <div className="grid grid-cols-2 gap-4 text-sm bg-slate-900/60 p-4 rounded-lg border border-slate-700/60">
            <div><span className="text-slate-400">Name:</span> <span className="font-medium text-white">{profile.name}</span></div>
            <div><span className="text-slate-400">Target Role:</span> <span className="font-medium text-indigo-300">{profile.target_role}</span></div>
            <div><span className="text-slate-400">Experience:</span> <span className="font-medium text-white">{profile.experience_level} ({profile.years_of_experience} yrs)</span></div>
            {profile.education?.length > 0 && (
              <div className="col-span-2"><span className="text-slate-400">Education:</span> <span className="text-slate-200">{profile.education.join(' • ')}</span></div>
            )}
            <div className="col-span-2">
              <span className="text-slate-400 block mb-1.5">Detected Skills:</span>
              <div className="flex flex-wrap gap-1.5">
                {profile.skills?.map((s: string, idx: number) => (
                  <span key={idx} className="px-2 py-0.5 bg-indigo-950/80 border border-indigo-700 text-indigo-200 text-xs rounded">
                    {s}
                  </span>
                ))}
              </div>
            </div>
          </div>
          <div className="flex gap-4">
            <button
              onClick={handleReset}
              className="px-4 py-3 bg-slate-700 hover:bg-slate-600 rounded-lg font-semibold text-slate-200 transition-colors"
            >
              Upload Different Resume
            </button>
            <button
              onClick={handleConfirm}
              className="flex-1 py-3 bg-indigo-600 hover:bg-indigo-500 rounded-lg font-semibold text-white transition-colors"
            >
              Confirm & Configure Interview
            </button>
          </div>
        </div>
      ) : (
        <div className="bg-slate-800/50 rounded-xl border border-slate-700 overflow-hidden">
          <div className="flex border-b border-slate-700">
            <button
              onClick={() => { setTab('upload'); setError(null); }}
              className={`flex-1 py-4 text-center font-medium transition-colors ${tab === 'upload' ? 'bg-slate-700 text-white' : 'text-slate-400 hover:bg-slate-800'}`}
            >
              Upload Resume (PDF)
            </button>
            <button
              onClick={() => { setTab('manual'); setError(null); }}
              className={`flex-1 py-4 text-center font-medium transition-colors ${tab === 'manual' ? 'bg-slate-700 text-white' : 'text-slate-400 hover:bg-slate-800'}`}
            >
              Manual Entry
            </button>
          </div>
          
          <div className="p-6">
            {tab === 'upload' && (
              <div className="border-2 border-dashed border-slate-600 hover:border-indigo-500 rounded-xl p-12 text-center transition-colors relative cursor-pointer group">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileUpload}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                />
                <svg className="w-12 h-12 mx-auto text-slate-500 group-hover:text-indigo-400 transition-colors mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <div className="text-slate-300 font-medium mb-1">Drag & drop your PDF resume here, or click to browse</div>
                <div className="text-xs text-slate-500">Supports standard text-based PDF resumes (up to 10MB)</div>
              </div>
            )}
            
            {tab === 'manual' && (
              <form onSubmit={handleManualSubmit} className="space-y-4">
                <div><label className="block text-sm text-slate-400 mb-1">Full Name</label><input required name="name" placeholder="e.g. Rahul Verma" className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-white" /></div>
                <div><label className="block text-sm text-slate-400 mb-1">Target Job Role</label><input required name="target_role" placeholder="e.g. Machine Learning Engineer" className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-white" /></div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm text-slate-400 mb-1">Experience Level</label>
                    <select name="experience_level" className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-white">
                      <option value="fresher">Fresher / Graduate</option>
                      <option value="junior">Junior (0-2 years)</option>
                      <option value="mid">Mid-level (2-5 years)</option>
                      <option value="senior">Senior (5+ years)</option>
                    </select>
                  </div>
                  <div><label className="block text-sm text-slate-400 mb-1">Years of Experience</label><input type="number" min="0" max="40" defaultValue="0" required name="years_of_experience" className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-white" /></div>
                </div>
                <div><label className="block text-sm text-slate-400 mb-1">Key Technical Skills (comma separated)</label><textarea required name="skills" placeholder="e.g. Python, PyTorch, SQL, Docker, RAG" className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-white" rows={3}></textarea></div>
                <button type="submit" className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 rounded-lg font-semibold text-white transition-colors">Submit Profile</button>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
