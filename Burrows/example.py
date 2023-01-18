from BWTs import BWTSuffixes, invertTransformFaster, BWTSuffixes2, BWTSuffixesIndexes, invertTransformFasterWindow

BWT = BWTSuffixesIndexes()
text = "AATCGCTAGGATCCTAATCGCTAGTCCG"
print(f'Input: {text}')
transformed = BWT.transformWindow(text, 2)
print(f'Transformed: {transformed}')
inverted = invertTransformFasterWindow(transformed, 2)
print(f'Inverted: {inverted}')
print(text == inverted)

