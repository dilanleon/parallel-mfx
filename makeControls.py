# used by main.app to create button and knob controls

# THERE ARE MANY MAGIC NUMBERS IN THIS FILE. They are arbitrary and subjective
# as they are used for the positioning of elements in the UI, so it's best
# that they are easy to tweak. Button and Knob objects scale automatically,
# so their x and y positions and other such params are fixed values.

import os
from UIClasses import *
from pedalboard import LadderFilter
from pedalboard.io import AudioStream
from AudioHandler import AudioHandler

HOV_COLOR = 'mediumSlateBlue'  # hover color for non-main app screens

#                  -----------------------------
#                          many screens
def makeAudioStream(app):
    # make the stream if it doesn't exist. Else, update settings and start it
    try:
        app.audio
    except AttributeError:
        app.audio = AudioHandler(app.inputDevice, app.outputDevice, 
                                 bufferSize=app.bufferSize, 
                                 sampleRate=app.sampleRate)
    else:
        app.audio.changeSettings(app.inputDevice, app.outputDevice,
                                 bufferSize=app.bufferSize, 
                                 sampleRate=app.sampleRate)
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
                   color='lightGray', font='arial', hoverBorderColor=HOV_COLOR)
        )
    # same thing but for buffer sizes
    bufferSizes = ['64', '128', '256', '512', '1024', '2048']
    for i in range(len(bufferSizes)):
        bufferSize = bufferSizes[i]
        app.bufferSizeButtons.append(
            Button(bufferSize, 187.5, 100+i*33.3, 187.5, 31.25, 
                   makeSampleAndBufferFunctions(bufferSize),
                   color='lightGray', font='arial', hoverBorderColor=HOV_COLOR)
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
                color='lightGray', font='arial', boldText=True, 
                hoverBorderColor=HOV_COLOR
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
            makeAudioStream(app)
            setActiveScreen('mainScreen')
        return yes
    if yesNo == 'no':
        def no(app):
            setActiveScreen('inputsScreen')
        return no

def makeIdiotCheckButtons(app):
    app.idiotCheckScreenButtons = [
        Button('NO', 125, 250, 70, 35, makeIdiotCheckYesNoFunction('no'), 
               color='paleGreen', hoverBorderColor='green', borderWidth=3),
        Button('YES', 250, 250, 70, 35, makeIdiotCheckYesNoFunction('yes'),
               hoverBorderColor='darkRed', borderWidth=3)
    ]
#                  -----------------------------------
#                           IR select screen
# https://builtin.com/data-science/python-list-files-in-directory
def makeIRButtonFunctions(filename):
    def fileButtonFunction(app):
        app.IRpath += '/' + filename
        app.audio.changePluginParam('Convolution', 'impulse_response_filename',
                                    app.IRpath)
        setActiveScreen('mainScreen')
    return fileButtonFunction

def makeIRButtons(app, folder):
    app.IRButtons = [ ]
    app.files = os.listdir('EchoThiefImpulseResponseLibrary/' + folder)
    i = 0
    while i < len(app.files):
        if app.files[i][0] != '.':        # hide hidden files
            app.IRButtons.append(
                Button(app.files[i], 275, 50 + i*17, 160, 16,
                       makeIRButtonFunctions(app.files[i]), font='arial',
                       hoverBorderColor=HOV_COLOR)
            )
            i += 1
        else:
            app.files.pop(i)

def makeFolderButtonFunctions(folderName):
    def folderButtonFunction(app):
        app.IRpath = 'EchoThiefImpulseResponseLibrary/' + folderName
        makeIRButtons(app, folderName)
    return folderButtonFunction

def makeFolderButtons(app):
    app.IRFolderButtons = [ ]
    app.folders = os.listdir('EchoThiefImpulseResponseLibrary')
    i = 0
    while i < len(app.folders):
        if app.folders[i][0] != '.':        # hidden files should stay hidden!
            app.IRFolderButtons.append(
                Button(app.folders[i] + ' >', 105, 60 + i*33.3, 100, 31.25,
                       makeFolderButtonFunctions(app.folders[i]), font='arial',
                       hoverBorderColor=HOV_COLOR)
            )
            i += 1
        else:
            app.folders.pop(i)
        
#                  -----------------------------------
#                           main screen
# the below function is why this whole file exists (it's really long...)
def makeControlFunction(type):
    # Functions used by knobs and buttons throughout the  main app
    # one big ass function to group a bunch of stuff together really
    #                        *buttons*
    def switchToSampleBufferScreen(app):
        app.audio.killStream()
        setActiveScreen('sampleRateBufferSize')
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
    def bitcrushToggle(app):
        app.audio.togglePlugin('Bitcrush')
    def chorusToggle(app):
        app.audio.togglePlugin('Chorus')
    def delayToggle(app):
        app.audio.togglePlugin('Delay')
    def reverbToggle(app):
        app.audio.togglePlugin('Reverb')
    def convolutionToggle(app):
        app.audio.togglePlugin('Convolution')
    def convolutionFileSelect(app):
        setActiveScreen('IRSelectScreen')
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
    def changeBitDepth(app, newDepth):
        app.audio.changePluginParam('Bitcrush', 'bit_depth', newDepth)
    def changeChorusRate(app, newRate):
        app.audio.changePluginParam('Chorus', 'rate_hz', newRate)
    def changeChorusDepth(app, newDepth):
        app.audio.changePluginParam('Chorus', 'depth', newDepth)
    def changeChorusCenterDelay(app, newDelay):
        app.audio.changePluginParam('Chorus', 'centre_delay_ms', newDelay)
    def changeChorusFeedback(app, newFeedback):
        app.audio.changePluginParam('Chorus', 'feedback', newFeedback)
    def changeChorusMix(app, newMix):
        app.audio.changePluginParam('Chorus', 'mix', newMix)
    def changeDelayTime(app, newTime):
        app.audio.changePluginParam('Delay', 'delay_seconds', newTime)
    def changeDelayFeedback(app, newFeedback):
        app.audio.changePluginParam('Delay', 'feedback', newFeedback)
    def changeDelayMix(app, newMix):
        app.audio.changePluginParam('Delay', 'mix', newMix)
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
        'bitcrush':bitcrushToggle,
        'bitDepth':changeBitDepth,
        'chorus':chorusToggle,                          # fucking
        'chorusRate':changeChorusRate,
        'chorusDepth':changeChorusDepth,
        'chorusDelay':changeChorusCenterDelay,
        'chorusFeedback':changeChorusFeedback,
        'chorusMix':changeChorusMix,                  
        'delay':delayToggle,                            # ass
        'delayTime':changeDelayTime,
        'delayFeedback':changeDelayFeedback,
        'delayMix':changeDelayMix,
        'reverb':reverbToggle,
        'reverbSize':changeReverbSize,
        'reverbDamping':changeReverbDamping,            # dictionary
        'reverbDryWet':changeReverbDryWet,
        'reverbWidth':changeReverbWidth,
        'convolution':convolutionToggle,
        'convolutionSelect':convolutionFileSelect,
        'convolutionMix':changeConvolutionMix,
        'switchToInputsScreen':switchToSampleBufferScreen,  # lol
        'gainWet':gainWet,
        'gainDry':gainDry,
        'muteDry':muteDry,
        'muteWet':muteWet                               # its over now
        }
    return functionDict[type]

