__author__ = 'Matt'
from inventory import *

class shopkeeper(npc):
    def __init__(self):
        self.inventory = inventory()
        #populates shop with 3 items at a time.
        for index in range(3):
            self.inventory.addManaPotion()
            self.inventory.addHealthPotion()

