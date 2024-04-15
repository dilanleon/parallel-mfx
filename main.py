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

########################## SET INPUTS SCREEN ############################

# here lie the remains of the stuff now in makeControls.py

def inputsScreen_onScreenActivate(app):
    app.IOButtons = [ ]
    app.inputDevice = None
    app.outputDevice = None
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

def inputsScreen_onMouseMove(app, mX, mY):
    for button in app.IOButtons:
        button.mouseMove(mX, mY, app)

def inputsScreen_onMousePress(app, mX, mY):
    for button in app.IOButtons:
        button.checkIfPressed(mX, mY, app)
    if app.inputDevice != None and app.outputDevice != None:
        if (app.inputDevice == 'MacBook Pro Microphone' and
            app.outputDevice == 'MacBook Pro Speakers'):
            setActiveScreen('idiotCheckScreen')
            return
        makeAudioStream(app)
        setActiveScreen('mainScreen')

######################### IDIOT CHECK SCREEN ###########################
# because I made this mistake too many times
def idiotCheckScreen_onScreenActivate(app):
    app.idiotCheckScreenButtons = [
        Button('NO', 125, 250, 70, 35, getIdiotCheckYesNoFunction('no')),
        Button('YES', 250, 250, 70, 35, getIdiotCheckYesNoFunction('yes'))
    ]

def idiotCheckScreen_redrawAll(app):
    drawLabel('Are you sure?', app.width/2, app.height/9, size=app.height/22)
    drawLabel('This will cause feedback!', app.width/2, app.height/5, 
              fill='red', font='impact', size=app.height/22)
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
    makeControlObjects(app)

def mainScreen_redrawAll(app):
    sizeConstant = app.height/app.baseWindowSize
    drawRect(0, app.height*19/20, app.width, app.height/20, fill='dimGray')
    drawLabel('PBPP-112', app.width/12, app.height*19.5/20, font='impact',
              size=14*sizeConstant, italic=True, fill='ghostWhite')
    for button in app.activeButtons:
        button.draw(app)
    for knob in app.activeKnobs:
        knob.draw(app)

def mainScreen_onMousePress(app, mX, mY):
    for button in app.activeButtons:
        button.checkIfPressed(mX, mY, app)
    for knob in app.activeKnobs:
        knob.checkIfPressed(mX, mY, app)

def mainScreen_onMouseMove(app, mX, mY):
    for button in app.activeButtons:
        button.mouseMove(mX, mY, app)

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
    runAppWithScreens('inputsScreen')

main()