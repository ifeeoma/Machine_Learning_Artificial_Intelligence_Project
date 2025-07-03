#---------Use this program to make a base X 48 feature matrix from all three timestamps----------#

import pandas as pd
import time

#list of sample numbers by folder identifier
example_list = [25,26,27,28,30,31,32,33,34,35,36,38,39,40,41,42,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60]

#initialize paths for combined file retrieval
path_25_s = '0.25s/'
path_1_s = '1s/'
path_4_s = '4s/'

start_path_list = [path_25_s, path_1_s, path_4_s]

path_f = '-WholeGenome-int.csv'

identifier_list = ['_0.25s','_1s','_4s']


for e in example_list:
    for p in range(0,len(start_path_list)):
        #concatenate path strings to pull from each exposure time.
        sample_path = start_path_list[p]+str(e)+'/'+str(e)+path_f

        example = pd.read_csv(sample_path, delimiter = ',')
        example = example.iloc[:,1:]
        example_remainder_calls = example.iloc[:,2:4]
        
        #separates the reference base and the position the first time through to reduce redundancy
        if e == example_list[0] and p == 0:
            pos_ref_frame = pd.DataFrame(example.loc[:, ['pos','Ref_base']])
            #create list of float types (aka numbers) and change dataset to a float only matrix with the parameters we care about. Once made, we can reuse headerlist as we wish. AS intensity for A starts at position 12.
            headerlist = []
            for i in range(11,example.shape[1]):
                if example.dtypes[i] == 'float64':
                    headerlist.append(i)
            print(headerlist)
            
            
        #preprocess each example before concatenation
        example = example.iloc[:, headerlist]
        example = example.add_suffix(identifier_list[p])
        if e == example_list[0] and p == 0:
            smb_gonelist =[]
            for i in range(0,example.shape[1]):
                if (i+2)%3 != 0:
                    smb_gonelist.append(i)
                    
        smb_gone_example = example.iloc[:,smb_gonelist]
        
        example_remainder_calls = example_remainder_calls.add_suffix(identifier_list[p])
        
        
        #initialize all time snapshots for the first instance, then concatenate the rest
        if p == 0:
            combo_ex = smb_gone_example
            combo_calls = example_remainder_calls
        else:
            combo_ex = pd.concat([combo_ex,smb_gone_example], axis = 1)
            combo_calls = pd.concat([combo_calls, example_remainder_calls], axis =1)
            
        example_calls = pd.concat([pos_ref_frame,combo_calls], axis = 1)
        
    full_combo = pd.concat([example_calls, combo_ex], axis = 1)
    full_string = str(e)+'_training_set_combo.csv'
    full_combo.to_csv(full_string)
