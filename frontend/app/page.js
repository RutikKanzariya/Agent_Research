"use client";

import { useCallback, useRef, useState } from "react";

const BACKEND_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

const STAGE_LABELS = [
  "Step 1 - Search agent scanning the web ...",
  "Step 2 - Reader agent scraping top resources ...",
  "Step 3 - Writer drafting the report ...",
  "Step 4 - Critic reviewing the report ...",
];

export default function Home() {
  const [topic, setTopic] = useState("");
  const [status, setStatus] = useState("idle"); // idle | starting | running | done | error
  const [stage, setStage] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const pollRef = useRef(null);

  const stopPolling = useCallback(() => {
    if (pollRef.current) {
      clearInterval(pollRef.current);
      pollRef.current = null;
    }
  }, []);

  const startStageTimer = useCallback(() => {
    setStage(0);
    pollRef.current = setInterval(() => {
      setStage((s) => Math.min(s + 1, STAGE_LABELS.length - 1));
    }, 8000);
  }, []);

  const pollJob = useCallback(
    async (jobId) => {
      const endpoint = `${BACKEND_URL}/research/${jobId}`;
      const check = async () => {
        let res;
        try {
          res = await fetch(endpoint);
        } catch {
          return;
        }
        if (!res.ok) return;
        const data = await res.json();
        if (data.status === "done") {
          stopPolling();
          setResult(data.result);
          setStatus("done");
        } else if (data.status === "error") {
          stopPolling();
          setError(data.error || "Research failed.");
          setStatus("error");
        }
      };
      await check();
      pollRef.current = setInterval(check, 3000);
    },
    [stopPolling]
  );

  const handleSubmit = async (e) => {
    e.preventDefault();
    const trimmed = topic.trim();
    if (!trimmed) return;

    setError("");
    setResult(null);
    setStatus("starting");
    startStageTimer();

    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 90000);
      const res = await fetch(`${BACKEND_URL}/research`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: trimmed }),
        signal: controller.signal,
      });
      clearTimeout(timeout);

      if (!res.ok) {
        throw new Error(`Backend responded with ${res.status}`);
      }
      const data = await res.json();
      setStatus("running");
      pollJob(data.job_id);
    } catch (err) {
      stopPolling();
      setStatus("error");
      if (err.name === "AbortError") {
        setError(
          "Backend took too long to respond. It may still be waking up on Render's free tier - try again in a moment."
        );
      } else {
        setError(
          `Could not reach the backend at ${BACKEND_URL}. Check the Render URL in NEXT_PUBLIC_BACKEND_URL.`
        );
      }
    }
  };

  const scoreMatch = result?.feedback?.match(/Score:\s*(\d+)\s*\/\s*10/i);

  return (
    <main className="container">
      <header className="header">
        <span className="badge">AI Research</span>
        <h1>Agent Research</h1>
        <p>
          Multi-agent pipeline: web search, scraping, report writing and critic
          review.
        </p>
      </header>

      <form onSubmit={handleSubmit} className="form">
        <input
          type="text"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="Enter a research topic, e.g. Artificial Intelligence in Healthcare"
          disabled={status === "starting" || status === "running"}
        />
        <button
          type="submit"
          disabled={!topic.trim() || status === "starting" || status === "running"}
        >
          {status === "starting" || status === "running"
            ? "Researching..."
            : "Research"}
        </button>
      </form>

      {status === "starting" && (
        <p className="wake-note">
          Contacting backend ... (first call may take up to a minute while a
          free Render instance wakes up)
        </p>
      )}

      {(status === "running" || status === "starting") && (
        <div className="status-card">
          <div className="spinner" />
          <p>{STAGE_LABELS[stage]}</p>
        </div>
      )}

      {status === "error" && (
        <div className="error-card">
          <strong>Something went wrong</strong>
          <p>{error}</p>
          <button className="link-button" onClick={() => window.location.reload()}>
            Reload
          </button>
        </div>
      )}

      {status === "done" && result && (
        <section className="results">
          <div className="report-card">
            <h2>Research Report</h2>
            <pre>{result.report}</pre>
          </div>

          <div className="feedback-card">
            <h2>Critic Feedback {scoreMatch && <span className="score">{scoreMatch[1]}/10</span>}</h2>
            <pre>{result.feedback}</pre>
          </div>

          <details className="raw-card">
            <summary>Show raw search results</summary>
            <pre>{result.search_result}</pre>
          </details>

          <details className="raw-card">
            <summary>Show scraped content</summary>
            <pre>{result.scrapped_result}</pre>
          </details>
        </section>
      )}
    </main>
  );
}