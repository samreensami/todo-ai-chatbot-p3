"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      // IMPORTANT: OAuth2 requires application/x-www-form-urlencoded
      const formData = new URLSearchParams();
      formData.append("username", email);  // OAuth2 uses "username" field
      formData.append("password", password);

      console.log("📤 Logging in to http://localhost:8000/auth/login");

      const response = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData.toString(),
      });

      const data = await response.json();

      if (response.ok && data.access_token) {
        console.log("✅ Login successful!");
        // Token is stored in httpOnly cookie automatically
        router.push("/dashboard");
      } else {
        console.error("❌ Login failed:", data);
        setError(data.detail || "Invalid email or password");
      }
    } catch (err: any) {
      console.error("❌ Network error:", err);
      setError("Network Error: Backend is not responding. Check that backend is running on http://localhost:8000");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-24 bg-emerald-950">
      <div className="w-full max-w-md space-y-8 bg-emerald-900 p-8 rounded-3xl shadow-lg border border-emerald-800">
        <div>
          <h2 className="text-center text-4xl font-bold tracking-tight text-white">
            TaskSphere Login
          </h2>
          <p className="mt-2 text-center text-sm text-emerald-300">
            Sign in to your account
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleLogin}>
          {/* Error Message */}
          {error && (
            <div className="text-red-400 text-sm text-center bg-red-900/30 p-3 rounded border border-red-700/50">
              ⚠️ {error}
            </div>
          )}

          <div className="space-y-4">
            {/* Email Input */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-emerald-200 mb-1">
                Email Address
              </label>
              <input
                id="email"
                type="email"
                required
                autoComplete="email"
                disabled={loading}
                className="appearance-none block w-full px-4 py-3 border border-emerald-700/50 placeholder-emerald-500 text-emerald-100 bg-emerald-800/50 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed sm:text-sm"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            {/* Password Input */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-emerald-200 mb-1">
                Password
              </label>
              <input
                id="password"
                type="password"
                required
                autoComplete="current-password"
                disabled={loading}
                className="appearance-none block w-full px-4 py-3 border border-emerald-700/50 placeholder-emerald-500 text-emerald-100 bg-emerald-800/50 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed sm:text-sm"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 px-4 text-sm font-bold rounded-2xl text-white bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>

        {/* Register Link */}
        <div className="text-center text-sm text-emerald-300/80">
          Don't have an account?{" "}
          <Link href="/register" className="font-bold hover:underline text-emerald-200">
            Register here
          </Link>
        </div>
      </div>
    </div>
  );
}
