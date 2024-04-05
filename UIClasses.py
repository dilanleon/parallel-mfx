from cmu_graphics import *

# Button Class
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
        if (self.cx - self.width/2 < mX < self.cx + self.width/2 and
            self.cy - self.height/2 < mY < self.cy + self.height/2):
            self.function(app)
        
    def draw(self):
        # Should only be called in redrawAll(app)
        drawRect(self.cx, self.cy, self.width, self.height, 
                 fill=self.color, border=self.border, 
                 borderWidth=self.borderWidth, align='center')
        drawLabel(self.labelText, self.cx, self.cy, size=self.labelSize,
                  font=self.font, fill=self.labelColor, bold=True)