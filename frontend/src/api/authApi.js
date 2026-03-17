import apiClient from './apiClient';

export const registerUser = async (userData) => {
  const response = await apiClient.post('/auth/register', userData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const loginUser = async (email, password) => {
  const response = await apiClient.post('/auth/login', { email, password });
  return response.data;
};
