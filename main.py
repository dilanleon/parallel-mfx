from UIClasses import *
from cmu_graphics import *
from makeControls import *
from pedalboard.io import AudioStream

# Realtime Parallel Multi-Effects Processing using Pedalboard
# MFX-112 (Multi Effects Processor for 15-112)
# Written by Dilan Juan Leon for CMU 15-112 project2

'''
Standout features:
 - Realtime audio processing
    - HPF, LPF, BPF, all with 12 or 24 db/octave slopes and inverse polarity
    - Noise Gate, Compressor, Clipping, Distortion, Bitcrush, Chorus, Delay,
      Reverb, Convolution Reverb with a free library of IRs
    - Dry channel and wet channel, both with mute buttons
 - All UI scales to window height, supporting windows of arbitrary height
 - Snaps to 3:4 window scaling based on height
 - Impulse response selection reads files in /EchoThiefImpulseResponseLibrary/
 - Knob class with logarithmic, exponential, or linear knobs
 - Mouse hover effects for buttons/knobs
 - Automatic scaling for control objects - makes UI design easier
 - User selectable I/O, buffer size, and sample rate
 - Idiot check screen if input and output are mic/speakers
 - Supports virtual audio devices, so can be passed through a DAW


Sources:

Pedalboard:
https://spotify.github.io/pedalboard/index.html

Ambiances by EchoThief:
http://www.echothief.com/

Additionally consulted:

https://stackoverflow.com/questions/9390126/pythonic-way-to-check-if-something-exists

https://stackoverflow.com/questions/13479163/round-float-to-x-decimals

https://builtin.com/data-science/python-list-files-in-directory

https://www.geeksforgeeks.org/execute-string-code-python/
'''


###############################################################################
############################# CMU_GRAPHICS APP ################################
###############################################################################

#            ---------- general api calls and helpers ----------
def onAppStart(app):
    app.baseWindowSize = 500 # size that buttons/knobs scale to
    app.windowSize = 500 # app.windowSize == app.height, exists for clarity
    app.width, app.height = int(app.windowSize*(3/4)), app.windowSize
    app.backgroundColor = gradient('darkGray', 'lightSlateGray', start='top')
    app.inputDevice = None
    app.outputDevice = None

def onResize(app):
    app.windowSize = app.height
    forceResizeTo3By4(app)

def forceResizeTo3By4(app):
    # changes the width ONLY!
    if app.width != int(app.windowSize*3/4):
        # If the w : h ratio is anything other than 3 : 4, force it to 3 : 4,
        # always maintaining the height
        app.width, app.height = int(app.windowSize*3/4), app.windowSize

##################### SAMPLE RATE/BUFFER SIZE SCREEN ####################

def sampleRateBufferSize_onScreenActivate(app):
    # always reset sample rate and buffer size to None
    app.sampleRate, app.bufferSize = None, None
    makeSampleAndBufferButtons(app) # see makeControls.py

def sampleRateBufferSize_redrawAll(app):
    # background:
    drawRect(0, 0, app.width, app.height, fill=app.backgroundColor)
    # sample rate selection:
    if app.sampleRate == None:
        drawLabel('Select a sample rate:', app.width/2, app.height/9, 
                  size=app.height/20)
        for button in app.sampleRateButtons: button.draw(app)
    # buffer size selection:
    else:
        drawLabel('Select a buffer size:', app.width/2, app.height/9, 
                  size=app.height/20)
        for button in app.bufferSizeButtons: button.draw(app)

def sampleRateBufferSize_onMouseMove(app, mX, mY):
    for button in app.sampleRateButtons + app.bufferSizeButtons:
        # check for hover:
        button.mouseMove(mX, mY, app)

def sampleRateBufferSize_onMousePress(app, mX, mY):
    # these need to be separate or they will both get pressed at the same time
    if app.sampleRate == None:
        for button in app.sampleRateButtons:
            button.checkIfPressed(mX, mY, app)
    else:
        for button in app.bufferSizeButtons:
            button.checkIfPressed(mX, mY, app)
    # If they are both set on mouse press, switch to the input screen
    if app.sampleRate != None and app.bufferSize != None:
        setActiveScreen('inputsScreen')

########################## SET INPUTS SCREEN ############################

# here lie the remains of the stuff now in makeControls.py

def inputsScreen_onScreenActivate(app):
    # reset:
    app.IOButtons = [ ]
    app.inputDevice = None
    app.outputDevice = None
    makeIOButtons(app, AudioStream.input_device_names, 'input')

