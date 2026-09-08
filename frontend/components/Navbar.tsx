import Link from 'next/link';

export function Navbar() {
  return (
    <nav className="flex items-center justify-between p-4 bg-slate-900 border-b border-slate-800">
      <Link href="/" className="text-xl font-bold text-indigo-400">InterviewAI</Link>
      <div className="flex gap-4">
        <Link href="/dashboard" className="text-sm text-slate-300 hover:text-white">Dashboard</Link>
        <Link href="/upload" className="text-sm bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded-lg text-white font-medium transition-colors">Start Interview</Link>
      </div>
    </nav>
  );
}
