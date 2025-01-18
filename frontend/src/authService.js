import api from './api'; // Use the Axios instance from api.js

export const login = async (email, password) => {
  try {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Login failed');
  }
};

export const logout = async () => {
  try {
    await api.post('/auth/logout');
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Logout failed');
  }
};

export const refreshToken = async () => {
  try {
    const response = await api.post('/auth/refresh');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Token refresh failed');
  }
};

export const getUserData = async () => {
  try {
    const response = await api.get('/auth/home'); // withCredentials is already set in api.js
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch user data');
  }
};
