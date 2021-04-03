import os
import glob

for filename in glob.glob('temp/frames/*.png'):
    print(filename)