import base64

def binary_to_decimal(binary_str: str) -> int:
    return int(binary_str, 2)

def decimal_to_binary(decimal_num: int) -> str:
    return bin(decimal_num)[2:]

if __name__ == "__main__":
    binary = "1011"
    decimal = 1013123

    print(f"{binary} (二進位) -> {binary_to_decimal(binary)} (十進位)")
    print(f"{decimal} (十進位) -> {decimal_to_binary(decimal)} (二進位)")