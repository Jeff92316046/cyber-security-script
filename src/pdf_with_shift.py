from typing import Any
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from PIL import Image

plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]
plt.rcParams["axes.unicode_minus"] = False


def read_text_as_binary(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    ascii_values = [ord(char) for char in text]
    binary_values = [format(value, "08b") for value in ascii_values]
    return ascii_values, binary_values


def read_image_as_binary(file_path):
    image = Image.open(file_path)
    pixels = np.array(image).flatten()
    return [format(value, "08b") for value in pixels]


def shift_binary_values(data, shift_amount=15, mod_value=256):
    shifted_data = []
    for binary_str in data:
        decimal_value = int(binary_str, 2)
        shifted_value = (decimal_value + shift_amount) % mod_value
        shifted_binary = format(shifted_value, "08b")
        shifted_data.append(shifted_binary)
    return shifted_data


def compute_probability_distribution(data, binary_mode=False):
    count = Counter(data)
    sorted_items = sorted(
        count.items(), key=lambda x: int(x[0], 2) if binary_mode else x[0]
    )
    total = sum(count.values())

    prob_distribution = {
        (key if binary_mode else int(key, 2)): value / total
        for key, value in sorted_items
    }

    nonzero_probs = np.array(list(prob_distribution.values()))
    information_values = -np.log2(nonzero_probs)
    information_total = np.sum(information_values)
    entropy = np.sum(nonzero_probs * information_values)

    return prob_distribution, information_total, entropy


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
(
    text_prob_distribution_original,
    text_information_total_original,
    text_entropy_original,
) = compute_probability_distribution(binary_values)
shifted_text_values = shift_binary_values(binary_values)
text_prob_distribution_shifted, text_information_total_shifted, text_entropy_shifted = (
    compute_probability_distribution(shifted_text_values)
)

print(
    f"Text Shannon Entropy (Original): {text_entropy_original:.4f}\nText Information Total (Original): {text_information_total_original:.4f}"
)
print(
    f"Text Shannon Entropy (Shifted): {text_entropy_shifted:.4f}\nText Information Total (Shifted): {text_information_total_shifted:.4f}"
)

fig, axs = plt.subplots(1, 2, figsize=(12, 6))
plot_probability_distribution(
    text_prob_distribution_original,
    axs[0],
    "Original Text ASCII Probability Distribution",
)
plot_probability_distribution(
    text_prob_distribution_shifted,
    axs[1],
    "Shifted Text ASCII Probability Distribution",
)
plt.tight_layout()
plt.show()

image_data = read_image_as_binary(image_file)
(
    image_prob_distribution_original,
    image_information_total_original,
    image_entropy_original,
) = compute_probability_distribution(image_data)
shifted_image_values = shift_binary_values(image_data)
(
    image_prob_distribution_shifted,
    image_information_total_shifted,
    image_entropy_shifted,
) = compute_probability_distribution(shifted_image_values)

print(
    f"Image Shannon Entropy (Original): {image_entropy_original:.4f}\nImage Information Total (Original): {image_information_total_original:.4f}"
)
print(
    f"Image Shannon Entropy (Shifted): {image_entropy_shifted:.4f}\nImage Information Total (Shifted): {image_information_total_shifted:.4f}"
)

fig, axs = plt.subplots(1, 2, figsize=(12, 6))
plot_probability_distribution(
    image_prob_distribution_original,
    axs[0],
    "Original Image Binary Probability Distribution",
)
plot_probability_distribution(
    image_prob_distribution_shifted,
    axs[1],
    "Shifted Image Binary Probability Distribution",
)
plt.tight_layout()
plt.show()
