# modules/textToBinary.py
def text_to_binary(text):
    return [format(ord(char), '08b') for char in text]