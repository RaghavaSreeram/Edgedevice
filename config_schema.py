
#!/usr/bin/env python3
"""Configuration schema validation"""

import yaml
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

REQUIRED_CONFIG_SCHEMA = {
    'device_id': str,
    'backend_url': str,
    'server': {
        'host': str,
        'port': int,
        'log_level': str
    },
    'camera': {
        'scan_subnet': str,
        'rtsp_timeout': int,
        'discovery_interval': int
    },
    'recording': {
        'output_dir': str,
        'max_file_size': str,
        'segment_duration': int
    }
}

def validate_config_schema(config: Dict[str, Any]) -> bool:
    """
    Validate configuration against required schema
    
    Args:
        config: Configuration dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    def validate_nested(config_section, schema_section, path=""):
        for key, expected_type in schema_section.items():
            current_path = f"{path}.{key}" if path else key
            
            if key not in config_section:
                logger.error(f"Missing required config key: {current_path}")
                return False
                
            if isinstance(expected_type, dict):
                if not isinstance(config_section[key], dict):
                    logger.error(f"Config key {current_path} should be a dict")
                    return False
                if not validate_nested(config_section[key], expected_type, current_path):
                    return False
            else:
                if not isinstance(config_section[key], expected_type):
                    logger.error(f"Config key {current_path} should be {expected_type.__name__}")
                    return False
        return True
    
    return validate_nested(config, REQUIRED_CONFIG_SCHEMA)
