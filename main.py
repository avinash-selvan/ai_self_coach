import threading
from notifier import Notifier,TEST_INTERVAL
from recorder import Recorder, TEST_DURATION

def run_notifier(event):
    notifier = Notifier(sleep_time=TEST_INTERVAL)
    notifier.start(event=event)

def run_recorder(event):
    recorder = Recorder(duration=TEST_DURATION)  # 30 sec voice log every hour
    recorder.start(event=event, interval=TEST_INTERVAL)  # Match notification interval

if __name__ == "__main__":

    event = threading.Event()

    # Create threads for both
    notifier_thread = threading.Thread(target=run_notifier, args=(event,))
    recorder_thread = threading.Thread(target=run_recorder, args=(event,))

    # Start both threads
    notifier_thread.start()
    recorder_thread.start()

    try:
        # Keep running
        notifier_thread.join()
        recorder_thread.join()
    except KeyboardInterrupt:
        print("\nStopping gracefully...")
