import pandas as pd

def fcfs(workload):
    """
    First Come First Serve (non-preemptive)
    Returns a DataFrame with waiting and turnaround times.
    """
    workload = workload.sort_values(by="arrival_time").reset_index(drop=True)
    time = 0
    results = []

    for _, row in workload.iterrows():
        pid = row["pid"]
        arrival = row["arrival_time"]
        burst = row["burst_time"]

        if time < arrival:
            time = arrival

        start = time
        finish = time + burst
        waiting = start - arrival
        turnaround = finish - arrival

        results.append({
            "pid": pid,
            "arrival": arrival,
            "burst": burst,
            "start": start,
            "finish": finish,
            "waiting": waiting,
            "turnaround": turnaround
        })

        time = finish

    df = pd.DataFrame(results)
    return df


def sjf(workload):
    """
    Shortest Job First (non-preemptive)
    """
    workload = workload.sort_values(by=["arrival_time", "burst_time"]).reset_index(drop=True)
    time = 0
    results = []
    processes = workload.to_dict("records")
    completed = []

    while processes:
        available = [p for p in processes if p["arrival_time"] <= time]
        if not available:
            time += 1
            continue
        current = min(available, key=lambda p: p["burst_time"])
        processes.remove(current)

        start = max(time, current["arrival_time"])
        finish = start + current["burst_time"]
        waiting = start - current["arrival_time"]
        turnaround = finish - current["arrival_time"]

        results.append({
            "pid": current["pid"],
            "arrival": current["arrival_time"],
            "burst": current["burst_time"],
            "start": start,
            "finish": finish,
            "waiting": waiting,
            "turnaround": turnaround
        })

        time = finish

    return pd.DataFrame(results)


def rr(workload, quantum=2):
    """
    Round Robin Scheduler
    """
    queue = workload.sort_values(by="arrival_time").to_dict("records")
    time = 0
    results = []
    ready = []
    remaining = {p["pid"]: p["burst_time"] for p in queue}

    while queue or ready:
        arrived = [p for p in queue if p["arrival_time"] <= time]
        for p in arrived:
            ready.append(p)
            queue.remove(p)

        if not ready:
            time += 1
            continue

        current = ready.pop(0)
        pid = current["pid"]
        exec_time = min(quantum, remaining[pid])
        start = time
        time += exec_time
        remaining[pid] -= exec_time

        if remaining[pid] == 0:
            finish = time
            waiting = finish - current["arrival_time"] - current["burst_time"]
            turnaround = finish - current["arrival_time"]
            results.append({
                "pid": pid,
                "arrival": current["arrival_time"],
                "burst": current["burst_time"],
                "start": start,
                "finish": finish,
                "waiting": waiting,
                "turnaround": turnaround
            })
        else:
            # still has burst left
            arrived = [p for p in queue if p["arrival_time"] <= time]
            for p in arrived:
                ready.append(p)
                queue.remove(p)
            ready.append(current)

    return pd.DataFrame(results)


def priority(workload):
    """
    Priority Scheduling (non-preemptive)
    Lower number = higher priority
    """
    workload = workload.sort_values(by=["arrival_time", "priority"]).reset_index(drop=True)
    time = 0
    results = []
    processes = workload.to_dict("records")

    while processes:
        available = [p for p in processes if p["arrival_time"] <= time]
        if not available:
            time += 1
            continue
        current = min(available, key=lambda p: p["priority"])
        processes.remove(current)

        start = max(time, current["arrival_time"])
        finish = start + current["burst_time"]
        waiting = start - current["arrival_time"]
        turnaround = finish - current["arrival_time"]

        results.append({
            "pid": current["pid"],
            "arrival": current["arrival_time"],
            "burst": current["burst_time"],
            "priority": current["priority"],
            "start": start,
            "finish": finish,
            "waiting": waiting,
            "turnaround": turnaround
        })

        time = finish

    return pd.DataFrame(results)
