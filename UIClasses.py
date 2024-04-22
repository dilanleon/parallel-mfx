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
                 hoverBorderColor='red', borderWidth=1, font='monospace', 
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
        else:
            self.labelSize = labelSize

    def isMouseInside(self, mX, mY, app):
        # checks if the mouse is inside the Button's Bounding Box (BBB)
        scaledX, scaledY, scaledWidth, scaledHeight = self.getScaledXYWH(app)
        return (scaledX - (scaledWidth/2) < mX < scaledX + (scaledWidth/2) and
                scaledY - (scaledHeight/2) < mY < scaledY + (scaledHeight/2))
    
    def checkIfPressed(self, mX, mY, app):
        # If the button is pressed, call its assigned function:
        if self.isMouseInside(mX, mY, app):
            self.function(app)
            # if it's toggleable, toggle it:
            if self.drawAsToggled:
                self.toggled = not self.toggled
    
    def mouseMove(self, mX, mY, app):
        # 1/2 of the hovering effect:
        if self.isMouseInside(mX, mY, app):
            self.hovered = True
        else:
            self.hovered = False
        
    def draw(self, app):
        x, y, w, h = self.getScaledXYWH(app)
        sizeConstant = app.windowSize/app.baseWindowSize
        # set border color based on if hovered:
        if self.hovered:
            borderColor = self.hoverBorderColor
        else:
            borderColor = self.border
        # draw the stuff that's always visible:
        drawRect(x, y, w, h, fill=self.color, border=borderColor, 
                 borderWidth=self.borderWidth, align='center')
        drawLabel(self.labelText, x, y, size=self.labelSize*sizeConstant,
                  font=self.font, fill=self.labelColor, bold=self.boldText,
                  italic=self.italicText)
        # if untoggled, make it darker:
        if self.drawAsToggled and not self.toggled:
            drawRect(x, y, w, h, fill='black', border=borderColor, 
                     borderWidth=self.borderWidth, opacity=45, align='center')

    def getScaledXYWH(self, app):
        # returns the scaled bounds of the button
        sizeConstant = app.windowSize/app.baseWindowSize
        scaledX, scaledY = self.cx*sizeConstant, self.cy*sizeConstant
        scaledWidth = self.width*sizeConstant 
        scaledHeight = self.height*sizeConstant
        return scaledX, scaledY, scaledWidth, scaledHeight
    
