import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt

def avgUserEntropyPerDay(users):
    total = len(users)
    sum = 0
    for user in users:
        sum += userEntropy(users[user])
    return sum/total

def userEntropy(user):
    sum = 0
    entropy = 0
    for tag in user:
        sum += len(tag)
    for tag in user:
        entropy -= (len(tag)/sum) * math.log2(len(tag)/sum)
    return entropy


def systemEntropy(date):
    sum = 0
    entropy = 0
    for tag in date:
        sum += date[tag]
    for tag in date:
        entropy -= (date[tag]/sum) * math.log2(date[tag]/sum)
    return entropy

data = pd.read_table("onlyhash.data", names=["user","date","hashtag"])
data.head()

datesUsersHashtags = dict()
datesSystemHashtag = dict()

for date in data["date"]:
    datesUsersHashtags[date] = dict()
    datesSystemHashtag[date] = dict()

for i in range(len(data.values)):
    user = data.values[i][0]
    date = data.values[i][1]
    if user not in datesUsersHashtags[date]:
        datesUsersHashtags[date][user] = dict()
    hashtags = data.values[i][2].split(" ")
    for hashtag in hashtags:
        # for users
        if hashtag not in datesUsersHashtags[date][user]:
            datesUsersHashtags[date][user][hashtag] = 0
        datesUsersHashtags[date][user][hashtag] += 1
        # for system
        if hashtag not in datesSystemHashtag[date]:
            datesSystemHashtag[date][hashtag] = 0
        datesSystemHashtag[date][hashtag] += 1

entropyPerDayUser = dict()
entropyPerDaySystem = dict()

for date in datesUsersHashtags:
    entropyPerDayUser[date] = avgUserEntropyPerDay(datesUsersHashtags[date])
    entropyPerDaySystem[date] = systemEntropy(datesSystemHashtag[date])

x = [x for x in range(0, len(entropyPerDayUser))]
yUser = list(entropyPerDayUser.values())

ySystem = sorted(list(entropyPerDaySystem.values()))

plt.title(" Average User Entropy Per Day and System Entropy Sorted")
plt.xticks(np.arange(0, max(x), 40))
plt.yticks(range(0,int(max(ySystem)+1)))
plt.xlabel("Days Rank")
plt.ylabel("Entropy")
plt.scatter(x, yUser, color = 'r')
plt.scatter(x, ySystem, color = 'b')
plt.show()
