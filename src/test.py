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

    gen1_moves = {
        "absorb": [20, "grass", 1],
        "acid": [40, "poison", 0],
        "acid-armor": [0, "poison", 0],
        "agility": [0, "psychic", 1],
        "amnesia": [0, "psychic", 1],
        "aurora-beam": [65, "ice", 1],
        "bide": [0, "normal", 0],
        "bind": [15, "normal", 0],
        "blizzard": [120, "ice", 1],
        "body-slam": [85, "normal", 0],
        "bone-club": [65, "ground", 0],
        "bonemerang": [50, "ground", 0],
        "bubble": [20, "water", 1],
        "bubble-beam": [65, "water", 1],
        "clamp": [35, "water", 1],
        "comet-punch": [18, "normal", 0],
        "confusion": [50, "psychic", 1],
        "counter": [0, "fighting", 0],
        "crabhammer": [90, "water", 1],
        "cut": [50, "normal", 0],
        "defense-curl": [0, "normal", 0],
        "dig": [100, "ground", 0],
        "disable": [0, "normal", 0],
        "dizzy-punch": [70, "normal", 0],
        "double-kick": [30, "fighting", 0],
        "double-team": [0, "normal", 0],
        "double-edge": [120, "normal", 0],
        "dragon-rage": [0, "dragon", 1],
        "dream-eater": [100, "psychic", 1],
        "drill-peck": [80, "flying", 0],
        "earthquake": [100, "ground", 0],
        "ember": [40, "fire", 1],
        "explosion": [250, "normal", 0],
        "fire-blast": [120, "fire", 1],
        "fire-punch": [75, "fire", 1],
        "flamethrower": [95, "fire", 1],
        "fly": [90, "flying", 0],
        "focus-energy": [0, "normal", 0],
        "fury-attack": [15, "normal", 0],
        "fury-swipes": [18, "normal", 0],
        "glare": [0, "normal", 0],
        "growl": [0, "normal", 0],
        "growth": [0, "normal", 0],
        "guillotine": [0, "normal", 0],
        "gust": [40, "normal", 0],
        "harden": [0, "normal", 0],
        "haze": [0, "ice", 1],
        "headbutt": [70, "normal", 0],
        "high-jump-kick": [85, "fighting", 0],
        "horn-attack": [65, "normal", 0],
        "horn-drill": [0, "normal", 0],
        "hydro-pump": [120, "water", 1],
        "hyper-beam": [150, "normal", 0],
        "hyper-fang": [80, "normal", 0],
        "ice-beam": [95, "ice", 1],
        "ice-punch": [75, "ice", 1],
        "jump-kick": [70, "fighting", 0],
        "karate-chop": [50, "normal", 0],
        "leech-life": [20, "bug", 0],
        "lick": [20, "ghost", 0],
        "light-screen": [0, "psychic", 1],
        "low-kick": [0, "fighting", 0],
        "metronome": [0, "normal", 0],
        "mimic": [0, "normal", 0],
        "night-shade": [0, "ghost", 0],
        "pay-day": [40, "normal", 0],
        "peck": [35, "flying", 0],
        "pin-missile": [25, "bug", 0],
        "poison-sting": [15, "poison", 0],
        "psybeam": [65, "psychic", 1],
        "psychic": [90, "psychic", 1],
        "quick-attack": [40, "normal", 0],
        "razor-leaf": [55, "grass", 1],
        "rest": [0, "psychic", 1],
        "rock-slide": [75, "rock", 0],
        "rock-throw": [50, "rock", 0],
        "rolling-kick": [60, "fighting", 0],
        "seismic-toss": [0, "fighting", 0],
        "sing": [0, "normal", 0],
        "sky-attack": [140, "flying", 0],
        "slash": [70, "normal", 0],
        "sludge": [65, "poison", 0],
        "smokescreen": [0, "normal", 0],
        "solar-beam": [120, "grass", 1],
        "splash": [0, "normal", 0],
        "stomp": [65, "normal", 0],
        "strength": [80, "normal", 0],
        "struggle": [50, "normal", 0],
        "submission": [80, "fighting", 0],
        "substitute": [0, "normal", 0],
        "surf": [95, "water", 1],
        "swift": [60, "normal", 0],
        "tackle": [35, "normal", 0],
        "take-down": [90, "normal", 0],
        "teleport": [0, "psychic", 1],
        "thrash": [90, "normal", 0],
        "thunder": [120, "electric", 1],
        "thunder-shock": [40, "electric", 1],
        "thunderbolt": [95, "electric", 1],
        "toxic": [0, "poison", 0],
        "transform": [0, "normal", 0],
        "tri-attack": [80, "normal", 0],
        "vine-whip": [35, "grass", 1],
        "water-gun": [40, "water", 1],
        "waterfall": [80, "water", 1],
        "wrap": [15, "normal", 0],
    }

    with open('moveEffects', 'wb') as file:
        pickle.dump(gen1_moves, file)

    with open('moveEffects', 'rb') as file: 
        print(pickle.load(file))

    type_chart = {
        "normal": {
            "rock": 0.5,
            "ghost": 0.0
        },
        "fire": {
            "fire": 0.5,
            "water": 0.5,
            "grass": 2.0,
            "ice": 2.0,
            "bug": 2.0,
            "rock": 0.5,
            "dragon": 0.5
        },
        "water": {
            "fire": 2.0,
            "water": 0.5,
            "grass": 0.5,
            "ground": 2.0,
            "rock": 2.0,
            "dragon": 0.5
        },
        "electric": {
            "water": 2.0,
            "grass": 0.5,
            "electric": 0.5,
            "ground": 0.0,
            "flying": 2.0,
            "dragon": 0.5
        },
        "grass": {
            "fire": 0.5,
            "water": 2.0,
            "grass": 0.5,
            "poison": 0.5,
            "ground": 2.0,
            "flying": 0.5,
            "bug": 0.5,
            "rock": 2.0,
            "dragon": 0.5
        },
        "ice": {
            "fire": 0.5,
            "water": 0.5,
            "grass": 2.0,
            "ice": 0.5,
            "ground": 2.0,
            "flying": 2.0,
            "dragon": 2.0
        },
        "fighting": {
            "normal": 2.0,
            "ice": 2.0,
            "poison": 0.5,
            "flying": 0.5,
            "psychic": 0.5,
            "bug": 0.5,
            "rock": 2.0,
            "ghost": 0.0
        },
        "poison": {
            "grass": 2.0,
            "poison": 0.5,
            "ground": 0.5,
            "bug": 2.0,
            "rock": 0.5,
            "ghost": 0.5
        },
        "ground": {
            "fire": 2.0,
            "grass": 0.5,
            "electric": 2.0,
            "poison": 2.0,
            "flying": 0.0,
            "bug": 0.5,
            "rock": 2.0
        },
        "flying": {
            "electric": 0.5,
            "grass": 2.0,
            "fighting": 2.0,
            "bug": 2.0,
            "rock": 0.5
        },
        "psychic": {
            "fighting": 2.0,
            "poison": 2.0,
            "psychic": 0.5
        },
        "bug": {
            "fire": 0.5,
            "grass": 2.0,
            "fighting": 0.5,
            "poison": 2.0,
            "flying": 0.5,
            "psychic": 2.0,
            "ghost": 0.5
        },
        "rock": {
            "fire": 2.0,
            "ice": 2.0,
            "fighting": 0.5,
            "ground": 0.5,
            "flying": 2.0,
            "bug": 2.0
        },
        "ghost": {
            "normal": 0.0,
            "psychic": 2.0,
            "ghost": 2.0
        },
        "dragon": {
            "dragon": 2.0
        }
    }

    with open('typeChart', 'wb') as file:
        pickle.dump(type_chart, file)

    with open('typeChart', 'rb') as file: 
        print(pickle.load(file))

main()