from threading import Thread
from pedalboard.io import AudioStream
from pedalboard import (LadderFilter, Compressor, PeakFilter,
                        Convolution, NoiseGate, Invert, Gain,
                        Distortion, Reverb, Pedalboard, Chain,
                        Mix)

# GLOBAL SETTINGS
########################################
inputAudio = 'MacBook Pro Microphone'
outputAudio = 'External Headphones'
bufferSize = 64
sampleRate = 44100.0
pluginChain = Pedalboard([ Mix([ Chain([ Gain() ]), Gain() ]) ])
########################################


stream = AudioStream(input_device_name=inputAudio, 
                    output_device_name=outputAudio,
                    buffer_size=bufferSize,
                    sample_rate=sampleRate,
                    plugins=pluginChain)
audioThread = Thread(target=stream.run, daemon=True)

audioThread.start()

input("Press enter to invert wet channel (Should null)")
stream.plugins[0][0].insert(0, Invert())
nextGain = float(input('Next gain for wet? >>> '))
stream.plugins[0][0][-1] = Gain(gain_db=nextGain)
nextGain = float(input('Next gain for dry? >>> '))
stream.plugins[0][-1] = Gain(gain_db=nextGain)
input()