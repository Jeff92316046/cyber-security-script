from typing import Any
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from PIL import Image

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

def read_text_as_binary(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    ascii_values = [ord(char) for char in text]  # 轉成 ASCII
    binary_values = [format(value, "08b") for value in ascii_values]  # 轉成二進制
    return ascii_values, binary_values

def read_image_as_binary(file_path):
    image = Image.open(file_path)

    binary_list = []

    if getattr(image, "is_animated", False):  # 是 GIF 多幀動畫
        for frame in range(image.n_frames):
            image.seek(frame)
            gray = image.convert("L")
            pixels = np.array(gray).flatten()
            binary_list.extend([format(value, "08b") for value in pixels])
            plt.imshow(np.array(gray), cmap="gray")
            plt.title(f"Frame {frame}")
            plt.axis("off")
            plt.show()
    else:  # 一般圖片
        pixels = np.array(image.convert("L")).flatten()
        binary_list = [format(value, "08b") for value in pixels]
    return binary_list

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

def plot_probability_distribution(prob_distribution:dict[Any | int, float], title="Probability Distribution"):
    probs = [prob_distribution.get(i, 0) for i in range(256)]
    plt.figure(figsize=(12, 6))
    plt.bar(range(256), probs, color="skyblue", width=1.0)
    plt.xlabel("Value")
    plt.ylabel("Probability")
    plt.title(title)
    plt.xticks(range(0, 256, 25))
    plt.xlim(0, 255)
    plt.show()

text_file = "assets/output.txt"
image_file = "assets/nyamuchi_gray.gif"

# ascii_values, binary_values = read_text_as_binary(text_file)
# text_prob_distribution,text_information_total, text_entropy = compute_probability_distribution(binary_values)
# print(f"Text Shannon Entropy: {text_entropy:.4f}\nText Information Total: {text_information_total:.4f}")
# plot_probability_distribution(text_prob_distribution, title="Text ASCII Probability Distribution")

image_data = read_image_as_binary(image_file)
image_prob_distribution,image_information_total, image_entropy = compute_probability_distribution(image_data)
print(image_prob_distribution[150])
print(image_prob_distribution[200])
print(f"Image Shannon Entropy: {image_entropy:.4f}\nImage Information Total: {image_information_total:.4f}")
plot_probability_distribution(image_prob_distribution, title="Image Binary Probability Distribution")
