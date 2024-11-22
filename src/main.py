from cmu_graphics import *
import requests
import random
import pickle
# Gen 1 is all pokemon with id <= 151

class Pokemon: 

    # Imports a file of a set of all gen one pokemon names
    genOnePokemon = None
    with open('genOnePokemonNameList', 'rb') as file:
        genOnePokemon = pickle.load(file)

    # Imports a file of a dictionary of natures and their stat effects (increase index, decrease index)
    natureEffectsDictionary = None
    with open('natureEffectList', 'rb') as file:
        natureEffectsDictionary = pickle.load(file)
    
    ''' 
    Creates a basic instance of Pokemon Class
    @param name - name of the pokemon (str)
    @param species - species name of pokemon (str)
    @param team - battle side of the pokemon ('me' for my side, 'opp' for enemy)
    battleURL is image of pokemon in battle, iconURL is icon of pokemon in menus
    

    ToDo: add get/set battle stats, health, and status conditions, start working on UI, get Types 
        and start figuring out how to access moves/ability effects
    '''
    def __init__(self, name, species, team): 
        self.name = name
        
        self.statusCondition = None
        # Stat change stages that affect the Pokemon instance in battle
        # max is +6, min is -6
        self.statChanges = [0, 0, 0, 0, 0, 0]

        # Stats that all pokemon start the battle with (accuracy, evasion)
        # only affected by move accuracy and stat changes
        self.battleAccuracyStats = [0, 0]
        
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
        
        # Set the default nature
        self.nature = None
        self.natureBattleEffects = None
        self.setNature('serious')

        # Get in-battle stats based on equation
        self.battleStats = None
        self.calculateInitialBattleStats()
        self.currHealth = self.battleStats[0]

        self.movesList = []
        # List of possible moves for this pokemon (gen 1 only)
        for moveIndex in self.infoDictionary['moves']: 
            firstMoveGen = moveIndex['version_group_details'][0]['version_group']['name']
            if firstMoveGen == 'red-blue' or firstMoveGen == 'yellow': 
                self.movesList.append(moveIndex['move']['name'])
        
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
    Return a list of possible Natures for a pokemon to have
    @return - list of nature names (str)
    '''
    def getNatures(self): 
        return Pokemon.natureEffectsDictionary.keys()

    '''
    Set the nature of a pokemon and update the effects on battle stats
    @param nature - Name of the nature to set for the Pokemon instance (str)
    '''
    def setNature(self, nature): 
        self.nature = nature
        self.natureBattleEffects = [1 for _ in range(6)]
        self.natureBattleEffects[Pokemon.natureEffectsDictionary[self.nature][0]] += 0.1
        self.natureBattleEffects[Pokemon.natureEffectsDictionary[self.nature][0]] -= 0.1

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

    '''
    Find and return list of stats on Pokemon instance currently in battle
    @return - [hp, attack, defense, special-attack, special-defense, speed, 
                accuracyChanges, evasionChanges]
    '''
    def getBattleStats(self): 
        return self.battleStats + self.battleAccuracyStats

    '''
    Initial calculatation and change battle stats based only on EVs, IVs, and Nature (1.1 and 0.9)
    stats are calculated where Lvls are 50: 
        HP = ((2*Base + IV + EV//4 + 100) * Level) // 100 + 10 + Level
        Stat = (((2*Base + IV + EV//4) * Level) // 100 + 5) * Nature
    '''
    def calculateInitialBattleStats(self): 
        # Formula for HP is different from other stats
        self.battleStats[0] = ((((2*self.baseStatList[0] + self.individualValues[0] 
                                    + self.effortValues[0]//4 + 100) * 50) // 100) + 10 + 50)
        for i in range(1, 6):
            baseStat = self.baseStatList[i]
            indValue = self.individualValues[i]
            effValue = self.effortValues[i]
            natureEffect = self.natureBattleEffects[i]
            self.battleStats[i] = (((((2*baseStat + indValue + effValue//4) * 50)
                                        // 100) + 5) * natureEffect)


    '''
    When in battle, calculate any stat drops/raises based on a stat change
    @param statChange - stage of stat change [6, -6]
    @param statIndex - location of affected stat (hp cannot be affected)
                        [hp, attack, defense, special-attack, special-defense, speed, accuracy, evasion]
    '''
    def setBattleStats(self, statChange, statIndex): 
        if 5 < statIndex < 8: 
            self.battleAccuracyStats[statIndex - 6] += statChange
        elif 0 < statIndex < 6: 
            self.battleStats[statIndex] += statChange
        self.calculateCurrBattleStats()

    '''
    
    '''
    def calculateCurrBattleStats(self): 
        pass


    

def onAppStart(app): 
    pass

def redrawAll(app):
    pass

def main():
    runApp(width=2560, height=1600)

main()