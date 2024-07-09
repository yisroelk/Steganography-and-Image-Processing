import heapq
from collections import Counter


class Tree:
    def __init__(self, ch, freq, left=None, right=None):
        self.ch = ch
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCoding:
    def __init__(self):
        self.root = None
        self.encoding_map = {}
        self.encode_string = ""
        self.text = None



    def __build_tree(self, text):
        counter = Counter(text)
        pq = [Tree(ch, counter[ch]) for ch in counter]
        heapq.heapify(pq)
        while len(pq) > 1:
            left = heapq.heappop(pq)
            right = heapq.heappop(pq)
            parent = Tree(None, left.freq + right.freq, left, right)
            heapq.heappush(pq, parent)
        self.root = heapq.heappop(pq)


    def __build_map(self):
        def dfs(node, code):
            if node.ch:
                self.encoding_map[node.ch] = ''.join(code)
            else:
                code.append('0')
                dfs(node.left, code)
                code.pop()
                code.append('1')
                dfs(node.right, code)
                code.pop()
        dfs(self.root, [])


    def encode(self, text):
        self.__build_tree(text)
        self.__build_map()
        self.text = text
        self.encode_string = ''.join(self.encoding_map[ch] for ch in text)
        print(self.encode_string)
        return self.encode_string


    def decode(self, encoded):
        if self.root.ch:
            return self.root.ch * len(encoded)
        decoded = []
        node = self.root
        for bit in encoded:
            if bit == "0":
                node = node.left
            else:
                node = node.right
            if node.ch:
                decoded.append(node.ch)
                node = self.root
        decoded_text = ''.join(decoded)
        if (decoded_text is self.text):
            return decoded_text
        else:
            return None

    def encode_with_same_tree(self, text):
        if self.encoding_map:
            return ''.join(self.encoding_map[ch] for ch in text)
        else:
            return None