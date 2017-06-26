from __future__ import print_function
from __future__ import division
import os
from os.path import join
import numpy as np
import pandas as pd
import json

"""
Combine the data files for all subjects into
single master dataframe.

Save output in data/groupResults/allSubjs_cursorTracking.tsv
"""

data_dir = '../data'
output_dir = join(data_dir, 'groupData')

# create list of all subjects based on folders in the data directory
subjFolders = os.listdir(data_dir)
if 'groupData' in subjFolders:
    subjFolders.remove('groupData')


# Loop through all subject directories
for f in subjFolders:
    if os.path.isdir(join(data_dir, f)):
        # the subject ID will be the name of the directory
        subjID = f
        print('adding subject {}'.format(subjID))

        # read the subject's data file
        subj_df = pd.read_table(join(data_dir, f, (f + '_data.tsv')), sep='\t')

        # add to the master (or create if necessary)
        if 'allSubj_df' not in locals():
            allSubj_df = subj_df.copy()
        else:
            allSubj_df = pd.concat([allSubj_df, subj_df])

# write the output dataframe to csv
allSubj_df.to_csv(join(output_dir, 'allSubjs_cursorTracking.tsv'), sep='\t', index=False)
