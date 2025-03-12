import threading
import time
from notifier import Notifier,TEST_INTERVAL
from recorder import Recorder, TEST_DURATION
from AI_intervention import AIIntervention

RUNNING = True

def run_notifier(record_event):
    global RUNNING
    notifier = Notifier(sleep_time=TEST_INTERVAL)
    try:
        notifier.start(record_event)
    except KeyboardInterrupt:
        print("\n[Notifier] Stopping safely...")
        notifier.running = False

def run_recorder(record_event, ai_event):
    global RUNNING
    recorder = Recorder(duration=TEST_DURATION)  # 30 sec voice log every hour
    try:
        recorder.start(record_event, interval=TEST_INTERVAL)
    except KeyboardInterrupt:
        print("\n[Recorder] Stopping safely...")
        recorder.running = False

def run_ai_intervention():
    """Runs AI intervention, waiting for new transcriptions before analyzing."""
    ai = AIIntervention()
    try:
        ai.run(ai_event)
    except KeyboardInterrupt:
        print("\n[AI Intervention] Stopping safely...")

if __name__ == "__main__":

    record_event = threading.Event()
    ai_event = threading.Event()

    # Create threads for both
    notifier_thread = threading.Thread(target=run_notifier, args=(record_event,))
    recorder_thread = threading.Thread(target=run_recorder, args=(record_event,))
    ai_thread = threading.Thread(target=run_ai_intervention, args=(ai_event,))

    # Start both threads
    notifier_thread.start()
    recorder_thread.start()
    ai_thread.start()

    try:
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        print("\n[Main] Stopping all processes...")

        # Signal both threads to stop
        record_event.set()  # Unblock event.wait()
        
        # Wait for threads to complete
        notifier_thread.join()
        recorder_thread.join()

        print("[Main] Successfully exited.")
