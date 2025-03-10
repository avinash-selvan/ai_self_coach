import time
from plyer import notification

def main():
    notification.notify(
        title="Future Avinash here",
        message="Please study bro.",
        timeout=2,
        app_name="Ai_coach"
    )

if __name__=="__main__":
    while True:
        main()
        time.sleep(10)
