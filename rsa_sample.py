import random


def gcd(a=1, b=1):
    if a < b:
        a, b = b, a
    if b == 0:
        return a
    else:
        # print(a % b)
        return gcd(b, (a % b))


def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)


def multiplicative_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def candidate(n=100000000):
    a = []
    for i in range(100):
        x = random.randint(n, (10 * n))
        if (x % 2) != 0 and (x % 3) != 0 and (x % 5) != 0 and (x % 7) != 0 and (x % 11) != 0:
            a.append(x)
    return a

def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True


def generate_keypair():

    prime_numbers = candidate()
    p = 0
    q = 0

    for x in prime_numbers:
        if is_prime(x) and p == 0:
            p = x
        elif is_prime(x) and q == 0:
            q = x
            break

    if not (is_prime(p) and is_prime(q)):
        raise ValueError('One or more numbers is not prime')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    n = p * q

    phi = (p-1) * (q-1)

    e = random.randrange(1, phi)

    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = multiplicative_inverse(e, phi)
    
    return ((e, n), (d, n))


def encrypt(pk, plaintext):
    key, n = pk
    cipher = [pow(ord(char), key, n) for char in plaintext]

    return cipher


def decrypt(pk, ciphertext):
    key, n = pk
    plain = [chr(pow(char, key, n)) for char in ciphertext]
    return ''.join(plain)
    


if __name__ == '__main__':
    print("RSA encryption system")
    print("Establishing public and private keys. ")
    public, private = generate_keypair()
    print("Your public key is ", public ," and your private key is ", private)
    message = input("Enter a message to be encrypted: ")
    encrypted_msg = encrypt(public, message)
    print("Your encrypted message is: ")
    print(''.join(map(lambda x: str(x), encrypted_msg)))
    print("Using private key ", private ," to decrypt . . .")
    print("Your message is:")
    print(decrypt(private, encrypted_msg))
