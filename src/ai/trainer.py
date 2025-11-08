import sys, os
import pandas as pd
from pathlib import Path

# ✅ Ensure project root is visible to Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.sim.workload import generate_workload
from src.sim.schedulers import fcfs, sjf, rr, priority
from src.logging.logger import EventLogger

def train_scheduler_model():
    print("✅ Trainer started successfully.")
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    logger = EventLogger()

    total_runs = 50
    print(f"Generating {total_runs} workloads...")

    time = 0
    for run in range(total_runs):
        workload = generate_workload(100)  # 100 processes per run
        for _, proc in workload.iterrows():
            logger.log(time, proc["pid"], "START", len(workload))
            time += proc["burst_time"]
            logger.log(time, proc["pid"], "FINISH", len(workload) - 1)

    logger.save("data/raw/run_log.csv")
    print(f"✅ Finished generating {total_runs * 100} processes worth of logs!")

if __name__ == "__main__":
    train_scheduler_model()
