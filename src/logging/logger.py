import pandas as pd

class EventLogger:
    def __init__(self):
        self.events = []

    def log(self, time, pid, action, ready_q_len):
        """Record an event in the log."""
        self.events.append({
            "time": time,
            "process_id": pid,
            "action": action,
            "ready_queue_len": ready_q_len
        })

    def to_dataframe(self):
        """Convert events to a pandas DataFrame."""
        return pd.DataFrame(self.events)

    def save(self, path="data/raw/run_log.csv"):
        """Save events to CSV."""
        df = self.to_dataframe()
        df.to_csv(path, index=False)
        print(f"✅ Log saved to {path}")
