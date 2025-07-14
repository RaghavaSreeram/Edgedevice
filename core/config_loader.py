import os
import yaml
import json
from collections.abc import Mapping

def deep_merge(a: dict, b: dict) -> dict:
    """Recursively merge b into a, returning a new dict."""
    result = dict(a)
    for key, val in b.items():
        if (
            key in result 
            and isinstance(result[key], Mapping) 
            and isinstance(val, Mapping)
        ):
            result[key] = deep_merge(result[key], val)
        else:
            result[key] = val
    return result

def load_file(path: str, required: bool = False) -> dict:
    """
    Load a single config file (YAML or JSON).
    If required but missing, raises FileNotFoundError.
    Otherwise returns {} when absent.
    """
    if not os.path.exists(path):
        if required:
            raise FileNotFoundError(f"Config not found: {path}")
        return {}
    with open(path) as f:
        if path.lower().endswith((".yaml", ".yml")):
            return yaml.safe_load(f) or {}
        elif path.lower().endswith(".json"):
            return json.load(f)
        else:
            raise ValueError(f"Unsupported config format: {path}")

def load_config(
    files: list[str] = ["/config/config.yaml", "/config/qr_config.json"],
    required: list[str] = ["/config/config.yaml"],
) -> dict:
    """
    Load and merge multiple config files.

    Args:
      files:    List of file paths to load, in merge order.
      required: Subset of `files` that must exist or we’ll error.

    Returns:
      A single dict with all configs deep-merged.
    """
    merged: dict = {}
    for path in files:
        cfg = load_file(path, required=path in required)
        merged = deep_merge(merged, cfg)
    return merged
