"use client";

import Markdown from "react-markdown";

type Props = {
  role: "user" | "assistant";
  content: string;
  sources?: string[];
  tokens?: number;
  durationMs?: number;
};

export default function MessageBubble({
  role,
  content,
  sources,
  tokens,
  durationMs,
}: Props) {
  const isUser = role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
      <div
        className={`relative max-w-[85%] ${
          isUser
            ? "bg-gradient-to-br from-blue-500 to-indigo-600 text-white rounded-2xl rounded-br-md px-5 py-3 shadow-md"
            : "bg-white text-slate-800 rounded-2xl rounded-bl-md px-5 py-4 shadow-sm border border-slate-100"
        }`}
      >
        {isUser ? (
          <p className="text-sm leading-relaxed">{content}</p>
        ) : (
          <>
            <div className="prose prose-sm prose-slate max-w-none prose-p:my-2 prose-ul:my-2 prose-ol:my-2 prose-li:my-0.5 prose-headings:mt-3 prose-headings:mb-1 prose-strong:text-slate-900">
              <Markdown>{content}</Markdown>
            </div>

            {(sources?.length || tokens || durationMs) ? (
              <div className="mt-3 pt-3 border-t border-slate-100 flex flex-wrap gap-x-4 gap-y-1.5 text-xs text-slate-400">
                {sources && sources.length > 0 && (
                  <div className="flex items-center gap-1.5">
                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <span>{sources.join(", ")}</span>
                  </div>
                )}
                {tokens ? (
                  <div className="flex items-center gap-1.5">
                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A2 2 0 013 12V7a4 4 0 014-4z" />
                    </svg>
                    <span>{tokens} tokens</span>
                  </div>
                ) : null}
                {durationMs ? (
                  <div className="flex items-center gap-1.5">
                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span>{(durationMs / 1000).toFixed(1)}s</span>
                  </div>
                ) : null}
              </div>
            ) : null}
          </>
        )}
      </div>
    </div>
  );
}
