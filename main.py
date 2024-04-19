from UIClasses import *
from cmu_graphics import *
from makeControls import *
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

#            ---------- general api calls and helpers ----------
def onAppStart(app):
    app.baseWindowSize = 500
    app.windowSize = 500 # app.windowSize == app.height, exists for clarity
    app.width, app.height = int(app.windowSize*(3/4)), app.windowSize
    app.backgroundColor = gradient('darkGray', 'lightSlateGray', start='top')
    app.inputDevice = None
    app.outputDevice = None

def onResize(app):
    app.windowSize = app.height
    forceResizeTo3By4(app)

def forceResizeTo3By4(app):
    if app.width != int(app.windowSize*3/4):
        # If the w : h ratio is anything other than 3 : 4, force it to 3 : 4,
        # always maintaining the height
        app.width, app.height = int(app.windowSize*3/4), app.windowSize

##################### SAMPLE RATE/BUFFER SIZE SCREEN ####################

def sampleRateBufferSize_onScreenActivate(app):     # @TODO
    app.sampleRate, app.bufferSize = None, None
    makeSampleAndBufferButtons(app)

def sampleRateBufferSize_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.backgroundColor)
    if app.sampleRate == None:
        drawLabel('Select a sample rate:', app.width/2, app.height/9, 
                  size=app.height/20)
        for button in app.sampleRateButtons: button.draw(app)
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
    if app.sampleRate != None and app.bufferSize != None:
        setActiveScreen('inputsScreen')

########################## SET INPUTS SCREEN ############################

# here lie the remains of the stuff now in makeControls.py

def inputsScreen_onScreenActivate(app):
    app.IOButtons = [ ]
    app.inputDevice = None
    app.outputDevice = None
    makeIOButtons(app, AudioStream.input_device_names, 'input')

def inputsScreen_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.backgroundColor)
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

def inputsScreen_onMouseMove(app, mX, mY):
    for button in app.IOButtons:
        # check if the button is hovered:
        button.mouseMove(mX, mY, app)

def inputsScreen_onMousePress(app, mX, mY):
    for button in app.IOButtons:
        button.checkIfPressed(mX, mY, app)
    if app.inputDevice != None and app.outputDevice != None:
        if (app.inputDevice == 'MacBook Pro Microphone' and
            app.outputDevice == 'MacBook Pro Speakers'):
            setActiveScreen('idiotCheckScreen')
            return
        makeAudioStream(app, app.sampleRate, app.bufferSize)
        setActiveScreen('mainScreen')

######################### IDIOT CHECK SCREEN ###########################
# because I made this mistake too many times
def idiotCheckScreen_onScreenActivate(app):
    makeIdiotCheckButtons(app)

def idiotCheckScreen_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.backgroundColor)
    drawLabel('Are you sure?', app.width/2, app.height/9, size=app.height/22)
    drawLabel('YOU FUCKING MORON', app.width/2, app.height/5.5,  # jest
              fill='crimson', font='impact', size=app.height/16,
              border='black')
    drawLabel('This will cause feedback!', app.width/2, app.height/4, 
              fill='red', font='impact', size=app.height/16,
              border='black')
    for button in app.idiotCheckScreenButtons:
        button.draw(app)

def idiotCheckScreen_onMouseMove(app, mX, mY):
    for button in app.idiotCheckScreenButtons:
        button.mouseMove(mX, mY, app)

def idiotCheckScreen_onMousePress(app, mX, mY):
    for button in app.idiotCheckScreenButtons:
        button.checkIfPressed(mX, mY, app)

############################# MAIN SCREEN ##############################

# here lies the remains of stuff now in makeControls.py

def mainScreen_onScreenActivate(app):
    app.filterColor = 'gold'
    app.gateColor = 'khaki'
    app.compColor = 'oliveDrab'
    app.distColor = 'fireBrick'
    app.bitcrushColor = 'lime'
    app.chorusColor = 'teal'
    app.delayColor = 'orange'
    app.reverbColor = 'skyBlue'
    app.convolutionColor = 'thistle'
    makeControlObjects(app)

