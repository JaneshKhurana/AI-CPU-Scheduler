import joblib
from src.sim.workload import generate_workload
from src.sim.schedulers import fcfs, sjf, rr, priority
from src.ai.trainer import extract_features

def adaptive_scheduler(workload):
    """Choose best scheduler using trained model and run it."""
    model = joblib.load("data/models/scheduler_model.pkl")
    features = extract_features(workload)
    import pandas as pd
    X = pd.DataFrame([features])
    pred = model.predict(X)[0]
    print(f"🤖 AI chose: {pred}")

    if pred == "FCFS":
        res = fcfs(workload)
    elif pred == "SJF":
        res = sjf(workload)
    elif pred == "RR":
        res = rr(workload, quantum=3)
    else:
        res = priority(workload)

    print("Results:")
    print(res)
    print(f"Average Waiting Time: {res['waiting'].mean():.2f}")
    return res

if __name__ == "__main__":
    workload = generate_workload(6)
    print("Generated workload:")
    print(workload)
    print("-" * 40)
    adaptive_scheduler(workload)
