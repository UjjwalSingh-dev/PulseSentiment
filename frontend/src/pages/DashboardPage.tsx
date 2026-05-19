import { Activity, Frown, Meh, MessageSquareText, Smile } from "lucide-react";

import { PostTable } from "../components/PostTable";
import { SentimentChart } from "../components/SentimentChart";
import { StatCard } from "../components/StatCard";
import type { DashboardResponse } from "../types";

interface DashboardPageProps {
  data: DashboardResponse | null;
  loading: boolean;
  error: string | null;
  onRefresh: () => void;
}

export function DashboardPage({ data, loading, error, onRefresh }: DashboardPageProps) {
  if (loading && !data) {
    return <div className="loading-block">Loading dashboard...</div>;
  }

  if (error && !data) {
    return (
      <div className="error-block">
        <p>{error}</p>
        <button type="button" onClick={onRefresh}>
          Retry
        </button>
      </div>
    );
  }

  const stats = data?.stats ?? {
    total_posts: 0,
    positive_posts: 0,
    neutral_posts: 0,
    negative_posts: 0,
    average_score: 0,
  };

  return (
    <div className="page-stack">
      <section className="stat-grid">
        <StatCard label="Total Posts" value={stats.total_posts} tone="blue" icon={<MessageSquareText />} />
        <StatCard label="Positive" value={stats.positive_posts} tone="green" icon={<Smile />} />
        <StatCard label="Neutral" value={stats.neutral_posts} tone="amber" icon={<Meh />} />
        <StatCard label="Negative" value={stats.negative_posts} tone="red" icon={<Frown />} />
      </section>

      <section className="score-strip">
        <Activity aria-hidden="true" />
        <span>Average compound score</span>
        <strong>{stats.average_score.toFixed(3)}</strong>
      </section>

      <SentimentChart stats={stats} trend={data?.trend ?? []} />

      <section className="panel">
        <div className="panel__header">
          <h2>Recent Posts</h2>
          <button type="button" className="button button--secondary" onClick={onRefresh}>
            Refresh
          </button>
        </div>
        <PostTable posts={data?.recent_posts ?? []} />
      </section>
    </div>
  );
}
