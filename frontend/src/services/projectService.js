import httpClient from './httpClient';

export const projectService = {
  getAll: async () => {
    const response = await httpClient.get('/projects');
    return response.data;
  },

  getById: async (id) => {
    const response = await httpClient.get(`/projects/${id}`);
    return response.data;
  },

  create: async (data) => {
    const response = await httpClient.post('/projects', data);
    return response.data;
  },

  update: async (id, data) => {
    const response = await httpClient.put(`/projects/${id}`, data);
    return response.data;
  },

  delete: async (id) => {
    const response = await httpClient.delete(`/projects/${id}`);
    return response.data;
  },
};
