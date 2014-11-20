__author__ = 'Andrea'
from combat.monster import *

monsterPool = []

def createMonsterPool(scene):
    global monsterPool

    if scene == 'map1':
        monster1 = monster('Spidronus', 'monsters/spidermonster1.png', 1)
        monsterPool.append(monster1)
        monster1 = monster('Pickles', 'monsters/chickenmonster1.png', 1)
        monsterPool.append(monster1)
        monster1 = monster('Drule', 'monsters/batmonster1.png', 1)
        monsterPool.append(monster1)



