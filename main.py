import threading
import time
from notifier import Notifier,TEST_INTERVAL
from recorder import Recorder, TEST_DURATION

RUNNING = True

def run_notifier(event):
    global RUNNING
    notifier = Notifier(sleep_time=TEST_INTERVAL)
    try:
        notifier.start(event)
    except KeyboardInterrupt:
        print("\n[Notifier] Stopping safely...")
        notifier.running = False

def run_recorder(event):
    global RUNNING
    recorder = Recorder(duration=TEST_DURATION)  # 30 sec voice log every hour
    try:
        recorder.start(event, interval=TEST_INTERVAL)
    except KeyboardInterrupt:
        print("\n[Recorder] Stopping safely...")
        recorder.running = False

if __name__ == "__main__":

    event = threading.Event()

    # Create threads for both
    notifier_thread = threading.Thread(target=run_notifier, args=(event,))
    recorder_thread = threading.Thread(target=run_recorder, args=(event,))

    # Start both threads
    notifier_thread.start()
    recorder_thread.start()

    try:
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        print("\n[Main] Stopping all processes...")

        # Signal both threads to stop
        event.set()  # Unblock event.wait()
        
        # Wait for threads to complete
        notifier_thread.join()
        recorder_thread.join()

        print("[Main] Successfully exited.")
