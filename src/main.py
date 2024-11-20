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
    stats are calculated based on IVs and EVs: IVs will always be perfect (31 in each stat)

    '''
    def __init__(self, name, species, team): 
        self.name = name
        
        self.species = species.lower()
        # Get the dictionary for the pokemon from the API
        app.unparsed = requests.get(f'https://pokeapi.co/api/v2/pokemon/{self.species}/')
        if app.unparsed.status_code != 200:
            print("Error: ", app.unparsed.status_code)
        self.infoDictionary = app.unparsed.json()
        
        # Get shiny or default sprite
        shinyOrDef = 'default' if random.random() > 0.1 else 'shiny'
        self.iconURL = self.infoDictionary['sprites']['front_' + shinyOrDef]
        self.battleURL = None
        # Getting front / back sprite depending on team
        if(team == 'me'): 
            spriteKey = 'back_' + shinyOrDef
            self.battleURL = self.infoDictionary['sprites'][spriteKey]
        else: 
            self.battleURL = self.iconURL
        
        self.ability = None
        # Fix this (three abilities sometimes)
        if len(self.infoDictionary['abilities']) > 1: 
            self.ability = ability
        

        self.statList = statList # List of stats used for calculations in battle
        # [hp, attack, defense, special-attack, special-defense, speed]
        self.effortValues = [0, 0, 0, 0, 0, 0] # Boosts to each stat (maxes: 510 total, 252 per stat)
        # effortValue // 4 is the number of stat points added to each base stat

        self.movesList = movesList # List of possible moves for this pokemon
        self.usedMoves = [None, None, None, None] 
        # List of used moves for this pokemon (max of 4)
        self.heldItem = ''
        

    def __repr__(self): 
        return self.name
    
    def __eq__(self, other): 
        return isinstance(other, Pokemon) and self.species == other.species


def onAppStart(app): 
    pass

def redrawAll(app):
    pass

def main():
    runApp(width=2560, height=1600)

main()