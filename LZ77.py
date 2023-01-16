import re

def LZ77_encode(text, window_size):
    input_char_array = list(text)
    output = ""
    window = []
    while len(input_char_array) > 0:
        match = find_maximum_matching(input_char_array, window)
        output += str(match).replace(" ","").replace("'","")
        for i in range(max(0, len(window) - window_size + match[1] + 1)):
            window.pop(0)
        for i in range(min(match[1] + 1, len(input_char_array))):
            window.append(input_char_array.pop(0))
    output += ';' + str(window_size)
    return output
    
def find_maximum_matching(input_char_array, window):
    char_array_len = len(input_char_array)
    window_len = len(window)
    if char_array_len == 0:
        return (0,0,"")
    next_symb = input_char_array[0]
    max_length = 0 
    max_start = 0
    start = 0
    length = 0
    while start < window_len and length < char_array_len and start + length < char_array_len + window_len:
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
    window_start = 0
    for triple in list_of_triples:
        for i in range(int(triple[1])):
            try:
                decoded_text += decoded_text[window_start + int(triple[0]) + i]
            except:
                raise Exception(str(window_start) +(triple[0]) + str(i))
        decoded_text += triple[2]
        if triple[2] == "":
            decoded_text += " "
        window_start = max(0, len(decoded_text) - window_size)
    return decoded_text

def process_decoded_text(text):
    list_of_triples = []
    window_size = ""
    for i in range(len(text)):
        if text[-1-i] == ';':
            break
        window_size = text[-1-i] + window_size
    triple_regex = re.compile(r'\(\d+,\d+,.?\)')
    matches = triple_regex.findall(text)
    for match in matches:
        triple_list = match[1:-1].replace("'","").split(",")
        if len(triple_list) > 3:
            triple_list = [triple_list[0],triple_list[1],","]
        list_of_triples.append(tuple(triple_list))
    return list_of_triples, int(window_size)

def LZ77_encode_file(file_name, window_size):
    file = open(file_name, 'r',encoding="utf-8")
    text = file.read()
    file.close()
    file = open("compressed_" + file_name, 'w+')
    file.write(LZ77_encode(text, window_size))
    file.close()

def LZ77_decode_file(file_name):
    file = open(file_name, 'r',encoding="utf-8")
    text = file.read()
    file.close()
    file = open("decompressed_" + file_name, 'w+')
    file.write(LZ77_decode(text))
    file.close()

print(find_maximum_matching("bab","abbaa"))
print(find_maximum_matching("baa","abbaa"))
print(find_maximum_matching("dbaa","abbaa"))
print(find_maximum_matching("babbbabbababbaa","abbaa"))
print(find_maximum_matching("bab","abbaabababababaabaaabaabaaaaba"))
print(find_maximum_matching("bbaa","abbaa"))
print(find_maximum_matching("bbaab","abbaa"))
print(find_maximum_matching("bbaabbababa","abbaa"))
print(str(find_maximum_matching("abbaa","bbaa")))

print(LZ77_decode(LZ77_encode('cabracadabrarrarra', 7)))
print(LZ77_decode(LZ77_encode('See on katse lause! ÖÄÜÕ', 7)))
LZ77_encode_file("Lorem_ipsum.txt",1000)
LZ77_decode_file("compressed_Lorem_ipsum.txt")