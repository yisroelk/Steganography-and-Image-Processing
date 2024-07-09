import re
from PIL import Image

class Crop_img:
    def __init__(self):
        self.img = None
        self.width = None
        self.height = None
        self.matches = []
        self.matches_bin = []
        self.huffman_obj = None
        self.encode_text = None
        self.indexes = []
        self.regex = None
        self.text = None


    def __calculation(self,indxs):
        indxs = indxs//3
        y = indxs//self.width
        x = indxs%self.width 
        return(x,y)

       
    def __find_text_matches(self):
        i = 0
        print(self.text)
        print(self.regex)
        while True :
            search_reg = re.search(self.regex, self.text[i:])
            if search_reg:
                start,end = search_reg.span()
                matche = search_reg.group()
                start += i
                end += i
                self.matches.append(matche)
                i = end
            else:
                return self.matches
            
            
    def __find_in_string(self):
        print(self.matches)
        for matche in self.matches:
            matche_bin = self.huffman_obj.encode_with_same_tree(matche)
            self.matches_bin.append(matche_bin)
        start = 0
        for bin in self.matches_bin:
            start_i = self.huffman_obj.encode_string.find(bin, start)
            end_i = self.__calculation(start_i+len(bin))
            start = start_i+len(bin)
            start_i = self.__calculation(start_i)
            if start_i[1] == end_i[1]:
                self.indexes.append((start_i,end_i))
            else:
                self.indexes.append((start_i,(self.width-1,start_i[1])))
                self.indexes.append(((0,end_i[1]),end_i))
        return(self.indexes)
    

    def crop(self, image_path, regex_pattern, output_image_path, huffman_obj):
        self.img = Image.open(image_path)
        self.width = self.img.size[0]
        self.height = self.img.size[1]
        self.huffman_obj = huffman_obj
        self.text = huffman_obj.text
        self.encode_text = huffman_obj.encode_string
        self.regex = regex_pattern
        self.__find_text_matches()
        self.__find_in_string()

        new_img = Image.new('RGBA',(self.img.size),(0,0,0,0))
        for index in self.indexes:
            x,y,= index[0]
            print(x,y)
            x_e,y_e =index[1]
            print(x_e,y_e)
            crop_i=self.img.crop((x,y,x+(x_e-x),y+1))
            new_img.paste(crop_i,(x,y))
        new_img.save(output_image_path)
        print(self.indexes)






# text = "hi 23 to 24 you and all 78 scripts"
# regex_pattern = "\d{2}"
# a = find_text_matches(text,regex_pattern)
# print(a)
# e= Image.open("im.png")
# x_i = 5
# y_i = 5
# for i in range(0,25):
#     y = i//x_i
#     x = i%x_i 
#     print(x,y)
 
