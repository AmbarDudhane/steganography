import os
basepath = './encrypted/'
filelist = []
for entry in os.listdir(basepath):
    if os.path.isfile(os.path.join(basepath, entry)):
        filelist.append()
print("File List:", filelist)