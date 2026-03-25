import hashlib
import random
import string

def menu():
    print("\n--- Password Manager ---")
    print("1. Add Password")
    print("2. View Passwords")
    print("3. Search Password")
    print("4. Delete Password")
    print("5. Exit")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_password():
    length = 12
    char = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(char) for _ in range(length))
    print(f"Generated password: {password}")
    return password
    

def login():
    master_hash = hash_password("admin123")
    attempt = input("Enter master password: ")

    if hash_password(attempt) != master_hash:
        print("Incorrect password. Access denied.")
        return False
    return True

def add_password():
    website = input("Enter website: ")
    username = input("Enter username: ")
    choice = input("Generate password? (y/n): ")

    if choice == "y":
        password = generate_password()
    else:
        password = input("Enter password: ")

    with open("passwords.txt", "a") as file:
        file.write(f"Website: {website} | Username: {username} | Password: {password}\n")
    print("Password has been saved.")

def view_passwords():
    try:
        with open("passwords.txt", "r") as file:
            lines = file.readlines()

            if not lines:
                print("\n No passwords saved currently.\n")
            else:
                print("\n--- Saved Passwords ---")
                for line in lines:
                    print(line.strip())
    except FileNotFoundError:
        print("\n No passwords saved currently.\n")

def search_password():
    search = input("Enter website to search: ")

    try:
        with open("passwords.txt", "r") as file:
            found = False
            for line in file:
                if search.lower() in line.lower():
                    print(line.strip())
                    found = True
            if not found:
                print("No matching results.")

    except FileNotFoundError:
        print("No passwords saved currently.")

def delete_password():
    website = input("Enter website to delete: ")

    try: 
        with open("passwords.txt", "r") as file:
            lines = file.readlines()

        with open("passwords.txt", "w") as file:
            found = False
            for line in lines:
                if website.lower() not in line.lower():
                    file.write(line)
                else:
                    found = True
        
        if found:
            print("Password deleted.")
        else:
            print("Website not found.")
    
    except FileNotFoundError:
        print("No passwords saved currently.")

def main():
    while True:
        menu()
        choice = input("Choose an option: ")

        if choice == "1":
            add_password()
        elif choice == "2":
            view_passwords()
        elif choice == "3":
            search_password()
        elif choice == "4":
            delete_password()
        elif choice == "5":
            print("Goodbye!")
            break
        else: 
            print("Invalid choice.")

if __name__ == "__main__":
    if login():
        main()