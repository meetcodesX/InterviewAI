import { CandidateProfile, InterviewConfig, QuestionResponse, AnswerEvaluationResponse, InterviewReport, DashboardStats } from '../types';

async function fetchAPI(endpoint: string, options?: RequestInit) {
  const response = await fetch(endpoint, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    let errorDetail = `API Error: ${response.statusText}`;
    try {
      const errJson = await response.json();
      if (errJson && errJson.detail) {
        errorDetail = errJson.detail;
      }
    } catch {}
    throw new Error(errorDetail);
  }
  
  if (response.headers.get('content-type')?.includes('application/json')) {
      return response.json();
  }
  return response.text();
}

export const api = {
  uploadResume: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch('/api/resume/upload', {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) {
      let detail = 'Unable to extract resume information. Please upload a valid text-based PDF.';
      try {
        const errJson = await response.json();
        if (errJson?.detail) detail = errJson.detail;
      } catch {}
      throw new Error(detail);
    }
    return response.json();
  },
  extractProfile: (resume_text: string) => fetchAPI('/api/profile/extract', { method: 'POST', body: JSON.stringify({ resume_text }) }),
  manualProfile: (data: any) => fetchAPI('/api/profile/manual', { method: 'POST', body: JSON.stringify(data) }),
  createInterview: (profile: CandidateProfile, config: InterviewConfig) => fetchAPI('/api/interview/create', { method: 'POST', body: JSON.stringify({ profile, config }) }),
  answerQuestion: (interview_id: string, question_id: string, answer: string) => fetchAPI('/api/interview/answer', { method: 'POST', body: JSON.stringify({ interview_id, question_id, answer }) }),
  nextQuestion: (interview_id: string) => fetchAPI('/api/interview/next', { method: 'POST', body: JSON.stringify({ interview_id }) }),
  finishInterview: (interview_id: string) => fetchAPI('/api/interview/finish', { method: 'POST', body: JSON.stringify({ interview_id }) }),
  getInterview: (id: string) => fetchAPI(`/api/interview/${id}`),
  getReport: (id: string) => fetchAPI(`/api/report/${id}`),
  getStats: () => fetchAPI('/api/dashboard/stats'),
  getHealth: () => fetchAPI('/api/health'),
};
