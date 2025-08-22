from datetime import datetime, timedelta

def next_review(last_review, success, current_interval):
    if success:
        return last_review + timedelta(days=current_interval * 2)
    else:
        return last_review + timedelta(days=1)
