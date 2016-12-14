import random
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


def dice(n):
    total = 0
    for i in range(0, n):
        total += random.randint(1, 6)
    return total

def getSum():
    suma = list()
    for i in range(100):
        suma.append(dice(2))
    return suma

def getFreqSum(suma):
    freqSum = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}

    for i in range(0, 100):
        freqSum[suma[i]] += 1
    return freqSum

def getCDF(freq):
    cumsum = np.cumsum(freq)
    normedcumsum = [x/float(cumsum[-1]) for x in cumsum]
    return normedcumsum

suma = getSum()
freqSum = getFreqSum(suma)
# histogram with the frequencies of dice sum outcomes
plt.bar(list(freqSum.keys()), freqSum.values(), align='center', width=0.5)
plt.xticks(list(freqSum.keys()))
histogramLegend = mpatches.Patch(color='blue', label='Histogram')
plt.legend(handles=[histogramLegend], loc=5)
plt.xlabel("Sums")
plt.ylabel("Frequency")
plt.show()

cdf = getCDF(list(freqSum.values()))

cdfLegend = mpatches.Patch(color='blue', label='CDF')
medianLegend = mpatches.Patch(color='red', label='Median')
nineLegend = mpatches.Patch(color='green', label='9 mark')
plt.legend(handles=[cdfLegend, medianLegend, nineLegend], loc=4)
plt.xlabel("Sums")
plt.ylabel("Frequency")

median = np.median(suma)
medianfreq = np.median(cdf)
equalOrLessThanNine = cdf[8]

plt.axvline(median, color='b', linestyle='dashed', linewidth=2)
plt.axhline(medianfreq, color='r', linestyle='solid', linewidth=2)
plt.axhline(equalOrLessThanNine, color='g', linestyle='solid', linewidth=2)

plt.plot(list(freqSum.keys()),cdf)
plt.show()
