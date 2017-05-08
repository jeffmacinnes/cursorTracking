from __future__ import print_function
from __future__ import division
import os
from os.path import join
import shutil


"""
Go through every data file in the raw WBL folder, check to see if it has been
copied already. If so, cool, do nothing. If not, copy it.
"""


# Make a list of all existing raw data files
raw_WBL_dir = '../../_copy_WBL_data_here/cursorTracking'
data_dir = '../Data'
for f in os.listdir(raw_WBL_dir):
    # skip any hidden files
    if f[0] != '.':

        # subj ID is the first part of the file name
        subj_id = f.split('_')[0]

        # check if this subject has a data directory already, if not make it
        subj_dir = join(data_dir, subj_id)
        if not os.path.isdir(subj_dir):
            os.makedirs(subj_dir)

        # check if the data has been copied over already or not
        if not os.path.exists(join(subj_dir, f)):
            shutil.copy(join(raw_WBL_dir, f), join(subj_dir, f))
