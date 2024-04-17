# used by main.app to create button and knob controls

# THERE ARE MANY MAGIC NUMBERS IN THIS FILE. They are arbitrary and subjective
# as they are used for the positioning of elements in the UI, so it's best
# that they are easy to tweak. Button and Knob objects scale automatically,
# so their x and y positions and other such params are fixed values.

from UIClasses import *
from pedalboard import LadderFilter
from pedalboard.io import AudioStream
from AudioHandler import AudioHandler

#                  -----------------------------
#                          many screens
def makeAudioStream(app, sampleRate, bufferSize):
    app.audio = AudioHandler(app.inputDevice, app.outputDevice, 
                             bufferSize=bufferSize, sampleRate=sampleRate)
#                  -----------------------------
#                  sample rate/buffer size select
def makeSampleAndBufferFunctions(type):
    # sample rate settings
    def sampleRate44k(app):
        app.sampleRate = 44100
    def sampleRate48k(app):
        app.sampleRate = 48000
    # higher sample rates than 48k are dumb. but go ahead, user, be dumb.
    def sampleRate88k(app):
        app.sampleRate = 88200
    def sampleRate96k(app):
        app.sampleRate = 96000
    def sampleRate176k(app):
        app.sampleRate = 176400
    def sampleRate192k(app):
        app.sampleRate = 192000
    # buffer size settings
    def buffer64(app):
        app.bufferSize = 64
    def buffer128(app):
        app.bufferSize = 128
    def buffer256(app):
        app.bufferSize = 256
    def buffer512(app):
        app.bufferSize = 512
    def buffer1024(app):
        app.bufferSize = 1024
    def buffer2048(app):
        app.bufferSize = 2048
    functionDict = {
        # sample rates
        '44.1k':sampleRate44k,
        '48k':sampleRate48k,
        '88.2k':sampleRate88k,
        '96k':sampleRate96k,
        '176.4k':sampleRate176k,
        '192k':sampleRate192k,
        # buffers
        '64':buffer64,
        '128':buffer128,
        '256':buffer256,
        '512':buffer512,
        '1024':buffer1024,
        '2048':buffer2048
    }
    return functionDict[type]

def makeSampleAndBufferButtons(app):
    app.sampleRateButtons = [ ]
    app.bufferSizeButtons = [ ]
    # loop through the below list and make buttons with those labels/fns
    sampleRates = ['44.1k', '48k', '88.2k', '96k', '176.4k', '192k']
    for i in range(len(sampleRates)):
        sampleRate = sampleRates[i]
        app.sampleRateButtons.append(
            Button(sampleRate, 187.5, 100+i*33.3, 187.5, 31.25,
                   makeSampleAndBufferFunctions(sampleRate),
                   color='lightGray', font='arial')
        )
    # same thing but for buffer sizes
    bufferSizes = ['64', '128', '256', '512', '1024', '2048']
    for i in range(len(bufferSizes)):
        bufferSize = bufferSizes[i]
        app.bufferSizeButtons.append(
            Button(bufferSize, 187.5, 100+i*33.3, 187.5, 31.25, 
                   makeSampleAndBufferFunctions(bufferSize),
                   color='lightGray', font='arial')
        )
#                  -----------------------------
#                           I/O screen
def makeIOButtons(app, IOList, direction):
    # makes the buttons to select input
    for i in range(len(IOList)):
        setInputName = makeIOSetterFunction(i, direction)
        app.IOButtons.append(
            Button(
                IOList[i], 187.5, 100+i*33.3, 187.5, 31.25, setInputName, 
                color='lightGray', font='arial', boldText=True
                )
            )

def makeIOSetterFunction(i, direction):
    # Creates a function that sets app I/O device to index i of the list of 
    # I/O devices. Direction should be set to 'input' or 'output'.
    # Required to avoid function aliasing. Thanks Mike!
    if direction == 'input':
        def f(app):
            app.inputDevice = AudioStream.input_device_names[i]
            app.IOButtons = [ ]
            makeIOButtons(app, AudioStream.output_device_names, 'output')
    elif direction == 'output':
        def f(app):
            app.outputDevice = AudioStream.output_device_names[i]
            app.IOButtons = [ ]
    return f
