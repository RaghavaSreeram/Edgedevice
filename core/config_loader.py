import yaml, json, os

def load_yaml_config(path="/config/config.yaml"):
    if not os.path.exists(path): raise FileNotFoundError(f"Missing YAML config: {path}")
    with open(path, 'r') as f: return yaml.safe_load(f)

def load_qr_config(path="/config/qr_config.json"):
    if not os.path.exists(path): raise FileNotFoundError(f"Missing QR config: {path}")
    with open(path, 'r') as f: return json.load(f)

def get_merged_config():
    yaml_cfg = load_yaml_config()
    qr_cfg = load_qr_config()
    config = yaml_cfg or {}
    config.update(qr_cfg or {})
    return config
