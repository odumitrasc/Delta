import pandas as pd
import collections
import math

import random
import operator
import itertools


def calcJaccardSimilarity(wordSet1, wordSet2):
    jaccardValue = len(wordSet1.intersection(wordSet2)) / len(wordSet1.union(wordSet2))
    return jaccardValue


def calculateCosineSimilarity(tfIdfDict1, tfIdfDict2):
    numerator = 0
    d1Len = 0
    d2Len = 0
    if len(tfIdfDict1) >= len(tfIdfDict2):
        for key in tfIdfDict1.keys():
            if key not in tfIdfDict2:
                numerator += 0
            else:
                numerator += (tfIdfDict1[key] * tfIdfDict2[key])
    else:
        for key in tfIdfDict2.keys():
            if key not in tfIdfDict1:
                numerator += 0
            else:
                numerator += (tfIdfDict1[key] * tfIdfDict2[key])

    for v in tfIdfDict1.values():
        d1Len += math.pow(v, 2)
    for v in tfIdfDict2.values():
        d2Len += math.pow(v, 2)

    return (numerator / (math.sqrt(d1Len) * math.sqrt(d2Len)))


def randomArticles(df1, count):
    articleDict = dict()
    while len(articleDict) < count:
        index = random.randint(0, len(df1['text']) - 1)
        articleDict[df1['name'][index]] = df1.get_value(index, 'text')
    return articleDict


store = pd.HDFStore('store2.h5')
df1 = store['df1']
df2 = store['df2']
store.close()
articlesWordSets = dict()
articlesWordFreq = dict()
documentWordFreq = dict()
tfidf = dict()

outLinkSets = dict()

numOfDocuments = len(df1['text'])

for i in range(numOfDocuments):
    article = df1.get_value(i, 'text').split()
    articlesWordSets[df1['name'][i]] = set(article)
    articlesWordFreq[df1['name'][i]] = collections.Counter(article)
    link = df2.get_value(i, 'out_links')
    outLinkSets[df1['name'][i]] = set(link)

for wordSet in articlesWordSets.values():
    for word in wordSet:
        if word not in documentWordFreq.keys():
            documentWordFreq[word] = 1
        else:
            documentWordFreq[word] += 1

for article in articlesWordFreq.keys():
    for term in articlesWordFreq[article].keys():
        if article not in tfidf.keys():
            tfidf[article] = {}
        tfidf[article].update(
            {term:
                 ((articlesWordFreq[article][term]) *
                  math.log(numOfDocuments / documentWordFreq[term]))})

print("Jaccard similarity for \"Germany\" & \"Europe\": ",
      str(calcJaccardSimilarity(articlesWordSets['Germany'], articlesWordSets['Europe'])))

print("Cosine similarity for \"Germany\" & \"Europe\": ",
      str(calculateCosineSimilarity(tfidf['Germany'], tfidf['Europe'])))

print("Jaccard similarity for \"Germany\" & \"Europe\" out links: ",
      str(calcJaccardSimilarity(outLinkSets['Germany'], outLinkSets['Europe'])))

numberOfArticles = 5
randomArticles = list(randomArticles(df1, numberOfArticles))
pairs = itertools.combinations(randomArticles, 2)
pairvalues = []
for pair1, pair2 in pairs:
    jac = calcJaccardSimilarity(articlesWordSets[pair1], articlesWordSets[pair2])
    cos = calculateCosineSimilarity(tfidf[pair1], tfidf[pair2])
    pairvalues.append(list([pair1, pair2, jac, cos]))

posJaccardSimilarity = []
posCosineSimilarity = []

rankJaccardSimilarity = dict()
rankCosineSimilarity = dict()

difference = dict()

for ra in randomArticles:
    # jaccard values article <->all others
    tempdictj = dict()
    tempdictc = dict()
    for pv in pairvalues:
        if pv[0] == ra:
            tempdictj[pv[1]] = pv[2]
            tempdictc[pv[1]] = pv[2]
        if pv[1] == ra:
            tempdictj[pv[0]] = pv[2]
            tempdictc[pv[1]] = pv[2]
    # jaccard values all articles <-> all others + values
    posJaccardSimilarity.append(tempdictj)
    posCosineSimilarity.append(tempdictc)

fsortedjaccard = []
fsortedcosine = []
for key in posJaccardSimilarity:
    sortedJaccard = sorted(key.items(), key=operator.itemgetter(1))
    fsortedjaccard.append(sortedJaccard)
for key in posCosineSimilarity:
    sortedCosine = sorted(key.items(), key=operator.itemgetter(1))
    fsortedcosine.append(sortedCosine)

frankedjaccard = []
for sortedJaccard in fsortedjaccard:
    index = 0
    for key, value in sortedJaccard:
        rankJaccardSimilarity[key] = index
        index += 1
    frankedjaccard.append(rankJaccardSimilarity)

frankedcosine = []
for sortedCosine in fsortedcosine:
    index = 0
    for key, value in sortedCosine:
        rankCosineSimilarity[key] = index
        index += 1
    frankedcosine.append(rankCosineSimilarity)

for i in range(0, len(frankedcosine) - 1):
    squaredDifference = 0
    for key, value in frankedcosine[i]:
        difference[key] = frankedjaccard[i][key] - value
        squaredDifference += (frankedjaccard[i][key] - value) * (
            frankedjaccard[i][key] - value)

        print("the rank correlation coefficient for" + randomArticles[i] + ": " + str(
            1 - ((6 * squaredDifference) / (numberOfArticles * (numberOfArticles * numberOfArticles - 1)))))
