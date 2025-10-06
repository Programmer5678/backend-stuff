from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

# Function to run
def write_to_file():
    with open("file.txt", "w") as f:
        f.write("123")
    print(f"Written to file at {datetime.now()}")

# Create scheduler
sched = BlockingScheduler()

# Schedule one-off job at a specific datetime
# Example: October 4, 2025 at 22:05
sched.add_job(write_to_file, 'date', run_date=datetime(2025, 10, 4, 22, 5))

print("Scheduler started, waiting for job...")
sched.start()  # Blocks here until job runs
print("Scheduler finished all jobs")

