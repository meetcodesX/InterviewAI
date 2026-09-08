'use client';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();

  const handleDemo = () => {
    const demoProfile = {
      name: "Alex Sharma",
      target_role: "ML Engineer",
      skills: ["Python", "Machine Learning", "Deep Learning", "RAG", "NLP"],
      experience_level: "Fresher",
      years_of_experience: 0,
      education: [],
      projects: [],
      experience: [],
      certifications: []
    };
    sessionStorage.setItem('candidateProfile', JSON.stringify(demoProfile));
    router.push('/configure');
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-64px)] px-4 py-16 bg-gradient-to-b from-slate-900 to-slate-950">
      <div className="max-w-4xl w-full text-center space-y-8">
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">
          InterviewAI
        </h1>
        <p className="text-xl md:text-2xl text-slate-300">
          Your AI-powered, personalized interview trainer
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 my-12 text-left">
          {[
            { title: "Resume-aware", desc: "Interviews tailored to your specific experience" },
            { title: "RAG-powered", desc: "Deep knowledge base for accurate role evaluation" },
            { title: "Adaptive AI", desc: "Questions scale in difficulty based on your answers" },
            { title: "Instant Feedback", desc: "Real-time evaluation of your responses" },
            { title: "Skill Analysis", desc: "Detailed gap analysis and improvement areas" },
          ].map((feature, i) => (
            <div key={i} className="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50 backdrop-blur-sm">
              <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
              <p className="text-slate-400 text-sm">{feature.desc}</p>
            </div>
          ))}
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mt-8">
          <Link href="/upload" className="px-8 py-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-semibold text-lg transition-all shadow-[0_0_20px_rgba(79,70,229,0.3)]">
            Start Interview
          </Link>
          <button onClick={handleDemo} className="px-8 py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-semibold text-lg transition-all border border-slate-700">
            Try Demo
          </button>
        </div>

        <div className="pt-16 flex justify-center items-center">
          <p className="text-sm text-slate-400 font-medium tracking-wide">
            Made with <span className="text-red-500">❤️</span> by Meet Sahu
          </p>
        </div>
      </div>
    </div>
  );
}
