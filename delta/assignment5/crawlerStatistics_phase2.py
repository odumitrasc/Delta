import os
import re
from urllib.parse import urlparse 
import matplotlib.pyplot as plt

def getAllUrls(file):
    urls = re.findall(r'href=[\'"]?([^\'" >]+)', str(file))
    return urls
    

extDict = dict()
intDict = dict()
extlink = []
intlink = []
for root, dirs, files in os.walk(".\simple"):
    for name in files:
        extLinkCount = 0
        intLinkCount = 0
        fileToRead = open(os.path.join(root, name), "rb")
        urllinks = getAllUrls(fileToRead.read())
        for url in urllinks:     
            if  (urlparse(url).netloc.find("simple.wikipedia.org") is -1) and (urlparse(url).netloc.find("141.26.208.82") is -1 ) and not url[0] ==".":
                extlink.append(url)
                extLinkCount += 1
            else:
                intlink.append(url)
                intLinkCount += 1
    
        extDict[name] = extLinkCount
        intDict[name] = intLinkCount

plt.scatter(list(intDict.values()), list(extDict.values()), s=list(intDict.values()))
plt.title("Number of Internal Links Vs. External Links for each page")
plt.xlabel("Internal Links")
plt.ylabel("External Links")
plt.show()


