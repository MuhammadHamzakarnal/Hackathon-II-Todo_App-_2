let API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://hamza1222-todo.hf.space';

// Ensure API_BASE_URL doesn't end with '/api' to prevent double prefixes
if (API_BASE_URL.endsWith('/api')) {
  API_BASE_URL = API_BASE_URL.slice(0, -'/api'.length);
  // Ensure it doesn't end with '/' so we can properly append endpoints
  if (API_BASE_URL.endsWith('/')) {
    API_BASE_URL = API_BASE_URL.slice(0, -1);
  }
}

const API_URL = API_BASE_URL;

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

// Helper to handle API responses
const handleResponse = async (response: Response) => {
  if (!response.ok) {
    // Try to parse error as JSON
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      const errorData = await response.json();
      throw new Error(errorData.detail || errorData.message || `HTTP ${response.status} error`);
    }
    // Otherwise, get text
    const errorText = await response.text();
    throw new Error(errorText.substring(0, 200) || `HTTP ${response.status} error`);
  }
  return response.json();
};

export const api = {
  get: async (endpoint: string) => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'GET',
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  post: async (endpoint: string, data: any) => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  put: async (endpoint: string, data: any) => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(data),
    });
    return handleResponse(response);
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
    return handleResponse(response);
  },

  // Extended API methods
  getTasks: async (completed?: boolean | null) => {
    let url = '/api/tasks';
    if (completed !== undefined && completed !== null) {
      url += `?completed=${completed}`;
    }
    return api.get(url);
  },

  createTask: async (data: { title: string; description?: string }) => {
    return api.post('/api/tasks', data);
  },

  updateTask: async (id: number, data: { title?: string; description?: string; completed?: boolean }) => {
    return api.put(`/api/tasks/${id}`, data);
  },

  deleteTask: async (id: number) => {
    return api.delete(`/api/tasks/${id}`);
  },

  toggleTaskCompletion: async (id: number) => {
    return api.patch(`/api/tasks/${id}/complete`, {});
  },

  patch: async (endpoint: string, data: any) => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'PATCH',
      headers: getHeaders(),
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },
};