# you made it to the end! there's another one :-)
def makeControlObjects(app):
    # knobs and buttons separate for your (my) calling convenience!
    # creates all the control objects required by the app.
    # lots of magic numbers - they are arbitrary and determine UI layout.
    app.activeKnobs = [
        # filter freq
        Knob(77, 55, 25, 20, 20000, 200, makeControlFunction('filterFreq'),
             curveFunction='exponential', label='freq', color=app.filterColor),
        # filter resonance
        Knob(125, 70, 13, 0, 1, 0, makeControlFunction('filterResonance'),
             curveFunction='linear', label='reso', color=app.filterColor,
             percentKnob=True),
        # filter drive
        Knob(160, 35, 13, 1, 30, 1, makeControlFunction('filterDrive'),
             curveFunction='linear', label='drive', color=app.filterColor),
        # gate threshold
        Knob(30, 165, 17, -60, 0, -60, makeControlFunction('gateThresh'),
            curveFunction='logarithmic', label='thresh', color=app.gateColor),
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
            curveFunction='logarithmic', label='dBthresh', color=app.distColor),
        # distortion gain
        Knob(130, 350, 22, 0, 60, 0, makeControlFunction('distGain'), 
             curveFunction='linear', label='dBgain', color=app.distColor),
        # bitcrush depth
        Knob(93.75, 435, 25, 0, 10, 8, makeControlFunction('bitDepth'),
             curveFunction='linear', label='depth', color=app.bitcrushColor),
        # chorus rate
        Knob(281.25, 60, 20, 0, 100, 1.0, makeControlFunction('chorusRate'),
             curveFunction='exponential', label='rate', color=app.chorusColor),
        # chorus center delay
        Knob(235, 35, 13, 0.5, 50, 7, makeControlFunction('chorusDelay'),
             curveFunction='exponential', label='delay', color=app.chorusColor),
        # chorus depth
        Knob(235, 72.5, 13, 0, 1, 0.25, makeControlFunction('chorusDepth'),
             curveFunction='linear', label='depth', color=app.chorusColor,
             percentKnob=True),
        # chorus feedback
        Knob(327.5, 35, 13, 0, 1, 0, makeControlFunction('chorusFeedback'),
             curveFunction='linear', label='feedback', color=app.chorusColor),
        # chorus mix
        Knob(327.5, 72.5, 13, 0, 1, 0.5, makeControlFunction('chorusMix'),
             curveFunction='linear', label='dry/wet', color=app.chorusColor,
             percentKnob=True),
        # delay time [seconds]
        Knob(237.5, 155, 22, 0.001, 10, 0.5, makeControlFunction('delayTime'),
            curveFunction='exponential', label='time', color=app.delayColor),
        # delay feedback
        Knob(290, 155, 22, 0, 1, 0, makeControlFunction('delayFeedback'),
             curveFunction='linear', label='feedback', color=app.delayColor,
             percentKnob=True),
        # delay mix
        Knob(345, 160, 13, 0, 1, 0.5, makeControlFunction('delayMix'),
             curveFunction='linear', label='dry/wet', color=app.delayColor,
             percentKnob=True),
        # reverb size
        Knob(217.5, 262.5, 17, 0, 1, 0.5, makeControlFunction('reverbSize'),
             curveFunction='linear', label='size', color=app.reverbColor,
             percentKnob=True),
        # reverb damping
        Knob(257.5, 232.5, 17, 0, 1, 0.5, makeControlFunction('reverbDamping'),
             curveFunction='linear', label='damp', color=app.reverbColor,
             percentKnob=True),
        # reverb dry/wet
        Knob(297.5, 262.5, 17, 0, 1, 0.5, makeControlFunction('reverbDryWet'),
             curveFunction='linear', label='dry/wet', color=app.reverbColor,
             percentKnob=True),
        # reverb width
        Knob(337.5, 232.5, 17, 0, 1, 0.5, makeControlFunction('reverbWidth'),
             curveFunction='linear', label='width', color=app.reverbColor,
             percentKnob=True),
        # convolution mix
        Knob(281.25, 350, 25, 0, 1, 0.5, makeControlFunction('convolutionMix'),
             curveFunction='linear', label='dry/wet', color=app.convolutionColor,
             percentKnob=True),
        # dry gain
        Knob(250, 435, 22, -60, 6, 0, makeControlFunction('gainDry'),
             curveFunction='logarithmic', color='lightSlateGray', 
             label='dBdry'),
        # wet gain
        Knob(312.5, 435, 22, -60, 6, 0, makeControlFunction('gainWet'), 
            curveFunction='logarithmic', color='darkRed', label='dBwet',
            hoverColor='crimson')
    ]
    ON_SYMBOL = 'X'         # Ѳ
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
        # toggle bitcrush
        Button(ON_SYMBOL, 15, 422.5, 20, 20, makeControlFunction('bitcrush'),
               drawAsToggled=True, color=app.bitcrushColor),
        # toggle chorus
        Button(ON_SYMBOL, 202.5, 35, 20, 20, makeControlFunction('chorus'),
               drawAsToggled=True, color=app.chorusColor),
        # toggle delay
        Button(ON_SYMBOL, 202.5, 130, 20, 20, makeControlFunction('delay'),
               drawAsToggled=True, color=app.delayColor),
        # toggle reverb
        Button(ON_SYMBOL, 202.5, 227.5, 20, 20, makeControlFunction('reverb'),
               drawAsToggled=True, color=app.reverbColor),
        # toggle convolution
        Button(ON_SYMBOL, 202.5, 325, 20, 20, 
               makeControlFunction('convolution'), drawAsToggled=True,
               color=app.convolutionColor),
        # select convolution file
        Button('select', 203.5, 380, 23, 13, 
               makeControlFunction('convolutionSelect'), font='arial',
               italicText=True),
        # mute dry
        Button('M', 220, 420, 15, 15, makeControlFunction('muteDry'),
               drawAsToggled=True, color='yellow', font='arial', 
               labelSize=8, border=None),
        # mute wet
        Button('M', 282.5, 420, 15, 15, makeControlFunction('muteWet'),
               drawAsToggled=True, color='yellow', font='arial', 
               labelSize=8, border=None)
    ]