import yaml
import json
import os

def load_yaml_config(path="/config/config.yaml"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"YAML config not found at {path}")
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def load_qr_config(path="/config/qr_config.json"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"QR config not found at {path}")
    with open(path, 'r') as f:
        return json.load(f)

def merge_configs(yaml_cfg, qr_cfg):
    merged = yaml_cfg.copy()
    merged.update(qr_cfg)
    return merged
