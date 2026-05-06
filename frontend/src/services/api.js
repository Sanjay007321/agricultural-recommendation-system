import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/api/auth/refresh`, null, {
            params: { refresh_token: refreshToken }
          });
          
          const { access_token, refresh_token: newRefreshToken } = response.data;
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', newRefreshToken);
          
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        } catch (refreshError) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('farmer_id');
          window.location.href = '/login';
        }
      }
    }
    
    return Promise.reject(error);
  }
);

// API functions
export const authAPI = {
  login: (mobile, password) => api.post('/api/auth/login', { mobile, password }),
  register: (data) => api.post('/api/auth/register', data),
  getProfile: () => api.get('/api/auth/me'),
  updateProfile: (data) => api.put('/api/auth/profile', data),
};

export const analysisAPI = {
  analyze: (data) => api.post('/api/analyze', data),
  getHistory: () => api.get('/api/history'),
  getAnalysisDetail: (id) => api.get(`/api/history/${id}`),
  getClimateDashboard: async () => {
    const response = await api.get('/api/climate-dashboard');
    return response.data;
  }
};

export const dataAPI = {
  getCrops: () => api.get('/api/crops'),
  getSchemes: () => api.get('/api/schemes'),
  getStates: () => api.get('/api/states'),
};

export default api;
