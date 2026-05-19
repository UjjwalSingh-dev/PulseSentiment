import type { PostRead } from "../types";
import { StatusBadge } from "./StatusBadge";

interface PostTableProps {
  posts: PostRead[];
}

function formatDate(value: string): string {
  return new Intl.DateTimeFormat("en", {
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

function isDemoPost(post: PostRead): boolean {
  return post.reddit_id.startsWith("demo-");
}

function getAuthorLabel(post: PostRead): string {
  return isDemoPost(post) ? "Demo data" : `u/${post.author}`;
}

export function PostTable({ posts }: PostTableProps) {
  if (posts.length === 0) {
    return <div className="empty-state">No posts available yet.</div>;
  }

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Post</th>
            <th>Subreddit</th>
            <th>Sentiment</th>
            <th>Score</th>
            <th>Analyzed</th>
          </tr>
        </thead>
        <tbody>
          {posts.map((post) => {
            const demoPost = isDemoPost(post);

            return (
              <tr key={post.id}>
                <td data-label="Post">
                  <a href={post.url} target="_blank" rel="noreferrer">
                    {post.title}
                  </a>
                  <span className={demoPost ? "demo-author" : undefined}>{getAuthorLabel(post)}</span>
                </td>
                <td data-label="Subreddit">r/{post.subreddit}</td>
                <td data-label="Sentiment">
                  <StatusBadge label={post.sentiment_label} />
                </td>
                <td data-label="Score">{post.sentiment_score.toFixed(3)}</td>
                <td data-label="Analyzed">{formatDate(post.analyzed_at)}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
