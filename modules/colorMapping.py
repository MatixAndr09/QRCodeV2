# modules/colorMapping.py
def char_to_color(char):
    # Generate a unique RGB color for each character
    r = (ord(char) * 37) % 256
    g = (ord(char) * 73) % 256
    b = (ord(char) * 109) % 256
    return (r, g, b)