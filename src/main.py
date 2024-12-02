# Pokemon data from Pokeapi.co
# Battle background image from https://www.pinterest.com/ideas/pokemon-battle-background/934038905355/
# Pokemon formulas from https://bulbagarden.net/home/

from cmu_graphics import *
import requests, pickle, os, pathlib
import random, copy, time
from PIL import Image
from pokemon import Pokemon
from uiElements import Button, TextInput
'''
Make generic moves
cmu_graphics screen changes sizes
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
    app.win, app.lose = False, False
    setActiveScreen('start')
    app.enemyTeam = []
    numEnemyPokemon = 1
    for i in range(numEnemyPokemon): 
        randomPokemon = random.choice(list(Pokemon.genOnePokemon))
        newEnemyPokemon = Pokemon(randomPokemon.capitalize(), randomPokemon, 'opp')
        app.enemyTeam.append(newEnemyPokemon)
        if len(app.enemyTeam[i].getMoves()) >= 4: 
            for j in range(1, 4): 
                randomMoveIndex = random.randint(0, len(app.enemyTeam[i].getMoves()) - 1)
                app.enemyTeam[0].addMove(app.enemyTeam[0].getMoves()[randomMoveIndex], j)
        randomMoveIndex = random.randint(0, len(app.enemyTeam[i].getMoves()) - 1)
        app.enemyTeam[0].addMove(app.enemyTeam[0].getMoves()[randomMoveIndex], 0)
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
    newPokemon = Pokemon('no_name', 'ditto', 'me')
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
    drawRect(27 * app.width//32, app.height//6, app.width // 12, app.width // 12, 
             fill=rgb(255, 203, 5), border=rgb(60, 90, 166), borderWidth=3)
    drawLabel(app.teamBuildButtons[app.selectedIndex].text, 27 * app.width//32,2 * app.height//16, bold=True, align='left', 
              size=40, fill=rgb(255, 203, 5), border=rgb(60, 90, 166), borderWidth=1)
    app.teamBuildButtons[app.selectedIndex].pokemon.drawSprite(27 * app.width//32, app.height//6, 
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
    randomMoveIndex = random.randint(0, len(app.pokemonTeam[0].getMoves()) - 1)
    # app.pokemonTeam[0].addMove(app.pokemonTeam[0].getMoves()[randomMoveIndex], 0)
    app.pokemonTeam[0].addMove(app.pokemonTeam[0].getMoves()[1], 0)
    app.currPlayPokeIndex = 0
    app.currOppPokeIndex = 0
    makeMoveButtons(app)

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
    if app.win or app.lose: 
        drawRect(0,0,app.width,app.height,fill=rgb(250, 101, 101), opacity=50)
        ending = 'won!!!' if app.win else 'lost :('
        drawLabel(f'You {ending}', app.width//2, app.height//2, size=app.height//5)
        drawLabel('Press r to restart', app.width//2, app.height//2 + app.height//4, size=app.height//10)

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
    if app.win or app.lose: 
        return
    # Need to do this but for enemy as well
    for button in app.battleMovesButtons: 
        if button.clickIn(mouseX, mouseY) and button.text.lower() in Pokemon.moveEffectsDictionary and button.text != 'None': 
            moveInfo = Pokemon.moveEffectsDictionary[button.text.lower()]
            oppHpDamage = getHealthDamage(app.pokemonTeam[app.currPlayPokeIndex], app.enemyTeam[app.currOppPokeIndex], moveInfo)
            randomMoveIndex = random.randint(0, 3)
            oppMoveInfo = [0, 'normal', 0]
            if app.enemyTeam[app.currOppPokeIndex].movesToUse[randomMoveIndex] in Pokemon.moveEffectsDictionary: 
                oppMoveInfo = Pokemon.moveEffectsDictionary[app.enemyTeam[app.currOppPokeIndex].movesToUse[randomMoveIndex]]
            allyHpDamage = getHealthDamage(app.enemyTeam[app.currOppPokeIndex], app.pokemonTeam[app.currPlayPokeIndex], oppMoveInfo)

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
            break

    
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

'''
Get the amount of damage a move will do in hp based 
on the two pokemon in battle and move used
@param attackingPokemon - the pokemon using the attack
@param defendingPokemon - the pokemon defending against the attack
@param moveInfo - list of information about the move [movePower, type, physical/special=0/1]
@return - health damage dealt to opponent
'''
def getHealthDamage(attackingPokemon, defendingPokemon, moveInfo): 
    level = 50
    critical = 2 if random.random() < (1/16) else 1
    damage = ((2 * level * critical) / 5 + 2) * moveInfo[0]
    # if special attack
    if bool(moveInfo[2]): 
        damage *= (attackingPokemon.getBattleStats()[3] / defendingPokemon.getBattleStats()[4])
    else: 
        damage *= (attackingPokemon.getBattleStats()[1] / defendingPokemon.getBattleStats()[2])
    damage = (damage / 50) + 2
    
    stab = 1
    for type in attackingPokemon.typing: 
        if type == moveInfo[1]: 
            stab = 1.5
    damage *= stab
    typesToConsider = Pokemon.typeChart[moveInfo[1]].keys()
    # supereffective or not very effective
    for type in defendingPokemon.typing: 
        if type in list(typesToConsider): 
            damage *= Pokemon.typeChart[moveInfo[1]][type]
    
    rng = random.randrange(217, 256)
    damage = (damage * rng) // 255
    return damage

def battle_onKeyPress(app, key): 
    if app.win or app.lose and key == 'r': 
        restart(app)


############################################################
# Main
############################################################
def main():
    runAppWithScreens(width=2560, height=1600, initialScreen='start')

main()