__author__ = 'Andrea'

import random
from combat.items.inventory import *
class hero:

    def __init__(self, name, level):
        self.name = name
        self.health = 100*level
        self.speed = 10
        self.mana = 50*level
        self.attack = 5*level
        self.defense = level
        self.level = level
        self.currentHealth = self.health
        self.currentMana = self.mana
        #these attributes are optional to a particular scene.
        #used to increase bonuses (attack, defense)
        self.tempBonus = 0
        self.experience = 0
        self.xpNeeded = 100*level
        self.inventory = inventory()

    def loseHealth(self, amount):
        self.currentHealth = int(self.currentHealth - amount)
        #Prevent negative hp
        if self.currentHealth < 0:
            self.currentHealth = 0

    def gainHealth(self,amount):
        self.currentHealth= self.currentHealth + amount
        #make sure it doesn't go over max health
        if self.currentHealth > self.health:
            self.health = self.currentHealth

    def heal(self):
        amount = self.level*10
        if self.currentHealth+amount<self.health:
            self.gainHealth(amount)
        else:
            self.currentHealth = self.health

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

    def attackMonster(self):
        #damage a random amount
        amplifier = random.uniform(1,1.8)
        result = int(self.attack*amplifier)
        return result

    def defend(self, attack):
        #uses defense value to calculate damage done.
        defending = self.defense
        block = (defending*5)/(100)
        ##never go above a %50 block value
        if block > .5:
            block = .5
        defending = float((block)*attack)
        #lose health
        self.loseHealth(attack-defending)
        #return the amount defended.
        return defending

    def increaseAttackBonus(self, amount):
        #increases attack for a temporary amount of time
        self.tempBonus = amount

    def removeBonus(self):
        self.tempBonus = 0

    def increaseDefBonus(self, amount):
        self.tempBonus = amount

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

    def levelUp(self):
        self.level+=1
        self.health = 100+25*self.level
        self.speed+=int(self.level*0.8)
        self.mana = 50*self.level
        self.attack = 5*self.level
        self.defense +=int(self.level*1.8)
        self.currentHealth = self.health
        self.currentMana = self.mana
        if self.level>=10:
            self.xpNeeded = int(100*self.level*0.2)
        else:
            self.xpNeeded = int(100*self.level)

    def gainExperience(self, xp):
        self.experience+=xp
        if self.experience>=self.xpNeeded:
            self.experience = self.experience-self.xpNeeded
            self.levelUp()
            print('level up, you are now: '+str(self.level))

    def sellItem(self, item):
        ""
    def buyItem(self, item):
        ""
    def closeInventory(self):
        ""
        #save inventory