def mainScreen_drawPrettyStuff(app):
    # where everything that makes stuff look better but does nothing else goes
    realWindowHeight = app.height*19.5/20
    textSize = app.height/28
    textOffset = app.height/50
    drawLine(app.width/2, 0, app.width/2, app.height)
    for i in range(1, 5):
        lineHeight = (realWindowHeight/5)*i
        drawLine(0, lineHeight, app.width, lineHeight)
    drawLabel('F   i   L   T   E   R', app.width/45, textOffset, 
              font='arial', fill=app.filterColor, align='left', size=textSize)
    drawLabel('G   A   T   e', app.width/45, realWindowHeight/5 + textOffset, 
              font='arial', fill=app.gateColor, align='left', size=textSize)
    drawLabel('C   O   m   P', app.width/45, realWindowHeight*2/5 + textOffset,
              font='arial', fill=app.compColor, align='left', size=textSize)
    drawLabel('C   L   i   P /D   i   S   T', app.width/45,
              realWindowHeight*3/5 + textOffset, font='arial', 
              fill=app.distColor, align='left', size=textSize),
    drawLabel('B   i   T   C   R   S   H', app.width/45,
              realWindowHeight*4/5 + textOffset, font='arial',
              fill=app.bitcrushColor, align='left', size=textSize),
    drawLabel('C   H   O   R   u   S', app.width/2 + app.width/45,
              textOffset, fill=app.chorusColor, align='left', size=textSize),
    drawLabel('D   E   L   A   y', app.width/2 + app.width/45,
              realWindowHeight/5 + textOffset, font='arial', 
              fill=app.delayColor, align='left', size=textSize),
    drawLabel('R   e   V   E   R   B', app.width/2 + app.width/45, 
              realWindowHeight*2/5 + textOffset, font='arial',
              fill=app.reverbColor, align='left', size=textSize)
    drawLabel('C   O   N   V   o   L   V', app.width/2 + app.width/45,
              realWindowHeight*3/5 + textOffset, font='arial',
              fill=app.convolutionColor, align='left', size=textSize)
    drawLabel('M   A   S   T   E   r', app.width/2 + app.width/45,
              realWindowHeight*4/5 + textOffset, font='arial',
              fill='black', align='left', size=textSize)
    drawRect(0, app.height*19/20, app.width, app.height/20, 
             fill=gradient('darkGray', 'silver', start='bottom'))
    drawLabel('MFX-112', app.width/12, app.height*19.5/20, font='impact',
              size=app.height/35, italic=True, 
              fill=gradient('gainsboro', 'white', start='left'))

def mainScreen_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.backgroundColor)
    mainScreen_drawPrettyStuff(app)
    # draw the actual stuff:
    for control in app.activeButtons + app.activeKnobs:
        control.draw(app)

def mainScreen_onMousePress(app, mX, mY):
    for control in app.activeButtons + app.activeKnobs:
        control.checkIfPressed(mX, mY, app)
    print(mX, mY)

def mainScreen_onMouseMove(app, mX, mY):
    for control in app.activeButtons + app.activeKnobs:
        control.mouseMove(mX, mY, app)

def mainScreen_onMouseDrag(app, mX, mY):
    for knob in app.activeKnobs:
        knob.mouseDrag(mY, app)

def mainScreen_onMouseRelease(app, mX, mY):
    for knob in app.activeKnobs:
        knob.mouseRelease()

def mainScreen_onKeyPress(app, key):
    if key == '`':
        for knob in app.activeKnobs:
            knob.toggleLowSens()

def mainScreen_onKeyRelease(app, key):
    if key == '`':
        for knob in app.activeKnobs:
            knob.toggleLowSens()

def mainScreen_onStep(app):
    for knob in app.activeKnobs:
        knob.stepTimer(app)

################################# MAIN() ################################
def main():
    runAppWithScreens('sampleRateBufferSize')

main()