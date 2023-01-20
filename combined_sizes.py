from Burrows.BWTs import BWTSuffixesIndexes, invertTransformFaster, runBWTonFile, reverseBWTonFile
from LZ77 import LZ77_encode, LZ77_decode, LZ77_encode_file_binary, LZ77_decode_file_binary
from huffman_baitidega import huff_encode_file, huff_decode_file
from dahuffman import HuffmanCodec
# We used dahuffman library for Huffman encoding, because our own implementation kept failing on some inputs.
# - https://pypi.org/project/dahuffman/

filename = "bible.txt"

# LZ77
#print("Starting")
#text, transformed = runBWTonFile(BWTSuffixesIndexes, "random_DNA_5m.txt", 80000)
#print("BWT done")
#LZ77_encode_file_binary("BWT_80000_random_DNA_5m.txt",2047)
#print("Encoding done")
#LZ77_decode_file_binary("2047_BWT_80000_random_DNA_5m.txt")
#print("Decoding done")
#inverted = reverseBWTonFile("2047_BWT_80000_random_DNA_5m.txt", 80000)
#print("BWT revert done")
#print(text == inverted)
#LZ77_encode_file_binary("random_DNA_5m.txt",2047)
#print("All done!")


def encode_file_dahuffman(in_file, out_file):
    with open(in_file, 'r', encoding="utf8") as fi:
        text = fi.read()
    with open(out_file, 'wb') as fo:
        codec = HuffmanCodec.from_data(text)
        encoded = codec.encode(text)
        fo.write(encoded)
    return codec

def decode_file_dahuffman(in_file, out_file, codec):
    with open(in_file, 'rb') as fi:
        text = fi.read()
    with open(out_file, 'w', encoding="utf8") as fo:
        decoded = codec.decode(text)
        fo.write(decoded)
    return codec

print("Starting")
#text, transformed = runBWTonFile(BWTSuffixesIndexes, filename, 80000)
file = open("text_files\\" + filename, 'r', encoding="utf-8")
text = file.read()
file.close()
print("BWT done")
#huff_encode_file("text_files\\BWT_80000_" + filename, "compressed\\huff_BWT_80000_" + filename[:-4])
codec = encode_file_dahuffman("text_files\\BWT_80000_" + filename, "compressed\\huff_BWT_80000_" + filename[:-4])
print("Encoding done")
codec = decode_file_dahuffman("compressed\\huff_BWT_80000_" + filename[:-4], "decompressed\\dec_huff_BWT_80000_" + filename, codec)
print("Decoding done")
inverted = reverseBWTonFile("dec_huff_BWT_80000_" + filename, 80000)
print("BWT revert done")
print(text == inverted)
encode_file_dahuffman("text_files\\" + filename, "compressed\\huff_" + filename[:-4])
print("All done!")
