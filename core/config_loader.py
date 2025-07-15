# config_loader.py – Merges YAML + QR configuration into unified config

import os
import yaml
import json
import logging

def load_yaml_config(yaml_path):
    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"YAML config not found at {yaml_path}")
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

def load_qr_config(qr_path):
    if not os.path.exists(qr_path):
        return {}
    with open(qr_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            logging.warning("QR config is not valid JSON. Skipping.")
            return {}

def merge_configs(base_config, override_config):
    """Override YAML with QR values where provided"""
    result = base_config.copy()
    for key, value in override_config.items():
        if isinstance(value, dict) and key in result:
            result[key] = merge_configs(result.get(key, {}), value)
        else:
            result[key] = value
    return result

def load_config(yaml_path, qr_path):
    yaml_config = load_yaml_config(yaml_path)
    qr_config = load_qr_config(qr_path)
    merged = merge_configs(yaml_config, qr_config)

    # Validate required fields
    required = ["device_id", "backend_url"]
    for field in required:
        if field not in merged:
            raise ValueError(f"Missing required config field: {field}")

    return merged
