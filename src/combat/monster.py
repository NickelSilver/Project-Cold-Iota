__author__ = 'Matt'

import random
import math

class monster:

    def __init__(self, name, sprite, level):
        self.name = name
        self.sprite = sprite
        self.health = 100*level
        self.speed = 10
        self.mana = 50*level
        self.attack = 5*level
        self.defense = level
        self.level = level
        self.currentHealth = health
        self.currentMana = mana

    def loseHealth(self, amount):
        self.currentHealth = self.currentHealth - amount
        #Prevent negative hp
        if self.currentHealth < 0:
            self.currentHealth = 0

    def gainHealth(self,amount):
        self.currentHealth= self.currentHealth + amount
        #make sure it doesn't go over max health
        if self.currentHealth > self.health
            self.health = self.currentHealth

    def loseMana(self, mana):
        self.currentMana = self.currentMana - mana
        if self.currentMana < 0:
            self.currentMana = 0

    def gainMana(self, mana):
        self.currentMana = self.currentMana + mana
        if self.mana > self.mana:
            self.currentMana = self.mana

    def attack(self):
        #damage a random amount
        amplifier = random.randrange(.8,1.2,.1)
        result = self.attack*amplifier
        return result


    def defend(self, attack):
        #uses defense value to calculate damage done.
        defense = self.defense
        block = (defense*5)/(100)
        ##never go above a %50 block value
        if block > .5:
            block = .5
        defense = float((block)*attack)
        #return the amount defended.
        return defense


#testing
car = monster("Raptor","Raptorsprite", 3)
print("attacked for:  ",car.attack)
print(car.defend(15))
print("Resulting damage done:  ",car.attack - car.defend(15))