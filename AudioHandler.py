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
        defaultPlugins = Pedalboard([Mix([Chain([Gain(0.0)]), Gain(0.0)])]) 
        self.stream = AudioStream(input_device_name=inputAudio, 
                                  output_device_name=outputAudio,
                                  buffer_size=bufferSize,
                                  sample_rate=sampleRate,
                                  plugins=defaultPlugins,
                                  allow_feedback=True)
        self.audioThread = Thread(target=self.stream.run, daemon=True)
        self.audioThread.start()
        self.dryGain, self.wetGain = 0.0, 0.0       # not stored in pluginParams
        self.dryMute, self.wetMute = False, False   # not stored in pluginParams
        MakeupGain = Gain       # So it has a different name @TODO
        # The below dictionary will be called for plugin constructors as kwargs
        self.pluginParams = { 
            LadderFilter:{
                'mode':LadderFilter.BPF12,
                'cutoff_hz':175.0,
                'resonance':0.0,
                'drive':1.0
                },
            Invert:{ },
            NoiseGate:{
                'threshold_db':-60.0, 
                'ratio':1.0,
                'attack_ms':2.5,
                'release_ms':250.0
                },
            Compressor:{
                'threshold_db':0.0, 
                'ratio':1.0,
                'attack_ms':2.5,
                'release_ms':250.0
                },
            MakeupGain:{
                'gain_db':0.0
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
                'wet_level':0.5,
                'dry_level':0.5,
                'width':1.0,
                'freeze_mode':0.0
                },
            Convolution:{
                'impulse_response_filename':'''EchoThiefImpulseResponseLibrary\
/Underground/Batcave.wav''',
                'mix':0.5
                }
            }
        self.effectOrder = (LadderFilter, Invert, NoiseGate, Compressor,
                            MakeupGain, Clipping, Distortion, Reverb, 
                            Convolution, Gain)

    def changeDryGain(self, newGain, unmute=False):
        # Gain is always last
        # if trying to change param while muted, don't actually change it:
        if self.dryMute and not unmute:
            self.prevDryGain = newGain
        # elif trying to unmute, set gain equal to remembered gain:
        elif self.dryMute and unmute:
            self.stream.plugins[0][-1].gain_db = float(newGain)
            self.dryGain = self.prevDryGain
        # else, change value as normal:
        else:
            self.stream.plugins[0][-1].gain_db = float(newGain)
            self.dryGain = newGain
            # we need to re-make the plugin on each param change
    
    def changeWetGain(self, newGain, unmute=False):
        # Gain is always last within the wet chain
        # Same idea as self.changeDryGain()
        if self.wetMute and not unmute:
            self.prevWetGain = newGain
        elif self.dryMute and unmute:
            self.stream.plugins[0][0][-1].gain_db = float(newGain)
            self.wetGain = self.prevWetGain
        else:
            self.stream.plugins[0][0][-1].gain_db = float(newGain)
            self.wetGain = newGain
            # stream.plugins gets overwritten on each param change
    
    def toggleDryMute(self):
        if self.dryMute:
            self.changeDryGain(self.prevDryGain, unmute=True)
        else:
            self.prevDryGain = self.dryGain     # don't forget what it was!
            self.changeDryGain(-999)
            # even -60 dB is basically inaudible, this is easier than true mute
        self.dryMute = not self.dryMute
    
    def toggleWetMute(self):
        if self.wetMute:
            self.changeWetGain(self.prevWetGain, unmute=True)
        else:
            self.prevWetGain = self.wetGain     # rerember the value!
            self.changeWetGain(-999)
            # you will not be able to hear this, I promise
        self.wetMute = not self.wetMute

    def updateChainTypes(self):
        # Sets self.chainTypes to be a list of the plugin types currently in
        # the wet channel - we only care about types and not params for toggles
        self.chainTypes = [ ]
        for plugin in self.stream.plugins[0][0]:
            self.chainTypes.append(type(plugin))
    
    def pluginStrToType(self, pluginStr):
        MakeupGain = Gain           # @TODO make MakeupGain work
        typeDict = {
            'Filter':LadderFilter,
            'Invert':Invert,
            'Gate':NoiseGate,
            'Compressor':Compressor,
            'MakeupGain':MakeupGain,
            'Clipping':Clipping,
            'Distortion':Distortion,
            'Reverb':Reverb,
            'Convolution':Convolution
        }
        return typeDict[pluginStr]
    
    def updateChain(self, newChain):
        # Update the entirety of self.stream.plugins (the only way that worked)
        self.stream.plugins = Pedalboard([
            Mix([Chain(newChain), Gain(self.dryGain)])])

    def removePlugin(self, plugin):
        # Create a new chain object without the plugin
        # make an empty list:
        newChain = [ ]
        for activePlugin in self.stream.plugins[0][0]:
            # if it's not the one to be removed, add it to the list:
            if type(activePlugin) != plugin:
                newChain.append(activePlugin)
        # update the chain:
        self.updateChain(newChain)
    
    def insertPlugin(self, pluginObj, index):
        # Create a new chain object with the new plugin
        # first make a list of the plugins in the chain:
        chainAsList = [plugin for plugin in self.stream.plugins[0][0]]
        # then insert into that list:
        chainAsList.insert(index, pluginObj)
        # then update the chain:
        self.updateChain(chainAsList)

    def getInsertionIndex(self, plugin):
        # gets the index needed to maintain this plugin order:
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
                return self.chainTypes.index(expectedNextPlugin)
        raise Exception("The plugin you tried to add is not supported.")

    def createPluginInstance(self, plugin):
        # Make an instance of specified plugin with the correct parameters,
        # as stored in self.pluginParams
        params = self.pluginParams[plugin]
        return plugin(**params)

    def togglePlugin(self, plugin):
        # first convert plugin from string to type:
        plugin = self.pluginStrToType(plugin)
        self.updateChainTypes()
        # comparing types means params aren't considered (good!)
        if plugin in self.chainTypes:
            # if it's in remove it;
            self.removePlugin(plugin)
        else:
            # if it's out add it:
            insertionIndex = self.getInsertionIndex(plugin)
            insertedPlugin = self.createPluginInstance(plugin)
            self.insertPlugin(insertedPlugin, insertionIndex)

    def changePluginParam(self, plugin, paramName, value):
        # first, convert plugin from string to type:
        plugin = self.pluginStrToType(plugin)
        self.updateChainTypes()
        # Wether the plugin is enabled or not, self.pluginParams needs updated
        self.pluginParams[plugin][paramName] = value
        if plugin in self.chainTypes:   # if the plugin is enabled:
            pluginIndex = self.chainTypes.index(plugin)
            # make a str with the command to execute
            # https://www.geeksforgeeks.org/execute-string-code-python/
            # {plugin}.paramName = value doesn't work w/o this hack
            execStr = (
               f'self.stream.plugins[0][0][{pluginIndex}].{paramName} = {value}'
            )
            exec(execStr)
            chainAsList = [plugin for plugin in self.stream.plugins[0][0]]
            # also, just changing the value doesn't work - 
            # we need to remake the whole pedalboard object... 
            # every time a knob is moved...
            self.updateChain(chainAsList)

    def killStream(self):
            del self.runStream