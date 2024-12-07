import json

class ConfigValidator:
    _instance = None

    DEFAULT_CONFIG = {
        'max_text_length': 1000,
        'max_image_size': 4096,
        'max_matrix_size': 512,
        'allowed_formats': ['png', 'jpeg', 'jpg'],
        'output_directory': 'output',
        'chunk_size': 1024,
        'scale_factor': 10
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigValidator, cls).__new__(cls)
            cls._instance._config = None
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_config'):
            self._config = None

    @property
    def config(self):
        if self._config is None:
            self._config = self.load_and_validate_config()
        return self._config

    def load_and_validate_config(self, config_path: str = 'config.json'):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)

            validated_config = self.DEFAULT_CONFIG.copy()
            validated_config.update({
                k: v for k, v in config.items()
                if k in self.DEFAULT_CONFIG
            })

            return validated_config
        except Exception:
            return self.DEFAULT_CONFIG.copy()