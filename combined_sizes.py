from huffman import encode, decode
from Burrows.BWTs import BWTSuffixesIndexes, invertTransformFaster, runBWTonFile, reverseBWTonFile
from time import perf_counter
from random import choices
from string import ascii_letters
from LZ77 import LZ77_encode, LZ77_decode, LZ77_encode_file_binary, LZ77_decode_file_binary
import matplotlib.pyplot as plt



#runBWTonFile(BWTSuffixesIndexes, "Tõde_ja_õigus_I.txt", 80000)
reverseBWTonFile("BWT_80000_Tõde_ja_õigus_I.txt", 80000)


#LZ77_encode_file_binary("Tõde_ja_õigus_I.txt",2047)
#print("Kodeeritud")
#LZ77_decode_file_binary("2047_Tõde_ja_õigus_I.txt")
#print("Korras")


