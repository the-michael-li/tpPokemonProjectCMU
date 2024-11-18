from cmu_graphics import *
import requests

def onAppStart(app): 
    app.unparsed = requests.get('https://pokeapi.co/api/v2/pokemon/barboach/')
    if app.unparsed.status_code != 200:
        print("Error: ", app.unparsed.status_code)
    
    app.dittoDict = app.unparsed.json()
    app.abilityInfo = app.dittoDict['abilities'][0]['ability']['name']
    soundUrl = app.dittoDict['cries']['legacy']
    print(soundUrl)
    app.sound = Sound(soundUrl)
    app.imgUrl = app.dittoDict['sprites']['front_shiny']

def onKeyPress(app, key):
    if key == 'p':
        app.sound.play(restart=True)

def redrawAll(app):
    drawLabel(app.abilityInfo, app.width // 2, app.height // 2 - 100)
    drawImage(app.imgUrl, app.width // 2, app.height // 2)

def main():
    runApp(width=2560, height=1600)

main()