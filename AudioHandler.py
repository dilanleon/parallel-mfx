from threading import Thread
from pedalboard.io import AudioStream
from pedalboard import (LadderFilter, Invert, NoiseGate, Compressor, Clipping,
                        Distortion, Reverb, Convolution, Gain, Mix, Chain,
                        Pedalboard)


class AudioHandler:

    def defRunStream(self):
        def runStream():
            audioThread = Thread(target=self.stream.run, daemon=True)
            audioThread.start()
        return runStream
        
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
        self.runStream = self.defRunStream() # delete this on close
        self.runStream()
        # maybe turn allow_feedback off?
        # The below dictionary will be called for plugin constructors as kwargs
        self.pluginParams = { 
            LadderFilter : {
                'mode':LadderFilter.BPF12,
                'cuttof_hz':175.0,
                'resonance':0.0,
                'drive':1.0
                },
            Invert : { },
            NoiseGate:{
                'threshold_db':-60.0, 
                'ratio':2.5,
                'attack_ms':2.5,
                'release_ms':250.0
                },
            Compressor:{
                'threshold_db':0.0, 
                'ratio':1.0,
                'attack_ms':2.5,
                'release_ms':250.0
                },
            Clipping:{
                'threshold_db':0.0
                },
            Distortion:{
                'drive_db':0.0
                },
            Reverb:{
                'room_size':0.5,
                'damping':0.5,
                'wet_level':0.33,
                'dry_level':0.0,
                'width':1.0,
                'freeze_mode':0.0
                },
            Convolution:{
                'impulse_response_filename':'''EchoThiefImpulseResponseLibrary\
/Underground/Batcave.wav''',
                'mix':0.3
                }
            }
        self.effectOrder = (LadderFilter, Invert, NoiseGate, Compressor, 
                            Clipping, Distortion, Reverb, Convolution, Gain)

    def changeDryGain(self, newGain):
        # Gain is always last
        self.stream.plugins[0][-1].gain_db = float(newGain)
    
    def changeWetGain(self, newGain):
        # Gain is always last within the wet chain
        self.stream.plugins[0][0][-1].gain_db = float(newGain)

    def updateChainTypes(self):
        # Sets self.chainTypes to be a list of the plugin types currently in
        # the wet channel - we only care about types and not params for toggles
        self.chainTypes = [ ]
        for plugin in self.stream.plugins[0][0]:
            self.chainTypes.append(type(plugin))

    def getInsertionIndex(self, plugin):
        # @TODO FIX THIS FUCKING FUNCTION
        # Filter|Invert|Gate|Compress|Clip|Distort|Reverb|Convolution|Gain
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
                if self.chainTypes[0] == expectedNextPlugin:
                    return 0
                else:
                    return (self.chainTypes.index(expectedNextPlugin) - 1)
        raise Exception("The plugin you tried to add is not supported.")
    
    def pluginStrToType(self, pluginStr):
        # probably not needed. @TODO
        typeDict = {
            'Filter':LadderFilter,
            'Invert':Invert,
            'Gate':NoiseGate,
            'Compressor':Compressor,
            'Clipping':Clipping,
            'Distortion':Distortion,
            'Reverb':Reverb,
            'Convolution':Convolution
        }
        return typeDict[pluginStr]
    
    def updateChain(self, newChain):
        # Update the entirety of self.stream.plugins (the only way that worked)
        print(f'New Chain: {newChain}')
        self.stream.plugins = Pedalboard( [Mix ( [Chain(newChain), Gain()] )] )

    def removePlugin(self, plugin):
        # Create a new chain object without the plugin
        newChain = [ ]
        for activePlugin in self.stream.plugins[0][0]:
            if type(activePlugin) == plugin:
                pass
            else:
                newChain.append(activePlugin)
        self.updateChain(newChain)
    
    def insertPlugin(self, plugin, index):
        # Create a new chain object with the new plugin
        newChain = [ ]
        for i in range(len(self.stream.plugins[0][0])):
            if i == index:
                print(newChain[i:])
                newChain.append(plugin)
            newChain.append(self.stream.plugins[0][0][i])
        self.updateChain(newChain)

    def createPluginInstance(self, plugin):
        # Make an instance of specified plugin with the correct parameters,
        # as stored in self.pluginParams
        params = self.pluginParams[plugin]
        return plugin(**params)

    def togglePlugin(self, plugin):
        plugin = self.pluginStrToType(plugin) # str -> type conversion
        # Plugin order should always be:
        # Filter|Invert|Gate|Compress|Clip|Distort|Reverb|Convolution|Gain
        # The user will not be allowed to toggle the Gain
        self.updateChainTypes()
        if plugin in self.chainTypes:
            self.removePlugin(plugin)
        else:
            insertionIndex = self.getInsertionIndex(plugin)
            print(f'InsertionIndex:{insertionIndex}')
            insertedPlugin = self.createPluginInstance(plugin)
            self.insertPlugin(insertedPlugin, insertionIndex)
            print('Sucessfully inserted plugin to chain')

    def killStream(self):
            del self.runStream

