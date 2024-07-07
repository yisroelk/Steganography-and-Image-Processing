import Huffman
import cv2



text_path = 'sample.txt'
text = ""
encoded_text = ""
encoded_text_len = 0
image = 'test_img.jpg'
height = 0
width = 0



# Open the file in read mode
try:
    with open(text_path, 'r') as file:
        # Read the content of the file
        text = file.read()
except FileNotFoundError:
    print(f"File '{text_path}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")


# Use Hoffman's algorithm to encode the text in the file
encoded_text, root = Huffman.encode(text)



image = cv2.imread('test_img.jpg')
height, width = image.shape[:2]
string_length = len(encoded_text)
string_length_in_dec = bin(string_length).replace("0b", "")
string_length_in_dec32bit = string_length_in_dec.zfill(32)
full_string = string_length_in_dec32bit + encoded_text
len_full_string = len(full_string)



def embed_code_in_image():
    counter = 0
    for i in range(height):
        for j in range(width):
            for rgb in range(3):
                if counter < len_full_string:
                    in_dec = bin(image[i][j][rgb]).replace("0b", "")
                    without_last_character = in_dec[0:-1]
                    new_pixel_value = str(without_last_character) + full_string[counter]
                    # aaa = in_dec.replace(str(in_dec[-1]), str(1))
                    # print(new_pixel_value)
                    image[i][j][rgb] = int(new_pixel_value, 2)
                # print(image)
                # print(image[i][j][rgb])

                # bb = a[0:-1] + b[counter]
                # if image[i][j][rgb] % 2 == 0:
                #     c = image[i][j][rgb]
                #     d = c + int(b[counter])
                #     print(b[5])
                #     image[i][j][rgb] = d
                # else:
                #     c = image[i][j][rgb]
                #     d = c + int(b[counter])
                #     print(b[90])
                #     image[i][j][rgb] = d
                    counter += 1
                else:
                    return image
                
def save_incoded_img():
    filename = 'savedImage.png'
    cv2.imwrite(filename, image)                


def find_string_length(image):
    string = ""
    for i in range(height):
        for j in range(width):
            for rgb in range(3):
                if len(string) < 32:
                    a = bin(image[i][j][rgb]).replace("0b", "")
                    aa = str(a)
                    string += str(aa[-1])
                else:
                    return int(string, 2)


def extract_code_from_img(image, lencode):
    string2 = ""
    for i in range(height):
        for j in range(width):
            for rgb in range(3):
                if len(string2) < lencode:
                    # a = (image[i][j][rgb])
                    a = bin(image[i][j][rgb]).replace("0b", "")
                    aa = str(a)
                    string2 += str(aa[-1])
                    # if a % 2 == 0:
                    #     string2 += str(0)
                    # else:
                    #     string2 += str(1)
                else:
                    return string2


embed_code_in_image()
save_incoded_img()
image2 = cv2.imread('savedImage.png')
height2, width2 = image2.shape[:2]
res = find_string_length(image2)
code = extract_code_from_img(image2, int(res)+32)
code2 = code[32:]
zz = decoded_text = Huffman.decode(code2, root)
print(zz)

