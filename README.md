# StegaPass: A Steganographic Password Manager

StegaPass is a cutting-edge Python application that combines the power of steganography and cryptography to provide a secure and innovative way of managing passwords. By embedding encrypted passwords within images, StegaPass ensures that your sensitive information remains hidden in plain sight, offering an additional layer of security beyond traditional password managers.

## Features

- **Secure Password Storage**: Encrypts and stores passwords within images using steganography.
- **User-Friendly Interface**: Offers a simple and intuitive interface for managing passwords.
- **Advanced Encryption**: Utilizes state-of-the-art encryption techniques to protect your information.
- **Image Storage Management**: Organizes original and steganography-enhanced images for easy retrieval.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Pip for Python package management

### Installation

1. **Clone the Repository**

   Begin by cloning the StegaPass repository to your local machine using Git.

   ```sh
   git clone https://github.com/dkrishnakumar987/StegaPass.git
   ```

2. **Navigate to the Project Directory**

   Change into the project directory.

   ```sh
   cd StegaPass
   ```

3. **Install Dependencies**

   Install the required Python packages using pip.

   ```sh
   pip install -r requirements.txt
   ```

### Usage

1. **Start StegaPass**

   Launch the application by running the main Python script.

   ```sh
   python gui.py
   ```
   or
   ```bash
   python3 gui.py
   ```

2. **Register or Log In**

   Use the graphical interface to either register as a new user or log in with your existing credentials.

3. **Manage Passwords**

   The GUI provides an intuitive way to add, retrieve, and manage your passwords. Follow the on-screen instructions to navigate through the application.

## Project Structure

- `gui.py`: The graphical user interface for StegaPass, serving as the main entry point for users.
- `main.py`: Handles core functionalities like user registration, login, and password management.
- `encryption.py`: Contains the encryption logic used to secure passwords before embedding them into images.
- `steganography.py`: Implements the steganography techniques for hiding and retrieving encrypted data within images.

## Contributing

Contributions to StegaPass are welcome! Feel free to fork the repository, make your changes, and submit a pull request.
