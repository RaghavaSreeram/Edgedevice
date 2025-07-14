
import json, yaml, os

def load_yaml(path="/config/config.yaml"):
    if os.path.exists(path):
        with open(path) as f: return yaml.safe_load(f)
    return {}

def load_qr_config(path="/config/qr_config.json"):
    if os.path.exists(path):
        with open(path) as f: return json.load(f)
    return {}

def merge_config():
    cfg = load_yaml()
    qr = load_qr_config()
    cfg.update(qr)
    return cfg
