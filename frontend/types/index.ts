export interface CandidateProfile {
  name: string;
  education: string[];
  skills: string[];
  projects: string[];
  experience: string[];
  certifications: string[];
  target_role: string;
  experience_level: string;
  years_of_experience: number;
}

export interface InterviewConfig {
  job_role: string;
  experience_level: string;
  interview_type: 'technical' | 'hr' | 'behavioral' | 'mixed';
  difficulty: 'easy' | 'medium' | 'hard' | 'adaptive';
  num_questions: number;
}

export interface QuestionResponse {
  question_id: string;
  question_number: number;
  total_questions: number;
  category: string;
  difficulty: string;
  question: string;
  interview_id: string;
}

export interface EvaluationResponse {
  overall_score: number;
  technical_accuracy: number;
  relevance: number;
  clarity: number;
  completeness: number;
  strengths: string[];
  weaknesses: string[];
  feedback: string;
  recommended_difficulty: string;
}

export interface AnswerEvaluationResponse {
  question_id: string;
  question: string;
  answer: string;
  evaluation: EvaluationResponse;
}

export interface InterviewReport {
  interview_id: string;
  candidate_name: string;
  target_role: string;
  overall_score: number;
  technical_score: number;
  communication_score: number;
  problem_solving_score: number;
  role_readiness_score: number;
  questions_answered: number;
  total_questions: number;
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
  difficulty_progression: string[];
  question_evaluations: any[];
  created_at: string;
}

export interface DashboardStats {
  total_interviews: number;
  average_score: number;
  strongest_skill: string;
  weakest_skill: string;
  recent_interviews: any[];
  score_history: any[];
}
