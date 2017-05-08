import os
from os.path import join
import sys

# loop through all subjs in data dir, submit each to plotRaw

for f in os.listdir('../data'):
    if os.path.isdir(join('../data', f)):
        try:
            cmd_str = 'python plotRaw.py ' + f
            os.system(cmd_str)
        except:
            pass
