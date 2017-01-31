import random
import json
import matplotlib.pyplot as plt
import numpy as np

def calcGini(ls):
    numerator  = np.sum(np.abs(np.subtract.outer(ls, ls)))
    denominator = 2 * len(ls) * np.sum(ls)
    
    gini = numerator/denominator
    
    return gini

def generateChineseRestaurant(customers):
    # First customer always sits at the first table
    tables = [1]
    
    #customerChances = [1]
    giniCoefficients = []
    
    #for all other customers do
    for cust in range(2, customers+1):
            # rand between 0 and 1
            rand = random.random()
            # Total probability to sit at a table
            prob = 0
            # No table found yet
            table_found = False
            # Iterate over tables
            for table, guests in enumerate(tables):
                # calc probability for actual table and add it to total probability
                prob += guests / (cust)
                # If rand is smaller than the current total prob., customer will sit down at current table
                if rand < prob:
                    #customerChances.append(prob)
                    # incr. #customers for that table
                    tables[table] += 1
                    # customer has found table
                    table_found = True
                    # no more tables need to be iterated, break out for loop
                    break
                
            # If table iteration is over and no table was found, open new table
            if not table_found:
                #customerChances.append(1)
                tables.append(1)
                
            giniCoefficients.append(calcGini(tables))
                
    return tables, giniCoefficients

restaurants = 1000

giniCoef = list()

giniCoefs = list()
networks = list()

for i in range(5):
    network, giniCoef = generateChineseRestaurant(restaurants)
    
    networks.append(network)
    giniCoefs.append(giniCoef)


with open('network_' + str(restaurants) + '.json', 'w') as out:
    json.dump(network, out)
    
    
plt.plot(range(np.size(giniCoefs[0])), giniCoefs[0], label='1st run')
plt.plot(range(np.size(giniCoefs[0])), giniCoefs[1], label='2nd run')
plt.plot(range(np.size(giniCoefs[0])), giniCoefs[2], label='3rd run')
plt.plot(range(np.size(giniCoefs[0])), giniCoefs[3], label='4th run')
plt.plot(range(np.size(giniCoefs[0])), giniCoefs[4], label='5th run')
plt.xlabel("Number Of Customers")
plt.ylabel("Gini Coefficient G")
plt.legend()
plt.show()