#                  -----------------------------------
#                        idiot check screen    
def makeIdiotCheckYesNoFunction(yesNo):
    if yesNo == 'yes':
        def yes(app):
            makeAudioStream(app, app.sampleRate, app.bufferSize)
            setActiveScreen('mainScreen')
        return yes
    if yesNo == 'no':
        def no(app):
            setActiveScreen('inputsScreen')
        return no

def makeIdiotCheckButtons(app):
    app.idiotCheckScreenButtons = [
        Button('NO', 125, 250, 70, 35, makeIdiotCheckYesNoFunction('no')),
        Button('YES', 250, 250, 70, 35, makeIdiotCheckYesNoFunction('yes'))
    ]
#                  -----------------------------------
#                           main screen

def makeControlFunction(type):
    # Functions used by knobs and buttons throughout the  main app
    # one big ass function to group a bunch of stuff together really
    #                        *buttons*
    def switchToInputsScreen(app):
        app.audio.killStream()
        setActiveScreen('inputsScreen')
    def filterToggle(app):
        app.audio.togglePlugin('Filter')
    def setFilterTypeLPF12(app):
        app.audio.changePluginParam('Filter', 'mode', LadderFilter.LPF12)
    def setFilterTypeHPF12(app):
        app.audio.changePluginParam('Filter', 'mode', LadderFilter.HPF12)
    def setFilterTypeBPF12(app):
        app.audio.changePluginParam('Filter', 'mode', LadderFilter.BPF12)
    def setFilterTypeLPF24(app):
        app.audio.changePluginParam('Filter', 'mode', LadderFilter.LPF24)
    def setFilterTypeHPF24(app):
        app.audio.changePluginParam('Filter', 'mode', LadderFilter.HPF24)
    def setFilterTypeBPF24(app):
        app.audio.changePluginParam('Filter', 'mode', LadderFilter.BPF24)
    def invertToggle(app):
        app.audio.togglePlugin('Invert')
    def gateToggle(app):
        app.audio.togglePlugin('Gate')
    def compToggle(app):
        app.audio.togglePlugin('Compressor')
    def clipToggle(app):
        app.audio.togglePlugin('Clipping')
    def distortionToggle(app):
        app.audio.togglePlugin('Distortion')
    def reverbToggle(app):
        app.audio.togglePlugin('Reverb')
    def convolutionToggle(app):
        app.audio.togglePlugin('Convolution')
    def muteDry(app):
        app.audio.toggleDryMute()
    def muteWet(app):
        app.audio.toggleWetMute()
    #                             *knobs*
    def changeFilterFrequency(app, newFrequency):
        app.audio.changePluginParam('Filter', 'cutoff_hz', newFrequency)
    def changeFilterResonance(app, newResonance):
        app.audio.changePluginParam('Filter', 'resonance', newResonance)
    def changeFilterDrive(app, newDrive):
        app.audio.changePluginParam('Filter', 'drive', newDrive)
    def changeGateThreshold(app, newThreshold):
        app.audio.changePluginParam('Gate', 'threshold_db', newThreshold)
    def changeGateRatio(app, newRatio):
        app.audio.changePluginParam('Gate', 'ratio', newRatio)
    def changeGateAttack(app, newAttack):
        app.audio.changePluginParam('Gate', 'attack_ms', newAttack)
    def changeGateRelease(app, newRelease):
        app.audio.changePluginParam('Gate', 'release_ms', newRelease)
    def changeCompThreshold(app, newThreshold):
        app.audio.changePluginParam('Compressor', 'threshold_db', newThreshold)
    def changeCompRatio(app, newRatio):
        app.audio.changePluginParam('Compressor', 'ratio', newRatio)
    def changeCompAttack(app, newAttack):
        app.audio.changePluginParam('Compressor', 'attack_ms', newAttack)
    def changeCompRelease(app, newRelease):
        app.audio.changePluginParam('Compressor', 'release_ms', newRelease)
    def changeClippingThreshold(app, newThreshold):
        app.audio.changePluginParam('Clipping', 'threshold_db', newThreshold)
    def changeDistortionGain(app, newGain):
        app.audio.changePluginParam('Distortion', 'drive_db', newGain)
    def changeReverbSize(app, newSize):
        app.audio.changePluginParam('Reverb', 'room_size', newSize)
    def changeReverbDamping(app, newDamping):
        app.audio.changePluginParam('Reverb', 'damping', newDamping)
    def changeReverbDryWet(app, newWet):
        newDry = 1 - newWet
        app.audio.changePluginParam('Reverb', 'wet_level', newWet)
        app.audio.changePluginParam('Reverb', 'dry_level', newDry)
    def changeReverbWidth(app, newWidth):
        app.audio.changePluginParam('Reverb', 'width', newWidth)
    # @TODO Figure out what Reverb 'freeze mode' does and why it's a float
    def changeConvolutionMix(app, newMix):
        app.audio.changePluginParam('Convolution', 'mix', newMix)
    def gainWet(app, newGain):
        app.audio.changeWetGain(newGain)
    def gainDry(app, newGain):
        app.audio.changeDryGain(newGain)
    #     put the functions in a dictionary and return the desired one
    functionDict = {        # holy fucking fuck
        'filter':filterToggle,
        'filterLPF12':setFilterTypeLPF12,               # really
        'filterHPF12':setFilterTypeHPF12,
        'filterBPF12':setFilterTypeBPF12,
        'filterLPF24':setFilterTypeLPF24,
        'filterHPF24':setFilterTypeHPF24,
        'filterBPF24':setFilterTypeBPF24,               # insanely
        'filterFreq':changeFilterFrequency,
        'filterResonance':changeFilterResonance,
        'filterDrive':changeFilterDrive,
        'invert':invertToggle,
        'gate':gateToggle,                              # long
        'gateThresh':changeGateThreshold,
        'gateRatio':changeGateRatio,
        'gateAttack':changeGateAttack,
        'gateRelease':changeGateRelease,
        'comp':compToggle,                              # fuckin
        'compThresh':changeCompThreshold,
        'compRatio':changeCompRatio,
        'compAttack':changeCompAttack,
        'compRelease':changeCompRelease,
        'clipper':clipToggle,                           # ass
        'clipThresh':changeClippingThreshold,
        'distortion':distortionToggle,
        'distGain':changeDistortionGain,
        'reverb':reverbToggle,
        'reverbSize':changeReverbSize,
        'reverbDamping':changeReverbDamping,            # dictionary
        'reverbDryWet':changeReverbDryWet,
        'reverbWidth':changeReverbWidth,
        'convolution':convolutionToggle,
        'convolutionMix':changeConvolutionMix,
        'switchToInputsScreen':switchToInputsScreen,    # lol
        'gainWet':gainWet,
        'gainDry':gainDry,
        'muteDry':muteDry,
        'muteWet':muteWet                               # its over now
        }
    return functionDict[type]

