import base64
import os
import random
import string
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

PASSWORD_FILE = "passwords.txt"
SALT_FILE = "salt.bin"
CHECK_FILE = "check.bin"

def get_salt():
    if not os.path.exists(SALT_FILE):
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
    else:
        with open(SALT_FILE, "rb") as f:
            salt = f.read()
    return salt

def derive_key(password):
    salt = get_salt()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000,)
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def get_cipher(master_password):
    key = derive_key(master_password)
    return Fernet(key)

def verify_master_password(cipher):
    if not os.path.exists(CHECK_FILE):
        # first time setup master password is "admin123"
        with open(CHECK_FILE, "wb") as f:
            f.write(cipher.encrypt(b"verified"))
        return True
    else:
        try:
            with open(CHECK_FILE, "rb") as f:
                cipher.decrypt(f.read())
            return True
        except:
            return False

def menu():
    print("\n--- Password Manager ---")
    print("1. Add Password")
    print("2. View Passwords")
    print("3. Search Password")
    print("4. Delete Password")
    print("5. Exit")

def generate_password():
    length = 12
    char = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(char) for _ in range(length))
    print(f"Generated password: {password}")
    return password
    

def login():
    return input("Enter master password: ")

def add_password(cipher):
    website = input("Enter website: ")
    username = input("Enter username: ")
    choice = input("Generate password? (y/n): ")

    if choice.lower() == "y":
        password = generate_password()
    else:
        password = input("Enter password: ")

    encrypted = cipher.encrypt(password.encode())

    with open(PASSWORD_FILE, "ab") as file:
        line = f"{website}|{username}|".encode() + encrypted + b"\n"
        file.write(line)

    print("Password has been saved.")

def view_passwords(cipher):
    try:
        with open(PASSWORD_FILE, "rb") as file:
           print("Saved Passwords")
           for line in file:
            parts = line.strip().split(b"|")
            website = parts[0].decode()
            username = parts[1].decode()
            encrypted_password = parts[2]
            
            decrypted = cipher.decrypt(encrypted_password).decode()
            print(f"{website} | {username} | {decrypted}")

    except FileNotFoundError:
        print("There are no passwords saved.")

def search_password(cipher):
    search = input("ENter a website to search: ").lower()

    try:
        with open(PASSWORD_FILE, "rb") as file:
            found = False
            for line in file:
                parts = line.strip().split(b"|")
                website = parts[0].decode()

                if search in website.lower():
                    username = parts[1].decode()
                    decrypted = cipher.decrypt(parts[2]).decode()
                    print(f"{website} | {username} | {decrypted}")
                    found = True

            if not found:
                print("No matching results.")
    except FileNotFoundError:
        print("There are no passwords saved.")

def delete_password(cipher):
    website_delete = input("Enter website to delete: ").lower()
    try:
        with open(PASSWORD_FILE, "rb") as file:
            lines = file.readlines()

        with open(PASSWORD_FILE, "wb") as file:
            found = False
            for line in lines:
                parts = line.strip().split(b"|")
                website = parts[0].decode().lower()

                if website_delete not in website:
                    file.write(line)
                else:
                    found = True
        if found:
            print("Password has been deleted.")
        else:
            print("Website not found.")

    except FileNotFoundError:
        print("There are no passwords saved.")

def main(cipher):
    while True:
        menu()
        choice = input("Choose an option: ")

        if choice == "1":
            add_password(cipher)
        elif choice == "2":
            view_passwords(cipher)
        elif choice == "3":
            search_password(cipher)
        elif choice == "4":
            delete_password(cipher)
        elif choice == "5":
            print("Goodbye!")
            break
        else: 
            print("Invalid choice.")

if __name__ == "__main__":
    master_password = login()
    cipher = get_cipher(master_password)
    
    if verify_master_password(cipher):
        main(cipher)
    else:
        print("Incorrect master password.")
