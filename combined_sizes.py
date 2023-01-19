from huffman import encode, decode
from Burrows.BWTs import BWTSuffixesIndexes, invertTransformFaster, runBWTonFile, reverseBWTonFile
from time import perf_counter
from random import choices
from string import ascii_letters
from LZ77 import LZ77_encode, LZ77_decode, LZ77_encode_file_binary, LZ77_decode_file_binary
import matplotlib.pyplot as plt


print("Starting")
text, transformed = runBWTonFile(BWTSuffixesIndexes, "random_DNA_5m.txt", 80000)
print("BWT done")
LZ77_encode_file_binary("BWT_80000_random_DNA_5m.txt",2047)
print("Encoding done")
LZ77_decode_file_binary("2047_BWT_80000_random_DNA_5m.txt")
print("Decoding done")
inverted = reverseBWTonFile("2047_BWT_80000_random_DNA_5m.txt", 80000)
print("BWT revert done")
print(text == inverted)

#print()
#BWT = BWTSuffixesIndexes
#text, transformed = runBWTonFile(BWT,"katkend.txt", 90000)
#inverted = reverseBWTonFile("BWT_90000_katkend.txt", 90000)

#print(text == inverted)

LZ77_encode_file_binary("random_DNA_5m.txt",2047)