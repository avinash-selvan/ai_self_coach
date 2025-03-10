# to understand the schedule module

import schedule
import time
from plyer import notification

def show_notification():
    notification.notify(
        title="Reminder",
        message="This is a test notification.",
        timeout=3
    )
    print("Notification sent!")

    schedule.every(6).seconds.do(show_Avinash).tag("delayed avinash")

def show_Avinash():
    notification.notify(
        title="YAY",
        message="This is a test notification as well.",
        timeout=3
    )
    print("Avinash Notification sent!")

    schedule.clear("delayed avinash")


schedule.every(20).seconds.do(show_notification)


while True:
    schedule.run_pending()
    time.sleep(1)