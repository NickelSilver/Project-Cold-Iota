__author__ = 'Matt'
import pickle

class Game:
    def __init__(self):
        #manages game state
        self.GameFile
        self.StartMap
        self.PlayerProgress


    def loadGame(self):

        gamefile = open(r'C:\Users\Matt\Computer Science\Python\SWScience\Project-Cold-Iota\src\data\Game1.txt','w')
        gamedata = pickle.Unpickler(gamefile).load()
        return gamedata

    def saveGame(self, gamedata):
        #if new game, create a save file
        pickle.Pickler(gamedata)

        #if old game, overwrite save file or create a new timestamp

    def getMap(self):
        #


