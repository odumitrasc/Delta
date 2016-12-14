# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 16:08:57 2016

@author: Omar K. Aly
"""

import matplotlib.pyplot as plt
import collections
import numpy as np

simplEngWikiFile = open("simple-20160801-1-article-per-line", "rb")
smplEngWiki = simplEngWikiFile.read()
wrdsSEW = smplEngWiki.decode("ascii", "ignore").split()
wrdsFreqSEW = collections.Counter(wrdsSEW)
wrdsCntSEW = len(wrdsSEW)


zipfTextFile = open("zipfText.txt", "r")
zipfText = zipfTextFile.read()
wrdsZipf = zipfText.split()
wrdsFreqZipf = collections.Counter(wrdsZipf)
wrdsCntZipf = len(wrdsZipf)

uniformTextFile = open("uniformText.txt", "r")
uniformText = uniformTextFile.read()
wrdsUniform = uniformText.split()
wrdsFreqUniform = collections.Counter(wrdsUniform)
wrdsCntUniform = len(wrdsUniform)

frequencySEW = sorted(wrdsFreqSEW.values(), reverse=True)
wrdsProbSEW = np.array([(x/wrdsCntSEW) for x in frequencySEW])
wrdsCDFSEW = np.cumsum(wrdsProbSEW)
rankSEW = list(range(len(frequencySEW)))

frequencyZipf = sorted(wrdsFreqZipf.values(), reverse=True)
wrdsProbZipf = np.array([(x/wrdsCntZipf) for x in frequencyZipf])
wrdsCDFZipf = np.cumsum(wrdsProbZipf)
rankZipf = list(range(len(frequencyZipf)))

frequencyUniform = sorted(wrdsFreqUniform.values(), reverse=True)
wrdsProbUniform = np.array([(x/wrdsCntUniform) for x in frequencyUniform])
wrdsCDFUniform = np.cumsum(wrdsProbUniform)
rankUniform = list(range(len(frequencyUniform)))


kolSmrTestSEWZipf = np.array([np.abs(wrdsCDFSEW[i]-wrdsCDFZipf[i]) for i in range(len(wrdsCDFSEW))])
zipfSEWMaxPntWiseDist = np.max(kolSmrTestSEWZipf)

kolSmrTestSEWUniform = np.array([np.abs(wrdsCDFSEW[i]- wrdsCDFUniform[i]) for i in range(len(wrdsCDFSEW))])
uniSEWMaxPntWiseDist = np.max(kolSmrTestSEWUniform)

print("SEW & zipf maximum point wise distance",str(zipfSEWMaxPntWiseDist))
print("SEW & uniform maximum point wise distance", str(uniSEWMaxPntWiseDist))

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)

ax1.loglog(rankSEW, frequencySEW, basex=10, basey=10, linestyle = 'None',
           marker='.', c='b', label="Simple English Wiki")
ax1.loglog(rankZipf, frequencyZipf, basex=10, basey=10, linestyle='None',
           marker='.', c='r', label="zipf text")
ax1.loglog(rankUniform, frequencyUniform, basex=10, basey=10, linestyle='None',
           marker='.', c='g', label = "uniform text")

ax2.plot(rankSEW, wrdsCDFSEW,
         c='b',label="SEW CDF")
ax2.plot(rankZipf, wrdsCDFZipf,
         c='r', label="zipf CDF")
ax2.plot(rankUniform, wrdsCDFUniform,
         c='g', label="uniform CDF")


ax1.set_xlabel("word rank")
ax1.set_ylabel("word frequency")
ax1.legend()

ax2.set_xlabel("word rank")
ax2.set_ylabel("CDF")
ax2.set_ylim(0,1)
ax2.set_xscale("log")
handles, labels = ax2.get_legend_handles_labels()
ax2.legend(handles, labels, loc=2)

plt.show()
