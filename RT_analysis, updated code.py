# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 16:45:05 2021

@author: allip
"""

#The structure of this code is copied from Adam Bricker. Some changes have been done to 
#make this program work with the specific Go/No-go experiment I created.
#While performing this data-analysis I received help from Lauri Hälinen.

import pandas as pd
import matplotlib.pyplot as plt
import math
from statistics import mean, stdev
from os import listdir
from statsmodels.stats.anova import AnovaRM
from scipy.stats import ttest_ind
from scipy.stats import norm



##import data
dataPath = "data_group/"
fileList = listdir(dataPath)
#For testing if the files open correctly -> print(fileList)

#data frame for mean RTs
meanRTs = pd.DataFrame({"participant" : [], "mask" : [], "mean RT" : []})

counter = 0
for dataFile in fileList:
    #New ID for each participant
    counter += 1
    pNum = "P-" + str(counter)
    rawData = pd.read_csv(dataPath + dataFile)

    expData = pd.DataFrame(rawData, columns = ["condition", "response", "mask", "key_resp_2.keys", "key_resp_2.rt", "key_resp_3.keys", "key_resp_3.rt"])

    expData = expData.rename(columns = {"key_resp_2.keys" : "un_resp", "key_resp_2.rt" : "un_RT", "key_resp_3.keys" : "ma_resp", "key_resp_3.rt" : "ma_RT"})
    #For testing purposes ->  print(expData)
    
    #only include trials with a response
    unRT  = expData[expData.un_RT.notnull()].un_RT
    maRT  = expData[expData.ma_RT.notnull()].ma_RT
   

    meanRTsList = [mean(unRT), mean(maRT)]
    #for testing purposes -> print(meanRTsList)
    
    pNumList = [pNum, pNum]
    maskList = ["unmasked", "masked"]
    
    
    newLines = pd.DataFrame({"participant" : pNumList, "mask" : maskList, "mean RT" : meanRTsList})

    #append newLines to meanRTs
    #(note: unlike appending a list, this doesn't change the initial data frame)
    meanRTs = meanRTs.append(newLines, ignore_index=True) #don't want index duplicates

print(meanRTs)



#group means
unmasked_means = meanRTs[meanRTs["mask"] == "unmasked"]["mean RT"]
masked_means = meanRTs[meanRTs["mask"] == "masked"]["mean RT"]


#T-test to compare group means between the masked and unmasked conditions.
t_test = ttest_ind(unmasked_means, masked_means)
#print(expData["ma_RT"].to_numpy())
print(t_test)

#Means and standard deviation for umasked and masked conditions:
print("This is the mean of unmasked trials:", mean(unmasked_means))
print("This is the standard devation of unmasked trials:", stdev(unmasked_means))
print("This is the mean of masked trials:", mean(masked_means))
print("This is the standard devation of masked trials:", stdev(masked_means))




#vizualizing the masked and unmasked conditions with a boxplot.
fig, ax = plt.subplots()

box = ax.boxplot([unmasked_means, masked_means])

ax.set_ylabel("RT (s)")
ax.set_xticklabels(["Unmasked", "Masked"])

plt.show()