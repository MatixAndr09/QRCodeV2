# main.py
from modules.textToBinary import text_to_binary
from modules.encoder import encode_to_qr
from modules.decoder import generate_qr_image, decode_qr_image, qr_matrix_to_text
from modules.sizeDetect import calculate_qr_size

def main():
    mode = input("Enter mode (encode/decode): ").strip().lower()

    if mode == "encode":
        text = input("Enter text to encode: ").strip()
        size = calculate_qr_size(len(text))
        qr_matrix = encode_to_qr(text, size)
        qr_image = generate_qr_image(qr_matrix)
        qr_image.save("custom_qr_code.png")
        print("QR code generated and saved as custom_qr_code.png")

    elif mode == "decode":
        image_path = input("Enter path to QR code image: ").strip()
        qr_matrix = decode_qr_image(image_path)
        text = qr_matrix_to_text(qr_matrix)
        print("Decoded text:", text)

    else:
        print("Invalid mode. Please enter 'encode' or 'decode'.")

if __name__ == "__main__":
    main()