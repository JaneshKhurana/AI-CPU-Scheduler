import sys, os
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
import joblib

# Allow importing src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.sim.workload import generate_workload
from src.logging.logger import EventLogger


def extract_features(log_df):
    features = []

    processes = log_df["process_id"].unique()

    for pid in processes:
        proc_df = log_df[log_df["process_id"] == pid]

        start = proc_df[proc_df["action"] == "START"]["time"].min()
        finish = proc_df[proc_df["action"] == "FINISH"]["time"].max()

        burst = finish - start
        wait = start
        tat = finish

        features.append({
            "pid": pid,
            "start_time": start,
            "finish_time": finish,
            "burst_time": burst,
            "wait_time": wait,
            "turnaround_time": tat
        })

    return pd.DataFrame(features)


def train_scheduler_model():
    print("🚀 Starting training...")

    Path("data/raw").mkdir(parents=True, exist_ok=True)
    Path("data/models").mkdir(parents=True, exist_ok=True)

    logger = EventLogger()
    time = 0

    workload = generate_workload(50)

    for _, proc in workload.iterrows():
        logger.log(time, proc["pid"], "START", len(workload))
        time += proc["burst_time"]
        logger.log(time, proc["pid"], "FINISH", len(workload) - 1)

    log_df = logger.to_dataframe()
    log_df.to_csv("data/raw/run_log.csv", index=False)

    print("📁 Log saved → data/raw/run_log.csv")

    feat_df = extract_features(log_df)

    X = feat_df[["burst_time", "wait_time"]]
    y = feat_df["turnaround_time"]

    model = RandomForestRegressor(n_estimators=50)
    model.fit(X, y)

    joblib.dump(model, "data/models/scheduler_model.pkl")

    print("✅ Model saved → data/models/scheduler_model.pkl")
    print("🎉 Training completed!")


if __name__ == "__main__":
    train_scheduler_model()
