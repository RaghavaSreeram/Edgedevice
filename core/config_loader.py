import os, yaml

def load_config(path="/config/config.yaml"):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Missing config file: {path}")
    with open(path, 'r') as f:
        return yaml.safe_load(f)
