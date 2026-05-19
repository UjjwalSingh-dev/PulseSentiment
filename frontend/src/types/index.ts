export type SourceMode = "auto" | "reddit" | "demo";
export type SortMode = "hot" | "new" | "top";
export type SentimentLabel = "positive" | "neutral" | "negative";

export interface AnalyzeRequest {
  subreddit: string;
  keyword: string;
  limit: number;
  sort: SortMode;
  source: SourceMode;
}

export interface PostRead {
  id: number;
  reddit_id: string;
  title: string;
  body: string;
  subreddit: string;
  author: string;
  url: string;
  created_utc: number;
  sentiment_label: SentimentLabel;
  sentiment_score: number;
  analyzed_at: string;
}

export interface AnalyzeResponse {
  message: string;
  source_used: "reddit" | "demo";
  analyzed_count: number;
  posts: PostRead[];
}

export interface StatsResponse {
  total_posts: number;
  positive_posts: number;
  neutral_posts: number;
  negative_posts: number;
  average_score: number;
}

export interface TrendPoint {
  bucket: string;
  positive: number;
  neutral: number;
  negative: number;
  average_score: number;
}

export interface DashboardResponse {
  stats: StatsResponse;
  trend: TrendPoint[];
  recent_posts: PostRead[];
}
