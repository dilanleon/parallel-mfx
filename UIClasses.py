from cmu_graphics import *
import math

# inexcusably consulted stack overflow for one little thing:
# format(n, 'xf') - formats x decimals of float n to a string
# this function is innacurate, but it's purely for UI so it doesn't matter
# found in Knob -> draw() -> if mouseHold or alwaysShowVal
# https://stackoverflow.com/questions/13479163/round-float-to-x-decimals

# ####################    Button Class    #########################
class Button:
    
    def __init__(self, labelText, cx, cy, width, height, function,
                 border='black', color='white', labelColor='black', 
                 hoverBorderColor='orange', borderWidth=1, font='monospace', 
                 labelSize=None, boldText=False, italicText=False, 
                 drawAsToggled=False):
        self.labelText = labelText
        self.cx, self.cy = cx, cy
        self.width, self.height = width, height
        self.function = function
        self.border = border
        self.color = color
        self.labelColor = labelColor
        self.hoverBorderColor = hoverBorderColor
        self.borderWidth = borderWidth
        self.font = font
        self.boldText = boldText
        self.italicText = italicText
        self.drawAsToggled = drawAsToggled
        self.hovered = False
        if drawAsToggled:
            self.toggled = False
        if labelSize == None:
            self.labelSize = min(self.width/len(self.labelText)+3, self.height)

    def isMouseInside(self, mX, mY):
        # checks if the mouse is inside the Button's Bounding Box (BBB)
        scaledX, scaledY, scaledWidth, scaledHeight = self.getScaledXYWH(app)
        return (scaledX - (scaledWidth/2) < mX < scaledX + (scaledWidth/2) and
                scaledY - (scaledHeight/2) < mY < scaledY + (scaledHeight/2))
    
    def checkIfPressed(self, mX, mY, app):
        # If the button is pressed, call its assigned function
        # scale by sizeConstant to check by where the button actually is
        if self.isMouseInside(mX, mY):
            self.function(app)
            if self.drawAsToggled:
                self.toggled = not self.toggled
    
    def mouseMove(self, mX, mY):
        # hovering effect
        if self.isMouseInside(mX, mY):
            self.hovered = True
        else:
            self.hovered = False
        
    def draw(self, app):
        # Should only be called in redrawAll(app)
        x, y, w, h = self.getScaledXYWH(app)
        sizeConstant = app.windowSize/500
        if self.hovered:
            borderColor = self.hoverBorderColor
        else:
            borderColor = self.border
        drawRect(x, y, w, h, fill=self.color, border=borderColor, 
                 borderWidth=self.borderWidth, align='center')
        drawLabel(self.labelText, x, y, size=self.labelSize*sizeConstant,
                  font=self.font, fill=self.labelColor, bold=self.boldText,
                  italic=self.italicText)
        if self.drawAsToggled and not self.toggled:
            drawRect(x, y, w, h, fill=self.labelColor, border=borderColor,
                     opacity=50, align='center')

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
                 borderWidth=1, alwaysShowVal=False, label=None, 
                 labelColor='black', percentKnob=False):
        self.cx, self.cy, self.radius = cx, cy, radius
        self.min, self.max = min, max
        self.defaultVal = defaultVal
        self.percentTransform, self.inversePercentTransform = (
            self.createCurveFunction(curveFunction))
        self.label=label
        self.resetPosition()
        self.function = function
        self.color = color
        self.accentColor = accentColor
        self.labelColor = labelColor
        self.borderWidth = borderWidth
        self.alwaysShowVal=alwaysShowVal
        self.percentKnob = percentKnob # bool -> self.val represents a percent
        self.mouseHold = False
        self.lastY = None
        self.recentClick = False # to check if the timer should be incremented
        self.timer = 0          # to check if a knob has been double clicked
        self.sensitivity = 8
    
    def resetPosition(self):
        # reset the position of the knob to default
        self.val = self.defaultVal
        self.valPercent = self.inversePercentTransform()
        # !!! valPercent is % of 1k for better precision !!!
    
    def createCurveFunction(self, type):
        # needed for aliasing reasons
        if type == 'linear':
            def percentTransform():
                # % in, value out
                range = self.max - self.min
                return range * self.valPercent/1000 + self.min
            def inversePercentTransform():
                # value in, % out
                # normalizing to min = 0 means no risk of division by 0
                range = self.max - self.min
                adjustedVal = self.val - self.min
                return (adjustedVal/range)*1000
        elif type == 'logarithmic':
            # useful for non-linear things, like frequency and volume
            def percentTransform():
                # % in, value out
                range = self.max - self.min
                percentLog = (
                    # get the percent**2, add 1 (no log(0)), divide by 2*2
                    # i.e. (100**2/(10**3)**2) = 1, therefore
                    # log10(100**2)/4 = 1 and any % < 1 will scale by log10.
                    # by squaring, the bottom of the range is less dense
                    # (tested higher powers but the difference is negligible)
                    (math.log10(self.valPercent**2 + 1))/6)
                return range * percentLog + self.min
            def inversePercentTransform():
                # value in, % out
                # normalize to min = 0
                range = self.max - self.min
                adjustedVal = self.val - self.min
                scaledPercent = adjustedVal/range
                # undo the logarithmic scaling(just percentLog in reverse)
                return (10**(6 * scaledPercent) - 1)**0.5
                # to be implemented
        elif type == 'exponential':
            def percentTransform():
                # % in, value out
                range = self.max - self.min
                # higher power = steeper curve, 4 is a nice middle ground
                scaledPercent = self.valPercent**4/1000**4
                return range * scaledPercent + self.min
            def inversePercentTransform():
                # value in, % out
                range = self.max - self.min
                adjustedVal = self.val - self.min
                scaledPercent = adjustedVal/range
                return (scaledPercent*1000**4)**0.25
        else:
            raise Exception("ArgError: curveFunction must be 'linear'" +
                            " or 'logarithmic' or 'exponential'")
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
            scaledW = r*1.7
            scaledH = r*0.9
            drawRect(x, y - r*1.5, scaledW, scaledH, fill=self.color, 
                     align='center', border=self.accentColor, 
                     borderWidth=self.borderWidth)
            if self.percentKnob:
                # if it's a percent knob, display the integer percent and %
                displayVal = str(int(self.val*100)) + '%'
            elif abs(self.val) < 1:
                # else, if it's below 1, display 2 decimals
                displayVal = format(self.val, '.2f')
            elif abs(self.val) < 10 or 0 < self.val < 100:
                # else, display decimals where possible (3 chars max)
                displayVal = format(self.val, '.1f')
            elif abs(self.val) < 1000:
                # else, int is fine for numbers less than 1k
                displayVal = int(self.val)
            else:
                # else, display (thousands).(hundreds)k
                megaVal = format(self.val/1000, '.1f')
                displayVal = f'{megaVal}k'
            drawLabel(displayVal, x, y - r*1.5, size=r*0.5, font='monospace',
                      fill=self.labelColor)
        if self.label != None:
            drawLabel(self.label, x, y + r*1.33, size=11*sizeConstant, 
                      fill=self.labelColor)
    
    def getPointOnEdge(self, x, y, r):
        # Get the desired angle in radians of a particular value first
        angleRads = math.pi*5/4 - (math.pi*3/2) * self.valPercent/1000
        # then, return x, y minus the coords of that on the unit circle times r
        return (x + math.cos(angleRads)*r, y - math.sin(angleRads)*r)

    def checkIfPressed(self, mX, mY, app):
        x, y, r = self.getScaledXYRad(app)
        if ((x - mX)**2 + (y - mY)**2)**0.5 < r: # distance function
            self.mouseHold = True
            self.lastY = mY
            if self.recentClick:
                self.resetPosition()
                self.function(app, self.val)
            self.recentClick = True
    
    def mouseDrag(self, mY, app):
        # All the changes to the params based on knob position happen here
        if self.mouseHold:
            self.valPercent -= (mY - self.lastY)*self.sensitivity
            self.checkBounds()
            self.lastY = mY
            self.val = self.percentTransform()
            self.function(app, self.val)
    
    def mouseRelease(self):
        self.lastY = None
        self.mouseHold = False

    def checkBounds(self):
        # Make sure the value stays within the min, max bounds
        if self.valPercent > 1000:
            self.valPercent = 1000
        elif self.valPercent < 0:
            self.valPercent = 0
    
    def stepTimer(self, app):
        if self.recentClick:
            self.timer += 1
            if self.timer > app.stepsPerSecond/5: # 200ms double click window
                self.timer = 0
                self.recentClick = False
    
    def toggleLowSens(self):
        if self.sensitivity == 8:
            self.sensitivity = 1
        else:
            self.sensitivity = 8

    def getScaledXYRad(self, app):
        # similar to button class. returns scaled x, y, and radius
        sizeConstant = app.windowSize/500
        scaledX, scaledY = self.cx*sizeConstant, self.cy*sizeConstant
        scaledRad = self.radius*sizeConstant
        return scaledX, scaledY, scaledRad