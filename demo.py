from threading import Thread
from pedalboard.io import AudioStream
from pedalboard import (LadderFilter, Compressor, PeakFilter,
                        Convolution, NoiseGate, Invert, Gain,
                        Distortion, Reverb, Pedalboard, Chain,
                        Mix)

# GLOBAL SETTINGS - CHANGE THESE ACCORDING TO YOUR SYSTEM
########################################
inputAudio = 'MacBook Pro Microphone'
outputAudio = 'MacBook Pro Speakers'
bufferSize = 64
sampleRate = 44100.0
pluginChain = Pedalboard([ Mix([ Chain([ Gain() ]), Gain() ]) ])
########################################

class audioHandler:
    def __init__(self, inputAudio, outputAudio, 
                 bufferSize, sampleRate, pluginChain):
        self.stream = AudioStream(input_device_name=inputAudio, 
                            output_device_name=outputAudio,
                            buffer_size=bufferSize,
                            sample_rate=sampleRate,
                            plugins=pluginChain,
                            allow_feedback=True)
        self.audioThread = Thread(target=self.stream.run, daemon=True)
        self.audioThread.start()

audio = audioHandler(inputAudio, outputAudio, bufferSize, 
                     sampleRate, pluginChain)

input("Press enter to invert wet channel (Should null)")
audio.stream.plugins[0][0].insert(0, Invert())
nextGain = float(input('Next gain for wet? >>> '))
audio.stream.plugins[0][0][-1] = Gain(gain_db=nextGain)
nextGain = float(input('Next gain for dry? >>> '))
audio.stream.plugins[0][-1] = Gain(gain_db=nextGain)
input()