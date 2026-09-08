'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { LoadingSpinner } from '@/components/LoadingSpinner';

export default function ConfigurePage() {
  const router = useRouter();
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const p = sessionStorage.getItem('candidateProfile');
    if (p) setProfile(JSON.parse(p));
    else router.push('/upload');
  }, [router]);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData(e.currentTarget);
    const config = {
      job_role: formData.get('job_role') as string,
      experience_level: formData.get('experience_level') as string,
      interview_type: formData.get('interview_type') as any,
      difficulty: formData.get('difficulty') as any,
      num_questions: Number(formData.get('num_questions'))
    };

    try {
      const res = await api.createInterview(profile, config);
      // Store first question so interview page can load it instantly
      sessionStorage.setItem('firstQuestion', JSON.stringify(res));
      router.push(`/interview/${res.interview_id}`);
    } catch (err) {
      console.error(err);
      alert('Failed to start interview');
      setLoading(false);
    }
  };

  if (!profile) return null;

  return (
    <div className="max-w-3xl mx-auto w-full p-6 py-12">
      <h1 className="text-3xl font-bold mb-8 text-white">Configure Interview</h1>
      
      {loading ? (
        <LoadingSpinner message="Preparing your customized interview environment..." />
      ) : (
        <form onSubmit={handleSubmit} className="space-y-8 bg-slate-800/50 p-6 rounded-xl border border-slate-700">
          <div className="grid grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Job Role</label>
              <input name="job_role" defaultValue={profile.target_role} className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white focus:border-indigo-500 outline-none" />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Experience Level</label>
              <select name="experience_level" defaultValue={profile.experience_level} className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white focus:border-indigo-500 outline-none">
                <option>Fresher</option><option>0-2 years</option><option>2-5 years</option><option>5+ years</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">Interview Type</label>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {['technical', 'hr', 'behavioral', 'mixed'].map(t => (
                <label key={t} className="cursor-pointer">
                  <input type="radio" name="interview_type" value={t} defaultChecked={t === 'technical'} className="peer sr-only" />
                  <div className="text-center py-2 px-3 bg-slate-900 border border-slate-700 rounded-lg peer-checked:border-indigo-500 peer-checked:bg-indigo-900/30 text-slate-400 peer-checked:text-indigo-300 capitalize transition-all">{t}</div>
                </label>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">Difficulty</label>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {['easy', 'medium', 'hard', 'adaptive'].map(d => (
                <label key={d} className="cursor-pointer">
                  <input type="radio" name="difficulty" value={d} defaultChecked={d === 'adaptive'} className="peer sr-only" />
                  <div className="text-center py-2 px-3 bg-slate-900 border border-slate-700 rounded-lg peer-checked:border-indigo-500 peer-checked:bg-indigo-900/30 text-slate-400 peer-checked:text-indigo-300 capitalize transition-all">{d}</div>
                </label>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">Number of Questions</label>
            <div className="flex gap-4">
              {[5, 10, 15].map(n => (
                <label key={n} className="cursor-pointer flex items-center gap-2">
                  <input type="radio" name="num_questions" value={n} defaultChecked={n === 5} className="text-indigo-500" />
                  <span className="text-slate-300">{n}</span>
                </label>
              ))}
            </div>
          </div>

          <button type="submit" className="w-full py-4 bg-indigo-600 hover:bg-indigo-500 rounded-lg font-bold text-white text-lg transition-colors shadow-lg shadow-indigo-500/20">
            Start AI Interview
          </button>
        </form>
      )}
    </div>
  );
}
