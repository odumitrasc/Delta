import pandas as pd
import re

articles = []
numOfWordsPerArticle = []
wordsThatAreNumbersPerArticle = []
percentageOfNumberWordsInArticle = []

#reading lines from simple article file
#and doing our opperations on each line(article)
with open('simple-20160801-1-article-per-line', 'rb') as fp:
    for line in fp:
        articles.append(line.decode("utf-8"))
        xWords = len(str(line).split(" "))
        numOfWordsPerArticle.append(xWords)
        xNumWords = len(re.findall(r"\s[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\s", str(line)))
        wordsThatAreNumbersPerArticle.append(xNumWords)
        percentage = ((xNumWords/xWords)*100) if xWords != 0 else 0
        percentageOfNumberWordsInArticle.append(percentage)

#creating dictionary
data = {"Articles": articles,
        "Words/Article": numOfWordsPerArticle,
        "Words that are Numbers/Article": wordsThatAreNumbersPerArticle,
        "% of \"Number Words\"/Article": percentageOfNumberWordsInArticle}

#creating dataframe
dataFrame = pd.DataFrame(data, columns=['Articles',
                                        'Words/Article',
                                        'Words that are Numbers/Article',
                                        '% of \"Number Words\"/Article'])

#sorting data frame according to values in % column
dataFrame = dataFrame.sort_values('% of \"Number Words\"/Article')
#writing to xlsx file
writer = pd.ExcelWriter("resultsDataFrame.xlsx", engine='xlsxwriter')
dataFrame.to_excel(writer, sheet_name='Sheet1', index=False)
writer.save()

#Showing the results of our calculations
print("Maximum % of \"number words\"/Article: ", max(dataFrame['% of \"Number Words\"/Article']))
articlesWithNoNumWords = len(dataFrame[dataFrame['% of \"Number Words\"/Article'] == 0])
allArticles = len(dataFrame['% of \"Number Words\"/Article'])
print("% of articles with no \"number words\": ", (articlesWithNoNumWords/allArticles)*100)