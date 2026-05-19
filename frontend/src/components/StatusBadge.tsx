import type { SentimentLabel } from "../types";

interface StatusBadgeProps {
  label: SentimentLabel;
}

export function StatusBadge({ label }: StatusBadgeProps) {
  return <span className={`status-badge status-badge--${label}`}>{label}</span>;
}
