from huffman import encode, decode
from Burrows.BWTs import BWTSuffixesIndexes, invertTransformFaster
from time import perf_counter
from random import choices
from string import ascii_letters
from LZ77 import LZ77_encode, LZ77_decode
import matplotlib.pyplot as plt


def runBWT(BWT_class, text):
    start = perf_counter()
    transformed = BWT_class().transform(text)
    BWTtimeT = perf_counter() - start
    return transformed, BWTtimeT

def runEncoder(encoder, text):
    start = perf_counter()
    encoded = encoder(text)
    encoderTime = perf_counter() - start
    return encoded, encoderTime

def runDecoder(decoder, text):
    start = perf_counter()
    decoded = decoder(text)
    decoderTime = perf_counter() - start
    return decoded, decoderTime

def runInverseBWT(text):
    start = perf_counter()
    original = invertTransformFaster(text)
    BWTtimeI = perf_counter() - start
    return original, BWTtimeI

def runWithBWT(BWT_class, encoder, decoder, text, include_BWT_time=True, name=""):
    # Runs BWT, endcoder and decoder.
    # Returns encoding time (BWT time included), decoding time (BWT time included) and total time
    title = name + " encoding and decoding with BWT"
    if not include_BWT_time:
        title += " (time not included)"
    print(title)
    #print(f'Input: {text}')
    # BWT transformation
    transformed, BWTtimeT = runBWT(BWT_class, text)
    #print(f'BWT: {transformed}')
    # Encoder
    encoded, encoderTime = runEncoder(encoder, transformed)
    #print("Encoded:", encoded)
    # Decoder
    decoded, decoderTime = runDecoder(decoder, encoded)
    #print("Decoded:", decoded)
    # BWT inversion
    original, BWTtimeI = runInverseBWT(decoded)
    #print(f'Inverted: {original}')
    print(f'Correct: {text == original}')
    # time with BWT, both encoding and decoding
    if not include_BWT_time:
        # don't include time taken to BWT
        BWTtimeT = 0
        BWTtimeI = 0
    print(f'Encoding time: {BWTtimeT + encoderTime};\n'
          f'Decoding time: {decoderTime + BWTtimeI};\n'
          f'Total time   : {BWTtimeT + encoderTime + decoderTime + BWTtimeI}\n')
    # returns encoding, decoding and total time
    return BWTtimeT + encoderTime, decoderTime + BWTtimeI, BWTtimeT + encoderTime + decoderTime + BWTtimeI

def runWithoutBWT(encoder, decoder, text, name=""):
    # Runs endcoder and decoder.
    # Returns encoding time, decoding time and total time
    print(name + " encoding and decoding without BWT")
    #print(f'Input: {text}')
    # Encoder
    encoded, encoderTime = runEncoder(encoder, text)
    #print("Encoded:", encoded)
    # Decoder
    decoded, decoderTime = runDecoder(decoder, encoded)
    #print(f'Decoded: {decoded}')
    print(f'Correct: {text == decoded}')
    # time with BWT, both encoding and decoding
    print(f'Encoding time: {encoderTime};\n'
          f'Decoding time: {decoderTime};\n'
          f'Total time   : {encoderTime + decoderTime}\n')
    # returns encoding, decoding and total time
    return encoderTime, decoderTime, encoderTime + decoderTime


def runBothCompressorsMultiple(minTextSize, maxTextSize, points):
    results = dict()
    print("Running multiple tests with different text sizes.")
    for i in range(minTextSize, maxTextSize, int((maxTextSize)/points)):
        text = ''.join(choices(ascii_letters, k=i))
        print(f'Strings size: {len(text)}')
        for comp in [(encode, decode, "Huffman"), (LZ77_encode, LZ77_decode, "LZ77")]:
            encoderTimeNoBWT, decoderTimeNoBWT, totalNoBWT = runWithoutBWT(comp[0], comp[1], text, name=comp[2])
            encoderTimeBWTMinus, decoderTimeBWTMinus, totalBWTminus = runWithBWT(BWTSuffixesIndexes, comp[0], comp[1], text, include_BWT_time=False, name=comp[2])
            encoderTimeBWT, decoderTimeBWT, totalBWT = runWithBWT(BWTSuffixesIndexes, comp[0], comp[1], text, name=comp[2])
            res = {"compressor": comp[2],
                   "without BWT": (encoderTimeNoBWT, decoderTimeNoBWT, totalNoBWT),
                   "with BWT -": (encoderTimeBWTMinus, decoderTimeBWTMinus, totalBWTminus),
                   "with BWT": (encoderTimeBWT, decoderTimeBWT, totalBWT)}
            if i not in results:
                results[i] = [res]
            else:
                results[i].append(res)
    return results


