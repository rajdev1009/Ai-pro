"""
Alarm management using APScheduler BackgroundScheduler.
Each user can set one alarm (HH:MM local server time). On trigger, bot sends private message.
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import threading

_scheduler = BackgroundScheduler()
_scheduler_started = False

# store user alarms in memory: {user_id: "HH:MM"}
_user_alarms = {}
_lock = threading.Lock()


def start_scheduler():
    global _scheduler_started
    if not _scheduler_started:
        _scheduler.start()
        _scheduler_started = True


def set_alarm(bot, user_id: int, hhmm: str, callback_message: str = "Aapka study time hai"):
    """Set or replace user's alarm (single daily alarm at hh:mm)."""
    start_scheduler()
    job_id = f"alarm_{user_id}"

    # parse hhmm
    hh, mm = hhmm.split(":")

    with _lock:
        # remove existing
        try:
            _scheduler.remove_job(job_id)
        except Exception:
            pass

        # schedule cron job every day at hh:mm
        trigger = CronTrigger(hour=int(hh), minute=int(mm))

        def _job():
            try:
                bot.send_message(user_id, f"⏰ Reminder: {callback_message}")
            except Exception as e:
                print(f"Failed to send alarm msg to {user_id}: {e}")

        _scheduler.add_job(_job, trigger, id=job_id, replace_existing=True)
        _user_alarms[user_id] = hhmm


def remove_alarm(user_id: int):
    job_id = f"alarm_{user_id}"
    with _lock:
        try:
            _scheduler.remove_job(job_id)
        except Exception:
            pass
        if user_id in _user_alarms:
            del _user_alarms[user_id]


def get_alarm(user_id: int):
    return _user_alarms.get(user_id)
  
