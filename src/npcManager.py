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
        npc1 = npc("town1", 7, 7, "down", "sprites/emoSpriteSheet.png")
        npc1.setText("Geez, like, get out of my way!")
        npc1.setText("Can't you see I'm brooding over here?")
        npcList.append(npc1)
        npc1 = npc("town1", 9, 9, "left", "sprites/emoSpriteSheet.png")
        npcList.append(npc1)
        npc1 = npc("town1", 13, 8, "right", "sprites/emoSpriteSheet.png")
        npcList.append(npc1)
        npc1 = npc("town1", 14, 6, "up", "sprites/emoSpriteSheet.png")
        npcList.append(npc1)
        npc1 = npc("town1", 10, 9, "left", "sprites/emoSpriteSheet.png")
        npcList.append(npc1)
        
def getNPCList():
    global npcList
    return npcList
