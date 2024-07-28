import encryption as enc
import steganography as steg

InputDir = "ImageStorage/OriginalImages/"
OutputDir = "ImageStorage/SteganoImages/"  
key = enc.get_random_bytes(16)

while (True):
    print("1. Encrypt and Encode")
    print("2. Decrypt and Decode")
    print("3. Exit")
    choice = int(input("Enter your choice: "))
    if (choice == 1):
        password = input("Enter the password to be encrypted: ")
        img = input("Enter the name of the image: ")
        encrypted_password, nonce, tag = enc.encrypt_pwd(password, key)
        data = enc.add_data(encrypted_password, nonce, tag)
        data_len = len(data)
        try:
            steg.encode_img(InputDir + "test1.png", data, OutputDir + "test1.png")
            print("Encrypted and encoded password successfully!")
        except ValueError as e:
            print(e)
    elif (choice == 2):
        img = input("Enter the name of the image: ")
        data = steg.decode_img(OutputDir + img, data_len)
        ciphertext, nonce, tag = enc.separate_data(data, 16, 16)
        try:
            password = enc.decrypt_pwd(ciphertext, nonce, tag, key)
            print("Decrypted password: ", password)
        except Exception as e:
            print(e)
            print("Decryption failed")
    elif(choice == 3):
        break
    else:
        print("Invalid choice")