def makeControlObjects(app):
    # knobs and buttons separate for your (my) calling convenience!
    # creates all the control objects required by the app.
    app.activeKnobs = [
        # filter freq
        Knob(77, 55, 25, 20, 20000, 200, makeControlFunction('filterFreq'),
             curveFunction='exponential', label='freq', color=app.filterColor),
        # filter resonance
        Knob(135, 70, 13, 0, 1, 0, makeControlFunction('filterResonance'),
             curveFunction='linear', label='reso', color=app.filterColor,
             percentKnob=True),
        # filter drive
        Knob(160, 35, 13, 1, 30, 1, makeControlFunction('filterDrive'),
             curveFunction='linear', label='dBdrive', color=app.filterColor),
        # gate threshold
        Knob(30, 165, 17, -60, 0, -60, makeControlFunction('gateThresh'),
            curveFunction='logarithmic', label='dBthresh', color=app.gateColor),
        # gate ratio
        Knob(70, 135, 17, 1, 10, 1.0, makeControlFunction('gateRatio'),
             curveFunction='linear', label='ratio', color=app.gateColor),
        # gate attack
        Knob(110, 165, 17, 0.1, 500, 2.5, makeControlFunction('gateAttack'), 
             curveFunction='exponential', label='attack', color=app.gateColor),
        # gate release
        Knob(150, 135, 17, 1, 1000, 250, makeControlFunction('gateRelease'),
            curveFunction='exponential', label='release', color=app.gateColor),
        # compressor threshold
        Knob(30, 262.5, 17, -60, 0, 0, makeControlFunction('compThresh'),
             curveFunction='logarithmic', label='thresh', color=app.compColor),
        # compressor ratio
        Knob(70, 232.5, 17, 1, 20, 1, makeControlFunction('compRatio'), 
             curveFunction='linear', label='ratio', color=app.compColor),
        # compressor attack
        Knob(110, 262.5, 17, 0.1, 500, 2.5, makeControlFunction('compAttack'),
             curveFunction='exponential', label='attack', color=app.compColor),
        # compressor release
        Knob(150, 232.5, 17, 1, 1000, 250, makeControlFunction('compRelease'),
             curveFunction='exponential', label='release', color=app.compColor),
        #clipping threshold
        Knob(50, 350, 22, -24, 0, 0, makeControlFunction('clipThresh'),
             curveFunction='logarithmic', label='thresh', color=app.distColor),
        # distortion gain
        Knob(130, 350, 22, 0, 30, 0, makeControlFunction('distGain'), 
             curveFunction='linear', label='gain', color=app.distColor),
        # reverb size
        Knob(217.5, 262.5, 17, 0, 1, 0.5, makeControlFunction('reverbSize'),
             curveFunction='linear', label='size', color=app.reverbColor,
             percentKnob=True),
        # reverb damping
        Knob(257.5, 232.5, 17, 0, 1, 0.5, makeControlFunction('reverbDamping'),
             curveFunction='linear', label='damping', color=app.reverbColor,
             percentKnob=True),
        # reverb dry/wet
        Knob(297.5, 262.5, 17, 0, 1, 0.5, makeControlFunction('reverbDryWet'),
             curveFunction='linear', label='dry/wet', color=app.reverbColor,
             percentKnob=True),
        # reverb width
        Knob(327.5, 232.5, 17, 0, 1, 0.5, makeControlFunction('reverbWidth'),
             curveFunction='linear', label='width', color=app.reverbColor,
             percentKnob=True),
        # convolution mix
        Knob(281.25, 345, 25, 0, 1, 0.5, makeControlFunction('convolutionMix'),
             curveFunction='linear', label='mix', color=app.convolutionColor,
             percentKnob=True),
        # dry gain
        Knob(250, 435, 22, -60, 6, 0, makeControlFunction('gainDry'),
             curveFunction='logarithmic', color='lightSlateGray', 
             label='dBdry'),
        # wet gain
        Knob(312.5, 435, 22, -60, 6, 0, makeControlFunction('gainWet'), 
            curveFunction='logarithmic', color='darkRed', label='dBwet')
    ]
    ON_SYMBOL = 'Ѳ'
    app.activeButtons = [
        # goto edit I/O screen
        Button('Edit I/O', 350, 487.5, 44, 12.5, 
               makeControlFunction('switchToInputsScreen'), color='dimGray', 
               labelColor='ghostWhite', font='arial',
               border=None, italicText=True),
        # toggle filter
        Button(ON_SYMBOL, 15, 35, 20, 20, makeControlFunction('filter'),
               drawAsToggled=True, color=app.filterColor),
        # toggle invert
        # ø is standard iconography in audio for a polarity switch
        Button('ø', 15, 80, 20, 20, makeControlFunction('invert'),
               drawAsToggled=True, font='symbols', labelSize=18),
        # toggle gate
        Button(ON_SYMBOL, 15, 130, 20, 20, makeControlFunction('gate'),
               drawAsToggled=True, color=app.gateColor),
        # toggle compressor
        Button(ON_SYMBOL, 15, 227.5, 20, 20, makeControlFunction('comp'),
               drawAsToggled=True, color=app.compColor),
        # toggle clipping
        Button(ON_SYMBOL, 15, 325, 20, 20, makeControlFunction('clipper'),
               drawAsToggled=True, color=app.distColor),
        # toggle distortion
        Button(ON_SYMBOL, 95, 325, 20, 20, makeControlFunction('distortion'),
               drawAsToggled=True, color=app.distColor),
        # toggle reverb
        Button(ON_SYMBOL, 202.5, 227.5, 20, 20, makeControlFunction('reverb'),
               drawAsToggled=True, color=app.reverbColor),
        # toggle convolution
        Button(ON_SYMBOL, 202.5, 325, 20, 20, 
               makeControlFunction('convolution'), drawAsToggled=True,
               color=app.convolutionColor),
        # mute dry
        Button('M', 220, 420, 10, 10, makeControlFunction('muteDry'),
               drawAsToggled=True, color='yellow', font='arial', 
               labelSize=8, border=None),
        # mute wet
        Button('M', 285, 420, 10, 10, makeControlFunction('muteWet'),
               drawAsToggled=True, color='yellow', font='arial', 
               labelSize=8, border=None)
    ]