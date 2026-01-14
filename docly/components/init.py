from pathlib import Path
import yaml
from docly.scanner import scan_repo

def init_project(force=False, ignore_name=None):
    path = Path("docly.yaml")
    if path.exists() and not force:
        raise SystemExit("docly.yaml already exists")
    data = scan_repo(ignore_name)
    path.write_text(yaml.dump(data, sort_keys=False))
    print("Docly initialized successfully")
