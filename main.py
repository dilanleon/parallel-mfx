from AudioHandler import AudioHandler
from UIClasses import *
from cmu_graphics import *
from pedalboard.io import AudioStream

# Parallel Bandpass Drum Dynamics, Harmonics, and Reverb Processing
# PBPP-112 (Parallel Band Pass Processor for 15-112)
# Written by Dilan Juan Leon for CMU 15-112 project2

'''
Sources:

Pedalboard:
https://spotify.github.io/pedalboard/index.html

Ambiances by EchoThief:
http://www.echothief.com/

'''


###############################################################################
############################# CMU_GRAPHICS APP ################################
###############################################################################

#               ---------- general functions ----------
def onAppStart(app):
    app.windowSize = 500 # app.windowSize == app.height
    app.width, app.height = int(app.windowSize*(3/4)), app.windowSize
    app.inputDevice = None
    app.outputDevice = None

def onResize(app):
    app.windowSize = app.height
    forceResizeTo3By4(app)

def forceResizeTo3By4(app):
    if app.width != int(app.height*3/4):
        # If the w : h ratio is anything other than 3 : 4, force it to 3 : 4,
        # always maintaining the height
        app.width, app.height = int(app.height*3/4), app.height


########################## SET INPUTS SCREEN ############################

#                       ------ helpers --------
def createIOButtons(app, IOList, direction):
    for i in range(len(IOList)):
        getInputName = makeIOSetterFunction(i, direction)
        app.IOButtons.append(
            Button(
                IOList[i], app.width/2, app.height/5+i*app.height/15, 
                app.width/2, app.height/16, getInputName, color='antiqueWhite', 
                labelColor='darkSlateGray', font='arial', boldText=True
                )
            )

def makeIOSetterFunction(i, direction):
    # Creates a function that returns index i of the list of I/O devices.
    # Direction should be set to 'input' or 'output'.
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
#                 -------- api called functions --------
def inputsScreen_onScreenActivate(app):
    app.IOButtons = [ ]
    createIOButtons(app, AudioStream.input_device_names, 'input')

def inputsScreen_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='slateGray')
    if app.inputDevice == None:
        drawLabel(
            'Please select an input device.', app.width/2, app.height/9,
            size=app.height/20
            )
        for button in app.IOButtons: button.draw(app)
    else:
        drawLabel(
            'Please select an output device.', app.width/2, app.height/9,
            size=app.height/20
            )
        for button in app.IOButtons: button.draw(app)

def inputsScreen_onMousePress(app, mX, mY):
    for button in app.IOButtons:
        button.checkIfPressed(mX, mY, app)
    if app.inputDevice != None and app.outputDevice != None:
        app.audio = AudioHandler(app.inputDevice, app.outputDevice, 
                                 bufferSize=256)
        setActiveScreen('mainScreen')

############################# MAIN SCREEN ##############################

