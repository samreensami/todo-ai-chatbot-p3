import Link from "next/link";

export default function HomePage() {
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
          <Link href="/chat" className="px-10 py-4 text-lg bg-emerald-500 text-white rounded-2xl font-bold shadow-md hover:scale-105 transition-transform">
            Start Chatting
          </Link>
        </div>
      </div>
    </div>
  );
}
