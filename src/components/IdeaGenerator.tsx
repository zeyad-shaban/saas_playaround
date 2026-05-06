"use client";

import { useEffect, useState } from "react";

export default function IdeaGenerator() {
    const [idea, setIdea] = useState<string>("")
    const [loading, setLoading] = useState<boolean>(false)
    const [error, setError] = useState<string | null>(null)

    const fetchIdea = async () => {
        setIdea("");
        setLoading(true);
        setError(null);

        try {
            const res = await fetch("/api/python/idea");
            if (!res.ok) throw new Error(`HTTP ${res.status}`);

            const reader = res.body?.getReader();
            if (!reader) throw new Error("Stream reader not available");

            const decoder = new TextDecoder();
            let fullText = "";
            while (true) {
                const { value, done } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                fullText += chunk;

                setIdea((idea) => idea + chunk);
            }

            // Check if response is an error message
            if (fullText.startsWith("ERROR:")) {
                setError(fullText.replace("ERROR: ", ""));
                setIdea("");
            }

        } catch (err) {
            const errorMsg = err instanceof Error ? err.message : "Unknown error";
            console.error("Fetch error:", errorMsg);
            setError(errorMsg);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-8">
            <div className="w-full max-w-2xl">
                <div className="bg-slate-800/50 backdrop-blur-md border border-slate-700/50 rounded-2xl p-8 shadow-2xl">
                    <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent mb-8 text-center">
                        💡 Idea Generator LOL
                    </h1>

                    <div className="relative min-h-40 bg-slate-900/50 rounded-xl p-6 border border-slate-700/30">
                        {loading && !idea ? (
                            <div className="flex flex-col items-center justify-center h-40 gap-4">
                                <div className="flex gap-2">
                                    <div className="w-3 h-3 bg-blue-400 rounded-full animate-pulse"></div>
                                    <div className="w-3 h-3 bg-blue-400 rounded-full animate-pulse" style={{ animationDelay: "0.2s" }}></div>
                                    <div className="w-3 h-3 bg-blue-400 rounded-full animate-pulse" style={{ animationDelay: "0.4s" }}></div>
                                </div>
                                <p className="text-slate-300 animate-pulse font-medium">Generating your amazing idea...</p>
                            </div>
                        ) : error ? (
                            <div className="text-red-400 font-semibold text-center">
                                ❌ Error: {error}
                            </div>
                        ) : idea ? (
                            <div className="prose prose-invert max-w-none">
                                <p className="text-slate-100 leading-relaxed text-lg whitespace-pre-wrap">{idea}</p>
                            </div>
                        ) : (
                            <div className="flex items-center justify-center h-40 text-slate-400">
                                Click the button to generate an idea
                            </div>
                        )}
                    </div>

                    <button
                        onClick={fetchIdea}
                        disabled={loading}
                        className={`w-full mt-8 py-3 px-6 rounded-xl font-bold text-lg transition-all duration-300 ${loading
                                ? "bg-slate-700 text-slate-400 cursor-not-allowed opacity-50"
                                : "bg-gradient-to-r from-blue-500 to-cyan-500 text-white hover:shadow-lg hover:shadow-blue-500/50 hover:scale-105"
                            }`}
                    >
                        {loading ? "Generating..." : "Generate New Idea"}
                    </button>
                </div>
            </div>
        </div>
    )
}