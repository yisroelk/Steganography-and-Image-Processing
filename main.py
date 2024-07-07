import Huffman
import cv2


# Open the file in read mode
text_path = 'sample.txt'
text = ""
 
try:
    with open(text_path, 'r') as file:
        # Read the content of the file
        text = file.read()

 
except FileNotFoundError:
    print(f"File '{text_path}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")

# text = "In computer science and information theory, a Huffman code is a particular type of optimal prefix code that is commonly used for lossless data compression. The process of finding or using such a code is Huffman coding, an algorithm developed by David A. Huffman while he was a Sc.D. student at MIT, and published in the 1952 paper A Method for the Construction of Minimum-Redundancy Codes"

encoded_text, root = Huffman.encode(text)





# print("------")
decoded_text = Huffman.decode(encoded_text, root)
# print(decoded_text)

def decimalToBinary(n): 
    return bin(n).replace("0b", "")


image = cv2.imread('test_img.jpg')
height, width = image.shape[:2]
string_length = len(encoded_text)
string_length_in_dec = decimalToBinary(string_length)
a = string_length_in_dec.zfill(32)
b = a + encoded_text
print(b)
print("------")




counter = 0

for i in range(height):
    for j in range(width):
        for rgb in range(3):
            if image[i][j][rgb] % 2 == 0:
                c = image[i][j][rgb]
                d = c + int(b[counter])
                image[i][j][rgb] = d
            else:
                c = image[i][j][rgb]
                d = c + int(b[counter])
                image[i][j][rgb] = d
            counter =+ 1



# # Window name in which image is displayed 
# window_name = 'image'
  
# # Using cv2.imshow() method 
# # Displaying the image 
# cv2.imshow(window_name, image) 
  
# # waits for user to press any key 
# # (this is necessary to avoid Python kernel form crashing) 
# cv2.waitKey(0) 
  
# # closing all open windows 
# cv2.destroyAllWindows() 

string = "1795"
def findstringLength(image):
    for i in range(height):
        for j in range(width):
            for rgb in range(3):
                if len(string) < 32:
                    string + image[i][j][rgb]
                else:
                    return

def Convertbinarytodecimal(string):
    return
    pass


def Extractcode(image):
    stringlen = 1763
    string2 = ""
    for i in range(height):
        for j in range(width):
            for rgb in range(3):
                if len(string2) < stringlen:
                    a = (image[i][j][rgb])
                    if a % 2 == 0:
                        string2 += str(0)
                    else:
                        string2 += str(1)
                else:
                    return string2
                
res = Extractcode(image)
print(res)


# from PIL import Image
# import numpy as np

# # Open the image using Pillow
# image = Image.open('test_img.jpeg')

# # Convert the image to a NumPy array
# image_matrix = np.array(image)

# # Display the image matrix
# print(image_matrix)

