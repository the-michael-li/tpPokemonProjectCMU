# Pokemon data from Pokeapi.co
# Battle background image from https://www.pinterest.com/ideas/pokemon-battle-background/934038905355/

from cmu_graphics import *
import requests, pickle, os, pathlib
import random, copy
from PIL import Image
from pokemon import Pokemon
'''
Make generic moves
'''
    
def loadSound(relativePath):
    # Convert to absolute path (because pathlib.Path only takes absolute paths)
    absolutePath = os.path.abspath(relativePath)
    # Get local file URL
    url = pathlib.Path(absolutePath).as_uri()
    # Load Sound file from local URL
    return Sound(url)

def onAppStart(app):
    app.img = Image.open(os.path.join('images', 'pokemonBattleGround.png'))
    app.img = CMUImage(app.img)
    restart(app)

def restart(app): 
    setActiveScreen('start')
    app.pokemonTeam = [None, None, None, None, None, None]

############################################################
# Start Screen
############################################################
def start_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill=rgb(250, 101, 101))
    pokemonList = ['P', 'o', 'K', 'é', 'B', 'o', 'u', 't', 's', 'V', 'G', 'C', '!']
    for characterIndex in range(len(pokemonList)): 
        drawLabel(pokemonList[characterIndex], app.width // 2 - (300-50 * characterIndex), 
                  app.height // 2 - 300 + abs(42-7 * characterIndex), fill=rgb(255, 203, 5),
                   border=rgb(60, 90, 166), borderWidth=5, size=90, bold=True, 
                   rotateAngle=-16 + (characterIndex) ** 1.4, align='bottom')
    drawLabel('Tap anywhere to start', app.width // 2, app.height - 300, size=20, bold=True)

def start_onMousePress(app, mouseX, mouseY): 
    setActiveScreen('teamBuild')

############################################################
# Team Build Screen
############################################################
def teamBuild_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill=rgb(250, 101, 101))
    pokemonRectWidth = app.width // 3
    pokemonRectHeight = app.height // 8
    for pokemonSlot in range(len(app.pokemonTeam)): 
        drawRect(app.width // 8 + (pokemonSlot % 2) * (pokemonRectWidth + app.width // 8),
                 app.height // 8 + (pokemonSlot) * pokemonRectHeight,
                 pokemonRectWidth, pokemonRectHeight, fill=rgb(250, 51, 51))
    
############################################################
# Pokemon Build Screen
############################################################
def pokeBuild_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill=rgb(250, 101, 101))
    
    
############################################################
# Battle Screen
############################################################
def battle_redrawAll(app):
    drawImage(app.img, app.width // 2, app.height // 2, width=app.width, 
              height=app.height, align='center')

############################################################
# Main
############################################################
def main():
    runAppWithScreens(width=2560, height=1600, initialScreen='start')

main()