import {
  ArcElement,
  CategoryScale,
  Chart as ChartJS,
  Filler,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Tooltip,
} from "chart.js";
import { Doughnut, Line } from "react-chartjs-2";

import type { StatsResponse, TrendPoint } from "../types";

ChartJS.register(
  ArcElement,
  CategoryScale,
  Filler,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Tooltip,
);

interface SentimentChartProps {
  stats: StatsResponse;
  trend: TrendPoint[];
}

export function SentimentChart({ stats, trend }: SentimentChartProps) {
  const hasData = stats.total_posts > 0;

  if (!hasData) {
    return (
      <section className="panel chart-panel">
        <div className="panel__header">
          <h2>Sentiment Trend</h2>
        </div>
        <div className="empty-state">Run an analysis to populate the trend chart.</div>
      </section>
    );
  }

  const labels = trend.map((point) => point.bucket);
  const lineData = {
    labels,
    datasets: [
      {
        label: "Positive",
        data: trend.map((point) => point.positive),
        borderColor: "#16A34A",
        backgroundColor: "rgba(22, 163, 74, 0.12)",
        fill: true,
        tension: 0.35,
      },
      {
        label: "Neutral",
        data: trend.map((point) => point.neutral),
        borderColor: "#CA8A04",
        backgroundColor: "rgba(202, 138, 4, 0.1)",
        fill: true,
        tension: 0.35,
      },
      {
        label: "Negative",
        data: trend.map((point) => point.negative),
        borderColor: "#DC2626",
        backgroundColor: "rgba(220, 38, 38, 0.1)",
        fill: true,
        tension: 0.35,
      },
    ],
  };

  const doughnutData = {
    labels: ["Positive", "Neutral", "Negative"],
    datasets: [
      {
        data: [stats.positive_posts, stats.neutral_posts, stats.negative_posts],
        backgroundColor: ["#16A34A", "#CA8A04", "#DC2626"],
        borderColor: "#FFFFFF",
        borderWidth: 2,
      },
    ],
  };

  return (
    <div className="chart-grid">
      <section className="panel chart-panel">
        <div className="panel__header">
          <h2>Sentiment Trend</h2>
        </div>
        <Line
          data={lineData}
          options={{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: "bottom",
              },
            },
            scales: {
              y: {
                beginAtZero: true,
                ticks: {
                  precision: 0,
                },
              },
            },
          }}
        />
      </section>

      <section className="panel chart-panel chart-panel--compact">
        <div className="panel__header">
          <h2>Sentiment Mix</h2>
        </div>
        <Doughnut
          data={doughnutData}
          options={{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: "bottom",
              },
            },
          }}
        />
      </section>
    </div>
  );
}
