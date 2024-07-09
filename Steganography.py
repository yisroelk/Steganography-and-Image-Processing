import cv2
from Huffman import HuffmanCoding

class Steganography:
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
        try:
            with open(text_path, 'r') as file:
                self.text = file.read()
        except FileNotFoundError:
            print(f"File '{text_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def __encode_text(self):
        self.encoded_text = self.huffman.encode(self.text)
        string_length = len(self.encoded_text)
        string_length_in_bin = bin(string_length).replace("0b", "")
        string_length_in_bin32bit = string_length_in_bin.zfill(32)
        self.full_string = string_length_in_bin32bit + self.encoded_text


    def __load_image(self, image_path):
        try:
            self.image = cv2.imread(image_path)
            self.height, self.width = self.image.shape[:2]
        except FileNotFoundError:
            print(f"File '{image_path}' not found.")


    def hide_text_in_image(self, text_path, image_path, output_image_path):
        self.__load_text(text_path)
        self.__encode_text()
        self.__load_image(image_path)
        counter = 0
        len_full_string = len(self.full_string)
        if self.height * self.width * 3 > len_full_string:
            for i in range(self.height):
                for j in range(self.width):
                    for rgb in range(3):
                        if counter < len_full_string:
                            in_bin = bin(self.image[i][j][rgb]).replace("0b", "")
                            without_last_char = in_bin[:-1]
                            new_pixel_value = without_last_char + self.full_string[counter]
                            self.image[i][j][rgb] = int(new_pixel_value, 2)
                            counter += 1
                        else:
                            return self.__save_encoded_image(output_image_path)
        else:
            return None


    def __save_encoded_image(self, output_image_path):
        cv2.imwrite(output_image_path, self.image)


    def __find_string_length(self, image):
        string = ""
        for i in range(self.height):
            for j in range(self.width):
                for rgb in range(3):
                    if len(string) < 32:
                        in_bin = bin(image[i][j][rgb]).replace("0b", "")
                        string += in_bin[-1]
                    else:
                        return int(string, 2)

    def __extract_code_from_image(self, image, lencode):
        string = ""
        for i in range(self.height):
            for j in range(self.width):
                for rgb in range(3):
                    if len(string) < lencode:
                        in_bin = bin(image[i][j][rgb]).replace("0b", "")
                        string += in_bin[-1]
                    else:
                        return string

    def extract_text_from_image(self, image_path):
        image = cv2.imread(image_path)
        self.height, self.width = image.shape[:2]
        string_length = self.__find_string_length(image)
        full_code = self.__extract_code_from_image(image, string_length + 32)
        encoded_text = full_code[32:]
        decoded_text = self.huffman.decode(encoded_text)
        return decoded_text

    
    def return_huffman_obj(self):
        return self.huffman

# Usage
test = Steganography()
test.hide_text_in_image("sample.txt", "test_img.jpg", "encoded_image.png")
print(test.extract_text_from_image("encoded_image.png"))