def inputsScreen_redrawAll(app):
    # draw background:
    drawRect(0, 0, app.width, app.height, fill=app.backgroundColor)
    # input buttons:
    if app.inputDevice == None:
        drawLabel(
            'Please select an input device.', app.width/2, app.height/9,
            size=app.height/20
            )
        for button in app.IOButtons: button.draw(app)
    # output buttons:
    else:
        drawLabel(
            'Please select an output device.', app.width/2, app.height/9,
            size=app.height/20
            )
        for button in app.IOButtons: button.draw(app)

def inputsScreen_onMouseMove(app, mX, mY):
    # check if the button is hovered:
    for button in app.IOButtons:
        button.mouseMove(mX, mY, app)

def inputsScreen_checkForFeedback(app):
    # checks if 'microphone' and 'speakers' are in the input/output:
    return ('microphone' in app.inputDevice.lower() and 
            'speakers' in app.outputDevice.lower())

def inputsScreen_onMousePress(app, mX, mY):
    # check if a button has been pressed:
    for button in app.IOButtons:
        button.checkIfPressed(mX, mY, app)
    # check if the I/O has been set:
    if app.inputDevice != None and app.outputDevice != None:
        # if it's going to feedback, check with the user:
        if inputsScreen_checkForFeedback(app):
            setActiveScreen('idiotCheckScreen')
            return
        # otherwise, go ahead to the main app:
        makeAudioStream(app)
        setActiveScreen('mainScreen')

######################### IDIOT CHECK SCREEN ###########################
# because I made this mistake too many times
def idiotCheckScreen_onScreenActivate(app):
    makeIdiotCheckButtons(app)  # makeControls.py

def idiotCheckScreen_redrawAll(app):
    # background:
    drawRect(0, 0, app.width, app.height, fill=app.backgroundColor)
    # text:
    drawLabel('Are you sure?', app.width/2, app.height/9, size=app.height/22)
    drawLabel('YOU FUCKING MORON!', app.width/2, app.height/5.5,  # jest
              fill='crimson', font='arial', size=app.height/16, bold=True, 
              italic=True)
    drawLabel('This will cause feedback!', app.width/2, app.height/4, 
              fill='red', font='arial', size=app.height/16, bold=True)
    # yes/no:
    for button in app.idiotCheckScreenButtons:
        button.draw(app)

def idiotCheckScreen_onMouseMove(app, mX, mY):
    # for hover highlighting
    for button in app.idiotCheckScreenButtons:
        button.mouseMove(mX, mY, app)

def idiotCheckScreen_onMousePress(app, mX, mY):
    # check for button press
    for button in app.idiotCheckScreenButtons:
        button.checkIfPressed(mX, mY, app)

########################## IR SELECT SCREEN ############################

def IRSelectScreen_onScreenActivate(app):
    # reset IR path
    app.IRpath = ''
    # make an empy list of buttons (none are displayed at first)
    app.IRButtons = [ ]
    makeFolderButtons(app) # makeControls.py

def IRSelectScreen_redrawAll(app):
    # background:
    drawRect(0, 0, app.width, app.height, fill=app.backgroundColor)
    # text:
    drawLabel('IR SELECT', app.width/2, app.height/30, size=app.height/20,
              bold=True, italic=True)
    # buttons:
    for button in app.IRFolderButtons + app.IRButtons:
        button.draw(app)

def IRSelectScreen_onMouseMove(app, mX, mY):
    # check for hover highlights:
    for button in app.IRFolderButtons + app.IRButtons:
        button.mouseMove(mX, mY, app)

def IRSelectScreen_onMousePress(app, mX, mY):
    # check for button presses:
    for button in app.IRFolderButtons + app.IRButtons:
        button.checkIfPressed(mX, mY, app)

############################# MAIN SCREEN ##############################

# here lies the remains of stuff now in makeControls.py

def mainScreen_onScreenActivate(app):
    app.filterColor = 'gold'
    app.gateColor = 'khaki'
    app.compColor = 'oliveDrab'
    app.distColor = 'maroon'
    app.bitcrushColor = 'lime'
    app.chorusColor = 'teal'
    app.delayColor = 'orange'
    app.reverbColor = 'skyBlue'
    app.convolutionColor = 'thistle'
    app.filterSlope = 12
    app.filterBand = 'BPF'
    # if the objects don't exist, make them:
    try:
        app.activeButtons + app.activeKnobs
    except AttributeError:
        makeControlObjects(app) # makeControls.py
    # otherwise, do nothing, because they already exist

