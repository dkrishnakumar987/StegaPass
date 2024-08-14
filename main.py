import json
import os
from getpass import getpass

import encryption as enc
import steganography as steg

UsrDataFile = "services.json"
UsrDataDir = "user_data"
InputDir = "ImageStorage/OriginalImages/"
OutputDir = "ImageStorage/SteganoImages/"


def load_user_data(username: str):
    """Load user data from JSON file."""
    usr_data_file = os.path.join(UsrDataDir, username, UsrDataFile)
    if not os.path.exists(usr_data_file):
        return {}
    with open(usr_data_file, "r") as f:
        return json.load(f)


def save_user_data(username: str, data: dict):
    """Save user data to JSON file."""
    usr_data_file = os.path.join(UsrDataDir, username, UsrDataFile)
    with open(usr_data_file, "w") as f:
        json.dump(data, f, indent=4)


def register_user(username: str, password: str):
    """Register a new user and create an encryption key."""
    user_dir = os.path.join(UsrDataDir, username)
    key_file = os.path.join(user_dir, "encryption_key.bin")
    if os.path.exists(user_dir):
        print("User already exists.")
        return None

    image_dir = os.path.join(user_dir, "ImageStorage")
    os.makedirs(os.path.join(image_dir, "OriginalImages"))
    os.makedirs(os.path.join(image_dir, "SteganoImages"))
    key = enc.gen_key(password)
    with open(key_file, "wb") as f:
        f.write(key)
    print(f"User {username} registered.")
    return key


def login_user(username: str, password: str):
    """Authenticate an existing user and load their encryption key."""
    user_dir = os.path.join(UsrDataDir, username)
    key_file = os.path.join(user_dir, "encryption_key.bin")
    if not os.path.exists(key_file):
        print("User does not exist.")
        return None

    stored_key = enc.load_key(key_file)
    if enc.verify_key(password, stored_key):
        print(f"User {username} logged in.")
        return enc.extract_key(stored_key)
    else:
        print("Incorrect password.")
        return None


def add_password(username: str, service: str, password: str, key: bytes, img_name: str):
    """Add a new password for a specific user."""
    user_data = load_user_data(username)
    user_services = user_data.get(username, {})

    ciphertext, nonce, tag = enc.encrypt_pwd(password, key)
    encrypted_data = enc.add_data(ciphertext, nonce, tag)
    img_inp_path = os.path.join(UsrDataDir, username, InputDir, f"{img_name}.png")
    img_out_path = os.path.join(UsrDataDir, username, OutputDir, f"{img_name}.png")
    steg.encode_img(img_inp_path, encrypted_data, img_out_path)

    user_services[service] = {"image_path": img_out_path}

    user_data[username] = user_services
    save_user_data(username, user_data)
    print(f"Password for {service} added for user {username}.")


def get_password(username: str, service: str, key: bytes):
    """Retrieve a password for a specific user."""
    user_data = load_user_data(username)
    user_services = user_data.get(username, {})
    service_data = user_services.get(service)

    if not service_data:
        print(f"Service {service} not found for user {username}.")
        return

    image_path = service_data["image_path"]
    encrypted_data = steg.decode_img(image_path)
    cipher, nonce, tag = enc.separate_data(encrypted_data, enc.nonce_len, enc.tag_len)
    decrypted_pwd = enc.decrypt_pwd(cipher, nonce, tag, key)
    return decrypted_pwd


def main_menu():
    """Display the main menu and handle user input."""
    while True:
        print("\nMain Menu")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            username = input("Enter a new username: ").strip()
            password = getpass("Enter a master password: ").strip()
            register_user(username, password)
        elif choice == "2":
            username = input("Enter your username: ").strip()
            password = getpass("Enter your master password: ").strip()
            key = login_user(username, password)
            if key:
                user_sub_menu(username, key)
        elif choice == "3":
            break
        else:
            print("Invalid option. Please choose again.")


def user_sub_menu(username, key):
    """Display the user sub-menu after login."""
    while True:
        print(f"\nUser Menu - {username}")
        print("1. Add Service")
        print("2. Get Password")
        print("3. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            service = input("Enter service name: ").strip()
            password = getpass("Enter password: ").strip()
            img_name = input("Enter image name: ").strip()
            add_password(username, service, password, key, img_name)
        elif choice == "2":
            service = input("Enter service name: ").strip()
            get_password(username, service, key)
        elif choice == "3":
            break
        else:
            print("Invalid option. Please choose again.")


if __name__ == "__main__":
    main_menu()
