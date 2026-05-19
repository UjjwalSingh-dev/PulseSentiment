import type { ReactNode } from "react";

interface StatCardProps {
  label: string;
  value: string | number;
  icon: ReactNode;
  tone: "blue" | "green" | "amber" | "red";
}

export function StatCard({ label, value, icon, tone }: StatCardProps) {
  return (
    <section className={`stat-card stat-card--${tone}`}>
      <div className="stat-card__icon" aria-hidden="true">
        {icon}
      </div>
      <div>
        <p>{label}</p>
        <strong>{value}</strong>
      </div>
    </section>
  );
}
