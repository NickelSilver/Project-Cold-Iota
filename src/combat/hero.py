__author__ = 'Andrea'

import random

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
        self.gainHealth(amount)

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
        amplifier = random.uniform(1.8,2.8)
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
        if self.level>=10:
            self.xpNeeded = int(10*self.level*0.2)

    def gainExperience(self, xp):
        self.experience+=xp
        if self.experience>=self.xpNeeded:
            self.experience = self.experience-self.xpNeeded
            self.levelUp()
