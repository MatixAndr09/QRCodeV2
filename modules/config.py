from typing import Dict, Any
import json

class ConfigValidator:
    DEFAULT_CONFIG = {
        'max_text_length': 1000,
        'max_image_size': 4096,
        'max_matrix_size': 512,
        'allowed_formats': ['png', 'jpeg', 'jpg'],
        'output_directory': 'output'
    }

    @staticmethod
    def load_and_validate_config(config_path: str = 'config.json') -> Dict[str, Any]:
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)

            for key, default_value in ConfigValidator.DEFAULT_CONFIG.items():
                if key not in config:
                    config[key] = default_value

            return config
        except Exception:
            return ConfigValidator.DEFAULT_CONFIG.copy()