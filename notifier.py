import time
from plyer import notification

SLEEP = 3600  # Default to 1 hour

def show_notification():
    notification.notify(
        title="Future Avinash here",
        message="Please study bro.",
        timeout=2,
        app_name="Ai_coach"
    )

def schedule_notification(sleep_time=None):
    global SLEEP  
    while True:
        show_notification()
        time.sleep(sleep_time if sleep_time else SLEEP)  # Use passed value or global SLEEP

if __name__ == "__main__":
    schedule_notification()  # Uses global SLEEP, but AI can update it dynamically
