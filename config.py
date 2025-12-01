import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
MODEL_NAME: str = os.getenv("GENAI_MODEL", "gemini-1.5-flash")
PORT: int = int(os.getenv("PORT", "8000"))

if not GOOGLE_API_KEY or not TELEGRAM_BOT_TOKEN:
    raise EnvironmentError("GOOGLE_API_KEY or TELEGRAM_BOT_TOKEN missing in environment (.env)")
