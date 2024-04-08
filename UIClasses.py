from cmu_graphics import *
import math

# ####################    Button Class    #########################
class Button:
    
    def __init__(self, labelText, cx, cy, width, height, function,
                 border='black', color='white', labelColor='black', 
                 borderWidth=1, font='monospace', labelSize=None):
        self.labelText = labelText
        self.cx, self.cy = cx, cy
        self.width, self.height = width, height
        self.function = function
        self.border = border
        self.color = color
        self.labelColor = labelColor
        self.borderWidth = borderWidth
        self.font = font
        if labelSize == None:
            self.labelSize = min(self.width/len(self.labelText)+3, self.height)
    
    def checkIfPressed(self, mX, mY, app):
        # If the button is pressed, call its assigned function
        # scale by sizeConstant to make sure we check where the button is
        scaledX, scaledY, scaledWidth, scaledHeight = self.getScaledXYWH(app)
        if (scaledX - (scaledWidth/2) < mX < scaledX + (scaledWidth/2) and
            scaledY - (scaledHeight/2) < mY < scaledY + (scaledHeight/2)):
            self.function(app)
        
    def draw(self, app):
        # Should only be called in redrawAll(app)
        x, y, w, h = self.getScaledXYWH(app)
        sizeConstant = app.windowSize/500
        drawRect(x, y, w, h, fill=self.color, border=self.border, 
                 borderWidth=self.borderWidth, align='center')
        drawLabel(self.labelText, x, y, size=self.labelSize*sizeConstant,
                  font=self.font, fill=self.labelColor, bold=True)

    def getScaledXYWH(self, app):
        # returns the scaled bounds of the button (base scale = 500px height)
        sizeConstant = app.windowSize/500
        scaledX, scaledY = self.cx*sizeConstant, self.cy*sizeConstant
        scaledWidth = self.width*sizeConstant 
        scaledHeight = self.height*sizeConstant
        return scaledX, scaledY, scaledWidth, scaledHeight
    
# ########################    Knob Class    #############################
class Knob:

    def __init__(self, cx, cy, radius, min, max, functionCalled,
                 curveFunction='linear', color='white', 
                 accentColor='black', borderWidth=2):
        self.cx, self.cy, self.radius = cx, cy, radius
        self.min, self.max = min, max
        self.val = min
        self.functionCalled = functionCalled
        # TO DO: Implement non-linear knobs (for freq. for example)
        self.color = color
        self.accentColor = accentColor
        self.borderWidth = borderWidth
        self.mouseHold = False
        self.lastY = None
    
    def draw(self, app):
        x, y, r = self.getScaledXYRad(app)
        sizeConstant = app.windowSize/500
        drawCircle(x, y, r, fill=self.color, border=self.accentColor,
                   borderWidth=self.borderWidth)
        x1, y1 = self.getPointOnEdge(x, y, r) # pass these in to not compute x2
        drawLine(x, y, x1, y1, fill=self.accentColor)
        if self.mouseHold:
            # When changing the parameter, display its value
            drawRect(x, y - r*1.5, r*1.3, r*0.9, fill=self.color, 
                     align='center', border=self.accentColor, 
                     borderWidth=self.borderWidth, opacity=50)
            drawLabel(self.val, x, y - r*1.5, size=r*0.5, font='monospace',
                      fill=self.accentColor)
    
    def getPointOnEdge(self, x, y, r):
        # Get the desired angle of a particular value first
        angleRads = math.pi*5/4 - (math.pi*3/2) * self.val/self.max
        # then, return x, y - the coords of that on the unit circle times r
        return (x + math.cos(angleRads)*r, y - math.sin(angleRads)*r)

    def checkIfPressed(self, mX, mY, app):
        x, y, r = self.getScaledXYRad(app)
        if ((x - mX)**2 + (y - mY)**2)**0.5 < r: # distance function
            self.mouseHold = True
            self.lastY = mY
    
    def mouseDrag(self, mY, app):
        if self.mouseHold:
            self.val -= mY - self.lastY
            self.checkBounds()
            self.lastY = mY
            self.functionCalled(app, self.val)
    
    def mouseRelease(self):
        self.lastY = None
        self.mouseHold = False

    def checkBounds(self):
        # Make sure the value stays within the min, max bounds
        if self.val > self.max:
            self.val = self.max
        elif self.val < self.min:
            self.val = self.min

    def getScaledXYRad(self, app):
        # similar to button class. returns scaled x, y, and radius
        sizeConstant = app.windowSize/500
        scaledX, scaledY = self.cx*sizeConstant, self.cy*sizeConstant
        scaledRad = self.radius*sizeConstant
        return scaledX, scaledY, scaledRad

# #######################   Fader Class    ################################
class Fader:

    def __init__(self, cx, yBottom, yTop, faderWidth, faderHeight, 
                 functionCalled, min=-60, max=12, color='white', 
                 accentColor='black', grooveWidth=5):
        # faderWidth/Height refer to the clickable (or touchable IRL) part
        self.cx = cx
        self.yBottom, self.yTop = yBottom, yTop
        self.faderWidth = faderWidth
        self.faderHeight = faderHeight
        self.functionCalled = functionCalled
        self.min = min
        self.max = max
        self.color = color
        self.accentColor = accentColor
        self.grooveWidth = grooveWidth
    
    def getScaledXYWH(self, app):
        sizeConstant = app.windowSize/500
        scaledX = self.cx*sizeConstant
        scaledYBottom = self.yBottom*sizeConstant
        scaledYTop = self.yTop*sizeConstant
        scaledFaderWidth = self.faderWidth*sizeConstant
        scaledFaderHeight = self.faderHeight*sizeConstant
        return (scaledX, scaledYBottom, scaledYTop, 
                scaledFaderWidth, scaledFaderHeight)

######################### REMOVE FROM FINAL ###################################

# TESTING STUFF

def buttonFunction(app):
    print('button pressed')

def knobFunction(app, val):
    print(val)

def testUIElements():
    runApp()

def onAppStart(app):
    app.windowSize = 500
    app.width, app.height = int(app.windowSize*(3/4)), app.windowSize
    app.button = Button('press me', 50, 50, 50, 25, buttonFunction)
    app.knob = Knob(200, 200, 30, 0, 100, knobFunction)

def onResize(app):
    app.windowSize = app.height
    forceResizeTo3By4(app)

def forceResizeTo3By4(app):
    if app.width != int(app.height*3/4):
        # If the w : h ratio is anything other than 3 : 4, force it to 3 : 4,
        # always maintaining the height
        app.width, app.height = int(app.height*3/4), app.height

def redrawAll(app):
    app.button.draw(app)
    app.knob.draw(app)

def onMousePress(app, mX, mY):
    app.button.checkIfPressed(mX, mY, app)
    app.knob.checkIfPressed(mX, mY, app)

def onMouseDrag(app, mX, mY):
    app.knob.mouseDrag(mY, app)

def onMouseRelease(app, mX, mY):
    app.knob.mouseRelease()

testUIElements()