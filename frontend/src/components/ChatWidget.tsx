"use client";

import { useState, useRef, useEffect, FormEvent } from "react";
import MessageBubble from "./MessageBubble";
import TypingIndicator from "./TypingIndicator";

type Message = {
  role: "user" | "assistant";
  content: string;
  sources?: string[];
  tokens?: number;
  durationMs?: number;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";

export default function ChatWidget() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Bonjour ! Je suis l'assistant de **Narymane Chabane**. Posez-moi vos questions sur son parcours professionnel, sa formation, ses projets et ses compétences.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const text = input.trim();
    if (!text || loading) return;

    const userMsg: Message = { role: "user", content: text };
    const updated = [...messages, userMsg];
    setMessages(updated);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: updated }),
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const data = await res.json();
      setMessages([
        ...updated,
        {
          role: "assistant",
          content: data.reply,
          sources: data.sources,
          tokens: data.total_tokens,
          durationMs: data.duration_ms,
        },
      ]);
    } catch {
      setMessages([
        ...updated,
        {
          role: "assistant",
          content: "Désolé, une erreur est survenue. Réessayez dans un instant.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col h-full max-w-4xl w-full mx-auto">
      {/* Header */}
      <div className="px-6 pt-8 pb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white font-bold text-lg shadow-md">
            N
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-800">Ask Narymane</h1>
            <p className="text-sm text-slate-500">
              Ingénieure Systèmes Embarqués Linux &amp; IA/ML
            </p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 pb-4 scroll-smooth">
        <div className="space-y-1">
          {messages.map((msg, i) => (
            <MessageBubble
              key={i}
              role={msg.role}
              content={msg.content}
              sources={msg.sources}
              tokens={msg.tokens}
              durationMs={msg.durationMs}
            />
          ))}
          {loading && <TypingIndicator />}
          <div ref={bottomRef} />
        </div>
      </div>

      {/* Input */}
      <div className="px-6 pb-6 pt-2">
        <form
          onSubmit={handleSubmit}
          className="flex gap-3 bg-white rounded-2xl shadow-lg border border-slate-200 p-2 focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-transparent transition-all"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Posez votre question sur le parcours de Narymane..."
            className="flex-1 px-4 py-3 text-sm text-slate-800 bg-transparent focus:outline-none placeholder:text-slate-400"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white px-6 py-3 rounded-xl text-sm font-medium hover:from-blue-600 hover:to-indigo-700 disabled:opacity-40 disabled:cursor-not-allowed transition-all shadow-sm"
          >
            Envoyer
          </button>
        </form>
        <p className="text-center text-xs text-slate-400 mt-3">
          Propulsé par Ollama &amp; ChromaDB — Les réponses sont basées sur le profil de Narymane
        </p>
      </div>
    </div>
  );
}
