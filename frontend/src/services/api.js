import axios from 'axios';

// Get API URL from environment or use localhost
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

console.log('🌐 API Base URL:', API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Important for CORS with credentials
  timeout: 30000, // 30 second timeout
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    console.log('📤 Request:', config.method.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('❌ Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh and errors
api.interceptors.response.use(
  (response) => {
    console.log('✅ Response Success:', response.status);
    return response;
  },
  async (error) => {
    console.error('❌ Response Error:', error.response?.status, error.message);
    
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          console.log('🔄 Attempting token refresh...');
          const response = await axios.post(`${API_BASE_URL}/api/auth/refresh`, null, {
            params: { refresh_token: refreshToken },
            withCredentials: true,
          });
          
          const { access_token, refresh_token: newRefreshToken } = response.data;
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', newRefreshToken);
          
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          console.log('✅ Token refreshed successfully');
          return api(originalRequest);
        } catch (refreshError) {
          console.error('❌ Token refresh failed:', refreshError);
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
