import base64

def binary_to_decimal(binary_str: str) -> int:
    return int(binary_str, 2)

def decimal_to_binary(decimal_num: int) -> str:
    return bin(decimal_num)[2:]

def text_to_ascii_binary(text: str) -> str:
    return ' '.join(format(ord(char), '08b') for char in text)

def ascii_binary_to_text(binary_str: str) -> str:
    chars = binary_str.split()
    return ''.join(chr(int(char, 2)) for char in chars)

def write_text_file(file_path: str, content: str):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def read_text_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return text_to_ascii_binary(content)

def read_image_file(file_path: str) -> str:
    with open(file_path, 'rb') as image_file:
        encoded_data = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_data

def write_image_file(file_path: str, encoded_data: str):
    with open(file_path, 'wb') as image_file:
        image_file.write(base64.b64decode(encoded_data))

if __name__ == "__main__":
    binary = "1010"
    decimal = 10
    text = "Hello World"
    text_file = "assets/Txt_File.txt"
    output_file = "assets/output.txt"
    image_file = "assets/Img_File.bmp"
    restored_image_file = "assets/restored.jpg"

    print(f"{binary} (二進位) -> {binary_to_decimal(binary)} (十進位)")
    print(f"{decimal} (十進位) -> {decimal_to_binary(decimal)} (二進位)")
    print(f"文字轉 ASCII 二進位: {text_to_ascii_binary(text)}")
    ascii_binary = text_to_ascii_binary(text)
    print(f"ASCII 二進位轉回文字: {ascii_binary_to_text(ascii_binary)}")
    print(f"讀取文字檔並轉換: {read_text_file(text_file)[:50]}...")
    decoded_text = ascii_binary_to_text(read_text_file(text_file))
    print(f"decoded_text:\n{decoded_text}")
    write_text_file(output_file, decoded_text)
    print(f"已將 ASCII 二進位轉換的文字寫入 {output_file}")
    encoded_image = read_image_file(image_file)
    print(f"讀取圖片檔並轉換: {encoded_image[:50]}...")
    write_image_file(restored_image_file, encoded_image)
    print(f"已將 Base64 二進位轉換回圖片並存為 {restored_image_file}")
    