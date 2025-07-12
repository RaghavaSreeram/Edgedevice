import os, yaml
def load_config(path="/config/config.yaml"):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Config not found: {path}")
    with open(path) as f:
        return yaml.safe_load(f)
