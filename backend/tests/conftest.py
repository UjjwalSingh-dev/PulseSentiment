from __future__ import annotations

import os
from pathlib import Path
import sys


BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

os.environ.setdefault("DATABASE_URL", f"sqlite:///{BACKEND_DIR / 'test_pulse_sentiment.db'}")
os.environ.setdefault("FORCE_DEMO_SOURCE", "true")
