'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { api } from './api';
import type { User } from '@/types';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Initialize auth state from localStorage after component mounts
    const initializeAuth = async () => {
      const token = localStorage.getItem('token');
      const userData = localStorage.getItem('user');

      if (token && userData) {
        try {
          // Validate the token by calling the /me endpoint
          const userResponse = await api.get('/auth/me');
          setUser(userResponse);
        } catch (error) {
          // If token is invalid, clear it
          localStorage.removeItem('token');
          localStorage.removeItem('user');
        }
      }
      setIsLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (email: string, password: string) => {
    const response = await api.post('/auth/login', { email, password });
    if (response?.access_token) {
      localStorage.setItem('token', response.access_token);
      // Assuming the user object is returned at the root of the response
      const userResponse = await api.get('/auth/me');
      localStorage.setItem('user', JSON.stringify(userResponse));
      setUser(userResponse);
    } else {
      throw new Error(response.detail || 'Login failed');
    }
  };

  const register = async (email: string, password: string) => {
    const response = await api.post('/auth/register', { email, password });
     if (response?.access_token) {
      localStorage.setItem('token', response.access_token);
      // Assuming the user object is returned at the root of the response
      const userResponse = await api.get('/auth/me');
      localStorage.setItem('user', JSON.stringify(userResponse));
      setUser(userResponse);
    } else {
      throw new Error(response.detail || 'Registration failed');
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
