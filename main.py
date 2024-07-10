from Steganography import Steganography
from ImageCrop import Crop_img
from settings import *


# Instantiate Steganography object and hide text in an image
steganography = Steganography()
steganography.hide_text_in_image(TEXT, ORIGINAL_IMG_PATH, ENCODED_IMAGE_PATH)
huffman_obj = steganography.return_huffman_obj()

# Instantiate Crop_img object and crop based on regex pattern in the encoded image
crop = Crop_img()
crop.crop(ENCODED_IMAGE_PATH, REGEX_PATTERN, CROPPED_IMAGE_PATH, huffman_obj)
