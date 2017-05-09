from __future__ import print_function
from __future__ import division

import os
from os.path import join
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
import seaborn as sns
import argparse


"""
Create a heatmap for each image found in data/groupResults/allSubjsRaw.tsv

output stored in data/groupData/plots
"""


def mk_heatmaps(datafile):
    """
    make a heatmap for every unique image found in the datafile

    datafile is expected to be a combined raw 'gaze' data for all subject, with
    columns for x, y, stim (stimPath), and subjID

    """
    # set up output dir, make if necessary
    output_dir = '../data/groupData/plots'
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    # load the datafile
    df = pd.read_table(datafile)

    # loop through each unique stimuli
    for stim in np.unique(df.stim):

        # isolate the data for this stim only
        stim_df = df[df.stim == stim]

        # create a heatmap
        plotHeatmap(stim_df, output_dir, levels=11)


        print('heatmap created for image: {}'.format(stim.split('/')[-1]))


def plotHeatmap(df, outputDir, levels=10):
    """
    create a single heatmap for the data specified in df

    df: datafile containing all x,y gaze locations for single stim
    levels: how many levels in the contour (i.e. heat) map
    outputDir: directory to store output file in
    """

    # read in the background stim
    stimName = df.stim.iloc[0]
    bgImg = mpimg.imread(join('../stimuli', stimName))

    # set sns style
    sns.set_style('white')

    # start figure
    if bgImg.shape[0] > bgImg.shape[1]:
        fig = plt.figure(figsize=(8,10))
    else:
        fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111)

    # add number of subjects to title
    n_subjects = len(np.unique(df.subjID))
    title = '{} - {} subjects'.format(stimName.split('/')[-1], str(n_subjects))
    fig.suptitle(title, fontsize=18)

    # add the bg image
    plt.imshow(bgImg, alpha=.6)
    plt.axis('off')
    ax.set_xlim([0, bgImg.shape[1]])
    ax.set_ylim([bgImg.shape[0], 0])

    # add heatmap
    sns.kdeplot(df['x'], df['y'],
                shade=True,
                shade_lowest=False,
                cmap='viridis',
                n_levels=levels,
                alpha=0.7)

    # save
    plt.savefig(join(outputDir, (stimName.split('/')[-1].split('.')[0] + '.png')))
    plt.close()


if __name__ == "__main__":
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('dataFile', help='path to combined raw datafile')
    args = parser.parse_args()

    # submit
    mk_heatmaps(args.dataFile)
