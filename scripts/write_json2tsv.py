from __future__ import print_function
from __future__ import division
import os
from os.path import join
import numpy as np
import pandas as pd
import json

"""
Combine the raw data files for all subjects into
single master dataframe.

Save output in data/groupResults/allSubjsRaw.tsv
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
        subj_df = pd.DataFrame({})      # empty dataframe to store subject data
        print('reading subject {}'.format(subjID))

        # read the subject's raw data file
        with open(join(data_dir, subjID, (subjID + '_output.json'))) as datafile:
            rawData = json.load(datafile)

        # loop over all trials for this subject
        nTrials = len(rawData['taskData'])      # total trials
        for t in np.arange(nTrials):

            # grab the data for this trial only
            trial = rawData['taskData'][t]
            stimName = trial['stimName']

            # get all 'gaze' data, translate w/r/t image origin on canvas
            imgOrigin = trial['imgOrigin']
            x = np.asarray(trial['imgGaze']['x'], dtype=int) - float(imgOrigin[0])
            y = np.asarray(trial['imgGaze']['y'], dtype=int) - float(imgOrigin[1])

            # get timestamps
            ts = np.asarray(trial['imgGaze']['ts'], dtype=int)

            # put it all together into a dataframe
            trial_df = pd.DataFrame({'ts':ts, 'x':x, 'y':y})
            trial_df['subjID'] = subjID
            trial_df['stim'] = stimName
            trial_df['trialNum'] = trial['trialNum']

            # add trial_df to subject dataframe
            subj_df = pd.concat([subj_df, trial_df])

        # write to disk
        subj_df.to_csv(join(data_dir, f, (f + '_data.tsv')), sep='\t', index=False)
