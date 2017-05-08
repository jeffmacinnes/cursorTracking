from __future__ import print_function
from __future__ import division
import os
from os.path import join
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import argparse
import json



def processSubj(subj):
    """
    Setup output dirs, submit each trial
    """

    subj_dir = join('../data', subj)

    # make the plot output directory, if necessary
    plot_dir = join(subj_dir, 'plots')
    if not os.path.isdir(plot_dir):
        os.makedirs(plot_dir)

    # read the subjects raw json datafile
    with open(join(subj_dir, (subj + "_output.json"))) as datafile:
        rawData = json.load(datafile)

    # total trials
    nTrials = len(rawData['taskData'])

    # loop through each trial, plot
    for t in np.arange(nTrials):
        plotRawTrial(t, rawData, plot_dir)
        print('plot: trial {} for subj {}'.format(str(t+1), subj))



def plotRawTrial(idx, rawData, plot_dir):
    """
    plot the raw data for the trial at index location idx.
    rawData should be a dictionary containing raw data from all trials
    output plot will be stored in plot_dir
    """

    # isolate the data for this trial
    trial = rawData['taskData'][idx]
    trialNum = trial['trialNum']

    # convert the x and y "gaze" data from list to np array
    x = np.asarray(trial['imgGaze']['x'], dtype=int)
    y = np.asarray(trial['imgGaze']['y'], dtype=int)

    # translate gaze points to be relative to stim (instead of canvas)
    imgOrigin = trial['imgOrigin']
    x = x - float(imgOrigin[0])
    y = y - float(imgOrigin[1])

    # get the fixation cross location on this trial
    fixX = int(trial['fixLocation'][0]) - float(imgOrigin[0])
    fixY = int(trial['fixLocation'][1]) - float(imgOrigin[1])

    ### Plot results ############
    # load stim
    stim = mpimg.imread(join('../stimuli', trial['stimName']))

    # set figure dimensions
    if stim.shape[0] > stim.shape[1]:
        plt.figure(figsize=(10,8))
    else:
        plt.figure(figsize=(8,10))

    # draw stim
    plt.imshow(stim, alpha=.5)

    # # set color map for scatter plot
    cmap = plt.get_cmap('RdPu', x.shape[0])
    plt.scatter(x, y, s=300, c=np.arange(x.shape[0]), cmap=cmap, alpha=.75)

    # connect the points with lines
    plt.plot(x,y, 'k', alpha=.5, lw=.5)

    # fixation cross location
    plt.axhline(y=fixY, color='orange', ls='--', lw=2)
    plt.axvline(x=fixX, color='orange', ls='--', lw=2)

    # save
    figName = 'trial' + str(trialNum) + '.png'
    plt.savefig(join(plot_dir, figName))
    plt.close()


if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('subj', help='Subj ID whose data you want to plot')
    args = parser.parse_args()

    # submit this subject
    processSubj(args.subj)
