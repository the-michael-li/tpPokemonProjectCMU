# Pokemon data from Pokeapi.co
# Battle background image from https://www.pinterest.com/ideas/pokemon-battle-background/934038905355/
# Pokemon formulas from https://bulbagarden.net/home/
# ChatGPT taught me how to webscrape lololol
# All the Move Info is webscraped from https://pokemondb.net/move/all

from cmu_graphics import *
import requests, pickle, os, pathlib
import random, copy
from PIL import Image

class Pokemon: 
    # Imports a file of a set of all gen one pokemon names
    genOnePokemon = None
    with open('genOneNames', 'rb') as file:
        genOnePokemon = pickle.load(file)
    genOneLIST = list(genOnePokemon)

    # Imports a file of a dictionary of natures mapped to their stat effects (increase index, decrease index)
    natureEffectsDictionary = None
    with open('natureEffects', 'rb') as file:
        natureEffectsDictionary = pickle.load(file)
    
    # Imports a file of a dictionary of moves mapped to their effects 
    # [base power, type, physical/special] physical = 0, special = 1, status = 2
    moveEffectsDictionary = None
    with open('moveEffects', 'rb') as file:
        moveEffectsDictionary = pickle.load(file)
    
    # Imports a file of a dictionary of type mapped to dictionaries of types
    # that map to how much damage is done (attackingType: defendingType: multiplier)
    typeChart = None
    with open('typeChart', 'rb') as file:
        typeChart = pickle.load(file)
    ''' 
    Creates a basic instance of Pokemon Class
    @param name - name of the pokemon (str)
    @param species - species name of pokemon (str)
    @param team - battle side of the pokemon ('me' for my side, 'opp' for enemy)
    battleURL is image of pokemon in battle, iconURL is icon of pokemon in menus
    
    Important instance variables: 
    name: name of the pokemon
    species: name of species of the pokemon
    statusCondition: name of the status condition
    statChanges and battleAccuracyStats:    changes in stats that 
                                            affect battleStats in battle
    infoDictionary: dictionary for the pokemon species
    iconURL: image link for menu icon of pokemon
    battleURL: image link for battle image of pokemon
    baseStatList: list of base stats
    individualValues: list of IVs for the pokemon
    effortValues: list of the EVs for the pokemon
    nature: name of the nature for the pokemon
    natureBattleEffects: list of stat multipliers based on the nature
    healthStatus: name of color of health bar based on percentage of health left
    pokemonFainted: boolean of whether the pokemon is fainted or not
    battleStats: list of the fluctuating stats in battle
    startingStats: a list of starting battleStats for reference
    movesList: list of possible move names for the pokemon
    movesToUse: list of four moves that a pokemon can use in battle
    typing: list of types of pokemon


    ToDo: start working on UI, 
        and start figuring out how to access moves effects
    '''
    def __init__(self, name, species, team): 
        self.name = name if name != None else species.capitalize()

        # Pokemon health status (options are 'green', 'yellow', and 'red')
        self.healthStatus = 'green'
        self.pokemonFainted = False
        
        # Can be sleep, burn, paralysis, freeze, poison, etc.
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

        self.typing = copy.copy(self.infoDictionary['types'])

        # Get in-battle stats based on equation
        self.battleStats = [None, None, None, None, None, None]
        self.startingStats = None
        self.calculateInitialBattleStats()
        self.currHealth = self.startingStats[0]
        self.currHealthPercentage = self.currHealth / self.startingStats[0]

        self.movesList = []
        # List of possible moves for this pokemon (gen 1 only)
        for moveIndex in self.infoDictionary['moves']: 
            firstMoveGen = moveIndex['version_group_details'][0]['version_group']['name']
            if firstMoveGen == 'red-blue' or firstMoveGen == 'yellow': 
                self.movesList.append(moveIndex['move']['name'])
        
        # List of useable moves for this pokemon (max of 4)
        self.movesToUse = [None, None, None, None]

    def __repr__(self): 
        return self.name
    
    def __eq__(self, other): 
        return isinstance(other, Pokemon) and self.species == other.species and self.name == other.name

    '''
    Find and return current hp value
    @return - hp value (int), percentage of hp (float), color of health bar (str)
    '''
    def getCurrHealthInfo(self): 
        return (self.currHealth, self.currHealthPercentage, self.healthStatus)
    
    '''
    Set currHealth based on the change in health, if fainted, sets health to 0 and pokemonFainted to True
    If needed, change the healthbar color based on % of health left
    @param healthChange - Name change in health (-ve if damage, +ve if healing)
    '''
    def setHealth(self, healthChange): 
        self.currHealth += int(healthChange)
        if(self.currHealth <= 0): 
            self.pokemonFainted = True
            self.currHealth = 0

        self.currHealthPercentage = self.currHealth / self.startingStats[0]
        if self.currHealthPercentage > 0.5: 
            self.healthStatus = 'green'
        elif self.currHealthPercentage > 0.2: 
            self.healthStatus = 'yellow'
        else: 
            self.healthStatus = 'red'
    
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
        self.nature = nature.lower()
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
            self.movesToUse[index] = moveName.lower()
            return True
        else: 
            return False

    '''
    Find and return list of ivs set for pokemon instance
    @return - list of ivs on pokemon instance
    '''
    def getIvs(self): 
        return self.individualValues
    
    '''
    Set an iv value for the pokemon instance and if over max values, set to max
    @param ivIndex - index of iv stat to change (ie. 0 = health, 1 = attack, etc.)
    @param ivValue - value of iv to set iv to
    '''
    def setIvs(self, ivIndex, ivValue): 
        if ivValue > 31: 
            ivValue = 31
        elif ivValue < 0: 
            ivValue = 0
        self.individualValues[ivIndex] = ivValue

    '''
    Find and return list of evs set for pokemon instance
    @return - list of evs on pokemon instance
    '''
    def getEvs(self): 
        return self.effortValues
    
    '''
    Set an ev value for the pokemon instance and if over max values, set to max
    @param evIndex - index of ev stat to change (ie. 0 = health, 1 = attack, etc.)
    @param evValue - value of ev to set ev to
    '''
    def setEvs(self, evIndex, evValue): 
        if evValue > 252: 
            evValue = 252
        elif evValue < 0: 
            evValue = 0
        self.effortValues[evIndex] = evValue
        overflow = 0
        if sum(self.effortValues) > 510: 
            overflow = sum(self.effortValues) - 510
            self.effortValues[evIndex] -= overflow

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
        self.startingStats = copy.copy(self.battleStats)

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
            self.statChanges[statIndex] += statChange
        
        # Make sure stat changes are limited to the 6th stage
        self.statChanges[statIndex] = min(6, self.statChanges[statIndex])
        self.battleAccuracyStats[statIndex - 6] = min(6, self.battleAccuracyStats[statIndex - 6])
        self.statChanges[statIndex] = max(-6, self.statChanges[statIndex])
        self.battleAccuracyStats[statIndex - 6] = max(-6, self.battleAccuracyStats[statIndex - 6])

        self.calculateCurrBattleStats()

    '''
    Calculate current battleStats based on stat changes and statusCondition
    '''
    def calculateCurrBattleStats(self): 
        for statIndex in range(1, len(self.battleStats)): 
            if self.statChanges[statIndex] > 0: 
                self.battleStats[statIndex] = (self.startingStats[statIndex] * (1 + 0.5 * (self.statChanges[statIndex])))
            else: 
                self.battleStats[statIndex] = (self.startingStats[statIndex] // (1 + abs(0.5 * (self.statChanges[statIndex]))))
        # Template for if I want to implement status conditions
        if self.statusCondition != None: 
            pass
    
    def drawSprite(self, xPos, yPos, width, height): 
        drawImage(self.iconURL, xPos, yPos, width=width, height=height)
    
    def drawBattleSprite(self, xPos, yPos, width, height): 
        drawImage(self.battleURL, xPos, yPos, width=width, height=height)

    '''
    Get the amount of damage a move will do in hp based 
    on the two pokemon in battle and move used
    @param attackingPokemon - the pokemon using the attack
    @param defendingPokemon - the pokemon defending against the attack
    @param moveInfo - list of information about the move [movePower, type, physical/special=0/1]
    @return - health damage dealt to opponent
    '''
    @staticmethod
    def getHealthDamage(attackingPokemon, defendingPokemon, moveInfo): 
        level = 50
        critical = 2 if random.random() < (1/16) else 1
        damage = ((2 * level * critical) / 5 + 2) * int(moveInfo[0])
        # if special attack
        if moveInfo[2] == 1: 
            damage *= (attackingPokemon.getBattleStats()[3] / defendingPokemon.getBattleStats()[4])
        elif moveInfo[2] == 0: 
            damage *= (attackingPokemon.getBattleStats()[1] / defendingPokemon.getBattleStats()[2])
        damage = (damage / 50) + 2 if damage != 0 else 0
        
        stab = 1
        for type in attackingPokemon.typing: 
            if type == moveInfo[1]: 
                stab = 1.5
        damage *= stab
        if moveInfo[1] in Pokemon.typeChart: 
            typesToConsider = Pokemon.typeChart[moveInfo[1]].keys()
            # supereffective or not very effective
            for type in defendingPokemon.typing: 
                if type in list(typesToConsider): 
                    damage *= Pokemon.typeChart[moveInfo[1]][type]
        
        rng = random.randrange(217, 256)
        damage = (damage * rng) // 255
        return damage