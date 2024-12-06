from cmu_graphics import *
import requests, os, random
from PIL import Image
from pokemon import Pokemon

class Button: 
    def __init__(self, rectLeft, rectTop, rectWidth, rectHeight, text='+', theme='teamAdd', pokemon='None', num=None): 
        self.rectLeft = rectLeft
        self.rectTop = rectTop
        self.rectWidth = rectWidth
        self.rectHeight = rectHeight
        self.text = text
        self.theme = theme
        self.pokemon = pokemon
        self.num=num

    def getPokemon(self): 
        return self.pokemon
    
    def clickIn(self, mouseX, mouseY): 
        # Check if mouse outside X bounds
        if (mouseX > self.rectLeft + self.rectWidth or mouseX < self.rectLeft): 
            return False
        # Check if mouse outside Y bounds
        if (mouseY > self.rectTop + self.rectHeight or mouseY < self.rectTop): 
            return False
        return True
    
    def drawButton(self, selected=False): 
        if (self.theme == 'teamAdd'): 
            drawRect(self.rectLeft, self.rectTop, self.rectWidth, self.rectHeight, 
                 fill=rgb(255, 203, 5), border=rgb(60, 90, 166), borderWidth=5)
        
            drawLabel(self.text, self.rectLeft + self.rectWidth // 2, 
                    self.rectTop + self.rectHeight // 2, 
                    fill=rgb(250, 2, 2), bold=True, size=self.rectHeight//2)
        elif (self.theme == 'pokeAdded'): 
            if selected: 
                borderColor = rgb(240, 36, 36)
                textSize = self.rectHeight//3.5
            else: 
                borderColor = rgb(60, 90, 166)
                textSize = self.rectHeight//4
            
            drawRect(self.rectLeft, self.rectTop, self.rectWidth, self.rectHeight, 
                fill=rgb(255, 203, 5), border=borderColor, borderWidth=5)

            self.pokemon.drawSprite(self.rectLeft + self.rectWidth // 8, self.rectTop, 
                                    self.rectWidth // 4, self.rectWidth // 4)

            drawLabel(self.pokemon.name, self.rectLeft + self.rectWidth // 2, 
                    self.rectTop + self.rectHeight // 2, 
                    fill=rgb(250, 2, 2), bold=True, size=textSize)
        elif (self.theme == 'moves'): 
            drawRect(self.rectLeft, self.rectTop, self.rectWidth, self.rectHeight, 
                 fill=rgb(255, 203, 5), border=rgb(60, 90, 166), borderWidth=5)

            moveText = self.text.replace(',', ' ')
            drawLabel(moveText, self.rectLeft + self.rectWidth // 2, 
                      self.rectTop + self.rectHeight // 2,
                      fill=rgb(250, 2, 2), bold=True, size=self.rectHeight//2)
        elif (self.theme == 'moveTxtBox'): 
            drawRect(self.rectLeft, self.rectTop, self.rectWidth, self.rectHeight, 
                 fill=rgb(255, 203, 5), border=rgb(60, 90, 166), borderWidth=5)
            drawLabel(str(self.num), self.rectLeft + 30, self.rectTop + 15, 
                 fill=rgb(250, 2, 2), bold=True, size=self.rectHeight//3)
            drawLabel(self.text.replace('-', ' ').capitalize(), self.rectLeft + self.rectWidth // 2, 
                    self.rectTop + self.rectHeight // 2, 
                    fill=rgb(250, 2, 2), bold=True, size=self.rectHeight//2)
    
    def addPokemon(self, pokemon): 
        self.theme = 'pokeAdded'
        self.pokemon = pokemon
        self.text = self.pokemon.name

    def resetDimensions(self, rectLeft, rectTop, rectWidth, rectHeight): 
        self.rectLeft = rectLeft
        self.rectTop = rectTop
        self.rectWidth = rectWidth
        self.rectHeight = rectHeight

    @staticmethod
    def distance(x1, y1, x2, y2): 
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    
class TextInput: 
    def __init__(self, rectLeft, rectTop, rectWidth, rectHeight): 
        self.rectLeft = rectLeft
        self.rectTop = rectTop
        self.rectWidth = rectWidth
        self.rectHeight = rectHeight
        self.active = False
        self.text = ''
        self.button = Button(rectLeft + rectWidth, rectTop, 
                             rectWidth // 3, rectHeight, text='Choose')

    def drawBar(self): 
        if not self.active: 
            border='black'
            color='white'
        else: 
            border=rgb(60, 90, 166)
            color=rgb(255, 203, 5)
        drawRect(self.rectLeft, self.rectTop, self.rectWidth, self.rectHeight, 
                fill=color, border=border, borderWidth=3)
        drawLabel(self.text, self.rectLeft + 5, self.rectTop + self.rectHeight // 2, 
                  size=self.rectHeight - 10, fill='black', align='left')
        self.button.drawButton()
    
    def clickIn(self, mouseX, mouseY): 
        # Check if mouse outside X bounds
        if (mouseX > self.rectLeft + self.rectWidth or mouseX < self.rectLeft): 
            self.active = False
        # Check if mouse outside Y bounds
        elif (mouseY > self.rectTop + self.rectHeight or mouseY < self.rectTop): 
            self.active = False
        else: 
            self.active = True

    def typeChar(self, key): 
        if self.active: 
            if key == 'backspace': 
                self.text = self.text[:-1]
            elif key.isalnum() and len(key) == 1: 
                self.text += str(key)
            elif key == ',': 
                self.text += key
            elif key == '-': 
                self.text += key
            elif key == 'space': 
                self.text += ' '
        
    def getButton(self): 
        return self.button
        
class ScrollableBox: 
    def __init__(self, rectLeft, rectTop, rectWidth, rectHeight, list): 
        self.rectLeft = rectLeft
        self.rectTop = rectTop
        self.rectWidth = rectWidth
        self.rectHeight = rectHeight
        self.active = False
        self.list = list
        self.dy = 0
        self.numLines = 6 if len(self.list) >= 6 else len(self.list)

    def updateList(self, list): 
        self.list = list
        self.dy = 0
        self.numLines = 6 if len(self.list) >= 6 else len(self.list)

    def clickIn(self, mouseX, mouseY): 
        # Check if mouse outside X bounds
        if (mouseX > self.rectLeft + self.rectWidth or mouseX < self.rectLeft): 
            self.active = False
        # Check if mouse outside Y bounds
        elif (mouseY > self.rectTop + self.rectHeight or mouseY < self.rectTop): 
            self.active = False
        else: 
            self.active = True

    def checkScroll(self, key): 
        if self.active and len(self.list) != 1: 
            if key == 'up' and self.dy > 0: 
                self.dy -= 1
            elif key == 'down' and self.dy < (len(self.list) - self.numLines): 
                self.dy += 1
    
    def drawBox(self): 
        if not self.active: 
            border='black'
            color='white'
        else: 
            border=rgb(60, 90, 166)
            color=rgb(255, 203, 5)
        drawRect(self.rectLeft, self.rectTop, self.rectWidth, self.rectHeight, 
                fill=color, border=border, borderWidth=3)
        if self.numLines > 1: 
            for lineIndex in range(self.dy, self.dy + self.numLines): 
                drawLabel(self.list[lineIndex].capitalize(), self.rectLeft + 5, 
                          self.rectTop + 20 + (lineIndex - self.dy) * ((self.rectHeight) // 6), 
                          size=self.rectHeight//10, fill='black', align='left')
        else: 
            drawLabel(self.list[0].capitalize(), self.rectLeft + 5, self.rectTop + 20 + (0 - self.dy) * (self.rectHeight // self.numLines), 
                        size=self.rectHeight//10, fill='black', align='left')