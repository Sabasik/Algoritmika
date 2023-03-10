from BWTs import BWTSuffixes, invertTransformFaster, BWTSuffixes2, BWTSuffixesIndexes, invertTransformFasterWindow, runBWTonFile, reverseBWTonFile

BWT = BWTSuffixesIndexes()
text = "AATCGCTAGGATCCTAATCGCTAGTCCG"

print(f'Input: {text}')
transformed = BWT.transformWindow(text, 100)
print(f'Transformed: {transformed}')
inverted = invertTransformFasterWindow(transformed, 100)
print(f'Inverted: {inverted}')
print(text == inverted)
print(len(text), len(transformed))
print()


