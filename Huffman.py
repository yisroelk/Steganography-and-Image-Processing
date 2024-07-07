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
    

def build_tree(text):
    counter = Counter(text)
    pq = [Tree(ch, counter[ch]) for ch in counter]
    heapq.heapify(pq)
    while len(pq) > 1:
        left = heapq.heappop(pq)
        right = heapq.heappop(pq)
        parent = Tree(None, left.freq+right.freq, left, right)
        heapq.heappush(pq, parent)
    return heapq.heappop(pq)


def build_map(root):
    def dfs(root, code, encoding_map):
        if root.ch:
            encoding_map[root.ch] = ''.join(code)
        else:
            code.append('0')
            dfs(root.left, code, encoding_map)
            code.pop()
            code.append('1')
            dfs(root.right, code, encoding_map)
            code.pop()
    encoding_map = {}
    dfs(root, [], encoding_map)
    return encoding_map


def encode(text):
    root = build_tree(text)
    encoding_map = build_map(root)
    return ''.join([encoding_map[ch] for ch in text]), root


def decode(encoded, root):
    if root.ch:
        return root.ch * len(encoded)
    decoded = []
    node = root
    for bit in encoded:
        if bit == "0":
            node = node.left
        else:
            node = node.right
        if node.ch:
            decoded.append(node.ch)
            node = root
    return ''.join(decoded)