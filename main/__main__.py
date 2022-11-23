import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

import base64
import getpass


def derive_salt(salt):
    return bytes(salt, 'utf-8')


def derive_key(password, salt):
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())


def generate_key(password, salt):
    derived_salt = derive_salt(salt)
    derived_key = derive_key(password, derived_salt)
    return base64.urlsafe_b64encode(derived_key)


def encrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)
    print("File encrypted successfully")


def decrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    try:
        decrypted_data = f.decrypt(encrypted_data)
    except cryptography.fernet.InvalidToken:
        print("Invalid token, most likely the password is incorrect")
        return
    with open(filename, "wb") as file:
        file.write(decrypted_data)
    print("File decrypted successfully")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="File Encryptor Script with a Password")
    parser.add_argument("file", help="File to encrypt/decrypt")
    parser.add_argument("-e", "--encrypt", action="store_true",
                        help="Whether to encrypt the file, only -e or -d can be specified.")
    parser.add_argument("-d", "--decrypt", action="store_true",
                        help="Whether to decrypt the file, only -e or -d can be specified.")

    args = parser.parse_args()
    file = args.file

    if args.encrypt:
        salt = getpass.getpass("Enter the salt for encryption: ")
        password = getpass.getpass("Enter the password for encryption: ")
    elif args.decrypt:
        salt = getpass.getpass(
            "Enter the salt you used for encryption: ")
        password = getpass.getpass(
            "Enter the password you used for encryption: ")

    key = generate_key(password, salt)

    encrypt_ = args.encrypt
    decrypt_ = args.decrypt

    if encrypt_ and decrypt_:
        raise TypeError(
            "Please specify whether you want to encrypt the file or decrypt it.")
    elif encrypt_:
        encrypt(file, key)
    elif decrypt_:
        decrypt(file, key)
    else:
        raise TypeError(
            "Please specify whether you want to encrypt the file or decrypt it.")
