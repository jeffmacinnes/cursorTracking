from __future__ import print_function
from __future__ import division

import os
from os.path import join
import numpy as np
import pandas as pd
import argparse
import cv2

pd.options.mode.chained_assignment = None  # default='warn'


"""
Run this before combineSubjs.py

Loop through a given subject's output .tsv file. For each trial,
find the corresponding AOIs image (if any). For each "gaze" point in the trial,
determine which, if any, AOI it falls within.

assign the AOI label to a column in the orig dataframe and rewrite
"""

AOI_scaleFactor = 500/707    # scale factor between displayed sized, and AOI size


class AOIs:
    """
    Class to work with specified AOI image file, store each AOIs coordinates
    Input:  -2D ndarray containing unique AOI labels by number
        -scaleFactor: scale factor between AOI image and displayed stim size during the task
    """
    def __init__(self, AOIimage, scaleFactor):

        # calculate scale factor between AOI image and displayed image
        self.scaleFactor = scaleFactor
        self.AOI = AOIimage

        # extract the unique, nonzero, values in this AOI
        self.AOI_codes = np.unique(self.AOI[self.AOI > 0])

        #### CREATE DICT TO STORE EACH AOIS COORDS
        self.AOIs = {}				# dicitionary to store all of the AOIs and coordinates
        for val in self.AOI_codes:
            self.this_AOI = self.AOI == val 					# make a unique image for this value only
            self.Xcoords = np.where(self.this_AOI==True)[1]		# pull out x-coordinates for this AOI (NOTE: remember, (row,col) convention means (y,x))
            self.Ycoords = np.where(self.this_AOI==True)[0]		# pull out y-coordinates for this AOI
            self.coords = [(self.Xcoords[x], self.Ycoords[x]) for x in range(len(self.Xcoords))]	# convert to list of tuples

            # map values to names
            if val == 64:
            	self.AOI_name = 'rightEye'
            elif val == 128:
            	self.AOI_name = 'leftEye'
            elif val == 191:
            	self.AOI_name = 'nose'
            elif val == 255:
            	self.AOI_name = 'mouth'
            else:
            	print('AOI image has value of: ' + str(val) + '. Not found in key.')

            # store names and coordinates in dictionary (NOTE: coordinates are stored as (x,y) pairs...so: (column, row))
            self.AOIs[self.AOI_name] = self.coords


    def isAOI(self, coordinates):
        "check if the specified coordinates fall into one of the AOIs"

        # scale coordinates
        self.x = np.round(coordinates[0] * self.scaleFactor) #.astype('uint8')
        self.y = np.round(coordinates[1] * self.scaleFactor) #.astype('uint8')
        self.this_coord = (self.x, self.y)

        # loop through the AOIs in the dictionary until you find which (if any) it belongs to
        self.found_AOI = False
        for name, coords in self.AOIs.items():
            if self.this_coord in coords:
                self.AOI_label = name
                self.found_AOI = True
                break

        if not self.found_AOI:
            self.AOI_label = 'none'

        return self.AOI_label

# ===============================================================
def processSubj(subj):
    """
    load the tsv file for this subj, loop through all trials,
    submit to processTrial, write output tsv for subj
    """

    # path to subject directory
    subj_dir = join('../data', subj)

    # load the tsv
    subj_df = pd.read_table(join(subj_dir, (subj + '_data.tsv')), sep='\t')

    AOI_df = pd.DataFrame({})  # empty dataframe to write results into

    # loop through all trials
    for t in sorted(np.unique(subj_df['trialNum'])):

        # grab just the rows for this trial
        trial_df = subj_df[subj_df['trialNum'] == t]

        # submit to processTrial
        trial_df = processTrial(trial_df)

        # store results
        AOI_df = pd.concat([AOI_df, trial_df])

    # overwrite the existing datafile with this new one
    AOI_df.to_csv(join(subj_dir, (subj + '_data.tsv')), sep='\t', index=False)



def processTrial(trial_df):
    """
    take the given trial_df and first find the corresponding AOIs image
    file (if any). Load the AOIs file, create AOIs object. Loop through
    all "gaze" points for this trial, assign AOI label.

    return trial_df with AOI label column added
    """

    # get stim name for this trial
    stimPath = trial_df['stim'].iloc[0]
    stim_fname = stimPath.split('/')[-1]

    # set up AOI name
    AOI_fname = stim_fname.split('.')[0] + '_AOIs.png'
    AOI_dir = '../stimuli/AOIs'

    # check if AOI exists
    if os.path.isfile(join(AOI_dir, AOI_fname)):
        AOI_image = cv2.imread(join(AOI_dir, AOI_fname))
        AOI_image = AOI_image[:,:,0]        # take first color channel only

        # create AOIs
        theseAOIs = AOIs(AOI_image, AOI_scaleFactor)

        # figure out the AOI label for each row
        trial_df['AOI'] = trial_df.apply(
                            lambda row: theseAOIs.isAOI((row['x'], row['y'])),
                            axis=1)
    else:
        print('no AOI found for stim: {}'.format(stim_fname))
        trial_df['AOI'] = np.nan

    # return the trial_df with AOI label column appended
    return trial_df




if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('subj', help='SUBJ ID for dataset you want to assign AOIs to ("all" for all subjects in data folder)')
    args = parser.parse_args()

    # loop through all subjects
    if args.subj == 'all':
        data_dir = '../data'
        subjFolders = os.listdir(data_dir)
        if 'groupData' in subjFolders: subjFolders.remove('groupData')

        for f in subjFolders:
            if os.path.isdir(join(data_dir, f)):
                print('processing subject: {}'.format(f))
                processSubj(f)

    # or just do the one
    else:
        # submit this subject
        processSubj(args.subj)
