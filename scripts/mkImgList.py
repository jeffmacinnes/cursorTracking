import os
from os.path import join

stimDir = '../data/groupData/plots'

f = open('imageURL.txt','w')

for s in sorted(os.listdir(stimDir)):
    if s[0] != '.':
        thisLine = '<img src="images/heatmaps/{}">'.format(s)
        f.write(thisLine + '\n')
f.close()
