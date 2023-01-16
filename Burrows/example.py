from BWTs import BWTSuffixes, invertTransformFaster, BWTSuffixes2, BWTSuffixesIndexes

BWT = BWTSuffixesIndexes()
text = "banana"
print(f'Input: {text}')
transformed = BWT.transform(text)
print(f'Transformed: {transformed}')
inverted = invertTransformFaster(transformed)
print(f'Inverted: {inverted}')