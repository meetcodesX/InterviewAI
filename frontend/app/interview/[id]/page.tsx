'use client';
import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { LoadingSpinner } from '@/components/LoadingSpinner';
import { ScoreCard } from '@/components/ScoreCard';
import { TechBadge } from '@/components/TechBadge';
import { QuestionResponse, EvaluationResponse } from '@/types';

export default function InterviewPage() {
  const { id } = useParams();
  const router = useRouter();
  const interviewId = id as string;

  const [loading, setLoading] = useState(true);
  const [loadingMsg, setLoadingMsg] = useState('Retrieving role-specific interview context...');
  const [question, setQuestion] = useState<QuestionResponse | null>(null);
  const [answer, setAnswer] = useState('');
  const [evaluation, setEvaluation] = useState<EvaluationResponse | null>(null);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [isFinished, setIsFinished] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    // Try to get the first question from sessionStorage (set by configure page)
    const stored = sessionStorage.getItem('firstQuestion');
    if (stored) {
      try {
        const q = JSON.parse(stored);
        if (q && q.question_id) {
          setQuestion(q);
          setLoading(false);
          sessionStorage.removeItem('firstQuestion');
          return;
        }
      } catch (e) {}
    }

    // Fallback: fetch current question from API
    const fetchQuestion = async () => {
      try {
        const q = await api.nextQuestion(interviewId);
        if (q && q.question_id) {
          setQuestion(q);
        } else {
          setIsFinished(true);
        }
      } catch (e) {
        console.error(e);
        setError('Failed to load interview question. Please try again.');
      } finally {
        setLoading(false);
      }
    };
    fetchQuestion();
  }, [interviewId]);

  const handleSubmitAnswer = async () => {
    if (!answer.trim() || !question) return;
    setIsEvaluating(true);
    setError('');
    try {
      const res = await api.answerQuestion(interviewId, question.question_id, answer);
      // Handle different response shapes
      const evalData = res.evaluation || res;
      setEvaluation(evalData);
    } catch (error) {
      console.error(error);
      setError('Failed to evaluate answer. Please try again.');
    } finally {
      setIsEvaluating(false);
    }
  };

  const handleSkip = async () => {
    // Submit empty answer first to advance state, then get next
    try {
      setLoading(true);
      setLoadingMsg('Skipping to next question...');
      setEvaluation(null);
      setAnswer('');
      await api.answerQuestion(interviewId, question?.question_id || '', '(Skipped)');
      const q = await api.nextQuestion(interviewId);
      if (q && q.question_id) {
        setQuestion(q);
      } else {
        setIsFinished(true);
      }
    } catch (e) {
      console.error(e);
      setIsFinished(true);
    } finally {
      setLoading(false);
    }
  };

  const handleNext = async () => {
    setEvaluation(null);
    setAnswer('');
    setError('');
    setLoading(true);
    setLoadingMsg('Gemini is generating next question...');
    try {
      const q = await api.nextQuestion(interviewId);
      if (q && q.question_id) {
        setQuestion(q);
      } else {
        setIsFinished(true);
      }
    } catch (e) {
      console.error(e);
      setIsFinished(true);
    } finally {
      setLoading(false);
    }
  };

  const handleFinish = async () => {
    setLoading(true);
    setLoadingMsg('Compiling your interview report...');
    try {
      await api.finishInterview(interviewId);
      router.push(`/report/${interviewId}`);
    } catch (e) {
      console.error(e);
      router.push(`/report/${interviewId}`);
    }
  };

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center min-h-[60vh]">
        <LoadingSpinner message={loadingMsg} />
      </div>
    );
  }

  if (isEvaluating) {
    return (
      <div className="flex-1 flex items-center justify-center min-h-[60vh]">
        <LoadingSpinner message="Evaluating your answer..." />
      </div>
    );
  }

  if (isFinished) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-6 space-y-6 min-h-[60vh]">
        <div className="w-16 h-16 rounded-full bg-emerald-900/30 flex items-center justify-center mb-4">
          <svg className="w-8 h-8 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
        </div>
        <h2 className="text-3xl font-bold text-white">Interview Complete!</h2>
        <p className="text-slate-400 text-lg">Great job. Let&apos;s see how you performed.</p>
        <button onClick={handleFinish} className="px-8 py-3 bg-indigo-600 hover:bg-indigo-500 rounded-lg font-bold text-white text-lg shadow-lg shadow-indigo-500/20 transition-all">
          View Final Report
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto w-full p-4 py-8 flex flex-col">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-6 gap-4">
        <div className="flex items-center gap-3 flex-wrap">
          <div className="px-3 py-1.5 bg-slate-800 rounded-lg text-sm font-medium text-white border border-slate-700">
            Question {question?.question_number} of {question?.total_questions}
          </div>
          <span className="text-xs font-medium px-2.5 py-1 bg-indigo-900/40 text-indigo-300 rounded-full border border-indigo-800/50 uppercase tracking-wider">
            {question?.category}
          </span>
          <span className={`text-xs font-medium px-2.5 py-1 rounded-full border uppercase tracking-wider ${
            question?.difficulty === 'easy' ? 'bg-emerald-900/40 text-emerald-300 border-emerald-800/50' :
            question?.difficulty === 'hard' ? 'bg-rose-900/40 text-rose-300 border-rose-800/50' :
            'bg-amber-900/40 text-amber-300 border-amber-800/50'
          }`}>
            {question?.difficulty}
          </span>
        </div>
        <div className="hidden md:flex gap-2">
          <TechBadge text="Powered by Gemini + RAG" />
          <TechBadge text="LangGraph" />
        </div>
      </div>

      {/* Progress bar */}
      <div className="w-full bg-slate-800 rounded-full h-1.5 mb-6">
        <div
          className="bg-indigo-500 h-1.5 rounded-full transition-all duration-500"
          style={{ width: `${((question?.question_number || 1) / (question?.total_questions || 10)) * 100}%` }}
        />
      </div>

      {/* Question */}
      <div className="bg-slate-800/80 p-6 rounded-xl border border-slate-700 mb-6 shadow-xl">
        <h2 className="text-xl md:text-2xl font-semibold text-white leading-relaxed">
          {question?.question}
        </h2>
      </div>

      {error && (
        <div className="mb-4 p-4 bg-rose-900/20 border border-rose-800/50 rounded-xl text-rose-300 text-sm">
          {error}
        </div>
      )}

      {!evaluation ? (
        /* Answer input */
        <div className="flex flex-col flex-1 space-y-4">
          <textarea
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            placeholder="Type your answer here... Be detailed and provide examples where possible."
            className="w-full flex-1 min-h-[200px] bg-slate-900 border border-slate-700 rounded-xl p-4 text-white text-base leading-relaxed resize-none focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500/50 transition-all placeholder-slate-600"
          />
          <div className="flex justify-between items-center">
            <div className="text-sm text-slate-500">{answer.length} characters</div>
            <div className="flex gap-3">
              <button
                onClick={handleSkip}
                className="px-6 py-2.5 text-slate-400 hover:text-white transition-colors rounded-lg hover:bg-slate-800"
              >
                Skip Question
              </button>
              <button
                onClick={handleSubmitAnswer}
                disabled={!answer.trim()}
                className="px-8 py-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 disabled:cursor-not-allowed rounded-lg font-semibold text-white transition-all shadow-lg shadow-indigo-500/20"
              >
                Submit Answer
              </button>
            </div>
          </div>
        </div>
      ) : (
        /* Evaluation display */
        <div className="space-y-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <ScoreCard label="Overall" score={evaluation.overall_score || 0} />
            <ScoreCard label="Tech Accuracy" score={evaluation.technical_accuracy || 0} />
            <ScoreCard label="Relevance" score={evaluation.relevance || 0} />
            <ScoreCard label="Clarity" score={evaluation.clarity || 0} />
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-emerald-900/20 border border-emerald-800/50 p-5 rounded-xl">
              <h3 className="text-emerald-400 font-semibold mb-3 flex items-center gap-2">
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                What You Did Well
              </h3>
              <ul className="list-disc list-inside text-sm text-slate-300 space-y-1">
                {evaluation.strengths?.map((s: string, i: number) => <li key={i}>{s}</li>)}
              </ul>
            </div>
            <div className="bg-amber-900/20 border border-amber-800/50 p-5 rounded-xl">
              <h3 className="text-amber-400 font-semibold mb-3 flex items-center gap-2">
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" /></svg>
                How to Improve
              </h3>
              <ul className="list-disc list-inside text-sm text-slate-300 space-y-1">
                {evaluation.weaknesses?.map((w: string, i: number) => <li key={i}>{w}</li>)}
              </ul>
            </div>
          </div>

          <div className="bg-slate-800 p-5 rounded-xl border border-slate-700">
            <h3 className="text-white font-semibold mb-2">Feedback</h3>
            <p className="text-slate-300 text-sm leading-relaxed">{evaluation.feedback}</p>
          </div>

          <div className="flex justify-between items-center pt-2">
            <div className="text-sm text-slate-500">
              Next difficulty: <span className={`font-medium ${
                evaluation.recommended_difficulty === 'hard' ? 'text-rose-400' :
                evaluation.recommended_difficulty === 'easy' ? 'text-emerald-400' :
                'text-amber-400'
              }`}>{evaluation.recommended_difficulty}</span>
            </div>
            {(question?.question_number || 0) >= (question?.total_questions || 0) ? (
              <button
                onClick={handleFinish}
                className="px-8 py-3 bg-emerald-600 hover:bg-emerald-500 rounded-lg font-bold text-white shadow-lg transition-all"
              >
                Complete Interview
              </button>
            ) : (
              <button
                onClick={handleNext}
                className="px-8 py-3 bg-indigo-600 hover:bg-indigo-500 rounded-lg font-bold text-white shadow-lg shadow-indigo-500/20 transition-all"
              >
                Next Question →
              </button>
            )}
          </div>
        </div>
      )}

      {/* Mobile tech badge */}
      <div className="flex md:hidden justify-center gap-2 mt-8 pt-4 border-t border-slate-800">
        <TechBadge text="Powered by Gemini + RAG" />
        <TechBadge text="LangGraph" />
      </div>
    </div>
  );
}
