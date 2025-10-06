from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta

def write_to_file():
    with open("job_log.txt", "a") as f:  # append mode, keeps previous entries
        f.write(f"Job executed at {datetime.now()}\n")
    print(f"Job executed and written to file at {datetime.now()}")

sched = BlockingScheduler()

# Run after 15 seconds
sched.add_job(write_to_file, 'date', run_date=datetime.now() + timedelta(seconds=15))

# Run after 2 minutes
sched.add_job(write_to_file, 'date', run_date=datetime.now() + timedelta(minutes=2))

print("Scheduler started...")
sched.start()
