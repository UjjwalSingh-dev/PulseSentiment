import type {
  AnalyzeRequest,
  AnalyzeResponse,
  DashboardResponse,
  PostRead,
  SentimentLabel,
} from "../types";

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000").replace(/\/$/, "");

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    let message = "Something went wrong while contacting the API.";
    try {
      const payload = (await response.json()) as { detail?: string };
      message = payload.detail ?? message;
    } catch {
      message = response.statusText || message;
    }
    throw new Error(message);
  }

  return response.json() as Promise<T>;
}

export function getDashboard(): Promise<DashboardResponse> {
  return request<DashboardResponse>("/api/dashboard");
}

export function analyzePosts(payload: AnalyzeRequest): Promise<AnalyzeResponse> {
  return request<AnalyzeResponse>("/api/analyze", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getPosts(filters: {
  subreddit?: string;
  sentiment?: SentimentLabel | "";
  limit?: number;
}): Promise<PostRead[]> {
  const params = new URLSearchParams();
  if (filters.subreddit) params.set("subreddit", filters.subreddit);
  if (filters.sentiment) params.set("sentiment", filters.sentiment);
  params.set("limit", String(filters.limit ?? 50));

  return request<PostRead[]>(`/api/posts?${params.toString()}`);
}
