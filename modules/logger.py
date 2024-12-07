from datetime import datetime
import logging
import os

class SecurityLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SecurityLogger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if not self._initialized:
            log_dir = 'logs'
            os.makedirs(log_dir, exist_ok=True)

            log_file = f'logs/qr_security_{datetime.now().strftime("%Y%m%d")}.log'

            logging.basicConfig(
                filename=log_file,
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
            self._initialized = True

    def log_security_event(self, event_type: str, details: str):
        logging.info(f"Security Event - {event_type}: {details}")

    def log_error(self, error_type: str, details: str):
        logging.error(f"Error - {error_type}: {details}")