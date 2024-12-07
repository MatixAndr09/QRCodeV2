from pathlib import Path
import re

class InputSanitizer:
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        safe_name = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
        return safe_name or 'default_qr'

    @staticmethod
    def sanitize_path(path: str) -> str:
        return str(Path(path).resolve())

    @staticmethod
    def sanitize_text(text: str) -> str:
        return ''.join(char for char in text if char.isprintable() or char == '\n')