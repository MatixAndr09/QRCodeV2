from datetime import datetime
import logging
import os


def log_security_event(event_type: str, details: str):
    logging.info(f"Security Event - {event_type}: {details}")


def log_error(error_type: str, details: str):
    logging.error(f"Error - {error_type}: {details}")


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