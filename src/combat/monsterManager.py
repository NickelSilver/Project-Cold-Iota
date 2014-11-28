__author__ = 'Andrea'
from combat.monster import *

monsterPool = []
levelMin = 1
levelCap = 0
npcMonsterPool = []

#IMPLEMENT NPCMONSTER POOL

def createMonsterPool(scene):
    global monsterPool, levelCap, levelMin, npcMonsterPool
    monsterPool = [] #empties monster pool each time
    npcMonsterPool = []

    if scene == 'map1':
        levelCap = 7
        monster1 = monster('Spidronus', 'monsters/spidermonster1.png', 1)
        monsterPool.append(monster1)
        monster1 = monster('Pickles', 'monsters/chickenmonster1.png', 1)
        monsterPool.append(monster1)
        monster1 = monster('Drule', 'monsters/batmonster1.png', 1)
        monsterPool.append(monster1)
        monster1 = monster('Ghost', 'monsters/ghostmonster1.png', 1)
        monsterPool.append(monster1)
        npcMonsterPool.append(monster1) #this adds ghost to the npc monster pool
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
def getNpcMonsterPool():
    return npcMonsterPool


