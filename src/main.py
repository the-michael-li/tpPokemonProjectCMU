# Pokemon data from Pokeapi.co
# Battle background image from https://www.pinterest.com/ideas/pokemon-battle-background/934038905355/

from cmu_graphics import *
import requests, pickle, os, pathlib
import random, copy, time
from PIL import Image
from pokemon import Pokemon
from uiElements import Button, TextInput
'''
Make generic moves
cmu_graphics won't work?
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
    app.width, app.height = 2560, 1600
    setActiveScreen('start')
    app.enemyTeam = []
    numEnemyPokemon = 1
    for _ in range(numEnemyPokemon): 
        randomPokemon = random.choice(list(Pokemon.genOnePokemon))
        newEnemyPokemon = Pokemon(randomPokemon, randomPokemon, 'opp')
        newEnemyPokemon.addMove(newEnemyPokemon.getMoves()[-1], 0)
        app.enemyTeam.append(newEnemyPokemon)
        time.sleep(0.000002)
    app.pokemonTeam = [None, None, None, None, None, None]
    app.teamBuildButtons = []

    pokemonRectWidth = 5 * app.width // 16
    pokemonRectHeight = app.height // 8
    for pokemonSlot in range(len(app.pokemonTeam)): 
        rectLeft = app.width // 8 + (pokemonSlot % 2) * (pokemonRectWidth + app.width // 8)
        rectTop = app.height // 4 + (pokemonSlot // 2) * (pokemonRectHeight + app.height // 8)
        newButton = Button(rectLeft, rectTop, pokemonRectWidth, pokemonRectHeight)
        app.teamBuildButtons += [newButton]
    

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
def teamBuild_onScreenActivate(app): 
    app.selectedIndex = None
    pokemonRectWidth = 5 * app.width // 16
    pokemonRectHeight = app.height // 8
    for pokemonSlot in range(len(app.teamBuildButtons)): 
        rectLeft = app.width // 8 + (pokemonSlot % 2) * (pokemonRectWidth + app.width // 8)
        rectTop = app.height // 4 + (pokemonSlot // 2) * (pokemonRectHeight + app.height // 8)
        app.teamBuildButtons[pokemonSlot].resetDimensions(rectLeft, rectTop, pokemonRectWidth, pokemonRectHeight)
    
    pokeBuildToTeamBuildButtonWidth = 300
    pokeBuildToTeamBuildButtonHeight = 50
    app.teamBuildToBattleButton = Button(app.width - pokeBuildToTeamBuildButtonWidth, 0,
                                      pokeBuildToTeamBuildButtonWidth, pokeBuildToTeamBuildButtonHeight, 
                                      text='Battle!')

def teamBuild_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill=rgb(250, 101, 101))
    drawLabel('Make a team!',app.width//4,app.height//8, bold=True,
              size=85, fill=rgb(255, 203, 5), border=rgb(60, 90, 166), borderWidth=3)
    for button in app.teamBuildButtons:
        button.drawButton()
    app.teamBuildToBattleButton.drawButton()

def teamBuild_onMousePress(app, mouseX, mouseY): 
    for buttonIndex in range(len(app.teamBuildButtons)): 
        if app.teamBuildButtons[buttonIndex].clickIn(mouseX, mouseY): 
            app.selectedIndex = buttonIndex
            setActiveScreen('pokeBuild')
    if app.pokemonTeam[0] != None and app.teamBuildToBattleButton.clickIn(mouseX, mouseY): 
        setActiveScreen('battle')

    
############################################################
# Pokemon Build Screen
############################################################
def pokeBuild_onScreenActivate(app):
    newPokemon = Pokemon(None, 'ditto', 'me')
    app.pokemonTeam[app.selectedIndex] = newPokemon
    app.teamBuildButtons[app.selectedIndex].addPokemon(newPokemon)

    pokeBuildToTeamBuildButtonWidth = 300
    pokeBuildToTeamBuildButtonHeight = 50
    app.pokeBuildToTeamBuildButton = Button(app.width - pokeBuildToTeamBuildButtonWidth, 0,
                                      pokeBuildToTeamBuildButtonWidth, pokeBuildToTeamBuildButtonHeight, 
                                      text='Team Builder')

    uInputWidth = app.width // 8
    uInputHeight = app.height // 30
    
    speciesTxtBoxLeft = app.width//32
    speciesTxtBoxTop = app.height//7
    app.pokeBuildSpeciesTxtBox = TextInput(speciesTxtBoxLeft, speciesTxtBoxTop, uInputWidth, uInputHeight)

def pokeBuild_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill=rgb(250, 101, 101))
    drawLabel(f'Pokémon No. {app.selectedIndex + 1}',app.width//6,app.height//16, bold=True,
              size=70, fill=rgb(255, 203, 5), border=rgb(60, 90, 166), borderWidth=3)
    app.pokeBuildToTeamBuildButton.drawButton()

    ############################################################
    # Pokemon Species UI Bar
    ############################################################
    drawLabel('Choose Your Pokemon', app.width//32,2 * app.height//16, bold=True, align='left', 
              size=25, fill=rgb(255, 203, 5), border=rgb(60, 90, 166), borderWidth=1)
    app.pokeBuildSpeciesTxtBox.drawBar()

    ############################################################
    # Pokemon Species Icon
    ############################################################
    drawRect(29 * app.width//32, app.height//6, app.width // 12, app.width // 12, 
             fill=rgb(255, 203, 5), border=rgb(60, 90, 166), borderWidth=3)
    drawLabel(app.teamBuildButtons[app.selectedIndex].text, 29 * app.width//32,2 * app.height//16, bold=True, align='left', 
              size=40, fill=rgb(255, 203, 5), border=rgb(60, 90, 166), borderWidth=1)
    app.teamBuildButtons[app.selectedIndex].pokemon.drawSprite(29 * app.width//32, app.height//6, 
                                                               app.width // 12, app.width // 12)

def pokeBuild_onMousePress(app, mouseX, mouseY): 
    app.pokeBuildSpeciesTxtBox.clickIn(mouseX, mouseY)
    if app.pokeBuildSpeciesTxtBox.getButton().clickIn(mouseX, mouseY): 
        pokemonSpecies = app.pokeBuildSpeciesTxtBox.text.lower()
        app.pokeBuildSpeciesTxtBox.text = ''
        if pokemonSpecies in Pokemon.genOnePokemon: 
            newPokemon = Pokemon(None, pokemonSpecies, 'me')
            app.pokemonTeam[app.selectedIndex] = newPokemon
            app.teamBuildButtons[app.selectedIndex].addPokemon(newPokemon)
    if app.pokeBuildToTeamBuildButton.clickIn(mouseX, mouseY): 
        setActiveScreen('teamBuild')

def pokeBuild_onKeyPress(app, key): 
    app.pokeBuildSpeciesTxtBox.typeChar(key)
    
############################################################
# Battle Screen
############################################################
def battle_onScreenActivate(app): 
    # Given one move right now: 
    app.pokemonTeam[0].addMove(app.pokemonTeam[0].getMoves()[-1], 0)

    app.battleMovesButtons = []
    moveRectWidth = app.width // 10
    moveRectHeight = app.height // 18
    for moveSlot in range(4): 
        rectLeft = app.width - (app.width//8 + ((3-moveSlot) % 2) * (moveRectWidth + app.width // 64))
        rectTop = app.height - (app.height//8 + ((3-moveSlot) // 2) * (moveRectHeight + app.height // 32))
        text = (app.pokemonTeam[0].movesToUse[moveSlot].capitalize() 
                if app.pokemonTeam[0].movesToUse[moveSlot] != None else 'None')
        newButton = Button(rectLeft, rectTop, moveRectWidth, moveRectHeight, 
                           text=text)
        app.battleMovesButtons += [newButton]


def battle_redrawAll(app):
    drawImage(app.img, app.width // 2, app.height // 2, width=app.width, 
              height=app.height, align='center')
    for button in app.battleMovesButtons: 
        button.drawButton()
    
def battle_onMousePress(app, mouseX, mouseY): 
    pass

def battle_onKeyPress(app, key): 
    pass

############################################################
# Main
############################################################
def main():
    runAppWithScreens(initialScreen='start')

main()