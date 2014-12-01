__author__ = 'Matt'

from combat.items.item import *

class inventory():
    def __init__(self):
        self.inventory = []

    #gather inventory from pickled file.
    def loadInventory(self, items):
        for item in range(items.count):
            self.inventory.addItem(item)

    def addItem(self, item):
        self.inventory.append(item)
        return "You picked up ",item.name,"! You can find it in your inventory."
        #remove item by index

    def addHealthPotion(self, price, value):
        hp = item()
        hp.name = "Health Potion"
        hp.description = "Increase hp by" + str(value) + "\n" + "Sell Value:  " + str(price)
        hp.price = price
        hp.value = value
        self.addItem(hp)

    def addManaPotion(self, price, value):
        mp = item()
        mp.name = "Mana Potion"
        mp.description = "Increases mana by" + str(value) + "\n" + "Sell Value:  " + str(price)
        mp.price = price
        mp.value = value
        self.addItem(mp)

    def removeItem(self, item):
        tempItem = ""
        for listItem in range(len(self.inventory)):
            if self.inventory[listItem].name == item:
                tempItem = self.inventory[listItem]
                self.inventory.remove(tempItem)
                break


        return tempItem.name

    #counts the number of items in an inventory e.g. 3 health potions.
    def countItems(self, item):
        count = 0
        for listItem in range(len(self.inventory)):
            if self.inventory[listItem].name == item:
                count = count + 1
        return count

    def countHealthPotions(self):
        return self.countItems("Health Potion")

    def countManaPotions(self):
        return self.countItems("Mana Potion")


