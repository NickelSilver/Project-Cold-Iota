'''
Created on 21 Oct 2014

@author: Nickel
'''

from npc import *

npcList = []

#Note: drawing quads seems to be incredibly slow. Recommend not using more than 5 NPC's per map until fixed
def createNPCList(scene): #add NPC's here. Additional features will be added later. 
    global npcList
    if scene == "town1":
        npc1 = npc("town1", 7, 7, "down", "sprites/npc1SpriteSheet1.png")
        npc1.setText("Geez, like, get out of my way!")
        npc1.setText("Can't you see I'm brooding over here?")
        npcList.append(npc1)
        npc1 = npc("town1", 9, 9, "left", "sprites/npc1SpriteSheet1.png")
        npcList.append(npc1)
        npc1 = npc("town1", 13, 8, "right", "sprites/npc1SpriteSheet1.png")
        npcList.append(npc1)
        npc1 = npc("town1", 14, 6, "up", "sprites/npc1SpriteSheet1.png")
        npcList.append(npc1)
        npc1 = npc("town1", 10, 9, "left", "sprites/npc1SpriteSheet1.png")
        npcList.append(npc1)
        npc1 = npc("town1", 11, 9, "left", "sprites/npc1SpriteSheet1.png")
        npcList.append(npc1)
        npc1 = npc("town1", 12, 9, "left", "sprites/npc1SpriteSheet1.png")
        npcList.append(npc1)
        npc1 = npc("town1", 13, 9, "left", "sprites/npc1SpriteSheet1.png")
        npcList.append(npc1)
        npc1 = npc("town1", 14, 9, "left", "sprites/npc1SpriteSheet1.png")
        npcList.append(npc1)
        npc1 = npc("town1", 15, 9, "left", "sprites/npc1SpriteSheet1.png")
        npcList.append(npc1)
        npc1 = npc("town1", 16, 9, "left", "sprites/npc1SpriteSheet1.png")
        npcList.append(npc1)
        npc1 = npc("town1", 17, 9, "left", "sprites/npc1SpriteSheet1.png")
        npcList.append(npc1)
        npc1 = npc("town1", 18, 9, "left", "sprites/npc1SpriteSheet1.png")
        npcList.append(npc1)
        npc1 = npc("town1", 19, 9, "left", "sprites/npc1SpriteSheet1.png")
        npcList.append(npc1)
        npc1 = npc("town1", 20, 9, "left", "sprites/npc1SpriteSheet1.png")
        npcList.append(npc1)
        
def getNPCList():
    global npcList
    return npcList
