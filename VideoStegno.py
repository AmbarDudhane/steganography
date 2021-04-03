# reference: https://betterprogramming.pub/a-guide-to-video-steganography-using-python-4f010b32a5b7
# reference: https://github.com/llopen-sourcell/Video-Steganography/blob/master/main.py

import cv2
import os
import math
from stegano import lsb
import glob
from subprocess import call, STDOUT
import moviepy.editor as mp


class VideoStegno:

    def split_string(self, s_str: str, count=10):
        per_c = math.ceil(len(s_str) / count)
        c_cout = 0
        out_str = ''
        split_list = []
        for s in s_str:
            out_str += s
            c_cout += 1
            if c_cout == per_c:
                split_list.append(out_str)
                out_str = ''
                c_cout = 0
        if c_cout != 0:
            split_list.append(out_str)
        return split_list

    def encode_string(self, input_string, root="./temp/frames/"):
        split_string_list = self.split_string(input_string)
        for i in range(0, len(split_string_list)):
            f_name = "{}frame{}.png".format(root, i)
            secret_enc = lsb.hide(f_name, split_string_list[i])
            secret_enc.save(f_name)
            print("[INFO] frame {} holds {}".format(f_name, split_string_list[i]))

    def generateVideo(self, filename):
        img = cv2.imread('temp/frames/frame0.png')

        # height, width, number of channels in image
        height = img.shape[0]
        width = img.shape[1]
        frameSize = (width, height)

        out = cv2.VideoWriter("encrypted//" + 'enc_' + filename, cv2.VideoWriter_fourcc(*'MPEG'), 30, frameSize)

        for filename in glob.glob('temp/frames/*.png'):
            img = cv2.imread(filename)
            out.write(img)

        out.release()

    def clearframes(self):

        for filename in glob.glob('temp/frames/*.png'):
            os.remove(filename)

    def loadVideo(self, secretMsg, filename):
        vidcap = cv2.VideoCapture("temp//" + filename)
        # success, image = vidcap.read()
        count = 0
        while True:
            success, image = vidcap.read()
            if not success:
                break
            cv2.imwrite(os.path.join("temp//frames//", "frame{:d}.png".format(count)), image)
            count += 1

        # extract audio from video
        my_clip = mp.VideoFileClip(r"temp//" + filename)
        my_clip.audio.write_audiofile(r"temp//my_result.mp3")

        self.encode_string(secretMsg)

        # make final video
        self.generateVideo(filename)

        # clear the frames dir
        self.clearframes()