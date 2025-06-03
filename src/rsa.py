import os
from math import gcd

def mod_pow(base, exponent, mod):
    result = 1
    base %= mod
    while exponent > 0:
        if exponent % 2 == 1:
            result = result * base % mod
        base = base * base % mod
        exponent //= 2
    return result

def mod_inverse(e, phi):
    def egcd(a, b):
        if b == 0:
            return a, 1, 0
        g, y, x = egcd(b, a % b)
        return g, x, y - (a // b) * x
    g, x, _ = egcd(e, phi)
    if g != 1:
        raise ValueError("e and phi are not coprime")
    return x % phi

def encrypt_bytes(data, e, n):
    return [mod_pow(b, e, n) for b in data]

def decrypt_bytes(data, d, n):
    return [mod_pow(b, d, n) for b in data]

def handle_text_mode(file_path, e, d, n):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # bytes_data = list(chr(25).encode('utf-8'))
    bytes_data = list(content.encode('utf-8'))
    enc = encrypt_bytes(bytes_data, e, n)
    enc_path = file_path + '.enc'
    with open(enc_path, 'w') as f:
        f.write(' '.join(map(str, enc)))
    print(f'[Text] 已加密: {enc_path}')

    with open(enc_path, 'r') as f:
        encrypted = list(map(int, f.read().strip().split()))
    # encrypted = [95,155]
    dec = decrypt_bytes(encrypted, d, n)
    print(f'[Text] 解密結果: {dec}')
    dec_path = file_path + '.dec.txt'
    with open(dec_path, 'w', encoding='utf-8') as f:
        f.write(bytes(dec).decode('utf-8'))
    print(f'[Text] 已解密: {dec_path}')

def handle_fig_mode(file_path, e, d, n):
    with open(file_path, 'rb') as f:
        data = list(f.read())

    if max(data) >= n:
        raise ValueError(f"圖片中有位元組值 >= n={n}，請選擇更大質數")

    enc = encrypt_bytes(data, e, n)
    enc_path = file_path + '.enc'
    with open(enc_path, 'w') as f:
        f.write(' '.join(map(str, enc)))
    print(f'[Fig] 已加密: {enc_path}')

    with open(enc_path, 'r') as f:
        encrypted = list(map(int, f.read().strip().split()))
    dec = decrypt_bytes(encrypted, d, n)
    dec_path = file_path + '.dec' + os.path.splitext(file_path)[1]
    with open(dec_path, 'wb') as f:
        f.write(bytes(dec))
    print(f'[Fig] 已解密: {dec_path}')

def rsa_tool(p, q, e, mode:str, filepath):
    n = p * q
    phi = (p - 1) * (q - 1)
    print(f'[RSA] n={n}, φ(n)={phi}, e={e}')
    if gcd(e, phi) != 1:
        raise ValueError("e 與 φ(n) 必須互質")
    d = mod_inverse(e, phi) 
    print(f'[RSA] d={d} 已成功計算')

    if mode.lower() == 'text':
        handle_text_mode(filepath, e, d, n)
    elif mode.lower() == 'fig':
        handle_fig_mode(filepath, e, d, n)
    else:
        raise ValueError("模式錯誤，請選擇 'Text' 或 'Fig'")

if __name__ == '__main__':
    p = 13
    q = 19
    e = 7
    mode = 'text'
    file_path = 'Txt_File.txt'
    # mode = 'fig'
    # file_path = 'Img_File.bmp
    rsa_tool(p, q, e, mode, file_path)
    # 最小私鑰是 (n, d)
    # 最大公鑰是 (n, e)
