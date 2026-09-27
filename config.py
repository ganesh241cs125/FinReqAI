from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6").strip()
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/finreqai.db")

KB_DIR = BASE_DIR / "knowledge_base"
DATA_DIR = BASE_DIR / "data"
GENERATED_DIR = BASE_DIR / "generated"
KB_INDEX_DIR = DATA_DIR / "rag_index"

for d in (KB_DIR, DATA_DIR, GENERATED_DIR, KB_INDEX_DIR):
    d.mkdir(parents=True, exist_ok=True)
