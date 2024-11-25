from cmu_graphics import *
import requests
from PIL import Image
import os

def onAppStart(app): 
    # name = 'charizard'
    # app.unparsed = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}/')
    # if app.unparsed.status_code != 200:
    #     print("Error: ", app.unparsed.status_code)
    
    # app.dittoDict = app.unparsed.json()
    # app.abilityInfo = app.dittoDict['abilities'][0]['ability']['name']
    # soundUrl = app.dittoDict['cries']['legacy']
    # print(soundUrl)
    # app.sound = Sound(soundUrl)
    # app.imgUrl = app.dittoDict['sprites']['front_shiny']
    app.img = Image.open(os.path.join('images', 'pokemonBattleGround.png'))
    app.img = CMUImage(app.img)

def onKeyPress(app, key):
    # if key == 'p':
    #     app.sound.play(restart=True)
    pass

def redrawAll(app):
    # drawLabel(app.abilityInfo, app.width // 2, app.height // 2 - 100)
    # drawImage(app.imgUrl, app.width // 2, app.height // 2)
    drawImage(app.img, app.width // 2, app.height // 2)

def main():
    runApp(width=2560, height=1600)

main()