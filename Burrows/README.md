Burrows wheeler transform (BWT)

Here is naive BWT implementation and multiple that use suffixes.
Also includes inversion methods, one being a lot faster than the other.

```
BWT = BWTSuffixesIndexes()
text = "banana"
print(f'Input: {text}')
transformed = BWT.transform(text)
print(f'Transformed: {transformed}')
inverted = invertTransformFaster(transformed)
print(f'Inverted: {inverted}')
```