import cv2
import numpy as np
import glob

# for filename in glob.glob('temp/frames/*.png'):
#     print(filename)


# read image
img = cv2.imread('temp/frames/frame0.png')

# get dimensions of image
dimensions = img.shape

# height, width, number of channels in image
height = img.shape[0]
width = img.shape[1]
channels = img.shape[2]

print('Image Dimension    : ', dimensions)
print('Image Height       : ', height)
print('Image Width        : ', width)
print('Number of Channels : ', channels)

