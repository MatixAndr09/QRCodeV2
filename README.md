# QRCodeV2
A new generation of QR Codes capable of transferring more data in a smaller image.

[//]: # (> [!WARNING])

[//]: # (> **Alpha Version**: This code is highly unoptimized. Avoid inputting large data as it may cause disk issues or OS crashes. **Expect significant changes in future updates.**)

---

## 🚩 Known Issues
- **Custom geometrical shapes and colors for data types**: 
  The feature that uses geometrical shapes (e.g., square, triangle, circle) with specific colors to indicate data types (e.g., link, code, text) is not working correctly.
  - [ ] Links
  - [ ] Code
  - [ ] Text

- **After decode, spaces are not displayed correctly**:  
  The spaces in the decoded string are not displayed correctly, making it difficult to read the output.

[//]: # (---)

[//]: # ()
[//]: # (## Future Updates)

[//]: # ()
[//]: # (~~- **Remove imghdr dependency**:  )

[//]: # (  The `imghdr` will be removed in Python 3.13 so it will be replaced with a custom function made by me.~~)

---

## 🛠️ How to Use
1. Run `main.py` and follow the prompts.
   - Choose the `encode` option.
     - Enter your string (e.g., `test`) and press Enter.
     - The QR code will be saved as `custom_qr_code.png` in the directory called `output`.
   - Chose the `decode` option to read the QR code
     - After that enter the path of the QR code image and press Enter.
     - The decoded string will be displayed on the console (Or if custom, predefined data it will execute an operation eg. open a link).
     - **Note**: The QR code must be in the `output` directory.
2. **Note**: Currently, only English letters, numbers, and specific special characters are supported.
3. **Note**: All logs are saved in `logs` directory.

---

## 🤝 Contributing
If you encounter any issues, please report them on GitHub. I’ll address them as soon as possible. If you’d like to contribute, please fork the repository and make a pull request.

---

### 🏷️ Current Version
- **Code**:  0.1.0 Pre-Release
- **Python**: 3.12.2, 3.12.6 (64-bit)
- **Last Update Date**: 07.12.2024
- **Required Packages**: in `requirements`
