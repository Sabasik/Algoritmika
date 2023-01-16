from heapq import *


class Node:
    def __init__(self, char, count, left=None, right=None):
        self.char = char
        self.count = count
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.count < other.count


def get_codes(codes, element, path):
    if len(element.char) > 0:
        codes[element.char] = path
    else:
        get_codes(codes, element.left, path + "0")
        get_codes(codes, element.right, path + "1")


def encode(text):
    elements = {}
    for el in text:
        if el not in elements:
            elements[el] = 0
        elements[el] += 1

    heap = [Node(key, value) for key, value in elements.items()]
    heapify(heap)

    while len(heap) > 1:
        el1 = heappop(heap)
        el2 = heappop(heap)
        new = Node("", el1.count + el2.count, el1, el2)
        heappush(heap, new)

    codes = {}
    get_codes(codes, heap[0], "")

    res = ""
    for el in text:
        res += codes[el]

    return str(codes)[1:-1] + "**" + res


def decode(encoded):
    pieces = encoded.split("**")
    codes = {}
    coded = pieces[0].split(", ")
    for c in coded:
        c = c.split(": ")
        codes[c[1][1:-1]] = c[0][1:-1]

    text = pieces[1]
    res = ""
    i = 0
    while i < len(text):
        for j in range(i + 1, len(text) + 1):
            if text[i: j] in codes:
                res += codes[text[i: j]]
                i = j - 1
                break
        i += 1

    return res


e = encode("mina elan siin, aga sina????")
print(e)
print(decode(e))
