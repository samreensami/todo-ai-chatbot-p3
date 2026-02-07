'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function HomePage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check authentication status
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
      // Sync token to cookie
      document.cookie = `token=${token}; path=/; max-age=86400; SameSite=Lax`;
    } else {
      // Redirect to login if not authenticated
      router.push('/login');
      return;
    }
    setIsLoading(false);
  }, [router]);

  // Show loading state while checking auth
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-emerald-950">
        <div className="text-emerald-300 text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-emerald-950 font-sans p-5">
      <div className="bg-emerald-900 border border-emerald-800 rounded-3xl p-10 text-center max-w-2xl">
        <h1 className="text-6xl mb-5 font-bold text-white">
          Todo AI Assistant
        </h1>
        <p className="text-2xl mb-4 text-emerald-300/80">
          Powered by Gemini AI
        </p>
        <p className="text-lg mb-10 text-emerald-400/70">
          Manage your tasks with natural language. Just tell the AI what you need!
        </p>
        <div className="flex gap-5 justify-center flex-wrap">
          {isAuthenticated ? (
            <Link
              href="/chat"
              className="px-10 py-4 text-lg bg-emerald-500 text-white rounded-2xl font-bold shadow-md hover:scale-105 transition-transform"
            >
              Start Chatting
            </Link>
          ) : (
            <div className="flex flex-col items-center gap-4">
              <button
                disabled
                className="px-10 py-4 text-lg bg-emerald-700/50 text-emerald-400/50 rounded-2xl font-bold shadow-md cursor-not-allowed"
              >
                Start Chatting
              </button>
              <p className="text-emerald-400/70 text-sm">
                Please <Link href="/login" className="text-emerald-300 underline hover:text-emerald-200">login</Link> to start chatting
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
