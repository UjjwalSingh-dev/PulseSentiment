import { useCallback, useEffect, useState } from "react";
import type { ReactNode } from "react";
import { BarChart3, Database, Gauge, RefreshCw, Search } from "lucide-react";

import { getDashboard } from "./api/client";
import { AnalyzePage } from "./pages/AnalyzePage";
import { DashboardPage } from "./pages/DashboardPage";
import { HistoryPage } from "./pages/HistoryPage";
import type { DashboardResponse } from "./types";

type View = "dashboard" | "analyze" | "history";

const navItems: Array<{ id: View; label: string; icon: ReactNode }> = [
  { id: "dashboard", label: "Dashboard", icon: <Gauge /> },
  { id: "analyze", label: "Analyze", icon: <Search /> },
  { id: "history", label: "History", icon: <Database /> },
];

export default function App() {
  const [view, setView] = useState<View>("dashboard");
  const [dashboard, setDashboard] = useState<DashboardResponse | null>(null);
  const [loadingDashboard, setLoadingDashboard] = useState(true);
  const [dashboardError, setDashboardError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);

  const loadDashboard = useCallback(async () => {
    setLoadingDashboard(true);
    setDashboardError(null);
    try {
      const response = await getDashboard();
      setDashboard(response);
      setLastUpdated(new Date().toLocaleTimeString());
    } catch (caught) {
      setDashboardError(caught instanceof Error ? caught.message : "Could not load dashboard.");
    } finally {
      setLoadingDashboard(false);
    }
  }, []);

  useEffect(() => {
    void loadDashboard();
    const intervalId = window.setInterval(() => {
      void loadDashboard();
    }, 7000);

    return () => window.clearInterval(intervalId);
  }, [loadDashboard]);

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand__mark">
            <BarChart3 aria-hidden="true" />
          </div>
          <div>
            <strong>PulseSentiment</strong>
            <span>Reddit sentiment dashboard</span>
          </div>
        </div>

        <nav className="nav-list" aria-label="Primary navigation">
          {navItems.map((item) => (
            <button
              key={item.id}
              type="button"
              className={view === item.id ? "nav-item nav-item--active" : "nav-item"}
              onClick={() => setView(item.id)}
            >
              {item.icon}
              {item.label}
            </button>
          ))}
        </nav>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div>
            <p>Live Reddit analysis</p>
            <h1>{view === "dashboard" ? "Dashboard" : view === "analyze" ? "Analyze" : "History"}</h1>
          </div>
          <button type="button" className="button button--secondary" onClick={loadDashboard}>
            <RefreshCw aria-hidden="true" />
            {lastUpdated ? `Updated ${lastUpdated}` : "Refresh"}
          </button>
        </header>

        {view === "dashboard" ? (
          <DashboardPage
            data={dashboard}
            loading={loadingDashboard}
            error={dashboardError}
            onRefresh={loadDashboard}
          />
        ) : null}

        {view === "analyze" ? <AnalyzePage onAnalyzed={loadDashboard} /> : null}
        {view === "history" ? <HistoryPage /> : null}
      </section>
    </main>
  );
}
