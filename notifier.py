import time
from plyer import notification

class Notifier:
    def __init__(self, sleep_time=3600, title="Future Avinash here", message="Please study bro."):
        self.sleep_time = sleep_time
        self.title = title
        self.message = message

    def show_notification(self):
        notification.notify(
            title=self.title,
            message=self.message,
            timeout=2,
            app_name="Ai_coach"
        )

    def start(self):
        while True:
            self.show_notification()
            time.sleep(self.sleep_time)

if __name__ == "__main__":
    notifier = Notifier()  # Default: 1-hour interval
    notifier.start()
