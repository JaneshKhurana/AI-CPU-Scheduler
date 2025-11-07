import random
import pandas as pd

def generate_workload(num_processes=5):
    """
    Generate a simple workload: list of processes with burst time, arrival time, and priority.
    """
    workload = []
    for i in range(num_processes):
        process = {
            "pid": f"P{i+1}",
            "arrival_time": random.randint(0, 10),
            "burst_time": random.randint(1, 10),
            "priority": random.randint(1, 5)
        }
        workload.append(process)

    df = pd.DataFrame(workload)
    return df
