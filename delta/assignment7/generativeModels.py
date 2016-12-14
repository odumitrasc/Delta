# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 18:34:18 2016

@author: Omar K. Aly
"""

import collections
import numpy as np

file = open('simple-20160801-1-article-per-line', 'rb')
simpleEnglishWiki = file.read()

#print(type(simpleEnglishWiki))
countingResult = collections.Counter(str(simpleEnglishWiki))

totNumOfChars = sum(countingResult.values())

probsFile = open('probabilities.py.txt', 'r')
probs = probsFile.read()
probs = probs.split("\n")
zipf_probabilities = eval(probs[0].split("=")[1])
uniform_probabilities = eval(probs[2].split("=")[1])

zipfLetters = list(zipf_probabilities.keys())
zipfProbs = np.fromiter(iter(zipf_probabilities.values()), dtype=float)
zipfCDF = np.cumsum(zipfProbs)

uniformLetters = list(uniform_probabilities.keys())
uniformProbs = np.fromiter(iter(uniform_probabilities.values()), dtype=float)
uniformCDF = np.cumsum(uniformProbs)


zipfFile = open("zipfText.txt", "w")
uniformFile = open("uniformText.txt", "w")


zipfFile.write("".join(zipfLetters[np.argmax(zipfCDF > np.random.random())] for i in range(totNumOfChars)))	
uniformFile.write("".join(uniformLetters[np.argmax(uniformCDF > np.random.random())] for i in range(totNumOfChars)))
