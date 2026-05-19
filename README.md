# PulseSentiment

PulseSentiment is a mini full-stack project for analyzing sentiment in Reddit posts. It fetches posts from Reddit or local demo data, runs VADER sentiment analysis, stores the results in SQLite, and visualizes trends in a real-time React dashboard.

## Features

- Analyze Reddit posts by subreddit, keyword, sort mode, and limit.
- Use VADER sentiment scoring to classify posts as positive, neutral, or negative.
- Save analyzed posts in SQLite.
- View dashboard stats, sentiment trend charts, sentiment mix, and recent posts.
- Use demo mode without Reddit credentials.
- Refresh dashboard data automatically.

## Tech Stack

- Backend: FastAPI, Pydantic, SQLite, PRAW, VADER
- Frontend: React, Vite, TypeScript, Chart.js, lucide-react
- Testing: pytest, FastAPI TestClient

## Project Structure

```text
PulseSentiment/
  backend/
    app/
      api/
      core/
      db/
      models/
      schemas/
      services/
      main.py
    tests/
    .env.example
    requirements.txt
  frontend/
    public/
    src/
      api/
      components/
      pages/
      types/
      App.tsx
      main.tsx
      styles.css
    package.json
  .gitignore
  README.md
```

PowerShell commands to create this structure manually:

```powershell
New-Item -ItemType Directory -Force backend, frontend
New-Item -ItemType Directory -Force backend\app, backend\app\api, backend\app\core, backend\app\db, backend\app\models, backend\app\schemas, backend\app\services, backend\tests
New-Item -ItemType Directory -Force frontend\public, frontend\src, frontend\src\api, frontend\src\components, frontend\src\pages, frontend\src\types

New-Item -ItemType File -Force backend\app\main.py
New-Item -ItemType File -Force backend\requirements.txt
New-Item -ItemType File -Force backend\.env.example
New-Item -ItemType File -Force frontend\package.json
New-Item -ItemType File -Force frontend\index.html
New-Item -ItemType File -Force README.md
New-Item -ItemType File -Force .gitignore
```

## Database

SQLite table: `posts`

| Column | Purpose |
| --- | --- |
| `id` | Local database ID |
| `reddit_id` | Unique Reddit or demo post ID |
| `title` | Post title |
| `body` | Post body/selftext |
| `subreddit` | Source subreddit |
| `author` | Post author |
| `url` | Reddit URL |
| `created_utc` | Original post timestamp |
| `sentiment_label` | positive, neutral, or negative |
| `sentiment_score` | VADER compound score |
| `analyzed_at` | Analysis timestamp |

## Backend Setup

PowerShell commands:

```powershell
Set-Location D:\03_PROJECTS\PulseSentiment\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend health check:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Run backend tests:

```powershell
Set-Location D:\03_PROJECTS\PulseSentiment\backend
.\.venv\Scripts\Activate.ps1
pytest
```

## Reddit Credentials

The app works without Reddit credentials by using demo data. For real Reddit posts, create a Reddit script app and update `backend\.env`.

```powershell
Set-Location D:\03_PROJECTS\PulseSentiment\backend
notepad .env
```

Fill these values:

```env
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=PulseSentimentMiniProject/1.0 by your_reddit_username
```

To force local demo data:

```env
FORCE_DEMO_SOURCE=true
```

## Frontend Setup

PowerShell commands:

```powershell
Set-Location D:\03_PROJECTS\PulseSentiment\frontend
npm install
npm run dev
```

Open:

```text
http://127.0.0.1:5173
```

If npm is broken on your machine, reinstall Node.js LTS or use Corepack with pnpm:

```powershell
corepack enable
corepack prepare pnpm@latest --activate
pnpm install
pnpm dev
```

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | API health check |
| `POST` | `/api/analyze` | Fetch, analyze, and store posts |
| `GET` | `/api/dashboard` | Dashboard stats, trend, and recent posts |
| `GET` | `/api/posts` | Stored posts with optional filters |

Example analyze request:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8000/api/analyze `
  -ContentType "application/json" `
  -Body '{"subreddit":"technology","keyword":"AI","limit":10,"sort":"hot","source":"demo"}'
```

## Module Roadmap

1. Project setup: folders, config, Git ignore, docs.
2. Backend sentiment module: VADER service and validation.
3. Reddit ingestion module: real Reddit API plus demo fallback.
4. Database module: SQLite table, repository, dashboard queries.
5. Frontend module: dashboard, analyze page, history page.
6. API integration module: client wrapper, forms, error states, refresh loop.
7. Final cleanup: README, tests, GitHub-ready structure.

## Git Workflow

Initialize the repository:

```powershell
Set-Location D:\03_PROJECTS\PulseSentiment
git init
git add .
git commit -m "chore: initialize pulse sentiment project"
```

Suggested commits after future changes:

```powershell
git add .
git commit -m "feat: add reddit sentiment ingestion"
git commit -m "feat: add dashboard charts"
git commit -m "test: add backend api coverage"
git commit -m "docs: update setup instructions"
```

## Notes

- `source: "auto"` uses Reddit when credentials exist and demo data otherwise.
- `source: "demo"` always uses local generated posts.
- `source: "reddit"` requires Reddit credentials.
- Demo rows are generated locally and are labeled as demo data in the UI, not real Reddit users.
- SQLite files are ignored by Git so local analysis data does not pollute the repository.
