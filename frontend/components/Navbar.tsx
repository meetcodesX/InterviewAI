import Link from "next/link";

export function Navbar() {
  return (
    <nav className="w-full border-b border-slate-800 bg-slate-950">
      <div className="mx-auto flex min-h-[76px] w-full max-w-7xl items-center justify-between px-6 sm:px-8">
        {/* Logo */}
        <Link
          href="/"
          className="text-2xl font-bold tracking-tight text-indigo-400 transition-colors hover:text-indigo-300"
        >
          InterviewAI
        </Link>

        {/* Navigation */}
        <div className="flex items-center gap-6">
          <Link
            href="/dashboard"
            className="text-sm font-medium text-slate-300 transition-colors hover:text-white"
          >
            Dashboard
          </Link>

          <Link
            href="/upload"
            className="rounded-lg bg-indigo-600 px-5 py-3 text-sm font-semibold text-white transition-colors hover:bg-indigo-700"
          >
            Start Interview
          </Link>
        </div>
      </div>
    </nav>
  );
}