# main.py
import os
from modules.textToBinary import text_to_binary
from modules.encoder import encode_to_qr
from modules.decoder import generate_qr_image, decode_qr_image, qr_matrix_to_text
from modules.sizeDetect import calculate_qr_size

def format_file_size(size):
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def main():
    mode = input("Enter mode (encode/decode): ").strip().lower()

    if mode == "encode":
        text = input("Enter text to encode: ").strip()
        size = calculate_qr_size(len(text))
        qr_matrix = encode_to_qr(text, size)
        qr_image = generate_qr_image(qr_matrix)
        file_path = "custom_qr_code.png"
        qr_image.save(file_path)
        file_size = os.path.getsize(file_path)
        formatted_file_size = format_file_size(file_size)
        print("QR code generated and saved as custom_qr_code.png")
        print(f"QR code matrix size: {size}x{size} pixels")
        print(f"Generated image size: {qr_image.size[0]}x{qr_image.size[1]} pixels")
        print(f"File size: {formatted_file_size}")

    elif mode == "decode":
        image_path = input("Enter path to QR code image: ").strip()
        qr_matrix = decode_qr_image(image_path)
        text = qr_matrix_to_text(qr_matrix)
        print("Decoded text:", text)

    else:
        print("Invalid mode. Please enter 'encode' or 'decode'.")

if __name__ == "__main__":
    main()