def plotResults(results, compressors, BWTs, times, save=False):
    # compressors - what compressor results to plot, ["Huffman", "LZ77"]
    # BWT - with or without BWT, ["without BWT", "with BWT -", "with BWT"]
    # times - [0, 1, 2] = encoding, decoding, total
    timeToText = {0: "encoding", 1:"decoding", 2:"total"}

    x = list(results.keys())
    plt.figure(figsize=(10, 10))
    for comp in compressors:
        for bwt in BWTs:
            for time in times:
                y = []
                for stringSize in x:
                    for data in results[stringSize]:
                        if data["compressor"] == comp:
                            print(comp, bwt, time)
                            y.append(data[bwt][time])
                print(x)
                print(y)
                plt.plot(x, y, label=f'{comp} {bwt} {timeToText[time]}')

    #plt.figure(figsize=(10, 10))
    plt.xlabel("String size")
    plt.ylabel("Time taken (s)")
    plt.title("Execution times")
    plt.legend()
    plt.grid()
    if save:
        plt.savefig("figure.png")
    else:
        plt.show()


def runSingleText(text, mult=1):
    runWithBWT(BWTSuffixesIndexes, encoder=encode, decoder=decode, text=text*mult)
    runWithBWT(BWTSuffixesIndexes, encoder=encode, decoder=decode, text=text*mult, include_BWT_time=False)
    runWithoutBWT(encoder=encode, decoder=decode, text=text*mult)
    print("================ LZ77 ===============")
    runWithBWT(BWTSuffixesIndexes, encoder=LZ77_encode, decoder=LZ77_decode, text=text*mult)
    runWithBWT(BWTSuffixesIndexes, encoder=LZ77_encode, decoder=LZ77_decode, text=text*mult, include_BWT_time=False)
    runWithoutBWT(encoder=LZ77_encode, decoder=LZ77_decode, text=text*mult)

