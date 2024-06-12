def prime_checker(p):
    if p < 1:
        return False
    elif p > 1:
        if p == 2:
            return True
        for i in range(2, p):
            if p % i == 0:
                return False
        return True
def primitive_check(g, p, L):
    for i in range(1, p):
        L.append(pow(g, i) % p)
    for i in range(1, p):
        if L.count(i) > 1:
            L.clear()
            return False
    return True
def diffie_hellman():
    l = []
    P = int(input("Enter the value of P: "))
    G = int(input("Enter the value of G: "))
    x1 = int(input("Enter the private key a for Alice: "))
    x2 = int(input("Enter the private key b for Bob: "))
    if not prime_checker(P):
        print("P is not a prime number.")
        return
    if not primitive_check(G, P, l):
        print("G is not a primitive root of P.")
        return
    y1 = pow(G, x1) % P
    y2 = pow(G, x2) % P
    k1 = pow(y2, x1) % P
    k2 = pow(y1, x2) % P
    print(f"\nSecret key for the Alice is: {k1}")
    print(f"Secret Key for the Bob is: {k2}")
    if k1 == k2:
        print("Keys Have Been Exchanged Successfully")
    else:
        print("Keys Have Not Been Exchanged Successfully")
if __name__ == "__main__":
    diffie_hellman()

