import os
from textwrap import dedent

# ================================================================
# CONFIG: folder & file layout
# ================================================================
structure = {
    "data": ["raw", "processed"],
    "src": {
        "sim": ["__init__.py", "process.py", "workload.py", "schedulers.py", "runner.py"],
        "logging": ["__init__.py", "logger.py"],
        "ml": ["__init__.py", "features.py", "train.py", "model.py"],
        "ai_scheduler": ["__init__.py", "ai_scheduler.py"],
        "eval": ["__init__.py", "evaluate.py"],
    },
    "notebooks": [],
    "experiments": [],
}

requirements = """numpy
pandas
scikit-learn
matplotlib
joblib
tqdm
pytest
stable-baselines3
gymnasium
streamlit
"""

# ================================================================
# HELPER FUNCTIONS
# ================================================================
def safe_create(path, content=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")

def create_structure(base_path="."):
    print(f"Creating AI Scheduler repo structure in: {os.path.abspath(base_path)}\n")

    # Base directories
    for folder, subitems in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)

        if isinstance(subitems, dict):
            for subfolder, files in subitems.items():
                sub_path = os.path.join(folder_path, subfolder)
                os.makedirs(sub_path, exist_ok=True)
                for filename in files:
                    safe_create(os.path.join(sub_path, filename))
        else:
            for subfolder in subitems:
                os.makedirs(os.path.join(folder_path, subfolder), exist_ok=True)

    # Root-level files
    safe_create(os.path.join(base_path, "README.md"), "# AI-Powered Adaptive OS Scheduler\n")
    safe_create(os.path.join(base_path, "requirements.txt"), requirements)
    safe_create(os.path.join(base_path, "src", "utils.py"), "# utility functions\n")

    # ============================================================
    # Starter code injection
    # ============================================================

    # Process class
    safe_create(os.path.join(base_path, "src/sim/process.py"), dedent('''
    import itertools

    class Process:
        _ids = itertools.count()

        def __init__(self, arrival, burst, priority=0):
            self.pid = next(self._ids)
            self.arrival = arrival
            self.burst = burst
            self.remaining = burst
            self.priority = priority
            self.start_time = None
            self.finish_time = None

        def run(self, quantum):
            executed = min(self.remaining, quantum)
            self.remaining -= executed
            return executed

        def is_finished(self):
            return self.remaining <= 0

        def __repr__(self):
            return f"P{self.pid}(arr={self.arrival}, burst={self.burst}, rem={self.remaining})"
    '''))

    # Workload generator
    safe_create(os.path.join(base_path, "src/sim/workload.py"), dedent('''
    import random
    from sim.process import Process

    def generate_workload(n=5, max_arrival=10, max_burst=8):
        """Generate n processes with random arrival and burst times."""
        workload = [
            Process(
                arrival=random.randint(0, max_arrival),
                burst=random.randint(1, max_burst),
                priority=random.randint(1, 5)
            )
            for _ in range(n)
        ]
        workload.sort(key=lambda p: p.arrival)
        return workload
    '''))

    # Basic schedulers
    safe_create(os.path.join(base_path, "src/sim/schedulers.py"), dedent('''
    def fcfs(ready):
        return ready[0] if ready else None

    def sjf(ready):
        return min(ready, key=lambda p: p.remaining) if ready else None

    def priority(ready):
        return min(ready, key=lambda p: p.priority) if ready else None

    def rr(ready, last_index):
        if not ready:
            return None, last_index
        next_idx = (last_index + 1) % len(ready)
        return ready[next_idx], next_idx
    '''))

    # Logger
    safe_create(os.path.join(base_path, "src/logging/logger.py"), dedent('''
    import pandas as pd

    class EventLogger:
        def __init__(self):
            self.records = []

        def log(self, time, pid, action, queue_len):
            self.records.append({
                "time": time,
                "pid": pid,
                "action": action,
                "queue_len": queue_len
            })

        def to_dataframe(self):
            return pd.DataFrame(self.records)
    '''))

    # Runner simulation
    safe_create(os.path.join(base_path, "src/sim/runner.py"), dedent('''
    from sim.workload import generate_workload
    from sim.schedulers import fcfs, sjf, rr, priority
    from logging.logger import EventLogger

    def run_sim(algorithm="RR", quantum=2, n=5):
        workload = generate_workload(n)
        ready = []
        time = 0
        last_idx = -1
        logger = EventLogger()
        algo_fn = {"FCFS": fcfs, "SJF": sjf, "PR": priority, "RR": rr}[algorithm.upper()]

        while workload or ready:
            # Add arrivals
            arrived = [p for p in workload if p.arrival <= time]
            for p in arrived:
                ready.append(p)
                workload.remove(p)

            # Pick process
            if algorithm.upper() == "RR":
                proc, last_idx = rr(ready, last_idx)
                quantum_used = proc.run(quantum)
            else:
                proc = algo_fn(ready)
                if not proc:
                    time += 1
                    continue
                quantum_used = proc.run(quantum if algorithm == "RR" else proc.remaining)

            logger.log(time, proc.pid, f"RUN({algorithm})", len(ready))

            time += quantum_used
            if proc.is_finished():
                ready.remove(proc)
                logger.log(time, proc.pid, "FINISH", len(ready))

        df = logger.to_dataframe()
        print(df.head())
        df.to_csv("data/raw/run_log.csv", index=False)
        print("Simulation complete → saved to data/raw/run_log.csv")

    if __name__ == "__main__":
        run_sim("RR", quantum=2, n=6)
    '''))

    # Features + Training placeholders
    safe_create(os.path.join(base_path, "src/ml/features.py"), "# TODO: Extract features from logs\n")
    safe_create(os.path.join(base_path, "src/ml/train.py"), "# TODO: Train ML model here\n")

    print("✅ Full project scaffold + starter code created successfully!")
    print("Next steps:")
    print("1. cd into the folder and run: pip install -r requirements.txt")
    print("2. Test the simulator: python src/sim/runner.py")
    print("3. Check the output CSV in data/raw/run_log.csv")
    print("\n🚀 You now have a working scheduling simulator to build your AI Scheduler on top of!")
    print("Happy coding, Janesh 😄")
    print("-" * 70)

# ================================================================
# MAIN
# ================================================================
if __name__ == "__main__":
    create_structure(".")
