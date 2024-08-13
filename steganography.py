from numpy import array
from PIL import Image


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
    pixels = array(img)

    # Flattening the pixels array
    flat_pixels = pixels.flatten()
    flat_pixels_len = len(flat_pixels)

    # Converting byte data to binary string
    bin_data = "".join([format(byte, "08b") for byte in data])
    data_len = len(bin_data)

    # Ensure the data is not too large to fit in the img
    if data_len + 32 > flat_pixels_len:
        raise ValueError("Data is too large to fit in the given image.")

    # Encoding Data length in first 32 bits
    bin_data_len = bin(data_len)[2:].rjust(32, "0")
    for i in range(32):
        flat_pixels[i] = (flat_pixels[i] & 254) | int(bin_data_len[i])

    # Encode data in LSB of each pixel after 32 bits
    for i in range(32, data_len + 32):
        # Modify the LSB of the current pixel with the current bit of data
        # & 254 clears the LSB and | int(bin_data[i - 32]) sets the LSB
        flat_pixels[i] = (flat_pixels[i] & 254) | int(bin_data[i - 32])

    # Reshape the array back to its original shape
    encoded_pixels = flat_pixels.reshape(pixels.shape)

    encoded_img = Image.fromarray(encoded_pixels)
    encoded_img.save(out_path)


def decode_img(img_path):
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
    pixels = array(image)

    # Flattening the pixels array
    flat_pixels = pixels.flatten()

    # Extract the number of bits to decode
    len_bits = [flat_pixels[i] & 1 for i in range(32)]
    data_len = int("".join(map(str, len_bits)), 2)

    # Extracting the LSB from each pixel
    data_bits = [flat_pixels[i] & 1 for i in range(32, data_len + 32)]

    # Convert the bits to bytes
    data = bytearray()
    for i in range(0, len(data_bits), 8):
        byte = data_bits[i : i + 8]
        byte_str = "".join(map(str, byte))
        data.append(int(byte_str, 2))

    return bytes(data)


# Testing
""" img_path = 'ImageStorage/OriginalImages/test2.png'
out_path = 'ImageStorage/SteganoImages/test2.png'
data = b'Hello, World!'
encode_img(img_path, data, out_path)
print(decode_img(out_path, len(data))) """
