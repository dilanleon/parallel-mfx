from AudioHandler import *
from cmu_graphics import *
from UIClasses import Button
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
    app.IOButtons = [ ]
    app.controlObjects = [ ]
    createIOButtons(app, AudioStream.input_device_names, 'input')

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
                labelColor='darkSlateGray', font='arial'
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
    # Just make sure, since we're getting the user to select I/O,
    # that there is no assigned I/O
    app.inputDevice, app.outputDevice == None, None

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
        app.audio = AudioHandler(app.inputDevice, app.outputDevice)
        setActiveScreen('mainScreen')


############################# MAIN SCREEN ##############################

def mainScreen_onScreenActivate(app):
    # for i in range(len(app.audio.effectOrder)):
    #     app.controlObjects.append(
    #         Button(str(type(app.audio.effectOrder)), app.width/2, 
    #                app.height/5+i*app.height/15, app.width/2, app.height/16,
    #                ))
    pass

def mainScreen_redrawAll(app):
    drawRect(0, 0, app.width, app.height)
    drawLabel(
        'Under Construction', app.width/2, app.height/2, size=40,
              bold=True, fill='antiqueWhite')
    drawLabel(
        'sound will be coming through your speakers now', app.width/2,
        app.height*8/9, bold=True, fill='antiqueWhite'
              )

def main():
    runAppWithScreens('inputsScreen')

main()