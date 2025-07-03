#reading json file with python
#need this to read json files
import json

#these are used for data structure creation
import numpy as np
import pandas as pd

#define all functions for use now, to be used later.
#defining a function to get the variable names into a workable list
def getList(dict):
        list = []
        for key in dict.keys():
                list.append(key)
        return list
        
#loop over all directories to make an array of all WholeGenome data. this file needs to be in the same directory as the numbered directories for this code to work



#i think you have to initialize data first to use it in the loop below.
data=[]
#initialize data variables to for the for loop later
main_data = [None]*len(range(0,11))
antisense = [None]*len(range(0,4))**2
sense = [None]*len(range(0,4))**2

#samplenumbers are all the samples that we are pulling data from [25-??] its in the directory
SampleNumbers = list(range(30,37))+list(range(38,45))+list(range(46,61))
for z in SampleNumbers:
    t=open(str(z)+"/WholeGenome-int.json")
        
        #this makes "data" your json file in the numbered directory. Access this list and the lists/dictionaries inside to fill out the data table for csv file.
    data = json.load(t)
        
        #access keys of json file
    keys_data=data[0]
        #access keys of the key antisense since this is embedded in json file list.
    keys_AS=data[0]["antisense"][0]

        #writing values as a list. Lists are easier to put into pandas data frame (i think)
    inner_keys_as_list=getList(keys_AS)
    keys_as_list=getList(keys_data)
        
    listholder = [None]*len(inner_keys_as_list)
    innerlistholder = [None]*(len(inner_keys_as_list))**2*2
    base_list = ["A", "T", "C", "G"]
#finalizing the identifiers for the array in a list

    for j in range(0,len(inner_keys_as_list)):
        for k in range(0, len(base_list)):
            innerlistholder[4*j+k] = "AS_"+base_list[j]+"_"+inner_keys_as_list[k]
            innerlistholder[4*j+k+16]="S_"+base_list[j]+"_"+inner_keys_as_list[k]


#concatenating the lists together and removing redundant keys
    keys_as_list  = keys_as_list+innerlistholder

#I am removing the redundant sense and antisense features from the keys list. The keys that would follow are all antisense and sense anyway and I already relabelled them above in the for loop starting at line 50.
    keys_as_list.remove("antisense")
    keys_as_list.remove("sense")

#This needs to be done for EACH position it loops over the length of data from position 13 to the final position I start this loop now because we dont need this loop for the keys_as_list identifiers

    #initialize an empty list for df creation
    final_list = []
    print(z)
    for h in range(0, len(data)):
        #filling out list of results for each position, if the number of keys we use in keys_as_list changes then that number 11 has to change too
        for i in range(0, 11):
            main_data[i]=data[h][keys_as_list[i]]
        #this will fill out all 32 (4x4+4x4) data points in the sense and antisense strains
        for j in range(0,4):
            for k in range(0,4):
                antisense[4*j+k]=data[h]["antisense"][j][inner_keys_as_list[k]]

        for j in range(0,4):
            for k in range(0,4):
                sense[4*j+k] = data[h]["sense"][j][inner_keys_as_list[k]]
#this concatenates the three lists to make one final list of the values at each key
        results_per_position = main_data+antisense+sense
        final_list.append(results_per_position)
#this is a final data frame using pandas that has the column headers as the keys and the data within by position
    final_list=pd.DataFrame(final_list, columns = keys_as_list)
    
#confirms the expected size
    print(final_list.shape)
#saves the files into the directories as csv files
    final_list.to_csv(str(z)+'//' +str(z)+'-'+'WholeGenome-int.csv')

#files to check on: 45 in 1s


        



