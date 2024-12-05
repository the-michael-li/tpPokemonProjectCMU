# Pokemon data from Pokeapi.co
# Battle background image from https://www.pinterest.com/ideas/pokemon-battle-background/934038905355/
# Pokemon formulas from https://bulbagarden.net/home/
# ChatGPT taught me how to webscrape lololol
# All the Move Info is webscraped from https://pokemondb.net/move/all

from cmu_graphics import *
import requests, pickle, os, pathlib
import random, copy, time
from PIL import Image
from pokemon import Pokemon
from uiElements import Button, TextInput
'''
gameEnd Bug (Doesn't exist, just cant switch)
Move custom
add search popups
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
    app.currPlayPokeIndex = 0
    app.currOppPokeIndex = 0
    app.activePokemon = None
    app.activeOppPokemon = None
    app.win, app.lose = False, False
    setActiveScreen('start')
    app.enemyTeam = []
    numEnemyPokemon = 2
    for i in range(numEnemyPokemon): 
        randomPokemon = random.choice(list(Pokemon.genOnePokemon))
        newEnemyPokemon = Pokemon(None, randomPokemon, 'opp')
        app.enemyTeam.append(newEnemyPokemon)
        if len(app.enemyTeam[i].getMoves()) >= 4: 
            for j in range(1, 4): 
                randomMoveIndex = random.randint(0, len(app.enemyTeam[i].getMoves()) - 1)
                app.enemyTeam[i].addMove(app.enemyTeam[i].getMoves()[randomMoveIndex], j)
        randomMoveIndex = random.randint(0, len(app.enemyTeam[i].getMoves()) - 1)
        app.enemyTeam[i].addMove(app.enemyTeam[i].getMoves()[randomMoveIndex], 0)
        time.sleep(0.0000002)
    app.pokemonTeam = [None, None, None, None, None, None]
    app.teamBuildButtons = []
    app.stepTimeBro = 0
    pokemonRectWidth = 5 * app.width // 16
    pokemonRectHeight = app.height // 8
    for pokemonSlot in range(len(app.pokemonTeam)): 
        rectLeft = app.width // 8 + (pokemonSlot % 2) * (pokemonRectWidth + app.width // 8)
        rectTop = app.height // 4 + (pokemonSlot // 2) * (pokemonRectHeight + app.height // 8)
        newButton = Button(rectLeft, rectTop, pokemonRectWidth, pokemonRectHeight)
        app.teamBuildButtons += [newButton]
    app.doDamageAfterSwitch = False
    

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
    if app.pokemonTeam[0] != None and app.teamBuildToBattleButton.clickIn(mouseX, mouseY):
        app.currPlayPokeIndex = 0
        app.currOppPokeIndex = 0
        app.activePokemon = app.pokemonTeam[app.currPlayPokeIndex]
        app.activeOppPokemon = app.enemyTeam[app.currOppPokeIndex]
        setActiveScreen('battle')
    for buttonIndex in range(len(app.teamBuildButtons)): 
        if app.teamBuildButtons[buttonIndex].clickIn(mouseX, mouseY): 
            app.selectedIndex = buttonIndex
            setActiveScreen('pokeBuild')
            return

    
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

    nameTxtBoxLeft = app.width//32
    nameTxtBoxTop = 2*app.height//7
    app.pokeBuildNameTxtBox = TextInput(nameTxtBoxLeft, nameTxtBoxTop, uInputWidth, uInputHeight)

    ############################################################
    # Moves
    ############################################################
    app.pokeBuildMoves = [None, None, None, None]
    for pokemonSlot in range(4): 
        rectLeft = app.width//32 + (pokemonSlot % 2) * (uInputWidth + app.width // 32)
        rectTop = 13*app.height//32 + (pokemonSlot // 2) * (uInputHeight + app.height//32)
        app.pokeBuildMoves[pokemonSlot] = Button(rectLeft, rectTop, uInputWidth, uInputHeight, text='None', 
                                                 theme='moveTxtBox', num=pokemonSlot)
    moveTxtBoxLeft = app.width//32
    moveTxtBoxTop = 4*app.height//7
    app.pokeBuildMoveTxtBox = TextInput(moveTxtBoxLeft, moveTxtBoxTop, uInputWidth, uInputHeight)
    

def pokeBuild_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill=rgb(250, 101, 101))
    #####################################################
    # for i in range(1, 15): 
    #     drawLine(0, i*app.height//14, app.width, i*app.height//14)
    #####################################################
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
    # Pokemon Name UI Bar
    ############################################################
    drawLabel('Choose a Name', app.width//32,app.height//4, bold=True, align='left', 
              size=25, fill=rgb(255, 203, 5), border=rgb(60, 90, 166), borderWidth=1)
    app.pokeBuildNameTxtBox.drawBar()

    ############################################################
    # Pokemon Moves
    ############################################################
    drawLabel('Moves', app.width//32,3*app.height//8, bold=True, align='left', 
              size=25, fill=rgb(255, 203, 5), border=rgb(60, 90, 166), borderWidth=1)
    for box in app.pokeBuildMoves: 
        box.drawButton()
    drawLabel('Choose a move (input as: moveName,moveNum)', app.width//32,15*app.height//28, bold=True, align='left', 
              size=20, fill=rgb(255, 203, 5), border=rgb(60, 90, 166), borderWidth=1)
    app.pokeBuildMoveTxtBox.drawBar()
    

    ############################################################
    # Pokemon Species Icon
    ############################################################
    drawRect(27 * app.width//32, app.height//6, app.width // 12, app.width // 12, 
             fill=rgb(255, 203, 5), border=rgb(60, 90, 166), borderWidth=3)
    drawLabel(app.teamBuildButtons[app.selectedIndex].pokemon.name, 27 * app.width//32,2 * app.height//16, bold=True, align='left', 
              size=40, fill=rgb(255, 203, 5), border=rgb(60, 90, 166), borderWidth=1)
    app.teamBuildButtons[app.selectedIndex].pokemon.drawSprite(27 * app.width//32, app.height//6, 
                                                               app.width // 12, app.width // 12)

def pokeBuild_onMousePress(app, mouseX, mouseY): 
    if app.pokeBuildToTeamBuildButton.clickIn(mouseX, mouseY): 
        setActiveScreen('teamBuild')
    
    app.pokeBuildSpeciesTxtBox.clickIn(mouseX, mouseY)
    if app.pokeBuildSpeciesTxtBox.getButton().clickIn(mouseX, mouseY): 
        pokemonSpecies = app.pokeBuildSpeciesTxtBox.text.lower()
        app.pokeBuildSpeciesTxtBox.text = ''
        if pokemonSpecies in Pokemon.genOnePokemon: 
            newPokemon = Pokemon(None, pokemonSpecies, 'me')
            app.pokemonTeam[app.selectedIndex] = newPokemon
            app.teamBuildButtons[app.selectedIndex].addPokemon(newPokemon)
    
    app.pokeBuildNameTxtBox.clickIn(mouseX, mouseY)
    if app.pokeBuildNameTxtBox.getButton().clickIn(mouseX, mouseY): 
        pokemonName = app.pokeBuildNameTxtBox.text.lower()
        app.pokeBuildNameTxtBox.text = ''
        app.pokemonTeam[app.selectedIndex].name = pokemonName

    app.pokeBuildMoveTxtBox.clickIn(mouseX, mouseY)
    if app.pokeBuildMoveTxtBox.getButton().clickIn(mouseX, mouseY): 
        pokemonMoveTLocation = app.pokeBuildMoveTxtBox.text.lower()
        app.pokeBuildMoveTxtBox.text = ''
        pokemonMove = pokemonMoveTLocation[:pokemonMoveTLocation.find(',')]
        pokemonMoveLocation = -1
        if pokemonMoveTLocation.find(',') + 1 < len(pokemonMoveTLocation) and pokemonMoveTLocation[pokemonMoveTLocation.find(',') + 1:].isdigit(): 
            pokemonMoveLocation = int(pokemonMoveTLocation[pokemonMoveTLocation.find(',') + 1:])
        if 0 <= pokemonMoveLocation < 4 and pokemonMove in app.pokemonTeam[app.selectedIndex].getMoves(): 
            app.pokemonTeam[app.selectedIndex].addMove(pokemonMove, pokemonMoveLocation)
            app.pokeBuildMoves[pokemonMoveLocation].text = pokemonMove
        

def pokeBuild_onKeyPress(app, key): 
    app.pokeBuildSpeciesTxtBox.typeChar(key)
    app.pokeBuildNameTxtBox.typeChar(key)
    app.pokeBuildMoveTxtBox.typeChar(key)
    
############################################################
# Battle Screen
############################################################
def battle_onScreenActivate(app): 
    # Given one move right now: 
    randomMoveIndex = random.randint(0, len(app.pokemonTeam[0].getMoves()) - 1)
    app.pokemonTeam[0].addMove(app.pokemonTeam[0].getMoves()[randomMoveIndex], 0)

    makeMoveButtons(app)
    moveRectWidth, moveRectHeight = app.width // 9, app.height // 18
    rectLeft = app.width - (app.width//8 + moveRectWidth // 2)
    rectTop = app.height - (app.height//18)
    app.switchButton = Button(rectLeft, rectTop, moveRectWidth, moveRectHeight, 
                              text='Switch', theme='moves')
    app.activeMove = None
    app.activeOppMove = None
    if app.doDamageAfterSwitch: 
        randomMoveIndex = random.randint(0, 3)
        randomMoveName = app.enemyTeam[app.currOppPokeIndex].movesToUse[randomMoveIndex]
        oppMoveInfo = Pokemon.moveEffectsDictionary[randomMoveName]
        allyHpDamage = Pokemon.getHealthDamage(app.enemyTeam[app.currOppPokeIndex], app.pokemonTeam[app.currPlayPokeIndex], oppMoveInfo)
        app.pokemonTeam[app.currPlayPokeIndex].setHealth(-allyHpDamage)
        if checkEndGame(app, 'opp') == True: 
            return
        app.activeMove = 'switch'
        app.activeOppMove = randomMoveName
    app.doDamageAfterSwitch = False

def makeMoveButtons(app): 
    app.battleMovesButtons = []
    moveRectWidth, moveRectHeight = app.width // 9, app.height // 18
    for moveSlot in range(4): 
        rectLeft = app.width - (app.width//8 + ((3-moveSlot) % 2) * (moveRectWidth + app.width // 64))
        rectTop = app.height - (app.height//8 + ((3-moveSlot) // 2) * (moveRectHeight + app.height // 32))
        text = (app.pokemonTeam[app.currPlayPokeIndex].movesToUse[moveSlot].capitalize() 
                if app.pokemonTeam[app.currPlayPokeIndex].movesToUse[moveSlot] != None else 'None')
        newButton = Button(rectLeft, rectTop, moveRectWidth, moveRectHeight, 
                           text=text, theme='moves')
        app.battleMovesButtons += [newButton]

def battle_redrawAll(app):
    drawImage(app.img, app.width // 2, app.height // 2, width=app.width, 
              height=app.height, align='center')
    for button in app.battleMovesButtons: 
        button.drawButton()
    app.switchButton.drawButton()
    app.pokemonTeam[app.currPlayPokeIndex].drawBattleSprite(app.width//6, 9*app.height//16, 
                                                            app.width//4, app.width//4)
    app.enemyTeam[app.currOppPokeIndex].drawBattleSprite(17*app.width//24, 4*app.height//9, 
                                                            app.width//8, app.width//8)
    playHpValue, playHpRatio, playHpColor = app.pokemonTeam[app.currPlayPokeIndex].getCurrHealthInfo()
    oppHpValue, oppHpRatio, oppHpColor = app.enemyTeam[app.currOppPokeIndex].getCurrHealthInfo()
    drawHealthBar(app, 24*app.width//32, 23*app.height//32, playHpValue, playHpRatio, playHpColor, 
                  app.pokemonTeam[app.currPlayPokeIndex].name)
    drawHealthBar(app, app.width//32, app.height//16, oppHpValue, oppHpRatio, oppHpColor, 
                  app.enemyTeam[app.currOppPokeIndex].name)
    
    if app.activeMove != None or app.activeOppMove != None:
        drawMoveLabel(app)

    if app.win or app.lose: 
        drawRect(0,0,app.width,app.height,fill=rgb(250, 101, 101), opacity=50)
        ending = 'won!!!' if app.win else 'lost :('
        drawLabel(f'You {ending}', app.width//2, app.height//2, size=app.height//5)
        drawLabel('Press r to restart', app.width//2, app.height//2 + app.height//4, size=app.height//10)

def battle_onStep(app): 
    if app.activeMove != None or app.activeOppMove != None: 
        app.stepTimeBro += 1
    if app.stepTimeBro >= 6: 
        app.activeMove = None
        app.activeOppMove = None
        app.stepTimeBro = 0

def drawHealthBar(app, rectLeft, rectTop, hpVal, hpRatio, color, text): 
    rectWidth, rectHeight = app.width//10, app.height//24
    drawRect(rectLeft, rectTop, rectWidth, rectHeight,fill='darkGray', border='black', borderWidth=2)
    if(hpRatio != 0): 
        drawRect(rectLeft, rectTop, rectWidth * hpRatio, rectHeight,fill=color)
    else: 
        drawRect(rectLeft, rectTop, 5, rectHeight,fill=color)
    drawLabel(str(hpVal), rectLeft + rectWidth//2, rectTop + rectHeight//2, size=rectHeight//2)
    drawLabel(text, rectLeft + 5, rectTop - rectHeight//4, size=rectHeight//2, align='left')

def battle_onMousePress(app, mouseX, mouseY): 
    if app.win or app.lose or app.stepTimeBro != 0: 
        return
    # Switching
    if app.switchButton.clickIn(mouseX, mouseY): 
        app.doDamageAfterSwitch = True
        setActiveScreen('userSwitch')
    checkMovesHappening(app, mouseX, mouseY)
    checkFaintToSwitch(app)

def checkFaintToSwitch(app): 
    if app.activeOppPokemon.pokemonFainted and not(app.lose or app.win): 
        app.currOppPokeIndex += 1
        app.activeOppPokemon = app.enemyTeam[app.currOppPokeIndex]
    if app.activePokemon.pokemonFainted and not(app.lose or app.win): 
        for pokemonIndex in range(len(app.pokemonTeam)): 
            if app.pokemonTeam[pokemonIndex] != None and not app.pokemonTeam[pokemonIndex].pokemonFainted:
                app.currPlayPokeIndex = pokemonIndex
                app.activePokemon = app.pokemonTeam[app.currPlayPokeIndex]
        setActiveScreen('userSwitch')
    
def checkMovesHappening(app, mouseX, mouseY): 
    for button in app.battleMovesButtons: 
        if button.clickIn(mouseX, mouseY) and button.text.lower() in Pokemon.moveEffectsDictionary and button.text != 'None': 
            moveInfo = Pokemon.moveEffectsDictionary[button.text.lower()]
            oppHpDamage = Pokemon.getHealthDamage(app.pokemonTeam[app.currPlayPokeIndex], app.enemyTeam[app.currOppPokeIndex], moveInfo)
            randomMoveIndex = random.randint(0, 3)
            randomMoveName = app.enemyTeam[app.currOppPokeIndex].movesToUse[randomMoveIndex]
            oppMoveInfo = Pokemon.moveEffectsDictionary[randomMoveName]
            allyHpDamage = Pokemon.getHealthDamage(app.enemyTeam[app.currOppPokeIndex], app.pokemonTeam[app.currPlayPokeIndex], oppMoveInfo)

            allySpeed = app.pokemonTeam[app.currPlayPokeIndex].getBattleStats()[5]
            oppSpeed = app.enemyTeam[app.currOppPokeIndex].getBattleStats()[5]
            if allySpeed >= oppSpeed: 
                app.enemyTeam[app.currOppPokeIndex].setHealth(-oppHpDamage)
                if checkEndGame(app, 'play') == True: 
                    return
                app.pokemonTeam[app.currPlayPokeIndex].setHealth(-allyHpDamage)
                if checkEndGame(app, 'opp') == True: 
                    return
            elif allySpeed < oppSpeed: 
                app.pokemonTeam[app.currPlayPokeIndex].setHealth(-allyHpDamage)
                if checkEndGame(app, 'opp') == True: 
                    return
                app.enemyTeam[app.currOppPokeIndex].setHealth(-oppHpDamage)
                if checkEndGame(app, 'play') == True: 
                    return
            app.activeMove = button.text.lower()
            app.activeOppMove = randomMoveName
            return

def drawMoveLabel(app): 
    allySpeed = app.pokemonTeam[app.currPlayPokeIndex].getBattleStats()[5]
    oppSpeed = app.enemyTeam[app.currOppPokeIndex].getBattleStats()[5]
    drawRect(0, 7*app.height//8, 3*app.width//4, app.height//8, fill='white',
              border=rgb(60, 90, 166), borderWidth=5)
    if (allySpeed > oppSpeed and app.stepTimeBro <= 3) or (allySpeed < oppSpeed and app.stepTimeBro > 3):
        text = f'{app.activePokemon.name} used {app.activeMove}!' if app.activeMove != 'switch' else 'You switched'
        drawLabel(text, 3*app.width//8, 15*app.height//16, size=app.height//18)
    else: 
        drawLabel(f'{app.activeOppPokemon.name} used {app.activeOppMove}!', 3*app.width//8, 15*app.height//16, size=app.height//18)

def checkEndGame(app, side): 
    numOppsFainted = 0
    for oppPokemon in app.enemyTeam: 
        if oppPokemon.currHealth == 0: 
            numOppsFainted += 1
    if side == 'play' and numOppsFainted == len(app.enemyTeam): 
        app.win = True
        return app.win
    numAllyFainted = 0
    for allyPokemon in app.pokemonTeam: 
        if allyPokemon == None or allyPokemon.currHealth == 0: 
            numAllyFainted += 1
    if side == 'opp' and numAllyFainted == len(app.pokemonTeam): 
        app.lose = True
        return app.lose

def battle_onKeyPress(app, key): 
    if app.win or app.lose and key == 'r': 
        restart(app)

############################################################
# userSwitch Screen
############################################################
def userSwitch_onScreenActivate(app): 
    pokemonRectWidth = 5 * app.width // 16
    pokemonRectHeight = app.height // 8
    app.userSwitchButtons = [None, None, None, None, None, None]
    for pokemonSlot in range(len(app.userSwitchButtons)): 
        rectLeft = app.width // 8 + (pokemonSlot % 2) * (pokemonRectWidth + app.width // 8)
        rectTop = app.height // 4 + (pokemonSlot // 2) * (pokemonRectHeight + app.height // 8)
        theme = 'pokeAdded' if app.pokemonTeam[pokemonSlot] != None else 'teamAdd'
        text = app.pokemonTeam[pokemonSlot].name.capitalize() if app.pokemonTeam[pokemonSlot] != None else 'None'
        app.userSwitchButtons[pokemonSlot] = Button(rectLeft, rectTop, pokemonRectWidth, pokemonRectHeight, 
                                                    theme=theme, pokemon=app.pokemonTeam[pokemonSlot], text=text)
    
    userSwitchToBattleButtonWidth = 300
    userSwitchToBattleButtonHeight = 50
    app.userSwitchToBattleButton = Button(app.width - userSwitchToBattleButtonWidth, 0,
                                      userSwitchToBattleButtonWidth, userSwitchToBattleButtonHeight, 
                                      text='Battle!')

def userSwitch_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill=rgb(250, 101, 101))
    drawLabel("Choose a 'mon to switch in!",app.width//4,app.height//8, bold=True,
              size=55, fill=rgb(255, 203, 5), border=rgb(60, 90, 166), borderWidth=3)
    for buttonIndex in range(len(app.userSwitchButtons)):
        if buttonIndex == app.currPlayPokeIndex: 
            app.userSwitchButtons[buttonIndex].drawButton(selected=True)
        else: 
            app.userSwitchButtons[buttonIndex].drawButton()
    app.userSwitchToBattleButton.drawButton()

def userSwitch_onMousePress(app, mouseX, mouseY): 
    if app.userSwitchToBattleButton.clickIn(mouseX, mouseY): 
        setActiveScreen('battle')
    for buttonIndex in range(len(app.userSwitchButtons)): 
        if (app.userSwitchButtons[buttonIndex].clickIn(mouseX, mouseY) 
            and app.pokemonTeam[buttonIndex] != None and not app.pokemonTeam[buttonIndex].pokemonFainted): 
            app.currPlayPokeIndex = buttonIndex
            app.activePokemon = app.pokemonTeam[app.currPlayPokeIndex]
            return


############################################################
# Main
############################################################
def main():
    runAppWithScreens(width=2560, height=1600, initialScreen='start')

main()