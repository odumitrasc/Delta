import os
import re
import numpy
import matplotlib.pyplot as plt

def getAllUrls(file):
    urls = re.findall(r'href=[\'"]?([^\'" >]+)', str(file))
    return len(urls)

numOfPages = 0
resDict = dict()
for root, dirs, files in os.walk(".\simple"):
    for name in files:
        numOfPages += 1
        fileToRead = open(os.path.join(root, name), "rb")
        resDict[name] = getAllUrls(fileToRead.read())
		
print("Total Number Of Pages: ", numOfPages)
totalNumLinks =  sum(resDict.values())
print("Total Number Of Links: ", totalNumLinks)
avgNumLinksPerPage = numpy.mean(list(resDict.values()))
print("Average Number Of Links/Page: ", avgNumLinksPerPage)
medianOfNumLinksPerPage = numpy.median(numpy.array(list(resDict.values())))
print("Median Number Of Links/Page: ", medianOfNumLinksPerPage)

        
plt.hist(list(resDict.values()), bins=range(0, 150, 5))
plt.title("Distribution of links on the crawled web pages")
plt.xlabel("Number Of Links/Page")
plt.ylabel("Frequency")
plt.show()