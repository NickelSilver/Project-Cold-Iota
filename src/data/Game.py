__author__ = 'Matt'
import pickle
import os

#class is in charge of persisting data from one map to the next.
class Game():
    def __init__(self):
        #manages game state
        self.gamefile = ""
        self.currentmap = ""
        #Some time of calculation, probably incremental.
        self.playerprogress = ""


    def loadGame(self):

        file = open("GameFiles.txt","rb")

        gamedata = pickle.Unpickler(file).load()
        return gamedata

    def saveGame(self):
        filename = open(b'GameFiles.txt','wb')
        gamedata = []
        gamedata.append(self.gamefile)
        gamedata.append(self.currentmap)
        gamedata.append(self.playerprogress)
        #if new game, create a save file
        pickle.Pickler(filename)
        pickle.dump(gamedata, filename)
        #if old game, overwrite save file or create a new timestamp

    def setGameFile(self, gfile):
        self.gamefile = gfile

    def getGameFile(self):
        return self.gamefile

    def getMap(self):
        return self.currentmap

    def setMap(self, map):
        # for saving
        self.currentmap = map

    def getProgress(self):
        return self.playerprogress

    def setProgress(self, progress):
        self.playerprogress = progress


#class Player(self):
    #def __init__(self):
        #gather items from protag
      #  self.name
       # self.health
      # self.items
       # self.progress