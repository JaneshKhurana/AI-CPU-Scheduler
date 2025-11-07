from src.sim.workload import generate_workload
from src.sim.schedulers import fcfs, sjf, rr, priority

def run_sim(algorithm="RR", quantum=2, n=5):
    workload = generate_workload(n)
    print("Generated Workload:")
    print(workload)
    print("-" * 40)

    if algorithm.upper() == "FCFS":
        results = fcfs(workload)
    elif algorithm.upper() == "SJF":
        results = sjf(workload)
    elif algorithm.upper() == "RR":
        results = rr(workload, quantum)
    else:
        results = priority(workload)

    print(f"Results for {algorithm} Scheduling:")
    print(results)
    print("-" * 40)
    print(f"Average Waiting Time: {results['waiting'].mean():.2f}")
    print(f"Average Turnaround Time: {results['turnaround'].mean():.2f}")

if __name__ == "__main__":
    run_sim("RR", quantum=3, n=5)
