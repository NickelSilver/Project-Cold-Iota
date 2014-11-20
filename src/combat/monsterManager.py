__author__ = 'Andrea'
from combat.monster import *

monsterPool = []
levelMin = 1
levelCap = 0

def createMonsterPool(scene):
    global monsterPool, levelCap, levelMin
    monsterPool = [] #empties monster pool each time

    if scene == 'map1':
        levelCap = 7
        monster1 = monster('Spidronus', 'monsters/spidermonster1.png', 1)
        monsterPool.append(monster1)
        monster1 = monster('Pickles', 'monsters/chickenmonster1.png', 1)
        monsterPool.append(monster1)
        monster1 = monster('Drule', 'monsters/batmonster1.png', 1)
        monsterPool.append(monster1)
    elif scene == 'pseudocampusmap':
        levelCap = 7
        monster1 = monster('Spidronus', 'monsters/spidermonster1.png', 1)
        monsterPool.append(monster1)
        monster1 = monster('Pickles', 'monsters/chickenmonster1.png', 1)
        monsterPool.append(monster1)
        monster1 = monster('Drule', 'monsters/batmonster1.png', 1)
        monsterPool.append(monster1)
    elif scene=='fortesmap':
        levelCap = 7
        monster1 = monster('Spidronus', 'monsters/spidermonster1.png', 1)
        monsterPool.append(monster1)
        monster1 = monster('Pickles', 'monsters/chickenmonster1.png', 1)
        monsterPool.append(monster1)
        monster1 = monster('Drule', 'monsters/batmonster1.png', 1)
        monsterPool.append(monster1)

def getLevelCap():
    return levelCap
def getLevelMin():
    return levelMin
def getMonsterPool():
    return monsterPool


