"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { api } from "../../lib/api-service";

export default function RegisterPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      // Direct registration - NO CSRF needed
      const response = await api.post("/auth/register", {
        name: name.trim(),
        email: email.trim(),
        password: password,
      });

      console.log("✅ Registration successful:", response.data);
      setSuccess(true);

      // Redirect to login after 2 seconds
      setTimeout(() => {
        router.push("/login");
      }, 2000);
    } catch (err: any) {
      console.error("❌ Registration failed:", err);

      // Extract error message
      let errorMessage = "Registration failed";

      if (err.response?.data?.detail) {
        // FastAPI validation error
        if (Array.isArray(err.response.data.detail)) {
          errorMessage = err.response.data.detail.map((e: any) => e.msg).join(", ");
        } else {
          errorMessage = err.response.data.detail;
        }
      } else if (err.message) {
        errorMessage = err.message;
      }

      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-24 bg-emerald-950">
      <div className="w-full max-w-md space-y-8 bg-emerald-900 p-8 rounded-3xl shadow-lg border border-emerald-800">
        <div>
          <h2 className="text-center text-4xl font-bold tracking-tight text-white">
            Create Account
          </h2>
          <p className="mt-2 text-center text-sm text-emerald-300">
            Join TaskSphere today
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleRegister}>
          {/* Error Message */}
          {error && (
            <div className="text-red-400 text-sm text-center bg-red-900/30 p-3 rounded border border-red-700/50">
              ⚠️ {error}
            </div>
          )}

          {/* Success Message */}
          {success && (
            <div className="text-emerald-300 text-sm text-center bg-emerald-900/30 p-3 rounded border border-emerald-700/50">
              ✓ Registration successful! Redirecting to login...
            </div>
          )}

          <div className="space-y-4">
            {/* Name Input */}
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-emerald-200 mb-1">
                Full Name
              </label>
              <input
                id="name"
                type="text"
                required
                autoComplete="name"
                disabled={loading || success}
                className="appearance-none relative block w-full px-4 py-3 border border-emerald-700/50 placeholder-emerald-500 text-emerald-100 bg-emerald-800/50 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed sm:text-sm"
                placeholder="Enter your name"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>

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
                disabled={loading || success}
                className="appearance-none relative block w-full px-4 py-3 border border-emerald-700/50 placeholder-emerald-500 text-emerald-100 bg-emerald-800/50 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed sm:text-sm"
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
                autoComplete="new-password"
                disabled={loading || success}
                className="appearance-none relative block w-full px-4 py-3 border border-emerald-700/50 placeholder-emerald-500 text-emerald-100 bg-emerald-800/50 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed sm:text-sm"
                placeholder="Create a password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <p className="mt-2 text-xs text-emerald-400/70">
                Must be 8+ characters with uppercase, lowercase, number, and special character
              </p>
            </div>
          </div>

          {/* Submit Button */}
          <div>
            <button
              type="submit"
              disabled={loading || success}
              className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-bold rounded-2xl text-white bg-emerald-500 hover:bg-emerald-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? "Creating Account..." : "Create Account"}
            </button>
          </div>
        </form>

        {/* Login Link */}
        <div className="text-center text-sm text-emerald-300/80">
          Already have an account?{" "}
          <Link href="/login" className="font-bold hover:underline text-emerald-200">
            Log in here
          </Link>
        </div>
      </div>
    </div>
  );
}
