import re
from math import log2, floor

def LZ77_encode(text, window_size):
    input_char_array = list(text)
    output = ""
    window = []
    while len(input_char_array) > 0:
        match = find_maximum_matching(input_char_array, window, window_size)
        output += str(match).replace(" ","").replace("'","")
        for i in range(max(0, len(window) - window_size + match[1] + 1)):
            window.pop(0)
        for i in range(min(match[1] + 1, len(input_char_array))):
            window.append(input_char_array.pop(0))
    output += ';' + str(window_size)
    return output
    
def find_maximum_matching(input_char_array, window, window_size):
    char_array_len = len(input_char_array)
    window_len = len(window)
    if char_array_len == 0:
        return (0,0,"")
    next_symb = input_char_array[0]
    max_length = 0 
    max_start = 0
    start = 0
    length = 0
    n = 2**(15 - floor(log2(window_size)))-1
    while start < window_len and length < char_array_len and start + length < char_array_len + window_len and length < n:
        if start + length >= window_len:
            character_to_compare = input_char_array[start + length - window_len]
        else:
            character_to_compare = window[start + length]
        if input_char_array[length] == character_to_compare:
            length += 1
        else:
            if max_length<length:
                max_length = length
                max_start = start
                if length < char_array_len:
                    next_symb = input_char_array[length]
                else:
                    next_symb = ""
            length = 0
            start += 1
    if max_length<length:
        max_length = length
        max_start = start
        if length < char_array_len:
            next_symb = input_char_array[length]
        else:
            next_symb = ""
    return (max_start, max_length, next_symb)

def LZ77_decode(text):
    list_of_triples, window_size = process_decoded_text(text)
    decoded_text = ""
    decoded_list = []
    for triple in list_of_triples:
        for i in range(int(triple[1])):
            try:
                decoded_list.append(decoded_list[int(triple[0]) + i])
            except:
                raise Exception((triple[0]) + str(i))
        if triple[2] == "":
            decoded_list.append(" ")
        else:
            decoded_list.append(triple[2])
        for i in range(max(0, len(decoded_list) - window_size)):
            decoded_text += decoded_list.pop(0)
    while len(decoded_list)>0:
        decoded_text += decoded_list.pop(0)
    return decoded_text

def process_decoded_text(text):
    list_of_triples = []
    window_size = ""
    for i in range(len(text)):
        if text[-1-i] == ';':
            break
        window_size = text[-1-i] + window_size
    triple_regex = re.compile(r'\(.*?\)')
    matches = triple_regex.findall(text)
    for match in matches:
        triple_list = match[1:-1].split(",")
        if len(triple_list) > 3:
            triple_list = [triple_list[0],triple_list[1],","]
        list_of_triples.append(tuple(triple_list))
    return list_of_triples, int(window_size)

def LZ77_encode_file(file_name, window_size):
    file = open("text_files\\"+file_name, 'r',encoding="utf-8")
    text = file.read()
    file.close()
    file = open("compressed\\" + file_name, 'w+')
    file.write(LZ77_encode(text, window_size))
    file.close()

def LZ77_decode_file(file_name):
    file = open("compressed\\" + file_name, 'r',encoding="utf-8")
    text = file.read()
    file.close()
    file = open("decompressed\\" + file_name, 'w+')
    file.write(LZ77_decode(text))
    file.close()

def LZ77_encode_binary(text, window_size):
    input_char_array = list(text)
    output = [window_size]
    window = []
    while len(input_char_array) > 0:
        match = find_maximum_matching(input_char_array, window, window_size)
        output.append(match)
        for i in range(max(0, len(window) - window_size + match[1] + 1)):
            window.pop(0)
        for i in range(min(match[1] + 1, len(input_char_array))):
            window.append(input_char_array.pop(0))
    return output

