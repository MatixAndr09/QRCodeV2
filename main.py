from pathlib import Path
import imghdr
import os

from modules.decoder import generate_qr_image, decode_qr_image, qr_matrix_to_text
from modules.sizeDetect import calculate_qr_size
from modules.textToBinary import text_to_binary
from modules.encoder import encode_to_qr

MAX_TEXT_LENGTH = 1000
ALLOWED_IMAGE_TYPES = {'png', 'jpeg', 'jpg'}
OUTPUT_DIR = "output"


def validate_image_file(path):
    try:
        if not os.path.exists(path):
            return False
        if not os.path.isfile(path):
            return False
        img_type = imghdr.what(path)
        return img_type in ALLOWED_IMAGE_TYPES
    except Exception:
        return False


def safe_save_path(filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    safe_filename = os.path.basename(filename)
    return os.path.join(OUTPUT_DIR, safe_filename)


def format_file_size(size):
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024


def main():
    mode = input("Enter mode (encode/decode): ").strip().lower()

    if mode == "encode":
        text = input("Enter text to encode: ").strip()

        # Input validation
        if len(text) > MAX_TEXT_LENGTH:
            print(f"Text too long. Maximum length is {MAX_TEXT_LENGTH} characters.")
            return

        if not text:
            print("Text cannot be empty.")
            return

        try:
            size = calculate_qr_size(len(text))
            qr_matrix = encode_to_qr(text, size)
            qr_image = generate_qr_image(qr_matrix)

            # Secure file saving
            file_path = safe_save_path("custom_qr_code.png")
            qr_image.save(file_path)

            file_size = os.path.getsize(file_path)
            formatted_file_size = format_file_size(file_size)
            print(f"QR code generated and saved as {file_path}")
            print(f"QR code matrix size: {size}x{size} pixels")
            print(f"Generated image size: {qr_image.size[0]}x{qr_image.size[1]} pixels")
            print(f"File size: {formatted_file_size}")

        except Exception as e:
            print(f"An error occurred while encoding: {str(e)}")

    elif mode == "decode":
        image_path = input("Enter path to QR code image: ").strip()

        if not validate_image_file(image_path):
            print("Invalid image file or unsupported format.")
            return

        try:
            qr_matrix = decode_qr_image(image_path)
            text = qr_matrix_to_text(qr_matrix)
            print("Decoded text:", text)

        except Exception as e:
            print(f"An error occurred while decoding: {str(e)}")

    else:
        print("Invalid mode. Please enter 'encode' or 'decode'.")


if __name__ == "__main__":
    main()