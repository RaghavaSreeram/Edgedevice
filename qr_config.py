
#!/usr/bin/env python3
"""QR configuration loader and validator"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def load_qr_config(config_path: str = "qr_config.json") -> Optional[Dict[str, Any]]:
    """
    Load and validate QR JSON config
    
    Args:
        config_path: Path to the QR config JSON file
        
    Returns:
        Dictionary containing configuration or None if failed
    """
    try:
        config_file = Path(config_path)
        if not config_file.exists():
            logger.warning(f"QR config file not found: {config_path}")
            return None
            
        with open(config_file, 'r') as f:
            config = json.load(f)
            
        # Validate required fields
        required_fields = ['device_id', 'backend_url']
        missing_fields = [field for field in required_fields if not config.get(field)]
        
        if missing_fields:
            logger.error(f"Missing required fields in QR config: {missing_fields}")
            return None
            
        logger.info("QR configuration loaded successfully")
        return config
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in QR config: {e}")
        return None
    except Exception as e:
        logger.error(f"Error loading QR config: {e}")
        return None

def save_qr_config(config: Dict[str, Any], config_path: str = "qr_config.json") -> bool:
    """
    Save QR configuration to JSON file
    
    Args:
        config: Configuration dictionary to save
        config_path: Path where to save the config
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        logger.info(f"QR configuration saved to {config_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving QR config: {e}")
        return False

def validate_qr_config(config: Dict[str, Any]) -> bool:
    """
    Validate QR configuration structure
    
    Args:
        config: Configuration dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_structure = {
        'device_id': str,
        'location': str,
        'backend_url': str,
        'api_key': str,
        'settings': dict
    }
    
    for field, expected_type in required_structure.items():
        if field not in config:
            logger.error(f"Missing required field: {field}")
            return False
        if not isinstance(config[field], expected_type):
            logger.error(f"Invalid type for {field}: expected {expected_type.__name__}")
            return False
            
    return True
