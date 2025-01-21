import axiosInstance from '../api/axiosInstance';

export const login = async (username: string, password: string) => {
  const response = await axiosInstance.get('/login', {
    auth: { username, password },
  });
  return response.data;
};

export const fetchUserDetails = async () => {
  const response = await axiosInstance.get('/me');
  return response.data;
};
