# reference: https://www.geeksforgeeks.org/convert-binary-to-string-using-python/?ref=rp
class TextStegno:

    def BinaryToDecimal(self, binary):
        string = int(binary, 2)
        return string

    def encodetext(self, secretmsg, filename):
        print("Secret Message:", secretmsg, "filename: ", filename)
        f = open("temp//" + filename, "r")
        txtcontent = f.read()

        bin_text = ''.join(format(ord(i), '08b') for i in txtcontent)
        bin_secretmsg = ''.join(format(ord(i), '08b') for i in secretmsg)
        outputbin = ""
        j = 0  # pointer for bin_secretmsg
        print("bin of secret msg:", bin_secretmsg)

        # replace every 4th bit
        for i in range(0, len(bin_text)):
            if i + 1 % 4 == 0:
                outputbin = outputbin + bin_secretmsg[j]
                j += 1
            else:
                outputbin = outputbin + bin_text[i]

        print("Original bin array:", bin_text)
        print("After encoding, bin array:", outputbin)

        # Lets convert bin array to String and save it to text file
        str_data = ' '

        for i in range(0, len(outputbin), 7):
            temp_data = outputbin[i:i + 7]
            decimal_data = self.BinaryToDecimal(temp_data)
            str_data = str_data + chr(decimal_data)

        f = open(r"encrypted//"+"enc_"+filename, "w")
        f.write(str_data)
        f.close()