# ########################    Knob Class    #############################
class Knob:
    # THE HARDEST FUCKING PART OF THIS PROJECT
    def __init__(self, cx, cy, radius, min, max, defaultVal, function,
                 curveFunction='linear', color='white', accentColor='black', 
                 borderWidth=1, alwaysShowVal=False, label=None, 
                 labelColor='black', percentKnob=False, hoverColor='red'):
        self.cx, self.cy, self.radius = cx, cy, radius
        self.min, self.max = min, max
        self.defaultVal = defaultVal
        self.percentTransform, self.inversePercentTransform = (
            self.createCurveFunction(curveFunction))
        self.resetPosition() # set val and valPercent to their defaults
        self.function = function
        self.label=label
        self.color = color
        self.accentColor = accentColor
        self.labelColor = labelColor
        self.hoverColor = hoverColor
        self.hovered = False
        self.borderWidth = borderWidth
        self.alwaysShowVal=alwaysShowVal
        self.fontSize = radius * 0.65 if radius < 22 else 11
        self.percentKnob = percentKnob # does self.val represent a percent?
        self.mouseHold = False         # is this knob being modified?
        self.lastY = None              # by how much? (Y - lastY)
        self.recentClick = False       # was the button recently clicked?
        self.timer = 0          # how long ago? resets recentClick over 200ms
        self.sensitivity = 8    # multiplier for deltaY in knob drag
    
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
                # get the percent**2, add 1 (no log(0)), divide by 2*2
                # i.e. (1000**3/(10**3)**3) = 1, therefore
                # log10(1000**3)/4 = 1 and any % < 1 will scale by log10.
                # by cubing valPercent, the bottom of the range is less dense
                # (tested higher powers but the difference is negligible)
                percentLog = (math.log10(self.valPercent**3 + 1))/9
                return range * percentLog + self.min
            def inversePercentTransform():
                # value in, % out
                # normalize to min = 0
                range = self.max - self.min
                adjustedVal = self.val - self.min
                # get the percentage scaled by percentLog:
                scaledPercent = adjustedVal/range
                # undo the logarithmic scaling(percentLog in reverse):
                return (10**(9 * scaledPercent) - 1)**(1/3)
        elif type == 'exponential':
            def percentTransform():
                # % in, value out
                range = self.max - self.min
                # higher power = steeper curve, 3 is arbitrary
                scaledPercent = self.valPercent**3/1000**3
                return range * scaledPercent + self.min
            def inversePercentTransform():
                # value in, % out
                range = self.max - self.min
                adjustedVal = self.val - self.min
                # get the percentage scaled by the above:
                scaledPercent = adjustedVal/range
                # do the inverse of the above scaling:
                return (scaledPercent*1000**3)**(1/3)
        else:
            # we are all dumbasses who mispell things, so crash and tell me why
            raise Exception("ArgError: curveFunction must be 'linear'" +
                            " or 'logarithmic' or 'exponential'")
        return percentTransform, inversePercentTransform
    
    def getPointOnEdge(self, x, y, r):
        # Get the desired angle in radians of a particular value first
        angleRads = math.pi*5/4 - (math.pi*3/2) * self.valPercent/1000
        # then, return x, y minus the coords of that on the unit circle times r
        return (x + math.cos(angleRads)*r, y - math.sin(angleRads)*r)
    
    def draw(self, app):
        x, y, r = self.getScaledXYRad(app)
        sizeConstant = app.windowSize/app.baseWindowSize
        if self.hovered or self.mouseHold:
            borderColor = self.hoverColor
        else:
            borderColor = self.accentColor
        # draw the circle:
        drawCircle(x, y, r, fill=self.color, border=borderColor,
                   borderWidth=self.borderWidth)
        # get the point along the circle corresponding to knob position:
        x1, y1 = self.getPointOnEdge(x, y, r) # pass these in to not compute x2
        # draw a line between center and that point:
        drawLine(x, y, x1, y1, fill=borderColor)
        if self.mouseHold or self.alwaysShowVal:
            # When changing the parameter or on alwaysShowVal, display its value
            scaledW = r*1.7 # arbitrary/aesthetic
            scaledH = r*0.9 # arbitrary/aesthetic
            distanceY = r*1.5 # arbitrary/aesthetic
            drawRect(x, y - distanceY, scaledW, scaledH, fill=self.color, 
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
            # r*0.5 is also arbitrary
            drawLabel(displayVal, x, y - distanceY, size=r*0.5, font='arial',
                      fill=self.labelColor)
        if self.label != None:
            drawLabel(self.label, x, y + r*1.30, 
                      size=self.fontSize*sizeConstant, fill=self.labelColor)

    def mouseInKnob(self, mX, mY, app):
        # check if distance between knob center and mX, mY < radius
        x, y, r = self.getScaledXYRad(app)
        return ((x - mX)**2 + (y - mY)**2)**0.5 < r

    def checkIfPressed(self, mX, mY, app):
        if self.mouseInKnob(mX, mY, app):
            self.mouseHold = True
            self.lastY = mY
            if self.recentClick: # check for double click and reset
                self.resetPosition()
                self.function(app, self.val)
            self.recentClick = True # gets set to false by self.stepTimer

    def checkBounds(self):
        # Make sure the value stays within the min, max bounds
        if self.valPercent > 1000:
            self.valPercent = 1000
        elif self.valPercent < 0:
            self.valPercent = 0
    
    def mouseDrag(self, mY, app):
        # All the changes to the params based on knob position happen here
        if self.mouseHold:
            # change the percent, so log/exponential scaling works
            self.valPercent -= (mY - self.lastY)*self.sensitivity
            self.checkBounds()  # limits % to 0 < % < 1000
            self.lastY = mY     # reset distance measurement
            self.val = self.percentTransform() # change val by the curve
            self.function(app, self.val)    # change whatever this knob changes
    
    def mouseMove(self, mX, mY, app):
        # just a boring hover effect
        if self.mouseInKnob(mX, mY, app):
            self.hovered = True
        else:
            self.hovered = False
    
    def mouseRelease(self):
        self.mouseHold = False
        self.hovered = False

    
    def stepTimer(self, app):
        # count for 200ms after being clicked for double click check
        if self.recentClick:
            # add time
            self.timer += 1
            if self.timer > app.stepsPerSecond/5:
                # reset timer
                self.timer = 0
                self.recentClick = False
    
    def toggleLowSens(self):
        # if it's one, make it the other
        if self.sensitivity == 8:
            self.sensitivity = 1
        else:
            self.sensitivity = 8

    def getScaledXYRad(self, app):
        # similar to button class. returns scaled x, y, and radius
        sizeConstant = app.windowSize/app.baseWindowSize
        scaledX, scaledY = self.cx*sizeConstant, self.cy*sizeConstant
        scaledRad = self.radius*sizeConstant
        return scaledX, scaledY, scaledRad