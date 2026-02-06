'use client';

import React, { useEffect, useRef, useState } from 'react';

const API_BASE_URL = 'http://localhost:8000';

interface Message {
  role: 'user' | 'assistant' | 'tool';
  content: string;
  toolName?: string;
  toolResult?: any;
}

interface ChatApiResponse {
  success: boolean;
  conversation_id?: string;
  response?: string;
  tool_calls?: Array<{
    tool?: string;
    arguments?: any;
    result?: any;
  }>;
  error?: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [userId] = useState('demo-user');

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Auto scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Send message with simple JSON response
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setIsLoading(true);

    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage,
          conversation_id: conversationId,
          user_id: userId,
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }

      const data: ChatApiResponse = await response.json();

      // Update conversation ID
      if (data.conversation_id) {
        setConversationId(data.conversation_id);
      }

      // Add tool call messages
      if (data.tool_calls && data.tool_calls.length > 0) {
        for (const tc of data.tool_calls) {
          if (tc.arguments) {
            // Tool call
            setMessages(prev => [...prev, {
              role: 'tool',
              content: `Calling ${tc.tool}(${JSON.stringify(tc.arguments)})`,
              toolName: tc.tool,
            }]);
          } else if (tc.result) {
            // Tool result
            setMessages(prev => [...prev, {
              role: 'tool',
              content: `${tc.tool} result:\n${JSON.stringify(tc.result, null, 2)}`,
              toolName: tc.tool,
              toolResult: tc.result,
            }]);
          }
        }
      }

      // Handle response
      if (data.success && data.response) {
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: data.response,
        }]);
      } else if (data.error) {
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: `Error: ${data.error}`,
        }]);
      } else if (data.success && !data.response && data.tool_calls?.length) {
        // Tool calls executed but no final response (quota exhausted mid-request)
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: 'Tool executed successfully. (AI response unavailable due to quota)',
        }]);
      }

    } catch (err: any) {
      console.error('Chat error:', err);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Connection error: ${err.message}. Make sure the backend is running at ${API_BASE_URL}`,
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Start new conversation
  const handleNewChat = () => {
    setMessages([]);
    setConversationId(null);
  };

  // Quick action buttons
  const quickActions = [
    { label: 'List tasks', prompt: 'Show me all my tasks' },
    { label: 'Add task', prompt: 'Add a task: ' },
    { label: 'Complete task', prompt: 'Mark task #1 as complete' },
    { label: 'Delete task', prompt: 'Delete task #1' },
    { label: 'High priority', prompt: 'Show high priority tasks' },
  ];

  return (
    <div className="flex flex-col h-[calc(100vh-120px)] bg-emerald-900/50 rounded-2xl shadow-lg">
      {/* Header */}
      <div className="p-4 border-b border-emerald-700 flex justify-between items-center">
        <h1 className="text-lg font-semibold text-emerald-100">Todo AI Assistant (Gemini)</h1>
        <button
          onClick={handleNewChat}
          className="px-4 py-2 bg-emerald-700 rounded-lg hover:bg-emerald-600 text-sm"
        >
          New Chat
        </button>
      </div>

      {/* Quick Actions */}
      <div className="p-3 border-b border-emerald-700 flex flex-wrap gap-2">
        {quickActions.map((action, i) => (
          <button
            key={i}
            onClick={() => setInput(action.prompt)}
            className="px-3 py-1 text-xs bg-emerald-700/50 hover:bg-emerald-600 rounded-full transition-colors"
          >
            {action.label}
          </button>
        ))}
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-emerald-300 py-8">
            <p className="text-lg mb-2">Welcome to Todo AI Assistant!</p>
            <p className="text-sm opacity-75">Ask me to manage your tasks. Try &quot;Show me all my tasks&quot; or &quot;Add a task: Buy groceries&quot;</p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-2xl px-4 py-3 rounded-xl text-sm ${
                msg.role === 'user'
                  ? 'bg-emerald-600 text-white'
                  : msg.role === 'tool'
                  ? 'bg-yellow-800/50 text-yellow-100 font-mono text-xs'
                  : 'bg-emerald-800 text-emerald-100'
              }`}
            >
              {msg.role === 'tool' && (
                <div className="text-yellow-400 text-xs mb-1 font-semibold">Tool Result</div>
              )}
              <pre className="whitespace-pre-wrap font-sans">{msg.content}</pre>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-emerald-800 text-emerald-100 px-4 py-3 rounded-xl flex items-center gap-2">
              <div className="animate-pulse">Thinking...</div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="border-t border-emerald-700 p-4 flex gap-3">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me to manage your tasks..."
          className="flex-1 p-3 rounded-lg bg-emerald-800/80 text-white placeholder-emerald-400 focus:outline-none focus:ring-2 focus:ring-emerald-500"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="px-6 py-3 bg-emerald-600 rounded-lg hover:bg-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
        >
          Send
        </button>
      </form>
    </div>
  );
}
