# reference: https://towardsdatascience.com/hiding-data-in-an-image-image-steganography-using-python-e491b68b1372

import cv2
import numpy as np
import types

class ImageStegno:

    def messageToBinary(self, message):
        if type(message) == str:
            return ''.join([format(ord(i), "08b") for i in message])
        elif type(message) == bytes or type(message) == np.ndarray:
            return [format(i, "08b") for i in message]
        elif type(message) == int or type(message) == np.uint8:
            return format(message, "08b")
        else:
            raise TypeError("Input type not supported")

    # Function to hide the secret message into the image
    def hideData(self, image, secret_message):
        # calculate the maximum bytes to encode
        n_bytes = image.shape[0] * image.shape[1] * 3 // 8
        print("Maximum bytes to encode:", n_bytes)

        # Check if the number of bytes to encode is less than the maximum bytes in the image
        if len(secret_message) > n_bytes:
            raise ValueError("Error encountered insufficient bytes, need bigger image or less data !!")

        secret_message += "#####"  # you can use any string as the delimeter

        data_index = 0
        # convert input data to binary format using messageToBinary() fucntion
        binary_secret_msg = self.messageToBinary(secret_message)

        data_len = len(binary_secret_msg)  # Find the length of data that needs to be hidden
        for values in image:
            for pixel in values:
                # convert RGB values to binary format
                r, g, b = self.messageToBinary(pixel)
                # modify the least significant bit only if there is still data to store
                if data_index < data_len:
                    # hide the data into least significant bit of red pixel
                    pixel[0] = int(r[:-1] + binary_secret_msg[data_index], 2)
                    data_index += 1
                if data_index < data_len:
                    # hide the data into least significant bit of green pixel
                    pixel[1] = int(g[:-1] + binary_secret_msg[data_index], 2)
                    data_index += 1
                if data_index < data_len:
                    # hide the data into least significant bit of  blue pixel
                    pixel[2] = int(b[:-1] + binary_secret_msg[data_index], 2)
                    data_index += 1
                # if data is encoded, just break out of the loop
                if data_index >= data_len:
                    break

        return image

    # Encode data into image
    def encode_text(self, secretText, filename):
        # image_name = input("Enter image name(with extension): ")
        image = cv2.imread(r"temp//"+filename)  # Read the input image using OpenCV-Python.
        # It is a library of Python bindings designed to solve computer vision problems.

        # details of the image
        # print("The shape of the image is: ", image.shape)  # check the shape of image to calculate the number of bytes
        # in it
        print("The original image is as shown below: ")
        # image = imagefile
        resized_image = cv2.resize(image, (500, 500))  # resize the image as per your requirement
        cv2.imshow("Resized image", resized_image)  # display the image

        # data = input("Enter data to be encoded : ")
        # if (len(data) == 0):
        #     raise ValueError('Data is empty')

        # filename = input("Enter the name of new encoded image(with extension): ")
        filename = "enc_" + filename
        encoded_image = self.hideData(image, secretText)  # call the hideData function to hide the secret message into the
        # selected image
        cv2.imwrite(r"encrypted//" + filename, encoded_image)