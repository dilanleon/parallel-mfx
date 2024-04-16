from UIClasses import *
from pedalboard.io import AudioStream
from AudioHandler import AudioHandler

# used by main.app 

def makeAudioStream(app):
    app.audio = AudioHandler(app.inputDevice, app.outputDevice, bufferSize=256)

#                  -----------------------------
#                           I/O screen
def createIOButtons(app, IOList, direction):
    # makes the buttons to select input
    for i in range(len(IOList)):
        getInputName = makeIOSetterFunction(i, direction)
        app.IOButtons.append(
            Button(
                IOList[i], 187.5, 100+i*33.3, 187.5, 31.25, getInputName, 
                color='antiqueWhite', labelColor='darkSlateGray', font='arial', 
                boldText=True
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
            createIOButtons(app, AudioStream.output_device_names, 'output')
    elif direction == 'output':
        def f(app):
            app.outputDevice = AudioStream.output_device_names[i]
            app.IOButtons = [ ]
    return f
#                  -----------------------------------
#                        idiot check screen    
def getIdiotCheckYesNoFunction(yesNo):
    if yesNo == 'yes':
        def yes(app):
            makeAudioStream(app)
            setActiveScreen('mainScreen')
        return yes
    if yesNo == 'no':
        def no(app):
            setActiveScreen('inputsScreen')
        return no
#                  -----------------------------------
#                           main screen

def makeControlFunction(type):
    # Functions used by knobs and buttons throughout the  main app
    # one big ass function to group a bunch of stuff together really
    #                        *buttons*
    def switchToInputsScreen(app):
        # stop app.audio @TODO
        del app.audio           #@TODO HOW THE FUCK DO I DO THIS
        setActiveScreen('inputsScreen')
    def filterToggle(app):
        app.audio.togglePlugin('Filter')
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
        'filterFreq':changeFilterFrequency,
        'filterResonance':changeFilterResonance,
        'filterDrive':changeFilterDrive,
        'invert':invertToggle,
        'gate':gateToggle,
        'gateThresh':changeGateThreshold,
        'gateRatio':changeGateRatio,
        'gateAttack':changeGateAttack,
        'gateRelease':changeGateRelease,
        'comp':compToggle,
        'compThresh':changeCompThreshold,
        'compRatio':changeCompRatio,
        'compAttack':changeCompAttack,
        'compRelease':changeCompRelease,
        'clipper':clipToggle,
        'clipThresh':changeClippingThreshold,
        'distortion':distortionToggle,
        'distGain':changeDistortionGain,
        'reverb':reverbToggle,
        'reverbSize':changeReverbSize,
        'reverbDamping':changeReverbDamping,
        'reverbDryWet':changeReverbDryWet,
        'reverbWidth':changeReverbWidth,
        'convolution':convolutionToggle,
        'convolutionMix':changeConvolutionMix,
        'switchToInputsScreen':switchToInputsScreen,
        'gainWet':gainWet,
        'gainDry':gainDry,
        'muteDry':muteDry,
        'muteWet':muteWet
        }
    return functionDict[type]

def makeControlObjects(app):
    # knobs and buttons separate for your (my) calling convenience!
    app.activeKnobs = [
        # filter freq
        Knob(155, 30, 17, 20, 20000, 175, makeControlFunction('filterFreq'),
             curveFunction='exponential', label='freq', color='gold'),
        # filter resonance
        Knob(200, 30, 17, 0, 1, 0, makeControlFunction('filterResonance'),
             curveFunction='linear', label='reso', color='gold',
             percentKnob=True),
        # filter drive
        Knob(245, 30, 17, 1, 30, 1, makeControlFunction('filterDrive'),
             curveFunction='linear', label='drive', color='gold'),
        # gate threshold
        Knob(155, 130, 17, -60, 0, -60, makeControlFunction('gateThresh'),
             curveFunction='logarithmic', label='thresh', color='khaki'),
        # gate ratio
        Knob(200, 130, 17, 1, 10, 1.0, makeControlFunction('gateRatio'),
             curveFunction='linear', label='ratio', color='khaki'),
        # gate attack
        Knob(245, 130, 17, 0.1, 500, 2.5, makeControlFunction('gateAttack'), 
             curveFunction='exponential', label='attack', color='khaki'),
        # gate release
        Knob(290, 130, 17, 1, 1000, 250, makeControlFunction('gateRelease'),
            curveFunction='exponential', label='release', color='khaki'),
        # compressor threshold
        Knob(155, 180, 17, -60, 0, 0, makeControlFunction('compThresh'),
             curveFunction='logarithmic', label='thresh', color='oliveDrab'),
        # compressor ratio
        Knob(200, 180, 17, 1, 20, 1, makeControlFunction('compRatio'), 
             curveFunction='linear', label='ratio', color='oliveDrab'),
        # compressor attack
        Knob(245, 180, 17, 0.1, 500, 2.5, makeControlFunction('compAttack'),
             curveFunction='exponential', label='attack', color='oliveDrab'),
        # compressor release
        Knob(290, 180, 17, 1, 1000, 250, makeControlFunction('compRelease'),
             curveFunction='exponential', label='release', color='oliveDrab'),
        #clipping threshold
        Knob(155, 230, 17, -24, 0, 0, makeControlFunction('clipThresh'),
             curveFunction='logarithmic', label='thresh', color='lime'),
        # distortion gain
        Knob(155, 280, 17, 0, 30, 0, makeControlFunction('distGain'), 
             curveFunction='linear', label='gain', color='fireBrick'),
        # reverb size
        Knob(155, 330, 17, 0, 1, 0.5, makeControlFunction('reverbSize'),
             curveFunction='linear', label='size', color='skyBlue',
             percentKnob=True),
        # reverb damping
        Knob(200, 330, 17, 0, 1, 0.5, makeControlFunction('reverbDamping'),
             curveFunction='linear', label='damping', color='skyBlue',
             percentKnob=True),
        # reverb dry/wet
        Knob(245, 330, 17, 0, 1, 0.5, makeControlFunction('reverbDryWet'),
             curveFunction='linear', label='dry/wet', color='skyBlue',
             percentKnob=True),
        # reverb width
        Knob(290, 330, 17, 0, 1, 0.5, makeControlFunction('reverbWidth'),
             curveFunction='linear', label='width', color='skyBlue',
             percentKnob=True),
        # convolution mix
        Knob(155, 380, 17, 0, 1, 0.5, makeControlFunction('convolutionMix'),
             curveFunction='linear', label='mix', color='thistle',
             percentKnob=True),
        # dry gain
        Knob(315, 445, 17, -60, 6, 0, makeControlFunction('gainDry'),
             curveFunction='logarithmic', color='lightSlateGray', 
             label='dBdry'),
        # wet gain
        Knob(355, 445, 17, -60, 6, 0, makeControlFunction('gainWet'), 
            curveFunction='logarithmic', color='darkRed', label='dBwet')
    ]
    app.activeButtons = [
        # goto edit I/O screen
        Button('Edit I/O', 350, 487.5, 44, 12.5, 
               makeControlFunction('switchToInputsScreen'), color='gray', 
               labelColor='ghostWhite', font='arial',
               border=None, italicText=True),
        # toggle filter
        Button('Filter', 80, 30, 70, 20, makeControlFunction('filter'),
               drawAsToggled=True),
        # toggle invert
        Button('Invert', 80, 80, 70, 20, makeControlFunction('invert'),
               drawAsToggled=True),
        # toggle gate
        Button('Gate', 80, 130, 70, 20, makeControlFunction('gate'),
               drawAsToggled=True),
        # toggle compressor
        Button('Compressor', 80, 180, 70, 20, makeControlFunction('comp'),
               drawAsToggled=True),
        # toggle clipping
        Button('Clipping', 80, 230, 70, 20, makeControlFunction('clipper'),
               drawAsToggled=True),
        # toggle distortion
        Button('Distortion', 80, 280, 70, 20, makeControlFunction('distortion'),
               drawAsToggled=True),
        # toggle reverb
        Button('Reverb', 80, 330, 70, 20, makeControlFunction('reverb'),
               drawAsToggled=True),
        # toggle convolution
        Button('Convolution', 80, 380, 70, 20, 
               makeControlFunction('convolution'), drawAsToggled=True),
        # mute dry
        Button('M', 315, 420, 10, 10, makeControlFunction('muteDry'),
               drawAsToggled=True, color='yellow', font='arial'),
        # mute wet
        Button('M', 355, 420, 10, 10, makeControlFunction('muteWet'),
               drawAsToggled=True, color='yellow', font='arial')
    ]