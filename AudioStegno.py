# reference: https://sumit-arora.medium.com/audio-steganography-the-art-of-hiding-secrets-within-earshot-part-2-of-2-c76b1be719b3
import wave


class AudioStegno:

    def load(self, secretmsg, filename):
        audio = wave.open("temp//" + filename, mode='rb')
        # Read frames and convert to byte array
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

        string = secretmsg + int((len(frame_bytes) - (len(secretmsg) * 8 * 8)) / 8) * '#'
        # Convert text to bit array
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in string])))

        # Replace LSB of each byte of the audio data by one bit from the text bit array
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 254) | bit
        # Get the modified bytes
        frame_modified = bytes(frame_bytes)

        # Write bytes to a new wave audio file
        with wave.open('encrypted/enc_' + filename, 'wb') as fd:
            fd.setparams(audio.getparams())
            fd.writeframes(frame_modified)
        audio.close()
