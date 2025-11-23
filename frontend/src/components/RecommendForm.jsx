import React, { useState, useRef } from "react";

export default function RecommendForm() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);

  const recognitionRef = useRef(null);
  const silenceTimerRef = useRef(null);

  // ---- SPEECH RECOGNITION SETUP ----
  const startRecording = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech recognition not supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";
    recognitionRef.current = recognition;

    recognition.onstart = () => {
      setIsRecording(true);
      resetSilenceTimer();
    };

    recognition.onresult = (event) => {
      let transcript = "";

      for (let i = 0; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript + " ";
      }

      setQuery(transcript);
      resetSilenceTimer();
    };

    recognition.onerror = () => stopRecording();
    recognition.onend = () => setIsRecording(false);

    recognition.start();
  };

  const stopRecording = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      recognitionRef.current = null;
    }
    setIsRecording(false);

    if (silenceTimerRef.current) clearTimeout(silenceTimerRef.current);
  };

  const resetSilenceTimer = () => {
    if (silenceTimerRef.current) clearTimeout(silenceTimerRef.current);

    // Auto-stop after 3 seconds of silence
    silenceTimerRef.current = setTimeout(() => {
      stopRecording();
    }, 3000);
  };

  const toggleRecording = () => {
    if (isRecording) stopRecording();
    else startRecording();
  };

  // ---- BACKEND CALL ----
  async function onSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setResults([]);
    try {
      const res = await fetch("http://localhost:8000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, n_results: 6 }),
      });

      const j = await res.json();
      if (res.ok) {
        setResults(j.recommendations || []);
      } else {
        alert("Error: " + j.detail || JSON.stringify(j));
      }
    } catch (err) {
      alert("Backend not running or CORS issue: " + err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-gray-50 to-blue-100 p-6 flex flex-col items-center">
      <main className="w-full max-w-7xl">
        <form
          onSubmit={onSubmit}
          className="w-full glass p-6 rounded-2xl shadow-xl border border-white/30 backdrop-blur-lg"
        >
          <label className="block text-gray-700 font-semibold text-xl mb-2">
            Assessment Recommendation Assistant
          </label>

          <div className="flex flex-col md:flex-row gap-4 items-start">
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Paste a job description or speak to describe the role..."
              rows={3}
              className="w-full md:w-3/4 border border-gray-300 rounded-xl p-4 text-lg shadow focus:ring-2 focus:ring-blue-500 outline-none transition"
            />

            {/* MIC BUTTON + Submit */}
            <div className="flex flex-col gap-3 w-full md:w-1/4">
              <button
                type="button"
                onClick={toggleRecording}
                className={`py-3 rounded-xl text-white font-semibold shadow-md transition ${isRecording
                    ? "bg-red-600 animate-pulse"
                    : "bg-gray-700 hover:bg-gray-500"
                  }`}
              >
                {isRecording ? "🎤 Stop Recording" : "🎤 Tap & Ask"}
              </button>

              <button
                className="w-full py-4 bg-blue-600 hover:bg-blue-700 text-white text-lg font-semibold rounded-xl shadow-md transition disabled:opacity-50"
                disabled={loading}
              >
                {loading ? "Processing..." : "Recommend"}
              </button>
            </div>
          </div>
        </form>

        {/* RESULTS */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {loading && (
            <p className="text-blue-600 font-semibold text-lg">
              Analyzing job description...
            </p>
          )}

          {!loading &&
            results.length > 0 &&
            results.map((r, i) => (
              <div
                key={i}
                className="glass p-6 rounded-2xl shadow-lg border border-white/20 backdrop-blur-lg hover:scale-[1.02] transition"
              >
                <h3 className="text-xl font-bold">{r.assessment_name}</h3>
                <p className="text-gray-600 mt-2">
                  Match Score:{" "}
                  <span className="font-semibold text-blue-700">
                    {(r.score || 0).toFixed(4)}
                  </span>
                </p>
                <a
                  href={r.assessment_url}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-block mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition"
                >
                  Open Assessment
                </a>
              </div>
            ))}
        </div>
      </main>
    </div>
  );
}
