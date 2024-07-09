# Steganography and Image Crop

## Overview

This project includes Python classes for performing steganography (hiding text within an image) and cropping parts of an image based on matches found in encoded text using Huffman coding.

### Files Included

- `Steganography.py`: Contains the `Steganography` class for hiding text in an image using Huffman coding.
- `image_crop.py`: Includes the `Crop_img` class for cropping parts of an image based on matches found in the encoded text.

### Dependencies

- Python 3.x
- Pillow (PIL fork) for image processing (`pip install Pillow`)

## Usage

### Steganography (`Steganography.py`)

#### Class: `Steganography`

#### Methods

- `hide_text_in_image(text_path, image_path, output_image_path)`: Hides text from a file within an image.

  ```python
  from Steganography import Steganography
  
  steganography = Steganography()
  steganography.hide_text_in_image("sample.txt", "test_img.jpg", "encoded_image.png")
  ```

- `extract_text_from_image(image_path)`: Extracts hidden text from an image.

  ```python
  from Steganography import Steganography
  
  steganography = Steganography()
  decoded_text = steganography.extract_text_from_image("encoded_image.png")
  print(decoded_text)
  ```

- `return_huffman_obj()`: Returns the HuffmanCoding object used for encoding and decoding.

  ```python
  from Steganography import Steganography
  
  steganography = Steganography()
  huffman_obj = steganography.return_huffman_obj()
  ```

### Image Crop (`image_crop.py`)

#### Class: `Crop_img`

#### Methods

- `crop(image_path, regex_pattern, output_image_path, huffman_obj)`: Crops parts of an image based on matches found in the encoded image.

  ```python
  from Steganography import Steganography
  from image_crop import Crop_img
  
  steganography = Steganography()
  steganography.hide_text_in_image("sample.txt", "test_img.jpg", "encoded_image.png")
  huffman_obj = steganography.return_huffman_obj()
  
  crop = Crop_img()
  crop.crop("encoded_image.png", "\d{2}", "cropped_image.png", huffman_obj)
  ```

## Example

1. **Hide Text in Image**
   - Use `Steganography` to hide text from `sample.txt` in `test_img.jpg` and save as `encoded_image.png`.

2. **Crop Image Based on Encoded Text**
   - Use `Crop_img` to load `encoded_image.png`, search for digits (`\d{2}`) in the encoded text, and save the cropped image as `cropped_image.png`.


