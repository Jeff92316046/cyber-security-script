def diffie_hellman_key_exchange(p, g, a, b):
    A_pub = pow(g, a, p)
    B_pub = pow(g, b, p)
    
    shared_key_A = pow(B_pub, a, p)
    shared_key_B = pow(A_pub, b, p)
    
    assert shared_key_A == shared_key_B, "Shared keys do not match!"
    return shared_key_A

def encrypt_decrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        data = f.read()

    # 簡單的 XOR 加密
    encrypted_data = bytes([b ^ (key % 256) for b in data])

    with open(output_file, 'wb') as f:
        f.write(encrypted_data)

    print(f"已使用 key={key} 對 {input_file} 加密/解密，輸出檔案：{output_file}")

if __name__ == "__main__":
    # D-H public values
    mod = 23
    base = 17
    a = 11  # A's private key
    b = 7  # B's private key

    key = diffie_hellman_key_exchange(mod, base, a, b)
    print(f"共享金鑰 (Shared Key): {key}")

    # 測試加密和解密
    encrypt_decrypt_file("assets/Txt_File.txt", "encrypted.txt", key)
    encrypt_decrypt_file("assets/encrypted.txt", "decrypted.txt", key)
