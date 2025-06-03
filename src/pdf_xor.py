from typing import Any
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from PIL import Image

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# === 加密相關設定 ===
XOR_KEY_HEX = "a3b2c1d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90"  # 128 hex chars = 512 bytes = 1024 bits
XOR_KEY_BIN = "".join(format(int(h, 16), "04b") for h in XOR_KEY_HEX)  # 轉成 1024 位元二進制

def xor_encrypt(binary_data: list[str], key_bin: str) -> list[str]:
    key_length = len(key_bin)
    flat_bits = "".join(binary_data)[:key_length * (len(binary_data) * 8 // key_length)]
    result = []
    for i in range(0, len(flat_bits), 8):
        byte = flat_bits[i:i+8]
        key_slice = key_bin[(i % key_length):(i % key_length) + 8]
        xor_byte = format(int(byte, 2) ^ int(key_slice, 2), "08b")
        result.append(xor_byte)
    return result

def read_text_as_binary(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    ascii_values = [ord(char) for char in text]  # 轉成 ASCII
    binary_values = [format(value, "08b") for value in ascii_values]  # 轉成二進制
    return ascii_values, binary_values

def read_image_as_binary(file_path):
    image = Image.open(file_path)
    pixels = np.array(image).flatten()
    return [format(value, "08b") for value in pixels]

def compute_probability_distribution(data, binary_mode=False):
    count = Counter(data)
    sorted_items = sorted(count.items(), key=lambda x: int(x[0], 2) if binary_mode else x[0]) 
    total = sum(count.values())
    
    prob_distribution = {
        (key if binary_mode else int(key, 2)): value / total for key, value in sorted_items
    }

    # 計算 Shannon Entropy
    nonzero_probs = np.array(list(prob_distribution.values()))
    information_values = -np.log2(nonzero_probs)
    information_total = np.sum(information_values)
    entropy = np.sum(nonzero_probs * information_values)

    return prob_distribution,information_total, entropy  # 返回機率分佈與 Entropy

def plot_probability_distribution(
    prob_distribution: dict[Any | int, float],
    ax: plt.Axes,
    title="Probability Distribution",
):
    probs = [prob_distribution.get(i, 0) for i in range(256)]
    ax.bar(range(256), probs, color="skyblue", width=1.0)
    ax.set_xlabel("Value")
    ax.set_ylabel("Probability")
    ax.set_title(title)
    ax.set_xticks(range(0, 256, 25))
    ax.set_xlim(0, 255)

text_file = "assets/output.txt"
image_file = "assets/Img_File.bmp"

ascii_values, binary_values = read_text_as_binary(text_file)
text_prob_distribution,text_information_total, text_entropy = compute_probability_distribution(binary_values)
xor_text = xor_encrypt(binary_values, XOR_KEY_BIN)
xor_text_prob_distribution,xor_text_information_total, xor_text_entropy = compute_probability_distribution(xor_text)
print(f"Text Shannon Entropy: {text_entropy:.4f}")
print(f"Text Information Total: {text_information_total:.4f}")
print(f"XOR Text Shannon Entropy: {xor_text_entropy:.4f}")  
print(f"XOR Text Information Total: {xor_text_information_total:.4f}")
print(f"security capacity(Information Total): {xor_text_information_total - text_information_total:.4f}")
print(f"security capacity(Entropy): {xor_text_entropy - text_entropy:.4f}")
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
plot_probability_distribution(
    text_prob_distribution,
    axs[0],
    "Original Text ASCII Probability Distribution",
)
plot_probability_distribution(
    xor_text_prob_distribution,
    axs[1],
    "XOR Text ASCII Probability Distribution",
)
plt.tight_layout()
plt.show()


image_data = read_image_as_binary(image_file)
image_prob_distribution,image_information_total, image_entropy = compute_probability_distribution(image_data)
xor_image_data = xor_encrypt(image_data, XOR_KEY_BIN)
xor_image_prob_distribution,xor_image_information_total, xor_image_entropy = compute_probability_distribution(xor_image_data)
print(f"Image Shannon Entropy: {image_entropy:.4f}")
print(f"Image Information Total: {image_information_total:.4f}")
print(f"XOR Image Shannon Entropy: {xor_image_entropy:.4f}")
print(f"XOR Image Information Total: {xor_image_information_total:.4f}")
print(f"security capacity(Information Total): {xor_image_information_total - image_information_total:.4f}")
print(f"security capacity(Entropy): {xor_image_entropy - image_entropy:.4f}")
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
plot_probability_distribution(
    image_prob_distribution,
    axs[0],
    "Original Text ASCII Probability Distribution",
)
plot_probability_distribution(
    xor_image_prob_distribution,
    axs[1],
    "XOR Text ASCII Probability Distribution",
)
plt.tight_layout()
plt.show()