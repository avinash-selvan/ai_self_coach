import time
from plyer import notification
import schedule

TEST_INTERVAL = 20

class Notifier:
    def __init__(self, sleep_time=3600, title="Recording Alert", message="Recording now......"):
        self.sleep_time = sleep_time
        self.title = title
        self.message = message
        self.running = True
        self.last_interval = sleep_time  # Track last used interval

    def show_notification(self):
        notification.notify(
            title=self.title,
            message=self.message,
            timeout=2,
            app_name="Ai_coach"
        )
        print("[Notifier] Notification sent. Triggering recorder...")
        self.event.set()

    def update_interval(self, new_interval):
        """Change the notification interval dynamically"""
        self.sleep_time = new_interval

    def schedule_task(self):
        """Schedules the notification with the updated interval"""
        schedule.clear()  # Remove old jobs
        schedule.every(self.sleep_time).seconds.do(self.show_notification)

    def start(self, event):
        """Runs the scheduler in a loop, allowing dynamic interval updates"""
        self.event=event
        self.show_notification()
        self.schedule_task()  # Initial scheduling
        while self.running:
            if self.sleep_time != self.last_interval:  # Detects interval change
                print(f"Updating notification interval to {self.sleep_time} seconds")  # Debugging
                self.schedule_task()  # Reschedule with the new interval
                self.last_interval = self.sleep_time  # Update tracker

            schedule.run_pending()  # Executes any scheduled jobs
            time.sleep(1)  # Small delay to avoid CPU overuse

    def stop(self):
        """Stops the scheduler loop"""
        self.running = False
        schedule.clear()

if __name__ == "__main__":
    notifier = Notifier(sleep_time=TEST_INTERVAL)  # Testing with 10 sec interval
    notifier.start()