#                   -----     helpers       -----
def makeControlFunction(type):
    # Functions used by knobs and buttons throughout the app
    #                        *buttons*
    def switchToInputsScreen(app):
        # button always calls function(app), even if app isn't needed
        # Need to find a way to end the audiostream here @TODO
        app.audio.killStream() # doesnt work
        app.inputDevice, app.outputDevice = None, None
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
    app.activeKnobs = [
        # filter freq
        Knob(155, 30, 17, 20, 20000, 175, makeControlFunction('filterFreq'),
             curveFunction='exponential', label='freq', color='gold'),
        # filter resonance
        Knob(200, 30, 17, 0, 1, 0, makeControlFunction('filterResonance'),
             curveFunction='linear', label='reso', color='gold'),
        # filter drive
        Knob(245, 30, 17, 1, 10, 1, makeControlFunction('filterDrive'),
             curveFunction='linear', label='drive', color='gold'),
        # gate threshold
        Knob(155, 130, 17, -60, 0, -60, makeControlFunction('gateThresh'),
             curveFunction='logarithmic', label='thresh', color='khaki'),
        # gate ratio
        Knob(200, 130, 17, 1, 10, 2.5, makeControlFunction('gateRatio'),
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
             curveFunction='linear', label='size', color='skyBlue'),
        # reverb damping
        Knob(200, 330, 17, 0, 1, 0.5, makeControlFunction('reverbDamping'),
             curveFunction='linear', label='damping', color='skyBlue'),
        # reverb dry/wet
        Knob(245, 330, 17, 0, 1, 0.5, makeControlFunction('reverbDryWet'),
             curveFunction='linear', label='dry/wet', color='skyBlue'),
        # reverb width
        Knob(290, 330, 17, 0, 1, 0.5, makeControlFunction('reverbWidth'),
             curveFunction='linear', label='width', color='skyBlue'),
        # convolution mix
        Knob(155, 380, 17, 0, 1, 0.5, makeControlFunction('convolutionMix'),
             curveFunction='linear', label='mix', color='thistle'),
        # dry gain
        Knob(315, 445, 17, -60, 12, 0, makeControlFunction('gainDry'),
             curveFunction='logarithmic', color='lightSlateGray', 
             label='dBdry'),
        # wet gain
        Knob(355, 445, 17, -60, 12, 0, makeControlFunction('gainWet'), 
            curveFunction='logarithmic', color='darkRed', label='dBwet')
    ]
    app.activeButtons = [
        Button('Edit I/O', 350, 487.5, 44, 12.5, 
               makeControlFunction('switchToInputsScreen'), color='gray', 
               labelColor='ghostWhite', font='arial',
               border=None, italicText=True),
        Button('Filter', 80, 30, 70, 20, makeControlFunction('filter'),
               drawAsToggled=True),
        Button('Invert', 80, 80, 70, 20, makeControlFunction('invert'),
               drawAsToggled=True),
        Button('Gate', 80, 130, 70, 20, makeControlFunction('gate'),
               drawAsToggled=True),
        Button('Compressor', 80, 180, 70, 20, makeControlFunction('comp'),
               drawAsToggled=True),
        Button('Clipping', 80, 230, 70, 20, makeControlFunction('clipper'),
               drawAsToggled=True),
        Button('Distortion', 80, 280, 70, 20, makeControlFunction('distortion'),
               drawAsToggled=True),
        Button('Reverb', 80, 330, 70, 20, makeControlFunction('reverb'),
               drawAsToggled=True),
        Button('Convolution', 80, 380, 70, 20, 
               makeControlFunction('convolution'), drawAsToggled=True),
        # mute dry
        Button('M', 315, 420, 10, 10, makeControlFunction('muteDry'),
               drawAsToggled=True, color='yellow'),
        # mute wet
        Button('M', 355, 420, 10, 10, makeControlFunction('muteWet'),
               drawAsToggled=True, color='yellow')
    ]
#                  -----------------------------------

def mainScreen_onScreenActivate(app):
    makeControlObjects(app)
    app.showMousePos = False

def mainScreen_redrawAll(app):
    sizeConstant = app.height/500
    drawRect(0, app.height*19/20, app.width, app.height/20, fill='dimGray')
    drawLabel('PBPP-112', app.width/10, app.height*19.5/20, 
              size=14*sizeConstant, bold=True, italic=True, fill='ghostWhite')
    for button in app.activeButtons:
        button.draw(app)
    for knob in app.activeKnobs:
        knob.draw(app)

def mainScreen_onMouseMove(app, mX, mY):
    if app.showMousePos:    # useful for creating the UI
        print(mX, mY)

def mainScreen_onMousePress(app, mX, mY):
    for button in app.activeButtons:
        button.checkIfPressed(mX, mY, app)
    for knob in app.activeKnobs:
        knob.checkIfPressed(mX, mY, app)

def mainScreen_onMouseDrag(app, mX, mY):
    for knob in app.activeKnobs:
        knob.mouseDrag(mY, app)

def mainScreen_onMouseRelease(app, mX, mY):
    for knob in app.activeKnobs:
        knob.mouseRelease()

def mainScreen_onStep(app):
    for knob in app.activeKnobs:
        knob.stepTimer(app)

def mainScreen_onKeyPress(app, key):
    if key == 'p':
        app.showMousePos = not app.showMousePos


################################# MAIN() ################################
def main():
    runAppWithScreens('inputsScreen')

main()

