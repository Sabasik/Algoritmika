import numpy as np
from functools import partial
# Need for bigger BurrowsWheelerTransformRadix inputs
#import sys
#sys.setrecursionlimit(3000)


class BWTNaive:
    # Default naive version.
    # Create and sort all rotations of the text.
    # Referenced: https://en.wikipedia.org/wiki/Burrows–Wheeler_transform

    def getName(self):
        return "Naive BWT"

    def transform(self, text):
        text += "\003"
        rotations = [text[i:] + text[:i] for i in range(len(text))]
        rotationsSorted = sorted(rotations)
        last_col = "".join([rotation[-1] for rotation in rotationsSorted])
        return last_col


class BWTSuffixes:
    # BWT using suffixes of given text
    # Reference: https://github.com/egonelbre/fm-index/blob/master/src/bwt.py

    def getName(self):
        return "Suffixes BWT"

    def transform(self, text):
        text += "\003"
        rotations = sorted(text[i:] for i in range(len(text)))
        suffixesCount = len(rotations)
        transformed = [""] * suffixesCount
        for i in range(suffixesCount):
            suffixLength = len(rotations[i])
            if suffixLength == suffixesCount:
                transformed[i] = "\003"
            else:
                transformed[i] = text[-suffixLength-1]
        return "".join(transformed)

class BWTSuffixes2:
    # BWT using suffixes of given text
    # Might be a bit faster than BWTSuffixes
    # Reference: https://github.com/dabane-ghassan/dnazip/blob/08ea951782fb3d4bfe50adc23485c88c7f0a6f10/dnazip/burros_wheeler.py#L167

    def getName(self):
        return "Suffixes BWT 2"

    def transform(self, text):
        text += "\003"
        suff_arr = []
        for i in range(0, len(text)):
            suff_arr.append((text[i:], i))
        arrSorted = sorted(suff_arr)
        bwt = []
        for suff in arrSorted:
            i = suff[1]  # The suffix's index is the 2nd element in the tuple
            if i == 0:
                bwt.append("\003")
            else:
                bwt.append(text[i - 1])

        return ''.join(bwt)

class BWTSuffixesIndexes:
    # BWT using suffixes of given text, but not saving whole table as a variable
    # Might be a bit faster than BWTSuffixes
    # Reference: https://stackoverflow.com/questions/51839722/memory-efficient-sorting-with-key

    def getName(self):
        return "Suffixes Indexes BWT"

    def transform(self, text):
        text += "\003"
        ids = [i for i in range(len(text))]
        ids.sort(key=lambda i: text[i:])
        res = ""
        for i in ids:
            if text[:i]:
                res += text[:i][-1]
            else:
                res += "\003"
        return res


def invertTransform(BFT_text):
    # It gets quite slow with larger texts.
    # "ban"*1000 took 4.5 seconds
    # Referenced: https://en.wikipedia.org/wiki/Burrows–Wheeler_transform
    table = [""] * len(BFT_text)
    for i in range(len(BFT_text)):
        table = sorted(BFT_text[i] + table[i] for i in range(len(BFT_text)))
    s = [row for row in table if row.endswith("\003")][0]
    return s[:-1]


def _getIndexes(text):
    indexes = dict()
    for i, char in enumerate(text):
        if char in indexes:
            indexes[char].append(i)
        else:
            indexes[char] = [i]
    return indexes


def invertTransformFaster(BFT_text):
    # Faster method. "ban"*1000 took 0.04 seconds.
    inverted = ""
    firstCol = []
    firstCol.extend(BFT_text)
    firstCol = sorted(firstCol)
    lastCol = []
    lastCol.extend(BFT_text)
    firstColIndexes = _getIndexes(firstCol)
    lastColIndexes = _getIndexes(lastCol)
    idx = lastCol.index("\003")
    for i in range(len(BFT_text) - 1):
        char = firstCol[idx]
        inverted += char
        idxs = firstColIndexes[char]
        for j in range(len(idxs)):  # finding n'th x character first column
            newIdx = 0
            if idxs[j] == idx:
                newIdx = j
                break
        # finding n'th x character in last column
        idx = lastColIndexes[char][newIdx]
    return inverted

