from PIL import Image
import numpy as np

def encode_img(img_path, data, out_path):
    """
    Encodes binary data into the least significant bits of each pixel in an image.

    Args:
        img_path (str): The path to the image file.
        data (bytes): The binary data to encode.
        out_path (str): The path to save the encoded image.

    Raises:
        ValueError: If the data is too large to fit in the given image.

    Returns:
        None
    """
    img = Image.open(img_path)
    pixels = np.array(img)
    
    # Flattening the pixels array
    flat_pixels = pixels.flatten()
    flat_pixels_len = len(flat_pixels)

    # Converting byte data to binary string
    bin_data = ''.join([format(byte, '08b') for byte in data])
    data_len = len(bin_data)

    # Ensure the data is not too large to fit in the img
    if data_len > flat_pixels_len:
        raise ValueError("Data is too large to fit in the given image.")

    # Encode data in LSB of each pixel
    for i in range(data_len):
        # Modify the LSB of the current pixel with the current bit of data
        # & 254 clears the LSB and | int(bin_data[i]) sets the LSB
        flat_pixels[i] = (flat_pixels[i] & 254) | int(bin_data[i])

    # Reshape the array back to its original shape
    encoded_pixels = flat_pixels.reshape(pixels.shape)
    
    encoded_img = Image.fromarray(encoded_pixels)
    encoded_img.save(out_path)

def decode_img(img_path, data_len):
    """
    Decodes binary data from the least significant bits of each pixel in an image.

    Args:
        img_path (str): The path to the image file.
        data_len (int): The length of the binary data to decode.
    
    Raises:
        None

    Returns:
        bytes: The decoded binary data.
    """
    image = Image.open(img_path)
    pixels = np.array(image)

    # Flattening the pixels array
    flat_pixels = pixels.flatten()
    
    # Calculate the number of bits to decode
    tot_bits = data_len * 8
    
    # Extracting the LSB from each pixel
    data_bits = [flat_pixels[i] & 1 for i in range(tot_bits)]

    # Convert the bits to bytes
    data = bytearray()
    for i in range(0, len(data_bits), 8):
        byte = data_bits[i:i+8]
        byte_str = ''.join(map(str, byte))
        data.append(int(byte_str, 2))

    return bytes(data)

#Testing
""" img_path = 'ImageStorage/OriginalImages/test2.png'
out_path = 'ImageStorage/SteganoImages/test2.png'
data = b'Hello, World!'
encode_img(img_path, data, out_path)
print(decode_img(out_path, len(data))) """