import numpy as np
from PIL import Image
import math


def read_image_grayscale(path: str) -> np.ndarray:
    img = Image.open(path).convert("L")
    return np.array(img)


def save_image_grayscale(arr: np.ndarray, path: str):
    Image.fromarray(arr).save(path)


def read_message_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def str_to_bin(s: str) -> str:
    return ''.join(f"{ord(c):08b}" for c in s)


def bin_to_str(b: str) -> str:
    chars = [b[i:i+8] for i in range(0, len(b), 8)]
    return ''.join(chr(int(c, 2)) for c in chars if len(c) == 8)


def embed_message(img_array: np.ndarray, message_bits: str, L: int) -> np.ndarray:
    flat = img_array.flatten()
    max_bits = L * flat.size
    if len(message_bits) > max_bits:
        raise ValueError(f"Message is too long for L={L}. Max bits: {max_bits}, got: {len(message_bits)}")

    message_bits = message_bits.ljust(max_bits, '0')  # 補 0 至可嵌入長度

    for i in range(flat.size):
        bits = message_bits[L*i:L*(i+1)].ljust(L, '0')
        mask = (1 << L) - 1
        flat[i] = (flat[i] & (~mask & 0xFF)) | int(bits, 2)

    return flat.reshape(img_array.shape)


def extract_message(img_array: np.ndarray, L: int, total_bits: int) -> str:
    flat = img_array.flatten()
    bits = ''
    for i in range(flat.size):
        byte = flat[i]
        bits += bin(byte)[-L:].rjust(L, '0')
        if len(bits) >= total_bits:
            break
    return bits[:total_bits]


def calculate_psnr(original: np.ndarray, modified: np.ndarray) -> float:
    mse = np.mean((original.astype(np.float32) - modified.astype(np.float32)) ** 2)
    if mse == 0:
        return float('inf')
    PIXEL_MAX = 255.0
    return 10 * math.log10((PIXEL_MAX ** 2) / mse)


def main():
    image_path = "assets/Img_File.bmp"
    message_path = "assets/Txt_File.txt"

    img_array = read_image_grayscale(image_path)
    message = read_message_file(message_path)
    message_bits = str_to_bin(message)
    total_bits = len(message_bits)

    for L in range(1, 6):
        try:
            stego_array = embed_message(img_array.copy(), message_bits, L)
            extracted_bits = extract_message(stego_array, L, total_bits)
            extracted_message = bin_to_str(extracted_bits)
            psnr = calculate_psnr(img_array, stego_array)
            print(f"L={L} | PSNR={psnr:.4f} dB | Extracted='{extracted_message[:30]}{'...' if len(extracted_message) > 30 else ''}'")

            # 可選：儲存圖片
            save_image_grayscale(stego_array, f"stego_L{L}.png")

        except ValueError as e:
            print(f"L={L} | Error: {e}")


if __name__ == "__main__":
    main()
