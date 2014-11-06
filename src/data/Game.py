__author__ = 'Matt'
import pickle

class Game:
    def __init__(self):
        #manages game state
        self.GameFile
        self.StartMap
        self.PlayerProgress


    def loadGame(self):

        gamefile = open(r'filelocation','w')
        gamedata = pickle.Unpickler(gamefile).load()
        return gamedata

    def saveGame(self, gamedata):
        #if new game, create a save file
        pickle.Pickler(gamedata)

        #if old game, overwrite save file or create a new timestamp

    def getMap(self):
        #


