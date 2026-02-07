'use client';

import React from 'react';

export default function LogoutButton() {
  const handleLogout = () => {
    if (typeof window !== 'undefined') {
      // Clear token from localStorage and cookie
      localStorage.removeItem('token');
      document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
      window.location.href = '/login';
    }
  };

  return (
    <button
      onClick={handleLogout}
      className="w-full text-left px-4 py-2 text-sm text-red-400 hover:text-red-300 transition"
    >
      🚪 Logout
    </button>
  );
}