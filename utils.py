import time

def now_ts():
    return int(time.time())

def format_time_hhmm(ts):
    # ts is unix timestamp
    import datetime
    return datetime.datetime.fromtimestamp(ts).strftime('%H:%M')

