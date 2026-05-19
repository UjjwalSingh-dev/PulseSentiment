import { useEffect, useState } from "react";
import { Filter } from "lucide-react";

import { getPosts } from "../api/client";
import { PostTable } from "../components/PostTable";
import type { PostRead, SentimentLabel } from "../types";

export function HistoryPage() {
  const [subreddit, setSubreddit] = useState("");
  const [sentiment, setSentiment] = useState<SentimentLabel | "">("");
  const [posts, setPosts] = useState<PostRead[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function loadPosts() {
    setLoading(true);
    setError(null);
    try {
      const response = await getPosts({
        subreddit: subreddit.trim() || undefined,
        sentiment,
        limit: 100,
      });
      setPosts(response);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Could not load posts.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadPosts();
  }, []);

  return (
    <div className="page-stack">
      <section className="panel">
        <div className="panel__header">
          <h2>History</h2>
        </div>

        <div className="history-filters">
          <label>
            Subreddit
            <input value={subreddit} onChange={(event) => setSubreddit(event.target.value)} />
          </label>

          <label>
            Sentiment
            <select value={sentiment} onChange={(event) => setSentiment(event.target.value as SentimentLabel | "")}>
              <option value="">All</option>
              <option value="positive">Positive</option>
              <option value="neutral">Neutral</option>
              <option value="negative">Negative</option>
            </select>
          </label>

          <button type="button" className="button button--primary" onClick={loadPosts}>
            <Filter aria-hidden="true" />
            Apply
          </button>
        </div>
      </section>

      <section className="panel">
        <div className="panel__header">
          <h2>Analyzed Posts</h2>
        </div>
        {loading ? <div className="loading-block">Loading history...</div> : null}
        {error ? <div className="form-error">{error}</div> : null}
        {!loading && !error ? <PostTable posts={posts} /> : null}
      </section>
    </div>
  );
}
