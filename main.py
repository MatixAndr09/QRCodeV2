from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from typing import Optional
from PIL import Image
import asyncio
import os

from modules.decoder import generate_qr_image, decode_qr_image, qr_matrix_to_text
from modules.sizeDetect import calculate_qr_size
from modules.encoder import encode_to_qr
from modules.security import MemoryGuard
from modules.sanitizer import InputSanitizer
from modules.config import ConfigValidator
from modules.logger import SecurityLogger


@lru_cache(maxsize=128)
def format_file_size(size: int) -> str:
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024


class QRCodeProcessor:
    def __init__(self):
        self.config = ConfigValidator.get_instance().config
        self.logger = SecurityLogger.get_instance()
        self.sanitizer = InputSanitizer()
        self.memory_guard = MemoryGuard()
        self.executor = ThreadPoolExecutor(max_workers=4)  # Add this line
        os.makedirs(self.config['output_directory'], exist_ok=True)

    async def validate_image_file(self, path: str) -> bool:
        try:
            if not os.path.isfile(path):
                return False
            with Image.open(path) as img:
                img.verify()
                return img.format.lower() in self.config['allowed_formats']
        except Exception as e:
            self.logger.log_error("File Validation", str(e))
            return False

    def safe_save_path(self, filename: str) -> str:
        return os.path.join(self.config['output_directory'],
                            self.sanitizer.sanitize_filename(filename))

    async def process_encode(self, text: str) -> Optional[str]:
        try:
            if not self.memory_guard.check_memory_usage():
                raise MemoryError("Insufficient memory available")

            clean_text = self.sanitizer.sanitize_text(text)
            if not clean_text or len(clean_text) > self.config['max_text_length']:
                raise ValueError(f"Invalid text length. Must be between 1 and {self.config['max_text_length']}")

            size = calculate_qr_size(len(clean_text))
            if not self.memory_guard.validate_matrix_size(size, size):
                raise ValueError("Resulting QR code too large")

            qr_matrix = await asyncio.to_thread(encode_to_qr, clean_text, size)
            qr_image = await asyncio.to_thread(generate_qr_image, qr_matrix)

            file_path = self.safe_save_path("qr_code.png")
            await asyncio.to_thread(lambda: qr_image.save(file_path))

            self.logger.log_security_event("Encode", f"QR code generated: {file_path}")
            return file_path

        except Exception as e:
            self.logger.log_error("Encode", str(e))
            raise

    async def process_decode(self, image_path: str) -> Optional[str]:
        try:
            safe_path = self.sanitizer.sanitize_path(image_path)
            if not await self.validate_image_file(safe_path):
                raise ValueError("Invalid or unsupported image file")

            if not self.memory_guard.check_memory_usage():
                raise MemoryError("Insufficient memory available")

            qr_matrix = await asyncio.to_thread(decode_qr_image, safe_path)
            text = await asyncio.to_thread(qr_matrix_to_text, qr_matrix)

            self.logger.log_security_event("Decode", f"QR code decoded: {safe_path}")
            return text

        except Exception as e:
            self.logger.log_error("Decode", str(e))
            raise


async def main():
    processor = QRCodeProcessor()

    try:
        mode = input("Enter mode (encode/decode): ").strip().lower()

        if mode == "encode":
            text = input("Enter text to encode: ").strip()
            try:
                output_path = await processor.process_encode(text)
                if output_path:
                    print(f"\nQR code generated successfully!")
                    print(f"Saved as: {output_path}")

                    file_size = os.path.getsize(output_path)
                    with Image.open(output_path) as img:
                        print(f"Image size: {img.size[0]}x{img.size[1]} pixels")
                    print(f"File size: {format_file_size(file_size)}")

            except (ValueError, MemoryError) as e:
                print(f"Error: {str(e)}")

        elif mode == "decode":
            image_path = input("Enter path to QR code image: ").strip()
            try:
                decoded_text = await processor.process_decode(image_path)
                if decoded_text:
                    print("\nSuccessfully decoded QR code!")
                    print(f"Decoded text: {decoded_text}")

            except (ValueError, MemoryError) as e:
                print(f"Error: {str(e)}")

        else:
            print("Invalid mode. Please enter 'encode' or 'decode'.")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        processor.logger.log_error("Main", str(e))


if __name__ == "__main__":
    asyncio.run(main())