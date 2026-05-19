import { useState } from "react";
import type { FormEvent } from "react";
import { Search } from "lucide-react";

import { analyzePosts } from "../api/client";
import { PostTable } from "../components/PostTable";
import type { AnalyzeRequest, AnalyzeResponse, SortMode, SourceMode } from "../types";

interface AnalyzePageProps {
  onAnalyzed: () => void;
}

const initialForm: AnalyzeRequest = {
  subreddit: "technology",
  keyword: "AI",
  limit: 15,
  sort: "hot",
  source: "auto",
};

export function AnalyzePage({ onAnalyzed }: AnalyzePageProps) {
  const [form, setForm] = useState<AnalyzeRequest>(initialForm);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function updateField<Key extends keyof AnalyzeRequest>(key: Key, value: AnalyzeRequest[Key]) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await analyzePosts(form);
      setResult(response);
      onAnalyzed();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Could not analyze posts.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page-stack">
      <section className="panel">
        <div className="panel__header">
          <h2>Analyze Reddit Posts</h2>
        </div>

        <form className="analysis-form" onSubmit={handleSubmit}>
          <label>
            Subreddit
            <input
              value={form.subreddit}
              minLength={2}
              maxLength={50}
              pattern="[A-Za-z0-9_]+"
              required
              onChange={(event) => updateField("subreddit", event.target.value)}
            />
          </label>

          <label>
            Keyword
            <input
              value={form.keyword}
              maxLength={80}
              onChange={(event) => updateField("keyword", event.target.value)}
            />
          </label>

          <label>
            Limit
            <input
              type="number"
              min={5}
              max={100}
              value={form.limit}
              onChange={(event) => updateField("limit", Number(event.target.value))}
            />
          </label>

          <label>
            Sort
            <select value={form.sort} onChange={(event) => updateField("sort", event.target.value as SortMode)}>
              <option value="hot">Hot</option>
              <option value="new">New</option>
              <option value="top">Top</option>
            </select>
          </label>

          <label>
            Source
            <select
              value={form.source}
              onChange={(event) => updateField("source", event.target.value as SourceMode)}
            >
              <option value="auto">Auto</option>
              <option value="reddit">Reddit API</option>
              <option value="demo">Demo data</option>
            </select>
          </label>

          <button type="submit" className="button button--primary" disabled={loading}>
            <Search aria-hidden="true" />
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </form>

        {error ? <div className="form-error">{error}</div> : null}
      </section>

      {result ? (
        <section className="panel">
          <div className="panel__header">
            <h2>Latest Result</h2>
            <span className="source-pill">{result.source_used}</span>
          </div>
          <p className="result-message">{result.message}</p>
          <PostTable posts={result.posts} />
        </section>
      ) : null}
    </div>
  );
}
