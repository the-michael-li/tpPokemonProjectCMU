from cmu_graphics import *
import requests, os
from PIL import Image

class Button: 
    def __init__(self, rectLeft, rectTop, rectWidth, rectHeight, theme='teamAdd'): 
        self.rectLeft = rectLeft
        self.rectTop = rectTop
        self.rectWidth = rectWidth
        self.rectHeight = rectHeight
        self.theme = theme
        self.pokemon = None

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
    
    def drawButton(self): 
        if (self.theme == 'teamAdd'): 
            drawRect(self.rectLeft, self.rectTop, self.rectWidth, self.rectHeight, 
                 fill=rgb(255, 203, 5), border=rgb(60, 90, 166), borderWidth=5)
        
            drawLabel('+', self.rectLeft + self.rectWidth // 2, 
                    self.rectTop + self.rectHeight // 2, 
                    fill=rgb(250, 2, 2), bold=True, size=45)
        elif (self.theme == 'pokeAdded'): 
            pass
    
    def addPokemon(self, pokemon): 
        self.theme = 'pokeAdded'
        self.pokemon = pokemon

    @staticmethod
    def distance(x1, y1, x2, y2): 
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5