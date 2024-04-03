from threading import Thread
from pedalboard.io import AudioStream
from pedalboard import (LadderFilter, Invert, NoiseGate, Compressor, Clipping,
                        Distortion, Reverb, Convolution, Gain, Mix, Chain,
                        Pedalboard)


class AudioHandler:

    def __init__(self, inputAudio, outputAudio, 
                 bufferSize=256, sampleRate=4800):
        # The API requires lists for Pedalboard, Mix, and Chain:
        # The indexes of Chain and Gain will never change
        defaultPlugins = Pedalboard( [Mix ( [Chain( [ Gain() ] ), Gain()] )] ) 
        self.stream = AudioStream(input_device_name=inputAudio, 
                            output_device_name=outputAudio,
                            buffer_size=bufferSize,
                            sample_rate=sampleRate,
                            plugins=defaultPlugins,
                            allow_feedback=True)
        self.audioThread = Thread(target=self.stream.run, daemon=True)
        self.audioThread.start()
        self.effectOrder = (LadderFilter, Invert, NoiseGate, Compressor, 
                            Clipping, Distortion, Reverb, Convolution, Gain)

    def changeDryGain(self, newGain):
        # Gain is always last
        self.stream.plugins[0][0][-1] = Gain(gain_db=newGain)

    def updateChainTypes(self):
        # Sets self.chainTypes to be a list of the plugin types currently in
        # the wet channel - we only care about types and not params for toggles
        self.chainTypes = [ ]
        for plugin in self.stream.plugins[0][0]:
            self.chainTypes.append(type(plugin))

    def getInsertionIndex(self, plugin):
        # plugin is a specific plugin object, but this function just needs type
        plugin = type(plugin)
        if len(self.chainTypes) == 1:
            # In this case, gain is the only plugin, which should always be
            # last, so return 0
            return 0
        expectedNextIndex = self.effectOrder.index(plugin) + 1
        for expectedNextPlugin in self.effectOrder[expectedNextIndex:]:
            # Assume Gain is always the last plugin in the chain. Then iterate
            # through the expected order and if the next plugin is in the
            # list of active plugins, return the index ahead of it.
            if expectedNextPlugin in self.chainTypes:
                return (self.chainTypes.index(expectedNextPlugin) - 1)

    def removePlugin(self, plugin):
        # Create a new chain object without the plugin
        newChain = [ ]
        for activePlugin in self.stream.plugins[0][0]:
            if type(activePlugin) == type(plugin):
                pass
            else:
                newChain.append(activePlugin)
        # Update the entirety of self.stream.plugins (the only way that worked)
        self.stream.plugins = Pedalboard( [Mix ( [Chain(newChain), Gain()] )] )

    def togglePlugin(self, plugin):
        # Plugin order should always be:
        # Filter|Invert|Gate|Compress|Clip|Distort|Reverb|Convolution|Gain
        # The user will not be allowed to toggle the Gain
        self.updateChainTypes()
        if type(plugin) in self.chainTypes:
            self.removePlugin(plugin)
        else:
            insertionIndex = self.getInsertionIndex(plugin)
            self.stream.plugins[0][0].insert(insertionIndex, plugin)