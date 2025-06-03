from sympy import isprime, factorint

def prime_factorization(n: int):
    if n < 2:
        print("請輸入大於 1 的整數")
        return

    print(f"輸入的數字：{n}")
    print(f"是否為質數：{isprime(n)}")

    factors = factorint(n)
    print("質因數分解結果：")
    for prime, exponent in factors.items():
        if exponent == 1:
            print(f"{prime}")
        else:
            print(f"{prime}^{exponent}")

# 範例
number = int(input("請輸入一個整數："))
prime_factorization(number)
