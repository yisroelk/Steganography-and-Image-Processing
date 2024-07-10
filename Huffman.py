import heapq
from collections import Counter


class Tree:
    """
    A class representing a node in the Huffman tree.
    
    Attributes:
        ch (str): The character stored in the node.
        freq (int): The frequency of the character.
        left (Tree): The left child of the node.
        right (Tree): The right child of the node.
    """
    
    def __init__(self, ch, freq, left=None, right=None):
        self.ch = ch
        self.freq = freq
        self.left = left
        self.right = right


    def __lt__(self, other):
        """
        Less than comparison based on frequency.
        
        Args:
            other (Tree): Another Tree node to compare against.
        
        Returns:
            bool: True if the current node's frequency is less than the other node's frequency.
        """
        return self.freq < other.freq


class HuffmanCoding:
    """
    A class for Huffman coding, providing methods to encode and decode text.
    
    Attributes:
        root (Tree): The root of the Huffman tree.
        encoding_map (dict): A dictionary mapping characters to their Huffman codes.
        encode_string (str): The encoded string.
        text (str): The original text to be encoded.
    """
    
    def __init__(self):
        self.root = None
        self.encoding_map = {}
        self.encode_string = ""
        self.text = None


    def __build_tree(self, text):
        """
        Build the Huffman tree based on the frequency of characters in the text.
        
        Args:
            text (str): The text to be encoded.
        """
        counter = Counter(text)  # Count the frequency of each character
        pq = [Tree(ch, counter[ch]) for ch in counter]  # Create a priority queue of Tree nodes
        heapq.heapify(pq)  # Transform the list into a heap
        # Build the Huffman tree
        while len(pq) > 1:
            left = heapq.heappop(pq)
            right = heapq.heappop(pq)
            parent = Tree(None, left.freq + right.freq, left, right)
            heapq.heappush(pq, parent)
        self.root = heapq.heappop(pq)  # The root of the tree


    def __build_map(self):
        """
        Build the encoding map by traversing the Huffman tree.
        """
        def dfs(node, code):
            """
            Depth-first search to generate Huffman codes.
            
            Args:
                node (Tree): The current node in the Huffman tree.
                code (list): The current Huffman code as a list of bits.
            """
            if node.ch:
                # If the node is a leaf, add the character and its code to the map
                self.encoding_map[node.ch] = ''.join(code)
            else:
                # Traverse left with '0' and right with '1'
                code.append('0')
                dfs(node.left, code)
                code.pop()
                code.append('1')
                dfs(node.right, code)
                code.pop()
        dfs(self.root, [])  # Start DFS from the root of the tree


    def encode(self, text):
        """
        Encode the text using Huffman coding.
        
        Args:
            text (str): The text to be encoded.
        
        Returns:
            str: The encoded string.
        """
        self.__build_tree(text)  # Build the Huffman tree
        print(self.__build_tree)
        self.__build_map()  # Build the encoding map
        print(self.__build_map)
        self.text = text
        # Create the encoded string using the encoding map
        self.encode_string = ''.join(self.encoding_map[ch] for ch in text)  # Encode the text
        print(self.encode_string)
        return self.encode_string


    def decode(self, encoded):
        """
        Decode the encoded string using the Huffman tree.
        
        Args:
            encoded (str): The encoded string.
        
        Returns:
            str: The decoded text or None if the decoding is incorrect.
        """
        # If there's only one unique character in the tree
        if self.root.ch:
            return self.root.ch * len(encoded)
        
        decoded = []
        node = self.root
        # Traverse the tree according to the bits in the encoded string
        for bit in encoded:
            node = node.left if bit == "0" else node.right
            # If a leaf node is reached, add the character to the decoded list
            if node.ch:
                decoded.append(node.ch)
                node = self.root
        
        decoded_text = ''.join(decoded)
        # Verify if the decoded text matches the original text
        return decoded_text if decoded_text == self.text else None


    def encode_with_same_tree(self, text):
        """
        Encode the text using the existing Huffman tree.
        
        Args:
            text (str): The text to be encoded.
        
        Returns:
            str: The encoded string or None if the encoding map is not built.
        """
        if self.encoding_map:
            return ''.join(self.encoding_map[ch] for ch in text)
        else:
            return None
        

