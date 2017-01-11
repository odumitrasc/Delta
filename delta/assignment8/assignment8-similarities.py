import pandas as pd
import collections
import math


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
    article = df1.get_value(i, 'text').lower().split()
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