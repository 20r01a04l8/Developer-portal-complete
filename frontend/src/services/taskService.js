import httpClient from './httpClient';

export const taskService = {
  getAll: async () => {
    const response = await httpClient.get('/tasks');
    return response.data;
  },

  getById: async (id) => {
    const response = await httpClient.get(`/tasks/${id}`);
    return response.data;
  },

  create: async (data) => {
    const response = await httpClient.post('/tasks', data);
    return response.data;
  },

  update: async (id, data) => {
    const response = await httpClient.put(`/tasks/${id}`, data);
    return response.data;
  },

  delete: async (id) => {
    const response = await httpClient.delete(`/tasks/${id}`);
    return response.data;
  },
};
