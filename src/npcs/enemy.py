'''
Created on Oct 25, 2014

description:

Enemies inherit characteristics of the NPC class.

attributes:  Name, health, alive, mood

Methods:  Speak, move, attack
'''
from npcs import npc

class enemy(npc):
    
    def __init__(self, name, sprite, type, health, mood):
        
        #enemies can speak,
        self.Name = name
        self.species = type
        self.health = health
        self.alive = True
        self.mood = mood
        self.sprite = sprite
        #implement later
        self.loot = ""
        
        
    def speak(self, text):
        ""
        
    
        
    def attack(self):
        ""
    
    def move(self):
        ""

    #what happens on death
    def die(self):
        ""
    #when player r
    def giveGift(self):
        ""
        
    
    #generates the NPC inventory based on specific rules
    def generateInventory(self):
        ""