#runSingleText("mina elan siin, aga sina????")
#results = runBothCompressorsMultiple(10000, 100000, 10)
#print(results)
saved = {10000: [{'compressor': 'Huffman', 'without BWT': (0.002194700005929917, 0.011566400004085153, 0.01376110001001507), 'with BWT -': (0.002197599969804287, 0.012206000043079257, 0.014403600012883544), 'with BWT': (0.035279200004879385, 0.04344829998444766, 0.07872749998932704)}, {'compressor': 'LZ77', 'without BWT': (0.028758600004948676, 0.011196799983736128, 0.0399553999886848), 'with BWT -': (0.02903500001411885, 0.010986999957822263, 0.040021999971941113), 'with BWT': (0.06006869999691844, 0.041221799969207495, 0.10129049996612594)}], 20000: [{'compressor': 'Huffman', 'without BWT': (0.004384399973787367, 0.024699000001419336, 0.029083399975206703), 'with BWT -': (0.004711900022812188, 0.024980399990454316, 0.029692300013266504), 'with BWT': (0.12804370000958443, 0.14764479995938018, 0.2756884999689646)}, {'compressor': 'LZ77', 'without BWT': (0.07148720003897324, 0.022820000012870878, 0.09430720005184412), 'with BWT -': (0.06999119999818504, 0.023026000009849668, 0.0930172000080347), 'with BWT': (0.18869590002577752, 0.1341667000669986, 0.3228626000927761)}], 30000: [{'compressor': 'Huffman', 'without BWT': (0.006883300025947392, 0.037051299994345754, 0.043934600020293146), 'with BWT -': (0.007448400021530688, 0.038280999986454844, 0.04572940000798553), 'with BWT': (0.4541628999868408, 0.29271290003089234, 0.7468758000177331)}, {'compressor': 'LZ77', 'without BWT': (0.12874590000137687, 0.03223919996526092, 0.1609850999666378), 'with BWT -': (0.11904859996866435, 0.03189280000515282, 0.15094139997381717), 'with BWT': (0.546851199993398, 0.27822629996808246, 0.8250774999614805)}], 40000: [{'compressor': 'Huffman', 'without BWT': (0.009296100004576147, 0.048262500029522926, 0.05755860003409907), 'with BWT -': (0.011018900026101619, 0.0492005999549292, 0.06021949998103082), 'with BWT': (1.5835871999734081, 0.5171129000373185, 2.1007001000107266)}, {'compressor': 'LZ77', 'without BWT': (0.18054050003411248, 0.041830900008790195, 0.22237140004290268), 'with BWT -': (0.18155159999150783, 0.04144459997769445, 0.22299619996920228), 'with BWT': (1.7185664999997243, 0.4798784999875352, 2.1984449999872595)}], 50000: [{'compressor': 'Huffman', 'without BWT': (0.01261279999744147, 0.06069730001036078, 0.07331010000780225), 'with BWT -': (0.014476499985903502, 0.05984180001541972, 0.07431830000132322), 'with BWT': (3.5152384000248276, 0.7795817000442185, 4.294820100069046)}, {'compressor': 'LZ77', 'without BWT': (0.2551288999966346, 0.051144500030204654, 0.3062734000268392), 'with BWT -': (0.2581301999744028, 0.05135860003065318, 0.30948880000505596), 'with BWT': (3.7597423000261188, 0.7533272000728175, 4.513069500098936)}], 60000: [{'compressor': 'Huffman', 'without BWT': (0.01673909998498857, 0.07175989996176213, 0.0884989999467507), 'with BWT -': (0.022723800037056208, 0.071529200009536, 0.0942530000465922), 'with BWT': (5.95409389998531, 1.1096235000295565, 7.063717400014866)}, {'compressor': 'LZ77', 'without BWT': (0.3498919999692589, 0.06206989998463541, 0.4119618999538943), 'with BWT -': (0.3530142999952659, 0.061437099997419864, 0.41445139999268577), 'with BWT': (6.3308960000867955, 1.0692618999746628, 7.400157900061458)}], 70000: [{'compressor': 'Huffman', 'without BWT': (0.02036170003702864, 0.08319160004612058, 0.10355330008314922), 'with BWT -': (0.030944099999032915, 0.08224079996580258, 0.1131848999648355), 'with BWT': (9.247352699982002, 1.487279299995862, 10.734631999977864)}, {'compressor': 'LZ77', 'without BWT': (0.4623559999745339, 0.0725329999695532, 0.5348889999440871), 'with BWT -': (0.4704662000294775, 0.07122409995645285, 0.5416902999859303), 'with BWT': (9.60766209999565, 1.4422533999895677, 11.049915499985218)}], 80000: [{'compressor': 'Huffman', 'without BWT': (0.026533299998845905, 0.09368300001369789, 0.1202163000125438), 'with BWT -': (0.03751840000040829, 0.09502740000607446, 0.13254580000648275), 'with BWT': (13.163915199926123, 1.9450536000076681, 15.108968799933791)}, {'compressor': 'LZ77', 'without BWT': (0.5915082000428811, 0.08260750002227724, 0.6741157000651583), 'with BWT -': (0.6018076000036672, 0.08080060000065714, 0.6826082000043243), 'with BWT': (13.682090800022706, 1.8824699000106193, 15.564560700033326)}], 90000: [{'compressor': 'Huffman', 'without BWT': (0.031201800040435046, 0.10577179997926578, 0.13697360001970083), 'with BWT -': (0.0477682999917306, 0.10530569998081774, 0.15307399997254834), 'with BWT': (17.70251030003419, 2.4508654000237584, 20.15337570005795)}, {'compressor': 'LZ77', 'without BWT': (0.7354343999759294, 0.09291499998653308, 0.8283493999624625), 'with BWT -': (0.752501700015273, 0.09163069998612627, 0.8441324000013992), 'with BWT': (18.354488200042397, 2.3841525000170805, 20.738640700059477)}]}
#plotResults(saved, compressors=["Huffman", "LZ77"], BWTs=["without BWT", "with BWT -", "with BWT"], times=[0, 1, 2])
plotResults(saved, compressors=["Huffman"], BWTs=["without BWT", "with BWT -", "with BWT"], times=[2])
plotResults(saved, compressors=["LZ77"], BWTs=["without BWT", "with BWT -", "with BWT"], times=[2], save=True)

text = "Banana"
enc = LZ77_encode(text, 20)
print(enc)
dec = LZ77_decode(enc)
print(dec)
print(text == dec)
print(text, dec)
print(len(text), len(dec))
