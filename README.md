# QRCodeV2
A new generation of QR Codes capable of transferring more data in a smaller image.

> [!WARNING]
> **Alpha Version**: This code is highly unoptimized. Avoid inputting large data as it may cause disk issues or OS crashes. **Expect significant changes in future updates.**

---

## 🚩 Known Issues
- **Custom geometrical shapes and colors for data types**: 
  The feature that uses geometrical shapes (e.g., square, triangle, circle) with specific colors to indicate data types (e.g., link, code, text) is not working correctly.
  - [ ] Links
  - [ ] Code
  - [ ] Text

- **After decode, spaces are not displayed correctly**:  
  The spaces in the decoded string are not displayed correctly, making it difficult to read the output.

~~- **Excessive white pixels**:~~  
  ~~Many pixels that should be filled are incorrectly left white, leading to inefficient QR codes.~~

~~- **Incorrect image scaling**:~~  
  ~~The automatic pixel size determination, which adjusts based on input data size, sometimes fails and produces excessively large images (e.g., 10,000 x 10,000 pixels for a 10-word input).~~

~~- **Large file sizes**:~~
  ~~Rarely, the generated QR code files can become extremely large (e.g., 33GB), causing Windows to crash when attempting to save. This bug is rare but critical when it occurs.~~

---

## 🛠️ How to Use
1. Run `main.py` and follow the prompts.
   - Choose the `encode` option.
     - Enter your string (e.g., `test`) and press Enter.
     - The QR code will be saved as `custom_qr_code.png` in the same directory as `main.py`.
   - Chose the `decode` option to read the QR code
     - After that enter the path of the QR code image and press Enter.
     - The decoded string will be displayed on the console (Or if custom, predefined data it will execute an operation eg. open a link).
2. **Note**: Currently, only English letters, numbers, and specific special characters are supported.

---

## 🤝 Contributing
If you encounter any issues, please report them on GitHub. I’ll address them as soon as possible.

---

### 🏷️ Current Version
- **Code**: 1.1 (Alpha)
- **Python**: 3.12.2 (64-bit)
- **Release Date**: 2024-12-04
- **Required Packages**: `numpy`, `pillow`
