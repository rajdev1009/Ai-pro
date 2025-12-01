"""
AI wrapper using google.generativeai (genai) package.
Sends recent history along with current message for context.
"""
import google.generativeai as genai
from typing import Optional
from config import GOOGLE_API_KEY, MODEL_NAME
from memory import get_recent

genai.configure(api_key=GOOGLE_API_KEY)

MODEL = MODEL_NAME


def generate_reply(user_id: int, user_text: str, max_tokens: int = 512) -> str:
    """Send a context-aware request and return text reply. Handles basic errors."""
    try:
        # build a prompt using last few messages
        recent = get_recent(user_id, limit=6)
        prompt_parts = []
        for m in recent:
            prompt_parts.append(f"User: {m['text']}")
        prompt_parts.append(f"User: {user_text}")
        prompt = "\n".join(prompt_parts)

        response = genai.generate_text(model=MODEL, prompt=prompt, max_output_tokens=max_tokens)
        # response may be a simple string or object; guard access
        if isinstance(response, str):
            return response
        # if response has 'candidates' or 'content' or 'output' structure
        if hasattr(response, 'text'):
            return response.text
        if hasattr(response, 'candidates') and response.candidates:
            c = response.candidates[0]
            return getattr(c, 'content', getattr(c, 'text', str(c)))
        # fallback
        return str(response)
    except Exception as e:
        # log and return safe message
        print(f"AI error: {e}")
        return "Maaf — AI se jawab nahi aa paaya. Thoda der baad try karein."
