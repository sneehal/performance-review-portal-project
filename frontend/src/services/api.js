import axios from 'axios';

export const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
export const AI_BASE = import.meta.env.VITE_AI_BASE_URL || 'http://localhost:5000';

const attachToken = (config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
};

export const api = axios.create({ baseURL: API_BASE });
export const aiApi = axios.create({ baseURL: AI_BASE });
api.interceptors.request.use(attachToken);
aiApi.interceptors.request.use(attachToken);

api.interceptors.response.use(r => r, err => {
  if (err?.response?.status === 401) {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }
  return Promise.reject(err);
});

export const unwrap = (res) => res.data?.data ?? res.data;
export const errMsg = (err) => err?.response?.data?.detail || err?.response?.data?.message || err.message || 'Something went wrong';
