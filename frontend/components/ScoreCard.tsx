export function ScoreCard({ label, score, max = 10 }: { label: string, score: number, max?: number }) {
  const percentage = (score / max) * 100;
  let color = "text-indigo-400";
  if (percentage >= 80) color = "text-emerald-400";
  else if (percentage < 60) color = "text-amber-400";

  return (
    <div className="bg-slate-800 p-4 rounded-xl border border-slate-700 flex flex-col items-center justify-center">
      <div className="text-sm text-slate-400 mb-1">{label}</div>
      <div className={`text-3xl font-bold ${color}`}>
        {score}<span className="text-sm text-slate-500">/{max}</span>
      </div>
    </div>
  );
}
