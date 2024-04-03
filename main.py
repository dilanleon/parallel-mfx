from AudioHandler import *
from pedalboard.io import AudioStream

def getAudioIO():
    def getIOHelper(L):
        for i in range(len(L)):
            print(f'{i+1}. {L[i]}')
        while True:
            selectedInput = input("Select an input by its number: >>> ")
            if not selectedInput.isnumeric():
                print('Not an integer. Try again.')
            elif (len(L) > int(selectedInput) > 0):
                return L[int(selectedInput) - 1]
            else:
                print('Invalid input. Try again.')
    print('Select an input device:')
    inputDevice = getIOHelper(AudioStream.input_device_names)
    print()
    print('Select an output device:')
    outputDevice = getIOHelper(AudioStream.output_device_names)
    return inputDevice, outputDevice

audio = AudioHandler(*getAudioIO())
input()




'''
Sources:

Sobot, P. Pedalboard. 0.7.3, Zenodo, 10 Apr. 2023, doi:10.5281/zenodo.7817839.

'''