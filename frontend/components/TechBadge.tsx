export function TechBadge({ text }: { text: string }) {
  return (
    <div className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-800 text-indigo-300 border border-slate-700">
      {text}
    </div>
  );
}
