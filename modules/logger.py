# modules/logger.py
import logging
from datetime import datetime
import os


class SecurityLogger:
    def __init__(self):
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)

        log_file = f'logs/qr_security_{datetime.now().strftime("%Y%m%d")}.log'

        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def log_security_event(self, event_type: str, details: str):
        logging.info(f"Security Event - {event_type}: {details}")

    def log_error(self, error_type: str, details: str):
        logging.error(f"Error - {error_type}: {details}")