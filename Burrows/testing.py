from BWTs import BWTNaive, BWTSuffixes, BWTSuffixes2, BWTSuffixesIndexes
from BWTs import invertTransform, invertTransformFaster
from time import perf_counter
from random import choices
from string import ascii_letters
import matplotlib.pyplot as plt


def simpleTest(BWT_class, text):
    BWT = BWT_class()
    print("--- " + BWT.getName() + " ---")
    #print(f'Input: {text}')
    start = perf_counter()
    transformed = BWT.transform(text)
    tTime = perf_counter() - start
    #print(f'BWT: {transformed}')
    start = perf_counter()
    original = invertTransformFaster(transformed)
    iTime = perf_counter() - start
    #print(f'Inverted: {original}')
    print(f'Correct: {text == original}')
    print(f'Transform time: {tTime}; Invert time: {iTime}\n')
    return tTime, iTime


def multipleTests(classes, minTextSize, maxTextSize, points):
    results = dict()
    print("Running multiple tests with different text sizes.")
    for i in range(minTextSize, maxTextSize, int((maxTextSize)/points)):
        text = ''.join(choices(ascii_letters, k=i))
        print(f'Strings size: {len(text)}')
        for BWT_class in classes:
            tTime, iTime = simpleTest(BWT_class, text)
            if i not in results:
                results[i] = [(BWT_class().getName(), tTime, iTime)]
            else:
                results[i].append((BWT_class().getName(), tTime, iTime))
    return results

def plotResults(results, save=False):
    x = list(results.keys())
    tTimes = [[-1] for _ in range(len(results[x[0]]))]
    iTimes = [[-1] for _ in range(len(results[x[0]]))]
    for size in x:
        times = results[size]
        for i in range(len(times)):
            tTimes[i].append(times[i][1])
            iTimes[i].append(times[i][2])

    plt.figure(figsize=(10, 10))
    for j in range(len(tTimes)):
        plt.plot(x, tTimes[j][1:], label=results[x[0]][j][0] + " transform")
    plt.plot(x, iTimes[0][1:], label="Invert")
    plt.xlabel("String size")
    plt.ylabel("Time taken (s)")
    plt.title("Execution times")
    plt.legend()
    plt.grid()
    if save:
        plt.savefig("figure.png")
    else:
        plt.show()


#N = 89200
#text = ''.join(choices(ascii_letters, k=N))
#simpleTest(BWTNaive, text)
#simpleTest(BWTSuffixes, text)
#simpleTest(BWTSuffixes2, text)
#simpleTest(BWTSuffixesIndexes, text)


results = multipleTests([BWTNaive, BWTSuffixes, BWTSuffixes2, BWTSuffixesIndexes], 10000, 100000, 10)
print(results)
plotResults(results, save=True)


