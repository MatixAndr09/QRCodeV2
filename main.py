from typing import Optional
from PIL import Image
import imghdr
import os

from modules.decoder import generate_qr_image, decode_qr_image, qr_matrix_to_text
from modules.sizeDetect import calculate_qr_size
from modules.encoder import encode_to_qr
from modules.security import MemoryGuard
from modules.sanitizer import InputSanitizer
from modules.config import ConfigValidator
from modules.logger import SecurityLogger


def format_file_size(size: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024


class QRCodeProcessor:
    def __init__(self):
        self.config = ConfigValidator.load_and_validate_config()
        self.logger = SecurityLogger()
        self.sanitizer = InputSanitizer()
        self.memory_guard = MemoryGuard()

        os.makedirs(self.config['output_directory'], exist_ok=True)

    def validate_image_file(self, path: str) -> bool:
        """Validate if the file is a valid image file."""
        try:
            if not os.path.exists(path):
                return False
            if not os.path.isfile(path):
                return False
            img_type = imghdr.what(path)
            return img_type in self.config['allowed_formats']
        except Exception as e:
            self.logger.log_error("File Validation", str(e))
            return False

    def safe_save_path(self, filename: str) -> str:
        """Generate a safe path for saving files."""
        safe_filename = self.sanitizer.sanitize_filename(filename)
        return os.path.join(self.config['output_directory'], safe_filename)

    def process_encode(self, text: str) -> Optional[str]:
        """Process text encoding to QR code with security measures."""
        try:
            # Memory check
            if not self.memory_guard.check_memory_usage():
                raise MemoryError("Insufficient memory available")

            # Input validation
            clean_text = self.sanitizer.sanitize_text(text)
            if not clean_text:
                raise ValueError("Text cannot be empty")

            if len(clean_text) > self.config['max_text_length']:
                raise ValueError(f"Text too long. Maximum length is {self.config['max_text_length']} characters")

            # Generate QR code
            size = calculate_qr_size(len(clean_text))
            if not self.memory_guard.validate_matrix_size(size, size):
                raise ValueError("Resulting QR code would be too large")

            qr_matrix = encode_to_qr(clean_text, size)
            qr_image = generate_qr_image(qr_matrix)

            # Save file
            file_path = self.safe_save_path("custom_qr_code.png")
            qr_image.save(file_path)

            self.logger.log_security_event("Encode", f"Successfully generated QR code: {file_path}")
            return file_path

        except Exception as e:
            self.logger.log_error("Encode", str(e))
            raise

    def process_decode(self, image_path: str) -> Optional[str]:
        """Process QR code decoding with security measures."""
        try:
            # Path validation
            safe_path = self.sanitizer.sanitize_path(image_path)
            if not self.validate_image_file(safe_path):
                raise ValueError("Invalid image file or unsupported format")

            # Memory check
            if not self.memory_guard.check_memory_usage():
                raise MemoryError("Insufficient memory available")

            # Decode QR code
            qr_matrix = decode_qr_image(safe_path)
            text = qr_matrix_to_text(qr_matrix)

            self.logger.log_security_event("Decode", f"Successfully decoded QR code: {safe_path}")
            return text

        except Exception as e:
            self.logger.log_error("Decode", str(e))
            raise


def main():
    """Main function with error handling and user interface."""
    processor = QRCodeProcessor()

    try:
        mode = input("Enter mode (encode/decode): ").strip().lower()

        if mode == "encode":
            text = input("Enter text to encode: ").strip()

            try:
                output_path = processor.process_encode(text)
                if output_path:
                    print(f"\nQR code generated successfully!")
                    print(f"Saved as: {output_path}")

                    # Get file details
                    file_size = os.path.getsize(output_path)
                    img = Image.open(output_path)
                    print(f"Image size: {img.size[0]}x{img.size[1]} pixels")
                    print(f"File size: {format_file_size(file_size)}")

            except ValueError as e:
                print(f"Error: {str(e)}")
            except MemoryError as e:
                print(f"Memory Error: {str(e)}")
            except Exception as e:
                print(f"An unexpected error occurred: {str(e)}")

        elif mode == "decode":
            image_path = input("Enter path to QR code image: ").strip()

            try:
                decoded_text = processor.process_decode(image_path)
                if decoded_text:
                    print("\nSuccessfully decoded QR code!")
                    print(f"Decoded text: {decoded_text}")

            except ValueError as e:
                print(f"Error: {str(e)}")
            except MemoryError as e:
                print(f"Memory Error: {str(e)}")
            except Exception as e:
                print(f"An unexpected error occurred: {str(e)}")

        else:
            print("Invalid mode. Please enter 'encode' or 'decode'.")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        processor.logger.log_error("Main", str(e))


if __name__ == "__main__":
    main()