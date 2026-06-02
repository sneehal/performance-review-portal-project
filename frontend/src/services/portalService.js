import { api, aiApi, unwrap } from './api';
export const cycles = {
  list: async () => unwrap(await api.get('/review-cycles')),
  create: async (p) => unwrap(await api.post('/review-cycles', p)),
  update: async (id,p) => unwrap(await api.put(`/review-cycles/${id}`, p)),
  progress: async (id) => unwrap(await api.get(`/review-cycles/${id}/progress`)),
};
export const goals = {
  mine: async (cycleId) => unwrap(await api.get('/goals/my', { params: cycleId ? {cycle_id: cycleId} : {} })),
  create: async (p) => unwrap(await api.post('/goals', p)),
  update: async (id,p) => unwrap(await api.put(`/goals/${id}`, p)),
  achievement: async (id, achievement) => unwrap(await api.put(`/goals/${id}/achievement`, { achievement })),
};
export const reviews = {
  mine: async (cycleId) => unwrap(await api.get(`/reviews/my/${cycleId}`)),
  selfAssessment: async (p) => unwrap(await api.post('/reviews/self-assessment', p)),
  submit: async (id) => unwrap(await api.put(`/reviews/${id}/submit`)),
};
export const manager = {
  pending: async () => unwrap(await api.get('/manager/pending-reviews')),
  submit: async (reviewId,p) => unwrap(await api.post(`/manager/review/${reviewId}`, p)),
  summary: async () => unwrap(await api.get('/manager/team-summary')),
  compare: async (reviewId) => unwrap(await api.get(`/manager/compare/${reviewId}`)),
};
export const competencies = {
  list: async () => unwrap(await api.get('/competencies')),
  submit: async (p) => unwrap(await api.post('/competencies/ratings', p)),
  ratings: async (reviewId) => unwrap(await api.get(`/competencies/ratings/${reviewId}`)),
};
export const admin = {
  ratingsSummary: async () => unwrap(await api.get('/admin/reports/ratings-summary')),
  completion: async () => unwrap(await api.get('/admin/reports/completion')),
  exportCsvUrl: () => `${api.defaults.baseURL}/admin/reports/export`,
};
export const chatbot = {
  ask: async (question, user_id) => unwrap(await aiApi.post('/chatbot/ask', { question, user_id })),
};
