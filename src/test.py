# ChatGPT helped me make these datasets
# ChatGPT taught me how to webscrape lololol
# All the Move Info is webscraped from https://pokemondb.net/move/all

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

    import requests
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin

    # URL of the page to scrape
    url = "https://pokemondb.net/move/all"

    # Send a GET request to fetch the page content
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the table that contains the move data
    table = soup.find("table")  # Assuming the first table is the one you need

    # Extract the rows of the table
    rows = table.find_all("tr")

    # Extract the columns needed from each row, ommitting based on information from another column
    moveMap = { }
    for row in rows:
        # Find all cells in the row
        cells = row.find_all("td")  # `td` is for table data cells
        if cells:  # Skip header rows that don't have `td`
            # Get the string info from each column
            moveName = cells[0].get_text(strip=True).replace(' ', '-').lower()
            moveDescription = cells[6].get_text(strip=True)
            movePower = cells[3].get_text(strip=True) if cells[3].get_text(strip=True) != '—' else 0

            # Get all of the images in the row
            img_tags = row.find_all("img")
            image_urls = [urljoin(url, img.get("src")) for img in img_tags if img.get("src")]
            
            # We only care about the first image in the row, convert the info into a number
            # (0 = physical, 1 = special, 2 = status)
            moveCategory = None
            if len(image_urls) >= 1:
                if 'move-physical' in image_urls[0]: 
                    moveCategory = 0
                elif 'move-special' in image_urls[0]: 
                    moveCategory = 1
                elif 'move-status' in image_urls[0]: 
                    moveCategory = 2
            # Ignore special moves from next generations
            if not ('Z-Move' in moveDescription or 'G-Max' in moveDescription or 'Dynamax' in moveDescription):
                moveMap[moveName] = [movePower, cells[1].get_text(strip=True).lower(), moveCategory]

    with open('moveEffects', 'wb') as file:
        pickle.dump(moveMap, file)

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
