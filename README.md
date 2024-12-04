# QRCodeV2
A new generation of QR Codes transfer more data in smaller image

## Known Issues

- Custom objects in QR code to determine what is the data saved is not working (eg. link, code, or just text)
- There is a lot of white spaces that are useless (I will fix this in the next version)
- Image scaling don't always work
- Image can be very big (for some reason)

## How to use

Run main.py and there will be encode/decode options. Type encode then type yours string for example `test` and then press enter and the QR code will generate. To see it search for file named `custom_qr_code.png` int the same directory as main.py

## Contributing

If there is any issue please create an issue on github i will try to fix it as soon as possible

### Current version

- Code: 1.0 (Alpha)
- Python: 3.12.2 (64-bit)
- Release Date: 04.12.2024
- Required packages: `numpy`, `pillow`
