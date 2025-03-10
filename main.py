from recorder import VoiceRecorder
from notifier import Notifier
import threading
import time

RECORD_DURATION = 10
NOTIFICATION_TITLE = "Record Alert!⚠️"
NOTIFICATION_MESSAGE = "Recording Starts in 5 seconds, be ready"
SLEEP_TIME = 10
DELAY_BEFORE_RECORDING = 5



class AI_Coach:
    def __init__(self,sleep_time=3600, delay_before_recording=5):
        self.notifier = Notifier(sleep_time=sleep_time, message=NOTIFICATION_MESSAGE, title=NOTIFICATION_TITLE)
        self.recorder = VoiceRecorder(duration=RECORD_DURATION)
        self.delay_before_recording = delay_before_recording

    def run_cycle(self):
        """RUNS A SINGLE CYCLE: SHOWS NOTIFICATION, WAITS, THEN RECORDS."""
        self.notifier.show_notification()
        time.sleep(self.delay_before_recording)
        self.recorder.record()
    
    def start(self):
        """Runs the AI coach continuously."""
        while True:
            thread = threading.Thread(target=self.run_cycle)
            thread.start()
            time.sleep(self.notifier.sleep_time)  # Wait for next interval

if __name__ == "__main__":
    coach = AI_Coach(sleep_time=SLEEP_TIME, delay_before_recording=DELAY_BEFORE_RECORDING)  # Adjust delay as needed
    coach.start()