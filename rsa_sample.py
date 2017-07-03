import random
from enum import Enum

class Error(Enum):
  invalidPrime = '\n ERROR: Not a prime number \n'


#Using the Euclidean Algorithm to find the Greastest Common Denominator
def gcd(a=1, b=1):
    if a < b:
        a, b = b, a
    if b == 0:
        return a
    else:
        # print(a % b)
        return gcd(b, (a % b))


#Extended Euclidean Algorithm
def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)


# Returns the multiplicative inverse if it exist
def multiplicative_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

# Generates possible prime numbers
def candidate(n=100000000):
    a = []
    # creates a range from 0 to 100
    for i in range(100):
        x = random.randint(n, (10 * n))
        if (x % 2) != 0 and (x % 3) != 0 and (x % 5) != 0 and (x % 7) != 0 and (x % 11) != 0:
            a.append(x)
    return a



def get_prime_nums():
    primeOne = 0
    primeTwo = 0

    # This is an infinte loop until the number given is prime
    while True:
        primeOne = int(input("Enter the first prime number: "))
        if (is_prime(primeOne)):
            break

        print(Error.invalidPrime.value)

    while True:
        primeTwo = int(input("Enter the second prime number: "))
        if (is_prime(primeTwo)):
            break

        print(Error.invalidPrime.value)

    return (primeOne, primeTwo)



# Checks for a number being prime and returns a boolean
def is_prime(num):
    # First check for 2 b/c it's prime
    if num == 2:
        return True
    # Exclude numbers less than 2 and numbers who give a remainder if divided by 2
    if num < 2 or num % 2 == 0:
        return False
    # Loop the numbers from 3 to sqrt(num)
    for n in range(3, int(num**0.5)+2, 2):
        # Check if the modular returns 0
        if num % n == 0:
            return False
    return True


# Generates the public and private key paris for encrypt and decrypt
def generate_keypair(a,b):

    p = a
    q = b

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


# Use the public key to encrypt our messagee
def encrypt(pk, plaintext):
    key, n = pk
    # ord() returns the unicode representation of the character
    cipher = [pow(ord(char), key, n) for char in plaintext]

    return cipher


# Use the private key to decrypt message
def decrypt(pk, ciphertext):
    key, n = pk
    # chr returns the string representing a character represented by Unicode
    plain = [chr(pow(char, key, n)) for char in ciphertext]
    return ''.join(plain)



if __name__ == '__main__':
    print("\nRSA encryption system\n")
    primeOne, primeTwo = get_prime_nums()
    print("\nEstablishing public and private keys... ")
    public, private = generate_keypair(primeOne, primeTwo)
    print("Your public key is ", public ," and your private key is ", private)
    message = input("\nEnter a message to be encrypted: ")
    encrypted_msg = encrypt(public, message)
    print("Your encrypted message is: ")
    print(''.join(map(lambda x: str(x), encrypted_msg)))
    print("\nUsing private key ", private ," to decrypt . . .")
    print("Your message is:")
    print(decrypt(private, encrypted_msg))
