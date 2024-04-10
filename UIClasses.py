from cmu_graphics import *
import math

# inexcusably consulted stack overflow for one little thing:
# this method is innacurate, but it's purely for UI so it doesn't matter
# found in Knob -> draw() -> if mouseHold or alwaysShowVal
# https://stackoverflow.com/questions/13479163/round-float-to-x-decimals

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

    def __init__(self, cx, cy, radius, min, max, defaultVal, function,
                 curveFunction='linear', color='white', accentColor='black', 
                 borderWidth=2, alwaysShowVal=False):
        self.cx, self.cy, self.radius = cx, cy, radius
        self.min, self.max = min, max
        self.defaultVal = defaultVal
        self.percentTransform, self.inversePercentTransform = (
            self.createCurveFunction(curveFunction))
        self.resetPosition()
        self.function = function
        self.color = color
        self.accentColor = accentColor
        self.borderWidth = borderWidth
        self.alwaysShowVal=alwaysShowVal
        self.mouseHold = False
        self.lastY = None
        self.recentClick = False # to check if the timer should be incremented
        self.timer = 0          # to check if a knob has been double clicked
    
    def resetPosition(self):
        # reset the position of the knob to default
        self.val = self.defaultVal
        # TO DO: Fix below line for log knobs
        self.valPercent = self.inversePercentTransform()
        
    
    def createCurveFunction(self, type):
        # needed for aliasing reasons
        if type == 'linear':
            def percentTransform():
                range = self.max - self.min
                return range * self.valPercent/100 + self.min
            def inversePercentTransform():
                # normalizing to min = 0 means no risk of division by 0
                adjustedMax = self.max - self.min   # sets min to 0
                adjustedVal = self.val - self.min
                return (adjustedVal/adjustedMax)*100
        elif type == 'logarithmic':
            # useful for non-linear things, like frequency and volume
            def percentTransform():
                range = self.max - self.min
                percentLog = (
                    # get the percent**2, add 1 (no log(0)), divide by 2*2
                    # i.e. (100**2/(10**2)**2) = 1, therefore
                    # log10(100**2)/4 = 1 and any % < 1 will scale by log10.
                    # by squaring, the bottom of the range is less dense
                    # (tested higher powers but the difference is negligible)
                    (math.log10(self.valPercent**2 + 1))/4)
                return range * percentLog + self.min
            def inversePercentTransform():
                # normalize to min = 0
                adjustedMax = self.max - self.min
                adjustedVal = self.val - self.min
                # to be implemented
                return 80 # placeholder
        # If type is not 'linear' or 'logarithmic', code will crash here (good)
        return percentTransform, inversePercentTransform
    
    def draw(self, app):
        x, y, r = self.getScaledXYRad(app)
        sizeConstant = app.windowSize/500
        drawCircle(x, y, r, fill=self.color, border=self.accentColor,
                   borderWidth=self.borderWidth)
        x1, y1 = self.getPointOnEdge(x, y, r) # pass these in to not compute x2
        drawLine(x, y, x1, y1, fill=self.accentColor)
        if self.mouseHold or self.alwaysShowVal:
            # When changing the parameter, display its value
            drawRect(x, y - r*1.5, r*1.3, r*0.9, fill=self.color, 
                     align='center', border=self.accentColor, 
                     borderWidth=self.borderWidth, opacity=50)
            if abs(self.val) < 10:
                # display with decimal precision for numbers < 10
                displayVal = format(self.val, '.1f')
            else:
                # otherwise int is fine
                displayVal = int(self.val)
            drawLabel(displayVal, x, y - r*1.5, size=r*0.5, font='monospace',
                      fill=self.accentColor)
    
    def getPointOnEdge(self, x, y, r):
        # Get the desired angle in radians of a particular value first
        angleRads = math.pi*5/4 - (math.pi*3/2) * self.valPercent/100
        # then, return x, y minus the coords of that on the unit circle times r
        return (x + math.cos(angleRads)*r, y - math.sin(angleRads)*r)

    def checkIfPressed(self, mX, mY, app):
        x, y, r = self.getScaledXYRad(app)
        if ((x - mX)**2 + (y - mY)**2)**0.5 < r: # distance function
            self.mouseHold = True
            self.lastY = mY
            if self.recentClick:
                self.resetPosition()
            self.recentClick = True
    
    def mouseDrag(self, mY, app):
        # All the changes to the params based on knob position happen here
        if self.mouseHold:
            self.valPercent -= mY - self.lastY # up is down
            self.checkBounds()
            self.lastY = mY
            self.val = self.percentTransform()
            self.function(app, self.val)
    
    def mouseRelease(self):
        self.lastY = None
        self.mouseHold = False

    def checkBounds(self):
        # Make sure the value stays within the min, max bounds
        if self.valPercent > 100:
            self.valPercent = 100
        elif self.valPercent < 0:
            self.valPercent = 0
    
    def stepTimer(self, app):
        if self.recentClick:
            self.timer += 1
            if self.timer > app.stepsPerSecond/5: # 200ms double click window
                self.timer = 0
                self.recentClick = False

    def getScaledXYRad(self, app):
        # similar to button class. returns scaled x, y, and radius
        sizeConstant = app.windowSize/500
        scaledX, scaledY = self.cx*sizeConstant, self.cy*sizeConstant
        scaledRad = self.radius*sizeConstant
        return scaledX, scaledY, scaledRad

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
    app.knob = Knob(200, 200, 30, -100, 6, 0, knobFunction, color='red',
                    alwaysShowVal=True)
    app.knoblog = Knob(260, 260, 30, -100, 6, 0, knobFunction, 
                       curveFunction='logarithmic', alwaysShowVal=True)
    app.altHeld = False

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
    app.knoblog.draw(app)

def onMousePress(app, mX, mY):
    app.button.checkIfPressed(mX, mY, app)
    app.knob.checkIfPressed(mX, mY, app)
    app.knoblog.checkIfPressed(mX, mY, app)

def onMouseDrag(app, mX, mY):
    app.knob.mouseDrag(mY, app)
    app.knoblog.mouseDrag(mY, app)

def onMouseRelease(app, mX, mY):
    app.knob.mouseRelease()
    app.knoblog.mouseRelease()

def onStep(app):
    app.knob.stepTimer(app)
    app.knoblog.stepTimer(app)

testUIElements()