def LZ77_encode_file_binary(file_name, window_size):
    byte_const = 2**8
    file = open("text_files\\"+file_name, 'r', encoding="utf-8")
    text = file.read()
    file.close()
    list_of_triples = LZ77_encode_binary(text, window_size)
    window_size = list_of_triples.pop(0)
    n = floor(log2(window_size)) + 1
    window_size_letter_1 = chr(window_size // byte_const + 2**6)
    window_size_letter_2 = chr(window_size % byte_const)
    file = open("compressed\\"+ str(window_size)+'_' + file_name, 'w', encoding="utf-8", newline = '')
    file.write(window_size_letter_1 + window_size_letter_2)
    for triple in list_of_triples:
        start = triple[0]
        length = triple[1]
        start_plus_length = start * 2**(16-n) + length
        first_letter = chr(start_plus_length // byte_const)
        second_letter = chr(start_plus_length % byte_const)
        file.write(first_letter + second_letter + triple[2])
    file.close()

def LZ77_decode_binary(file):
    list_of_triples, window_size = process_file_binary(file)
    decoded_text = ""
    decoded_list = []
    for count, triple in enumerate(list_of_triples):
        for i in range(triple[1]):
            decoded_list.append(decoded_list[int(triple[0]) + i])
        decoded_list.append(triple[2])
        for i in range(max(0, len(decoded_list) - window_size)):
            decoded_text += decoded_list.pop(0)
    while len(decoded_list)>0:
        decoded_text += decoded_list.pop(0)
    return decoded_text

def process_file_binary(file):
    list_of_triples = []
    window_size_letter_1 = file.read(1)
    window_size_letter_2 = file.read(1)
    window_size = (ord(window_size_letter_1)-64)*2**8+ord(window_size_letter_2)
    n = floor(log2(window_size)) + 1
    first_letter = file.read(1)
    second_letter = file.read(1)
    third_letter = file.read(1)
    while (first_letter != ""):
        start_plus_length = ord(first_letter)*2**8 + ord(second_letter)
        start = start_plus_length // (2**(16-n))
        length = start_plus_length % (2**(16-n))
        list_of_triples.append((start, length, third_letter))
        first_letter = file.read(1)
        second_letter = file.read(1)
        third_letter = file.read(1)

    return list_of_triples, int(window_size)


def LZ77_decode_file_binary(file_name):
    file = open("compressed\\" + file_name, 'r',encoding="utf-8", newline = '')
    text = LZ77_decode_binary(file)
    file.close()
    file = open("decompressed\\" + file_name, 'w', encoding="utf-8")
    file.write(text)
    file.close()

print(LZ77_decode(LZ77_encode('cabracadabrarrarra', 7)))
print(LZ77_encode('See on katse lause! ÖÄÜÕ', 7))
print(LZ77_encode_binary('See on katse lause! ÖÄÜÕ', 7))
print(LZ77_decode(LZ77_encode('See on katse lause! ÖÄÜÕ', 7)))
#LZ77_encode_file("Lorem_ipsum.txt",2047)
#LZ77_decode_file("Lorem_ipsum.txt")
file2 = open("text_files\\Lorem_ipsum.txt")
a = 'Ö'
print(a,'{0:08b}'.format(ord(a)))
print(chr(64))
window_size = 2002
window_size_letter_1 = chr(window_size // 2**8 + 2**6)
window_size_letter_2 = chr(window_size % 2**8)
print(window_size_letter_1 + window_size_letter_2)
print(ord(window_size_letter_1),ord(window_size_letter_2),(ord(window_size_letter_1)-64)*2**8+ord(window_size_letter_2))
file2.close()
LZ77_encode_file_binary("Lorem_ipsum.txt",2047)
LZ77_decode_file_binary("2047_Lorem_ipsum.txt")
#LZ77_encode_file_binary("Tõde_ja_õigus_I.txt",2047)
#print("Kodeeritud")
#LZ77_decode_file_binary("2047_Tõde_ja_õigus_I.txt")
#print("Korras")