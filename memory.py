"""
Simple in-memory per-user rolling 24-hour chat history.
Note: This is ephemeral (process memory). For persistence, use a DB.
"""
import time
import threading
from typing import Dict, List

_RETENTION_SECONDS = 24 * 3600

_history: Dict[int, List[Dict]] = {}
_lock = threading.Lock()


def add_message(user_id: int, text: str):
    entry = {"time": int(time.time()), "text": text}
    with _lock:
        _history.setdefault(user_id, []).append(entry)


def get_recent(user_id: int, limit: int = 10):
    with _lock:
        items = _history.get(user_id, [])
        # return last `limit` items
        return items[-limit:]


def cleanup_once():
    cutoff = int(time.time()) - _RETENTION_SECONDS
    with _lock:
        for uid in list(_history.keys()):
            lst = _history[uid]
            # keep only messages newer than cutoff
            newlst = [m for m in lst if m['time'] >= cutoff]
            if newlst:
                _history[uid] = newlst
            else:
                del _history[uid]


def start_cleaner(interval_seconds: int = 600):
    def _run():
        while True:
            cleanup_once()
            time.sleep(interval_seconds)

    t = threading.Thread(target=_run, daemon=True)
    t.start()