def mainScreen_drawPrettyStuff(app):
    # where everything that makes things look better but does nothing else goes
    realWindowHeight = app.height*19.5/20 # excludes the bottom facia
    textSize = app.height/28 # for audio process types
    textOffset = app.height/50 # offset from the top of the screen/section
    drawLine(app.width/2, 0, app.width/2, app.height) # line down the middle
    for i in range(1, 5):
        lineHeight = (realWindowHeight/5)*i # lines to split in 4 vertically
        drawLine(0, lineHeight, app.width, lineHeight)
    drawLabel('F   i   L   T   E   R', app.width/60, textOffset, bold=True,
              font='arial', fill=app.filterColor, align='left', size=textSize)
    drawLabel('G   A   T   e', app.width/60, realWindowHeight/5 + textOffset, 
              font='arial', fill=app.gateColor, align='left', size=textSize,
              bold=True)
    drawLabel('C   O   m   P', app.width/60, realWindowHeight*2/5 + textOffset,
              font='arial', fill=app.compColor, align='left', size=textSize,
              bold=True)
    drawLabel('C   L   i   P /D   i   S   T', app.width/60,
              realWindowHeight*3/5 + textOffset, font='arial', bold=True,
              fill=app.distColor, align='left', size=textSize),
    drawLabel('B   i   T   C   R   S   H', app.width/60,
              realWindowHeight*4/5 + textOffset, font='arial', bold=True,
              fill=app.bitcrushColor, align='left', size=textSize),
    drawLabel('C   H   O   R   u   S', app.width/2 + app.width/60, textOffset, 
              bold=True, fill=app.chorusColor, align='left', size=textSize),
    drawLabel('D   E   L   A   y', app.width/2 + app.width/60,
              realWindowHeight/5 + textOffset, font='arial', bold=True,
              fill=app.delayColor, align='left', size=textSize),
    drawLabel('R   e   V   E   R   B', app.width/2 + app.width/60, 
              realWindowHeight*2/5 + textOffset, font='arial', bold=True,
              fill=app.reverbColor, align='left', size=textSize)
    drawLabel('C   O   N   V   o   L   V', app.width/2 + app.width/60,
              realWindowHeight*3/5 + textOffset, font='arial', bold=True,
              fill=app.convolutionColor, align='left', size=textSize)
    drawLabel(app.audio.getConvolutionName(), app.width*3/4, 
              realWindowHeight*3/5 + textOffset*1.95, font='arial', italic=True,
              fill='dimGray', size=textSize*0.3)
    drawLabel('M   A   S   T   E   r', app.width/2 + app.width/60,
              realWindowHeight*4/5 + textOffset, font='arial', bold=True,
              fill='black', align='left', size=textSize)
    # Bottom little facia thing:
    drawRect(0, app.height*19/20, app.width, app.height/20, 
             fill=gradient('darkGray', 'silver', start='bottom'))
    drawLabel('MFX-112', app.width/10, app.height*19.5/20, font='arial',
              size=app.height/35, italic=True, bold=True,
              fill=gradient('gainsboro', 'white', start='left'))

def mainScreen_redrawAll(app):
    # background:
    drawRect(0, 0, app.width, app.height, fill=app.backgroundColor)
    sizeConstant = app.windowSize/app.baseWindowSize
    mainScreen_drawPrettyStuff(app) # above
    # draw the actual controls:
    for control in app.activeButtons + app.activeKnobs:
        control.draw(app)
    # hacky way to darken the filter mode buttons when not toggled:
    if not app.audio.isPluginActive('Filter'):
        drawRect(5*sizeConstant, 45*sizeConstant, 20*sizeConstant, 
                 25*sizeConstant, opacity=50)

def mainScreen_onMousePress(app, mX, mY):
    # check if a control was clicked:
    for control in app.activeButtons + app.activeKnobs:
        control.checkIfPressed(mX, mY, app)

def mainScreen_onMouseMove(app, mX, mY):
    # check for hover effects:
    for control in app.activeButtons + app.activeKnobs:
        control.mouseMove(mX, mY, app)

def mainScreen_onMouseDrag(app, mX, mY):
    # check if a knob should be changed:
    for knob in app.activeKnobs:
        knob.mouseDrag(mY, app)

def mainScreen_onMouseRelease(app, mX, mY):
    # reset knob selected state
    for knob in app.activeKnobs:
        knob.mouseRelease()

def mainScreen_onKeyPress(app, key):
    # low knob sensitivity modifier
    if key == '`':
        for knob in app.activeKnobs:
            knob.toggleLowSens()

def mainScreen_onKeyRelease(app, key):
    # low knob sensitivity modifier
    if key == '`':
        for knob in app.activeKnobs:
            knob.toggleLowSens()

def mainScreen_onStep(app):
    # keep track of time for double click to reset knobs
    for knob in app.activeKnobs:
        knob.stepTimer(app)

################################# MAIN() ################################
def main():
    runAppWithScreens('sampleRateBufferSize')

main()
