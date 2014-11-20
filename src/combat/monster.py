__author__ = 'Matt'

#methods in this
import random
import math
import decimal

class monster:

    #default values for a monster.  Monster will scale based on level chosen.
    def __init__(self, name, sprite, level):
        self.name = name
        self.sprite = sprite
        self.health = 100*level
        self.speed = 10
        self.mana = 50*level
        self.attack = 5*level
        self.defense = level
        self.level = level
        self.currentHealth = self.health
        self.currentMana = self.mana
        self.loot = ""
        #HOW MUCH the monster is worth
        self.experience = 100*level
        #these attributes are optional to a particular scene.
        #used to increase bonuses (attack, defense)
        self.tempBonus = 0

    def loseHealth(self, amount):
        self.currentHealth = self.currentHealth - amount
        #Prevent negative hp
        if self.currentHealth < 0:
            self.currentHealth = 0

    def gainHealth(self,amount):
        self.currentHealth= self.currentHealth + amount
        #make sure it doesn't go over max health
        if self.currentHealth > self.health:
            self.health = self.currentHealth

    def getCurrentHealth(self):
        return self.currentHealth

    def loseMana(self, mana):
        self.currentMana = self.currentMana - mana
        if self.currentMana < 0:
            self.currentMana = 0

    def gainMana(self, mana):
        self.currentMana = self.currentMana + mana
        if self.mana > self.mana:
            self.currentMana = self.mana

    def getCurrentMana(self):
        return self.currentMana

    def attackHero(self):
        #damage a random amount
        amplifier = random.uniform(.8,1.2)
        result = int(self.attack*amplifier)
        return result

    def defend(self, attack):
        #uses defense value to calculate damage done.
        defense = self.defense
        block = (defense*5)/(100)
        ##never go above a %50 block value
        if block > .5:
            block = .5
        defense = float((block)*attack)
        #lose health
        self.loseHealth(attack-defense)
        #return the amount defended.
        return defense

    def increaseAttackBonus(self, amount):
        #increases attack for a temporary amount of time
        self.tempBonus = amount

    def removeBonus(self):
        self.tempBonus = 0

    def increaseDefBonus(self, amount):
        self.tempBonus = amount

    #when monster is defeated

    def isDead(self):
        if self.currentHealth == 0:
            #die
            return True
        else:
            return False

    def hasMana(self, spellMana):
        if spellMana > self.currentMana:
            return False
        else:
            return True

    def getExperience(self):
        return self.experience

    def dropLoot(self):
        return self.loot

    def speak(self, text):
        sentence = self.name,":  ", text
        return sentence

#testing
#car = monster("Raptor","Raptorsprite", 3)
#print("attacked for:  ",car.attack)
#print(car.defend(15))
#print("Resulting damage done:  ",car.attack - car.defend(15))

