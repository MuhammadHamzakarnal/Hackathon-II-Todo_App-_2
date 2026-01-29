const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

const getAuthToken = () => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('token');
  }
  return null;
};

const getHeaders = () => {
  const token = getAuthToken();
  const headers: { [key: string]: string } = {
    'Content-Type': 'application/json',
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
};

export const api = {
  get: async (endpoint: string) => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'GET',
      headers: getHeaders(),
    });
    return response.json();
  },

  post: async (endpoint: string, data: any) => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(data),
    });
    return response.json();
  },

  put: async (endpoint: string, data: any) => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(data),
    });
    return response.json();
  },

  delete: async (endpoint: string) => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'DELETE',
      headers: getHeaders(),
    });
    // DELETE might not return a body, so we handle that case
    if (response.status === 204) {
      return { success: true };
    }
    return response.json();
  },

  // Extended API methods
  getTasks: async (completed?: boolean | null) => {
    let url = '/tasks';
    if (completed !== undefined && completed !== null) {
      url += `?completed=${completed}`;
    }
    return api.get(url);
  },

  createTask: async (data: { title: string; description?: string }) => {
    return api.post('/tasks', data);
  },

  updateTask: async (id: number, data: { title?: string; description?: string; completed?: boolean }) => {
    return api.put(`/tasks/${id}`, data);
  },

  deleteTask: async (id: number) => {
    return api.delete(`/tasks/${id}`);
  },

  toggleTaskCompletion: async (id: number) => {
    return api.patch(`/tasks/${id}/complete`, {});
  },

  patch: async (endpoint: string, data: any) => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'PATCH',
      headers: getHeaders(),
      body: JSON.stringify(data),
    });
    return response.json();
  },
};