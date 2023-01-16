from huffman import encode, decode
from Burrows.BWTs import BWTSuffixesIndexes, invertTransformFaster

text = "mina elan siin, aga sina????"
print("Input:", text)
BWT = BWTSuffixesIndexes()
transformed = BWT.transform(text)
print("BWT:", transformed)
e = encode(transformed)
print("Huffman:", e)
decoded = decode(e)
print("Decoded:", decoded)
original = invertTransformFaster(decoded)
print("InvertBWT:", original)