'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface AuthState {
  isAuthenticated: boolean;
  isLoading: boolean;
  token: string | null;
}

export function useAuth() {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    isLoading: true,
    token: null,
  });
  const router = useRouter();

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = () => {
    if (typeof window === 'undefined') {
      setAuthState({ isAuthenticated: false, isLoading: false, token: null });
      return;
    }

    const token = localStorage.getItem('token');
    const isAuthenticated = !!token;

    // Also sync token to cookie for middleware
    if (token) {
      document.cookie = `token=${token}; path=/; max-age=86400; SameSite=Lax`;
    }

    setAuthState({
      isAuthenticated,
      isLoading: false,
      token,
    });
  };

  const login = (token: string) => {
    localStorage.setItem('token', token);
    document.cookie = `token=${token}; path=/; max-age=86400; SameSite=Lax`;
    setAuthState({ isAuthenticated: true, isLoading: false, token });
  };

  const logout = () => {
    localStorage.removeItem('token');
    document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
    setAuthState({ isAuthenticated: false, isLoading: false, token: null });
    router.push('/login');
  };

  return {
    ...authState,
    checkAuth,
    login,
    logout,
  };
}

// Helper to check auth without hook (for one-time checks)
export function isAuthenticated(): boolean {
  if (typeof window === 'undefined') return false;
  return !!localStorage.getItem('token');
}

// Helper to get token
export function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('token');
}
