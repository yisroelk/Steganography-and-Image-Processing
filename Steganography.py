import cv2
from Huffman import HuffmanCoding


class Steganography:
    """
    A class for performing steganography by hiding text within an image using Huffman coding.
    
    Attributes:
        text (str): The text to be hidden.
        encoded_text (str): The encoded text.
        image (numpy.ndarray): The image where text will be hidden.
        height (int): The height of the image.
        width (int): The width of the image.
        huffman (HuffmanCoding): An instance of HuffmanCoding for text encoding and decoding.
        root (Tree): The root of the Huffman tree.
        full_string (str): The full binary string containing the encoded text and its length.
    """
    
    def __init__(self):
        self.text = ""
        self.encoded_text = ""
        self.image = None
        self.height = 0
        self.width = 0
        self.huffman = HuffmanCoding()
        self.root = None
        self.full_string = ""


    def __load_text(self, text_path):
        """
        Load text from a file.
        
        Args:
            text_path (str): The path to the text file.
        """
        try:
            with open(text_path, 'r') as file:
                self.text = file.read()
        except FileNotFoundError:
            print(f"File '{text_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")


    def __encode_text(self):
        """
        Encode the text using Huffman coding and prepare the binary string for hiding in the image.
        """
        # Encode the text using Huffman coding
        self.encoded_text = self.huffman.encode(self.text)
        # Get the length of the encoded string
        string_length = len(self.encoded_text)
        # Convert the length to a 32-bit binary string
        string_length_in_bin = bin(string_length).replace("0b", "")
        string_length_in_bin32bit = string_length_in_bin.zfill(32)
        # Concatenate the length and the encoded text
        self.full_string = string_length_in_bin32bit + self.encoded_text


    def __load_image(self, image_path):
        """
        Load an image from a file.
        
        Args:
            image_path (str): The path to the image file.
        """
        try:
            # Read the image using OpenCV
            self.image = cv2.imread(image_path)
            # Get the image dimensions
            self.height, self.width = self.image.shape[:2]
        except FileNotFoundError:
            print(f"File '{image_path}' not found.")


    def hide_text_in_image(self, text_path, image_path, output_image_path):
        """
        Hide the text from the specified file in the specified image and save the resulting image.
        
        Args:
            text_path (str): The path to the text file.
            image_path (str): The path to the image file.
            output_image_path (str): The path where the output image will be saved.
        """
        # Load the text, encode it, and load the image
        self.__load_text(text_path)
        self.__encode_text()
        self.__load_image(image_path)
        counter = 0
        len_full_string = len(self.full_string)
        # Check if the image has enough pixels to hide the text
        if self.height * self.width * 3 >= len_full_string:
            for i in range(self.height):
                for j in range(self.width):
                    for rgb in range(3):
                        if counter < len_full_string:
                            # Get the binary representation of the pixel value
                            in_bin = bin(self.image[i][j][rgb]).replace("0b", "")
                            # Replace the least significant bit with the encoded text bit
                            without_last_char = in_bin[:-1]
                            new_pixel_value = without_last_char + self.full_string[counter]
                            # Update the pixel value with the new binary value
                            self.image[i][j][rgb] = int(new_pixel_value, 2)
                            counter += 1
                        else:
                            # Save the encoded image
                            return self.__save_encoded_image(output_image_path)
        else:
            return None


    def __save_encoded_image(self, output_image_path):
        """
        Save the image with the hidden text to a file.
        
        Args:
            output_image_path (str): The path where the output image will be saved.
        """
        cv2.imwrite(output_image_path, self.image)


    def __find_string_length(self, image):
        """
        Extract the length of the hidden binary string from the image.
        
        Args:
            image (numpy.ndarray): The image from which to extract the string length.
        
        Returns:
            int: The length of the hidden binary string.
        """
        string = ""
        for i in range(self.height):
            for j in range(self.width):
                for rgb in range(3):
                    if len(string) < 32:
                        # Extract the least significant bit of the pixel value
                        in_bin = bin(image[i][j][rgb]).replace("0b", "")
                        string += in_bin[-1]
                    else:
                        # Convert the binary string to an integer
                        return int(string, 2)


    def __extract_code_from_image(self, image, len_code):
        """
        Extract the binary string from the image.
        
        Args:
            image (numpy.ndarray): The image from which to extract the binary string.
            len_code (int): The length of the binary string to be extracted.
        
        Returns:
            str: The extracted binary string.
        """
        string = ""
        for i in range(self.height):
            for j in range(self.width):
                for rgb in range(3):
                    if len(string) < len_code:
                        # Extract the least significant bit of the pixel value
                        in_bin = bin(image[i][j][rgb]).replace("0b", "")
                        string += in_bin[-1]
                    else:
                        return string


    def extract_text_from_image(self, image_path):
        """
        Extract and decode the hidden text from the specified image.
        
        Args:
            image_path (str): The path to the image file.
        
        Returns:
            str: The decoded text.
        """
        image = cv2.imread(image_path)
        self.height, self.width = image.shape[:2]
        # Extract the length of the encoded string
        string_length = self.__find_string_length(image)
        # Extract the full encoded string
        full_code = self.__extract_code_from_image(image, string_length + 32)
        # Remove the length part of the string
        encoded_text = full_code[32:]
        # Decode the text using Huffman coding
        decoded_text = self.huffman.decode(encoded_text)
        return decoded_text


    def return_huffman_obj(self):
        """
        Return the HuffmanCoding object used for encoding and decoding text.
        
        Returns:
            HuffmanCoding: The HuffmanCoding object.
        """
        return self.huffman

# # Usage
# test = Steganography()
# test.hide_text_in_image("sample.txt", "test_img.jpg", "encoded_image.png")
# print(test.extract_text_from_image("encoded_image.png"))
