import base64
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


def huff_encode(text):
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

    bitstring = ""
    for el in text:
        bitstring += codes[el]

    bitstring = "0" * ((8 - len(bitstring) % 8) % 8) + bitstring
    enc = int(bitstring, 2).to_bytes(len(bitstring) // 8, byteorder='big')

    return str(codes)[1:-1].encode() + b"**" + enc


def huff_decode(encoded):
    pieces = encoded.split(b"**")
    codes = {}
    coded = pieces[0].decode().split(", ")
    for c in coded:
        c = c.split(": ")
        codes[c[1][1:-1]] = c[0][1:-1]

    enc = pieces[1]

    text = "{0:b}".format(int.from_bytes(enc, byteorder='big'))
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


def huff_encode_file(in_file, out_file):
    with open(in_file, 'r', encoding="utf8") as fi:
        text = fi.read()
    with open(out_file, 'wb') as fo:
        fo.write(huff_encode(text))


def huff_decode_file(in_file, out_file):
    with open(in_file, 'rb') as fi:
        text = fi.read()
    with open(out_file, 'w', encoding="utf8") as fo:
        fo.write(huff_decode(text))


if __name__ == "__main__":
    e = huff_encode("mina elan siin, aga sina????")
    print(e)
    print(huff_decode(e))

    huff_encode_file("text_files/Tõde_ja_õigus_I.txt", "compressed/huff_Tõde_ja_õigus_I")
    huff_decode_file("compressed/huff_Tõde_ja_õigus_I", "decompressed/huff_Tõde_ja_õigus_I.txt")
