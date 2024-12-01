import pickle

def main(): 
    pokemon = {'bulbasaur', 'ivysaur', 'venusaur', 'charmander', 'charmeleon', 'charizard', 'squirtle', 'wartortle', 'blastoise', 'caterpie', 'metapod', 'butterfree', 'weedle', 'kakuna', 'beedrill', 'pidgey', 'pidgeotto', 'pidgeot', 'rattata', 'raticate', 'spearow', 'fearow', 'ekans', 'arbok', 'pikachu', 'raichu', 'sandshrew', 'sandslash', 'nidoran', 'nidorina', 'nidoqueen', 'nidorino', 'nidoking', 'clefairy', 'clefable', 'vulpix', 'ninetales', 'jigglypuff', 'wigglytuff', 'zubat', 'golbat', 'oddish', 'gloom', 'vileplume', 'paras', 'parasect', 'venonat', 'venomoth', 'diglett', 'dugtrio', 'meowth', 'persian', 'psyduck', 'golduck', 'mankey', 'primeape', 'growlithe', 'arcanine', 'poliwag', 'poliwhirl', 'poliwrath', 'abra', 'kadabra', 'alakazam', 'machop', 'machoke', 'machamp', 'bellsprout', 'weepinbell', 'victreebel', 'tentacool', 'tentacruel', 'geodude', 'graveler', 'golem', 'ponyta', 'rapidash', 'slowpoke', 'slowbro', 'magnemite', 'magneton', 'farfetch’d', 'doduo', 'dodrio', 'seel', 'dewgong', 'grimer', 'muk', 'shellder', 'cloyster', 'gastly', 'haunter', 'gengar', 'onix', 'drowzee', 'hypno', 'krabby', 'kingler', 'voltorb', 'electrode', 'exeggcute', 'exeggutor', 'cubone', 'marowak', 'hitmonlee', 'hitmonchan', 'lickitung', 'koffing', 'weezing', 'rhyhorn', 'rhydon', 'chansey', 'tangela', 'kangaskhan', 'horsea', 'seadra', 'goldeen', 'seaking', 'staryu', 'starmie', 'mr. mime', 'scyther', 'jynx', 'electabuzz', 'magmar', 'pinsir', 'tauros', 'magikarp', 'gyarados', 'lapras', 'ditto', 'eevee', 'vaporeon', 'jolteon', 'flareon', 'porygon', 'omanyte', 'omastar', 'kabuto', 'kabutops', 'aerodactyl', 'snorlax', 'articuno', 'zapdos', 'moltres', 'dratini', 'dragonair', 'dragonite', 'mewtwo', 'mew'}

    with open('genOneNames', 'wb') as file:
        pickle.dump(pokemon, file)
    
    with open('genOneNames', 'rb') as file: 
        print(pickle.load(file))

    natureEffectDict = {
        'adamant': (1, 3),
        'bashful': (3, 3),
        'bold': (2, 1),
        'brave': (1, 5),
        'calm': (4, 1),
        'careful': (4, 3),
        'docile': (2, 2),
        'gentle': (4, 2),
        'hardy': (1, 1),
        'hasty': (5, 2),
        'impish': (2, 3),
        'jolly': (5, 3),
        'lax': (2, 4),
        'lonely': (1, 2),
        'mild': (3, 2),
        'modest': (3, 1),
        'naive': (5, 4),
        'naughty': (1, 4),
        'quiet': (3, 5),
        'quirky': (4, 4),
        'rash': (3, 4),
        'relaxed': (2, 5),
        'sassy': (4, 5),
        'serious': (5, 5),
        'timid': (5, 1)
    }

    with open('natureEffects', 'wb') as file:
        pickle.dump(natureEffectDict, file)

    with open('natureEffects', 'rb') as file: 
        print(pickle.load(file))

main()