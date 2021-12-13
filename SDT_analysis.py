# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 17:19:25 2021

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


#Fonction to calculate criterion and d'-prime. Code derived from Adam Bricker.
#d' function
def dPrime(hitRate, FArate):
    stat = norm.ppf(hitRate) - norm.ppf(FArate)

    return stat

#criterion function
def criterion(hitRate, FArate):
    stat = -.5*(norm.ppf(hitRate) + norm.ppf(FArate))

    return stat

#This code for opening the csv files is derived from Daniel Suchý.
#Opening the data files in csv form from file called data_group.
dataPath = "data_group/"
csvFiles = [dataPath + file for file in listdir(dataPath) if ".csv" in file]
#print(csvFiles)

allData = pd.concat(map(pd.read_csv, csvFiles))

#Testing if the files open correctly.
#print(allData)
#print(allData.to_string()) #every entry
#print(allData.columns) #column labels

#A new data frame only with the data we need
expData = pd.DataFrame(allData, columns = ["condition", "response", "mask", "key_resp_2.keys", "key_resp_2.rt", "key_resp_3.keys", "key_resp_3.rt"])
print(expData) #for testing the data frame with the needed data.

#Renaming the needed variables.
expData = expData.rename(columns = {"key_resp_2.keys" : "un_resp", "key_resp_2.rt" : "un_RT", "key_resp_3.keys" : "ma_resp", "key_resp_3.rt" : "ma_RT"}) #un refering to unmasked condition and ma to masked condition

#The data frame we'll be using
accuracy = pd.DataFrame({"mask" : ["nan", "gabor_0_deg.png"], "hits" : [0,0], "misses" : [0,0],
                        "CRs" : [0,0], "FAs" : [0,0]})
#There are two different conditions in this experiment, unmasked and masked. The masked one uses a gabor image.


#Data frame for SDT information.

for index, row in expData.iterrows():
    #condition: non mask
    #print(row["un_resp"])
    if pd.isna(row["mask"]):#row["mask"] == "nan":
        
        rowInd = 0
        #Hit
        if row["condition"] == "go" and row["un_resp"] == "space":
            accuracy.loc[rowInd,"hits"] += 1
        #Miss
        elif row["condition"] == "go" and row["un_resp"] != "space": #row["un_resp"] == "NaN":
            accuracy.loc[rowInd,"misses"] += 1
        #Correct rejection
        elif row["condition"] == "no-go" and row["un_resp"] != "space":
            accuracy.loc[rowInd,"CRs"] += 1
        #False alarm
        elif row["condition"] == "no-go" and row["un_resp"] == "space":
            accuracy.loc[rowInd,"FAs"] += 1

    #condition: mask
    elif row["mask"] == "gabor_0_deg.png":
        rowInd = 1
        #Hit
        if row["condition"] == "go" and row["ma_resp"] == "space":
            accuracy.loc[rowInd,"hits"] += 1
        #Miss
        elif row["condition"] == "go" and row["ma_resp"] != "space":
            accuracy.loc[rowInd,"misses"] += 1
        #Correct rejection
        elif row["condition"] == "no-go" and row["ma_resp"] != "space":
            accuracy.loc[rowInd,"CRs"] += 1
        #False alarm
        elif row["condition"] == "no-go" and row["ma_resp"] == "space":
            accuracy.loc[rowInd,"FAs"] += 1


print(accuracy)
print("*" * 40) #to make the outcome print easier to read

#Calculate rates from response counts
hitRateUnmasked = accuracy.loc[0,"hits"]/320
#For testing purposes: print(hitRateUnmasked)
FArateUnmasked = accuracy.loc[0,"FAs"]/40
#For testing purposes: print(FArateUnmasked)
hitRateMasked = accuracy.loc[1,"hits"]/320
FArateMasked = (accuracy.loc[1,"FAs"]+1)/40

#Cacluate d' and criterion
print("d' (unmasked):", dPrime(hitRateUnmasked, FArateUnmasked))
print("criterion (unmasked):", criterion(hitRateUnmasked, FArateUnmasked))

print("d' (masked):", dPrime(hitRateMasked, FArateMasked))
print("criterion (masked):", criterion(hitRateMasked, FArateMasked))



