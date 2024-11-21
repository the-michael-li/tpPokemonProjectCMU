from cmu_graphics import *
import requests
import random
# Gen 1 is all pokemon with id <= 151

class Pokemon: 
    ''' 
    Creates a basic instance of Pokemon Class
    @param name - name of the pokemon (str)
    @param species - species name of pokemon (str)
    @param team - battle side of the pokemon ('me' for my side, 'opp' for enemy)
    battleURL is image of pokemon in battle, iconURL is icon of pokemon in menus
    stats are calculated based on IVs and EVs and Nature (1.1 and 0.9) and Lvls are 50: 
        HP = ((2*Base + IV + EV/4 + 100) * Level) / 100 + 10
        Stat = (((2*Base + IV + EV/4) * Level) / 100 + 5) * Nature

    '''
    def __init__(self, name, species, team): 
        self.name = name
        
        self.statusCondition = None
        # Stat changes that affect the Pokemon instance in battle
        # max is +6, min is -6
        self.statChanges = [0, 0, 0, 0, 0, 0]

        # Stats that all pokemon start the battle with (accuracy, evasion)
        # only affected by move accuracy and stat changes
        self.battleStartStats = [0, 0]
        
        self.species = species.lower()
        # Get the dictionary for the pokemon from the API
        app.unparsed = requests.get(f'https://pokeapi.co/api/v2/pokemon/{self.species}/')
        if app.unparsed.status_code != 200:
            print("Error: ", app.unparsed.status_code)
        self.infoDictionary = app.unparsed.json()

        # Get shiny or default sprite as menu icon
        shinyOrDef = 'default' if random.random() > 0.1 else 'shiny'
        self.iconURL = self.infoDictionary['sprites']['front_' + shinyOrDef]
        self.battleURL = None

        # Getting front / back sprite depending on team in battle
        if(team == 'me'): 
            spriteKey = 'back_' + shinyOrDef
            self.battleURL = self.infoDictionary['sprites'][spriteKey]
        else: 
            self.battleURL = self.iconURL
        
        # Get the current ability name for Pokemon instance
        self.ability = self.infoDictionary['abilities'][0]['ability']['name']

        # Get a list of possible abilities for Pokemon instance
        self.abilityList = []
        for abilityDict in self.infoDictionary['abilities']: 
            self.abilityList.append(abilityDict['ability']['name'])

        # List of base stats of Pokemon species
        # [hp, attack, defense, special-attack, special-defense, speed]
        self.baseStatList = [stat['base_stat'] for stat in self.infoDictionary['stats']] 

        # Boosts to each stat (max: 31 per stat)
        self.individualValues = [31, 31, 31, 31, 31, 31] 
        # Boosts to each stat (maxes: 510 total, 252 per stat)
        self.effortValues = [0, 0, 0, 0, 0, 0]

        # Get in-battle stats based on equation from __init__ description
        self.battleStats = self.getBattleStats()

        self.movesList = []
        # List of possible moves for this pokemon (gen 1 only)
        for moveIndex in self.infoDictionary['moves']: 
            firstMoveGen = moveIndex['version_group_details'][0]['version_group']['name']
            if firstMoveGen == 'red-blue' or firstMoveGen == 'yellow': 
                self.movesList.append(moveIndex['moves']['name'])
        
        # List of useable moves for this pokemon (max of 4)
        self.movesToUse = [None, None, None, None]
        
        self.heldItem = ''

    def __repr__(self): 
        return self.name
    
    def __eq__(self, other): 
        return isinstance(other, Pokemon) and self.species == other.species
    
    '''
    Find and return list of names of abilities available to Pokemon instance
    @return - list of ability names available to Pokemon to choose from
    '''
    def getAbilites(self): 
        return self.abilityList
    
    '''
    Set self.ability for the Pokemon instance if it is allowable
    @param abilityName - Name of ability to set self.ability to
    @return - True if set properly, False if ability is not allowed on Pokemon
    '''
    def setAbility(self, abilityName): 
        if abilityName in self.abilityList: 
            self.ability = abilityName
            return True
        else: 
            return False
        
    '''
    Find and return list of names of moves available to Pokemon instance
    @return - list of move names available to Pokemon to choose from
    '''
    def getMoves(self): 
        return self.movesList
    
    '''
    Add move to self.movesToUse for the Pokemon instance if it is allowable
    @param moveName - Name of move to add to self.movesToUse
    @param index - Where to place move in self.movesToUse
    @return - True if set properly, False if move is not allowed on Pokemon
    '''
    def addMove(self, moveName, index): 
        if index < 4 and moveName in self.movesList: 
            self.movesToUse[index] = moveName
            return True
        else: 
            return False



def onAppStart(app): 
    pass

def redrawAll(app):
    pass

def main():
    runApp(width=2560, height=1600)

main()