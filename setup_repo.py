import os

# --- Define your project structure ---
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

# --- Requirements to include ---
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

# --- Helper function to create files safely ---
def safe_create(path, content=""):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(content)

# --- Create folders and files recursively ---
def create_structure(base_path="."):
    print(f"Creating AI Scheduler repo structure in: {os.path.abspath(base_path)}\n")
    
    # Base folders
    for folder, subitems in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)

        if isinstance(subitems, dict):
            # Nested directories (like src/*)
            for subfolder, files in subitems.items():
                sub_path = os.path.join(folder_path, subfolder)
                os.makedirs(sub_path, exist_ok=True)
                for filename in files:
                    safe_create(os.path.join(sub_path, filename))
        else:
            # Simple folder (like data/raw)
            for subfolder in subitems:
                os.makedirs(os.path.join(folder_path, subfolder), exist_ok=True)

    # --- Create root-level files ---
    safe_create(os.path.join(base_path, "README.md"), "# AI-Powered Adaptive OS Scheduler\n")
    safe_create(os.path.join(base_path, "requirements.txt"), requirements)
    safe_create(os.path.join(base_path, "src", "utils.py"), "# utility functions\n")

    print("✅ Project structure created successfully!")
    print("Next steps:")
    print("1. Run: pip install -r requirements.txt")
    print("2. Start coding in src/sim/process.py or src/sim/runner.py")
    print("3. Initialize Git repo with: git init && git add . && git commit -m 'Initial scaffold'")
    print("\n🚀 You’re ready to build your AI Scheduler!")

# --- Run the script ---
if __name__ == "__main__":
    create_structure(".")
