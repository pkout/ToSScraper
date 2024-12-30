from pathlib import Path

def ensure_dir_exists(path):
    Path(path).mkdir(parents=True, exist_ok=True)