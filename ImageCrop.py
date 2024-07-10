import re
from PIL import Image


class Crop_img:
    """
    A class to crop parts of an image based on encoded text matches.

    Attributes:
        img (PIL.Image.Image): The image to be processed.
        width (int): The width of the image.
        height (int): The height of the image.
        matches (list): List of matched text patterns.
        matches_bin (list): List of matched text patterns in binary form.
        huffman_obj (HuffmanCoding): Huffman coding object for encoding and decoding text.
        encode_text (str): The encoded text string.
        indexes (list): List of tuples containing start and end indexes of matches in the image.
        regex (str): Regular expression pattern to search in the text.
        text (str): The text to be encoded and searched.
    """
    
    def __init__(self):
        self.img = None
        self.width = None
        self.height = None
        self.huffman_obj = None
        self.encode_text = None
        self.regex = None
        self.text = None
        # Initialize lists for matches and their binary representations
        self.matches = []
        self.matches_bin = []
        # Initialize list for indexes
        self.indexes = []


    def __calculation(self, index):
        """
        Calculate the (x, y) coordinates in the image from the index.
        
        Args:
            index (int): The index to be converted.
        
        Returns:
            tuple: A tuple containing the (x, y) coordinates.
        """
        index = index // 3  # Each pixel in RGB takes 3 values; adjust index accordingly
        y = index // self.width  # Calculate row (y-coordinate)
        x = index % self.width   # Calculate column (x-coordinate)
        return (x, y)


    def __find_text_matches(self):
        """
        Find all matches of the regex pattern in the text and store them.
        
        Returns:
            list: A list of all matched text patterns.
        """
        string_i = 0
        while True:
            search_reg = re.search(self.regex, self.text[string_i:])
            if search_reg:
                start, end = search_reg.span()
                matche = search_reg.group()
                start += string_i
                end += string_i
                self.matches.append(matche)  # Store the matched text pattern
                string_i = end  # Move to the end of the matched text
            else:
                return self.matches  # Return all matched patterns
            

    def __find_in_string(self):
        """
        Find the binary representations of the matches and calculate their positions in the image.
        
        Returns:
            list: A list of tuples containing the start and end coordinates of the matches.
        """
        for matche in self.matches:
            matche_bin = self.huffman_obj.encode_with_same_tree(matche)  # Encode the matched text
            self.matches_bin.append(matche_bin)  # Store the binary representation
        start = 0
        for bin in self.matches_bin:
            start_i = self.huffman_obj.encode_string.find(bin, start)  # Find the binary pattern in the encoded text
            end_i = self.__calculation(start_i + len(bin))  # Calculate end coordinates
            start = start_i + len(bin)
            start_i = self.__calculation(start_i)  # Calculate start coordinates
            if start_i[1] == end_i[1]:
                self.indexes.append((start_i, end_i))  # Store as (start, end) if in the same row
            else:
                self.indexes.append((start_i, (self.width - 1, start_i[1])))  # Store across rows
                self.indexes.append(((0, end_i[1]), end_i))
        return self.indexes
    

    def crop(self, image_path, regex_pattern, output_image_path, huffman_obj):
        """
        Crop the image based on matches of the regex pattern in the encoded text.
        
        Args:
            image_path (str): The path to the image file.
            regex_pattern (str): The regex pattern to search for in the text.
            output_image_path (str): The path where the output image will be saved.
            huffman_obj (HuffmanCoding): Huffman coding object containing the encoded text.
        """
        self.img = Image.open(image_path)
        self.width = self.img.size[0]
        self.height = self.img.size[1]
        self.huffman_obj = huffman_obj
        self.text = huffman_obj.text
        self.encode_text = huffman_obj.encode_string
        self.regex = regex_pattern
        self.__find_text_matches()  # Find all regex matches in the text
        self.__find_in_string()    # Find binary representations and positions in the image
        new_img = Image.new('RGBA', (self.img.size), (0, 0, 0, 0))  # Create a new transparent image
        # Iterate through all indexes and crop the image
        for index in self.indexes:
            start_x, start_y = index[0]
            end_x, end_y = index[1]
            crop_i = self.img.crop((start_x, start_y, start_x + (end_x - start_x), start_y + 1))  # Crop image segment
            new_img.paste(crop_i, (start_x, start_y))  # Paste cropped segment into new image
        new_img.save(output_image_path)  # Save the new cropped image

