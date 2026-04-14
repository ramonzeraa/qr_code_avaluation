import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ─── SUPABASE ─────────────────────────────────────────────────────────────
    SUPABASE_URL      = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
    # ─── SEGURANÇA ────────────────────────────────────────────────────────────
    OWNER_PASSWORD    = os.getenv("OWNER_PASSWORD")
    SECRET_KEY        = os.getenv("SECRET_KEY")

    # ─── GOOGLE ───────────────────────────────────────────────────────────────
    GOOGLE_REVIEW_URL = os.getenv(
        "GOOGLE_REVIEW_URL",
        "https://maps.app.goo.gl/PYUZ2rcoVZURj4NR9")

    # ─── FLASK ────────────────────────────────────────────────────────────────
    DEBUG             = os.getenv("FLASK_DEBUG", "false").lower() == "true"