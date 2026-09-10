'use client';
import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/lib/api';
import { LoadingSpinner } from '@/components/LoadingSpinner';
import { ScoreCard } from '@/components/ScoreCard';
import { TechBadge } from '@/components/TechBadge';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { InterviewReport } from '@/types';

export default function ReportPage() {
  const { id } = useParams();
  const [report, setReport] = useState<InterviewReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    api.getReport(id as string)
      .then(setReport)
      .catch((e) => {
        console.error(e);
        setError('Failed to load report. The interview may not be completed yet.');
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="flex-1 flex items-center justify-center min-h-[60vh]"><LoadingSpinner message="Loading your performance report..." /></div>;

  if (error || !report) return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 min-h-[60vh] space-y-4">
      <div className="w-16 h-16 rounded-full bg-rose-900/30 flex items-center justify-center">
        <svg className="w-8 h-8 text-rose-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" /></svg>
      </div>
      <p className="text-rose-400 text-lg">{error || 'Report not available'}</p>
      <Link href="/dashboard" className="px-6 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg transition-colors border border-slate-700">
        Go to Dashboard
      </Link>
    </div>
  );

  const chartData = [
    { name: 'Overall', score: report.overall_score },
    { name: 'Technical', score: report.technical_score },
    { name: 'Communication', score: report.communication_score },
    { name: 'Problem Solving', score: report.problem_solving_score },
    { name: 'Role Readiness', score: report.role_readiness_score },
  ];

  return (
    <div className="max-w-5xl mx-auto w-full p-4 py-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Interview Performance Report</h1>
          <p className="text-slate-400">
            Candidate: <span className="text-white">{report.candidate_name}</span> •
            Role: <span className="text-white">{report.target_role}</span> •
            Questions: <span className="text-white">{report.questions_answered}/{report.total_questions}</span>
          </p>
        </div>
        <div className="flex gap-3">
          <Link href="/dashboard" className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg transition-colors border border-slate-700 text-sm">
            Dashboard
          </Link>
          <Link href="/upload" className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg transition-colors text-sm">
            New Interview
          </Link>
        </div>
      </div>

      {/* Score Cards */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="col-span-2 md:col-span-1">
          <ScoreCard label="Overall Score" score={report.overall_score} max={100} />
        </div>
        <ScoreCard label="Technical" score={report.technical_score} max={100} />
        <ScoreCard label="Communication" score={report.communication_score} max={100} />
        <ScoreCard label="Problem Solving" score={report.problem_solving_score} max={100} />
        <ScoreCard label="Role Readiness" score={report.role_readiness_score} max={100} />
      </div>

      {/* Chart and Difficulty */}
      <div className="grid md:grid-cols-3 gap-6">
        <div className="md:col-span-2 bg-slate-800 p-6 rounded-xl border border-slate-700">
          <h3 className="text-lg font-semibold text-white mb-6">Performance Breakdown</h3>
          <div className="h-[250px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} domain={[0, 100]} />
                <Tooltip
                  cursor={{fill: '#1e293b'}}
                  contentStyle={{backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '8px', color: '#e2e8f0'}}
                />
                <Bar dataKey="score" fill="#6366f1" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 space-y-6">
          <div>
            <h3 className="text-sm font-semibold text-slate-400 mb-3 uppercase tracking-wider">Difficulty Progression</h3>
            <div className="flex flex-wrap gap-2">
              {report.difficulty_progression?.map((d: string, i: number) => (
                <span key={i} className={`text-xs px-2 py-1 rounded font-medium ${
                  d === 'easy' ? 'bg-emerald-900/30 text-emerald-400 border border-emerald-800/50' :
                  d === 'hard' ? 'bg-rose-900/30 text-rose-400 border border-rose-800/50' :
                  'bg-amber-900/30 text-amber-400 border border-amber-800/50'
                }`}>
                  {i > 0 && <span className="text-slate-600 mr-1">→</span>}
                  {d}
                </span>
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-emerald-400 mb-2 uppercase tracking-wider">Key Strengths</h3>
            <ul className="text-sm text-slate-300 space-y-1">
              {report.strengths?.map((s: string, i: number) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-0.5">✓</span>
                  <span>{s}</span>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-amber-400 mb-2 uppercase tracking-wider">Areas to Improve</h3>
            <ul className="text-sm text-slate-300 space-y-1">
              {report.weaknesses?.map((w: string, i: number) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-amber-400 mt-0.5">△</span>
                  <span>{w}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
        <h3 className="text-lg font-semibold text-white mb-4">
          AI-Generated Personalized Improvement Roadmap
        </h3>
        <ul className="space-y-3">
          {report.recommendations?.map((r: string, i: number) => (
            <li key={i} className="flex gap-3 items-start bg-slate-900/50 p-4 rounded-lg">
              <span className="flex-shrink-0 w-7 h-7 rounded-full bg-indigo-900/50 text-indigo-400 flex items-center justify-center text-sm font-bold border border-indigo-800/50">
                {i + 1}
              </span>
              <span className="text-slate-300 text-sm leading-relaxed">{r}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Question-by-question breakdown */}
      {report.question_evaluations && report.question_evaluations.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-white">Question-by-Question Breakdown</h3>
          {report.question_evaluations.map((q: any, i: number) => (
            <details key={i} className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden group">
              <summary className="p-4 cursor-pointer font-medium text-slate-200 hover:bg-slate-700/50 transition-colors flex justify-between items-center">
                <span className="flex-1 truncate mr-4">Q{i + 1}: {q.question || `Question ${i + 1}`}</span>
                <span className={`text-sm font-bold flex-shrink-0 ${
                  (q.score || q.evaluation?.overall_score || 0) >= 7 ? 'text-emerald-400' :
                  (q.score || q.evaluation?.overall_score || 0) >= 4 ? 'text-amber-400' :
                  'text-rose-400'
                }`}>
                  Score: {q.score || q.evaluation?.overall_score || 0}/10
                </span>
              </summary>
              <div className="p-4 bg-slate-900/50 border-t border-slate-700 text-sm space-y-3">
                {q.answer && (
                  <div>
                    <span className="text-slate-500 font-medium block mb-1">Your Answer:</span>
                    <div className="text-slate-300 italic bg-slate-800/50 p-3 rounded-lg">&quot;{q.answer}&quot;</div>
                  </div>
                )}
                <div>
                  <span className="text-slate-500 font-medium block mb-1">Feedback:</span>
                  <div className="text-slate-300">{q.feedback || q.evaluation?.feedback || 'No detailed feedback available.'}</div>
                </div>
              </div>
            </details>
          ))}
        </div>
      )}

      {/* Tech footer */}
      <div className="flex justify-center gap-3 pt-4 border-t border-slate-800">
        <TechBadge text="Powered by Gemini + RAG" />
        <TechBadge text="LangGraph" />
      </div>
    </div>
  );
}
