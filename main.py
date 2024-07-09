from Steganography import *
from image_crop import *

steganography = Steganography()
steganography.hide_text_in_image("sample.txt", "test_img.jpg", "encoded_image.png")
huffman_obj = steganography.return_huffman_obj()
crop = Crop_img()
crop.crop("encoded_image.png", "\d{2}", "cropt_image.png", huffman_obj)