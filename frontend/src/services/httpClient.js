import axios from 'axios';
import { config } from '../config/environment';

const httpClient = axios.create({
  baseURL: config.apiBaseUrl,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

httpClient.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

httpClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response;
      
      if (status === 401) {
        console.error('Unauthorized access');
      } else if (status === 403) {
        console.error('Forbidden access');
      } else if (status === 404) {
        console.error('Resource not found');
      } else if (status >= 500) {
        console.error('Server error');
      }
      
      return Promise.reject(data || error.message);
    }
    
    if (error.request) {
      console.error('Network error');
      return Promise.reject('Network error. Please check your connection.');
    }
    
    return Promise.reject(error.message);
  }
);

export default httpClient;
