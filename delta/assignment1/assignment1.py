# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import random
import math
import matplotlib.pyplot as plt

#1
#first we generate 10 random numbers between 0 and 90
randNumbers = random.sample(range(0, 90), 10)

#2
#then we print the sin and cos for each number
for i in randNumbers:
    print (math.sin(i))
    print (math.cos(i))
    
#3
#we create empty lists to append sin and cos values to them
#and we use for loop to do so
#then we pring the two lists
SIN = []
COSIN = []

for i in randNumbers:
    SIN.append(math.sin(i))
    COSIN.append(math.cos(i))
    
print(SIN)
print(COSIN)

#4
#we plot results on scatter plot random numbers as x-axis
#and sin/cos values as y-axis with blue and green colors respectively
plt.scatter(randNumbers,SIN,  color="blue")
plt.scatter(randNumbers,COSIN, color="green")
    
#5
#we then label each axis and draw our legend
plt.xlabel('Random Generated Numbers')
plt.ylabel('SIN / COS Values')
plt.legend(["SIN", "COS"])