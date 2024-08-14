import os
import shutil
from tkinter import filedialog

import customtkinter as ctk
import pyperclip

from main import UsrDataDir, add_password, get_password, login_user, register_user

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class PasswordManager(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Main Menu")
        self.geometry("400x300")

        self.main_menu()

    def main_menu(self):
        """
        Displays the main menu of the application, providing options to add a user, login, or exit.
        """
        self.clear_window()
        ctk.CTkLabel(self, text="Main Menu", font=("Arial", 20)).pack(pady=10)

        ctk.CTkButton(self, text="Add User", command=self.register).pack(pady=5)
        ctk.CTkButton(self, text="Login", command=self.login).pack(pady=5)
        ctk.CTkButton(self, text="Exit", command=self.destroy).pack(pady=5)

    def register(self):
        """
        Displays the registration menu of the application, allowing users to input a new username and master password.
        """
        self.clear_window()
        self.title("Register")

        ctk.CTkLabel(self, text="Enter a new username: ", font=("Arial", 20)).pack(
            pady=10
        )
        username_field = ctk.CTkEntry(self)
        username_field.pack(pady=5)

        ctk.CTkLabel(self, text="Enter a master password: ", font=("Arial", 20)).pack(
            pady=10
        )
        password_field = ctk.CTkEntry(self, show="*")
        password_field.pack(pady=5)

        def on_register_pressed():
            username = username_field.get()
            master_password = password_field.get()
            if username and master_password:
                register_user(username.strip(), master_password.strip())
                username_field.delete(0, "end")
                password_field.delete(0, "end")
                self.return_to_main_menu()

        ctk.CTkButton(self, text="Register", command=on_register_pressed).pack(pady=5)
        ctk.CTkButton(self, text="Back", command=self.main_menu).pack(pady=5)

    def login(self):
        """
        Displays the login menu, checks user credentials, and navigates to the user's sub-menu if valid.
        """
        self.clear_window()
        self.title("Login")

        ctk.CTkLabel(self, text="Enter your username", font=("Arial", 20)).pack(pady=10)
        username_field = ctk.CTkEntry(self)
        username_field.pack(pady=5)

        ctk.CTkLabel(self, text="Enter a master password: ", font=("Arial", 20)).pack(
            pady=10
        )
        password_field = ctk.CTkEntry(self, show="*")
        password_field.pack(pady=5)

        def on_login_pressed():
            username = username_field.get()
            master_password = password_field.get()
            if username and master_password:
                key = login_user(username.strip(), master_password.strip())
                if key:
                    self.user_sub_menu(username, key)
                else:
                    ctk.CTkLabel(self, text="Invalid username or password").pack()
                    username_field.delete(0, "end")
                    password_field.delete(0, "end")
            else:
                ctk.CTkLabel(self, text="Please enter a username and password").pack()

        ctk.CTkButton(self, text="Login", command=on_login_pressed).pack(pady=5)
        ctk.CTkButton(self, text="Back", command=self.main_menu).pack(pady=5)

    def user_sub_menu(self, username, key):
        """
        Displays the user sub-menu after a successful login.

        Parameters:
        username (str): The username of the logged-in user.
        key (bytes): The key used for encryption and decryption.
        """
        self.clear_window()
        self.title(f"User Menu - {username}")

        ctk.CTkLabel(self, text=f"User Menu - {username}", font=("Arial", 20)).pack(
            pady=10
        )

        ctk.CTkButton(
            self, text="Add Service", command=lambda: self.add_service(username, key)
        ).pack(pady=5)
        ctk.CTkButton(
            self, text="Get Password", command=lambda: self.get_password(username, key)
        ).pack(pady=5)

        def browse_and_copy_image(self):
            file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
            if file_path:
                target_dir = os.path.join(
                    UsrDataDir, username, "ImageStorage", "OriginalImages"
                )
                os.makedirs(target_dir, exist_ok=True)
                shutil.copy(file_path, target_dir)
                print(f"File copied to {target_dir}")
                self.clear_window()
                ctk.CTkLabel(self, text="Image copied successfully").pack(pady=10)
                ctk.CTkButton(
                    self, text="OK", command=lambda: self.user_sub_menu(username, key)
                ).pack(pady=5)

        ctk.CTkButton(
            self, text="Add Image", command=lambda: browse_and_copy_image(self)
        ).pack(pady=5)

        ctk.CTkButton(self, text="Logout", command=self.main_menu).pack(pady=5)

    def add_service(self, username, key):
        """
        Displays the add service menu, allowing users to input service name, password, and image name.
        
        Parameters:
        username (str): The username of the logged-in user.
        key (bytes): The key used for encryption and decryption.
        """
        self.clear_window()
        self.title("Add Service")

        ctk.CTkLabel(self, text="Enter service name:", font=("Arial", 20)).pack(pady=10)
        service_field = ctk.CTkEntry(self)
        service_field.pack(pady=5)

        ctk.CTkLabel(self, text="Enter password:", font=("Arial", 20)).pack(pady=10)
        password_field = ctk.CTkEntry(self, show="*")
        password_field.pack(pady=5)

        ctk.CTkLabel(self, text="Enter image name:", font=("Arial", 20)).pack(pady=10)
        img_name_field = ctk.CTkEntry(self)
        img_name_field.pack(pady=5)

        def on_submit_pressed():
            service = service_field.get().strip()
            password = password_field.get().strip()
            img_name = img_name_field.get().strip()

            if service and password and img_name:
                try:
                    self.clear_window()
                    add_password(username, service, password, key, img_name)
                    ctk.CTkLabel(self, text="Service added successfully").pack(pady=10)
                    ctk.CTkButton(
                        self,
                        text="OK",
                        command=lambda: self.user_sub_menu(username, key),
                    ).pack(pady=5)
                except Exception as e:
                    print(str(e))
                    ctk.CTkLabel(
                        self,
                        text=f"Image {img_name}.png does not exist in /ImageStorage/OriginalImages/",
                    ).pack(pady=10)
                    ctk.CTkButton(
                        self,
                        text="OK",
                        command=lambda: self.user_sub_menu(username, key),
                    ).pack(pady=5)
            else:
                ctk.CTkLabel(self, text="Please fill in all fields").pack()

        ctk.CTkButton(self, text="Submit", command=on_submit_pressed).pack(pady=20)

    def get_password(self, username, key):
        """
        Retrieves a password for a specific service associated with the given username.
        
        Parameters:
        username (str): The username of the account.
        key (bytes): The key used for decryption.
        """
        self.clear_window()
        self.title("Get Password")

        ctk.CTkLabel(self, text="Enter service name:", font=("Arial", 20)).pack(pady=10)
        service_field = ctk.CTkEntry(self)
        service_field.pack(pady=5)

        def on_submit_pressed():
            service = service_field.get().strip()
            if service:
                password = get_password(username, service, key)
                service_field.delete(0, "end")
                self.clear_window()
                if password:
                    ctk.CTkLabel(
                        self,
                        text=f"Password for {service} : {password}",
                        font=("Arial", 20),
                    ).pack(pady=10)
                    ctk.CTkButton(
                        self, text="Copy", command=lambda: pyperclip.copy(password)
                    ).pack(pady=5)
                    ctk.CTkButton(
                        self,
                        text="OK",
                        command=lambda: self.user_sub_menu(username, key),
                    ).pack(pady=5)
                else:
                    ctk.CTkLabel(
                        self, text="Service not found", font=("Arial", 20)
                    ).pack(pady=10)
                    ctk.CTkButton(
                        self,
                        text="OK",
                        command=lambda: self.user_sub_menu(username, key),
                    ).pack(pady=5)
            else:
                ctk.CTkLabel(self, text="Please enter the service name").pack()

        ctk.CTkButton(self, text="Submit", command=on_submit_pressed).pack(pady=20)

    def clear_window(self):
        """
        Clear all widgets from the current window.
        """
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = PasswordManager()
    app.mainloop()
