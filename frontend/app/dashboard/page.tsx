'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { api } from '@/lib/api';
import { LoadingSpinner } from '@/components/LoadingSpinner';
import { DashboardStats } from '@/types';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getStats()
      .then(setStats)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="flex-1 flex items-center justify-center"><LoadingSpinner message="Loading dashboard..." /></div>;

  return (
    <div className="max-w-6xl mx-auto w-full p-6 py-8 space-y-8">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-white">Dashboard</h1>
        <Link href="/upload" className="px-6 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-lg transition-colors">New Interview</Link>
      </div>

      {!stats || stats.total_interviews === 0 ? (
        <div className="text-center py-20 bg-slate-800/50 rounded-xl border border-slate-700">
          <h3 className="text-xl font-semibold text-slate-300 mb-2">No interviews yet</h3>
          <p className="text-slate-500 mb-6">Start your first AI mock interview to see your stats here.</p>
          <Link href="/upload" className="px-6 py-2 bg-slate-700 hover:bg-slate-600 text-white font-medium rounded-lg transition-colors">Get Started</Link>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-slate-800 p-5 rounded-xl border border-slate-700">
              <div className="text-slate-400 text-sm mb-1">Total Interviews</div>
              <div className="text-3xl font-bold text-white">{stats.total_interviews}</div>
            </div>
            <div className="bg-slate-800 p-5 rounded-xl border border-slate-700">
              <div className="text-slate-400 text-sm mb-1">Average Score</div>
              <div className="text-3xl font-bold text-indigo-400">{stats.average_score}<span className="text-lg text-slate-500">/100</span></div>
            </div>
            <div className="bg-slate-800 p-5 rounded-xl border border-slate-700 flex flex-col">
              <div className="text-slate-400 text-sm mb-1">Strongest Skill</div>
              <div className="text-base sm:text-lg font-bold text-emerald-400 mt-2 break-words leading-snug whitespace-normal">
                {stats.strongest_skill || 'N/A'}
              </div>
            </div>
            <div className="bg-slate-800 p-5 rounded-xl border border-slate-700 flex flex-col">
              <div className="text-slate-400 text-sm mb-1">Weakest Skill</div>
              <div className="text-base sm:text-lg font-bold text-rose-400 mt-2 break-words leading-snug whitespace-normal">
                {stats.weakest_skill || 'N/A'}
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-6">Score History</h3>
              <div className="h-[250px]">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={stats.score_history} margin={{ top: 5, right: 20, bottom: 5, left: -20 }}>
                    <Line type="monotone" dataKey="score" stroke="#6366f1" strokeWidth={3} dot={{ fill: '#6366f1', strokeWidth: 2 }} />
                    <CartesianGrid stroke="#334155" strokeDasharray="5 5" vertical={false} />
                    <XAxis dataKey="date" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} domain={[0, 100]} />
                    <Tooltip contentStyle={{backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '8px'}} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-4">Recent Interviews</h3>
              <div className="space-y-3">
                {stats.recent_interviews?.map((int: any, i: number) => (
                  <Link key={i} href={`/report/${int.id}`} className="flex items-center justify-between p-4 bg-slate-900/50 hover:bg-slate-700/50 rounded-lg transition-colors border border-slate-800 hover:border-slate-600">
                    <div>
                      <div className="font-medium text-slate-200">{int.role}</div>
                      <div className="text-sm text-slate-500">{new Date(int.date).toLocaleDateString()}</div>
                    </div>
                    <div className="text-xl font-bold text-indigo-400">{int.score}</div>
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
